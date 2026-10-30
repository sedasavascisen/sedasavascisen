"""
step5_generalisation.py
-----------------------
What the symmetries actually buy, measured rather than asserted.

Two properties are claimed for the equivariant model and tested here against
the user-concatenated extension of the published architecture:

1. INVARIANCE TO USER ORDERING. The set of users has no natural order, so a
   model whose output changes when the users are relabelled is fitting an
   artefact. Measured as the spread of the achieved min-rate over random
   relabellings of the same scenario.

2. GENERALISATION ACROSS USER COUNT. A deployment does not hold U fixed.
   The equivariant model is defined for any U and is evaluated at user counts
   it never saw; the concatenated model cannot accept them at all, which is
   itself the result.

Both models are loaded from the step 4 checkpoints, so this script measures
the models that were actually trained rather than retrained variants.

Usage:  python scripts/step5_generalisation.py --n 4000
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario      # noqa: E402
from ris_mu.features import mu_features                            # noqa: E402
from ris_mu.models import EquivariantRIS, MUCNNLSTM                # noqa: E402
from ris_mu.losses import rate_metrics                             # noqa: E402
from ris_mu import baselines as BL                                 # noqa: E402


def make_set(users, n, seed):
    panel, cfg = make_scenario(n_users=users, seed=seed)
    d = MultiUserRISChannel(panel, cfg).generate(n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    return (panel, cfg, X,
            torch.from_numpy(d["F"]).to(torch.complex64),
            torch.from_numpy(d["G"]).to(torch.complex64),
            torch.from_numpy(d["hd"]).to(torch.complex64))


@torch.no_grad()
def score(model, X, Fc, Gc, hd, N, sc, bs=256):
    acc, n = {}, 0
    for i in range(0, len(X), bs):
        sl = slice(i, i + bs)
        m = rate_metrics(Fc[sl], Gc[sl], hd[sl], model(X[sl]), N, sc)
        for k, v in m.items():
            acc[k] = acc.get(k, 0.0) + v * (sl.stop - sl.start)
        n += min(bs, len(X) - i)
    return {k: v / n for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--trained_users", type=int, default=4)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    eq = EquivariantRIS(residual=False).eval()
    eq.load_state_dict(torch.load(os.path.join(args.out, "step4_Equivariant.pt")))
    res = {}

    # --- 1. sensitivity to user ordering ------------------------------------
    panel, cfg, X, Fc, Gc, hd = make_set(args.trained_users, args.n, seed=909)
    N, sc = panel.N, cfg.snr_scale()

    mu = MUCNNLSTM(N, args.trained_users).eval()
    mu.load_state_dict(torch.load(os.path.join(args.out, "step4_MU-CNN-LSTM.pt")))

    print(f"user-ordering sensitivity  (U={args.trained_users}, "
          f"{args.n} scenarios, 8 relabellings)")
    order = {}
    for name, model in (("MU-CNN-LSTM", mu), ("Equivariant", eq)):
        vals = []
        for r in range(8):
            p = torch.randperm(args.trained_users) if r else torch.arange(args.trained_users)
            vals.append(score(model, X[:, p], Fc, Gc[:, p], hd[:, p], N, sc)["min_rate"])
        vals = np.array(vals)
        order[name] = dict(mean=float(vals.mean()), std=float(vals.std()),
                           spread=float(vals.max() - vals.min()))
        print(f"  {name:<13} min-rate {vals.mean():.4f} "
              f"+- {vals.std():.4f}   spread {vals.max()-vals.min():.4f}")
    res["user_ordering"] = order

    # --- 2. generalisation across user count --------------------------------
    print(f"\ngeneralisation across user count (trained at U={args.trained_users})")
    print(f"{'U':>3}{'Equivariant':>14}{'PGA':>10}{'% of PGA':>10}{'MU-CNN-LSTM':>14}")
    print("-" * 51)
    gen = {}
    for U in (2, 3, 4, 6, 8):
        panel, cfg, X, Fc, Gc, hd = make_set(U, args.n, seed=1000 + U)
        N, sc = panel.N, cfg.snr_scale()
        e = score(eq, X, Fc, Gc, hd, N, sc)["min_rate"]
        pga = BL.summarise(BL.pga_maxmin(Fc, Gc, hd, sc, iters=250, restarts=3)[1])
        su = BL.summarise(BL.su_closed_form(Fc, Gc, hd, sc)[1])
        if U == args.trained_users:
            m = score(mu, X, Fc, Gc, hd, N, sc)["min_rate"]
            mu_str = f"{m:>13.3f}"
        else:
            m = None
            mu_str = f"{'undefined':>13}"
        gen[U] = dict(equivariant=e, pga=pga["min_rate"], su_closed=su["min_rate"],
                      mu_cnn_lstm=m)
        print(f"{U:>3}{e:>14.3f}{pga['min_rate']:>10.3f}"
              f"{100*e/pga['min_rate']:>9.1f}%{mu_str}")
    res["user_count"] = gen

    print("\n('undefined' is the result: the concatenated model fixes U in its "
          "first layer\n and cannot be evaluated at another user count without "
          "retraining.)")

    p = os.path.join(args.out, "step5_generalisation.json")
    json.dump(res, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
