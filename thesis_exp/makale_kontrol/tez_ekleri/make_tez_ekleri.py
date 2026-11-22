"""
Thesis-ready tables and figures for items 8-14 (Paper 1 as it enters the thesis). No new measurement: every number is
read from an existing raw file, named next to each output. Figures are plain SVG (matplotlib is broken here) and are
also rendered to PDF/PNG with the pre-installed Chromium. Labels are Turkish (thesis language).

  T1_gosterim       same-architecture representation comparison   <- results/sumiso_representation.json
  T2_klasik         how each classical baseline is implemented    <- aisy_paket/orijinal/ris_CD.m, audit/scripts/step2_baselines.py (ports)
  T3_ortak_faz      invariant RMSE + rate, CNN-LSTM vs CD         <- audit/raw/step8_invariant_rmse.json
  T4_parametre      parameter counts that have code               <- audit/raw/step3_arith_check.json, audit/raw/train/*.json
  S1_cdf            |phase error| CDF (published + invariant)     <- audit/raw/step8_cdf.svg (audit/scripts/step8_cdf_plot.py)
  S2_csi            CSI-error robustness with a STATED error model <- audit/raw/step6_eval.json, audit/raw/step2_baselines.json
Output: this folder (*.md, *.tex, *.svg, *.pdf, *.png)
"""
import json, pathlib, shutil, subprocess
import numpy as np
H = pathlib.Path(__file__).resolve().parent; R = H.parents[2]
J = lambda p: json.load(open(R / p))
md, tex = {}, {}


def table(name, head, rows, caption, src):
    md[name] = f"**{caption}**\n\n| " + " | ".join(head) + " |\n|" + "---|" * len(head) + "\n" + \
        "\n".join("| " + " | ".join(r) + " |" for r in rows) + f"\n\nKaynak: {src}\n"
    esc = lambda s: s.replace("%", r"\%").replace("_", r"\_").replace("±", r"$\pm$").replace("°", r"$^\circ$").replace("≈", r"$\approx$").replace("×", r"$\times$").replace("−", "--")
    tex[name] = "\\begin{table}[t]\n\\centering\n\\caption{" + esc(caption) + "}\n\\begin{tabular}{" + "l" * len(head) + "}\n\\toprule\n" + \
        " & ".join(map(esc, head)) + " \\\\\n\\midrule\n" + "\n".join(" & ".join(map(esc, r)) + " \\\\" for r in rows) + \
        "\n\\bottomrule\n\\end{tabular}\n\\end{table}\n% Kaynak: " + src + "\n"


# ---- T1: representation, same architecture, 3 seeds
r = J("results/sumiso_representation.json"); rows = []
names = {"sincos": "sin/cos", "angle_circ": "açı, 1−cos kaybı", "angle_mse": "açı, düz MSE"}
for sc, lab in (("siso", "SISO"), ("miso", "MISO, N_t = 8")):
    for k in ("sincos", "angle_circ", "angle_mse"):
        v = r[sc][k]; rr = [x["rmse"] for x in v["runs"]]
        rows.append([lab, names[k], f"{v['rmse']['mean']:.2f} ± {v['rmse']['std']:.2f}", f"%{100 * np.mean([x['sr5'] for x in v['runs']]):.1f}",
                     f"{np.mean([x['rmse_near_wrap'] for x in v['runs']]):.2f}", f"{np.mean([x['rate'] for x in v['runs']]):.3f}"])
table("T1_gosterim", ["Senaryo", "Çıkış", "RMSE (°)", "SR@5°", "±π yakınında RMSE (°)", "Hız (b/s/Hz)"], rows,
      "Aynı mimaride çıkış gösterimi karşılaştırması (3 tohum, ortalama ± örneklem std; JSON'daki kayıtlı değerler)", "results/sumiso_representation.json (scripts/sumiso_representation_summary.py)")

# ---- T2: classical baselines as implemented (read from code)
rows = [["CD", "var", "bütün fazlar 0", "eleman başına kapalı form, sürekli faz", "sabit K tarama (K = 5)"],
        ["AO", "var", "bütün fazlar 0", "CD ile aynı güncelleme", "sabit, K = 1"],
        ["SPA", "var", "h_d", "elemanları sırayla hizalama", "tek geçiş"],
        ["PGD", "var", "bütün fazlar 0", "gradyan adımı 0.2 + birim modüle izdüşüm", "sabit 50 yineleme"],
        ["\"WMMSE\" (betik)", "var", "bütün fazlar 0", "eleman başına bir gradyan adımı (0.1)", "1 yineleme"],
        ["PSO", "var (alınan güç)", "rastgele, tekdüze", "20 parçacık", "sabit 30 yineleme"],
        ["Etiket (Denk. 8)", "yok", "—", "−∠(G_n F_n)", "—"]]
