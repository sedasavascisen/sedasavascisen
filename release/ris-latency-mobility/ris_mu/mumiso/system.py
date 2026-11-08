"""
system.py
---------
MU-MISO downlink: the single source of truth for the system equations.

    y_k = ( h_d,k^H + g_k^H diag(v) F ) sum_j w_j s_j + n_k

    F  : [B, N, T]    BS  -> RIS          (T = N_t antennas)
    G  : [B, K, N]    RIS -> user k       (g_k^H stored as a row)
    hd : [B, K, T]    direct BS -> user
    v  : [B, N]       v_n = exp(j theta_n)
    W  : [B, T, K]    precoder, ||W||_F^2 = Pt

    SINR_k = |h_k^H w_k|^2 / ( sum_{j!=k} |h_k^H w_j|^2 + sigma^2 )

Everything is batched and differentiable. Complex autograd is used directly
-- the real-arithmetic decomposition the MATLAB port needed is unnecessary
here, which removes a whole class of sign errors.

WHY THE PRECODER IS CLOSED FORM
-------------------------------
MRT and ZF are computed from the effective channel, not learned. With the
precoder fixed, every measured gain is attributable to the RIS phase. If
both were learned, a good result could not be apportioned between them --
and that is the first question a thesis committee asks.
"""

import torch

__all__ = ["unit_phase", "effective_channel", "mrt", "zf", "precode",
           "rates", "sinr", "maxmin_loss", "sumrate_loss", "rate_metrics",
           "quantise_phase", "quantise_ste", "su_align_phase"]


# --------------------------------------------------------------- phase

def unit_phase(cos_t, sin_t, eps=1e-12):
    """
    Map a raw (cos, sin) pair onto the unit circle.

    The network's two outputs per element are not constrained to have unit
    modulus, and a passive element requires exactly that. Normalising the
    pair -- rather than taking atan2 and re-expanding -- keeps the gradient
    well conditioned and enforces |v_n| = 1 identically.

    The epsilon sits INSIDE the square root: sqrt has infinite derivative at
    zero, so sqrt(x) + eps still produces NaN gradients when the pair happens
    to vanish, while sqrt(x + eps) does not.
    """
    r = torch.sqrt(cos_t * cos_t + sin_t * sin_t + eps)
    return cos_t / r, sin_t / r


def su_align_phase(F, G, hd, k=None):
    """
    Single-user alignment phase, the K=1 closed form, per user.

    theta_n = angle(h_d) - angle(g_n f_n)

    With T > 1 antennas h_d is not a scalar, so the cascade is projected onto
    the direct channel's own direction (matched filtering), u = h_d/||h_d||:

        a_n = g_{k,n} * (f_n^H u)        theta_n = -angle(a_n)

    which reduces to the scalar form when T = 1. Note the general form keeps
    the angle(h_d) term that the published Eq. (8) drops: with the direct path
    present, dropping it costs real gain (measured: 1.0000 vs 0.8977 of the
    analytic bound). The published paper assumes a blocked direct path, where
    the two coincide -- this is a scope extension, not an erratum.

    returns [B, K, N] if k is None, else [B, N]
    """
    nrm = torch.linalg.norm(hd, dim=-1, keepdim=True)            # [B,K,1]
    safe = nrm.clamp_min(1e-30)
    u = hd / safe                                                # [B,K,T]
    # where the direct path is absent, any direction will do
    u = torch.where(nrm > 1e-30, u, F[:, :1, :].conj() /
                    torch.linalg.norm(F[:, :1, :], dim=-1, keepdim=True)
                    .clamp_min(1e-30))
    # a_{k,n} = g_{k,n} * sum_t f_{n,t} conj(u_{k,t})
    proj = torch.einsum("bnt,bkt->bkn", F, u.conj())             # [B,K,N]
    a = G * proj
    theta = -torch.angle(a)
    return theta if k is None else theta[:, k]


# ------------------------------------------------------- effective channel

def effective_channel(F, G, hd, cos_t, sin_t):
    """
    h_k^H = h_d,k^H + g_k^H diag(v) F          ->  [B, K, T]

    SIGN CONVENTION, because getting this wrong is silent. G[b,k,:] stores
    g_k^H, so the reflection enters as diag(v) with v_n = exp(+j theta_n),
    NOT diag(v^H). An independent audit built both forms by hand: this code
    matches diag(v) to 1.8e-15 and the diag(v^H) form only to 9.7. The two
    differ by theta -> -theta, so no optimised result changes -- but the
    optimal phase that goes with THIS convention is
    theta_n = angle(h_d) - angle(g_n f_n), and writing the v^H form next to
    that expression gives 7% of the coherent bound instead of 100%. Earlier
    docstrings in this package had exactly that inconsistency.

    cos_t, sin_t : [B, N] real (already unit modulus, or raw -- call
    unit_phase first if raw).
    """
    v = torch.complex(cos_t, sin_t)                              # [B,N]
    return hd + torch.einsum("bkn,bnt->bkt", G * v.unsqueeze(1), F)


