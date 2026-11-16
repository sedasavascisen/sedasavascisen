"""
NOT PRE-REGISTERED (written after seeing REPORT_S3_S1.md, where compiled CD beat Python Adam): the fair version of
jury question 1 -- EVERY arm is sped up by the same factor r (as if the whole stack were compiled equally).
For r in the pre-registered grid: SU-average, SU-best-of, Adam-L (L in 1..48), CD-s (s = 1..8) and long-run Adam at
latency/r (same-session latencies, raw/arms.json lat_meas), evaluated exactly; the best Adam-L, best CD-s and best
overall arm chosen on seed 12, reported on seed 11 with paired bootstrap. -> raw/s1b.json
"""
import sys, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import Aging, commit, boot
from ris_mu.mumiso import baselines as B
torch.set_num_threads(2)
H = pathlib.Path(__file__).parent; R = H / "raw"
D = json.load(open(R / "arms.json")); LAT = D["lat_meas"]; RG = D["rgrid"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
ARMS = list(LAT)
SPEEDS = {"1.5mps": 1.5, "10kmh": 10 / 3.6}
key = lambda a, r: f"{a}@r{r:g}"
times = [0.0] + sorted({round(LAT[a] / r, 9) for a in ARMS for r in RG})
ev = {}
t_start = time.time()
for seed in (12, 11):
    A0 = Aging(seed, [0.0]); m0 = 0; su = A0.su_average()
    PH = {"SU-average": su, "SU-best-of": A0.su_best_of(), "Long-run Adam": B.pga(A0.F, A0.G[m0], A0.H[m0], A0.pt, A0.nv)[1],
          **{f"Adam-{L}": A0.adam(su, L) for L in STEPS},
          **{f"CD-{s}": B.coord_descent(A0.F, A0.G[m0], A0.H[m0], A0.pt, A0.nv, iters=s)[1] for s in range(1, 9)}}
    del A0
    for sp, v in SPEEDS.items():
        A = Aging(seed, times, v=v)
        ev[(seed, sp)] = {key(a, r): A.minrate(PH[a], A.idx(round(LAT[a] / r, 9))).numpy() for a in ARMS for r in RG}
        del A
        print(f"seed {seed} {sp} ({time.time() - t_start:.0f} s)", flush=True)
out = dict(commit=commit(), note="not pre-registered", rgrid=RG, rows={})
for sp in SPEEDS:
    rows = []
    for r in RG:
        fam = lambda pre: [a for a in ARMS if a.startswith(pre)]
        pick = lambda arms: max(arms, key=lambda a: ev[(12, sp)][key(a, r)].mean())
        ba, bc, bo = pick(fam("Adam-")), pick(fam("CD-")), pick(ARMS)
        d = ev[(11, sp)][key(bc, r)] - ev[(11, sp)][key(ba, r)]
        rows.append(dict(r=r, best_adam=ba, adam_eff=float(ev[(11, sp)][key(ba, r)].mean()), best_cd=bc,
                         cd_eff=float(ev[(11, sp)][key(bc, r)].mean()), cd_minus_adam=float(d.mean()), ci=boot(d), best_overall=bo,
                         su_best_of_eff=float(ev[(11, sp)][key("SU-best-of", r)].mean())))
        print(f"{sp} r {r:g}: Adam {ba} {rows[-1]['adam_eff']:.3f} | CD {bc} {rows[-1]['cd_eff']:.3f} | CD-Adam {d.mean():+.3f} {rows[-1]['ci']} | best {bo}", flush=True)
    out["rows"][sp] = rows
json.dump(out, open(R / "s1b.json", "w"), indent=1)
print("wrote", flush=True)
