"""
step4b_residual.py
------------------
Trains the residual variant of the equivariant model and merges its result
into the step 4 table, so the two models already trained are not repeated.

Usage:  python scripts/step4b_residual.py --n 16000 --epochs 50
"""

import argparse
import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics             # noqa: E402
from ris_mu.train import run_training, make_loaders, set_seed   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16000)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    panel, cfg = make_scenario(n_users=args.users, seed=11)
    d = MultiUserRISChannel(panel, cfg).generate(args.n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    Fc = torch.from_numpy(d["F"]).to(torch.complex64)
    Gc = torch.from_numpy(d["G"]).to(torch.complex64)
    hd = torch.from_numpy(d["hd"]).to(torch.complex64)
    N, sc = panel.N, cfg.snr_scale()

    itr, iva, ite = split_indices(args.n, seed=0)
    tr, va, te = make_loaders((X, Fc, Gc, hd), itr, iva, ite, batch_size=128)

    def step_fn(model, b):
        Xb, Fb, Gb, hb = b
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

    set_seed(42)
    model = EquivariantRIS(residual=True)
    print(f"Equiv+residual  ({count_params(model):,} params)")
    _, m0 = eval_fn(model, te)
    print(f"  before training: min={m0['min_rate']:.3f}  sum={m0['sum_rate']:.3f}")

    info = run_training(model, tr, va, step_fn, eval_fn, epochs=args.epochs,
                        lr=2e-3, tag="residual", patience=12,
                        milestones=(25, 40, 48))
    _, m = eval_fn(model, te)
    model.eval()
    with torch.no_grad():
        t0 = time.perf_counter()
        for Xb, *_ in te:
            model(Xb)
        m["ms_per_sample"] = (time.perf_counter() - t0) * 1e3 / len(ite)
    m["params"] = count_params(model)
    m["untrained_min_rate"] = m0["min_rate"]
    print(f"  after  training: min={m['min_rate']:.3f}  sum={m['sum_rate']:.3f}"
          f"  ({info['minutes']:.1f} min)")

    torch.save(model.state_dict(), os.path.join(args.out, "step4_Equiv+residual.pt"))
    p = os.path.join(args.out, "step4_multiuser.json")
    res = json.load(open(p))
    res["Equiv+residual"] = m
    json.dump(res, open(p, "w"), indent=2)

    ref = res["PGA max-min"]["min_rate"]
    print(f"\n{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}{'ms/sample':>11}")
    print("-" * 58)
    for k, v in res.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}")


if __name__ == "__main__":
    main()
