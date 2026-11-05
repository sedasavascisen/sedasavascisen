"""
Site-specific channel: one fixed room in which the channel is a deterministic
function of the user position.

Why a new generator
-------------------
In ris_mu.mumiso (and its mobile subclass) the scattered-path gains, the LoS
state, the Ricean K and the shadowing are drawn per USER link. Two users at
the same position in the same room therefore get different channels, and a
phase cannot be predicted from position. This module keeps the parent's
physics (3GPP TR 38.901 InH path loss and excess loss, cos^q element pattern,
Tang two-hop cascade amplitude, 40 dB direct-link blockage) and draws the
randomness ONCE PER SITE:

  - scatterers: positions and one complex reflectivity each, shared by every
    user and every BS antenna (physically the scatterer's own reflection);
  - obstacles: axis-aligned boxes -- furniture (1-2.5 m high) and full-height
    partitions (0.2 m thick, 3-8 m long, never across the BS-RIS link); a link
    is LoS iff the straight segment misses every box (geometric, not a
    probability). The number of partitions is calibrated so that the RIS-user
    LoS fraction matches the 3GPP InH model on the same geometry;
  - Ricean K: one value per link type for the site;
  - shadowing: a fixed, spatially correlated log-normal field over the room
    (sum of random cosines; Gaussian correlation with length sf_corr_dist).

Nothing in ris_mu.mumiso is changed; existing results are unaffected.

    site = Site(seed=1)
    pos  = site.sample_positions(1000, np.random.default_rng(0))
    F, G, hd = site.channels(pos)      # [P,N,T], [P,1,N], [P,1,T] complex64
"""
import numpy as np

from ..channel import _centre_cos
from ..mumiso.channel import make_mumiso_scenario
from ..mumiso.mobile import MobileConfig, MobileMuMisoChannel

__all__ = ["Site"]


def _segment_hits_box(a, b, lo, hi):
    """a, b [P,3]; lo, hi [3]. True where the segment a->b passes through the box."""
    d = b - a
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = (lo - a) / d
        t2 = (hi - a) / d
    tmin = np.where(np.isfinite(t1), np.minimum(t1, t2), -np.inf)
    tmax = np.where(np.isfinite(t2), np.maximum(t1, t2), np.inf)
    # axes where the segment is parallel: inside the slab or not
    par = d == 0
    inside = (a >= lo) & (a <= hi)
    tmin = np.where(par, np.where(inside, -np.inf, np.inf), tmin)
    tmax = np.where(par, np.where(inside, np.inf, -np.inf), tmax)
    t_enter = tmin.max(-1)
    t_exit = tmax.min(-1)
    return (t_enter <= t_exit) & (t_exit >= 0) & (t_enter <= 1)


