"""Shapes, array correlation, Ricean K and effective rank of the MU-MISO channel."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   effective_rank, neighbour_corr)
from ris_mu.mumiso import system as S

print("=== 1) shapes, for several (K, T) ===")
for K_u, T in [(4, 4), (1, 4), (4, 1), (1, 1), (6, 8)]:
    panel, cfg = make_mumiso_scenario(n_users=K_u, n_bs_antennas=T, seed=1)
    d = MuMisoChannel(panel, cfg).generate(8)
    N = panel.positions.shape[0]
    ok = (d["F"].shape == (8, N, T) and d["G"].shape == (8, K_u, N)
          and d["hd"].shape == (8, K_u, T))
    print(f"  K={K_u} T={T}: F{d['F'].shape} G{d['G'].shape} hd{d['hd'].shape}"
          f"   {'OK' if ok else 'MISMATCH'}")

print("\n=== 2) diagnostics, K=4 T=4, 600 samples ===")
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=4, seed=7)
d = MuMisoChannel(panel, cfg).generate(600)
N = panel.positions.shape[0]
F, G, hd = d["F"], d["G"], d["hd"]
print(f"  N = {N}, T = {F.shape[-1]}, K = {G.shape[1]}")
print(f"  G effective rank (pooled users) : {effective_rank(G.reshape(-1, N)):6.2f}  (max {N})")
print(f"  G effective rank (user 0)       : {effective_rank(G[:, 0]):6.2f}")
print(f"  F effective rank (antenna 0)    : {effective_rank(F[:, :, 0]):6.2f}"
      f"   <- low is EXPECTED, BS and RIS are static")
print(f"  G neighbour |corr| (n, n+1)     : {neighbour_corr(G.reshape(-1, N)):6.4f}")
print(f"  F neighbour |corr| (n, n+1)     : {neighbour_corr(F[:, :, 0]):6.4f}")

print("\n=== 3) array correlation across ANTENNAS (should be high, not 1) ===")
Ft = F.transpose(0, 2, 1).reshape(-1, F.shape[-1])     # [(S*N), T]
print(f"  antenna-axis neighbour |corr|   : {neighbour_corr(Ft):6.4f}")
print(f"  antenna-axis effective rank     : {effective_rank(Ft):6.4f}  (max {F.shape[-1]})")

print("\n=== 4) Ricean K actually realised (from the 3GPP draw) ===")
print(f"  LoS fraction  BS->RIS : {d['los_ris_bs'].mean():.3f}")
print(f"  LoS fraction  RIS->UE : {d['los_ris_ue'].mean():.3f}")
print(f"  LoS fraction  direct  : {d['los_direct'].mean():.3f}")

print("\n=== 5) link budget sanity: baseline rates ===")
from ris_mu.mumiso.channel import to_torch
tF, tG, tH, rdt = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
print(f"  snr_scale = {cfg.snr_scale():.3e}  ->  noise_var = {nv:.3e}")
rng = np.random.default_rng(0)
def rate(th, prec="zf"):
    t = torch.as_tensor(th, dtype=rdt)
    return S.rates(tF, tG, tH, torch.cos(t), torch.sin(t), pt, nv, prec)
th_r = rng.uniform(-np.pi, np.pi, (600, N))
R_rand = rate(th_r)
th_su = S.su_align_phase(tF, tG, tH)              # [S,K,N]
pw = (np.abs(G) ** 2).sum(-1)
weak = pw.argmin(-1)
th_w = th_su[np.arange(600), weak].numpy()
R_su = rate(th_w)
He0 = tH
W0 = S.zf(He0, pt)
R_nr = torch.log2(1 + S.sinr(He0, W0, nv))
for nm, R in [("no RIS", R_nr), ("random phase", R_rand), ("SU (weakest)", R_su)]:
    m = S.rate_metrics(R)
    print(f"  {nm:14s} min {m['min_rate']:7.3f}   sum {m['sum_rate']:8.3f}  b/s/Hz")
