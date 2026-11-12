"""Builds thesis_exp/p4/ayrik_faz/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.5 — 1 ve 2 bitlik ayrık faz: L* ve yavaş çözücü (rapor)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}` (results.json). Yaşlanma kümesi (seed 11, 400 senaryo), seçim doğrulama çekilişinde (seed 12). Fazlar t=0 kanalından; "
  "sürekli kollar system.quantise_phase ile yuvarlandı (yuvarlama bedava sayıldı). dCD-s: baselines.coord_descent(bits=b, iters=s), "
  "gerçek 2^b ızgarasında. SU-best-of ve Adam-L gecikmeleri tek iş parçacıklı yeniden ölçümden (thesis_exp/infra); "
  "dCD gecikmeleri bu deneyde boş makinede ölçüldü (tek iş parçacığı, tek senaryo, 10 senaryo × 5 tekrarın medyanı, 3 tur). "
  "Karşılaştırmalar SU-best-of→q'ya karşı eşli bootstrap (2000, %95 GA).")
for b, v in r["bits"].items():
    W(""); W(f"## {b} bit"); W("")
    la = v["load_avg"]
    W(f"Yük ortalaması: başlangıç {la['start']:.2f}, ölçüm öncesi {la['before']:.2f}, sonrası {la['after']:.2f}. "
      f"Doğrulamada seçilen kol: **{v['selected_on_val']}**. L* (test, yuvarlanmış Adam kolları): **{v['L_star']}**. "
      f"Adam-48→q'nun L*'a göre kaybı: %{v['loss_L48_vs_Lstar_pct']:.1f}.")
    W(""); W("| Kol | Gecikme (ms) | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |"); W("| --- | --- | --- | --- | --- |")
    for k, x in sorted(v["rows"].items(), key=lambda kv: kv[1]["latency_ms"]):
        W(f"| {k} | {x['latency_ms']:.2f} | {x['t0']:.4f} | {x['effective']:.4f} [{x['effective_ci'][0]:.4f}, {x['effective_ci'][1]:.4f}] | "
          f"{x['minus_su_best_of_q']:+.4f} [{x['minus_su_best_of_q_ci'][0]:+.4f}, {x['minus_su_best_of_q_ci'][1]:+.4f}] |")
    W(""); W("dCD zamanlaması (tur medyanları, ms): " + "; ".join(f"{k}: {t['median_ms']:.1f} ({', '.join(f'{q:.1f}' for q in t['rounds_ms'])})"
                                                          for k, t in v["dcd_timing"].items()))
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/ayrik_faz/run.py | kanal 11 (test) / 12 (doğrulama), bootstrap 0 | raw/results.json, raw/run.log |")
yorum = H / "yorum.md"
if yorum.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(yorum.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
