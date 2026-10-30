"""
geometry.py
-----------
RIS panel geometry, element positions and element radiation pattern.

The panel is defined by an origin, two orthonormal in-plane vectors (e1, e2)
and a normal. Element n is placed at

    p_n = p0 + i * d * e1 + j * d * e2,     n = i * K + j

with row-major ordering (i over rows / M, j over columns / K), matching the
serialisation used by the sequential part of the model.
"""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class RISPanel:
    """Uniform rectangular array of passive reflecting elements."""

    M: int = 8                    # rows
    K: int = 4                    # columns
    fc: float = 3e9               # carrier frequency [Hz]
    center: tuple = (20.0, 10.0, 3.0)
    e1: tuple = (1.0, 0.0, 0.0)   # in-plane direction for rows
    e2: tuple = (0.0, 1.0, 0.0)   # in-plane direction for columns
    normal: tuple = (0.0, 0.0, -1.0)
    q: float = 1.0                # element pattern exponent, gain = 2(2q+1)

    positions: np.ndarray = field(init=False)

    def __post_init__(self):
        self.c = 299_792_458.0
        self.lam = self.c / self.fc
        self.k = 2 * np.pi / self.lam
        self.d = self.lam / 2

        e1 = _unit(np.asarray(self.e1, float))
        e2 = _unit(np.asarray(self.e2, float))
        if abs(e1 @ e2) > 1e-9:
            raise ValueError("e1 and e2 must be orthogonal")
        self.n_hat = _unit(np.asarray(self.normal, float))

        c = np.asarray(self.center, float)
        i = np.arange(self.M) - (self.M - 1) / 2
        j = np.arange(self.K) - (self.K - 1) / 2
        # row-major: index = i * K + j
        offs = (i[:, None, None] * self.d * e1) + (j[None, :, None] * self.d * e2)
        self.positions = (c + offs).reshape(self.M * self.K, 3)

    @property
    def N(self) -> int:
        return self.M * self.K

    @property
    def element_gain(self) -> float:
        """Boresight gain of a single element for a cos^q pattern."""
        return 2.0 * (2.0 * self.q + 1.0)

    def pattern(self, points: np.ndarray) -> np.ndarray:
        """
        cos^q element pattern evaluated for the direction from each element to
        each point.

        points : (..., 3)
        returns: (..., N) real gain (linear, includes boresight gain)
        """
        pts = np.asarray(points, float)
        vec = pts[..., None, :] - self.positions        # (..., N, 3)
        rng = np.linalg.norm(vec, axis=-1)
        cos_t = np.einsum("...i,i->...", vec, self.n_hat) / np.maximum(rng, 1e-12)
        cos_t = np.clip(cos_t, 0.0, 1.0)                # no radiation behind panel
        return self.element_gain * cos_t ** self.q

    def distances(self, points: np.ndarray) -> np.ndarray:
        """Exact element-wise distances (near-field safe). points (...,3) -> (...,N)."""
        pts = np.asarray(points, float)
        return np.linalg.norm(pts[..., None, :] - self.positions, axis=-1)


def _unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)
