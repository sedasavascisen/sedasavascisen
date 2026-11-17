"""
Periodic-mode controller v4 (round 4) and its evaluation on warm cubes (harness_warm.py). Same predictor as v1b:
R_hat(a) = R_floor + (R0_12(a) - R_floor) * psi(f_d tau_a, f_d W), psi from the design rule at 3 GHz and the empirical
carrier-specific psi (controllers._emp_psi, from the FRESH seed-12 cube) at 28 GHz. R0 is the seed-12 t = 0 rate of the
arm in the same condition of the warm cube (the previous phase depends on the condition's speed).
Usage: python3 periodic.py [--tag _P50]      (calibration seed 12, dev seed 14)
"""
import sys, json, argparse, pathlib
import numpy as np
import controllers as C
from common import boot
H = pathlib.Path(__file__).resolve().parent


def load(tag, seed):
    return json.load(open(H / "cube" / f"warm{tag}_seed{seed}.json")), np.load(H / "cube" / f"warm{tag}_seed{seed}.npz")


def make(allowed_prefixes):
    fresh_cal = C.load(12)

    def fn(m, cal, c, W):
        mc, zc = cal; ci = C.cond_info(m, c); t0 = zc[f"{c}_t0"].mean(1)
        if ci["fc"] == 28:
            cen, med = C._emp_psi(fresh_cal, 28, W)
        best, bv = None, -1e9
        for a in m["arms"]:
            if not a.split("+")[0] in allowed_prefixes:
                continue
            i = mc["arms"].index(a); tau = m["lat"][a]
            u, b, du = ci["fd"] * tau / 1000, ci["fd"] * W / 1000, ci["fd"] * 2.0 / 1000
            psi = C.rule.psi_bar(C.PSI, u, b, du) if ci["fc"] == 3 else float(np.interp(np.log(max(u, 1e-6)), cen, med))
            r = C.PSI["R_floor"] + (t0[i] - C.PSI["R_floor"]) * psi
            if r > bv:
                best, bv = a, r
        return best
    return fn


V4 = make(("avg", "best", "warm"))
V1B_FRESH = make(("avg", "best"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--tag", default=""); a = ap.parse_args()
    cal = load(a.tag, 12); m, z = load(a.tag, 14)
    vec = lambda r: np.mean([v[1] for v in r.values()], 0)
    rw, rf, o = C.evaluate(V4, m, z, cal), C.evaluate(V1B_FRESH, m, z, cal), C.oracle(m, z)
    base = {n: C.evaluate(f, m, z, cal) for n, f in C.BASE.items()}
    xw, xf = vec(rw), vec(rf)
    print(f"P{m['P_ms']:g}: v4 {xw.mean():.4f}, fresh-only {xf.mean():.4f}, v4 - fresh {(xw - xf).mean():+.4f} {boot(xw - xf)}, oracle {np.mean([v[1].mean() for v in o.values()]):.4f}")
    for n, r in base.items():
        d = xw - vec(r); print(f"   v4 - {n}: {d.mean():+.4f} {boot(d)}")
    print("   picks:", {k: v[0] for k, v in rw.items()})
