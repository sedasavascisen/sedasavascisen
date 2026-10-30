"""
The latency-quality frontier, and the coherence-time budget.

This is the script that decided the project's conclusion, so it is worth
running yourself rather than taking the numbers on trust.

It asks the only question that matters for a deployed RIS: at a given
millisecond budget, what is the best min-rate anyone can achieve? Then it
places the learned update rule on that curve. The learned model turns out
NOT to be on the frontier -- tuned gradient ascent reaches a higher rate in
half the time -- which is why the thesis conclusion is framed around the
coherence-time constraint rather than around a neural network.

Coherence time, for reference: a user walking at 1.5 m/s at 3 GHz gives
f_d = v f_c / c = 15 Hz and T_c = 0.423 / f_d = 28 ms.
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
ap.add_argument("--samples", type=int, default=600)
ap.add_argument("--eval-n", type=int, default=450)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--velocity", type=float, default=1.5, help="m/s")
ap.add_argument("--tag", default="frontier")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH0 = B.su_average(F, G, hd, pt, nv)
ev = slice(0, a.eval_n)
one = slice(0, 1)

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()


def adam_phase(ids, L, lr):
    n = len(range(*ids.indices(a.samples)))
    dl = torch.zeros(n, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


def rate_of(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


def timeit(fn, reps):
    for _ in range(3):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.percentile(np.array(ts) * 1e3, 50))


fd = a.velocity * cfg.__dict__.get("fc", 3e9) / 3e8 if False else \
    a.velocity * panel.fc / 3e8
tc = 0.423 / fd * 1e3
say(f"N={N} T={a.tx} K={a.users}, {a.eval_n} scenarios, CPU, batch 1")
say(f"coherence time at {a.velocity} m/s, {panel.fc/1e9:.1f} GHz : "
    f"f_d = {fd:.1f} Hz, T_c = {tc:.1f} ms\n")

rows = []
rows.append(("su_average", rate_of(TH0[ev], ev),
             timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)))
for L in (4, 8, 16, 32, 64, 128):
    rows.append((f"tuned Adam, {L} steps", rate_of(adam_phase(ev, L, a.lr), ev),
                 timeit(lambda: adam_phase(one, L, a.lr), 8)))
with torch.no_grad():
    th_net = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
rows.append((f"learned, {a.steps} steps", rate_of(th_net, ev),
             timeit(lambda: net(X[one], F[one], G[one], hd[one], pt, nv,
                                TH0[one]), 20)))
rows.append(("coord descent", S.rate_metrics(
    B.coord_descent(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)))
rows.append(("AO (cd+su+rnd starts)", S.rate_metrics(
    B.ao(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 2)))
# PGA = 3 purely RANDOM restarts. Measured to be marginally but
# CONSISTENTLY better than ao across four (T,K) settings, so the
# coordinate-descent and su_average starts are not just redundant, they
# are worse than random ones. The honest "strongest classical" is the max
# of the two, which is why both are listed.
rows.append(("PGA (3 random starts)", S.rate_metrics(
    B.pga(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.pga(F[one], G[one], hd[one], pt, nv), 2)))

rows.sort(key=lambda r: r[2])
best_in_budget = max((r for r in rows if r[2] <= tc), key=lambda r: r[1])
say(f"{'method':>22}{'min rate':>11}{'latency p50':>14}{'in budget':>11}")
say("-" * 58)
for nm, q, t in rows:
    fits = "yes" if t <= tc else "NO"
    star = "  <-- best in budget" if (nm, q, t) == best_in_budget else ""
    say(f"{nm:>22}{q:11.4f}{t:12.1f} ms{fits:>11}{star}")

# which points are Pareto optimal
pareto = []
for nm, q, t in rows:
    if not any(q2 >= q and t2 <= t and (nm2 != nm) for nm2, q2, t2 in rows):
        pareto.append(nm)
say(f"\n  Pareto-optimal: {', '.join(pareto)}")
learned = [r for r in rows if r[0].startswith("learned")][0]
say(f"  learned model on the frontier: "
    f"{'yes' if learned[0] in pareto else 'NO -- dominated'}")
strongest = max(rows, key=lambda r: r[1])
say(f"  strongest classical overall : {strongest[0]}  {strongest[1]:.4f} "
    f"at {strongest[2]:.0f} ms")
best_budget_frac = best_in_budget[1] / strongest[1]
say(f"  best-in-budget / strongest  : {best_budget_frac:.3f}")
res_extra = dict(strongest=strongest[0], strongest_rate=strongest[1],
                 best_in_budget_frac=best_budget_frac)

res = dict(**res_extra, config=vars(a), coherence_ms=tc, fd_hz=fd,
           rows=[dict(method=n, min_rate=q, latency_ms=t) for n, q, t in rows],
           pareto=pareto, best_in_budget=best_in_budget[0])
with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
