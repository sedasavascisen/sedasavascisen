"""
Round 4 (idea 4): warm start in periodic operation. Update period P (default 20 ms; round 5: --P 50). The previous phase is SU-best-of + Adam-6
computed on the t = 0 channel. The new update happens at t = P with fresh CSI of the t = P channel; candidate arms:
avg+L, best+L (as in harness.py, now on the t = P channel) and warm+L (Adam from the previous phase, start cost 0).
Each arm is evaluated at P + tau (+ W window, 2 ms grid). Same conditions, latencies and seeds rules as harness.py
(seed 41 only with --final). -> cube/warm_seed{S}.npz / .json
"""
import sys, json, time, argparse, pathlib
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "juri" / "s5")); sys.path.insert(0, str(H.parent / "p4"))
import numpy as np, torch
from ch28 import Aging28, Aging, commit
ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, required=True); ap.add_argument("--final", action="store_true"); ap.add_argument("--P", type=float, default=20.0)
a = ap.parse_args()
if a.seed == 41 and not a.final:
    sys.exit("seed 41 is the sealed test (PROTOKOL.md); refused without --final")
torch.set_num_threads(2)
P = a.P
TAG = "" if P == 20.0 else f"_P{P:g}"
T2 = json.load(open(H.parent / "juri" / "raw" / "timing2.json"))["median_ms"]
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam_ms = lambda L: 0.0 if L == 0 else float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
STEPS = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
START_MS = {"avg": T2["su_average"], "best": T2["su_best_of"], "warm": 0.0}
COND = {"A1": (3, 3 / 3.6), "A2": (3, 1.5), "A3": (3, 10 / 3.6), "A4": (3, 30 / 3.6), "B1": (28, 3 / 3.6), "B2": (28, 1.5)}
WGRID = np.arange(0, 21, 2.0)
ARMS = [f"{s}+{L}" for s in ("avg", "best", "warm") for L in STEPS]
LAT = {k: START_MS[k.split("+")[0]] + adam_ms(int(k.split("+")[1])) for k in ARMS}
store, meta = {}, dict(commit=commit(), seed=a.seed, P_ms=P, arms=ARMS, lat=LAT, cond=COND, wgrid=WGRID.tolist(), steps=STEPS)
t_start = time.time()
for c, (fc, v) in COND.items():
    times = [0.0, P] + sorted({round(P + LAT[k] + w, 9) for k in ARMS for w in WGRID} - {P})
    A = (Aging28(a.seed, times, v=v) if fc == 28 else Aging(a.seed, times, v=v))
    m0, mP = A.idx(0.0), A.idx(P)
    prev = A.adam(A.su_best_of(), 6)                                    # previous update, t = 0 channel
    GP, HP = A.G[mP], A.H[mP]
    st = {"avg": A.su_average(G=GP, H=HP), "best": A.su_best_of(G=GP, H=HP), "warm": prev}
    PH = {f"{s}+{L}": (th if L == 0 else A.adam(th, L, G=GP, H=HP)) for s, th in st.items() for L in STEPS}
    cur = np.stack([np.stack([A.minrate(PH[k], A.idx(round(P + LAT[k] + w, 9))).numpy() for w in WGRID], 1) for k in ARMS])
    store[f"{c}_eff0"] = cur[:, :, 0].astype(np.float32); store[f"{c}_eff20"] = cur.mean(2).astype(np.float32)
    store[f"{c}_t0"] = np.stack([A.minrate(PH[k], mP).numpy() for k in ARMS]).astype(np.float32)
    del A
    print(f"seed {a.seed} {c} ({time.time() - t_start:.0f} s)", flush=True)
np.savez_compressed(H / "cube" / f"warm{TAG}_seed{a.seed}.npz", **store)
meta["seconds"] = time.time() - t_start
json.dump(meta, open(H / "cube" / f"warm{TAG}_seed{a.seed}.json", "w"), indent=1)
print("wrote", flush=True)
