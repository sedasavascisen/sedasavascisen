"""
Exact element-wise coordinate ascent for single-user MISO with an RIS.

With one user the regularised-ZF precoder reduces to matched filtering, so
the rate is log2(1 + P ||h(theta)||^2 / sigma^2) with
    h(theta) = h_d + sum_n v_n b_n,   b_n = g_n F_n in C^T,  v_n = e^{j theta_n}.
Holding all other elements fixed, ||c + v_n b_n||^2 is maximised by
    theta_n = -angle(b_n c^H),   c = h_d + sum_{m != n} v_m b_m,
so each update is exact and the objective never decreases. Several starts
(SU alignment plus random) are run and the best kept.
"""
import torch


def cascade(F, G, hd):
    """F [S,N,T], G [S,1,N], hd [S,1,T] -> a [S,T], B [S,N,T]."""
    return hd[:, 0, :], G[:, 0, :, None] * F


def gain(theta, a, B):
    h = a + (torch.exp(1j * theta.to(torch.complex64))[..., None] * B).sum(1)
    return (h.abs() ** 2).sum(-1)


def coord_ascent(a, B, theta0, sweeps=30, tol=1e-7):
    th = theta0.clone()
    v = torch.exp(1j * th.to(torch.complex64))
    h = a + (v[..., None] * B).sum(1)
    prev = (h.abs() ** 2).sum(-1)
    for _ in range(sweeps):
        for n in range(B.shape[1]):
            c = h - v[:, n, None] * B[:, n]
            z = (B[:, n] * c.conj()).sum(-1)
            th[:, n] = -torch.angle(z)
            v[:, n] = torch.exp(1j * th[:, n].to(torch.complex64))
            h = c + v[:, n, None] * B[:, n]
        cur = (h.abs() ** 2).sum(-1)
        if torch.all((cur - prev) <= tol * cur):
            break
        prev = cur
    return th, (h.abs() ** 2).sum(-1)


def su_align(a, B):
    """Closed-form alignment that ignores coupling: each b_n aligned to a."""
    ref = a / (a.norm(dim=-1, keepdim=True) + 1e-30)
    return -torch.angle((B * ref[:, None, :].conj()).sum(-1))


def solve(a, B, restarts=3, sweeps=30, seed=0):
    g = torch.Generator().manual_seed(seed)
    best_th, best = coord_ascent(a, B, su_align(a, B), sweeps)
    for _ in range(restarts):
        t0 = (torch.rand(B.shape[:2], generator=g) * 2 - 1) * torch.pi
        th, val = coord_ascent(a, B, t0, sweeps)
        up = val > best
        best = torch.where(up, val, best)
        best_th = torch.where(up[:, None], th, best_th)
    return torch.remainder(best_th + torch.pi, 2 * torch.pi) - torch.pi, best
