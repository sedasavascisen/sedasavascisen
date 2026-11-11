"""
PyTorch port of Paper 1's training (theta_NN_multioutput.m, zip md5 35f31d6e...; and the
FC-DNN of transformer_baseline.m). Port choices follow MATLAB defaults where the .m file is silent:

  input        X_s = [Re F; Im F; Re G; Im G]  (4 x N), NO normalisation
               (sequenceInputLayer default Normalization = 'none')
  CNN-LSTM     conv1d(4->64,k3,same)+BN+ReLU, conv1d(64->64,k3,same)+BN+ReLU, Dropout(0.2),
               LSTM(128, sequence), LSTM(64, sequence), Dropout(0.3), FC(2) per element
               (fullyConnectedLayer on a sequence acts per time step)
  target       [sin theta; cos theta]; loss = MATLAB regressionLayer half-MSE
               (0.5 * sum over responses, mean over observations and time steps)
  training     Adam lr 1e-3, piecewise x0.5 every 15 epochs, 50 epochs, batch 256,
               shuffle every epoch, L2Regularization 1e-4 (MATLAB default, applied as
               weight decay on all learnables), no gradient clipping (GradientThreshold Inf),
               the network after the LAST epoch is used (no checkpoint selection; MATLAB default)
  FC-DNN       transformer_baseline.m: z-scored flat input [Re F, Im F, Re G, Im G],
               512-BN-ReLU-Drop0.2-512-BN-ReLU-Drop0.2-256-ReLU-N, target = theta (direct), MSE
  --permute    fixed random permutation of the element order (input AND label), seed 7:
               the spatial-neighbourhood control

Every run writes audit/raw/train/<tag>.json (+ .pt): config, commit, seeds, per-epoch loss,
test RMSE (deg, wrapped), SR@{1,3,5,10}, received-power ratio to the label, per-element RMSE.
Data: audit/scripts/m1_data.py (NumPy port; independent draw, not the MATLAB samples).
"""
import sys, json, time, argparse, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
import torch
import torch.nn as nn
from m1_data import generate, split

ap = argparse.ArgumentParser()
ap.add_argument("--arch", default="cnnlstm", choices=["cnnlstm", "fcdnn_direct"])
ap.add_argument("--n", type=int, default=40000)
ap.add_argument("--N", type=int, default=32)
ap.add_argument("--data_seed", type=int, default=42)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--permute", action="store_true")
ap.add_argument("--hidden_scale", default="none", choices=["none", "sqrt"],
                help="sqrt: LSTM sizes {128,64}*(N/32)^0.5 rounded to a power of two (scalability_analysis.m comment)")
ap.add_argument("--tag", default="")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "audit" / "raw" / "train"; OUT.mkdir(parents=True, exist_ok=True)
tag = a.tag or f"{a.arch}_N{a.N}_s{a.seed}{'_perm' if a.permute else ''}"
torch.manual_seed(a.seed); np.random.seed(a.seed); torch.set_num_threads(a.threads)

cache = ROOT / "audit" / "raw" / "data" / f"m1_N{a.N}_n{a.n}_seed{a.data_seed}.npz"
cache.parent.mkdir(parents=True, exist_ok=True)
if cache.exists():
    z = np.load(cache); F, G, hd, TH = z["F"], z["G"], z["hd"], z["theta"]
else:
    D = generate(a.n, N=a.N, seed=a.data_seed); F, G, hd, TH = D["F"], D["G"], D["hd"], D["theta"]
    np.savez(cache, F=F, G=G, hd=hd, theta=TH)
perm = np.arange(a.N)
if a.permute:
    perm = np.random.default_rng(7).permutation(a.N)
    F, G, TH = F[:, perm], G[:, perm], TH[:, perm]
tr, va, te = split(a.n, seed=a.data_seed)

X = np.stack([F.real, F.imag, G.real, G.imag], 1).astype(np.float32)        # [S,4,N]
Xt = torch.tensor(X); THt = torch.tensor(TH, dtype=torch.float32)


def pow2(x):
    return int(2 ** round(np.log2(x)))


