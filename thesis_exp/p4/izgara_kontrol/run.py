"""
Grid check for Paper 2 (verification K3 follow-up): the paper's aging sweep (scripts/mumiso_aging_sweep.py) and
aging comparison (scripts/mumiso_aging.py) evaluate the effective rate (Definition 1) by LINEAR INTERPOLATION
on an irregular time grid (gaps up to 6.6 ms below 50 ms, 25 ms at 50-75, 1000 ms at 500-1500, 4100 ms at
1500-5600). Here every arm is evaluated EXACTLY at its latency and compared with the interpolated value.

Setup identical to scripts/mumiso_aging_sweep.py: seed 11, 400 scenarios, 20 clusters, 1.5 m/s, ZF, min-user
rate, SU-average + Adam-L (lr 0.5, soft-min beta 8), SU-best-of, CD and PGA (baselines defaults, as
scripts/mumiso_aging.py). Scenario identity: t = 0 first (common.py), checked against
results/mumiso_aging_fixzf.json, and the interpolated sweep values are compared with
results/mumiso_aging_sweep_repro.json (read only).
Two latency sets:
  paper   L * 13.3/8 ms, SU-best-of 0.05 ms, CD 1500 ms, PGA 5600 ms (as in the scripts)
  rerun   one-thread rerun (thesis_exp/infra): adam_latency(L), SU-best-of 1.63 ms, CD 702.97, PGA 4950.35
Paired bootstrap (2000, 95%) on the per-scenario exact-minus-interpolated difference and on the comparisons
the paper reports (SU-best-of - CD, SU-best-of - Adam-48, SU-best-of - Adam-20).
Output: thesis_exp/p4/izgara_kontrol/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, adam_latency, LAT, boot, commit, check_same_scenarios, ROOT
from ris_mu.mumiso import baselines as B
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
STEPS = [1, 2, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
LATS = {"paper": {"SU-best-of": 0.05, "CD": 1500.0, "PGA": 5600.0, **{f"Adam-{L}": L * 13.3 / 8 for L in STEPS}},
        "rerun": {"SU-best-of": LAT["su_best_of"], "CD": LAT["cd"], "PGA": LAT["pga"], **{f"Adam-{L}": adam_latency(L) for L in STEPS}}}
extra = sorted({v for s in LATS.values() for v in s.values()} - set(TIMES))
A = Aging(11, list(TIMES) + extra)
chk = check_same_scenarios(A)
m0 = A.idx(0.0); su = A.su_average()
PH = {"SU-best-of": A.su_best_of(), "CD": B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1],
      "PGA": B.pga(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1], **{f"Adam-{L}": A.adam(su, L) for L in STEPS}}
print("phases done", flush=True)
grid_curve = {k: np.stack([A.minrate(th, A.idx(t)).numpy() for t in TIMES], 1) for k, th in PH.items()}   # [S, len(TIMES)]
res = dict(commit=commit(), su_average_t0_check=chk, times_ms=list(TIMES), sets={})
# reproduction check against the published sweep file (mean curve interpolated at the paper latencies)
pub = json.load(open(ROOT / "results/mumiso_aging_sweep_repro.json"))
repro = []
for row in pub:
    k = "SU-best-of" if row["L"] == 0 else f"Adam-{row['L']}"
    if k in grid_curve:
        mine = float(np.interp(row["latency_ms"], TIMES, grid_curve[k].mean(0)))
        repro.append(dict(arm=k, published=row["effective"], mine=mine, abs_diff=abs(mine - row["effective"])))
res["published_sweep_check"] = repro
print("max |published - mine|:", max(r["abs_diff"] for r in repro), flush=True)
for sname, lat in LATS.items():
    rows, X, I = {}, {}, {}
    for k, th in PH.items():
        I[k] = np.array([np.interp(lat[k], TIMES, r) for r in grid_curve[k]])
        X[k] = A.minrate(th, A.idx(lat[k])).numpy()
        d = X[k] - I[k]
        rows[k] = dict(latency_ms=lat[k], interpolated=float(I[k].mean()), exact=float(X[k].mean()),
                       exact_minus_interp=float(d.mean()), ci=boot(d))
    adams = [k for k in PH if k.startswith("Adam")]
    Ls = {how: max(adams, key=lambda k: V[k].mean()) for how, V in (("interpolated", I), ("exact", X))}
    loss = {how: float(100 * (1 - V["Adam-48"].mean() / V[Ls[how]].mean())) for how, V in (("interpolated", I), ("exact", X))}
    comps = {}
    for a_, b_ in (("SU-best-of", "CD"), ("SU-best-of", "Adam-48"), ("SU-best-of", "Adam-20")):
        comps[f"{a_} - {b_}"] = {how: dict(diff=float((V[a_] - V[b_]).mean()), ci=boot(V[a_] - V[b_])) for how, V in (("interpolated", I), ("exact", X))}
    res["sets"][sname] = dict(rows=rows, L_star=Ls, loss_L48_pct=loss, comparisons=comps)
    print(sname, "L*", Ls, "L48 loss", {k: round(v, 2) for k, v in loss.items()}, flush=True)
    for k in ("SU-best-of", "Adam-6", "Adam-20", "Adam-48", "CD", "PGA"):
        r = rows[k]; print(f"  {k}: lat {r['latency_ms']:.2f} interp {r['interpolated']:.4f} exact {r['exact']:.4f} diff {r['exact_minus_interp']:+.4f}", flush=True)
json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", flush=True)
