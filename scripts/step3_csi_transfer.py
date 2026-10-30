"""
step3_csi_transfer.py
---------------------
Why a realistic channel is a prerequisite for an architecture claim.

The argument
------------
For a single user the optimal phase is theta_n = -angle(F_n) - angle(G_n).
That map is ELEMENT-LOCAL: element n's answer depends on element n's own
channel pair and on nothing else, whatever channel model produced it. Under
perfect CSI, therefore, no architecture that mixes elements can beat a
sufficiently expressive element-local model -- there is nothing to mix.

Spatial processing can only pay off when the per-element observation is
corrupted, so that neighbouring elements carry information about each other.
That requires the channel to be spatially correlated. It follows that:

  * on the LEGACY channel (independent coefficient per element) neighbours are
    uninformative, so spatial models cannot help at any noise level;
  * on the GEOMETRIC channel neighbours are correlated, so spatial models
    should pull ahead as CSI degrades.

This experiment measures exactly that, crossing

    channel in {legacy, geometric}
  x CSI error in {0, 0.1, 0.25}
  x model   in {element-local, local mixing (CNN), global mixing (CNN-LSTM)}

The CSI error is applied to the model INPUT only; labels come from the true
channel, so the task is estimation under uncertainty rather than a different
task. All models use the width-1 output head, so the comparison isolates the
body.

Usage:  python scripts/step3_csi_transfer.py --n 20000 --epochs 25
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.geometry import RISPanel                                   # noqa: E402
from ris_mu.channel import legacy_generate, MultiUserRISChannel, make_scenario  # noqa: E402
from ris_mu.features import su_features, su_labels, split_indices       # noqa: E402
from ris_mu.models import SharedMLP, CNNOnly, CNNLSTM, count_params     # noqa: E402
from ris_mu.losses import phase_aware_mse, rmse_deg, success_rate       # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed          # noqa: E402


def add_csi_error(F, G, sigma, rng):
    """
    Multiplicative-power CSI error: the perturbation is scaled to each
    sample's own channel power, so sigma is a relative error and the two
    channel models are perturbed comparably despite very different absolute
    path loss.
    """
    if sigma <= 0:
        return F, G

    def perturb(H):
        p = np.sqrt(np.mean(np.abs(H) ** 2, axis=-1, keepdims=True))
        e = (rng.standard_normal(H.shape) + 1j * rng.standard_normal(H.shape)) / np.sqrt(2)
        return H + sigma * p * e
    return perturb(F), perturb(G)


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


def get_channel(kind, n, panel):
    if kind == "legacy":
        d = legacy_generate(n, panel)
        return d["F"], d["G"][:, 0, :]
    p2, cfg = make_scenario(n_users=1, seed=7)
    d = MultiUserRISChannel(p2, cfg).generate(n)
    return d["F"], d["G"][:, 0, :]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    panel = RISPanel(M=8, K=4)
    N = panel.N
    eval_fn = build_eval(N)
    itr, iva, ite = split_indices(args.n, seed=0)

    builders = {
        "element-local":  lambda: SharedMLP(N),
        "local mixing":   lambda: CNNOnly(N, head="local"),
        "global mixing":  lambda: CNNLSTM(N, head="local"),
    }
    sigmas = [0.0, 0.10, 0.25]
    res = {}

    for ch_kind in ("legacy", "geometric"):
        set_seed(1)
        F, G = get_channel(ch_kind, args.n, panel)
        Y = torch.from_numpy(su_labels(F, G))           # labels from TRUE channel
        for sg in sigmas:
            rng = np.random.default_rng(100)
            Fe, Ge = add_csi_error(F, G, sg, rng)
            X = torch.from_numpy(su_features(Fe, Ge))
            tr, va, te = make_loaders((X, Y), itr, iva, ite)
            for mname, build in builders.items():
                set_seed(42)
                model = build()
                tag = f"{ch_kind[:4]}/s{sg}/{mname[:5]}"
                print(f"--- {ch_kind:<10} sigma={sg:<5} {mname:<14} "
                      f"({count_params(model):,} par)")
                run_training(model, tr, va, step_fn, eval_fn,
                             epochs=args.epochs, tag=tag, verbose=False)
                _, m = eval_fn(model, te)
                res[f"{ch_kind}|{sg}|{mname}"] = dict(
                    channel=ch_kind, sigma=sg, model=mname,
                    params=count_params(model),
                    rmse=m["rmse"], sr5=m["sr5"])
                print(f"    RMSE={m['rmse']:7.3f}°   SR@5={m['sr5']:6.2f}%")

    # ---- summary table -----------------------------------------------------
    print(f"\n{'channel':<11}{'sigma':>7}" + "".join(f"{k:>16}" for k in builders))
    print("-" * (18 + 16 * len(builders)))
    for ch_kind in ("legacy", "geometric"):
        for sg in sigmas:
            row = f"{ch_kind:<11}{sg:>7.2f}"
            for mname in builders:
                row += f"{res[f'{ch_kind}|{sg}|{mname}']['rmse']:>15.2f}°"
            print(row)

    print("\nadvantage of spatial mixing over element-local "
          "(negative = mixing helps):")
    for ch_kind in ("legacy", "geometric"):
        for sg in sigmas:
            base = res[f"{ch_kind}|{sg}|element-local"]["rmse"]
            best = min(res[f"{ch_kind}|{sg}|{m}"]["rmse"] for m in builders)
            print(f"  {ch_kind:<10} sigma={sg:<5}  {100*(best-base)/base:+6.1f}%")

    p = os.path.join(args.out, "step3_csi_transfer.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
