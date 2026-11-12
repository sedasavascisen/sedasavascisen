"""Builds thesis_exp/p4/onkodlayici_pilot/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.3 — Ön kodlayıcı tazeleme pilotlarının ücretlendirilmesi (rapor)"); W("")
# --- correction notice (added after the follow-up thesis_exp/p4/onkodlayici_siralama found the bias) ---
_f = H.parent / "onkodlayici_siralama/raw/results.json"
if _f.exists():
    _r = json.load(open(_f))
    W("> **DÜZELTME — bu raporun pilot ücretli sayıları yanlı.** Tazeleme anları mutlak 0.1 ms ızgarasına yuvarlanıyor; yuvarlamanın yönü kolun "
      "gecikmesine bağlı. SU-best-of (1.63 ms) aşağı yuvarlandığı için her örneği 0.1 ms fazla eskimiş bir W ile ölçüldü; Adam-6 (8.09 ms) yukarı "
      "yuvarlandı. Bu da SU-best-of'u cezalandırıp aradaki farkı şişirdi. Kolun kendi devreye girme anına hizalanmış ızgarayla düzeltilmiş "
      "değerler (thesis_exp/p4/onkodlayici_siralama, R doğrulamada seçildi):")
    W(">"); W("> | Kol | Taze W | 15 kHz | 30 kHz | 60 kHz | Hiç tazelenmeyen |"); W("> | --- | --- | --- | --- | --- | --- |")
    for _k in ("SU-best-of", "Adam-6"):
        W(f"> | {_k} | {_r['fresh']['rows'][_k]['rate']:.4f} | " + " | ".join(
            f"{_r['numerologies'][n]['rows'][_k]['rate']:.4f} (R {_r['numerologies'][n]['rows'][_k]['R_selected_on_val']:g} ms)" for n in _r['numerologies'])
          + f" | {_r['never'][_k]:.4f} |")
    W(">"); W("> Aşağıdaki tablolar ilk (yanlı) koşunun kaydı olarak bırakıldı; taze W ve hiç tazelenmeyen W sütunları yuvarlamadan etkilenmiyor "
              "(ikincisi ≤0.01 b/s/Hz). Bütün kolların sıralaması için onkodlayici_siralama/REPORT.md.")
    W("")
W(f"Commit `{c}`. Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s), 0.1 ms ızgara. Faz t=0'da hesaplanıp kolun gecikmesinde devreye alınıyor; "
  f"ZF ön kodlayıcı her R ms'de bir, o anın (kusursuz) etkin kanal kestiriminden yeniden hesaplanıyor ve arada eski haliyle kullanılıyor. "
  f"Her tazeleme {r['pilots_per_refresh']} pilot sembolü (kullanıcı başına bir), veri yok: veri oranı 1 − t_p/R ile ücretlendirildi. "
  f"Ortalama penceresi devreye almadan sonraki {r['window_ms']:.0f} ms.")
W(""); W("## 1) Bulgular"); W("")
for ph, v in r["phases"].items():
    W(f"**{ph}:** makalenin varsayımı (her an taze ve bedava W) {v['fresh']:.4f}; hiç tazelenmeyen W {v['never']:.4f} b/s/Hz.")
    W("")
    W("| R (ms) | " + " | ".join(f"{n} hız [taze'ye göre]" for n in v["by"]) + " |")
    W("| --- | " + " | ".join("---" for _ in v["by"]) + " |")
    Rs = [k for k in next(iter(v["by"].values())) if k != "best_R_ms"]
    for R_ in Rs:
        cells = []
        for n, b in v["by"].items():
            x = b[R_]; cells.append(f"{x['rate']:.3f} [{x['minus_fresh']:+.3f}]")
        W(f"| {R_} | " + " | ".join(cells) + " |")
    W("| en iyi R | " + " | ".join(f"{b['best_R_ms']:g} ms" for b in v["by"].values()) + " |")
    W("")
W("## 2) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/onkodlayici_pilot/run.py | kanal 11, bootstrap 0 | raw/results.json |")
W(""); W("## 3) Yorum (bulgulardan ayrı)"); W("")
W("- Makale 2'nin bütün etkin hızları 'taze ve bedava ön kodlayıcı' varsayımına dayanıyor (makalede sınırlılık olarak yazılı). Pilot süresi ücretlendirilince en iyi tazeleme periyodu 1–2 ms çıkıyor ve hız belirgin düşüyor: ZF girişim sıfırlaması kanal değişimine çok duyarlı.")
W("- Bu, mutlak hızları ve muhtemelen öğrenilen/klasik farklarının büyüklüğünü etkiler; yöntem sıralamasının bu ücretlendirme altında değişip değişmediği ayrı bir deneyle sınanmalı (bu deney yalnızca iki fazla yapıldı).")
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
