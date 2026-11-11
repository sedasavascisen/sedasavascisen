"""
How robust is the intrinsic optimum? Two questions a reviewer will ask.

1. CHANNEL-ACQUISITION DELAY. The effective rate in the paper charges each
   method only for its own run time. A real system also spends time on
   pilots, estimation and feedback before the optimiser starts. Here every
   latency gets an extra offset T_ov, and we see where the optimum moves.

2. USER SPEED, AND GETTING IT WRONG. The optimum depends on how fast the
   channel changes. We repeat the sweep at several speeds, and price a
   mismatch: choose L at the speed you assumed, pay at the speed you got.

Same setup as `mumiso_aging.py` / `mumiso_aging_sweep.py` (seeds, 20 clusters,
time grid, linear interpolation, 13.3 ms / 8 per Adam step). At v = 1.5 m/s
and T_ov = 0 the rows must equal `results/mumiso_aging_sweep_repro.json`.
The time grid is coarse between samples, so at high speed the interpolated
effective rate is only approximate; the grid is kept so the baseline still
reproduces.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--velocities", default="1.0,1.5,1.8,3.0")
ap.add_argument("--overheads", default="0,1,2,5,10")
ap.add_argument("--steps", default="1,2,3,4,5,6,8,10,12,16,20,24,32,48")
ap.add_argument("--clusters", type=int, default=20)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--tag", default="aging_sensitivity")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[3] / "thesis_exp" / "infra" / "raw"

TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
MS_PER_STEP = 13.3 / 8
SU_BEST_MS = 0.05
STEPS = [int(s) for s in a.steps.split(",")]
OVS = [float(x) for x in a.overheads.split(",")]


def curves_at(v):
    """t=0 rate and full aging curve for SU-best-of (L=0) and Adam-L."""
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": v,
                          "times_ms": TIMES, "n_clusters": a.clusters})
    d = MobileMuMisoChannel(panel, cfg).generate(a.scenarios)
    N = panel.positions.shape[0]
    pt, nv = 1.0, 1.0 / cfg.snr_scale()
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    G0, H0 = Gt[0], Ht[0]

    def curve(th):
        return [S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                        "zf").min(-1).values.mean().item() for m in range(len(TIMES))]

    def adam_phase(L, start):
        dl = torch.zeros(a.scenarios, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=a.lr)
        for _ in range(L):
            th = start + dl
            R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        return start + dl.detach()

    _, TH_SU = B.su_average(F, G0, H0, pt, nv)
    _, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
    out = {0: (SU_BEST_MS, curve(TH_BEST))}
    for L in STEPS:
        out[L] = (L * MS_PER_STEP, curve(adam_phase(L, TH_SU)))
    return out


res = {"config": vars(a), "by_velocity": {}}
for v in [float(x) for x in a.velocities.split(",")]:
    cv = curves_at(v)
    tc = 0.423 / (v * 3e9 / 3e8) * 1e3
    block = {"coherence_ms": tc, "by_overhead": {}}
    for ov in OVS:
        rows = [dict(L=L, latency_ms=lat + ov, t0=c[0],
                     effective=float(np.interp(lat + ov, TIMES, c)))
                for L, (lat, c) in cv.items()]
        best = max(rows, key=lambda r: r["effective"])
        block["by_overhead"][str(ov)] = dict(rows=rows, best_L=best["L"],
                                             best_eff=best["effective"])
        print(f"v={v:4.2f} m/s (T_c={tc:5.1f} ms)  T_ov={ov:5.1f} ms  ->  "
              f"best L={best['L']:2d}  eff {best['effective']:.4f}   "
              + " ".join(f"{r['L']}:{r['effective']:.3f}" for r in rows))
    res["by_velocity"][str(v)] = block

# mismatch: L chosen for the assumed speed, paid at the true speed (T_ov = 0)
vs = list(res["by_velocity"])
mm = {}
print("\nmismatch at T_ov = 0: rows = assumed speed, cols = true speed, "
      "entry = loss vs. the true speed's own optimum")
for va in vs:
    La = res["by_velocity"][va]["by_overhead"]["0.0"]["best_L"]
    mm[va] = {}
    line = f"assumed {va:>4} (L={La:2d}): "
    for vt in vs:
        b = res["by_velocity"][vt]["by_overhead"]["0.0"]
        got = next(r["effective"] for r in b["rows"] if r["L"] == La)
        loss = 1 - got / b["best_eff"]
        mm[va][vt] = dict(L=La, effective=got, loss=loss)
        line += f" {vt}:{loss:6.2%}"
    print(line)
res["mismatch"] = mm

json.dump(res, open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
print(f"wrote results/mumiso_{a.tag}.json")
