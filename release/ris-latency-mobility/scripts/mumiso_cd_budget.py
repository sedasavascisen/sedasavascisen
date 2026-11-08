"""
Coordinate descent with a tuned budget (multi-user aging set).

Why: the paper's slow solvers run at fixed budgets (coordinate descent up to
8 sweeps, long-run Adam 1000 iterations). A reviewer will ask whether the
"slow solvers lose" finding is just an untuned budget. In the single-user
study one coordinate sweep was the best method at every delay. Here we run
coordinate descent (16-level grid, max-min objective, from SU-average) with
1, 2, 3, 4 and 8 sweeps on the aging set, measure each budget's latency on an
idle machine, and compare effective rates with SU-best-of and Adam's best
step count.

Same scenarios as the aging run (seed 11, 400 scenarios, 4 users, 20
scatterers); time grid 0.5 ms up to 40 ms, coarser beyond, and the measured
latencies on it. Timing: one scenario at a time, one thread, `--reps`
repetitions, `--rounds` rounds over `--n_time` scenarios, after the 1-min
load average falls below 0.5 (recorded). SU-best-of and Adam latencies are
the stored measurements (results/mumiso_mobility_latency.json, 13.3/8 ms per
Adam step), as in the paper. Writes results/mumiso_cd_budget.json.
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
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--kmh", default="5.4,10")
ap.add_argument("--sweeps", default="1,2,3,4,8")
ap.add_argument("--n_time", type=int, default=10)
ap.add_argument("--reps", type=int, default=3)
ap.add_argument("--rounds", type=int, default=3)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
SWEEPS = [int(s) for s in a.sweeps.split(",")]
ADAM_L = [1, 2, 3, 4, 5, 6, 8]
MS_PER_STEP = 13.3 / 8
ML = json.load(open(ROOT / "results" / "mumiso_mobility_latency.json"))["median"]
TIMES = np.unique(np.r_[np.arange(0, 40.01, 0.5), np.arange(45, 201, 5), 300, 500, 1000, 1500])
v_of = lambda kmh: 1.5 if abs(kmh - 5.4) < 1e-9 else kmh / 3.6
rng = np.random.default_rng(0)


def gen(v, n=a.scenarios):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": v, "times_ms": tuple(TIMES), "n_clusters": 20})
    return panel, cfg, MobileMuMisoChannel(panel, cfg).generate(n)


def paired(x, y):
    d = x - y
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    return [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


panel, cfg, d0 = gen(1.5)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
N = panel.positions.shape[0]
F = torch.as_tensor(d0["F"], dtype=torch.complex64)
G0 = torch.as_tensor(d0["G_t"][:, 0], dtype=torch.complex64)
H0 = torch.as_tensor(d0["hd_t"][:, 0], dtype=torch.complex64)

# ---- phases on the (speed-independent) t=0 channel --------------------------
t0 = time.time()
_, TH_SU = B.su_average(F, G0, H0, pt, nv)
_, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
phases = {"su_best_of": TH_BEST}
LAT = {"su_best_of": ML["su_best_of"]}
for k in SWEEPS:
    phases[f"cd{k}"] = B.coord_descent(F, G0, H0, pt, nv, iters=k)[1]


def adam_phase(L):
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for _ in range(L):
        th = TH_SU + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step(); opt.zero_grad()
    return TH_SU + dl.detach()


for L in ADAM_L:
    phases[f"adam{L}"] = adam_phase(L)
    LAT[f"adam{L}"] = L * MS_PER_STEP
print(f"phases computed in {time.time()-t0:.0f}s", flush=True)

# ---- latency of each coordinate-descent budget (idle machine) ---------------
torch.set_num_threads(1)
t_wait = time.time()
while os.getloadavg()[0] >= 0.5:
    time.sleep(10)
load_before = os.getloadavg()[0]
print(f"timing starts at load {load_before:.2f} after waiting {time.time()-t_wait:.0f} s", flush=True)
rounds = {}
for k in SWEEPS:
    per_round = []
    for _ in range(a.rounds):
        per = []
        for i in range(a.n_time):
            sl = slice(i, i + 1)
            f1, g1, h1 = F[sl], G0[sl], H0[sl]
            B.coord_descent(f1, g1, h1, pt, nv, iters=k)          # warm-up
            ts = []
            for _ in range(a.reps):
                t1 = time.perf_counter(); B.coord_descent(f1, g1, h1, pt, nv, iters=k); ts.append(time.perf_counter() - t1)
            per.append(np.median(ts) * 1e3)
        per_round.append(float(np.median(per)))
    rounds[f"cd{k}"] = per_round
    LAT[f"cd{k}"] = float(np.median(per_round))
    print(f"  CD {k} sweep(s): {LAT[f'cd{k}']:.1f} ms (rounds {[round(x, 1) for x in per_round]})", flush=True)
load_after = os.getloadavg()[0]

# ---- effective rates at each speed --------------------------------------------
res = dict(config=vars(a), latency_ms=LAT, latency_rounds_ms=rounds,
           load_avg=dict(before_timing=load_before, after_timing=load_after), speeds={})
for kmh in [float(x) for x in a.kmh.split(",")]:
    v = v_of(kmh)
    _, _, d = gen(v)
    assert np.array_equal(d["G_t"][:, 0], d0["G_t"][:, 0])
    Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    curves = {k: np.stack([S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv, "zf").min(-1).values.numpy()
                           for m in range(len(TIMES))], 1) for k, th in phases.items()}
    E = {k: np.array([np.interp(LAT[k], TIMES, row) for row in c]) for k, c in curves.items()}
    best_cd = max((f"cd{k}" for k in SWEEPS), key=lambda k: E[k].mean())
    best_adam = max((f"adam{L}" for L in ADAM_L), key=lambda k: E[k].mean())
    blk = dict(t0={k: float(c[:, 0].mean()) for k, c in curves.items()},
               effective={k: float(e.mean()) for k, e in E.items()},
               best_cd=best_cd, best_adam=best_adam,
               su_best_minus_best_cd=paired(E["su_best_of"], E[best_cd]),
               best_adam_minus_best_cd=paired(E[best_adam], E[best_cd]),
               cd1_minus_cd8=paired(E["cd1"], E["cd8"]))
    res["speeds"][f"{kmh:g}"] = blk
    print(f"{kmh:g} km/h: " + " | ".join(f"{k} {LAT[k]:.0f}ms t0 {blk['t0'][k]:.3f} eff {blk['effective'][k]:.3f}"
                                          for k in [f'cd{s}' for s in SWEEPS]) +
          f" || SU-best {blk['effective']['su_best_of']:.3f}, best Adam {best_adam} {blk['effective'][best_adam]:.3f}; "
          f"SU-best - best CD {blk['su_best_minus_best_cd']}", flush=True)
json.dump(res, open(ROOT / "results" / "mumiso_cd_budget.json", "w"), indent=1)
print("wrote results/mumiso_cd_budget.json")
