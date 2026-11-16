"""
Latency of CD-s (s = 1..8 sweeps, torch) and compiled CD (cd_fast: direct and rank-1 incremental, numba, float64),
same protocol as scripts/mumiso_mobility_latency.py: seed 11 mobility scenario, ONE scenario, one torch thread,
perf_counter, median of reps after warm-ups, 5 rounds, median over rounds; load before/after. Anchors adam1, adam48 and
torch CD (default) are re-timed to check drift against thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json.
Waits for load < 0.5 before starting. -> raw/timing.json
"""
import sys, os, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit, ROOT
from ris_mu.mumiso import baselines as B, system as S
import cd_fast as C
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
load1 = os.getloadavg()[0]
torch.set_num_threads(1)
A = Aging(11, [0.0], n=16)
one = slice(0, 1)
F, G, H = A.F[one], A.G[0][one], A.H[0][one]
_, TH0 = B.su_average(F, G, H, A.pt, A.nv)
Fn, Gn, Hn = (x[0].numpy().astype(np.complex128) for x in (F, G, H))
T0n = TH0[0].numpy().astype(np.float64)
C.cd_direct(Fn, Gn, Hn, T0n, A.pt, A.nv, 1, 16); C.cd_incremental(Fn, Gn, Hn, T0n, A.pt, A.nv, 1, 16)   # compile


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


jobs = {"adam1": (adam(1), 25, 3), "adam48": (adam(48), 25, 3)}
for s in range(1, 9):
    jobs[f"cd{s}"] = (lambda s=s: B.coord_descent(F, G, H, A.pt, A.nv, iters=s), 3, 1)
for s in range(1, 9):
    jobs[f"numba_direct{s}"] = (lambda s=s: C.cd_direct(Fn, Gn, Hn, T0n, A.pt, A.nv, s, 16), 20, 2)
    jobs[f"numba_incr{s}"] = (lambda s=s: C.cd_incremental(Fn, Gn, Hn, T0n, A.pt, A.nv, s, 16), 50, 5)
rounds = {k: [] for k in jobs}; loads = []
for r in range(5):
    loads.append(os.getloadavg()[0])
    for k, (fn, reps, warm) in jobs.items():
        rounds[k].append(med_ms(fn, reps, warm))
    print(f"round {r + 1}: " + " ".join(f"{k} {rounds[k][-1]:.2f}" for k in jobs), flush=True)
ref = json.load(open(ROOT / "thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json"))["median"]
med = {k: float(np.median(v)) for k, v in rounds.items()}
res = dict(commit=commit(), threads=1, scenario="seed 11, index 0", load=dict(start=load0, before=load1, per_round=loads,
           after=os.getloadavg()[0]), rounds_ms=rounds, median_ms=med,
           drift_vs_rerun=dict(adam1=med["adam1"] / ref["adam1"], adam48=med["adam48"] / ref["adam48"], cd8=med["cd8"] / ref["cd"]))
json.dump(res, open(OUT / "timing.json", "w"), indent=1)
print("drift", res["drift_vs_rerun"]); print("wrote", flush=True)
