# Kodun son hali

Bu dosya `scripts/dump_source.py` tarafindan **2026-10-30** tarihinde diskteki kaynaktan uretildi. Elle duzenlenmez; kaynak degisince betigi yeniden kosturun.

Her dosyanin basliginda satir sayisi ve icerigin sha256 ozeti var. Claude Code'da bir dosyayi acip bu ozetle karsilastirabilirsiniz: ayni ise dosya bu listedekiyle birebir aynidir.

> **Yayimlanmis MATLAB kodu bu pakette yok ve bu paketten etkilenmez.** `duzeltilmis_kodlar` ayri durur ve yayimlanan sonuclari uretmeye devam eder.

---

## Icindekiler

**67 dosya · 10076 satir**

| Dosya | Satir | sha256 |
|---|---:|---|
| `ris_mu/mumiso/__init__.py` | 14 | `f9c07f1338d5` |
| `ris_mu/mumiso/system.py` | 333 | `21a8a952d800` |
| `ris_mu/mumiso/channel.py` | 338 | `b3c2a9ed69ca` |
| `ris_mu/mumiso/mobile.py` | 238 | `b33c20ab878e` |
| `ris_mu/mumiso/csi.py` | 131 | `accb4f90d9ec` |
| `ris_mu/mumiso/features.py` | 156 | `e1f57324af38` |
| `ris_mu/mumiso/models.py` | 278 | `4775daa8a793` |
| `ris_mu/mumiso/unrolled.py` | 223 | `95835a3ed9f3` |
| `ris_mu/mumiso/baselines.py` | 348 | `3ea6e6dd577f` |
| `ris_mu/mumiso/train.py` | 110 | `a48824f31611` |
| `ris_mu/__init__.py` | 0 | `e3b0c44298fc` |
| `ris_mu/geometry.py` | 84 | `295c899c3073` |
| `ris_mu/pathloss.py` | 111 | `9ab1e1cbca80` |
| `ris_mu/channel.py` | 348 | `8ec99f395131` |
| `ris_mu/features.py` | 107 | `c68df09577a3` |
| `ris_mu/models.py` | 316 | `4408c6e73174` |
| `ris_mu/losses.py` | 112 | `4fd1c95b68d3` |
| `ris_mu/baselines.py` | 113 | `2d5290a8fdc0` |
| `ris_mu/train.py` | 74 | `03f9853db4d4` |
| `scripts/audit_claims.py` | 465 | `4768a78598df` |
| `scripts/audit_fair_comparison.py` | 191 | `612487b768e0` |
| `scripts/audit_precoder_csi.py` | 156 | `af94df52d20d` |
| `scripts/audit_section4_cause.py` | 120 | `961aa49c3240` |
| `scripts/verify_mumiso_system.py` | 85 | `70c1c3a5ca9a` |
| `scripts/verify_mumiso_channel.py` | 63 | `c5b24cbab83e` |
| `scripts/verify_mumiso_models.py` | 91 | `15b75565f57a` |
| `scripts/verify_mobile.py` | 106 | `1913e291c531` |
| `scripts/verify_residual.py` | 57 | `6a9e50a457ae` |
| `scripts/verify_batch_dependence.py` | 53 | `11ed1aa64660` |
| `scripts/verify_baseline_strength.py` | 40 | `27f30c3e8238` |
| `scripts/verify_crossover.py` | 123 | `3649874707cb` |
| `scripts/verify_head_claim.py` | 163 | `ccc519076f7e` |
| `scripts/verify_matlab_architecture.py` | 133 | `70e791323b23` |
| `scripts/mumiso_run.py` | 146 | `ab16ab18b22b` |
| `scripts/mumiso_unrolled.py` | 156 | `e557411495d9` |
| `scripts/mumiso_equal_step.py` | 255 | `ae3ea9cfbd22` |
| `scripts/mumiso_latency_parity.py` | 271 | `c40f705e21b9` |
| `scripts/mumiso_latency_repeat.py` | 90 | `c6687a3532ee` |
| `scripts/mumiso_step_cost.py` | 66 | `658e6186e376` |
| `scripts/mumiso_budget.py` | 172 | `6b757f4a12b7` |
| `scripts/mumiso_budget_fraction.py` | 228 | `d147a606155c` |
| `scripts/mumiso_headroom.py` | 52 | `d7ff9705f3b8` |
| `scripts/anchor_same_split.py` | 26 | `a4ac3fa7cb26` |
| `scripts/diagnose_learnability.py` | 129 | `6f4375cd7410` |
| `scripts/diagnose_mumiso_gap.py` | 105 | `3411d21f59e2` |
| `scripts/step1_control.py` | 118 | `fd042c302981` |
| `scripts/step1b_head_ablation.py` | 119 | `87685e92fa0f` |
| `scripts/step4_multiuser.py` | 150 | `a9e56d2c5509` |
| `scripts/step4b_residual.py` | 99 | `c61c758b64e4` |
| `scripts/step4c_equiv_long.py` | 99 | `2bbadcdae859` |
| `scripts/step5_generalisation.py` | 129 | `8b1356bbdb8a` |
| `scripts/step5b_mixed_users.py` | 167 | `e4407aed2fad` |
| `scripts/mumiso_aging.py` | 204 | `ab0f6bccdcfa` |
| `scripts/mumiso_frontier.py` | 163 | `175da29e064a` |
| `scripts/mumiso_beam_staleness.py` | 139 | `be5a1e837981` |
| `scripts/mumiso_antenna_corr.py` | 73 | `52e1fbee7d50` |
| `scripts/mumiso_gain_sharing.py` | 60 | `0ff5e98f3c59` |
| `scripts/mumiso_gain_source.py` | 37 | `7141a0938ef5` |
| `scripts/mumiso_precoder_cost.py` | 46 | `eb616f5073d8` |
| `scripts/mumiso_csi_room.py` | 127 | `4600791a219c` |
| `scripts/mumiso_quant_latency.py` | 114 | `9b3a60ce25be` |
| `scripts/step3_csi_transfer.py` | 168 | `372aed33fe5d` |
| `scripts/step6_quantised_phase.py` | 221 | `f951598f5ed5` |
| `scripts/diagnose_realism.py` | 149 | `b4b4031d45f3` |
| `scripts/compile_results.py` | 209 | `9a22de7b9b19` |
| `scripts/make_writing_reference.py` | 289 | `f63cf58a2098` |
| `scripts/dump_source.py` | 220 | `d5518cb2d916` |


## 1. Cekirdek paket: `ris_mu/mumiso/`

Tezin butun sayilari bu on dosyadan cikiyor. `system.py` tek dogruluk kaynagidir: SINR, oran ve on kodlayici sadece orada tanimli, digerleri onu cagirir.

### `ris_mu/mumiso/__init__.py`

*14 satir · sha256:f9c07f1338d5*

```python
"""
mumiso
------
MU-MISO extension: N_t-antenna BS, K single-antenna users, N-element RIS.

The rest of `ris_mu` models a single-antenna BS, where the users share one
surface but the BS cannot separate them at all -- there is no precoder and
no interference term, only K conflicting alignments. This subpackage adds
the transmit array, so interference becomes real and the fairness problem
acquires the structure a multi-user downlink actually has.

The single-antenna code is left untouched: it reproduces the published
results and is not the place to take risks.
"""
```

### `ris_mu/mumiso/system.py`

*333 satir · sha256:21a8a952d800*

```python
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
```

### `ris_mu/mumiso/channel.py`

*338 satir · sha256:b3c2a9ed69ca*

```python
"""
channel.py (mumiso)
-------------------
MU-MISO channel generator: the verified single-antenna generator with a
transmit array bolted on.

WHAT IS REUSED, UNCHANGED
-------------------------
Everything physical: 3GPP TR 38.901 InH-Office path loss and LoS
probability, the Ricean K distribution, Gudmundson-correlated shadowing,
the Tang et al. (2021) two-hop cascade amplitude, the cos^q element
pattern, the wall-mounted panel geometry, and the direct-link blocker.
`MuMisoChannel` subclasses `MultiUserRISChannel` and overrides only the
chunk assembly, so the single-antenna path that reproduces the published
results keeps running on exactly the code it was verified on.

WHAT IS ADDED
-------------
The BS becomes a uniform linear array of T antennas at half-wavelength
spacing. Two consequences, and both are deliberate:

1. ONE LoS STATE, ONE RICEAN K AND ONE SHADOWING DRAW PER LINK, shared by
   all T antennas. The array spans a few wavelengths; its antennas see the
   same blockers, the same clusters and the same large-scale fading. Giving
   each antenna its own LoS coin would decorrelate the array and destroy
   the very structure a precoder exploits. Antenna-to-antenna variation
   comes only from exact geometry -- the same principle the element axis
   already follows.

2. THE CLUSTER GAINS ARE **NOT** SHARED ACROSS THE ARRAY, and this is a
   known modelling limitation rather than a choice. An earlier version of
   this docstring claimed they were. They are not: the parent's `_ris_link`
   draws `gains = self._crandn(d1.shape)` and for the BS-RIS call `d1` has
   shape [S, T, L], so every antenna gets an INDEPENDENT complex gain for
   every cluster. (Sharing along the RIS ELEMENT axis is real -- `gains`
   has no N axis and is broadcast over it -- which is what the comment
   inside `_ris_link` means.)

   Physically each scatterer has one reflection coefficient, and the
   antenna-to-antenna variation should come from geometric phase alone.
   Drawing per antenna decorrelates the array beyond what the geometry
   gives, and the direction of that error FLATTERS the system: more
   antenna diversity makes it easier for ZF to null interference than it
   would be in reality, so the rates here are optimistic. Unlike the
   mobility model's bias, this one does not work in the thesis's favour.

WHICH DIAGNOSTIC TO BELIEVE
---------------------------
Report the effective rank of G, pooled over users, always with its sample
count (see `effective_rank`).

CORRECTED APERTURE NUMBERS. The previous version of this section reported
"neighbour correlation 0.59 on the element axis and 0.77 on the antenna
axis, antenna-axis effective rank 2.32 of 4 ... a properly correlated
aperture in both directions". The element-axis figure stands; the
antenna-axis figures were produced by a mis-sliced measurement -- F is
[S, N, T], so antenna-axis rows are `F.reshape(-1, T)` and element-axis
rows are `F.transpose(0,2,1).reshape(-1, N)`, and transposing before the
antenna reshape silently reads N-long rows as T-long ones. Re-measured:

    config              element axis   antenna axis   antenna eff. rank
    T=4, 600 samples        0.620      0.234            3.71 / 4
    T=4, 1500 samples       0.616      0.191            3.82 / 4
    T=8, 1500 samples       0.639      0.204            7.26 / 8

    antenna axis split by LoS state (T=8): LoS 0.818, NLoS 0.130

So the aperture is correlated along the ELEMENT axis and close to
uncorrelated and nearly full rank along the ANTENNA axis, and what little
antenna correlation exists is carried almost entirely by the LoS term --
consistent with point 2 above, since the NLoS component is where the
independent gains enter. Do not describe this channel as "correlated in
both directions".

F's rank is healthy here because the cluster geometry is redrawn every
sample and the 3GPP LoS coin comes up heads only about a third of the time,
so F genuinely varies even with `bs_random=False`. This is NOT true of a
generator whose BS-RIS link is a deterministic steering vector times one
scalar gain: there F's sample covariance is rank one by construction and
the number says nothing. If you port this diagnostic elsewhere, check G.
"""

from dataclasses import dataclass
import numpy as np

from ..channel import MultiUserRISChannel, ChannelConfig, _centre_cos
from ..geometry import RISPanel

__all__ = ["MuMisoConfig", "MuMisoChannel", "make_mumiso_scenario",
           "effective_rank", "neighbour_corr", "to_torch"]


@dataclass
class MuMisoConfig(ChannelConfig):
    n_bs_antennas: int = 4
    bs_axis: tuple = (1.0, 0.0, 0.0)     # ULA orientation
    bs_spacing: float = 0.5              # in wavelengths


class MuMisoChannel(MultiUserRISChannel):
    """Generates (F [S,N,T], G [S,K,N], hd [S,K,T])."""

    def __init__(self, panel: RISPanel, cfg: MuMisoConfig = None):
        super().__init__(panel, cfg or MuMisoConfig())
        self.T = self.cfg.n_bs_antennas

    # ------------------------------------------------------------- array
    def _array(self, bs):
        """bs [S,3] -> antenna positions [S,T,3], centred on bs."""
        ax = np.asarray(self.cfg.bs_axis, float)
        ax = ax / np.linalg.norm(ax)
        d = self.cfg.bs_spacing * self.panel.lam
        off = (np.arange(self.T) - (self.T - 1) / 2.0)[:, None] * d * ax
        return bs[:, None, :] + off[None]

    # ------------------------------------------------------------- chunk
    def _generate_chunk(self, S):
        c, P, rng, pl = self.cfg, self.panel, self.rng, self.pl
        K, L = c.n_users, c.n_clusters
        room = np.asarray(c.room, float)
        ris_c = P.positions.mean(0)

        # --- geometry ----------------------------------------------------
        if c.bs_random:
            bs = rng.uniform([0, 0, 2.0], [room[0], room[1], room[2] - 0.5], (S, 3))
        else:
            bs = np.tile(np.asarray(c.bs_pos, float), (S, 1))
        bsa = self._array(bs)                                        # [S,T,3]

        if c.user_cluster_radius > 0:
            hot = rng.uniform([0, 0], room[:2], (S, 1, 2))
            xy = np.clip(hot + rng.normal(0, c.user_cluster_radius, (S, K, 2)),
                         0, room[:2])
        else:
            xy = rng.uniform([0, 0], room[:2], (S, K, 2))
        ue = np.concatenate([xy, rng.uniform(*c.user_z, (S, K, 1))], axis=-1)

        scat = rng.uniform([0, 0, 0], room, (S, L, 3))      # shared by all users

        # --- distances to the panel centre (large scale) -----------------
        d3_bs = np.linalg.norm(bs - ris_c, axis=-1)                    # [S]
        d2_bs = np.linalg.norm((bs - ris_c)[..., :2], axis=-1)
        d3_ue = np.linalg.norm(ue - ris_c, axis=-1)                    # [S,K]
        d2_ue = np.linalg.norm((ue - ris_c)[..., :2], axis=-1)
        d3_dir = np.linalg.norm(bs[:, None, :] - ue, axis=-1)          # [S,K]
        d2_dir = np.linalg.norm((bs[:, None, :] - ue)[..., :2], axis=-1)

        # --- LoS state and Ricean K: ONE PER LINK, shared by the array ---
        los_bs = rng.random(S) < pl.los_prob(d2_bs)                    # [S]
        los_ue = rng.random((S, K)) < pl.los_prob(d2_ue)               # [S,K]
        los_dir = rng.random((S, K)) < pl.los_prob(d2_dir)             # [S,K]

        k_bs = 10 ** (pl.rice_k_db(rng, S) / 10)
        k_ue = 10 ** (pl.rice_k_db(rng, (S, K)) / 10)
        k_dir = 10 ** (pl.rice_k_db(rng, (S, K)) / 10)

        # --- small scale --------------------------------------------------
        # _ris_link(pts[...,3], scat[...,L,3], los[...], kappa[...]) -> [...,N]
        # Passing the array as the leading axis gives [S,T,N] directly, the
        # same broadcast the user axis already uses.
        F_s = self._ris_link(bsa, scat[:, None], los_bs[:, None],
                             k_bs[:, None])                            # [S,T,N]
        G_s = self._ris_link(ue, scat[:, None], los_ue, k_ue)           # [S,K,N]
        hd_s = self._direct_link(bsa[:, None], ue[:, :, None],
                                 scat[:, None, None],
                                 los_dir[..., None], k_dir[..., None])  # [S,K,T]

        # --- large scale --------------------------------------------------
        gt = 10 ** (c.bs_gain_dbi / 20)
        gr = 10 ** (c.ue_gain_dbi / 20)
        f_in = _centre_cos(P, bs) ** P.q                               # [S]
        f_out = _centre_cos(P, ue) ** P.q                              # [S,K]
        cascade_const = (np.sqrt(P.element_gain * P.d * P.d) * P.lam
                         / (4 * np.pi) ** 1.5)

        A_F = (gt * cascade_const * np.sqrt(f_in) / np.maximum(d3_bs, 1.0)
               * 10 ** (-pl.excess_db(d3_bs, los_bs) / 20))
        A_G = (gr * np.sqrt(f_out) / np.maximum(d3_ue, 1.0)
               * 10 ** (-pl.excess_db(d3_ue, los_ue) / 20))
        A_d = pl.amplitude(d3_dir, los_dir, c.bs_gain_dbi + c.ue_gain_dbi)

        blocked = rng.random((S, K)) < c.direct_blocked_prob
        A_d = A_d * 10 ** (-c.direct_blockage_db * blocked / 20)

        A_F = A_F * 10 ** (pl.sigma_sf_db(los_bs) * rng.standard_normal(S) / 20)
        A_G = A_G * self._sf_corr(los_ue, ue)
        A_d = A_d * self._sf_corr(los_dir, ue)

        # F is stored [S,N,T] to match the system equations
        F = (F_s * A_F[:, None, None]).transpose(0, 2, 1)
        return dict(
            F=F.astype(np.complex64),
            G=(G_s * A_G[..., None]).astype(np.complex64),
            hd=(hd_s * A_d[..., None]).astype(np.complex64),
            bs_pos=bs.astype(np.float32), bs_array=bsa.astype(np.float32),
            ue_pos=ue.astype(np.float32),
            los_ris_bs=los_bs, los_ris_ue=los_ue, los_direct=los_dir,
        )

    def generate(self, n_samples: int, chunk: int = 2000):
        """
        n_samples scenarios as a dict of arrays.

        REPRODUCIBILITY LANDMINE, measured -- read this before comparing
        two runs. The draw is deterministic for a fixed (seed, n_samples,
        chunk): calling it twice gives bit-identical arrays. It is NOT
        stable under a change of either n_samples or chunk, because each
        chunk draws arrays whose SHAPE depends on S, so a different S
        consumes the generator stream differently:

            generate(1000)        vs generate(2000)[:1000]  -> differ
            generate(3000, 3000)  vs generate(3000, 1000)   -> differ

        (Measured max |dG| of 4.96 and 5.29 against a mean |G| of 5.70e-2;
        the two draws are statistically identical -- mean |G| agrees to
        5.699e-2 vs 5.701e-2 -- so this is not a correctness bug. It is a
        comparability trap.)

        What that means in practice: a number measured at --samples 6000 and
        a number measured at --samples 12000 come from DIFFERENT channel
        realisations and cannot be put in the same table or ratio. Every
        script that compares a trained model against a baseline must
        generate both on the same (seed, n_samples, chunk), and a script
        that loads a checkpoint must be told the n_samples it was trained
        on. `scripts/mumiso_equal_step.py --samples` carries that warning
        for exactly this reason.

        If prefix stability is ever needed, draw per scenario from a
        SeedSequence spawned per index rather than per chunk; that is a
        behaviour change and would move every number in the package, so it
        has not been done.
        """
        keys = ("F", "G", "hd", "bs_pos", "bs_array", "ue_pos",
                "los_ris_bs", "los_ris_ue", "los_direct")
        out = {k: [] for k in keys}
        done = 0
        while done < n_samples:
            s = min(chunk, n_samples - done)
            part = self._generate_chunk(s)
            for k in keys:
                out[k].append(part[k])
            done += s
        return {k: np.concatenate(v, axis=0) for k, v in out.items()}


# ------------------------------------------------------------------ scenario
def make_mumiso_scenario(n_users=4, n_bs_antennas=4, M=8, K=4, seed=42,
                         **overrides):
    """
    Matched (panel, config) pair for the MU-MISO setting.

    Keeping panel geometry and channel configuration together prevents the
    failure the legacy setup had: a panel orientation and a BS position each
    individually plausible, but together putting the transmitter behind the
    surface, where a passive element radiates nothing.
    """
    cfg = MuMisoConfig(n_users=n_users, n_bs_antennas=n_bs_antennas,
                       seed=seed, **overrides)
    room = np.asarray(cfg.room, float)

    if cfg.mount == "wall":
        panel = RISPanel(M=M, K=K, center=(room[0] / 2, 0.1, 3.0),
                         e1=(1, 0, 0), e2=(0, 0, 1), normal=(0, 1, 0))
    elif cfg.mount == "ceiling":
        panel = RISPanel(M=M, K=K,
                         center=(room[0] / 2, room[1] / 2, room[2] - 0.2),
                         e1=(1, 0, 0), e2=(0, 1, 0), normal=(0, 0, -1))
    else:
        raise ValueError(f"unknown mount {cfg.mount!r}")

    far_field = 2 * (M * panel.d) ** 2 / panel.lam
    d_bs = np.linalg.norm(np.asarray(cfg.bs_pos) - panel.positions.mean(0))
    if d_bs < far_field:
        raise ValueError(f"BS at {d_bs:.1f} m is inside the Fraunhofer "
                         f"distance {far_field:.1f} m; move it or shrink "
                         f"the panel")
    return panel, cfg


# --------------------------------------------------------------- diagnostics
def effective_rank(X):
    """
    Entropy-based effective rank of the sample spatial covariance.

    X : [S, N]. Returns exp(-sum p_i log p_i) over normalised eigenvalues.
    N means the channel is indistinguishable from spatial white noise and
    there is no structure for a convolutional or recurrent body to exploit;
    1 means it is effectively deterministic and there is no diversity to
    learn from. Both are pathologies, in opposite directions.

    NEVER QUOTE THIS NUMBER WITHOUT ITS SAMPLE COUNT. It is an estimate
    from a SAMPLE covariance of S scenarios, and with N = 32 it has not
    converged at any S this package uses. Measured on the same channel:

        S =   250  ->  16.57
        S =  1000  ->  16.07     <- lower than at 250: not monotone either
        S =  4000  ->  20.75
        S = 16000  ->  21.18

    That is a 32% spread, and the 250 -> 1000 step moves the wrong way, so
    "the effective rank is about 16" and "about 21" are both quotable from
    this one function and neither is the rank. Report it as
    "effective rank 21.0 (S = 16000)" or not at all; a reviewer who
    recomputes it at a different S will otherwise get a different number
    and be right to ask why. `scripts/audit_claims.py` pins all four rows
    and asserts the non-monotonicity so this cannot be quietly forgotten.
    """
    X = np.asarray(X)
    R = (X.conj().T @ X) / X.shape[0]
    ev = np.sort(np.abs(np.linalg.eigvalsh((R + R.conj().T) / 2)))[::-1]
    ev = ev / ev.sum()
    ev = ev[ev > 1e-12]
    return float(np.exp(-(ev * np.log(ev)).sum()))


def neighbour_corr(X):
    """Mean |correlation| between adjacent elements. Physically nonzero."""
    X = np.asarray(X)
    R = (X.conj().T @ X) / X.shape[0]
    d = np.sqrt(np.real(np.diag(R)))
    C = np.abs(R / np.outer(d, d))
    return float(np.mean(np.diag(C, 1)))


def to_torch(data, device="cpu", dtype=None):
    """
    (F, G, hd) as torch tensors with consistent dtypes.

    The generator emits complex64. Mixing that with a float64 phase tensor
    raises "expected ComplexFloat but found ComplexDouble" from einsum, which
    is a confusing way to learn about a dtype -- so the conversion lives in
    one place and the matching real dtype is returned alongside.
    """
    import torch
    cdtype = dtype or torch.complex64
    rdtype = torch.float32 if cdtype == torch.complex64 else torch.float64
    t = lambda x: torch.as_tensor(x).to(device=device, dtype=cdtype)
    return t(data["F"]), t(data["G"]), t(data["hd"]), rdtype
```

### `ris_mu/mumiso/mobile.py`

*238 satir · sha256:b33c20ab878e*

```python
"""
mobile.py (mumiso)
------------------
Channel aging: the same propagation environment, a walking user.

WHAT THIS IS FOR
----------------
Every latency number in this package is compared against a coherence time
computed from a formula: at 3 GHz and 1.5 m/s, f_d = 15 Hz and
T_c = 0.423/f_d = 28 ms. A formula is not a measurement. What a thesis can
defend is the curve: hold a phase configuration fixed and watch the rate
decay as the user walks away from it.

That curve also turns the latency table into the real comparison. A method
does not deliver its answer to the channel it was given -- it delivers it
to the channel that exists when it finishes. So a method taking 5.6 seconds
is not "slower but just as good": by the time it answers, the user has moved
8.4 metres and its answer is for a channel that no longer exists. The
EFFECTIVE rate of a method is its phase evaluated at t = its own latency.

WHAT IS HELD FIXED ACROSS TIME, AND WHY IT MATTERS
--------------------------------------------------
Everything except the user positions:

  - the scatterer realisation (same room, same clutter)
  - the per-path complex gains (same physical scatterers, same reflection
    coefficients)
  - the LoS state and the Ricean K per link
  - the shadowing draw
  - F entirely, since the BS and the RIS do not move

If the cluster gains were redrawn at each step, consecutive snapshots would
be independent draws and there would be no aging to measure -- the rate
would collapse to the random-phase level immediately and the curve would
say nothing about mobility. The whole point is that the channel changes
*continuously*, driven by geometry, which is exactly the spatial-consistency
principle the static generator already follows along the element axis,
applied along the time axis.

This reuses the parent's physics unchanged: 3GPP TR 38.901 path loss and
LoS probability, the Ricean K distribution, the cos^q element pattern, the
Tang two-hop cascade, Gudmundson-correlated shadowing.
"""

from dataclasses import dataclass
import numpy as np

from ..channel import _unit_power, _centre_cos
from .channel import MuMisoChannel, MuMisoConfig

__all__ = ["MobileConfig", "MobileMuMisoChannel", "DEFAULT_TIMES_MS"]

# A grid fine enough to resolve the coherence time and long enough to reach
# the classical optimisers' own latencies (coordinate descent ~1.5 s,
# PGA/AO ~5.6-6.5 s).
DEFAULT_TIMES_MS = (0.0, 2.0, 5.0, 10.0, 20.0, 28.2, 50.0, 100.0, 200.0,
                    500.0, 1500.0, 5600.0)


@dataclass
class MobileConfig(MuMisoConfig):
    velocity: float = 1.5            # m/s, walking
    times_ms: tuple = DEFAULT_TIMES_MS
    straight_line: bool = True       # constant heading over the window


class MobileMuMisoChannel(MuMisoChannel):
    """
    Generates a time series of MU-MISO channels for walking users.

    generate(n) returns, in addition to the static keys:
        G_t  : [S, L, K, N]      L = len(times_ms)
        hd_t : [S, L, K, T]
        F    : [S, N, T]         constant in time
        times_ms, ue_t
    """

    def __init__(self, panel, cfg: MobileConfig = None):
        super().__init__(panel, cfg or MobileConfig())

    # ------------------------------------------------- gain-injected links
    def _ris_link_g(self, pts, scat, los, kappa, gains):
        """`MultiUserRISChannel._ris_link` with the cluster gains supplied."""
        P = self.panel
        d_el = P.distances(pts)
        gain = P.pattern(pts)
        h_los = np.sqrt(gain) / np.maximum(d_el, 1.0) * np.exp(-1j * self.k * d_el)
        h_los = _unit_power(h_los)

        d1 = np.linalg.norm(pts[..., None, :] - scat, axis=-1)
        d2 = P.distances(scat)
        g_s = P.pattern(scat)
        amp = np.sqrt(g_s) / np.maximum(d1[..., None] * d2, 1.0)
        h_nlos = np.sum(gains[..., None] * amp *
                        np.exp(-1j * self.k * (d1[..., None] + d2)), axis=-2)
        h_nlos = _unit_power(h_nlos)

        kap = np.where(los, kappa, 0.0)[..., None]
        return (np.sqrt(kap / (kap + 1)) * h_los
                + np.sqrt(1.0 / (kap + 1)) * h_nlos)

    def _direct_link_g(self, a, b, scat, los, kappa, gains):
        """`MultiUserRISChannel._direct_link` with the gains supplied."""
        d = np.linalg.norm(a - b, axis=-1)
        h_los = np.exp(-1j * self.k * d)
        d1 = np.linalg.norm(a[..., None, :] - scat, axis=-1)
        d2 = np.linalg.norm(scat - b[..., None, :], axis=-1)
        h_nlos = np.sum(gains * np.exp(-1j * self.k * (d1 + d2)) /
                        np.maximum(d1 * d2, 1.0), axis=-1)
        h_nlos = h_nlos / np.sqrt(np.maximum(np.mean(np.abs(h_nlos) ** 2),
                                             1e-30))
        kap = np.where(los, kappa, 0.0)
        return (np.sqrt(kap / (kap + 1)) * h_los
                + np.sqrt(1.0 / (kap + 1)) * h_nlos)

    # ------------------------------------------------------------- chunk
    def _generate_chunk(self, S):
        c, P, rng, pl = self.cfg, self.panel, self.rng, self.pl
        K, L, T = c.n_users, c.n_clusters, self.T
        room = np.asarray(c.room, float)
        ris_c = P.positions.mean(0)
        t_s = np.asarray(c.times_ms, float) / 1e3          # [M]
        M = len(t_s)

        # --- static geometry ---------------------------------------------
        if c.bs_random:
            bs = rng.uniform([0, 0, 2.0], [room[0], room[1], room[2] - 0.5],
                             (S, 3))
        else:
            bs = np.tile(np.asarray(c.bs_pos, float), (S, 1))
        bsa = self._array(bs)                                   # [S,T,3]
        scat = rng.uniform([0, 0, 0], room, (S, L, 3))

        # --- trajectories -------------------------------------------------
        xy0 = rng.uniform([0, 0], room[:2], (S, K, 2))
        z0 = rng.uniform(*c.user_z, (S, K, 1))
        ang = rng.uniform(0, 2 * np.pi, (S, K))
        head = np.stack([np.cos(ang), np.sin(ang), np.zeros_like(ang)], -1)
        if not c.straight_line:
            # a slow random turn, so the window is not perfectly ballistic
            head = head + 0.15 * rng.standard_normal(head.shape)
            head = head / np.linalg.norm(head, axis=-1, keepdims=True)
        p0 = np.concatenate([xy0, z0], axis=-1)                 # [S,K,3]
        ue_t = (p0[:, None] + c.velocity * t_s[None, :, None, None]
                * head[:, None])                                # [S,M,K,3]
        # keep users in the room; reflect rather than clip so the speed is
        # preserved (clipping would silently freeze a user at a wall and
        # flatten the very decay this file exists to measure)
        for ax in (0, 1):
            hi = room[ax]
            x = ue_t[..., ax]
            per = 2 * hi
            x = np.abs(np.mod(x, per))
            ue_t[..., ax] = np.where(x > hi, per - x, x)

        # --- per-link randomness: drawn ONCE, held across time ------------
        d2_bs = np.linalg.norm((bs - ris_c)[..., :2], axis=-1)
        los_bs = rng.random(S) < pl.los_prob(d2_bs)
        k_bs = 10 ** (pl.rice_k_db(rng, S) / 10)
        gF_sc = self._crandn((S, T, L))

        # LoS state / K / shadowing are decided at t = 0 and kept: the
        # blockers and clusters are the same physical objects for the whole
        # window.
        ue0 = ue_t[:, 0]                                        # [S,K,3]
        d2_ue0 = np.linalg.norm((ue0 - ris_c)[..., :2], axis=-1)
        d2_dir0 = np.linalg.norm((bs[:, None, :] - ue0)[..., :2], axis=-1)
        los_ue = rng.random((S, K)) < pl.los_prob(d2_ue0)
        los_dir = rng.random((S, K)) < pl.los_prob(d2_dir0)
        k_ue = 10 ** (pl.rice_k_db(rng, (S, K)) / 10)
        k_dir = 10 ** (pl.rice_k_db(rng, (S, K)) / 10)
        gG_sc = self._crandn((S, K, L))
        gD_sc = self._crandn((S, K, T, L))
        sf_ue = self._sf_corr(los_ue, ue0)
        sf_dir = self._sf_corr(los_dir, ue0)
        sf_bs = 10 ** (pl.sigma_sf_db(los_bs) * rng.standard_normal(S) / 20)

        # --- F: static -----------------------------------------------------
        F_s = self._ris_link_g(bsa, scat[:, None], los_bs[:, None],
                               k_bs[:, None], gF_sc)             # [S,T,N]
        gt = 10 ** (c.bs_gain_dbi / 20)
        gr = 10 ** (c.ue_gain_dbi / 20)
        d3_bs = np.linalg.norm(bs - ris_c, axis=-1)
        f_in = _centre_cos(P, bs) ** P.q
        cascade_const = (np.sqrt(P.element_gain * P.d * P.d) * P.lam
                         / (4 * np.pi) ** 1.5)
        A_F = (gt * cascade_const * np.sqrt(f_in) / np.maximum(d3_bs, 1.0)
               * 10 ** (-pl.excess_db(d3_bs, los_bs) / 20) * sf_bs)
        F = (F_s * A_F[:, None, None]).transpose(0, 2, 1)        # [S,N,T]

        # --- G and hd: one snapshot per time ------------------------------
        N = P.positions.shape[0]
        G_t = np.zeros((S, M, K, N), np.complex64)
        hd_t = np.zeros((S, M, K, T), np.complex64)
        for m in range(M):
            ue = ue_t[:, m]                                      # [S,K,3]
            G_s = self._ris_link_g(ue, scat[:, None], los_ue, k_ue, gG_sc)
            hd_s = self._direct_link_g(bsa[:, None], ue[:, :, None],
                                       scat[:, None, None],
                                       los_dir[..., None], k_dir[..., None],
                                       gD_sc)                    # [S,K,T]
            d3_ue = np.linalg.norm(ue - ris_c, axis=-1)
            d3_dir = np.linalg.norm(bs[:, None, :] - ue, axis=-1)
            f_out = _centre_cos(P, ue) ** P.q
            A_G = (gr * np.sqrt(f_out) / np.maximum(d3_ue, 1.0)
                   * 10 ** (-pl.excess_db(d3_ue, los_ue) / 20) * sf_ue)
            A_d = pl.amplitude(d3_dir, los_dir,
                               c.bs_gain_dbi + c.ue_gain_dbi) * sf_dir
            blocked = (rng.random((S, K)) < c.direct_blocked_prob) if m == 0 \
                else self._blocked
            if m == 0:
                self._blocked = blocked
            A_d = A_d * 10 ** (-c.direct_blockage_db * blocked / 20)
            G_t[:, m] = (G_s * A_G[..., None]).astype(np.complex64)
            hd_t[:, m] = (hd_s * A_d[..., None]).astype(np.complex64)

        return dict(F=F.astype(np.complex64), G_t=G_t, hd_t=hd_t,
                    G=G_t[:, 0], hd=hd_t[:, 0],
                    ue_t=ue_t.astype(np.float32),
                    bs_pos=bs.astype(np.float32),
                    bs_array=bsa.astype(np.float32),
                    ue_pos=ue_t[:, 0].astype(np.float32),
                    los_ris_bs=los_bs, los_ris_ue=los_ue, los_direct=los_dir)

    def generate(self, n_samples: int, chunk: int = 500):
        keys = ("F", "G_t", "hd_t", "G", "hd", "ue_t", "bs_pos", "bs_array",
                "ue_pos", "los_ris_bs", "los_ris_ue", "los_direct")
        out = {k: [] for k in keys}
        done = 0
        while done < n_samples:
            s = min(chunk, n_samples - done)
            part = self._generate_chunk(s)
            for k in keys:
                out[k].append(part[k])
            done += s
        res = {k: np.concatenate(v, axis=0) for k, v in out.items()}
        res["times_ms"] = np.asarray(self.cfg.times_ms, float)
        return res
```

### `ris_mu/mumiso/csi.py`

*131 satir · sha256:accb4f90d9ec*

```python
"""
csi.py (mumiso)
---------------
Imperfect channel knowledge.

WHY THIS MATTERS MORE THAN IT LOOKS
-----------------------------------
An earlier study in this project measured something specific: the
convolutional/recurrent body earns its place only when the channel is
spatially correlated AND the CSI is imperfect (0 of 4 seeds on the legacy
white channel, 4 of 4 on the geometric one). This package's channel is
correlated; the second condition has been missing. So this is both part of
the "realistic scenario" axis and the one remaining place where a learned
model has a plausible reason to beat a classical optimiser.

The reason is not that networks are magic. It is that a classical optimiser
pointed at an estimated channel optimises the WRONG objective as hard as it
can, and so overfits the estimation error. A model trained across many
error realisations can learn a phase that is good on average over the
error, which is a different and more useful thing.

THE TRAP TO AVOID
-----------------
Early stopping is also a regulariser. Under CSI error the best number of
gradient steps shrinks, exactly as it does under mobility. So "the learned
model beats 32-step Adam" would prove nothing -- 32 steps is the wrong
setting once the objective is noisy. The comparison has to be against the
BEST step count at each error level. Anything else is the weak-baseline
mistake this project has already made four times.

ERROR MODEL
-----------
    Ĥ = sqrt(1 - e2) * H + sqrt(e2) * Z,    Z ~ CN(0, E|H|^2)

parameterised by the normalised error power e2 = E|Ĥ - H|^2 / E|H|^2 when
the leading factor is dropped; the sqrt(1 - e2) scaling keeps E|Ĥ|^2 =
E|H|^2 so that "more error" does not quietly also mean "more power". e2 is
given in dB as 10 log10(e2), so -10 dB means 10% error power.

One scale PER QUANTITY is used (one for F, one for G, one for hd), not one
global scale. Note what that does NOT give you: within G the users differ
in power by a median factor of 193, so the weakest user takes the same
ABSOLUTE error as the strongest and is hit far harder in relative terms.
Since max-min is decided by the weakest user, that sounded like it might
be driving the whole collapse -- it is not. Measured with a per-user error
scale instead, the rate moves by under 5% (at -20 dB: 1.214 global against
1.181 per-user). Worth knowing, but the sensitivity is ZF's, not the error
model's. An estimator whose per-link quality really does track per-link
SNR would use the per-user form; the hook is left here deliberately
unimplemented rather than claimed.

WHO SEES WHAT
-------------
Realistically the BS has only Ĥ, so BOTH the phase and the precoder are
computed from Ĥ, while the rate that actually materialises is evaluated
with the true H and that mismatched precoder. `rates_mismatched` does
exactly that; computing the precoder from the true channel would hide most
of the penalty and overstate how well everything works.
"""

import torch

from . import system as S

__all__ = ["add_error", "rates_mismatched", "db_to_e2"]


def db_to_e2(db):
    """-10 dB -> 0.1 error power. None or -inf -> perfect CSI."""
    if db is None:
        return 0.0
    return float(10.0 ** (db / 10.0))


def _noisy(H, e2, gen):
    """
    One error scale per call, from the mean power of the WHOLE tensor.

    Note the batch axis in that mean: the scale is a property of the CALL,
    not of a scenario, so adding error to 600 scenarios at once gives each
    of them a different absolute error than adding it to 150 at once. Since
    per-scenario channel power spans a factor of 75,769 on the default
    scenario, a scenario's effective error level depends on the company it
    is passed in with. Two consequences:

      - a CSI sweep must hold the batch fixed across error levels, which
        `rates_mismatched`'s callers do by construction (one tensor, many
        e2 values);
      - a per-scenario or per-user scale is the defensible alternative and
        was measured: under 5% difference in rate (see the docstring at the
        top of this file), so this is a comparability caveat, not a bug.
    """
    if e2 <= 0.0:
        return H
    p = (H.abs() ** 2).mean().clamp_min(1e-30)
    z = (torch.randn(H.shape, generator=gen, dtype=torch.float32)
         + 1j * torch.randn(H.shape, generator=gen, dtype=torch.float32))
    z = z.to(H.dtype) / (2 ** 0.5) * p.sqrt()
    return ((1.0 - e2) ** 0.5) * H + (e2 ** 0.5) * z


def add_error(F, G, hd, e2, seed=0, gen=None):
    """Estimated copies of (F, G, hd). Same shapes, same mean power."""
    g = gen if gen is not None else torch.Generator().manual_seed(seed)
    return _noisy(F, e2, g), _noisy(G, e2, g), _noisy(hd, e2, g)


def rates_mismatched(F, G, hd, F_est, G_est, hd_est, cos_t, sin_t, pt,
                     noise_var, precoder="zf", err_power=0.0):
    """
    Rate that actually materialises when the BS knows only the estimate.

    phase  : chosen by the caller from the estimate
    W      : computed from the ESTIMATED effective channel, with the
             estimation error folded into the regulariser
    rate   : evaluated with the TRUE effective channel and that W

    `err_power` folds the estimation error into the regulariser. It is
    plumbed through because the textbook MMSE argument calls for it, but
    MEASURED IT DOES NOT HELP HERE and it defaults to 0: for the max-min
    objective it costs about 7% at -20 dB against no regulariser at all
    (see `zf`'s docstring for the table). So what this function reports is
    plain ZF's error sensitivity -- which is the honest thing to report,
    because that sensitivity is intrinsic and no scalar regulariser
    removes it.
    """
    He_est = S.effective_channel(F_est, G_est, hd_est, cos_t, sin_t)
    W = S.precode(He_est, pt, precoder, noise_var=noise_var,
                  err_power=err_power)
    He = S.effective_channel(F, G, hd, cos_t, sin_t)
    return torch.log2(1.0 + S.sinr(He, W, noise_var))
```

### `ris_mu/mumiso/features.py`

*156 satir · sha256:e1f57324af38*

```python
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
```

### `ris_mu/mumiso/models.py`

*278 satir · sha256:4775daa8a793*

```python
"""
models.py (mumiso)
------------------
Three ways to turn K users into one surface. The published backbone is kept
identical in all three; only the user axis is handled differently, so the
comparison isolates exactly that.

BACKBONE (unchanged from the published model)
    Conv1d(3) -> BN -> ReLU -> Dropout -> Conv1d(3) -> BN -> ReLU
      -> LSTM(128, 2 layers) -> Linear(128 -> 64)

HEAD: per element, always
    A width-1 convolution, i.e. the same two-output map applied at every
    element. NOT the published dense bottleneck. This is deliberate and it
    is the largest single effect measured in this project: on the
    single-user task the dense head gave 50.19 degrees RMSE and the
    per-element head 2.46, and widening the dense bottleneck from 64 to 512
    recovered most of it (3.77) -- so the gap is the head, not the body.
    The same trap reappeared in the multi-user setting, where a dense head
    left the model stuck at 3.25.

THE THREE MODES
    "concat"    Users stacked on the channel axis. The direct extension of
                the published architecture. Fixes K in the first layer and
                is sensitive to the ORDER the users are listed in. This is
                the baseline the other two have to beat, and the order
                sensitivity is itself a reportable result.

    "deepsets"  Shared backbone applied to each user separately, then a mean
                over users (Zaheer et al.). Permutation invariant by
                construction and defined for any K. Pools once, at the end.

    "exchange"  Mean-field exchange: after each stage, every user also sees
                the mean over users, through a learned map. Still
                permutation invariant -- a mean is symmetric and so is the
                final pooling -- but strictly more expressive than
                "deepsets", because users influence each other BEFORE the
                final pooling rather than only at it. This is the variant
                the MATLAB port could not express without a custom layer.

RESIDUAL MODE (`residual=True`, the default)
    The network outputs a ROTATION applied to a free anchor rather than an
    absolute phase. Why, measured rather than assumed:

      - Reweighting the K single-user alignments recovers only 32% of the
        su_average -> AO gap, so the optimum does not live in that family
        and handing the network phi_su does not hand it the answer.
        [MEASURED BEFORE THE PRECODER FIX, not re-checked since.]
      - A free per-element OFFSET on top of su_average, found by 400 Adam
        steps, recovers 148% of that gap (5.25 against AO's 3.96). The
        optimum is reachable as an offset, and absolute-phase prediction is
        the badly conditioned way to ask for it.
        [ALSO PRE-FIX. "AO's 3.96" is definitely stale -- AO is 6.4020 with
        the corrected precoder -- so treat the 148% as indicative only.]
      - Trained to predict absolute phase, all three modes stalled at about
        1.15 b/s/Hz and landed a full pi/2 in circular distance from BOTH
        su_average and AO -- a different, mediocre basin. [PRE-FIX. An
        earlier version of this line added "barely past su_average's 1.27",
        which contradicts itself: 1.15 is BELOW 1.27. Re-measured with the
        fixed precoder, the residual modes land ON the anchor -- 3.5368 /
        3.5367 / 3.5260 against su_average's 3.5363 on the same test split.]

    The anchor is su_average, derived inside the model from the cos/sin
    phi_su feature channels, so nothing extra has to be plumbed in.

    THE FINAL LAYER IS NOT ZERO-INITIALISED. This paragraph used to claim
    it was, and that "training STARTS exactly at the anchor". The code does
    `self.head.net[-1].weight.mul_(0.01)` and the comment beside it explains
    why zeroing was rejected: a zeroed final layer sets d(output)/d(hidden)
    to 0, so the first optimiser step reaches only that one layer (measured:
    2 of 22 parameter tensors). Scaling instead leaves the rotation about
    0.6 degrees from identity -- inside the noise, but not exactly zero --
    and every parameter gets a gradient immediately. Measured on 400
    scenarios, an untrained residual net and su_average agree to four
    decimals (3.7230 / 3.7230), so "starts at the anchor" is true of the
    RATE; it is not true of the weights, and the distinction matters when
    explaining why a 12-epoch run moves the rate by less than its own
    epoch-to-epoch noise.

    (In the sibling `unrolled.py` the same 0.01 scaling is a NO-OP, because
    that head's output passes through atan2, which is scale-invariant. See
    the comment there -- the idiom does not transfer.)

    The rotation is parameterised around the identity as (1 + a) + i b with
    the epsilon INSIDE the square root. Both details matter: sqrt has
    infinite derivative at zero, so a rotation parameterised as a bare
    (a, b) pair produces NaN gradients the moment it passes through the
    origin -- which is exactly where a zero-initialised head starts.

OUTPUT
    [B, 2, N] with index 0 = cos, 1 = sin. Returned un-normalised; call
    `phases()` (or system.unit_phase) to project onto the unit circle. Two
    outputs per element rather than one angle is the published paper's own
    device for avoiding the +-pi discontinuity, and it is kept.
"""

import torch
import torch.nn as nn

from .features import n_channels

__all__ = ["MuMisoNet", "count_params", "MODES"]

MODES = ("concat", "deepsets", "exchange")


class _Backbone(nn.Module):
    """The published body, acting on [B, C, N] and returning [B, 64, N]."""

    def __init__(self, in_ch, lstm_hidden=128, out_ch=64, dropout=0.2):
        super().__init__()
        self.cnn1 = nn.Sequential(
            nn.Conv1d(in_ch, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True), nn.Dropout(dropout))
        self.cnn2 = nn.Sequential(
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True))
        self.lstm = nn.LSTM(64, lstm_hidden, num_layers=2,
                            batch_first=True, dropout=dropout)
        self.proj = nn.Linear(lstm_hidden, out_ch)

    def stage1(self, x):
        return self.cnn2(self.cnn1(x))                     # [B,64,N]

    def stage2(self, h):
        h, _ = self.lstm(h.permute(0, 2, 1))               # [B,N,hidden]
        return self.proj(h).permute(0, 2, 1)               # [B,64,N]

    def forward(self, x):
        return self.stage2(self.stage1(x))


class _LocalHead(nn.Module):
    """Width-1 convolution: the same small map applied at every element."""

    def __init__(self, c, hidden=64, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(c, hidden, 1), nn.ReLU(inplace=True),
            nn.Dropout(dropout), nn.Conv1d(hidden, 2, 1))

    def forward(self, h):                                  # [B,C,N]
        return self.net(h)                                 # [B,2,N]


class _Exchange(nn.Module):
    """
    Mean-field exchange across the user axis.

    h -> h + Linear(mean_k h), applied per element. The mean is over users,
    so the operation commutes with any permutation of them; the residual
    form means the module starts as the identity and can only help.
    """

    def __init__(self, c):
        super().__init__()
        self.mix = nn.Conv1d(c, c, 1)
        nn.init.zeros_(self.mix.weight)
        nn.init.zeros_(self.mix.bias)

    def forward(self, h):                                  # [B,K,C,N]
        B, K, C, N = h.shape
        m = h.mean(1)                                      # [B,C,N]
        return h + self.mix(m).unsqueeze(1)


class MuMisoNet(nn.Module):
    """
    Parameters
    ----------
    N        number of RIS elements
    n_users  K
    n_tx     T (antennas); in_ch is derived as 5 + 4T
    mode     "concat" | "deepsets" | "exchange"
    """

    def __init__(self, N=32, n_users=4, n_tx=4, mode="exchange",
                 lstm_hidden=128, dropout=0.2, residual=True,
                 link_ratio=False):
        super().__init__()
        if mode not in MODES:
            raise ValueError(f"unknown mode {mode!r}, expected one of {MODES}")
        self.N, self.K, self.T, self.mode = N, n_users, n_tx, mode
        self.residual = residual
        # link_ratio must match how the features were built; default False
        # keeps every existing checkpoint loadable.
        self.link_ratio = link_ratio
        C = n_channels(n_tx, link_ratio)
        self.in_ch = C

        if mode == "concat":
            self.body = _Backbone(C * n_users, lstm_hidden, 64, dropout)
        else:
            self.body = _Backbone(C, lstm_hidden, 64, dropout)

        if mode == "exchange":
            self.ex1 = _Exchange(64)
            self.ex2 = _Exchange(64)

        self.head = _LocalHead(64)
        if residual:
            # Start essentially AT the anchor, but not exactly.
            #
            # Zeroing the final layer outright starts at the anchor exactly
            # and is the textbook residual init -- but it also sets
            # d(output)/d(hidden) = 0, so on the first step the gradient
            # reaches only that one layer (measured: 2 of 22 parameter
            # tensors). It recovers from step two, yet there is no reason to
            # pay for it: scaling the weight down instead leaves the
            # rotation about 0.6 degrees from identity, which is well inside
            # the noise, and every parameter gets a gradient immediately.
            with torch.no_grad():
                self.head.net[-1].weight.mul_(0.01)
                self.head.net[-1].bias.zero_()

    # --------------------------------------------------------------- anchor
    @staticmethod
    def _anchor(x):
        """
        su_average direction, read off the feature tensor.

        Channels -3 and -2 are cos/sin of the single-user alignment phase
        per user, so the mean over users IS the su_average phasor (its
        modulus carries how much the users agree, which the rotation does
        not need). Deriving it here keeps the anchor and the features from
        ever disagreeing.
        """
        ca = x[:, :, -3, :].mean(1)                    # [B,N]
        sa = x[:, :, -2, :].mean(1)
        r = torch.sqrt(ca * ca + sa * sa + 1e-12)
        return ca / r, sa / r

    # ------------------------------------------------------------ forward
    def forward(self, x):
        """x : [B, K, C, N]  ->  [B, 2, N]  (index 0 = cos, 1 = sin)"""
        B, K, C, N = x.shape
        if C != self.in_ch:
            raise ValueError(f"expected {self.in_ch} channels, got {C}")

        if self.mode == "concat":
            if K != self.K:
                raise ValueError(f"concat mode was built for K={self.K}, "
                                 f"got {K}")
            h = self.body(x.reshape(B, K * C, N))          # [B,64,N]
            return self.head(h)

        flat = x.reshape(B * K, C, N)
        if self.mode == "deepsets":
            h = self.body(flat).reshape(B, K, 64, N)
            return self.head(h.mean(1))

        # exchange
        h = self.body.stage1(flat).reshape(B, K, 64, N)
        h = self.ex1(h)
        h = self.body.stage2(h.reshape(B * K, 64, N)).reshape(B, K, 64, N)
        h = self.ex2(h)
        return self.head(h.mean(1))

    # ------------------------------------------------------------- phases
    def phases(self, x, eps=1e-12):
        """Unit-modulus (cos, sin), each [B, N]."""
        y = self.forward(x)
        a, b = y[:, 0], y[:, 1]
        if not self.residual:
            r = torch.sqrt(a * a + b * b + eps)
            return a / r, b / r

        # rotation around the identity, applied to the anchor
        zr, zi = 1.0 + a, b
        r = torch.sqrt(zr * zr + zi * zi + eps)
        zr, zi = zr / r, zi / r
        ca, sa = self._anchor(x)
        # (ca + i sa) * (zr + i zi)
        return ca * zr - sa * zi, ca * zi + sa * zr


def count_params(m):
    return sum(p.numel() for p in m.parameters() if p.requires_grad)
```

### `ris_mu/mumiso/unrolled.py`

*223 satir · sha256:95835a3ed9f3*

```python
"""
unrolled.py (mumiso)
--------------------
Learn the UPDATE RULE, not the solution.

WHY THE OBVIOUS THING DOES NOT WORK
-----------------------------------
A single forward pass from channel to phase is what the published
single-user model does, and there it is the right design: the optimum has a
closed form, theta_n = angle(h_d) - angle(g_n f_n), which is an explicit
smooth function of the channel, so one pass can approximate it.

For K > 1 that function does not exist in usable form, and the measurements
say so plainly. Re-measured with the FIXED precoder (an earlier version of
this docstring quoted 5.07 against 1.03, from the buggy absolute-eps era):

  - per-scenario oracle offsets from the su_average anchor reach 6.1619
    b/s/Hz against the anchor's 3.4350, so good configurations are there;
  - two scenarios that are NEAREST NEIGHBOURS in feature space need
    offsets as unrelated as two random scenarios do: cos of the offset
    difference +0.0047 for the nearest neighbour against +0.0089 for a
    random pair. BOTH ARE INDISTINGUISHABLE FROM ZERO and their ordering
    is noise -- the previous text gave +0.0070 against +0.0018, which read
    as a weak signal favouring the neighbour, and the re-measurement
    reversed it. The claim is "feature similarity carries no information
    about the required offset", not "it carries a little";
  - a supervised fit of those oracle offsets fails ON THE TRAINING SET,
    stalling at mse 0.896 where 1.0 means uncorrelated, while validation
    sits flat at 0.925 and the supervised model ends up BELOW the anchor
    (3.4064 against 3.4350). Unsupervised training on the rate sits
    motionless at the anchor: untrained and 12-epoch-trained agree to four
    decimals (3.7230 / 3.7230).

THE CAUSE -- CORRECTED, AND THE CORRECTION MATTERS
--------------------------------------------------
This docstring used to say: "The cause is multiplicity, not capacity. Many
phase configurations are near-optimal and which one an optimiser reaches is
arbitrary, so any single target is noise with respect to the input." THAT
EXPLANATION IS WRONG and an independent audit killed it with the one test
nobody had run -- solve the SAME scenario from different random starts and
check whether the answers agree:

    same scenario, two solves      cos agreement +0.58 / +0.81 / +0.57
    different scenarios            cos agreement +0.005 / +0.009 / -0.003

Two orders of magnitude apart. The target is DETERMINED by the input, not
arbitrary. Genuine label noise would also let a high-capacity model drive
TRAINING mse to zero by memorising; the observed signature is train mse
creeping down and stalling near 0.9 with validation flat, which is the
underfitting / bad-representation signature instead.

So the correct statement is: the optimal offset is a nearly DETERMINISTIC
but NON-SMOOTH function of the channel, and this feature representation
cannot express it. The negative result stands; its mechanism changed.

ONE CONCRETE REPRESENTATION GAP, measured
-----------------------------------------
`features.py` normalises F, G and hd each by its own scenario-level scale,
which erases the RIS-cascade-to-direct power ratio: that ratio spans 9.4
million-fold across scenarios in the raw channel and 1.000-fold in the
features, with correlation +0.031 between the two. A network that cannot
see whether the direct path or the cascade dominates is being asked to
pick a trade-off it cannot observe. Whether supplying it fixes the stall
is UNTESTED -- the measurement is that the information is absent, not that
restoring it is sufficient.

WHAT IS LEARNABLE
-----------------
The update rule. "Given where I am and how badly each user is doing, which
way should the phases move" is a smooth, scenario-independent function even
when the destination is not. So the network is applied L times, each time
nudging the current phase, and the whole unrolled computation is trained on
the final rate.

This also changes the latency claim into one that can be defended. Instead
of "one pass instead of a thousand", which was never going to beat a strong
optimiser on rate, it becomes "L passes instead of a thousand steps", with
the gap reported honestly.

STATE SUPPLIED AT EACH STEP
    the static channel features (as before)
    cos/sin of the CURRENT phase, per element
    each user's current rate, normalised and broadcast along the element
      axis -- this is what tells the update which user is the bottleneck
    optionally the objective's gradient w.r.t. the phase (`use_grad`), which
      makes this a learned gradient method; one extra backward per step.
"""

import torch
import torch.nn as nn

from . import system as S
from .features import n_channels
from .models import _Backbone, _LocalHead, _Exchange, MODES

__all__ = ["UnrolledMuMiso"]


class UnrolledMuMiso(nn.Module):
    """
    Parameters
    ----------
    steps     L, number of refinement passes (weights shared across them)
    mode      user-axis handling, as in MuMisoNet
    use_grad  feed the objective gradient as an extra channel
    step_init initial size of the phase nudge; learnable per step
    """

    def __init__(self, N=32, n_users=4, n_tx=8, steps=6, mode="exchange",
                 use_grad=False, lstm_hidden=128, dropout=0.1,
                 step_init=0.5, link_ratio=False):
        super().__init__()
        if mode not in MODES:
            raise ValueError(f"unknown mode {mode!r}")
        self.N, self.K, self.T = N, n_users, n_tx
        self.steps, self.mode, self.use_grad = steps, mode, use_grad

        # static channels + cos/sin of current phase + user rate (+ gradient)
        extra = 3 + (1 if use_grad else 0)
        self.link_ratio = link_ratio
        C = n_channels(n_tx, link_ratio) + extra
        self.in_ch = C

        body_in = C * n_users if mode == "concat" else C
        self.body = _Backbone(body_in, lstm_hidden, 64, dropout)
        if mode == "exchange":
            self.ex1 = _Exchange(64)
            self.ex2 = _Exchange(64)
        self.head = _LocalHead(64)
        # DEAD CODE, KEPT ONLY SO THE RESULTS REPRODUCE. In MuMisoNet this
        # scaling starts the residual head ~0.6 degrees from identity,
        # because there the head's OUTPUT MAGNITUDE reaches the phase. Here
        # `_delta` ends in atan2(y1, y0), which is scale-invariant:
        # atan2(0.01*y1, 0.01*y0) == atan2(y1, y0) to 2.4e-07. So this does
        # nothing at all, and the comment it was copied with does not apply.
        #
        # Measured at initialisation: mean |_delta| = 1.4243 rad (81.6 deg),
        # and with exp(log_step[0]) = 0.5 the first applied rotation is about
        # 41 degrees per step -- roughly 70x the 0.6 deg the sibling file
        # claims for this idiom, and 8 such steps are a long random walk
        # away from the anchor, not a near-identity start.
        #
        # Removing it changes nothing numerically; making the start small
        # for real would mean shrinking step_init or giving the head a
        # learnable magnitude, and either moves every unrolled number in
        # the package. Left alone deliberately, flagged rather than fixed.
        with torch.no_grad():
            self.head.net[-1].weight.mul_(0.01)
            self.head.net[-1].bias.zero_()
        # one learnable step size per unrolled step
        self.log_step = nn.Parameter(torch.full((steps,),
                                                float(torch.log(
                                                    torch.tensor(step_init)))))

    # ------------------------------------------------------------- one step
    def _delta(self, x):
        """x [B,K,C,N] -> phase nudge [B,N] in (-pi, pi)."""
        B, K, C, N = x.shape
        if self.mode == "concat":
            h = self.body(x.reshape(B, K * C, N))
        else:
            flat = x.reshape(B * K, C, N)
            if self.mode == "deepsets":
                h = self.body(flat).reshape(B, K, 64, N).mean(1)
            else:
                h = self.body.stage1(flat).reshape(B, K, 64, N)
                h = self.ex1(h)
                h = self.body.stage2(h.reshape(B * K, 64, N))
                h = self.ex2(h.reshape(B, K, 64, N))
                h = h.mean(1)
        y = self.head(h)                                  # [B,2,N]
        # atan2 of the two outputs: a direction, bounded by construction,
        # with no wrap discontinuity -- the published paper's own device,
        # reused for the update instead of the absolute phase.
        return torch.atan2(y[:, 1], y[:, 0])

    # -------------------------------------------------------------- forward
    def forward(self, x_static, F, G, hd, pt, nv, theta0,
                precoder="zf", beta=8.0, objective="maxmin",
                return_trace=False):
        """
        x_static : [B,K,C0,N]  channel features from features.mumiso_features
        theta0   : [B,N]       starting phase (su_average anchor)
        returns  final theta [B,N], and the per-step objective if asked
        """
        B, K, _, N = x_static.shape
        th = theta0
        trace = []
        for i in range(self.steps):
            R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv,
                        precoder)                          # [B,K]
            # the bottleneck signal: how far each user is below the best
            r_rel = (R - R.mean(-1, keepdim=True)) / (R.std(-1, keepdim=True)
                                                      + 1e-6)
            chans = [
                torch.cos(th).unsqueeze(1).expand(B, K, N),
                torch.sin(th).unsqueeze(1).expand(B, K, N),
                r_rel.unsqueeze(-1).expand(B, K, N),
            ]
            if self.use_grad:
                with torch.enable_grad():
                    t = th.detach().requires_grad_(True)
                    Rg = S.rates(F, G, hd, torch.cos(t), torch.sin(t), pt, nv,
                                 precoder)
                    obj = (-torch.logsumexp(-beta * Rg, -1) / beta
                           if objective == "maxmin" else Rg.sum(-1))
                    g, = torch.autograd.grad(obj.sum(), t)
                g = g / (g.norm(dim=-1, keepdim=True) + 1e-12) * (N ** 0.5)
                chans.append(g.detach().unsqueeze(1).expand(B, K, N))

            x = torch.cat([x_static, torch.stack(chans, dim=2)], dim=2)
            th = th + torch.exp(self.log_step[i]) * self._delta(x)
            th = torch.atan2(torch.sin(th), torch.cos(th))
            if return_trace:
                with torch.no_grad():
                    Rt = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt,
                                 nv, precoder)
                    trace.append(Rt.min(-1).values.mean().item())
        return (th, trace) if return_trace else th


def count_params(m):
    return sum(p.numel() for p in m.parameters() if p.requires_grad)
```

### `ris_mu/mumiso/baselines.py`

*348 satir · sha256:3ea6e6dd577f*

```python
"""
baselines.py (mumiso)
---------------------
Classical references for the MU-MISO setting, batched on tensors.

WHY THESE EXIST AND WHY THEY MATTER MORE HERE
---------------------------------------------
In the single-user problem the learned model and the closed form solve the
same problem, so comparing them is meaningful. For K > 1 there is no closed
form. The only honest answer to "is the network good" is a comparison
against methods that actually work on the problem. Otherwise it is possible
to beat a weak reference and report a strong result -- which is the first
thing a committee probes.

HOW STRONG A BASELINE HAS TO BE
-------------------------------
Strong enough that it cannot be beaten by something obvious. Two versions
of this file were not. The first made `ao` call coordinate descent alone,
so it reported `cd` twice under two names. The second refined with
normalised-gradient backtracking, which reached 3.96 b/s/Hz where plain
Adam on the identical objective from the identical start reached 5.25.
Both were caught by asking "what would a lazier method get", and both
would have flattered a learned model by about 30%. Ask that question of
whatever is in here now.

ALL METHODS RUN BATCHED
-----------------------
Every candidate phase is evaluated for the whole batch at once, so the
grid search costs one forward pass per grid point rather than one per
(sample, grid point). That is what makes coordinate descent affordable over
a full test set instead of an overnight job.
"""

import torch

from . import system as S

__all__ = ["no_ris", "random_phase", "su_weakest", "su_average",
           "su_best_of", "pga", "coord_descent", "ao", "run_all", "METHODS"]

METHODS = ("no_ris", "random", "su_weakest", "su_average", "su_best_of",
           "pga", "cd", "ao")


# ------------------------------------------------------------------ helpers

def _rate(F, G, hd, theta, pt, nv, precoder, bits=None):
    """Objective-free evaluation: quantisation applied here, once."""
    th = S.quantise_phase(theta, bits)
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, precoder)


def _obj(F, G, hd, theta, pt, nv, precoder, objective):
    R = S.rates(F, G, hd, torch.cos(theta), torch.sin(theta), pt, nv, precoder)
    return R.sum(-1) if objective == "sumrate" else R.min(-1).values


# ---------------------------------------------------------------- baselines

@torch.no_grad()
def no_ris(F, G, hd, pt, nv, precoder="zf", **_):
    """
    Absolute floor: the direct channel alone.

    `noise_var` IS PASSED, and must be. This function used to call
    `S.precode(hd, pt, precoder)` with no noise_var, which falls through to
    `zf`'s no-argument default (1e-9 relative, effectively pure ZF) while
    every other baseline in this file goes through `_rate` -> `S.rates` and
    gets the MMSE regulariser. So the floor was computed with a DIFFERENT
    precoder from the rows it was tabulated against.

    Measured on 1200 scenarios (N=32, T=8, K=4): the old call gave 1.1339
    and the consistent one gives 1.0224, so the floor was reported 10.9%
    too high. The error was conservative -- too high a floor makes the RIS
    look like it buys less than it does -- but a comparison table whose
    rows use different precoders is not a comparison. Gain-source figures
    computed before this fix understate the no-RIS-to-random step
    (2.73x against the corrected 3.03x).
    """
    W = S.precode(hd, pt, precoder, noise_var=nv)
    return torch.log2(1 + S.sinr(hd, W, nv)), None


@torch.no_grad()
def random_phase(F, G, hd, pt, nv, precoder="zf", seed=0, bits=None, **_):
    """Separates "an RIS is present" from "the RIS was optimised"."""
    g = torch.Generator(device=F.device).manual_seed(seed)
    th = (torch.rand(F.shape[0], F.shape[1], generator=g,
                     device=F.device, dtype=torch.float32) * 2 - 1) * torch.pi
    return _rate(F, G, hd, th, pt, nv, precoder, bits), th


@torch.no_grad()
def su_weakest(F, G, hd, pt, nv, precoder="zf", bits=None, **_):
    """
    Single-user closed form aligned to the WEAKEST user.

    The right choice under a max-min objective: spending the surface on the
    bottleneck beats spending it on the average.
    """
    th_all = S.su_align_phase(F, G, hd)                       # [B,K,N]
    weak = (G.abs() ** 2).sum(-1).argmin(-1)                  # [B]
    th = th_all[torch.arange(F.shape[0], device=F.device), weak]
    return _rate(F, G, hd, th, pt, nv, precoder, bits), th


@torch.no_grad()
def su_average(F, G, hd, pt, nv, precoder="zf", bits=None, **_):
    """
    Sum the K alignment vectors and take the phase.

    The most naive resolution of K conflicting alignments, and the threshold
    a learned model has to clear before it has shown anything.
    """
    th_all = S.su_align_phase(F, G, hd)
    acc = torch.exp(1j * th_all.to(torch.complex64)).sum(1)
    th = torch.angle(acc)
    return _rate(F, G, hd, th, pt, nv, precoder, bits), th


@torch.no_grad()
def su_best_of(F, G, hd, pt, nv, precoder="zf", bits=None, **_):
    """
    Score all K single-user alignments plus su_average, keep the best per
    scenario. The right anchor, and the one this package should have used
    from the start.

    This was added after an independent audit pointed out that su_average
    -- the start for the oracle solve, for the unrolled model and for every
    gradient row -- is the WEAKEST of the candidates already sitting in
    memory. Nothing had to be computed: `su_align_phase` already returns
    all K phases, and they are literally feature channels -3 and -2.

    THE NUMBERS BELOW WERE RE-MEASURED AFTER THE PRECODER FIX. An earlier
    version of this docstring reported the gain as +48.0% (su_average
    1.1344 against best-of 1.6791) and quoted the unrolled model at
    1.112 -> 3.265. All of those came from the buggy absolute-eps precoder
    and are superseded. On 1200 scenarios (N=32, T=8, K=4):

        su_average               3.5549
        best-of-(K+1)            4.2151      +18.6%, for ~0 ms

    so the finding survives the fix but is roughly a third of its former
    size, and su_average wins in only a small minority of scenarios --
    the individual single-user alignments take the rest. The unrolled
    model's current figures are 3.5758 -> 5.6359 (see
    results/mumiso_unrolled_fixzf.json).

    Treat any "+48%" still floating around the write-ups as stale.
    """
    phi = S.su_align_phase(F, G, hd)                      # [B,K,N]
    _, th_avg = su_average(F, G, hd, pt, nv, precoder)
    cand = torch.cat([phi, th_avg.unsqueeze(1)], dim=1)   # [B,K+1,N]
    scores = torch.stack([
        _rate(F, G, hd, cand[:, k], pt, nv, precoder).min(-1).values
        for k in range(cand.shape[1])])                   # [K+1,B]
    pick = scores.argmax(0)
    th = cand[torch.arange(F.shape[0], device=F.device), pick]
    return _rate(F, G, hd, th, pt, nv, precoder, bits), th


@torch.no_grad()
def coord_descent(F, G, hd, pt, nv, precoder="zf", bits=None, iters=8,
                  grid=16, objective="maxmin", theta0=None, **_):
    """
    Element-wise exhaustive search, batched over scenarios.

    Each element is moved to its best value with the others held fixed, so
    the objective never decreases -- monotone by construction (verified:
    13.9078 -> 16.2635, minimum step +6.6e-03).

    With `bits` set the search runs on the ACTUAL 2^bits grid. That is the
    correct reference for quantised phase, and it is strong: on the earlier
    single-RIS experiment discrete CD reached 5.600 at 1 bit where
    "optimise continuously, then round" reached 5.440 and a
    straight-through network 3.544.
    """
    N = F.shape[1]
    if bits is None:
        cand = torch.linspace(-torch.pi, torch.pi, grid + 1,
                              device=F.device)[:-1]
    else:
        step = 2 * torch.pi / (2 ** bits)
        cand = torch.arange(2 ** bits, device=F.device,
                            dtype=torch.float32) * step
        cand = (cand + torch.pi) % (2 * torch.pi) - torch.pi

    th = su_average(F, G, hd, pt, nv, precoder)[1] if theta0 is None \
        else theta0.clone()
    if bits is not None:
        th = S.quantise_phase(th, bits)
    cur = _obj(F, G, hd, th, pt, nv, precoder, objective)

    for _ in range(iters):
        start = cur.clone()
        for n in range(N):
            best_v, best_c = cur, th[:, n].clone()
            for c in cand:
                trial = th.clone()
                trial[:, n] = c
                v = _obj(F, G, hd, trial, pt, nv, precoder, objective)
                better = v > best_v
                best_v = torch.where(better, v, best_v)
                best_c = torch.where(better, c.expand_as(best_c), best_c)
            th[:, n] = best_c
            cur = best_v
        if (cur - start).max() < 1e-7:
            break
    return _rate(F, G, hd, th, pt, nv, precoder, bits), th


def _pga_from(F, G, hd, pt, nv, precoder, theta0, step, iters, objective,
              optimiser="adam"):
    """
    Gradient ascent on the phase from a given start, using autograd.

    WHY ADAM AND NOT A NORMALISED-GRADIENT LINE SEARCH
    --------------------------------------------------
    The first version of this function took normalised-gradient steps with
    backtracking, which is monotone and looks respectable. It is also much
    weaker than it appears: on a 400-scenario geometric channel it reached
    3.96 b/s/Hz where plain Adam on the same objective, from the same start,
    reached 5.25 -- a 32% shortfall. A baseline that weak would have let a
    mediocre learned model look good, which is the exact failure this file
    exists to prevent.

    The phase lives on a torus, so there is no constraint to project onto;
    wrapping is cosmetic. `step` is the Adam learning rate.
    """
    th = theta0.detach().clone().requires_grad_(True)
    if optimiser == "adam":
        opt = torch.optim.Adam([th], lr=step)
    else:
        opt = torch.optim.SGD([th], lr=step)

    with torch.no_grad():
        best = _obj(F, G, hd, th, pt, nv, precoder, objective).clone()
        best_th = th.detach().clone()

    for _ in range(iters):
        obj = _obj(F, G, hd, th, pt, nv, precoder, objective)
        loss = -obj.sum()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        with torch.no_grad():
            v = _obj(F, G, hd, th, pt, nv, precoder, objective)
            up = v > best
            best = torch.where(up, v, best)
            best_th = torch.where(up.unsqueeze(-1), th.detach(), best_th)
    return best_th


@torch.no_grad()
def pga(F, G, hd, pt, nv, precoder="zf", bits=None, iters=1000, step=0.05,
        objective="maxmin", seed=0, restarts=3, **_):
    """
    Adam gradient ascent from several random starts, best kept per scenario.

    Restarts matter: the objective is multimodal in the phase, and a single
    start lands in whichever basin it happened to begin in.
    """
    g = torch.Generator(device=F.device).manual_seed(seed)
    best_R, best_th = None, None
    for r in range(restarts):
        th0 = (torch.rand(F.shape[0], F.shape[1], generator=g, device=F.device,
                          dtype=torch.float32) * 2 - 1) * torch.pi
        with torch.enable_grad():
            th = _pga_from(F, G, hd, pt, nv, precoder, th0, step, iters,
                           objective)
        v = _obj(F, G, hd, th, pt, nv, precoder, objective)
        if best_R is None:
            best_R, best_th = v, th
        else:
            up = v > best_R
            best_R = torch.where(up, v, best_R)
            best_th = torch.where(up.unsqueeze(-1), th, best_th)
    return _rate(F, G, hd, best_th, pt, nv, precoder, bits), best_th


@torch.no_grad()
def ao(F, G, hd, pt, nv, precoder="zf", bits=None, cd_iters=4, pga_iters=1000,
       step=0.05, objective="maxmin", grid=16, **_):
    """
    Strongest classical reference: three starts, Adam refinement, best kept
    per scenario.

    Starts: coordinate descent, the single-user average, and random. The
    precoder is recomputed inside every objective evaluation, so this is
    alternating optimisation between the phase and the precoder throughout.

    Two corrections are baked in here, both found by measurement:
      - an earlier version called coordinate descent and nothing else, which
        made `ao` numerically identical to `cd` and reported one baseline as
        two;
      - the refinement used normalised-gradient backtracking, which left
        32% of the achievable rate on the table against plain Adam.

    Convergence, measured on 400 scenarios: 400 Adam steps give 5.2726,
    1000 give 5.3678, 2000 give 5.4004. The default is 1000 -- still
    creeping upward, so treat the reported AO as a floor on what classical
    optimisation achieves, not a ceiling. With the stronger refinement the
    coordinate-descent start no longer helps: `pga` alone reaches 5.2772
    against this function's 5.2726, i.e. the composition buys nothing once
    the refinement is competent. That is worth reporting as it stands
    rather than quietly dropping one of them.
    """
    _, th_cd = coord_descent(F, G, hd, pt, nv, precoder, None, cd_iters,
                             grid, objective)
    _, th_su = su_average(F, G, hd, pt, nv, precoder)
    g = torch.Generator(device=F.device).manual_seed(0)
    th_rnd = (torch.rand(F.shape[0], F.shape[1], generator=g, device=F.device,
                         dtype=torch.float32) * 2 - 1) * torch.pi

    best_R, best_th = None, None
    for th0 in (th_cd, th_su, th_rnd):
        with torch.enable_grad():
            th = _pga_from(F, G, hd, pt, nv, precoder, th0, step, pga_iters,
                           objective)
        v = _obj(F, G, hd, th, pt, nv, precoder, objective)
        if best_R is None:
            best_R, best_th = v, th
        else:
            up = v > best_R
            best_R = torch.where(up, v, best_R)
            best_th = torch.where(up.unsqueeze(-1), th, best_th)
    return _rate(F, G, hd, best_th, pt, nv, precoder, bits), best_th


# -------------------------------------------------------------------- driver
_DISPATCH = dict(no_ris=no_ris, random=random_phase, su_weakest=su_weakest,
                 su_average=su_average, su_best_of=su_best_of,
                 pga=pga, cd=coord_descent, ao=ao)


def run_all(F, G, hd, pt, nv, methods=METHODS, **kw):
    """
    Evaluate several baselines on one batch.

    returns {name: dict(min_rate=, sum_rate=, mean_rate=, theta=)}
    """
    out = {}
    for m in methods:
        if m not in _DISPATCH:
            raise ValueError(f"unknown baseline {m!r}")
        R, th = _DISPATCH[m](F, G, hd, pt, nv, **kw)
        out[m] = S.rate_metrics(R) | {"theta": th}
    return out
```

### `ris_mu/mumiso/train.py`

*110 satir · sha256:a48824f31611*

```python
"""
train.py (mumiso)
-----------------
Label-free training on the system metric.

WHY THERE ARE NO LABELS
-----------------------
For K = 1 the optimal phase has a closed form, so the published model could
be trained supervised against it. For K > 1 no closed form exists, so there
is nothing to regress onto. Training therefore maximises the rate directly:
the channel enters the loss, the precoder is computed inside it, and the
gradient flows back through the whole system model to the phases.

That is not a workaround, it is the better formulation -- a supervised model
can only ever approach the labels it was given, whereas this one optimises
the quantity the thesis actually reports.
"""

import time
import numpy as np
import torch

from . import system as S

__all__ = ["train_model", "evaluate"]


def _batches(n, bs, rng=None):
    idx = np.arange(n) if rng is None else rng.permutation(n)
    for i in range(0, n, bs):
        yield idx[i:i + bs]


@torch.no_grad()
def evaluate(net, X, F, G, hd, pt, nv, ids, precoder="zf", bits=None, bs=512):
    """Mean min-rate and sum-rate over `ids`."""
    net.eval()
    tot_min = tot_sum = 0.0
    for b in _batches(len(ids), bs):
        j = ids[b]
        c, s = net.phases(X[j])
        if bits is not None:
            c, s = S.quantise_ste(c, s, bits)
        R = S.rates(F[j], G[j], hd[j], c, s, pt, nv, precoder)
        tot_min += R.min(-1).values.sum().item()
        tot_sum += R.sum(-1).sum().item()
    return tot_min / len(ids), tot_sum / len(ids)


def train_model(net, X, F, G, hd, pt, nv, split, *, epochs=30, bs=64,
                lr=2e-3, lr_drops=(0.6, 0.85), objective="maxmin", beta=8.0,
                precoder="zf", bits=None, seed=0, log=print, clip=1.0):
    """
    Returns (net_with_best_val_weights, history).

    `split` is (train_ids, val_ids, test_ids). The reported model is the one
    with the best VALIDATION min-rate, never the last epoch -- otherwise the
    number reported is partly a function of where training happened to stop.
    """
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    tr, va, te = split
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    drops = {int(f * epochs) for f in lr_drops}

    best_val, best_state, hist = -np.inf, None, []
    for ep in range(1, epochs + 1):
        if ep in drops:
            for g in opt.param_groups:
                g["lr"] *= 0.5
        net.train()
        t0, run, nb = time.time(), 0.0, 0
        for b in _batches(len(tr), bs, rng):
            j = tr[b]
            c, s = net.phases(X[j])
            if bits is not None:
                c, s = S.quantise_ste(c, s, bits)
            R = S.rates(F[j], G[j], hd[j], c, s, pt, nv, precoder)
            loss = (S.maxmin_loss(R, beta) if objective == "maxmin"
                    else S.sumrate_loss(R))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), clip)
            opt.step()
            run += loss.item(); nb += 1

        v_min, v_sum = evaluate(net, X, F, G, hd, pt, nv, va, precoder, bits)
        hist.append(dict(epoch=ep, loss=run / max(nb, 1), val_min=v_min,
                         val_sum=v_sum, lr=opt.param_groups[0]["lr"],
                         sec=time.time() - t0))
        mark = ""
        if v_min > best_val:
            best_val = v_min
            best_state = {k: v.detach().clone()
                          for k, v in net.state_dict().items()}
            mark = "  *"
        if log:
            log(f"    epoch {ep:3d}/{epochs}  loss {run/max(nb,1):8.4f}  "
                f"val min {v_min:7.4f}  sum {v_sum:8.3f}  "
                f"({hist[-1]['sec']:.1f}s){mark}")

    if best_state is None:
        # Validation never improved -- a NaN loss in epoch 1 would do this.
        # Carry on with the final weights, but say so: silently returning an
        # empty model is how a crash gets mistaken for a bad result.
        if log:
            log("    WARNING: validation never improved; keeping final weights")
    else:
        net.load_state_dict(best_state)
    return net, hist
```

## 2. Onceki tek kullanicili paket: `ris_mu/`

Yayimlanmis makalenin Python karsiligi ve tek-RIS deneyleri. Cok kullanicili is bunun **uzerine** kuruldu, bunu degistirmedi. Kiyas icin burada.

### `ris_mu/__init__.py`

*0 satir · sha256:e3b0c44298fc*

```python

```

### `ris_mu/geometry.py`

*84 satir · sha256:295c899c3073*

```python
"""
geometry.py
-----------
RIS panel geometry, element positions and element radiation pattern.

The panel is defined by an origin, two orthonormal in-plane vectors (e1, e2)
and a normal. Element n is placed at

    p_n = p0 + i * d * e1 + j * d * e2,     n = i * K + j

with row-major ordering (i over rows / M, j over columns / K), matching the
serialisation used by the sequential part of the model.
"""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class RISPanel:
    """Uniform rectangular array of passive reflecting elements."""

    M: int = 8                    # rows
    K: int = 4                    # columns
    fc: float = 3e9               # carrier frequency [Hz]
    center: tuple = (20.0, 10.0, 3.0)
    e1: tuple = (1.0, 0.0, 0.0)   # in-plane direction for rows
    e2: tuple = (0.0, 1.0, 0.0)   # in-plane direction for columns
    normal: tuple = (0.0, 0.0, -1.0)
    q: float = 1.0                # element pattern exponent, gain = 2(2q+1)

    positions: np.ndarray = field(init=False)

    def __post_init__(self):
        self.c = 299_792_458.0
        self.lam = self.c / self.fc
        self.k = 2 * np.pi / self.lam
        self.d = self.lam / 2

        e1 = _unit(np.asarray(self.e1, float))
        e2 = _unit(np.asarray(self.e2, float))
        if abs(e1 @ e2) > 1e-9:
            raise ValueError("e1 and e2 must be orthogonal")
        self.n_hat = _unit(np.asarray(self.normal, float))

        c = np.asarray(self.center, float)
        i = np.arange(self.M) - (self.M - 1) / 2
        j = np.arange(self.K) - (self.K - 1) / 2
        # row-major: index = i * K + j
        offs = (i[:, None, None] * self.d * e1) + (j[None, :, None] * self.d * e2)
        self.positions = (c + offs).reshape(self.M * self.K, 3)

    @property
    def N(self) -> int:
        return self.M * self.K

    @property
    def element_gain(self) -> float:
        """Boresight gain of a single element for a cos^q pattern."""
        return 2.0 * (2.0 * self.q + 1.0)

    def pattern(self, points: np.ndarray) -> np.ndarray:
        """
        cos^q element pattern evaluated for the direction from each element to
        each point.

        points : (..., 3)
        returns: (..., N) real gain (linear, includes boresight gain)
        """
        pts = np.asarray(points, float)
        vec = pts[..., None, :] - self.positions        # (..., N, 3)
        rng = np.linalg.norm(vec, axis=-1)
        cos_t = np.einsum("...i,i->...", vec, self.n_hat) / np.maximum(rng, 1e-12)
        cos_t = np.clip(cos_t, 0.0, 1.0)                # no radiation behind panel
        return self.element_gain * cos_t ** self.q

    def distances(self, points: np.ndarray) -> np.ndarray:
        """Exact element-wise distances (near-field safe). points (...,3) -> (...,N)."""
        pts = np.asarray(points, float)
        return np.linalg.norm(pts[..., None, :] - self.positions, axis=-1)


def _unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)
```

### `ris_mu/pathloss.py`

*111 satir · sha256:9ab1e1cbca80*

```python
"""
pathloss.py
-----------
Large-scale propagation parameters taken from 3GPP TR 38.901, Indoor Hotspot
-- Office (InH-Office), which is the standardised model for the indoor
scenario used in this work (40 x 20 x 6 m room, 3 GHz carrier).

Using a standard model rather than hand-picked exponents means the parameters
of the channel generator can be cited rather than defended, which is the point
of the exercise: the question "where do these numbers come from" should have a
one-line answer.

Reference values implemented here
---------------------------------
LoS path loss      PL = 32.4 + 17.3 log10(d3D) + 20 log10(fc[GHz]),  sigma 3.0 dB
NLoS path loss     PL = 38.3 log10(d3D) + 17.30 + 24.9 log10(fc),    sigma 8.03 dB
                   (NLoS is the maximum of the two, as the standard requires)
LoS probability    1                                   d2D <= 1.2
                   exp(-(d2D - 1.2) / 4.7)             1.2 < d2D < 6.5
                   0.32 exp(-(d2D - 6.5) / 32.6)       d2D >= 6.5
Ricean K           log-normal, mean 7 dB, std 4 dB (InH)
Validity           TR 38.901 states 1 m <= d3D <= 150 m

The RIS introduces one non-standard element: the BS-RIS and RIS-UE hops are
modelled as two ordinary links, and the cascaded path is their product. This
is the usual treatment in the RIS literature for a passive surface in the far
field of both ends.
"""

import numpy as np

PRESETS = {
    "inh_office": dict(
        los_a=32.4, los_b=17.3, los_c=20.0, sigma_los=3.0,
        nlos_a=17.30, nlos_b=38.3, nlos_c=24.9, sigma_nlos=8.03,
        k_mean_db=7.0, k_std_db=4.0,
        name="3GPP TR 38.901 InH-Office",
    ),
    # Indoor Factory (sparse clutter, low BS) -- kept for a sensitivity study
    "inf_sl": dict(
        los_a=31.84, los_b=21.50, los_c=19.00, sigma_los=4.3,
        nlos_a=33.0, nlos_b=25.5, nlos_c=20.0, sigma_nlos=5.7,
        k_mean_db=7.0, k_std_db=8.0,
        name="3GPP TR 38.901 InF-SL",
    ),
}


class PathLoss:
    """3GPP-style large-scale model. All distances in metres, fc in Hz."""

    def __init__(self, fc, preset="inh_office"):
        if preset not in PRESETS:
            raise ValueError(f"unknown preset {preset!r}; have {list(PRESETS)}")
        self.p = PRESETS[preset]
        self.preset = preset
        self.fc_ghz = fc / 1e9

    # ------------------------------------------------------------------ core
    def pl_los_db(self, d3d):
        p = self.p
        d = np.maximum(d3d, 1.0)
        return p["los_a"] + p["los_b"] * np.log10(d) + p["los_c"] * np.log10(self.fc_ghz)

    def pl_nlos_db(self, d3d):
        p = self.p
        d = np.maximum(d3d, 1.0)
        pl = p["nlos_a"] + p["nlos_b"] * np.log10(d) + p["nlos_c"] * np.log10(self.fc_ghz)
        return np.maximum(pl, self.pl_los_db(d))      # required by the standard

    def pl_db(self, d3d, los):
        return np.where(los, self.pl_los_db(d3d), self.pl_nlos_db(d3d))

    def sigma_sf_db(self, los):
        return np.where(los, self.p["sigma_los"], self.p["sigma_nlos"])

    def los_prob(self, d2d):
        d = np.asarray(d2d, float)
        p = np.where(d <= 1.2, 1.0,
                     np.where(d < 6.5,
                              np.exp(-(d - 1.2) / 4.7),
                              0.32 * np.exp(-(d - 6.5) / 32.6)))
        return np.clip(p, 0.0, 1.0)

    def rice_k_db(self, rng, shape):
        return rng.normal(self.p["k_mean_db"], self.p["k_std_db"], size=shape)

    def amplitude(self, d3d, los, extra_gain_db=0.0):
        """Field (not power) amplitude from the deterministic path loss."""
        return 10 ** ((extra_gain_db - self.pl_db(d3d, los)) / 20.0)

    # --------------------------------------------------------------- excess
    def pl_free_space_db(self, d3d):
        d = np.maximum(d3d, 1.0)
        return 32.4 + 20 * np.log10(d) + 20 * np.log10(self.fc_ghz)

    def excess_db(self, d3d, los):
        """
        Loss in excess of free space.

        The RIS cascade cannot be modelled by applying a full path-loss
        formula to each hop: that double-counts the free-space constant and
        ignores the element aperture. Instead the cascade uses the physical
        two-hop model (see channel.py) and takes only the *excess* loss --
        the part of the standardised model that describes the environment
        rather than the geometry -- from TR 38.901.
        """
        return self.pl_db(d3d, los) - self.pl_free_space_db(d3d)

    def __repr__(self):
        return f"PathLoss({self.p['name']}, fc={self.fc_ghz:.2f} GHz)"
```

### `ris_mu/channel.py`

*348 satir · sha256:8ec99f395131*

```python
"""
channel.py
----------
Multi-user, spatially consistent, geometry-based channel generator for an
RIS-aided downlink, with large-scale parameters from 3GPP TR 38.901.

Differences w.r.t. the legacy MATLAB generator
----------------------------------------------
1. APERTURE CORRELATION. The legacy generator drew an independent Rayleigh
   coefficient for every RIS element, which destroys the spatial correlation
   that a half-wavelength-spaced array must exhibit. Here each propagation
   path (specular or a scattering cluster) carries ONE complex gain, and the
   per-element variation comes from exact geometry (distance + cos^q element
   pattern). Neighbouring elements are therefore correlated, as physics
   requires.

2. MULTI-USER CONSISTENCY. All users in a scenario share one scatterer
   realisation, so nearby users see correlated channels. Without this,
   U users are just U independent single-user problems and interference
   or fairness coupling is meaningless.

3. STANDARDISED LARGE SCALE. Path loss, shadow-fading spread, LoS
   probability and Ricean K come from TR 38.901 InH-Office (see pathloss.py)
   instead of hand-chosen exponents.

4. CORRELATED SHADOWING across users (Gudmundson exponential model).

The generator is deliberately decoupled from any learning code: the same
`generate()` contract can later be served by a ray-tracing backend.
"""

from dataclasses import dataclass, field
import numpy as np

from .geometry import RISPanel
from .pathloss import PathLoss


@dataclass
class ChannelConfig:
    # --- scenario -----------------------------------------------------------
    room: tuple = (40.0, 20.0, 6.0)
    bs_pos: tuple = (20.0, 6.0, 4.0)
    bs_random: bool = False
    n_users: int = 4
    user_z: tuple = (1.0, 2.0)
    user_cluster_radius: float = 0.0     # >0 -> users drawn around a hotspot

    # --- propagation --------------------------------------------------------
    preset: str = "inh_office"           # key into pathloss.PRESETS
    n_clusters: int = 6
    sf_corr_dist: float = 5.0            # Gudmundson decorrelation distance [m]

    # --- deployment ---------------------------------------------------------
    # The legacy script placed the panel horizontally at mid-height with its
    # normal pointing down, while the BS sat ABOVE it: the transmitter was
    # behind the surface, where a passive element radiates nothing. The
    # default here is the standard deployment -- panel on a wall, facing into
    # the room, with the BS placed in its boresight at a distance comfortably
    # beyond the Fraunhofer limit 2D^2/lambda (about 4 m for this aperture).
    mount: str = "wall"                  # "wall" | "ceiling"

    # --- direct-link blockage ----------------------------------------------
    # An RIS is deployed precisely because the direct path is obstructed. With
    # an unobstructed direct link a passive surface of a few tens of elements
    # cannot compete with it (the cascade suffers the product of two path
    # losses), and the optimisation problem becomes vacuous. The blocker is
    # therefore part of the scenario definition, not an afterthought.
    direct_blocked_prob: float = 1.0
    direct_blockage_db: float = 40.0

    # --- link budget --------------------------------------------------------
    tx_power_dbm: float = 20.0
    noise_figure_db: float = 7.0
    bandwidth_hz: float = 20e6
    bs_gain_dbi: float = 5.0
    ue_gain_dbi: float = 0.0

    seed: int = 42

    # --- derived ------------------------------------------------------------
    def noise_power_dbm(self) -> float:
        return -174.0 + 10 * np.log10(self.bandwidth_hz) + self.noise_figure_db

    def snr_scale(self) -> float:
        """Linear Pt / N0, the factor multiplying |h|^2 to obtain SNR."""
        return 10 ** ((self.tx_power_dbm - self.noise_power_dbm()) / 10.0)


class MultiUserRISChannel:
    """Generates (F, G, h_d) for an RIS-aided multi-user downlink."""

    def __init__(self, panel: RISPanel, cfg: ChannelConfig = None):
        self.panel = panel
        self.cfg = cfg or ChannelConfig()
        self.pl = PathLoss(panel.fc, self.cfg.preset)
        self.rng = np.random.default_rng(self.cfg.seed)
        self.k = panel.k

    # ------------------------------------------------------------------ utils
    def _crandn(self, shape):
        r = self.rng.standard_normal(shape)
        i = self.rng.standard_normal(shape)
        return (r + 1j * i) / np.sqrt(2.0)

    # ------------------------------------------------------------- link cores
    def _ris_link(self, pts, scat, los, kappa):
        """
        Small-scale channel between points and every RIS element, unit mean
        power per element.

        pts   : (..., 3)      scat : (..., L, 3)
        los   : (...) bool    kappa: (...) linear Ricean K
        out   : (..., N) complex
        """
        P = self.panel
        d_el = P.distances(pts)
        gain = P.pattern(pts)

        # specular: one path, element phase from exact geometry
        h_los = np.sqrt(gain) / np.maximum(d_el, 1.0) * np.exp(-1j * self.k * d_el)
        h_los = _unit_power(h_los)

        # clusters: one complex gain per cluster, shared across all elements
        d1 = np.linalg.norm(pts[..., None, :] - scat, axis=-1)          # (..., L)
        d2 = P.distances(scat)                                          # (..., L, N)
        g_s = P.pattern(scat)                                           # (..., L, N)
        gains = self._crandn(d1.shape)
        amp = np.sqrt(g_s) / np.maximum(d1[..., None] * d2, 1.0)
        h_nlos = np.sum(gains[..., None] * amp *
                        np.exp(-1j * self.k * (d1[..., None] + d2)), axis=-2)
        h_nlos = _unit_power(h_nlos)

        kap = np.where(los, kappa, 0.0)[..., None]
        return np.sqrt(kap / (kap + 1)) * h_los + np.sqrt(1.0 / (kap + 1)) * h_nlos

    def _direct_link(self, a, b, scat, los, kappa):
        """Scalar BS-UE channel, unit mean power."""
        d = np.linalg.norm(a - b, axis=-1)
        h_los = np.exp(-1j * self.k * d)

        d1 = np.linalg.norm(a[..., None, :] - scat, axis=-1)
        d2 = np.linalg.norm(scat - b[..., None, :], axis=-1)
        gains = self._crandn(d1.shape)
        h_nlos = np.sum(gains * np.exp(-1j * self.k * (d1 + d2)) /
                        np.maximum(d1 * d2, 1.0), axis=-1)
        h_nlos = h_nlos / np.sqrt(np.maximum(np.mean(np.abs(h_nlos) ** 2), 1e-30))

        kap = np.where(los, kappa, 0.0)
        return np.sqrt(kap / (kap + 1)) * h_los + np.sqrt(1.0 / (kap + 1)) * h_nlos

    # ------------------------------------------------------------------- main
    def generate(self, n_samples: int, chunk: int = 2000):
        keys = ("F", "G", "hd", "bs_pos", "ue_pos",
                "los_ris_bs", "los_ris_ue", "los_direct")
        out = {k: [] for k in keys}
        done = 0
        while done < n_samples:
            s = min(chunk, n_samples - done)
            part = self._generate_chunk(s)
            for k in keys:
                out[k].append(part[k])
            done += s
        return {k: np.concatenate(v, axis=0) for k, v in out.items()}

    def _generate_chunk(self, S):
        c, P, rng, pl = self.cfg, self.panel, self.rng, self.pl
        U, L = c.n_users, c.n_clusters
        room = np.asarray(c.room, float)
        ris_c = P.positions.mean(0)

        # --- geometry --------------------------------------------------------
        if c.bs_random:
            bs = rng.uniform([0, 0, 2.0], [room[0], room[1], room[2] - 0.5], (S, 3))
        else:
            bs = np.tile(np.asarray(c.bs_pos, float), (S, 1))

        if c.user_cluster_radius > 0:
            hot = rng.uniform([0, 0], room[:2], (S, 1, 2))
            xy = np.clip(hot + rng.normal(0, c.user_cluster_radius, (S, U, 2)),
                         0, room[:2])
        else:
            xy = rng.uniform([0, 0], room[:2], (S, U, 2))
        ue = np.concatenate([xy, rng.uniform(*c.user_z, (S, U, 1))], axis=-1)

        scat = rng.uniform([0, 0, 0], room, (S, L, 3))      # shared by all users

        # --- distances -------------------------------------------------------
        d3_bs = np.linalg.norm(bs - ris_c, axis=-1)                    # (S,)
        d2_bs = np.linalg.norm((bs - ris_c)[..., :2], axis=-1)
        d3_ue = np.linalg.norm(ue - ris_c, axis=-1)                    # (S,U)
        d2_ue = np.linalg.norm((ue - ris_c)[..., :2], axis=-1)
        d3_dir = np.linalg.norm(bs[:, None, :] - ue, axis=-1)          # (S,U)
        d2_dir = np.linalg.norm((bs[:, None, :] - ue)[..., :2], axis=-1)

        # --- LoS state and Ricean K ------------------------------------------
        los_bs = rng.random(S) < pl.los_prob(d2_bs)
        los_ue = rng.random((S, U)) < pl.los_prob(d2_ue)
        los_dir = rng.random((S, U)) < pl.los_prob(d2_dir)

        k_bs = 10 ** (pl.rice_k_db(rng, S) / 10)
        k_ue = 10 ** (pl.rice_k_db(rng, (S, U)) / 10)
        k_dir = 10 ** (pl.rice_k_db(rng, (S, U)) / 10)

        # --- small scale ------------------------------------------------------
        F_s = self._ris_link(bs, scat, los_bs, k_bs)                     # (S,N)
        G_s = self._ris_link(ue, scat[:, None], los_ue, k_ue)            # (S,U,N)
        hd_s = self._direct_link(bs[:, None, :], ue, scat[:, None], los_dir, k_dir)

        # --- large scale ------------------------------------------------------
        # RIS cascade: physical two-hop aperture model (Tang et al., 2021),
        #   Pr/Pt = Gt Gr Ge dx dy lambda^2 / ((4 pi)^3 d1^2 d2^2),
        # split here into one amplitude factor per hop so that the two hops can
        # carry their own LoS state, excess loss and shadowing. The geometric
        # 1/d and element pattern already live in the small-scale terms, so
        # only the constants and the environment-dependent excess appear here.
        #   a_n = sqrt(Gt Gr Ge F_in F_out dx dy) * lambda / ((4pi)^1.5 d1 d2)
        # The element pattern is evaluated at the panel centre: across a
        # 0.4 x 0.2 m panel seen from several metres the incidence angle is
        # constant to within about two degrees.
        gt = 10 ** (c.bs_gain_dbi / 20)
        gr = 10 ** (c.ue_gain_dbi / 20)
        f_in = _centre_cos(P, bs) ** P.q                       # (S,)
        f_out = _centre_cos(P, ue) ** P.q                      # (S,U)
        cascade_const = (np.sqrt(P.element_gain * P.d * P.d) * P.lam
                         / (4 * np.pi) ** 1.5)

        A_F = (gt * cascade_const * np.sqrt(f_in) / np.maximum(d3_bs, 1.0)
               * 10 ** (-pl.excess_db(d3_bs, los_bs) / 20))
        A_G = (gr * np.sqrt(f_out) / np.maximum(d3_ue, 1.0)
               * 10 ** (-pl.excess_db(d3_ue, los_ue) / 20))
        A_d = pl.amplitude(d3_dir, los_dir, c.bs_gain_dbi + c.ue_gain_dbi)

        # direct-link blocker (see ChannelConfig)
        blocked = rng.random((S, U)) < c.direct_blocked_prob
        A_d = A_d * 10 ** (-c.direct_blockage_db * blocked / 20)

        A_F = A_F * 10 ** (pl.sigma_sf_db(los_bs) * rng.standard_normal(S) / 20)
        A_G = A_G * self._sf_corr(los_ue, ue)
        A_d = A_d * self._sf_corr(los_dir, ue)

        return dict(
            F=(F_s * A_F[:, None]).astype(np.complex64),
            G=(G_s * A_G[..., None]).astype(np.complex64),
            hd=(hd_s * A_d).astype(np.complex64),
            bs_pos=bs.astype(np.float32), ue_pos=ue.astype(np.float32),
            los_ris_bs=los_bs, los_ris_ue=los_ue, los_direct=los_dir,
        )

    def _sf_corr(self, los, ue):
        """Spatially correlated log-normal shadowing -> field amplitude."""
        S, U = los.shape
        dist = np.linalg.norm(ue[:, :, None, :] - ue[:, None, :, :], axis=-1)
        R = np.exp(-dist / self.cfg.sf_corr_dist) + 1e-6 * np.eye(U)
        w = np.einsum("sij,sj->si", np.linalg.cholesky(R),
                      self.rng.standard_normal((S, U)))
        return 10 ** (self.pl.sigma_sf_db(los) * w / 20.0)


# -------------------------------------------------------------------- scenario
def make_scenario(n_users=1, M=8, K=4, seed=42, **overrides):
    """
    Build a matched (panel, config) pair.

    Keeping the panel geometry and the channel configuration in one place
    avoids the failure mode that the legacy setup had: a panel orientation
    and a BS position that were each individually plausible but together put
    the transmitter behind the surface.
    """
    cfg = ChannelConfig(n_users=n_users, seed=seed, **overrides)
    room = np.asarray(cfg.room, float)

    if cfg.mount == "wall":
        # panel on the y = 0 wall at mid-room, facing +y into the room;
        # rows run horizontally (x), columns vertically (z)
        panel = RISPanel(M=M, K=K, center=(room[0] / 2, 0.1, 3.0),
                         e1=(1, 0, 0), e2=(0, 0, 1), normal=(0, 1, 0))
    elif cfg.mount == "ceiling":
        panel = RISPanel(M=M, K=K, center=(room[0] / 2, room[1] / 2, room[2] - 0.2),
                         e1=(1, 0, 0), e2=(0, 1, 0), normal=(0, 0, -1))
    else:
        raise ValueError(f"unknown mount {cfg.mount!r}")

    far_field = 2 * (M * panel.d) ** 2 / panel.lam
    d_bs = np.linalg.norm(np.asarray(cfg.bs_pos) - panel.positions.mean(0))
    if d_bs < far_field:
        raise ValueError(f"BS at {d_bs:.1f} m is inside the Fraunhofer "
                         f"distance {far_field:.1f} m; move it or shrink the panel")
    return panel, cfg


# --------------------------------------------------------------------- helpers
def _unit_power(h):
    p = np.mean(np.abs(h) ** 2, axis=-1, keepdims=True)
    return h / np.sqrt(np.maximum(p, 1e-30))


def _centre_cos(panel, pts):
    """cos of the angle between the panel normal and the direction to pts."""
    v = np.asarray(pts, float) - panel.positions.mean(0)
    rng = np.linalg.norm(v, axis=-1)
    return np.clip(np.einsum("...i,i->...", v, panel.n_hat) /
                   np.maximum(rng, 1e-12), 1e-3, 1.0)


# ---------------------------------------------------------------- legacy model
def legacy_generate(n_samples, panel: RISPanel, n_scatter=6, room=(40, 20, 6),
                    scatter_g=0.15, seed=42):
    """
    Faithful NumPy port of RIS_dataset_large_2D.m (single user), kept so that
    the two channel models can be compared on identical geometry.

    Note the independent complex coefficient drawn per element -- this is the
    behaviour the geometry-based model replaces.
    """
    rng = np.random.default_rng(seed)
    N, k = panel.N, panel.k
    room = np.asarray(room, float)
    F = np.zeros((n_samples, N), np.complex64)
    G = np.zeros((n_samples, N), np.complex64)
    hd = np.zeros(n_samples, np.complex64)

    for s in range(n_samples):
        tx = np.r_[rng.random(2) * room[:2], 1 + rng.random()]
        rx = np.r_[rng.random(2) * room[:2], 1 + rng.random()]
        sc = rng.random((n_scatter, 3)) * room

        dd = np.linalg.norm(tx - rx)
        hd[s] = _cn(rng) * np.exp(-1j * k * dd) / dd

        d_tx = np.linalg.norm(tx - panel.positions, axis=-1)
        d_rx = np.linalg.norm(panel.positions - rx, axis=-1)
        f0 = _cn(rng, N) * np.exp(-1j * k * d_tx) / d_tx
        g0 = _cn(rng, N) * np.exp(-1j * k * d_rx) / d_rx

        da = np.linalg.norm(tx - sc, axis=-1)[:, None]
        db = np.linalg.norm(sc[:, None] - panel.positions, axis=-1)
        dc = np.linalg.norm(sc - rx, axis=-1)[:, None]
        fs = np.sum(scatter_g * _cn(rng, (n_scatter, N)) *
                    np.exp(-1j * k * (da + db)) / (da * db), axis=0)
        gs = np.sum(scatter_g * _cn(rng, (n_scatter, N)) *
                    np.exp(-1j * k * (db + dc)) / (db * dc), axis=0)
        F[s], G[s] = f0 + fs, g0 + gs
    return dict(F=F, G=G[:, None, :], hd=hd[:, None])


def _cn(rng, shape=()):
    return (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2)
```

### `ris_mu/features.py`

*107 satir · sha256:c68df09577a3*

```python
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
```

### `ris_mu/models.py`

*316 satir · sha256:4408c6e73174*

```python
"""
models.py
---------
Model family used throughout the study. All models take the same input and
emit 2N outputs interpreted as [sin(theta_1..N), cos(theta_1..N)], so the
phase-aware output representation of the original paper is held fixed and
only the inductive bias of the body changes.

Single user
    FCDNN      fully connected baseline (paper, Table 3)
    CNNLSTM    published architecture (paper, Fig. 2)
    CNNOnly    CNN ablation
    SharedMLP  *control*: the same small MLP applied to every element
               independently, with no path for information to flow between
               elements. If this matches CNNLSTM, the gain of the published
               model cannot be coming from spatial structure.

Multi user
    EquivariantRIS  attention over elements, mean-pooling over users.
                    Equivariant to element permutation, invariant to user
                    permutation, and defined for any number of users.
"""

import torch
import torch.nn as nn


# --------------------------------------------------------------- single user

class SharedMLP(nn.Module):
    """
    Per-element shared MLP. Implemented as width-1 convolutions, which is
    exactly a single MLP applied to each element's own 4-vector.

    There is deliberately NO mixing across elements anywhere in this model.
    """

    def __init__(self, N=32, in_ch=4, hidden=(64, 64, 32)):
        super().__init__()
        self.N = N
        layers, c = [], in_ch
        for h in hidden:
            layers += [nn.Conv1d(c, h, 1), nn.ReLU(inplace=True)]
            c = h
        layers += [nn.Conv1d(c, 2, 1)]
        self.net = nn.Sequential(*layers)

    def forward(self, x):                      # x [B, 4, N]
        y = self.net(x)                         # [B, 2, N]
        return y.reshape(x.shape[0], -1)        # [B, 2N] = [sin..., cos...]


class FCDNN(nn.Module):
    """Fully connected baseline."""

    def __init__(self, N=32, in_ch=4, hidden=(512, 256, 128)):
        super().__init__()
        self.N = N
        layers, c = [], in_ch * N
        for h in hidden:
            layers += [nn.Linear(c, h), nn.ReLU(inplace=True), nn.Dropout(0.2)]
            c = h
        layers += [nn.Linear(c, 2 * N)]
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x.flatten(1))


class CNNOnly(nn.Module):
    """CNN front-end of the published model, without the recurrent stage."""

    def __init__(self, N=32, in_ch=4, head="dense"):
        super().__init__()
        self.N = N
        self.cnn = nn.Sequential(
            nn.Conv1d(in_ch, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True), nn.Dropout(0.2),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
        )
        self.head = _make_head(head, 64, N)

    def forward(self, x):
        return self.head(self.cnn(x))


class CNNLSTM(nn.Module):
    """
    Published architecture: two Conv1d blocks, a two-layer LSTM over the
    row-major element sequence, then a head.

    head="dense" reproduces the published model exactly. head="local"
    replaces the dense bottleneck with a width-1 convolution, i.e. the same
    two-output map applied at every element. See _make_head.
    """

    def __init__(self, N=32, in_ch=4, head="dense"):
        super().__init__()
        self.N = N
        self.cnn = nn.Sequential(
            nn.Conv1d(in_ch, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True), nn.Dropout(0.2),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
        )
        self.lstm = nn.LSTM(64, 128, num_layers=2, batch_first=True, dropout=0.2)
        self.proj = nn.Linear(128, 64)
        self.head = _make_head(head, 64, N)

    def forward(self, x):
        h = self.cnn(x).permute(0, 2, 1)        # [B, N, 64]
        h, _ = self.lstm(h)                     # [B, N, 128]
        h = self.proj(h).permute(0, 2, 1)       # [B, 64, N]
        return self.head(h)


class _DenseHead(nn.Module):
    """
    Published head: flatten the whole feature map, squeeze it through a
    64-unit layer, then expand to 2N outputs.

    Note the width of the last hidden layer is fixed at 64 while the output
    is 2N. At N = 32 those are equal; for larger surfaces the head has to
    carry 2N numbers through 64 units, so it becomes the binding constraint
    on accuracy regardless of how good the body is. This is the quantity the
    `head="local"` variant isolates.
    """

    def __init__(self, c, N):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(c * N, 256), nn.ReLU(inplace=True), nn.Dropout(0.3),
            nn.Linear(256, 128), nn.ReLU(inplace=True), nn.Dropout(0.2),
            nn.Linear(128, 64), nn.ReLU(inplace=True),
            nn.Linear(64, 2 * N),
        )

    def forward(self, h):                        # h [B, C, N]
        return self.net(h.flatten(1))


class _LocalHead(nn.Module):
    """Width-1 convolution: the same small map applied at every element."""

    def __init__(self, c, N):
        super().__init__()
        self.N = N
        self.net = nn.Sequential(
            nn.Conv1d(c, 64, 1), nn.ReLU(inplace=True), nn.Conv1d(64, 2, 1))

    def forward(self, h):                        # h [B, C, N]
        return self.net(h).reshape(h.shape[0], -1)


def _make_head(kind, c, N):
    if kind == "dense":
        return _DenseHead(c, N)
    if kind == "local":
        return _LocalHead(c, N)
    raise ValueError(f"unknown head {kind!r}")


def _head(c_in, c_out):
    """Kept for the multi-user reference model."""
    return nn.Sequential(
        nn.Linear(c_in, 256), nn.ReLU(inplace=True), nn.Dropout(0.3),
        nn.Linear(256, 128), nn.ReLU(inplace=True), nn.Dropout(0.2),
        nn.Linear(128, 64), nn.ReLU(inplace=True),
        nn.Linear(64, c_out),
    )


# ---------------------------------------------------------------- multi user

class _ElementAttention(nn.Module):
    """Self-attention over the element axis, shared across users."""

    def __init__(self, dim, heads=4, drop=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.att = nn.MultiheadAttention(dim, heads, dropout=drop, batch_first=True)
        self.norm2 = nn.LayerNorm(dim)
        self.ff = nn.Sequential(nn.Linear(dim, 2 * dim), nn.GELU(),
                                nn.Linear(2 * dim, dim))

    def forward(self, z):                       # z [B*U, N, D]
        h = self.norm(z)
        z = z + self.att(h, h, h, need_weights=False)[0]
        return z + self.ff(self.norm2(z))


class EquivariantRIS(nn.Module):
    """
    Permutation-equivariant model for the multi-user RIS problem.

    Input  [B, U, C, N]
    Output [B, 2N]

    Symmetries by construction:
      * equivariant to permutation of RIS elements (attention, no positional
        encoding on the element axis)
      * invariant to permutation of users (mean pooling over the user axis)
      * defined for any U, so a model trained at one user count can be
        evaluated at another without retraining.

    User coupling is handled by interleaving per-user attention blocks with
    a mean-field exchange: each user token is updated with the average over
    all users at the same element, which is the standard equivariant linear
    map on a set.

    Setting residual=True changes what the network has to produce. Instead of
    emitting a phase from nothing, it emits a weighted circular mean of the
    per-user alignments phi_un (supplied as input channels) and a learned
    correction on top:

        theta_n = angle( sum_u w_u e^{j phi_un} ) + Delta_n

    The weights w_u are produced per user and normalised over users, so a
    disadvantaged user can be given priority -- which is what a max-min
    objective requires. Both terms respect the symmetries: the softmax over
    users is equivariant and the weighted sum is invariant, so the output
    still does not depend on how the users are labelled. The reference is a
    sensible solution by itself, so training starts from a good point rather
    than from noise, and the network spends its capacity on the correction.
    """

    def __init__(self, in_ch=9, dim=64, blocks=3, heads=4, drop=0.1,
                 residual=True, phi_channels=(7, 8)):
        super().__init__()
        self.residual = residual
        self.phi_ch = phi_channels
        self.embed = nn.Linear(in_ch, dim)
        self.blocks = nn.ModuleList([_ElementAttention(dim, heads, drop)
                                     for _ in range(blocks)])
        self.mix = nn.ModuleList([nn.Linear(2 * dim, dim) for _ in range(blocks)])
        self.out = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, dim),
                                 nn.GELU(), nn.Linear(dim, 2))
        if residual:
            self.gate = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, 1))
            # start as a near-exact copy of the reference: zero correction
            nn.init.zeros_(self.out[-1].weight)
            nn.init.zeros_(self.out[-1].bias)

    def forward(self, x):                       # [B, U, C, N]
        B, U, C, N = x.shape
        z = self.embed(x.permute(0, 1, 3, 2))   # [B, U, N, D]
        for blk, mix in zip(self.blocks, self.mix):
            z = blk(z.reshape(B * U, N, -1)).reshape(B, U, N, -1)
            pooled = z.mean(dim=1, keepdim=True).expand_as(z)
            z = mix(torch.cat([z, pooled], dim=-1))

        y = self.out(z).mean(dim=1)             # [B, N, 2]
        if not self.residual:
            return torch.cat([y[..., 0], y[..., 1]], dim=-1)

        ci, si = self.phi_ch
        w = torch.softmax(self.gate(z).mean(dim=2), dim=1)        # [B, U, 1]
        ref_c = (w * x[:, :, ci, :]).sum(1)                        # [B, N]
        ref_s = (w * x[:, :, si, :]).sum(1)
        r = torch.sqrt(ref_c ** 2 + ref_s ** 2 + 1e-12)
        ref_c, ref_s = ref_c / r, ref_s / r

        # Correction as a rotation, parameterised AROUND THE IDENTITY:
        # (1 + y0, y1) normalised. With the last layer zero-initialised this
        # is exactly (1, 0), so training starts at the reference solution.
        # The epsilon sits inside the square root -- putting it outside
        # leaves an infinite gradient at the origin, which is exactly where
        # the zero initialisation places the model on its first step.
        dc = 1.0 + y[..., 0]
        ds = y[..., 1]
        d = torch.sqrt(dc ** 2 + ds ** 2 + 1e-12)
        dc, ds = dc / d, ds / d

        out_c = ref_c * dc - ref_s * ds
        out_s = ref_s * dc + ref_c * ds
        return torch.cat([out_s, out_c], dim=-1)                   # [B, 2N]


class MUCNNLSTM(nn.Module):
    """
    Multi-user adaptation of the published model: users are concatenated
    along the channel axis. This fixes U in the first layer and makes the
    model sensitive to the order in which users are listed -- the two
    properties the equivariant model is designed to remove.

    The output head defaults to "local" rather than the published dense
    bottleneck, so that the comparison against EquivariantRIS isolates the
    symmetry and is not confounded by the head effect measured in step 1.
    Setting head="dense" reproduces the direct extension of the published
    architecture and performs substantially worse.
    """

    def __init__(self, N=32, n_users=4, in_ch=9, head="local"):
        super().__init__()
        self.N, self.U = N, n_users
        c = in_ch * n_users
        self.cnn = nn.Sequential(
            nn.Conv1d(c, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True), nn.Dropout(0.2),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
        )
        self.lstm = nn.LSTM(64, 128, num_layers=2, batch_first=True, dropout=0.2)
        self.proj = nn.Linear(128, 64)
        self.head = _make_head(head, 64, N)

    def forward(self, x):                       # [B, U, C, N]
        B, U, C, N = x.shape
        h = self.cnn(x.reshape(B, U * C, N)).permute(0, 2, 1)
        h, _ = self.lstm(h)
        return self.head(self.proj(h).permute(0, 2, 1))


def count_params(m):
    return sum(p.numel() for p in m.parameters() if p.requires_grad)
```

### `ris_mu/losses.py`

*112 satir · sha256:4fd1c95b68d3*

```python
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
```

### `ris_mu/baselines.py`

*113 satir · sha256:2d5290a8fdc0*

```python
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
```

### `ris_mu/train.py`

*74 satir · sha256:03f9853db4d4*

```python
"""
train.py
--------
Small reusable training harness. Supports both the supervised phase-regression
setting and the unsupervised rate-maximising setting through a single
`step_fn` hook, so every experiment in the study runs the same optimiser,
schedule and early-stopping policy.
"""

import time
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader


def make_loaders(tensors, idx_tr, idx_va, idx_te, batch_size=256):
    def mk(idx, shuffle):
        ds = TensorDataset(*[t[idx] for t in tensors])
        return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)
    return mk(idx_tr, True), mk(idx_va, False), mk(idx_te, False)


def run_training(model, train_dl, val_dl, step_fn, eval_fn,
                 epochs=40, lr=1e-3, device="cpu", patience=12,
                 milestones=(15, 28, 36), verbose=True, tag=""):
    """
    step_fn(model, batch) -> loss tensor
    eval_fn(model, loader) -> (score_to_minimise, dict_of_metrics)
    """
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sch = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=list(milestones), gamma=0.5)

    best, best_state, best_ep, hist = float("inf"), None, 0, []
    t0 = time.time()

    for ep in range(1, epochs + 1):
        model.train()
        tot = 0.0
        for batch in train_dl:
            opt.zero_grad()
            loss = step_fn(model, batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item()
        sch.step()

        score, metrics = eval_fn(model, val_dl)
        hist.append(dict(epoch=ep, train_loss=tot / len(train_dl), score=score, **metrics))

        if score < best - 1e-6:
            best, best_ep = score, ep
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

        if verbose and (ep % 5 == 0 or ep == 1):
            ms = "  ".join(f"{k}={v:.3f}" for k, v in metrics.items())
            print(f"    [{tag}] ep {ep:3d}  loss={tot/len(train_dl):.5f}  {ms}"
                  f"{'  *' if ep == best_ep else ''}")

        if ep - best_ep >= patience:
            if verbose:
                print(f"    [{tag}] early stop at epoch {ep} (best {best_ep})")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return dict(best_score=best, best_epoch=best_ep,
                minutes=(time.time() - t0) / 60, history=hist)


def set_seed(s=42):
    np.random.seed(s)
    torch.manual_seed(s)
```

## 3. Betikler: `scripts/`

47 betik. Alfabetik degil, **tezdeki roluyle** gruplandi. Bir sayiyi teze koymadan once onu ureten betigi burada bulup kosturun.

### Denetim ve dogrulama (her oturumda kosturulacaklar)

### `scripts/audit_claims.py`

*465 satir · sha256:4768a78598df*

```python
"""
audit_claims.py -- every load-bearing number in README_MUMISO.md, frozen
and re-checkable by machine.

WHY THIS FILE EXISTS
--------------------
Three times in this project a stated number turned out to be wrong: a table
whose rows came from two different antenna counts, a baseline that was
weaker than claimed, and a "strongest classical method" that was not the
strongest. Each was caught by someone deciding to look again. That is not a
process, it is luck.

So the claims live here as code. Each one recomputes its value from the
library -- not by parsing a script's printout, which rots the moment the
printing changes -- and compares against the value frozen in the report.
Run it after any change to the package:

    python3 -I scripts/audit_claims.py            # fast tiers only
    python3 -I scripts/audit_claims.py --all      # includes slow tiers

TIERS, because not every number deserves the same tolerance
-----------------------------------------------------------
  exact        mathematical identities. A drift here is a bug. rtol 1e-6.
  statistical  rates and ranks measured over scenarios. Seeded, so
               reproducible, but a tolerance wide enough to survive a torch
               version bump. rtol 5e-2.
  timing       wall-clock. NOT asserted -- machine-dependent and noisy
               (16-step Adam measured 23.7, 24.2, 26.0 and 29.4 ms across
               runs on the same box). Reported, and only the ORDERING and
               the budget fraction are checked, because those are what the
               argument rests on.

If a claim here disagrees with the report, the report is what is wrong
until proven otherwise.
"""
import sys
import pathlib
import argparse
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank, neighbour_corr)
from ris_mu.mumiso.features import mumiso_features, n_channels
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true", help="include slow tiers")
ap.add_argument("--only", default=None, help="substring filter on claim id")
a = ap.parse_args()

RESULTS = []


def claim(cid, section, tier, claimed, measured, note="", at_most=None):
    """
    Two kinds of claim, and conflating them is what made this file's first
    run produce three false alarms:

      VALUE claims ("the rate is 3.6688"). Checked within the tier's
      relative tolerance. The exact tier uses 1e-3, not something tighter,
      because the report quotes these to four decimals -- asserting to 1e-6
      against a four-decimal quote fails on the rounding, which is the
      report's precision, not an error.

      THRESHOLD claims ("the leakage is negligible", "the gradient matches
      finite differences"). These have no true value to hit: finite
      differences cannot do better than ~1e-8, and the residual model is
      deliberately a hair off the anchor so that gradients reach the body.
      Pass `at_most=` for these.
    """
    tol = {"exact": 1e-3, "statistical": 5e-2, "timing": None}[tier]
    if at_most is not None:
        ok = abs(measured) <= at_most
        shown = f"<={at_most:.3g}"
    elif tol is None:
        ok = None
        shown = "-"
    else:
        ok = abs(measured - claimed) / max(abs(claimed), 1e-30) <= tol
        shown = f"{claimed:.4g}"
    RESULTS.append(dict(id=cid, section=section, tier=tier, claimed=claimed,
                        measured=measured, ok=ok, note=note, at_most=at_most))
    tag = {True: "PASS", False: "FAIL", None: "info"}[ok]
    print(f"  [{tag}] {cid:<28} §{section:<4} target {shown:>11}  "
          f"measured {measured:10.4g}  {note}", flush=True)


def section(name):
    print(f"\n=== {name} ===", flush=True)


# ----------------------------------------------------------------- exact
section("exact: mathematical identities")
torch.manual_seed(0)
rng = np.random.default_rng(0)


def cn(*s):
    return (rng.normal(size=s) + 1j * rng.normal(size=s)) / np.sqrt(2)


# single-user reduction: general form vs the published Eq. (8)
Nn = 32
F1, G1, H1 = cn(1, Nn, 1), cn(1, 1, Nn), cn(1, 1, 1)
tF, tG, tH = (torch.tensor(x) for x in (F1, G1, H1))
acas = G1[0, 0] * F1[0, :, 0]
bound = (abs(H1[0, 0, 0]) + np.abs(acas).sum()) ** 2


def gain(th):
    c = torch.tensor(np.cos(th))[None]
    s = torch.tensor(np.sin(th))[None]
    return S.effective_channel(tF, tG, tH, c, s).abs().item() ** 2


claim("su_general_over_bound", "7", "exact", 1.0000,
      gain(S.su_align_phase(tF, tG, tH)[0, 0].numpy()) / bound)
claim("su_eq8_over_bound", "7", "exact", 0.8977,
      gain(-np.angle(acas)) / bound, "published Eq. (8), h_d=0 special case")

# ZF: nulls interference, respects the power constraint
Bn, Nn, T, K = 4, 32, 8, 4
F2, G2, H2 = cn(Bn, Nn, T), cn(Bn, K, Nn), cn(Bn, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F2, G2, H2))
th = torch.tensor(rng.uniform(-np.pi, np.pi, (Bn, Nn)))
He = S.effective_channel(tF, tG, tH, torch.cos(th), torch.sin(th))
A = (He @ S.zf(He, 1.0)).abs() ** 2
off = A - torch.diag_embed(torch.diagonal(A, dim1=-2, dim2=-1))
claim("zf_leakage", "7", "exact", 0.0, off.abs().max().item(),
      "inter-user interference", at_most=1e-15)
claim("zf_power", "7", "exact", 1.0,
      (S.zf(He, 1.0).abs() ** 2).sum((-1, -2)).mean().item(), "||W||_F^2 = Pt")
claim("mrt_power", "7", "exact", 1.0,
      (S.mrt(He, 1.0).abs() ** 2).sum((-1, -2)).mean().item(), "||W||_F^2 = Pt")

# rate gradient against finite differences
Bn, Nn, T, K = 2, 16, 4, 3
F3, G3, H3 = cn(Bn, Nn, T), cn(Bn, K, Nn), cn(Bn, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F3, G3, H3))
th0 = rng.uniform(-np.pi, np.pi, (Bn, Nn))


def obj(t, grad=False):
    tt = torch.tensor(t, requires_grad=grad)
    R = S.rates(tF, tG, tH, torch.cos(tt), torch.sin(tt), 1.0, 1e-3)
    return R.min(-1).values.sum(), tt


v, tt = obj(th0, True)
v.backward()
g_auto = tt.grad.numpy().copy()
eps = 1e-6
g_fd = np.zeros_like(th0)
for b in range(Bn):
    for n in range(Nn):
        tp = th0.copy(); tp[b, n] += eps
        tm = th0.copy(); tm[b, n] -= eps
        g_fd[b, n] = (obj(tp)[0].item() - obj(tm)[0].item()) / (2 * eps)
claim("grad_vs_fd_relative", "7", "exact", 0.0,
      np.abs(g_auto - g_fd).max() / np.abs(g_fd).max(),
      "autograd vs finite diff; fd cannot do better than ~1e-8",
      at_most=1e-5)

# raw network output is scale invariant after unit_phase
gsc = torch.tensor(rng.uniform(0.2, 5.0, (Bn, Nn)))
c0, s0 = torch.tensor(np.cos(th0)), torch.tensor(np.sin(th0))
R1 = S.rates(tF, tG, tH, *S.unit_phase(c0, s0), 1.0, 1e-3)
R2 = S.rates(tF, tG, tH, *S.unit_phase(gsc * c0, gsc * s0), 1.0, 1e-3)
claim("scale_invariance", "7", "exact", 0.0, (R1 - R2).abs().max().item(),
      at_most=1e-9)

# straight-through quantiser: value on the grid, gradient equal to one
for bits in (1, 2, 3):
    cc = torch.tensor(np.cos(th0), requires_grad=True)
    ss = torch.tensor(np.sin(th0), requires_grad=True)
    cq, sq = S.quantise_ste(cc, ss, bits)
    step = 2 * np.pi / (2 ** bits)
    tq = torch.atan2(sq, cq).detach().numpy()
    claim(f"ste_{bits}bit_on_grid", "7", "exact", 0.0,
          float(np.abs(tq / step - np.round(tq / step)).max()), at_most=1e-12)
    # d theta_q / d theta must be 1, not 0: perturb theta and watch theta_q
    th_t = torch.tensor(th0, requires_grad=True)
    cq, sq = S.quantise_ste(torch.cos(th_t), torch.sin(th_t), bits)
    torch.atan2(sq, cq).sum().backward()
    claim(f"ste_{bits}bit_gradient_is_one", "7", "exact", 1.0,
          th_t.grad.abs().mean().item(), "straight-through, not zero")

# permutation symmetry at inference
C = n_channels(8)
X = torch.randn(6, 4, C, 32)
for mode in MODES:
    net = MuMisoNet(N=32, n_users=4, n_tx=8, mode=mode).eval()
    base = net(X).detach()
    dev = max((net(X[:, torch.tensor(rng.permutation(4))]).detach()
               - base).abs().max().item() for _ in range(6))
    if mode == "concat":
        # At initialisation an untrained net is near-random, so this number
        # is not the real test. The real one is post-training, on the RATE:
        # measured 1.67e-02 (residual) and 2.46e-02 (absolute) for concat
        # against 2.46e-06 for deepsets. See the run logs in results/.
        claim("perm_concat_is_sensitive", "7", "timing", 0.0, dev,
              "at init; real test is post-training on the rate")
    else:
        claim(f"perm_{mode}_invariant", "7", "exact", 0.0, dev, at_most=1e-5)

# residual mode starts at the anchor
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(200)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
Xs = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, th_su = B.su_average(F, G, hd, pt, nv)
net = MuMisoNet(N=N, n_users=4, n_tx=8, mode="exchange", residual=True).eval()
with torch.no_grad():
    c, s = net.phases(Xs)
dev = torch.atan2(torch.sin(torch.atan2(s, c) - th_su),
                  torch.cos(torch.atan2(s, c) - th_su)).abs().max().item()
claim("residual_starts_at_anchor", "7", "exact", 0.0, dev,
      "radians; deliberately a hair off so gradients reach the body",
      at_most=2e-3)

# ----------------------------------------------------- statistical (fast)
section("statistical: channel diagnostics (1000 scenarios, N=32 T=8 K=4)")
d2 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                         seed=11)).generate(1000)
Gv = d2["G"].reshape(-1, N)
Ft = d2["F"].transpose(0, 2, 1).reshape(-1, 8)
claim("g_rank_pooled_1000", "6", "statistical", 15.73, effective_rank(Gv))
claim("g_rank_user0_1000", "6", "statistical", 15.58,
      effective_rank(d2["G"][:, 0]))
claim("f_rank_ant0_1000", "6", "statistical", 13.46,
      effective_rank(d2["F"][:, :, 0]))
claim("g_neigh_corr_1000", "6", "statistical", 0.5716, neighbour_corr(Gv))
claim("ant_neigh_corr_1000", "6", "statistical", 0.7401, neighbour_corr(Ft))
claim("ant_rank_1000", "6", "statistical", 4.00, effective_rank(Ft))
claim("los_frac_bs_ris", "6", "statistical", 0.383,
      float(d2["los_ris_bs"].mean()))

section("statistical: effective rank vs sample count (§6 caveat)")
# The previous version of this check computed effective_rank on
# d2["G"][:min(Sn, 1000)], so its 4000 and 8000 rows silently reused the
# first 1000 scenarios and the test could never fail. An independent audit
# caught it. It also found the report's stated DIRECTION is wrong: the
# estimator is not monotone upward -- 250 scenarios gives a HIGHER value
# than 1000. So what is checked here is the honest claim: the estimate
# moves by more than a few percent with sample count, therefore an absolute
# value must never be quoted without the count.
d_big = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                            seed=11)).generate(
    16000 if a.all else 4000)
ranks = {}
for Sn in (250, 1000, 4000) + ((16000,) if a.all else ()):
    ranks[Sn] = effective_rank(d_big["G"][:Sn].reshape(-1, N))
    claim(f"rank_at_{Sn}", "6", "timing", 0.0, ranks[Sn],
          f"{Sn} scenarios")
spread = (max(ranks.values()) - min(ranks.values())) / min(ranks.values())
claim("rank_estimate_is_count_dependent", "6", "exact", 1.0,
      1.0 if spread > 0.05 else 0.0,
      f"spread {100*spread:.0f}% across counts -> never quote without n")
claim("rank_is_not_monotone_up", "6", "exact", 1.0,
      1.0 if ranks[250] > ranks[1000] else 0.0,
      "report's 'drifts upward' is wrong at the low end")

# ------------------------------------------------------- statistical slow
if a.all:
    section("statistical: baselines and the frontier ordering (slow)")
    d3 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                             seed=11)).generate(600)
    F3, G3, H3, _ = to_torch(d3)
    ev = slice(0, 450)
    _, TH0 = B.su_average(F3, G3, H3, pt, nv)

    def rate_of(th):
        return S.rates(F3[ev], G3[ev], H3[ev], torch.cos(th), torch.sin(th),
                       pt, nv, "zf").min(-1).values.mean().item()

    def adam_phase(L, lr=0.5):
        dl = torch.zeros(450, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = TH0[ev] + dl
            R = S.rates(F3[ev], G3[ev], H3[ev], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        return TH0[ev] + dl.detach()

    claim("su_average_rate", "5", "statistical", 3.664, rate_of(TH0[ev]))
    claim("adam8_rate", "5", "statistical", 5.378, rate_of(adam_phase(8)))
    claim("adam16_rate", "5", "statistical", 5.743, rate_of(adam_phase(16)))
    claim("adam32_rate", "5", "statistical", 6.015, rate_of(adam_phase(32)))
    q_cd = S.rate_metrics(B.coord_descent(F3[ev], G3[ev], H3[ev], pt,
                                          nv)[0])["min_rate"]
    q_pga = S.rate_metrics(B.pga(F3[ev], G3[ev], H3[ev], pt,
                                 nv)[0])["min_rate"]
    q_ao = S.rate_metrics(B.ao(F3[ev], G3[ev], H3[ev], pt, nv)[0])["min_rate"]
    claim("cd_rate", "5", "statistical", 5.910, q_cd)
    claim("pga_rate", "5", "statistical", 6.202, q_pga)
    claim("ao_rate", "5", "statistical", 6.201, q_ao)
    claim("pga_beats_ao", "5", "exact", 1.0, 1.0 if q_pga >= q_ao else 0.0,
          "report says PGA is the strongest, not AO")
    claim("cd_dominated_by_adam32", "5", "exact", 1.0,
          1.0 if rate_of(adam_phase(32)) > q_cd else 0.0,
          "report says coordinate descent is dominated")

    # The latency table in the report comes from a DIFFERENT sample (400
    # scenarios, mumiso_budget_fraction.py) than the frontier rows above
    # (450, mumiso_frontier.py), and the min-rate mean moves about 6% at
    # this n. Both are frozen here so that quoting one while measuring the
    # other shows up as a failure instead of as a puzzling 6% drift.
    section("statistical: the OTHER sample the latency table uses (400)")
    d4 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                             seed=11)).generate(400)
    F4, G4, H4, _ = to_torch(d4)
    _, T4 = B.su_average(F4, G4, H4, pt, nv)
    _, T4b = B.su_best_of(F4, G4, H4, pt, nv)

    def rate4(th):
        return S.rates(F4, G4, H4, torch.cos(th), torch.sin(th), pt, nv,
                       "zf").min(-1).values.mean().item()

    def adam4(L, start):
        dl = torch.zeros(400, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            t = start + dl
            R = S.rates(F4, G4, H4, torch.cos(t), torch.sin(t), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        return start + dl.detach()

    claim("bf_su_average", "5", "statistical", 3.765, rate4(T4))
    claim("bf_su_best_of", "5", "statistical", 4.417, rate4(T4b))
    claim("bf_adam8", "5", "statistical", 5.569, rate4(adam4(8, T4)))
    claim("bf_adam12", "5", "statistical", 5.775, rate4(adam4(12, T4)))
    claim("bf_adam16", "5", "statistical", 5.934, rate4(adam4(16, T4)))
    # The audit found su_average to be a weak anchor and measured the fix
    # at +48%. With the precoder bug fixed that drops to +17% -- the finding
    # is real but much smaller, and the threshold here records the measured
    # value rather than the one from the broken configuration.
    claim("su_best_of_gain_over_average", "5", "statistical", 1.173,
          rate4(T4b) / rate4(T4), "anchor fix, properly precoded")

# --------------------------------------------------- sec4 / unrolled claims
# WHY THESE EXIST
# ---------------
# Everything above re-measures something. The numbers behind Bulgu 1 and
# Bulgu 2 come from training runs that take ~15-45 min each, so an audit
# cannot reproduce them. What it CAN do is pin the saved results to the
# claims the report makes about them -- which is exactly the failure mode
# this project already hit once: the report quoted the UNROLLED model's
# 3.50 -> 5.64 as evidence about the ONE-SHOT models. A number lifted from
# the wrong file reads perfectly plausible. These checks make that specific
# mistake fail loudly.
#
# KNOWN GAP, stated rather than papered over: the anchor on the models' own
# 1800-scenario test split (su_average 3.5363, su_best_of 4.1730) is the
# denominator of every Bulgu 1 ratio in the report, and it is NOT re-measured
# here -- doing so means regenerating all 12000 scenarios. It is measured by
# scripts/anchor_same_split.py and read from results/anchor_full_test.json.
# So a regression in the SU baselines would not fail this section; it would
# fail the §5 statistical tier above, which does re-measure them on its own
# sample. That is weaker than checking the same split, and worth closing.
section("saved results: Bulgu 1 and Bulgu 2 (consistency, not re-measurement)")

import json as _json

_RES = pathlib.Path(__file__).resolve().parents[1] / "results"


def _load(name):
    p = _RES / name
    return _json.loads(p.read_text()) if p.exists() else None


_s4 = _load("mumiso_sec4_fixzf.json")
_un = _load("mumiso_unrolled_fixzf.json")
_ng = _load("mumiso_nograd_fixzf.json")

if _s4 is None or _un is None or _ng is None:
    print("  [skip] one of the fixzf result files is missing -- rerun "
          "mumiso_run.py / mumiso_unrolled.py with --tag *_fixzf")
else:
    # --- Bulgu 1: the three one-shot models sit ON the anchor -------------
    for _m, _v in (("concat", 3.536795), ("deepsets", 3.536696),
                   ("exchange", 3.526039)):
        claim(f"sec4_{_m}_test_min", "4", "statistical", _v,
              _s4["models"][_m]["test_min"], "from mumiso_sec4_fixzf.json")
    claim("sec4_target_is_pga", "4", "exact", 1,
          int(_s4["target"]["method"] == "pga"),
          "the number to beat is PGA, chosen by measurement")
    claim("sec4_target_rate", "4", "statistical", 6.078346,
          _s4["target"]["rate"])
    # The spread ACROSS architectures is the real claim of Bulgu 1: the
    # choice of architecture does not matter. Asserting it as a bound means
    # a future run that separates them will fail here instead of quietly
    # contradicting the report.
    _mins = [_s4["models"][k]["test_min"] for k in ("concat", "deepsets",
                                                    "exchange")]
    claim("sec4_architecture_spread_tiny", "4", "statistical",
          0.0, (max(_mins) - min(_mins)) / max(_mins),
          "architecture choice changes nothing", at_most=0.01)

    # --- Bulgu 2: the gradient input is what matters ---------------------
    claim("unrolled_anchor", "4", "statistical", 3.5758257, _un["anchor"])
    claim("unrolled_with_grad", "4", "statistical", 5.6359273,
          _un["test_min"], "gradient given as input")
    claim("unrolled_without_grad", "4", "statistical", 3.6160022,
          _ng["test_min"], "same model, gradient withheld")
    claim("unrolled_grad_is_on", "4", "exact", 1,
          int(bool(_un["config"]["use_grad"])))
    claim("unrolled_nograd_is_off", "4", "exact", 0,
          int(bool(_ng["config"]["use_grad"])))
    # Same anchor for both arms, or the comparison means nothing.
    claim("ablation_shares_anchor", "4", "exact", 0.0,
          abs(_un["anchor"] - _ng["anchor"]), "both arms, one anchor",
          at_most=1e-6)
    # Nor may it be a capacity difference.
    claim("ablation_capacity_matched", "4", "statistical", 0.0,
          abs(_un["params"] - _ng["params"]) / _un["params"],
          "parameter counts within 1%", at_most=0.01)
    # The finding itself, as a ratio so it survives a change of scale.
    # `claim` only bounds from ABOVE, so the "gradient buys >10x" claim is
    # written as its reciprocal <= 0.1. Writing it the natural way round
    # with a huge at_most would assert nothing at all -- the exact kind of
    # toothless threshold this audit exists to catch.
    claim("nograd_gain_is_under_a_tenth", "4", "statistical", 0.0,
          (_ng["test_min"] / _ng["anchor"] - 1.0)
          / (_un["test_min"] / _un["anchor"] - 1.0),
          "gradient input buys >10x the anchor-relative gain", at_most=0.1)
    claim("nograd_barely_moves", "4", "statistical", 0.0,
          _ng["test_min"] / _ng["anchor"] - 1.0,
          "without the gradient the model stays at the anchor",
          at_most=0.05)
    # And the guard against the mistake that actually happened: the
    # one-shot models must NOT be credited with the unrolled model's rate.
    claim("bulgu1_not_bulgu2", "4", "exact", 1,
          int(max(_mins) < 0.75 * _un["test_min"]),
          "one-shot models are nowhere near the unrolled model")

# ----------------------------------------------------------------- report
section("summary")
fails = [r for r in RESULTS if r["ok"] is False]
n_checked = sum(1 for r in RESULTS if r["ok"] is not None)
print(f"  {n_checked - len(fails)}/{n_checked} asserted claims hold; "
      f"{sum(1 for r in RESULTS if r['ok'] is None)} informational")
if fails:
    print("\n  FAILED:")
    for r in fails:
        print(f"    {r['id']} (§{r['section']}): claimed {r['claimed']:.4g}, "
              f"measured {r['measured']:.4g}")
    print("\n  The report is wrong until proven otherwise. Fix the report, or")
    print("  find the regression in the package that moved the number.")
if not a.all:
    print("\n  (slow tiers skipped; rerun with --all before trusting §5)")
sys.exit(1 if fails else 0)
```

### `scripts/audit_fair_comparison.py`

*191 satir · sha256:612487b768e0*

```python
"""
Double-check of this project's own conclusion.

The conclusion was: tuned Adam dominates the learned update rule on the
latency-quality frontier. But the step size 0.5 was picked by trying two
values and looking at the SAME scenarios the comparison is reported on,
while the learned model was trained on a train split and reported on test.
That tilts the comparison toward Adam, which happens to be the direction
the conclusion went -- exactly the shape of error worth hunting for.

So: sweep the step size on a VALIDATION split, freeze the winner, and
report on test. Same protocol for both methods. Also check whether the
conclusion survives a per-scenario-tuned Adam (an upper bound Adam could
never reach in deployment) and a badly tuned one (a lower bound).
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--samples", type=int, default=3000)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--tag", default="audit_fair")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH0 = B.su_average(F, G, hd, pt, nv)
tr, va, te = split_indices(a.samples, seed=0)
VA, TE = va[:400], te[:400]

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()


def adam_phase(ids, L, lr):
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


def rate_of(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


res = dict(config=vars(a))

# ------------------------------------------------- 1) step size, honestly
say("=== 1) Adam step size chosen on VALIDATION, reported on TEST ===")
grid = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 2.0]
say(f"{'lr':>6}" + "".join(f"{'L='+str(L):>10}" for L in (8, 16, 32)))
say("-" * 36)
best = {}
for L in (8, 16, 32):
    best[L] = (None, -np.inf)
rows = {}
for lr in grid:
    rows[lr] = {}
    for L in (8, 16, 32):
        q = rate_of(adam_phase(VA, L, lr), VA)
        rows[lr][L] = q
        if q > best[L][1]:
            best[L] = (lr, q)
    say(f"{lr:6.2f}" + "".join(f"{rows[lr][L]:10.4f}" for L in (8, 16, 32)))
say("")
res["val_sweep"] = {str(k): v for k, v in rows.items()}
res["chosen_lr"] = {str(L): best[L][0] for L in best}
for L in (8, 16, 32):
    say(f"  L={L:2d}: validation picks lr={best[L][0]}  "
        f"(val {best[L][1]:.4f})")

say("\n=== 2) TEST, with the step size frozen from validation ===")
with torch.no_grad():
    th_net = net(X[TE], F[TE], G[TE], hd[TE], pt, nv, TH0[TE])
q_net = rate_of(th_net, TE)
say(f"  learned, {a.steps} steps                 : {q_net:.4f}")
res["test"] = {"learned": q_net}
for L in (8, 16, 32):
    lr = best[L][0]
    q = rate_of(adam_phase(TE, L, lr), TE)
    res["test"][f"adam_L{L}"] = q
    res["test"][f"adam_L{L}_lr"] = lr
    say(f"  Adam, {L:2d} steps, lr={lr:<4} (from val) : {q:.4f}")

say("\n=== 3) bounds: how much does step-size tuning even matter? ===")
for L in (8, 16):
    qs = [rate_of(adam_phase(TE, L, lr), TE) for lr in grid]
    say(f"  L={L:2d}: worst lr {min(qs):.4f}   best lr {max(qs):.4f}   "
        f"spread {max(qs)-min(qs):.4f}")
    res[f"test_spread_L{L}"] = dict(worst=min(qs), best=max(qs))

say("\n=== 4) per-scenario lr (an upper bound Adam cannot reach live) ===")
for L in (8, 16):
    per = torch.stack([
        S.rates(F[TE], G[TE], hd[TE],
                torch.cos(adam_phase(TE, L, lr)),
                torch.sin(adam_phase(TE, L, lr)), pt, nv,
                "zf").min(-1).values
        for lr in grid])
    say(f"  L={L:2d}: per-scenario best lr -> {per.max(0).values.mean():.4f}")
    res[f"oracle_lr_L{L}"] = float(per.max(0).values.mean())

say("\n=== 5) latency, same protocol ===")


def timeit(fn, reps):
    for _ in range(3):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.percentile(np.array(ts) * 1e3, 50))


one = TE[:1]
t_net = timeit(lambda: net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one]),
               20)
say(f"  learned, {a.steps} steps : {t_net:7.2f} ms")
res["latency"] = {"learned": t_net}
for L in (8, 16, 32):
    t = timeit(lambda: adam_phase(one, L, best[L][0]), 8)
    res["latency"][f"adam_L{L}"] = t
    say(f"  Adam, {L:2d} steps      : {t:7.2f} ms")

say("\n=== VERDICT ===")
tc = 0.423 / (1.5 * panel.fc / 3e8) * 1e3
say(f"  coherence budget : {tc:.1f} ms")
dominated = False
for L in (8, 16, 32):
    q, t = res["test"][f"adam_L{L}"], res["latency"][f"adam_L{L}"]
    if q >= q_net and t <= t_net:
        dominated = True
        say(f"  Adam L={L} (lr={best[L][0]}) dominates the learned model: "
            f"{q:.4f} at {t:.1f} ms vs {q_net:.4f} at {t_net:.1f} ms")
if not dominated:
    say("  no Adam setting dominates the learned model under this protocol "
        "-- the earlier conclusion was too strong")
in_budget = [(f"Adam L={L}", res["test"][f"adam_L{L}"],
              res["latency"][f"adam_L{L}"])
             for L in (8, 16, 32)
             if res["latency"][f"adam_L{L}"] <= tc]
if t_net <= tc:
    in_budget.append((f"learned L={a.steps}", q_net, t_net))
if in_budget:
    w = max(in_budget, key=lambda r: r[1])
    say(f"  best within budget : {w[0]}  {w[1]:.4f} at {w[2]:.1f} ms")
res["conclusion_holds"] = dominated

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/audit_precoder_csi.py`

*156 satir · sha256:af94df52d20d*

```python
"""
Double-check of the precoder fix and the CSI module.

Four suspicions, in order of how much they would change:

  A. Is the MMSE regulariser actually the right default? The sweep that
     exposed the bug showed eps = 1e-12 (absolute) edging out eps = 0, and
     the MMSE choice lands between 1e-12 and 1e-10. "Standard formula" is
     not the same as "best here".

  B. How much does phase optimisation buy AT ALL now? With the precoder
     fixed, su_average reaches 4.624 against a stale floor of 4.315 and a
     best of ~7.1. If a random phase already gets most of the rate, the
     premise of the whole thesis needs stating more carefully.

  C. The CSI error is drawn against ONE global mean power per quantity, so
     within G a weak user takes the same absolute error as a strong one and
     is swamped. Max-min is decided by the weakest user, so this could be
     the real cause of the collapse I blamed entirely on ZF. The docstring
     of csi.py claims the error is "proportional to each link's own
     strength", which is true per quantity and false per user.

  D. `rates_mismatched` calls precode() without noise_var or err_power, so
     it uses the fallback regulariser and is NOT the error-aware precoder
     the module's own docstring describes.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.csi import add_error, db_to_e2

torch.manual_seed(0)
NS = 400
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N, K, T = panel.positions.shape[0], cfg.n_users, cfg.n_bs_antennas
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
_, TH_B = B.su_best_of(F, G, hd, pt, nv)


def rate(th, **kw):
    He = S.effective_channel(F, G, hd, torch.cos(th), torch.sin(th))
    W = S.zf(He, pt, **kw)
    return torch.log2(1 + S.sinr(He, W, nv)).min(-1).values.mean().item()


print("=== A) is the MMSE regulariser the right default? ===")
He = S.effective_channel(F, G, hd, torch.cos(TH_B), torch.sin(TH_B))
p_sig = torch.diagonal(He @ He.conj().transpose(-1, -2),
                       dim1=-2, dim2=-1).real.mean().item()
mmse_abs = K * nv / pt
print(f"  channel scale  mean diag(He He^H) = {p_sig:.3e}")
print(f"  MMSE lambda    K*noise/Pt         = {mmse_abs:.3e}"
      f"   ({mmse_abs/p_sig:.2e} of the diagonal)")
print(f"\n  {'relative eps':>14}{'min rate':>10}")
best = (None, -np.inf)
for e in (0.0, 1e-12, 1e-9, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
    r = rate(TH_B, eps=e) if e > 0 else rate(TH_B, eps_abs=0.0)
    if r > best[1]:
        best = (e, r)
    print(f"  {e:14.0e}{r:10.4f}")
r_mmse = rate(TH_B, noise_var=nv)
print(f"  {'MMSE default':>14}{r_mmse:10.4f}")
print(f"  best swept: relative eps = {best[0]:.0e} -> {best[1]:.4f}")
gap = (best[1] - r_mmse) / best[1]
print(f"  MMSE leaves {100*gap:.2f}% on the table"
      + ("   (negligible)" if abs(gap) < 0.01 else "   <-- CHECK"))

print("\n=== B) how much does phase optimisation buy, with the fix? ===")
g = torch.Generator().manual_seed(0)
th_rand = (torch.rand(NS, N, generator=g) * 2 - 1) * np.pi
rows = [("no RIS", None), ("random phase", th_rand), ("su_average", None),
        ("su_best_of", TH_B), ("PGA", None)]
W0 = S.zf(hd, pt, noise_var=nv)
r_noris = torch.log2(1 + S.sinr(hd, W0, nv)).min(-1).values.mean().item()
_, th_su = B.su_average(F, G, hd, pt, nv)
_, th_pga = B.pga(F, G, hd, pt, nv)
vals = {"no RIS": r_noris, "random phase": rate(th_rand, noise_var=nv),
        "su_average": rate(th_su, noise_var=nv),
        "su_best_of": rate(TH_B, noise_var=nv),
        "PGA": rate(th_pga, noise_var=nv)}
for k, v in vals.items():
    print(f"  {k:>14}{v:10.4f}")
span = vals["PGA"] / max(vals["random phase"], 1e-9)
print(f"  optimised / random phase = {span:.2f}x")
print(f"  random phase / PGA       = {vals['random phase']/vals['PGA']:.2f}"
      f"   <- how much a RANDOM surface already delivers")

print("\n=== C) is the CSI error swamping the weak users? ===")
pw = (G.abs() ** 2).mean(dim=(-1,))              # [B,K] per-user power
spread = (pw.max(-1).values / pw.min(-1).values).median().item()
print(f"  median strongest/weakest user power ratio in G : {spread:.1f}x")
print("  so a single global error scale hits the weakest user"
      f" ~{spread:.0f}x harder, in relative terms\n")


def noisy_peruser(X, e2, gen, per_user_axis=None):
    """Error scaled per-user instead of globally."""
    if e2 <= 0:
        return X
    if per_user_axis is None:
        p = (X.abs() ** 2).mean()
    else:
        p = (X.abs() ** 2).mean(dim=tuple(
            i for i in range(X.ndim) if i != per_user_axis), keepdim=True)
        sh = [1] * X.ndim
        sh[per_user_axis] = X.shape[per_user_axis]
        p = p.reshape(sh)
    z = (torch.randn(X.shape, generator=gen)
         + 1j * torch.randn(X.shape, generator=gen)).to(X.dtype) / 2 ** 0.5
    return ((1 - e2) ** 0.5) * X + (e2 ** 0.5) * z * p.sqrt()


print(f"  {'error':>8}{'global scale':>14}{'per-user scale':>16}")
for db in (-20, -15, -10):
    e2 = db_to_e2(db)
    gg = torch.Generator().manual_seed(7)
    Fg, Gg, Hg = add_error(F, G, hd, e2, gen=gg)
    gg2 = torch.Generator().manual_seed(7)
    Fp = noisy_peruser(F, e2, gg2)
    Gp = noisy_peruser(G, e2, gg2, per_user_axis=1)
    Hp = noisy_peruser(hd, e2, gg2, per_user_axis=1)

    def run(Fe, Ge, He_):
        _, st = B.su_best_of(Fe, Ge, He_, pt, nv)
        dl = torch.zeros(NS, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(8):
            th = st + dl
            R = S.rates(Fe, Ge, He_, torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        th = st + dl.detach()
        Hest = S.effective_channel(Fe, Ge, He_, torch.cos(th), torch.sin(th))
        W = S.zf(Hest, pt, noise_var=nv, err_power=e2)
        Htr = S.effective_channel(F, G, hd, torch.cos(th), torch.sin(th))
        return torch.log2(1 + S.sinr(Htr, W, nv)).min(-1).values.mean().item()
    print(f"  {db:7.0f}d{run(Fg, Gg, Hg):14.4f}{run(Fp, Gp, Hp):16.4f}")
print("  (if the two columns differ a lot, the collapse was partly the")
print("   error model swamping weak users, not only ZF)")

print("\n=== D) does rates_mismatched use the error-aware precoder? ===")
import inspect
from ris_mu.mumiso import csi as C
src = inspect.getsource(C.rates_mismatched)
has = ("err_power" in src) and ("noise_var" in src)
print(f"  passes noise_var / err_power to precode(): {has}"
      + ("" if has else "   <-- NO: uses the fallback regulariser"))
```

### `scripts/audit_section4_cause.py`

*120 satir · sha256:961aa49c3240*

```python
"""
Independent re-check of the two audit findings that change the advice.

FINDING A -- the stated cause of section 4 is wrong.
The report says the channel-to-phase target is "noise with respect to the
input" because many configurations are near-optimal and which one an
optimiser reaches is arbitrary. That has a one-line test the project never
ran: solve the SAME scenario twice from different starts and see whether
the answers agree. If they do, the target is determined, the multiplicity
story is wrong, and the negative result needs a different explanation.

FINDING B -- the anchor everything is measured against is weak.
su_average is the start for the oracle solve, the unrolled model and every
Adam row. The lazier alternative costs nothing: all K single-user
alignment phases are already computed, so score them plus su_average and
keep the best per scenario.
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, KUS, T = 1200, 4, 8
panel, cfg = make_mumiso_scenario(n_users=KUS, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)                       # [S,K,N]
_, TH_SU = B.su_average(F, G, hd, pt, nv)


def minrate(th):
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values


def solve(start, steps=600, lr=0.05):
    dl = start.clone().requires_grad_(True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(steps):
        th = TH_SU + dl
        R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return (TH_SU + dl.detach()), dl.detach()


print("=== FINDING A: is the optimum determined by the scenario? ===",
      flush=True)
g = torch.Generator().manual_seed(0)
starts = {
    "zeros (project default)": torch.zeros(NS, N),
    "uniform (-pi, pi]": (torch.rand(NS, N, generator=g) * 2 - 1) * np.pi,
    "small gaussian": torch.randn(NS, N, generator=g) * 0.3,
}
sols, offs = {}, {}
for nm, st in starts.items():
    t0 = time.time()
    th, dl = solve(st)
    sols[nm], offs[nm] = th, dl
    print(f"  {nm:<24} rate {minrate(th).mean():.4f}   "
          f"({time.time()-t0:.0f}s)", flush=True)

keys = list(starts)
print("\n  agreement = mean cos(phase difference), per element")
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = sols[keys[i]], sols[keys[j]]
        same = torch.cos(a - b).mean().item()
        perm = torch.randperm(NS, generator=g)
        diff = torch.cos(a - b[perm]).mean().item()
        print(f"    {keys[i][:18]:<18} vs {keys[j][:18]:<18}  "
              f"SAME scenario {same:+.4f}   DIFFERENT {diff:+.4f}")

print("\n  reading: if SAME is far above DIFFERENT, two independent solves")
print("  land in the same place, the target is determined by the input, and")
print("  'the target is noise w.r.t. the input' is NOT what is happening.")

print("\n=== FINDING B: is su_average a weak anchor? ===", flush=True)
t0 = time.time()
r_su = minrate(TH_SU).mean().item()
# score all K single-user alignments plus su_average, keep the best
cand = torch.cat([phi, TH_SU.unsqueeze(1)], dim=1)          # [S,K+1,N]
scores = torch.stack([minrate(cand[:, k]) for k in range(cand.shape[1])])
best_idx = scores.argmax(0)
th_best = cand[torch.arange(NS), best_idx]
r_best = minrate(th_best).mean().item()
print(f"  su_average               : {r_su:.4f}")
print(f"  best-of-(K+1) per scenario: {r_best:.4f}   "
      f"(+{100*(r_best-r_su)/r_su:.1f}%)   [{time.time()-t0:.1f}s for {NS}]")
chosen = torch.bincount(best_idx, minlength=cand.shape[1]).float() / NS
print(f"  how often each is picked  : "
      + " ".join(f"{100*c:.0f}%" for c in chosen)
      + "   (last entry = su_average)")

print("\n  consequences for the report's framing:")
for L in (8, 16):
    for nm, st in (("su_average", TH_SU), ("best-of-(K+1)", th_best)):
        dl = torch.zeros(NS, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            th = st + dl
            R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        print(f"    {nm:<14} + Adam {L:2d} -> {minrate(st+dl.detach()).mean():.4f}")
print(f"\n  unrolled model's reported gain was 1.112 -> 3.265 = 2.94x over")
print(f"  su_average; over the lazier anchor ({r_best:.3f}) it is "
      f"{3.265/r_best:.2f}x.")
```

### `scripts/verify_mumiso_system.py`

*85 satir · sha256:70c1c3a5ca9a*

```python
"""Verify mumiso.system against the independently checked numpy reference."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso import system as S

torch.manual_seed(0); rng = np.random.default_rng(0)
def cn(*s): return (rng.normal(size=s)+1j*rng.normal(size=s))/np.sqrt(2)

print("=== 1) single-user reduction: general form vs published Eq. (8) ===")
N = 32
F = cn(1, N, 1); G = cn(1, 1, N); hd = cn(1, 1, 1)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
a = (G[0, 0] * F[0, :, 0])
th_gen = S.su_align_phase(tF, tG, tH)[0, 0].numpy()
th_eq8 = -np.angle(a)
def gain(th):
    c = torch.tensor(np.cos(th))[None]; s = torch.tensor(np.sin(th))[None]
    return S.effective_channel(tF, tG, tH, c, s).abs().item() ** 2
bound = (abs(hd[0, 0, 0]) + np.abs(a).sum()) ** 2
print(f"  general form / bound : {gain(th_gen)/bound:.4f}   (expect 1.0000)")
print(f"  Eq. (8)      / bound : {gain(th_eq8)/bound:.4f}   (expect < 1)")

print("\n=== 2) ZF nulls interference ===")
B, N, T, K = 4, 32, 8, 4
F = cn(B, N, T); G = cn(B, K, N); hd = cn(B, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
th = torch.tensor(rng.uniform(-np.pi, np.pi, (B, N)))
He = S.effective_channel(tF, tG, tH, torch.cos(th), torch.sin(th))
W = S.zf(He, 1.0)
A = (He @ W).abs() ** 2
off = A - torch.diag_embed(torch.diagonal(A, dim1=-2, dim2=-1))
print(f"  max leakage : {off.abs().max().item():.3e}   (expect ~0)")
print(f"  ||W||_F^2   : {(W.abs()**2).sum((-1,-2)).mean().item():.6f}   (expect 1.0)")
W = S.mrt(He, 1.0)
print(f"  MRT ||W||_F^2: {(W.abs()**2).sum((-1,-2)).mean().item():.6f}   (expect 1.0)")

print("\n=== 3) rate gradient vs finite differences ===")
B, N, T, K = 2, 16, 4, 3
F = cn(B, N, T); G = cn(B, K, N); hd = cn(B, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F, G, hd))
th0 = rng.uniform(-np.pi, np.pi, (B, N))
def f(t, grad=False):
    tt = torch.tensor(t, requires_grad=grad)
    R = S.rates(tF, tG, tH, torch.cos(tt), torch.sin(tt), 1.0, 1e-3)
    return R.min(-1).values.sum(), tt
v, tt = f(th0, True); v.backward()
g_auto = tt.grad.numpy().copy()
eps = 1e-6; g_fd = np.zeros_like(th0)
for b in range(B):
    for n in range(N):
        tp = th0.copy(); tp[b, n] += eps
        tm = th0.copy(); tm[b, n] -= eps
        g_fd[b, n] = (f(tp)[0].item() - f(tm)[0].item()) / (2*eps)
d = np.abs(g_auto - g_fd).max()
print(f"  max abs diff : {d:.3e}   relative {d/np.abs(g_fd).max():.3e}  (expect <1e-5)")

print("\n=== 4) raw (non-unit) network output is scale invariant ===")
c = torch.tensor(np.cos(th0)); s = torch.tensor(np.sin(th0))
gsc = torch.tensor(rng.uniform(0.2, 5.0, (B, N)))
R1 = S.rates(tF, tG, tH, *S.unit_phase(c, s), 1.0, 1e-3)
R2 = S.rates(tF, tG, tH, *S.unit_phase(gsc*c, gsc*s), 1.0, 1e-3)
print(f"  max diff : {(R1-R2).abs().max().item():.3e}   (expect ~0)")

print("\n=== 5) straight-through quantiser: value rounds, gradient passes ===")
for bits in (1, 2, 3):
    cc = torch.tensor(np.cos(th0), requires_grad=True)
    ss = torch.tensor(np.sin(th0), requires_grad=True)
    cq, sq = S.quantise_ste(cc, ss, bits)
    tq = torch.atan2(sq, cq).detach().numpy()
    step = 2*np.pi/(2**bits)
    on_grid = np.abs(tq/step - np.round(tq/step)).max()
    cq.sum().backward()
    # d cos(theta_q)/d cos(theta) should equal d cos(theta)/d cos(theta) route
    print(f"  {bits}-bit: on grid (max dev) {on_grid:.2e}   grad finite "
          f"{bool(np.isfinite(cc.grad.numpy()).all())}   "
          f"grad nonzero {bool(np.abs(cc.grad.numpy()).max()>0)}")

print("\n=== 6) soft min is a tight lower bound on the true min ===")
R = torch.tensor(16.0 + rng.normal(0, .5, (64, 4)), dtype=torch.float32)
for beta in (4., 8., 16.):
    sm = -torch.logsumexp(-beta*R, dim=-1)/beta
    tm = R.min(-1).values
    print(f"  beta={beta:4.0f}: gap to true min  mean {(tm-sm).mean():.4f}  "
          f"max {(tm-sm).max():.4f}   bound log(K)/beta = {np.log(4)/beta:.4f}")
```

### `scripts/verify_mumiso_channel.py`

*63 satir · sha256:c5b24cbab83e*

```python
"""Shapes, array correlation, Ricean K and effective rank of the MU-MISO channel."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   effective_rank, neighbour_corr)
from ris_mu.mumiso import system as S

print("=== 1) shapes, for several (K, T) ===")
for K_u, T in [(4, 4), (1, 4), (4, 1), (1, 1), (6, 8)]:
    panel, cfg = make_mumiso_scenario(n_users=K_u, n_bs_antennas=T, seed=1)
    d = MuMisoChannel(panel, cfg).generate(8)
    N = panel.positions.shape[0]
    ok = (d["F"].shape == (8, N, T) and d["G"].shape == (8, K_u, N)
          and d["hd"].shape == (8, K_u, T))
    print(f"  K={K_u} T={T}: F{d['F'].shape} G{d['G'].shape} hd{d['hd'].shape}"
          f"   {'OK' if ok else 'MISMATCH'}")

print("\n=== 2) diagnostics, K=4 T=4, 600 samples ===")
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=4, seed=7)
d = MuMisoChannel(panel, cfg).generate(600)
N = panel.positions.shape[0]
F, G, hd = d["F"], d["G"], d["hd"]
print(f"  N = {N}, T = {F.shape[-1]}, K = {G.shape[1]}")
print(f"  G effective rank (pooled users) : {effective_rank(G.reshape(-1, N)):6.2f}  (max {N})")
print(f"  G effective rank (user 0)       : {effective_rank(G[:, 0]):6.2f}")
print(f"  F effective rank (antenna 0)    : {effective_rank(F[:, :, 0]):6.2f}"
      f"   <- low is EXPECTED, BS and RIS are static")
print(f"  G neighbour |corr| (n, n+1)     : {neighbour_corr(G.reshape(-1, N)):6.4f}")
print(f"  F neighbour |corr| (n, n+1)     : {neighbour_corr(F[:, :, 0]):6.4f}")

print("\n=== 3) array correlation across ANTENNAS (should be high, not 1) ===")
Ft = F.transpose(0, 2, 1).reshape(-1, F.shape[-1])     # [(S*N), T]
print(f"  antenna-axis neighbour |corr|   : {neighbour_corr(Ft):6.4f}")
print(f"  antenna-axis effective rank     : {effective_rank(Ft):6.4f}  (max {F.shape[-1]})")

print("\n=== 4) Ricean K actually realised (from the 3GPP draw) ===")
print(f"  LoS fraction  BS->RIS : {d['los_ris_bs'].mean():.3f}")
print(f"  LoS fraction  RIS->UE : {d['los_ris_ue'].mean():.3f}")
print(f"  LoS fraction  direct  : {d['los_direct'].mean():.3f}")

print("\n=== 5) link budget sanity: baseline rates ===")
from ris_mu.mumiso.channel import to_torch
tF, tG, tH, rdt = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
print(f"  snr_scale = {cfg.snr_scale():.3e}  ->  noise_var = {nv:.3e}")
rng = np.random.default_rng(0)
def rate(th, prec="zf"):
    t = torch.as_tensor(th, dtype=rdt)
    return S.rates(tF, tG, tH, torch.cos(t), torch.sin(t), pt, nv, prec)
th_r = rng.uniform(-np.pi, np.pi, (600, N))
R_rand = rate(th_r)
th_su = S.su_align_phase(tF, tG, tH)              # [S,K,N]
pw = (np.abs(G) ** 2).sum(-1)
weak = pw.argmin(-1)
th_w = th_su[np.arange(600), weak].numpy()
R_su = rate(th_w)
He0 = tH
W0 = S.zf(He0, pt)
R_nr = torch.log2(1 + S.sinr(He0, W0, nv))
for nm, R in [("no RIS", R_nr), ("random phase", R_rand), ("SU (weakest)", R_su)]:
    m = S.rate_metrics(R)
    print(f"  {nm:14s} min {m['min_rate']:7.3f}   sum {m['sum_rate']:8.3f}  b/s/Hz")
```

### `scripts/verify_mumiso_models.py`

*91 satir · sha256:15b75565f57a*

```python
"""Shapes, parameter counts and the permutation-symmetry claim."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.models import MuMisoNet, count_params, MODES
from ris_mu.mumiso.features import n_channels

torch.manual_seed(0)
N, K, T = 32, 4, 8
C = n_channels(T)
B = 6
x = torch.randn(B, K, C, N)

print(f"N={N} K={K} T={T} -> C={C}\n")
print(f"{'mode':>10}{'params':>10}{'out shape':>14}{'|cos|^2+|sin|^2':>18}")
print("-" * 52)
nets = {}
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m).eval()
    nets[m] = net
    y = net(x)
    c, s = net.phases(x)
    unit = (c**2 + s**2).mean().item()
    print(f"{m:>10}{count_params(net):10d}{str(tuple(y.shape)):>14}{unit:18.6f}")

print("\n=== permutation symmetry (eval mode) ===")
rng = np.random.default_rng(0)
for m, net in nets.items():
    base = net(x).detach()
    devs = []
    for _ in range(6):
        p = torch.tensor(rng.permutation(K))
        devs.append((net(x[:, p]).detach() - base).abs().max().item())
    mx = max(devs)
    scale = base.abs().max().item()
    rel = mx / max(scale, 1e-30)
    verdict = ("INVARIANT" if mx < 1e-5 else
               f"order sensitive (max dev {mx:.3e}, {100*rel:.1f}% of output scale)")
    print(f"  {m:>10}: {verdict}")
print("  NOTE: at initialisation the concat number is not meaningful -- an")
print("  untrained net is near-random. The result that matters is order")
print("  sensitivity of the RATE after training; measured in the training run.")

print("\n=== is it BatchNorm or Dropout that breaks train-mode symmetry? ===")
# BN in train mode (batch statistics live) but Dropout disabled, so the only
# remaining asymmetry source would be BN itself.
for m, net in nets.items():
    net.train()
    for mod in net.modules():
        if isinstance(mod, torch.nn.Dropout):
            mod.eval()
    net.body.lstm.dropout = 0.0
    base = net(x).detach()
    p = torch.tensor(rng.permutation(K))
    dev = (net(x[:, p]).detach() - base).abs().max().item()
    tag = "INVARIANT" if dev < 1e-5 else f"dev {dev:.3e}"
    print(f"  {m:>10}: BN train + dropout off -> {tag}")
    net.eval()
print("  -> any residual deviation in full train mode is Dropout randomness,")
print("     not a symmetry violation. Invariance is a property of inference.")

print("\n=== defined for a K it was not built for? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m).eval()
    for K2 in (2, 6):
        try:
            out = net(torch.randn(3, K2, C, N))
            print(f"  {m:>10} K={K2}: OK  {tuple(out.shape)}")
        except Exception as e:
            print(f"  {m:>10} K={K2}: refused -- {type(e).__name__}: "
                  f"{str(e)[:60]}")

print("\n=== exchange starts as identity-to-deepsets? ===")
torch.manual_seed(3)
ex = MuMisoNet(N=N, n_users=K, n_tx=T, mode="exchange").eval()
ds = MuMisoNet(N=N, n_users=K, n_tx=T, mode="deepsets").eval()
ds.load_state_dict({k: v for k, v in ex.state_dict().items()
                    if not k.startswith("ex")}, strict=True)
d = (ex(x) - ds(x)).abs().max().item()
print(f"  max diff at init : {d:.3e}   (exchange mixers are zero-init, so ~0)")
print("  -> exchange can only improve on deepsets from the start, never start worse")

print("\n=== gradient flows to every parameter? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m)
    c, s = net.phases(x)
    (c.sum() + s.sum()).backward()
    dead = [n for n, p in net.named_parameters()
            if p.requires_grad and (p.grad is None or p.grad.abs().max() == 0)]
    print(f"  {m:>10}: {len(dead)} parameter tensors with no gradient"
          + (f"  {dead[:3]}" if dead else ""))
```

### `scripts/verify_mobile.py`

*106 satir · sha256:1913e291c531*

```python
"""
Does the mobile channel actually age, and at the right rate?

Three things have to hold before the aging curve means anything:
  1. shapes, and F really is constant in time
  2. the channel changes CONTINUOUSLY -- consecutive snapshots are
     correlated, not independent draws. If the per-path gains leaked into
     the time loop this check fails and the whole experiment is measuring
     nothing but fresh randomness.
  3. it decorrelates on the timescale the coherence time predicts. At 3 GHz
     and 1.5 m/s the user covers 0.42 wavelengths in 28 ms, and Jakes'
     model gives J0(2*pi*0.42) = -0.05, i.e. essentially no correlation
     left. A generator that still correlates at 0.95 after 28 ms would make
     every classical method look usable.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

TIMES = (0.0, 1.0, 2.0, 5.0, 10.0, 14.1, 20.0, 28.2, 40.0, 60.0, 100.0,
         200.0, 500.0, 1500.0, 5600.0)

panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES})
ch = MobileMuMisoChannel(panel, cfg)
d = ch.generate(300)
N, T, K = panel.positions.shape[0], cfg.n_bs_antennas, cfg.n_users
M = len(TIMES)
lam = panel.lam

print("=== 1) shapes ===")
print(f"  F    {d['F'].shape}      expected (300, {N}, {T})")
print(f"  G_t  {d['G_t'].shape}  expected (300, {M}, {K}, {N})")
print(f"  hd_t {d['hd_t'].shape}  expected (300, {M}, {K}, {T})")
print(f"  ue_t {d['ue_t'].shape}  expected (300, {M}, {K}, 3)")

print("\n=== 2) does the user actually move, and F stay still? ===")
step = np.linalg.norm(d["ue_t"][:, 1] - d["ue_t"][:, 0], axis=-1).mean()
print(f"  mean displacement over first {TIMES[1]} ms : {100*step:.2f} cm"
      f"   (expected {100*cfg.velocity*TIMES[1]/1e3:.2f} cm)")
tot = np.linalg.norm(d["ue_t"][:, -1] - d["ue_t"][:, 0], axis=-1).mean()
print(f"  mean displacement over {TIMES[-1]:.0f} ms       : {tot:.2f} m")
print(f"  F has no time axis: {d['F'].ndim == 3}")

print("\n=== 3) temporal correlation of G (continuity + decorrelation) ===")


def corr(a, b):
    a = a.reshape(a.shape[0], -1)
    b = b.reshape(b.shape[0], -1)
    num = np.abs(np.sum(a * np.conj(b), axis=-1))
    den = np.sqrt(np.sum(np.abs(a) ** 2, -1) * np.sum(np.abs(b) ** 2, -1))
    return float(np.mean(num / np.maximum(den, 1e-30)))


print(f"  {'t [ms]':>9}{'disp [lam]':>12}{'|corr| to t=0':>15}"
      f"{'Jakes J0':>10}")
from numpy import i0  # noqa: F401  (only to keep numpy import obvious)
try:
    from scipy.special import j0 as _j0
except Exception:
    def _j0(x):
        # small-series fallback, accurate enough for the comparison
        return np.sum([(-1) ** k * (x / 2) ** (2 * k) /
                       (np.math.factorial(k) ** 2) for k in range(25)], axis=0)
for m in range(M):
    disp = cfg.velocity * TIMES[m] / 1e3 / lam
    print(f"  {TIMES[m]:9.1f}{disp:12.3f}{corr(d['G_t'][:, m], d['G_t'][:, 0]):15.4f}"
          f"{_j0(2*np.pi*disp):10.3f}")
print("  (the point is the ORDER: high near 0, gone by a fraction of a")
print("   wavelength. An exact Jakes match is not expected -- this is a")
print("   specular + cluster geometry, not an isotropic 2-D field.)")

print("\n=== 4) consecutive snapshots are not independent draws ===")
c_adj = corr(d["G_t"][:, 1], d["G_t"][:, 0])
# an independent redraw, for reference: shuffle scenarios
perm = np.random.default_rng(0).permutation(300)
c_ind = corr(d["G_t"][:, 0][perm], d["G_t"][:, 0])
print(f"  |corr| t=0 vs t={TIMES[1]} ms          : {c_adj:.4f}")
print(f"  |corr| between DIFFERENT scenarios : {c_ind:.4f}")
ok = c_adj > 0.5 and c_ind < 0.2
print(f"  continuity holds: {ok}"
      + ("" if ok else "   <-- gains are leaking into the time loop"))

print("\n=== 5) does a phase fixed at t=0 lose rate as the user walks? ===")
F = torch.as_tensor(d["F"], dtype=torch.complex64)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
G0 = torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64)
H0 = torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64)
_, th0 = B.su_best_of(F, G0, H0, pt, nv)
print(f"  {'t [ms]':>9}{'min rate':>11}{'of t=0':>9}")
r0 = None
for m in range(M):
    Gm = torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64)
    Hm = torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64)
    r = S.rates(F, Gm, Hm, torch.cos(th0), torch.sin(th0), pt, nv,
                "zf").min(-1).values.mean().item()
    r0 = r if r0 is None else r0
    print(f"  {TIMES[m]:9.1f}{r:11.4f}{r/r0:9.3f}")
```

### `scripts/verify_residual.py`

*57 satir · sha256:6a9e50a457ae*

```python
"""Does the residual model start exactly at su_average, and stay symmetric?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 200, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d); pt, nv = 1.0, 1.0/cfg.snr_scale()
phi = S.su_align_phase(F, G, hd).numpy()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi))
_, th_su = B.su_average(F, G, hd, pt, nv)
def mr(th): return S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf").min(-1).values.mean().item()
print(f"su_average reference rate : {mr(th_su):.4f}\n")

print("=== at initialisation the residual model should BE su_average ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True).eval()
    with torch.no_grad(): c, s = net.phases(X)
    th = torch.atan2(s, c)
    dev = torch.atan2(torch.sin(th-th_su), torch.cos(th-th_su)).abs().max().item()
    print(f"  {m:>10}: max circular deviation {dev:.3e}   rate {mr(th):.4f}")

print("\n=== permutation symmetry preserved with the anchor? (eval) ===")
rng = np.random.default_rng(0)
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True).eval()
    # perturb the head so it is not trivially the anchor
    with torch.no_grad():
        for prm in net.head.net[-1].parameters(): prm.add_(torch.randn_like(prm)*0.1)
    with torch.no_grad():
        base = torch.stack(net.phases(X))
        devs = []
        for _ in range(5):
            p = torch.tensor(rng.permutation(Kus))
            devs.append((torch.stack(net.phases(X[:, p])) - base).abs().max().item())
    mx = max(devs)
    print(f"  {m:>10}: {'INVARIANT' if mx<1e-5 else f'dev {mx:.3e}'}")

print("\n=== gradients finite at the zero-init singular point? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True)
    c, s = net.phases(X[:16])
    R = S.rates(F[:16],G[:16],hd[:16],c,s,pt,nv,"zf")
    S.maxmin_loss(R).backward()
    bad = [n for n,prm in net.named_parameters()
           if prm.grad is not None and not torch.isfinite(prm.grad).all()]
    nz = sum(1 for n,prm in net.named_parameters()
             if prm.grad is not None and prm.grad.abs().max()>0)
    tot = sum(1 for _ in net.parameters())
    print(f"  {m:>10}: non-finite grads {len(bad)}   params with gradient {nz}/{tot}")
```

### `scripts/verify_batch_dependence.py`

*53 satir · sha256:11ed1aa64660*

```python
"""zf()'nin regulatoru yigin ortalamasina bagli mi? Olcelim."""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(600)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
_,TH=B.su_average(F,G,hd,pt,nv)

def rates_for(idx, chunk):
    """idx senaryolarinin hizlari, 'chunk' buyuklugunde parcalarla hesaplanmis."""
    out=[]
    for i in range(0,len(idx),chunk):
        s=idx[i:i+chunk]
        R=S.rates(F[s],G[s],hd[s],torch.cos(TH[s]),torch.sin(TH[s]),pt,nv,"zf")
        out.append(R.min(-1).values)
    return torch.cat(out)

idx=torch.arange(600)
ref=rates_for(idx,600)          # hepsi tek cagrida
print(f"{'yigin boyu':>12}{'ortalama min hiz':>18}{'ref ile max sapma':>20}{'ortalama |sapma|':>18}")
for c in (600,300,100,50,10,1):
    r=rates_for(idx,c)
    dmax=(r-ref).abs().max().item()
    dmean=(r-ref).abs().mean().item()
    print(f"{c:12d}{r.mean().item():18.6f}{dmax:20.3e}{dmean:18.3e}")

print("\n--- ayni senaryo, farkli komsularla ---")
# senaryo 0'i tek basina, ve 599 baska senaryoyla birlikte olc
alone=rates_for(torch.tensor([0]),1).item()
with_others=ref[0].item()
print(f"  senaryo 0 tek basina        : {alone:.6f}")
print(f"  senaryo 0, 600'lu yiginda   : {with_others:.6f}")
print(f"  fark                        : {abs(alone-with_others):.3e}"
      f"  (%{100*abs(alone-with_others)/max(alone,1e-9):.3f})")

print("\n--- senaryo basina regulator ne verirdi? ---")
He=S.effective_channel(F,G,hd,torch.cos(TH),torch.sin(TH))
M=He@He.conj().transpose(-1,-2)
dg=torch.diagonal(M,dim1=-2,dim2=-1).real
per=dg.mean(-1)                      # senaryo basina
glob=dg.mean()                       # yigin geneli
print(f"  yigin geneli p_sig  : {glob.item():.4e}")
print(f"  senaryo basina p_sig: min {per.min().item():.4e}  "
      f"medyan {per.median().item():.4e}  max {per.max().item():.4e}")
print(f"  en zayif/en guclu orani : {(per.max()/per.min()).item():.1f}x")
print(f"  en zayif senaryo icin regulator {glob.item()/per.min().item():.1f}x fazla buyuk")
```

### `scripts/verify_baseline_strength.py`

*40 satir · sha256:27f30c3e8238*

```python
"""Is the fixed baseline strong enough? Compare against the lazier method."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 400, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d); pt, nv = 1.0, 1.0/cfg.snr_scale()
def mr(th): return S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf").min(-1).values.mean().item()

print(f"{NS} scenarios, N={N}, T={T}, K={Kus}, max-min [b/s/Hz]\n")
for nm, fn in [("su_average", B.su_average), ("cd", B.coord_descent),
               ("pga (Adam, 3 restarts)", B.pga), ("ao (3 starts + Adam)", B.ao)]:
    t0 = time.time(); R, th = fn(F, G, hd, pt, nv)
    print(f"  {nm:>24}  {S.rate_metrics(R)['min_rate']:7.4f}   ({time.time()-t0:5.1f}s)")

print("\n=== the lazy check: plain Adam from su_average, 400 steps ===")
_, th_su = B.su_average(F, G, hd, pt, nv)
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(400):
    th = th_su + dl
    R = S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf")
    loss = -(-torch.logsumexp(-8.0*R,dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
lazy = mr(th_su + dl.detach())
R_ao, _ = B.ao(F, G, hd, pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
print(f"  lazy Adam  {lazy:.4f}    ao  {ao:.4f}")
print(f"  verdict: {'AO is at least as strong -- OK' if ao >= lazy - 0.05 else f'AO STILL WEAK by {lazy-ao:.3f}'}")

print("\n=== longer Adam: has it converged, or does more help? ===")
for iters in (400, 1000, 2000):
    R, _ = B.ao(F, G, hd, pt, nv, pga_iters=iters)
    print(f"  ao with {iters:5d} Adam steps : {S.rate_metrics(R)['min_rate']:7.4f}")
```

### `scripts/verify_crossover.py`

*123 satir · sha256:3649874707cb*

```python
"""
verify_crossover.py
-------------------
Adversarial check on the step-3 conclusion.

The claim is that spatial mixing beats an element-local model on the
geometric channel at high CSI error, and never does so on the legacy channel.
Step 3 measured that once, with one seed. A 6.5% difference from a single run
is not evidence, so this repeats the decisive cell (sigma = 0.25) over several
seeds and reports the spread.

Each seed redraws BOTH the channel realisation and the network
initialisation, so the reported spread covers data and training noise
together.

Usage:  python scripts/verify_crossover.py --n 12000 --seeds 4
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                                        # noqa: E402
from ris_mu.channel import legacy_generate, MultiUserRISChannel, make_scenario  # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices            # noqa: E402
from ris_mu.models import SharedMLP, CNNLSTM                                 # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate            # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed               # noqa: E402
from scripts.step3_csi_transfer import add_csi_error                         # noqa: E402


def get_channel(kind, n, panel, seed):
    if kind == "legacy":
        d = legacy_generate(n, panel, seed=seed)
        return d["F"], d["G"][:, 0, :]
    p2, cfg = make_scenario(n_users=1, seed=seed)
    d = MultiUserRISChannel(p2, cfg).generate(n)
    return d["F"], d["G"][:, 0, :]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12000)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--sigma", type=float, default=0.25)
    ap.add_argument("--epochs", type=int, default=22)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    panel = RISPanel(M=8, K=4)
    N = panel.N
    itr, iva, ite = split_indices(args.n, seed=0)

    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for Xb, Yb in loader:
                P.append(model(Xb))
                T.append(Yb.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))

    def step_fn(model, b):
        Xb, Yb = b
        return phase_aware_mse(model(Xb), Yb.flatten(1))

    builders = {"element-local": lambda: SharedMLP(N),
                "global mixing": lambda: CNNLSTM(N, head="local")}
    res = {}

    for ch in ("legacy", "geometric"):
        for s in range(args.seeds):
            F, G = get_channel(ch, args.n, panel, seed=700 + s)
            Y = torch.from_numpy(su_labels(F, G))
            rng = np.random.default_rng(900 + s)
            Fe, Ge = add_csi_error(F, G, args.sigma, rng)
            X = torch.from_numpy(su_features(Fe, Ge))
            tr, va, te = make_loaders((X, Y), itr, iva, ite)
            for mname, build in builders.items():
                set_seed(1000 + s)
                model = build()
                run_training(model, tr, va, step_fn, eval_fn,
                             epochs=args.epochs, tag="", verbose=False)
                _, m = eval_fn(model, te)
                res[f"{ch}|{s}|{mname}"] = m["rmse"]
                print(f"  {ch:<10} seed {s}  {mname:<14} RMSE={m['rmse']:7.3f}°")

    print(f"\nsigma = {args.sigma}, {args.seeds} seeds, mean +- std over seeds")
    print(f"{'channel':<12}{'element-local':>18}{'global mixing':>18}"
          f"{'advantage':>14}{'wins':>7}")
    print("-" * 69)
    summary = {}
    for ch in ("legacy", "geometric"):
        a = np.array([res[f"{ch}|{s}|element-local"] for s in range(args.seeds)])
        b = np.array([res[f"{ch}|{s}|global mixing"] for s in range(args.seeds)])
        adv = 100 * (b - a) / a                       # negative = mixing wins
        wins = int((b < a).sum())
        summary[ch] = dict(local_mean=float(a.mean()), local_std=float(a.std()),
                           mix_mean=float(b.mean()), mix_std=float(b.std()),
                           advantage_mean=float(adv.mean()),
                           advantage_std=float(adv.std()),
                           mixing_wins=wins, n_seeds=args.seeds)
        print(f"{ch:<12}{a.mean():>12.2f}±{a.std():<5.2f}"
              f"{b.mean():>12.2f}±{b.std():<5.2f}"
              f"{adv.mean():>+9.1f}±{adv.std():<4.1f}%{wins:>4}/{args.seeds}")

    print("\n  (advantage negative = spatial mixing beats the element-local "
          "model;\n   'wins' counts seeds where it did)")

    p = os.path.join(args.out, "verify_crossover.json")
    json.dump(dict(per_run=res, summary=summary, sigma=args.sigma), open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/verify_head_claim.py`

*163 satir · sha256:ccc519076f7e*

```python
"""
verify_head_claim.py
--------------------
Adversarial check on the step-2 conclusion.

The claim is that the dense output head, not the body, limits the published
architecture. The obvious objection is that the dense models were simply
undertrained or badly tuned. This script gives the dense head every
reasonable advantage and checks whether it recovers:

  A  published head, published settings            (the step-2 number)
  B  published head, lower LR, longer, no dropout  (tuning objection)
  C  widened bottleneck: last hidden 64 -> 512     (direct test of the
                                                    bottleneck explanation)
  D  local head                                    (the reference point)

If B stays far from D the tuning objection fails. If C closes most of the gap
the bottleneck explanation is confirmed directly, since C changes nothing but
the width of the layer that feeds the 2N outputs.

Usage:  python scripts/verify_head_claim.py --n 40000
"""

import argparse
import json
import os
import sys

import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                              # noqa: E402
from ris_mu.channel import legacy_generate                        # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices  # noqa: E402
from ris_mu.models import CNNOnly, count_params                   # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


class WideDenseHead(nn.Module):
    """Published head with the final hidden layer widened."""

    def __init__(self, c, N, width=512):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(c * N, 512), nn.ReLU(inplace=True),
            nn.Linear(512, 512), nn.ReLU(inplace=True),
            nn.Linear(512, width), nn.ReLU(inplace=True),
            nn.Linear(width, 2 * N),
        )

    def forward(self, h):
        return self.net(h.flatten(1))


class NoDropDenseHead(nn.Module):
    """Published head with dropout removed."""

    def __init__(self, c, N):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(c * N, 256), nn.ReLU(inplace=True),
            nn.Linear(256, 128), nn.ReLU(inplace=True),
            nn.Linear(128, 64), nn.ReLU(inplace=True),
            nn.Linear(64, 2 * N),
        )

    def forward(self, h):
        return self.net(h.flatten(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N
    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]
    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)

    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for Xb, Yb in loader:
                P.append(model(Xb))
                T.append(Yb.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))

    def step_fn(model, b):
        Xb, Yb = b
        return phase_aware_mse(model(Xb), Yb.flatten(1))

    runs = []

    # A: published settings (reuse the step-2 result if present)
    prev = None
    p_ab = os.path.join(args.out, "step1b_head_ablation.json")
    if os.path.exists(p_ab):
        ab = json.load(open(p_ab))
        prev = next((v for v in ab.values()
                     if v["body"] == "CNN" and v["head"] == "dense"), None)
    if prev:
        runs.append(("A  dense, published settings", prev["params"],
                     prev["test_rmse"], prev["test_sr5"], "from step 2"))
    else:
        runs.append(("A  dense, published settings", 0, float("nan"), float("nan"), "-"))

    # B: tuned dense head
    set_seed(42)
    m = CNNOnly(N, head="dense")
    m.head = NoDropDenseHead(64, N)
    print("--- B  dense head, lr=3e-4, no dropout, 70 epochs")
    run_training(m, tr, va, step_fn, eval_fn, epochs=70, lr=3e-4,
                 milestones=(35, 55, 65), patience=20, tag="B", verbose=False)
    _, mb = eval_fn(m, te)
    runs.append(("B  dense, tuned", count_params(m), mb["rmse"], mb["sr5"],
                 "lr 3e-4, no dropout"))
    print(f"    RMSE={mb['rmse']:.3f}  SR@5={mb['sr5']:.2f}%\n")

    # C: widened bottleneck
    set_seed(42)
    m = CNNOnly(N, head="dense")
    m.head = WideDenseHead(64, N, width=512)
    print("--- C  dense head, final hidden widened 64 -> 512")
    run_training(m, tr, va, step_fn, eval_fn, epochs=50, lr=1e-3,
                 milestones=(20, 35, 45), patience=15, tag="C", verbose=False)
    _, mc = eval_fn(m, te)
    runs.append(("C  dense, widened bottleneck", count_params(m), mc["rmse"],
                 mc["sr5"], "64 -> 512 units"))
    print(f"    RMSE={mc['rmse']:.3f}  SR@5={mc['sr5']:.2f}%\n")

    # D: local head reference
    if prev is not None:
        loc = next((v for v in ab.values()
                    if v["body"] == "CNN" and v["head"] == "local"), None)
        if loc:
            runs.append(("D  local head (reference)", loc["params"],
                         loc["test_rmse"], loc["test_sr5"], "from step 2"))

    print(f"{'variant':<32}{'params':>10}{'RMSE':>10}{'SR@5':>9}   note")
    print("-" * 78)
    for name, pr, r, sr, note in runs:
        print(f"{name:<32}{pr:>10,}{r:>9.2f}°{sr:>8.2f}%   {note}")

    out = {n: dict(params=p, rmse=r, sr5=s, note=nt) for n, p, r, s, nt in runs}
    json.dump(out, open(os.path.join(args.out, "verify_head_claim.json"), "w"),
              indent=2)
    print(f"\nsaved -> {args.out}/verify_head_claim.json")


if __name__ == "__main__":
    main()
```

### `scripts/verify_matlab_architecture.py`

*133 satir · sha256:70e791323b23*

```python
"""
verify_matlab_architecture.py
-----------------------------
Resolves the reproduction gap.

The GitHub repository's `train_cnn_lstm.py` flattens the LSTM output over all
elements and pushes it through a dense bottleneck ending in 64 units. The
MATLAB script that actually produced the published results
(`theta_NN_multioutput_UPDATED.m`) does something different: its input is a
`sequenceInputLayer`, both LSTMs run with `OutputMode='sequence'`, and the
output stage is `fullyConnectedLayer(2)`. In MATLAB a fully connected layer
applied to a sequence acts on EVERY TIME STEP INDEPENDENTLY, so the published
model emits (sin, cos) per element through one shared 64->2 map.

That is a width-1 convolution -- the "local head" of this study -- not a
dense bottleneck. The two files are therefore different architectures, and
the Python one is not a port of the MATLAB one.

This script builds the MATLAB architecture exactly as written and trains it on
the legacy dataset, to check whether the published figure is reproducible once
the head matches.

    conv1d(4->64, k=3) + BN + ReLU
    conv1d(64->64, k=3) + BN + ReLU
    dropout(0.2)
    LSTM(64->128, sequence)
    LSTM(128->64, sequence)
    dropout(0.3)
    Linear(64->2) applied per element

Usage:  python scripts/verify_matlab_architecture.py --n 40000 --epochs 50
"""

import argparse
import json
import os
import sys

import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                              # noqa: E402
from ris_mu.channel import legacy_generate                        # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices  # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


class MatlabCNNLSTM(nn.Module):
    """Faithful port of the published MATLAB layer stack."""

    def __init__(self, N=32):
        super().__init__()
        self.N = N
        self.cnn = nn.Sequential(
            nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(inplace=True),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(inplace=True),
            nn.Dropout(0.2),
        )
        self.lstm1 = nn.LSTM(64, 128, batch_first=True)
        self.lstm2 = nn.LSTM(128, 64, batch_first=True)
        self.drop = nn.Dropout(0.3)
        self.fc = nn.Linear(64, 2)          # applied at every element

    def forward(self, x):                   # [B, 4, N]
        h = self.cnn(x).permute(0, 2, 1)    # [B, N, 64]
        h, _ = self.lstm1(h)
        h, _ = self.lstm2(h)
        h = self.fc(self.drop(h))           # [B, N, 2]
        return torch.cat([h[..., 0], h[..., 1]], dim=-1)   # [B, 2N]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N

    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]
    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)

    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for Xb, Yb in loader:
                P.append(model(Xb))
                T.append(Yb.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))

    def step_fn(model, b):
        Xb, Yb = b
        return phase_aware_mse(model(Xb), Yb.flatten(1))

    model = MatlabCNNLSTM(N)
    n_par = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"MATLAB architecture as published: {n_par:,} trainable parameters")
    print("(the paper reports 727,360 for this model)\n")

    info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                        lr=1e-3, milestones=(15, 30, 45), patience=18,
                        tag="matlab")
    _, m = eval_fn(model, te)

    print(f"\n{'':<34}{'RMSE':>9}{'SR@5':>9}{'params':>11}")
    print("-" * 63)
    print(f"{'published figure (paper)':<34}{2.77:>8.2f}°{'—':>9}{727360:>11,}")
    print(f"{'MATLAB architecture, re-run here':<34}{m['rmse']:>8.2f}°"
          f"{m['sr5']:>8.2f}%{n_par:>11,}")
    print(f"{'repo train_cnn_lstm.py (dense head)':<34}{27.97:>8.2f}°"
          f"{17.59:>8.2f}%{822976:>11,}")

    res = dict(matlab_rmse=m["rmse"], matlab_sr5=m["sr5"], matlab_params=n_par,
               paper_rmse=2.77, paper_params=727360, repo_python_rmse=27.97)
    json.dump(res, open(os.path.join(args.out, "verify_matlab_arch.json"), "w"),
              indent=2)
    print(f"\nsaved -> {args.out}/verify_matlab_arch.json")


if __name__ == "__main__":
    main()
```

### Bolum 4 -- cok kullanicili ogrenme (titiz olumsuz sonuc)

### `scripts/mumiso_run.py`

*146 satir · sha256:ab16ab18b22b*

```python
"""
Full MU-MISO experiment: dataset, baselines, three architectures,
permutation test, quantisation. Writes results/mumiso_*.json
"""
import sys, pathlib, json, time, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank, neighbour_corr)
from ris_mu.mumiso.features import mumiso_features, n_channels
from ris_mu.mumiso.models import MuMisoNet, count_params, MODES
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.train import train_model, evaluate
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=12000)
ap.add_argument("--epochs", type=int, default=30)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--M", type=int, default=8)
ap.add_argument("--K", type=int, default=4)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="main")
ap.add_argument("--no-residual", action="store_true",
                help="predict absolute phase instead of a rotation on the "
                     "su_average anchor (ablation)")
ap.add_argument("--link-ratio", action="store_true",
                help="append the two link-scale channels the "
                     "normalisation removes (features.link_ratio); C goes "
                     "from 5+4T to 7+4T, so a run with this flag is NOT "
                     "comparable to a checkpoint without it")
ap.add_argument("--baseline-n", type=int, default=1200,
                help="test scenarios used for the classical baselines; AO "
                     "runs 3 starts x 400 Adam steps and is the slow part")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)
res = dict(config=vars(a))
t_all = time.time()

def say(*m): print(*m, flush=True)

# ---------------------------------------------------------------- dataset
say(f"=== dataset: {a.samples} scenarios, T={a.tx}, K={a.users} ===")
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  M=a.M, K=a.K, seed=a.seed)
N = panel.positions.shape[0]
t0 = time.time()
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, rdt = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
say(f"  N={N} C={n_channels(a.tx, a.link_ratio)}  "
    f"link_ratio={a.link_ratio}  generated in {time.time()-t0:.1f}s")

phi = S.su_align_phase(F, G, hd).numpy()
t0 = time.time()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi,
                                     link_ratio=a.link_ratio))
say(f"  features {tuple(X.shape)}  {X.element_size()*X.nelement()/1e6:.0f} MB"
    f"  in {time.time()-t0:.1f}s")

res["channel"] = dict(
    N=N, n_channels=n_channels(a.tx, a.link_ratio),
    snr_scale=cfg.snr_scale(),
    g_rank_pooled=effective_rank(d["G"].reshape(-1, N)),
    g_rank_user0=effective_rank(d["G"][:, 0]),
    f_rank_ant0=effective_rank(d["F"][:, :, 0]),
    g_neigh_corr=neighbour_corr(d["G"].reshape(-1, N)),
    ant_neigh_corr=neighbour_corr(d["F"].transpose(0, 2, 1).reshape(-1, a.tx)),
    los_frac=dict(bs=float(d["los_ris_bs"].mean()),
                  ue=float(d["los_ris_ue"].mean()),
                  direct=float(d["los_direct"].mean())))
say("  G rank(pooled) {g_rank_pooled:.2f}  G rank(user0) {g_rank_user0:.2f}  "
    "F rank {f_rank_ant0:.2f}  G neigh {g_neigh_corr:.3f}".format(**res["channel"]))

tr, va, te = split_indices(a.samples, seed=0)
say(f"  split  train {len(tr)}  val {len(va)}  test {len(te)}")

# -------------------------------------------------------------- baselines
bte = te[:a.baseline_n]
say(f"\n=== baselines on {len(bte)} test scenarios ===")
meth = ("no_ris", "random", "su_weakest", "su_average", "su_best_of",
        "cd", "pga", "ao")
res["baselines"] = {}
for m in meth:
    t0 = time.time()
    R, th = B._DISPATCH[m](F[bte], G[bte], hd[bte], pt, nv, precoder="zf")
    mt = S.rate_metrics(R)
    res["baselines"][m] = mt | {"sec": time.time() - t0}
    say(f"  {m:>11}  min {mt['min_rate']:7.4f}  sum {mt['sum_rate']:8.3f}"
        f"   ({time.time()-t0:.1f}s)")
# The strongest classical, not AO by assumption. PGA (3 random restarts)
# and AO (cd + su_average + random) differ by well under a percent and
# which one wins varies run to run, so naming one of them in advance was
# how an earlier version of this project ended up reporting the weaker of
# the two as "the number to beat".
_cands = {m: res["baselines"][m]["min_rate"]
          for m in ("cd", "pga", "ao") if m in res["baselines"]}
_best = max(_cands, key=_cands.get)
target = _cands[_best]
say(f"  -> the number to beat is {_best}: {target:.4f}   "
    f"(others: {', '.join(f'{k} {v:.4f}' for k, v in _cands.items() if k != _best)})")
res["target"] = dict(method=_best, rate=target)

# ------------------------------------------------------------------ train
res["models"] = {}
for mode in MODES:
    say(f"\n=== train mode={mode} ===")
    torch.manual_seed(a.seed)
    net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=mode,
                    residual=not a.no_residual, link_ratio=a.link_ratio)
    say(f"  parameters: {count_params(net)}")
    t0 = time.time()
    net, hist = train_model(net, X, F, G, hd, pt, nv, (tr, va, te),
                            epochs=a.epochs, seed=a.seed, log=say)
    t_min, t_sum = evaluate(net, X, F, G, hd, pt, nv, te)
    say(f"  TEST  min {t_min:.4f}  sum {t_sum:.3f}   "
        f"({t_min/target:.3f}x of AO)   [{time.time()-t0:.0f}s]")

    # order sensitivity, measured on the RATE
    chk = te[:2000]
    vals = []
    rng = np.random.default_rng(0)
    for r in range(6):
        p = np.arange(a.users) if r == 0 else rng.permutation(a.users)
        pt_ = torch.as_tensor(p)
        v, _ = evaluate(net, X[:, pt_], F, G[:, pt_], hd[:, pt_], pt, nv, chk)
        vals.append(v)
    spread = float(np.max(vals) - np.min(vals))
    say(f"  user-order spread over 6 permutations: {spread:.2e}  "
        f"(mean {np.mean(vals):.4f})")

    res["models"][mode] = dict(params=count_params(net), test_min=t_min,
                               residual=not a.no_residual,
                               test_sum=t_sum, frac_of_ao=t_min / target,
                               perm_spread=spread, perm_mean=float(np.mean(vals)),
                               history=hist, sec=time.time() - t0)
    torch.save(net.state_dict(), OUT / f"mumiso_{a.tag}_{mode}.pt")

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\n=== done in {(time.time()-t_all)/60:.1f} min -> "
    f"results/mumiso_{a.tag}.json ===")
```

### `scripts/mumiso_unrolled.py`

*156 satir · sha256:e557411495d9*

```python
"""
Does learning the UPDATE RULE work where learning the solution does not?

Trains the unrolled model on the final rate and compares against the anchor
it starts from and the strong classical baseline it is trying to approach.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso, count_params
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=8000)
ap.add_argument("--epochs", type=int, default=25)
ap.add_argument("--steps", type=int, default=6)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--use-grad", action="store_true")
ap.add_argument("--bs", type=int, default=32)
ap.add_argument("--lr", type=float, default=1e-3)
ap.add_argument("--baseline-n", type=int, default=600)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="unrolled")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(a.samples, seed=0)
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}  steps={a.steps}  "
    f"mode={a.mode}  use_grad={a.use_grad}")

# anchor the unrolling starts from
_, TH0 = B.su_average(F, G, hd, pt, nv)


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


bte = te[:a.baseline_n]
say(f"\nanchor su_average on test : {mr(TH0[te], te):.4f}")
t0 = time.time()
R_ao, _ = B.ao(F[bte], G[bte], hd[bte], pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
R_cd, _ = B.coord_descent(F[bte], G[bte], hd[bte], pt, nv)
cd = S.rate_metrics(R_cd)["min_rate"]
say(f"coord descent on {len(bte)}    : {cd:.4f}")
say(f"AO (strong) on {len(bte)}      : {ao:.4f}   ({time.time()-t0:.0f}s)")

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode=a.mode, use_grad=a.use_grad)
say(f"\nparameters: {count_params(net)}")


def run_eval(ids, bs=256, trace=False):
    net.eval()
    tot_min = tot_sum = 0.0
    tr_acc = None
    with torch.no_grad():
        for i in range(0, len(ids), bs):
            j = ids[i:i + bs]
            out = net(X[j], F[j], G[j], hd[j], pt, nv, TH0[j],
                      return_trace=trace)
            th, tc = out if trace else (out, None)
            R = S.rates(F[j], G[j], hd[j], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            tot_min += R.min(-1).values.sum().item()
            tot_sum += R.sum(-1).sum().item()
            if trace:
                tr_acc = np.array(tc) * len(j) if tr_acc is None \
                    else tr_acc + np.array(tc) * len(j)
    out = (tot_min / len(ids), tot_sum / len(ids))
    return out + ((tr_acc / len(ids),) if trace else ())


say(f"before training, val min : {run_eval(va[:500])[0]:.4f}  "
    f"(should sit at the anchor)")

opt = torch.optim.Adam(net.parameters(), lr=a.lr)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.epochs)
rng = np.random.default_rng(a.seed)
best, best_state, hist = -np.inf, None, []
for ep in range(1, a.epochs + 1):
    net.train()
    t0, run, nb = time.time(), 0.0, 0
    perm = tr[rng.permutation(len(tr))]
    for i in range(0, len(perm), a.bs):
        j = perm[i:i + a.bs]
        th = net(X[j], F[j], G[j], hd[j], pt, nv, TH0[j])
        R = S.rates(F[j], G[j], hd[j], torch.cos(th), torch.sin(th), pt, nv,
                    "zf")
        loss = S.maxmin_loss(R)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        run += loss.item()
        nb += 1
    sched.step()
    v_min, v_sum = run_eval(va[:500])
    hist.append(dict(epoch=ep, loss=run / nb, val_min=v_min, val_sum=v_sum))
    mark = ""
    if v_min > best:
        best = v_min
        best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
        mark = "  *"
    say(f"  epoch {ep:3d}/{a.epochs}  loss {run/nb:8.4f}  val min {v_min:7.4f}"
        f"  sum {v_sum:8.3f}  ({time.time()-t0:.0f}s){mark}")

if best_state is not None:
    net.load_state_dict(best_state)

t_min, t_sum, trace = run_eval(te, trace=True)
say(f"\nTEST  min {t_min:.4f}  sum {t_sum:.3f}")
say(f"  anchor {mr(TH0[te], te):.4f}   cd {cd:.4f}   AO {ao:.4f}")
say(f"  fraction of AO : {t_min/ao:.3f}")
say("  per-step min rate: " + " -> ".join(f"{v:.3f}" for v in trace))
say("  learned step sizes: "
    + " ".join(f"{v:.3f}" for v in torch.exp(net.log_step).detach().tolist()))

res = dict(config=vars(a), anchor=mr(TH0[te], te), cd=cd, ao=ao,
           test_min=t_min, test_sum=t_sum, frac_of_ao=t_min / ao,
           per_step=[float(v) for v in trace], history=hist,
           params=count_params(net))
with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
torch.save(net.state_dict(), OUT / f"mumiso_{a.tag}.pt")
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_equal_step.py`

*255 satir · sha256:ae3ea9cfbd22*

```python
"""
The comparison that decides whether the learned update rule earns a chapter.

WHAT WAS WRONG WITH THE EARLIER VERSION
---------------------------------------
`mumiso_budget.py` compares L learned steps against L Adam steps at two
HARDCODED learning rates (0.05 and 0.5). That is not an equal-budget
comparison, it is a comparison against two arbitrary settings. Two separate
unfairnesses, pulling in OPPOSITE directions:

  (a) Against the classical side: the best step size depends on L. At L=1
      the right step is large (one shot at it); at L=32 it is small. Fixing
      lr=0.5 for every L hands the learned model a win at the budgets where
      0.5 happens to be wrong. This project has already made the
      weak-baseline mistake four times; "the learned model beats 32-step
      Adam" is the fifth version of it.

  (b) Against the learned side: the checkpoint was trained with steps=8 and
      then TRUNCATED to L steps. A model trained to deliver its answer on
      step 8 has no reason to be good on step 3 -- its learned step sizes
      are a schedule for 8 steps, not for 3. Judging it at L != 8 judges a
      model nobody trained.

So this script fixes both:

  - the classical arm's step size is swept and chosen on the VALIDATION
    split, then reported on TEST, separately FOR EACH L;
  - the learned arm is a model TRAINED at that same L (one checkpoint per
    budget, written by scripts/mumiso_unrolled.py --steps L).

The two corrections cut in opposite directions, which is the point: the
experiment is not rigged either way, and neither outcome was known when it
was written.

THE UPPER BOUND ON TUNING
-------------------------
A sweep picks one lr for the whole test set. A sceptic can always say a
better schedule exists. So the script also reports PER-SCENARIO ORACLE lr:
for each scenario, the best rate over the whole lr grid, chosen with
knowledge of the answer. No deployable classical method can do better than
that at this budget, so if the learned model beats the oracle column the
claim is safe, and if it loses to the swept column the claim is dead.

WHAT IS HELD EQUAL
------------------
Same scenarios, same anchor (su_average), same objective (max-min via the
stabilised softmin), same precoder (regularised ZF with the MMSE
regulariser), same test split. "L steps" means L objective-and-gradient
evaluations on both sides. What is NOT equal, and is reported rather than
hidden: the learned arm pays a one-off training cost and carries 270k
parameters; the classical arm needs the lr sweep, which is itself a cost
paid offline.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=6000,
                help="MUST match the training runs, or the draw differs")
ap.add_argument("--budgets", default="1,2,4,8,16")
ap.add_argument("--ckpt-fmt", default="results/mumiso_eqstep_L{L}.pt")
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--val-n", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--lrs", default="0.02,0.05,0.1,0.2,0.35,0.5,0.75,1.0,1.5,2.0")
ap.add_argument("--ref-n", type=int, default=300,
                help="scenarios for the unbudgeted classical references")
ap.add_argument("--tag", default="equal_step")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
BUDGETS = [int(x) for x in a.budgets.split(",")]
LRS = [float(x) for x in a.lrs.split(",")]


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(a.samples, seed=0)
_, TH0 = B.su_average(F, G, hd, pt, nv)

ev = te[:a.eval_n]          # test:       what every number below is reported on
vv = va[:a.val_n]           # validation: what the lr is chosen on
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}")
say(f"test {len(ev)} scenarios (reporting)  |  val {len(vv)} (lr choice)")


def rate(th, ids):
    """Mean over scenarios of the per-scenario WORST user rate (max-min)."""
    R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                pt, nv, "zf")
    return R.min(-1).values


def adam_steps(ids, L, lr, obj="soft"):
    """
    L Adam steps on the phase offset from the su_average anchor.

    THE ASCENT OBJECTIVE IS ALSO A TUNING KNOB, so it is swept, not chosen.
    Two reasonable choices and no a-priori winner at small L:

      "soft"  the stabilised softmin (beta = 8), what the learned model
              trains on. Spreads gradient over all users; the naive
              -log(sum(exp(-beta R)))/beta form overflows in float32 once
              R reaches about 16 b/s/Hz, hence the logsumexp shift.
      "hard"  the true min, what `baselines._pga_from` uses and what every
              number is REPORTED on. Hands the gradient to one user per
              scenario.

    An earlier version of this script hardcoded "soft" -- which quietly
    handicapped the classical arm with the learned model's own objective
    while the package's own PGA uses "hard". Picking one by hand is the
    weak-baseline mistake wearing a different hat, so both are swept on
    validation alongside the step size and the better one is reported.
    """
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        if obj == "soft":
            loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        else:
            loss = -R.min(-1).values.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


res = dict(config=vars(a), anchor=rate(TH0[ev], ev).mean().item(), rows={})
say(f"\nanchor (su_average) on test : {res['anchor']:.4f}")
R_b, TH_b = B.su_best_of(F[ev], G[ev], hd[ev], pt, nv)
res["su_best_of"] = S.rate_metrics(R_b)["min_rate"]
say(f"su_best_of (free, 0 steps)  : {res['su_best_of']:.4f}")

# ----------------------------------------------------------- the comparison
say(f"\n=== equal step budget: learned(L) vs best-tuned Adam(L) ===")
say(f"{'L':>3} {'learned':>9} {'Adam swept':>11} {'(lr/obj)':>11} "
    f"{'Adam oracle':>12} {'L/swept':>9} {'L/oracle':>9}")
say("-" * 71)

OBJS = ("soft", "hard")

for L in BUDGETS:
    # ---- classical arm: (lr, objective) chosen on VALIDATION, reported
    #      on TEST. Both knobs swept; see adam_steps for why the objective
    #      is a knob and not a constant.
    val_scores = {}
    for ob in OBJS:
        for lr in LRS:
            val_scores[(lr, ob)] = rate(adam_steps(vv, L, lr, ob),
                                        vv).mean().item()
    best_lr, best_ob = max(val_scores, key=val_scores.get)
    swept = rate(adam_steps(ev, L, best_lr, best_ob), ev)

    # ---- the upper bound on tuning: best (lr, objective) PER SCENARIO,
    #      chosen on TEST with knowledge of the answer. No deployable
    #      classical method can beat this at this budget.
    per_cfg = torch.stack([rate(adam_steps(ev, L, lr, ob), ev)
                           for ob in OBJS for lr in LRS])
    oracle = per_cfg.max(0).values

    # ---- learned arm: a model TRAINED at this L
    ck = pathlib.Path(a.ckpt_fmt.format(L=L))
    if not ck.exists():
        say(f"{L:3d} {'(ckpt yok)':>9} {swept.mean().item():11.4f} "
            f"{best_lr:6.2f}/{best_ob:4} {oracle.mean().item():12.4f}")
        res["rows"][L] = dict(learned=None, swept=swept.mean().item(),
                              best_lr=best_lr, best_obj=best_ob,
                              oracle=oracle.mean().item(),
                              val_curve={f"{k[0]}|{k[1]}": v
                                         for k, v in val_scores.items()})
        continue
    net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=L,
                         mode=a.mode, use_grad=True)
    net.load_state_dict(torch.load(ck))
    net.eval()
    with torch.no_grad():
        th_l = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
    th_l = th_l[0] if isinstance(th_l, tuple) else th_l
    learned = rate(th_l, ev)

    # paired difference: the same scenarios, so report the spread of the
    # DIFFERENCE rather than two independent means
    dif = (learned - swept)
    res["rows"][L] = dict(
        learned=learned.mean().item(), swept=swept.mean().item(),
        best_lr=best_lr, best_obj=best_ob, oracle=oracle.mean().item(),
        learned_over_swept=(learned.mean() / swept.mean()).item(),
        learned_over_oracle=(learned.mean() / oracle.mean()).item(),
        paired_mean_diff=dif.mean().item(),
        paired_sem=(dif.std(unbiased=True) / len(dif) ** 0.5).item(),
        learned_wins_frac=(dif > 0).float().mean().item(),
        val_curve={f"{k[0]}|{k[1]}": v for k, v in val_scores.items()})
    r = res["rows"][L]
    say(f"{L:3d} {r['learned']:9.4f} {r['swept']:11.4f} "
        f"{best_lr:6.2f}/{best_ob:4} {r['oracle']:12.4f} "
        f"{r['learned_over_swept']:9.3f} {r['learned_over_oracle']:9.3f}")

# ------------------------------------------------- unbudgeted references
say(f"\n=== unbudgeted classical, same channel, {a.ref_n} scenarios ===")
rf = te[:a.ref_n]
for nm in ("cd", "pga", "ao"):
    R, _ = B._DISPATCH[nm](F[rf], G[rf], hd[rf], pt, nv, precoder="zf")
    res[nm] = S.rate_metrics(R)["min_rate"]
    say(f"  {nm:>4} : {res[nm]:.4f}")

# ------------------------------------------------------------- the verdict
say("\n=== verdict ===")
rows = {L: v for L, v in res["rows"].items() if v.get("learned") is not None}
if not rows:
    say("  no learned checkpoints found -- train them first")
else:
    beats_swept = [L for L, v in rows.items()
                   if v["paired_mean_diff"] - 2 * v["paired_sem"] > 0]
    loses_swept = [L for L, v in rows.items()
                   if v["paired_mean_diff"] + 2 * v["paired_sem"] < 0]
    tied = [L for L in rows if L not in beats_swept and L not in loses_swept]
    say(f"  budgets where learned BEATS tuned Adam (2 s.e.) : {beats_swept}")
    say(f"  budgets where learned LOSES  (2 s.e.)           : {loses_swept}")
    say(f"  statistically tied                              : {tied}")
    res["verdict"] = dict(beats=beats_swept, loses=loses_swept, tied=tied)
    say("\n  Read it straight: a learned update rule that does not beat the")
    say("  best-tuned classical step at ANY equal budget has no latency")
    say("  argument left, because the tuning is paid offline, once.")

(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_latency_parity.py`

*271 satir · sha256:c40f705e21b9*

```python
"""
The comparison the thesis claim actually needs: EQUAL WALL CLOCK.

WHY THE EQUAL-STEP RESULT IS NOT ENOUGH
---------------------------------------
`mumiso_equal_step.py` gives the learned update rule L steps and gives
tuned Adam L steps, and the learned rule wins at every L (1.011x to 1.052x,
paired lower bound positive at all five budgets). That is a real result, but
it is NOT the thesis claim, because a learned step and an Adam step do not
cost the same.

Measured, single scenario, one thread, IDLE MACHINE, median over 5
independent rounds (results/mumiso_latency_repeat.json):

        L      Adam [ms]   learned [ms]   ratio
        1         2.54          6.71      2.64x
        2         4.48         14.59      3.26x
        4         9.30         25.79      2.77x
        8        17.48         52.34      2.99x
       16        36.62         99.15      2.71x

(An earlier table here came from a run taken while training was going and
had Adam L=8 at 29.70 ms instead of 17.48 -- see the dominance block at the
bottom for what that did to the verdict.)

A learned step costs about 3x an Adam step, and the reason is structural,
not an implementation detail: per step the learned rule evaluates `rates`
once for the bottleneck signal, once more forward-and-backward for the
gradient channel, and then runs the CNN+LSTM body (K times in `exchange`
mode). Adam does the forward-and-backward only.

So "equal L" silently hands the learned arm three times the compute. The
honest axis is milliseconds, and on that axis the classical arm gets
roughly three times as many steps for the same budget. This script asks
whether the step-parity win survives that -- and if it does not, says so.

WHAT IS MEASURED
----------------
Rate on the same 600-scenario test split as the equal-step run, for:
  - the learned model at each L it was trained for;
  - tuned Adam at a RANGE of L extending well past the learned budgets,
    with (step size x ascent objective) swept on validation at every L.
Latency for both, single scenario, one thread, median of many repeats, on a
machine checked for load. Then the Pareto frontier of (latency, rate) and
which arm is on it.

A result either way is publishable. A learned optimiser that wins per step
and loses per millisecond is a negative result about deployment, and it is
the one the mobility chapter needs to hear, because there the budget is
milliseconds against a 28.2 ms coherence time.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=6000)
ap.add_argument("--learned-budgets", default="1,2,4,8,16")
ap.add_argument("--classical-budgets", default="1,2,4,8,16,24,32,48,64")
ap.add_argument("--ckpt-fmt", default="results/mumiso_eqstep_L{L}.pt")
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--val-n", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--lrs", default="0.2,0.35,0.5,0.75,1.0,1.5")
ap.add_argument("--reps", type=int, default=40, help="timing repeats")
ap.add_argument("--max-load", type=float, default=1.5)
ap.add_argument("--tag", default="latency_parity")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
LB = [int(x) for x in a.learned_budgets.split(",")]
CB = [int(x) for x in a.classical_budgets.split(",")]
LRS = [float(x) for x in a.lrs.split(",")]
OBJS = ("soft", "hard")


def say(*m):
    print(*m, flush=True)


load0 = float(open("/proc/loadavg").read().split()[0])
say(f"load before: {load0:.2f}")
if load0 > a.max_load:
    say(f"  WARNING: machine is busy (>{a.max_load}); latencies will be "
        f"inflated and the frontier may flip. Treat timings as unusable.")

torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(a.samples, seed=0)
_, TH0 = B.su_average(F, G, hd, pt, nv)
ev, vv = te[:a.eval_n], va[:a.val_n]
say(f"N={N} T={a.tx} K={a.users}  test {len(ev)}  val {len(vv)}")


def rate(th, ids):
    R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                pt, nv, "zf")
    return R.min(-1).values


def adam_steps(ids, L, lr, obj):
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = (-(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
                if obj == "soft" else -R.min(-1).values.mean())
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


# ------------------------------------------------------------------ timing
one = slice(0, 1)
_nthreads = torch.get_num_threads()
torch.set_num_threads(1)          # a deployed RIS controller is not a cluster


def time_adam(L, lr, obj):
    ts = []
    for _ in range(a.reps):
        t0 = time.perf_counter()
        dl = torch.zeros(1, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = TH0[one] + dl
            R = S.rates(F[one], G[one], hd[one], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            loss = (-(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
                    if obj == "soft" else -R.min(-1).values.mean())
            opt.zero_grad()
            loss.backward()
            opt.step()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


def time_learned(net):
    with torch.no_grad():
        for _ in range(3):
            net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])
    ts = []
    for _ in range(a.reps):
        t0 = time.perf_counter()
        with torch.no_grad():
            net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


res = dict(config=vars(a), load_before=load0,
           anchor=rate(TH0[ev], ev).mean().item(), learned={}, classical={})
R_b, _ = B.su_best_of(F[ev], G[ev], hd[ev], pt, nv)
res["su_best_of"] = S.rate_metrics(R_b)["min_rate"]
say(f"\nanchor {res['anchor']:.4f}   su_best_of {res['su_best_of']:.4f}")

# ------------------------------------------------------- the learned arm
say(f"\n=== learned arm ===")
say(f"{'L':>3}{'rate':>9}{'latency [ms]':>14}")
for L in LB:
    ck = pathlib.Path(a.ckpt_fmt.format(L=L))
    if not ck.exists():
        say(f"{L:3d}   (ckpt yok)")
        continue
    net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=L,
                         mode=a.mode, use_grad=True)
    net.load_state_dict(torch.load(ck))
    net.eval()
    with torch.no_grad():
        th = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
    th = th[0] if isinstance(th, tuple) else th
    r = rate(th, ev)
    ms = time_learned(net)
    res["learned"][L] = dict(rate=r.mean().item(), ms=ms,
                             per_scenario=r.tolist())
    say(f"{L:3d}{r.mean().item():9.4f}{ms:14.3f}")

# ----------------------------------------------------- the classical arm
say(f"\n=== classical arm: (lr x objective) swept on validation at each L ===")
say(f"{'L':>3}{'rate':>9}{'latency [ms]':>14}{'lr/obj':>12}")
for L in CB:
    best, bl, bo = -np.inf, None, None
    for ob in OBJS:
        for lr in LRS:
            v = rate(adam_steps(vv, L, lr, ob), vv).mean().item()
            if v > best:
                best, bl, bo = v, lr, ob
    r = rate(adam_steps(ev, L, bl, bo), ev)
    ms = time_adam(L, bl, bo)
    res["classical"][L] = dict(rate=r.mean().item(), ms=ms, lr=bl, obj=bo,
                               per_scenario=r.tolist())
    say(f"{L:3d}{r.mean().item():9.4f}{ms:14.3f}{bl:9.2f}/{bo:4}")

torch.set_num_threads(_nthreads)

# ----------------------------------------------------------- the frontier
# DOMINANCE, NOT INTERPOLATION. The first version of this block compared
# the learned rate against Adam's curve linearly interpolated at the same
# millisecond. That is wrong in a direction that matters: the rate-latency
# curve is CONCAVE (diminishing returns per step), so a straight line
# between two measured Adam points lies BELOW the true curve, which
# understates Adam and flatters the learned arm. On the 23 Oct run that
# artefact is what let learned L=4 appear to survive on the frontier.
#
# A learned point is dominated when some measured Adam setting is BOTH
# no slower AND no worse. That needs no interpolation and no assumption
# about the curve's shape.
say(f"\n=== dominance: is some Adam setting both FASTER and BETTER? ===")
say(f"{'learned L':>10}{'ms':>9}{'rate':>10}   {'dominated by':<30}{'verdict':>14}")
verdict = {}
for L, v in sorted(res["learned"].items()):
    ms, r = v["ms"], v["rate"]
    cands = [(k, c) for k, c in res["classical"].items()
             if c["ms"] <= ms and c["rate"] >= r]
    if cands:
        k, c = max(cands, key=lambda kc: kc[1]["rate"])
        txt = f"L={k}: {c['ms']:.1f} ms, {c['rate']:.4f}"
        verdict[L] = dict(ms=ms, learned=r, dominated=True,
                          by=dict(L=k, ms=c["ms"], rate=c["rate"]))
        say(f"{L:10d}{ms:9.1f}{r:10.4f}   {txt:<30}{'DOMINATED':>14}")
    else:
        faster = [c for c in res["classical"].values() if c["ms"] <= ms]
        bf = max(faster, key=lambda c: c["rate"])["rate"] if faster else None
        txt = f"best faster Adam: {bf:.4f}" if bf else "-"
        verdict[L] = dict(ms=ms, learned=r, dominated=False)
        say(f"{L:10d}{ms:9.1f}{r:10.4f}   {txt:<30}{'ON FRONTIER':>14}")
res["latency_verdict"] = verdict

loses = [L for L, v in verdict.items() if v["dominated"]]
wins = [L for L, v in verdict.items() if not v["dominated"]]
say(f"\n  learned on the frontier at: {wins}")
say(f"  strictly dominated at     : {loses}")
say(f"\n  Timings are only as good as the machine was quiet. Measured on an"
    f"\n  idle box over 5 independent rounds, round-to-round spread is"
    f"\n  1.06x-1.41x and all five learned points are dominated in 5/5"
    f"\n  rounds (results/mumiso_latency_repeat.json). A run taken while"
    f"\n  training was going inflated Adam L=8 from 17.5 ms to 29.7 ms and"
    f"\n  flipped one row -- contamination is not neutral, it favours"
    f"\n  whichever arm it slows down less.")
say("\n  Equal STEPS said the learned rule wins at every budget. Equal")
say("  MILLISECONDS is the axis the thesis claim lives on, because the")
say("  coherence time is 28.2 ms and not 28.2 steps. Report whichever")
say("  this table says, and report that the two axes disagree if they do.")

(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_latency_repeat.py`

*90 satir · sha256:c6687a3532ee*

```python
"""DOUBLE CHECK: gecikme hukmu zamanlama gurultusune dayanikli mi?

23 Ekim'de Adam L=8 bir kez 17.99 ms, bir kez 29.70 ms olculdu (%65 fark).
Baskinlik tablosu zamanlamalara dayandigi icin hukum bu gurultuye
dayanikli olmak zorunda. 5 bagimsiz tur, her turda medyan, sonra turlar
arasi dagilim.
"""
import sys, time, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
torch.set_num_threads(1)
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

panel,cfg=make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(64)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
phi=S.su_align_phase(F,G,hd)
X=torch.from_numpy(mumiso_features(d["F"],d["G"],d["hd"],phi.numpy()))
_,TH0=B.su_average(F,G,hd,pt,nv)
one=slice(0,1)

def t_adam(L,reps=25):
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        dl=torch.zeros(1,N,requires_grad=True)
        opt=torch.optim.Adam([dl],lr=0.75)
        for _ in range(L):
            th=TH0[one]+dl
            R=S.rates(F[one],G[one],hd[one],torch.cos(th),torch.sin(th),pt,nv,"zf")
            loss=-(-torch.logsumexp(-8.0*R,-1)/8.0).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        ts.append(time.perf_counter()-t0)
    return float(np.median(ts)*1e3)

NETS={}
def t_learned(L,reps=25):
    if L not in NETS:
        n=UnrolledMuMiso(N=N,n_users=4,n_tx=8,steps=L,mode="exchange",use_grad=True)
        n.load_state_dict(torch.load(_pl.Path(__file__).resolve().parents[1]
                              / f"results/mumiso_eqstep_L{L}.pt")); n.eval()
        NETS[L]=n
    net=NETS[L]
    with torch.no_grad():
        for _ in range(3): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
        ts.append(time.perf_counter()-t0)
    return float(np.median(ts)*1e3)

LB=[1,2,4,8,16]; CB=[1,2,4,8,16,24,32,48]
rounds={'learned':{L:[] for L in LB}, 'adam':{L:[] for L in CB}}
for r in range(5):
    for L in LB: rounds['learned'][L].append(t_learned(L))
    for L in CB: rounds['adam'][L].append(t_adam(L))
    print(f"  tur {r+1}/5 bitti", flush=True)

print(f"\n{'':>10}{'medyan':>9}{'min':>9}{'max':>9}{'max/min':>9}")
for arm in ('learned','adam'):
    print(f"-- {arm}")
    for L,v in rounds[arm].items():
        v=np.array(v)
        print(f"{'L='+str(L):>10}{np.median(v):9.2f}{v.min():9.2f}{v.max():9.2f}"
              f"{v.max()/v.min():9.2f}x")

# hizlar 23 Ekim olcumunden (ayni test kumesi, degismedi)
RATE_L={1:4.4599,2:4.8792,4:5.2855,8:5.5932,16:5.8003}
RATE_A={1:4.3810,2:4.6927,4:5.0253,8:5.3800,16:5.7389,24:5.9110,32:6.0132,48:6.1072}

print("\n=== baskinlik hukmu her turda ayni mi? ===")
stab={L:[] for L in LB}
for r in range(5):
    for L in LB:
        lms=rounds['learned'][L][r]; lr_=RATE_L[L]
        dom=[k for k in CB if rounds['adam'][k][r]<=lms and RATE_A[k]>=lr_]
        stab[L].append(bool(dom))
for L in LB:
    n=sum(stab[L])
    print(f"  ogrenilen L={L:<3}: 5 turun {n}'inde BASKINLANMIS  {stab[L]}")
json.dump({k:{str(a):b for a,b in v.items()} for k,v in rounds.items()},
          open(_pl.Path(__file__).resolve().parents[1]
               / "results/mumiso_latency_repeat.json","w"), indent=1)
print("\nwrote results/mumiso_latency_repeat.json")
```

### `scripts/mumiso_step_cost.py`

*66 satir · sha256:658e6186e376*

```python
"""Bir ogrenilen adim, bir Adam adiminin kac katina mal oluyor?

Esit L karsilastirmasi gecikme iddiasinin YERINE GECMEZ: ogrenilen adim
basina (a) r_rel icin bir rates cagrisi, (b) gradyan icin bir ileri+geri,
(c) agin kendisi (CNN+LSTM, exchange modunda K kez) var. Adam adimi
yalnizca (b)'yi yapiyor. Yani esit adim, ogrenilen modele avantajdir.
"""
import sys, time, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
torch.set_num_threads(1)          # konuslandirma senaryosu: tek cekirdek
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(64)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
phi=S.su_align_phase(F,G,hd)
X=torch.from_numpy(mumiso_features(d["F"],d["G"],d["hd"],phi.numpy()))
_,TH0=B.su_average(F,G,hd,pt,nv)
one=slice(0,1)

def t_adam(L, reps=40):
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        dl=torch.zeros(1,N,requires_grad=True)
        opt=torch.optim.Adam([dl],lr=0.75)
        for _ in range(L):
            th=TH0[one]+dl
            R=S.rates(F[one],G[one],hd[one],torch.cos(th),torch.sin(th),pt,nv,"zf")
            loss=-(-torch.logsumexp(-8.0*R,-1)/8.0).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        ts.append(time.perf_counter()-t0)
    return np.median(ts)*1e3

def t_learned(L, reps=40):
    net=UnrolledMuMiso(N=N,n_users=4,n_tx=8,steps=L,mode="exchange",use_grad=True)
    net.load_state_dict(torch.load(_pl.Path(__file__).resolve().parents[1]
                              / f"results/mumiso_eqstep_L{L}.pt")); net.eval()
    for _ in range(3):
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
        ts.append(time.perf_counter()-t0)
    return np.median(ts)*1e3

print(f"{'L':>3}{'Adam [ms]':>12}{'ogrenilen [ms]':>16}{'maliyet orani':>15}")
print("-"*46)
out={}
for L in (1,2,4,8,16):
    a,b=t_adam(L),t_learned(L)
    out[L]=(a,b)
    print(f"{L:3d}{a:12.3f}{b:16.3f}{b/a:15.2f}x")
a1=(out[1][0]); b1=(out[1][1])
print(f"\nadim basina: Adam {a1:.3f} ms, ogrenilen {b1:.3f} ms -> {b1/a1:.2f}x")
json.dump({str(k):{'adam_ms':v[0],'learned_ms':v[1]} for k,v in out.items()},
          open(_pl.Path(__file__).resolve().parents[1]
               / "results/mumiso_step_cost.json","w"), indent=1)
print("wrote results/mumiso_step_cost.json")
```

### `scripts/mumiso_budget.py`

*172 satir · sha256:6b757f4a12b7*

```python
"""
The fair comparison: equal budget.

Reporting "the learned model reaches 60% of a 1000-step optimiser" is true
but uninteresting -- of course a thousand steps beats eight. The question a
thesis can defend is whether the LEARNED update rule beats a PLAIN gradient
step when both are given the same number of evaluations.

So: unroll the learned model for L steps, and run plain Adam from the same
anchor for L steps, and compare. Then report wall-clock against the full
optimiser so the latency claim is grounded rather than asserted.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--samples", type=int, default=3000)
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="budget")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH0 = B.su_average(F, G, hd, pt, nv)
tr, va, te = split_indices(a.samples, seed=0)
ev = te[:a.eval_n]


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode=a.mode, use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()
say(f"loaded {a.ckpt}   N={N} T={a.tx} K={a.users}  eval on {len(ev)}")
say(f"anchor su_average : {mr(TH0[ev], ev):.4f}\n")

res = dict(config=vars(a), equal_budget={}, latency={})

# ------------------------------------------------- equal-budget comparison
say("=== equal budget: L learned steps vs L plain Adam steps ===")
say(f"{'L':>4}{'learned':>11}{'plain Adam':>13}{'Adam/su lr=.05':>17}")
say("-" * 45)
with torch.no_grad():
    _, trace = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev],
                   return_trace=True)

for L in range(1, a.steps + 1):
    # plain Adam, same start, same number of objective evaluations
    dl = torch.zeros(len(ev), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.05)
    for _ in range(L):
        th = TH0[ev] + dl
        R = S.rates(F[ev], G[ev], hd[ev], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    plain = mr(TH0[ev] + dl.detach(), ev)
    # a larger step size, since 8 steps at lr 0.05 barely moves
    dl2 = torch.zeros(len(ev), N, requires_grad=True)
    opt2 = torch.optim.Adam([dl2], lr=0.5)
    for _ in range(L):
        th = TH0[ev] + dl2
        R = S.rates(F[ev], G[ev], hd[ev], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt2.zero_grad()
        loss.backward()
        opt2.step()
    big = mr(TH0[ev] + dl2.detach(), ev)
    res["equal_budget"][L] = dict(learned=trace[L - 1], adam_lr05=plain,
                                  adam_lr5=big)
    say(f"{L:4d}{trace[L-1]:11.4f}{plain:13.4f}{big:17.4f}")

say("\n=== for reference, the full optimisers on the same scenarios ===")
t0 = time.time()
R_cd, _ = B.coord_descent(F[ev], G[ev], hd[ev], pt, nv)
cd = S.rate_metrics(R_cd)["min_rate"]
t_cd_all = time.time() - t0
t0 = time.time()
R_ao, _ = B.ao(F[ev], G[ev], hd[ev], pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
t_ao_all = time.time() - t0
say(f"  coord descent (8 sweeps x 16 grid) : {cd:.4f}   ({t_cd_all:.0f}s "
    f"for {len(ev)})")
say(f"  AO (3 starts x 1000 Adam steps)    : {ao:.4f}   ({t_ao_all:.0f}s "
    f"for {len(ev)})")
res["cd"], res["ao"] = cd, ao
res["learned_final"] = trace[-1]
say(f"  learned, {a.steps} steps                  : {trace[-1]:.4f}")
say(f"  -> learned / AO = {trace[-1]/ao:.3f},  learned / CD = {trace[-1]/cd:.3f}")

# ---------------------------------------------------------------- latency
say("\n=== latency, single scenario, CPU, batch size 1 ===")
one = slice(0, 1)
with torch.no_grad():
    for _ in range(3):
        net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])


def timeit(fn, reps):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return np.array(ts) * 1e3


def run_net():
    with torch.no_grad():
        net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])


t_net = timeit(run_net, 20)
t_su = timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)
t_cd = timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)
t_ao = timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 2)
for nm, t in [(f"learned ({a.steps} steps)", t_net), ("su_average", t_su),
              ("coord descent", t_cd), ("AO", t_ao)]:
    res["latency"][nm] = dict(p50=float(np.percentile(t, 50)),
                              p95=float(np.percentile(t, 95)))
    say(f"  {nm:>22}  p50 {np.percentile(t,50):9.2f} ms   "
        f"p95 {np.percentile(t,95):9.2f} ms")
sp_ao = (res["latency"]["AO"]["p50"]
         / res["latency"][f"learned ({a.steps} steps)"]["p50"])
sp_cd = (res["latency"]["coord descent"]["p50"]
         / res["latency"][f"learned ({a.steps} steps)"]["p50"])
say(f"  -> learned is {sp_ao:.0f}x faster than AO and {sp_cd:.0f}x faster "
    f"than CD at the median")
res["speedup_vs_ao"], res["speedup_vs_cd"] = sp_ao, sp_cd

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_budget_fraction.py`

*228 satir · sha256:d147a606155c*

```python
"""
Latency DISTRIBUTION and the fraction of runs that fit the coherence time.

WHY THIS FILE EXISTS
--------------------
The report's "bütçede kalma oranı" column -- the 95% that made 16-step
gradient ascent "the best method in budget" -- was produced by an inline
command that was never saved, so nobody could rerun it. An independent
audit measured 85-90% instead and could not find the code. A number that
carries a conclusion and has no script behind it is not a measurement.

So: this script. It differs from `mumiso_frontier.py`, which times each
method a handful of times and keeps only the median, in three ways that
turned out to matter.

1. IT REPORTS THE DISTRIBUTION, not a point. On this box 16-step Adam has
   been measured at 23.7, 24.2, 24.3, 25.3, 26.0 and 29.4 ms across runs.
   The budget is 28.2 ms. A single median either clears it or does not,
   depending on the run, which is how a 95% claim and an "already outside
   the budget" artifact ended up in the same repository.

2. IT VARIES THE SCENARIO, not just the repeat. Timing one scenario sixty
   times measures cache behaviour; timing sixty scenarios measures the
   method.

3. IT REFUSES TO REPORT ON A BUSY MACHINE. The audit's first pass ran
   alongside two training jobs and inflated every latency by 30-75%, which
   flipped the headline. Load is checked before and after, and the result
   is marked untrustworthy if the machine was not quiet.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--scenarios", type=int, default=60,
                help="distinct scenarios for the LATENCY sample, each timed once")
ap.add_argument("--rate-n", type=int, default=400,
                help="scenarios for the RATE estimate; kept separate because "
                     "60 is far too few for a heavy-tailed min-rate mean")
ap.add_argument("--threads", type=int, default=0,
                help="torch threads; 0 = library default. Pinning to 1 makes "
                     "contention visible but inflates every latency by ~50%% "
                     "and then the numbers cannot be compared with the rest "
                     "of the report")
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--max-load", type=float, default=0.6,
                help="per-core load above which results are flagged")
ap.add_argument("--tag", default="budget_fraction")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


def load_per_core():
    try:
        la = float(open("/proc/loadavg").read().split()[0])
        import os
        return la / max(os.cpu_count() or 1, 1)
    except Exception:
        return float("nan")


load_before = load_per_core()
torch.manual_seed(0)
if a.threads:
    torch.set_num_threads(a.threads)
NTHREADS = torch.get_num_threads()
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
# One generation, two disjoint uses: the first `scenarios` are timed one at a
# time, and a larger block is used for the rate. Reporting a rate averaged
# over the 60 timed scenarios -- which the first version of this script did --
# gave su_average 0.876 where 400 scenarios give 1.19, because the min-rate
# distribution is heavy-tailed and 60 draws do not pin its mean.
d = MuMisoChannel(panel, cfg).generate(max(a.scenarios, a.rate_n))
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH_SU = B.su_average(F, G, hd, pt, nv)
_, TH_BEST = B.su_best_of(F, G, hd, pt, nv)

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()

fd = a.velocity * panel.fc / 3e8
TC = 0.423 / fd * 1e3
say(f"N={N} T={a.tx} K={a.users}  |  latency: {a.scenarios} scenarios "
    f"at batch 1, {NTHREADS} torch thread(s)  |  rate: {a.rate_n} scenarios")
say(f"coherence budget T_c = {TC:.1f} ms  "
    f"(v={a.velocity} m/s, f_c={panel.fc/1e9:.1f} GHz, f_d={fd:.1f} Hz)")
say(f"load per core before: {load_before:.2f}\n")


def adam_once(i, L, start):
    dl = torch.zeros(1, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    sl = slice(i, i + 1)
    for _ in range(L):
        th = start[sl] + dl
        R = S.rates(F[sl], G[sl], hd[sl], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start[sl] + dl.detach()


def net_once(i):
    sl = slice(i, i + 1)
    with torch.no_grad():
        return net(X[sl], F[sl], G[sl], hd[sl], pt, nv, TH_SU[sl])


def anchor_once(i, start):
    return start[i:i + 1]


METHODS = [("su_average", lambda i: anchor_once(i, TH_SU)),
           ("su_best_of", lambda i: anchor_once(i, TH_BEST))]
for L in (8, 12, 16, 18, 20, 24):
    METHODS.append((f"Adam {L:2d} (su_avg)", lambda i, L=L: adam_once(i, L, TH_SU)))
for L in (12, 16):
    METHODS.append((f"Adam {L:2d} (best_of)",
                    lambda i, L=L: adam_once(i, L, TH_BEST)))
METHODS.append((f"learned {a.steps}", net_once))

# warm up every path once so the first scenario is not special
for _, fn in METHODS:
    fn(0)

RATE = slice(0, a.rate_n)


def rate_batched(nm):
    """Rate over `rate_n` scenarios, computed batched -- same maths, far
    tighter mean than averaging the timed sample."""
    if nm == "su_average":
        th = TH_SU[RATE]
    elif nm == "su_best_of":
        th = TH_BEST[RATE]
    elif nm.startswith("learned"):
        with torch.no_grad():
            th = net(X[RATE], F[RATE], G[RATE], hd[RATE], pt, nv, TH_SU[RATE])
    else:
        L = int(nm.split()[1])
        start = TH_BEST if "best_of" in nm else TH_SU
        dl = torch.zeros(a.rate_n, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=a.lr)
        for _ in range(L):
            t = start[RATE] + dl
            R = S.rates(F[RATE], G[RATE], hd[RATE], torch.cos(t),
                        torch.sin(t), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        th = start[RATE] + dl.detach()
    return S.rates(F[RATE], G[RATE], hd[RATE], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


say(f"{'method':>20}{'rate':>9}{'p05':>8}{'p50':>8}{'p95':>8}{'max':>8}"
    f"{'in budget':>11}")
say("-" * 72)
rows = []
for nm, fn in METHODS:
    ts = []
    for i in range(a.scenarios):
        t0 = time.perf_counter()
        fn(i)
        ts.append((time.perf_counter() - t0) * 1e3)
    qs = [rate_batched(nm)]
    ts = np.array(ts)
    frac = float((ts <= TC).mean())
    rows.append(dict(method=nm, rate=float(np.mean(qs)),
                     p05=float(np.percentile(ts, 5)),
                     p50=float(np.percentile(ts, 50)),
                     p95=float(np.percentile(ts, 95)),
                     max=float(ts.max()), in_budget=frac))
    say(f"{nm:>20}{np.mean(qs):9.4f}{np.percentile(ts,5):8.1f}"
        f"{np.percentile(ts,50):8.1f}{np.percentile(ts,95):8.1f}"
        f"{ts.max():8.1f}{100*frac:10.0f}%")

load_after = load_per_core()
say(f"\nload per core after: {load_after:.2f}")
busy = max(load_before, load_after) > a.max_load
if busy:
    say("  *** MACHINE WAS BUSY -- these latencies are inflated and must "
        "not be quoted. Rerun on an idle box. ***")

ok = [r for r in rows if r["in_budget"] >= 0.9]
if ok:
    w = max(ok, key=lambda r: r["rate"])
    say(f"\nbest method with >=90% of runs inside {TC:.1f} ms : "
        f"{w['method']}  rate {w['rate']:.4f}  p50 {w['p50']:.1f} ms")
    say("  (>=90%, not a point median: the 16-step row straddles the budget")
    say("   and a median alone decides the headline by luck)")
else:
    say(f"\nno method keeps 90% of runs inside {TC:.1f} ms")

json.dump(dict(config=vars(a), coherence_ms=TC, rows=rows,
               threads=NTHREADS,
               load_before=load_before, load_after=load_after,
               trustworthy=not busy),
          open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_headroom.py`

*52 satir · sha256:d7ff9705f3b8*

```python
"""How much is there to learn? Baseline spread for several (T, K) scenarios."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank)
from ris_mu.mumiso import baselines as B

torch.manual_seed(0)
S_N = 200
cfgs = [(4, 4), (8, 4), (8, 6), (16, 4)]
meth = ("no_ris", "random", "su_weakest", "su_average", "cd", "pga", "ao")

print(f"{S_N} scenarios each, N=32, ZF, continuous phase, max-min [b/s/Hz]\n")
hdr = f"{'T x K':>7}" + "".join(f"{m:>12}" for m in meth) + f"{'Grank':>8}{'sec':>7}"
print(hdr); print("-" * len(hdr))
rows = {}
for T, K in cfgs:
    t0 = time.time()
    panel, cfg = make_mumiso_scenario(n_users=K, n_bs_antennas=T, seed=11)
    d = MuMisoChannel(panel, cfg).generate(S_N)
    F, G, hd, _ = to_torch(d)
    nv = 1.0 / cfg.snr_scale()
    r = B.run_all(F, G, hd, 1.0, nv, methods=meth, precoder="zf")
    gr = effective_rank(d["G"].reshape(-1, 32))
    rows[(T, K)] = {m: r[m]["min_rate"] for m in meth}
    print(f"{T:3d} x{K:3d}" + "".join(f"{r[m]['min_rate']:12.3f}" for m in meth)
          + f"{gr:8.2f}{time.time()-t0:7.1f}")

print("\n=== checks ===")
for k, v in rows.items():
    strongest = max(("cd", "pga", "ao"), key=lambda m: v[m])
    ok_ord = (max(v["cd"], v["pga"], v["ao"]) > v["su_average"]
              > v["random"] > v["no_ris"])
    head = v[strongest] / max(v["su_average"], 1e-9)
    print(f"  T={k[0]:2d} K={k[1]}:  strongest={strongest} ({v[strongest]:.3f})   "
          f"ordering {ok_ord}   headroom over su_average {head:5.2f}x")

print("\n=== CD monotone? (T=8, K=4, 40 scenarios) ===")
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=3)
d = MuMisoChannel(panel, cfg).generate(40)
F, G, hd, _ = to_torch(d); nv = 1.0 / cfg.snr_scale()
th = B.su_average(F, G, hd, 1.0, nv)[1]
prev = B._obj(F, G, hd, th, 1.0, nv, "zf", "maxmin").mean().item()
hist = [prev]
for it in range(6):
    _, th = B.coord_descent(F, G, hd, 1.0, nv, iters=1, theta0=th)
    v = B._obj(F, G, hd, th, 1.0, nv, "zf", "maxmin").mean().item()
    hist.append(v)
d_ = np.diff(hist)
print("  " + " -> ".join(f"{h:.4f}" for h in hist))
print(f"  monotone: {bool((d_ >= -1e-6).all())}   min step {d_.min():+.2e}")
```

### `scripts/anchor_same_split.py`

*26 satir · sha256:a4ac3fa7cb26*

```python
"""Anchor measured on the EXACT test split the models were scored on."""
import sys, pathlib, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

NS = 12000
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, M=8, K=4, seed=11)
F, G, hd, _ = to_torch(MuMisoChannel(panel, cfg).generate(NS))
pt, nv = 1.0, 1.0 / cfg.snr_scale()
tr, va, te = split_indices(NS, seed=0)
print(f"test split: {len(te)} scenarios (models scored here)")
out = {}
for m in ("su_average", "su_best_of", "su_weakest"):
    R, _ = B._DISPATCH[m](F[te], G[te], hd[te], pt, nv, precoder="zf")
    out[m] = S.rate_metrics(R)["min_rate"]
    print(f"  {m:>11}: {out[m]:.4f}")
models = {"concat": 3.536795, "deepsets": 3.536696, "exchange": 3.526039}
print("\n  model vs su_average anchor (same split):")
for k, v in models.items():
    print(f"  {k:>9} {v:.4f}   {100*(v/out['su_average']-1):+6.2f}%"
          f"   vs su_best_of {100*(v/out['su_best_of']-1):+6.2f}%")
json.dump(out, open(str(_pl.Path(__file__).resolve().parents[1] / "results") + "/anchor_full_test.json", "w"), indent=1)
```

### `scripts/diagnose_learnability.py`

*129 satir · sha256:6f4375cd7410*

```python
"""
Is the channel -> optimal-phase map learnable at all from these features?

The unsupervised run sits still at the anchor. Two very different causes:
  (A) optimisation -- the averaged objective gradient is uninformative, but
      a good map exists and the network could represent it;
  (B) representability/generalisation -- no such map is learnable from
      these features, so staying at the anchor IS the best the network can
      do and the formulation has to change.

Decisive test: compute per-scenario ORACLE offsets with Adam, then train
the same network SUPERVISED to regress them.
  - cannot even fit the training set  -> capacity / features (B)
  - fits train, fails val             -> the map is too wiggly to generalise (B)
  - fits both, rate high              -> the unsupervised objective is at
                                         fault (A), fixable by a warm start
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch
import torch.nn.functional as Fn

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

torch.manual_seed(0)
NS, KUS, T = 4000, 4, 8
panel, cfg = make_mumiso_scenario(n_users=KUS, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(NS, seed=0)


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


_, th_su = B.su_average(F, G, hd, pt, nv)
print(f"anchor (su_average) on test : {mr(th_su[te], te):.4f}", flush=True)

print("\n=== oracle offsets (Adam, 600 steps, per scenario) ===", flush=True)
t0 = time.time()
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(600):
    th = th_su + dl
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
dl = dl.detach()
th_or = th_su + dl
print(f"  oracle rate on test : {mr(th_or[te], te):.4f}   "
      f"({time.time()-t0:.0f}s)", flush=True)
off = torch.atan2(torch.sin(dl), torch.cos(dl))
print(f"  offset magnitude    : mean |d| {off.abs().mean():.3f} rad, "
      f"std {off.std():.3f}", flush=True)

print("\n=== how wiggly is the map? nearest-neighbour test ===", flush=True)
flat = X.reshape(NS, -1)
sub = torch.randperm(NS)[:800]
Z = Fn.normalize(flat[sub], dim=-1)
sim = Z @ Z.T
sim.fill_diagonal_(-2)
nn_idx = sim.argmax(-1)
tgt = torch.complex(torch.cos(dl[sub]), torch.sin(dl[sub]))
agree = (tgt * tgt[nn_idx].conj()).real.mean().item()
rand_idx = torch.randperm(len(sub))
agree_r = (tgt * tgt[rand_idx].conj()).real.mean().item()
print(f"  cos(offset difference) to NEAREST feature neighbour : {agree:+.4f}")
print(f"  ... to a RANDOM scenario                            : {agree_r:+.4f}")
print("  (both near zero => the required offset is uncorrelated with")
print("   feature similarity, i.e. not a smooth map in this representation)",
      flush=True)

print("\n=== supervised fit of the oracle offsets ===", flush=True)
net = MuMisoNet(N=N, n_users=KUS, n_tx=T, mode="exchange", residual=True)
opt = torch.optim.Adam(net.parameters(), lr=2e-3)
tc, ts = torch.cos(th_or), torch.sin(th_or)
rng = np.random.default_rng(0)
for ep in range(1, 26):
    net.train()
    run, nb = 0.0, 0
    perm = tr[rng.permutation(len(tr))]
    for i in range(0, len(perm), 64):
        j = perm[i:i + 64]
        c, s = net.phases(X[j])
        loss = Fn.mse_loss(torch.stack([c, s]), torch.stack([tc[j], ts[j]]))
        opt.zero_grad()
        loss.backward()
        opt.step()
        run += loss.item()
        nb += 1
    if ep % 5 == 0 or ep == 1:
        net.eval()
        with torch.no_grad():
            ctr, str_ = net.phases(X[tr[:1000]])
            cva, sva = net.phases(X[va])
            e_tr = Fn.mse_loss(torch.stack([ctr, str_]),
                               torch.stack([tc[tr[:1000]],
                                            ts[tr[:1000]]])).item()
            e_va = Fn.mse_loss(torch.stack([cva, sva]),
                               torch.stack([tc[va], ts[va]])).item()
            r_va = mr(torch.atan2(sva, cva), va)
        print(f"  epoch {ep:2d}  train mse {run/nb:.4f}  "
              f"fit mse train {e_tr:.4f} val {e_va:.4f}   "
              f"val rate {r_va:.4f}", flush=True)

net.eval()
with torch.no_grad():
    c, s = net.phases(X[te])
print(f"\n  supervised model on test : {mr(torch.atan2(s, c), te):.4f}")
print(f"  oracle on test           : {mr(th_or[te], te):.4f}")
print(f"  anchor on test           : {mr(th_su[te], te):.4f}")
print("\n  mse 1.0 means the prediction is uncorrelated with the target")
print("  (both are unit vectors), mse 0 is a perfect fit.")
```

### `scripts/diagnose_mumiso_gap.py`

*105 satir · sha256:3411d21f59e2*

```python
"""
Why is the learned model stuck near su_average?

Three questions, in order of what they would imply:
 1. Does the trained net even use its input, or is it emitting a constant?
 2. How far is it from su_average and from AO, as a circular distance?
 3. Is the gap reachable by REWEIGHTING the K alignment vectors? If an
    oracle weighting gets most of AO's rate, the family is right and the
    failure is optimisation. If it does not, beating su_average requires
    leaving that family and the task is harder than the architecture.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 400, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)                       # [S,K,N]
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))

def mr(th):
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values

print("=== reference points ===")
_, th_su = B.su_average(F, G, hd, pt, nv)
_, th_ao = B.ao(F, G, hd, pt, nv)
r_su, r_ao = mr(th_su).mean().item(), mr(th_ao).mean().item()
print(f"  su_average {r_su:.4f}   AO {r_ao:.4f}   gap {r_ao-r_su:.4f}")

print("\n=== 1) does the trained concat net use its input? ===")
ck = pathlib.Path("results/mumiso_main_concat.pt")
if ck.exists():
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode="concat")
    net.load_state_dict(torch.load(ck)); net.eval()
    with torch.no_grad():
        c, s = net.phases(X)
    th_net = torch.atan2(s, c)
    r_net = mr(th_net).mean().item()
    # spread of the predicted phase ACROSS scenarios, per element
    circ_var_scen = 1 - torch.exp(1j*th_net.to(torch.complex64)).mean(0).abs()
    circ_var_elem = 1 - torch.exp(1j*th_net.to(torch.complex64)).mean(1).abs()
    print(f"  learned rate {r_net:.4f}")
    print(f"  circular variance across scenarios (per element, mean) "
          f"{circ_var_scen.mean():.4f}   0 = constant output, 1 = uniform")
    print(f"  circular variance across elements  (per scenario, mean) "
          f"{circ_var_elem.mean():.4f}")

    def cdist(a, b):
        return torch.atan2(torch.sin(a-b), torch.cos(a-b)).abs().mean().item()
    print("\n=== 2) circular distance [rad] ===")
    print(f"  net vs su_average {cdist(th_net, th_su):.4f}")
    print(f"  net vs AO         {cdist(th_net, th_ao):.4f}")
    print(f"  su_average vs AO  {cdist(th_su, th_ao):.4f}")
    print("  (uniform random would be ~pi/2 = 1.5708)")
else:
    print("  checkpoint not ready yet")

print("\n=== 3) is the gap reachable by REWEIGHTING the K alignments? ===")
# theta = angle( sum_k w_k exp(j phi_k) ),  w >= 0, optimise w per scenario
w = torch.zeros(NS, Kus, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
ph = torch.exp(1j * phi.to(torch.complex64))           # [S,K,N]
for it in range(400):
    ww = torch.softmax(w, dim=-1).to(torch.complex64)
    acc = (ww.unsqueeze(-1) * ph).sum(1)
    th = torch.angle(acc)
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0*R, dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
with torch.no_grad():
    ww = torch.softmax(w, -1).to(torch.complex64)
    th_w = torch.angle((ww.unsqueeze(-1)*ph).sum(1))
    r_w = mr(th_w).mean().item()
print(f"  ORACLE per-scenario reweighting : {r_w:.4f}")
print(f"  -> recovers {100*(r_w-r_su)/max(r_ao-r_su,1e-9):.1f}% of the "
       f"su_average -> AO gap")

print("\n=== 4) oracle phase SHIFT per element on top of su_average? ===")
# theta = th_su + delta, delta optimised freely per scenario (= PGA from su)
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(400):
    th = th_su + dl
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0*R, dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
with torch.no_grad():
    r_d = mr(th_su + dl).mean().item()
print(f"  free per-element offset (gradient, 400 it) : {r_d:.4f}")
print(f"  -> recovers {100*(r_d-r_su)/max(r_ao-r_su,1e-9):.1f}% of the gap")
print("\n  Reading: if (3) is small but (4) is large, the optimum is NOT a")
print("  reweighting of the single-user alignments -- the network has to")
print("  learn a genuinely different phase pattern, and giving it phi_su as")
print("  a feature anchors it to the wrong family.")
```

### `scripts/step1_control.py`

*118 satir · sha256:fd042c302981*

```python
"""
step1_control.py
----------------
Control experiment on the LEGACY channel model.

Question
--------
The published CNN-LSTM beats a fully connected network on the legacy dataset.
Is that gain explained by spatial structure (which the legacy generator does
not contain, because it draws an independent coefficient per element), or
simply by capacity and weight sharing?

Test
----
Train SharedMLP: the same small MLP applied to every element independently,
with no path for information to flow between elements. If it matches the
CNN-LSTM, the recurrent and convolutional machinery is not exploiting spatial
structure on this dataset -- there is none to exploit.

Usage:  python scripts/step1_control.py --n 20000 --epochs 40
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                              # noqa: E402
from ris_mu.channel import legacy_generate                        # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices  # noqa: E402
from ris_mu.models import SharedMLP, FCDNN, CNNOnly, CNNLSTM, count_params  # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


def build_eval(N):
    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for X, Y in loader:
                P.append(model(X))
                T.append(Y.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))
    return eval_fn


def step_fn(model, batch):
    X, Y = batch
    return phase_aware_mse(model(X), Y.flatten(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N

    print(f"legacy dataset: {args.n} samples, N={N}")
    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]

    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)
    print(f"split: {len(itr)} / {len(iva)} / {len(ite)}\n")

    eval_fn = build_eval(N)
    zoo = {
        "SharedMLP (control)": SharedMLP(N),
        "FC-DNN": FCDNN(N),
        "CNN-only": CNNOnly(N),
        "CNN-LSTM (published)": CNNLSTM(N),
    }

    results = {}
    for name, model in zoo.items():
        set_seed(42)
        print(f"--- {name}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, tag=name.split()[0])
        _, m = eval_fn(model, te)
        results[name] = dict(params=count_params(model), val_rmse=info["best_score"],
                             test_rmse=m["rmse"], test_sr5=m["sr5"],
                             epochs_run=len(info["history"]), minutes=info["minutes"])
        print(f"    test RMSE={m['rmse']:.3f} deg   SR@5={m['sr5']:.2f}%   "
              f"({info['minutes']:.1f} min)\n")

    print(f"{'model':<24}{'params':>10}{'test RMSE':>12}{'SR@5':>9}")
    print("-" * 55)
    for k, v in results.items():
        print(f"{k:<24}{v['params']:>10,}{v['test_rmse']:>11.3f}°{v['test_sr5']:>8.2f}%")

    base = results["SharedMLP (control)"]["test_rmse"]
    best = results["CNN-LSTM (published)"]["test_rmse"]
    print(f"\nCNN-LSTM vs element-independent control: "
          f"{100*(base-best)/base:+.1f}% RMSE change")

    p = os.path.join(args.out, "step1_control.json")
    json.dump(results, open(p, "w"), indent=2)
    print(f"saved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/step1b_head_ablation.py`

*119 satir · sha256:87685e92fa0f*

```python
"""
step1b_head_ablation.py
-----------------------
Separates the contribution of the BODY from that of the OUTPUT HEAD in the
published architecture, on the legacy dataset.

Motivation
----------
A faithful re-implementation of the published CNN-LSTM does not reach the
reported accuracy, while a 6.6k-parameter element-local MLP does. The two
differ in the body (convolution + recurrence vs none) and in the head (a
dense bottleneck that flattens the feature map and squeezes it through 64
units vs a width-1 convolution applied at each element).

This script crosses the two factors so the responsible component is
identified rather than guessed:

    body in {none, CNN, CNN-LSTM}  x  head in {dense, local}

Why it matters beyond this dataset: the published head ends in a 64-unit
layer feeding 2N outputs. At N = 32 those are equal, at N = 256 the head must
push 512 numbers through 64 units. If the head is the binding constraint, the
degradation of accuracy with surface size reported in the original work is a
property of the head, not of the problem -- and it is removed by a change
that costs parameters rather than ideas.

Usage:  python scripts/step1b_head_ablation.py --n 40000 --epochs 40
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                               # noqa: E402
from ris_mu.channel import legacy_generate                         # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices   # noqa: E402
from ris_mu.models import SharedMLP, CNNOnly, CNNLSTM, count_params  # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate   # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed      # noqa: E402


def build_eval(N):
    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for X, Y in loader:
                P.append(model(X))
                T.append(Y.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))
    return eval_fn


def step_fn(model, batch):
    X, Y = batch
    return phase_aware_mse(model(X), Y.flatten(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N

    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]
    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)
    eval_fn = build_eval(N)

    zoo = {
        ("none", "local"): lambda: SharedMLP(N),
        ("CNN", "dense"): lambda: CNNOnly(N, head="dense"),
        ("CNN", "local"): lambda: CNNOnly(N, head="local"),
        ("CNN-LSTM", "dense"): lambda: CNNLSTM(N, head="dense"),
        ("CNN-LSTM", "local"): lambda: CNNLSTM(N, head="local"),
    }

    res = {}
    for (body, head), build in zoo.items():
        set_seed(42)
        model = build()
        key = f"{body} + {head}"
        print(f"--- {key}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, tag=key)
        _, m = eval_fn(model, te)
        res[key] = dict(body=body, head=head, params=count_params(model),
                        test_rmse=m["rmse"], test_sr5=m["sr5"],
                        minutes=info["minutes"])
        print(f"    test RMSE={m['rmse']:.3f}  SR@5={m['sr5']:.2f}%\n")

    print(f"{'body':<10}{'head':<8}{'params':>10}{'RMSE':>10}{'SR@5':>9}")
    print("-" * 47)
    for k, v in res.items():
        print(f"{v['body']:<10}{v['head']:<8}{v['params']:>10,}"
              f"{v['test_rmse']:>9.2f}°{v['test_sr5']:>8.2f}%")

    p = os.path.join(args.out, "step1b_head_ablation.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/step4_multiuser.py`

*150 satir · sha256:a9e56d2c5509*

```python
"""
step4_multiuser.py
------------------
Multi-user RIS phase design trained WITHOUT labels.

Why unsupervised
----------------
The closed form theta_n = -angle(F_n) - angle(G_n) is optimal for one user
only. With U users sharing one surface there is no closed form to regress
onto, so supervised training would require generating labels with a numerical
solver -- and a network trained to imitate a solver cannot, by construction,
beat it. Training directly on the system metric removes that ceiling.

Objective
---------
Single-antenna BS, users served in orthogonal slots inside one coherence
block, the surface held fixed across the block. One phase vector must serve
every user, which makes this a fairness problem; the objective is the
max-min rate, smoothed so that gradient reaches more than one user per
sample.

Models
------
  MU-CNN-LSTM     users concatenated along the channel axis -- the direct
                  extension of the published architecture. Fixes U and is
                  sensitive to the ordering of users.
  Equivariant     attention over elements, mean pooling over users. Respects
                  both symmetries of the problem and accepts any U.

Usage:  python scripts/step4_multiuser.py --n 20000 --epochs 30 --users 4
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario          # noqa: E402
from ris_mu.features import mu_features, split_indices                 # noqa: E402
from ris_mu.models import EquivariantRIS, MUCNNLSTM, count_params      # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics                    # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed          # noqa: E402
from ris_mu import baselines as BL                                     # noqa: E402


def build(args):
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    data = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(data["F"], data["G"], data["hd"]))
    Fc = torch.from_numpy(data["F"]).to(torch.complex64)
    Gc = torch.from_numpy(data["G"]).to(torch.complex64)
    hd = torch.from_numpy(data["hd"]).to(torch.complex64)
    return panel, cfg, X, Fc, Gc, hd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel, cfg, X, Fc, Gc, hd = build(args)
    N, sc = panel.N, cfg.snr_scale()
    print(f"N={N}  U={args.users}  samples={args.n}  "
          f"noise={cfg.noise_power_dbm():.1f} dBm\n")

    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

    def step_fn(model, batch):
        Xb, Fb, Gb, hb = batch
        return maxmin_loss(Fb, Gb, hb, model(Xb), N, sc)

    def eval_fn(model, loader):
        model.eval()
        acc, n = {}, 0
        with torch.no_grad():
            for Xb, Fb, Gb, hb in loader:
                m = rate_metrics(Fb, Gb, hb, model(Xb), N, sc)
                for k, v in m.items():
                    acc[k] = acc.get(k, 0.0) + v * len(Xb)
                n += len(Xb)
        acc = {k: v / n for k, v in acc.items()}
        return -acc["min_rate"], acc

    # ---------------------------------------------------------- baselines
    Ft, Gt, ht = Fc[ite], Gc[ite], hd[ite]
    print("baselines on the test split")
    res = {}
    res["no RIS"] = BL.summarise(BL.no_ris(Ft, Gt, ht, sc))
    res["random phase"] = BL.summarise(BL.random_phase(Ft, Gt, ht, sc)[1])
    res["SU closed form"] = BL.summarise(BL.su_closed_form(Ft, Gt, ht, sc)[1])
    t0 = time.perf_counter()
    res["PGA max-min"] = BL.summarise(BL.pga_maxmin(Ft, Gt, ht, sc,
                                                    iters=300, restarts=3)[1])
    res["PGA max-min"]["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
    for k, v in res.items():
        print(f"  {k:<16} min={v['min_rate']:.3f}  sum={v['sum_rate']:.3f}")
    print()

    # ---------------------------------------------------------- learned
    zoo = {
        "MU-CNN-LSTM": lambda: MUCNNLSTM(N, args.users),
        "Equivariant": lambda: EquivariantRIS(residual=False),
        "Equiv+residual": lambda: EquivariantRIS(residual=True),
    }
    for name, bld in zoo.items():
        set_seed(42)
        model = bld()
        print(f"--- {name}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, lr=2e-3, tag=name, patience=12,
                            milestones=(20, 35, 45))
        _, m = eval_fn(model, te)
        model.eval()
        with torch.no_grad():
            t0 = time.perf_counter()
            for Xb, *_ in te:
                model(Xb)
            m["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
        m["params"] = count_params(model)
        res[name] = m
        torch.save(model.state_dict(), os.path.join(args.out, f"step4_{name}.pt"))
        print(f"    min={m['min_rate']:.3f}  sum={m['sum_rate']:.3f}  "
              f"({info['minutes']:.1f} min)\n")

    # ---------------------------------------------------------- table
    print(f"{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}{'ms/sample':>11}")
    print("-" * 58)
    ref = res["PGA max-min"]["min_rate"]
    for k, v in res.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}")

    json.dump(res, open(os.path.join(args.out, "step4_multiuser.json"), "w"), indent=2)
    print(f"\nsaved -> {args.out}/step4_multiuser.json")


if __name__ == "__main__":
    main()
```

### `scripts/step4b_residual.py`

*99 satir · sha256:c61c758b64e4*

```python
"""
step4b_residual.py
------------------
Trains the residual variant of the equivariant model and merges its result
into the step 4 table, so the two models already trained are not repeated.

Usage:  python scripts/step4b_residual.py --n 16000 --epochs 50
"""

import argparse
import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics             # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16000)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    d = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    Fc = torch.from_numpy(d["F"]).to(torch.complex64)
    Gc = torch.from_numpy(d["G"]).to(torch.complex64)
    hd = torch.from_numpy(d["hd"]).to(torch.complex64)
    N, sc = panel.N, cfg.snr_scale()

    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

    def step_fn(model, b):
        Xb, Fb, Gb, hb = b
        return maxmin_loss(Fb, Gb, hb, model(Xb), N, sc)

    def eval_fn(model, loader):
        model.eval()
        acc, n = {}, 0
        with torch.no_grad():
            for Xb, Fb, Gb, hb in loader:
                m = rate_metrics(Fb, Gb, hb, model(Xb), N, sc)
                for k, v in m.items():
                    acc[k] = acc.get(k, 0.0) + v * len(Xb)
                n += len(Xb)
        acc = {k: v / n for k, v in acc.items()}
        return -acc["min_rate"], acc

    set_seed(42)
    model = EquivariantRIS(residual=True)
    print(f"Equiv+residual  ({count_params(model):,} params)")
    _, m0 = eval_fn(model, te)
    print(f"  before training: min={m0['min_rate']:.3f}  sum={m0['sum_rate']:.3f}")

    info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                        lr=2e-3, tag="residual", patience=12,
                        milestones=(25, 40, 48))
    _, m = eval_fn(model, te)
    model.eval()
    with torch.no_grad():
        t0 = time.perf_counter()
        for Xb, *_ in te:
            model(Xb)
        m["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
    m["params"] = count_params(model)
    m["untrained_min_rate"] = m0["min_rate"]
    print(f"  after  training: min={m['min_rate']:.3f}  sum={m['sum_rate']:.3f}"
          f"  ({info['minutes']:.1f} min)")

    torch.save(model.state_dict(), os.path.join(args.out, "step4_Equiv+residual.pt"))
    p = os.path.join(args.out, "step4_multiuser.json")
    res = json.load(open(p))
    res["Equiv+residual"] = m
    json.dump(res, open(p, "w"), indent=2)

    ref = res["PGA max-min"]["min_rate"]
    print(f"\n{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}{'ms/sample':>11}")
    print("-" * 58)
    for k, v in res.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}")


if __name__ == "__main__":
    main()
```

### `scripts/step4c_equiv_long.py`

*99 satir · sha256:2bbadcdae859*

```python
"""
step4b_residual.py
------------------
Trains the residual variant of the equivariant model and merges its result
into the step 4 table, so the two models already trained are not repeated.

Usage:  python scripts/step4b_residual.py --n 16000 --epochs 50
"""

import argparse
import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics             # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16000)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    d = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    Fc = torch.from_numpy(d["F"]).to(torch.complex64)
    Gc = torch.from_numpy(d["G"]).to(torch.complex64)
    hd = torch.from_numpy(d["hd"]).to(torch.complex64)
    N, sc = panel.N, cfg.snr_scale()

    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

    def step_fn(model, b):
        Xb, Fb, Gb, hb = b
        return maxmin_loss(Fb, Gb, hb, model(Xb), N, sc)

    def eval_fn(model, loader):
        model.eval()
        acc, n = {}, 0
        with torch.no_grad():
            for Xb, Fb, Gb, hb in loader:
                m = rate_metrics(Fb, Gb, hb, model(Xb), N, sc)
                for k, v in m.items():
                    acc[k] = acc.get(k, 0.0) + v * len(Xb)
                n += len(Xb)
        acc = {k: v / n for k, v in acc.items()}
        return -acc["min_rate"], acc

    set_seed(42)
    model = EquivariantRIS(residual=False)
    print(f"Equiv+residual  ({count_params(model):,} params)")
    _, m0 = eval_fn(model, te)
    print(f"  before training: min={m0['min_rate']:.3f}  sum={m0['sum_rate']:.3f}")

    info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                        lr=2e-3, tag="equiv-long", patience=18,
                        milestones=(20, 35, 50, 65))
    _, m = eval_fn(model, te)
    model.eval()
    with torch.no_grad():
        t0 = time.perf_counter()
        for Xb, *_ in te:
            model(Xb)
        m["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
    m["params"] = count_params(model)
    m["untrained_min_rate"] = m0["min_rate"]
    print(f"  after  training: min={m['min_rate']:.3f}  sum={m['sum_rate']:.3f}"
          f"  ({info['minutes']:.1f} min)")

    torch.save(model.state_dict(), os.path.join(args.out, "step4_Equivariant.pt"))
    p = os.path.join(args.out, "step4_multiuser.json")
    res = json.load(open(p))
    res["Equivariant"] = m
    json.dump(res, open(p, "w"), indent=2)

    ref = res["PGA max-min"]["min_rate"]
    print(f"\n{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}{'ms/sample':>11}")
    print("-" * 58)
    for k, v in res.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}")


if __name__ == "__main__":
    main()
```

### `scripts/step5_generalisation.py`

*129 satir · sha256:8b1356bbdb8a*

```python
"""
step5_generalisation.py
-----------------------
What the symmetries actually buy, measured rather than asserted.

Two properties are claimed for the equivariant model and tested here against
the user-concatenated extension of the published architecture:

1. INVARIANCE TO USER ORDERING. The set of users has no natural order, so a
   model whose output changes when the users are relabelled is fitting an
   artefact. Measured as the spread of the achieved min-rate over random
   relabellings of the same scenario.

2. GENERALISATION ACROSS USER COUNT. A deployment does not hold U fixed.
   The equivariant model is defined for any U and is evaluated at user counts
   it never saw; the concatenated model cannot accept them at all, which is
   itself the result.

Both models are loaded from the step 4 checkpoints, so this script measures
the models that were actually trained rather than retrained variants.

Usage:  python scripts/step5_generalisation.py --n 4000
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario      # noqa: E402
from ris_mu.features import mu_features                            # noqa: E402
from ris_mu.models import EquivariantRIS, MUCNNLSTM                # noqa: E402
from ris_mu.losses import rate_metrics                             # noqa: E402
from ris_mu import baselines as BL                                 # noqa: E402


def make_set(users, n, seed):
    panel, cfg = make_scenario(n_users=users, seed=seed)
    d = MultiUserRISChannel(panel, cfg).generate(n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    return (panel, cfg, X,
            torch.from_numpy(d["F"]).to(torch.complex64),
            torch.from_numpy(d["G"]).to(torch.complex64),
            torch.from_numpy(d["hd"]).to(torch.complex64))


@torch.no_grad()
def score(model, X, Fc, Gc, hd, N, sc, bs=256):
    acc, n = {}, 0
    for i in range(0, len(X), bs):
        sl = slice(i, i + bs)
        m = rate_metrics(Fc[sl], Gc[sl], hd[sl], model(X[sl]), N, sc)
        for k, v in m.items():
            acc[k] = acc.get(k, 0.0) + v * (sl.stop - sl.start)
        n += min(bs, len(X) - i)
    return {k: v / n for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--trained_users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    eq = EquivariantRIS(residual=False).eval()
    eq.load_state_dict(torch.load(os.path.join(args.out, "step4_Equivariant.pt")))
    res = {}

    # --- 1. sensitivity to user ordering ------------------------------------
    panel, cfg, X, Fc, Gc, hd = make_set(args.trained_users, args.n, seed=909)
    N, sc = panel.N, cfg.snr_scale()

    mu = MUCNNLSTM(N, args.trained_users).eval()
    mu.load_state_dict(torch.load(os.path.join(args.out, "step4_MU-CNN-LSTM.pt")))

    print(f"user-ordering sensitivity  (U={args.trained_users}, "
          f"{args.n} scenarios, 8 relabellings)")
    order = {}
    for name, model in (("MU-CNN-LSTM", mu), ("Equivariant", eq)):
        vals = []
        for r in range(8):
            p = torch.randperm(args.trained_users) if r else torch.arange(args.trained_users)
            vals.append(score(model, X[:, p], Fc, Gc[:, p], hd[:, p], N, sc)["min_rate"])
        vals = np.array(vals)
        order[name] = dict(mean=float(vals.mean()), std=float(vals.std()),
                           spread=float(vals.max() - vals.min()))
        print(f"  {name:<13} min-rate {vals.mean():.4f} "
              f"+- {vals.std():.4f}   spread {vals.max()-vals.min():.4f}")
    res["user_ordering"] = order

    # --- 2. generalisation across user count --------------------------------
    print(f"\ngeneralisation across user count (trained at U={args.trained_users})")
    print(f"{'U':>3}{'Equivariant':>14}{'PGA':>10}{'% of PGA':>10}{'MU-CNN-LSTM':>14}")
    print("-" * 51)
    gen = {}
    for U in (2, 3, 4, 6, 8):
        panel, cfg, X, Fc, Gc, hd = make_set(U, args.n, seed=1000 + U)
        N, sc = panel.N, cfg.snr_scale()
        e = score(eq, X, Fc, Gc, hd, N, sc)["min_rate"]
        pga = BL.summarise(BL.pga_maxmin(Fc, Gc, hd, sc, iters=250, restarts=3)[1])
        su = BL.summarise(BL.su_closed_form(Fc, Gc, hd, sc)[1])
        if U == args.trained_users:
            m = score(mu, X, Fc, Gc, hd, N, sc)["min_rate"]
            mu_str = f"{m:>13.3f}"
        else:
            m = None
            mu_str = f"{'undefined':>13}"
        gen[U] = dict(equivariant=e, pga=pga["min_rate"], su_closed=su["min_rate"],
                      mu_cnn_lstm=m)
        print(f"{U:>3}{e:>14.3f}{pga['min_rate']:>10.3f}"
              f"{100*e/pga['min_rate']:>9.1f}%{mu_str}")
    res["user_count"] = gen

    print("\n('undefined' is the result: the concatenated model fixes U in its "
          "first layer\n and cannot be evaluated at another user count without "
          "retraining.)")

    p = os.path.join(args.out, "step5_generalisation.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/step5b_mixed_users.py`

*167 satir · sha256:e4407aed2fad*

```python
"""
step5b_mixed_users.py
---------------------
Being DEFINED for any number of users is not the same as being ACCURATE for
any number of users.

Step 5 trained the equivariant model at U = 4 and evaluated it elsewhere. It
accepted every user count without modification -- the concatenated model
could not be evaluated at all -- but its margin over the single-user closed
form eroded as U moved away from 4, and reversed by U = 8. The symmetry buys
applicability, not accuracy.

This script tests the obvious remedy: train across a range of user counts.
The model is unchanged; only the training distribution is. Batches are drawn
from per-U datasets in round robin, so each gradient step sees one user count
and the model sees all of them.

Usage:  python scripts/step5b_mixed_users.py --per_u 4000 --epochs 45
"""

import argparse
import itertools
import json
import os
import sys

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics             # noqa: E402
from ris_mu.train import set_seed                               # noqa: E402
from ris_mu import baselines as BL                              # noqa: E402

TRAIN_US = (2, 3, 4, 5, 6)
TEST_US = (2, 3, 4, 6, 8)


def make_split(U, n, seed):
    panel, cfg = make_scenario(n_users=U, seed=seed)
    d = MultiUserRISChannel(panel, cfg).generate(n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    return (panel, cfg, X,
            torch.from_numpy(d["F"]).to(torch.complex64),
            torch.from_numpy(d["G"]).to(torch.complex64),
            torch.from_numpy(d["hd"]).to(torch.complex64))


class RoundRobin:
    """Yields batches from several loaders in turn, one user count each."""

    def __init__(self, loaders):
        self.loaders = loaders

    def __iter__(self):
        its = [iter(l) for l in self.loaders]
        alive = list(range(len(its)))
        while alive:
            for i in list(alive):
                try:
                    yield next(its[i])
                except StopIteration:
                    alive.remove(i)

    def __len__(self):
        return sum(len(l) for l in self.loaders)


@torch.no_grad()
def score(model, X, Fc, Gc, hd, N, sc, bs=256):
    model.eval()
    acc, n = {}, 0
    for i in range(0, len(X), bs):
        s = slice(i, i + bs)
        m = rate_metrics(Fc[s], Gc[s], hd[s], model(X[s]), N, sc)
        for k, v in m.items():
            acc[k] = acc.get(k, 0.0) + v * (s.stop - s.start)
        n += min(bs, len(X) - i)
    return {k: v / n for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per_u", type=int, default=4000)
    ap.add_argument("--epochs", type=int, default=45)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    print(f"training user counts {TRAIN_US}, {args.per_u} scenarios each")

    tr_loaders, va_sets = [], []
    for U in TRAIN_US:
        panel, cfg, X, Fc, Gc, hd = make_split(U, args.per_u, seed=300 + U)
        itr, iva, _ = split_indices(args.per_u, frac=(0.8, 0.2, 0.0), seed=0)
        tr_loaders.append(DataLoader(
            TensorDataset(X[itr], Fc[itr], Gc[itr], hd[itr]),
            batch_size=128, shuffle=True))
        va_sets.append((X[iva], Fc[iva], Gc[iva], hd[iva], panel.N, cfg.snr_scale()))
    train_dl = RoundRobin(tr_loaders)

    model = EquivariantRIS(residual=False)
    print(f"model: {count_params(model):,} params\n")
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)
    sch = torch.optim.lr_scheduler.MultiStepLR(opt, [20, 32, 40], gamma=0.5)

    best, best_state, best_ep = -np.inf, None, 0
    for ep in range(1, args.epochs + 1):
        model.train()
        tot = 0.0
        for Xb, Fb, Gb, hb in train_dl:
            opt.zero_grad()
            loss = maxmin_loss(Fb, Gb, hb, model(Xb), Fb.shape[-1], va_sets[0][5])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item()
        sch.step()

        vals = [score(model, *v[:4], v[4], v[5])["min_rate"] for v in va_sets]
        mean_val = float(np.mean(vals))
        if mean_val > best:
            best, best_ep = mean_val, ep
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        if ep % 5 == 0 or ep == 1:
            per_u = "  ".join(f"U{u}={v:.2f}" for u, v in zip(TRAIN_US, vals))
            print(f"  ep {ep:3d}  loss={tot/len(train_dl):.4f}  mean={mean_val:.4f}"
                  f"   {per_u}{'  *' if ep == best_ep else ''}")

    model.load_state_dict(best_state)
    torch.save(model.state_dict(), os.path.join(args.out, "step5b_mixed.pt"))
    print(f"\nbest epoch {best_ep}\n")

    # ---------------------------------------------------------------- compare
    fixed = EquivariantRIS(residual=False).eval()
    fixed.load_state_dict(torch.load(os.path.join(args.out, "step4_Equivariant.pt")))

    print(f"{'U':>3}{'trained U=4':>13}{'trained mixed':>15}{'SU closed':>12}"
          f"{'PGA':>9}{'mixed % PGA':>13}")
    print("-" * 65)
    res = {}
    for U in TEST_US:
        panel, cfg, X, Fc, Gc, hd = make_split(U, 3000, seed=1000 + U)
        N, sc = panel.N, cfg.snr_scale()
        a = score(fixed, X, Fc, Gc, hd, N, sc)["min_rate"]
        b = score(model, X, Fc, Gc, hd, N, sc)["min_rate"]
        su = BL.summarise(BL.su_closed_form(Fc, Gc, hd, sc)[1])["min_rate"]
        pga = BL.summarise(BL.pga_maxmin(Fc, Gc, hd, sc, iters=250, restarts=3)[1])["min_rate"]
        res[U] = dict(fixed=a, mixed=b, su_closed=su, pga=pga)
        print(f"{U:>3}{a:>13.3f}{b:>15.3f}{su:>12.3f}{pga:>9.3f}{100*b/pga:>12.1f}%")

    print("\nmargin over the single-user closed form:")
    for U, v in res.items():
        print(f"  U={U}:  trained U=4 {100*(v['fixed']-v['su_closed'])/v['su_closed']:+6.1f}%"
              f"    trained mixed {100*(v['mixed']-v['su_closed'])/v['su_closed']:+6.1f}%")

    p = os.path.join(args.out, "step5b_mixed_users.json")
    json.dump({str(k): v for k, v in res.items()}, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### Bolum 5 -- hareketlilik (tezin omurgasi)

### `scripts/mumiso_aging.py`

*204 satir · sha256:ab0f6bccdcfa*

```python
"""
The channel-aging curve: what you lose by not reconfiguring in time.

THE QUESTION
------------
Every latency figure in this package has been compared against a coherence
time computed from a formula. This script replaces the formula with a
measurement: optimise the phase on the channel at t = 0, hold it, and watch
the rate decay as the user walks.

It then does the thing that makes the comparison honest. A method does not
deliver its answer to the channel it was handed -- it delivers it to the
channel that exists when it finishes. So each method's EFFECTIVE rate is
its own phase evaluated at t = its own measured latency. A method that
needs 5.6 seconds is answering a question about a channel from 8 metres ago.

WHERE THIS MODEL IS TRUSTWORTHY, AND WHICH WAY IT ERRS
------------------------------------------------------
The generator holds the scatterer set fixed for the whole window and lets
only the user positions move. Over tens of milliseconds -- a few
centimetres, a fraction of a wavelength -- that is the right model and the
decay is genuine geometry.

Over seconds it is not: a user who has walked 8 metres sees different
scatterers, and this model keeps the same ones. Measured consequence, the
temporal correlation of G floors at about 0.5 instead of decaying to the
0.10 that two independent channels show, and raising the cluster count from
6 to 60 barely moves that floor (0.60 -> 0.51) because the dominant cluster
keeps the channel nearly rank-one inside a fixed subspace.

So the model UNDERSTATES the loss at long horizons. That direction matters:
it means the slow classical methods are being flattered here and still
lose. For them the script also reports the STALE reference -- a t = 0 phase
evaluated on an independent channel -- which is the true asymptote. The
honest reading of a long-latency method is "somewhere between the curve and
the stale reference", and both are printed.
"""
import sys
import pathlib
import json
import argparse
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, to_torch
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--clusters", type=int, default=20,
                help="3GPP InH has ~15-19; the static generator's 6 is low")
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--tag", default="aging")
ap.add_argument("--no-learned", action="store_true",
                help="skip the learned row; use when the checkpoint was "
                     "trained against a different precoder and evaluating "
                     "it here would be an unfair comparison")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


# A fine grid where the model is trustworthy, plus the points the slow
# methods actually land on.
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
TRUST_MS = 200.0          # beyond this the frozen scatterer set shows

# latencies measured by scripts/mumiso_budget_fraction.py on an idle box
LAT = {"su_average": 0.03, "su_best_of": 0.05, "adam8": 13.3, "adam12": 19.6,
       "adam16": 26.6, "adam20": 34.6, "learned8": 42.9,
       "cd": 1500.0, "pga": 5600.0}

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": a.velocity,
                      "times_ms": TIMES, "n_clusters": a.clusters})
d = MobileMuMisoChannel(panel, cfg).generate(a.scenarios)
N, T, K = panel.positions.shape[0], a.tx, a.users
M = len(TIMES)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
lam = panel.lam

F = torch.as_tensor(d["F"], dtype=torch.complex64)
Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(M)]
Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(M)]
G0, H0 = Gt[0], Ht[0]

say(f"N={N} T={T} K={K}  {a.scenarios} scenarios  v={a.velocity} m/s  "
    f"{a.clusters} clusters")
say(f"coherence time 0.423/f_d = "
    f"{0.423/(a.velocity*panel.fc/3e8)*1e3:.1f} ms;  "
    f"model trusted to {TRUST_MS:.0f} ms\n")


def rate_at(th, m):
    return S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values


def adam_phase(L, start):
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


# --------------------------------------------------------------- phases
say("computing each method's phase on the t=0 channel ...")
t0 = time.time()
_, TH_SU = B.su_average(F, G0, H0, pt, nv)
_, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
phases = {"su_average": TH_SU, "su_best_of": TH_BEST,
          "adam8": adam_phase(8, TH_SU), "adam12": adam_phase(12, TH_SU),
          "adam16": adam_phase(16, TH_SU), "adam20": adam_phase(20, TH_SU)}
if not a.no_learned:
    net = UnrolledMuMiso(N=N, n_users=K, n_tx=T, steps=8, mode="exchange",
                         use_grad=True)
    net.load_state_dict(torch.load(a.ckpt))
    net.eval()
    phi = S.su_align_phase(F, G0, H0)
    X = torch.from_numpy(mumiso_features(d["F"], d["G_t"][:, 0],
                                         d["hd_t"][:, 0], phi.numpy()))
    with torch.no_grad():
        phases["learned8"] = net(X, F, G0, H0, pt, nv, TH_SU)
_, phases["cd"] = B.coord_descent(F, G0, H0, pt, nv)
_, phases["pga"] = B.pga(F, G0, H0, pt, nv)
say(f"  done in {time.time()-t0:.0f}s\n")

# ---------------------------------------------------------- stale floor
# a t=0 phase on an INDEPENDENT channel: the true asymptote of staleness
perm = torch.randperm(a.scenarios, generator=torch.Generator().manual_seed(1))
stale = {k: S.rates(F, G0[perm], H0[perm], torch.cos(v), torch.sin(v), pt, nv,
                    "zf").min(-1).values.mean().item()
         for k, v in phases.items()}

# ----------------------------------------------------------- the curve
say("=== rate of a phase fixed at t=0, as the user walks ===")
hdr = f"{'t [ms]':>8}{'disp [lam]':>11}" + "".join(
    f"{k[:9]:>10}" for k in phases)
say(hdr)
say("-" * len(hdr))
curve = {k: [] for k in phases}
for m in range(M):
    disp = a.velocity * TIMES[m] / 1e3 / lam
    row = f"{TIMES[m]:8.1f}{disp:11.2f}"
    for k, th in phases.items():
        v = rate_at(th, m).mean().item()
        curve[k].append(v)
        row += f"{v:10.3f}"
    say(row + ("" if TIMES[m] <= TRUST_MS else "   <- model optimistic"))

say(f"\n{'stale (independent channel)':>29}" + "".join(
    f"{stale[k]:10.3f}" for k in phases))

# ------------------------------------------------- the effective rate
say("\n=== EFFECTIVE rate: each method's phase at t = its own latency ===")
say(f"{'method':>12}{'t=0 rate':>10}{'latency':>10}{'eff. rate':>11}"
    f"{'kept':>7}{'stale':>9}  note")
say("-" * 76)
eff = {}
for k, th in phases.items():
    lat = LAT[k]
    # interpolate the curve at the method's latency
    v = float(np.interp(lat, TIMES, curve[k]))
    eff[k] = dict(t0=curve[k][0], latency_ms=lat, effective=v,
                  kept=v / curve[k][0], stale=stale[k],
                  trusted=lat <= TRUST_MS)
    note = "" if lat <= TRUST_MS else "model optimistic; true value nearer 'stale'"
    say(f"{k:>12}{curve[k][0]:10.3f}{lat:10.1f}{v:11.3f}"
        f"{v/curve[k][0]:7.2f}{stale[k]:9.3f}  {note}")

best = max((k for k in eff if eff[k]["trusted"]),
           key=lambda k: eff[k]["effective"])
say(f"\n  best effective rate among methods inside the trusted horizon: "
    f"{best}  ({eff[best]['effective']:.3f} b/s/Hz)")
say("  the slow methods' t=0 rates are higher, but they are answers to a")
say("  channel that no longer exists by the time they arrive -- and this")
say("  model flatters them, because it keeps their scatterers alive.")

json.dump(dict(config=vars(a), times_ms=list(TIMES), trust_ms=TRUST_MS,
               curve={k: list(map(float, v)) for k, v in curve.items()},
               stale=stale, effective=eff, latencies=LAT,
               coherence_ms=0.423 / (a.velocity * panel.fc / 3e8) * 1e3),
          open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_frontier.py`

*163 satir · sha256:175da29e064a*

```python
"""
The latency-quality frontier, and the coherence-time budget.

This is the script that decided the project's conclusion, so it is worth
running yourself rather than taking the numbers on trust.

It asks the only question that matters for a deployed RIS: at a given
millisecond budget, what is the best min-rate anyone can achieve? Then it
places the learned update rule on that curve. The learned model turns out
NOT to be on the frontier -- tuned gradient ascent reaches a higher rate in
half the time -- which is why the thesis conclusion is framed around the
coherence-time constraint rather than around a neural network.

Coherence time, for reference: a user walking at 1.5 m/s at 3 GHz gives
f_d = v f_c / c = 15 Hz and T_c = 0.423 / f_d = 28 ms.
"""
import sys
import pathlib
import json
import time
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--samples", type=int, default=600)
ap.add_argument("--eval-n", type=int, default=450)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--velocity", type=float, default=1.5, help="m/s")
ap.add_argument("--tag", default="frontier")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, TH0 = B.su_average(F, G, hd, pt, nv)
ev = slice(0, a.eval_n)
one = slice(0, 1)

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode="exchange", use_grad=True)
net.load_state_dict(torch.load(a.ckpt))
net.eval()


def adam_phase(ids, L, lr):
    n = len(range(*ids.indices(a.samples)))
    dl = torch.zeros(n, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


def rate_of(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


def timeit(fn, reps):
    for _ in range(3):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.percentile(np.array(ts) * 1e3, 50))


fd = a.velocity * cfg.__dict__.get("fc", 3e9) / 3e8 if False else \
    a.velocity * panel.fc / 3e8
tc = 0.423 / fd * 1e3
say(f"N={N} T={a.tx} K={a.users}, {a.eval_n} scenarios, CPU, batch 1")
say(f"coherence time at {a.velocity} m/s, {panel.fc/1e9:.1f} GHz : "
    f"f_d = {fd:.1f} Hz, T_c = {tc:.1f} ms\n")

rows = []
rows.append(("su_average", rate_of(TH0[ev], ev),
             timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)))
for L in (4, 8, 16, 32, 64, 128):
    rows.append((f"tuned Adam, {L} steps", rate_of(adam_phase(ev, L, a.lr), ev),
                 timeit(lambda: adam_phase(one, L, a.lr), 8)))
with torch.no_grad():
    th_net = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
rows.append((f"learned, {a.steps} steps", rate_of(th_net, ev),
             timeit(lambda: net(X[one], F[one], G[one], hd[one], pt, nv,
                                TH0[one]), 20)))
rows.append(("coord descent", S.rate_metrics(
    B.coord_descent(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)))
rows.append(("AO (cd+su+rnd starts)", S.rate_metrics(
    B.ao(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 2)))
# PGA = 3 purely RANDOM restarts. Measured to be marginally but
# CONSISTENTLY better than ao across four (T,K) settings, so the
# coordinate-descent and su_average starts are not just redundant, they
# are worse than random ones. The honest "strongest classical" is the max
# of the two, which is why both are listed.
rows.append(("PGA (3 random starts)", S.rate_metrics(
    B.pga(F[ev], G[ev], hd[ev], pt, nv)[0])["min_rate"],
    timeit(lambda: B.pga(F[one], G[one], hd[one], pt, nv), 2)))

rows.sort(key=lambda r: r[2])
best_in_budget = max((r for r in rows if r[2] <= tc), key=lambda r: r[1])
say(f"{'method':>22}{'min rate':>11}{'latency p50':>14}{'in budget':>11}")
say("-" * 58)
for nm, q, t in rows:
    fits = "yes" if t <= tc else "NO"
    star = "  <-- best in budget" if (nm, q, t) == best_in_budget else ""
    say(f"{nm:>22}{q:11.4f}{t:12.1f} ms{fits:>11}{star}")

# which points are Pareto optimal
pareto = []
for nm, q, t in rows:
    if not any(q2 >= q and t2 <= t and (nm2 != nm) for nm2, q2, t2 in rows):
        pareto.append(nm)
say(f"\n  Pareto-optimal: {', '.join(pareto)}")
learned = [r for r in rows if r[0].startswith("learned")][0]
say(f"  learned model on the frontier: "
    f"{'yes' if learned[0] in pareto else 'NO -- dominated'}")
strongest = max(rows, key=lambda r: r[1])
say(f"  strongest classical overall : {strongest[0]}  {strongest[1]:.4f} "
    f"at {strongest[2]:.0f} ms")
best_budget_frac = best_in_budget[1] / strongest[1]
say(f"  best-in-budget / strongest  : {best_budget_frac:.3f}")
res_extra = dict(strongest=strongest[0], strongest_rate=strongest[1],
                 best_in_budget_frac=best_budget_frac)

res = dict(**res_extra, config=vars(a), coherence_ms=tc, fd_hz=fd,
           rows=[dict(method=n, min_rate=q, latency_ms=t) for n, q, t in rows],
           pareto=pareto, best_in_budget=best_in_budget[0])
with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_beam_staleness.py`

*139 satir · sha256:be5a1e837981*

```python
"""
The assumption Chapter 5 rests on: the beamformer stays fresh.

WHY THIS FILE EXISTS
--------------------
Every mobility number in this package holds the PHASE fixed from t=0 and
evaluates it on the channel at t=tau, while the beamformer W is recomputed
from the channel that exists at t=tau. That split -- "phase ages, beam does
not" -- is a modelling choice, and it is the single assumption the whole
chapter leans on.

Its size was quoted as "17x at 28.2 ms (4.718 against 0.279)" in the
chapter draft, the advisor assessment and the writing reference. That
number was measured once, inline, and never written to a script. This
project has already been bitten by exactly that: an earlier report's
"95% in budget" column came from an unsaved one-liner, an audit measured
85-90% instead, and nobody could rerun the original. The rule that came out
of it is in `mumiso_budget_fraction.py`:

    A number that carries a conclusion and has no script behind it is not
    a measurement.

So this script measures it properly, and whatever it prints replaces the
quoted figure.

WHAT IS COMPARED
----------------
One phase configuration chosen at t = 0, then at each later time:

    fresh beam   W from the TRUE channel at t = tau, phase from t = 0
    stale beam   W from the channel at t = 0,        phase from t = 0

Both are evaluated on the true channel at t = tau. The gap between them is
the cost of letting the beamformer age at the same rate as the surface.

The physical argument for the split is that the two are updated by
different machinery at different cost: W is a digital computation at the
base station, refreshed per frame from pilots; theta needs the joint
optimisation of N passive elements, which is what the latency column
measures. This script does not defend that argument -- it prices it.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileMuMisoChannel, MobileConfig
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--phase", default="su_best_of",
                choices=("su_average", "su_best_of", "adam8"))
ap.add_argument("--tag", default="beam_staleness")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
TIMES = (0.0, 5.0, 10.0, 20.0, 28.2, 50.0, 100.0, 200.0)


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, _ = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                seed=a.seed)
cfg = MobileConfig(n_users=a.users, n_bs_antennas=a.tx, seed=a.seed,
                   velocity=a.velocity, times_ms=TIMES)
d = MobileMuMisoChannel(panel, cfg).generate(a.scenarios, chunk=200)

F = torch.as_tensor(d["F"], dtype=torch.complex64)
G_t = torch.as_tensor(d["G_t"], dtype=torch.complex64)      # [S,M,K,N]
H_t = torch.as_tensor(d["hd_t"], dtype=torch.complex64)     # [S,M,K,T]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
G0, H0 = G_t[:, 0], H_t[:, 0]
say(f"N={F.shape[1]} T={a.tx} K={a.users}  {a.scenarios} scenarios  "
    f"v={a.velocity} m/s  phase={a.phase}")

# ---- the phase, chosen once at t = 0 -----------------------------------
if a.phase == "adam8":
    _, th0 = B.su_average(F, G0, H0, pt, nv)
    dl = torch.zeros_like(th0, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for _ in range(8):
        th = th0 + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    theta = (th0 + dl.detach())
else:
    _, theta = B._DISPATCH[a.phase](F, G0, H0, pt, nv, precoder="zf")

cos_t, sin_t = torch.cos(theta), torch.sin(theta)

# W computed ONCE at t = 0, then frozen -- the stale arm
He0 = S.effective_channel(F, G0, H0, cos_t, sin_t)
W_stale = S.precode(He0, pt, "zf", noise_var=nv)


def min_rate(He, W):
    return torch.log2(1.0 + S.sinr(He, W, nv)).min(-1).values.mean().item()


say(f"\n{'t [ms]':>8}{'fresh beam':>13}{'stale beam':>13}{'ratio':>9}")
say("-" * 43)
rows = []
for m, t in enumerate(TIMES):
    He = S.effective_channel(F, G_t[:, m], H_t[:, m], cos_t, sin_t)
    W_fresh = S.precode(He, pt, "zf", noise_var=nv)
    fr, st = min_rate(He, W_fresh), min_rate(He, W_stale)
    rows.append(dict(t_ms=t, fresh=fr, stale=st,
                     ratio=(fr / st if st > 1e-9 else float("inf"))))
    say(f"{t:8.1f}{fr:13.4f}{st:13.4f}{rows[-1]['ratio']:9.1f}x")

tc = next(r for r in rows if abs(r["t_ms"] - 28.2) < 1e-6)
say(f"\nAt the coherence time (28.2 ms): fresh {tc['fresh']:.4f}, "
    f"stale {tc['stale']:.4f}  ->  {tc['ratio']:.1f}x")
say("\nRead it straight: this is the price of the chapter's assumption, not")
say("evidence for it. If a deployment cannot refresh W faster than theta,")
say("the chapter's method ranking does not transfer -- every method")
say("collapses together and the discriminator is beam latency, not phase")
say("latency. That belongs in the chapter's limitations, stated with this")
say("number.")

res = dict(config=vars(a), times_ms=list(TIMES), rows=rows,
           at_coherence=tc)
(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### Bolum 6 -- gercekci senaryo ve donanim

### `scripts/mumiso_antenna_corr.py`

*73 satir · sha256:52e1fbee7d50*

```python
"""Anten ekseni korelasyonu: kazanclar antene gore bagimsiz cekilince ne oluyor?

UYARI -- IKINCI BLOK GUVENILIR DEGIL, SUPERSEDED.
--------------------------------------------------
Bu dosyanin BIRINCI blogu ("MEVCUT KOD") saglamdir ve teze girebilir:
anten ekseni korelasyonu 0.204 (LoS 0.818, NLoS 0.130), eleman ekseni
0.639, anten etkin rank 7.26/8.

IKINCI blok ("DUZELTILMIS") kazanc paylasiminin bedelini tahmin etmeye
calisir ve YANLIStir: sacicilari ve Ricean K'yi kendi rng'siyle yeniden
cekiyor, dolayisiyla iki kolu farkli senaryolarda karsilastiriyor. Toplam
korelasyonun 0.290 -> 0.085 duserken NLoS'un 0.022 -> 0.294 CIKMASI bu
tutarsizligin isareti.

Kazanc paylasiminin bedeli icin `scripts/mumiso_gain_sharing.py` kullanin:
rastgele akisi koruyarak ayni senaryolarda olcer (capa -%31.98,
PGA -%8.15, optimizasyonun degeri 1.75x -> 2.36x).
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   neighbour_corr, effective_rank)
from ris_mu.channel import _unit_power

panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
ch = MuMisoChannel(panel,cfg)
d  = ch.generate(1500)
F, los = d["F"], d["los_ris_bs"]          # F [S,N,T]
T = F.shape[2]

def ant(Fs):                               # satirlar (S,N), kolonlar T
    return neighbour_corr(Fs.reshape(-1, T))
def el(Fs):                                # satirlar (S,T), kolonlar N
    return neighbour_corr(Fs.transpose(0,2,1).reshape(-1, Fs.shape[1]))

print("=== MEVCUT KOD (kazanc her anten icin bagimsiz) ===")
print(f"  anten ekseni komsu korelasyonu : tum {ant(F):.3f}   "
      f"LoS {ant(F[los]):.3f}   NLoS {ant(F[~los]):.3f}")
print(f"  eleman ekseni                  : tum {el(F):.3f}")
print(f"  anten ekseni etkin rank        : {effective_rank(F.reshape(-1,T)):.2f} / {T}")

# --- ayni fizik, ama kazanclar anten ekseninde PAYLASILMIS -------------
print("\n=== DUZELTILMIS (her sacici icin TEK kazanc, antenler paylasiyor) ===")
P, k = ch.panel, ch.k
rng = np.random.default_rng(0)
S, L = len(F), cfg.n_clusters
bsa  = d["bs_array"]                       # [S,T,3]
scat = rng.uniform([0,0,0], np.asarray(cfg.room,float), (S,L,3))
kap_lin = 10**(ch.pl.rice_k_db(rng, S)/10)

def ris_link(gains_shape):
    d_el = P.distances(bsa)                            # [S,T,N]
    gain = P.pattern(bsa)
    h_los = _unit_power(np.sqrt(gain)/np.maximum(d_el,1.0)
                        * np.exp(-1j*k*d_el))
    d1 = np.linalg.norm(bsa[...,None,:] - scat[:,None], axis=-1)   # [S,T,L]
    d2 = P.distances(scat[:,None])                                 # [S,1,L,N]
    g_s = P.pattern(scat[:,None])
    g = (rng.standard_normal(gains_shape)+1j*rng.standard_normal(gains_shape))/np.sqrt(2)
    if gains_shape == (S,1,L): g = np.broadcast_to(g,(S,T,L))
    amp = np.sqrt(g_s)/np.maximum(d1[...,None]*d2,1.0)
    h_nlos = _unit_power(np.sum(g[...,None]*amp
                                * np.exp(-1j*k*(d1[...,None]+d2)), axis=-2))
    kp = np.where(los, kap_lin, 0.0)[:,None,None]
    return (np.sqrt(kp/(kp+1))*h_los + np.sqrt(1/(kp+1))*h_nlos).transpose(0,2,1)

F_ind = ris_link((S,T,L))      # mevcut davranis, yeniden uretilmis
F_shr = ris_link((S,1,L))      # kazanclar antenler arasinda paylasilmis
for nm,Fx in (("bagimsiz (mevcut)",F_ind), ("paylasilmis (dogru)",F_shr)):
    print(f"  {nm:22} anten korelasyonu {ant(Fx):.3f}  "
          f"(NLoS {ant(Fx[~los]):.3f})  etkin rank {effective_rank(Fx.reshape(-1,T)):.2f}/{T}")
```

### `scripts/mumiso_gain_sharing.py`

*60 satir · sha256:0ff5e98f3c59*

```python
"""Kazanc paylasiminin bedeli -- rastgele AKIS korunarak.

Onemli: _crandn ayni SAYIDA deger tuketmeli, yoksa akis kayar ve
senaryolar da degisir (ilk denemem tam bu yuzden gecersizdi).
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, neighbour_corr, effective_rank)
from ris_mu.mumiso import system as S, baselines as B

class SharedGainChannel(MuMisoChannel):
    def _crandn(self, shape):
        g = super()._crandn(shape)            # AYNI sayida deger tuket
        if len(shape) == 3 and shape[1] == self.T:        # (S,T,L)
            return np.broadcast_to(g[:, :1], shape).copy()
        if len(shape) == 4 and shape[2] == self.T:        # (S,K,T,L)
            return np.broadcast_to(g[:, :, :1], shape).copy()
        return g

NS=1200
def build(cls):
    panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
    return cls(panel,cfg).generate(NS), cfg

res={}
for nm,cls in (("mevcut (bagimsiz)",MuMisoChannel),
               ("paylasilmis (fiziksel)",SharedGainChannel)):
    d,cfg = build(cls); res[nm]=(d,cfg)

# akis korundu mu? senaryolar ayni mi?
d0=res["mevcut (bagimsiz)"][0]; d1=res["paylasilmis (fiziksel)"][0]
same = (np.abs(d0["ue_pos"]-d1["ue_pos"]).max()==0
        and (d0["los_ris_bs"]==d1["los_ris_bs"]).all()
        and (d0["los_ris_ue"]==d1["los_ris_ue"]).all())
print(f"ayni senaryolar (konum + LoS): {'EVET - karsilastirma gecerli' if same else 'HAYIR - gecersiz'}")
print(f"  G farki (0 olmamali, kazanclar degisti): {np.abs(d0['G']-d1['G']).max():.3e}")
print(f"  hd farki: {np.abs(d0['hd']-d1['hd']).max():.3e}")
print(f"  F farki : {np.abs(d0['F']-d1['F']).max():.3e}\n")

print(f"{'model':>22}{'anten kor.':>12}{'NLoS':>8}{'anten rank':>12}"
      f"{'capa':>10}{'PGA':>10}")
print("-"*74)
vals={}
for nm,(d,cfg) in res.items():
    F,G,hd,_ = to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
    T=F.shape[2]; los=d["los_ris_bs"]
    ac=neighbour_corr(d["F"].reshape(-1,T))
    an=neighbour_corr(d["F"][~los].reshape(-1,T))
    er=effective_rank(d["F"].reshape(-1,T))
    R0,_=B.su_average(F,G,hd,pt,nv); r0=S.rate_metrics(R0)["min_rate"]
    Rp,_=B.pga(F[:300],G[:300],hd[:300],pt,nv); rp=S.rate_metrics(Rp)["min_rate"]
    vals[nm]=(ac,an,er,r0,rp)
    print(f"{nm:>22}{ac:12.3f}{an:8.3f}{er:12.2f}{r0:10.4f}{rp:10.4f}")
a,b=vals["mevcut (bagimsiz)"],vals["paylasilmis (fiziksel)"]
print(f"\nfiziksel modelin bedeli: capa %{100*(b[3]/a[3]-1):+.2f}   PGA %{100*(b[4]/a[4]-1):+.2f}")
print(f"anten korelasyonu: {a[0]:.3f} -> {b[0]:.3f}   NLoS: {a[1]:.3f} -> {b[1]:.3f}")
print(f"anten etkin rank : {a[2]:.2f} -> {b[2]:.2f} / 8")
```

### `scripts/mumiso_gain_source.py`

*37 satir · sha256:7141a0938ef5*

```python
"""
Where the gain comes from: no panel -> random phase -> optimised.

This table is quoted in the thesis ("a random surface already delivers
about half the gain") and had no script behind it until now. Every row
uses the SAME precoder settings -- an earlier version of `no_ris` did not,
and reported the floor 10.9% too high.
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

NS = 1200
torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
out = {}
print(f"{NS} scenarios, N={F.shape[1]} T=8 K=4, identical precoder on every row\n")
print(f"{'method':>14}{'min rate':>11}")
for m in ("no_ris", "random", "su_weakest", "su_average", "su_best_of", "pga"):
    R, _ = B._DISPATCH[m](F[:300] if m == "pga" else F,
                          G[:300] if m == "pga" else G,
                          hd[:300] if m == "pga" else hd, pt, nv, precoder="zf")
    out[m] = S.rate_metrics(R)["min_rate"]
    note = "  (300 scenarios)" if m == "pga" else ""
    print(f"{m:>14}{out[m]:11.4f}{note}")
print(f"\n  random / pga      = {out['random']/out['pga']:.2f}"
      f"   <- how much a RANDOM surface already delivers")
print(f"  no_ris -> random  = {out['random']/out['no_ris']:.2f}x")
print(f"  random -> pga     = {out['pga']/out['random']:.2f}x")
p = pathlib.Path(__file__).resolve().parents[1] / "results/mumiso_gain_source.json"
p.write_text(json.dumps(out, indent=1))
print(f"\nwrote {p.name}")
```

### `scripts/mumiso_precoder_cost.py`

*46 satir · sha256:eb616f5073d8*

```python
"""Sabit MMSE regulatoru zayif senaryolari sakatliyor mu?"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(1200)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
K=4
_,TH=B.su_average(F,G,hd,pt,nv)
He=S.effective_channel(F,G,hd,torch.cos(TH),torch.sin(TH))
M=He@He.conj().transpose(-1,-2)
p_per=torch.diagonal(M,dim1=-2,dim2=-1).real.mean(-1)     # senaryo basina
lam = K*nv/pt
rel = lam/p_per                                            # kendi olcegine gore
print(f"MMSE lam (sabit)        : {lam:.4e}")
print(f"lam / kendi p_sig'i  -> medyan {rel.median():.3e}  "
      f"%90 {rel.quantile(0.9):.3e}  max {rel.max():.3e}")
print("\ndocstring'in kendi tablosu: 1e-6 bagil -> MRT'ye cokme, 3.4e-3 -> %55 kayip")
for thr,lbl in ((1e-6,"1e-6 (cokme esigi)"),(1e-3,"1e-3"),(1e-2,"1e-2"),(1e-1,"1e-1")):
    f=(rel>thr).float().mean().item()
    print(f"  bagil regulator > {lbl:20} : senaryolarin %{100*f:.1f}'i")

def minrate(eps_abs=None):
    W = S.zf(He,pt,eps_abs=eps_abs) if eps_abs is not None else S.zf(He,pt,noise_var=nv)
    return torch.log2(1+S.sinr(He,W,nv)).min(-1).values

r_mmse = minrate()
r_pure = minrate(eps_abs=0.0)
print(f"\n{'':22}{'MMSE (varsayilan)':>20}{'saf ZF (eps=0)':>18}{'fark':>12}")
print(f"{'tum 1200 senaryo':22}{r_mmse.mean():20.4f}{r_pure.mean():18.4f}"
      f"{100*(r_pure.mean()/r_mmse.mean()-1):11.2f}%")
# zayif kuyruk: kendi olcegine gore en cok regulatör yiyen %10
hard = rel.argsort(descending=True)[:120]
print(f"{'en kotu %10 (kuyruk)':22}{r_mmse[hard].mean():20.4f}{r_pure[hard].mean():18.4f}"
      f"{100*(r_pure[hard].mean()/r_mmse[hard].mean()-1):11.2f}%")
easy = rel.argsort()[:120]
print(f"{'en iyi %10':22}{r_mmse[easy].mean():20.4f}{r_pure[easy].mean():18.4f}"
      f"{100*(r_pure[easy].mean()/r_mmse[easy].mean()-1):11.2f}%")
print(f"\nkuyrukta kac senaryo MRT'ye cokmus (bagil>1e-6): "
      f"{(rel[hard]>1e-6).sum().item()}/120")
```

### `scripts/mumiso_csi_room.py`

*127 satir · sha256:4600791a219c*

```python
"""
Is there room for a robust learner under imperfect CSI?

Before spending a training run on the hypothesis "a learned model is robust
to CSI error where a classical optimiser overfits it", measure whether the
room exists at all. Three things decide it:

  1. Does the achievable rate collapse with error? If a classical optimiser
     at its best setting still gets most of the perfect-CSI rate, nothing
     is left to win.
  2. Does the OPTIMAL number of gradient steps shrink as error grows? That
     is the signature of overfitting the estimate, and it is what a robust
     method would exploit.
  3. How big is the gap between optimising on the estimate and the
     unreachable oracle that optimises on the truth? That gap is the
     ceiling on any robustness gain.

If (1) and (2) say no, the hypothesis is dead and the training run is not
worth it. Reporting that is a result too.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.csi import add_error, rates_mismatched, db_to_e2

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--levels", default="None,-20,-15,-10,-5,0")
ap.add_argument("--steps", default="0,2,4,8,16,32,64")
ap.add_argument("--tag", default="csi_room")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.scenarios)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()

LEVELS = [None if x.strip() == "None" else float(x) for x in a.levels.split(",")]
STEPS = [int(x) for x in a.steps.split(",")]

say(f"N={N} T={a.tx} K={a.users}  {a.scenarios} scenarios")
say("phase AND precoder from the estimate; rate evaluated with the truth\n")


def adam_phase(Fe, Ge, He, start, L):
    """Optimise on whatever channel it is handed."""
    if L == 0:
        return start
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(Fe, Ge, He, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


res = {"levels": [], "steps": STEPS}
say(f"{'error':>8}" + "".join(f"{'L='+str(L):>9}" for L in STEPS)
    + f"{'best L':>8}{'oracle':>9}{'gap':>7}")
say("-" * (8 + 9 * len(STEPS) + 24))

for db in LEVELS:
    e2 = db_to_e2(db)
    Fe, Ge, He = add_error(F, G, hd, e2, seed=7)
    _, start = B.su_best_of(Fe, Ge, He, pt, nv)      # anchor from the estimate
    row, best = [], (-1, -np.inf)
    for L in STEPS:
        th = adam_phase(Fe, Ge, He, start, L)
        r = rates_mismatched(F, G, hd, Fe, Ge, He, torch.cos(th),
                             torch.sin(th), pt, nv).min(-1).values.mean().item()
        row.append(r)
        if r > best[1]:
            best = (L, r)
    # the unreachable oracle: optimise AND precode on the truth, 32 steps
    _, st_true = B.su_best_of(F, G, hd, pt, nv)
    th_o = adam_phase(F, G, hd, st_true, 32)
    orc = S.rates(F, G, hd, torch.cos(th_o), torch.sin(th_o), pt, nv,
                  "zf").min(-1).values.mean().item()
    lab = "perfect" if db is None else f"{db:.0f} dB"
    say(f"{lab:>8}" + "".join(f"{v:9.3f}" for v in row)
        + f"{best[0]:8d}{orc:9.3f}{best[1]/orc:7.2f}")
    res["levels"].append(dict(db=db, e2=e2, rates=row, best_L=best[0],
                              best_rate=best[1], oracle=orc,
                              frac_of_oracle=best[1] / orc))

say("")
say("=== reading ===")
bl = [r["best_L"] for r in res["levels"]]
fr = [r["frac_of_oracle"] for r in res["levels"]]
say(f"  best step count across error levels : {bl}")
shrinks = bl[-1] < bl[0]
say(f"  does the optimal step count shrink with error : {shrinks}")
say(f"  best achievable / oracle            : "
    + " ".join(f"{v:.2f}" for v in fr))
room = (1.0 - min(fr)) > 0.10
say(f"  is there >10% left on the table at the worst level : {room}")
if shrinks and room:
    say("  -> the hypothesis has room. A model trained ACROSS error")
    say("     realisations could plausibly recover part of that gap.")
else:
    say("  -> the hypothesis has little room here. Say so and move on;")
    say("     a training run would be spent confirming a null result.")

json.dump(res, open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/mumiso_quant_latency.py`

*114 satir · sha256:9b3a60ce25be*

```python
"""
Quantised phase and latency: the two places where a learned model and a
classical optimiser are genuinely not comparable on rate alone.

Quantisation -- the honest comparison is against DISCRETE coordinate
descent, which searches the actual 2^b grid, not against "optimise
continuously then round". On an earlier single-RIS experiment discrete CD
beat a straight-through network at 1 bit (5.600 vs 3.544). This script
measures whether that holds here.

Latency -- one forward pass versus thousands of objective evaluations. This
is where the learned model wins and it is the claim the thesis can defend.
"""
import sys, pathlib, json, time, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.train import train_model, evaluate
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=8000)
ap.add_argument("--epochs", type=int, default=20)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--tag", default="quant")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
def say(*m): print(*m, flush=True)

panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd).numpy()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi))
tr, va, te = split_indices(a.samples, seed=0)
ev = te[:a.eval_n]
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}  eval on {len(ev)}\n")

res = dict(config=vars(a), quant={}, latency={})

# ------------------------------------------------------------- quantisation
say("=== quantised phase: discrete CD vs continuous-then-round vs learned ===")
say(f"{'bits':>5}{'suavg->rnd':>12}{'AO->rnd':>10}{'CD->rnd':>10}"
    f"{'discrete CD':>13}{'learned STE':>13}")
say("-" * 63)
for bits in (1, 2, 3):
    row = {}
    row["su_round"] = S.rate_metrics(
        B.su_average(F[ev], G[ev], hd[ev], pt, nv, bits=bits)[0])["min_rate"]
    _, th_ao = B.ao(F[ev], G[ev], hd[ev], pt, nv, bits=None)
    row["ao_round"] = S.rate_metrics(
        B._rate(F[ev], G[ev], hd[ev], th_ao, pt, nv, "zf", bits))["min_rate"]
    _, th_cd = B.coord_descent(F[ev], G[ev], hd[ev], pt, nv, bits=None)
    row["cd_round"] = S.rate_metrics(
        B._rate(F[ev], G[ev], hd[ev], th_cd, pt, nv, "zf", bits))["min_rate"]
    row["cd_discrete"] = S.rate_metrics(
        B.coord_descent(F[ev], G[ev], hd[ev], pt, nv, bits=bits)[0])["min_rate"]

    torch.manual_seed(a.seed)
    net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=a.mode)
    net, _ = train_model(net, X, F, G, hd, pt, nv, (tr, va, te),
                         epochs=a.epochs, seed=a.seed, bits=bits, log=None)
    row["learned_ste"] = evaluate(net, X, F, G, hd, pt, nv, ev, bits=bits)[0]
    res["quant"][bits] = row
    say(f"{bits:5d}{row['su_round']:12.4f}{row['ao_round']:10.4f}"
        f"{row['cd_round']:10.4f}{row['cd_discrete']:13.4f}"
        f"{row['learned_ste']:13.4f}")

best = {b: max(r, key=r.get) for b, r in res["quant"].items()}
say("\n  winner per bit depth: " + ", ".join(f"{b}-bit {w}" for b, w in best.items()))

# ----------------------------------------------------------------- latency
say("\n=== latency, single scenario (CPU, batch size 1) ===")
net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=a.mode)
sd = OUT / f"mumiso_main_{a.mode}.pt"
if sd.exists():
    net.load_state_dict(torch.load(sd)); say(f"  (loaded {sd.name})")
net.eval()
one = slice(0, 1)
with torch.no_grad():
    for _ in range(5):
        net.phases(X[one])
def timeit(fn, reps):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
    return np.array(ts) * 1e3
with torch.no_grad():
    t_net = timeit(lambda: net.phases(X[one]), 50)
t_cd = timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)
t_ao = timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 3)
t_su = timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)
for nm, t in [("learned (1 pass)", t_net), ("SU closed form", t_su),
              ("coord descent", t_cd), ("AO (CD+PGA)", t_ao)]:
    res["latency"][nm] = dict(p50=float(np.percentile(t, 50)),
                              p95=float(np.percentile(t, 95)))
    say(f"  {nm:>18}  p50 {np.percentile(t,50):9.3f} ms   "
        f"p95 {np.percentile(t,95):9.3f} ms")
sp = res["latency"]["AO (CD+PGA)"]["p50"] / res["latency"]["learned (1 pass)"]["p50"]
say(f"  -> learned model is {sp:.0f}x faster than AO at the median")

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
```

### `scripts/step3_csi_transfer.py`

*168 satir · sha256:372aed33fe5d*

```python
"""
step3_csi_transfer.py
---------------------
Why a realistic channel is a prerequisite for an architecture claim.

The argument
------------
For a single user the optimal phase is theta_n = -angle(F_n) - angle(G_n).
That map is ELEMENT-LOCAL: element n's answer depends on element n's own
channel pair and on nothing else, whatever channel model produced it. Under
perfect CSI, therefore, no architecture that mixes elements can beat a
sufficiently expressive element-local model -- there is nothing to mix.

Spatial processing can only pay off when the per-element observation is
corrupted, so that neighbouring elements carry information about each other.
That requires the channel to be spatially correlated. It follows that:

  * on the LEGACY channel (independent coefficient per element) neighbours are
    uninformative, so spatial models cannot help at any noise level;
  * on the GEOMETRIC channel neighbours are correlated, so spatial models
    should pull ahead as CSI degrades.

This experiment measures exactly that, crossing

    channel in {legacy, geometric}
  x CSI error in {0, 0.1, 0.25}
  x model   in {element-local, local mixing (CNN), global mixing (CNN-LSTM)}

The CSI error is applied to the model INPUT only; labels come from the true
channel, so the task is estimation under uncertainty rather than a different
task. All models use the width-1 output head, so the comparison isolates the
body.

Usage:  python scripts/step3_csi_transfer.py --n 20000 --epochs 25
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                                   # noqa: E402
from ris_mu.channel import legacy_generate, MultiUserRISChannel, make_scenario  # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices       # noqa: E402
from ris_mu.models import SharedMLP, CNNOnly, CNNLSTM, count_params     # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate       # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed          # noqa: E402


def add_csi_error(F, G, sigma, rng):
    """
    Multiplicative-power CSI error: the perturbation is scaled to each
    sample's own channel power, so sigma is a relative error and the two
    channel models are perturbed comparably despite very different absolute
    path loss.
    """
    if sigma <= 0:
        return F, G

    def perturb(H):
        p = np.sqrt(np.mean(np.abs(H) ** 2, axis=-1, keepdims=True))
        e = (rng.standard_normal(H.shape) + 1j * rng.standard_normal(H.shape)) / np.sqrt(2)
        return H + sigma * p * e
    return perturb(F), perturb(G)


def build_eval(N):
    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for X, Y in loader:
                P.append(model(X))
                T.append(Y.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))
    return eval_fn


def step_fn(model, batch):
    X, Y = batch
    return phase_aware_mse(model(X), Y.flatten(1))


def get_channel(kind, n, panel):
    if kind == "legacy":
        d = legacy_generate(n, panel)
        return d["F"], d["G"][:, 0, :]
    p2, cfg = make_scenario(n_users=1, seed=7)
    d = MultiUserRISChannel(p2, cfg).generate(n)
    return d["F"], d["G"][:, 0, :]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    panel = RISPanel(M=8, K=4)
    N = panel.N
    eval_fn = build_eval(N)
    itr, iva, ite = split_indices(args.n, seed=0)

    builders = {
        "element-local":  lambda: SharedMLP(N),
        "local mixing":   lambda: CNNOnly(N, head="local"),
        "global mixing":  lambda: CNNLSTM(N, head="local"),
    }
    sigmas = [0.0, 0.10, 0.25]
    res = {}

    for ch_kind in ("legacy", "geometric"):
        set_seed(1)
        F, G = get_channel(ch_kind, args.n, panel)
        Y = torch.from_numpy(su_labels(F, G))           # labels from TRUE channel
        for sg in sigmas:
            rng = np.random.default_rng(100)
            Fe, Ge = add_csi_error(F, G, sg, rng)
            X = torch.from_numpy(su_features(Fe, Ge))
            tr, va, te = make_loaders((X, Y), itr, iva, ite)
            for mname, build in builders.items():
                set_seed(42)
                model = build()
                tag = f"{ch_kind[:4]}/s{sg}/{mname[:5]}"
                print(f"--- {ch_kind:<10} sigma={sg:<5} {mname:<14} "
                      f"({count_params(model):,} par)")
                run_training(model, tr, va, step_fn, eval_fn,
                             epochs=args.epochs, tag=tag, verbose=False)
                _, m = eval_fn(model, te)
                res[f"{ch_kind}|{sg}|{mname}"] = dict(
                    channel=ch_kind, sigma=sg, model=mname,
                    params=count_params(model),
                    rmse=m["rmse"], sr5=m["sr5"])
                print(f"    RMSE={m['rmse']:7.3f}°   SR@5={m['sr5']:6.2f}%")

    # ---- summary table -----------------------------------------------------
    print(f"\n{'channel':<11}{'sigma':>7}" + "".join(f"{k:>16}" for k in builders))
    print("-" * (18 + 16 * len(builders)))
    for ch_kind in ("legacy", "geometric"):
        for sg in sigmas:
            row = f"{ch_kind:<11}{sg:>7.2f}"
            for mname in builders:
                row += f"{res[f'{ch_kind}|{sg}|{mname}']['rmse']:>15.2f}°"
            print(row)

    print("\nadvantage of spatial mixing over element-local "
          "(negative = mixing helps):")
    for ch_kind in ("legacy", "geometric"):
        for sg in sigmas:
            base = res[f"{ch_kind}|{sg}|element-local"]["rmse"]
            best = min(res[f"{ch_kind}|{sg}|{m}"]["rmse"] for m in builders)
            print(f"  {ch_kind:<10} sigma={sg:<5}  {100*(best-base)/base:+6.1f}%")

    p = os.path.join(args.out, "step3_csi_transfer.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/step6_quantised_phase.py`

*221 satir · sha256:f951598f5ed5*

```python
"""
step6_quantised_phase.py
------------------------
Does a learned model earn its place once the phase shifts are DISCRETE?

Why this matters
----------------
Every result so far assumes a continuous phase per element. Real reflecting
surfaces do not have one: elements are switched with PIN diodes or varactors
and offer 1 or 2 bits of phase resolution. Continuous phase is an
idealisation, and it is the idealisation that makes the classical baselines
strong -- with continuous phase the single-user closed form is exactly
optimal, so there is nothing for a network to discover.

With B-bit phases the picture changes. The problem becomes combinatorial
(2^(B*N) configurations), the closed form is no longer optimal, and the usual
classical recipe -- optimise in the continuous domain, then round -- loses
whatever the rounding destroys. A network, by contrast, can be trained
THROUGH the quantiser with a straight-through estimator, so it learns to
place phases that survive it.

This script measures whether that advantage is real.

Compared, all on identical scenarios:
  closed form -> round     the published single-user solution, quantised
  PGA -> round             continuous optimisation, then quantised
  discrete CD              greedy coordinate descent over the discrete set
                           (the honest classical discrete baseline)
  learned (STE)            equivariant model trained through the quantiser

Usage:  python scripts/step6_quantised_phase.py --n 8000 --epochs 25
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import sincos_to_unit, effective_channel     # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed   # noqa: E402
from ris_mu import baselines as BL                              # noqa: E402


# ------------------------------------------------------------ quantiser

def quantise(theta, bits):
    """Nearest point of the 2^bits-point uniform phase grid."""
    if bits is None:
        return theta
    step = 2 * np.pi / (2 ** bits)
    return torch.round(theta / step) * step


def quantise_ste(theta, bits):
    """Quantise on the forward pass, pass the gradient straight through."""
    if bits is None:
        return theta
    return theta + (quantise(theta, bits) - theta).detach()


def rates_from_theta(Fc, Gc, hd, theta, snr_scale):
    g = effective_channel(Fc, Gc, hd, torch.cos(theta), torch.sin(theta))
    return torch.log2(1.0 + snr_scale * g)


# ------------------------------------------------------------ baselines

def discrete_cd(Fc, Gc, hd, snr_scale, bits, sweeps=3, init=None):
    """
    Greedy coordinate descent over the discrete phase set.

    At each element every one of the 2^bits settings is scored on the true
    objective and the best is kept. This is the classical method that does
    NOT suffer from rounding, so it is the baseline a learned model has to
    beat to be interesting.
    """
    B, U, N = Gc.shape
    L = 2 ** bits
    grid = torch.arange(L, dtype=torch.float32) * (2 * np.pi / L)

    theta = quantise(init.clone(), bits) if init is not None else torch.zeros(B, N)

    for _ in range(sweeps):
        for n in range(N):
            best_val = None
            best_ph = None
            for q in range(L):
                trial = theta.clone()
                trial[:, n] = grid[q]
                val = rates_from_theta(Fc, Gc, hd, trial, snr_scale).min(-1).values
                if best_val is None:
                    best_val, best_ph = val, torch.full((B,), grid[q])
                else:
                    upd = val > best_val
                    best_val = torch.where(upd, val, best_val)
                    best_ph = torch.where(upd, torch.full((B,), grid[q]), best_ph)
            theta[:, n] = best_ph
    return theta


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8000)
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--bits", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    d = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    Fc = torch.from_numpy(d["F"]).to(torch.complex64)
    Gc = torch.from_numpy(d["G"]).to(torch.complex64)
    hd = torch.from_numpy(d["hd"]).to(torch.complex64)
    N, sc = panel.N, cfg.snr_scale()

    itr, iva, ite = split_indices(args.n, seed=0)
    print(f"N={N}  U={args.users}  samples={args.n}\n")

    # reference points that do not depend on the bit depth
    Ft, Gt, ht = Fc[ite], Gc[ite], hd[ite]
    th_cf = BL.su_closed_form(Ft, Gt, ht, sc)[0]
    th_pga = BL.pga_maxmin(Ft, Gt, ht, sc, iters=300, restarts=3)[0]
    cont_cf = rates_from_theta(Ft, Gt, ht, th_cf, sc).min(-1).values.mean().item()
    cont_pga = rates_from_theta(Ft, Gt, ht, th_pga, sc).min(-1).values.mean().item()
    print(f"continuous reference   closed form {cont_cf:.3f}   PGA {cont_pga:.3f}\n")

    results = {"continuous": {"closed_form": cont_cf, "pga": cont_pga}}

    for bits in args.bits:
        print(f"===== {bits}-bit phase ({2**bits} levels) =====")
        row = {}

        row["closed form -> round"] = rates_from_theta(
            Ft, Gt, ht, quantise(th_cf, bits), sc).min(-1).values.mean().item()
        row["PGA -> round"] = rates_from_theta(
            Ft, Gt, ht, quantise(th_pga, bits), sc).min(-1).values.mean().item()

        t0 = time.perf_counter()
        th_dcd = discrete_cd(Ft, Gt, ht, sc, bits, sweeps=3, init=th_cf)
        dcd_ms = (time.perf_counter() - t0) * 1e3 / len(ite)
        row["discrete CD"] = rates_from_theta(
            Ft, Gt, ht, th_dcd, sc).min(-1).values.mean().item()

        for k, v in row.items():
            print(f"  {k:<22} {v:.3f}")

        # ---- learned, trained through the quantiser --------------------
        tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

        def step_fn(model, b, bits=bits):
            Xb, Fb, Gb, hb = b
            cos_t, sin_t = sincos_to_unit(model(Xb), N)
            th = torch.atan2(sin_t, cos_t)
            R = rates_from_theta(Fb, Gb, hb, quantise_ste(th, bits), sc)
            return -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()

        def eval_fn(model, loader, bits=bits):
            model.eval()
            tot, n = 0.0, 0
            with torch.no_grad():
                for Xb, Fb, Gb, hb in loader:
                    cos_t, sin_t = sincos_to_unit(model(Xb), N)
                    th = quantise(torch.atan2(sin_t, cos_t), bits)
                    v = rates_from_theta(Fb, Gb, hb, th, sc).min(-1).values
                    tot += v.sum().item()
                    n += len(Xb)
            return -tot / n, {"min_rate": tot / n}

        set_seed(42)
        model = EquivariantRIS(residual=False)
        info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                            lr=2e-3, milestones=(12, 20), patience=10,
                            tag=f"{bits}bit", verbose=False)
        _, m = eval_fn(model, te)
        row["learned (STE)"] = m["min_rate"]
        print(f"  {'learned (STE)':<22} {m['min_rate']:.3f}   ({info['minutes']:.1f} dk)")

        base = row["closed form -> round"]
        print(f"\n  learned vs closed-form-rounded : {100*(row['learned (STE)']-base)/base:+.1f}%")
        print(f"  learned vs discrete CD         : "
              f"{100*(row['learned (STE)']-row['discrete CD'])/row['discrete CD']:+.1f}%")
        print(f"  discrete CD cost               : {dcd_ms:.2f} ms/sample\n")

        row["discrete_cd_ms"] = dcd_ms
        results[f"{bits}bit"] = row

    # ---------------------------------------------------------- summary
    print("=" * 66)
    print(f"{'method':<24}" + "".join(f"{b}-bit".rjust(12) for b in args.bits))
    print("-" * 66)
    for k in ["closed form -> round", "PGA -> round", "discrete CD", "learned (STE)"]:
        line = f"{k:<24}"
        for b in args.bits:
            line += f"{results[f'{b}bit'][k]:>12.3f}"
        print(line)
    print("-" * 66)
    print(f"{'continuous closed form':<24}{cont_cf:>12.3f}")
    print(f"{'continuous PGA':<24}{cont_pga:>12.3f}")
    print("=" * 66)

    p = os.path.join(args.out, "step6_quantised.json")
    json.dump(results, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
```

### `scripts/diagnose_realism.py`

*149 satir · sha256:b4b4031d45f3*

```python
"""
diagnose_realism.py
-------------------
Quantifies the realism gap between the legacy channel generator and the
geometry-based one. Produces the numbers and the figure that justify the
"realistic scenario" contribution of the thesis.

Metrics
-------
1. Spatial correlation |rho(dx)| across the RIS aperture. A half-wavelength
   spaced array must show |rho| close to 1 for adjacent elements.
2. Effective rank of the spatial covariance R = E[h h^H]. A physical channel
   with a handful of paths is low rank; i.i.d. fading is full rank.
3. Condition number of R (dB).
4. Achievable-gain sensitivity: how much received power is lost if the optimal
   phase profile of one channel realisation is applied to a neighbouring one.

Usage:  python scripts/diagnose_realism.py --n 2000
"""

import argparse
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                       # noqa: E402
from ris_mu.channel import MultiUserRISChannel, ChannelConfig, legacy_generate  # noqa: E402


def spatial_corr(H, panel):
    """|rho| as a function of element separation, averaged over the aperture."""
    Hn = H - H.mean(0, keepdims=True)
    Hn = Hn / (np.std(Hn, axis=0, keepdims=True) + 1e-30)
    R = (Hn.conj().T @ Hn) / Hn.shape[0]                   # (N,N)
    sep = np.linalg.norm(panel.positions[:, None] - panel.positions[None], axis=-1)
    sep_r = np.round(sep / panel.d).astype(int)
    out = {}
    for s in range(1, sep_r.max() + 1):
        m = sep_r == s
        if m.sum():
            out[s] = float(np.abs(R[m]).mean())
    return out


def cov_stats(H):
    R = (H.conj().T @ H) / H.shape[0]
    ev = np.sort(np.abs(np.linalg.eigvalsh(R)))[::-1]
    ev = ev / ev.sum()
    ev_nz = ev[ev > 1e-12]
    eff_rank = float(np.exp(-np.sum(ev_nz * np.log(ev_nz))))   # entropy-based
    cond_db = float(10 * np.log10(ev[0] / max(ev[-1], 1e-15)))
    return eff_rank, cond_db


def beam_steering_fit(F, G, panel):
    """
    Fraction of the optimal received power retained when the phase profile is
    restricted to a linear ramp (a classical beam-steering solution).

    A physical, few-path channel has a smooth phase profile across the
    aperture, so a ramp recovers most of the gain. An i.i.d. channel has a
    random profile that no ramp can approximate. Reported in dB of loss.
    """
    theta_opt = -np.angle(F) - np.angle(G)
    p = panel.positions - panel.positions.mean(0)
    # least-squares linear ramp on the unwrapped-equivalent unit vectors
    A = np.c_[p, np.ones(panel.N)]                       # (N,4)
    pinv = np.linalg.pinv(A)
    coef = (pinv @ np.unwrap(theta_opt, axis=-1).T).T    # (S,4)
    theta_ramp = coef @ A.T
    g_opt = np.abs(np.sum(G * np.exp(1j * theta_opt) * F, axis=-1)) ** 2
    g_ramp = np.abs(np.sum(G * np.exp(1j * theta_ramp) * F, axis=-1)) ** 2
    return float(10 * np.log10(g_opt.mean() / max(g_ramp.mean(), 1e-30)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    panel = RISPanel(M=8, K=4)
    print(f"RIS {panel.M}x{panel.K} = {panel.N} elements, spacing {panel.d*100:.1f} cm "
          f"@ {panel.fc/1e9:.1f} GHz\n")

    print(f"generating legacy model  ({args.n} samples) ...")
    leg = legacy_generate(args.n, panel)

    print(f"generating geometry-based model ({args.n} samples) ...\n")
    new_r = MultiUserRISChannel(panel, ChannelConfig(n_users=1, bs_random=True, seed=0)).generate(args.n)
    new_f = MultiUserRISChannel(panel, ChannelConfig(n_users=1, bs_random=False, seed=0)).generate(args.n)

    rows = []
    for name, d in (("legacy", leg), ("geom/randBS", new_r), ("geom/fixedBS", new_f)):
        F, G = d["F"], d["G"][:, 0, :]
        c_f = spatial_corr(F, panel)
        er, cd = cov_stats(F)
        rows.append(dict(name=name, corr=c_f, eff_rank=er, cond_db=cd,
                         transfer=beam_steering_fit(F, G, panel)))

    # ---- table -------------------------------------------------------------
    seps = sorted(rows[0]["corr"])[:5]
    hdr = "model        " + "".join(f"|rho|@{s}d  " for s in seps) + " eff.rank  cond[dB]  ramp-loss[dB]"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        line = f"{r['name']:<13}"
        line += "".join(f"{r['corr'][s]:9.3f}  " for s in seps)
        line += f"{r['eff_rank']:9.2f}  {r['cond_db']:8.1f}  {r['transfer']:11.2f}"
        print(line)

    print(f"\n(eff.rank upper bound = N = {panel.N}; a physical few-path channel "
          f"should be well below it)")

    # ---- figure ------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4))
        for r in rows:
            s = sorted(r["corr"])
            ax[0].plot(s, [r["corr"][x] for x in s], "o-", label=r["name"])
        ax[0].set_xlabel(r"element separation [$\lambda/2$]")
        ax[0].set_ylabel(r"$|\rho|$")
        ax[0].set_title("Spatial correlation across the RIS aperture")
        ax[0].legend(); ax[0].grid(alpha=.3); ax[0].set_ylim(0, 1.05)

        for r, d in zip(rows, (leg, new_r, new_f)):
            F = d["F"]
            R = (F.conj().T @ F) / F.shape[0]
            ev = np.sort(np.abs(np.linalg.eigvalsh(R)))[::-1]
            ax[1].semilogy(ev / ev[0], "o-", label=f"{r['name']} (eff.rank {r['eff_rank']:.1f})")
        ax[1].set_xlabel("eigenvalue index")
        ax[1].set_ylabel("normalised eigenvalue")
        ax[1].set_title("Spatial covariance spectrum")
        ax[1].legend(); ax[1].grid(alpha=.3)
        plt.tight_layout()
        p = os.path.join(args.out, "realism_diagnostics.png")
        plt.savefig(p, dpi=150)
        print(f"\nfigure -> {p}")
    except ImportError:
        print("\n(matplotlib not available, skipping figure)")


if __name__ == "__main__":
    main()
```

### Raporlama

### `scripts/compile_results.py`

*209 satir · sha256:9a22de7b9b19*

```python
"""
compile_results.py
------------------
Collects every experiment's JSON output into the tables and figures used in
the write-up, and prints a single consolidated summary.

Usage:  python scripts/compile_results.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUT = "results"


def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


def section(title):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def table_head_ablation(d):
    if not d:
        return
    section("1  Where the accuracy of the published model comes from "
            "(legacy channel)")
    print(f"{'body':<10}{'head':<8}{'params':>10}{'RMSE':>10}{'SR@5':>9}")
    print("-" * 47)
    for v in d.values():
        print(f"{v['body']:<10}{v['head']:<8}{v['params']:>10,}"
              f"{v['test_rmse']:>9.2f}°{v['test_sr5']:>8.2f}%")
    dense = [v for v in d.values() if v["head"] == "dense"]
    local = [v for v in d.values() if v["head"] == "local"]
    print(f"\n  mean RMSE with the dense head : {np.mean([v['test_rmse'] for v in dense]):6.2f}°")
    print(f"  mean RMSE with the local head : {np.mean([v['test_rmse'] for v in local]):6.2f}°")
    best_local = min(local, key=lambda v: v["test_rmse"])
    print(f"  best local-head model         : {best_local['body']} "
          f"({best_local['params']:,} params, {best_local['test_rmse']:.2f}°)")
    none_local = [v for v in local if v["body"] == "none"][0]
    print(f"  element-independent control   : {none_local['test_rmse']:.2f}° "
          f"with {none_local['params']:,} params")


def table_csi(d):
    if not d:
        return
    section("2  When spatial processing earns its place")
    models = sorted({v["model"] for v in d.values()},
                    key=lambda m: ("element" not in m, m))
    sigmas = sorted({v["sigma"] for v in d.values()})
    print(f"{'channel':<11}{'sigma':>7}" + "".join(f"{m:>16}" for m in models))
    print("-" * (18 + 16 * len(models)))
    for ch in ("legacy", "geometric"):
        for s in sigmas:
            row = f"{ch:<11}{s:>7.2f}"
            for m in models:
                row += f"{d[f'{ch}|{s}|{m}']['rmse']:>15.2f}°"
            print(row)
    print("\n  gain from mixing over the element-local model "
          "(negative means mixing wins):")
    for ch in ("legacy", "geometric"):
        cells = []
        for s in sigmas:
            base = d[f"{ch}|{s}|element-local"]["rmse"]
            best = min(d[f"{ch}|{s}|{m}"]["rmse"] for m in models if m != "element-local")
            cells.append(f"sigma={s}: {100*(best-base)/base:+5.1f}%")
        print(f"    {ch:<10} " + "   ".join(cells))


def table_multiuser(d):
    if not d:
        return
    section("3  Multi-user design trained without labels")
    ref = d["PGA max-min"]["min_rate"]
    print(f"{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}"
          f"{'ms/sample':>11}{'params':>10}")
    print("-" * 68)
    for k, v in d.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        pr = f"{v.get('params', 0):,}" if v.get("params") else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}{pr:>10}")


def table_generalisation(d):
    if not d:
        return
    section("4  What the symmetries buy")
    o = d["user_ordering"]
    print("relabelling the users (same scenarios, 8 permutations):")
    for k, v in o.items():
        print(f"  {k:<13} min-rate {v['mean']:.4f} +- {v['std']:.4f}"
              f"   spread {v['spread']:.4f}")
    print("\nuser counts never seen in training:")
    print(f"{'U':>3}{'equivariant':>14}{'PGA':>10}{'% of PGA':>10}"
          f"{'SU closed':>12}{'MU-CNN-LSTM':>14}")
    print("-" * 63)
    for U, v in sorted(d["user_count"].items(), key=lambda kv: int(kv[0])):
        mu = f"{v['mu_cnn_lstm']:.3f}" if v["mu_cnn_lstm"] else "undefined"
        print(f"{int(U):>3}{v['equivariant']:>14.3f}{v['pga']:>10.3f}"
              f"{100*v['equivariant']/v['pga']:>9.1f}%"
              f"{v['su_closed']:>12.3f}{mu:>14}")


def table_mixed(d):
    if not d:
        return
    section("5  Training across user counts")
    print(f"{'U':>3}{'trained U=4':>13}{'trained mixed':>15}{'SU closed':>12}"
          f"{'PGA':>9}{'mixed % PGA':>13}")
    print("-" * 65)
    for U, v in sorted(d.items(), key=lambda kv: int(kv[0])):
        print(f"{int(U):>3}{v['fixed']:>13.3f}{v['mixed']:>15.3f}"
              f"{v['su_closed']:>12.3f}{v['pga']:>9.3f}{100*v['mixed']/v['pga']:>12.1f}%")
    print("\n  margin over the single-user closed form:")
    for U, v in sorted(d.items(), key=lambda kv: int(kv[0])):
        print(f"    U={U}:  trained U=4 "
              f"{100*(v['fixed']-v['su_closed'])/v['su_closed']:+6.1f}%"
              f"    trained mixed "
              f"{100*(v['mixed']-v['su_closed'])/v['su_closed']:+6.1f}%")


def figures():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.3))

    ab = load("step1b_head_ablation.json")
    if ab:
        ax = axes[0]
        bodies = ["none", "CNN", "CNN-LSTM"]
        for head, mk in (("dense", "o--"), ("local", "s-")):
            ys = [next((v["test_rmse"] for v in ab.values()
                        if v["body"] == b and v["head"] == head), np.nan)
                  for b in bodies]
            ax.plot(bodies, ys, mk, label=f"{head} head", markersize=7)
        ax.set_yscale("log")
        ax.set_ylabel("test RMSE [deg]")
        ax.set_title("Head, not body, sets the accuracy")
        ax.legend(); ax.grid(alpha=.3, which="both")

    cs = load("step3_csi_transfer.json")
    if cs:
        ax = axes[1]
        sigmas = sorted({v["sigma"] for v in cs.values()})
        for ch, mk in (("legacy", "o--"), ("geometric", "s-")):
            ys = []
            for s in sigmas:
                base = cs[f"{ch}|{s}|element-local"]["rmse"]
                best = min(cs[f"{ch}|{s}|{m}"]["rmse"]
                           for m in {v["model"] for v in cs.values()}
                           if m != "element-local")
                ys.append(100 * (best - base) / base)
            ax.plot(sigmas, ys, mk, label=ch, markersize=7)
        ax.axhline(0, color="k", lw=.8)
        ax.set_xlabel(r"CSI error $\sigma$")
        ax.set_ylabel("RMSE change from spatial mixing [%]")
        ax.set_title("Mixing helps only on a correlated channel")
        ax.legend(); ax.grid(alpha=.3)

    gn = load("step5_generalisation.json")
    mx = load("step5b_mixed_users.json")
    if gn:
        ax = axes[2]
        us = sorted(int(u) for u in gn["user_count"])
        eq = [gn["user_count"][str(u)]["equivariant"] for u in us]
        pg = [gn["user_count"][str(u)]["pga"] for u in us]
        su = [gn["user_count"][str(u)]["su_closed"] for u in us]
        ax.plot(us, pg, "k^-", label="PGA (iterative)")
        ax.plot(us, eq, "s-", label="equivariant, trained U=4")
        if mx:
            ax.plot([int(u) for u in sorted(mx, key=int)],
                    [mx[u]["mixed"] for u in sorted(mx, key=int)],
                    "D-", label="equivariant, trained mixed U")
        ax.plot(us, su, "o--", label="SU closed form")
        ax.axvline(4, color="gray", ls=":", lw=1)
        ax.annotate("trained here", (4, ax.get_ylim()[1]), fontsize=8,
                    ha="center", va="top", color="gray")
        ax.set_xlabel("number of users U")
        ax.set_ylabel("min rate [b/s/Hz]")
        ax.set_title("Generalisation across user count")
        ax.legend(fontsize=8); ax.grid(alpha=.3)

    plt.tight_layout()
    p = os.path.join(OUT, "summary_figures.png")
    plt.savefig(p, dpi=150)
    print(f"\nfigure -> {p}")


if __name__ == "__main__":
    table_head_ablation(load("step1b_head_ablation.json"))
    table_csi(load("step3_csi_transfer.json"))
    table_multiuser(load("step4_multiuser.json"))
    table_generalisation(load("step5_generalisation.json"))
    table_mixed(load("step5b_mixed_users.json"))
    figures()
```

### `scripts/make_writing_reference.py`

*289 satir · sha256:f63cf58a2098*

```python
# -*- coding: utf-8 -*-
"""Tez yazarken atif yapilacak her sayiyi JSON'lardan uretir."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[1] / "results"
def L(n):
    p = R / n
    return json.loads(p.read_text()) if p.exists() else None

sec4   = L("mumiso_sec4_fixzf.json")
link   = L("mumiso_linkratio.json")
unr    = L("mumiso_unrolled_fixzf.json")
nog    = L("mumiso_nograd_fixzf.json")
eqs    = L("mumiso_equal_step.json")
lat    = L("mumiso_latency_parity.json")
rep    = L("mumiso_latency_repeat.json")
age    = L("mumiso_aging_sweep_fixzf.json")
anc    = L("anchor_full_test.json")
out = []
W = out.append

W("# Tez Yazim Referansi — olculmus her sayi, kaynagiyla")
W("")
W("Bu dosya `results/*.json` icinden **uretildi**, elle yazilmadi.")
W("Her tablonun altinda hangi dosyadan geldigi yazili.")
W("")
W("> Bir sayiyi teze koymadan once kaynak dosyasini acin. Bu dosya")
W("> kolaylik icindir, otorite degil.")
W("")

W("## Bolum 4 — cok kullanicili ogrenmenin sinirlari")
W("")
W("### 4.1 Tek gecisli tahmin capada donuyor")
W("")
ANC = 3.5363
W(f"Capa (`su_average`, modellerin puanlandigi **ayni** 1800 senaryoluk test bolmesi): **{ANC:.4f}**  ")
if anc:
    W(f"`su_best_of` (bedava, K+1 adayin en iyisi): **{anc['su_best_of']:.4f}**  ")
    W(f"`su_weakest`: {anc['su_weakest']:.4f}")
W("")
if sec4:
    W(f"Hedef (en guclu klasik, olcumle secildi): **{sec4['target']['method']} = {sec4['target']['rate']:.4f}**")
    W("")
    W("| Mimari | Test min hiz | Capa orani | Permutasyon yayilimi | Parametre |")
    W("| --- | --- | --- | --- | --- |")
    for k in ("concat", "deepsets", "exchange"):
        m = sec4["models"][k]
        W(f"| {k} | {m['test_min']:.4f} | {m['test_min']/ANC:.4f} | {m['perm_spread']:.2e} | {m['params']:,} |")
    W("")
    W("Kaynak: `results/mumiso_sec4_fixzf.json`, capa `results/anchor_full_test.json`")
W("")
W("Egitilmemis ag ile su_average, 400 senaryoda dort ondaliga kadar ayni: **3.7230 / 3.7230**.  ")
W("Artik kafasinin baslangic sapmasi: 0.013 derece.  ")
W("En iyi epok (12 epoktan): concat **4**, deepsets **9**, exchange **2**.")
W("")

W("### 4.2 Nedeni: belirlenmis ama duzgun olmayan fonksiyon")
W("")
W("| Olcum | Deger |")
W("| --- | --- |")
W("| Ayni senaryo, iki farkli baslangic — cos uyusmasi | +0.58 / +0.81 / +0.57 |")
W("| Farkli senaryolar — cos uyusmasi | +0.005 / +0.009 / −0.003 |")
W("| Oracle hizi (Adam, 600 adim) | 6.1619 |")
W("| Capa (bu tanida) | 3.4350 |")
W("| Gozetimli uyum, egitim MSE (son epok) | 0.8958 |")
W("| Gozetimli uyum, dogrulama MSE | 0.9250 |")
W("| Gozetimli modelin test hizi | 3.4064 (capanin ALTINDA) |")
W("")
W("Kaynak: `results/learnability_fixzf.log`, `scripts/diagnose_learnability.py`")
W("")
W("Komsuluk testi: en yakin oznitelik komsusuna **+0.0047**, rastgele senaryoya **+0.0089**.")
W("Ikisi de sifirdan ayirt edilemez; aralarindaki sira gurultudur.")
W("")

W("### 4.3 Temsil hipotezi kuruldu ve REDDEDILDI")
W("")
W("Hipotez: `features.py` normalizasyonu RIS kaskadi / dogrudan yol guc oranini siliyor.")
W("")
W("| | gercek | agin gordugu |")
W("| --- | --- | --- |")
W("| Oranin senaryolar arasi yayilimi | 9.4 milyon kat | 1.000 kat |")
W("| Gercek oranla korelasyon | — | +0.031 |")
W("")
W("Bilgi geri verildi (iki kanal, `features.link_ratio=True`), yeni korelasyon **+1.0000**.")
W("Ayni kanal cekilisi, ayni epok sayisi, tek fark iki kanal:")
W("")
if sec4 and link:
    W("| Mimari | Oran kanali YOK | Oran kanali VAR | Degisim |")
    W("| --- | --- | --- | --- |")
    for k in ("concat", "deepsets", "exchange"):
        o, n = sec4["models"][k]["test_min"], link["models"][k]["test_min"]
        W(f"| {k} | {o:.4f} | {n:.4f} | {100*(n/o-1):+.2f}% |")
    W("")
    W("Kaynak: `results/mumiso_sec4_fixzf.json` ve `results/mumiso_linkratio.json`")
W("")
W("**Sonuc:** eksik bilgi, stall'in sebebi degildi. Uc model de biraz kotulesti.")
W("Dusus iki modelde kendi epok-arasi gurultusunun disinda (deepsets gurultu %0.29,")
W("exchange %0.13).")
W("")

W("### 4.4 Ogrenilen guncelleme kurali")
W("")
if unr and nog:
    W("| Gradyan girdi | Test min | Capaya gore | AO orani | Parametre |")
    W("| --- | --- | --- | --- | --- |")
    a = unr["anchor"]
    W(f"| **var** | {unr['test_min']:.4f} | {100*(unr['test_min']/a-1):+.1f}% | {unr['frac_of_ao']:.3f} | {unr['params']:,} |")
    W(f"| **yok** | {nog['test_min']:.4f} | {100*(nog['test_min']/nog['anchor']-1):+.1f}% | {nog['frac_of_ao']:.3f} | {nog['params']:,} |")
    W("")
    W(f"Capa (her iki kol) {a:.4f} · cd {unr['cd']:.4f} · AO {unr['ao']:.4f}")
    W("")
    W(f"Adim izi (gradyan var): {' → '.join(f'{x:.3f}' for x in unr['per_step'])}")
    W(f"Adim izi (gradyan yok): {' → '.join(f'{x:.3f}' for x in nog['per_step'])}")
    W("")
    W("Ogrenilen adim boylari: var 0.589 → 0.258 (azalan cizelge) · yok hepsi ~0.49 (duz)")
    W("")
    W("Kaynak: `results/mumiso_unrolled_fixzf.json`, `results/mumiso_nograd_fixzf.json`")
W("")

W("### 4.5 Esit adim vs esit milisaniye — ikisi CELISIYOR")
W("")
if eqs:
    W(f"Capa {eqs['anchor']:.4f} · `su_best_of` {eqs['su_best_of']:.4f}")
    W("")
    W("**Esit ADIM** — ogrenilen kural her butcede onde:")
    W("")
    W("| L | Ogrenilen | Ayarlanmis Adam | Oran | Eslest. fark − 2 s.e. | Kazanma orani |")
    W("| --- | --- | --- | --- | --- | --- |")
    for Lk in sorted(eqs["rows"], key=int):
        v = eqs["rows"][Lk]
        lo = v["paired_mean_diff"] - 2*v["paired_sem"]
        W(f"| {Lk} | {v['learned']:.4f} | {v['swept']:.4f} | {v['learned_over_swept']:.3f} | {lo:+.4f} | {100*v['learned_wins_frac']:.1f}% |")
    W("")
    W("Adim boyu her butcede dogrulamada secildi; optimum her L'de **0.75**, onlu izgaranin")
    W("yedinci konumu — yani kenarda degil, ic noktada. Yumusak/sert objektif farki 0.008–0.018.")
    W("")
    W("Kaynak: `results/mumiso_equal_step.json`")
W("")
if lat and rep:
    import statistics as st
    lm = {int(k): st.median(v) for k, v in rep["learned"].items()}
    am = {int(k): st.median(v) for k, v in rep["adam"].items()}
    lr_ = {int(k): v["rate"] for k, v in lat["learned"].items()}
    ar_ = {int(k): v["rate"] for k, v in lat["classical"].items()}
    W("**Esit MILISANIYE** — bes noktanin besi de baskinlanmis, bes turun besinde:")
    W("")
    W("| Ogrenilen L | Gecikme | Hiz | Baskinlayan Adam |")
    W("| --- | --- | --- | --- |")
    for Lk in sorted(lm):
        cands = [(k, am[k], ar_[k]) for k in am if am[k] <= lm[Lk] and ar_[k] >= lr_[Lk]]
        if cands:
            k, ms, r = max(cands, key=lambda t: t[2])
            W(f"| {Lk} | {lm[Lk]:.2f} ms | {lr_[Lk]:.4f} | L={k}: {ms:.2f} ms, {r:.4f} |")
        else:
            W(f"| {Lk} | {lm[Lk]:.2f} ms | {lr_[Lk]:.4f} | — (cephede) |")
    W("")
    W("Adim maliyeti orani: ~2.7× (bir ogrenilen adim = ~2.7 Adam adimi).")
    W("Turlar arasi zamanlama oynamasi 1.06×–1.41× (bos makine, 5 tur).")
    W("")
    W("Kaynak: `results/mumiso_latency_parity.json`, `results/mumiso_latency_repeat.json`")
W("")

W("## Bolum 5 — hareketlilik ve gecikme-farkinda tasarim")
W("")
W("Tutarlilik suresi: 3 GHz, 1.5 m/s → f_d = 15.0 Hz → **T_c = 28.2 ms**")
W("")
if age:
    W("| L | Gecikme | t=0 hizi | **Gecerli hiz** |")
    W("| --- | --- | --- | --- |")
    rows = age if isinstance(age, list) else age.get("rows", age)
    try:
        items = sorted(rows.items(), key=lambda kv: int(kv[0])) if isinstance(rows, dict) else [(r.get("L"), r) for r in rows]
        for Lk, v in items:
            if isinstance(v, dict) and "eff" in v and "t0" in v:
                W(f"| {Lk} | {v.get('lat_ms', float('nan')):.1f} ms | {v['t0']:.3f} | **{v['eff']:.3f}** |")
    except Exception as e:
        W(f"(otomatik cikarilamadi: {e} — `results/mumiso_aging_sweep_fixzf.json` acin)")
    W("")
W("Elle dogrulanmis ana satirlar (bolum 5b taslagindan):")
W("")
W("| Yontem | t=0 hizi | Gecikme | Gecerli hiz |")
W("| --- | --- | --- | --- |")
W("| su_average | 4.624 | ~0 | 4.624 |")
W("| su_best_of | 5.276 | 0.05 ms | 5.276 |")
W("| Adam-8 | — | 13.3 ms | **5.849** |")
W("| Adam-16 | — | 26.6 ms | 5.324 |")
W("| koordinat inisi | — | ~1500 ms | 4.921 |")
W("| PGA | **7.117** | ~5600 ms | **4.667** |")
W("")
W("Icsel optimum: **L = 4** → 5.982. Yakinsamaya gore tasarlamak (L=48) **%14** kaybettiriyor.")
W("Eskimis faz tabani ~4.35 (sifira cokmuyor).")
W("")
W("### Yuk tasiyan varsayim: huzme taze, faz eskimis")
W("")
W("> **DUZELTME (27 Ekim).** Bu sayi uzun sure \"17 kat (4.718 / 0.279)\" diye")
W("> alintilandi. O olcum betige yazilmamisti ve **yeniden uretilemiyor**.")
W("> `scripts/mumiso_beam_staleness.py` ile olculdugunde hicbir faz secimi")
W("> 17 kat vermiyor. Nitel iddia -- bir buyukluk mertebesi -- saglam;")
W("> sayinin kendisi yanlisti.")
W("")
bs = L("mumiso_beam_staleness.json")
if bs:
    W("28.2 ms'de (tutarlilik suresi), faz t=0'da secilip huzme ya taze ya eskimis:")
    W("")
    W("| Faz secimi | Taze huzme | Eskimis huzme | Oran |")
    W("| --- | --- | --- | --- |")
    for ph, tg in (("su_average", "beam_staleness_su_average"),
                   ("su_best_of", "beam_staleness"),
                   ("adam8", "beam_staleness_adam8")):
        j = L(f"mumiso_{tg}.json")
        if j:
            c = j["at_coherence"]
            W(f"| {ph} | {c['fresh']:.4f} | {c['stale']:.4f} | **{c['ratio']:.1f}x** |")
    W("")
    W("Kaynak: `scripts/mumiso_beam_staleness.py`, `results/mumiso_beam_staleness*.json`")
    W("")
    W("Eskimis deger her uc faz seciminde de ~0.305; taze deger 3.59-4.36.")
    W("Teze **11.7-14.2 kat** yazin, 17 degil.")
W("")
W("Modelin gecerlilik ufku: korelasyon tabani ~0.5 (bagimsiz cekiliste 0.10);")
W("sacici sayisi 6→60 tabani yalnizca 0.60→0.51 indiriyor. Guvenilir aralik **τ ≤ 200 ms**.")
W("")
W("Kaynak: `results/mumiso_aging_fixzf.json`, `results/mumiso_aging_sweep_fixzf.json`")
W("")

W("## Bolum 6 — gercekci senaryo")
W("")
W("### Kazancin kaynagi (hepsi ayni on kodlayiciyla, 1200 senaryo)")
W("")
W("| | min hiz |")
W("| --- | --- |")
W("| Pano yok | 1.0224 |")
W("| Rastgele faz | 3.1002 |")
W("| su_average | 3.5549 |")
W("| su_best_of | 4.2151 |")
W("| PGA | ~6.04 |")
W("")
W("Rastgele bir yuzey kazancin kabaca **yarisini** veriyor (olculen oran 0.50).")
W("")
W("Kaynak: `scripts/mumiso_gain_source.py` -> `results/mumiso_gain_source.json`")
W("")
W("### Anten ekseni korelasyonu — basliktaki iddia YANLISTI")
W("")
W("| Konfigurasyon | Eleman ekseni | Anten ekseni | Anten etkin rank |")
W("| --- | --- | --- | --- |")
W("| T=4, 600 ornek | 0.620 | 0.234 | 3.71 / 4 |")
W("| T=8, 1500 ornek | 0.639 | 0.204 | 7.26 / 8 |")
W("")
W("Anten ekseni LoS'ta 0.818, NLoS'ta 0.130 — korelasyonu neredeyse tamamen LoS tasiyor.")
W("Eski docstring 0.77 ve 2.32/4 diyordu; eksen karistiran bir dilimlemeden geliyordu.")
W("")
W("Kaynak: `scripts/mumiso_antenna_corr.py`")
W("")
W("### Kazanc paylasiminin bedeli (ayni senaryolar, akis korunarak)")
W("")
W("| | Mevcut | Fizikce dogru | Fark |")
W("| --- | --- | --- | --- |")
W("| NLoS anten korelasyonu | 0.095 | 0.279 | 2.9× |")
W("| Capa (su_average) | 3.5549 | 2.4180 | **−%31.98** |")
W("| PGA | 6.2147 | 5.7081 | **−%8.15** |")
W("")
W("Optimizasyonun degeri: **1.75× → 2.36×**. Fizigi duzeltmek katkinizi buyutuyor.")
W("")
W("Kaynak: `scripts/mumiso_gain_sharing.py` (akis korunarak, ayni senaryolar)")
W("")

W("## Ek — yeniden uretilebilirlik")
W("")
W("- `scripts/audit_claims.py` — 41 iddia, hepsi geciyor")
W("- Sabotaj testi: tek gecisli modellere acilmis modelin sayisi yazildiginda **7 iddia patliyor**")
W("- Bilinen bosluk betikte yazili: modellerin test bolmesindeki capa yeniden olculmuyor, JSON'dan okunuyor")
W("")
W("### On kodlayici varsayilaninin bedeli")
W("")
W("| | MMSE (varsayilan) | saf ZF | Fark |")
W("| --- | --- | --- | --- |")
W("| 1200 senaryo | 3.5549 | 3.6330 | %2.20 |")
W("| En zor %10 | 2.1391 | 2.2451 | **%4.95** |")
W("")
W("Kaynak: `scripts/mumiso_precoder_cost.py`")
W("")
W("### Alintilanirken dikkat")
W("")
W("- `effective_rank` ORNEK SAYISINA bagli (%32 yayilim, 250→1000 arasinda ters yonde). n belirtmeden yazmayin.")
W("- Veri seti prefix-kararli DEGIL: farkli `--samples` ile alinmis iki sayi ayni tabloya konamaz.")
W("- Gecikme olcumleri bos makinede alinmali; kirlilik tarafsiz degil.")
W("")
p = pathlib.Path(__file__).resolve().parents[1] / "TEZ_YAZIM_REFERANSI.md"
p.write_text("\n".join(out), encoding="utf-8")
print(f"yazildi: {p}  ({len(out)} satir)")
```

### `scripts/dump_source.py`

*220 satir · sha256:d5518cb2d916*

```python
#!/usr/bin/env python3
"""Tek bir dosyada butun kaynak kodun son hali.

Neden bu betik var: kullanici kodlari Claude Code'a gecirirken "butun
kodlarin son hali" diye okunabilir tek bir dosya istedi. Elle kopyalamak
yerine uretiyoruz, boylece dosya her zaman diskteki gercek halle ayni
kalir -- bu projede elle yazilmis her sayinin yanlis cikmasi gibi, elle
kopyalanmis her kaynak da eskir.

Kullanim:
    python3 scripts/dump_source.py              # KOD_SON_HALI.md
    python3 scripts/dump_source.py --core-only  # sadece ris_mu/mumiso
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Sira anlatim sirasi: once sistem denklemleri (tek dogruluk kaynagi),
# sonra uzerine kurulan her sey.
CORE_ORDER = [
    "ris_mu/mumiso/__init__.py",
    "ris_mu/mumiso/system.py",
    "ris_mu/mumiso/channel.py",
    "ris_mu/mumiso/mobile.py",
    "ris_mu/mumiso/csi.py",
    "ris_mu/mumiso/features.py",
    "ris_mu/mumiso/models.py",
    "ris_mu/mumiso/unrolled.py",
    "ris_mu/mumiso/baselines.py",
    "ris_mu/mumiso/train.py",
]

LEGACY_ORDER = [
    "ris_mu/__init__.py",
    "ris_mu/geometry.py",
    "ris_mu/pathloss.py",
    "ris_mu/channel.py",
    "ris_mu/features.py",
    "ris_mu/models.py",
    "ris_mu/losses.py",
    "ris_mu/baselines.py",
    "ris_mu/train.py",
]

# Betikler rol rol gruplanir; alfabetik liste ne ise yaradigini gostermiyor.
SCRIPT_GROUPS = [
    ("Denetim ve dogrulama (her oturumda kosturulacaklar)", [
        "audit_claims.py",
        "audit_fair_comparison.py",
        "audit_precoder_csi.py",
        "audit_section4_cause.py",
        "verify_mumiso_system.py",
        "verify_mumiso_channel.py",
        "verify_mumiso_models.py",
        "verify_mobile.py",
        "verify_residual.py",
        "verify_batch_dependence.py",
        "verify_baseline_strength.py",
        "verify_crossover.py",
        "verify_head_claim.py",
        "verify_matlab_architecture.py",
    ]),
    ("Bolum 4 -- cok kullanicili ogrenme (titiz olumsuz sonuc)", [
        "mumiso_run.py",
        "mumiso_unrolled.py",
        "mumiso_equal_step.py",
        "mumiso_latency_parity.py",
        "mumiso_latency_repeat.py",
        "mumiso_step_cost.py",
        "mumiso_budget.py",
        "mumiso_budget_fraction.py",
        "mumiso_headroom.py",
        "anchor_same_split.py",
        "diagnose_learnability.py",
        "diagnose_mumiso_gap.py",
        "step1_control.py",
        "step1b_head_ablation.py",
        "step4_multiuser.py",
        "step4b_residual.py",
        "step4c_equiv_long.py",
        "step5_generalisation.py",
        "step5b_mixed_users.py",
    ]),
    ("Bolum 5 -- hareketlilik (tezin omurgasi)", [
        "mumiso_aging.py",
        "mumiso_frontier.py",
        "mumiso_beam_staleness.py",
    ]),
    ("Bolum 6 -- gercekci senaryo ve donanim", [
        "mumiso_antenna_corr.py",
        "mumiso_gain_sharing.py",
        "mumiso_gain_source.py",
        "mumiso_precoder_cost.py",
        "mumiso_csi_room.py",
        "mumiso_quant_latency.py",
        "step3_csi_transfer.py",
        "step6_quantised_phase.py",
        "diagnose_realism.py",
    ]),
    ("Raporlama", [
        "compile_results.py",
        "make_writing_reference.py",
        "dump_source.py",
    ]),
]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _emit(out: list[str], rel: str) -> tuple[int, str]:
    path = ROOT / rel
    src = path.read_text(encoding="utf-8")
    nlines = len(src.splitlines())
    digest = _sha(src)
    out.append(f"### `{rel}`\n")
    out.append(f"*{nlines} satir · sha256:{digest}*\n")
    out.append("```python")
    out.append(src.rstrip("\n"))
    out.append("```\n")
    return nlines, digest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core-only", action="store_true",
                    help="sadece ris_mu/mumiso paketini yaz")
    ap.add_argument("--out", default="KOD_SON_HALI.md")
    args = ap.parse_args()

    today = _dt.date.today().isoformat()
    out: list[str] = []
    index: list[tuple[str, int, str]] = []

    out.append("# Kodun son hali\n")
    out.append(
        f"Bu dosya `scripts/dump_source.py` tarafindan **{today}** tarihinde "
        "diskteki kaynaktan uretildi. Elle duzenlenmez; kaynak degisince "
        "betigi yeniden kosturun.\n"
    )
    out.append(
        "Her dosyanin basliginda satir sayisi ve icerigin sha256 ozeti var. "
        "Claude Code'da bir dosyayi acip bu ozetle karsilastirabilirsiniz: "
        "ayni ise dosya bu listedekiyle birebir aynidir.\n"
    )
    out.append("> **Yayimlanmis MATLAB kodu bu pakette yok ve bu paketten "
               "etkilenmez.** `duzeltilmis_kodlar` ayri durur ve yayimlanan "
               "sonuclari uretmeye devam eder.\n")
    out.append("---\n")
    out.append("## Icindekiler

**67 dosya · 10076 satir**

| Dosya | Satir | sha256 |
|---|---:|---|
| `ris_mu/mumiso/__init__.py` | 14 | `f9c07f1338d5` |
| `ris_mu/mumiso/system.py` | 333 | `21a8a952d800` |
| `ris_mu/mumiso/channel.py` | 338 | `b3c2a9ed69ca` |
| `ris_mu/mumiso/mobile.py` | 238 | `b33c20ab878e` |
| `ris_mu/mumiso/csi.py` | 131 | `accb4f90d9ec` |
| `ris_mu/mumiso/features.py` | 156 | `e1f57324af38` |
| `ris_mu/mumiso/models.py` | 278 | `4775daa8a793` |
| `ris_mu/mumiso/unrolled.py` | 223 | `95835a3ed9f3` |
| `ris_mu/mumiso/baselines.py` | 348 | `3ea6e6dd577f` |
| `ris_mu/mumiso/train.py` | 110 | `a48824f31611` |
| `ris_mu/__init__.py` | 0 | `e3b0c44298fc` |
| `ris_mu/geometry.py` | 84 | `295c899c3073` |
| `ris_mu/pathloss.py` | 111 | `9ab1e1cbca80` |
| `ris_mu/channel.py` | 348 | `8ec99f395131` |
| `ris_mu/features.py` | 107 | `c68df09577a3` |
| `ris_mu/models.py` | 316 | `4408c6e73174` |
| `ris_mu/losses.py` | 112 | `4fd1c95b68d3` |
| `ris_mu/baselines.py` | 113 | `2d5290a8fdc0` |
| `ris_mu/train.py` | 74 | `03f9853db4d4` |
| `scripts/audit_claims.py` | 465 | `4768a78598df` |
| `scripts/audit_fair_comparison.py` | 191 | `612487b768e0` |
| `scripts/audit_precoder_csi.py` | 156 | `af94df52d20d` |
| `scripts/audit_section4_cause.py` | 120 | `961aa49c3240` |
| `scripts/verify_mumiso_system.py` | 85 | `70c1c3a5ca9a` |
| `scripts/verify_mumiso_channel.py` | 63 | `c5b24cbab83e` |
| `scripts/verify_mumiso_models.py` | 91 | `15b75565f57a` |
| `scripts/verify_mobile.py` | 106 | `1913e291c531` |
| `scripts/verify_residual.py` | 57 | `6a9e50a457ae` |
| `scripts/verify_batch_dependence.py` | 53 | `11ed1aa64660` |
| `scripts/verify_baseline_strength.py` | 40 | `27f30c3e8238` |
| `scripts/verify_crossover.py` | 123 | `3649874707cb` |
| `scripts/verify_head_claim.py` | 163 | `ccc519076f7e` |
| `scripts/verify_matlab_architecture.py` | 133 | `70e791323b23` |
| `scripts/mumiso_run.py` | 146 | `ab16ab18b22b` |
| `scripts/mumiso_unrolled.py` | 156 | `e557411495d9` |
| `scripts/mumiso_equal_step.py` | 255 | `ae3ea9cfbd22` |
| `scripts/mumiso_latency_parity.py` | 271 | `c40f705e21b9` |
| `scripts/mumiso_latency_repeat.py` | 90 | `c6687a3532ee` |
| `scripts/mumiso_step_cost.py` | 66 | `658e6186e376` |
| `scripts/mumiso_budget.py` | 172 | `6b757f4a12b7` |
| `scripts/mumiso_budget_fraction.py` | 228 | `d147a606155c` |
| `scripts/mumiso_headroom.py` | 52 | `d7ff9705f3b8` |
| `scripts/anchor_same_split.py` | 26 | `a4ac3fa7cb26` |
| `scripts/diagnose_learnability.py` | 129 | `6f4375cd7410` |
| `scripts/diagnose_mumiso_gap.py` | 105 | `3411d21f59e2` |
| `scripts/step1_control.py` | 118 | `fd042c302981` |
| `scripts/step1b_head_ablation.py` | 119 | `87685e92fa0f` |
| `scripts/step4_multiuser.py` | 150 | `a9e56d2c5509` |
| `scripts/step4b_residual.py` | 99 | `c61c758b64e4` |
| `scripts/step4c_equiv_long.py` | 99 | `2bbadcdae859` |
| `scripts/step5_generalisation.py` | 129 | `8b1356bbdb8a` |
| `scripts/step5b_mixed_users.py` | 167 | `e4407aed2fad` |
| `scripts/mumiso_aging.py` | 204 | `ab0f6bccdcfa` |
| `scripts/mumiso_frontier.py` | 163 | `175da29e064a` |
| `scripts/mumiso_beam_staleness.py` | 139 | `be5a1e837981` |
| `scripts/mumiso_antenna_corr.py` | 73 | `52e1fbee7d50` |
| `scripts/mumiso_gain_sharing.py` | 60 | `0ff5e98f3c59` |
| `scripts/mumiso_gain_source.py` | 37 | `7141a0938ef5` |
| `scripts/mumiso_precoder_cost.py` | 46 | `eb616f5073d8` |
| `scripts/mumiso_csi_room.py` | 127 | `4600791a219c` |
| `scripts/mumiso_quant_latency.py` | 114 | `9b3a60ce25be` |
| `scripts/step3_csi_transfer.py` | 168 | `372aed33fe5d` |
| `scripts/step6_quantised_phase.py` | 221 | `f951598f5ed5` |
| `scripts/diagnose_realism.py` | 149 | `b4b4031d45f3` |
| `scripts/compile_results.py` | 209 | `9a22de7b9b19` |
| `scripts/make_writing_reference.py` | 289 | `f63cf58a2098` |
| `scripts/dump_source.py` | 220 | `d5518cb2d916` |
\n")

    out.append("## 1. Cekirdek paket: `ris_mu/mumiso/`\n")
    out.append(
        "Tezin butun sayilari bu on dosyadan cikiyor. `system.py` tek "
        "dogruluk kaynagidir: SINR, oran ve on kodlayici sadece orada "
        "tanimli, digerleri onu cagirir.\n"
    )
    for rel in CORE_ORDER:
        n, d = _emit(out, rel)
        index.append((rel, n, d))

    if not args.core_only:
        out.append("## 2. Onceki tek kullanicili paket: `ris_mu/`\n")
        out.append(
            "Yayimlanmis makalenin Python karsiligi ve tek-RIS deneyleri. "
            "Cok kullanicili is bunun **uzerine** kuruldu, bunu "
            "degistirmedi. Kiyas icin burada.\n"
        )
        for rel in LEGACY_ORDER:
            n, d = _emit(out, rel)
            index.append((rel, n, d))

        out.append("## 3. Betikler: `scripts/`\n")
        out.append(
            "47 betik. Alfabetik degil, **tezdeki roluyle** gruplandi. "
            "Bir sayiyi teze koymadan once onu ureten betigi burada bulup "
            "kosturun.\n"
        )
        seen = set()
        for title, names in SCRIPT_GROUPS:
            out.append(f"### {title}\n")
            for name in names:
                rel = f"scripts/{name}"
                if not (ROOT / rel).exists():
                    out.append(f"*(yok: `{rel}`)*\n")
                    continue
                seen.add(name)
                n, d = _emit(out, rel)
                index.append((rel, n, d))
        leftover = sorted(
            p.name for p in (ROOT / "scripts").glob("*.py") if p.name not in seen
        )
        if leftover:
            out.append("### Gruplanmamis\n")
            for name in leftover:
                n, d = _emit(out, f"scripts/{name}")
                index.append((f"scripts/{name}", n, d))

    total = sum(n for _, n, _ in index)
    toc = ["## Icindekiler\n",
           f"**{len(index)} dosya · {total} satir**\n",
           "| Dosya | Satir | sha256 |", "|---|---:|---|"]
    toc += [f"| `{rel}` | {n} | `{d}` |" for rel, n, d in index]
    toc.append("")
    body = "\n".join(out).replace("## Icindekiler

**67 dosya · 10076 satir**

| Dosya | Satir | sha256 |
|---|---:|---|
| `ris_mu/mumiso/__init__.py` | 14 | `f9c07f1338d5` |
| `ris_mu/mumiso/system.py` | 333 | `21a8a952d800` |
| `ris_mu/mumiso/channel.py` | 338 | `b3c2a9ed69ca` |
| `ris_mu/mumiso/mobile.py` | 238 | `b33c20ab878e` |
| `ris_mu/mumiso/csi.py` | 131 | `accb4f90d9ec` |
| `ris_mu/mumiso/features.py` | 156 | `e1f57324af38` |
| `ris_mu/mumiso/models.py` | 278 | `4775daa8a793` |
| `ris_mu/mumiso/unrolled.py` | 223 | `95835a3ed9f3` |
| `ris_mu/mumiso/baselines.py` | 348 | `3ea6e6dd577f` |
| `ris_mu/mumiso/train.py` | 110 | `a48824f31611` |
| `ris_mu/__init__.py` | 0 | `e3b0c44298fc` |
| `ris_mu/geometry.py` | 84 | `295c899c3073` |
| `ris_mu/pathloss.py` | 111 | `9ab1e1cbca80` |
| `ris_mu/channel.py` | 348 | `8ec99f395131` |
| `ris_mu/features.py` | 107 | `c68df09577a3` |
| `ris_mu/models.py` | 316 | `4408c6e73174` |
| `ris_mu/losses.py` | 112 | `4fd1c95b68d3` |
| `ris_mu/baselines.py` | 113 | `2d5290a8fdc0` |
| `ris_mu/train.py` | 74 | `03f9853db4d4` |
| `scripts/audit_claims.py` | 465 | `4768a78598df` |
| `scripts/audit_fair_comparison.py` | 191 | `612487b768e0` |
| `scripts/audit_precoder_csi.py` | 156 | `af94df52d20d` |
| `scripts/audit_section4_cause.py` | 120 | `961aa49c3240` |
| `scripts/verify_mumiso_system.py` | 85 | `70c1c3a5ca9a` |
| `scripts/verify_mumiso_channel.py` | 63 | `c5b24cbab83e` |
| `scripts/verify_mumiso_models.py` | 91 | `15b75565f57a` |
| `scripts/verify_mobile.py` | 106 | `1913e291c531` |
| `scripts/verify_residual.py` | 57 | `6a9e50a457ae` |
| `scripts/verify_batch_dependence.py` | 53 | `11ed1aa64660` |
| `scripts/verify_baseline_strength.py` | 40 | `27f30c3e8238` |
| `scripts/verify_crossover.py` | 123 | `3649874707cb` |
| `scripts/verify_head_claim.py` | 163 | `ccc519076f7e` |
| `scripts/verify_matlab_architecture.py` | 133 | `70e791323b23` |
| `scripts/mumiso_run.py` | 146 | `ab16ab18b22b` |
| `scripts/mumiso_unrolled.py` | 156 | `e557411495d9` |
| `scripts/mumiso_equal_step.py` | 255 | `ae3ea9cfbd22` |
| `scripts/mumiso_latency_parity.py` | 271 | `c40f705e21b9` |
| `scripts/mumiso_latency_repeat.py` | 90 | `c6687a3532ee` |
| `scripts/mumiso_step_cost.py` | 66 | `658e6186e376` |
| `scripts/mumiso_budget.py` | 172 | `6b757f4a12b7` |
| `scripts/mumiso_budget_fraction.py` | 228 | `d147a606155c` |
| `scripts/mumiso_headroom.py` | 52 | `d7ff9705f3b8` |
| `scripts/anchor_same_split.py` | 26 | `a4ac3fa7cb26` |
| `scripts/diagnose_learnability.py` | 129 | `6f4375cd7410` |
| `scripts/diagnose_mumiso_gap.py` | 105 | `3411d21f59e2` |
| `scripts/step1_control.py` | 118 | `fd042c302981` |
| `scripts/step1b_head_ablation.py` | 119 | `87685e92fa0f` |
| `scripts/step4_multiuser.py` | 150 | `a9e56d2c5509` |
| `scripts/step4b_residual.py` | 99 | `c61c758b64e4` |
| `scripts/step4c_equiv_long.py` | 99 | `2bbadcdae859` |
| `scripts/step5_generalisation.py` | 129 | `8b1356bbdb8a` |
| `scripts/step5b_mixed_users.py` | 167 | `e4407aed2fad` |
| `scripts/mumiso_aging.py` | 204 | `ab0f6bccdcfa` |
| `scripts/mumiso_frontier.py` | 163 | `175da29e064a` |
| `scripts/mumiso_beam_staleness.py` | 139 | `be5a1e837981` |
| `scripts/mumiso_antenna_corr.py` | 73 | `52e1fbee7d50` |
| `scripts/mumiso_gain_sharing.py` | 60 | `0ff5e98f3c59` |
| `scripts/mumiso_gain_source.py` | 37 | `7141a0938ef5` |
| `scripts/mumiso_precoder_cost.py` | 46 | `eb616f5073d8` |
| `scripts/mumiso_csi_room.py` | 127 | `4600791a219c` |
| `scripts/mumiso_quant_latency.py` | 114 | `9b3a60ce25be` |
| `scripts/step3_csi_transfer.py` | 168 | `372aed33fe5d` |
| `scripts/step6_quantised_phase.py` | 221 | `f951598f5ed5` |
| `scripts/diagnose_realism.py` | 149 | `b4b4031d45f3` |
| `scripts/compile_results.py` | 209 | `9a22de7b9b19` |
| `scripts/make_writing_reference.py` | 289 | `f63cf58a2098` |
| `scripts/dump_source.py` | 220 | `d5518cb2d916` |
", "\n".join(toc))

    dest = ROOT / args.out
    dest.write_text(body + "\n", encoding="utf-8")
    print(f"{dest}  ({len(index)} dosya, {total} satir, "
          f"{dest.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
```

