"""Builds thesis_exp/p4/gecikme_muhasebesi/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Gecikme muhasebesi — SU-average başlangıcını Adam-L gecikmesine eklemenin etkisi (denetim U16)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}`. Yaşlanma kümesi (seed 11, 400 senaryo), 0.5 ms ızgara 0–70 ms, tek iş parçacığı. "
  f"Her Adam-L kolu (sürekli; 1 ve 2 bite yuvarlanmış) için etkin hız (Tanım 1) adam_latency(L)'de ve buna SU-average süresi ({r['su_average_ms']:.3f} ms) "
  "eklenmiş gecikmede; eşli fark, bootstrap 2000, %95 GA.")
W(""); W("| Kol | Gecikme (ms) | Etkin hız | Başlangıç eklenince | Fark [%95 GA] |"); W("| --- | --- | --- | --- | --- |")
for k, v in r["arms"].items():
    W(f"| {k} | {v['lat_ms']:.2f} | {v['eff']:.4f} | {v['eff_charged']:.4f} | {v['diff']:+.4f} [{v['diff_ci'][0]:+.4f}, {v['diff_ci'][1]:+.4f}] |")
s = r["summary"]
W(""); W(f"Özet: fark {s['min_diff']:+.4f} … {s['max_diff']:+.4f} b/s/Hz; ortalama mutlak fark {s['mean_abs_diff']:.4f}.")
W(""); W("Komut: `python3 thesis_exp/p4/gecikme_muhasebesi/run.py` (betik koşudan önce commit'lendi). Ham çıktı: raw/results.json.")
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
