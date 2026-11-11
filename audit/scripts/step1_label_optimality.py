"""
Audit step 1: is the published label optimal? Received power |h_d + sum_n G_n e^{j th_n} F_n|^2 with
 (a) th_n = -angle(G_n F_n)                  (paper Eq. 8)
 (b) th_n = angle(h_d) - angle(G_n F_n)      (all reflections co-phased with the direct link: the true optimum
                                              for a single-antenna link, since |h_d + e^{j phi} S| is maximal at phi = angle(h_d) - angle(S)
                                              and (a) gives S = sum |G_n F_n| real positive)
Usage: python3 audit/scripts/step1_label_optimality.py [--n 6000 --seed 42]
Output: audit/raw/step1_label_optimality.json
"""
import sys, json, argparse, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
from m1_data import generate

ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=6000); ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = generate(a.n, seed=a.seed)
F, G, hd = D["F"], D["G"], D["hd"]
b = G * F
th_a = -np.angle(b)
th_b = np.angle(hd)[:, None] - np.angle(b)
P = lambda th: np.abs(hd + (b * np.exp(1j * th)).sum(1)) ** 2
pa, pb = P(th_a), P(th_b)
d_db = 10 * np.log10(pb / pa)
ratio = np.abs(hd) / np.abs(b.sum(1))          # |h_d| / |sum G_n F_n| as requested
ratio_aligned = np.abs(hd) / np.abs(b).sum(1)  # |h_d| / sum |G_n F_n| (magnitude of the aligned RIS sum)
rng = np.random.default_rng(0)
boot = np.array([d_db[rng.integers(0, a.n, a.n)].mean() for _ in range(2000)])
q = lambda x, p: float(np.percentile(x, p))
snr_gain_a = 10 * np.log10(pa / np.abs(hd) ** 2)
snr_gain_b = 10 * np.log10(pb / np.abs(hd) ** 2)
res = dict(
    commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
    n=a.n, seed=a.seed, generator="audit/scripts/m1_data.py (NumPy port; independent draw, not MATLAB rng(42))",
    gain_b_minus_a_db=dict(mean=float(d_db.mean()), mean_ci95=[q(boot, 2.5), q(boot, 97.5)], median=q(d_db, 50),
                           p95=q(d_db, 95), p5=q(d_db, 5), min=float(d_db.min()), max=float(d_db.max()),
                           frac_above_0p1db=float((d_db > 0.1).mean()), frac_negative=float((d_db < -1e-9).mean())),
    hd_over_sumGF=dict(median=q(ratio, 50), p5=q(ratio, 5), p25=q(ratio, 25), p75=q(ratio, 75), p95=q(ratio, 95), mean=float(ratio.mean())),
    hd_over_sum_absGF=dict(median=q(ratio_aligned, 50), p5=q(ratio_aligned, 5), p95=q(ratio_aligned, 95)),
    snr_gain_over_direct_db=dict(label_a_median=q(snr_gain_a, 50), label_b_median=q(snr_gain_b, 50),
                                 label_a_mean=float(snr_gain_a.mean()), label_b_mean=float(snr_gain_b.mean())),
    rmse_b_vs_a_deg=float(np.sqrt(np.mean(np.angle(np.exp(1j * (th_b - th_a))) ** 2)) * 180 / np.pi),
)
out = ROOT / "audit" / "raw" / "step1_label_optimality.json"
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
