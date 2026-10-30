"""
verify_matlab_architecture.py
-----------------------------
Resolves the reproduction gap.

The GitHub repository's `train_cnn_lstm.py` flattens the LSTM output over all
elements and pushes it through a dense bottleneck ending in 64 units. The
MATLAB script that actually produced the published results
(`theta_NN_multioutput_UPDATED.m`) does something different: its input is a
`sequenceInputLayer`, both LSTMs run with `OutputMode='sequence'`, and the
output stage is `fullyConnectedLayer(2)`. In MATLAB a fully connected layer
applied to a sequence acts on EVERY TIME STEP INDEPENDENTLY, so the published
model emits (sin, cos) per element through one shared 64->2 map.

That is a width-1 convolution -- the "local head" of this study -- not a
dense bottleneck. The two files are therefore different architectures, and
the Python one is not a port of the MATLAB one.

This script builds the MATLAB architecture exactly as written and trains it on
the legacy dataset, to check whether the published figure is reproducible once
the head matches.

    conv1d(4->64, k=3) + BN + ReLU
    conv1d(64->64, k=3) + BN + ReLU
    dropout(0.2)
    LSTM(64->128, sequence)
    LSTM(128->64, sequence)
    dropout(0.3)
    Linear(64->2) applied per element

Usage:  python scripts/verify_matlab_architecture.py --n 40000 --epochs 50
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
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate  # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed     # noqa: E402


class MatlabCNNLSTM(nn.Module):
    """Faithful port of the published MATLAB layer stack."""

    def __init__(self, N=32):
        super().__init__()
        self.N = N
        self.cnn = nn.Sequential(
            nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(inplace=True),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(inplace=True),
            nn.Dropout(0.2),
        )
        self.lstm1 = nn.LSTM(64, 128, batch_first=True)
        self.lstm2 = nn.LSTM(128, 64, batch_first=True)
        self.drop = nn.Dropout(0.3)
        self.fc = nn.Linear(64, 2)          # applied at every element

    def forward(self, x):                   # [B, 4, N]
        h = self.cnn(x).permute(0, 2, 1)    # [B, N, 64]
        h, _ = self.lstm1(h)
        h, _ = self.lstm2(h)
        h = self.fc(self.drop(h))           # [B, N, 2]
        return torch.cat([h[..., 0], h[..., 1]], dim=-1)   # [B, 2N]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--epochs", type=int, default=50)
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

    model = MatlabCNNLSTM(N)
    n_par = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"MATLAB architecture as published: {n_par:,} trainable parameters")
    print("(the paper reports 727,360 for this model)\n")

    info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                        lr=1e-3, milestones=(15, 30, 45), patience=18,
                        tag="matlab")
    _, m = eval_fn(model, te)

    print(f"\n{'':<34}{'RMSE':>9}{'SR@5':>9}{'params':>11}")
    print("-" * 63)
    print(f"{'published figure (paper)':<34}{2.77:>8.2f}°{'—':>9}{727360:>11,}")
    print(f"{'MATLAB architecture, re-run here':<34}{m['rmse']:>8.2f}°"
          f"{m['sr5']:>8.2f}%{n_par:>11,}")
    print(f"{'repo train_cnn_lstm.py (dense head)':<34}{27.97:>8.2f}°"
          f"{17.59:>8.2f}%{822976:>11,}")

    res = dict(matlab_rmse=m["rmse"], matlab_sr5=m["sr5"], matlab_params=n_par,
               paper_rmse=2.77, paper_params=727360, repo_python_rmse=27.97)
    json.dump(res, open(os.path.join(args.out, "verify_matlab_arch.json"), "w"),
              indent=2)
    print(f"\nsaved -> {args.out}/verify_matlab_arch.json")


if __name__ == "__main__":
    main()
