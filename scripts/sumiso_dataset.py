"""
Dataset for the phase-aware CNN-LSTM in the mobility scenario (single user).

Scenario = the aging set of the latency study with one user: 3GPP TR 38.901
InH-Office, 8-antenna BS at (20,6,4) m, wall-mounted 8x4 RIS, 20 scatterers,
direct link blocked by 40 dB, 3 GHz. Training snapshots are drawn with a
different seed (2026) from the evaluation set (seed 11), 40 000 scenarios
as in the published model, split 70/15/15.

Labels: exact element-wise coordinate ascent (ris_mu.sumiso.solver), best of
SU-alignment and 3 random starts; it matches 3-start, 1000-step Adam to
within 1.3e-3 b/s/Hz per scenario (checked on 300 scenarios).

Output: data_sumiso/sumiso_<tag>.npz (not committed; regenerate with this
script). Input features follow the published model's per-element layout,
extended to a multi-antenna BS: Re/Im of g_n (2), Re/Im of F_n (2T) and
Re/Im of h_d broadcast to every element (2T) -> 2 + 4T channels x N.
"""
import sys
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=40000)
ap.add_argument("--seed", type=int, default=2026)
ap.add_argument("--tag", default="train")
ap.add_argument("--tx", type=int, default=8, help="BS antennas (1 = the published SISO setting)")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "data_sumiso"
OUT.mkdir(exist_ok=True)

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=a.tx, seed=a.seed)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,), "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(a.n)
F = torch.as_tensor(d["F"], dtype=torch.complex64)
G = torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64)
H = torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64)
A, Bc = SV.cascade(F, G, H)
th = torch.empty(a.n, F.shape[1])
val = torch.empty(a.n)
for i in range(0, a.n, 2000):
    s = slice(i, i + 2000)
    th[s], val[s] = SV.solve(A[s], Bc[s], seed=i)
    print(f"  labelled {min(i + 2000, a.n)}/{a.n}", flush=True)
np.savez_compressed(OUT / f"sumiso_{a.tag}.npz", F=d["F"], G=d["G_t"][:, 0], hd=d["hd_t"][:, 0],
                    theta=th.numpy(), gain=val.numpy(), snr_scale=cfg.snr_scale(), seed=a.seed)
print(f"wrote data_sumiso/sumiso_{a.tag}.npz  ({a.n} scenarios, N={F.shape[1]}, T={F.shape[2]})")
