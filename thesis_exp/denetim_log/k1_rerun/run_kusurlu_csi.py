"""
Prompt 4.4 — imperfect CSI whose error depends on the pilot SNR, on the effective-rate axis.

Error model: ris_mu/mumiso/csi.py (one scale per quantity F, G, h_d; variance-preserving), with the
normalised error power tied to a pilot SNR rho (per coefficient, after LS processing): e2 = 1 / (1 + rho).
rho in {0, 5, 10, 20, 30} dB and perfect CSI. Independent estimation noise at every time instant.
The BS sees only estimates: the phase is computed from the t = 0 estimate; at delivery time tau the ZF
precoder is computed from a FRESH estimate of the effective channel (same rho) and the rate is evaluated
on the TRUE channel (csi.rates_mismatched).
Arms: SU-best-of and SU-average + Adam-L (L in STEPS), measured one-thread latencies (thesis_exp/infra).
Per rho, Adam's step size per L is chosen on the validation draw (seed 12) from LRS, and the best arm is
chosen there too; the aging set (seed 11) is reported, with paired bootstrap against SU-best-of.
Output: thesis_exp/p4/kusurlu_csi/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str('/home/user/sedasavascisen/thesis_exp/p4'))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import csi as C
torch.set_num_threads(2)
OUT = pathlib.Path('/tmp/claude-0/-home-user-sedasavascisen/36a1538b-b28f-5b37-970a-9a1a9a74083b/scratchpad/rerun_k1/kusurlu_csi'); OUT.mkdir(exist_ok=True)
GRID = [float(x) for x in np.arange(0.0, 40.0 + 0.25, 0.5)] + [50.0, 75.0, 100.0]
RHO_DB = [None, 30.0, 20.0, 10.0, 5.0, 0.0]
LRS = [0.1, 0.25, 0.5, 0.75, 1.0]


def estimates(A, e2, seed):
    if e2 == 0:
        return [(A.F, A.G[m], A.H[m]) for m in range(len(GRID))]
    g = torch.Generator().manual_seed(seed)
    return [C.add_error(A.F, A.G[m], A.H[m], e2, gen=g) for m in range(len(GRID))]


def eff_curves(A, est, P, lat):
    out = {}
    for k, th in P.items():
        c = torch.stack([C.rates_mismatched(A.F, A.G[m], A.H[m], *est[m], torch.cos(th), torch.sin(th), A.pt, A.nv).min(-1).values
                         for m in range(len(GRID))], 1).numpy()
        out[k] = np.array([np.interp(lat[k], GRID, r) for r in c])
    return out


def phases(A, est0, lr_of):
    F_, G_, H_ = est0
    P = {"SU-best-of": A.su_best_of(F=F_, G=G_, H=H_)}
    su = A.su_average(F=F_, G=G_, H=H_)
    for L in STEPS:
        P[f"Adam-{L}"] = A.adam(su, L, lr=lr_of[L], F=F_, G=G_, H=H_)
    return P


lat = {"SU-best-of": LAT["su_best_of"], **{f"Adam-{L}": adam_latency(L) for L in STEPS}}
val, test = Aging(12, GRID), Aging(11, GRID)
res = dict(commit=commit(), su_average_t0_check=check_same_scenarios(test), e2_of_rho="1/(1+rho)", levels={})
for i, rho in enumerate(RHO_DB):
    e2 = 0.0 if rho is None else 1.0 / (1.0 + 10 ** (rho / 10))
    ev, et = estimates(val, e2, 100 + i), estimates(test, e2, 200 + i)
    # step size per L on validation, scored on the effective rate at that L's latency
    lr_of = {}
    su_v = val.su_average(F=ev[0][0], G=ev[0][1], H=ev[0][2])
    for L in STEPS:
        sc = {}
        for lr in LRS:
            th = val.adam(su_v, L, lr=lr, F=ev[0][0], G=ev[0][1], H=ev[0][2])
            sc[lr] = eff_curves(val, ev, {"x": th}, {"x": lat[f"Adam-{L}"]})["x"].mean()
        lr_of[L] = max(sc, key=sc.get)
    Ev = eff_curves(val, ev, phases(val, ev[0], lr_of), lat)
    Et = eff_curves(test, et, phases(test, et[0], lr_of), lat)
    best = max(Ev, key=lambda k: Ev[k].mean())
    d = Et[best] - Et["SU-best-of"]
    key = "perfect" if rho is None else f"{rho:g}dB"
    res["levels"][key] = dict(e2=e2, lr_per_L=lr_of, selected_on_val=best, test=float(Et[best].mean()), test_ci=boot(Et[best]),
                              su_best_of=float(Et["SU-best-of"].mean()), best_minus_su_best_of=float(d.mean()), ci=boot(d),
                              L_star_test=max([k for k in Et if k.startswith("Adam")], key=lambda k: Et[k].mean()),
                              by_arm={k: float(v.mean()) for k, v in Et.items()})
    print(key, best, round(float(Et[best].mean()), 4), "SU-best-of", round(float(Et["SU-best-of"].mean()), 4), boot(d), flush=True)
    json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", OUT / "results.json")
