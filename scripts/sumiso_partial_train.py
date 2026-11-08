"""
Train a learned arm of the partial-CSI experiment (ON_KAYIT_KISMI_CSI.md).

  --model A : the published phase-aware CNN-LSTM (head 'seq'), input +1 mask channel
  --model B : the new phase-aware 2D-CNN-BiLSTM (ris_mu.sumiso.partial.CNN2DBiLSTM)
  --model C : B with a direct-angle output and plain MSE (representation ablation)
  --M       : observed elements (8, 16, 32) -> M + 1 pilots

Input: masked cascade features (unobserved b_n zeroed) + a + mask, z-scored
with training statistics. Target: the optimum of the TRUE full channel with
its common phase removed (element 1 at zero). Recipe identical to
scripts/sumiso_train.py: same 70/15/15 split, 50 epochs, Adam 1e-3 halved at
15/30/45, batch 256, gradient clipping 1.0, checkpoint with the best
validation phase RMSE. Output: results/sumiso_partial_<model>_M<M>_s<seed>.{pt,json}.
Evaluation against the classical arms is done by scripts/sumiso_partial_eval.py.
"""
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, phase_aware_loss, angle_mse_loss, canonical
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso import partial as P

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True, choices=["A", "B", "C"])
ap.add_argument("--M", type=int, required=True, choices=[8, 16, 32])
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--batch", type=int, default=256)
ap.add_argument("--threads", type=int, default=2)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.manual_seed(a.seed)
torch.set_num_threads(a.threads)
tag = f"sumiso_partial_{a.model}_M{a.M}_s{a.seed}"

z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
A_all, B_all = SV.cascade(torch.as_tensor(z["F"]), torch.as_tensor(z["G"]), torch.as_tensor(z["hd"]))
TH = canonical(torch.as_tensor(z["theta"]).float())
m = P.mask(a.M)
X = P.features_partial(A_all, B_all, m)
S, C, N = X.shape
idx = np.random.default_rng(0).permutation(S)          # same split as sumiso_train.py
ntr, nva = int(0.7 * S), int(0.15 * S)
tr, va = idx[:ntr], idx[ntr:ntr + nva]
mu = X[tr].mean(0, keepdim=True)
sd = X[tr].std(0, keepdim=True)
Xn = (X - mu) / (sd + 1e-9)

if a.model == "A":
    model = PhaseAwareCNNLSTM(C, N, "seq", n_out=2)
else:
    model = P.CNN2DBiLSTM(C, N, n_out=2 if a.model == "B" else 1)
LOSS = angle_mse_loss if a.model == "C" else phase_aware_loss
nparam = sum(p.numel() for p in model.parameters())
opt = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999), eps=1e-8)
sched = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=[15, 30, 45], gamma=0.5)


def predict(ix):
    model.eval()
    with torch.no_grad():
        return torch.cat([phase(model(Xn[ix[i:i + 2048]])) for i in range(0, len(ix), 2048)])


def rmse_deg(th_hat, th):
    d = torch.angle(torch.exp(1j * (th_hat - th).to(torch.complex64)))
    return float(torch.sqrt((d ** 2).mean()) * 180 / np.pi)


print(f"{tag}: S={S} C={C} N={N} params={nparam}", flush=True)
hist, best, best_state = [], 1e9, None
for ep in range(1, a.epochs + 1):
    model.train()
    t0 = time.time()
    perm = torch.as_tensor(np.random.default_rng(ep + 1000 * a.seed).permutation(tr))
    tot = 0.0
    for i in range(0, len(perm), a.batch):
        b = perm[i:i + a.batch]
        loss = LOSS(model(Xn[b]), TH[b])
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tot += loss.item() * len(b)
    sched.step()
    vr = rmse_deg(predict(va), TH[va])
    hist.append(dict(epoch=ep, train_loss=tot / len(tr), val_rmse_deg=vr, sec=time.time() - t0))
    if vr < best:
        best, best_state = vr, {k: v.clone() for k, v in model.state_dict().items()}
    print(f"ep {ep:2d}  loss {tot / len(tr):.4f}  val RMSE {vr:6.2f} deg  ({time.time() - t0:.0f}s)", flush=True)

torch.save(dict(state=best_state, mu=mu, sd=sd, C=C, N=N, model=a.model, M=a.M), ROOT / "results" / f"{tag}.pt")
json.dump(dict(config=vars(a), params=nparam, best_val_rmse_deg=best, history=hist),
          open(ROOT / "results" / f"{tag}.json", "w"), indent=1)
print("wrote", tag)
