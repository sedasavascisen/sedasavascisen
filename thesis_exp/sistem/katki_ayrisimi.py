"""
Decomposition of the controller's gain into its design decisions, on the SEALED test draw (seed 41; calibration 12),
from the stored cubes (no new channels). Reported as absolute differences (b/s/Hz, paired bootstrap 2000) and as a
percentage of the comparison's mean. Ladder (fresh mode, 12 conditions):
  K4      closed-form L, SU-average start            (the paper's rule, as in PROTOKOL)
  K4b     closed-form L, SU-best-of start            (+ start choice)
  FIX     best single fixed pipeline chosen on seed 12 (best+3)   (strongest fixed setting)
  SYS     v1b controller                              (+ per-condition step choice)
Periodic mode (P = 20 ms): K4w (closed form from the previous phase) vs V4; fresh-only v1b vs V4 (warm-start value).
-> katki_ayrisimi.json, printed table
"""
import json, pathlib
import numpy as np
import controllers as C
import periodic as Pm
from common import boot
H = pathlib.Path(__file__).resolve().parent
vec = lambda m, z, picks: np.mean([z[f"{c}_eff{W}"][m["arms"].index(picks[f"{c}|W{W}"])] for c in m["cond"] for W in C.WS], 0)


def picks_of(fn, m, cal):
    return {f"{c}|W{W}": fn(m, cal, c, W) for c in m["cond"] for W in C.WS}


out = {}
# ---- fresh mode
cal = C.load(12); m, z = C.load(41); m12, z12 = cal
k4 = picks_of(C.k4, m, cal)
k4b = {k: v.replace("avg", "best") for k, v in k4.items()}
fix_arm = max(m12["arms"], key=lambda a: np.mean([z12[f"{c}_eff{W}"][m12["arms"].index(a)].mean() for c in m12["cond"] for W in C.WS]))
fix = {k: fix_arm for k in k4}
sysp = picks_of(C.v1b_carrier, m, cal)
X = {n: vec(m, z, p) for n, p in (("K4", k4), ("K4b", k4b), ("FIX", fix), ("SYS", sysp))}
rows = []
for a, b, what in (("K4b", "K4", "başlangıç seçimi (SU-average → SU-best-of)"), ("SYS", "K4b", "koşula göre adım sayısı (kapalı form → denetleyici)"),
                   ("SYS", "FIX", "denetleyici − en iyi sabit hat"), ("SYS", "K4", "toplam: denetleyici − kapalı form")):
    d = X[a] - X[b]
    rows.append(dict(step=what, a=a, b=b, diff=float(d.mean()), ci=boot(d), pct=float(100 * d.mean() / X[b].mean())))
out["fresh"] = dict(means={k: float(v.mean()) for k, v in X.items()}, fixed_arm=fix_arm, rows=rows)
# ---- periodic mode
calw = Pm.load("", 12); mw, zw = Pm.load("", 41)
k4w = {k: v.replace("avg", "warm") for k, v in picks_of(C.k4, mw, calw).items()}
Y = {"K4w": vec(mw, zw, k4w), "V4": vec(mw, zw, picks_of(Pm.V4, mw, calw)), "FRESH": vec(mw, zw, picks_of(Pm.V1B_FRESH, mw, calw))}
prow = []
for a, b, what in (("V4", "FRESH", "sıcak başlangıcın değeri (aynı denetleyici)"), ("V4", "K4w", "denetleyici − sıcak başlangıçlı kapalı form")):
    d = Y[a] - Y[b]
    prow.append(dict(step=what, a=a, b=b, diff=float(d.mean()), ci=boot(d), pct=float(100 * d.mean() / Y[b].mean())))
out["periodic"] = dict(means={k: float(v.mean()) for k, v in Y.items()}, rows=prow)
json.dump(out, open(H / "katki_ayrisimi.json", "w"), indent=1)
for mode in ("fresh", "periodic"):
    print(mode, {k: round(v, 4) for k, v in out[mode]["means"].items()}, out[mode].get("fixed_arm", ""))
    for r in out[mode]["rows"]:
        print(f"  {r['step']}: {r['diff']:+.4f} [{r['ci'][0]:+.3f}, {r['ci'][1]:+.3f}]  ({r['pct']:+.2f} %)")
