"""
Training-free radio map from a site survey (the baseline the independent
audit of 2026-11-06 showed the position-trained CNN must beat).

build:  for every surveyed position, the phase that maximises the summed gain
        over the stacked channels of its k nearest surveyed positions (exact
        coordinate ascent on the stacked problem). Done offline.
lookup: at run time, the stored phase of the nearest surveyed position
        (brute-force nearest neighbour), then the 4 common-phase candidates.
"""
import numpy as np
import torch

from . import solver as SV


def stacked_solve(Bs, As, sweeps=10):
    """Bs [S,k,N,T], As [S,k,T] -> theta [S,N] maximising sum_j |a_j + B_j^T v|^2."""
    S, k, N, T = Bs.shape
    Bcat = Bs.permute(0, 2, 1, 3).reshape(S, N, k * T)
    Acat = As.reshape(S, k * T)
    return SV.coord_ascent(Acat, Bcat, SV.su_align(Acat, Bcat), sweeps=sweeps)[0]


class RadioMap:
    def __init__(self, pos, A, B, k=20, chunk=1000):
        self.pos = np.asarray(pos, float)
        th = []
        for i in range(0, len(pos), chunk):
            p = self.pos[i:i + chunk]
            d2 = ((p[:, None, :] - self.pos[None]) ** 2).sum(-1)
            nn = torch.as_tensor(np.argsort(d2, axis=1)[:, :k])
            th.append(stacked_solve(B[nn], A[nn]))
        self.theta = torch.cat(th)

    def lookup(self, q):
        d2 = ((np.asarray(q, float)[:, None, :] - self.pos[None]) ** 2).sum(-1)
        return self.theta[torch.as_tensor(d2.argmin(1))]
