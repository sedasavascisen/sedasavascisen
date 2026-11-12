"""Audit check: with csi._noisy's batch-global scale, what per-scenario / per-user relative error does e2 imply?
Reads only; uses thesis_exp/p4/common.Aging (seed 11 test set, seed 12 val set), t=0 only."""
import sys, torch, numpy as np
torch.set_num_threads(1)
sys.path.insert(0, '/home/user/sedasavascisen/thesis_exp/p4')
from common import Aging
for seed in (11, 12):
    A = Aging(seed, [0.0])
    G, H, F = A.G[0], A.H[0], A.F
    out = {}
    for name, X in (("F", F), ("G", G), ("hd", H)):
        pb = (X.abs()**2).mean().item()
        ax = tuple(range(1, X.dim()))
        ps = (X.abs()**2).mean(dim=ax).numpy()           # per scenario
        r = pb / ps                                      # relative error multiplier
        out[name] = r
        print(seed, name, tuple(X.shape), "batch/scen power ratio: median %.3g p5 %.3g p95 %.3g max %.3g" % (np.median(r), np.percentile(r,5), np.percentile(r,95), r.max()))
    # per-user within G (users assumed on axis 1)
    pu = (G.abs()**2).mean(dim=tuple(i for i in range(G.dim()) if i != 1)).numpy() if G.dim() > 2 else None
    # for rho=30 dB (e2=1e-3): effective per-scenario SNR in dB for G
    rG = out["G"]
    eff = 10*np.log10(1/(1e-3*rG))
    print(seed, "rho=30dB -> per-scenario effective G 'pilot SNR' dB: median %.1f p5 %.1f p95 %.1f; frac < 10 dB: %.3f" % (np.median(eff), np.percentile(eff,5), np.percentile(eff,95), (eff<10).mean()))
    print(seed, "batch mean power G %.4g" % (G.abs()**2).mean().item())
