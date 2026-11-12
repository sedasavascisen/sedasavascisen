"""
Prompt 4.5 — 1- and 2-bit discrete phases (multi-user, aging set): does the intrinsic optimum L* survive,
and does the slow solver still lose?

Arms per bit width b (phases from the t = 0 channel, quantised with system.quantise_phase):
  SU-best-of -> q         closed form, rounded
  Adam-L -> q             SU-average + L Adam steps (step 0.5, the paper's aging-set value), rounded
  dCD-s                   discrete coordinate descent on the actual 2^b grid (baselines.coord_descent,
                          bits=b, iters=s; stops early once converged), s in {1, 2, 3, 4, 8}
Latencies: SU-best-of and Adam-L from the one-thread rerun (thesis_exp/infra; rounding is free); dCD-s is
TIMED HERE on an idle machine (load < 0.5), one scenario, one thread, median of reps over rounds.
Effective rate (Definition 1) on the aging set (seed 11); the best arm is selected on seed 12; paired
bootstrap of every arm against SU-best-of -> q. L* = argmax over the rounded-Adam arms (test).
Output: thesis_exp/p4/ayrik_faz/raw/results.json
"""
import sys, os, time, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S, baselines as B
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
GRID = [float(x) for x in np.arange(0.0, 40.0 + 0.25, 0.5)] + [50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0]
BITS = [1, 2]
SWEEPS = [1, 2, 3, 4, 8]


def phases(A, b):
    m0 = A.idx(0.0)
    P = {"SU-best-of->q": S.quantise_phase(A.su_best_of(), b)}
    su = A.su_average()
    for L in STEPS:
        P[f"Adam-{L}->q"] = S.quantise_phase(A.adam(su, L), b)
    for s in SWEEPS:
        P[f"dCD-{s}"] = B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv, bits=b, iters=s)[1]
    return P


def time_dcd(A, b):
    load0 = os.getloadavg()[0]
    while os.getloadavg()[0] >= 0.5:
        time.sleep(15)
    load1 = os.getloadavg()[0]
    torch.set_num_threads(1)
    m0 = A.idx(0.0); out = {}
    for s in SWEEPS:
        rounds = []
        for r in range(3):
            per = []
            for i in range(10):
                sl = slice(i, i + 1)
                f = lambda: B.coord_descent(A.F[sl], A.G[m0][sl], A.H[m0][sl], A.pt, A.nv, bits=b, iters=s)
                f(); t = []
                for _ in range(5):
                    t0 = time.perf_counter(); f(); t.append(time.perf_counter() - t0)
                per.append(np.median(t) * 1e3)
            rounds.append(float(np.median(per)))
        out[f"dCD-{s}"] = dict(rounds_ms=rounds, median_ms=float(np.median(rounds)))
        print(f"  b={b} dCD-{s}: {out[f'dCD-{s}']['median_ms']:.1f} ms {rounds}", flush=True)
    torch.set_num_threads(2)
    return out, dict(start=load0, before=load1, after=os.getloadavg()[0])


val, test = Aging(12, GRID), Aging(11, GRID)
res = dict(commit=commit(), su_average_t0_check=check_same_scenarios(test), bits={})
curves = {}
for b in BITS:
    Pv, Pt = phases(val, b), phases(test, b)
    curves[b] = ({k: val.curve(th, GRID) for k, th in Pv.items()}, {k: test.curve(th, GRID) for k, th in Pt.items()})
    print(f"curves done b={b}", flush=True)
for b in BITS:
    tdcd, load = time_dcd(test, b)
    lat = {"SU-best-of->q": LAT["su_best_of"], **{f"Adam-{L}->q": adam_latency(L) for L in STEPS},
           **{k: v["median_ms"] for k, v in tdcd.items()}}
    cv, ct = curves[b]
    Ev = {k: np.array([np.interp(lat[k], GRID, r) for r in c]) for k, c in cv.items()}
    Et = {k: np.array([np.interp(lat[k], GRID, r) for r in c]) for k, c in ct.items()}
    best = max(Ev, key=lambda k: Ev[k].mean())
    adams = [k for k in Et if k.startswith("Adam")]
    Lstar = max(adams, key=lambda k: Et[k].mean())
    res["bits"][str(b)] = dict(
        latency_ms=lat, dcd_timing=tdcd, load_avg=load, selected_on_val=best,
        rows={k: dict(latency_ms=lat[k], t0=float(ct[k][:, 0].mean()), effective=float(Et[k].mean()), effective_ci=boot(Et[k]),
                      minus_su_best_of_q=float((Et[k] - Et["SU-best-of->q"]).mean()), minus_su_best_of_q_ci=boot(Et[k] - Et["SU-best-of->q"]))
              for k in Et},
        L_star=Lstar, loss_L48_vs_Lstar_pct=float(100 * (1 - Et["Adam-48->q"].mean() / Et[Lstar].mean())))
    print(f"b={b}: best (val) {best} {Et[best].mean():.4f}; L* {Lstar}; dCD-8 t0 {ct['dCD-8'][:, 0].mean():.4f} eff {Et['dCD-8'].mean():.4f}", flush=True)
    json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", OUT / "results.json")
