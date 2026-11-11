"""
Audit step 5b: element-permutation control. Same data, same settings; the permuted runs see the
elements in a fixed random order (seed 7, input and label permuted together). Per-sample mean squared
phase error (test split, 6000 x 32) from audit/raw/train/*_test_abs_err_deg.npy; RMSE per run and the
paired difference (perm - original) with a paired bootstrap over test samples (2000 resamples, seed 0).
Output: audit/raw/step5_permutation.json
"""
import json, pathlib, subprocess
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
R = ROOT / "audit/raw/train"
res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(), seeds={})
rng = np.random.default_rng(0)
for s in (0, 1, 2):
    o = np.load(R / f"cnnlstm_N32_s{s}_test_abs_err_deg.npy").astype(np.float64)
    p = np.load(R / f"cnnlstm_N32_s{s}_perm_test_abs_err_deg.npy").astype(np.float64)
    mo, mp = (o ** 2).mean(1), (p ** 2).mean(1)
    n = len(mo)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, n, n); bs.append(np.sqrt(mp[i].mean()) - np.sqrt(mo[i].mean()))
    res["seeds"][str(s)] = dict(rmse_original=float(np.sqrt(mo.mean())), rmse_permuted=float(np.sqrt(mp.mean())),
                                diff_perm_minus_orig=float(np.sqrt(mp.mean()) - np.sqrt(mo.mean())),
                                ci95=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
ro = [v["rmse_original"] for v in res["seeds"].values()]; rp = [v["rmse_permuted"] for v in res["seeds"].values()]
res["across_seeds"] = dict(original_mean=float(np.mean(ro)), original_std=float(np.std(ro, ddof=1)),
                           permuted_mean=float(np.mean(rp)), permuted_std=float(np.std(rp, ddof=1)))
json.dump(res, open(ROOT / "audit/raw/step5_permutation.json", "w"), indent=1)
print(json.dumps(res, indent=1))