table("T2_klasik", ["Yöntem", "Amaçta h_d", "Başlangıç", "Güncelleme", "Durma"], rows,
      "Klasik yöntemlerin yayımlanan koddaki uygulaması",
      "aisy_paket/orijinal/ris_CD.m; ris_AO/SPA/PGD/WMMSE/PSO.m satır satır aktarımı audit/scripts/step2_baselines.py")

# ---- T3: invariant RMSE + rate
s = J("audit/raw/step8_invariant_rmse.json"); rows = []
f = lambda m: [f"{m['rmse_pub_deg']:.2f}", f"{m['rmse_inv_deg']:.2f}", f"%{100 * m['sr5_inv']:.2f}", f"{m['rate_bpshz']:.3f}", f"{m['loss_vs_opt_bpshz']:.3f}"]
for k in ("s0", "s1", "s2"):
    rows.append([f"CNN–LSTM, tohum {k[1]}"] + f(s["cnnlstm"][k]))
for k in ("K5", "K20", "K50"):
    rows.append([f"CD, K = {k[1:]}"] + f(s["cd"][k]))
rows.append(["Etiket (Denk. 8)"] + f(s["label_a"])); rows.append(["Optimum (h_d dahil)"] + f(s["optimum_b"]))
table("T3_ortak_faz", ["Yöntem", "Etikete RMSE (°)", "Ortak fazsız RMSE (°)", "Ortak fazsız SR@5°", "Hız (b/s/Hz)", "Optimuma kayıp"], rows,
      f"Ortak faz kaymasından arındırılmış RMSE ve hız ({s['n_test']} test senaryosu, bağımsız Python yeniden üretimi)",
      "audit/raw/step8_invariant_rmse.json (audit/scripts/step8_invariant_rmse.py)")

# ---- T4: parameter counts that have code
a = J("audit/raw/step3_arith_check.json")["params"]
tp = lambda n: J(f"audit/raw/train/{n}.json")["params"]
rows = [["CNN–LSTM (önerilen)", "727 360", f"{a['theta_NN_multioutput_m']['total']:,}".replace(",", " ") + " (MATLAB); " + f"{tp('cnnlstm_N32_s0'):,}".replace(",", " ") + " (PyTorch)", "theta_NN_multioutput.m"],
        ["CNN-Transformer", "201 K", f"{tp('transformer_N32_s0'):,}".replace(",", " "), "transformer_baseline.m (PyTorch aktarımı)"],
        ["FC-DNN (doğrudan)", "—", f"{tp('fcdnn_direct_N32_s0'):,}".replace(",", " "), "transformer_baseline.m (PyTorch aktarımı)"],
        ["Diğer 5 ablasyon varyantı", "89 K … 680 K", "ÜRETİLEMEDİ (kodu yok)", "—"]]
table("T4_parametre", ["Model", "Makalede", "Koddan sayılan", "Kod"], rows,
      "Parametre sayıları: yalnızca kodu olan modeller sayılabildi",
      "audit/raw/step3_arith_check.json; audit/raw/train/{cnnlstm,transformer,fcdnn_direct}_N32_s0.json. PyTorch sayısı MATLAB'dan 768 fazla: PyTorch iki LSTM katmanında ek yanlılık vektörü taşıyor (4·128 + 4·64).")

# ---- S1: CDF (already drawn from the real reproduction errors)
shutil.copy(R / "audit/raw/step8_cdf.svg", H / "S1_cdf.svg")

# ---- S2: CSI error, stated model: F_hat = F + sqrt(x|F_n|^2) CN(0,1), same for G (audit/scripts/step2_baselines.py)
e6, e2 = J("audit/raw/step6_eval.json"), J("audit/raw/step2_baselines.json")
xs = ["0.0", "0.05", "0.1", "0.15", "0.2"]; xv = [float(x) for x in xs]
cnn_r = [np.mean([e6["seeds"][k]["csi_error"][x]["rmse_deg"] for k in e6["seeds"]]) for x in xs]
cnn_h = [np.mean([e6["seeds"][k]["csi_error"][x]["rate_bpshz"] for k in e6["seeds"]]) for x in xs]
g = lambda m, key: [e2["csi_error"][x][m][key] for x in xs]
P1 = [("CNN–LSTM (3 tohum ort.)", cnn_r, "#1f4e79", ""), ("Kapalı form, Denk. 8 (aynı girdi)", g("closed_form_a (Eq. 8 label)", "rmse_pub_deg"), "#7f7f7f", "6,4")]
P2 = [("Kapalı form, h_d dahil (aynı girdi)", g("closed_form_b (angle h_d)", "rate_bpshz"), "#2e7d32", "2,3"), ("CD, K = 5 (aynı girdi)", g("CD K=5", "rate_bpshz"), "#c0504d", "6,4"),
      ("CNN–LSTM (3 tohum ort.)", cnn_h, "#1f4e79", ""), ("Kapalı form, Denk. 8", g("closed_form_a (Eq. 8 label)", "rate_bpshz"), "#7f7f7f", "6,4")]
