"""
Deviation 2 (ON_KAYIT_S3_S1.md; after the independent audit DENETIM_JURI_S1_S4.md): timing.py measured CD-s on ONE
scenario that stops early after 6 sweeps, so CD-6/7/8 got the same latency, while in the evaluated batch (torch,
iters = s, joint stop) most scenarios run all s sweeps (288/400 still change in sweep 8). Here CD-s is timed WITHOUT
early stop: torch = SU-average start + s chained coord_descent(iters=1, theta0=...) calls; numba = early=False.
Same protocol otherwise (seed 11 scenario 0, one thread, 5 rounds, median; load recorded). -> raw/timing3.json
"""
import sys, os, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit
from ris_mu.mumiso import baselines as B
import cd_fast as C
OUT = pathlib.Path(__file__).parent / "raw"
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
load1 = os.getloadavg()[0]
torch.set_num_threads(1)
A = Aging(11, [0.0], n=16); one = slice(0, 1)
F, G, H = A.F[one], A.G[0][one], A.H[0][one]
Fn, Gn, Hn = (x[0].numpy().astype(np.complex128) for x in (F, G, H))
_, TH0 = B.su_average(F, G, H, A.pt, A.nv); T0n = TH0[0].numpy().astype(np.float64)
C.cd_direct(Fn, Gn, Hn, T0n, A.pt, A.nv, 1, 16, False); C.cd_incremental(Fn, Gn, Hn, T0n, A.pt, A.nv, 1, 16, False)


def torch_cd(s):
    th = B.su_average(F, G, H, A.pt, A.nv)[1]
    for _ in range(s):
        th = B.coord_descent(F, G, H, A.pt, A.nv, iters=1, theta0=th)[1]


def med_ms(fn, reps, warm):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


jobs = {}
for s in range(1, 9):
    jobs[f"cd{s}"] = (lambda s=s: torch_cd(s), 3, 1)
    jobs[f"numba_direct{s}"] = (lambda s=s: C.cd_direct(Fn, Gn, Hn, T0n, A.pt, A.nv, s, 16, False), 20, 2)
    jobs[f"numba_incr{s}"] = (lambda s=s: C.cd_incremental(Fn, Gn, Hn, T0n, A.pt, A.nv, s, 16, False), 50, 5)
rounds = {k: [] for k in jobs}; loads = []
for r in range(5):
    loads.append(os.getloadavg()[0])
    for k, (fn, reps, warm) in jobs.items():
        rounds[k].append(med_ms(fn, reps, warm))
    print(f"round {r + 1}: " + " ".join(f"{k} {rounds[k][-1]:.2f}" for k in jobs), flush=True)
med = {k: float(np.median(v)) for k, v in rounds.items()}
json.dump(dict(commit=commit(), threads=1, early_stop=False, load=dict(start=load0, before=load1, per_round=loads, after=os.getloadavg()[0]),
               rounds_ms=rounds, median_ms=med), open(OUT / "timing3.json", "w"), indent=1)
print("wrote", flush=True)
