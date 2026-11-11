"""
Infra task 4: Paper 1's phase-aware CNN-LSTM on this repository's 3GPP TR 38.901 generator.

Data interface (single user, N_t = 1, N = 32):
  channels  data_sumiso/sumiso_siso.npz, written by scripts/sumiso_dataset.py --tx 1 --tag siso
            (InH-Office, 8x4 RIS, 20 scatterers, 3 GHz, seed 2026, 40 000 static snapshots).
            If missing it is regenerated with that exact command (deterministic).
  input     Paper 1 format [Re F; Im F; Re G; Im G] per element, plus [Re h_d; Im h_d] broadcast over the
            elements (6 x N). The h_d channels are a deviation from Paper 1 (approved 11 Nov 2026): the
            optimal label below depends on angle(h_d), which Paper 1's input does not contain.
  label     theta_n = angle(h_d) - angle(G_n F_n)   (the optimum for N_t = 1; audit/AUDIT_REPORT.md item 1)
  scaling   --scale raw  : no input normalisation (Paper 1 / MATLAB sequenceInputLayer default)
            --scale norm : each scenario divided by the RMS of its cascaded coefficients (phase labels are
                           invariant to a positive scale, so the target is unchanged)
Arms: --head sincos (published) | angle (same network, one output per element, plain MSE on the wrapped
angle: the "direct phase" twin) ; --permute (fixed random element order, seed 7).
Training as audit/scripts/m1_train.py (MATLAB defaults; last epoch kept). Split 70/15/15, permutation seed 0.
Output: thesis_exp/infra/raw/m1_38901/<tag>.json (+ per-sample test errors .npy)
"""
import sys, json, time, argparse, pathlib, subprocess
import numpy as np, torch, torch.nn as nn

ap = argparse.ArgumentParser()
ap.add_argument("--head", default="sincos", choices=["sincos", "angle"])
ap.add_argument("--scale", default="raw", choices=["raw", "norm"])
ap.add_argument("--permute", action="store_true")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--threads", type=int, default=2)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "thesis_exp/infra/raw/m1_38901"; OUT.mkdir(parents=True, exist_ok=True)
tag = f"{a.head}_{a.scale}_s{a.seed}{'_perm' if a.permute else ''}"
torch.manual_seed(a.seed); torch.set_num_threads(a.threads)

src = ROOT / "data_sumiso/sumiso_siso.npz"
if not src.exists():
    subprocess.run([sys.executable, str(ROOT / "scripts/sumiso_dataset.py"), "--tx", "1", "--tag", "siso"], check=True, cwd=ROOT)
z = np.load(src)
F = z["F"][:, :, 0].astype(np.complex128)          # [S,N]   (T = 1)
G = z["G"][:, 0, :].astype(np.complex128)          # [S,N]
hd = z["hd"][:, 0, 0].astype(np.complex128)        # [S]
S, N = F.shape
b = G * F
TH = np.angle(np.exp(1j * (np.angle(hd)[:, None] - np.angle(b))))
perm = np.random.default_rng(7).permutation(N) if a.permute else np.arange(N)
F, G, TH = F[:, perm], G[:, perm], TH[:, perm]
if a.scale == "norm":
    sc = np.sqrt((np.abs(b) ** 2).mean(1, keepdims=True))
    Fx, Gx, hx = F / np.sqrt(sc), G / np.sqrt(sc), hd / sc[:, 0]
else:
    Fx, Gx, hx = F, G, hd
X = np.concatenate([np.stack([Fx.real, Fx.imag, Gx.real, Gx.imag], 1),
                    np.repeat(np.stack([hx.real, hx.imag], 1)[:, :, None], N, 2)], 1).astype(np.float32)
idx = np.random.default_rng(0).permutation(S)
ntr, nva = int(0.7 * S), int(0.15 * S)
tr, va, te = idx[:ntr], idx[ntr:ntr + nva], idx[ntr + nva:]
Xt, THt = torch.tensor(X), torch.tensor(TH, dtype=torch.float32)


