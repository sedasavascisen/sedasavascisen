"""
Is the channel -> optimal-phase map learnable at all from these features?

The unsupervised run sits still at the anchor. Two very different causes:
  (A) optimisation -- the averaged objective gradient is uninformative, but
      a good map exists and the network could represent it;
  (B) representability/generalisation -- no such map is learnable from
      these features, so staying at the anchor IS the best the network can
      do and the formulation has to change.

Decisive test: compute per-scenario ORACLE offsets with Adam, then train
the same network SUPERVISED to regress them.
  - cannot even fit the training set  -> capacity / features (B)
  - fits train, fails val             -> the map is too wiggly to generalise (B)
  - fits both, rate high              -> the unsupervised objective is at
                                         fault (A), fixable by a warm start
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch
import torch.nn.functional as Fn

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

torch.manual_seed(0)
NS, KUS, T = 4000, 4, 8
panel, cfg = make_mumiso_scenario(n_users=KUS, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(NS, seed=0)


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


_, th_su = B.su_average(F, G, hd, pt, nv)
print(f"anchor (su_average) on test : {mr(th_su[te], te):.4f}", flush=True)

print("\n=== oracle offsets (Adam, 600 steps, per scenario) ===", flush=True)
t0 = time.time()
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(600):
    th = th_su + dl
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
dl = dl.detach()
th_or = th_su + dl
print(f"  oracle rate on test : {mr(th_or[te], te):.4f}   "
      f"({time.time()-t0:.0f}s)", flush=True)
off = torch.atan2(torch.sin(dl), torch.cos(dl))
print(f"  offset magnitude    : mean |d| {off.abs().mean():.3f} rad, "
      f"std {off.std():.3f}", flush=True)

print("\n=== how wiggly is the map? nearest-neighbour test ===", flush=True)
flat = X.reshape(NS, -1)
sub = torch.randperm(NS)[:800]
Z = Fn.normalize(flat[sub], dim=-1)
sim = Z @ Z.T
sim.fill_diagonal_(-2)
nn_idx = sim.argmax(-1)
tgt = torch.complex(torch.cos(dl[sub]), torch.sin(dl[sub]))
agree = (tgt * tgt[nn_idx].conj()).real.mean().item()
rand_idx = torch.randperm(len(sub))
agree_r = (tgt * tgt[rand_idx].conj()).real.mean().item()
print(f"  cos(offset difference) to NEAREST feature neighbour : {agree:+.4f}")
print(f"  ... to a RANDOM scenario                            : {agree_r:+.4f}")
print("  (both near zero => the required offset is uncorrelated with")
print("   feature similarity, i.e. not a smooth map in this representation)",
      flush=True)

print("\n=== supervised fit of the oracle offsets ===", flush=True)
net = MuMisoNet(N=N, n_users=KUS, n_tx=T, mode="exchange", residual=True)
opt = torch.optim.Adam(net.parameters(), lr=2e-3)
tc, ts = torch.cos(th_or), torch.sin(th_or)
rng = np.random.default_rng(0)
for ep in range(1, 26):
    net.train()
    run, nb = 0.0, 0
    perm = tr[rng.permutation(len(tr))]
    for i in range(0, len(perm), 64):
        j = perm[i:i + 64]
        c, s = net.phases(X[j])
        loss = Fn.mse_loss(torch.stack([c, s]), torch.stack([tc[j], ts[j]]))
        opt.zero_grad()
        loss.backward()
        opt.step()
        run += loss.item()
        nb += 1
    if ep % 5 == 0 or ep == 1:
        net.eval()
        with torch.no_grad():
            ctr, str_ = net.phases(X[tr[:1000]])
            cva, sva = net.phases(X[va])
            e_tr = Fn.mse_loss(torch.stack([ctr, str_]),
                               torch.stack([tc[tr[:1000]],
                                            ts[tr[:1000]]])).item()
            e_va = Fn.mse_loss(torch.stack([cva, sva]),
                               torch.stack([tc[va], ts[va]])).item()
            r_va = mr(torch.atan2(sva, cva), va)
        print(f"  epoch {ep:2d}  train mse {run/nb:.4f}  "
              f"fit mse train {e_tr:.4f} val {e_va:.4f}   "
              f"val rate {r_va:.4f}", flush=True)

net.eval()
with torch.no_grad():
    c, s = net.phases(X[te])
print(f"\n  supervised model on test : {mr(torch.atan2(s, c), te):.4f}")
print(f"  oracle on test           : {mr(th_or[te], te):.4f}")
print(f"  anchor on test           : {mr(th_su[te], te):.4f}")
print("\n  mse 1.0 means the prediction is uncorrelated with the target")
print("  (both are unit vectors), mse 0 is a perfect fit.")
