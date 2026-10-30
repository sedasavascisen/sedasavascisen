"""
Latency DISTRIBUTION and the fraction of runs that fit the coherence time.

WHY THIS FILE EXISTS
--------------------
The report's "bütçede kalma oranı" column -- the 95% that made 16-step
gradient ascent "the best method in budget" -- was produced by an inline
command that was never saved, so nobody could rerun it. An independent
audit measured 85-90% instead and could not find the code. A number that
carries a conclusion and has no script behind it is not a measurement.

So: this script. It differs from `mumiso_frontier.py`, which times each
method a handful of times and keeps only the median, in three ways that
turned out to matter.

1. IT REPORTS THE DISTRIBUTION, not a point. On this box 16-step Adam has
   been measured at 23.7, 24.2, 24.3, 25.3, 26.0 and 29.4 ms across runs.
   The budget is 28.2 ms. A single median either clears it or does not,
   depending on the run, which is how a 95% claim and an "already outside
   the budget" artifact ended up in the same repository.

2. IT VARIES THE SCENARIO, not just the repeat. Timing one scenario sixty
   times measures cache behaviour; timing sixty scenarios measures the
   method.

3. IT REFUSES TO REPORT ON A BUSY MACHINE. The audit's first pass ran
   alongside two training jobs and inflated every latency by 30-75%, which
   flipped the headline. Load is checked before and after, and the result
   is marked untrustworthy if the machine was not quiet.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--scenarios", type=int, default=60,
                help="distinct scenarios for the LATENCY sample, each timed once")
ap.add_argument("--rate-n", type=int, default=400,
                help="scenarios for the RATE estimate; kept separate because "
                     "60 is far too few for a heavy-tailed min-rate mean")
ap.add_argument("--threads", type=int, default=0,
                help="torch threads; 0 = library default. Pinning to 1 makes "
                     "contention visible but inflates every latency by ~50%% "
                     "and then the numbers cannot be compared with the rest "
                     "of the report")
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--max-load", type=float, default=0.6,
                help="per-core load above which results are flagged")
ap.add_argument("--tag", default="budget_fraction")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


def load_per_core():
    try:
        la = float(open("/proc/loadavg").read().split()[0])
        import os
        return la / max(os.cpu_count() or 1, 1)
    except Exception:
        return float("nan")


load_before = load_per_core()
torch.manual_seed(0)
if a.threads:
    torch.set_num_threads(a.threads)
NTHREADS = torch.get_num_threads()
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
# One generation, two disjoint uses: the first `scenarios` are timed one at a
# time, and a larger block is used for the rate. Reporting a rate averaged
# over the 60 timed scenarios -- which the first version of this script did --
# gave su_average 0.876 where 400 scenarios give 1.19, because the min-rate
# distribution is heavy-tailed and 60 draws do not pin its mean.
d = MuMisoChannel(panel, cfg).generate(max(a.scenarios, a.rate_n))
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH_SU = B.su_average(F, G, hd, pt, nv)
_, TH_BEST = B.su_best_of(F, G, hd, pt, nv)

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()

fd = a.velocity * panel.fc / 3e8
TC = 0.423 / fd * 1e3
say(f"N={N} T={a.tx} K={a.users}  |  latency: {a.scenarios} scenarios "
    f"at batch 1, {NTHREADS} torch thread(s)  |  rate: {a.rate_n} scenarios")
say(f"coherence budget T_c = {TC:.1f} ms  "
    f"(v={a.velocity} m/s, f_c={panel.fc/1e9:.1f} GHz, f_d={fd:.1f} Hz)")
say(f"load per core before: {load_before:.2f}\n")


def adam_once(i, L, start):
    dl = torch.zeros(1, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    sl = slice(i, i + 1)
    for _ in range(L):
        th = start[sl] + dl
        R = S.rates(F[sl], G[sl], hd[sl], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start[sl] + dl.detach()


def net_once(i):
    sl = slice(i, i + 1)
    with torch.no_grad():
        return net(X[sl], F[sl], G[sl], hd[sl], pt, nv, TH_SU[sl])


def anchor_once(i, start):
    return start[i:i + 1]


METHODS = [("su_average", lambda i: anchor_once(i, TH_SU)),
           ("su_best_of", lambda i: anchor_once(i, TH_BEST))]
for L in (8, 12, 16, 18, 20, 24):
    METHODS.append((f"Adam {L:2d} (su_avg)", lambda i, L=L: adam_once(i, L, TH_SU)))
for L in (12, 16):
    METHODS.append((f"Adam {L:2d} (best_of)",
                    lambda i, L=L: adam_once(i, L, TH_BEST)))
METHODS.append((f"learned {a.steps}", net_once))

# warm up every path once so the first scenario is not special
for _, fn in METHODS:
    fn(0)

RATE = slice(0, a.rate_n)


def rate_batched(nm):
    """Rate over `rate_n` scenarios, computed batched -- same maths, far
    tighter mean than averaging the timed sample."""
    if nm == "su_average":
        th = TH_SU[RATE]
    elif nm == "su_best_of":
        th = TH_BEST[RATE]
    elif nm.startswith("learned"):
        with torch.no_grad():
            th = net(X[RATE], F[RATE], G[RATE], hd[RATE], pt, nv, TH_SU[RATE])
    else:
        L = int(nm.split()[1])
        start = TH_BEST if "best_of" in nm else TH_SU
        dl = torch.zeros(a.rate_n, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=a.lr)
        for _ in range(L):
            t = start[RATE] + dl
            R = S.rates(F[RATE], G[RATE], hd[RATE], torch.cos(t),
                        torch.sin(t), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        th = start[RATE] + dl.detach()
    return S.rates(F[RATE], G[RATE], hd[RATE], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


say(f"{'method':>20}{'rate':>9}{'p05':>8}{'p50':>8}{'p95':>8}{'max':>8}"
    f"{'in budget':>11}")
say("-" * 72)
rows = []
for nm, fn in METHODS:
    ts = []
    for i in range(a.scenarios):
        t0 = time.perf_counter()
        fn(i)
        ts.append((time.perf_counter() - t0) * 1e3)
    qs = [rate_batched(nm)]
    ts = np.array(ts)
    frac = float((ts <= TC).mean())
    rows.append(dict(method=nm, rate=float(np.mean(qs)),
                     p05=float(np.percentile(ts, 5)),
                     p50=float(np.percentile(ts, 50)),
                     p95=float(np.percentile(ts, 95)),
                     max=float(ts.max()), in_budget=frac))
    say(f"{nm:>20}{np.mean(qs):9.4f}{np.percentile(ts,5):8.1f}"
        f"{np.percentile(ts,50):8.1f}{np.percentile(ts,95):8.1f}"
        f"{ts.max():8.1f}{100*frac:10.0f}%")

load_after = load_per_core()
say(f"\nload per core after: {load_after:.2f}")
busy = max(load_before, load_after) > a.max_load
if busy:
    say("  *** MACHINE WAS BUSY -- these latencies are inflated and must "
        "not be quoted. Rerun on an idle box. ***")

ok = [r for r in rows if r["in_budget"] >= 0.9]
if ok:
    w = max(ok, key=lambda r: r["rate"])
    say(f"\nbest method with >=90% of runs inside {TC:.1f} ms : "
        f"{w['method']}  rate {w['rate']:.4f}  p50 {w['p50']:.1f} ms")
    say("  (>=90%, not a point median: the 16-step row straddles the budget")
    say("   and a median alone decides the headline by luck)")
else:
    say(f"\nno method keeps 90% of runs inside {TC:.1f} ms")

json.dump(dict(config=vars(a), coherence_ms=TC, rows=rows,
               threads=NTHREADS,
               load_before=load_before, load_after=load_after,
               trustworthy=not busy),
          open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
