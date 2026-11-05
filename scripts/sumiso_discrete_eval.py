"""
Discrete RIS phases (1, 2, 3 bits), single-user MISO (Task 3, single-user part).

Three approaches, as the task requires:
  continuous then round   SU-align -> round; CD-s (continuous, s sweeps) -> round
  discrete CD             exact element-wise ascent on the grid, s sweeps,
                          from rounded SU alignment (ris_mu.sumiso.solver.discrete_cd)
  learned                 (a) CNN-LSTM trained on continuous labels, rounded
                          (b) CNN-LSTM trained on discrete labels (--disc_bits)
                          (c) (b) fine-tuned straight-through on the rate
                          and (b)/(c) + one discrete CD sweep
Every network output is deployed as the better (per scenario) of: round -> best
of the 2^b grid rotations, and closed-form common phase -> round -> same.
Offline reference: the discrete label (best of discrete CD from two starts).

Axis 1, static: validation 1000 / test 6000 of the training draw's split.
Axis 2, mobility: effective rate at the measured latency on the single-user
set (seed 11), configuration selected on seed 12.
Latency: single scenario, one thread, median of 25 calls, 3 rounds, 20
scenarios; timing waits until the load average is below 0.5 and records it.
"""
import sys
import os
import json
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features_ab, restore_common_phase

ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(1)
load0 = os.getloadavg()[0]
BITS = (1, 2, 3)
S_LIST = [1, 2, 3, 5, 10]
z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
snr = float(z["snr_scale"])
perm = np.random.default_rng(0).permutation(len(z["theta"]))
iva, ite = perm[28000:29000], perm[34000:]


def cas(idx):
    return SV.cascade(torch.as_tensor(z["F"][idx]), torch.as_tensor(z["G"][idx]), torch.as_tensor(z["hd"][idx]))


def load_net(tag):
    ck = torch.load(ROOT / "results" / f"{tag}.pt")
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck.get("head", "flat"), ck.get("n_out", 2))
    net.load_state_dict(ck["state"]); net.eval()
    return net, ck["mu"], ck["sd"]


def net_phase(pack, a, B, bits):
    net, mu, sd = pack
    with torch.no_grad():
        th = torch.cat([phase(net((features_ab(a[i:i + 2000], B[i:i + 2000]) - mu) / (sd + 1e-9)))
                        for i in range(0, len(a), 2000)])
    # two deployments, the better one per scenario (known channel, so this is allowed):
    # round then best grid rotation, or closed-form common phase first, then the same
    t1 = SV.best_grid_rotation(SV.quantise(th, bits), a, B, bits)
    t2 = SV.best_grid_rotation(SV.quantise(restore_common_phase(th, a, B), bits), a, B, bits)
    return torch.where((SV.gain(t2, a, B) > SV.gain(t1, a, B))[:, None], t2, t1)


def arms(a, B, bits, nets):
    al = SV.su_align(a, B)
    alq = SV.quantise(al, bits)
    P = {"SU-align -> round": alq}
    for s in S_LIST:
        P[f"CD-{s} -> round"] = SV.quantise(SV.coord_ascent(a, B, al, sweeps=s, tol=-1)[0], bits)
        P[f"discrete CD-{s}"] = SV.discrete_cd(a, B, alq, bits, sweeps=s, tol=-1)[0]
    for k, pack in nets.items():
        th = net_phase(pack, a, B, bits)
        P[k] = th
        if k != "CNN (a) continuous labels":
            P[k + " + discrete CD-1"] = SV.discrete_cd(a, B, th, bits, sweeps=1, tol=-1)[0]
    return P


rate = lambda th, a, B: torch.log2(1 + snr * SV.gain(th, a, B))
CLASSICAL = lambda keys: [k for k in keys if not k.startswith("CNN")]

# ---- mobility draws ---------------------------------------------------------
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2, 35.0, 42.9, 50.0, 75.0, 100.0)


def mob(seed, n=400):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(n)
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    return [SV.cascade(F, torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64),
                       torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64)) for m in range(len(TIMES))]


MOB = {"val": mob(12), "test": mob(11)}
res = dict(levels={})
pre = {}
for b in BITS:
    nets = {"CNN (a) continuous labels": load_net("sumiso_cnnlstm_seq"),
            "CNN (b) discrete labels": load_net(f"sumiso_cnnlstm_seq_disc{b}"),
            "CNN (c) straight-through": load_net(f"sumiso_cnnlstm_seq_ste{b}")}
    pre[b] = nets
    Av, Bv = cas(iva); At, Bt = cas(ite)
    val = {k: float(rate(t, Av, Bv).mean()) for k, t in arms(Av, Bv, b, nets).items()}
    rt = {k: rate(t, At, Bt).numpy() for k, t in arms(At, Bt, b, nets).items()}
    lab = torch.as_tensor(np.load(ROOT / "data_sumiso" / f"sumiso_train_disc{b}.npz")["theta"][ite]).float()
    best_cl = max(CLASSICAL(val), key=val.get)
    res["levels"][str(b)] = dict(static=dict(val=val, test={k: float(v.mean()) for k, v in rt.items()},
                                             classical_selected_on_val=best_cl,
                                             offline_discrete_optimum=float(rate(lab, At, Bt).mean()),
                                             continuous_optimum=float(rate(torch.as_tensor(z["theta"][ite]).float(), At, Bt).mean())))
    print(f"{b} bit static: best classical {best_cl} {rt[best_cl].mean():.4f}; "
          + "; ".join(f"{k} {v.mean():.4f}" for k, v in rt.items() if k.startswith("CNN")), flush=True)


