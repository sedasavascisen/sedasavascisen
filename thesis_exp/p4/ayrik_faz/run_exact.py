"""
Prompt 4.5, corrected evaluation (verification K3 and U20).

K3: run.py interpolated the effective rate linearly on a grid that is 0.5 ms only up to 40 ms and then jumps
to 50/75/100/150 ms (coherence time ~28 ms), so every arm slower than 40 ms (Adam-32/48->q, dCD-2..8) was
mis-estimated by up to ~0.055 b/s/Hz. Here every arm is evaluated EXACTLY at its own latency: the aging
set is built with times [0] + sorted(all arm latencies) (t = 0 first -> same scenarios, check_same_scenarios).
dCD latencies are the ones TIMED by run.py on the idle machine (raw/results.json, dcd_timing) -- not re-timed.
U20: Adam's step size was fixed at 0.5 (the paper's aging-set value). In addition to that design ("lr0.5"),
the step size per L and bit width is chosen on the validation draw (seed 12) from LRS on the effective rate
("lr-val"); both are reported. dCD and SU-best-of are unchanged.
Everything else as run.py: selection on seed 12, report on seed 11, paired bootstrap vs SU-best-of->q.
Output: thesis_exp/p4/ayrik_faz/raw/results_exact.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S, baselines as B
torch.set_num_threads(2)
H = pathlib.Path(__file__).parent
R0 = json.load(open(H / "raw/results.json"))
BITS, SWEEPS, LRS = [1, 2], [1, 2, 3, 4, 8], [0.25, 0.5, 0.75, 1.0]

lat = {b: {"SU-best-of->q": LAT["su_best_of"], **{f"Adam-{L}->q": adam_latency(L) for L in STEPS},
           **{k: v["median_ms"] for k, v in R0["bits"][str(b)]["dcd_timing"].items()}} for b in BITS}
TIMES = [0.0] + sorted({v for b in BITS for v in lat[b].values()})
val, test = Aging(12, TIMES), Aging(11, TIMES)
res = dict(commit=commit(), source_timing="raw/results.json (dcd_timing)", su_average_t0_check=check_same_scenarios(test),
           times_ms=TIMES, lrs=LRS, bits={})


def eff(A, th, t):
    return A.minrate(th, A.idx(t)).numpy()


for b in BITS:
    out = {}
    for name, A in (("val", val), ("test", test)):
        m0 = A.idx(0.0); su = A.su_average(); E, T0 = {}, {}
        th = S.quantise_phase(A.su_best_of(), b)
        E["SU-best-of->q"], T0["SU-best-of->q"] = eff(A, th, lat[b]["SU-best-of->q"]), eff(A, th, 0.0)
        for L in STEPS:
            for lr in LRS:
                th = S.quantise_phase(A.adam(su, L, lr=lr), b)
                E[f"Adam-{L}->q@{lr}"], T0[f"Adam-{L}->q@{lr}"] = eff(A, th, lat[b][f"Adam-{L}->q"]), eff(A, th, 0.0)
        for s in SWEEPS:
            th = B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv, bits=b, iters=s)[1]
            E[f"dCD-{s}"], T0[f"dCD-{s}"] = eff(A, th, lat[b][f"dCD-{s}"]), eff(A, th, 0.0)
        out[name] = (E, T0)
    Ev, _ = out["val"]; Et, Tt = out["test"]
    lr_val = {L: max(LRS, key=lambda lr: Ev[f"Adam-{L}->q@{lr}"].mean()) for L in STEPS}
    designs = {}
    for design, pick in (("lr0.5", {L: 0.5 for L in STEPS}), ("lr-val", lr_val)):
        keys = {"SU-best-of->q": "SU-best-of->q", **{f"Adam-{L}->q": f"Adam-{L}->q@{pick[L]}" for L in STEPS},
                **{f"dCD-{s}": f"dCD-{s}" for s in SWEEPS}}
        ref = Et["SU-best-of->q"]
        best = max(keys, key=lambda k: Ev[keys[k]].mean())
        adams = [k for k in keys if k.startswith("Adam")]
        Lstar = max(adams, key=lambda k: Et[keys[k]].mean())
        rows = {k: dict(latency_ms=lat[b][k], lr=(pick[int(k[5:].split("-")[0])] if k.startswith("Adam") else None),
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
    res["bits"][str(b)] = dict(latency_ms=lat[b], lr_selected_on_val=lr_val, designs=designs,
                               dcd_timing=R0["bits"][str(b)]["dcd_timing"], load_avg=R0["bits"][str(b)]["load_avg"])
    json.dump(res, open(H / "raw/results_exact.json", "w"), indent=1)
print("wrote", flush=True)
