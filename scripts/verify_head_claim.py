"""
verify_head_claim.py
--------------------
Adversarial check on the step-2 conclusion.

The claim is that the dense output head, not the body, limits the published
architecture. The obvious objection is that the dense models were simply
undertrained or badly tuned. This script gives the dense head every
reasonable advantage and checks whether it recovers:

  A  published head, published settings            (the step-2 number)
  B  published head, lower LR, longer, no dropout  (tuning objection)
  C  widened bottleneck: last hidden 64 -> 512     (direct test of the
                                                    bottleneck explanation)
  D  local head                                    (the reference point)

If B stays far from D the tuning objection fails. If C closes most of the gap
the bottleneck explanation is confirmed directly, since C changes nothing but
the width of the layer that feeds the 2N outputs.

Usage:  python scripts/verify_head_claim.py --n 40000
"""

import argparse
import json
import os
import sys

import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                              # noqa: E402
from ris_mu.channel import legacy_generate                        # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices  # noqa: E402
from ris_mu.models import CNNOnly, count_params                   # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


class WideDenseHead(nn.Module):
    """Published head with the final hidden layer widened."""

    def __init__(self, c, N, width=512):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(c * N, 512), nn.ReLU(inplace=True),
            nn.Linear(512, 512), nn.ReLU(inplace=True),
            nn.Linear(512, width), nn.ReLU(inplace=True),
            nn.Linear(width, 2 * N),
        )

    def forward(self, h):
        return self.net(h.flatten(1))


class NoDropDenseHead(nn.Module):
    """Published head with dropout removed."""

    def __init__(self, c, N):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(c * N, 256), nn.ReLU(inplace=True),
            nn.Linear(256, 128), nn.ReLU(inplace=True),
            nn.Linear(128, 64), nn.ReLU(inplace=True),
            nn.Linear(64, 2 * N),
        )

    def forward(self, h):
        return self.net(h.flatten(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel = RISPanel(M=8, K=4)
    N = panel.N
    d = legacy_generate(args.n, panel)
    F, G = d["F"], d["G"][:, 0, :]
    X = torch.from_numpy(su_features(F, G))
    Y = torch.from_numpy(su_labels(F, G))
    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Y), itr, iva, ite)

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

    runs = []

    # A: published settings (reuse the step-2 result if present)
    prev = None
    p_ab = os.path.join(args.out, "step1b_head_ablation.json")
    if os.path.exists(p_ab):
        ab = json.load(open(p_ab))
        prev = next((v for v in ab.values()
                     if v["body"] == "CNN" and v["head"] == "dense"), None)
    if prev:
        runs.append(("A  dense, published settings", prev["params"],
                     prev["test_rmse"], prev["test_sr5"], "from step 2"))
    else:
        runs.append(("A  dense, published settings", 0, float("nan"), float("nan"), "-"))

    # B: tuned dense head
    set_seed(42)
    m = CNNOnly(N, head="dense")
    m.head = NoDropDenseHead(64, N)
    print("--- B  dense head, lr=3e-4, no dropout, 70 epochs")
    run_training(m, tr, va, step_fn, eval_fn, epochs=70, lr=3e-4,
                 milestones=(35, 55, 65), patience=20, tag="B", verbose=False)
    _, mb = eval_fn(m, te)
    runs.append(("B  dense, tuned", count_params(m), mb["rmse"], mb["sr5"],
                 "lr 3e-4, no dropout"))
    print(f"    RMSE={mb['rmse']:.3f}  SR@5={mb['sr5']:.2f}%\n")

    # C: widened bottleneck
    set_seed(42)
    m = CNNOnly(N, head="dense")
    m.head = WideDenseHead(64, N, width=512)
    print("--- C  dense head, final hidden widened 64 -> 512")
    run_training(m, tr, va, step_fn, eval_fn, epochs=50, lr=1e-3,
                 milestones=(20, 35, 45), patience=15, tag="C", verbose=False)
    _, mc = eval_fn(m, te)
    runs.append(("C  dense, widened bottleneck", count_params(m), mc["rmse"],
                 mc["sr5"], "64 -> 512 units"))
    print(f"    RMSE={mc['rmse']:.3f}  SR@5={mc['sr5']:.2f}%\n")

    # D: local head reference
    if prev is not None:
        loc = next((v for v in ab.values()
                    if v["body"] == "CNN" and v["head"] == "local"), None)
        if loc:
            runs.append(("D  local head (reference)", loc["params"],
                         loc["test_rmse"], loc["test_sr5"], "from step 2"))

    print(f"{'variant':<32}{'params':>10}{'RMSE':>10}{'SR@5':>9}   note")
    print("-" * 78)
    for name, pr, r, sr, note in runs:
        print(f"{name:<32}{pr:>10,}{r:>9.2f}°{sr:>8.2f}%   {note}")

    out = {n: dict(params=p, rmse=r, sr5=s, note=nt) for n, p, r, s, nt in runs}
    json.dump(out, open(os.path.join(args.out, "verify_head_claim.json"), "w"),
              indent=2)
    print(f"\nsaved -> {args.out}/verify_head_claim.json")


if __name__ == "__main__":
    main()
