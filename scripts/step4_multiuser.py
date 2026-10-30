"""
step4_multiuser.py
------------------
Multi-user RIS phase design trained WITHOUT labels.

Why unsupervised
----------------
The closed form theta_n = -angle(F_n) - angle(G_n) is optimal for one user
only. With U users sharing one surface there is no closed form to regress
onto, so supervised training would require generating labels with a numerical
solver -- and a network trained to imitate a solver cannot, by construction,
beat it. Training directly on the system metric removes that ceiling.

Objective
---------
Single-antenna BS, users served in orthogonal slots inside one coherence
block, the surface held fixed across the block. One phase vector must serve
every user, which makes this a fairness problem; the objective is the
max-min rate, smoothed so that gradient reaches more than one user per
sample.

Models
------
  MU-CNN-LSTM     users concatenated along the channel axis -- the direct
                  extension of the published architecture. Fixes U and is
                  sensitive to the ordering of users.
  Equivariant     attention over elements, mean pooling over users. Respects
                  both symmetries of the problem and accepts any U.

Usage:  python scripts/step4_multiuser.py --n 20000 --epochs 30 --users 4
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario          # noqa: E402
from ris_mu.features import mu_features, split_indices                 # noqa: E402
from ris_mu.models import EquivariantRIS, MUCNNLSTM, count_params      # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics                    # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed          # noqa: E402
from ris_mu import baselines as BL                                     # noqa: E402


def build(args):
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    data = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(data["F"], data["G"], data["hd"]))
    Fc = torch.from_numpy(data["F"]).to(torch.complex64)
    Gc = torch.from_numpy(data["G"]).to(torch.complex64)
    hd = torch.from_numpy(data["hd"]).to(torch.complex64)
    return panel, cfg, X, Fc, Gc, hd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel, cfg, X, Fc, Gc, hd = build(args)
    N, sc = panel.N, cfg.snr_scale()
    print(f"N={N}  U={args.users}  samples={args.n}  "
          f"noise={cfg.noise_power_dbm():.1f} dBm\n")

    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

    def step_fn(model, batch):
        Xb, Fb, Gb, hb = batch
        return maxmin_loss(Fb, Gb, hb, model(Xb), N, sc)

    def eval_fn(model, loader):
        model.eval()
        acc, n = {}, 0
        with torch.no_grad():
            for Xb, Fb, Gb, hb in loader:
                m = rate_metrics(Fb, Gb, hb, model(Xb), N, sc)
                for k, v in m.items():
                    acc[k] = acc.get(k, 0.0) + v * len(Xb)
                n += len(Xb)
        acc = {k: v / n for k, v in acc.items()}
        return -acc["min_rate"], acc

    # ---------------------------------------------------------- baselines
    Ft, Gt, ht = Fc[ite], Gc[ite], hd[ite]
    print("baselines on the test split")
    res = {}
    res["no RIS"] = BL.summarise(BL.no_ris(Ft, Gt, ht, sc))
    res["random phase"] = BL.summarise(BL.random_phase(Ft, Gt, ht, sc)[1])
    res["SU closed form"] = BL.summarise(BL.su_closed_form(Ft, Gt, ht, sc)[1])
    t0 = time.perf_counter()
    res["PGA max-min"] = BL.summarise(BL.pga_maxmin(Ft, Gt, ht, sc,
                                                    iters=300, restarts=3)[1])
    res["PGA max-min"]["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
    for k, v in res.items():
        print(f"  {k:<16} min={v['min_rate']:.3f}  sum={v['sum_rate']:.3f}")
    print()

    # ---------------------------------------------------------- learned
    zoo = {
        "MU-CNN-LSTM": lambda: MUCNNLSTM(N, args.users),
        "Equivariant": lambda: EquivariantRIS(residual=False),
        "Equiv+residual": lambda: EquivariantRIS(residual=True),
    }
    for name, bld in zoo.items():
        set_seed(42)
        model = bld()
        print(f"--- {name}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, lr=2e-3, tag=name, patience=12,
                            milestones=(20, 35, 45))
        _, m = eval_fn(model, te)
        model.eval()
        with torch.no_grad():
            t0 = time.perf_counter()
            for Xb, *_ in te:
                model(Xb)
            m["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
        m["params"] = count_params(model)
        res[name] = m
        torch.save(model.state_dict(), os.path.join(args.out, f"step4_{name}.pt"))
        print(f"    min={m['min_rate']:.3f}  sum={m['sum_rate']:.3f}  "
              f"({info['minutes']:.1f} min)\n")

    # ---------------------------------------------------------- table
    print(f"{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}{'ms/sample':>11}")
    print("-" * 58)
    ref = res["PGA max-min"]["min_rate"]
    for k, v in res.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}")

    json.dump(res, open(os.path.join(args.out, "step4_multiuser.json"), "w"), indent=2)
    print(f"\nsaved -> {args.out}/step4_multiuser.json")


if __name__ == "__main__":
    main()
