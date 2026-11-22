"""CDF of |phase error| from audit/raw/step8_abs_err_deg.npz (written by step8_invariant_rmse.py), drawn as plain SVG
(matplotlib is broken in this environment). (a) published metric (vs label (a), Eq. 8); (b) common-phase-invariant metric.
Independent NumPy draw (not MATLAB rng(42)); CNN-LSTM weights audit/raw/train/cnnlstm_N32_s{0,1,2}.pt. -> audit/raw/step8_cdf.svg"""
import pathlib, numpy as np
R = pathlib.Path(__file__).resolve().parents[2] / "audit/raw"
z = np.load(R / "step8_abs_err_deg.npz")
W, H, PW, PH, L, T = 1000, 400, 400, 270, 70, 40
x = np.linspace(0, 20, 401)
cdf = lambda e: np.searchsorted(np.sort(e), x, side="right") / len(e)
series = [(f"cnnlstm_s{s}", f"CNN–LSTM, tohum {s}", c, "") for s, c in zip((0, 1, 2), ("#1f4e79", "#4f81bd", "#8fb3d9"))]
series += [("cd_K5", "CD, K = 5", "#c0504d", "6,4"), ("cd_K20", "CD, K = 20", "#e08a1e", "6,4")]
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="DejaVu Sans, sans-serif" font-size="12">',
     f'<rect width="{W}" height="{H}" fill="white"/>']
for k, (ttl, suf) in enumerate((("(a) Makaledeki ölçüt: Denk. 8 etiketine göre", "_pub"), ("(b) Ortak faz çıkarılmış ölçüt", "_inv"))):
    x0 = L + k * (PW + 100); X = lambda v: x0 + v / 20 * PW; Y = lambda p: T + (1 - p) * PH
    o.append(f'<text x="{x0}" y="{T - 14}" font-size="13" font-weight="bold">{ttl}</text>')
    for v in range(0, 21, 5):
        o.append(f'<line x1="{X(v)}" y1="{T}" x2="{X(v)}" y2="{T + PH}" stroke="#e5e5e5"/><text x="{X(v)}" y="{T + PH + 16}" text-anchor="middle">{v}</text>')
    for p in (0, .25, .5, .75, 1):
        o.append(f'<line x1="{x0}" y1="{Y(p)}" x2="{x0 + PW}" y2="{Y(p)}" stroke="#e5e5e5"/><text x="{x0 - 6}" y="{Y(p) + 4}" text-anchor="end">{p:.2f}</text>')
    o.append(f'<rect x="{x0}" y="{T}" width="{PW}" height="{PH}" fill="none" stroke="#555"/>')
    o.append(f'<line x1="{X(5)}" y1="{T}" x2="{X(5)}" y2="{T + PH}" stroke="#666" stroke-dasharray="2,3"/>')
    o.append(f'<text x="{x0 + PW / 2}" y="{T + PH + 34}" text-anchor="middle">|faz hatası| (derece)</text>')
    for i, (key, lab, c, da) in enumerate(series):
        e = z[key + suf]; pts = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(x, cdf(e)))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="{da}"/>')
        ly = T + PH - 92 + i * 17
        o.append(f'<line x1="{x0 + 170}" y1="{ly - 4}" x2="{x0 + 195}" y2="{ly - 4}" stroke="{c}" stroke-width="2" stroke-dasharray="{da}"/>'
                 f'<text x="{x0 + 200}" y="{ly}" font-size="11">{lab}: 5°\'de %{100 * (e < 5).mean():.1f}</text>')
o.append(f'<text transform="translate(18,{T + PH / 2}) rotate(-90)" text-anchor="middle">Birikimli oran (CDF)</text></svg>')
(R / "step8_cdf.svg").write_text("\n".join(o)); print("wrote", R / "step8_cdf.svg")
