"""
Development harness for the latency-aware RIS controller (PROTOKOL.md).
Builds a per-(seed, condition) "cube": for every candidate pipeline (start in {avg, best} x Adam L in {0}+STEPS),
its latency (start + Adam, thesis_exp/juri/raw/timing2.json), t = 0 rate and effective rate at W = 0 and averaged over
[tau, tau + 20 ms] on a 2 ms grid. Controllers are then evaluated from the cube without regenerating channels.

Usage: python3 harness.py --seed 12|14          (seed 41 only with --final, see PROTOKOL.md)
-> cube/seed{S}.npz + cube/seed{S}.json (latencies, arm names)
"""
import sys, json, time, argparse, pathlib
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "juri" / "s5")); sys.path.insert(0, str(H.parent / "p4"))
import numpy as np, torch
from ch28 import Aging28, Aging, commit

ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, required=True); ap.add_argument("--final", action="store_true")
a = ap.parse_args()
if a.seed == 41 and not a.final:
    sys.exit("seed 41 is the sealed test (PROTOKOL.md); refused without --final")
torch.set_num_threads(2)
T2 = json.load(open(H.parent / "juri" / "raw" / "timing2.json"))["median_ms"]
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam_ms = lambda L: 0.0 if L == 0 else float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
STEPS = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
START_MS = {"avg": T2["su_average"], "best": T2["su_best_of"]}
COND = {"A1": (3, 3 / 3.6), "A2": (3, 1.5), "A3": (3, 10 / 3.6), "A4": (3, 30 / 3.6), "B1": (28, 3 / 3.6), "B2": (28, 1.5)}
WGRID = np.arange(0, 21, 2.0)
ARMS = [f"{s}+{L}" for s in ("avg", "best") for L in STEPS]
LAT = {k: START_MS[k.split("+")[0]] + adam_ms(int(k.split("+")[1])) for k in ARMS}
OUT = H / "cube"; OUT.mkdir(exist_ok=True)
t_start = time.time()
store, meta = {}, dict(commit=commit(), seed=a.seed, arms=ARMS, lat=LAT, cond=COND, wgrid=WGRID.tolist(), steps=STEPS)
for fc in (3, 28):
    Mk = (lambda t, v: Aging28(a.seed, t, v=v)) if fc == 28 else (lambda t, v: Aging(a.seed, t, v=v))
    A0 = Mk([0.0], 1.5)
    st = {"avg": A0.su_average(), "best": A0.su_best_of()}
    PH = {}
    for s, th0 in st.items():
        for L in STEPS:
            PH[f"{s}+{L}"] = th0 if L == 0 else A0.adam(th0, L)
    t0 = {k: A0.minrate(th, 0).numpy() for k, th in PH.items()}
    del A0
    times = [0.0] + sorted({round(LAT[k] + w, 9) for k in ARMS for w in WGRID} - {0.0})
    for c, (cfc, v) in COND.items():
        if cfc != fc:
            continue
        A = Mk(times, v)
        cur = np.stack([np.stack([A.minrate(PH[k], A.idx(round(LAT[k] + w, 9))).numpy() for w in WGRID], 1) for k in ARMS])  # [arm, S, W]
        store[f"{c}_eff0"] = cur[:, :, 0].astype(np.float32)
        store[f"{c}_eff20"] = cur.mean(2).astype(np.float32)
        store[f"{c}_t0"] = np.stack([t0[k] for k in ARMS]).astype(np.float32)
        del A
        print(f"seed {a.seed} {c} ({time.time() - t_start:.0f} s)", flush=True)
np.savez_compressed(OUT / f"seed{a.seed}.npz", **store)
meta["seconds"] = time.time() - t_start
json.dump(meta, open(OUT / f"seed{a.seed}.json", "w"), indent=1)
print("wrote", flush=True)
