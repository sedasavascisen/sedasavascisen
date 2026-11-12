"""Builds thesis_exp/p4/onkodlayici_siralama/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
W("# Deney 4.3 devamı — Pilot ücreti altında bütün kolların sıralaması (rapor)"); W("")
W(f"Commit `{c}` (ölçüm commit'i `{r['commit'][:7]}`). Model Deney 4.3 ile aynı: ZF her R ms'de bir kusursuz etkin kanal kestiriminden "
  f"tazeleniyor, tazeleme başına {r['pilots_per_refresh']} pilot sembolü veri oranı 1 − t_p/R ile ücretlendiriliyor, faz t=0 kanalından ve "
  f"kolun gecikmesinde devreye giriyor, hız [gecikme, gecikme + {r['window_ms']:g} ms] üzerinde ortalanıyor. Tazeleme periyodu R her kol ve "
  "numeroloji için doğrulama çekilişinde (seed 12) seçildi; en iyi kol da orada seçildi; rapor yaşlanma kümesi (seed 11, 400 senaryo). "
  "Eşli bootstrap 2000, %95 GA. Gecikmeler tek iş parçacıklı yeniden ölçümden (thesis_exp/infra).")
W(""); W("## 1) Özet: seçilen kol"); W("")
W("| Ücretlendirme | Doğrulamada seçilen | Testte hızı | SU-best-of | Fark [%95 GA] |"); W("| --- | --- | --- | --- | --- |")
fr = r["fresh"]; b = fr["selected_on_val"]
W(f"| yok (makalenin varsayımı, taze W) | {b} | {fr['rows'][b]['rate']:.4f} | {fr['rows']['SU-best-of']['rate']:.4f} | "
  f"{fr['rows'][b]['minus_su_best_of']:+.4f} {ci(fr['rows'][b]['minus_su_best_of_ci'])} |")
for num, v in r["numerologies"].items():
    b = v["selected_on_val"]; x = v["rows"][b]
    W(f"| {num} | {b} (R = {x['R_selected_on_val']:g} ms) | {x['rate']:.4f} | {v['rows']['SU-best-of']['rate']:.4f} | "
      f"{x['minus_su_best_of']:+.4f} {ci(x['minus_su_best_of_ci'])} |")
W(""); W("## 2) Bütün kollar (test, b/s/Hz)"); W("")
nums = list(r["numerologies"])
W("| Kol | Gecikme (ms) | Taze W | " + " | ".join(f"{n}: hız (R) | {n}: − seçilen [%95 GA]" for n in nums) + " |")
W("| --- | --- | --- | " + " | ".join("--- | ---" for _ in nums) + " |")
for k in sorted(r["latency_ms"], key=lambda k: r["latency_ms"][k]):
    if k not in fr["rows"]:
        continue
    cells = []
    for n in nums:
        x = r["numerologies"][n]["rows"][k]
        cells.append(f"{x['rate']:.4f} ({x['R_selected_on_val']:g}) | {x['minus_selected']:+.4f} {ci(x['minus_selected_ci'])}")
    W(f"| {k} | {r['latency_ms'][k]:.2f} | {fr['rows'][k]['rate']:.4f} | " + " | ".join(cells) + " |")
W(""); W("## 3) Sıralama karşılaştırması (testteki ortalamaya göre, ilk 6)"); W("")
rank = lambda d: sorted(d, key=lambda k: -d[k])
W("| Sıra | Taze W | " + " | ".join(nums) + " |"); W("| --- | --- | " + " | ".join("---" for _ in nums) + " |")
R0 = rank({k: v["rate"] for k, v in fr["rows"].items()})
Rn = [rank({k: v["rate"] for k, v in r["numerologies"][n]["rows"].items()}) for n in nums]
for i in range(min(6, len(R0))):
    W(f"| {i+1} | {R0[i]} | " + " | ".join(x[i] for x in Rn) + " |")
W(""); W("## 4) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W(f"| THREADS=2 python3 thesis_exp/p4/onkodlayici_siralama/run.py ({r['seconds']/60:.0f} dk) | kanal 12 (doğrulama) / 11 (test), bootstrap 0 | raw/results.json, raw/run.log; deneme: PROBE=1 → raw/probe.json |")
y = H / "yorum.md"
if y.exists():
    W(""); W("## 5) Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
