"""
features.py (mumiso)
--------------------
Network input for the MU-MISO setting. Training and evaluation call this
same function, so the two cannot drift apart silently.

    X : [S, K, C, N]      C = 5 + 4T

Channels, per (user k, element n):
    0,1            Re/Im  g_{k,n}                RIS -> user
    2 .. 1+2T      Re/Im  f_{n,t}, t=1..T        BS -> RIS (shared by users,
                                                 varies along the element axis)
    .. .. 1+4T     Re/Im  hd_{k,t}, t=1..T       direct (constant along n)
    C-3, C-2       cos/sin phi_su(k,n)           single-user alignment phase
    C-1            log relative user power

WHY phi_su IS AN INPUT
----------------------
phi_su is the single-user closed form and costs nothing to compute. Handing
it over is not handing over the answer: the multi-user problem is to merge K
conflicting alignments onto ONE surface, and that has no closed form. This
spends the network's capacity on the part of the problem that is actually
open instead of on rediscovering an arctangent.

WHY RELATIVE USER POWER IS AN EXPLICIT CHANNEL
----------------------------------------------
Normalising each user's channel to unit power -- the obvious thing to do --
erases the power difference BETWEEN users, which is exactly what a max-min
objective turns on: the surface must favour whoever is worst off, and a
network that cannot see who that is has to guess. So the complex channels
are divided by ONE scenario-level constant, preserving relative strength,
and the removed scale is supplied separately in log form.

This is not hypothetical. In an earlier run a per-user normalisation put the
learned model BELOW the closed form; switching to scenario-level scaling
plus the explicit log-power channel is what fixed it.
"""

import numpy as np

__all__ = ["n_channels", "mumiso_features"]


def n_channels(T, link_ratio=False):
    return 5 + 4 * T + (2 if link_ratio else 0)


# A fixed offset that puts log10(cascade power) near zero for THIS link
# budget (per-scenario cascade power runs 1.15e-10 to 8.72e-6, so log10 is
# -9.9 to -5.1). It is a constant, not a fitted or batch-derived quantity,
# so it introduces no dependence on which scenarios are passed together.
# Change it if the room, bandwidth or transmit power change.
_LOGP_OFFSET = 8.0


def mumiso_features(F, G, hd, phi_su, normalise=True, link_ratio=False):
    """
    F     : [S, N, T] complex
    G     : [S, K, N] complex
    hd    : [S, K, T] complex
    phi_su: [S, K, N] real      (system.su_align_phase output)
    returns [S, K, C, N] float32

    `link_ratio` (default False, so every existing checkpoint and audit
    claim keeps working) appends TWO channels that put back what the
    normalisation above removes.

    WHAT THE NORMALISATION REMOVES, MEASURED
    ----------------------------------------
    F, G and hd are each divided by their OWN scenario-level scale. That
    preserves relative user power inside G -- which is what the long note
    above is about -- but it also erases the ratio BETWEEN the quantities,
    and that ratio is not a detail:

        RIS-cascade / direct power, spread across scenarios
            in the raw channel      9.4 million-fold
            in the features         1.000-fold
            correlation between the two            +0.031

    So the network cannot tell a scenario where the cascade dominates from
    one where the direct path does, across seven orders of magnitude. The
    optimal phase strategy depends on exactly that: with a strong direct
    path the surface should align to it, with a dominant cascade the
    trade-off is different. The absolute scale goes too, and with a fixed
    noise variance that is the operating SNR.

    The two channels are the logs of the scales the function itself divided
    out, which is the cheapest honest way to hand the information back:

        C-2   log10(sG * sF / sH)                 cascade-to-direct ratio
        C-1   log10(sG * sF) + 8                  absolute cascade scale

    sF, sG and sH are AMPLITUDE scales (root mean square), so C-2 is half
    the log POWER ratio quoted above: it spans -2.24 to 0.99 where the power
    ratio spans -4.48 to 1.98. Nothing is lost by that -- measured
    correlation with the true log power ratio is +1.0000 against the base
    set's +0.031 -- and a factor of two is the easiest thing a first layer
    can absorb. It is written this way because these are literally the
    numbers the function divided by, which is harder to get wrong than
    recomputing the ratio a second way.

    Both are per SCENARIO (constant over users and elements), because that
    is the axis the information was lost on; per-user relative power is
    already channel C-3 of the base set.

    WHETHER THIS FIXES THE ONE-SHOT STALL IS UNTESTED. The measurement is
    that the information is absent, not that restoring it is sufficient --
    see `unrolled.py` for why the target may be non-smooth for reasons this
    does not touch.
    """
    F = np.asarray(F); G = np.asarray(G); hd = np.asarray(hd)
    phi_su = np.asarray(phi_su)
    S_, N, T = F.shape
    K = G.shape[1]

    if normalise:
        # ONE scale per scenario per quantity, never per user
        sF = np.sqrt(np.mean(np.abs(F) ** 2, axis=(1, 2), keepdims=True))
        sG = np.sqrt(np.mean(np.abs(G) ** 2, axis=(1, 2), keepdims=True))
        sH = np.sqrt(np.mean(np.abs(hd) ** 2, axis=(1, 2), keepdims=True))
        Fn = F / np.maximum(sF, 1e-30)
        Gn = G / np.maximum(sG, 1e-30)
        Hn = hd / np.maximum(sH, 1e-30)
    else:
        Fn, Gn, Hn = F, G, hd

    pw = np.mean(np.abs(G) ** 2, axis=-1, keepdims=True)            # [S,K,1]
    logp = (np.log10(pw + 1e-30)
            - np.log10(np.mean(pw, axis=1, keepdims=True) + 1e-30))  # [S,K,1]

    chans = [Gn.real, Gn.imag]                                       # [S,K,N]
    Fb = np.broadcast_to(Fn.transpose(0, 2, 1)[:, None], (S_, K, T, N))
    for t in range(T):
        chans += [Fb[:, :, t].real, Fb[:, :, t].imag]
    Hb = np.broadcast_to(Hn[..., None], (S_, K, T, N))
    for t in range(T):
        chans += [Hb[:, :, t].real, Hb[:, :, t].imag]
    chans += [np.cos(phi_su), np.sin(phi_su),
              np.broadcast_to(logp, (S_, K, N))]

    if link_ratio:
        if not normalise:
            # Nothing was divided out, so the information is still in the
            # complex channels and these two would be constants.
            raise ValueError("link_ratio needs normalise=True; with "
                             "normalise=False the scales are still present")
        casc = sF * sG                                  # [S,1,1] each
        ratio = np.log10(np.maximum(casc, 1e-300)
                         / np.maximum(sH, 1e-300))      # [S,1,1]
        scale = np.log10(np.maximum(casc, 1e-300)) + _LOGP_OFFSET
        chans += [np.broadcast_to(ratio.reshape(S_, 1, 1), (S_, K, N)),
                  np.broadcast_to(scale.reshape(S_, 1, 1), (S_, K, N))]

    X = np.stack(chans, axis=2)
    assert X.shape == (S_, K, n_channels(T, link_ratio), N), X.shape
    return np.ascontiguousarray(X, dtype=np.float32)
