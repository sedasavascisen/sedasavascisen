"""
NumPy port of Paper 1's channel generator (RIS_dataset_large_2D.m; zip copy,
md5 98cdc170b8feac42ff16b8834ec70916). Same model and parameters:
8x4 (or larger) horizontal panel at (20,10,3) m, lambda/2 spacing, fc = 3 GHz,
TX/RX uniform in a 40x20 m room at 1-2 m height, 6 scatterers, gain 0.15,
per-element CN(0,1) LoS coefficient, label theta_n = wrapToPi(-angle(F_n)-angle(G_n)).

NOT bit-identical to MATLAB: the random stream (NumPy PCG64 vs MATLAB
Mersenne twister, and the draw order) differs, so every number obtained with
this port is an independent draw from the same distribution ("bağımsız çekiliş").
"""
import numpy as np

FC, C = 3e9, 3e8
LAM = C / FC
K_WAVE = 2 * np.pi / LAM
ROOM = np.array([40.0, 20.0, 6.0])
SHAPES = {32: (8, 4), 64: (8, 8), 128: (16, 8), 256: (16, 16)}


def element_positions(N=32):
    M, K = SHAPES[N]
    d = LAM / 2
    ctr = np.array([ROOM[0] / 2, ROOM[1] / 2, 3.0])
    x0, y0 = ctr[0] - (M - 1) / 2 * d, ctr[1] - (K - 1) / 2 * d
    return np.array([[x0 + i * d, y0 + j * d, ctr[2]] for i in range(M) for j in range(K)])   # n = (i-1)K + j


def generate(n, N=32, seed=42, n_scatter=6, scatter_g=0.15):
    rng = np.random.default_rng(seed)
    cn = lambda *s: (rng.standard_normal(s) + 1j * rng.standard_normal(s)) / np.sqrt(2)
    pos = element_positions(N)
    F = np.zeros((n, N), complex); G = np.zeros((n, N), complex); hd = np.zeros(n, complex)
    for s in range(n):
        tx = np.r_[rng.random(2) * ROOM[:2], 1 + rng.random()]
        rx = np.r_[rng.random(2) * ROOM[:2], 1 + rng.random()]
        sc = rng.random((n_scatter, 3)) * ROOM
        dd = np.linalg.norm(tx - rx)
        hd[s] = cn(1)[0] * np.exp(-1j * K_WAVE * dd) / dd
        dtx = np.linalg.norm(tx - pos, axis=1); drx = np.linalg.norm(pos - rx, axis=1)
        f0 = cn(N) * np.exp(-1j * K_WAVE * dtx) / dtx
        g0 = cn(N) * np.exp(-1j * K_WAVE * drx) / drx
        da = np.linalg.norm(tx - sc, axis=1)[:, None]
        db = np.linalg.norm(sc[:, None] - pos, axis=2)
        dc = np.linalg.norm(sc - rx, axis=1)[:, None]
        F[s] = f0 + (scatter_g * cn(n_scatter, N) * np.exp(-1j * K_WAVE * (da + db)) / (da * db)).sum(0)
        G[s] = g0 + (scatter_g * cn(n_scatter, N) * np.exp(-1j * K_WAVE * (db + dc)) / (db * dc)).sum(0)
    theta = np.angle(np.exp(1j * (-np.angle(F) - np.angle(G))))
    return dict(F=F, G=G, hd=hd, theta=theta, N=N, seed=seed)


def split(n, seed=42):
    """70/15/15 as in theta_NN_multioutput.m (random permutation; NumPy stream, not MATLAB's)."""
    idx = np.random.default_rng(seed).permutation(n)
    a, b = round(0.70 * n), round(0.15 * n)
    return idx[:a], idx[a:a + b], idx[a + b:]
