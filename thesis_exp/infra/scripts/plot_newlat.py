"""Fig. 3 (step sweep) and Table I with the re-measured Adam latency, next to the paper's values.
Inputs: results/mumiso_aging_sensitivity.json (paper, v=1.5, T_ov=0), thesis_exp/infra/raw/mumiso_aging_sweep_newlat.json,
results/mumiso_aging_stats.json (paper Table I), thesis_exp/infra/raw/mumiso_aging_stats_newlat.json.
Outputs: thesis_exp/infra/raw/fig3_step_sweep_newlat.pdf/.png, thesis_exp/infra/raw/table1_newlat.md"""
import json, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = pathlib.Path(__file__).resolve().parents[3]
J = lambda p: json.load(open(ROOT / p))
old = J("results/mumiso_aging_sensitivity.json")["by_velocity"]["1.5"]["by_overhead"]["0.0"]["rows"]
new = J("thesis_exp/infra/raw/mumiso_aging_sweep_newlat.json")
fig, ax = plt.subplots(figsize=(5.2, 3.4), constrained_layout=True)
for rows, lab, st in ((old, "paper latency (1.66 ms/step)", "o--"), (new, "re-measured (1.33 ms/step)", "s-")):
    r = [x for x in rows if x["L"] > 0]
    ax.plot([x["L"] for x in r], [x["effective"] for x in r], st, label=lab, ms=4)
ax.plot([x["L"] for x in new if x["L"] > 0], [x["t0"] for x in new if x["L"] > 0], ":", color="0.4", label="rate at t = 0")
ax.set_xscale("log", base=2); ax.set_xlabel("Adam steps L"); ax.set_ylabel("min-user rate (b/s/Hz)"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
out = ROOT / "thesis_exp/infra/raw"
fig.savefig(out / "fig3_step_sweep_newlat.pdf"); fig.savefig(out / "fig3_step_sweep_newlat.png", dpi=150)
o, n = J("results/mumiso_aging_stats.json")["rows"], J("thesis_exp/infra/raw/mumiso_aging_stats_newlat.json")["rows"]
lines = ["| Method | latency (paper) ms | effective (paper) | latency (new) ms | effective (new) [95% CI] |", "| --- | --- | --- | --- | --- |"]
for k in ("su_average", "su_best_of", "adam8", "adam12", "adam16", "adam20", "cd", "pga"):
    lines.append(f"| {k} | {o[k]['latency_ms']:.2f} | {o[k]['effective']:.3f} | {n[k]['latency_ms']:.2f} | {n[k]['effective']:.3f} [{n[k]['eff_ci'][0]:.3f}, {n[k]['eff_ci'][1]:.3f}] |" if 'eff_ci' in n[k]
                 else f"| {k} | {o[k]['latency_ms']:.2f} | {o[k]['effective']:.3f} | {n[k]['latency_ms']:.2f} | {n[k]['effective']:.3f} |")
(out / "table1_newlat.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
