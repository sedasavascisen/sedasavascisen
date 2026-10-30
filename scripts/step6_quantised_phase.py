"""
step6_quantised_phase.py
------------------------
Does a learned model earn its place once the phase shifts are DISCRETE?

Why this matters
----------------
Every result so far assumes a continuous phase per element. Real reflecting
surfaces do not have one: elements are switched with PIN diodes or varactors
and offer 1 or 2 bits of phase resolution. Continuous phase is an
idealisation, and it is the idealisation that makes the classical baselines
strong -- with continuous phase the single-user closed form is exactly
optimal, so there is nothing for a network to discover.

With B-bit phases the picture changes. The problem becomes combinatorial
(2^(B*N) configurations), the closed form is no longer optimal, and the usual
classical recipe -- optimise in the continuous domain, then round -- loses
whatever the rounding destroys. A network, by contrast, can be trained
THROUGH the quantiser with a straight-through estimator, so it learns to
place phases that survive it.

This script measures whether that advantage is real.

Compared, all on identical scenarios:
  closed form -> round     the published single-user solution, quantised
  PGA -> round             continuous optimisation, then quantised
  discrete CD              greedy coordinate descent over the discrete set
                           (the honest classical discrete baseline)
  learned (STE)            equivariant model trained through the quantiser

Usage:  python scripts/step6_quantised_phase.py --n 8000 --epochs 25
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import sincos_to_unit, effective_channel     # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed   # noqa: E402
from ris_mu import baselines as BL                              # noqa: E402


# ------------------------------------------------------------ quantiser

def quantise(theta, bits):
    """Nearest point of the 2^bits-point uniform phase grid."""
    if bits is None:
        return theta
    step = 2 * np.pi / (2 ** bits)
    return torch.round(theta / step) * step


def quantise_ste(theta, bits):
    """Quantise on the forward pass, pass the gradient straight through."""
    if bits is None:
        return theta
    return theta + (quantise(theta, bits) - theta).detach()


def rates_from_theta(Fc, Gc, hd, theta, snr_scale):
    g = effective_channel(Fc, Gc, hd, torch.cos(theta), torch.sin(theta))
    return torch.log2(1.0 + snr_scale * g)


# ------------------------------------------------------------ baselines

def discrete_cd(Fc, Gc, hd, snr_scale, bits, sweeps=3, init=None):
    """
    Greedy coordinate descent over the discrete phase set.

    At each element every one of the 2^bits settings is scored on the true
    objective and the best is kept. This is the classical method that does
    NOT suffer from rounding, so it is the baseline a learned model has to
    beat to be interesting.
    """
    B, U, N = Gc.shape
    L = 2 ** bits
    grid = torch.arange(L, dtype=torch.float32) * (2 * np.pi / L)

    theta = quantise(init.clone(), bits) if init is not None else torch.zeros(B, N)

    for _ in range(sweeps):
        for n in range(N):
            best_val = None
            best_ph = None
            for q in range(L):
                trial = theta.clone()
                trial[:, n] = grid[q]
                val = rates_from_theta(Fc, Gc, hd, trial, snr_scale).min(-1).values
                if best_val is None:
                    best_val, best_ph = val, torch.full((B,), grid[q])
                else:
                    upd = val > best_val
                    best_val = torch.where(upd, val, best_val)
                    best_ph = torch.where(upd, torch.full((B,), grid[q]), best_ph)
            theta[:, n] = best_ph
    return theta


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8000)
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--bits", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    d = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    Fc = torch.from_numpy(d["F"]).to(torch.complex64)
    Gc = torch.from_numpy(d["G"]).to(torch.complex64)
    hd = torch.from_numpy(d["hd"]).to(torch.complex64)
    N, sc = panel.N, cfg.snr_scale()

    itr, iva, ite = split_indices(args.n, seed=0)
    print(f"N={N}  U={args.users}  samples={args.n}\n")

    # reference points that do not depend on the bit depth
    Ft, Gt, ht = Fc[ite], Gc[ite], hd[ite]
    th_cf = BL.su_closed_form(Ft, Gt, ht, sc)[0]
    th_pga = BL.pga_maxmin(Ft, Gt, ht, sc, iters=300, restarts=3)[0]
    cont_cf = rates_from_theta(Ft, Gt, ht, th_cf, sc).min(-1).values.mean().item()
    cont_pga = rates_from_theta(Ft, Gt, ht, th_pga, sc).min(-1).values.mean().item()
    print(f"continuous reference   closed form {cont_cf:.3f}   PGA {cont_pga:.3f}\n")

    results = {"continuous": {"closed_form": cont_cf, "pga": cont_pga}}

    for bits in args.bits:
        print(f"===== {bits}-bit phase ({2**bits} levels) =====")
        row = {}

        row["closed form -> round"] = rates_from_theta(
            Ft, Gt, ht, quantise(th_cf, bits), sc).min(-1).values.mean().item()
        row["PGA -> round"] = rates_from_theta(
            Ft, Gt, ht, quantise(th_pga, bits), sc).min(-1).values.mean().item()

        t0 = time.perf_counter()
        th_dcd = discrete_cd(Ft, Gt, ht, sc, bits, sweeps=3, init=th_cf)
        dcd_ms = (time.perf_counter() - t0) * 1e3 / len(ite)
        row["discrete CD"] = rates_from_theta(
            Ft, Gt, ht, th_dcd, sc).min(-1).values.mean().item()

        for k, v in row.items():
            print(f"  {k:<22} {v:.3f}")

        # ---- learned, trained through the quantiser --------------------
        tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

        def step_fn(model, b, bits=bits):
            Xb, Fb, Gb, hb = b
            cos_t, sin_t = sincos_to_unit(model(Xb), N)
            th = torch.atan2(sin_t, cos_t)
            R = rates_from_theta(Fb, Gb, hb, quantise_ste(th, bits), sc)
            return -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()

        def eval_fn(model, loader, bits=bits):
            model.eval()
            tot, n = 0.0, 0
            with torch.no_grad():
                for Xb, Fb, Gb, hb in loader:
                    cos_t, sin_t = sincos_to_unit(model(Xb), N)
                    th = quantise(torch.atan2(sin_t, cos_t), bits)
                    v = rates_from_theta(Fb, Gb, hb, th, sc).min(-1).values
                    tot += v.sum().item()
                    n += len(Xb)
            return -tot / n, {"min_rate": tot / n}

        set_seed(42)
        model = EquivariantRIS(residual=False)
        info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                            lr=2e-3, milestones=(12, 20), patience=10,
                            tag=f"{bits}bit", verbose=False)
        _, m = eval_fn(model, te)
        row["learned (STE)"] = m["min_rate"]
        print(f"  {'learned (STE)':<22} {m['min_rate']:.3f}   ({info['minutes']:.1f} dk)")

        base = row["closed form -> round"]
        print(f"\n  learned vs closed-form-rounded : {100*(row['learned (STE)']-base)/base:+.1f}%")
        print(f"  learned vs discrete CD         : "
              f"{100*(row['learned (STE)']-row['discrete CD'])/row['discrete CD']:+.1f}%")
        print(f"  discrete CD cost               : {dcd_ms:.2f} ms/sample\n")

        row["discrete_cd_ms"] = dcd_ms
        results[f"{bits}bit"] = row

    # ---------------------------------------------------------- summary
    print("=" * 66)
    print(f"{'method':<24}" + "".join(f"{b}-bit".rjust(12) for b in args.bits))
    print("-" * 66)
    for k in ["closed form -> round", "PGA -> round", "discrete CD", "learned (STE)"]:
        line = f"{k:<24}"
        for b in args.bits:
            line += f"{results[f'{b}bit'][k]:>12.3f}"
        print(line)
    print("-" * 66)
    print(f"{'continuous closed form':<24}{cont_cf:>12.3f}")
    print(f"{'continuous PGA':<24}{cont_pga:>12.3f}")
    print("=" * 66)

    p = os.path.join(args.out, "step6_quantised.json")
    json.dump(results, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
