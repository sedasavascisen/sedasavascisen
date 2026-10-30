"""
step1_control.py
----------------
Control experiment on the LEGACY channel model.

Question
--------
The published CNN-LSTM beats a fully connected network on the legacy dataset.
Is that gain explained by spatial structure (which the legacy generator does
not contain, because it draws an independent coefficient per element), or
simply by capacity and weight sharing?

Test
----
Train SharedMLP: the same small MLP applied to every element independently,
with no path for information to flow between elements. If it matches the
CNN-LSTM, the recurrent and convolutional machinery is not exploiting spatial
structure on this dataset -- there is none to exploit.

Usage:  python scripts/step1_control.py --n 20000 --epochs 40
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                              # noqa: E402
from ris_mu.channel import legacy_generate                        # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices  # noqa: E402
from ris_mu.models import SharedMLP, FCDNN, CNNOnly, CNNLSTM, count_params  # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


def build_eval(N):
    def eval_fn(model, loader):
        model.eval()
        P, T = [], []
        with torch.no_grad():
            for X, Y in loader:
                P.append(model(X))
                T.append(Y.flatten(1))
        P, T = torch.cat(P), torch.cat(T)
        r = rmse_deg(P, T, N)
        return r, dict(rmse=r, sr5=success_rate(P, T, N))
    return eval_fn


def step_fn(model, batch):
    X, Y = batch
    return phase_aware_mse(model(X), Y.flatten(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N

    print(f"legacy dataset: {args.n} samples, N={N}")
    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]

    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)
    print(f"split: {len(itr)} / {len(iva)} / {len(ite)}\n")

    eval_fn = build_eval(N)
    zoo = {
        "SharedMLP (control)": SharedMLP(N),
        "FC-DNN": FCDNN(N),
        "CNN-only": CNNOnly(N),
        "CNN-LSTM (published)": CNNLSTM(N),
    }

    results = {}
    for name, model in zoo.items():
        set_seed(42)
        print(f"--- {name}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, tag=name.split()[0])
        _, m = eval_fn(model, te)
        results[name] = dict(params=count_params(model), val_rmse=info["best_score"],
                             test_rmse=m["rmse"], test_sr5=m["sr5"],
                             epochs_run=len(info["history"]), minutes=info["minutes"])
        print(f"    test RMSE={m['rmse']:.3f} deg   SR@5={m['sr5']:.2f}%   "
              f"({info['minutes']:.1f} min)\n")

    print(f"{'model':<24}{'params':>10}{'test RMSE':>12}{'SR@5':>9}")
    print("-" * 55)
    for k, v in results.items():
        print(f"{k:<24}{v['params']:>10,}{v['test_rmse']:>11.3f}°{v['test_sr5']:>8.2f}%")

    base = results["SharedMLP (control)"]["test_rmse"]
    best = results["CNN-LSTM (published)"]["test_rmse"]
    print(f"\nCNN-LSTM vs element-independent control: "
          f"{100*(base-best)/base:+.1f}% RMSE change")

    p = os.path.join(args.out, "step1_control.json")
    json.dump(results, open(p, "w"), indent=2)
    print(f"saved -> {p}")


if __name__ == "__main__":
    main()
