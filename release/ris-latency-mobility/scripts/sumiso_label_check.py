"""
Label quality: the coordinate-ascent labels of data_sumiso/sumiso_train.npz
against a long-run Adam reference (3 random starts, 1000 steps, step 0.05,
best kept) on the first 300 scenarios. Backs the statement in
scripts/sumiso_dataset.py; writes results/sumiso_label_check.json.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from ris_mu.sumiso import solver as SV

ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
n = 300
A, B = SV.cascade(torch.as_tensor(z["F"][:n]), torch.as_tensor(z["G"][:n]), torch.as_tensor(z["hd"][:n]))
snr = float(z["snr_scale"])
rate = lambda th: torch.log2(1 + snr * SV.gain(th, A, B))
r_lab = rate(torch.as_tensor(z["theta"][:n]).float())
g = torch.Generator().manual_seed(0)
best = torch.full((n,), -1e9)
for r in range(3):
    th = (torch.rand(n, B.shape[1], generator=g) * 2 * np.pi).requires_grad_(True)
    opt = torch.optim.Adam([th], lr=0.05)
    for _ in range(1000):
        loss = -rate(th).sum(); opt.zero_grad(); loss.backward(); opt.step()
    best = torch.maximum(best, rate(th.detach()))
d = (best - r_lab).numpy()
res = dict(n=n, rate_label=float(r_lab.mean()), rate_long_adam=float(best.mean()),
           max_adam_minus_label=float(d.max()), mean_adam_minus_label=float(d.mean()))
json.dump(res, open(ROOT / "results" / "sumiso_label_check.json", "w"), indent=1)
print(res)
