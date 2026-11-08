"""
Spatial correlation of the cascaded channel b_n = g_n F_n between RIS elements
(single-user MISO training draw, validation split), the reason the
partial-CSI experiment (ON_KAYIT_KISMI_CSI.md) favours element grouping.

|rho(lag)| = |E[b_n^H b_{n+lag}]| / E[|b_n|^2], each scenario normalised to unit
mean element power; lag 1 = vertical neighbour (same column), 4 = horizontal
neighbour, 8 = two columns apart. Element order n = 4 col + row.
Writes results/sumiso_partial_correlation.json.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso import solver as SV

ROOT = pathlib.Path(__file__).resolve().parents[1]
z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
perm = np.random.default_rng(0).permutation(len(z["theta"]))
out = {}
for name, ix in (("val_first_1000", perm[28000:29000]), ("val_6000", perm[28000:34000])):
    _, B = SV.cascade(torch.as_tensor(z["F"][ix]), torch.as_tensor(z["G"][ix]), torch.as_tensor(z["hd"][ix]))
    Bn = B / B.abs().pow(2).mean((1, 2), keepdim=True).sqrt()
    r = {}
    for lag, lbl in ((1, "vertical_lag1"), (4, "horizontal_lag4"), (8, "horizontal_lag8")):
        idx = [n for n in range(32 - lag) if (lag != 1 or n % 4 != 3)]
        c = (Bn[:, idx] * Bn[:, [i + lag for i in idx]].conj()).sum(-1).mean() / (Bn[:, idx].abs() ** 2).sum(-1).mean()
        r[lbl] = float(c.abs())
    out[name] = dict(n=len(ix), **r)
    print(name, r)
json.dump(out, open(ROOT / "results" / "sumiso_partial_correlation.json", "w"), indent=1)
