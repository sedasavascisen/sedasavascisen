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
