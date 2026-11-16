"""Builds thesis_exp/genis_bant/REPORT.md from raw/results.json, raw/timing.json, raw/g4.json (if present).
Hypothesis decisions follow ON_KAYIT.md exactly (no new criteria)."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent; R = H / "raw"
res = json.load(open(R / "results.json")); tm = json.load(open(R / "timing.json"))
g4 = json.load(open(R / "g4.json")) if (R / "g4.json").exists() else None
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
kof = lambda arm: int(arm.split("-")[0][1:]) if arm.startswith("K") else None
BWS, SPS = ("20", "50", "100"), ("1.5mps", "10kmh")
SPN = {"1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
C = res["cells"]

W("# Geniş bant OFDM — ön kayıtlı deney raporu"); W("")
W(f"Rapor commit'i `{commit}`, koşu commit'i `{res['commit'][:7]}`. Ön kayıt `ON_KAYIT.md` (sapmalar orada, koşudan önce). "
  "Seçim seed 12, rapor seed 11, 400 senaryo, 64 alt taşıyıcılı değerlendirme, min-kullanıcı hızı, Tanım 1 (kolun tam gecikmesinde). "
  "Fark ve GA'lar eşli bootstrap (2000, %95), seed 11 üzerinde.")
W("")
W("## 0) Önce okunmalı: sınırlar"); W("")
W("- **CD ayarlanmadı.** Plan 1–8 tarama taraması öngörüyordu; ön kayıtta varsayılan taramaya indirildi (702.97 ms). Adam adım boyu 0.5 sabit. "
  "CLAUDE.md'deki zayıf taban çizgisi kuralı bakımından G3'ün hükmü bu yüzden zayıftır.")
W("- **K_opt = 64 örneklem içidir** (değerlendirme ızgarasının kendisi); üst referans olarak okunmalı.")
W("- **Güven ufku.** 200 ms'yi aşan gecikmeler (aşağıdaki tabloda) kanal modelinin korelasyon tabanının içine düşer; oradaki hızlar fiziksel olarak güvenilir değildir.")
W("- Pilot, kestirim hatası ve ön kodlayıcı eskimesi yok (her alt taşıyıcıda taze ZF). Tek kanal modeli; genlik fc'de sabit.")
W("")
W("## 1) Ölçülmüş gecikme (boş makine, tek iş parçacığı)"); W("")
W(f"Yük: başlangıç {tm['load']['start']:.2f}, ölçüm öncesi {tm['load']['before']:.2f}, sonrası {tm['load']['after']:.2f} (sonraki değer ölçümün kendi iş parçacığını içerir).")
W(""); W("| K_opt | L=1 | L=4 | L=16 (ms, tur medyanı) | uydurma: sabit + adım (ms) | L = 48 gecikmesi (ms) |"); W("| --- | --- | --- | --- | --- | --- |")
for k in (1, 4, 16, 64):
    f = tm[f"fit_K{k}"]; m = [tm["arms"][f"K{k}_L{L}"]["median_ms"] for L in (1, 4, 16)]
    W(f"| {k} | {m[0]:.2f} | {m[1]:.2f} | {m[2]:.2f} | {f['intercept_ms']:+.2f} + {f['per_step_ms']:.3f}·L | {res['latency_ms'][f'K{k}-L48']:.1f} |")
W(""); W("SU-best-of 1.63 ms, CD 702.97 ms (dar bant, tek iş parçacıklı yeniden ölçüm; geniş bantta da fc'de optimize ettikleri için aynı).")

W(""); W("## 2) Hipotez kararları"); W("")
# G1
g1 = []
for bw in BWS:
    for sp in SPS:
        for k, d in C[f"{bw}MHz_{sp}"]["by_kopt"].items():
            g1.append((bw, sp, k, d, d["ci"][1] < 0))
n1 = sum(x[-1] for x in g1)
W(f"- **G1** (her (B, K_opt) için L = 48, L*'tan anlamlı düşük): {n1}/{len(g1)} hücrede GA sıfırın altında → "
  f"{yn(n1 == len(g1))}{'' if n1 == len(g1) else ' (tutmayan hücreler §3 tabloda)'}")
# G2
sel = {(bw, sp): C[f"{bw}MHz_{sp}"]["selected_on_val"] for bw in BWS for sp in SPS}
g2a = all((kof(sel[("20", sp)]) or 0) <= 4 and kof(sel[("20", sp)]) is not None for sp in SPS)
g2b = all((kof(sel[("100", sp)]) or 0) >= 16 for sp in SPS)
W(f"- **G2** (20 MHz'de seçilen K_opt ≤ 4, 100 MHz'de ≥ 16, her iki hızda): seçilenler "
  + "; ".join(f"{bw} MHz {SPN[sp]}: {sel[(bw, sp)]}" for bw in BWS for sp in SPS)
  + f" → 20 MHz kısmı {yn(g2a)}, 100 MHz kısmı {yn(g2b)}; bütün olarak {yn(g2a and g2b)}")
# G3
g3 = [(bw, sp, C[f"{bw}MHz_{sp}"]["cd_minus_selected"]) for bw in BWS for sp in SPS]
n3 = sum(d["ci"][1] < 0 for *_, d in g3)
W(f"- **G3** (CD, seçilen kolun anlamlı gerisinde, her B ve hızda): {n3}/{len(g3)} → {yn(n3 == len(g3))} (sınır: CD ayarlanmadı, §0)")
if g4:
    import numpy as np
    L = np.array([c["loss_pct"] for c in g4["cells"].values()])
    W(f"- **G4** (keşifsel; dar bantta kalibre edilmiş tasarım kuralı, yalnızca ölçülen adım maliyetiyle): {len(L)} hücrede kayıp medyan %{np.median(L):.2f}, "
      f"ortalama %{L.mean():.2f}, en kötü %{L.max():.2f} (ayrıntı §5)")
else:
    W("- **G4**: `g4.py` henüz koşulmadı.")

W(""); W("## 3) Hücre başına sonuç (seed 11)"); W("")
W("| B | hız | seçilen (seed 12) | etkin hız | − SU-best-of [GA] | − en iyi dar bant [GA] | CD − seçilen [GA] |"); W("| --- | --- | --- | --- | --- | --- | --- |")
for bw in BWS:
    for sp in SPS:
        c = C[f"{bw}MHz_{sp}"]
        W(f"| {bw} MHz | {SPN[sp]} | {c['selected_on_val']} | {c['selected']['eff']:.3f} | {c['selected']['minus_su_best_of']:+.3f} {ci(c['selected']['ci'])} | "
          f"{c['selected_minus_narrowband']['diff']:+.3f} {ci(c['selected_minus_narrowband']['ci'])} (dar bant: {c['narrowband_selected_on_val']}) | "
          f"{c['cd_minus_selected']['diff']:+.3f} {ci(c['cd_minus_selected']['ci'])} |")
W(""); W("### K_opt başına içsel optimum (seed 11 argmax; G1)"); W("")
W("| B | hız | K_opt | L* | gecikme (ms) | etkin hız | t = 0 hızı | L=48 − L* [GA] | L=48 kaybı (%) |"); W("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for bw, sp, k, d, _ in g1:
    flag = " ⚠ >200 ms" if d["latency_L_star"] > 200 else ""
    W(f"| {bw} MHz | {SPN[sp]} | {k} | {d['L_star_test'].split('-L')[1]} | {d['latency_L_star']:.1f}{flag} | {d['eff_L_star']:.3f} | {d['t0_L_star']:.3f} | "
      f"{d['L48_minus_Lstar']:+.3f} {ci(d['ci'])} | {d['loss_L48_pct']:.2f} |")
if g4:
    W(""); W("## 5) G4 — tasarım kuralı geniş bant kollarında"); W("")
    W("| hücre | adım (ms) | kural L | L* (seed 11) | kayıp (%) |"); W("| --- | --- | --- | --- | --- |")
    for key, c in g4["cells"].items():
        W(f"| {key} | {c['dT_ms']:.3f} | {c['L_rule']} | {c['L_star_test']} | {c['loss_pct']:.2f} |")
W(""); W("## 6) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/genis_bant/run.py --part timing | kanal 11, 20 senaryo | raw/timing.json, raw/timing.log |")
W(f"| python3 thesis_exp/genis_bant/run.py --part curves ({res['seconds']/60:.0f} dk) | kanal 12 seçim, 11 rapor; bootstrap 0 | raw/results.json, raw/curves.json, raw/curves.log |")
W("| python3 thesis_exp/genis_bant/g4.py | kanal 12 (R0), 11 (kayıp) | raw/g4.json, raw/g4.log |")
y = H / "yorum.md"
if y.exists():
    W(""); W("## 7) Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
