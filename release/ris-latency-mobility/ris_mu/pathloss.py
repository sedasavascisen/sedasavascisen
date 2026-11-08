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
