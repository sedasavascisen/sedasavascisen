"""
Does the mobile channel actually age, and at the right rate?

Three things have to hold before the aging curve means anything:
  1. shapes, and F really is constant in time
  2. the channel changes CONTINUOUSLY -- consecutive snapshots are
     correlated, not independent draws. If the per-path gains leaked into
     the time loop this check fails and the whole experiment is measuring
     nothing but fresh randomness.
  3. it decorrelates on the timescale the coherence time predicts. At 3 GHz
     and 1.5 m/s the user covers 0.42 wavelengths in 28 ms, and Jakes'
     model gives J0(2*pi*0.42) = -0.05, i.e. essentially no correlation
     left. A generator that still correlates at 0.95 after 28 ms would make
     every classical method look usable.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

TIMES = (0.0, 1.0, 2.0, 5.0, 10.0, 14.1, 20.0, 28.2, 40.0, 60.0, 100.0,
         200.0, 500.0, 1500.0, 5600.0)

panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES})
ch = MobileMuMisoChannel(panel, cfg)
d = ch.generate(300)
N, T, K = panel.positions.shape[0], cfg.n_bs_antennas, cfg.n_users
M = len(TIMES)
lam = panel.lam

print("=== 1) shapes ===")
print(f"  F    {d['F'].shape}      expected (300, {N}, {T})")
print(f"  G_t  {d['G_t'].shape}  expected (300, {M}, {K}, {N})")
print(f"  hd_t {d['hd_t'].shape}  expected (300, {M}, {K}, {T})")
print(f"  ue_t {d['ue_t'].shape}  expected (300, {M}, {K}, 3)")

print("\n=== 2) does the user actually move, and F stay still? ===")
step = np.linalg.norm(d["ue_t"][:, 1] - d["ue_t"][:, 0], axis=-1).mean()
print(f"  mean displacement over first {TIMES[1]} ms : {100*step:.2f} cm"
      f"   (expected {100*cfg.velocity*TIMES[1]/1e3:.2f} cm)")
tot = np.linalg.norm(d["ue_t"][:, -1] - d["ue_t"][:, 0], axis=-1).mean()
print(f"  mean displacement over {TIMES[-1]:.0f} ms       : {tot:.2f} m")
print(f"  F has no time axis: {d['F'].ndim == 3}")

print("\n=== 3) temporal correlation of G (continuity + decorrelation) ===")


def corr(a, b):
    a = a.reshape(a.shape[0], -1)
    b = b.reshape(b.shape[0], -1)
    num = np.abs(np.sum(a * np.conj(b), axis=-1))
    den = np.sqrt(np.sum(np.abs(a) ** 2, -1) * np.sum(np.abs(b) ** 2, -1))
    return float(np.mean(num / np.maximum(den, 1e-30)))


print(f"  {'t [ms]':>9}{'disp [lam]':>12}{'|corr| to t=0':>15}"
      f"{'Jakes J0':>10}")
from numpy import i0  # noqa: F401  (only to keep numpy import obvious)
try:
    from scipy.special import j0 as _j0
except Exception:
    def _j0(x):
        # small-series fallback, accurate enough for the comparison
        return np.sum([(-1) ** k * (x / 2) ** (2 * k) /
                       (np.math.factorial(k) ** 2) for k in range(25)], axis=0)
for m in range(M):
    disp = cfg.velocity * TIMES[m] / 1e3 / lam
    print(f"  {TIMES[m]:9.1f}{disp:12.3f}{corr(d['G_t'][:, m], d['G_t'][:, 0]):15.4f}"
          f"{_j0(2*np.pi*disp):10.3f}")
print("  (the point is the ORDER: high near 0, gone by a fraction of a")
print("   wavelength. An exact Jakes match is not expected -- this is a")
print("   specular + cluster geometry, not an isotropic 2-D field.)")

print("\n=== 4) consecutive snapshots are not independent draws ===")
c_adj = corr(d["G_t"][:, 1], d["G_t"][:, 0])
# an independent redraw, for reference: shuffle scenarios
perm = np.random.default_rng(0).permutation(300)
c_ind = corr(d["G_t"][:, 0][perm], d["G_t"][:, 0])
print(f"  |corr| t=0 vs t={TIMES[1]} ms          : {c_adj:.4f}")
print(f"  |corr| between DIFFERENT scenarios : {c_ind:.4f}")
ok = c_adj > 0.5 and c_ind < 0.2
print(f"  continuity holds: {ok}"
      + ("" if ok else "   <-- gains are leaking into the time loop"))

print("\n=== 5) does a phase fixed at t=0 lose rate as the user walks? ===")
F = torch.as_tensor(d["F"], dtype=torch.complex64)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
G0 = torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64)
H0 = torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64)
_, th0 = B.su_best_of(F, G0, H0, pt, nv)
print(f"  {'t [ms]':>9}{'min rate':>11}{'of t=0':>9}")
r0 = None
for m in range(M):
    Gm = torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64)
    Hm = torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64)
    r = S.rates(F, Gm, Hm, torch.cos(th0), torch.sin(th0), pt, nv,
                "zf").min(-1).values.mean().item()
    r0 = r if r0 is None else r0
    print(f"  {TIMES[m]:9.1f}{r:11.4f}{r/r0:9.3f}")
