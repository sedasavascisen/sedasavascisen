"""
Robustness checks of the small-delay model (Proposition 1), from stored results.

Reads results/mumiso_optimum_model.json and results/mumiso_step_scaling.json
(N = 32) and reports:
  * how the fitted convergence exponent gamma, and hence the predicted
    exponent -2/(gamma+2), depend on the fit range of the power law;
  * the growth of kappa_L with L (power-law fit kappa_L ~ L^beta) and the
    exponent -2/(gamma+2+beta) that a model with growing kappa would predict;
  * a bootstrap interval for the measured slope of log L* vs log x, drawn
    from the stored bootstrap distributions of the best step count;
  * the balance ratio (aging loss / remaining convergence gap) at the
    measured optimum, which Proposition 1 predicts to be gamma/2.
No channel is regenerated and nothing is timed.
"""
import json
import pathlib
import numpy as np

RES = pathlib.Path(__file__).resolve().parents[1] / "results"
om = json.load(open(RES / "mumiso_optimum_model.json"))
sc = json.load(open(RES / "mumiso_step_scaling.json"))
p = om["panels"]["8x4"]

t0 = {int(k): v for k, v in sc["adam_t0_by_L"].items()}
R_inf = t0[256]
out = {"fit_range": {}}
for hi in (16, 24, 32, 48, 64, 96, 128):
    Ls = np.array([L for L in t0 if 1 <= L <= hi and L < 256], float)
    g = R_inf - np.array([t0[int(L)] for L in Ls])
    slope = np.polyfit(np.log(Ls), np.log(g), 1)[0]
    gam = -slope
    out["fit_range"][str(hi)] = dict(gamma=float(gam), exponent=float(-2 / (gam + 2)))
    print(f"fit 1..{hi:>3}: gamma={gam:.3f} -> predicted exponent {-2/(gam+2):.3f}")

kL = {int(k): v for k, v in p["kappa_by_L"].items()}
Lk = np.array([L for L in kL if 2 <= L <= 96], float)
beta = float(np.polyfit(np.log(Lk), np.log([kL[int(L)] for L in Lk]), 1)[0])
exp_beta = -2 / (p["gamma"] + 2 + beta)
out["kappa_growth"] = dict(beta=beta, exponent_with_growing_kappa=float(exp_beta),
                           kappa_min=float(min(kL.values())), kappa_max=float(max(kL.values())))
print(f"kappa_L ~ L^{beta:.3f} (2<=L<=96) -> exponent with growing kappa {exp_beta:.3f}")

# bootstrap interval of the measured slope from stored best-L bootstrap counts
rng = np.random.default_rng(0)
ms = sorted(sc["scaling"], key=float)
xs = np.log([sc["scaling"][m]["x"] for m in ms])
draws = []
for _ in range(4000):
    Lb = []
    for m in ms:
        cnt = sc["scaling"][m]["best_L_bootstrap"]
        Ls_, w = zip(*[(int(k), v) for k, v in cnt.items()])
        w = np.array(w, float) / sum(w)
        Lb.append(rng.choice(Ls_, p=w))
    draws.append(np.polyfit(xs, np.log(Lb), 1)[0])
lo, hi_ = np.percentile(draws, [2.5, 97.5])
out["measured_slope"] = dict(point=p["exponent_measured_fit"], ci95=[float(lo), float(hi_)])
print(f"measured slope {p['exponent_measured_fit']:.3f}, bootstrap 95% [{lo:.3f}, {hi_:.3f}]")

# balance ratio at the measured optimum
out["balance"] = {}
for m in ms:
    v = sc["scaling"][m]
    L = v["best_L"]
    x = v["x"]
    aging = kL[L] * (x * L) ** 2
    gap = R_inf - t0[L]
    out["balance"][m] = dict(L=L, ratio=float(aging / gap))
rs = [b["ratio"] for b in out["balance"].values()]
out["balance_predicted"] = p["gamma"] / 2
print(f"balance aging/gap at measured L*: {[round(r, 2) for r in rs]} (model: {p['gamma']/2:.2f})")

# Fraunhofer distance of the full aperture (diagonal) against the BS distance
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from ris_mu.mumiso.channel import make_mumiso_scenario
out["fraunhofer"] = {}
for name, (M, K) in (("8x4", (8, 4)), ("8x8", (8, 8))):
    panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, M=M, K=K, seed=11)
    P = panel.positions
    span = P.max(0) - P.min(0)
    ext = np.where(span > 1e-9, span + panel.d, 0.0)         # edge-to-edge extent per axis
    D = float(np.linalg.norm(ext))                            # aperture diagonal
    dF = 2 * D ** 2 / panel.lam
    dbs = float(np.linalg.norm(np.asarray(cfg.bs_pos) - P.mean(0)))
    out["fraunhofer"][name] = dict(aperture_diag_m=D, fraunhofer_m=dF, bs_distance_m=dbs,
                                   far_field=dbs > dF)
    print(f"{name}: aperture diagonal {D:.3f} m, 2D^2/lambda {dF:.2f} m, BS at {dbs:.2f} m, far field {dbs > dF}")
json.dump(out, open(RES / "mumiso_optimum_model_checks.json", "w"), indent=1)
print("wrote results/mumiso_optimum_model_checks.json")
