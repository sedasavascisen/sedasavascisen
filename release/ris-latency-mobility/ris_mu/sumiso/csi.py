"""
Imperfect CSI for the single-user MISO extension.

The BS estimates the cascaded channel B (b_n = g_n F_n, what cascaded RIS
channel estimation delivers) and the direct channel a:

    B_hat = sqrt(1-e2) B + sqrt(e2) sqrt(p_B) Z,   a_hat likewise with p_a,

with Z ~ CN(0, 1) and p_B, p_a the mean element power of B and a IN EACH
SCENARIO. The scale is per scenario (not per call as in ris_mu.mumiso.csi),
so a scenario's error does not depend on which batch it is passed in with;
this matters here because networks are trained on one set and evaluated on
another. sqrt(1-e2) keeps the mean power unchanged.

Both the phase and the BS beam are computed from the estimate; the rate that
materialises is evaluated on the true channel with that mismatched beam
(maximum-ratio on the estimated effective channel).
"""
import torch


def estimate(a, B, e2, gen):
    if e2 <= 0:
        return a, B
    def noisy(X, dims):
        p = (X.abs() ** 2).mean(dim=dims, keepdim=True)
        z = torch.complex(torch.randn(X.shape, generator=gen), torch.randn(X.shape, generator=gen)) / 2 ** 0.5
        return (1 - e2) ** 0.5 * X + (e2 ** 0.5) * p.sqrt() * z.to(X.dtype)
    return noisy(a, (-1,)), noisy(B, (-2, -1))


def rate_mismatched(theta, a, B, a_hat, B_hat, snr):
    """log2(1 + snr |h w|^2), w = conj(h_hat)/|h_hat| from the estimate, h true."""
    v = torch.exp(1j * theta.to(torch.complex64))[..., None]
    h = a + (v * B).sum(1)
    hh = a_hat + (v * B_hat).sum(1)
    g = (h * hh.conj()).sum(-1).abs() ** 2 / (hh.abs() ** 2).sum(-1).clamp_min(1e-30)
    return torch.log2(1 + snr * g)
