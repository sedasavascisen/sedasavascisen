"""
Grid check at the EXACT latencies of Paper 2 Table I (verification of the revised paper, numeric audit K2).
Table I (paper_mobility/make_paper_assets.py) uses Adam-L at L*13.3/8 ms and, for SU-average, SU-best-of,
coordinate descent and long-run Adam (baselines.pga), the medians of results/mumiso_mobility_latency.json;
effective rates are interpolated on the aging grid. Here each arm is also evaluated exactly at that latency.
The interpolated values are compared with the published Table I numbers (sanity check of scenario identity).
Output: thesis_exp/p4/izgara_kontrol/raw/results_tab1.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, boot, commit, check_same_scenarios, ROOT
from ris_mu.mumiso import baselines as B
torch.set_num_threads(2)
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
ml = json.load(open(ROOT / "results/mumiso_mobility_latency.json"))["median"]
LAT = {"SU-average": ml["su_average"], "SU-best-of": ml["su_best_of"], "CD": ml["cd"], "Long-run Adam": ml["pga"],
       **{f"Adam-{L}": L * 13.3 / 8 for L in (8, 12, 16, 20)}}
PUB = {"SU-average": 4.623, "SU-best-of": 5.272, "Adam-8": 5.849, "Adam-12": 5.515, "Adam-16": 5.324, "Adam-20": 5.276,
       "CD": 4.975, "Long-run Adam": 4.667}
A = Aging(11, list(TIMES) + sorted(set(LAT.values()) - set(TIMES)))
chk = check_same_scenarios(A)
m0 = A.idx(0.0); su = A.su_average()
PH = {"SU-average": su, "SU-best-of": A.su_best_of(), "CD": B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1],
      "Long-run Adam": B.pga(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1], **{f"Adam-{L}": A.adam(su, L) for L in (8, 12, 16, 20)}}
rows = {}
for k, th in PH.items():
    c = np.stack([A.minrate(th, A.idx(t)).numpy() for t in TIMES], 1)
    I = np.array([np.interp(LAT[k], TIMES, r) for r in c]); X = A.minrate(th, A.idx(LAT[k])).numpy(); d = X - I
    rows[k] = dict(latency_ms=LAT[k], interpolated=float(I.mean()), published=PUB[k], exact=float(X.mean()),
                   exact_minus_interp=float(d.mean()), ci=boot(d))
    print(f"{k:14s} lat {LAT[k]:8.2f} interp {I.mean():.4f} (pub {PUB[k]}) exact {X.mean():.4f} diff {d.mean():+.4f}", flush=True)
res = dict(commit=commit(), su_average_t0_check=chk, rows=rows,
           max_abs_diff=max(abs(v["exact_minus_interp"]) for v in rows.values()),
           max_abs_diff_within_200ms=max(abs(v["exact_minus_interp"]) for v in rows.values() if v["latency_ms"] <= 200))
json.dump(res, open(pathlib.Path(__file__).parent / "raw/results_tab1.json", "w"), indent=1)
print("max", res["max_abs_diff"], "within 200 ms", res["max_abs_diff_within_200ms"])
