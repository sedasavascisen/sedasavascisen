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
    share_gains: bool = False            # share cluster gains across BS antennas


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
        # Share gains across BS antennas if configured (physically correct),
        # but NEVER across users (that would correlate interference).
        F_s = self._ris_link(bsa, scat[:, None], los_bs[:, None],
                             k_bs[:, None],
                             share_gains=self.cfg.share_gains)         # [S,T,N]
        G_s = self._ris_link(ue, scat[:, None], los_ue, k_ue,
                             share_gains=False)                        # [S,K,N]
        hd_s = self._direct_link(bsa[:, None], ue[:, :, None],
                                 scat[:, None, None],
                                 los_dir[..., None], k_dir[..., None],
                                 share_gains=self.cfg.share_gains)     # [S,K,T]

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
