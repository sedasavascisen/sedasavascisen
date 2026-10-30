"""
Where the gain comes from: no panel -> random phase -> optimised.

This table is quoted in the thesis ("a random surface already delivers
about half the gain") and had no script behind it until now. Every row
uses the SAME precoder settings -- an earlier version of `no_ris` did not,
and reported the floor 10.9% too high.
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

NS = 1200
torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
out = {}
print(f"{NS} scenarios, N={F.shape[1]} T=8 K=4, identical precoder on every row\n")
print(f"{'method':>14}{'min rate':>11}")
for m in ("no_ris", "random", "su_weakest", "su_average", "su_best_of", "pga"):
    R, _ = B._DISPATCH[m](F[:300] if m == "pga" else F,
                          G[:300] if m == "pga" else G,
                          hd[:300] if m == "pga" else hd, pt, nv, precoder="zf")
    out[m] = S.rate_metrics(R)["min_rate"]
    note = "  (300 scenarios)" if m == "pga" else ""
    print(f"{m:>14}{out[m]:11.4f}{note}")
print(f"\n  random / pga      = {out['random']/out['pga']:.2f}"
      f"   <- how much a RANDOM surface already delivers")
print(f"  no_ris -> random  = {out['random']/out['no_ris']:.2f}x")
print(f"  random -> pga     = {out['pga']/out['random']:.2f}x")
p = pathlib.Path(__file__).resolve().parents[1] / "results/mumiso_gain_source.json"
p.write_text(json.dumps(out, indent=1))
print(f"\nwrote {p.name}")
