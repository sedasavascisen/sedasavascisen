"""
Deviation 1 (ON_KAYIT_S3_S1.md, logged before arms.py ran): timing.py showed this machine is 0.69-0.86x the
rerun latencies, so EVERY arm is re-timed here with the same protocol (seed 11, one scenario, one thread, 5 rounds,
median), to keep one machine for all latencies: su_average, su_best_of, adam L in {1,2,4,8,16,32,48}, pga.
Waits for load < 0.5. -> raw/timing2.json
"""
import sys, os, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit
from ris_mu.mumiso import baselines as B, system as S
OUT = pathlib.Path(__file__).parent / "raw"
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
load1 = os.getloadavg()[0]
torch.set_num_threads(1)
A = Aging(11, [0.0], n=16); one = slice(0, 1)
F, G, H = A.F[one], A.G[0][one], A.H[0][one]
_, TH0 = B.su_average(F, G, H, A.pt, A.nv)


def med_ms(fn, reps, warm):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


def adam(L):
    def run():
        dl = torch.zeros(1, F.shape[1], requires_grad=True); opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            th = TH0 + dl
            R = S.rates(F, G, H, torch.cos(th), torch.sin(th), A.pt, A.nv, "zf")
            loss = -(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean(); opt.zero_grad(); loss.backward(); opt.step()
    return run


jobs = {"su_average": (lambda: B.su_average(F, G, H, A.pt, A.nv), 200, 20),
        "su_best_of": (lambda: B.su_best_of(F, G, H, A.pt, A.nv), 200, 20),
        **{f"adam{L}": (adam(L), 25, 3) for L in (1, 2, 4, 8, 16, 32, 48)},
        "pga": (lambda: B.pga(F, G, H, A.pt, A.nv), 2, 0)}
rounds = {k: [] for k in jobs}; loads = []
for r in range(5):
    loads.append(os.getloadavg()[0])
    for k, (fn, reps, warm) in jobs.items():
        rounds[k].append(med_ms(fn, reps, warm))
    print(f"round {r + 1}: " + " ".join(f"{k} {rounds[k][-1]:.2f}" for k in jobs), flush=True)
med = {k: float(np.median(v)) for k, v in rounds.items()}
steps = [1, 2, 4, 8, 16, 32, 48]
res = dict(commit=commit(), threads=1, load=dict(start=load0, before=load1, per_round=loads, after=os.getloadavg()[0]),
           rounds_ms=rounds, median_ms=med, adam_slope_ms=float(np.polyfit(steps, [med[f"adam{L}"] for L in steps], 1)[0]))
json.dump(res, open(OUT / "timing2.json", "w"), indent=1); print("wrote", flush=True)
