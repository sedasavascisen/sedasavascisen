"""
A small-delay model of the intrinsic optimum, checked against measurements
on two RIS sizes.

MODEL
-----
For Adam run L steps from SU-average, write r0(L) for the t=0 min-user rate
and Delta(L, u) for the loss after the user has moved u = f_d * tau
wavelengths. Two empirical laws are fitted on the measured curves:

  (i)  convergence:   R_inf - r0(L) = D * L^(-gamma)          (L in the fit range)
  (ii) small-delay aging:  Delta(L, u) = kappa_L * u^2       (tau <= 10 ms)

(ii) has the form of the leading term of the Clarke correlation 1 - (pi u)^2 for
isotropic scattering; for this geometric channel kappa_L is fitted, not derived;
kappa_L grows with how far the phase has been optimised. With latency
tau = L * dT, i.e. u = x * L with x = dT * f_d, the effective rate is

  R_eff(L) = r0(L) - kappa_L * x^2 * L^2.

With kappa constant, d/dL = 0 gives the closed form

  L* = (gamma * D / (2 * kappa))^(1 / (gamma + 2)) * x^(-2 / (gamma + 2)),

a power law in x with exponent -2/(gamma+2). A semi-analytic version keeps
the measured r0(L) and kappa_L and maximises over the L grid. Both are
compared with the measured optimum, i.e. the effective rate interpolated on
the generator's evolved channels, over the same x grid as
mumiso_step_scaling.py.

SCENARIOS
---------
8x4 (N = 32): the aging set of the paper (seed 11, 20 scatterers, 400
scenarios); its SU-average curve is asserted against the stored run.
8x8 (N = 64): same room, BS, users and seed with a larger panel. Its Adam
step is slower; the per-step latency is scaled by the measured N=64/N=32
step-time ratio (one thread, 20 scenarios, idle machine).
"""
import sys
import time
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

RES = pathlib.Path(__file__).resolve().parents[1] / "results"
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
MS_PER_STEP = 13.3 / 8
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128, 192, 256]
MULTS = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
FIT_L = (1, 64)            # range for the convergence law
KAPPA_TMAX = 10.0          # ms, small-delay range for the aging law
LOAD0 = float(open("/proc/loadavg").read().split()[0])


def build(M, K):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, M=M, K=K, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES,
                          "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(400)
    N = panel.positions.shape[0]
    pt, nv = 1.0, 1.0 / cfg.snr_scale()
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    fd = cfg.velocity * panel.fc / 3e8
    return dict(N=N, F=F, Gt=Gt, Ht=Ht, pt=pt, nv=nv, fd=fd)