class CNNLSTM(nn.Module):
    def __init__(self, N):
        super().__init__()
        s = (N / 32) ** 0.5 if a.hidden_scale == "sqrt" else 1.0
        h1, h2 = (pow2(128 * s), pow2(64 * s)) if a.hidden_scale == "sqrt" else (128, 64)
        self.cnn = nn.Sequential(nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                                 nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
        self.l1 = nn.LSTM(64, h1, batch_first=True); self.l2 = nn.LSTM(h1, h2, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(h2, 2))

    def forward(self, x):
        h = self.cnn(x).transpose(1, 2)
        h, _ = self.l1(h); h, _ = self.l2(h)
        return self.out(h)                                   # [B,N,2] = (sin, cos)


class FCDNN(nn.Module):
    def __init__(self, N):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(4 * N, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.2),
                                 nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.2),
                                 nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, N))

    def forward(self, x):
        return self.net(x)


if a.arch == "cnnlstm":
    model = CNNLSTM(a.N); inp = Xt
    tgt = torch.stack([torch.sin(THt), torch.cos(THt)], -1)
    loss_fn = lambda o, t: 0.5 * ((o - t) ** 2).sum(-1).mean()
    to_phase = lambda o: torch.atan2(o[..., 0], o[..., 1])
else:
    flat = np.concatenate([F.real, F.imag, G.real, G.imag], 1).astype(np.float32)
    mu, sd = flat[tr].mean(0), flat[tr].std(0) + 1e-9
    model = FCDNN(a.N); inp = torch.tensor((flat - mu) / sd); tgt = THt
    loss_fn = lambda o, t: 0.5 * ((o - t) ** 2).mean()
    to_phase = lambda o: torch.angle(torch.exp(1j * o.to(torch.complex64)))

nparam = sum(p.numel() for p in model.parameters() if p.requires_grad)
opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.StepLR(opt, step_size=15, gamma=0.5)


def predict(ix):
    model.eval()
    with torch.no_grad():
        return torch.cat([to_phase(model(inp[ix[i:i + 2048]])) for i in range(0, len(ix), 2048)])


def wrap(x):
    return torch.angle(torch.exp(1j * x.to(torch.complex64)))


hist = []
t_start = time.time()
for ep in range(1, a.epochs + 1):
    model.train(); t0 = time.time(); tot = 0.0
    order = torch.as_tensor(np.random.default_rng(1000 * a.seed + ep).permutation(tr))
    for i in range(0, len(order), 256):
        b = order[i:i + 256]
        loss = loss_fn(model(inp[b]), tgt[b])
        opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(b)
    sched.step()
    e = wrap(predict(va) - THt[va])
    hist.append(dict(epoch=ep, train_loss=tot / len(tr), val_rmse_deg=float(torch.sqrt((e ** 2).mean()) * 180 / np.pi),
                     sec=time.time() - t0))
    print(f"{tag} ep {ep:2d} loss {tot/len(tr):.5f} val {hist[-1]['val_rmse_deg']:.2f} ({hist[-1]['sec']:.0f}s)", flush=True)

th = predict(te); e = wrap(th - THt[te])
err_deg = (e.abs() * 180 / np.pi).numpy()
inv = np.argsort(perm)
b_te = (G * F)[te]
P = lambda t: np.abs(hd[te] + (b_te * np.exp(1j * t)).sum(1)) ** 2
pw = 10 * np.log10(P(th.numpy()) / P(TH[te]))
np.save(OUT / f"{tag}_test_abs_err_deg.npy", err_deg.astype(np.float32))
res = dict(tag=tag, config=vars(a), params=nparam,
           commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           data=str(cache.relative_to(ROOT)), n_train=len(tr), n_val=len(va), n_test=len(te), permutation=perm.tolist(),
           test_rmse_deg=float(np.sqrt((err_deg ** 2).mean())),
           sr={f"SR@{t}": float((err_deg < t).mean()) for t in (1, 3, 5, 10)},
           err_deg_p95=float(np.percentile(err_deg, 95)),
           per_element_rmse_deg=np.sqrt((err_deg ** 2).mean(0))[inv].tolist(),
           power_vs_label_db=dict(mean=float(pw.mean()), median=float(np.median(pw))),
           train_minutes=(time.time() - t_start) / 60, history=hist)
torch.save(model.state_dict(), OUT / f"{tag}.pt")
json.dump(res, open(OUT / f"{tag}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("history", "per_element_rmse_deg", "permutation")}, indent=1))
