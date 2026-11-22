"""
When the MATLAB output arrives: exact CDF and metrics from cnn_lstm_test_results.mat (written by
aisy_paket/orijinal/theta_NN_multioutput.m, section 11, '-v7.3' = HDF5). Reads phase_err [nTest x N] (rad, wrapped);
if THETA_pred and THETA_true are present it also gives the common-phase-invariant RMSE vs the label.
Nothing is re-trained or re-run in MATLAB; this only reads the saved file.
Usage: python3 audit/scripts/step9_mat_cdf.py /path/cnn_lstm_test_results.mat
Output: audit/raw/step9_mat_cdf.json, audit/raw/step9_mat_cdf.svg
"""
import sys, json, pathlib, hashlib
import numpy as np
R = pathlib.Path(__file__).resolve().parents[2] / "audit/raw"
f = pathlib.Path(sys.argv[1])


def load(path):
    try:
        import h5py                                    # v7.3: HDF5, MATLAB stores arrays transposed
        with h5py.File(path, "r") as h:
            return {k: np.array(h[k]).T for k in h.keys() if isinstance(h[k], h5py.Dataset)}
    except OSError:
        from scipy.io import loadmat                   # older -v7 files
        return {k: v for k, v in loadmat(path).items() if not k.startswith("__")}


d = load(f)
e = np.abs(np.asarray(d["phase_err"], float)) * 180 / np.pi
out = dict(file=f.name, sha256=hashlib.sha256(f.read_bytes()).hexdigest(), shape=list(e.shape),
           rmse_deg=float(np.sqrt((e ** 2).mean())), cdf_at_5deg=float((e < 5).mean()), err_p95_deg=float(np.percentile(e, 95)),
           sr={str(t): float((e < t).mean()) for t in (1, 3, 5, 10)})
if "rmse_deg" in d:
    out["matlab_printed_rmse_deg"] = float(np.asarray(d["rmse_deg"]).ravel()[0])
if "THETA_pred" in d and "THETA_true" in d:
    err = np.angle(np.exp(1j * (np.asarray(d["THETA_pred"], float) - np.asarray(d["THETA_true"], float))))
    phi = np.angle(np.exp(1j * err).mean(1, keepdims=True)); ei = np.angle(np.exp(1j * (err - phi)))
    out["rmse_inv_deg"] = float(np.sqrt((ei ** 2).mean()) * 180 / np.pi)
json.dump(out, open(R / "step9_mat_cdf.json", "w"), indent=1); print(json.dumps(out, indent=1))
x = np.linspace(0, 20, 401); c = np.searchsorted(np.sort(e.ravel()), x, side="right") / e.size
X = lambda v: 70 + v / 20 * 500; Y = lambda p: 30 + (1 - p) * 300
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="620" height="390" font-family="DejaVu Sans, sans-serif" font-size="12"><rect width="620" height="390" fill="white"/>']
s += [f'<line x1="{X(v)}" y1="30" x2="{X(v)}" y2="330" stroke="#e5e5e5"/><text x="{X(v)}" y="346" text-anchor="middle">{v}</text>' for v in range(0, 21, 5)]
s += [f'<line x1="70" y1="{Y(p)}" x2="570" y2="{Y(p)}" stroke="#e5e5e5"/><text x="64" y="{Y(p) + 4}" text-anchor="end">{p:.2f}</text>' for p in (0, .25, .5, .75, 1)]
s += ['<rect x="70" y="30" width="500" height="300" fill="none" stroke="#555"/>', f'<line x1="{X(5)}" y1="30" x2="{X(5)}" y2="330" stroke="#666" stroke-dasharray="2,3"/>',
      f'<polyline points="{" ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(x, c))}" fill="none" stroke="#1f4e79" stroke-width="2"/>',
      f'<text x="330" y="300">CNN–LSTM (MATLAB çıktısı): 5°\'de %{100 * out["cdf_at_5deg"]:.1f}</text>',
      '<text x="320" y="374" text-anchor="middle">|faz hatası| (derece)</text>', '<text transform="translate(18,180) rotate(-90)" text-anchor="middle">Birikimli oran (CDF)</text></svg>']
(R / "step9_mat_cdf.svg").write_text("\n".join(s)); print("wrote", R / "step9_mat_cdf.svg")
