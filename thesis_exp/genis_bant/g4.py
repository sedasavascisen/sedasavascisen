"""
G4 (exploratory, ON_KAYIT.md): does the pre-registered design rule (thesis_exp/tasarim_kurali, calibrated narrowband,
1.5 m/s, seed 12) pick a good L for each wideband (B, K_opt) arm, using only that arm's measured step cost?

R0(L): the arm's wideband min-user rate at t = 0 on the selection draw (seed 12), recomputed here with the same
code and seeds as run.py (phases are deterministic). psi: from raw/calibration.json of the design rule, unchanged.
tau(L) = 0.30 ms + a_K + b_K L (raw/timing.json; the rule's T0 = 0.30 ms plus this arm's fitted intercept).
W = 0 (Definition 1, as in run.py). Loss is measured against L* on the report draw (seed 11, raw/curves.json).
Writes raw/g4.json.
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tasarim_kurali"))
import numpy as np, torch
from wb import WB, KOPTS, commit
import rule
H = pathlib.Path(__file__).parent; OUT = H / "raw"
torch.set_num_threads(2)
LSET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
BWS = [20e6, 50e6, 100e6]
SPEEDS = {"1.5mps": 1.5, "10kmh": 10 / 3.6}
FC = 3e9
TM = json.load(open(OUT / "timing.json")); CV = json.load(open(OUT / "curves.json"))
cal = rule.load()
res = dict(commit=commit(), note=__doc__.strip().splitlines()[1], cells={})
for bw in BWS:
    w0 = WB(12, [0.0], bw); su = w0.su_average()
    R0 = {k: {L: float(w0.minrate(w0.adam(su, L, k), 0).mean()) for L in LSET} for k in KOPTS}
    del w0
    for sp, v in SPEEDS.items():
        fd = v * FC / 299792458.0
        et = CV[f"11|{bw/1e6:g}|{sp}"]
        for k in KOPTS:
            f = TM[f"fit_K{k}"]
            Rh = {}
            for L in LSET:
                tau = 0.30 + f["intercept_ms"] + f["per_step_ms"] * L
                Rh[L] = cal["R_floor"] + (R0[k][L] - cal["R_floor"]) * float(rule.psi(cal, fd * tau / 1000.0))
            Lh = max(Rh, key=Rh.get)
            m = {L: float(np.mean(et[f"K{k}-L{L}"])) for L in LSET}
            Ls = max(m, key=m.get)
            res["cells"][f"{bw/1e6:g}MHz_{sp}_K{k}"] = dict(L_rule=Lh, L_star_test=Ls, loss_pct=100 * (1 - m[Lh] / m[Ls]),
                                                            dT_ms=f["per_step_ms"])
            print(f"B {bw/1e6:g} {sp} K{k}: rule L {Lh}, L* {Ls}, loss {100 * (1 - m[Lh] / m[Ls]):.2f}%", flush=True)
json.dump(res, open(OUT / "g4.json", "w"), indent=1)
print("wrote g4", flush=True)
