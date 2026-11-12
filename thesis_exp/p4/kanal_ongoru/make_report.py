"""Builds thesis_exp/p4/kanal_ongoru/REPORT.md from raw/results*.json."""
import json, glob, pathlib, subprocess
H = pathlib.Path(__file__).parent
files = sorted(glob.glob(str(H / "raw/results*.json")))
R = {json.load(open(f))["e2"] if "e2" in json.load(open(f)) else 0.0: json.load(open(f)) for f in files}
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.1 — Kanal öngörüsü (rapor)")
W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{', '.join(sorted({v['commit'][:7] for v in R.values()}))}` (results*.json; o commit'te run.py yoktu — commit'li koddan bit-bit yeniden üretim: thesis_exp/denetim_log/k1_rerun.md). Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s); seçim seed 12. Gecikmeler: tek iş parçacıklı yeniden ölçüm (thesis_exp/infra). "
  "Ek anlık görüntü başına ek pilot: 48 sembol = 3.43 / 1.71 / 0.86 ms (15 / 30 / 60 kHz); 2 noktalı öngörücü 1, 3 noktalılar 2 ek anlık görüntü ister. "
  "Bu süre tek-atış etkin hıza **eklenmedi** (anlık görüntüler t=0'dan önce alınıyor); havada geçen süre olarak ayrıca raporlanmalı.")
W(""); W("Not (denetim U21): ızgara 40 ms'den sonra 50/75/100 ms'ye atlıyor; 40 ms'den yavaş kollar (Adam-32/48) interpolasyonla değerlendirildi. Raporlanan/seçilen kollar 40 ms altında ve bundan etkilenmiyor.")
W("")
W("## 1) Bulgular (önce kısıtlar)")
W("")
W("- **Kanal modeli öngörüyü kayırıyor:** saçıcılar sabit, kullanıcılar düz çizgide yürüyor; kanal zamanın düzgün bir fonksiyonu. Dönüşlü yörünge yok (CLAUDE.md: öngörücü tasarım için önkoşul eksik).")
for e2, r in sorted(R.items()):
    nb = r["no_prediction"]
    W(f"- **Kestirim hatası e2 = {e2:g}** (her anlık görüntü): öngörüsüz en iyi kol {nb['selected_on_val']} = {nb['test']:.4f} b/s/Hz.")
    for k, v in r["runs"].items():
        kind, d = k.split("|")
        W(f"  - {kind}, Δ = {d} ms ({v['extra_snapshots']} ek anlık görüntü{'; q/r=' + format(v['qr'], 'g') if v['qr'] else ''}): {v['selected_on_val']} = {v['test']:.4f}; "
          f"öngörüsüze göre {v['minus_no_prediction']:+.4f} [{v['minus_no_prediction_ci'][0]:+.4f}, {v['minus_no_prediction_ci'][1]:+.4f}]")
W("")
W("## 2) Komut, tohum, ham çıktı")
W("")
W("| Komut | Tohum | Ham çıktı |")
W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/kanal_ongoru/run.py [--e2 0.01 / 0.1] | kanal 11 (rapor) / 12 (seçim), gürültü 3/4, bootstrap 0 | raw/results.json, raw/results_e2_*.json |")
W("")
W("## 3) Yorum (bulgulardan ayrı)")
W("")
W("- Gürültüsüz anlık görüntülerle öngörü belirgin kazanç sağlıyor ve en iyi adım sayısını sağa kaydırıyor (öngörü gecikmenin bedelini kısmen telafi ediyor).")
W("- %1 kestirim hatasıyla (−20 dB) her öngörücü öngörüsüz Adam'ın altına düşüyor: fark alma gürültüyü büyütüyor. Bu modelde öngörü kazancı, kestirimin pratikte ulaşamayacağı bir doğruluğa bağlı.")
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote REPORT.md")
