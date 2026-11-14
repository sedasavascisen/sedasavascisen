"""Builds thesis_exp/p4/izgara_kontrol/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.4f}, {x[1]:+.4f}]"
W("# Makale 2 ızgara kontrolü — interpolasyon mu, tam gecikme mi? (rapor)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}`. Makale 2'nin yaşlanma taraması ve karşılaştırması (scripts/mumiso_aging_sweep.py, "
  "mumiso_aging.py) etkin hızı düzensiz bir ızgarada (0, 1, 2, 5, 7.5, 10, 13.3, 15, 19.6, 20, 26.6, 28.2, 35, 42.9, 50, 75, 100, 150, 200, 500, 1500, 5600 ms) "
  "doğrusal interpolasyonla hesaplıyor. Burada aynı kurulumla (seed 11, 400 senaryo) her kol tam kendi gecikmesinde de değerlendirildi. "
  "Izgara üzerindeki değerler yayımlanmış `results/mumiso_aging_sweep_repro.json` ile en fazla "
  f"{max(x['abs_diff'] for x in r['published_sweep_check']):.1e} farkla aynı (aynı senaryolar). Eşli bootstrap 2000, %95 GA.")
for s, v in r["sets"].items():
    W(""); W(f"## Gecikme kümesi: {s}"); W("")
    W(f"L* (bu betiğin adım kümesi, 5 dahil): interpolasyonla {v['L_star']['interpolated']}, tam {v['L_star']['exact']}. "
      f"Adam-48'in L*'a göre kaybı: interpolasyonla %{v['loss_L48_pct']['interpolated']:.2f}, tam %{v['loss_L48_pct']['exact']:.2f}.")
    W(""); W("| Kol | Gecikme (ms) | İnterpolasyon | Tam | Tam − interp. [%95 GA] |"); W("| --- | --- | --- | --- | --- |")
    for k, x in sorted(v["rows"].items(), key=lambda kv: kv[1]["latency_ms"]):
        W(f"| {k} | {x['latency_ms']:.2f} | {x['interpolated']:.4f} | {x['exact']:.4f} | {x['exact_minus_interp']:+.4f} {ci(x['ci'])} |")
    W(""); W("| Karşılaştırma | İnterpolasyon [%95 GA] | Tam [%95 GA] |"); W("| --- | --- | --- |")
    for k, x in v["comparisons"].items():
        W(f"| {k} | {x['interpolated']['diff']:+.4f} {ci(x['interpolated']['ci'])} | {x['exact']['diff']:+.4f} {ci(x['exact']['ci'])} |")
W(""); W("Komut: `python3 thesis_exp/p4/izgara_kontrol/run.py` (betik koşudan önce commit'lendi). Ham çıktı: raw/results.json, raw/run.log.")
y = H / "yorum.md"
if y.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
