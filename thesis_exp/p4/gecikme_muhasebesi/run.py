"""
Verification U16 — how much does charging the SU-average start (0.30 ms) to the Adam-L latency change
the effective rate?

common.adam_latency(L) excludes the SU-average closed form that every Adam arm starts from (the paper's
accounting rule). Here, on the aging set (seed 11, 400 scenarios), for every Adam-L arm (continuous phase,
and rounded to 1 and 2 bits as in p4/ayrik_faz), the effective rate (Definition 1) is computed at
  lat = adam_latency(L)            (as used in every p4 report)
  lat + LAT['su_average']          (start charged)
and the paired difference is reported with a bootstrap 95% CI.
Output: thesis_exp/p4/gecikme_muhasebesi/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S
torch.set_num_threads(1)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
GRID = [float(x) for x in np.arange(0.0, 70.0 + 0.25, 0.5)]

A = Aging(11, GRID)
res = dict(commit=commit(), su_average_t0_check=check_same_scenarios(A), su_average_ms=LAT["su_average"], arms={})
su = A.su_average()
for L in STEPS:
    th = A.adam(su, L)
    for tag, ph in (("continuous", th), ("1bit", S.quantise_phase(th, 1)), ("2bit", S.quantise_phase(th, 2))):
        c = A.curve(ph, GRID)
        a = np.array([np.interp(adam_latency(L), GRID, r) for r in c])
        b = np.array([np.interp(adam_latency(L) + LAT["su_average"], GRID, r) for r in c])
        d = b - a
        res["arms"][f"Adam-{L} {tag}"] = dict(lat_ms=adam_latency(L), eff=float(a.mean()), eff_charged=float(b.mean()),
                                              diff=float(d.mean()), diff_ci=boot(d))
    print(L, {t: round(res["arms"][f"Adam-{L} {t}"]["diff"], 4) for t in ("continuous", "1bit", "2bit")}, flush=True)
ds = [v["diff"] for v in res["arms"].values()]
res["summary"] = dict(min_diff=float(min(ds)), max_diff=float(max(ds)), mean_abs_diff=float(np.mean(np.abs(ds))))
json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", res["summary"], flush=True)