W, Hh, PW, PH, L, T = 1000, 420, 400, 280, 70, 40
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" font-family="DejaVu Sans, sans-serif" font-size="12"><rect width="{W}" height="{Hh}" fill="white"/>']
for k, (ttl, ser, lo, hi, step, yl) in enumerate((("(a) Etikete göre faz RMSE'si", P1, 0, 30, 5, "RMSE (°)"),
                                                  ("(b) Hız", P2, 5.0, 6.6, 0.4, "Hız (b/s/Hz)"))):
    x0 = L + k * (PW + 110); X = lambda v: x0 + v / 0.2 * PW; Y = lambda v: T + (hi - v) / (hi - lo) * PH
    o.append(f'<text x="{x0}" y="{T - 14}" font-size="13" font-weight="bold">{ttl}</text>')
    for v in xv:
        o.append(f'<line x1="{X(v)}" y1="{T}" x2="{X(v)}" y2="{T + PH}" stroke="#e5e5e5"/><text x="{X(v)}" y="{T + PH + 16}" text-anchor="middle">{v:g}</text>')
    for v in np.arange(lo, hi + 1e-9, step):
        o.append(f'<line x1="{x0}" y1="{Y(v)}" x2="{x0 + PW}" y2="{Y(v)}" stroke="#e5e5e5"/><text x="{x0 - 6}" y="{Y(v) + 4}" text-anchor="end">{v:g}</text>')
    o.append(f'<rect x="{x0}" y="{T}" width="{PW}" height="{PH}" fill="none" stroke="#555"/>')
    o.append(f'<text x="{x0 + PW / 2}" y="{T + PH + 34}" text-anchor="middle">Göreli CSI hata varyansı x</text>')
    o.append(f'<text transform="translate({x0 - 46},{T + PH / 2}) rotate(-90)" text-anchor="middle">{yl}</text>')
    for i, (lab, y, c, da) in enumerate(ser):
        o.append(f'<polyline points="{" ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(xv, y))}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="{da}"/>')
        o += [f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="3" fill="{c}"/>' for a, b in zip(xv, y)]
        ly = (T + 18 + i * 17) if k == 0 else (T + PH - 70 + i * 17)
        o.append(f'<line x1="{x0 + 12}" y1="{ly - 4}" x2="{x0 + 36}" y2="{ly - 4}" stroke="{c}" stroke-width="2" stroke-dasharray="{da}"/><text x="{x0 + 41}" y="{ly}" font-size="11">{lab}</text>')
o.append("</svg>"); (H / "S2_csi.svg").write_text("\n".join(o))
csi_rows = [[x, f"{a:.2f}", f"{b:.2f}", f"{c:.3f}", f"{d:.3f}", f"{e:.3f}"] for x, a, b, c, d, e in
            zip(xs, cnn_r, P1[1][1], cnn_h, g("CD K=5", "rate_bpshz"), g("closed_form_b (angle h_d)", "rate_bpshz"))]
table("T5_csi", ["x", "CNN–LSTM RMSE (°)", "Kapalı form RMSE (°)", "CNN–LSTM hız", "CD K = 5 hız", "Kapalı form, h_d dahil, hız"], csi_rows,
      "CSI hatasına gürbüzlük; hata modeli F̂ = F + √(x|F_n|²)·CN(0,1), Ĝ aynı; fazlar F̂, Ĝ'den, değerlendirme gerçek kanalda; son sütun bozuk CSI'dan hesaplanan h_d'li kapalı form, gerçek kanalın optimumu değil",
      "audit/raw/step6_eval.json, audit/raw/step2_baselines.json (hata modeli: audit/scripts/step2_baselines.py)")

# ---- write + render SVG -> PDF/PNG
for n in md:
    (H / f"{n}.md").write_text(md[n]); (H / f"{n}.tex").write_text(tex[n])
js = H / "_render.js"
js.write_text("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
for (const f of process.argv.slice(2)){await p.goto('file://'+f);const s=await p.$('svg');const bb=await s.boundingBox();
await p.setViewportSize({width:Math.ceil(bb.width),height:Math.ceil(bb.height)});
await p.screenshot({path:f.replace('.svg','.png'),clip:{x:0,y:0,width:bb.width,height:bb.height},scale:'device'});
await p.pdf({path:f.replace('.svg','.pdf'),width:bb.width+'px',height:bb.height+'px',printBackground:true,pageRanges:'1'});}
await b.close();})();""")
subprocess.run(["node", str(js), str(H / "S1_cdf.svg"), str(H / "S2_csi.svg")], check=True); js.unlink()
print("wrote", sorted(p.name for p in H.iterdir()))