def curves(sc):
    F, Gt, Ht, pt, nv, N = sc["F"], sc["Gt"], sc["Ht"], sc["pt"], sc["nv"], sc["N"]
    G0, H0 = Gt[0], Ht[0]
    _, th_su = B.su_average(F, G0, H0, pt, nv)

    def curve(th):
        return np.stack([S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                                 "zf").min(-1).values.numpy() for m in range(len(TIMES))], 1)
    out = {0: curve(th_su)}
    dl = torch.zeros(400, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for i in range(1, max(STEPS) + 1):
        th = th_su + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
        if i in STEPS:
            out[i] = curve((th_su + dl).detach())
    return out


def step_ms(M, K, n_scen=20, steps=8, reps=7):
    """Median per-step Adam time, one thread, one scenario at a time."""
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, M=M, K=K, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,),
                          "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(n_scen)
    N = panel.positions.shape[0]
    pt, nv = 1.0, 1.0 / cfg.snr_scale()
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    G = torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64)
    H = torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64)
    _, th0 = B.su_average(F, G, H, pt, nv)
    nt = torch.get_num_threads()
    torch.set_num_threads(1)
    meds = []
    for s in range(n_scen):
        o = slice(s, s + 1)

        def run():
            dl = torch.zeros(1, N, requires_grad=True)
            opt = torch.optim.Adam([dl], lr=0.5)
            for _ in range(steps):
                th = th0[o] + dl
                R = S.rates(F[o], G[o], H[o], torch.cos(th), torch.sin(th), pt, nv, "zf")
                (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
                opt.step()
                opt.zero_grad()
        for _ in range(2):
            run()
        ts = []
        for _ in range(reps):
            t0 = time.perf_counter()
            run()
            ts.append(time.perf_counter() - t0)
        meds.append(np.median(ts) * 1e3 / steps)
    torch.set_num_threads(nt)
    return float(np.median(meds))


def analyse(cv, fd, ms_base):
    t = np.array(TIMES)
    mean = {L: c.mean(0) for L, c in cv.items()}
    r0 = np.array([mean[L][0] for L in STEPS])
    # (i) convergence law on the gap to the L=256 value
    R_inf = mean[STEPS[-1]][0]
    sel = [i for i, L in enumerate(STEPS) if FIT_L[0] <= L <= FIT_L[1]]
    Lf = np.array([STEPS[i] for i in sel], float)
    gap = R_inf - r0[sel]
    slope, icpt = np.polyfit(np.log(Lf), np.log(gap), 1)
    gamma, D = -slope, float(np.exp(icpt))
    gap_fit = D * Lf ** (-gamma)
    r2_gap = 1 - ((np.log(gap) - np.log(gap_fit)) ** 2).sum() / ((np.log(gap) - np.log(gap).mean()) ** 2).sum()
    # (ii) small-delay aging law per L
    msk = (t > 0) & (t <= KAPPA_TMAX)
    u = fd * t[msk] / 1e3
    kap, r2k = {}, {}
    for L in STEPS:
        Dl = mean[L][0] - mean[L][msk]
        k = float((Dl * u ** 2).sum() / (u ** 4).sum())
        kap[L] = k
        r2k[L] = float(1 - ((Dl - k * u ** 2) ** 2).sum() / ((Dl - Dl.mean()) ** 2).sum())
    out = dict(gamma=float(gamma), D=D, R_inf=float(R_inf), r2_logGap=float(r2_gap),
               kappa_by_L={str(L): kap[L] for L in STEPS},
               kappa_r2_by_L={str(L): r2k[L] for L in STEPS}, by_mult={})
    kbar = float(np.median([kap[L] for L in STEPS if 2 <= L <= 48]))
    out["kappa_bar"] = kbar
    exp_model = -2.0 / (gamma + 2.0)
    out["exponent_model"] = exp_model
    xs, Lm, La, Lb = [], [], [], []
    for m in MULTS:
        dt = ms_base * m
        x = dt * 1e-3 * fd
        eff = np.array([np.interp(L * dt, t, mean[L]) for L in STEPS])
        Lmeas = STEPS[int(np.argmax(eff))]
        La_ = (gamma * D / (2 * kbar)) ** (1 / (gamma + 2)) * x ** exp_model
        semi = np.array([mean[L][0] - kap[L] * (x * L) ** 2 for L in STEPS])
        Lsemi = STEPS[int(np.argmax(semi))]
        out["by_mult"][str(m)] = dict(ms_per_step=dt, x=x, L_measured=Lmeas,
                                      L_closed_form=float(La_), L_semi_analytic=Lsemi,
                                      eff_measured_best=float(eff.max()),
                                      eff_semi_at_semi_best=float(semi.max()),
                                      eff_measured_at_semi_best=float(eff[STEPS.index(Lsemi)]))
        xs.append(x); Lm.append(Lmeas); La.append(La_); Lb.append(Lsemi)
    s_meas = np.polyfit(np.log(xs), np.log(Lm), 1)[0]
    out["exponent_measured_fit"] = float(s_meas)
    out["max_log_ratio_closed"] = float(np.max(np.abs(np.log(np.array(La) / np.array(Lm)))))
    out["semi_vs_measured_eff_loss_max"] = float(max(
        1 - v["eff_measured_at_semi_best"] / v["eff_measured_best"] for v in out["by_mult"].values()))
    # the paper's operating point
    eff1 = np.array([np.interp(L * ms_base, t, mean[L]) for L in STEPS])
    i1 = int(np.argmax(eff1))
    out["m1"] = dict(best_L=STEPS[i1], best_eff=float(eff1[i1]),
                     eff_L48=float(eff1[STEPS.index(48)]),
                     loss_L48=float(1 - eff1[STEPS.index(48)] / eff1[i1]),
                     t0_L48_over_best=float(r0[STEPS.index(48)] / r0[i1] - 1),
                     t0_su_average=float(mean[0][0]))
    return out


res = dict(load_at_start=LOAD0, fit_L=FIT_L, kappa_tmax_ms=KAPPA_TMAX, steps=STEPS,
           mults=MULTS, panels={})
# timing first, while the machine is idle
t32 = step_ms(8, 4)
t64 = step_ms(8, 8)
res["timing"] = dict(adam_step_ms_N32=t32, adam_step_ms_N64=t64, ratio=t64 / t32,
                     load_after=float(open("/proc/loadavg").read().split()[0]))
print(f"Adam step, 1 thread, median of 20 scenarios: N=32 {t32:.2f} ms, N=64 {t64:.2f} ms, "
      f"ratio {t64/t32:.2f}; load {LOAD0} -> {res['timing']['load_after']}", flush=True)

ref = json.load(open(RES / "mumiso_aging_fixzf.json"))
for name, (M, K), base_ms in (("8x4", (8, 4), MS_PER_STEP), ("8x8", (8, 8), MS_PER_STEP * t64 / t32)):
    sc = build(M, K)
    cv = curves(sc)
    if name == "8x4":
        dev = np.abs(cv[0].mean(0) - np.array(ref["curve"]["su_average"])).max()
        assert dev < 1e-4, dev
    a = analyse(cv, sc["fd"], base_ms)
    a.update(N=sc["N"], ms_per_step=base_ms)
    res["panels"][name] = a
    print(f"\n== {name} (N={sc['N']}), dT={base_ms:.2f} ms/step")
    print(f"   convergence law: gamma={a['gamma']:.3f} D={a['D']:.3f} R_inf={a['R_inf']:.3f} "
          f"(R^2 log-gap {a['r2_logGap']:.3f});  kappa_bar={a['kappa_bar']:.1f}")
    print("   kappa_L:", {L: round(a['kappa_by_L'][str(L)], 1) for L in (1, 4, 8, 16, 48, 256)},
          " R^2 min", round(min(a['kappa_r2_by_L'].values()), 3))
    print(f"   exponent: model {a['exponent_model']:.3f}, measured fit {a['exponent_measured_fit']:.3f}")
    for m, v in a["by_mult"].items():
        print(f"   m={m:>5} x={v['x']:.5f}  L*: measured {v['L_measured']:>3}  closed {v['L_closed_form']:6.1f}  "
              f"semi {v['L_semi_analytic']:>3}  (eff at semi's L {v['eff_measured_at_semi_best']:.3f} "
              f"vs best {v['eff_measured_best']:.3f})")
    print(f"   at m=1: best L={a['m1']['best_L']} {a['m1']['best_eff']:.3f}, L=48 {a['m1']['eff_L48']:.3f} "
          f"({a['m1']['loss_L48']:.1%} below), t0 +{a['m1']['t0_L48_over_best']:.1%}")

json.dump(res, open(RES / "mumiso_optimum_model.json", "w"), indent=1)
print("wrote results/mumiso_optimum_model.json")
