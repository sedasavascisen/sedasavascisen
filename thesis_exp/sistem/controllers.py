"""
Controllers and fixed baselines for the latency-aware RIS controller (PROTOKOL.md), evaluated from harness cubes.
A controller maps a condition's MEASURABLE inputs (f_c, f_d, W, arm latencies) plus calibration data from seed 12
to one pipeline (arm). Evaluation: python3 controllers.py --dev   (calibrate on 12, evaluate on 14)
"""
import sys, json, pathlib, argparse
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "tasarim_kurali")); sys.path.insert(0, str(H.parent / "p4"))
import numpy as np
import rule
from common import boot

C0 = 299792458.0
WS = (0, 20)


def load(seed):
    m = json.load(open(H / "cube" / f"seed{seed}.json")); z = np.load(H / "cube" / f"seed{seed}.npz")
    return m, z


def cond_info(m, c):
    fc, v = m["cond"][c]
    return dict(fc=fc, v=v, fd=v * fc * 1e9 / C0)


# ------------------------------------------------------------------ fixed baselines (PROTOKOL K1..K5)
def k1(m, cal, c, W):
    return "best+0"


def k2(m, cal, c, W):
    return "avg+5"


def k3(m, cal, c, W):
    return "avg+48"


def k4(m, cal, c, W):
    ci = cond_info(m, c); dT = (m["lat"]["avg+48"] - m["lat"]["avg+0"]) / 48
    L = rule.closed_form(dT, ci["fd"], [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48])
    return f"avg+{L}"


def k5(m, cal, c, W, budget=10.0):
    mc, zc = cal; fc = cond_info(m, c)["fc"]
    cand = [a for a in m["arms"] if m["lat"][a] <= budget and not a.startswith("warm")]   # fresh pipelines only
    ref = c if f"{c}_t0" in zc else [k for k in mc["cond"] if mc["cond"][k][0] == fc][0]
    t0 = zc[f"{ref}_t0"]
    return max(cand, key=lambda a: t0[mc["arms"].index(a)].mean())


BASE = {"K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5}

# ------------------------------------------------------------------ controllers (night ideas)
PSI = rule.load()


def v0_rule(m, cal, c, W):
    """Design rule generalised: R_hat(a) = R_floor + (R0_12(a) - R_floor) * psi_bar(f_d tau_a, f_d W), both starts,
    R0 from seed-12 t = 0 rates at this carrier; psi and R_floor from tasarim_kurali (3 GHz, 1.5 m/s, seed 12)."""
    mc, zc = cal; ci = cond_info(m, c)
    ref = [k for k in mc["cond"] if mc["cond"][k][0] == ci["fc"]][0]
    t0 = zc[f"{ref}_t0"].mean(1)
    best, bv = None, -1e9
    for i, a in enumerate(m["arms"]):
        tau = m["lat"][a]
        u, b, du = ci["fd"] * tau / 1000, ci["fd"] * W / 1000, ci["fd"] * 2.0 / 1000
        r = PSI["R_floor"] + (t0[i] - PSI["R_floor"]) * rule.psi_bar(PSI, u, b, du)
        if r > bv:
            best, bv = a, r
    return best


_EMP = {}


def _emp_psi(cal, fc, W):
    """Round 1: empirical psi per (carrier, W) from the seed-12 cube: psi_i = (eff_i - F)/(t0_i - F) over all arms and
    all conditions at this carrier, u_i = f_d tau_i; binned median over log u (25 bins), interpolated in log u."""
    key = (fc, W)
    if key not in _EMP:
        mc, zc = cal; us, ps = [], []
        for c in mc["cond"]:
            if mc["cond"][c][0] != fc:
                continue
            fd = cond_info(mc, c)["fd"]
            e, t = zc[f"{c}_eff{W}"].mean(1), zc[f"{c}_t0"].mean(1)
            for i, a in enumerate(mc["arms"]):
                us.append(fd * mc["lat"][a] / 1000); ps.append((e[i] - PSI["R_floor"]) / (t[i] - PSI["R_floor"]))
        lu, ps = np.log(np.array(us)), np.array(ps)
        edges = np.linspace(lu.min(), lu.max() + 1e-9, 26)
        cen, med = [], []
        for j in range(25):
            s = (lu >= edges[j]) & (lu < edges[j + 1])
            if s.any():
                cen.append(lu[s].mean()); med.append(np.median(ps[s]))
        _EMP[key] = (np.array(cen), np.array(med))
    return _EMP[key]


def v1_emp(m, cal, c, W):
    """v0 with psi replaced by the empirical, carrier- and W-specific psi of _emp_psi (round 1)."""
    mc, zc = cal; ci = cond_info(m, c)
    ref = [k for k in mc["cond"] if mc["cond"][k][0] == ci["fc"]][0]
    t0 = zc[f"{ref}_t0"].mean(1)
    cen, med = _emp_psi(cal, ci["fc"], W)
    best, bv = None, -1e9
    for i, a in enumerate(m["arms"]):
        u = ci["fd"] * m["lat"][a] / 1000
        r = PSI["R_floor"] + (t0[i] - PSI["R_floor"]) * float(np.interp(np.log(u), cen, med))
        if r > bv:
            best, bv = a, r
    return best


def v1b_carrier(m, cal, c, W):
    """Round 1b: the validated design rule where it was calibrated (3 GHz); the empirical carrier-specific psi elsewhere (28 GHz)."""
    return v0_rule(m, cal, c, W) if cond_info(m, c)["fc"] == 3 else v1_emp(m, cal, c, W)


CTRL = {"v0_rule": v0_rule, "v1_emp": v1_emp, "v1b_carrier": v1b_carrier}


def evaluate(fn, m, z, cal):
    out = {}
    for c in m["cond"]:
        for W in WS:
            a = fn(m, cal, c, W)
            out[f"{c}|W{W}"] = (a, z[f"{c}_eff{W}"][m["arms"].index(a)])
    return out


def oracle(m, z):
    out = {}
    for c in m["cond"]:
        for W in WS:
            e = z[f"{c}_eff{W}"]; i = int(e.mean(1).argmax())
            out[f"{c}|W{W}"] = (m["arms"][i], e[i])
    return out


def summary(res, ref):
    """Mean over conditions of per-scenario effective rate; paired bootstrap over scenarios of the condition-averaged difference."""
    keys = list(res)
    x = np.mean([res[k][1] for k in keys], 0)
    return float(x.mean()), {n: (float((x - np.mean([r[k][1] for k in keys], 0)).mean()), boot(x - np.mean([r[k][1] for k in keys], 0))) for n, r in ref.items()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dev", action="store_true"); ap.add_argument("--only", default=None)
    a = ap.parse_args()
    cal = load(12); m, z = load(14)
    base = {n: evaluate(f, m, z, cal) for n, f in BASE.items()}
    orc = oracle(m, z)
    print("baselines (seed 14):", {n: round(float(np.mean([r[k][1].mean() for k in r])), 4) for n, r in base.items()}, "oracle", round(float(np.mean([orc[k][1].mean() for k in orc])), 4))
    for n, f in CTRL.items():
        if a.only and n != a.only:
            continue
        r = evaluate(f, m, z, cal); mean, d = summary(r, base)
        loss = float(np.mean([orc[k][1].mean() for k in orc])) - mean
        print(f"{n}: mean {mean:.4f}  oracle gap {loss:.4f}  " + "  ".join(f"-{b} {v[0]:+.4f} [{v[1][0]:+.3f},{v[1][1]:+.3f}]" for b, v in d.items()))
        print("   picks:", {k: r[k][0] for k in r})
