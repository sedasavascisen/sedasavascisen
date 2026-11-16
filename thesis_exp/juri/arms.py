"""
Jury questions 3 and 1 (ON_KAYIT_S3_S1.md). For seed 12 (selection) and 11 (report), speeds 1.5 m/s and 10 km/h:
phases of every arm on the t = 0 channel, then the min-user rate of every arm EXACTLY at each latency it needs:
measured, FLOP-predicted, CD scaled by r (S1 grid) and compiled-CD measured. -> raw/arms.json (per-scenario values)
"""
import sys, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit, check_same_scenarios
from ris_mu.mumiso import baselines as B
torch.set_num_threads(2)
H = pathlib.Path(__file__).parent; OUT = H / "raw"
TM = json.load(open(OUT / "timing.json"))["median_ms"]
T2 = json.load(open(OUT / "timing2.json"))["median_ms"]                     # deviation 1: same-session latencies
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam_latency = lambda L: float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
LAT = {**T2}
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
SWEEPS = list(range(1, 9))
RGRID = [1, 1.5, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 1000]
SPEEDS = {"1.5mps": 1.5, "10kmh": 10 / 3.6}
K, N, T = 4, 32, 8
E = 8 * (K * N * T + 2 * K * K * T + K ** 3 + K * T)               # real FLOPs of one rate evaluation (ON_KAYIT)
FLOPS = {"SU-average": 2 * E, "SU-best-of": 8 * E, "Long-run Adam": (3 * (1 + 1000 * 4) + 4) * E,
         **{f"Adam-{L}": (2 + 3 * L) * E for L in STEPS}, **{f"CD-{s}": (4 + s * N * 16) * E for s in SWEEPS}}
MS_PER_FLOP = float(np.polyfit([1, 2, 4, 8, 16, 32, 48], [LAT[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)], 1)[0]) / (3 * E)
lat_meas = {"SU-average": LAT["su_average"], "SU-best-of": LAT["su_best_of"], "Long-run Adam": LAT["pga"],
            **{f"Adam-{L}": adam_latency(L) for L in STEPS}, **{f"CD-{s}": TM[f"cd{s}"] for s in SWEEPS}}
lat_flop = {k: FLOPS[k] * MS_PER_FLOP for k in lat_meas}
lat_s1 = {f"CD-{s}@r{r:g}": TM[f"cd{s}"] / r for s in SWEEPS for r in RGRID}
lat_nb = {**{f"CD-{s}@numba_direct": TM[f"numba_direct{s}"] for s in SWEEPS},
          **{f"CD-{s}@numba_incr": TM[f"numba_incr{s}"] for s in SWEEPS}}
EVAL = {**{f"{k}@meas": (k, v) for k, v in lat_meas.items()}, **{f"{k}@flop": (k, v) for k, v in lat_flop.items()},
        **{k: (k.split("@")[0], v) for k, v in {**lat_s1, **lat_nb}.items()}}
times = [0.0] + sorted({round(v, 9) for _, v in EVAL.values()} - {0.0})
t_start = time.time()
out = dict(commit=commit(), E_flops=E, ms_per_flop=MS_PER_FLOP, flops=FLOPS, lat_meas=lat_meas, lat_flop=lat_flop,
           lat_s1=lat_s1, lat_numba=lat_nb, rgrid=RGRID, data={})
for seed in (12, 11):
    A0 = Aging(seed, [0.0])
    if seed == 11:
        check_same_scenarios(A0)
    m0 = 0; su = A0.su_average()
    PH = {"SU-average": su, "SU-best-of": A0.su_best_of(),
          "Long-run Adam": B.pga(A0.F, A0.G[m0], A0.H[m0], A0.pt, A0.nv)[1],
          **{f"Adam-{L}": A0.adam(su, L) for L in STEPS},
          **{f"CD-{s}": B.coord_descent(A0.F, A0.G[m0], A0.H[m0], A0.pt, A0.nv, iters=s)[1] for s in SWEEPS}}
    t0 = {k: A0.minrate(th, m0).numpy() for k, th in PH.items()}
    del A0
    print(f"seed {seed}: phases done ({time.time() - t_start:.0f} s)", flush=True)
    for sp, v in SPEEDS.items():
        A = Aging(seed, times, v=v)
        ev = {key: A.minrate(PH[arm], A.idx(round(ms, 9))).numpy().tolist() for key, (arm, ms) in EVAL.items()}
        out["data"][f"{seed}|{sp}"] = dict(t0={k: x.tolist() for k, x in t0.items()}, eval=ev)
        del A
        print(f"  {sp} done ({time.time() - t_start:.0f} s)", flush=True)
out["seconds"] = time.time() - t_start
json.dump(out, open(OUT / "arms.json", "w"))
print("wrote", flush=True)