# ---- latency (idle machine) --------------------------------------------------
def timeit(fn, A0, B0, rounds=3, reps=25, n=20):
    out = []
    for _ in range(rounds):
        per = []
        for i in range(n):
            a1, b1 = A0[i:i + 1], B0[i:i + 1]
            fn(a1, b1)
            t = []
            for _ in range(reps):
                t0 = time.perf_counter(); fn(a1, b1); t.append(time.perf_counter() - t0)
            per.append(np.median(t) * 1e3)
        out.append(float(np.median(per)))
    return out


A0t, B0t = MOB["test"][0]
t_wait = time.time()
while os.getloadavg()[0] >= 0.5:              # CLAUDE.md: never time under load
    time.sleep(10)
load1 = os.getloadavg()[0]
print(f"timing starts at load {load1:.2f} after waiting {time.time()-t_wait:.0f} s", flush=True)
lat_rounds = {}
for b in BITS:
    nets = pre[b]
    fns = {"SU-align -> round": lambda a_, B_: SV.quantise(SV.su_align(a_, B_), b)}
    for s in S_LIST:
        fns[f"CD-{s} -> round"] = (lambda s: lambda a_, B_: SV.quantise(SV.coord_ascent(a_, B_, SV.su_align(a_, B_), sweeps=s, tol=-1)[0], b))(s)
        fns[f"discrete CD-{s}"] = (lambda s: lambda a_, B_: SV.discrete_cd(a_, B_, SV.quantise(SV.su_align(a_, B_), b), b, sweeps=s, tol=-1))(s)
    fns["CNN (deployed, any training)"] = lambda a_, B_: net_phase(nets["CNN (b) discrete labels"], a_, B_, b)
    fns["CNN + discrete CD-1"] = lambda a_, B_: SV.discrete_cd(a_, B_, net_phase(nets["CNN (b) discrete labels"], a_, B_, b), b, sweeps=1, tol=-1)
    lat_rounds[str(b)] = {k: timeit(f, A0t, B0t) for k, f in fns.items()}
load2 = os.getloadavg()[0]
res["load_avg"] = dict(start=load0, before_timing=load1, after_timing=load2)
res["latency_rounds_ms"] = lat_rounds


def lat_of(b, k):
    L = {kk: float(np.median(v)) for kk, v in lat_rounds[str(b)].items()}
    if k.startswith("CNN"):
        return L["CNN + discrete CD-1"] if k.endswith("discrete CD-1") else L["CNN (deployed, any training)"]
    return L[k]


# ---- mobility effective rate -------------------------------------------------
rng = np.random.default_rng(0)
for b in BITS:
    nets = pre[b]
    effs = {}
    for part in ("val", "test"):
        C = MOB[part]
        P = arms(*C[0], b, nets)
        effs[part] = {}
        for k, th in P.items():
            curve = np.stack([rate(th, A, B).numpy() for A, B in C], 1)
            effs[part][k] = np.array([np.interp(lat_of(b, k), TIMES, row) for row in curve])
    best_m = max(CLASSICAL(effs["val"]), key=lambda k: effs["val"][k].mean())
    te = effs["test"]
    mres = dict(test={k: float(v.mean()) for k, v in te.items()}, classical_selected_on_val=best_m,
                latency_ms={k: lat_of(b, k) for k in te})
    for k in te:
        if k.startswith("CNN"):
            diff = te[k] - te[best_m]
            bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
            mres[f"diff_to_classical[{k}]"] = [float(diff.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
            mres[f"dominated_by[{k}]"] = [c for c in CLASSICAL(te) if lat_of(b, c) < lat_of(b, k) and te[c].mean() > te[k].mean()]
    res["levels"][str(b)]["mobility"] = mres
    print(f"{b} bit mobility: best classical {best_m} {te[best_m].mean():.4f} ({lat_of(b, best_m):.2f} ms); "
          + "; ".join(f"{k} {v.mean():.4f}" for k, v in te.items() if k.startswith("CNN")), flush=True)
json.dump(res, open(ROOT / "results" / "sumiso_discrete_eval.json", "w"), indent=1)
print(f"load {load0:.2f} / {load1:.2f} / {load2:.2f}")
