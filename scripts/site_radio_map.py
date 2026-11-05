"""
Training-free baselines built from the SAME site survey as the position-trained
CNN (independent audit, 2026-11-06):

  kNN radio map   the phase that maximizes the summed gain over the stacked
                  channels of the k nearest surveyed positions (exact
                  coordinate ascent on the stacked problem), + best of 4
                  common phases
  NN lookup       the stored optimal phase of the nearest surveyed position
                  (+ best of 4 common phases)
  fixed phase     one phase for the whole site: the optimum of the stacked
                  channels of 2000 surveyed positions
compared with the CNN on the same test positions. No timing.
Writes results/site_radio_map.json.
"""
import sys
import json
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.site import Site
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase
from ris_mu.sumiso.position import position_features, pick_common_phase

ap = argparse.ArgumentParser()
ap.add_argument("--sites", type=int, nargs="*", default=[1, 2, 3, 4, 5])
ap.add_argument("--n_test", type=int, default=2000)
ap.add_argument("--k", type=int, default=20)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
rng_bs = np.random.default_rng(0)


def paired(x, y):
    d = x - y
    bs = [d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    return [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def stacked_solve(Bs, As, sweeps=10):
    """Maximize sum_j |a_j + B_j^T v|^2 over v: concatenate the T-dim channels of the neighbours."""
    S, k, N, T = Bs.shape
    Bcat = Bs.permute(0, 2, 1, 3).reshape(S, N, k * T)
    Acat = As.reshape(S, k * T)
    th0 = SV.su_align(Acat, Bcat)
    return SV.coord_ascent(Acat, Bcat, th0, sweeps=sweeps)[0]


res = {}
for s in a.sites:
    z = np.load(ROOT / "data_site" / f"site{s}.npz")
    site = Site(seed=s)
    snr = float(z["snr_scale"])
    n = a.n_test
    Fm = torch.as_tensor(z["F"])
    def cas(G, H):
        m = len(G)
        return SV.cascade(Fm.expand(m, *Fm.shape), torch.as_tensor(G), torch.as_tensor(H))
    At, Bt = cas(z["test_G"][:n], z["test_hd"][:n])
    Atr, Btr = cas(z["train_G"], z["train_hd"])
    rate = lambda th: torch.log2(1 + snr * SV.gain(th, At, Bt)).numpy()
    ptr, pte = z["train_pos"], z["test_pos"][:n]
    d2 = ((pte[:, None, :] - ptr[None]) ** 2).sum(-1)
    nn_idx = np.argsort(d2, axis=1)[:, :a.k]
    r_knn = rate(pick_common_phase(stacked_solve(Btr[nn_idx], Atr[nn_idx]), At, Bt))
    r_nn = rate(pick_common_phase(torch.as_tensor(z["train_theta"][nn_idx[:, 0]]), At, Bt))
    sub = torch.as_tensor(np.random.default_rng(s).choice(len(ptr), 2000, replace=False))
    fixed = stacked_solve(Btr[sub][None], Atr[sub][None], sweeps=20)[0]
    r_fix = rate(pick_common_phase(fixed.expand(n, -1).clone(), At, Bt))
    ck = torch.load(ROOT / "results" / f"site{s}_cnn_err0.pt")
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], "seq"); net.load_state_dict(ck["state"]); net.eval()
    with torch.no_grad():
        th = phase(net((position_features(site, pte) - ck["mu"]) / ck["sd"]))
    r_cnn = rate(pick_common_phase(th, At, Bt))
    res[str(s)] = dict(n_test=n, k=a.k, knn=float(r_knn.mean()), nn_lookup=float(r_nn.mean()),
                       fixed_site_phase=float(r_fix.mean()), cnn=float(r_cnn.mean()),
                       cnn_minus_knn=paired(r_cnn, r_knn), cnn_minus_nn=paired(r_cnn, r_nn),
                       median_nn_distance_m=float(np.sqrt(d2.min(1)).mean()))
    print(s, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[str(s)].items()}, flush=True)
json.dump(res, open(ROOT / "results" / "site_radio_map.json", "w"), indent=1)
