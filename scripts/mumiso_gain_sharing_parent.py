"""
mumiso_gain_sharing_parent.py
------------------------------
Measure gain sharing using the parent class implementation.

Compares:
  - share_gains=False (current, physically wrong but backward compatible)
  - share_gains=True (physically correct, cluster gains shared across antennas)

Same scenarios, same random stream, only cluster gain correlation differs.

Expected results (from prototype):
  - Anchor: -31.98%
  - PGA: -8.15%
  - Optimization value: 1.75× → 2.36×
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import json
import numpy as np, torch

from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, neighbour_corr, effective_rank)
from ris_mu.mumiso import system as S, baselines as B

NS = 1200
SEED = 11

def build(share_gains):
    """Generate scenarios with share_gains flag."""
    panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=SEED,
                                       share_gains=share_gains)
    chan = MuMisoChannel(panel, cfg)
    return chan.generate(NS), cfg

print("=" * 74)
print("GAIN SHARING: Parent class implementation")
print("=" * 74)

# Generate both arms
print(f"\nGenerating {NS} scenarios with each configuration...")
d_off, cfg_off = build(share_gains=False)
d_on, cfg_on = build(share_gains=True)

# Verify same scenarios (stream preserved)
print("\n[Stream check]")
same_ue = np.abs(d_off["ue_pos"] - d_on["ue_pos"]).max() == 0
same_los_bs = (d_off["los_ris_bs"] == d_on["los_ris_bs"]).all()
same_los_ue = (d_off["los_ris_ue"] == d_on["los_ris_ue"]).all()
same_los_d = (d_off["los_direct"] == d_on["los_direct"]).all()

stream_ok = same_ue and same_los_bs and same_los_ue and same_los_d
print(f"  Same scenarios (ue_pos + all LoS): {'YES' if stream_ok else 'NO - INVALID'}")
print(f"  G differs (cluster gains changed): {np.abs(d_off['G']-d_on['G']).max():.3e}")
print(f"  F differs: {np.abs(d_off['F']-d_on['F']).max():.3e}")
print(f"  hd differs: {np.abs(d_off['hd']-d_on['hd']).max():.3e}")

if not stream_ok:
    print("\n⚠️  ERROR: Random stream not preserved. Results invalid.")
    sys.exit(1)

# Table header
print("\n" + "=" * 74)
print(f"{'Model':<25}{'Antenna':>10}{'NLoS':>8}{'Rank':>8}{'Anchor':>10}{'PGA':>10}")
print("-" * 74)

results = {}
for name, d, cfg in [("Current (independent)", d_off, cfg_off),
                     ("Shared (physical)", d_on, cfg_on)]:
    F, G, hd, _ = to_torch(d)
    pt, nv = 1.0, 1.0 / cfg.snr_scale()
    T = F.shape[2]
    los_bs = d["los_ris_bs"]

    # Antenna correlation
    ant_corr = neighbour_corr(d["F"].reshape(-1, T))
    ant_corr_nlos = neighbour_corr(d["F"][~los_bs].reshape(-1, T))
    ant_rank = effective_rank(d["F"].reshape(-1, T))

    # Rates
    R_anch, _ = B.su_average(F, G, hd, pt, nv)
    r_anch = S.rate_metrics(R_anch)["min_rate"]

    R_pga, _ = B.pga(F[:300], G[:300], hd[:300], pt, nv)
    r_pga = S.rate_metrics(R_pga)["min_rate"]

    results[name] = {
        "antenna_corr": float(ant_corr),
        "antenna_corr_nlos": float(ant_corr_nlos),
        "antenna_rank": float(ant_rank),
        "anchor": float(r_anch),
        "pga": float(r_pga),
        "n_samples": NS,
        "n_antennas": T,
    }

    print(f"{name:<25}{ant_corr:>10.3f}{ant_corr_nlos:>8.3f}"
          f"{ant_rank:>8.2f}{r_anch:>10.4f}{r_pga:>10.4f}")

# Compute changes
r_off = results["Current (independent)"]
r_on = results["Shared (physical)"]

anch_change = 100 * (r_on["anchor"] / r_off["anchor"] - 1)
pga_change = 100 * (r_on["pga"] / r_off["pga"] - 1)

ratio_off = r_off["pga"] / r_off["anchor"]
ratio_on = r_on["pga"] / r_on["anchor"]

print("\n" + "=" * 74)
print("PHYSICS CORRECTION IMPACT:")
print(f"  Anchor: {anch_change:+.2f}%   ({r_off['anchor']:.4f} -> {r_on['anchor']:.4f})")
print(f"  PGA:    {pga_change:+.2f}%   ({r_off['pga']:.4f} -> {r_on['pga']:.4f})")
print(f"  Optimization value: {ratio_off:.2f}× -> {ratio_on:.2f}×")
print("\nANTENNA CORRELATION:")
print(f"  All:  {r_off['antenna_corr']:.3f} -> {r_on['antenna_corr']:.3f}")
print(f"  NLoS: {r_off['antenna_corr_nlos']:.3f} -> {r_on['antenna_corr_nlos']:.3f}")
print(f"  Effective rank: {r_off['antenna_rank']:.2f} -> {r_on['antenna_rank']:.2f} / {r_off['n_antennas']}")
print("=" * 74)

# Save results
out = {
    "share_gains_off": r_off,
    "share_gains_on": r_on,
    "changes": {
        "anchor_pct": float(anch_change),
        "pga_pct": float(pga_change),
        "ratio_off": float(ratio_off),
        "ratio_on": float(ratio_on),
    },
    "stream_preserved": bool(stream_ok),
    "n_samples": int(NS),
    "seed": int(SEED),
}

out_path = _pl.Path(__file__).resolve().parents[1] / "results" / "mumiso_gain_sharing_parent.json"
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print(f"\nResults saved: {out_path.name}")

# Check against expected
print("\n" + "=" * 74)
print("VALIDATION AGAINST PROTOTYPE:")
exp_anch = -31.98
exp_pga = -8.15
exp_ratio_on = 2.36

anch_ok = abs(anch_change - exp_anch) < 3  # ±3% tolerance
pga_ok = abs(pga_change - exp_pga) < 2    # ±2% tolerance
ratio_ok = abs(ratio_on - exp_ratio_on) < 0.15  # ±0.15 tolerance

print(f"  Anchor change: {anch_change:+.2f}% (expected {exp_anch:+.2f}%) - {'PASS' if anch_ok else 'WARN'}")
print(f"  PGA change: {pga_change:+.2f}% (expected {exp_pga:+.2f}%) - {'PASS' if pga_ok else 'WARN'}")
print(f"  Ratio (on): {ratio_on:.2f}× (expected {exp_ratio_on:.2f}×) - {'PASS' if ratio_ok else 'WARN'}")

if not (anch_ok and pga_ok and ratio_ok):
    print("\n⚠️  Results differ from prototype. Check implementation.")
else:
    print("\n✅ Results match prototype expectations!")
print("=" * 74)
