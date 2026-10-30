"""
diagnose_realism.py
-------------------
Quantifies the realism gap between the legacy channel generator and the
geometry-based one. Produces the numbers and the figure that justify the
"realistic scenario" contribution of the thesis.

Metrics
-------
1. Spatial correlation |rho(dx)| across the RIS aperture. A half-wavelength
   spaced array must show |rho| close to 1 for adjacent elements.
2. Effective rank of the spatial covariance R = E[h h^H]. A physical channel
   with a handful of paths is low rank; i.i.d. fading is full rank.
3. Condition number of R (dB).
4. Achievable-gain sensitivity: how much received power is lost if the optimal
   phase profile of one channel realisation is applied to a neighbouring one.

Usage:  python scripts/diagnose_realism.py --n 2000
"""

import argparse
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                       # noqa: E402
from ris_mu.channel import MultiUserRISChannel, ChannelConfig, legacy_generate  # noqa: E402


def spatial_corr(H, panel):
    """|rho| as a function of element separation, averaged over the aperture."""
    Hn = H - H.mean(0, keepdims=True)
    Hn = Hn / (np.std(Hn, axis=0, keepdims=True) + 1e-30)
    R = (Hn.conj().T @ Hn) / Hn.shape[0]                   # (N,N)
    sep = np.linalg.norm(panel.positions[:, None] - panel.positions[None], axis=-1)
    sep_r = np.round(sep / panel.d).astype(int)
    out = {}
    for s in range(1, sep_r.max() + 1):
        m = sep_r == s
        if m.sum():
            out[s] = float(np.abs(R[m]).mean())
    return out


def cov_stats(H):
    R = (H.conj().T @ H) / H.shape[0]
    ev = np.sort(np.abs(np.linalg.eigvalsh(R)))[::-1]
    ev = ev / ev.sum()
    ev_nz = ev[ev > 1e-12]
    eff_rank = float(np.exp(-np.sum(ev_nz * np.log(ev_nz))))   # entropy-based
    cond_db = float(10 * np.log10(ev[0] / max(ev[-1], 1e-15)))
    return eff_rank, cond_db


def beam_steering_fit(F, G, panel):
    """
    Fraction of the optimal received power retained when the phase profile is
    restricted to a linear ramp (a classical beam-steering solution).

    A physical, few-path channel has a smooth phase profile across the
    aperture, so a ramp recovers most of the gain. An i.i.d. channel has a
    random profile that no ramp can approximate. Reported in dB of loss.
    """
    theta_opt = -np.angle(F) - np.angle(G)
    p = panel.positions - panel.positions.mean(0)
    # least-squares linear ramp on the unwrapped-equivalent unit vectors
    A = np.c_[p, np.ones(panel.N)]                       # (N,4)
    pinv = np.linalg.pinv(A)
    coef = (pinv @ np.unwrap(theta_opt, axis=-1).T).T    # (S,4)
    theta_ramp = coef @ A.T
    g_opt = np.abs(np.sum(G * np.exp(1j * theta_opt) * F, axis=-1)) ** 2
    g_ramp = np.abs(np.sum(G * np.exp(1j * theta_ramp) * F, axis=-1)) ** 2
    return float(10 * np.log10(g_opt.mean() / max(g_ramp.mean(), 1e-30)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    panel = RISPanel(M=8, K=4)
    print(f"RIS {panel.M}x{panel.K} = {panel.N} elements, spacing {panel.d*100:.1f} cm "
          f"@ {panel.fc/1e9:.1f} GHz\n")

    print(f"generating legacy model  ({args.n} samples) ...")
    leg = legacy_generate(args.n, panel)

    print(f"generating geometry-based model ({args.n} samples) ...\n")
    new_r = MultiUserRISChannel(panel, ChannelConfig(n_users=1, bs_random=True, seed=0)).generate(args.n)
    new_f = MultiUserRISChannel(panel, ChannelConfig(n_users=1, bs_random=False, seed=0)).generate(args.n)

    rows = []
    for name, d in (("legacy", leg), ("geom/randBS", new_r), ("geom/fixedBS", new_f)):
        F, G = d["F"], d["G"][:, 0, :]
        c_f = spatial_corr(F, panel)
        er, cd = cov_stats(F)
        rows.append(dict(name=name, corr=c_f, eff_rank=er, cond_db=cd,
                         transfer=beam_steering_fit(F, G, panel)))

    # ---- table -------------------------------------------------------------
    seps = sorted(rows[0]["corr"])[:5]
    hdr = "model        " + "".join(f"|rho|@{s}d  " for s in seps) + " eff.rank  cond[dB]  ramp-loss[dB]"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        line = f"{r['name']:<13}"
        line += "".join(f"{r['corr'][s]:9.3f}  " for s in seps)
        line += f"{r['eff_rank']:9.2f}  {r['cond_db']:8.1f}  {r['transfer']:11.2f}"
        print(line)

    print(f"\n(eff.rank upper bound = N = {panel.N}; a physical few-path channel "
          f"should be well below it)")

    # ---- figure ------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4))
        for r in rows:
            s = sorted(r["corr"])
            ax[0].plot(s, [r["corr"][x] for x in s], "o-", label=r["name"])
        ax[0].set_xlabel(r"element separation [$\lambda/2$]")
        ax[0].set_ylabel(r"$|\rho|$")
        ax[0].set_title("Spatial correlation across the RIS aperture")
        ax[0].legend(); ax[0].grid(alpha=.3); ax[0].set_ylim(0, 1.05)

        for r, d in zip(rows, (leg, new_r, new_f)):
            F = d["F"]
            R = (F.conj().T @ F) / F.shape[0]
            ev = np.sort(np.abs(np.linalg.eigvalsh(R)))[::-1]
            ax[1].semilogy(ev / ev[0], "o-", label=f"{r['name']} (eff.rank {r['eff_rank']:.1f})")
        ax[1].set_xlabel("eigenvalue index")
        ax[1].set_ylabel("normalised eigenvalue")
        ax[1].set_title("Spatial covariance spectrum")
        ax[1].legend(); ax[1].grid(alpha=.3)
        plt.tight_layout()
        p = os.path.join(args.out, "realism_diagnostics.png")
        plt.savefig(p, dpi=150)
        print(f"\nfigure -> {p}")
    except ImportError:
        print("\n(matplotlib not available, skipping figure)")


if __name__ == "__main__":
    main()
