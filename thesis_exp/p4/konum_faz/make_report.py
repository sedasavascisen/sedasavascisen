"""Builds thesis_exp/p4/konum_faz/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.2 — Konum (LoS geometrisi) tabanlı faz (rapor)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}` (results.json). Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s). Faz yalnızca LoS geometrisinden (BS anten, RIS eleman ve kullanıcı konumları; "
  "genlik ~1/d, saçıcı/gölgelenme/örüntü yok, doğrudan yol 0) SU-average / SU-best-of ile hesaplandı; gerçek kanalda (taze ZF) değerlendirildi. "
  "Konum hatası σ (yatay eksenlerde, tohum 5). Konum edinme gecikmesi modellenmedi.")
W(""); W("## 1) Bulgular"); W("")
ch = [k for k in r["arms"] if k.startswith("channel")]
for k in ch:
    W(f"- {k}: gecikme {r['arms'][k]['latency_ms']:.2f} ms, t=0 {r['arms'][k]['t0']:.4f}, etkin {r['arms'][k]['effective']:.4f} b/s/Hz")
W("")
W("| Kol | σ (m) | Gecikme (ms) | t=0 hız | Etkin hız [%95 GA] | Kanal SU-best-of'a göre [%95 GA] | Her an konumdan yeniden (0–200 ms ort.) |")
W("| --- | --- | --- | --- | --- | --- | --- |")
for k, v in r["arms"].items():
    if not k.startswith("geom-") or "fresh" in k:
        continue
    kind, sig = k.split("@0 sigma=")
    fr = r["arms"][f"{kind}-fresh sigma={sig}"]["mean_rate_0_200ms"]
    W(f"| {kind} | {sig} | {v['latency_ms']:.2f} | {v['t0']:.4f} | {v['effective']:.4f} [{v['effective_ci'][0]:.4f}, {v['effective_ci'][1]:.4f}] | "
      f"{v['minus_channel_su_best_of']:+.4f} [{v['minus_channel_su_best_of_ci'][0]:+.4f}, {v['minus_channel_su_best_of_ci'][1]:+.4f}] | {fr:.4f} |")
rnd = json.load(open(H.parents[2] / "results/mumiso_aging_stats.json"))["rows"]["random"]["effective"]
gm = [v["minus_channel_su_best_of"] for k, v in r["arms"].items() if k.startswith("geom-") and "fresh" not in k]
W(""); W(f"Rastgele faz bu kümede {rnd:.3f} b/s/Hz (results/mumiso_aging_stats.json).")
W(""); W("## 2) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/konum_faz/run.py | kanal 11, konum hatası 5, bootstrap 0 | raw/results.json |")
W(""); W("## 3) Yorum (bulgulardan ayrı)"); W("")
W(f"- Bu iç mekân modelinde (20 saçıcı, LoS olasılığı 3GPP InH) yalnızca LoS geometrisine dayanan faz, kanal tabanlı SU-best-of'un {-max(gm):.2f}–{-min(gm):.2f} b/s/Hz altında kalıyor; konum hatası sonucu değiştirmiyor, çünkü sınır geometrinin kendisinde.")
W("- Konumdan her an yeniden hesaplamak yaşlanmayı ortadan kaldırıyor ama düşük taban değeri yükseltmiyor.")
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
