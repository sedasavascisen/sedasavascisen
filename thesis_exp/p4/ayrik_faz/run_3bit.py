"""
Prompt 4.5 extension — 3-bit discrete phase (user approval 13 Nov 2026), same protocol as 1/2 bit.

1) dCD-s timing for bits = 3 exactly as run.py::time_dcd: idle machine (load < 0.5 before timing), one thread,
   one scenario, median of 5 calls per scenario over 10 scenarios, 3 rounds; load start/before/after recorded.
2) Evaluation exactly as run_exact.py (every arm evaluated EXACTLY at its own latency; t = 0 first; same
   scenarios), designs lr0.5 and lr-val (Adam step size chosen on seed 12 from LRS), selection on seed 12,
   report on seed 11, paired bootstrap vs SU-best-of->q, L* over rounded Adam arms, paired dCD-1 vs Adam arms.
Output: thesis_exp/p4/ayrik_faz/raw/results_3bit.json
"""
import sys, os, time, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S, baselines as B
H = pathlib.Path(__file__).parent
BITS, SWEEPS, LRS = 3, [1, 2, 3, 4, 8], [0.25, 0.5, 0.75, 1.0]
QUICK = os.environ.get("QUICK") == "1"          # smoke test: no idle wait, 2 scenarios, 1 round, no output file


def time_dcd(A, b):
    load0 = os.getloadavg()[0]
    while not QUICK and os.getloadavg()[0] >= 0.5:
        time.sleep(15)
    load1 = os.getloadavg()[0]
    torch.set_num_threads(1)
    m0 = A.idx(0.0); out = {}
    for s in SWEEPS:
        rounds = []
        for r in range(1 if QUICK else 3):
            per = []
            for i in range(2 if QUICK else 10):
                sl = slice(i, i + 1)
                f = lambda: B.coord_descent(A.F[sl], A.G[m0][sl], A.H[m0][sl], A.pt, A.nv, bits=b, iters=s)
                f(); t = []
                for _ in range(5):
                    t0 = time.perf_counter(); f(); t.append(time.perf_counter() - t0)
                per.append(np.median(t) * 1e3)
            rounds.append(float(np.median(per)))
        out[f"dCD-{s}"] = dict(rounds_ms=rounds, median_ms=float(np.median(rounds)))
        print(f"  b={b} dCD-{s}: {out[f'dCD-{s}']['median_ms']:.1f} ms {rounds}", flush=True)
    return out, dict(start=load0, before=load1, after=os.getloadavg()[0])


T0 = Aging(11, [0.0])
tdcd, load = time_dcd(T0, BITS)
del T0
torch.set_num_threads(2)
b = BITS
lat = {"SU-best-of->q": LAT["su_best_of"], **{f"Adam-{L}->q": adam_latency(L) for L in STEPS},
       **{k: v["median_ms"] for k, v in tdcd.items()}}
TIMES = [0.0] + sorted(set(lat.values()))
n = 8 if QUICK else 400
val, test = Aging(12, TIMES, n=n), Aging(11, TIMES, n=n)
chk = None if QUICK else check_same_scenarios(test)


def eff(A, th, t):
    return A.minrate(th, A.idx(t)).numpy()


out = {}
for name, A in (("val", val), ("test", test)):
    m0 = A.idx(0.0); su = A.su_average(); E, T = {}, {}
    th = S.quantise_phase(A.su_best_of(), b)
    E["SU-best-of->q"], T["SU-best-of->q"] = eff(A, th, lat["SU-best-of->q"]), eff(A, th, 0.0)
    for L in STEPS:
        for lr in LRS:
            th = S.quantise_phase(A.adam(su, L, lr=lr), b)
            E[f"Adam-{L}->q@{lr}"], T[f"Adam-{L}->q@{lr}"] = eff(A, th, lat[f"Adam-{L}->q"]), eff(A, th, 0.0)
    for s in SWEEPS:
        th = B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv, bits=b, iters=s)[1]
        E[f"dCD-{s}"], T[f"dCD-{s}"] = eff(A, th, lat[f"dCD-{s}"]), eff(A, th, 0.0)
    out[name] = (E, T)
Ev, _ = out["val"]; Et, Tt = out["test"]
lr_val = {L: max(LRS, key=lambda lr: Ev[f"Adam-{L}->q@{lr}"].mean()) for L in STEPS}
designs = {}
for design, pick in (("lr0.5", {L: 0.5 for L in STEPS}), ("lr-val", lr_val)):
    keys = {"SU-best-of->q": "SU-best-of->q", **{f"Adam-{L}->q": f"Adam-{L}->q@{pick[L]}" for L in STEPS},
            **{f"dCD-{s}": f"dCD-{s}" for s in SWEEPS}}
    ref = Et["SU-best-of->q"]
    best = max(keys, key=lambda k: Ev[keys[k]].mean())
    Lstar = max([k for k in keys if k.startswith("Adam")], key=lambda k: Et[keys[k]].mean())
    rows = {k: dict(latency_ms=lat[k], lr=(pick[int(k[5:].split("-")[0])] if k.startswith("Adam") else None),
                    t0=float(Tt[v].mean()), effective=float(Et[v].mean()), effective_ci=boot(Et[v]),
                    minus_su_best_of_q=float((Et[v] - ref).mean()), minus_su_best_of_q_ci=boot(Et[v] - ref))
            for k, v in keys.items()}
    pair = {}
    for a_, b_ in (("dCD-1", "Adam-5->q"), ("dCD-1", Lstar), (best, Lstar)):
        if a_ != b_:
            d = Et[keys[a_]] - Et[keys[b_]]
            pair[f"{a_} - {b_}"] = dict(diff=float(d.mean()), ci=boot(d))
    designs[design] = dict(selected_on_val=best, L_star=Lstar, rows=rows, paired=pair,
                           loss_L48_vs_Lstar_pct=float(100 * (1 - Et[keys["Adam-48->q"]].mean() / Et[keys[Lstar]].mean())))
    print(f"b={b} {design}: selected {best} {Et[keys[best]].mean():.4f}; L* {Lstar}; L48 loss "
          f"{designs[design]['loss_L48_vs_Lstar_pct']:.1f}%; {pair}", flush=True)
res = dict(commit=commit(), su_average_t0_check=chk, times_ms=TIMES, lrs=LRS,
           bits={str(b): dict(latency_ms=lat, lr_selected_on_val=lr_val, designs=designs, dcd_timing=tdcd, load_avg=load)})
if not QUICK:
    json.dump(res, open(H / "raw/results_3bit.json", "w"), indent=1)
print("wrote" if not QUICK else "quick ok", flush=True)
