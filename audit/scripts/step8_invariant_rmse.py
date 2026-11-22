"""
Audit step 8: common-phase-invariant RMSE, the metric the thesis proposes (min over phi of RMSE(theta_hat + phi, theta*)),
for the trained CNN-LSTM (audit/raw/train/cnnlstm_N32_s{0,1,2}.pt, NO retraining) and coordinate descent (ris_CD.m port),
on the SAME test scenarios of the independent NumPy draw (m1_data.generate(40000, seed=42), split seed 42).

Why: the published label (a) = -angle(G_n F_n) ignores h_d; the true optimum (b) = angle(h_d) - angle(G_n F_n) differs from (a)
by one common phase per scenario. RMSE-to-(a) therefore punishes CD for converging to (b). Removing the best common phase makes
RMSE-to-(a) and RMSE-to-(b) identical, so it scores the SHAPE of the phase profile only. Received power and rate are reported
next to it, because the common phase is NOT free when h_d != 0 (it sets how the RIS path adds to the direct path).

Definitions (same as step2_baselines.metrics):
  e      = wrap(theta_hat - label_a)
  phi*   = angle(mean_n exp(j e_n))  (per scenario; the minimiser of sum_n |wrap(e_n - phi)|^2 up to wrap effects)
  rmse_inv = RMS over scenarios x elements of wrap(e - phi*)
  rate   = log2(1 + |h_d + sum_n G_n F_n e^{j theta_n}|^2 / 1e-3)   (Pt = 1, noise 1e-3, as step2/step6)
Output: audit/raw/step8_invariant_rmse.json, audit/raw/step8_abs_err_deg.npz (|error| per test scenario x element, deg)
"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch, torch.nn as nn
from m1_data import generate, split

ROOT = pathlib.Path(__file__).resolve().parents[2]
torch.set_num_threads(1)
cache = ROOT / "audit/raw/data/m1_N32_n40000_seed42.npz"
if not cache.exists():
    cache.parent.mkdir(parents=True, exist_ok=True)
    D = generate(40000, N=32, seed=42)
    np.savez(cache, F=D["F"], G=D["G"], hd=D["hd"], theta=D["theta"])
z = np.load(cache)
tr, va, te = split(len(z["hd"]), seed=42)
F, G, hd, TH = z["F"][te], z["G"][te], z["hd"][te], z["theta"][te]
N = F.shape[1]
wrap = lambda x: np.angle(np.exp(1j * x))
b = G * F


class CNNLSTM(nn.Module):                     # identical to step6_eval.py / m1_train.py (hidden 128/64)
    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                                 nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
        self.l1 = nn.LSTM(64, 128, batch_first=True); self.l2 = nn.LSTM(128, 64, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, 2))

    def forward(self, x):
        h = self.cnn(x).transpose(1, 2); h, _ = self.l1(h); h, _ = self.l2(h); return self.out(h)


def predict(m):
    X = torch.tensor(np.stack([F.real, F.imag, G.real, G.imag], 1).astype(np.float32))
    with torch.no_grad():
        o = torch.cat([m(X[i:i + 2000]) for i in range(0, len(X), 2000)])
    return torch.atan2(o[..., 0], o[..., 1]).numpy().astype(np.float64)


def cd(K):                                     # ris_CD.m: start theta = 0, closed-form per element incl. h_d, K sweeps
    th = np.zeros(F.shape)
    for _ in range(K):
        for n in range(N):
            msk = np.ones(N, bool); msk[n] = False
            Hm = hd + (b[:, msk] * np.exp(1j * th[:, msk])).sum(1)
            th[:, n] = wrap(np.angle(Hm) - np.angle(b[:, n]))
    return th


rate = lambda th: np.log2(1 + np.abs(hd + (b * np.exp(1j * th)).sum(1)) ** 2 / 1e-3)
lb = wrap(np.angle(hd)[:, None] - np.angle(b))
R_opt = rate(lb)


ERR = {}


def metrics(th, key=None):
    e = wrap(th - TH)
    phi = np.angle(np.exp(1j * e).mean(1, keepdims=True))
    ei = wrap(e - phi)
    d = lambda x: float(np.sqrt(np.mean(x ** 2)) * 180 / np.pi)
    r = rate(th)
    # same profile, but with its common phase re-aligned to h_d (what a 1-parameter post-correction would give)
    th_fix = wrap(th - phi + np.angle(hd)[:, None])
    if key:
        ERR[key + "_pub"] = (np.abs(e) * 180 / np.pi).astype(np.float32).ravel()
        ERR[key + "_inv"] = (np.abs(ei) * 180 / np.pi).astype(np.float32).ravel()
    return dict(rmse_pub_deg=d(e), rmse_inv_deg=d(ei), sr5_inv=float((np.abs(ei) < np.deg2rad(5)).mean()),
                rate_bpshz=float(r.mean()), loss_vs_opt_bpshz=float((R_opt - r).mean()),
                rate_after_common_phase_fix_bpshz=float(rate(th_fix).mean()))


res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           data="m1_data.generate(40000, N=32, seed=42), split seed 42 (NumPy port, independent draw, not MATLAB rng(42))",
           n_test=int(len(te)), optimum_rate_bpshz=float(R_opt.mean()),
           label_a=metrics(TH), optimum_b=metrics(lb), cnnlstm={}, cd={})
for s in (0, 1, 2):
    p = ROOT / f"audit/raw/train/cnnlstm_N32_s{s}.pt"
    net = CNNLSTM(); net.load_state_dict(torch.load(p)); net.eval()
    res["cnnlstm"][f"s{s}"] = metrics(predict(net), f"cnnlstm_s{s}"); print("cnnlstm", s, res["cnnlstm"][f"s{s}"], flush=True)
for K in (5, 20, 50):
    res["cd"][f"K{K}"] = metrics(cd(K), f"cd_K{K}"); print("cd", K, res["cd"][f"K{K}"], flush=True)
np.savez_compressed(ROOT / "audit/raw/step8_abs_err_deg.npz", **ERR)
json.dump(res, open(ROOT / "audit/raw/step8_invariant_rmse.json", "w"), indent=1)
print("label_a", res["label_a"]); print("optimum", res["optimum_b"])