# ------------------------------------------------------------- precoders

def mrt(He, pt):
    """Maximum ratio transmission, ||W||_F^2 = pt.  He [B,K,T] -> W [B,T,K]"""
    W = He.conj().transpose(-1, -2)
    n = torch.linalg.norm(W.reshape(W.shape[0], -1), dim=-1).clamp_min(1e-30)
    return W * (pt ** 0.5 / n).view(-1, 1, 1)


def zf(He, pt, eps=None, noise_var=None, err_power=0.0, eps_abs=None):
    """
    Regularised zero forcing, ||W||_F^2 = pt.

    THE REGULARISER MUST BE RELATIVE TO THE CHANNEL SCALE
    -----------------------------------------------------
    This function used to default to an ABSOLUTE eps = 1e-9, compared
    against a He He^H whose scale is set by path loss. Measured on the
    default scenario, the diagonal of He He^H averages 2.96e-7, so that
    default was 0.34% of the diagonal -- and it cost 55% of the min-rate:

        eps = 0 (pure ZF)      4.703
        eps = 1e-12            4.709
        eps = 1e-10            4.046
        eps = 1e-9  (old default)  2.095   <-- every number in this package
        eps = 1e-8             0.624
        eps >= 1e-6            0.093 = MRT exactly

    The last row is the tell: above 1e-6 the regulariser dominates the
    inverse, W collapses to He^H, and "regularised ZF" silently becomes
    MRT. An absolute constant cannot be right, because changing the link
    budget -- transmit power, bandwidth, room size -- moves the channel
    scale and the same number becomes either inert or catastrophic.

    So the default is now the MMSE/RZF choice, which is scale-correct by
    construction:

        eps = K * (noise_var + err_power * P_sig) / pt

    with P_sig the mean diagonal of He He^H.

    DOES err_power BUY ROBUSTNESS? MEASURED: NO.
    --------------------------------------------
    The textbook argument says the estimation error acts as extra
    interference and belongs in the regulariser. For SUM rate that is
    right. For the max-min rate this package reports, it is not -- the
    objective is decided by the single worst user, and shrinking the
    precoder toward MRT does not help that user. Measured on 400 scenarios
    (phase and precoder from the estimate, rate with the truth):

        error      eps=0    MMSE(noise)   MMSE+err    best swept
        perfect    5.756       5.720        5.720      5.757 @1e-5
        -20 dB     1.310       1.314        1.214      1.337 @1e-2
        -15 dB     0.689       0.690        0.667      0.704 @1e-2
        -10 dB     0.307       0.307        0.307      0.319 @1e-1

    Folding the error in COSTS 7% at -20 dB, and even the best swept
    regulariser beats eps = 0 by only about 2%. So `err_power` defaults to
    0 and is kept only for sum-rate work; the CSI collapse is intrinsic to
    ZF's error sensitivity, not a tuning failure, and no scalar
    regulariser fixes it.

    When `noise_var` is not supplied the regulariser falls back to a small
    multiple of the channel scale (1e-9 relative, not absolute), which sits
    deep in the harmless regime above.

    WHAT "SCALE-CORRECT" DOES AND DOES NOT MEAN HERE
    ------------------------------------------------
    Read the default formula again: with the `err_power` term at its
    default of 0 it is simply `lam = K * noise_var / pt`, which does not
    reference the channel at all. It is scale-correct in the DIMENSIONAL
    sense -- noise_var is a physical quantity in the same units as
    He He^H's diagonal, so the sum is meaningful and changing the link
    budget moves both together -- and that is what fixed the original bug.
    It is NOT adaptive to the individual scenario: `p_sig` enters only via
    `eps`, via `err_power`, or via the no-argument fallback.

    That distinction matters because the per-scenario channel scale spans
    a factor of 75,769 on the default scenario (per-scenario mean diagonal
    from 1.15e-10 to 8.72e-6). So one fixed lambda is a different amount of
    regularisation for every scenario, and it is RELATIVELY largest exactly
    where the channel is weakest -- which is where max-min is decided.

    MEASURED COST OF THE DEFAULT, 1200 scenarios, su_average phase:

                            MMSE default   eps_abs=0   pure ZF is better by
        all 1200               3.5549        3.6330           2.20%
        hardest decile *       2.1391        2.2451           4.95%
        easiest decile         5.1299        5.1754           0.89%

        * ranked by lam / that scenario's own mean diagonal.

    So the default costs about 2% overall -- an earlier version of this
    docstring said 1.4%, measured on 400 scenarios -- and the loss is
    concentrated in the hard tail rather than spread evenly. Do not read
    the relative-eps table above as implying those scenarios have
    "collapsed to MRT": that table's eps is a multiple of the BATCH mean
    diagonal, which is a different quantity from a scenario's own, and the
    measured cost is 2%, not 55%.

    It is still the default, for two measured reasons. Under CSI error the
    regulariser earns its keep (from the table above: at -20 dB eps=0 gives
    1.310 and the MMSE default 1.314), and the MMSE form is derived for
    sum-SINR while this package reports max-min, so it was never expected
    to be optimal here. With perfect CSI, pass `eps_abs=0.0` to recover the
    2%. Changing the DEFAULT would move every number in the package, so it
    is left alone deliberately rather than by oversight.

    `eps_abs` forces the old absolute behaviour, for reproducing earlier
    numbers on purpose.
    """
    K = He.shape[-2]
    M = He @ He.conj().transpose(-1, -2)
    I = torch.eye(K, dtype=He.dtype, device=He.device).expand_as(M)

    def _p_sig():
        """Mean diagonal of He He^H over users AND batch. Note the batch
        axis: this is a property of the call, not of one scenario, so any
        path that uses it makes a scenario's result depend on which others
        were passed alongside it. The default path does not use it."""
        return torch.diagonal(M, dim1=-2, dim2=-1).real.mean().clamp_min(1e-30)

    if eps_abs is not None:
        lam = eps_abs
    elif eps is not None:
        lam = eps * _p_sig()                       # relative multiple
    elif noise_var is not None:
        lam = K * noise_var / pt
        if err_power:                              # measured: does not help
            lam = lam + K * err_power * _p_sig() / pt
    else:
        lam = 1e-9 * _p_sig()
    W = He.conj().transpose(-1, -2) @ torch.linalg.inv(M + lam * I)
    n = torch.linalg.norm(W.reshape(W.shape[0], -1), dim=-1).clamp_min(1e-30)
    return W * (pt ** 0.5 / n).view(-1, 1, 1)


