"""Round 3 (idea 7): conservative Doppler bias. The controller uses f_d * b; b is chosen on seed 12 (in-sample,
calibration seed) from {1.0, 1.1, 1.25, 1.5, 2.0}, then evaluated on dev seed 14. Also: the same under a true
estimation error (controller sees f_d * s * b, s in {0.5, 0.8, 1.25, 2.0}). -> round3_bias.json"""
import copy, json, numpy as np
import controllers as C
from common import boot
cal = C.load(12); m12, z12 = cal; m14, z14 = C.load(14)
BASEF = C.CTRL["v1b_carrier"]


def biased(m, factor):
    mm = copy.deepcopy(m)
    for c in mm["cond"]:
        mm["cond"][c] = [mm["cond"][c][0], mm["cond"][c][1] * factor]
    return lambda _m, cal_, c, W: BASEF(mm, cal_, c, W)


def mean_vec(fn, m, z):
    r = C.evaluate(fn, m, z, cal)
    return np.mean([v[1] for v in r.values()], 0)


B = [1.0, 1.1, 1.25, 1.5, 2.0]
sel = {b: float(mean_vec(biased(m12, b), m12, z12).mean()) for b in B}
bstar = max(sel, key=sel.get)
print("seed 12 (selection):", {b: round(v, 4) for b, v in sel.items()}, "-> b*", bstar)
ref14 = mean_vec(biased(m14, 1.0), m14, z14)
out = dict(selection_seed12=sel, b_star=bstar, dev={})
for s in (1.0, 0.5, 0.8, 1.25, 2.0):
    x1 = mean_vec(biased(m14, s), m14, z14); xb = mean_vec(biased(m14, s * bstar), m14, z14)
    d = xb - x1
    out["dev"][str(s)] = dict(no_bias=float(x1.mean()), bias=float(xb.mean()), diff=float(d.mean()), ci=boot(d))
    print(f"seed 14, estimation error x{s}: no bias {x1.mean():.4f}, bias b*={bstar} {xb.mean():.4f}, diff {d.mean():+.4f} {boot(d)}")
json.dump(out, open("round3_bias.json", "w"), indent=1)
