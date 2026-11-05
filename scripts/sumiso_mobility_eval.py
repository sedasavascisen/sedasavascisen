"""
Effective rate of the published phase-aware CNN-LSTM in the mobility
scenario (single user), against tuned classical arms with measured latency.

Evaluation set: the aging set's construction with one user (seed 11, 400
scenarios, 20 scatterers, 1.5 m/s, the aging sweep's time grid). The network
was trained on 40 000 static snapshots drawn with seed 2026, i.e. on other
scenarios of the same generator. Each method computes its phase from the t=0
channel; its effective rate is the rate of that phase on the channel at its
own latency (+ T_ov), linearly interpolated on the time grid. The BS beam is
maximum-ratio on the current channel (the SU analogue of a recomputed
precoder), so rate = log2(1 + snr |a_t + B_t^T v|^2).

Arms
  SU-align        closed form, every b_n aligned to the direct link
  CD-s            exact element-wise coordinate ascent, s sweeps from SU-align
  Adam-L          Adam on -rate, L steps from SU-align; step size chosen on a
                  validation draw (seed 2026 training file, its val split)
  CNN-LSTM        one forward pass + closed-form common phase
  CNN-LSTM+CD-s   network output refined by s sweeps
Latency: one scenario at a time, one thread, median of `--reps` calls, in
several rounds; feature construction is included in the network's time.
Timing waits until the load average is below --idle (default 0.5) and records it.
The best arm per T_ov is selected on a second draw (seed 12) and reported on seed 11.
"""
import sys
import os
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features, restore_common_phase

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=400)
ap.add_argument("--ckpt", default="sumiso_cnnlstm_seq")
ap.add_argument("--reps", type=int, default=25)
ap.add_argument("--rounds", type=int, default=3)
ap.add_argument("--n_time", type=int, default=20, help="scenarios used for timing")
ap.add_argument("--tov", type=float, nargs="*", default=[0.0, 1.71, 3.43, 10.0])
ap.add_argument("--tag", default="sumiso_mobility_eval")
ap.add_argument("--idle", type=float, default=0.5, help="timing starts only once the 1-min load average is below this")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(1)
load0 = os.getloadavg()[0]

TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
def draw(seed):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(a.n)
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    cas = [SV.cascade(F, torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64),
                      torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64)) for m in range(len(TIMES))]
    return cfg.snr_scale(), F, torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64), \
        torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64), cas


snr, F, G0, H0, cas = draw(11)          # reported (the paper's single-user set)
_, Fv, G0v, H0v, cas_v = draw(12)       # selection of the best arm per T_ov
A0, B0 = cas[0]


def curve(th, cas=cas):
    """[S, len(TIMES)] rate of a fixed phase over time."""
    return torch.stack([torch.log2(1 + SV.gain(th, A, B) * snr) for A, B in cas], 1).numpy()


def adam(A, B, th0, L, lr):
    th = th0.clone().requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr)
    for _ in range(L):
        loss = -torch.log2(1 + SV.gain(th, A, B) * snr).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return th.detach()


# ---- network ---------------------------------------------------------------
ck = torch.load(ROOT / "results" / f"{a.ckpt}.pt")
net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck.get("head", "flat"), ck.get("n_out", 2))
net.load_state_dict(ck["state"])
net.eval()
kind = json.load(open(ROOT / "results" / f"{a.ckpt}.json"))["config"]["features"]
mu, sd = ck["mu"], ck["sd"]


def cnn(Fx, Gx, Hx, A, B):
    with torch.no_grad():
        x = (features(Fx, Gx, Hx, kind) - mu) / (sd + 1e-9)
        return restore_common_phase(phase(net(x)), A, B)


# ---- Adam step size on a validation draw (not the evaluation scenarios) ---
z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
vidx = np.random.default_rng(0).permutation(len(z["theta"]))[28000:28400]
Av, Bv = SV.cascade(torch.as_tensor(z["F"][vidx]), torch.as_tensor(z["G"][vidx]), torch.as_tensor(z["hd"][vidx]))
LRS = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
ADAM_L = [1, 2, 4, 8, 16, 32, 64]
lr_of = {}
for L in ADAM_L:
    v = {lr: float(SV.gain(adam(Av, Bv, SV.su_align(Av, Bv), L, lr), Av, Bv).log().mean()) for lr in LRS}
    lr_of[L] = max(v, key=v.get)
print("Adam step size per L (validation):", lr_of, flush=True)

# ---- phases on all evaluation scenarios -----------------------------------
CD_S = [1, 2, 3, 5, 10]
def all_arms(F, G0, H0, A0, B0):
    th_al = SV.su_align(A0, B0)
    arms = {"SU-align": th_al}
    for s in CD_S:
        arms[f"CD-{s}"] = SV.coord_ascent(A0, B0, th_al, sweeps=s, tol=-1)[0]
    for L in ADAM_L:
        arms[f"Adam-{L}"] = adam(A0, B0, th_al, L, lr_of[L])
    th_n = cnn(F, G0, H0, A0, B0)
    arms["CNN-LSTM"] = th_n
    for s in (1, 2):
        arms[f"CNN-LSTM+CD-{s}"] = SV.coord_ascent(A0, B0, th_n, sweeps=s, tol=-1)[0]
    arms["CD-converged (offline)"] = SV.solve(A0, B0)[0]
    return arms


