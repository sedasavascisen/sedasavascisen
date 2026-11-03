"""
Periodic re-optimisation: what a user actually experiences.

The single-shot effective rate computes a phase once and evaluates it at the
moment it is delivered. A deployed controller runs continuously: it takes a
channel snapshot, spends T_ov on acquisition and L * dT on optimisation,
deploys, and immediately starts the next cycle. The user sees each phase for
a whole cycle. This script simulates that loop on a 0.5 ms grid over 200 ms
(the horizon within which the mobility model is reliable) and reports the
time-averaged minimum user rate for

  * cold start: every cycle starts from SU-average on the new snapshot
  * warm start: every cycle starts from the phase currently deployed

for several L and acquisition delays. The rate is averaged over 50-200 ms so
that the start-up cycles do not dominate. Same scenarios as the aging set
(seed 11, 20 scatterers, 400 scenarios); the t = 0 channel is checked
against the stored aging run.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

RES = pathlib.Path(__file__).resolve().parents[1] / "results"
DT_GRID = 0.5
TIMES = tuple(float(x) for x in np.arange(0.0, 200.0 + DT_GRID / 2, DT_GRID))
MS_PER_STEP = 13.3 / 8
STEPS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 48]
OVERHEADS = [0.0, 2.0, 5.0]
WINDOW = (50.0, 200.0)
NBOOT = 2000

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES,
                      "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(400)
N = panel.positions.shape[0]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
F = torch.as_tensor(d["F"], dtype=torch.complex64)
G = torch.as_tensor(d["G_t"], dtype=torch.complex64)       # [S, M, K, N]
H = torch.as_tensor(d["hd_t"], dtype=torch.complex64)      # [S, M, K, T]
M = len(TIMES)

# same scenarios as the aging set: SU-average t=0 rate must match
ref = json.load(open(RES / "mumiso_aging_fixzf.json"))
_, th0 = B.su_average(F, G[:, 0], H[:, 0], pt, nv)
r0 = S.rates(F, G[:, 0], H[:, 0], torch.cos(th0), torch.sin(th0), pt, nv, "zf").min(-1).values
assert abs(r0.mean().item() - ref["curve"]["su_average"][0]) < 1e-4, r0.mean().item()


def minrate(th, m):
    return S.rates(F, G[:, m], H[:, m], torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values


def adam(start, m, L):
    dl = torch.zeros(400, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G[:, m], H[:, m], torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


def grid(t):
    return min(int(round(t / DT_GRID)), M - 1)


def simulate(L, t_ov, warm):
    cycle = t_ov + L * MS_PER_STEP
    deployed = th0.clone()                 # SU-average at t=0, assumed instant
    deploy_at = {}                         # grid index -> phase
    snap = 0.0
    while snap < TIMES[-1]:
        m = grid(snap)
        start = deployed_at(snap, deploy_at, th0) if warm else \
            B.su_average(F, G[:, m], H[:, m], pt, nv)[1]
        th = adam(start, m, L)
        deploy_at[grid(snap + cycle)] = th
        snap += cycle
    rates = np.zeros((400, M), np.float32)
    cur = th0
    for m in range(M):
        if m in deploy_at:
            cur = deploy_at[m]
        rates[:, m] = minrate(cur, m).numpy()
    sel = [m for m in range(M) if WINDOW[0] <= TIMES[m] <= WINDOW[1]]
    return rates[:, sel].mean(1)           # per-scenario time average


def deployed_at(t, deploy_at, init):
    m = grid(t)
    keys = [k for k in deploy_at if k <= m]
    return deploy_at[max(keys)] if keys else init


rng = np.random.default_rng(0)
idx = rng.integers(0, 400, (NBOOT, 400))
res = dict(window_ms=WINDOW, grid_ms=DT_GRID, ms_per_step=MS_PER_STEP, steps=STEPS,
           overheads=OVERHEADS, runs={})
static = minrate(th0, 0)
print(f"{'T_ov':>5}{'mode':>6}" + "".join(f"{'L='+str(L):>8}" for L in STEPS))
for t_ov in OVERHEADS:
    for warm in (False, True):
        per = {L: simulate(L, t_ov, warm) for L in STEPS}
        means = {L: float(v.mean()) for L, v in per.items()}
        Lb = max(means, key=means.get)
        near = []
        for L in STEPS:
            dd = per[Lb] - per[L]
            if np.percentile(dd[idx].mean(1), 2.5) <= 0:
                near.append(L)
        res["runs"][f"{t_ov}|{'warm' if warm else 'cold'}"] = dict(
            mean_by_L={str(L): v for L, v in means.items()}, best_L=Lb,
            best=means[Lb], not_sig_below_best=near,
            ci_best=[float(np.percentile(per[Lb][idx].mean(1), q)) for q in (2.5, 97.5)])
        print(f"{t_ov:5.1f}{'warm' if warm else 'cold':>6}"
              + "".join(f"{means[L]:8.3f}" for L in STEPS) + f"   best L={Lb} {near}")
json.dump(res, open(RES / "mumiso_tracking.json", "w"), indent=1)
print("wrote results/mumiso_tracking.json")
