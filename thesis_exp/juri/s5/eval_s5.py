"""
Evaluation for jury question 5 (ON_KAYIT_S5.md). Latencies (ms, this machine, one thread, batch 1): NN inference
timed here (features + forward, 5 rounds); SU-average, SU-best-of, Adam steps from ../raw/timing2.json; CD-s from
../raw/timing.json. Every arm's latency includes its start: Adam-L(start) = start + adam(L); NN+Adam-L = NN + adam(L).
For fc in {28, 3} GHz, seeds 12 (selection) and 11 (report), speeds 1.5 m/s and 3 km/h: phases on the t = 0 channel,
min-user rate exactly at each arm's latency. -> s5/raw/eval.json
"""
import sys, os, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np, torch
from ch28 import Aging28, Aging, commit
from model import PhaseNet, features
from ris_mu.mumiso import baselines as B
H = pathlib.Path(__file__).parent; OUT = H / "raw"; JR = H.parent / "raw"
T2 = json.load(open(JR / "timing2.json"))["median_ms"]; T1 = json.load(open(JR / "timing.json"))["median_ms"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam = lambda L: float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
SPEEDS = {"1.5mps": 1.5, "3kmh": 3 / 3.6}
nets = {}
for fc in (28, 3):
    for head in (["sincos", "angle"] if fc == 28 else ["sincos"]):
        n = PhaseNet(head); n.load_state_dict(torch.load(OUT / f"net_{fc}_{head}.pt")); n.eval(); nets[(fc, head)] = n
    n = PhaseNet("sincos"); n.load_state_dict(torch.load(OUT / f"net_{fc}_sincos_untrained.pt")); n.eval(); nets[(fc, "untrained")] = n
# ---- NN latency (idle machine, one thread, batch 1)
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
torch.set_num_threads(1)
A1 = Aging28(11, [0.0], n=4); one = slice(0, 1)
net = nets[(28, "sincos")]
def f():
    with torch.no_grad():
        net(features(A1.F[one], A1.G[0][one], A1.H[0][one]))
rounds = []
for r in range(5):
    for _ in range(20): f()
    ts = []
    for _ in range(200):
        t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    rounds.append(float(np.median(ts) * 1e3))
NN_MS = float(np.median(rounds))
print(f"NN latency {NN_MS:.3f} ms rounds {rounds}", flush=True)
torch.set_num_threads(2)
LAT = {"SU-average": T2["su_average"], "SU-best-of": T2["su_best_of"],
       **{f"Adam-{L}|avg": T2["su_average"] + adam(L) for L in STEPS},
       **{f"Adam-{L}|best": T2["su_best_of"] + adam(L) for L in STEPS},
       **{f"CD-{s}": T1[f"cd{s}"] for s in range(1, 9)},
       "NN-sincos": NN_MS, "NN-angle": NN_MS, "NN-untrained": NN_MS,
       **{f"NN+Adam-{L}": NN_MS + adam(L) for L in STEPS}}
times = [0.0] + sorted({round(v, 9) for v in LAT.values()})
res = dict(commit=commit(), nn_latency=dict(rounds_ms=rounds, median_ms=NN_MS, load_start=load0), lat=LAT, data={})
t_start = time.time()
for fc in (28, 3):
    Mk = (lambda s, t, v: Aging28(s, t, v=v)) if fc == 28 else (lambda s, t, v: Aging(s, t, v=v))
    for seed in (12, 11):
        A0 = Mk(seed, [0.0], 1.5); m0 = 0
        X = features(A0.F, A0.G[0], A0.H[0])
        with torch.no_grad():
            nn_th = {h: nets[(fc, h)](X) for h in (["sincos", "angle", "untrained"] if fc == 28 else ["sincos", "untrained"])}
        su, sb = A0.su_average(), A0.su_best_of()
        PH = {"SU-average": su, "SU-best-of": sb, **{f"Adam-{L}|avg": A0.adam(su, L) for L in STEPS},
              **{f"Adam-{L}|best": A0.adam(sb, L) for L in STEPS},
              **{f"CD-{s}": B.coord_descent(A0.F, A0.G[0], A0.H[0], A0.pt, A0.nv, iters=s)[1] for s in range(1, 9)},
              **{f"NN-{h}": th for h, th in nn_th.items()}, **{f"NN+Adam-{L}": A0.adam(nn_th["sincos"], L) for L in STEPS}}
        t0r = {k: A0.minrate(th, 0).numpy().tolist() for k, th in PH.items()}
        snr = float((1 / A0.nv)); del A0
        print(f"fc {fc} seed {seed}: phases ({time.time() - t_start:.0f} s)", flush=True)
        for sp, v in SPEEDS.items():
            A = Mk(seed, times, v)
            ev = {k: A.minrate(th, A.idx(round(LAT[k], 9))).numpy().tolist() for k, th in PH.items()}
            res["data"][f"{fc}|{seed}|{sp}"] = dict(t0=t0r, eff=ev, fd_hz=v * fc * 1e9 / 299792458.0)
            del A
            print(f"  {sp} ({time.time() - t_start:.0f} s)", flush=True)
res["seconds"] = time.time() - t_start
json.dump(res, open(OUT / "eval.json", "w"))
print("wrote", flush=True)
