"""
Compiled (numba) coordinate descent for jury question 1 ("would the ranking change if CD were written in C?").
Same algorithm as ris_mu.mumiso.baselines.coord_descent (16-level grid, up to 8 sweeps, hard max-min objective,
strict improvement, start from SU-average, per-scenario early stop when a sweep improves by < 1e-7), same system
equations as ris_mu.mumiso.system (effective channel h_d + g diag(v) F, regularised ZF with lam = K nv / pt,
Frobenius power normalisation, SINR with interference + noise). One scenario per call, complex128.

  cd_direct       recomputes the effective channel for every trial (the torch algorithm, compiled)
  cd_incremental  rank-1 update of the effective channel per trial (what a careful C implementation does)

early=False runs exactly `sweeps` sweeps (timing without the per-scenario early stop; deviation 2).
Shapes (one scenario): F [N, T], G [K, N], hd [K, T]. Returns theta [N] (float64).
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _inv(M):
    """Gauss-Jordan inverse with partial pivoting (no BLAS/LAPACK; K x K, K small)."""
    K = M.shape[0]
    a = M.copy()
    inv = np.zeros_like(M)
    for k in range(K):
        inv[k, k] = 1.0
    for c in range(K):
        p = c
        for r in range(c + 1, K):
            if abs(a[r, c]) > abs(a[p, c]):
                p = r
        if p != c:
            for j in range(K):
                a[c, j], a[p, j] = a[p, j], a[c, j]
                inv[c, j], inv[p, j] = inv[p, j], inv[c, j]
        piv = a[c, c]
        for j in range(K):
            a[c, j] /= piv
            inv[c, j] /= piv
        for r in range(K):
            if r != c:
                f = a[r, c]
                for j in range(K):
                    a[r, j] -= f * a[c, j]
                    inv[r, j] -= f * inv[c, j]
    return inv


@njit(cache=True)
def _minrate(He, pt, nv):
    K, T = He.shape
    M = np.zeros((K, K), dtype=He.dtype)
    for i in range(K):
        for j in range(K):
            acc = 0j
            for t in range(T):
                acc += He[i, t] * np.conj(He[j, t])
            M[i, j] = acc
    lam = K * nv / pt
    for k in range(K):
        M[k, k] += lam
    Mi = _inv(M)
    W = np.zeros((T, K), dtype=He.dtype)          # He^H Mi
    for t in range(T):
        for k in range(K):
            acc = 0j
            for i in range(K):
                acc += np.conj(He[i, t]) * Mi[i, k]
            W[t, k] = acc
    s = 0.0
    for t in range(T):
        for k in range(K):
            s += W[t, k].real ** 2 + W[t, k].imag ** 2
    sc = np.sqrt(pt) / max(np.sqrt(s), 1e-30)
    A = np.zeros((K, K), dtype=He.dtype)
    for i in range(K):
        for j in range(K):
            acc = 0j
            for t in range(T):
                acc += He[i, t] * W[t, j]
            A[i, j] = acc * sc
    best = 1e300
    for k in range(K):
        sig = A[k, k].real ** 2 + A[k, k].imag ** 2
        tot = 0.0
        for j in range(K):
            tot += A[k, j].real ** 2 + A[k, j].imag ** 2
        r = np.log2(1.0 + sig / (tot - sig + nv))
        if r < best:
            best = r
    return best


@njit(cache=True)
def _eff(F, G, hd, th):
    K, N = G.shape
    T = F.shape[1]
    He = hd.copy()
    for n in range(N):
        v = np.cos(th[n]) + 1j * np.sin(th[n])
        for k in range(K):
            gv = G[k, n] * v
            for t in range(T):
                He[k, t] += gv * F[n, t]
    return He


@njit(cache=True)
def cd_direct(F, G, hd, th0, pt, nv, sweeps, grid, early=True):
    N = F.shape[0]
    cand = np.linspace(-np.pi, np.pi, grid + 1)[:-1]
    th = th0.copy()
    cur = _minrate(_eff(F, G, hd, th), pt, nv)
    for _ in range(sweeps):
        start = cur
        for n in range(N):
            best_v, best_c = cur, th[n]
            for c in cand:
                old = th[n]; th[n] = c
                v = _minrate(_eff(F, G, hd, th), pt, nv)
                th[n] = old
                if v > best_v:
                    best_v, best_c = v, c
            th[n] = best_c; cur = best_v
        if early and cur - start < 1e-7:
            break
    return th


@njit(cache=True)
def cd_incremental(F, G, hd, th0, pt, nv, sweeps, grid, early=True):
    N = F.shape[0]
    K = G.shape[0]
    T = F.shape[1]
    cand = np.linspace(-np.pi, np.pi, grid + 1)[:-1]
    th = th0.copy()
    He = _eff(F, G, hd, th)
    cur = _minrate(He, pt, nv)
    trial = np.empty_like(He)
    for _ in range(sweeps):
        start = cur
        for n in range(N):
            vold = np.cos(th[n]) + 1j * np.sin(th[n])
            best_v, best_c = cur, th[n]
            for c in cand:
                dv = (np.cos(c) + 1j * np.sin(c)) - vold
                for k in range(K):
                    gd = G[k, n] * dv
                    for t in range(T):
                        trial[k, t] = He[k, t] + gd * F[n, t]
                v = _minrate(trial, pt, nv)
                if v > best_v:
                    best_v, best_c = v, c
            if best_c != th[n]:
                dv = (np.cos(best_c) + 1j * np.sin(best_c)) - vold
                for k in range(K):
                    gd = G[k, n] * dv
                    for t in range(T):
                        He[k, t] += gd * F[n, t]
                th[n] = best_c
            cur = best_v
        if early and cur - start < 1e-7:
            break
    return th


def run_batch(fn, F, G, hd, th0, pt, nv, sweeps=8, grid=16, cdt=np.complex128, rdt=np.float64):
    """torch/numpy batch -> numpy [S, N]; loops scenarios. cdt/rdt: precision (complex64/float32 = torch's)."""
    F, G, hd, th0 = (np.asarray(x) for x in (F, G, hd, th0))
    out = np.empty(th0.shape, dtype=np.float64)
    for s in range(F.shape[0]):
        out[s] = fn(F[s].astype(cdt), G[s].astype(cdt), hd[s].astype(cdt),
                    th0[s].astype(rdt), float(pt), float(nv), sweeps, grid)
    return out
