"""
Link-budget compensation for the 28 GHz set (ON_KAYIT_S5.md). With the 3 GHz link budget unchanged, the 28 GHz
min-user rate collapses (SU-average 0.05 b/s/Hz on seed 21), so the noise variance is scaled by the ratio of mean
incoherent received power P = mean_{s,k} (sum_n |g_kn|^2 ||f_n||^2 + ||h_d,k||^2) at 3 GHz and 28 GHz, computed on the
TRAINING seed 21 (n = 2000) only. Equivalent to a higher transmit power / antenna gain at 28 GHz.
-> raw/link_budget.json
"""
import json, pathlib, sys
import numpy as np
from ch28 import Aging28, Aging
import sys; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "p4")); from common import commit
def P(A):
    F, G, H = A.F, A.G[0], A.H[0]
    casc = (G.abs() ** 2 * (F.abs() ** 2).sum(-1).unsqueeze(1)).sum(-1)
    return float((casc + (H.abs() ** 2).sum(-1)).mean())
p28, p3 = P(Aging28(21, [0.0], n=2000, compensate=False)), P(Aging(21, [0.0], n=2000))
out = dict(commit=commit(), seed=21, n=2000, P3=p3, P28=p28, comp_db=float(10 * np.log10(p3 / p28)))
json.dump(out, open(pathlib.Path(__file__).parent / "raw/link_budget.json", "w"), indent=1); print(out)
