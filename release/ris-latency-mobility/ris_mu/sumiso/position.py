"""
Position-based phase design for a fixed site (ris_mu.sumiso.site).

geometric_phase   closed-form LoS steering from the user position: the phase
                  that compensates the BS-centre -> element -> user path length,
                  theta_n = k (d(BS, n) + d(n, u)). No CSI, no training.
position_features per-element input of the CNN-LSTM: cos/sin of that
                  geometric phase, the element-user distance, and the user
                  coordinates broadcast -> [P, 6, N].
pick_common_phase the common phase cannot be known without CSI; the BS
                  tries 4 rotations (one effective-channel pilot each) and
                  keeps the best (solver.best_grid_rotation with 2 bits).
"""
import numpy as np
import torch

from . import solver as SV


def geometric_phase(site, pos):
    P = site.panel
    k = 2 * np.pi / P.lam
    d_bs = np.linalg.norm(P.positions - site.bs, axis=-1)                      # [N]
    d_u = np.linalg.norm(pos[:, None, :] - P.positions[None], axis=-1)           # [P,N]
    return torch.as_tensor(np.angle(np.exp(1j * k * (d_bs[None] + d_u))), dtype=torch.float32)


def position_features(site, pos):
    P = site.panel
    k = 2 * np.pi / P.lam
    d_bs = np.linalg.norm(P.positions - site.bs, axis=-1)
    d_u = np.linalg.norm(pos[:, None, :] - P.positions[None], axis=-1)
    ph = k * (d_bs[None] + d_u)
    n = P.positions.shape[0]
    xyz = np.repeat((pos / site.room)[:, :, None], n, axis=2)                    # [P,3,N]
    f = np.concatenate([np.cos(ph)[:, None], np.sin(ph)[:, None], d_u[:, None] / 10.0, xyz], axis=1)
    return torch.as_tensor(f, dtype=torch.float32)


def pick_common_phase(theta, a, B):
    return SV.best_grid_rotation(theta, a, B, 2)
