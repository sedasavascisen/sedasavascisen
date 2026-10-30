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
