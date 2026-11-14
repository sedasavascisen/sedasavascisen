"""
Pilot charging (4.3 follow-up) and imperfect CSI (4.4) TOGETHER — the most realistic regime the two
experiments describe separately (recommended in TEZ_TAVSIYELERI §5, item 4; run under the user's go-ahead
of 14 Nov 2026).

Model = thesis_exp/p4/onkodlayici_siralama/run.py (deployment-aligned 0.1 ms grid, window [lat, lat + 50 ms],
ZF refreshed every R ms, K = 4 pilot symbols per refresh charged as the data fraction 1 - t_p/R, R chosen
on the validation draw per arm and numerology) with ONE change: the BS never sees the true channel.
  - phase: computed from an ESTIMATE of (F, G, h_d) at t = 0;
  - every ZF refresh (and the 'fresh' and 'never' references) uses an ESTIMATE taken at that instant;
  - the rate is evaluated on the TRUE channel.
Estimates: ris_mu/mumiso/csi.add_error with e2 = 1/(1+rho) (the 4.4 model; error scale from the mean power
of the whole 400-scenario tensor, independent draw at every grid instant). rho in {30, 20} dB (at 10 dB and
below the arms were indistinguishable already in 4.4).
Adam step size per L: the value selected on the validation draw in 4.4 at the same rho
(thesis_exp/p4/kusurlu_csi/raw/results.json, lr_per_L) -- reused, not re-selected here.
Noise seeds: 7000 + 100*rho_index + 10*(seed==11) + arm index (fixed and recorded).
Output: thesis_exp/p4/onkodlayici_csi/raw/results.json
"""
import sys, os, json, math, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, adam_latency, LAT, STEPS, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S, baselines as B, csi as C
torch.set_num_threads(int(os.environ.get("THREADS", "2")))
H_ = pathlib.Path(__file__).parent
OUT = H_ / "raw"; OUT.mkdir(exist_ok=True)
DT, WIN = 0.1, 50.0
NJ = int(round(WIN / DT))
R_GRID = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
SYM_MS = {"15kHz": 3.43 / 48, "30kHz": 1.71 / 48, "60kHz": 0.86 / 48}
K_PILOTS = 4
RHO_DB = [30.0, 20.0]
LR4 = json.load(open(H_.parent / "kusurlu_csi/raw/results.json"))["levels"]
ARMS = {"SU-average": LAT["su_average"], "SU-best-of": LAT["su_best_of"],
        **{f"Adam-{L}": adam_latency(L) for L in STEPS}, "CD": LAT["cd"], "PGA": LAT["pga"]}
ARM_IDX = {k: i for i, k in enumerate(ARMS)}


def window(lat):
    return [0.0] + [lat + j * DT for j in range(NJ + 1)]


