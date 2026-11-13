"""Builds thesis_exp/p4/ayrik_faz/REPORT.md from raw/results_exact.json (exact-latency evaluation; K3/U20).
raw/results.json (run.py, coarse-grid interpolation above 40 ms) is kept only as the source of the dCD timings."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results_exact.json"))
r0 = json.load(open(H / "raw/results.json"))
_r3 = H / "raw/results_3bit.json"
if _r3.exists():
    r3 = json.load(open(_r3)); r["bits"].update(r3["bits"]); r["commit_3bit"] = r3["commit"]
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.4f}, {x[1]:+.4f}]"
W("# Deney 4.5 — 1 ve 2 bitlik ayrık faz: L* ve yavaş çözücü (rapor)"); W("")
W("> **DÜZELTME (denetim K3, 12 Kasım):** İlk sürüm etkin hızı, 40 ms'den sonra 50/75/100/150 ms'ye atlayan kaba bir ızgarada doğrusal "
  "interpolasyonla hesaplıyordu (koherans süresi ~28 ms). Bu yüzden 40 ms'den yavaş her kolun (Adam-32/48→q, dCD-2…8) değeri ±0.055 b/s/Hz'e "
  "kadar yanlıştı. Bu rapor her kolu **tam kendi gecikme anında** değerlendiren `run_exact.py`'den (`raw/results_exact.json`). "
  "İlk sürümün `raw/results.json` dosyası yalnızca dCD zamanlamalarının kaynağı olarak duruyor.")
W("")
W(f"Rapor commit'i `{c}`. Ölçüm commit'leri: değerlendirme `{r['commit'][:7]}` (results_exact.json), dCD zamanlaması `{r0['commit'][:7]}` (results.json)" + (f"; 3 bit (zamanlama + değerlendirme) `{r['commit_3bit'][:7]}` (results_3bit.json)" if "commit_3bit" in r else "") + ". "
  "Yaşlanma kümesi (seed 11, 400 senaryo), seçim doğrulama çekilişinde (seed 12). Fazlar t=0 kanalından; sürekli kollar system.quantise_phase "
  "ile yuvarlandı (yuvarlama bedava sayıldı). dCD-s: baselines.coord_descent(bits=b, iters=s), gerçek 2^b ızgarasında. SU-best-of ve Adam-L "
  "gecikmeleri tek iş parçacıklı yeniden ölçümden (thesis_exp/infra; Adam-L SU-average başlangıcını içermiyor, etkisi p4/gecikme_muhasebesi). "
  "dCD gecikmeleri boş makinede ölçüldü (tek iş parçacığı, 10 senaryo × 5 tekrarın medyanı, 3 tur). İki tasarım: **lr0.5** (Adam adım boyu 0.5, "
  "makalenin yaşlanma kümesi değeri) ve **lr-val** (adım boyu her L ve bit için doğrulamada {0.25, 0.5, 0.75, 1.0} içinden seçildi; denetim U20). "
  "Eşli bootstrap 2000, %95 GA.")
for b, v in r["bits"].items():
    W(""); W(f"## {b} bit"); W("")
    la = v["load_avg"]
    W(f"dCD zamanlaması yük ortalaması: başlangıç {la['start']:.2f}, ölçüm öncesi {la['before']:.2f}, sonrası {la['after']:.2f}.")
    for dname, d in v["designs"].items():
        W(""); W(f"### Tasarım {dname}"); W("")
        W(f"Doğrulamada seçilen kol: **{d['selected_on_val']}**. L* (test, yuvarlanmış Adam kolları): **{d['L_star']}**. "
          f"Adam-48→q'nun L*'a göre kaybı: %{d['loss_L48_vs_Lstar_pct']:.1f}.")
        if d["paired"]:
            W(""); W("Eşli farklar (test): " + "; ".join(f"{k}: {x['diff']:+.4f} {ci(x['ci'])}" for k, x in d["paired"].items()))
        W(""); W("| Kol | Gecikme (ms) | lr | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |"); W("| --- | --- | --- | --- | --- | --- |")
        for k, x in sorted(d["rows"].items(), key=lambda kv: kv[1]["latency_ms"]):
            W(f"| {k} | {x['latency_ms']:.2f} | {'' if x['lr'] is None else x['lr']} | {x['t0']:.4f} | {x['effective']:.4f} "
              f"[{x['effective_ci'][0]:.4f}, {x['effective_ci'][1]:.4f}] | {x['minus_su_best_of_q']:+.4f} {ci(x['minus_su_best_of_q_ci'])} |")
    W(""); W("dCD zamanlaması (tur medyanları, ms): " + "; ".join(f"{k}: {t['median_ms']:.1f} ({', '.join(f'{q:.1f}' for q in t['rounds_ms'])})"
                                                          for k, t in v["dcd_timing"].items()))
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/ayrik_faz/run.py (dCD zamanlaması; boş makine) | kanal 11/12, bootstrap 0 | raw/results.json, raw/run.log |")
W("| python3 thesis_exp/p4/ayrik_faz/run_3bit.py (3 bit: boş makinede dCD zamanlaması + tam gecikmede değerlendirme) | kanal 11/12, bootstrap 0 | raw/results_3bit.json, raw/run_3bit.log |")
W("| python3 thesis_exp/p4/ayrik_faz/run_exact.py (tam gecikmede değerlendirme, iki lr tasarımı) | kanal 11 (test) / 12 (doğrulama), bootstrap 0 | raw/results_exact.json, raw/run_exact.log |")
yorum = H / "yorum.md"
if yorum.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(yorum.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
