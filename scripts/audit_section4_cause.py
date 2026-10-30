"""
Independent re-check of the two audit findings that change the advice.

FINDING A -- the stated cause of section 4 is wrong.
The report says the channel-to-phase target is "noise with respect to the
input" because many configurations are near-optimal and which one an
optimiser reaches is arbitrary. That has a one-line test the project never
ran: solve the SAME scenario twice from different starts and see whether
the answers agree. If they do, the target is determined, the multiplicity
story is wrong, and the negative result needs a different explanation.

FINDING B -- the anchor everything is measured against is weak.
su_average is the start for the oracle solve, the unrolled model and every
Adam row. The lazier alternative costs nothing: all K single-user
alignment phases are already computed, so score them plus su_average and
keep the best per scenario.
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, KUS, T = 1200, 4, 8
panel, cfg = make_mumiso_scenario(n_users=KUS, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)                       # [S,K,N]
_, TH_SU = B.su_average(F, G, hd, pt, nv)


def minrate(th):
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values


def solve(start, steps=600, lr=0.05):
    dl = start.clone().requires_grad_(True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(steps):
        th = TH_SU + dl
        R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return (TH_SU + dl.detach()), dl.detach()


print("=== FINDING A: is the optimum determined by the scenario? ===",
      flush=True)
g = torch.Generator().manual_seed(0)
starts = {
    "zeros (project default)": torch.zeros(NS, N),
    "uniform (-pi, pi]": (torch.rand(NS, N, generator=g) * 2 - 1) * np.pi,
    "small gaussian": torch.randn(NS, N, generator=g) * 0.3,
}
sols, offs = {}, {}
for nm, st in starts.items():
    t0 = time.time()
    th, dl = solve(st)
    sols[nm], offs[nm] = th, dl
    print(f"  {nm:<24} rate {minrate(th).mean():.4f}   "
          f"({time.time()-t0:.0f}s)", flush=True)

keys = list(starts)
print("\n  agreement = mean cos(phase difference), per element")
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = sols[keys[i]], sols[keys[j]]
        same = torch.cos(a - b).mean().item()
        perm = torch.randperm(NS, generator=g)
        diff = torch.cos(a - b[perm]).mean().item()
        print(f"    {keys[i][:18]:<18} vs {keys[j][:18]:<18}  "
              f"SAME scenario {same:+.4f}   DIFFERENT {diff:+.4f}")

print("\n  reading: if SAME is far above DIFFERENT, two independent solves")
print("  land in the same place, the target is determined by the input, and")
print("  'the target is noise w.r.t. the input' is NOT what is happening.")

print("\n=== FINDING B: is su_average a weak anchor? ===", flush=True)
t0 = time.time()
r_su = minrate(TH_SU).mean().item()
# score all K single-user alignments plus su_average, keep the best
cand = torch.cat([phi, TH_SU.unsqueeze(1)], dim=1)          # [S,K+1,N]
scores = torch.stack([minrate(cand[:, k]) for k in range(cand.shape[1])])
best_idx = scores.argmax(0)
th_best = cand[torch.arange(NS), best_idx]
r_best = minrate(th_best).mean().item()
print(f"  su_average               : {r_su:.4f}")
print(f"  best-of-(K+1) per scenario: {r_best:.4f}   "
      f"(+{100*(r_best-r_su)/r_su:.1f}%)   [{time.time()-t0:.1f}s for {NS}]")
chosen = torch.bincount(best_idx, minlength=cand.shape[1]).float() / NS
print(f"  how often each is picked  : "
      + " ".join(f"{100*c:.0f}%" for c in chosen)
      + "   (last entry = su_average)")

print("\n  consequences for the report's framing:")
for L in (8, 16):
    for nm, st in (("su_average", TH_SU), ("best-of-(K+1)", th_best)):
        dl = torch.zeros(NS, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            th = st + dl
            R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        print(f"    {nm:<14} + Adam {L:2d} -> {minrate(st+dl.detach()).mean():.4f}")
print(f"\n  unrolled model's reported gain was 1.112 -> 3.265 = 2.94x over")
print(f"  su_average; over the lazier anchor ({r_best:.3f}) it is "
      f"{3.265/r_best:.2f}x.")
