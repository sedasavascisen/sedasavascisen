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