def precode(He, pt, kind="zf", noise_var=None, err_power=0.0):
    if kind == "zf":
        return zf(He, pt, noise_var=noise_var, err_power=err_power)
    if kind == "mrt":
        return mrt(He, pt)
    raise ValueError(f"unknown precoder {kind!r}")


# ------------------------------------------------------------------ rates

def sinr(He, W, noise_var):
    """A[k,j] = |h_k^H w_j|^2  ->  SINR_k  [B, K]"""
    A = (He @ W).abs() ** 2                                      # [B,K,K]
    sig = torch.diagonal(A, dim1=-2, dim2=-1)                    # [B,K]
    interf = A.sum(-1) - sig
    return sig / (interf + noise_var)


def rates(F, G, hd, cos_t, sin_t, pt, noise_var, precoder="zf",
          err_power=0.0):
    """
    Per-user rate [b/s/Hz], [B, K].

    noise_var is passed through to the precoder so that regularised ZF uses
    the MMSE regulariser rather than a magic constant; see `zf`.
    """
    He = effective_channel(F, G, hd, cos_t, sin_t)
    W = precode(He, pt, precoder, noise_var=noise_var, err_power=err_power)
    return torch.log2(1.0 + sinr(He, W, noise_var))


# ----------------------------------------------------------------- losses

def maxmin_loss(R, beta=8.0):
    """
    Negative smooth minimum of the per-user rates.

    A hard min hands the gradient to exactly one user per sample, which makes
    training jerky; the soft minimum spreads it and converges to the true min
    as beta grows. torch.logsumexp is internally shifted by the max, so this
    is numerically safe at realistic rates -- the naive
    -log(sum(exp(-beta R)))/beta overflows in float32 once R reaches about
    16 b/s/Hz with beta = 8 (exp(-128) underflows, log(0) = -inf).
    """
    return -(-torch.logsumexp(-beta * R, dim=-1) / beta).mean()


def sumrate_loss(R):
    return -R.sum(-1).mean()


@torch.no_grad()
def rate_metrics(R):
    return dict(min_rate=R.min(-1).values.mean().item(),
                sum_rate=R.sum(-1).mean().item(),
                mean_rate=R.mean().item())


# ------------------------------------------------------------ quantisation

def quantise_phase(theta, bits):
    """Hard projection onto a 2^bits uniform phase grid."""
    if bits is None:
        return theta
    step = 2 * torch.pi / (2 ** bits)
    return torch.round(theta / step) * step


def quantise_ste(cos_t, sin_t, bits):
    """
    Straight-through quantiser: forward rounds, backward passes through.

    round has zero derivative everywhere, so theta + (round(.) - theta) would
    give gradient zero, not one. detach() is what makes the offset a
    constant, and hence d(theta + delta)/d(theta) = 1.

    Measured caveat: on the earlier single-RIS experiment a straight-through
    network did NOT beat discrete coordinate descent at 1 bit (3.544 vs
    5.600). Quantisation-aware training is worth reporting, but the claim
    that it wins has to be measured, not assumed.
    """
    if bits is None:
        return cos_t, sin_t
    theta = torch.atan2(sin_t, cos_t)
    step = 2 * torch.pi / (2 ** bits)
    delta = (torch.round(theta / step) * step - theta).detach()
    tq = theta + delta
    return torch.cos(tq), torch.sin(tq)
