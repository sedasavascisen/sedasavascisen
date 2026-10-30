"""
Double-check of the precoder fix and the CSI module.

Four suspicions, in order of how much they would change:

  A. Is the MMSE regulariser actually the right default? The sweep that
     exposed the bug showed eps = 1e-12 (absolute) edging out eps = 0, and
     the MMSE choice lands between 1e-12 and 1e-10. "Standard formula" is
     not the same as "best here".

  B. How much does phase optimisation buy AT ALL now? With the precoder
     fixed, su_average reaches 4.624 against a stale floor of 4.315 and a
     best of ~7.1. If a random phase already gets most of the rate, the
     premise of the whole thesis needs stating more carefully.

  C. The CSI error is drawn against ONE global mean power per quantity, so
     within G a weak user takes the same absolute error as a strong one and
     is swamped. Max-min is decided by the weakest user, so this could be
     the real cause of the collapse I blamed entirely on ZF. The docstring
     of csi.py claims the error is "proportional to each link's own
     strength", which is true per quantity and false per user.

  D. `rates_mismatched` calls precode() without noise_var or err_power, so
     it uses the fallback regulariser and is NOT the error-aware precoder
     the module's own docstring describes.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.csi import add_error, db_to_e2

torch.manual_seed(0)
NS = 400
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N, K, T = panel.positions.shape[0], cfg.n_users, cfg.n_bs_antennas
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
_, TH_B = B.su_best_of(F, G, hd, pt, nv)


def rate(th, **kw):
    He = S.effective_channel(F, G, hd, torch.cos(th), torch.sin(th))
    W = S.zf(He, pt, **kw)
    return torch.log2(1 + S.sinr(He, W, nv)).min(-1).values.mean().item()


print("=== A) is the MMSE regulariser the right default? ===")
He = S.effective_channel(F, G, hd, torch.cos(TH_B), torch.sin(TH_B))
p_sig = torch.diagonal(He @ He.conj().transpose(-1, -2),
                       dim1=-2, dim2=-1).real.mean().item()
mmse_abs = K * nv / pt
print(f"  channel scale  mean diag(He He^H) = {p_sig:.3e}")
print(f"  MMSE lambda    K*noise/Pt         = {mmse_abs:.3e}"
      f"   ({mmse_abs/p_sig:.2e} of the diagonal)")
print(f"\n  {'relative eps':>14}{'min rate':>10}")
best = (None, -np.inf)
for e in (0.0, 1e-12, 1e-9, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
    r = rate(TH_B, eps=e) if e > 0 else rate(TH_B, eps_abs=0.0)
    if r > best[1]:
        best = (e, r)
    print(f"  {e:14.0e}{r:10.4f}")
r_mmse = rate(TH_B, noise_var=nv)
print(f"  {'MMSE default':>14}{r_mmse:10.4f}")
print(f"  best swept: relative eps = {best[0]:.0e} -> {best[1]:.4f}")
gap = (best[1] - r_mmse) / best[1]
print(f"  MMSE leaves {100*gap:.2f}% on the table"
      + ("   (negligible)" if abs(gap) < 0.01 else "   <-- CHECK"))

print("\n=== B) how much does phase optimisation buy, with the fix? ===")
g = torch.Generator().manual_seed(0)
th_rand = (torch.rand(NS, N, generator=g) * 2 - 1) * np.pi
rows = [("no RIS", None), ("random phase", th_rand), ("su_average", None),
        ("su_best_of", TH_B), ("PGA", None)]
W0 = S.zf(hd, pt, noise_var=nv)
r_noris = torch.log2(1 + S.sinr(hd, W0, nv)).min(-1).values.mean().item()
_, th_su = B.su_average(F, G, hd, pt, nv)
_, th_pga = B.pga(F, G, hd, pt, nv)
vals = {"no RIS": r_noris, "random phase": rate(th_rand, noise_var=nv),
        "su_average": rate(th_su, noise_var=nv),
        "su_best_of": rate(TH_B, noise_var=nv),
        "PGA": rate(th_pga, noise_var=nv)}
for k, v in vals.items():
    print(f"  {k:>14}{v:10.4f}")
span = vals["PGA"] / max(vals["random phase"], 1e-9)
print(f"  optimised / random phase = {span:.2f}x")
print(f"  random phase / PGA       = {vals['random phase']/vals['PGA']:.2f}"
      f"   <- how much a RANDOM surface already delivers")

print("\n=== C) is the CSI error swamping the weak users? ===")
pw = (G.abs() ** 2).mean(dim=(-1,))              # [B,K] per-user power
spread = (pw.max(-1).values / pw.min(-1).values).median().item()
print(f"  median strongest/weakest user power ratio in G : {spread:.1f}x")
print("  so a single global error scale hits the weakest user"
      f" ~{spread:.0f}x harder, in relative terms\n")


def noisy_peruser(X, e2, gen, per_user_axis=None):
    """Error scaled per-user instead of globally."""
    if e2 <= 0:
        return X
    if per_user_axis is None:
        p = (X.abs() ** 2).mean()
    else:
        p = (X.abs() ** 2).mean(dim=tuple(
            i for i in range(X.ndim) if i != per_user_axis), keepdim=True)
        sh = [1] * X.ndim
        sh[per_user_axis] = X.shape[per_user_axis]
        p = p.reshape(sh)
    z = (torch.randn(X.shape, generator=gen)
         + 1j * torch.randn(X.shape, generator=gen)).to(X.dtype) / 2 ** 0.5
    return ((1 - e2) ** 0.5) * X + (e2 ** 0.5) * z * p.sqrt()


print(f"  {'error':>8}{'global scale':>14}{'per-user scale':>16}")
for db in (-20, -15, -10):
    e2 = db_to_e2(db)
    gg = torch.Generator().manual_seed(7)
    Fg, Gg, Hg = add_error(F, G, hd, e2, gen=gg)
    gg2 = torch.Generator().manual_seed(7)
    Fp = noisy_peruser(F, e2, gg2)
    Gp = noisy_peruser(G, e2, gg2, per_user_axis=1)
    Hp = noisy_peruser(hd, e2, gg2, per_user_axis=1)

    def run(Fe, Ge, He_):
        _, st = B.su_best_of(Fe, Ge, He_, pt, nv)
        dl = torch.zeros(NS, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(8):
            th = st + dl
            R = S.rates(Fe, Ge, He_, torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        th = st + dl.detach()
        Hest = S.effective_channel(Fe, Ge, He_, torch.cos(th), torch.sin(th))
        W = S.zf(Hest, pt, noise_var=nv, err_power=e2)
        Htr = S.effective_channel(F, G, hd, torch.cos(th), torch.sin(th))
        return torch.log2(1 + S.sinr(Htr, W, nv)).min(-1).values.mean().item()
    print(f"  {db:7.0f}d{run(Fg, Gg, Hg):14.4f}{run(Fp, Gp, Hp):16.4f}")
print("  (if the two columns differ a lot, the collapse was partly the")
print("   error model swamping weak users, not only ZF)")

print("\n=== D) does rates_mismatched use the error-aware precoder? ===")
import inspect
from ris_mu.mumiso import csi as C
src = inspect.getsource(C.rates_mismatched)
has = ("err_power" in src) and ("noise_var" in src)
print(f"  passes noise_var / err_power to precode(): {has}"
      + ("" if has else "   <-- NO: uses the fallback regulariser"))
