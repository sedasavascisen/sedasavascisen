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
