"""
train.py (mumiso)
-----------------
Label-free training on the system metric.

WHY THERE ARE NO LABELS
-----------------------
For K = 1 the optimal phase has a closed form, so the published model could
be trained supervised against it. For K > 1 no closed form exists, so there
is nothing to regress onto. Training therefore maximises the rate directly:
the channel enters the loss, the precoder is computed inside it, and the
gradient flows back through the whole system model to the phases.

That is not a workaround, it is the better formulation -- a supervised model
can only ever approach the labels it was given, whereas this one optimises
the quantity the thesis actually reports.
"""

import time
import numpy as np
import torch

from . import system as S

__all__ = ["train_model", "evaluate"]


def _batches(n, bs, rng=None):
    idx = np.arange(n) if rng is None else rng.permutation(n)
    for i in range(0, n, bs):
        yield idx[i:i + bs]


@torch.no_grad()
def evaluate(net, X, F, G, hd, pt, nv, ids, precoder="zf", bits=None, bs=512):
    """Mean min-rate and sum-rate over `ids`."""
    net.eval()
    tot_min = tot_sum = 0.0
    for b in _batches(len(ids), bs):
        j = ids[b]
        c, s = net.phases(X[j])
        if bits is not None:
            c, s = S.quantise_ste(c, s, bits)
        R = S.rates(F[j], G[j], hd[j], c, s, pt, nv, precoder)
        tot_min += R.min(-1).values.sum().item()
        tot_sum += R.sum(-1).sum().item()
    return tot_min / len(ids), tot_sum / len(ids)


def train_model(net, X, F, G, hd, pt, nv, split, *, epochs=30, bs=64,
                lr=2e-3, lr_drops=(0.6, 0.85), objective="maxmin", beta=8.0,
                precoder="zf", bits=None, seed=0, log=print, clip=1.0):
    """
    Returns (net_with_best_val_weights, history).

    `split` is (train_ids, val_ids, test_ids). The reported model is the one
    with the best VALIDATION min-rate, never the last epoch -- otherwise the
    number reported is partly a function of where training happened to stop.
    """
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    tr, va, te = split
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    drops = {int(f * epochs) for f in lr_drops}

    best_val, best_state, hist = -np.inf, None, []
    for ep in range(1, epochs + 1):
        if ep in drops:
            for g in opt.param_groups:
                g["lr"] *= 0.5
        net.train()
        t0, run, nb = time.time(), 0.0, 0
        for b in _batches(len(tr), bs, rng):
            j = tr[b]
            c, s = net.phases(X[j])
            if bits is not None:
                c, s = S.quantise_ste(c, s, bits)
            R = S.rates(F[j], G[j], hd[j], c, s, pt, nv, precoder)
            loss = (S.maxmin_loss(R, beta) if objective == "maxmin"
                    else S.sumrate_loss(R))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), clip)
            opt.step()
            run += loss.item(); nb += 1

        v_min, v_sum = evaluate(net, X, F, G, hd, pt, nv, va, precoder, bits)
        hist.append(dict(epoch=ep, loss=run / max(nb, 1), val_min=v_min,
                         val_sum=v_sum, lr=opt.param_groups[0]["lr"],
                         sec=time.time() - t0))
        mark = ""
        if v_min > best_val:
            best_val = v_min
            best_state = {k: v.detach().clone()
                          for k, v in net.state_dict().items()}
            mark = "  *"
        if log:
            log(f"    epoch {ep:3d}/{epochs}  loss {run/max(nb,1):8.4f}  "
                f"val min {v_min:7.4f}  sum {v_sum:8.3f}  "
                f"({hist[-1]['sec']:.1f}s){mark}")

    if best_state is None:
        # Validation never improved -- a NaN loss in epoch 1 would do this.
        # Carry on with the final weights, but say so: silently returning an
        # empty model is how a crash gets mistaken for a bad result.
        if log:
            log("    WARNING: validation never improved; keeping final weights")
    else:
        net.load_state_dict(best_state)
    return net, hist
