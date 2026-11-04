"""
Discrete-phase labels (1, 2, 3 bits) for data_sumiso/sumiso_train.npz:
best of exact discrete coordinate ascent started from the rounded continuous
optimum and from rounded SU alignment (ris_mu.sumiso.solver.solve_discrete).
Writes data_sumiso/sumiso_train_disc<b>.npz (theta, gain).
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from ris_mu.sumiso import solver as SV

ROOT = pathlib.Path(__file__).resolve().parents[1]
z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
A, Bc = SV.cascade(torch.as_tensor(z["F"]), torch.as_tensor(z["G"]), torch.as_tensor(z["hd"]))
TH = torch.as_tensor(z["theta"]).float()
snr = float(z["snr_scale"])
for b in (1, 2, 3):
    th = torch.empty_like(TH); g = torch.empty(len(TH))
    for i in range(0, len(TH), 2000):
        s = slice(i, i + 2000)
        th[s], g[s] = SV.solve_discrete(A[s], Bc[s], TH[s], b)
    np.savez_compressed(ROOT / "data_sumiso" / f"sumiso_train_disc{b}.npz", theta=th.numpy(), gain=g.numpy(), bits=b)
    r = torch.log2(1 + snr * g)
    rq = torch.log2(1 + snr * SV.gain(SV.quantise(TH, b), A, Bc))
    print(f"{b} bit: discrete label rate {r.mean():.4f}, rounded continuous optimum {rq.mean():.4f}, "
          f"on grid: {bool(torch.allclose(SV.quantise(th, b), th))}", flush=True)