class Net(nn.Module):
    def __init__(self, c_in, n_out):
        super().__init__()
        self.cnn = nn.Sequential(nn.Conv1d(c_in, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                                 nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
        self.l1 = nn.LSTM(64, 128, batch_first=True); self.l2 = nn.LSTM(128, 64, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, n_out))

    def forward(self, x):
        h = self.cnn(x).transpose(1, 2); h, _ = self.l1(h); h, _ = self.l2(h); return self.out(h)


model = Net(6, 2 if a.head == "sincos" else 1)
if a.head == "sincos":
    tgt = torch.stack([torch.sin(THt), torch.cos(THt)], -1)
    loss_fn = lambda o, t: 0.5 * ((o - t) ** 2).sum(-1).mean()
    to_phase = lambda o: torch.atan2(o[..., 0], o[..., 1])
else:
    tgt = THt
    loss_fn = lambda o, t: 0.5 * ((o[..., 0] - t) ** 2).mean()
    to_phase = lambda o: torch.angle(torch.exp(1j * o[..., 0].to(torch.complex64)))
opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.StepLR(opt, step_size=15, gamma=0.5)
wrap = lambda x: torch.angle(torch.exp(1j * x.to(torch.complex64)))


def predict(ix):
    model.eval()
    with torch.no_grad():
        return torch.cat([to_phase(model(Xt[ix[i:i + 2048]])) for i in range(0, len(ix), 2048)])


hist, t_all = [], time.time()
for ep in range(1, a.epochs + 1):
    model.train(); t0 = time.time(); tot = 0.0
    order = torch.as_tensor(np.random.default_rng(1000 * a.seed + ep).permutation(tr))
    for i in range(0, len(order), 256):
        bb = order[i:i + 256]
        loss = loss_fn(model(Xt[bb]), tgt[bb]); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(bb)
    sched.step()
    e = wrap(predict(va) - THt[va])
    hist.append(dict(epoch=ep, train_loss=tot / len(tr), val_rmse_deg=float(torch.sqrt((e ** 2).mean()) * 180 / np.pi), sec=time.time() - t0))
    print(f"{tag} ep {ep:2d} loss {tot/len(tr):.5f} val {hist[-1]['val_rmse_deg']:.2f} ({hist[-1]['sec']:.0f}s)", flush=True)

th = predict(te).numpy().astype(np.float64)
err = np.abs(np.angle(np.exp(1j * (th - TH[te])))) * 180 / np.pi
bt = (G * F)[te]
P = lambda t: np.abs(hd[te] + (bt * np.exp(1j * t)).sum(1)) ** 2
snr = float(z["snr_scale"])
rate = lambda t: np.log2(1 + snr * P(t))
np.save(OUT / f"{tag}_test_abs_err_deg.npy", err.astype(np.float32))
np.save(OUT / f"{tag}_test_rate.npy", rate(th).astype(np.float32))
res = dict(tag=tag, config=vars(a), commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           data="data_sumiso/sumiso_siso.npz (scripts/sumiso_dataset.py --tx 1 --tag siso, seed 2026)", n=dict(train=len(tr), val=len(va), test=len(te)),
           params=int(sum(p.numel() for p in model.parameters())),
           test_rmse_deg=float(np.sqrt((err ** 2).mean())), sr={f"SR@{t}": float((err < t).mean()) for t in (1, 3, 5, 10)},
           rate_bpshz=float(rate(th).mean()), rate_optimum_bpshz=float(rate(TH[te]).mean()),
           rate_published_label_a_bpshz=float(rate(-np.angle(bt)).mean()),
           power_vs_optimum_db=float(np.mean(10 * np.log10(P(th) / P(TH[te])))),
           train_minutes=(time.time() - t_all) / 60, history=hist)
torch.save(model.state_dict(), OUT / f"{tag}.pt")
json.dump(res, open(OUT / f"{tag}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "history"}, indent=1))