class Site:
    def __init__(self, seed, n_obstacles=4, n_walls=34, n_scatterers=20, n_bs_antennas=8, n_waves=64):
        panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=n_bs_antennas, seed=seed)
        cfg = MobileConfig(**{**base.__dict__, "times_ms": (0.0,), "n_clusters": n_scatterers})
        self.ch = MobileMuMisoChannel(panel, cfg)          # physics helpers only
        self.panel, self.cfg, self.pl = panel, cfg, self.ch.pl
        self.snr_scale = cfg.snr_scale()
        rng = np.random.default_rng(10_000 + seed)
        self.room = np.asarray(cfg.room, float)
        self.ris_c = panel.positions.mean(0)
        self.bs = np.asarray(cfg.bs_pos, float)
        self.bsa = self.ch._array(self.bs[None])[0]         # [T,3]

        # obstacles: footprint 1-4 m, height 1-2.5 m, kept clear of BS and RIS
        boxes = []
        while len(boxes) < n_obstacles:
            size = np.r_[rng.uniform(1, 4, 2), rng.uniform(1, 2.5)]
            lo = np.r_[rng.uniform(0, self.room[0] - size[0]), rng.uniform(0, self.room[1] - size[1]), 0.0]
            hi = lo + size
            clear = all(np.any((p < lo - 1.0) | (p > hi + 1.0)) for p in (self.bs, self.ris_c))
            if clear:
                boxes.append((lo, hi))
        # partitions: full-height, 0.2 m thick, 3-8 m long, along x or y
        while len(boxes) < n_obstacles + n_walls:
            ln = rng.uniform(3, 8)
            size = np.r_[ln, 0.2, self.room[2]] if rng.random() < 0.5 else np.r_[0.2, ln, self.room[2]]
            lo = np.r_[rng.uniform(0, self.room[0] - size[0]), rng.uniform(0, self.room[1] - size[1]), 0.0]
            hi = lo + size
            clear = all(np.any((p < lo - 1.0) | (p > hi + 1.0)) for p in (self.bs, self.ris_c))
            if clear and not _segment_hits_box(self.bs[None], self.ris_c[None], lo, hi)[0]:
                boxes.append((lo, hi))
        self.boxes = boxes

        self.scat = rng.uniform([0, 0, 0], self.room, (n_scatterers, 3))
        self.rho = (rng.standard_normal(n_scatterers) + 1j * rng.standard_normal(n_scatterers)) / np.sqrt(2)
        self.k_bs = 10 ** (self.pl.rice_k_db(rng, 1)[0] / 10)
        self.k_ue = 10 ** (self.pl.rice_k_db(rng, 1)[0] / 10)
        self.k_dir = 10 ** (self.pl.rice_k_db(rng, 1)[0] / 10)
        # shadowing fields (RIS-UE and direct), unit variance, Gaussian correlation
        L = cfg.sf_corr_dist
        self._sf_k = [rng.standard_normal((n_waves, 2)) / L for _ in range(2)]
        self._sf_ph = [rng.uniform(0, 2 * np.pi, n_waves) for _ in range(2)]
        sf_bs_w = rng.standard_normal()

        # BS-RIS link: static for the site
        los_bs = not self.blocked(self.bs[None], self.ris_c[None])[0]
        self.los_bs = los_bs
        F_s = self.ch._ris_link_g(self.bsa[None], self.scat[None, None], np.array([[los_bs]]),
                                  np.array([[self.k_bs]]), np.tile(self.rho, (1, self.bsa.shape[0], 1)))[0]  # [T,N]
        P = panel
        gt = 10 ** (cfg.bs_gain_dbi / 20)
        d3_bs = np.linalg.norm(self.bs - self.ris_c)
        f_in = _centre_cos(P, self.bs[None])[0] ** P.q
        cc = np.sqrt(P.element_gain * P.d * P.d) * P.lam / (4 * np.pi) ** 1.5
        sf_bs = 10 ** (self.pl.sigma_sf_db(np.array([los_bs]))[0] * sf_bs_w / 20)
        A_F = (gt * cc * np.sqrt(f_in) / max(d3_bs, 1.0)
               * 10 ** (-self.pl.excess_db(np.array([d3_bs]), np.array([los_bs]))[0] / 20) * sf_bs)
        self.F = (F_s * A_F).T.astype(np.complex64)          # [N,T]

    # ------------------------------------------------------------------ geometry
    def blocked(self, a, b):
        """[P] True if the segment from a to b passes through any obstacle."""
        a = np.broadcast_to(a, np.broadcast_shapes(a.shape, b.shape))
        b = np.broadcast_to(b, a.shape)
        hit = np.zeros(a.shape[0], bool)
        for lo, hi in self.boxes:
            hit |= _segment_hits_box(a, b, lo, hi)
        return hit

    def inside_obstacle(self, pos):
        out = np.zeros(len(pos), bool)
        for lo, hi in self.boxes:
            out |= np.all((pos >= lo) & (pos <= hi), axis=-1)
        return out

    def sample_positions(self, n, rng, margin=0.5):
        """Uniform in the room (heights 1-2 m), outside obstacles."""
        out = []
        while sum(len(o) for o in out) < n:
            p = np.c_[rng.uniform(margin, self.room[0] - margin, n), rng.uniform(margin, self.room[1] - margin, n),
                      rng.uniform(*self.cfg.user_z, n)]
            out.append(p[~self.inside_obstacle(p)])
        return np.concatenate(out)[:n]

    def _sf(self, i, pos):
        w = np.sqrt(2.0 / len(self._sf_ph[i])) * np.cos(pos[:, :2] @ self._sf_k[i].T + self._sf_ph[i]).sum(-1)
        return w

    # ------------------------------------------------------------------ channels
    def los_ue(self, pos):
        return ~self.blocked(pos, np.broadcast_to(self.ris_c, pos.shape))

    def channels(self, pos, chunk=2000):
        """pos [P,3] -> F [P,N,T], G [P,1,N], hd [P,1,T] (complex64)."""
        Fs, Gs, Hs = [], [], []
        for i in range(0, len(pos), chunk):
            F, G, H = self._channels(pos[i:i + chunk])
            Fs.append(F); Gs.append(G); Hs.append(H)
        return np.concatenate(Fs), np.concatenate(Gs), np.concatenate(Hs)

    def _channels(self, pos):
        P, pl, cfg = self.panel, self.pl, self.cfg
        n = len(pos)
        T = self.bsa.shape[0]
        los_ue = self.los_ue(pos)
        los_dir = ~self.blocked(pos, np.broadcast_to(self.bs, pos.shape))
        ue = pos[:, None, :]                                               # [n,1,3]
        G_s = self.ch._ris_link_g(ue, self.scat[None, None], los_ue[:, None],
                                  np.full((n, 1), self.k_ue), np.tile(self.rho, (n, 1, 1)))      # [n,1,N]
        hd_s = self.ch._direct_link_g(self.bsa[None, None], ue[:, :, None], self.scat[None, None, None],
                                      los_dir[:, None, None], np.full((n, 1, 1), self.k_dir),
                                      np.tile(self.rho, (n, 1, T, 1)))                           # [n,1,T]
        gr = 10 ** (cfg.ue_gain_dbi / 20)
        d3_ue = np.linalg.norm(pos - self.ris_c, axis=-1)
        d3_dir = np.linalg.norm(pos - self.bs, axis=-1)
        f_out = _centre_cos(P, pos) ** P.q
        sf_ue = 10 ** (pl.sigma_sf_db(los_ue) * self._sf(0, pos) / 20)
        sf_dir = 10 ** (pl.sigma_sf_db(los_dir) * self._sf(1, pos) / 20)
        A_G = (gr * np.sqrt(f_out) / np.maximum(d3_ue, 1.0)
               * 10 ** (-pl.excess_db(d3_ue, los_ue) / 20) * sf_ue)
        A_d = (pl.amplitude(d3_dir, los_dir, cfg.bs_gain_dbi + cfg.ue_gain_dbi) * sf_dir
               * 10 ** (-cfg.direct_blockage_db / 20))
        G = (G_s * A_G[:, None, None]).astype(np.complex64)
        hd = (hd_s * A_d[:, None, None]).astype(np.complex64)
        F = np.broadcast_to(self.F, (n,) + self.F.shape).copy()
        return F, G, hd
