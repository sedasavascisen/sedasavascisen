"""
The pre-registered design rule (ON_KAYIT.md, section 2). Reads ONLY raw/calibration.json (seed 12).

    R_hat(L) = R_floor + (R0(L) - R_floor) * psi_bar(f_d * tau, f_d * W),   tau = L * dT + T0
    psi_bar(a, b) = mean of psi on the grid a, a + du, ..., a + b (trapezoid), du = f_d * 0.5 ms; psi(a) if b = 0
    L_hat = argmax over LSET
"""
import json, pathlib
import numpy as np

CAL = pathlib.Path(__file__).parent / "raw" / "calibration.json"
T0_MS = 0.30
GRID_MS = 0.5


def load(path=CAL):
    c = json.load(open(path))
    c["_u"] = np.asarray(c["u"]); c["_psi"] = np.asarray(c["psi"])
    return c


def psi(cal, u):
    return np.interp(u, cal["_u"], cal["_psi"])          # beyond the table: last value (np.interp clamps)


def psi_bar(cal, a, b, du):
    if b <= 0:
        return float(psi(cal, a))
    n = int(round(b / du))
    v = psi(cal, a + du * np.arange(n + 1))
    return float(np.trapz(v, dx=1.0) / n)


def predict(cal, dT_ms, fd_hz, W_ms):
    out = {}
    for L in cal["LSET"]:
        tau = L * dT_ms + T0_MS
        a, b, du = fd_hz * tau / 1000.0, fd_hz * W_ms / 1000.0, fd_hz * GRID_MS / 1000.0
        out[L] = cal["R_floor"] + (cal["R0"][str(L)] - cal["R_floor"]) * psi_bar(cal, a, b, du)
    return max(out, key=out.get), out


def closed_form(dT_ms, fd_hz, LSET):
    """Paper 2 closed form, calibrated at the paper's main point (L = 5 at x = 0.025), exponent -0.675; W ignored."""
    x = dT_ms / 1000.0 * fd_hz
    Lc = 5.0 * (x / 0.025) ** (-0.675)
    return min(LSET, key=lambda L: abs(np.log(L) - np.log(max(Lc, 1e-9))))
