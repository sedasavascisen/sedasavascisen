"""Anchor measured on the EXACT test split the models were scored on."""
import sys, pathlib, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

NS = 12000
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, M=8, K=4, seed=11)
F, G, hd, _ = to_torch(MuMisoChannel(panel, cfg).generate(NS))
pt, nv = 1.0, 1.0 / cfg.snr_scale()
tr, va, te = split_indices(NS, seed=0)
print(f"test split: {len(te)} scenarios (models scored here)")
out = {}
for m in ("su_average", "su_best_of", "su_weakest"):
    R, _ = B._DISPATCH[m](F[te], G[te], hd[te], pt, nv, precoder="zf")
    out[m] = S.rate_metrics(R)["min_rate"]
    print(f"  {m:>11}: {out[m]:.4f}")
models = {"concat": 3.536795, "deepsets": 3.536696, "exchange": 3.526039}
print("\n  model vs su_average anchor (same split):")
for k, v in models.items():
    print(f"  {k:>9} {v:.4f}   {100*(v/out['su_average']-1):+6.2f}%"
          f"   vs su_best_of {100*(v/out['su_best_of']-1):+6.2f}%")
json.dump(out, open(str(_pl.Path(__file__).resolve().parents[1] / "results") + "/anchor_full_test.json", "w"), indent=1)
