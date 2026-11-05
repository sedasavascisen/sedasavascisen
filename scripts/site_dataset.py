"""
Site-specific dataset for position-based phase prediction.

For each site (ris_mu.sumiso.site.Site, seeds 1..5): user positions drawn
uniformly in the room outside obstacles, independently for the train / val /
test splits; channels are the deterministic function of position given by
the site; labels are the exact coordinate-ascent optimum (solver.solve).
Writes data_site/site<seed>.npz (gitignored; regenerate with this script).
"""
import sys
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.site import Site
from ris_mu.sumiso import solver as SV

ap = argparse.ArgumentParser()
ap.add_argument("--sites", type=int, nargs="*", default=[1, 2, 3, 4, 5])
ap.add_argument("--n", type=int, nargs=3, default=[20000, 2000, 4000], help="train val test")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "data_site"
OUT.mkdir(exist_ok=True)
torch.set_num_threads(4)
for sd in a.sites:
    t0 = time.time()
    site = Site(seed=sd)
    out = dict(seed=sd, snr_scale=site.snr_scale, los_bs=site.los_bs)
    for split, n, rs in zip(("train", "val", "test"), a.n, (1, 2, 3)):
        pos = site.sample_positions(n, np.random.default_rng(100 * sd + rs))
        F, G, H = site.channels(pos)
        A, B = SV.cascade(*(torch.as_tensor(x) for x in (F, G, H)))
        th = torch.empty(n, B.shape[1]); g = torch.empty(n)
        for i in range(0, n, 2000):
            s = slice(i, i + 2000)
            th[s], g[s] = SV.solve(A[s], B[s], seed=i)
        out.update({f"{split}_pos": pos.astype(np.float32), f"{split}_G": G, f"{split}_hd": H,
                    f"{split}_theta": th.numpy(), f"{split}_gain": g.numpy(), f"{split}_los": site.los_ue(pos)})
    out["F"] = site.F
    np.savez_compressed(OUT / f"site{sd}.npz", **out)
    r = np.log2(1 + site.snr_scale * out["test_gain"]).mean()
    print(f"site {sd}: test optimum {r:.3f} b/s/Hz, LoS {out['test_los'].mean():.2f}, {time.time()-t0:.0f}s", flush=True)