arms = all_arms(F, G0, H0, A0, B0)
curves_v = {k: curve(v, cas_v) for k, v in all_arms(Fv, G0v, H0v, *cas_v[0]).items()}
curves = {k: curve(v) for k, v in arms.items()}

# ---- latency ----------------------------------------------------------------
def timeit(fn):
    out = []
    for r in range(a.rounds):
        per = []
        for i in range(a.n_time):
            sl = slice(i, i + 1)
            args = (F[sl], G0[sl], H0[sl], A0[sl], B0[sl])
            fn(*args)
            t = []
            for _ in range(a.reps):
                t0 = time.perf_counter()
                fn(*args)
                t.append(time.perf_counter() - t0)
            per.append(np.median(t) * 1e3)
        out.append(float(np.median(per)))
    return out


def cd_fn(s, start):
    def f(Fx, Gx, Hx, A, B):
        th0 = SV.su_align(A, B) if start == "align" else cnn(Fx, Gx, Hx, A, B)
        return SV.coord_ascent(A, B, th0, sweeps=s, tol=-1)
    return f


fns = {"SU-align": lambda Fx, Gx, Hx, A, B: SV.su_align(A, B),
       "CNN-LSTM": cnn}
for s in CD_S:
    fns[f"CD-{s}"] = cd_fn(s, "align")
for s in (1, 2):
    fns[f"CNN-LSTM+CD-{s}"] = cd_fn(s, "cnn")
for L in ADAM_L:
    fns[f"Adam-{L}"] = (lambda L: lambda Fx, Gx, Hx, A, B: adam(A, B, SV.su_align(A, B), L, lr_of[L]))(L)
t_wait = time.time()
while os.getloadavg()[0] >= a.idle:          # CLAUDE.md: never time under load
    time.sleep(10)
load1 = os.getloadavg()[0]
print(f"timing starts at load {load1:.2f} after waiting {time.time()-t_wait:.0f} s", flush=True)
lat_rounds = {k: timeit(f) for k, f in fns.items()}
load2 = os.getloadavg()[0]
lat = {k: float(np.median(v)) for k, v in lat_rounds.items()}
lat["CD-converged (offline)"] = None


def eff(k, tov, curves=curves):
    c = curves[k]
    t = (lat[k] if lat[k] is not None else 0.0) + tov
    return np.array([np.interp(t, TIMES, row) for row in c])


rows = {}
rng = np.random.default_rng(0)


def paired(x, y):
    diff = x - y
    bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
    return [float(diff.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


for tov in a.tov:
    timed = [k for k in arms if lat[k] is not None]
    best = max(timed, key=lambda k: eff(k, tov, curves_v).mean())      # selected on seed 12
    eb = eff(best, tov)
    rows[str(tov)] = {}
    for k in arms:
        e = eff(k, tov)
        d_ = paired(e, eb)
        rows[str(tov)][k] = dict(effective=float(e.mean()), diff_to_best=d_[0], ci95=d_[1:])
    rows[str(tov)]["_best"] = best
    rows[str(tov)]["_best_on_test"] = max(timed, key=lambda k: eff(k, tov).mean())
    for k in ("CNN-LSTM", "CNN-LSTM+CD-1"):
        rows[str(tov)][f"_dominated_by[{k}]"] = [c for c in timed if not c.startswith("CNN")
                                                 and lat[c] < lat[k] and eff(c, tov).mean() > eff(k, tov).mean()]
t0 = {k: curves[k][:, 0] for k in arms}
pairs_t0 = {"CNN-LSTM - SU-align": paired(t0["CNN-LSTM"], t0["SU-align"]),
            "CNN-LSTM - Adam-1": paired(t0["CNN-LSTM"], t0["Adam-1"]),
            "CNN-LSTM+CD-1 - CD-1": paired(t0["CNN-LSTM+CD-1"], t0["CD-1"])}

res = dict(config=vars(a), times_ms=TIMES, adam_lr=lr_of, load_avg=dict(start=load0, before_timing=load1, after_timing=load2),
           latency_ms=lat, latency_rounds_ms=lat_rounds,
           rate_t0={k: float(c[:, 0].mean()) for k, c in curves.items()},
           curve_mean={k: c.mean(0).tolist() for k, c in curves.items()},
           effective=rows, paired_t0=pairs_t0, selection_seed=12)
json.dump(res, open(ROOT / "results" / f"{a.tag}.json", "w"), indent=1)
print(f"load {load0:.2f} / {load1:.2f} / {load2:.2f}")
print(f"{'arm':26s} {'lat ms':>8s} {'R(t=0)':>8s} " + " ".join(f"Tov={t:<5}" for t in a.tov))
for k in arms:
    l = "   -   " if lat[k] is None else f"{lat[k]:8.3f}"
    print(f"{k:26s} {l} {res['rate_t0'][k]:8.4f} " + " ".join(f"{rows[str(t)][k]['effective']:9.4f}" for t in a.tov))
for t in a.tov:
    print("best at Tov", t, rows[str(t)]["_best"], "(selected on seed 12; best on test:", rows[str(t)]["_best_on_test"], ")",
          "| CNN dominated by", rows[str(t)]["_dominated_by[CNN-LSTM]"][:3])
print("paired at t=0:", pairs_t0)
