"""
Double-check of this project's own conclusion.

The conclusion was: tuned Adam dominates the learned update rule on the
latency-quality frontier. But the step size 0.5 was picked by trying two
values and looking at the SAME scenarios the comparison is reported on,
while the learned model was trained on a train split and reported on test.
That tilts the comparison toward Adam, which happens to be the direction
the conclusion went -- exactly the shape of error worth hunting for.

So: sweep the step size on a VALIDATION split, freeze the winner, and
report on test. Same protocol for both methods. Also check whether the
conclusion survives a per-scenario-tuned Adam (an upper bound Adam could
never reach in deployment) and a badly tuned one (a lower bound).
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
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--tag", default="audit_fair")
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
tr, va, te = split_indices(a.samples, seed=0)
VA, TE = va[:400], te[:400]

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()


def adam_phase(ids, L, lr):
    dl = torch.zeros(len(ids), N, requires_grad=True)
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


res = dict(config=vars(a))

# ------------------------------------------------- 1) step size, honestly
say("=== 1) Adam step size chosen on VALIDATION, reported on TEST ===")
grid = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 2.0]
say(f"{'lr':>6}" + "".join(f"{'L='+str(L):>10}" for L in (8, 16, 32)))
say("-" * 36)
best = {}
for L in (8, 16, 32):
    best[L] = (None, -np.inf)
rows = {}
for lr in grid:
    rows[lr] = {}
    for L in (8, 16, 32):
        q = rate_of(adam_phase(VA, L, lr), VA)
        rows[lr][L] = q
        if q > best[L][1]:
            best[L] = (lr, q)
    say(f"{lr:6.2f}" + "".join(f"{rows[lr][L]:10.4f}" for L in (8, 16, 32)))
say("")
res["val_sweep"] = {str(k): v for k, v in rows.items()}
res["chosen_lr"] = {str(L): best[L][0] for L in best}
for L in (8, 16, 32):
    say(f"  L={L:2d}: validation picks lr={best[L][0]}  "
        f"(val {best[L][1]:.4f})")

say("\n=== 2) TEST, with the step size frozen from validation ===")
with torch.no_grad():
    th_net = net(X[TE], F[TE], G[TE], hd[TE], pt, nv, TH0[TE])
q_net = rate_of(th_net, TE)
say(f"  learned, {a.steps} steps                 : {q_net:.4f}")
res["test"] = {"learned": q_net}
for L in (8, 16, 32):
    lr = best[L][0]
    q = rate_of(adam_phase(TE, L, lr), TE)
    res["test"][f"adam_L{L}"] = q
    res["test"][f"adam_L{L}_lr"] = lr
    say(f"  Adam, {L:2d} steps, lr={lr:<4} (from val) : {q:.4f}")

say("\n=== 3) bounds: how much does step-size tuning even matter? ===")
for L in (8, 16):
    qs = [rate_of(adam_phase(TE, L, lr), TE) for lr in grid]
    say(f"  L={L:2d}: worst lr {min(qs):.4f}   best lr {max(qs):.4f}   "
        f"spread {max(qs)-min(qs):.4f}")
    res[f"test_spread_L{L}"] = dict(worst=min(qs), best=max(qs))

say("\n=== 4) per-scenario lr (an upper bound Adam cannot reach live) ===")
for L in (8, 16):
    per = torch.stack([
        S.rates(F[TE], G[TE], hd[TE],
                torch.cos(adam_phase(TE, L, lr)),
                torch.sin(adam_phase(TE, L, lr)), pt, nv,
                "zf").min(-1).values
        for lr in grid])
    say(f"  L={L:2d}: per-scenario best lr -> {per.max(0).values.mean():.4f}")
    res[f"oracle_lr_L{L}"] = float(per.max(0).values.mean())

say("\n=== 5) latency, same protocol ===")


def timeit(fn, reps):
    for _ in range(3):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.percentile(np.array(ts) * 1e3, 50))


one = TE[:1]
t_net = timeit(lambda: net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one]),
               20)
say(f"  learned, {a.steps} steps : {t_net:7.2f} ms")
res["latency"] = {"learned": t_net}
for L in (8, 16, 32):
    t = timeit(lambda: adam_phase(one, L, best[L][0]), 8)
    res["latency"][f"adam_L{L}"] = t
    say(f"  Adam, {L:2d} steps      : {t:7.2f} ms")

say("\n=== VERDICT ===")
tc = 0.423 / (1.5 * panel.fc / 3e8) * 1e3
say(f"  coherence budget : {tc:.1f} ms")
dominated = False
for L in (8, 16, 32):
    q, t = res["test"][f"adam_L{L}"], res["latency"][f"adam_L{L}"]
    if q >= q_net and t <= t_net:
        dominated = True
        say(f"  Adam L={L} (lr={best[L][0]}) dominates the learned model: "
            f"{q:.4f} at {t:.1f} ms vs {q_net:.4f} at {t_net:.1f} ms")
if not dominated:
    say("  no Adam setting dominates the learned model under this protocol "
        "-- the earlier conclusion was too strong")
in_budget = [(f"Adam L={L}", res["test"][f"adam_L{L}"],
              res["latency"][f"adam_L{L}"])
             for L in (8, 16, 32)
             if res["latency"][f"adam_L{L}"] <= tc]
if t_net <= tc:
    in_budget.append((f"learned L={a.steps}", q_net, t_net))
if in_budget:
    w = max(in_budget, key=lambda r: r[1])
    say(f"  best within budget : {w[0]}  {w[1]:.4f} at {w[2]:.1f} ms")
res["conclusion_holds"] = dominated

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
