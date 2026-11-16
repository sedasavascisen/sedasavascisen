"""
S5b evaluation (ON_KAYIT_S5b.md). 28 GHz, seeds 12/11, speeds 1.5 m/s and 3 km/h. New nets evaluated at their
latency; classical arms read from s5/raw/eval.json (same channels and seeds). Width-128 latency timed here
(idle machine, one thread, batch 1, 5 rounds). -> s5/raw/eval_s5b.json
"""
import sys, os, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np, torch
from ch28 import Aging28, commit
from model import PhaseNet, features
H = pathlib.Path(__file__).parent; OUT = H / "raw"
E0 = json.load(open(OUT / "eval.json"))
T2 = json.load(open(H.parent / "raw" / "timing2.json"))["median_ms"]
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam = lambda L: float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
NETS = {f"sincos_b{s}": ("sincos", 64) for s in range(3)} | {f"angle_b{s}": ("angle", 64) for s in range(3)} | {"sincos_w128": ("sincos", 128)}
nets = {}
for k, (head, w) in NETS.items():
    n = PhaseNet(head, w=w); n.load_state_dict(torch.load(OUT / f"net_28_{k.split('_')[0]}_{k.split('_')[1]}.pt")); n.eval(); nets[k] = n
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
torch.set_num_threads(1)
A1 = Aging28(11, [0.0], n=4); one = slice(0, 1)
def f():
    with torch.no_grad():
        nets["sincos_w128"](features(A1.F[one], A1.G[0][one], A1.H[0][one]))
rounds = []
for r in range(5):
    for _ in range(20): f()
    ts = []
    for _ in range(200):
        t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    rounds.append(float(np.median(ts) * 1e3))
W128 = float(np.median(rounds)); load1 = os.getloadavg()[0]
print(f"w128 latency {W128:.3f} ms {rounds}", flush=True)
torch.set_num_threads(2)
NN64 = E0["nn_latency"]["median_ms"]
LAT = {k: (W128 if k == "sincos_w128" else NN64) for k in NETS}
res = dict(commit=commit(), w128_latency=dict(rounds_ms=rounds, median_ms=W128, load_start=load0, load_after=load1), lat=LAT, data={})
SPEEDS = {"1.5mps": 1.5, "3kmh": 3 / 3.6}
for seed in (12, 11):
    A0 = Aging28(seed, [0.0], 1.5)
    X = features(A0.F, A0.G[0], A0.H[0])
    with torch.no_grad():
        PH = {k: n(X) for k, n in nets.items()}
    t0 = {k: A0.minrate(th, 0).numpy() for k, th in PH.items()}
    HY = {f"{k}+Adam-{L}": A0.adam(PH[k], L) for k in ("sincos_b0", "sincos_b1", "sincos_b2", "sincos_w128") for L in STEPS}
    t0.update({k: A0.minrate(th, 0).numpy() for k, th in HY.items()})
    for k in HY:
        LAT[k] = LAT[k.split("+")[0]] + adam(int(k.split("-")[-1]))
    allph = {**PH, **HY}
    del A0
    times = [0.0] + sorted({round(v, 9) for v in LAT.values()})
    for sp, v in SPEEDS.items():
        A = Aging28(seed, times, v=v)
        ev = {k: A.minrate(th, A.idx(round(LAT[k], 9))).numpy().tolist() for k, th in allph.items()}
        res["data"][f"{seed}|{sp}"] = dict(t0={k: x.tolist() for k, x in t0.items()}, eff=ev)
        del A
        print(f"seed {seed} {sp} done", flush=True)
res["lat"] = LAT
json.dump(res, open(OUT / "eval_s5b.json", "w"))
print("wrote", flush=True)
