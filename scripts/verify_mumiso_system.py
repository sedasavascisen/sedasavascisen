"""Verify mumiso.system against the independently checked numpy reference."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso import system as S

torch.manual_seed(0); rng = np.random.default_rng(0)
def cn(*s): return (rng.normal(size=s)+1j*rng.normal(size=s))/np.sqrt(2)

print("=== 1) single-user reduction: general form vs published Eq. (8) ===")
N = 32
F = cn(1, N, 1); G = cn(1, 1, N); hd = cn(1, 1, 1)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
a = (G[0, 0] * F[0, :, 0])
th_gen = S.su_align_phase(tF, tG, tH)[0, 0].numpy()
th_eq8 = -np.angle(a)
def gain(th):
    c = torch.tensor(np.cos(th))[None]; s = torch.tensor(np.sin(th))[None]
    return S.effective_channel(tF, tG, tH, c, s).abs().item() ** 2
bound = (abs(hd[0, 0, 0]) + np.abs(a).sum()) ** 2
print(f"  general form / bound : {gain(th_gen)/bound:.4f}   (expect 1.0000)")
print(f"  Eq. (8)      / bound : {gain(th_eq8)/bound:.4f}   (expect < 1)")

print("\n=== 2) ZF nulls interference ===")
B, N, T, K = 4, 32, 8, 4
F = cn(B, N, T); G = cn(B, K, N); hd = cn(B, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
th = torch.tensor(rng.uniform(-np.pi, np.pi, (B, N)))
He = S.effective_channel(tF, tG, tH, torch.cos(th), torch.sin(th))
W = S.zf(He, 1.0)
A = (He @ W).abs() ** 2
off = A - torch.diag_embed(torch.diagonal(A, dim1=-2, dim2=-1))
print(f"  max leakage : {off.abs().max().item():.3e}   (expect ~0)")
print(f"  ||W||_F^2   : {(W.abs()**2).sum((-1,-2)).mean().item():.6f}   (expect 1.0)")
W = S.mrt(He, 1.0)
print(f"  MRT ||W||_F^2: {(W.abs()**2).sum((-1,-2)).mean().item():.6f}   (expect 1.0)")

print("\n=== 3) rate gradient vs finite differences ===")
B, N, T, K = 2, 16, 4, 3
F = cn(B, N, T); G = cn(B, K, N); hd = cn(B, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
th0 = rng.uniform(-np.pi, np.pi, (B, N))
def f(t, grad=False):
    tt = torch.tensor(t, requires_grad=grad)
    R = S.rates(tF, tG, tH, torch.cos(tt), torch.sin(tt), 1.0, 1e-3)
    return R.min(-1).values.sum(), tt
v, tt = f(th0, True); v.backward()
g_auto = tt.grad.numpy().copy()
eps = 1e-6; g_fd = np.zeros_like(th0)
for b in range(B):
    for n in range(N):
        tp = th0.copy(); tp[b, n] += eps
        tm = th0.copy(); tm[b, n] -= eps
        g_fd[b, n] = (f(tp)[0].item() - f(tm)[0].item()) / (2*eps)
d = np.abs(g_auto - g_fd).max()
print(f"  max abs diff : {d:.3e}   relative {d/np.abs(g_fd).max():.3e}  (expect <1e-5)")

print("\n=== 4) raw (non-unit) network output is scale invariant ===")
c = torch.tensor(np.cos(th0)); s = torch.tensor(np.sin(th0))
gsc = torch.tensor(rng.uniform(0.2, 5.0, (B, N)))
R1 = S.rates(tF, tG, tH, *S.unit_phase(c, s), 1.0, 1e-3)
R2 = S.rates(tF, tG, tH, *S.unit_phase(gsc*c, gsc*s), 1.0, 1e-3)
print(f"  max diff : {(R1-R2).abs().max().item():.3e}   (expect ~0)")

print("\n=== 5) straight-through quantiser: value rounds, gradient passes ===")
for bits in (1, 2, 3):
    cc = torch.tensor(np.cos(th0), requires_grad=True)
    ss = torch.tensor(np.sin(th0), requires_grad=True)
    cq, sq = S.quantise_ste(cc, ss, bits)
    tq = torch.atan2(sq, cq).detach().numpy()
    step = 2*np.pi/(2**bits)
    on_grid = np.abs(tq/step - np.round(tq/step)).max()
    cq.sum().backward()
    # d cos(theta_q)/d cos(theta) should equal d cos(theta)/d cos(theta) route
    print(f"  {bits}-bit: on grid (max dev) {on_grid:.2e}   grad finite "
          f"{bool(np.isfinite(cc.grad.numpy()).all())}   "
          f"grad nonzero {bool(np.abs(cc.grad.numpy()).max()>0)}")

print("\n=== 6) soft min is a tight lower bound on the true min ===")
R = torch.tensor(16.0 + rng.normal(0, .5, (64, 4)), dtype=torch.float32)
for beta in (4., 8., 16.):
    sm = -torch.logsumexp(-beta*R, dim=-1)/beta
    tm = R.min(-1).values
    print(f"  beta={beta:4.0f}: gap to true min  mean {(tm-sm).mean():.4f}  "
          f"max {(tm-sm).max():.4f}   bound log(K)/beta = {np.log(4)/beta:.4f}")
