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
