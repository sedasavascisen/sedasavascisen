"""
One timing protocol for every method in the mobility tables.

The latencies the aging scripts use (`LAT` in mumiso_aging.py) came from
different runs: Adam from a two-thread, pre-precoder-fix run of
mumiso_budget_fraction.py, CD/PGA from mumiso_frontier.py (2-3 reps, no load
check), and the 0.03 / 0.05 ms of the single-user heuristics from a timing
that only sliced an already computed phase. This script re-times all of
them the same way, on one machine:

  * the mobility scenario (seed 11, 20 clusters, T=8, K=4), one scenario
  * one torch thread, time.perf_counter, median of `reps`, a few warm-ups
  * five rounds; the median over rounds is reported, the spread is kept
  * load average and CPU model recorded before and after

Adam is timed from a precomputed SU-average start, as in the latency
parity/repeat scripts; the start (SU-average) is timed separately. "PGA" is
`baselines.pga`: Adam, step 0.05, 1000 iterations, best of 3 random starts,
hard-min objective. CD is `baselines.coord_descent`: 16-level grid, up to 8
sweeps.
"""
import sys
import time
import json
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--rounds", type=int, default=5)
ap.add_argument("--adam-steps", default="1,2,4,8,16,32,48")
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--tag", default="mobility_latency")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[3] / "thesis_exp" / "infra" / "raw"


def load():
    return float(open("/proc/loadavg").read().split()[0])


cpu = next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo")
            if l.startswith("model name")), "unknown")
torch.set_num_threads(1)
load0 = load()

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,),
                      "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(16)
N = panel.positions.shape[0]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
one = slice(0, 1)
F = torch.as_tensor(d["F"], dtype=torch.complex64)[one]
G = torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64)[one]
H = torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64)[one]
_, TH0 = B.su_average(F, G, H, pt, nv)


def med_ms(fn, reps, warm):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


def adam(L):
    def run():
        dl = torch.zeros(1, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=a.lr)
        for _ in range(L):
            th = TH0 + dl
            R = S.rates(F, G, H, torch.cos(th), torch.sin(th), pt, nv, "zf")
            loss = -(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
    return run


jobs = {"su_average": (lambda: B.su_average(F, G, H, pt, nv), 200, 20),
        "su_best_of": (lambda: B.su_best_of(F, G, H, pt, nv), 200, 20)}
for L in map(int, a.adam_steps.split(",")):
    jobs[f"adam{L}"] = (adam(L), 25, 3)
jobs["cd"] = (lambda: B.coord_descent(F, G, H, pt, nv), 3, 1)
jobs["pga"] = (lambda: B.pga(F, G, H, pt, nv), 2, 0)

rounds = {k: [] for k in jobs}
loads = []
for r in range(a.rounds):
    loads.append(load())
    for k, (fn, reps, warm) in jobs.items():
        rounds[k].append(med_ms(fn, reps, warm))
    print(f"round {r+1}/{a.rounds}: " + "  ".join(
        f"{k} {rounds[k][-1]:.2f}" for k in jobs), flush=True)
load1 = load()

med = {k: float(np.median(v)) for k, v in rounds.items()}
steps = [int(s) for s in a.adam_steps.split(",")]
per_step = {L: med[f"adam{L}"] / L for L in steps}
slope = float(np.polyfit(steps, [med[f"adam{L}"] for L in steps], 1)[0])
print(f"\nCPU {cpu}; load {load0:.2f} -> {load1:.2f} (per round {loads})")
for k in jobs:
    v = rounds[k]
    print(f"{k:>11} median {med[k]:10.3f} ms   spread {max(v)/min(v):.2f}x")
print("per step: " + ", ".join(f"L{L}:{v:.2f}" for L, v in per_step.items())
      + f";  least-squares slope {slope:.3f} ms/step")
json.dump(dict(cpu=cpu, threads=1, load_before=load0, load_after=load1,
               load_per_round=loads, rounds=rounds, median=med,
               per_step=per_step, slope_ms_per_step=slope, config=vars(a)),
          open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
print(f"wrote results/mumiso_{a.tag}.json")