def run_arm(seed, name, rho_i, rho):
    e2 = 1.0 / (1.0 + 10 ** (rho / 10))
    lat = ARMS[name]
    A = Aging(seed, window(lat))
    chk = check_same_scenarios(A) if seed == 11 else None
    g = torch.Generator().manual_seed(7000 + 100 * rho_i + 10 * (seed == 11) + ARM_IDX[name])
    est = [C.add_error(A.F, A.G[m], A.H[m], e2, gen=g) for m in range(len(A.times))]
    F0, G0, H0 = est[0]
    lr_of = {int(k): v for k, v in LR4[f"{rho:g}dB"]["lr_per_L"].items()}
    if name == "SU-average":
        th = A.su_average(F=F0, G=G0, H=H0)
    elif name == "SU-best-of":
        th = A.su_best_of(F=F0, G=G0, H=H0)
    elif name.startswith("Adam-"):
        L = int(name[5:]); th = A.adam(A.su_average(F=F0, G=G0, H=H0), L, lr=lr_of[L], F=F0, G=G0, H=H0)
    elif name == "CD":
        th = B.coord_descent(F0, G0, H0, A.pt, A.nv)[1]
    else:
        th = B.pga(F0, G0, H0, A.pt, A.nv)[1]
    c, s = torch.cos(th), torch.sin(th)
    true_he = {}; W = {}
    def he(m):
        if m not in true_he:
            true_he[m] = S.effective_channel(A.F, A.G[m], A.H[m], c, s)
        return true_he[m]
    def w(m):
        if m not in W:
            Fe, Ge, He = est[m]
            W[m] = S.precode(S.effective_channel(Fe, Ge, He, c, s), A.pt, "zf", noise_var=A.nv)
        return W[m]
    rate = lambda m, mr: torch.log2(1.0 + S.sinr(he(m), w(mr), A.nv)).min(-1).values.numpy()
    J = range(NJ + 1)
    out = dict(check=chk, fresh=np.stack([rate(j + 1, j + 1) for j in J], 1).mean(1),
               never=np.stack([rate(j + 1, 1) for j in J], 1).mean(1), charged={})
    for num, sym in SYM_MS.items():
        tp = K_PILOTS * sym; out["charged"][num] = {}
        for Rr in R_GRID:
            per = int(round(Rr / DT))
            out["charged"][num][Rr] = np.stack([rate(j + 1, (j // per) * per + 1) for j in J], 1).mean(1) * max(0.0, 1.0 - tp / Rr)
    return out


res = dict(commit=commit(), window_ms=WIN, grid_ms=DT, pilots_per_refresh=K_PILOTS, symbol_ms=SYM_MS, R_grid=R_GRID,
           latency_ms=ARMS, rho_db=RHO_DB, e2_of_rho="1/(1+rho)", lr_source="kusurlu_csi/raw/results.json lr_per_L", levels={})
t_start = time.time()
for rho_i, rho in enumerate(RHO_DB):
    val, test = {}, {}
    for name in ARMS:
        t1 = time.time()
        val[name] = run_arm(12, name, rho_i, rho); test[name] = run_arm(11, name, rho_i, rho)
        print(f"rho {rho:g} dB {name}: fresh val {val[name]['fresh'].mean():.4f} test {test[name]['fresh'].mean():.4f} ({time.time() - t1:.0f} s)", flush=True)
    ref = "SU-best-of"
    fr_v = {k: v["fresh"].mean() for k, v in val.items()}
    best_fresh = max(fr_v, key=fr_v.get)
    lev = dict(e2=1.0 / (1.0 + 10 ** (rho / 10)),
               fresh=dict(selected_on_val=best_fresh,
                          rows={k: dict(rate=float(test[k]["fresh"].mean()), ci=boot(test[k]["fresh"]),
                                        minus_su_best_of=float((test[k]["fresh"] - test[ref]["fresh"]).mean()),
                                        minus_su_best_of_ci=boot(test[k]["fresh"] - test[ref]["fresh"])) for k in test}),
               never={k: float(test[k]["never"].mean()) for k in test}, numerologies={})
    for num in SYM_MS:
        rows, pick = {}, {}
        for k in test:
            Rk = max(R_GRID, key=lambda r: val[k]["charged"][num][r].mean())
            pick[k] = val[k]["charged"][num][Rk].mean(); rows[k] = (Rk, test[k]["charged"][num][Rk])
        best = max(pick, key=pick.get)
        xb, xr = rows[best][1], rows[ref][1]
        lev["numerologies"][num] = dict(selected_on_val=best, rows={
            k: dict(R_selected_on_val=Rk, rate=float(x.mean()), ci=boot(x),
                    minus_su_best_of=float((x - xr).mean()), minus_su_best_of_ci=boot(x - xr),
                    minus_selected=float((x - xb).mean()), minus_selected_ci=boot(x - xb),
                    test_rate_by_R={str(R): float(test[k]["charged"][num][R].mean()) for R in R_GRID})
            for k, (Rk, x) in rows.items()})
        print(f"rho {rho:g} dB {num}: selected {best} (R {rows[best][0]} ms) test {xb.mean():.4f}; SU-best-of {xr.mean():.4f}", flush=True)
    res["levels"][f"{rho:g}dB"] = lev
    res["seconds"] = time.time() - t_start
    json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", flush=True)
