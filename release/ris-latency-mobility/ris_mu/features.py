"""
features.py
-----------
Converts raw complex channels into model inputs and labels.

Single-user input layout (matches the published model): 4 channels per RIS
element -- [Re F, Im F, Re G, Im G] -- flattened to [B, 4N].

Multi-user input layout: 4 channels per (user, element) pair plus the direct
link, kept as [B, U, C, N] so that permutation-equivariant models can act on
the user axis.

Labels for the supervised (single-user) setting are the closed-form optimal
phases written as (sin, cos) pairs -- the phase-aware representation that is
the core contribution of the original paper, kept unchanged here.
"""

import numpy as np


def normalise_pair(F, G):
    """
    Scale F and G so that the mean per-element power is 1 within each sample.

    The optimal phase depends only on angle(F) + angle(G), so this scaling is
    label-preserving. It removes the large dynamic range caused by path loss
    and shadow fading, which would otherwise dominate the input statistics.
    The removed scales are returned so that rate-based losses can restore them.
    """
    sf = np.sqrt(np.mean(np.abs(F) ** 2, axis=-1, keepdims=True)) + 1e-30
    sg = np.sqrt(np.mean(np.abs(G) ** 2, axis=-1, keepdims=True)) + 1e-30
    return F / sf, G / sg, sf, sg


def su_features(F, G, normalise=True):
    """
    Single-user features.

    F : (S, N) complex       G : (S, N) complex
    returns X (S, 4, N) float32
    """
    if normalise:
        F, G, _, _ = normalise_pair(F, G)
    X = np.stack([F.real, F.imag, G.real, G.imag], axis=1)
    return X.astype(np.float32)


def su_labels(F, G):
    """Closed-form optimal phase (Eq. 8) as (sin, cos) -> (S, 2, N) float32."""
    theta = -np.angle(F) - np.angle(G)
    return np.stack([np.sin(theta), np.cos(theta)], axis=1).astype(np.float32)


MU_CHANNELS = 9


def mu_features(F, G, hd, normalise=True):
    """
    Multi-user features, (S, U, 9, N) float32.

    Per (user, element): [Re F, Im F, Re G_u, Im G_u, Re h_d,u, Im h_d,u,
    log-power of user u relative to the scenario mean, cos phi_un, sin phi_un]
    where phi_un = -angle(F_n) - angle(G_un) is the phase that would align
    element n to user u alone.

    Supplying phi explicitly is not giving away the answer: it is the
    single-user closed form, computable for free, and the multi-user problem
    is to COMBINE the U conflicting alignments into one surface. Making phi an
    input moves the network's capacity off rediscovering an arctangent and
    onto the part of the problem that has no closed form.

    The scaling matters more here than in the single-user case. Normalising
    each user's channel to unit power -- the obvious thing to do -- erases the
    difference in received power BETWEEN users, which is precisely what a
    max-min objective turns on: the surface must favour whoever is worst off,
    and a network that cannot see who that is has to guess. So the complex
    channels are scaled by ONE scenario-level constant, preserving relative
    user strength, and the removed scale is additionally supplied in log form
    as an explicit channel.
    """
    Fb = F[:, None, :]
    if normalise:
        sf = np.sqrt(np.mean(np.abs(Fb) ** 2, axis=-1, keepdims=True)) + 1e-30
        # one scale for the whole scenario, not one per user
        sg = np.sqrt(np.mean(np.abs(G) ** 2, axis=(1, 2), keepdims=True)) + 1e-30
        Fb, G, hd = Fb / sf, G / sg, hd / sg[..., 0]

    pw = np.mean(np.abs(G) ** 2, axis=-1, keepdims=True)                # (S,U,1)
    logp = np.log10(pw + 1e-30) - np.log10(pw.mean(axis=1, keepdims=True) + 1e-30)

    phi = -np.angle(Fb) - np.angle(G)                                   # (S,U,N)

    Fb = np.broadcast_to(Fb, G.shape)
    hb = np.broadcast_to(hd[..., None], G.shape)
    lb = np.broadcast_to(logp, G.shape)
    X = np.stack([Fb.real, Fb.imag, G.real, G.imag, hb.real, hb.imag, lb,
                  np.cos(phi), np.sin(phi)], axis=2)
    return X.astype(np.float32)


def split_indices(n, frac=(0.7, 0.15, 0.15), seed=0):
    """Deterministic train / val / test split."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    a = int(frac[0] * n)
    b = a + int(frac[1] * n)
    return idx[:a], idx[a:b], idx[b:]
