"""
Partial CSI from a reduced pilot budget (pre-registered: ON_KAYIT_KISMI_CSI.md).

Observation model (ON/OFF cascaded estimation, noiseless): pilot 0 with all
elements off gives the direct channel a; pilot i with only observed element
n_i on gives b_{n_i}. M observed elements cost M + 1 pilots.

Element order of the 8x4 panel: n = 4 * col + row (col 0..7 horizontal,
row 0..3 vertical), as in ris_mu.geometry.RISPanel.positions.

Contents
  mask(M)                observed-element pattern (M = 8, 16, 32)
  interp_fill            neighbour-averaging linear interpolation on the grid
  LMMSE                  widely-linear MMSE estimate of the unobserved b_n
  groups, group_solve    element grouping: M groups share one phase
  features_partial       network input: masked cascade + a + mask channel
  CNN2DBiLSTM            the new model (B; C with n_out = 1)
"""
import numpy as np
import torch
import torch.nn as nn

from ris_mu.sumiso import solver as SV

COLS, ROWS = 8, 4


def mask(M):
    col = torch.arange(32) // ROWS
    row = torch.arange(32) % ROWS
    if M == 8:
        m = (col % 2 == 0) & (row % 2 == 0)
    elif M == 16:
        m = (col + row) % 2 == 0
    elif M == 32:
        m = torch.ones(32, dtype=torch.bool)
    else:
        raise ValueError(M)
    assert int(m.sum()) == M
    return m


def _neighbours():
    nb = []
    for n in range(32):
        c, r = divmod(n, ROWS)
        nb.append([ROWS * cc + rr for cc, rr in ((c - 1, r), (c + 1, r), (c, r - 1), (c, r + 1))
                   if 0 <= cc < COLS and 0 <= rr < ROWS])
    return nb


NB = _neighbours()


def interp_fill(B, m):
    """B [S,N,T] with only m observed; unobserved filled by repeated simultaneous
    averaging of already-known 4-neighbours (linear interpolation on the grid,
    nearest neighbour at the edges)."""
    X = B.clone()
    known = m.clone()
    X[:, ~m] = 0
    while not bool(known.all()):
        new = known.clone()
        Y = X.clone()
        for n in range(32):
            if known[n]:
                continue
            k = [j for j in NB[n] if known[j]]
            if k:
                Y[:, n] = X[:, k].mean(1)
                new[n] = True
        X, known = Y, new
    return X


def _real(a, B):
    """[S, 2(N+1)T] real stacking of (vec B, a)."""
    z = torch.cat([B.reshape(B.shape[0], -1), a], 1)
    return torch.cat([z.real, z.imag], 1).double()


class LMMSE:
    """Widely-linear MMSE estimate of the unobserved b_n from (observed b_n, a).

    Mean and covariance are estimated on training channels, each scenario
    normalised by the norm of its observation, so that strong scenarios do
    not dominate the fit; the resulting estimator is linear, hence applied
    to unnormalised observations unchanged (it is scale-equivariant).
    """
    def __init__(self, a_tr, B_tr, m, ridge=1e-6):
        S, N, T = B_tr.shape
        self.N, self.T, self.m = N, T, m
        obs_c = torch.zeros(N + 1, T, dtype=torch.bool)
        obs_c[:N] = m[:, None]
        obs_c[N] = True                                     # a is observed
        obs = torch.cat([obs_c.reshape(-1), obs_c.reshape(-1)])
        self.o, self.u = obs, ~obs
        X = _real(a_tr, B_tr)
        X = X / X[:, self.o].norm(dim=1, keepdim=True)
        mu = X.mean(0)
        Xc = X - mu
        Cov = Xc.T @ Xc / S
        Coo = Cov[self.o][:, self.o]
        Cuo = Cov[self.u][:, self.o]
        Coo = Coo + ridge * torch.trace(Coo) / Coo.shape[0] * torch.eye(Coo.shape[0], dtype=Coo.dtype)
        self.W = torch.linalg.solve(Coo, Cuo.T).T           # [u, o]
        self.mean_norm = float(mu.norm() / Xc.norm(dim=1).mean())   # diagnostic: ~0 means zero-mean

    def __call__(self, a, B):
        X = _real(a, B)
        X[:, self.u] = X[:, self.o] @ self.W.T
        h = X.shape[1] // 2
        z = torch.complex(X[:, :h], X[:, h:]).to(torch.complex64)
        Bh = z[:, :self.N * self.T].reshape(-1, self.N, self.T)
        Bh[:, self.m] = B[:, self.m]                        # observed entries kept exactly
        return Bh


GROUP_SHAPES = {8: [(2, 2), (1, 4), (4, 1)], 16: [(2, 1), (1, 2)], 32: [(1, 1)]}


def groups(M, shape=None):
    """Group index per element; shape = (columns, rows) per group. Pre-registered:
    M = 8 -> (2, 2), M = 16 -> (2, 1); the other shapes of GROUP_SHAPES were added
    as tuned alternatives (deviation 1 of the pre-registration)."""
    shape = shape or GROUP_SHAPES[M][0]
    gc, gr = shape
    assert (COLS // gc) * (ROWS // gr) == M
    col = torch.arange(32) // ROWS
    row = torch.arange(32) % ROWS
    return (col // gc) * (ROWS // gr) + row // gr


def group_solve(a, B, M, shape=None, sweeps=30):
    """Pilot i measures the group sum channel with all of group i on; group phases
    by exact coordinate ascent over the M super-elements (SU-align + 3 random starts)."""
    g = groups(M, shape)
    Bg = torch.stack([B[:, g == k].sum(1) for k in range(M)], 1)
    thg, _ = SV.solve(a, Bg, sweeps=sweeps)
    return thg[:, g]


def features_partial(a, B, m):
    """Masked cascade (unobserved b_n set to zero), a broadcast, mask channel: [S, 4T+1, N]."""
    S, N, T = B.shape
    Bm = B * m[None, :, None].to(B.dtype)
    ab = a[:, None, :].expand(S, N, T)
    mk = m[None, :, None].float().expand(S, N, 1)
    return torch.cat([Bm.real, Bm.imag, ab.real, ab.imag, mk], -1).transpose(1, 2).contiguous().float()


class CNN2DBiLSTM(nn.Module):
    """Phase-aware 2D-CNN-BiLSTM (model B of the pre-registration).

    2 x [Conv2d 3x3 + BN + ReLU] (64 channels) on the 8x4 panel grid, Dropout 0.2;
    BiLSTM(64 -> 2x64), BiLSTM(128 -> 2x32) along the element sequence,
    Dropout 0.3, per-element Linear(64 -> n_out): n_out = 2 (sin, cos) or 1 (angle, model C).
    """
    def __init__(self, c_in, n_elem=32, n_out=2):
        super().__init__()
        assert n_elem == COLS * ROWS
        self.n, self.n_out = n_elem, n_out
        self.cnn = nn.Sequential(
            nn.Conv2d(c_in, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.Dropout(0.2))
        self.lstm1 = nn.LSTM(64, 64, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(128, 32, batch_first=True, bidirectional=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, n_out))

    def forward(self, x):                       # x [S, C, N], n = 4 col + row
        S, C, N = x.shape
        h = self.cnn(x.view(S, C, COLS, ROWS)).reshape(S, 64, N).transpose(1, 2)
        h, _ = self.lstm1(h)
        h, _ = self.lstm2(h)
        return self.out(h)
