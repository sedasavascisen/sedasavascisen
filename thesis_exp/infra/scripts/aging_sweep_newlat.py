"""
Effective rate against Adam step count: the intrinsic optimum.

`results/mumiso_aging_sweep_fixzf.json` carried the thesis's "L = 4 -> 5.982,
designing for convergence (L = 48) costs 14%" and had no script that wrote
it. This one does, on exactly the setup of `mumiso_aging.py` (same seeds,
same 20-cluster mobile channel, same time grid, same interpolation), so its
L = 8 row must equal that script's `adam8` effective rate bit for bit.

Latency is NOT re-measured per L. It is scaled linearly from the idle-box
Adam-8 figure that `mumiso_aging.py` uses (13.3 ms / 8 steps). L = 0 is
`su_best_of` at its own 0.05 ms, as in the original sweep.
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
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--clusters", type=int, default=20)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--steps", default="2,4,6,8,10,12,16,20,24,32,48")
ap.add_argument("--tag", default="aging_sweep_newlat")
ap.add_argument("--latency_json", default="thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json",
                help="per-L Adam latency (median ms) measured with one thread; L between measured points "
                     "is linearly interpolated; su_best_of uses its own measured median")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[3] / "thesis_exp" / "infra" / "raw"

TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
MS_PER_STEP = 13.3 / 8                     # the paper's value (old two-thread Adam-8 / 8), kept for comparison
_LJ = json.load(open(pathlib.Path(__file__).resolve().parents[3] / a.latency_json))
_ML = {int(k[4:]): v for k, v in _LJ["median"].items() if k.startswith("adam")}
_LS = sorted(_ML)
def new_latency(L):
    return float(np.interp(L, _LS, [_ML[x] for x in _LS]))
SU_BEST_MS = _LJ["median"]["su_best_of"]

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": a.velocity,
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

rows = []
c = curve(TH_BEST)
rows.append(dict(L=0, latency_ms=SU_BEST_MS, t0=c[0], effective=float(np.interp(SU_BEST_MS, TIMES, c)),
                 latency_ms_paper=0.05, effective_paper=float(np.interp(0.05, TIMES, c))))
for L in map(int, a.steps.split(",")):
    c = curve(adam_phase(L, TH_SU))
    lat = new_latency(L)
    rows.append(dict(L=L, latency_ms=lat, t0=c[0], effective=float(np.interp(lat, TIMES, c)),
                     latency_ms_paper=L * MS_PER_STEP, effective_paper=float(np.interp(L * MS_PER_STEP, TIMES, c))))

print(f"{'L':>4}{'latency':>10}{'t=0':>9}{'effective':>11}")
for r in rows:
    print(f"{r['L']:>4}{r['latency_ms']:10.2f}{r['t0']:9.4f}{r['effective']:11.4f}")
best = max(rows, key=lambda r: r["effective"])
last = rows[-1]
print(f"\nbest L = {best['L']} -> {best['effective']:.4f};  "
      f"L = {last['L']} -> {last['effective']:.4f}  "
      f"({1 - last['effective'] / best['effective']:.1%} below the best)")

json.dump(rows, open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
print(f"wrote results/mumiso_{a.tag}.json")
