"""
Audit step 5a: empirical correlation between neighbouring RIS elements in Paper 1's channel
(NumPy port, audit/raw/data/m1_N32_n40000_seed42.npz, all 40 000 samples).
Element order n = i*K + j (i = 0..7 along x, j = 0..3 along y), as in RIS_dataset_large_2D.m.
Neighbours: along j (lag 1 in the sequence the CNN-LSTM sees) and along i (lag K = 4).
  |rho_X| = |E[X_n conj(X_m)]| / sqrt(E|X_n|^2 E|X_m|^2), pooled over all neighbour pairs, X in {F, G, G*F}
  phase coherence of the optimal phases (label a): |E[exp(j(theta_n - theta_m))]|
  baseline: same statistics for elements 3 apart along i (distant pairs)
Output: audit/raw/step5_correlation.json
"""
import json, pathlib, subprocess
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
z = np.load(ROOT / "audit/raw/data/m1_N32_n40000_seed42.npz")
F, G, TH = z["F"], z["G"], z["theta"]
M, K = 8, 4
pairs = {"along_j (sequence lag 1)": [(i * K + j, i * K + j + 1) for i in range(M) for j in range(K - 1)],
         "along_i (sequence lag 4)": [(i * K + j, (i + 1) * K + j) for i in range(M - 1) for j in range(K)],
         "distant (3 apart along i)": [(i * K + j, (i + 3) * K + j) for i in range(M - 3) for j in range(K)]}
def rho(X, P):
    a = np.concatenate([X[:, n] for n, m in P]); b = np.concatenate([X[:, m] for n, m in P])
    return float(np.abs(np.mean(a * np.conj(b))) / np.sqrt(np.mean(np.abs(a) ** 2) * np.mean(np.abs(b) ** 2)))
def coh(P):
    d = np.concatenate([TH[:, n] - TH[:, m] for n, m in P]); return float(np.abs(np.mean(np.exp(1j * d))))
res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           n=len(TH), data="audit/raw/data/m1_N32_n40000_seed42.npz",
           pairs={k: dict(n_pairs=len(P), rho_F=rho(F, P), rho_G=rho(G, P), rho_GF=rho(G * F, P), phase_coherence_label_a=coh(P))
                  for k, P in pairs.items()})
json.dump(res, open(ROOT / "audit/raw/step5_correlation.json", "w"), indent=1)
print(json.dumps(res["pairs"], indent=1))
