"""
step5b_mixed_users.py
---------------------
Being DEFINED for any number of users is not the same as being ACCURATE for
any number of users.

Step 5 trained the equivariant model at U = 4 and evaluated it elsewhere. It
accepted every user count without modification -- the concatenated model
could not be evaluated at all -- but its margin over the single-user closed
form eroded as U moved away from 4, and reversed by U = 8. The symmetry buys
applicability, not accuracy.

This script tests the obvious remedy: train across a range of user counts.
The model is unchanged; only the training distribution is. Batches are drawn
from per-U datasets in round robin, so each gradient step sees one user count
and the model sees all of them.

Usage:  python scripts/step5b_mixed_users.py --per_u 4000 --epochs 45
"""

import argparse
import itertools
import json
import os
import sys

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ris_mu.channel import MultiUserRISChannel, make_scenario   # noqa: E402
from ris_mu.features import mu_features, split_indices          # noqa: E402
from ris_mu.models import EquivariantRIS, count_params          # noqa: E402
from ris_mu.losses import maxmin_loss, rate_metrics             # noqa: E402
from ris_mu.train import set_seed                               # noqa: E402
from ris_mu import baselines as BL                              # noqa: E402

TRAIN_US = (2, 3, 4, 5, 6)
TEST_US = (2, 3, 4, 6, 8)


def make_split(U, n, seed):
    panel, cfg = make_scenario(n_users=U, seed=seed)
    d = MultiUserRISChannel(panel, cfg).generate(n)
    X = torch.from_numpy(mu_features(d["F"], d["G"], d["hd"]))
    return (panel, cfg, X,
            torch.from_numpy(d["F"]).to(torch.complex64),
            torch.from_numpy(d["G"]).to(torch.complex64),
            torch.from_numpy(d["hd"]).to(torch.complex64))


class RoundRobin:
    """Yields batches from several loaders in turn, one user count each."""

    def __init__(self, loaders):
        self.loaders = loaders

    def __iter__(self):
        its = [iter(l) for l in self.loaders]
        alive = list(range(len(its)))
        while alive:
            for i in list(alive):
                try:
                    yield next(its[i])
                except StopIteration:
                    alive.remove(i)

    def __len__(self):
        return sum(len(l) for l in self.loaders)


@torch.no_grad()
def score(model, X, Fc, Gc, hd, N, sc, bs=256):
    model.eval()
    acc, n = {}, 0
    for i in range(0, len(X), bs):
        s = slice(i, i + bs)
        m = rate_metrics(Fc[s], Gc[s], hd[s], model(X[s]), N, sc)
        for k, v in m.items():
            acc[k] = acc.get(k, 0.0) + v * (s.stop - s.start)
        n += min(bs, len(X) - i)
    return {k: v / n for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per_u", type=int, default=4000)
    ap.add_argument("--epochs", type=int, default=45)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    set_seed(42)
    print(f"training user counts {TRAIN_US}, {args.per_u} scenarios each")

    tr_loaders, va_sets = [], []
    for U in TRAIN_US:
        panel, cfg, X, Fc, Gc, hd = make_split(U, args.per_u, seed=300 + U)
        itr, iva, _ = split_indices(args.per_u, frac=(0.8, 0.2, 0.0), seed=0)
        tr_loaders.append(DataLoader(
            TensorDataset(X[itr], Fc[itr], Gc[itr], hd[itr]),
            batch_size=128, shuffle=True))
        va_sets.append((X[iva], Fc[iva], Gc[iva], hd[iva], panel.N, cfg.snr_scale()))
    train_dl = RoundRobin(tr_loaders)

    model = EquivariantRIS(residual=False)
    print(f"model: {count_params(model):,} params\n")
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)
    sch = torch.optim.lr_scheduler.MultiStepLR(opt, [20, 32, 40], gamma=0.5)

    best, best_state, best_ep = -np.inf, None, 0
    for ep in range(1, args.epochs + 1):
        model.train()
        tot = 0.0
        for Xb, Fb, Gb, hb in train_dl:
            opt.zero_grad()
            loss = maxmin_loss(Fb, Gb, hb, model(Xb), Fb.shape[-1], va_sets[0][5])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item()
        sch.step()

        vals = [score(model, *v[:4], v[4], v[5])["min_rate"] for v in va_sets]
        mean_val = float(np.mean(vals))
        if mean_val > best:
            best, best_ep = mean_val, ep
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        if ep % 5 == 0 or ep == 1:
            per_u = "  ".join(f"U{u}={v:.2f}" for u, v in zip(TRAIN_US, vals))
            print(f"  ep {ep:3d}  loss={tot/len(train_dl):.4f}  mean={mean_val:.4f}"
                  f"   {per_u}{'  *' if ep == best_ep else ''}")

    model.load_state_dict(best_state)
    torch.save(model.state_dict(), os.path.join(args.out, "step5b_mixed.pt"))
    print(f"\nbest epoch {best_ep}\n")

    # ---------------------------------------------------------------- compare
    fixed = EquivariantRIS(residual=False).eval()
    fixed.load_state_dict(torch.load(os.path.join(args.out, "step4_Equivariant.pt")))

    print(f"{'U':>3}{'trained U=4':>13}{'trained mixed':>15}{'SU closed':>12}"
          f"{'PGA':>9}{'mixed % PGA':>13}")
    print("-" * 65)
    res = {}
    for U in TEST_US:
        panel, cfg, X, Fc, Gc, hd = make_split(U, 3000, seed=1000 + U)
        N, sc = panel.N, cfg.snr_scale()
        a = score(fixed, X, Fc, Gc, hd, N, sc)["min_rate"]
        b = score(model, X, Fc, Gc, hd, N, sc)["min_rate"]
        su = BL.summarise(BL.su_closed_form(Fc, Gc, hd, sc)[1])["min_rate"]
        pga = BL.summarise(BL.pga_maxmin(Fc, Gc, hd, sc, iters=250, restarts=3)[1])["min_rate"]
        res[U] = dict(fixed=a, mixed=b, su_closed=su, pga=pga)
        print(f"{U:>3}{a:>13.3f}{b:>15.3f}{su:>12.3f}{pga:>9.3f}{100*b/pga:>12.1f}%")

    print("\nmargin over the single-user closed form:")
    for U, v in res.items():
        print(f"  U={U}:  trained U=4 {100*(v['fixed']-v['su_closed'])/v['su_closed']:+6.1f}%"
              f"    trained mixed {100*(v['mixed']-v['su_closed'])/v['su_closed']:+6.1f}%")

    p = os.path.join(args.out, "step5b_mixed_users.json")
    json.dump({str(k): v for k, v in res.items()}, open(p, "w"), indent=2)
    print(f"\nsaved -> {p}")


if __name__ == "__main__":
    main()
