"""Builds thesis_exp/tasarim_kurali/REPORT.md from raw/validation.json and raw/calibration.json.
Hypothesis decisions follow ON_KAYIT.md section 5 exactly (no new criteria)."""
import json, pathlib, subprocess
import numpy as np
H = pathlib.Path(__file__).parent
v = json.load(open(H / "raw/validation.json")); c = json.load(open(H / "raw/calibration.json"))
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.2f}, {x[1]:+.2f}]"
W("# Tasarım kuralı — ön kayıtlı sınama raporu"); W("")
W(f"Rapor commit'i `{commit}`, sınama commit'i `{v['commit'][:7]}`, kalibrasyon commit'i `{c['commit'][:7]}`. "
  f"Ön kayıt: `ON_KAYIT.md` (sınamadan önce commit'lendi, d840144). Kalibrasyon seed 12, sınama seed {v['seed']}, {v['conditions']} koşul, 400 senaryo. "
  "Kayıp = 1 − R(L seçilen) / R(L*), L* sınama çekilişindeki argmax.")
W(""); W("## 1) Hipotez kararları"); W("")
h1 = v["H1"]
W(f"- **H1** (medyan kayıp ≤ %1, en kötü ≤ %3): medyan %{h1['median_loss_pct']:.2f}, en kötü %{h1['worst_loss_pct']:.2f} → {yn(h1['holds'])}")
W(f"- **H2** (kural, L = 48 ve L = 5'ten iyi; koşullar üzerinden ortalama kayıp farkı, eşli GA sıfırın üstünde): "
  f"L = 48'e göre {v['H2']['L48']['mean']:+.2f} puan {ci(v['H2']['L48']['ci'])}, L = 5'e göre {v['H2']['L5']['mean']:+.2f} puan {ci(v['H2']['L5']['ci'])} → {yn(v['H2']['holds'])}")
W(f"- **H3** (W > 0'da kural, makalenin kapalı formundan iyi): {v['H3']['mean']:+.2f} puan {ci(v['H3']['ci'])} → {yn(v['H3']['holds'])}")
W(""); W("## 2) Koşul başına kayıp (%)"); W("")
W("| km/h | ΔT (ms) | W (ms) | x | L* | kural L̂ | kayıp: kural | L=48 | L=5 | kapalı form |"); W("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for r in v["rows"]:
    p, l = r["pick"], r["loss_pct"]
    W(f"| {r['kmh']:g} | {r['dT_ms']:g} | {r['W_ms']:g} | {r['x']:.4f} | {r['L_star']} | {p['rule']} | {l['rule']:.2f} | {l['L48']:.2f} | {l['L5']:.2f} | {l['closed_form']:.2f} ({p['closed_form']}) |")
W(""); W("## 3) Kayıp özeti (60 koşul)"); W("")
W("| Kural | medyan | ortalama | en kötü |"); W("| --- | --- | --- | --- |")
for k, name in (("rule", "tasarım kuralı"), ("L48", "her zaman L = 48"), ("L5", "her zaman L = 5"), ("closed_form", "makalenin kapalı formu")):
    x = np.array([r["loss_pct"][k] for r in v["rows"]])
    W(f"| {name} | {np.median(x):.2f} | {x.mean():.2f} | {x.max():.2f} |")
W(""); W("## 4) Kalibrasyon tanılaması"); W("")
W(f"R_floor {c['R_floor']:.3f} b/s/Hz, f_d {c['fd_hz']:.2f} Hz; ψ'nin L'ler arası en büyük yayılımı {c['psi_spread_max']:.3f}.")
W(""); W("## 5) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/tasarim_kurali/calibrate.py | kanal 12 | raw/calibration.json, raw/calibrate.log |")
W(f"| python3 thesis_exp/tasarim_kurali/validate.py ({v['seconds']/60:.0f} dk) | kanal 13, bootstrap 0 | raw/validation.json, raw/validate.log |")
y = H / "yorum.md"
if y.exists():
    W(""); W("## 6) Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
