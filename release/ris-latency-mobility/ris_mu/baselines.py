"""
baselines.py
------------
Reference solutions for the multi-user RIS phase problem, used to place the
learned models on a meaningful scale.

  no_ris          surface absent (direct link only)
  random_phase    uniform phases -- the floor
  su_closed_form  closed-form alignment to ONE user, ignoring the others.
                  This is the published single-user solution applied to a
                  multi-user scenario, and is the honest way to show what the
                  extension buys.
  pga_maxmin      projected gradient ascent on the smooth max-min objective,
                  batched, with random restarts. This is the classical
                  numerical reference: it is allowed many iterations per
                  sample, so a learned model that approaches it while running
                  in one forward pass is the interesting outcome.

All functions take torch tensors and return a phase vector [B, N] (or a
metric dict), so they can be dropped into the same evaluation loop as the
networks.
"""

import torch

from .losses import effective_channel


def _rates(Fc, Gc, hd, theta, snr_scale):
    g = effective_channel(Fc, Gc, hd, torch.cos(theta), torch.sin(theta))
    return torch.log2(1.0 + snr_scale * g)


def no_ris(Fc, Gc, hd, snr_scale):
    g = hd.real ** 2 + hd.imag ** 2
    return torch.log2(1.0 + snr_scale * g)


def random_phase(Fc, Gc, hd, snr_scale, seed=0):
    gen = torch.Generator().manual_seed(seed)
    theta = (torch.rand(Fc.shape, generator=gen) * 2 - 1) * torch.pi
    return theta, _rates(Fc, Gc, hd, theta, snr_scale)


def su_closed_form(Fc, Gc, hd, snr_scale, user="best"):
    """
    Align the surface to one user with the closed form, then score all users.

    user="best"  -> the user whose own max-min contribution ends up highest
    user=int     -> that user index
    """
    B, U, N = Gc.shape
    if isinstance(user, int):
        theta = -(torch.angle(Fc) + torch.angle(Gc[:, user]))
        return theta, _rates(Fc, Gc, hd, theta, snr_scale)

    best_val = torch.full((B,), -float("inf"))
    best_theta = torch.zeros(B, N)
    for u in range(U):
        th = -(torch.angle(Fc) + torch.angle(Gc[:, u]))
        val = _rates(Fc, Gc, hd, th, snr_scale).min(-1).values
        upd = val > best_val
        best_val = torch.where(upd, val, best_val)
        best_theta[upd] = th[upd]
    return best_theta, _rates(Fc, Gc, hd, best_theta, snr_scale)


def pga_maxmin(Fc, Gc, hd, snr_scale, iters=400, restarts=4, lr=0.3,
               beta=8.0, seed=0, init_from_closed_form=True):
    """
    Projected gradient ascent on the smooth min of the per-user rates.

    Phases are unconstrained reals and wrapped only when reported, which makes
    the ascent free of the discontinuity that motivates the sin/cos output
    representation in the first place -- the classical solver does not suffer
    from the problem the network has to be designed around.
    """
    B, U, N = Gc.shape
    gen = torch.Generator().manual_seed(seed)

    best_val = torch.full((B,), -float("inf"))
    best_theta = torch.zeros(B, N)

    inits = []
    if init_from_closed_form:
        inits.append(su_closed_form(Fc, Gc, hd, snr_scale)[0])
    for r in range(restarts - len(inits)):
        inits.append((torch.rand(B, N, generator=gen) * 2 - 1) * torch.pi)

    for th0 in inits:
        th = th0.clone().requires_grad_(True)
        opt = torch.optim.Adam([th], lr=lr)
        for _ in range(iters):
            opt.zero_grad()
            R = _rates(Fc, Gc, hd, th, snr_scale)
            soft_min = -torch.logsumexp(-beta * R, dim=-1) / beta
            (-soft_min.sum()).backward()
            opt.step()
        with torch.no_grad():
            val = _rates(Fc, Gc, hd, th, snr_scale).min(-1).values
            upd = val > best_val
            best_val = torch.where(upd, val, best_val)
            best_theta[upd] = th.detach()[upd]

    best_theta = torch.atan2(torch.sin(best_theta), torch.cos(best_theta))
    return best_theta, _rates(Fc, Gc, hd, best_theta, snr_scale)


def summarise(R):
    """Rate tensor [B, U] -> the three numbers reported in every table."""
    return dict(min_rate=R.min(-1).values.mean().item(),
                sum_rate=R.sum(-1).mean().item(),
                mean_rate=R.mean().item())
