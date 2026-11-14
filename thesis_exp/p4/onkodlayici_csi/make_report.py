"""Builds thesis_exp/p4/onkodlayici_csi/REPORT.md from raw/results.json (and the perfect-CSI reference
thesis_exp/p4/onkodlayici_siralama/raw/results.json for comparison)."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
p = json.load(open(H.parent / "onkodlayici_siralama/raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
W("# Pilot yükü ve kusurlu CSI birlikte (rapor)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}`. Model `onkodlayici_siralama` ile aynı (devreye girme anına hizalı 0.1 ms ızgara, "
  f"[gecikme, gecikme + {r['window_ms']:g} ms] ortalaması, ZF her R ms'de tazeleniyor, tazeleme başına {r['pilots_per_refresh']} pilot sembolü 1 − t_p/R ile "
  "ücretlendiriliyor, R ve kol doğrulamada seçiliyor); tek fark: BS gerçek kanalı hiç görmüyor. Faz t=0 kestiriminden, her ZF tazelemesi o anın "
  "kestiriminden; hız gerçek kanalda. Hata modeli 4.4 ile aynı (csi.add_error, e2 = 1/(1+ρ), ölçek 400 senaryonun ortalama gücünden; senaryo başına "
  "etkin SNR daha düşük ve dağınık, bkz. kusurlu_csi). Adam adım boyu 4.4'te doğrulamada seçilen değerler. Yaşlanma kümesi seed 11 (rapor), seed 12 (seçim). "
  "Eşli bootstrap 2000, %95 GA.")
W(""); W("## 1) Özet: doğrulamada seçilen kol"); W("")
W("| ρ | Ücretlendirme | Seçilen | Testte hızı | SU-best-of | Fark [%95 GA] | Kusursuz CSI'da aynı satır (onkodlayici_siralama) |"); W("| --- | --- | --- | --- | --- | --- | --- |")
W(f"| kusursuz | taze W | {p['fresh']['selected_on_val']} | {p['fresh']['rows'][p['fresh']['selected_on_val']]['rate']:.4f} | {p['fresh']['rows']['SU-best-of']['rate']:.4f} | "
  f"{p['fresh']['rows'][p['fresh']['selected_on_val']]['minus_su_best_of']:+.4f} {ci(p['fresh']['rows'][p['fresh']['selected_on_val']]['minus_su_best_of_ci'])} | — |")
for lev, v in r["levels"].items():
    b = v["fresh"]["selected_on_val"]; x = v["fresh"]["rows"][b]
    W(f"| {lev} | taze W | {b} | {x['rate']:.4f} | {v['fresh']['rows']['SU-best-of']['rate']:.4f} | {x['minus_su_best_of']:+.4f} {ci(x['minus_su_best_of_ci'])} | "
      f"{p['fresh']['rows'][b]['rate']:.4f} |")
    for n, nv in v["numerologies"].items():
        b = nv["selected_on_val"]; x = nv["rows"][b]
        W(f"| {lev} | {n} | {b} (R = {x['R_selected_on_val']:g} ms) | {x['rate']:.4f} | {nv['rows']['SU-best-of']['rate']:.4f} | "
          f"{x['minus_su_best_of']:+.4f} {ci(x['minus_su_best_of_ci'])} | {p['numerologies'][n]['rows'][b]['rate']:.4f} |")
for lev, v in r["levels"].items():
    W(""); W(f"## 2) Bütün kollar, ρ = {lev} (test, b/s/Hz)"); W("")
    nums = list(v["numerologies"])
    W("| Kol | Gecikme (ms) | Taze W | Hiç tazelenmeyen | " + " | ".join(f"{n}: hız (R) | {n}: − seçilen [%95 GA]" for n in nums) + " |")
    W("| --- | --- | --- | --- | " + " | ".join("--- | ---" for _ in nums) + " |")
    for k in sorted(r["latency_ms"], key=lambda k: r["latency_ms"][k]):
        cells = []
        for n in nums:
            x = v["numerologies"][n]["rows"][k]
            cells.append(f"{x['rate']:.4f} ({x['R_selected_on_val']:g}) | {x['minus_selected']:+.4f} {ci(x['minus_selected_ci'])}")
        W(f"| {k} | {r['latency_ms'][k]:.2f} | {v['fresh']['rows'][k]['rate']:.4f} | {v['never'][k]:.4f} | " + " | ".join(cells) + " |")
    W(""); W("İlk 4 (nokta tahmini): " + "; ".join(f"{n}: " + ", ".join(sorted(v['numerologies'][n]['rows'], key=lambda k: -v['numerologies'][n]['rows'][k]['rate'])[:4]) for n in nums))
W(""); W("## 3) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W(f"| THREADS=2 python3 thesis_exp/p4/onkodlayici_csi/run.py ({r['seconds']/60:.0f} dk) | kanal 12/11; kestirim gürültüsü 7000 + 100·ρ_i + 10·[seed=11] + kol sırası; bootstrap 0 | raw/results.json, raw/run.log |")
y = H / "yorum.md"
if y.exists():
    W(""); W("## 4) Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
