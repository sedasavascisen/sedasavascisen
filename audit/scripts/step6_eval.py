"""
Audit step 2 (learned part: Fig. 8, Fig. 10 CNN arm) and step 6 (hardware impairments), using the
CNN-LSTM checkpoints trained by audit/scripts/m1_train.py (cnnlstm_N32_s{0,1,2}).

Fig. 8   CDF of |phase error| over test x elements: value of the CDF at 5 deg, and the error at 95 %.
Fig. 10  network fed F_hat, G_hat (audit/raw/step2_csi_inputs_x*.npz, error model in step2_baselines.py),
         scored against the TRUE label (a).
Step 6   (the paper gives no code; definitions here are stated, not inferred)
         quantisation: predicted phase rounded to the uniform 2^b grid {0, 2pi/2^b, ...}
         phase noise:  N(0, sigma^2) added to the predicted phase, sigma in {1,3,5} deg (seeded)
         each reported against the CONTINUOUS label (a): phase RMSE (deg) and rate loss (b/s/Hz),
         rate = log2(1 + Pt |h|^2 / noise_var), Pt = 1, noise_var = 1e-3; plus the same operations
         applied to the label itself (what quantising the optimum costs).
Output: audit/raw/step6_eval.json
"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch, torch.nn as nn
from m1_data import split

ROOT = pathlib.Path(__file__).resolve().parents[2]
torch.set_num_threads(2)
z = np.load(ROOT / "audit/raw/data/m1_N32_n40000_seed42.npz")
tr, va, te = split(len(z["hd"]), seed=42)
F, G, hd, TH = z["F"][te], z["G"][te], z["hd"][te], z["theta"][te]
wrap = lambda x: np.angle(np.exp(1j * x))


class CNNLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                                 nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
        self.l1 = nn.LSTM(64, 128, batch_first=True); self.l2 = nn.LSTM(128, 64, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, 2))

    def forward(self, x):
        h = self.cnn(x).transpose(1, 2); h, _ = self.l1(h); h, _ = self.l2(h); return self.out(h)


def predict(m, F, G):
    X = torch.tensor(np.stack([F.real, F.imag, G.real, G.imag], 1).astype(np.float32))
    with torch.no_grad():
        o = torch.cat([m(X[i:i + 2000]) for i in range(0, len(X), 2000)])
    return torch.atan2(o[..., 0], o[..., 1]).numpy().astype(np.float64)


def rate(th):
    return np.log2(1 + np.abs(hd + (G * F * np.exp(1j * th)).sum(1)) ** 2 / 1e-3)


def m(th):
    e = np.abs(wrap(th - TH)) * 180 / np.pi
    return dict(rmse_deg=float(np.sqrt((e ** 2).mean())), cdf_at_5deg=float((e < 5).mean()), err_p95_deg=float(np.percentile(e, 95)),
                rate_bpshz=float(rate(th).mean()), rate_loss_vs_label_bpshz=float((rate(TH) - rate(th)).mean()))


def quant(th, b):
    step = 2 * np.pi / 2 ** b
    return wrap(np.round(th / step) * step)


res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           n_test=len(te), label=dict(rate_bpshz=float(rate(TH).mean())), seeds={})
rng = np.random.default_rng(11)
res["label_impaired"] = {f"{b}bit": m(quant(TH, b)) for b in (1, 2, 3)}
res["label_impaired"].update({f"noise{s}deg": m(TH + np.deg2rad(s) * rng.standard_normal(TH.shape)) for s in (1, 3, 5)})
for s in (0, 1, 2):
    p = ROOT / f"audit/raw/train/cnnlstm_N32_s{s}.pt"
    if not p.exists():
        continue
    net = CNNLSTM(); net.load_state_dict(torch.load(p)); net.eval()
    th = predict(net, F, G)
    r = dict(clean=m(th))
    for b in (1, 2, 3):
        r[f"{b}bit"] = m(quant(th, b))
    for sd in (1, 3, 5):
        r[f"noise{sd}deg"] = m(th + np.deg2rad(sd) * rng.standard_normal(th.shape))
    r["csi_error"] = {}
    for x in (0.0, 0.05, 0.10, 0.15, 0.20):
        q = np.load(ROOT / f"audit/raw/step2_csi_inputs_x{x}.npz")
        r["csi_error"][str(x)] = m(predict(net, q["Fh"].astype(complex), q["Gh"].astype(complex)))
    res["seeds"][str(s)] = r
    print(s, {k: round(v["rmse_deg"], 2) for k, v in r.items() if k != "csi_error"},
          {k: round(v["rmse_deg"], 2) for k, v in r["csi_error"].items()}, flush=True)
json.dump(res, open(ROOT / "audit/raw/step6_eval.json", "w"), indent=1)
print("wrote audit/raw/step6_eval.json")
