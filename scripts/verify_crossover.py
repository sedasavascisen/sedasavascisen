"""
verify_crossover.py
-------------------
Adversarial check on the step-3 conclusion.

The claim is that spatial mixing beats an element-local model on the
geometric channel at high CSI error, and never does so on the legacy channel.
Step 3 measured that once, with one seed. A 6.5% difference from a single run
is not evidence, so this repeats the decisive cell (sigma = 0.25) over several
seeds and reports the spread.

Each seed redraws BOTH the channel realisation and the network
initialisation, so the reported spread covers data and training noise
together.

Usage:  python scripts/verify_crossover.py --n 12000 --seeds 4
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                                        # noqa: E402
from ris_mu.channel import legacy_generate, MultiUserRISChannel, make_scenario  # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices            # noqa: E402
from ris_mu.models import SharedMLP, CNNLSTM                                 # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate            # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed               # noqa: E402
from scripts.step3_csi_transfer import add_csi_error                         # noqa: E402


def get_channel(kind, n, panel, seed):
    if kind == "legacy":
        d = legacy_generate(n, panel, seed=seed)
        return d["F"], d["G"][:, 0, :]
    p2, cfg = make_scenario(n_users=1, seed=seed)
    d = MultiUserRISChannel(p2, cfg).generate(n)
    return d["F"], d["G"][:, 0, :]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12000)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--sigma", type=float, default=0.25)
    ap.add_argument("--epochs", type=int, default=22)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    panel = RISPanel(M=8, K=4)
    N = panel.N
    itr, iva, ite = split_indices(args.n, seed=0)

    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for Xb, Yb in loader:
                P.append(model(Xb))
                T.append(Yb.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))

    def step_fn(model, b):
        Xb, Yb = b
        return phase_aware_mse(model(Xb), Yb.flatten(1))

    builders = {"element-local": lambda: SharedMLP(N),
                "global mixing": lambda: CNNLSTM(N, head="local")}
    res = {}

    for ch in ("legacy", "geometric"):
        for s in range(args.seeds):
            F, G = get_channel(ch, args.n, panel, seed=700 + s)
            Y = torch.from_numpy(su_labels(F, G))
            rng = np.random.default_rng(900 + s)
            Fe, Ge = add_csi_error(F, G, args.sigma, rng)
            X = torch.from_numpy(su_features(Fe, Ge))
            tr, va, te = make_loaders((X, Y), itr, iva, ite)
            for mname, build in builders.items():
                set_seed(1000 + s)
                model = build()
                run_training(model, tr, va, step_fn, eval_fn,
                             epochs=args.epochs, tag="", verbose=False)
                _, m = eval_fn(model, te)
                res[f"{ch}|{s}|{mname}"] = m["rmse"]
                print(f"  {ch:<10} seed {s}  {mname:<14} RMSE={m['rmse']:7.3f}°")

    print(f"\nsigma = {args.sigma}, {args.seeds} seeds, mean +- std over seeds")
    print(f"{'channel':<12}{'element-local':>18}{'global mixing':>18}"
          f"{'advantage':>14}{'wins':>7}")
    print("-" * 69)
    summary = {}
    for ch in ("legacy", "geometric"):
        a = np.array([res[f"{ch}|{s}|element-local"] for s in range(args.seeds)])
        b = np.array([res[f"{ch}|{s}|global mixing"] for s in range(args.seeds)])
        adv = 100 * (b - a) / a                       # negative = mixing wins
        wins = int((b < a).sum())
        summary[ch] = dict(local_mean=float(a.mean()), local_std=float(a.std()),
                           mix_mean=float(b.mean()), mix_std=float(b.std()),
                           advantage_mean=float(adv.mean()),
                           advantage_std=float(adv.std()),
                           mixing_wins=wins, n_seeds=args.seeds)
        print(f"{ch:<12}{a.mean():>12.2f}±{a.std():<5.2f}"
              f"{b.mean():>12.2f}±{b.std():<5.2f}"
              f"{adv.mean():>+9.1f}±{adv.std():<4.1f}%{wins:>4}/{args.seeds}")

    print("\n  (advantage negative = spatial mixing beats the element-local "
          "model;\n   'wins' counts seeds where it did)")

    p = os.path.join(args.out, "verify_crossover.json")
    json.dump(dict(per_run=res, summary=summary, sigma=args.sigma), open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
