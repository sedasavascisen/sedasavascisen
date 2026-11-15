"""
COPY of scripts/mumiso_tracking.py (Paper 2, Table III) for verification K4 (round 7, 15 Nov 2026).
The published script is NOT modified. Two changes, selected by --fix:
  --fix 0  identical logic to the published script (reproduction check against results/mumiso_tracking.json)
  --fix 1  (a) pilot airtime charged FRACTIONALLY: grid sample m stands for [t_m, t_m + DT); its weight is
               1 - (overlap with pilot intervals)/DT, instead of zeroing round(t_p/DT) whole samples
               (0.86 / 1.71 / 3.43 ms were charged as 1.0 / 1.5 / 3.5 ms when cycles start on the grid);
           (b) a phase is active from its EXACT deployment instant: a sample that contains the deployment
               is the time-weighted mix of the old and the new phase, instead of rounding the deployment
               to the nearest grid point (which could deploy up to DT/2 early).
Snapshot instants keep the published rounding (channel sampled at the nearest grid point).
--pilot selects one T_p (so the four values can run in parallel); outputs raw/fix{0,1}_tp{T_p}.json.
Everything else (seeds, scenarios, steps, periods, window, bootstrap, selection on the reported set) unchanged.

Periodic re-optimisation: what a user actually experiences.

REVISED after an independent audit: pilot airtime is now charged (no data
while the cascaded channel is being measured), the averaging window starts
after every policy has deployed at least once (100-200 ms), deployments
falling past the grid are dropped, and the scenario check compares the
SU-average curve at 0, 50, 100 and 200 ms with the stored aging run.

The single-shot effective rate computes a phase once and evaluates it at the
moment it is delivered. A deployed controller runs continuously: it takes a
channel snapshot, spends T_ov on acquisition and L * dT on optimisation,
deploys, and immediately starts the next cycle. The user sees each phase for
a whole cycle. This script simulates that loop on a 0.5 ms grid over 200 ms
(the horizon within which the mobility model is reliable) and reports the
time-averaged minimum user rate for

  * cold start: every cycle starts from SU-average on the new snapshot
  * warm start: every cycle starts from the phase currently deployed

for several L and acquisition delays. The rate is averaged over WINDOW = 100-200 ms (docstring of the published script said 50-200; code uses 100-200) so
that the start-up cycles do not dominate. Same scenarios as the aging set
(seed 11, 20 scatterers, 400 scenarios); the t = 0 channel is checked
against the stored aging run.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

import argparse
_ap = argparse.ArgumentParser(); _ap.add_argument("--fix", type=int, required=True); _ap.add_argument("--pilot", type=float, required=True)
CLI = _ap.parse_args()
RES = pathlib.Path(__file__).resolve().parents[3] / "results"
OUTD = pathlib.Path(__file__).resolve().parent / "raw"
DT_GRID = 0.5
TIMES = tuple(float(x) for x in np.arange(0.0, 200.0 + DT_GRID / 2, DT_GRID))
MS_PER_STEP = 13.3 / 8
STEPS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 48]
# update periods for the decoupled policy (snapshot every U ms, L steps,
# deploy, idle until the next snapshot); None = back-to-back cycles
PERIODS = [None, 10.0, 20.0, 40.0, 80.0]
# pilot time per cycle: 0 (pilots free / pipelined) and the 48-symbol scheme of
# Wang et al. at 60, 30 and 15 kHz NR subcarrier spacing; no data during pilots
PILOTS = [CLI.pilot]
WINDOW = (100.0, 200.0)
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
for t_chk in (0.0, 50.0, 100.0, 200.0):
    mm = TIMES.index(t_chk)
    r_ = S.rates(F, G[:, mm], H[:, mm], torch.cos(th0), torch.sin(th0), pt, nv, "zf").min(-1).values
    want = ref["curve"]["su_average"][ref["times_ms"].index(t_chk)]
    assert abs(r_.mean().item() - want) < 1e-4, (t_chk, r_.mean().item(), want)


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
    return int(round(t / DT_GRID))


def simulate(L, t_p, warm, period=None):
    """Snapshot every `period` ms (back-to-back if None): pilots [s, s+t_p]
    carry no data, then L steps, then deploy."""
    busy = t_p + L * MS_PER_STEP
    cycle = busy if period is None else period
    if busy > cycle + 1e-9:
        return None
    deploy_at = {}                         # grid index -> phase
    events, pil_iv = [], []                # exact (time, phase) and pilot intervals (fix=1)
    pilot = np.zeros(M, bool)
    snap = 0.0
    while snap < TIMES[-1]:
        m = grid(snap)
        pilot[m:min(grid(snap + t_p), M)] = t_p > 0
        start = deployed_at(snap, deploy_at, th0) if warm else \
            B.su_average(F, G[:, m], H[:, m], pt, nv)[1]
        th = adam(start, m, L)
        if grid(snap + busy) < M:
            deploy_at[grid(snap + busy)] = th
        if snap + busy <= TIMES[-1] + DT_GRID:
            events.append((snap + busy, th))
        if t_p > 0:
            pil_iv.append((snap, snap + t_p))
        snap += cycle
    first = min(deploy_at)
    if TIMES[first] > WINDOW[0]:
        return None
    if CLI.fix:
        return _fixed_rates(events, pil_iv)
    rates = np.zeros((400, M), np.float32)
    cur = th0
    for m in range(M):
        if m in deploy_at:
            cur = deploy_at[m]
        rates[:, m] = 0.0 if pilot[m] else minrate(cur, m).numpy()
    sel = [m for m in range(M) if WINDOW[0] <= TIMES[m] <= WINDOW[1]]
    return rates[:, sel].mean(1)           # per-scenario time average


def _fixed_rates(events, pil_iv):
    """Time-weighted rate per grid sample m over [t_m, t_m + DT): exact deployment instants, fractional pilots."""
    events = sorted(events, key=lambda e: e[0])
    if not events or events[0][0] > WINDOW[0]:
        return None
    sel = [m for m in range(M) if WINDOW[0] <= TIMES[m] <= WINDOW[1]]
    out = np.zeros((400, len(sel)), np.float64)
    for j, m in enumerate(sel):
        a, b = TIMES[m], TIMES[m] + DT_GRID
        # phases active inside [a, b): the last event at or before a, then events inside (a, b)
        before = [e for e in events if e[0] <= a]
        cur = before[-1][1] if before else th0
        cuts = [(a, cur)] + [(t, ph) for t, ph in events if a < t < b]
        acc = np.zeros(400)
        for i, (t0, ph) in enumerate(cuts):
            t1 = cuts[i + 1][0] if i + 1 < len(cuts) else b
            acc += (t1 - t0) / DT_GRID * minrate(ph, m).numpy()
        ov = sum(max(0.0, min(b, q1) - max(a, q0)) for q0, q1 in pil_iv)
        out[:, j] = acc * max(0.0, 1.0 - ov / DT_GRID)
    return out.mean(1).astype(np.float32)


def deployed_at(t, deploy_at, init):
    m = grid(t)
    keys = [k for k in deploy_at if k <= m]
    return deploy_at[max(keys)] if keys else init


rng = np.random.default_rng(0)
idx = rng.integers(0, 400, (NBOOT, 400))
res = dict(window_ms=WINDOW, grid_ms=DT_GRID, ms_per_step=MS_PER_STEP, steps=STEPS,
           pilots_ms=PILOTS, runs={}, warm_minus_cold={})
static = minrate(th0, 0)
for t_ov in PILOTS:
    res["runs"][str(t_ov)] = {}
    for warm in (False, True):
        mode = "warm" if warm else "cold"
        table = {}
        for U in PERIODS:
            for L in STEPS:
                v = simulate(L, t_ov, warm, U)
                if v is not None:
                    table[(U, L)] = v
        means = {k: float(v.mean()) for k, v in table.items()}
        kb = max(means, key=means.get)
        near = [k for k in table
                if np.percentile((table[kb] - table[k])[idx].mean(1), 2.5) <= 0]
        b2b = {L: means[(None, L)] for L in STEPS if (None, L) in means}
        Lb2b = max(b2b, key=b2b.get)
        res["runs"][str(t_ov)][mode] = dict(
            mean={f"{'b2b' if U is None else U}|{L}": m for (U, L), m in means.items()},
            best={"period": kb[0], "L": kb[1], "rate": means[kb],
                  "ci": [float(np.percentile(table[kb][idx].mean(1), q)) for q in (2.5, 97.5)]},
            near_best=[{"period": U, "L": L, "rate": means[(U, L)]} for U, L in near],
            back_to_back=dict(by_L={str(L): v for L, v in b2b.items()}, best_L=Lb2b,
                              best=b2b[Lb2b]))
        table_best = table[kb]
        res["runs"][str(t_ov)][mode]["_best_vec"] = None
        if warm:
            dd = table_best - cold_best
            res["warm_minus_cold"][str(t_ov)] = dict(
                diff=float(dd.mean()),
                ci=[float(np.percentile(dd[idx].mean(1), q)) for q in (2.5, 97.5)])
        else:
            cold_best = table_best
        print(f"T_p={t_ov:4.2f} {mode}: best U={kb[0]} L={kb[1]} {means[kb]:.3f}; "
              f"near={[(U, L) for U, L in near]}; back-to-back best L={Lb2b} {b2b[Lb2b]:.3f}",
              flush=True)
        for U in PERIODS:
            row = [f"{means[(U, L)]:.2f}" if (U, L) in means else "  -  " for L in STEPS]
            print(f"     U={str(U):>5}: " + " ".join(row), flush=True)
    print(f"     warm-cold (best vs best): {res['warm_minus_cold'][str(t_ov)]}", flush=True)
for t_ in res["runs"].values():
    for m_ in t_.values():
        m_.pop("_best_vec", None)
res["periods"] = ["b2b" if U is None else U for U in PERIODS]
res["fix"] = CLI.fix; res["commit"] = __import__("subprocess").run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=RES.parent).stdout.strip()
_o = OUTD / f"fix{CLI.fix}_tp{CLI.pilot:g}.json"
json.dump(res, open(_o, "w"), indent=1)
print("wrote", _o)
