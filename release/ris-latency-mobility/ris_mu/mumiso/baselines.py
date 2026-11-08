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
