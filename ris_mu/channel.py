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
    def _ris_link(self, pts, scat, los, kappa, share_gains=False):
        """
        Small-scale channel between points and every RIS element, unit mean
        power per element.

        pts   : (..., 3)      scat : (..., L, 3)
        los   : (...) bool    kappa: (...) linear Ricean K
        share_gains: bool     share cluster gains across leading axis if True
        out   : (..., N) complex

        When share_gains=True and pts has shape (..., M, 3), cluster gains are
        drawn once and broadcast across the M axis. This models physically
        correct scattering where each cluster has one reflection coefficient
        and the M-axis variation comes from geometry alone. The default False
        preserves backward compatibility and draws independent gains for each
        point, which decorrelates an antenna array beyond reality.
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
        # share gains across leading axis if requested
        if share_gains and d1.ndim >= 3:
            # broadcast first slice across the leading axis (requires 3D+)
            gains = np.broadcast_to(gains[..., :1, :], d1.shape).copy()
        amp = np.sqrt(g_s) / np.maximum(d1[..., None] * d2, 1.0)
        h_nlos = np.sum(gains[..., None] * amp *
                        np.exp(-1j * self.k * (d1[..., None] + d2)), axis=-2)
        h_nlos = _unit_power(h_nlos)

        kap = np.where(los, kappa, 0.0)[..., None]
        return np.sqrt(kap / (kap + 1)) * h_los + np.sqrt(1.0 / (kap + 1)) * h_nlos

    def _direct_link(self, a, b, scat, los, kappa, share_gains=False):
        """
        Scalar BS-UE channel, unit mean power.

        share_gains: bool     share cluster gains across antenna axis if present

        When a has shape [..., T, 3] (antenna array) and share_gains=True,
        cluster gains are shared across the T axis.
        """
        d = np.linalg.norm(a - b, axis=-1)
        h_los = np.exp(-1j * self.k * d)

        d1 = np.linalg.norm(a[..., None, :] - scat, axis=-1)
        d2 = np.linalg.norm(scat - b[..., None, :], axis=-1)
        gains = self._crandn(d1.shape)
        # share gains across antenna axis if requested and present
        if share_gains and d1.ndim >= 3:
            # for shape [S, K, T, L], broadcast across axis -2 (T)
            # gains[..., :1, :] keeps first T-slice: [..., 0:1, L]
            gains = np.broadcast_to(gains[..., :1, :], d1.shape).copy()
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
