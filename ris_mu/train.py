"""
train.py
--------
Small reusable training harness. Supports both the supervised phase-regression
setting and the unsupervised rate-maximising setting through a single
`step_fn` hook, so every experiment in the study runs the same optimiser,
schedule and early-stopping policy.
"""

import time
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader


def make_loaders(tensors, idx_tr, idx_va, idx_te, batch_size=256):
    def mk(idx, shuffle):
        ds = TensorDataset(*[t[idx] for t in tensors])
        return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)
    return mk(idx_tr, True), mk(idx_va, False), mk(idx_te, False)


def run_training(model, train_dl, val_dl, step_fn, eval_fn,
                 epochs=40, lr=1e-3, device="cpu", patience=12,
                 milestones=(15, 28, 36), verbose=True, tag=""):
    """
    step_fn(model, batch) -> loss tensor
    eval_fn(model, loader) -> (score_to_minimise, dict_of_metrics)
    """
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sch = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=list(milestones), gamma=0.5)

    best, best_state, best_ep, hist = float("inf"), None, 0, []
    t0 = time.time()

    for ep in range(1, epochs + 1):
        model.train()
        tot = 0.0
        for batch in train_dl:
            opt.zero_grad()
            loss = step_fn(model, batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item()
        sch.step()

        score, metrics = eval_fn(model, val_dl)
        hist.append(dict(epoch=ep, train_loss=tot / len(train_dl), score=score, **metrics))

        if score < best - 1e-6:
            best, best_ep = score, ep
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

        if verbose and (ep % 5 == 0 or ep == 1):
            ms = "  ".join(f"{k}={v:.3f}" for k, v in metrics.items())
            print(f"    [{tag}] ep {ep:3d}  loss={tot/len(train_dl):.5f}  {ms}"
                  f"{'  *' if ep == best_ep else ''}")

        if ep - best_ep >= patience:
            if verbose:
                print(f"    [{tag}] early stop at epoch {ep} (best {best_ep})")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return dict(best_score=best, best_epoch=best_ep,
                minutes=(time.time() - t0) / 60, history=hist)


def set_seed(s=42):
    np.random.seed(s)
    torch.manual_seed(s)
