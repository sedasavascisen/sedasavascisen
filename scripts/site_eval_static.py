"""
Static comparison on the site test positions (4000 per site, 5 sites).

Arms (rate log2(1 + snr |h|^2) with a maximum-ratio beam on the true
effective channel, which one effective-channel pilot provides):
  oracle            coordinate-ascent optimum (full CSI, free)       [CSI]
  SU-align, CD-1    closed form / one CD sweep on the full cascaded CSI [CSI]
  geometric         LoS steering from the position + best of 4 common phases [position]
  CNN-LSTM          position-trained network + best of 4 common phases   [position]
Position error sigma (m, per axis) is applied to the position-based arms'
input; the network used is the one trained at that sigma if it exists
(results/site<s>_cnn_err<sigma>.pt), else the sigma = 0 network (marked).
Paired bootstrap over test positions, per site; results also split by
RIS-user LoS / NLoS. Writes results/site_eval_static.json.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.site import Site
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase
from ris_mu.sumiso.position import geometric_phase, position_features, pick_common_phase

ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
import argparse
_ap = argparse.ArgumentParser(); _ap.add_argument("--sites", type=int, nargs="*", default=[1, 2, 3, 4, 5]); _ap.add_argument("--tag", default="site_eval_static")
_a = _ap.parse_args()
SITES = _a.sites
SIGMAS = [0.0, 0.05, 0.1, 0.3, 1.0]
rng_bs = np.random.default_rng(0)


def paired(x, y):
    d = x - y
    bs = [d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    return [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def load_net(s, sigma):
    p = ROOT / "results" / f"site{s}_cnn_err{sigma:g}.pt"
    trained_at = sigma
    if not p.exists():
        p = ROOT / "results" / f"site{s}_cnn_err0.pt"; trained_at = 0.0
    ck = torch.load(p)
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], "seq"); net.load_state_dict(ck["state"]); net.eval()
    return net, ck["mu"], ck["sd"], trained_at


res = {}
for s in SITES:
    z = np.load(ROOT / "data_site" / f"site{s}.npz")
    site = Site(seed=s)
    snr = float(z["snr_scale"])
    n = len(z["test_pos"])
    F = torch.as_tensor(np.broadcast_to(z["F"], (n,) + z["F"].shape).copy())
    A, B = SV.cascade(F, torch.as_tensor(z["test_G"]), torch.as_tensor(z["test_hd"]))
    rate = lambda th: torch.log2(1 + snr * SV.gain(th, A, B)).numpy()
    los = z["test_los"]
    al = SV.su_align(A, B)
    R = {"oracle": rate(torch.as_tensor(z["test_theta"])), "SU-align": rate(al),
         "CD-1": rate(SV.coord_ascent(A, B, al, sweeps=1, tol=-1)[0])}
    out = dict(los_fraction=float(los.mean()), csi={k: float(v.mean()) for k, v in R.items()}, by_sigma={})
    g = np.random.default_rng(1000 + s)
    for sig in SIGMAS:
        pos = z["test_pos"] + sig * g.standard_normal(z["test_pos"].shape)
        rg = rate(pick_common_phase(geometric_phase(site, pos), A, B))
        net, mu, sd, tr_at = load_net(s, sig)
        with torch.no_grad():
            th = phase(net((position_features(site, pos) - mu) / sd))
        rc = rate(pick_common_phase(th, A, B))
        out["by_sigma"][str(sig)] = dict(
            geometric=float(rg.mean()), cnn=float(rc.mean()), cnn_trained_at_sigma=tr_at,
            cnn_minus_geometric=paired(rc, rg), cnn_minus_cd1=paired(rc, R["CD-1"]),
            los=dict(geometric=float(rg[los].mean()), cnn=float(rc[los].mean()), cd1=float(R["CD-1"][los].mean()),
                     oracle=float(R["oracle"][los].mean())),
            nlos=dict(geometric=float(rg[~los].mean()), cnn=float(rc[~los].mean()), cd1=float(R["CD-1"][~los].mean()),
                      oracle=float(R["oracle"][~los].mean())))
    res[str(s)] = out
    b0 = out["by_sigma"]["0.0"]
    print(f"site {s}: oracle {out['csi']['oracle']:.3f} CD-1 {out['csi']['CD-1']:.3f} SU {out['csi']['SU-align']:.3f} | "
          f"geom {b0['geometric']:.3f} CNN {b0['cnn']:.3f} (CNN-geom {b0['cnn_minus_geometric'][0]:+.3f} "
          f"[{b0['cnn_minus_geometric'][1]:+.3f},{b0['cnn_minus_geometric'][2]:+.3f}]) | NLoS geom {b0['nlos']['geometric']:.3f} "
          f"CNN {b0['nlos']['cnn']:.3f} CD-1 {b0['nlos']['cd1']:.3f}", flush=True)
json.dump(res, open(ROOT / "results" / f"{_a.tag}.json", "w"), indent=1)
