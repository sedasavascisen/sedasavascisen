"""
Straight-through fine-tuning of the phase-aware CNN-LSTM for b-bit phases.

Starts from the network trained on discrete labels (sumiso_train.py
--disc_bits b) and minimises -rate of the QUANTISED phase directly:
theta -> closed-form common phase -> theta_q = theta + (round(theta) - theta).detach(),
loss = -mean log2(1 + snr |a + B^T e^{j theta_q}|^2). The forward pass sees the
grid, the backward pass treats rounding as identity (straight-through).
Adam lr 1e-4, batch 256, `--epochs` epochs; the checkpoint with the best
validation rate of the deployed pipeline (round, best grid rotation) is kept.
"""
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features, restore_common_phase
from ris_mu.sumiso import solver as SV

ap = argparse.ArgumentParser()
ap.add_argument("--bits", type=int, required=True)
ap.add_argument("--epochs", type=int, default=10)
ap.add_argument("--threads", type=int, default=1)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.manual_seed(0)
torch.set_num_threads(a.threads)
src = f"sumiso_cnnlstm_seq_disc{a.bits}"
ck = torch.load(ROOT / "results" / f"{src}.pt")
net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck["head"], ck["n_out"])
net.load_state_dict(ck["state"])
mu, sd = ck["mu"], ck["sd"]

z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
F, G, H = (torch.as_tensor(z[k]) for k in ("F", "G", "hd"))
snr = float(z["snr_scale"])
Xn = (features(F, G, H, "cascade") - mu) / (sd + 1e-9)
A, B = SV.cascade(F, G, H)
idx = np.random.default_rng(0).permutation(len(F))
tr, va = idx[:28000], idx[28000:34000]


def deploy(th, a_, b_):
    return SV.best_grid_rotation(SV.quantise(restore_common_phase(th, a_, b_), a.bits), a_, b_, a.bits)


def val_rate():
    net.eval()
    with torch.no_grad():
        th = torch.cat([phase(net(Xn[va[i:i + 2000]])) for i in range(0, len(va), 2000)])
        return float(torch.log2(1 + snr * SV.gain(deploy(th, A[va], B[va]), A[va], B[va])).mean())


opt = torch.optim.Adam(net.parameters(), lr=1e-4)
start = val_rate()
best, best_state, hist = start, {k: v.clone() for k, v in net.state_dict().items()}, []
print(f"start (supervised discrete model): val rate {start:.4f}", flush=True)
step = 2 * torch.pi / 2 ** a.bits
for ep in range(1, a.epochs + 1):
    net.train()
    t0 = time.time()
    perm = torch.as_tensor(np.random.default_rng(100 + ep).permutation(tr))
    for i in range(0, len(perm), 256):
        b = perm[i:i + 256]
        th = restore_common_phase(phase(net(Xn[b])), A[b], B[b])
        thq = th + (torch.round(th / step) * step - th).detach()
        loss = -torch.log2(1 + snr * SV.gain(thq, A[b], B[b])).mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
    vr = val_rate()
    hist.append(dict(epoch=ep, val_rate=vr, sec=time.time() - t0))
    if vr > best:
        best, best_state = vr, {k: v.clone() for k, v in net.state_dict().items()}
    print(f"ep {ep:2d}  val rate {vr:.4f}  ({time.time()-t0:.0f}s)", flush=True)
torch.save(dict(ck, state=best_state), ROOT / "results" / f"sumiso_cnnlstm_seq_ste{a.bits}.pt")
json.dump(dict(config=vars(a), source=src, best_val_rate=best, start_val_rate=start, history=hist),
          open(ROOT / "results" / f"sumiso_cnnlstm_seq_ste{a.bits}.json", "w"), indent=1)
print("best val rate", best)
