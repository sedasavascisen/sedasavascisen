"""
Independent check of the AISY 2026 baseline-fairness numbers (published
Figure 2 / thesis Fig. 4): coordinate descent (CD) with K = 5, 20, 50 sweeps,
phase-aware RMSE against the closed-form label -angle(F_n) - angle(G_n).

Channel: NumPy port of the published RIS_dataset_large_2D.m (8x4 horizontal
panel at (20,10,3) m, lambda/2, Rayleigh LoS coefficient per element, 6
scatterers, scatter gain 0.15). The NumPy random stream differs from MATLAB's
rng(42), so values are a draw from the same distribution, not the same samples.

CD: exactly ris_CD.m -- start at theta = 0, element-by-element update
theta_n = angle(h_d + sum_{m != n} G_m v_m F_m) - angle(G_n F_n), K sweeps.

Also reported, because the RMSE reference ignores the direct link:
  - the same RMSE after removing each sample's common phase
  - the received power |h|^2 of CD and of the label (which one is higher)
Writes results/aisy_cd_k_check.json.
"""
import json
import pathlib
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=6000)
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]

fc, c = 3e9, 3e8
lam = c / fc
k = 2 * np.pi / lam
room = np.array([40.0, 20.0, 6.0])
M, Kr = 8, 4
N = M * Kr
d = lam / 2
ctr = np.array([room[0] / 2, room[1] / 2, 3.0])
x0, y0 = ctr[0] - (M - 1) / 2 * d, ctr[1] - (Kr - 1) / 2 * d
pos = np.array([[x0 + i * d, y0 + j * d, ctr[2]] for i in range(M) for j in range(Kr)])

rng = np.random.default_rng(a.seed)
cn = lambda *s: (rng.standard_normal(s) + 1j * rng.standard_normal(s)) / np.sqrt(2)
F = np.zeros((a.n, N), complex)
G = np.zeros((a.n, N), complex)
hd = np.zeros(a.n, complex)
for s in range(a.n):
    tx = np.r_[rng.random(2) * room[:2], 1 + rng.random()]
    rx = np.r_[rng.random(2) * room[:2], 1 + rng.random()]
    sc = rng.random((6, 3)) * room
    dd = np.linalg.norm(tx - rx)
    hd[s] = cn(1)[0] * np.exp(-1j * k * dd) / dd
    dtx = np.linalg.norm(tx - pos, axis=1)
    drx = np.linalg.norm(pos - rx, axis=1)
    f0 = cn(N) * np.exp(-1j * k * dtx) / dtx
    g0 = cn(N) * np.exp(-1j * k * drx) / drx
    da = np.linalg.norm(tx - sc, axis=1)[:, None]
    db = np.linalg.norm(sc[:, None] - pos, axis=2)
    dc = np.linalg.norm(sc - rx, axis=1)[:, None]
    F[s] = f0 + (0.15 * cn(6, N) * np.exp(-1j * k * (da + db)) / (da * db)).sum(0)
    G[s] = g0 + (0.15 * cn(6, N) * np.exp(-1j * k * (db + dc)) / (db * dc)).sum(0)

b = G * F                                   # cascaded coefficient per element
label = -np.angle(b)                        # published label (direct link ignored)


def wrap(x):
    return np.angle(np.exp(1j * x))


def rmse(th, ref):
    return float(np.sqrt(np.mean(wrap(th - ref) ** 2)) * 180 / np.pi)


def rmse_no_common(th, ref):
    e = wrap(th - ref)
    phi = np.angle(np.exp(1j * e).mean(1, keepdims=True))
    return float(np.sqrt(np.mean(wrap(e - phi) ** 2)) * 180 / np.pi)


def power(th):
    return np.abs(hd + (b * np.exp(1j * th)).sum(1)) ** 2


def cd(K):
    th = np.zeros((a.n, N))
    h = hd + (b * np.exp(1j * th)).sum(1)
    for _ in range(K):
        for n in range(N):
            hm = h - b[:, n] * np.exp(1j * th[:, n])
            th[:, n] = wrap(np.angle(hm) - np.angle(b[:, n]))
            h = hm + b[:, n] * np.exp(1j * th[:, n])
    return th


res = dict(n=a.n, seed=a.seed, note="NumPy draw of the published generator; not MATLAB's rng(42) samples",
           label_power_db_median=float(np.median(10 * np.log10(power(label)))), K={})
for K in (1, 5, 20, 50):
    th = cd(K)
    pw = power(th)
    res["K"][str(K)] = dict(rmse_deg=rmse(th, label), rmse_without_common_phase_deg=rmse_no_common(th, label),
                            cd_power_over_label_db_mean=float(np.mean(10 * np.log10(pw / power(label)))),
                            frac_cd_power_ge_label=float(np.mean(pw >= power(label) * (1 - 1e-9))))
    print(K, res["K"][str(K)], flush=True)
json.dump(res, open(ROOT / "results" / "aisy_cd_k_check.json", "w"), indent=1)
print("wrote results/aisy_cd_k_check.json")
