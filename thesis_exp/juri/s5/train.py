"""
Train PhaseNet without labels (soft-min beta = 8 user rate, fresh regularised ZF, t = 0 channel).
Usage: python3 train.py --fc 28|3 --head sincos|angle
Data: training seed 21 (n = 20000), validation seed 12 (n = 400; selection of the epoch), test seed 11 is never seen.
Adam lr 1e-3, batch 256, up to 60 epochs, wall-clock cap 25 min, best validation min-rate checkpoint kept.
Torch threads 2; model init seed 0; batch order seed 0. -> s5/raw/net_<fc>_<head>.pt and train_<fc>_<head>.json
"""
import sys, json, time, argparse, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np, torch
from ch28 import Aging28, Aging, commit
from model import PhaseNet, features
from ris_mu.mumiso import system as S
ap = argparse.ArgumentParser(); ap.add_argument("--fc", type=int, choices=(3, 28), required=True)
ap.add_argument("--head", choices=("sincos", "angle"), required=True); ap.add_argument("--n", type=int, default=20000)
a = ap.parse_args()
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
torch.set_num_threads(2)
Mk = (lambda s, n: Aging28(s, [0.0], n=n)) if a.fc == 28 else (lambda s, n: Aging(s, [0.0], n=n))
t0 = time.time()
tr, va = Mk(21, a.n), Mk(12, 400)
Xtr, Xva = features(tr.F, tr.G[0], tr.H[0]), features(va.F, va.G[0], va.H[0])
print(f"data {time.time() - t0:.0f} s; snr_scale {1 / tr.nv:.3e}", flush=True)
torch.manual_seed(0)
net = PhaseNet(a.head); opt = torch.optim.Adam(net.parameters(), lr=1e-3)
g = torch.Generator().manual_seed(0)


def minrate(A, X, idx=None):
    th = net(X if idx is None else X[idx])
    F, G, H = (A.F, A.G[0], A.H[0]) if idx is None else (A.F[idx], A.G[0][idx], A.H[0][idx])
    return S.rates(F, G, H, torch.cos(th), torch.sin(th), A.pt, A.nv, "zf")


with torch.no_grad():
    v0 = float(minrate(va, Xva).min(-1).values.mean())
hist, best, best_state = [dict(epoch=0, val=v0)], v0, {k: v.clone() for k, v in net.state_dict().items()}
torch.save(best_state, OUT / f"net_{a.fc}_{a.head}_untrained.pt")
for ep in range(1, 61):
    perm = torch.randperm(a.n, generator=g); tl = []
    for i in range(0, a.n, 256):
        idx = perm[i:i + 256]
        R = minrate(tr, Xtr, idx)
        loss = -(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()
        opt.zero_grad(); loss.backward(); opt.step(); tl.append(-loss.item())
    with torch.no_grad():
        v = float(minrate(va, Xva).min(-1).values.mean())
    hist.append(dict(epoch=ep, train_softmin=float(np.mean(tl)), val=v, seconds=time.time() - t0))
    if v > best:
        best, best_state = v, {k: x.clone() for k, x in net.state_dict().items()}
    print(f"ep {ep}: train {np.mean(tl):.4f} val {v:.4f} ({time.time() - t0:.0f} s)", flush=True)
    if time.time() - t0 > 25 * 60:
        print("time cap", flush=True); break
torch.save(best_state, OUT / f"net_{a.fc}_{a.head}.pt")
json.dump(dict(commit=commit(), fc_ghz=a.fc, head=a.head, n_train=a.n, best_val=best, history=hist),
          open(OUT / f"train_{a.fc}_{a.head}.json", "w"), indent=1)
print("wrote", flush=True)
