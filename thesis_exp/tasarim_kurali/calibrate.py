"""
Design-rule calibration (pre-registration ON_KAYIT.md, section 2). Calibration draw ONLY (seed 12, 1.5 m/s).
Outputs raw/calibration.json with
  R0[L]     t = 0 min-user rate of Adam-L (step 0.5, SU-average start), L in LSET
  R_floor   rate of the same phases on an independent channel (scenario s evaluated on scenario s+1), averaged over L
  psi(u)    normalised aging curve on u = f_d * t: mean over L of (R(L,t) - R_floor) / (R0(L) - R_floor);
            spread over L recorded as a diagnostic
Time grid: 0-200 ms every 0.5 ms, then 200-2200 ms every 5 ms (u up to ~33 at 1.5 m/s, 3 GHz).
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit, ROOT
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
LSET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
V = 1.5
TIMES = [round(float(x), 4) for x in np.arange(0.0, 200.0, 0.5)] + [round(float(x), 4) for x in np.arange(200.0, 2200.0 + 2.5, 5.0)]
A = Aging(12, TIMES, v=V)
FC = float(A.gen.panel.fc); lam = float(A.gen.panel.c) / FC
fd = V / lam
su = A.su_average()
R0, curves, floors = {}, {}, {}
roll = lambda X: torch.roll(X, 1, dims=0)
for L in LSET:
    th = A.adam(su, L)
    c = np.stack([A.minrate(th, A.idx(t)).numpy() for t in TIMES], 1).mean(0)       # mean over scenarios
    R0[L] = float(c[0]); curves[L] = c
    floors[L] = float(A.minrate(th, 0, F=roll(A.F), G=roll(A.G[0]), H=roll(A.H[0])).mean())
    print(f"L={L}: R0 {R0[L]:.4f} floor {floors[L]:.4f} R(100ms) {c[TIMES.index(100.0)]:.4f}", flush=True)
R_floor = float(np.mean(list(floors.values())))
psis = np.stack([(curves[L] - R_floor) / (R0[L] - R_floor) for L in LSET], 0)
u = (np.array(TIMES) / 1000.0 * fd).tolist()
res = dict(commit=commit(), seed=12, velocity_mps=V, fc_hz=FC, fd_hz=float(fd), LSET=LSET,
           R0={str(L): R0[L] for L in LSET}, R_floor=R_floor, floor_by_L={str(L): floors[L] for L in LSET},
           times_ms=TIMES, u=u, psi=psis.mean(0).tolist(), psi_spread_max=float((psis.max(0) - psis.min(0)).max()),
           psi_spread_at_u={f"{x:g}": float((psis.max(0) - psis.min(0))[int(np.argmin(np.abs(np.array(u) - x)))]) for x in (0.25, 0.5, 1, 2, 5, 10)})
json.dump(res, open(OUT / "calibration.json", "w"), indent=1)
print("R_floor", R_floor, "fd", fd, "psi spread max", res["psi_spread_max"], res["psi_spread_at_u"])
