"""Layout preview of adim4_sekil_fairness.m (matplotlib). NOT the thesis figure:
CD RMSE comes from scripts/aisy_cd_k_check.py (NumPy draw of the same generator),
CD latency and CNN-LSTM values are the published ones. The real figure is drawn
by MATLAB from fairness_K_results.mat (adim 3)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = pathlib.Path(__file__).resolve().parents[1]
r = json.load(open(ROOT / "results" / "aisy_cd_k_check.json"))
K = [5, 20, 50]
r_cd = [r["K"][str(k)]["rmse_without_common_phase_deg"] for k in K]
t_cd = [0.15, 0.60, 1.50]            # published (MATLAB)
r_cnn, t_cnn_batch = 2.77, 0.08      # published
plt.rcParams.update({"font.family": "serif", "font.size": 11})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.3, 5.6), sharex=True, constrained_layout=True)
cd, cn = "#0072BD", "#D95319"
a1.plot(K, r_cd, "-s", color=cd, lw=2, ms=7, label="CD")
a1.axhline(r_cnn, ls="--", color=cn, lw=2, label=f"CNN-LSTM ({r_cnn:.2f}°)")
for k, v in zip(K, r_cd):
    a1.annotate(f"{v:.2f}°", (k, v), xytext=(6, 4), textcoords="offset points", color=cd, fontsize=10)
a1.set_ylim(0, 1.25 * max(r_cd + [r_cnn]))
a1.set_ylabel("Phase RMSE, common\nphase removed [°]")
a1.set_title("(a) Accuracy", fontsize=11)
a1.legend(loc="upper right", fontsize=9.5)
a2.semilogy(K, t_cd, "-o", color=cd, lw=2, ms=7, label="CD (one sample)")
a2.axhline(t_cnn_batch, ls=":", color=cn, lw=2, label=f"CNN-LSTM, batch / sample ({t_cnn_batch:.2f} ms)")
a2.axhline(1.0, ls="-.", color="0.25", lw=1.5, label="1 ms (URLLC user-plane target)")
for k, v in zip(K, t_cd):
    a2.annotate(f"{v:.2f} ms", (k, v), xytext=(6, -12), textcoords="offset points", color=cd, fontsize=10)
a2.set_ylim(0.04, 5)
a2.set_ylabel("Latency [ms] (log scale)")
a2.set_xlabel("CD iterations K")
a2.set_title("(b) Latency per channel realisation", fontsize=11)
a2.set_xticks(K); a2.set_xlim(0, 60)
a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2, fontsize=9)
for a in (a1, a2):
    a.grid(alpha=0.3)
fig.text(0.5, 0.5, "ÖNİZLEME — düzen örneği", fontsize=26, color="0.85", ha="center", va="center", rotation=20, zorder=0)
out = pathlib.Path(__file__).resolve().parent / "onizleme_sekil_fairness.png"
fig.savefig(out, dpi=200)
print("wrote", out)
