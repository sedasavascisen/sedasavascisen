"""
Does the intrinsic optimum survive a faster implementation?

The latencies in the paper are those of a single-threaded PyTorch
implementation; an optimised one would be much faster per step. What sets
the optimum is not the absolute step time but the step time relative to
how fast the channel changes, x = dT * f_d. This script scales Adam's
per-step latency by m in {0.01 ... 3} at v = 1.5 m/s (so x spans two and a
half decades) and reports, with a paired bootstrap over scenarios:

  * the best step count L* and the set of L whose effective rate is not
    significantly below the best (95% paired bootstrap),
  * the loss of running to L = 256 (close to convergence) relative to L*.

It also adds a textbook classical optimiser, steepest ascent with Armijo
backtracking on the same soft-min objective, and compares it with Adam on
the effective-rate axis using per-step latencies measured here, on one
machine, for both. Same construction as mumiso_aging.py (seed 11, 20
scatterers, 400 scenarios, same time grid).
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
ADAM_STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128, 192, 256]
ARM_STEPS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
ARM_A0 = [0.1, 0.3, 1.0, 3.0, 10.0]     # initial step; best one kept (robustness)
MULTS = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
NBOOT = 2000

LOAD_START = float(open("/proc/loadavg").read().split()[0])
torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES,
                      "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(400)
N = panel.positions.shape[0]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
fd = cfg.velocity * panel.fc / 3e8
F = torch.as_tensor(d["F"], dtype=torch.complex64)
Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
G0, H0 = Gt[0], Ht[0]
_, TH_SU = B.su_average(F, G0, H0, pt, nv)


def softmin(F_, G_, H_, th):
    R = S.rates(F_, G_, H_, torch.cos(th), torch.sin(th), pt, nv, "zf")
    return -torch.logsumexp(-8.0 * R, -1) / 8.0


def curve(th):
    return np.stack([S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                             "zf").min(-1).values.numpy() for m in range(len(TIMES))], 1)


def adam_run(F_, G_, H_, start, steps, lr=0.5, record=()):
    dl = torch.zeros(start.shape[0], N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    out = {}
    for i in range(1, max(steps) + 1 if record else steps + 1):
        (-softmin(F_, G_, H_, start + dl).mean()).backward()
        opt.step()
        opt.zero_grad()
        if i in record:
            out[i] = (start + dl).detach().clone()
    return out if record else (start + dl).detach()


def armijo_run(F_, G_, H_, start, steps, record=(), a0=1.0, c=1e-4, shrink=0.5,
               max_bt=12):
    """Steepest ascent with per-scenario Armijo backtracking on soft-min."""
    th = start.clone()
    a = torch.full((start.shape[0],), a0)
    out = {}
    for i in range(1, max(steps) + 1 if record else steps + 1):
        th_ = th.clone().requires_grad_(True)
        f0 = softmin(F_, G_, H_, th_)
        g, = torch.autograd.grad(f0.sum(), th_)
        f0 = f0.detach()
        gn = (g ** 2).sum(-1)
        step = a.clone()
        done = torch.zeros_like(gn, dtype=torch.bool)
        with torch.no_grad():
            for _ in range(max_bt):
                cand = th + step[:, None] * g
                ok = softmin(F_, G_, H_, cand) >= f0 + c * step * gn
                done = done | ok
                if bool(done.all()):
                    break
                step = torch.where(done, step, step * shrink)
            th = torch.where(done[:, None], th + step[:, None] * g, th)
        # after success try a larger step; after a failed search restart at a0
        a = torch.where(done, step * 2.0, torch.full_like(step, a0))
        if i in record:
            out[i] = th.clone()
    return out if record else th


# ---------------------------------------------- per-scenario effective rates
print("computing phases ...", flush=True)
adam_ph = adam_run(F, G0, H0, TH_SU, ADAM_STEPS, record=set(ADAM_STEPS))
adam_c = {L: curve(th) for L, th in adam_ph.items()}
arm_all = {}
for a0_ in ARM_A0:
    ph = armijo_run(F, G0, H0, TH_SU, ARM_STEPS, record=set(ARM_STEPS), a0=a0_)
    arm_all[a0_] = {L: curve(th) for L, th in ph.items()}

# check against the stored sweep (same construction, lr 0.5)
sens = json.load(open(RES / "mumiso_aging_sensitivity.json"))
for r in sens["by_velocity"]["1.5"]["by_overhead"]["0.0"]["rows"]:
    if r["L"] in adam_c:
        e = np.interp(r["latency_ms"], TIMES, adam_c[r["L"]].mean(0))
        assert abs(e - r["effective"]) < 1e-4, (r["L"], e, r["effective"])


# ------------------------------------------------------------- timing
def med_ms(fn, reps=25, rounds=5):
    torch.set_num_threads(1)
    out = []
    for _ in range(rounds):
        for _ in range(3):
            fn()
        ts = []
        for _ in range(reps):
            t0 = time.perf_counter()
            fn()
            ts.append(time.perf_counter() - t0)
        out.append(float(np.median(ts) * 1e3))
    return float(np.median(out)), out


# pick a0 by Armijo's own best effective rate at Adam's step time (robustness
# check on the same scenarios, not a held-out selection); then time it
def _best(curves, ms):
    return max(np.interp(L * ms, TIMES, curves[L].mean(0)) for L in ARM_STEPS)


A0_TIME = max(ARM_A0, key=lambda a: _best(arm_all[a], MS_PER_STEP))
arm_c = arm_all[A0_TIME]
print("armijo a0 -> best effective at 1.66 ms/step:",
      {a: round(_best(arm_all[a], MS_PER_STEP), 3) for a in ARM_A0}, "chosen", A0_TIME)
# Armijo's cost per step depends on how many backtracking evaluations a
# scenario needs, so both methods are timed on 20 different scenarios (one
# at a time) and the median over scenarios is used.
load0 = float(open("/proc/loadavg").read().split()[0])
nthreads = torch.get_num_threads()
pa, pr = [], []
for s_ in range(20):
    o = slice(s_, s_ + 1)
    pa.append(med_ms(lambda: adam_run(F[o], G0[o], H0[o], TH_SU[o], 6), reps=7, rounds=3)[0])
    pr.append(med_ms(lambda: armijo_run(F[o], G0[o], H0[o], TH_SU[o], 6, a0=A0_TIME), reps=7, rounds=3)[0])
t_adam, t_arm = float(np.median(pa)), float(np.median(pr))
r_adam, r_arm = pa, pr
torch.set_num_threads(nthreads)
ratio = t_arm / t_adam
print(f"timing (6 steps, 1 thread, median of 20 scenarios): adam {t_adam:.2f} ms, armijo {t_arm:.2f} ms, "
      f"ratio {ratio:.2f}; load {load0}")

rng = np.random.default_rng(0)
idx = rng.integers(0, 400, (NBOOT, 400))


def eff_matrix(curves, steps, ms_per_step):
    return np.stack([[np.interp(L * ms_per_step, TIMES, curves[L][s]) for s in range(400)]
                     for L in steps])                                  # [nL, 400]


def summarise(E, steps):
    mean = E.mean(1)
    ib = int(np.argmax(mean))
    diff = E[ib][None] - E                                              # paired, [nL,400]
    bm = diff[:, idx].mean(2)                                           # [nL, NBOOT]
    lo = np.percentile(bm, 2.5, axis=1)
    near = [steps[j] for j in range(len(steps)) if lo[j] <= 0]          # not sig. below best
    best_boot = np.bincount(np.argmax(E[:, idx].mean(2), 0), minlength=len(steps))
    return mean, ib, near, best_boot


res = dict(fd_hz=fd, coherence_ms=0.423 / fd * 1e3, base_ms_per_step=MS_PER_STEP,
           adam_steps=ADAM_STEPS, scaling={})
print(f"\n{'m':>6}{'dT ms':>8}{'x=dT*fd':>10}{'L*':>5}  not-sig-below-best      "
      f"L=256 loss [95% CI]")
for m in MULTS:
    dt = MS_PER_STEP * m
    E = eff_matrix(adam_c, ADAM_STEPS, dt)
    mean, ib, near, bb = summarise(E, ADAM_STEPS)
    j256 = ADAM_STEPS.index(256)
    rel = (E[ib] - E[j256]) / E[ib].mean()
    bl = rel[idx].mean(1)
    loss = dict(mean=float(rel.mean()), ci=[float(np.percentile(bl, 2.5)),
                                            float(np.percentile(bl, 97.5))])
    res["scaling"][str(m)] = dict(
        ms_per_step=dt, x=dt * 1e-3 * fd, best_L=ADAM_STEPS[ib],
        best_eff=float(mean[ib]), not_sig_below_best=near,
        best_L_bootstrap={str(ADAM_STEPS[j]): int(bb[j]) for j in range(len(bb)) if bb[j]},
        latency_of_best_ms=ADAM_STEPS[ib] * dt,
        loss_L256=loss, eff_by_L=dict(zip(map(str, ADAM_STEPS), map(float, mean))),
        L256_beyond_trust=256 * dt > 200)
    print(f"{m:6.2f}{dt:8.3f}{dt*1e-3*fd:10.4f}{ADAM_STEPS[ib]:5d}  {str(near):22s}  "
          f"{loss['mean']:6.1%} [{loss['ci'][0]:.1%}, {loss['ci'][1]:.1%}]"
          + ("  (L=256 beyond 200 ms)" if 256 * dt > 200 else ""))

# key paired comparisons at the paper's step time (m = 1)
E1 = eff_matrix(adam_c, ADAM_STEPS, MS_PER_STEP)
j48, j5 = ADAM_STEPS.index(48), ADAM_STEPS.index(5)
r48 = (E1[j5] - E1[j48]) / E1[j5].mean()
res["paper_m1"] = dict(loss_L48_vs_L5=float(r48.mean()),
                       ci=[float(np.percentile(r48[idx].mean(1), 2.5)),
                           float(np.percentile(r48[idx].mean(1), 97.5))])
print("m=1: L=48 vs L=5 loss", res["paper_m1"])

# Armijo vs Adam on one latency axis (both timed here)
arm_ms = MS_PER_STEP * ratio
Ea = eff_matrix(arm_c, ARM_STEPS, arm_ms)
ma, iba, neara, _ = summarise(Ea, ARM_STEPS)
res["armijo"] = dict(a0=A0_TIME, a0_grid=ARM_A0,
                     best_eff_by_a0_at_adam_speed={str(a): float(_best(arm_all[a], MS_PER_STEP)) for a in ARM_A0},
                     timing=dict(adam_6_ms=t_adam, armijo_6_ms=t_arm, ratio=ratio,
                                 rounds_adam=r_adam, rounds_armijo=r_arm, load_before=load0,
                                 load_at_script_start=LOAD_START),
                     ms_per_step=arm_ms, steps=ARM_STEPS,
                     t0_by_L={str(L): float(arm_c[L][:, 0].mean()) for L in ARM_STEPS},
                     eff_by_L=dict(zip(map(str, ARM_STEPS), map(float, ma))),
                     best_L=ARM_STEPS[iba], best_eff=float(ma[iba]),
                     not_sig_below_best=neara)
# how much does the Armijo-vs-Adam verdict depend on the timing ratio?
res["armijo"]["best_eff_by_ratio"] = {}
E_ad = E1.mean(1).max()
for rr in (1.0, 1.2, 1.4, 1.6, 2.0):
    Er = eff_matrix(arm_c, ARM_STEPS, MS_PER_STEP * rr)
    res["armijo"]["best_eff_by_ratio"][str(rr)] = dict(
        best=float(Er.mean(1).max()), best_L=ARM_STEPS[int(np.argmax(Er.mean(1)))],
        minus_adam_best=float(Er.mean(1).max() - E_ad))
print("armijo best eff by timing ratio:", {k: (round(v["best"], 3), v["best_L"], round(v["minus_adam_best"], 3))
                                           for k, v in res["armijo"]["best_eff_by_ratio"].items()})
res["adam_t0_by_L"] = {str(L): float(adam_c[L][:, 0].mean()) for L in ADAM_STEPS}
# paired: best Adam vs best Armijo, both at m = 1
ib1 = int(np.argmax(E1.mean(1)))
dd = E1[ib1] - Ea[iba]
res["adam_vs_armijo_best"] = dict(adam_L=ADAM_STEPS[ib1], armijo_L=ARM_STEPS[iba],
                                  diff=float(dd.mean()),
                                  ci=[float(np.percentile(dd[idx].mean(1), 2.5)),
                                      float(np.percentile(dd[idx].mean(1), 97.5))])
print(f"armijo: {arm_ms:.2f} ms/step, best L={ARM_STEPS[iba]} eff {ma[iba]:.4f} "
      f"(adam best L={ADAM_STEPS[ib1]} {E1.mean(1)[ib1]:.4f}); diff {res['adam_vs_armijo_best']}")
print("armijo t0:", {L: round(v, 3) for L, v in res["armijo"]["t0_by_L"].items()})
print("adam   t0:", {L: round(v, 3) for L, v in res["adam_t0_by_L"].items()})

json.dump(res, open(RES / "mumiso_step_scaling.json", "w"), indent=1)
print("wrote results/mumiso_step_scaling.json")
