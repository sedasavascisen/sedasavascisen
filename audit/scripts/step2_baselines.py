"""
Audit step 2 (classical part) + step 6 reference metrics + Fig. 10 classical arms.

Python ports of the zip's ris_CD.m, ris_AO.m, ris_PGD.m, ris_PSO.m, ris_SPA.m, ris_WMMSE.m, line by line
(per-sample loops vectorised over samples where that is exact: every update depends only on the same
sample). PSO uses random numbers -> independent draw (NumPy, seed below), not MATLAB's stream.
Default arguments as in the .m files: CD K=5, AO K=1, PGD step 0.2 K=50, PSO P=20 I=30 w=.7 c1=c2=1.5,
WMMSE K=1 step 0.1, SPA single pass.

Metrics on the test split of audit/raw/data/m1_N32_n40000_seed42.npz (split as audit/scripts/m1_data.split):
  rmse_pub_deg     wrapped phase error vs the published label (a) -angle(G F)   [paper's definition]
  rmse_inv_deg     same after removing each sample's common phase
  rmse_vs_b_deg    vs label (b) angle(h_d) - angle(G F)  (the optimum for this single-antenna link)
  power_db_vs_a / power_db_vs_b   received power relative to labels (a)/(b), mean dB
  rate_bpshz       log2(1 + Pt |h|^2 / noise_var), Pt = 1, noise_var = 1e-3 (RIS_dataset_large_2D.m)
  script_rmse      what the .m file itself prints (|h_true - h_eff| with h_true = h_d + sum G F)
CSI error (Fig. 10 arms): F_hat = F + sqrt(x * |F_n|^2) CN(0,1), G_hat likewise (per-element relative error
variance x; the paper does not define its error model -- this is an assumption, stated in the report).
The method computes phases from (F_hat, G_hat, h_d) and is scored against the TRUE label/channel.
Output: audit/raw/step2_baselines.json
"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
from m1_data import split

ROOT = pathlib.Path(__file__).resolve().parents[2]
z = np.load(ROOT / "audit/raw/data/m1_N32_n40000_seed42.npz")
tr, va, te = split(len(z["hd"]), seed=42)
F, G, hd = z["F"][te], z["G"][te], z["hd"][te]
S, N = F.shape
wrap = lambda x: np.angle(np.exp(1j * x))


def cd(F, G, hd, K):                                   # ris_CD.m / ris_AO.m (identical update)
    b = G * F; th = np.zeros(F.shape)
    for _ in range(K):
        for n in range(N):
            m = np.ones(N, bool); m[n] = False
            Hm = hd + (b[:, m] * np.exp(1j * th[:, m])).sum(1)
            th[:, n] = wrap(np.angle(Hm) - np.angle(b[:, n]))
    return th


def pgd(F, G, hd, step=0.2, K=50):                     # ris_PGD.m
    a = G * F; zz = np.ones(F.shape, complex)
    for _ in range(K):
        h = hd + (a * zz).sum(1)
        zz = zz + step * np.conj(h)[:, None] * a
        zz = np.exp(1j * np.angle(zz))
    return np.angle(zz)


def pso(F, G, hd, P=20, I=30, w=0.7, c1=1.5, c2=1.5, seed=0):   # ris_PSO.m
    rng = np.random.default_rng(seed); a = F * G; out = np.zeros(F.shape)
    for s in range(F.shape[0]):
        phi = 2 * np.pi * rng.random((P, N)); vel = np.zeros((P, N))
        fit = np.abs(hd[s] + (a[s] * np.exp(1j * phi)).sum(1)) ** 2
        pb, pf = phi.copy(), fit.copy(); gi = fit.argmax(); gf, gb = fit[gi], phi[gi].copy()
        for _ in range(I):
            r1, r2 = rng.random((P, N)), rng.random((P, N))
            vel = w * vel + c1 * r1 * (pb - phi) + c2 * r2 * (gb - phi)
            phi = wrap(phi + vel)
            fit = np.abs(hd[s] + (a[s] * np.exp(1j * phi)).sum(1)) ** 2
            bt = fit > pf; pb[bt] = phi[bt]; pf[bt] = fit[bt]
            bi = fit.argmax()
            if fit[bi] > gf: gf, gb = fit[bi], phi[bi].copy()
        out[s] = gb
    return out


def spa(F, G, hd):                                     # ris_SPA.m
    b = G * F; th = np.zeros(F.shape); Hacc = hd.copy()
    for n in range(N):
        th[:, n] = wrap(np.angle(Hacc) - np.angle(b[:, n])); Hacc = Hacc + b[:, n] * np.exp(1j * th[:, n])
    return th


def wmmse(F, G, hd, K=1, step=0.1):                    # ris_WMMSE.m (a per-element gradient step, not WMMSE)
    b = G * F; th = np.zeros(F.shape)
    for _ in range(K):
        H = hd + (b * np.exp(1j * th)).sum(1)          # computed once per iteration, as in the .m file
        for n in range(N):
            grad = -2 * np.imag(np.conj(b[:, n]) * H)
            th[:, n] = wrap(th[:, n] - step * grad)
    return th


METHODS = {"closed_form_a (Eq. 8 label)": lambda F, G, hd: -np.angle(G * F),
           "closed_form_b (angle h_d)": lambda F, G, hd: np.angle(hd)[:, None] - np.angle(G * F),
           "CD K=5": lambda F, G, hd: cd(F, G, hd, 5), "CD K=20": lambda F, G, hd: cd(F, G, hd, 20),
           "CD K=50": lambda F, G, hd: cd(F, G, hd, 50), "AO K=1 (default)": lambda F, G, hd: cd(F, G, hd, 1),
           "PGD": pgd, "PSO": pso, "SPA": spa, "WMMSE (script)": wmmse}


def metrics(th, F, G, hd):
    b = G * F
    la, lb = -np.angle(b), np.angle(hd)[:, None] - np.angle(b)
    e = wrap(th - la); phi = np.angle(np.exp(1j * e).mean(1, keepdims=True)); ei = wrap(e - phi)
    P = lambda t: np.abs(hd + (b * np.exp(1j * t)).sum(1)) ** 2
    p = P(th)
    h_true = hd + b.sum(1); h_eff = hd + (b * np.exp(1j * th)).sum(1)
    d = lambda x: float(np.sqrt(np.mean(x ** 2)) * 180 / np.pi)
    return dict(rmse_pub_deg=d(e), rmse_inv_deg=d(ei), rmse_vs_b_deg=d(wrap(th - lb)),
                sr5_pub=float((np.abs(e) < np.deg2rad(5)).mean()),
                power_db_vs_a=float(np.mean(10 * np.log10(p / P(la)))), power_db_vs_b=float(np.mean(10 * np.log10(p / P(lb)))),
                rate_bpshz=float(np.mean(np.log2(1 + p / 1e-3))), script_rmse=float(np.sqrt(np.mean(np.abs(h_true - h_eff) ** 2))))


res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           data="audit/raw/data/m1_N32_n40000_seed42.npz (NumPy port, independent draw)", n_test=S,
           random_phase=metrics(np.random.default_rng(1).uniform(-np.pi, np.pi, F.shape), F, G, hd),
           perfect_csi={}, csi_error={})
for k, f in METHODS.items():
    res["perfect_csi"][k] = metrics(f(F, G, hd), F, G, hd); print(k, res["perfect_csi"][k], flush=True)
rng = np.random.default_rng(5)
for x in (0.0, 0.05, 0.10, 0.15, 0.20):
    noise = lambda X: X + np.sqrt(x * np.abs(X) ** 2) * (rng.standard_normal(X.shape) + 1j * rng.standard_normal(X.shape)) / np.sqrt(2)
    Fh, Gh = noise(F), noise(G)
    res["csi_error"][str(x)] = {k: metrics(METHODS[k](Fh, Gh, hd), F, G, hd)
                                for k in ("closed_form_a (Eq. 8 label)", "closed_form_b (angle h_d)", "CD K=5", "PSO")}
    np.savez_compressed(ROOT / f"audit/raw/step2_csi_inputs_x{x}.npz", Fh=Fh.astype(np.complex64), Gh=Gh.astype(np.complex64))
    print("csi", x, {k: round(v["rmse_pub_deg"], 2) for k, v in res["csi_error"][str(x)].items()}, flush=True)
json.dump(res, open(ROOT / "audit/raw/step2_baselines.json", "w"), indent=1)
print("wrote audit/raw/step2_baselines.json")
