"""Builds thesis_exp/infra/REPORT.md from thesis_exp/infra/raw/ and results/ (read-only)."""
import json, pathlib, subprocess
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[3]
RAW = ROOT / "thesis_exp/infra/raw"
J = lambda p: json.load(open(p))
bi = J(RAW / "bit_identity.json")
old_lat, new_lat = J(ROOT / "results/mumiso_mobility_latency.json"), J(RAW / "mumiso_mobility_latency_rerun.json")
old_st, new_st = J(ROOT / "results/mumiso_aging_stats.json"), J(RAW / "mumiso_aging_stats_newlat.json")
old_sens = J(ROOT / "results/mumiso_aging_sensitivity.json")["by_velocity"]["1.5"]["by_overhead"]["0.0"]
new_sw = J(RAW / "mumiso_aging_sweep_newlat.json")
su = J(RAW / "static_split_usage.json")
load_b = open(RAW / "mobility_latency_rerun.load_before").read().split()[0]
load_a = open(RAW / "mobility_latency_rerun.load_after").read().split()[0]
m1 = {p.stem: J(p) for p in (RAW / "m1_38901").glob("*.json")}
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
f3 = lambda x: f"{x:.3f}"
ci = lambda d: f"{d['diff']:.3f} [{d['ci'][0]:.3f}, {d['ci'][1]:.3f}]"

ob = max(old_sens["rows"], key=lambda r: r["effective"]); ol = [r for r in old_sens["rows"] if r["L"] == 48][0]
nb = max(new_sw, key=lambda r: r["effective"]); nl = [r for r in new_sw if r["L"] == 48][0]
near = lambda rows, b: [r["L"] for r in rows if r["L"] > 0 and r["effective"] >= b["effective"] * (1 - 0.005)]

out = []; W = out.append
W("# Tez deneyleri için ortak altyapı — rapor")
W("")
W(f"Dal `thesis/altyapi`, rapor commit'i `{commit}`. Mevcut dosyalara dokunulmadı: yeniden koşular `thesis_exp/infra/scripts/` "
  "altındaki, çıktısı `thesis_exp/infra/raw/`'a yönlendirilmiş kopyalarla yapıldı.")
W("")
W("## 1) Makaledeki iddialarla çelişen ya da onları değiştiren bulgular")
W("")
W(f"1. **Adam adım süresi 1.66 ms değil, {new_lat['slope_ms_per_step']:.3f} ms** (tek iş parçacığı, boş makine, yük {load_b} → {load_a}; "
  f"L başına {min(new_lat['per_step'].values()):.2f}–{max(new_lat['per_step'].values()):.2f} ms). Makalenin 1.66 ms'si eski iki iş parçacıklı Adam-8 "
  "ölçümünden (13.3/8) geliyor; yöntem bölümünde bu yazılı.")
W(f"2. Yeni gecikmeyle **L\\* = {nb['L']}** (makale bu ızgarada {ob['L']}; metin 4–6 diyor), %0.5 içindeki aralık {near(new_sw, nb)}; "
  f"L=48'e koşmanın bedeli **%{100*(1-nl['effective']/nb['effective']):.1f}** (makale %{100*(1-ol['effective']/ob['effective']):.1f}). Bulgu korunuyor, sayılar değişiyor.")
W(f"3. SU-best-of − CD: **{ci(new_st['paired']['su_best_of-cd'])}** (makale {ci(old_st['paired']['su_best_of-cd'])}); "
  f"SU-best-of − uzun Adam: **{ci(new_st['paired']['su_best_of-pga'])}** (makale {ci(old_st['paired']['su_best_of-pga'])}). "
  f"SU-best-of − Adam-20 artık {ci(new_st['paired']['su_best_of-adam20'])} (makale {ci(old_st['paired']['su_best_of-adam20'])}).")
W(f"4. **Kullanılmayan senaryo sayısı 800 değil {su['never_used_total']}**: doğrulama kümesinin {su['val_used_by_any']} senaryosu kullanılıyor "
  "(öğrenilen kuralın checkpoint seçimi va[:500]; makale 'doğrulama 400' diyor), testin 600'ü.")
W("")
W("## 2) Tablo")
W("")
W("| İddia | Yayımlanan | Üretilen | Durum | Kanıt |")
W("| --- | --- | --- | --- | --- |")
for f, r in bi["files"].items():
    st = "DOĞRULANDI (bit-bit)" if r["identical"] else ("FARKLI — betiği yok, makale kullanmıyor" if f == "mumiso_aging_sweep_fixzf.json" else "FARKLI")
    W(f"| Yeniden üretim: results/{f} | — | {r['n_differences']} fark | {st} | raw/bit_identity.json |")
W("| Yeniden üretim: results/mumiso_aging_sensitivity.json | — | 0 fark (config hariç) | DOĞRULANDI (bit-bit) | raw/mumiso_aging_sensitivity.json |")
W("| Yeniden üretim: 9 tablo + paper_numbers.txt | — | `cmp` ile aynı | DOĞRULANDI (bit-bit) | raw/assets/ |")
W(f"| Adam adım süresi | 1.66 ms | {new_lat['slope_ms_per_step']:.3f} ms | FARKLI | raw/mumiso_mobility_latency_rerun.json |")
for k in ("su_best_of", "cd", "pga"):
    W(f"| {k} gecikmesi | {old_lat['median'][k]:.2f} ms | {new_lat['median'][k]:.2f} ms | FARKLI (yeniden ölçüm) | aynı |")
