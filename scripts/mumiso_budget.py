"""
The fair comparison: equal budget.

Reporting "the learned model reaches 60% of a 1000-step optimiser" is true
but uninteresting -- of course a thousand steps beats eight. The question a
thesis can defend is whether the LEARNED update rule beats a PLAIN gradient
step when both are given the same number of evaluations.

So: unroll the learned model for L steps, and run plain Adam from the same
anchor for L steps, and compare. Then report wall-clock against the full
optimiser so the latency claim is grounded rather than asserted.
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
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--samples", type=int, default=3000)
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="budget")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH0 = B.su_average(F, G, hd, pt, nv)
tr, va, te = split_indices(a.samples, seed=0)
ev = te[:a.eval_n]


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode=a.mode, use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()
say(f"loaded {a.ckpt}   N={N} T={a.tx} K={a.users}  eval on {len(ev)}")
say(f"anchor su_average : {mr(TH0[ev], ev):.4f}\n")

res = dict(config=vars(a), equal_budget={}, latency={})

# ------------------------------------------------- equal-budget comparison
say("=== equal budget: L learned steps vs L plain Adam steps ===")
say(f"{'L':>4}{'learned':>11}{'plain Adam':>13}{'Adam/su lr=.05':>17}")
say("-" * 45)
with torch.no_grad():
    _, trace = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev],
                   return_trace=True)

for L in range(1, a.steps + 1):
    # plain Adam, same start, same number of objective evaluations
    dl = torch.zeros(len(ev), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.05)
    for _ in range(L):
        th = TH0[ev] + dl
        R = S.rates(F[ev], G[ev], hd[ev], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    plain = mr(TH0[ev] + dl.detach(), ev)
    # a larger step size, since 8 steps at lr 0.05 barely moves
    dl2 = torch.zeros(len(ev), N, requires_grad=True)
    opt2 = torch.optim.Adam([dl2], lr=0.5)
    for _ in range(L):
        th = TH0[ev] + dl2
        R = S.rates(F[ev], G[ev], hd[ev], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt2.zero_grad()
        loss.backward()
        opt2.step()
    big = mr(TH0[ev] + dl2.detach(), ev)
    res["equal_budget"][L] = dict(learned=trace[L - 1], adam_lr05=plain,
                                  adam_lr5=big)
    say(f"{L:4d}{trace[L-1]:11.4f}{plain:13.4f}{big:17.4f}")

say("\n=== for reference, the full optimisers on the same scenarios ===")
t0 = time.time()
R_cd, _ = B.coord_descent(F[ev], G[ev], hd[ev], pt, nv)
cd = S.rate_metrics(R_cd)["min_rate"]
t_cd_all = time.time() - t0
t0 = time.time()
R_ao, _ = B.ao(F[ev], G[ev], hd[ev], pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
t_ao_all = time.time() - t0
say(f"  coord descent (8 sweeps x 16 grid) : {cd:.4f}   ({t_cd_all:.0f}s "
    f"for {len(ev)})")
say(f"  AO (3 starts x 1000 Adam steps)    : {ao:.4f}   ({t_ao_all:.0f}s "
    f"for {len(ev)})")
res["cd"], res["ao"] = cd, ao
res["learned_final"] = trace[-1]
say(f"  learned, {a.steps} steps                  : {trace[-1]:.4f}")
say(f"  -> learned / AO = {trace[-1]/ao:.3f},  learned / CD = {trace[-1]/cd:.3f}")

# ---------------------------------------------------------------- latency
say("\n=== latency, single scenario, CPU, batch size 1 ===")
one = slice(0, 1)
with torch.no_grad():
    for _ in range(3):
        net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])


def timeit(fn, reps):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return np.array(ts) * 1e3


def run_net():
    with torch.no_grad():
        net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])


t_net = timeit(run_net, 20)
t_su = timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)
t_cd = timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)
t_ao = timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 2)
for nm, t in [(f"learned ({a.steps} steps)", t_net), ("su_average", t_su),
              ("coord descent", t_cd), ("AO", t_ao)]:
    res["latency"][nm] = dict(p50=float(np.percentile(t, 50)),
                              p95=float(np.percentile(t, 95)))
    say(f"  {nm:>22}  p50 {np.percentile(t,50):9.2f} ms   "
        f"p95 {np.percentile(t,95):9.2f} ms")
sp_ao = (res["latency"]["AO"]["p50"]
         / res["latency"][f"learned ({a.steps} steps)"]["p50"])
sp_cd = (res["latency"]["coord descent"]["p50"]
         / res["latency"][f"learned ({a.steps} steps)"]["p50"])
say(f"  -> learned is {sp_ao:.0f}x faster than AO and {sp_cd:.0f}x faster "
    f"than CD at the median")
res["speedup_vs_ao"], res["speedup_vs_cd"] = sp_ao, sp_cd

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
