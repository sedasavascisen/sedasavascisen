"""
step1b_head_ablation.py
-----------------------
Separates the contribution of the BODY from that of the OUTPUT HEAD in the
published architecture, on the legacy dataset.

Motivation
----------
A faithful re-implementation of the published CNN-LSTM does not reach the
reported accuracy, while a 6.6k-parameter element-local MLP does. The two
differ in the body (convolution + recurrence vs none) and in the head (a
dense bottleneck that flattens the feature map and squeezes it through 64
units vs a width-1 convolution applied at each element).

This script crosses the two factors so the responsible component is
identified rather than guessed:

    body in {none, CNN, CNN-LSTM}  x  head in {dense, local}

Why it matters beyond this dataset: the published head ends in a 64-unit
layer feeding 2N outputs. At N = 32 those are equal, at N = 256 the head must
push 512 numbers through 64 units. If the head is the binding constraint, the
degradation of accuracy with surface size reported in the original work is a
property of the head, not of the problem -- and it is removed by a change
that costs parameters rather than ideas.

Usage:  python scripts/step1b_head_ablation.py --n 40000 --epochs 40
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                               # noqa: E402
from ris_mu.channel import legacy_generate                         # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices   # noqa: E402
from ris_mu.models import SharedMLP, CNNOnly, CNNLSTM, count_params  # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate   # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed      # noqa: E402


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
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N

    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]
    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)
    eval_fn = build_eval(N)

    zoo = {
        ("none", "local"): lambda: SharedMLP(N),
        ("CNN", "dense"): lambda: CNNOnly(N, head="dense"),
        ("CNN", "local"): lambda: CNNOnly(N, head="local"),
        ("CNN-LSTM", "dense"): lambda: CNNLSTM(N, head="dense"),
        ("CNN-LSTM", "local"): lambda: CNNLSTM(N, head="local"),
    }

    res = {}
    for (body, head), build in zoo.items():
        set_seed(42)
        model = build()
        key = f"{body} + {head}"
        print(f"--- {key}  ({count_params(model):,} params)")
        info = run_training(model, tr, va, step_fn, eval_fn,
                            epochs=args.epochs, tag=key)
        _, m = eval_fn(model, te)
        res[key] = dict(body=body, head=head, params=count_params(model),
                        test_rmse=m["rmse"], test_sr5=m["sr5"],
                        minutes=info["minutes"])
        print(f"    test RMSE={m['rmse']:.3f}  SR@5={m['sr5']:.2f}%\n")

    print(f"{'body':<10}{'head':<8}{'params':>10}{'RMSE':>10}{'SR@5':>9}")
    print("-" * 47)
    for k, v in res.items():
        print(f"{v['body']:<10}{v['head']:<8}{v['params']:>10,}"
              f"{v['test_rmse']:>9.2f}°{v['test_sr5']:>8.2f}%")

    p = os.path.join(args.out, "step1b_head_ablation.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
