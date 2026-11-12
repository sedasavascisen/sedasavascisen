"""
Prompt 4.2 — position / statistics-based phase: the phase is computed from the LoS GEOMETRY only
(BS antenna positions, RIS element positions, user positions), with no channel pilots.

LoS-only model used by the BS (unit amplitudes ~ 1/d, no pattern, no shadowing, no scatterers):
  F_los[n,t] = exp(-j k d(bs_t, r_n)) / d(bs_t, r_n),  G_los[k,n] = exp(-j k d(u_k, r_n)) / d(u_k, r_n),
  h_d,los = 0 (the direct path is blocked by design in this scenario).
Phases: SU-average and SU-best-of computed on that model (ris_mu.mumiso.baselines), scored on the TRUE
channel (ZF precoder on the true channel at each time, as everywhere in the thesis).
Arms
  geom@0        phase from the user positions at t = 0, held fixed: aging curve + effective rate at the
                measured latency of the closed form (su_average / su_best_of from the one-thread rerun)
  geom-fresh    phase recomputed from the TRUE position at every time (no aging; position delay not modelled)
  position error: positions perturbed by N(0, sigma^2 I) per axis, sigma in {0, 0.5, 1.0} m (seed 5)
  reference     channel-based SU-best-of and best Adam-L (CSI at t = 0, measured latencies), as in Table I
Output: thesis_exp/p4/konum_faz/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import baselines as B
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
GRID = [float(x) for x in np.arange(0.0, 40.0 + 0.25, 0.5)] + [50.0, 75.0, 100.0, 150.0, 200.0]
SIGMAS = [0.0, 0.5, 1.0]

A = Aging(11, GRID)
chk = check_same_scenarios(A)
k_w = A.gen.k
R = A.gen.panel.positions                                      # [N,3]
bsa = A.d["bs_array"].astype(np.float64)                       # [S,T,3]
ue_t = A.d["ue_t"].astype(np.float64)                          # [S,M,K,3]


def los_model(ue):                                             # ue [S,K,3]
    dF = np.linalg.norm(bsa[:, :, None, :] - R[None, None], axis=-1)        # [S,T,N]
    dG = np.linalg.norm(ue[:, :, None, :] - R[None, None], axis=-1)         # [S,K,N]
    F = (np.exp(-1j * k_w * dF) / dF).transpose(0, 2, 1)                     # [S,N,T]
    G = np.exp(-1j * k_w * dG) / dG
    hd = np.zeros((ue.shape[0], ue.shape[1], bsa.shape[1]), complex)
    c = lambda x: torch.as_tensor(x, dtype=torch.complex64)
    return c(F), c(G), c(hd)


def geom_phase(ue, kind):
    F, G, hd = los_model(ue)
    fn = B.su_average if kind == "avg" else B.su_best_of
    return fn(F, G, hd, 1.0, 1.0)[1]


rng = np.random.default_rng(5)
res = dict(commit=commit(), su_average_t0_check=chk, grid_ms=GRID, arms={})
ch_best = A.su_best_of(); cb = A.curve(ch_best, GRID)
res["arms"]["channel SU-best-of"] = dict(latency_ms=LAT["su_best_of"], t0=float(cb[:, 0].mean()),
                                         effective=float(np.mean([np.interp(LAT["su_best_of"], GRID, r) for r in cb])),
                                         curve=cb.mean(0).tolist())
su = A.su_average(); best = None
for L in STEPS:
    c = A.curve(A.adam(su, L), GRID); e = np.array([np.interp(adam_latency(L), GRID, r) for r in c])
    if best is None or e.mean() > best[1].mean():
        best = (L, e, c)
res["arms"][f"channel Adam-{best[0]} (best on this set, optimistic)"] = dict(latency_ms=adam_latency(best[0]), t0=float(best[2][:, 0].mean()),
                                                                             effective=float(best[1].mean()), curve=best[2].mean(0).tolist())
for sig in SIGMAS:
    err = rng.normal(0, sig, ue_t.shape) if sig > 0 else np.zeros_like(ue_t)
    err[..., 2] = 0.0 if sig > 0 else 0.0                       # heights assumed known
    for kind, lat_key in (("avg", "su_average"), ("best", "su_best_of")):
        th0 = geom_phase(ue_t[:, 0] + err[:, 0], kind)
        c = A.curve(th0, GRID)
        eff = np.array([np.interp(LAT[lat_key], GRID, r) for r in c])
        fresh = np.stack([A.minrate(geom_phase(ue_t[:, m] + err[:, m], kind), m).numpy() for m in range(len(GRID))], 1)
        d = eff - np.array([np.interp(LAT["su_best_of"], GRID, r) for r in cb])
        res["arms"][f"geom-{kind}@0 sigma={sig}"] = dict(latency_ms=LAT[lat_key], t0=float(c[:, 0].mean()), effective=float(eff.mean()),
                                                         effective_ci=boot(eff), minus_channel_su_best_of=float(d.mean()),
                                                         minus_channel_su_best_of_ci=boot(d), curve=c.mean(0).tolist())
        res["arms"][f"geom-{kind}-fresh sigma={sig}"] = dict(mean_rate_0_200ms=float(fresh.mean()), curve=fresh.mean(0).tolist())
        print(sig, kind, round(float(c[:, 0].mean()), 4), round(float(eff.mean()), 4), round(float(d.mean()), 4), round(float(fresh.mean()), 4), flush=True)
json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", OUT / "results.json")
