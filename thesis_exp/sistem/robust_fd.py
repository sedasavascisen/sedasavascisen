"""Round 2: robustness of the controllers to Doppler mis-estimation. The controller sees f_d * s
(s in {0.5, 0.8, 1.25, 2.0}); the effective rate is still read on the true channel (dev seed 14, calibration 12)."""
import copy, json, numpy as np
import controllers as C
from common import boot
cal = C.load(12); m, z = C.load(14)
out = {}
for name in ("v0_rule", "v1b_carrier"):
    f = C.CTRL[name]
    ref = np.mean([v[1] for v in C.evaluate(f, m, z, cal).values()], 0)
    for s in (0.5, 0.8, 1.25, 2.0):
        mm = copy.deepcopy(m)
        for c in mm["cond"]:
            mm["cond"][c] = [mm["cond"][c][0], mm["cond"][c][1] * s]
        def g(_m, cal_, c, W, f=f, mm=mm):
            return f(mm, cal_, c, W)
        r = C.evaluate(g, m, z, cal)
        x = np.mean([v[1] for v in r.values()], 0); d = x - ref
        out[f"{name}|{s}"] = dict(mean=float(x.mean()), minus_exact=float(d.mean()), ci=boot(d))
        print(f"{name} fd x{s}: {x.mean():.4f}  vs exact {d.mean():+.4f} {boot(d)}", flush=True)
json.dump(out, open("robust_fd.json", "w"), indent=1)
