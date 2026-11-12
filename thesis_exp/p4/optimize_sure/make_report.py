"""Builds thesis_exp/p4/optimize_sure/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.6 — Optimize edilmiş çalışma süreleri: Adam adımı ve öğrenilen adım (rapor)"); W("")
la = r["load_avg"]
W(f"Commit `{c}` (ölçüm commit'i `{r['commit']}`). torch {r['torch']}, CPU: {r['cpu']}, iş parçacığı {r['threads']}, "
  f"CUDA: {r['cuda_available']}. Yük ortalaması: başlangıç {la['start']:.2f}, ölçüm öncesi {la['before']:.2f}, sonrası {la['after']:.2f}. "
  "Öğrenilen adım: UnrolledMuMiso (exchange, use_grad), eğitilmemiş ağırlıklar (ağırlık değeri yürütme yolunu değiştirmez). "
  "Adam: SU-average başlangıcı + L adım (soft-min, β=8, lr 0.5). 20 senaryo; senaryo başına 20 çağrının medyanı, senaryolar üzerinden medyan, 3 tur.")
W(""); W("## 1) Süreler (ms, tur medyanlarının medyanı)"); W("")
W("| Kol | Medyan (ms) | Turlar (ms) |"); W("| --- | --- | --- |")
for k, v in r["arms"].items():
    if "median_ms" in v:
        W(f"| {k} | {v['median_ms']:.3f} | {', '.join(f'{x:.3f}' for x in v['rounds_ms'])} |")
    else:
        W(f"| {k} | {' '.join(v['error'].split())} | — |")
W(""); W("## 2) Öğrenilen / Adam süre oranı"); W("")
W("| Arka uç, L | Oran |"); W("| --- | --- |")
for k, v in r["learned_over_adam"].items():
    W(f"| {k} | {v:.2f} |")
W(""); W("## 3) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/optimize_sure/run.py | senaryo seed 11, torch.manual_seed 0 | raw/results.json, raw/run.log |")
yorum = H / "yorum.md"
if yorum.exists():
    W(""); W("## 4) Yorum (bulgulardan ayrı)"); W(""); W(yorum.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
