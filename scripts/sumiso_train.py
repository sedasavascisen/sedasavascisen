"""
Train the published phase-aware CNN-LSTM on the single-user mobility dataset.

Same training recipe as the published model: 70/15/15 split, z-score input
standardisation (train statistics), Adam lr 1e-3 (betas 0.9/0.999,
eps 1e-8) halved at epochs 15, 30 and 45, 50 epochs, batch 256, phase-aware
MSE loss, gradient-norm clipping at 1.0 (as in the authors' train_cnn_lstm.py).
Targets are the labels with the common phase removed (element 1 at zero). The checkpoint with the best validation phase RMSE is kept.
Reports test phase RMSE (degrees) and SR@5 deg against the coordinate-ascent
labels, and the achieved rate against the label and against SU alignment.
"""
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.cnn_lstm import (PhaseAwareCNNLSTM, phase, phase_aware_loss, features,
                                    canonical, restore_common_phase)
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso import csi as CSI
from ris_mu.sumiso.cnn_lstm import features_ab

ap = argparse.ArgumentParser()
ap.add_argument("--data", default="sumiso_train")
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--batch", type=int, default=256)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--tag", default="sumiso_cnnlstm")
ap.add_argument("--features", default="cascade", choices=["cascade", "raw"])
ap.add_argument("--csi_e2", type=float, default=0.0,
                help="train on estimated channels with this error power (fresh draw per epoch); labels stay the true optimum")
ap.add_argument("--head", default="flat", choices=["flat", "seq"])
ap.add_argument("--label", default="ref1", choices=["ref1", "published"],
                help="ref1: optimum with element 1 at zero; published: -angle(G_n F_n) (SISO only)")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.manual_seed(a.seed)
torch.set_num_threads(a.threads)

z = np.load(ROOT / "data_sumiso" / f"{a.data}.npz")
F = torch.as_tensor(z["F"]); G = torch.as_tensor(z["G"]); H = torch.as_tensor(z["hd"])
TH_raw = torch.as_tensor(z["theta"]).float()
if a.label == "published":       # the published SISO label, -angle(G_n F_n)
    assert F.shape[2] == 1
    TH = -torch.angle(G[:, 0, :] * F[:, :, 0]).float()
else:
    TH = canonical(TH_raw)          # training target: common phase removed
X = features(F, G, H, a.features)
S, C, N = X.shape
idx = np.random.default_rng(0).permutation(S)
ntr, nva = int(0.7 * S), int(0.15 * S)
tr, va, te = idx[:ntr], idx[ntr:ntr + nva], idx[ntr + nva:]
A_all, B_all = SV.cascade(F, G, H)
if a.csi_e2 > 0:
    assert a.features == "cascade"
    gen_noise = torch.Generator().manual_seed(12345)
    def noisy_X():
        ah, Bh = CSI.estimate(A_all, B_all, a.csi_e2, gen_noise)
        return features_ab(ah, Bh)
    X = noisy_X()          # val/test keep this draw; train is redrawn every epoch
mu = X[tr].mean(0, keepdim=True)
sd = X[tr].std(0, keepdim=True)
Xn = (X - mu) / (sd + 1e-9)

model = PhaseAwareCNNLSTM(C, N, a.head)
nparam = sum(p.numel() for p in model.parameters())
opt = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999), eps=1e-8)
sched = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=[15, 30, 45], gamma=0.5)


def rmse_deg(th_hat, th):
    d = torch.angle(torch.exp(1j * (th_hat - th).to(torch.complex64)))
    return float(torch.sqrt((d ** 2).mean()) * 180 / np.pi), d


def predict(ix):
    model.eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(ix), 2048):
            out.append(phase(model(Xn[ix[i:i + 2048]])))
    return torch.cat(out)


print(f"S={S} C={C} N={N} params={nparam}  train {len(tr)} / val {len(va)} / test {len(te)}", flush=True)
hist, best, best_state = [], 1e9, None
for ep in range(1, a.epochs + 1):
    if a.csi_e2 > 0 and ep > 1:
        Xn[tr] = ((noisy_X()[tr]) - mu) / (sd + 1e-9)
    model.train()
    t0 = time.time()
    perm = torch.as_tensor(np.random.default_rng(ep).permutation(tr))
    tot = 0.0
    for i in range(0, len(perm), a.batch):
        b = perm[i:i + a.batch]
        loss = phase_aware_loss(model(Xn[b]), TH[b])
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tot += loss.item() * len(b)
    sched.step()
    vr, _ = rmse_deg(predict(va), TH[va])
    hist.append(dict(epoch=ep, train_loss=tot / len(tr), val_rmse_deg=vr, sec=time.time() - t0))
    if vr < best:
        best, best_state = vr, {k: v.clone() for k, v in model.state_dict().items()}
    print(f"ep {ep:2d}  loss {tot/len(tr):.4f}  val RMSE {vr:6.2f} deg  ({time.time()-t0:.0f}s)", flush=True)

model.load_state_dict(best_state)
th_te = predict(te)
rm, d = rmse_deg(th_te, TH[te])            # vs canonical label (common phase removed)
sr = {f"SR@{t}": float((d.abs() * 180 / np.pi < t).float().mean()) for t in (1, 3, 5, 10)}
A, Bc = SV.cascade(F[te], G[te], H[te])
snr = float(z["snr_scale"])
rate = lambda th: torch.log2(1 + SV.gain(th, A, Bc) * snr)
th_net = restore_common_phase(th_te, A, Bc)
th_net1, _ = SV.coord_ascent(A, Bc, th_net, sweeps=1)
r_lab, r_net, r_net1, r_al = rate(TH_raw[te]), rate(th_net), rate(th_net1), rate(SV.su_align(A, Bc))
r_noref = rate(th_te)
den = float(r_lab.mean() - r_al.mean())   # 0 in SISO, where SU alignment is the optimum
gap = lambda r: float((r.mean() - r_al.mean()) / den) if den > 1e-4 else None
res = dict(config=vars(a), params=nparam, n=dict(train=len(tr), val=len(va), test=len(te)),
           test_rmse_deg=rm, **sr, best_val_rmse_deg=best,
           rate_label=float(r_lab.mean()), rate_cnnlstm=float(r_net.mean()),
           rate_cnnlstm_no_common_phase=float(r_noref.mean()),
           rate_cnnlstm_plus_1_sweep=float(r_net1.mean()),
           rate_su_align=float(r_al.mean()),
           gap_closed_cnnlstm=gap(r_net), gap_closed_cnnlstm_plus_1_sweep=gap(r_net1),
           history=hist)
torch.save(dict(state=best_state, mu=mu, sd=sd, C=C, N=N, head=a.head), ROOT / "results" / f"{a.tag}.pt")
json.dump(res, open(ROOT / "results" / f"{a.tag}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "history"}, indent=1))