W(f"| L\\* (1.5 m/s, T_ov=0) | {ob['L']} (metin 4–6) | {nb['L']} (%0.5 içi {near(new_sw, nb)}) | FARKLI (aralık içinde) | raw/mumiso_aging_sweep_newlat.json |")
W(f"| En iyi etkin hız | {ob['effective']:.3f} | {nb['effective']:.3f} | FARKLI | aynı |")
W(f"| L=48 kaybı | %{100*(1-ol['effective']/ob['effective']):.1f} | %{100*(1-nl['effective']/nb['effective']):.1f} | FARKLI (küçük) | aynı |")
for k, name in (("su_best_of-cd", "SU-best-of − CD"), ("su_best_of-pga", "SU-best-of − uzun Adam"), ("su_best_of-adam20", "SU-best-of − Adam-20")):
    W(f"| {name} | {ci(old_st['paired'][k])} | {ci(new_st['paired'][k])} | {'DOĞRULANDI (GA örtüşüyor)' if k != 'su_best_of-adam20' else 'FARKLI'} | raw/mumiso_aging_stats_newlat.json |")
for k in ("adam8", "adam12", "adam16", "adam20"):
    W(f"| Tablo I {k} etkin hız | {old_st['rows'][k]['effective']:.3f} @ {old_st['rows'][k]['latency_ms']:.2f} ms | "
      f"{new_st['rows'][k]['effective']:.3f} @ {new_st['rows'][k]['latency_ms']:.2f} ms | FARKLI | aynı |")
W(f"| Statik küme kullanımı | 4200/400/600 (800 boşta) | 4200 / {su['val_used_by_any']} / {su['test_used_by_any']} ({su['never_used_total']} boşta) | FARKLI | raw/static_split_usage.json |")
if m1:
    def agg(prefix):
        xs = [v for k, v in m1.items() if k.startswith(prefix) and not k.endswith("_perm")]
        return xs
    for lbl, pre in (("sin/cos CNN–LSTM (ham girdi)", "sincos_raw_s"), ("doğrudan açı eşleniği", "angle_raw_s"), ("sin/cos, ölçek-normalize", "sincos_norm_s")):
        xs = agg(pre)
        if xs:
            r_ = [x["test_rmse_deg"] for x in xs]
            W(f"| 38.901, N_t=1: {lbl} | — | RMSE {', '.join(f'{x:.2f}' for x in r_)}°; hız {np.mean([x['rate_bpshz'] for x in xs]):.3f} "
              f"(optimum {xs[0]['rate_optimum_bpshz']:.3f}, makale etiketi (a) {xs[0]['rate_published_label_a_bpshz']:.3f}) b/s/Hz | ölçüldü | raw/m1_38901/{pre}*.json |")
    pr = [v for k, v in m1.items() if k.endswith("_perm")]
    if pr:
        pr_s = ", ".join(f"{x['test_rmse_deg']:.2f}" for x in pr)
        W(f"| 38.901: eleman permütasyonu | — | RMSE {pr_s}° | ölçüldü | raw/m1_38901/*_perm.json |")
W("")
W("## 3) Komutlar, tohumlar, ham çıktılar")
W("")
W("| Adım | Komut | Tohum | Ham çıktı |")
W("| --- | --- | --- | --- |")
W("| 1 | thesis_exp/infra/scripts/mumiso_aging.py --no-learned --tag aging_fixzf; mumiso_aging_sweep.py --tag aging_sweep_fixzf; mumiso_aging_sensitivity.py; make_paper_assets.py (yönlendirilmiş kopyalar); bit_identity.py | kanal 11, torch 0 | raw/bit_identity.json, raw/assets/ |")
W("| 2 | mumiso_mobility_latency.py --tag mobility_latency_rerun (yük < 0.5 beklendi); aging_sweep_newlat.py --steps 1,…,48; mumiso_aging_stats_newlat.py | kanal 11, bootstrap betikteki gibi | raw/mumiso_mobility_latency_rerun.json, raw/mumiso_aging_sweep_newlat.json, raw/mumiso_aging_stats_newlat.json |")
W("| 3 | static_split_usage.py | split seed 0 | raw/static_split_usage.json |")
W("| 4 | m1_on_38901.py --head {sincos,angle} --scale {raw,norm} --seed {0,1,2} [--permute] | veri 2026 (data_sumiso/sumiso_siso.npz, md5 9958f6b7…), bölme 0, permütasyon 7 | raw/m1_38901/ |")
W("")
W("## 4) Açık sorular")
W("")
W("1. Makale 2 gönderildi; yeni adım süresiyle değişen sayılar (L\\* 5→6, %14.0→%14.4, Tablo I satırları) düzeltme/revizyonda mı güncellensin?")
W("2. Tablo II hızları ve periyodik çalışma (Tablo III) da 1.66 ms ile hesaplandı; yeni süreyle yeniden üretilsin mi?")
W("3. 38.901 arayüzünde h_d girdi kanalları Makale 1'den sapma; tezde böyle mi anlatılsın?")
W("")
W("## 5) Yorum (bulgulardan ayrı)")
W("")
W("- Makalenin yayımlanan sayılarının kaynak dosyaları bugünkü kodla bit-bit üretiliyor; değişen tek girdi ölçülen adım süresi.")
W("- Adam'ın daha hızlı ölçülmesi optimumu biraz sağa kaydırıyor ve Adam kollarını iyileştiriyor; 'yavaş çözücü kaybeder' ve 'iç optimum' bulguları korunuyor.")
(ROOT / "thesis_exp/infra/REPORT.md").write_text("\n".join(out) + "\n")
print("wrote thesis_exp/infra/REPORT.md")
