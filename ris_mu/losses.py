"""
losses.py
---------
Supervised (phase-aware regression) and unsupervised (rate-based) objectives,
plus the metrics reported in the tables.

Why an unsupervised objective is needed
---------------------------------------
The closed-form label theta_n = -angle(F_n) - angle(G_n) is optimal only for a
single user: it aligns every element with one cascaded channel. With U users
sharing one reflecting surface no such closed form exists, so there is nothing
to regress onto. Instead the network is trained directly on the system metric,
which also removes the performance ceiling implied by imitating any particular
classical solver.

Multiple-access model
---------------------
Single-antenna BS, users served in orthogonal time slots within one coherence
block, RIS held fixed over the block (its reconfiguration is slower than the
slot duration). The design problem is therefore to pick one phase vector that
serves all users well, which is a genuine fairness problem -- the natural
objective is max-min rate.
"""

import torch
import torch.nn.functional as Fn


# ------------------------------------------------------------------- helpers

def sincos_to_unit(y, N):
    """
    Map raw network output [B, 2N] to a unit-modulus reflection coefficient.

    Returns (cos, sin) normalised to the unit circle. Using the normalised
    pair rather than atan2 keeps the gradient well conditioned and enforces
    |exp(j theta)| = 1 exactly, as a passive element requires.
    """
    s, c = y[:, :N], y[:, N:]
    r = torch.sqrt(s * s + c * c + 1e-12)   # epsilon inside: sqrt'(0) is infinite
    return c / r, s / r


def effective_channel(Fc, Gc, hd, cos_t, sin_t):
    """
    h_u = h_d,u + sum_n G_u,n exp(j theta_n) F_n

    Fc  : [B, N] complex      Gc : [B, U, N] complex
    hd  : [B, U] complex      cos_t, sin_t : [B, N] real
    returns |h_u|^2  [B, U]
    """
    phase = torch.complex(cos_t, sin_t)                 # [B, N]
    casc = Gc * (phase * Fc).unsqueeze(1)               # [B, U, N]
    h = hd + casc.sum(-1)
    return h.real ** 2 + h.imag ** 2


# -------------------------------------------------------------- supervised

def phase_aware_mse(y_pred, y_true):
    """MSE on the (sin, cos) pair: smooth across the +-pi wrap."""
    return Fn.mse_loss(y_pred, y_true)


@torch.no_grad()
def rmse_deg(y_pred, y_true, N):
    tp = torch.atan2(y_pred[:, :N], y_pred[:, N:])
    tt = torch.atan2(y_true[:, :N], y_true[:, N:])
    d = torch.atan2(torch.sin(tp - tt), torch.cos(tp - tt))
    return (torch.sqrt((d ** 2).mean()) * 180 / torch.pi).item()


@torch.no_grad()
def success_rate(y_pred, y_true, N, tau_deg=5.0):
    tp = torch.atan2(y_pred[:, :N], y_pred[:, N:])
    tt = torch.atan2(y_true[:, :N], y_true[:, N:])
    d = torch.atan2(torch.sin(tp - tt), torch.cos(tp - tt)).abs()
    return ((d * 180 / torch.pi) < tau_deg).float().mean().item() * 100


# ------------------------------------------------------------ unsupervised

def rates(Fc, Gc, hd, y, N, snr_scale):
    """Per-user rate [b/s/Hz]; snr_scale = Pt / noise_power."""
    cos_t, sin_t = sincos_to_unit(y, N)
    g = effective_channel(Fc, Gc, hd, cos_t, sin_t)
    return torch.log2(1.0 + snr_scale * g)


def maxmin_loss(Fc, Gc, hd, y, N, snr_scale, beta=8.0):
    """
    Negative smooth minimum of the per-user rates.

    A hard min passes gradient to one user per sample, which makes training
    unstable; the soft minimum (-logsumexp of -beta R) spreads the gradient
    while converging to the true min as beta grows.
    """
    R = rates(Fc, Gc, hd, y, N, snr_scale)
    soft_min = -torch.logsumexp(-beta * R, dim=-1) / beta
    return -soft_min.mean()


def sumrate_loss(Fc, Gc, hd, y, N, snr_scale):
    return -rates(Fc, Gc, hd, y, N, snr_scale).sum(-1).mean()


@torch.no_grad()
def rate_metrics(Fc, Gc, hd, y, N, snr_scale):
    R = rates(Fc, Gc, hd, y, N, snr_scale)
    return dict(min_rate=R.min(-1).values.mean().item(),
                sum_rate=R.sum(-1).mean().item(),
                mean_rate=R.mean().item())
