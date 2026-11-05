"""
Train the published phase-aware CNN-LSTM (authors' MATLAB architecture,
per-element head; published recipe: Adam 1e-3 halved every 15 epochs, 50
epochs, batch 256, phase-aware MSE, best-validation checkpoint, gradient
clipping 1.0) to predict the optimal RIS phase of a site from the USER
POSITION only (ris_mu.sumiso.position.position_features).
Labels: coordinate-ascent optimum with element 1 at zero (common phase is
chosen at deployment from 4 candidates, one pilot each).
Optional --pos_err: Gaussian position error (m, per axis) on the input,
redrawn every epoch; validation/test use one fixed draw.
"""
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, phase_aware_loss, canonical
from ris_mu.sumiso.site import Site
from ris_mu.sumiso.position import position_features

ap = argparse.ArgumentParser()
ap.add_argument("--site", type=int, required=True)
ap.add_argument("--pos_err", type=float, default=0.0)
ap.add_argument("--n_train", type=int, default=20000)
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--threads", type=int, default=1)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.manual_seed(a.seed); torch.set_num_threads(a.threads)
z = np.load(ROOT / "data_site" / f"site{a.site}.npz")
site = Site(seed=a.site)
tag = f"site{a.site}_cnn_err{a.pos_err:g}" + (f"_n{a.n_train}" if a.n_train != 20000 else "")
g = np.random.default_rng(7)
noisy = lambda p: p + a.pos_err * g.standard_normal(p.shape)
Ptr = z["train_pos"][:a.n_train]
Xtr = position_features(site, noisy(Ptr))
Xva = position_features(site, noisy(z["val_pos"]))
Ytr = canonical(torch.as_tensor(z["train_theta"][:a.n_train]))
Yva = canonical(torch.as_tensor(z["val_theta"]))
mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True) + 1e-9
model = PhaseAwareCNNLSTM(Xtr.shape[1], Xtr.shape[2], "seq")
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
sch = torch.optim.lr_scheduler.MultiStepLR(opt, [15, 30, 45], 0.5)


def val_rmse():
    model.eval()
    with torch.no_grad():
        th = phase(model((Xva - mu) / sd))
    d = torch.angle(torch.exp(1j * (th - Yva).to(torch.complex64)))
    return float(torch.sqrt((d ** 2).mean()) * 180 / np.pi)


best, state, hist = 1e9, None, []
for ep in range(1, a.epochs + 1):
    t0 = time.time()
    if a.pos_err > 0 and ep > 1:
        Xtr = position_features(site, noisy(Ptr))
    Xn = (Xtr - mu) / sd
    model.train()
    perm = torch.as_tensor(np.random.default_rng(ep + 1000 * a.seed).permutation(len(Xn)))
    for i in range(0, len(perm), 256):
        b = perm[i:i + 256]
        loss = phase_aware_loss(model(Xn[b]), Ytr[b])
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
    sch.step()
    v = val_rmse(); hist.append(dict(epoch=ep, val_rmse_deg=v))
    if v < best:
        best, state = v, {k: x.clone() for k, x in model.state_dict().items()}
    print(f"ep {ep:2d} val RMSE {v:6.2f} deg ({time.time()-t0:.0f}s)", flush=True)
torch.save(dict(state=state, mu=mu, sd=sd, C=Xtr.shape[1], N=Xtr.shape[2], head="seq", n_out=2), ROOT / "results" / f"{tag}.pt")
json.dump(dict(config=vars(a), best_val_rmse_deg=best, history=hist), open(ROOT / "results" / f"{tag}.json", "w"), indent=1)
print("best val RMSE", best)
