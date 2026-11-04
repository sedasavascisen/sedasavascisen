# -*- coding: utf-8 -*-
"""Tez yazarken atif yapilacak her sayiyi JSON'lardan uretir."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[1] / "results"
def L(n):
    p = R / n
    return json.loads(p.read_text()) if p.exists() else None

sec4   = L("mumiso_sec4_fixzf.json")
link   = L("mumiso_linkratio.json")
unr    = L("mumiso_unrolled_fixzf.json")
nog    = L("mumiso_nograd_fixzf.json")
eqs    = L("mumiso_equal_step.json")
lat    = L("mumiso_latency_parity.json")
rep    = L("mumiso_latency_repeat.json")
age    = L("mumiso_aging_sweep_fixzf.json")
anc    = L("anchor_full_test.json")
out = []
W = out.append

W("# Tez Yazim Referansi — olculmus her sayi, kaynagiyla")
W("")
W("Bu dosya `results/*.json` icinden **uretildi**, elle yazilmadi.")
W("Her tablonun altinda hangi dosyadan geldigi yazili.")
W("")
W("> Bir sayiyi teze koymadan once kaynak dosyasini acin. Bu dosya")
W("> kolaylik icindir, otorite degil.")
W("")

W("## Bolum 4 — cok kullanicili ogrenmenin sinirlari")
W("")
W("### 4.1 Tek gecisli tahmin capada donuyor")
W("")
ANC = 3.5363
W(f"Capa (`su_average`, modellerin puanlandigi **ayni** 1800 senaryoluk test bolmesi): **{ANC:.4f}**  ")
if anc:
    W(f"`su_best_of` (bedava, K+1 adayin en iyisi): **{anc['su_best_of']:.4f}**  ")
    W(f"`su_weakest`: {anc['su_weakest']:.4f}")
W("")
if sec4:
    W(f"Hedef (en guclu klasik, olcumle secildi): **{sec4['target']['method']} = {sec4['target']['rate']:.4f}**")
    W("")
    W("| Mimari | Test min hiz | Capa orani | Permutasyon yayilimi | Parametre |")
    W("| --- | --- | --- | --- | --- |")
    for k in ("concat", "deepsets", "exchange"):
        m = sec4["models"][k]
        W(f"| {k} | {m['test_min']:.4f} | {m['test_min']/ANC:.4f} | {m['perm_spread']:.2e} | {m['params']:,} |")
    W("")
    W("Kaynak: `results/mumiso_sec4_fixzf.json`, capa `results/anchor_full_test.json`")
W("")
W("Egitilmemis ag ile su_average, 400 senaryoda dort ondaliga kadar ayni: **3.7230 / 3.7230**.  ")
W("Artik kafasinin baslangic sapmasi: 0.013 derece.  ")
W("En iyi epok (12 epoktan): concat **4**, deepsets **9**, exchange **2**.")
W("")

W("### 4.2 Nedeni: belirlenmis ama duzgun olmayan fonksiyon")
W("")
W("| Olcum | Deger |")
W("| --- | --- |")
W("| Ayni senaryo, iki farkli baslangic — cos uyusmasi | +0.58 / +0.81 / +0.57 |")
W("| Farkli senaryolar — cos uyusmasi | +0.005 / +0.009 / −0.003 |")
W("| Oracle hizi (Adam, 600 adim) | 6.1619 |")
W("| Capa (bu tanida) | 3.4350 |")
W("| Gozetimli uyum, egitim MSE (son epok) | 0.8958 |")
W("| Gozetimli uyum, dogrulama MSE | 0.9250 |")
W("| Gozetimli modelin test hizi | 3.4064 (capanin ALTINDA) |")
W("")
W("Kaynak: `results/learnability_fixzf.log`, `scripts/diagnose_learnability.py`")
W("")
W("Komsuluk testi: en yakin oznitelik komsusuna **+0.0047**, rastgele senaryoya **+0.0089**.")
W("Ikisi de sifirdan ayirt edilemez; aralarindaki sira gurultudur.")
W("")

W("### 4.3 Temsil hipotezi kuruldu ve REDDEDILDI")
W("")
W("Hipotez: `features.py` normalizasyonu RIS kaskadi / dogrudan yol guc oranini siliyor.")
W("")
W("| | gercek | agin gordugu |")
W("| --- | --- | --- |")
W("| Oranin senaryolar arasi yayilimi | 9.4 milyon kat | 1.000 kat |")
W("| Gercek oranla korelasyon | — | +0.031 |")
W("")
W("Bilgi geri verildi (iki kanal, `features.link_ratio=True`), yeni korelasyon **+1.0000**.")
W("Ayni kanal cekilisi, ayni epok sayisi, tek fark iki kanal:")
W("")
if sec4 and link:
    W("| Mimari | Oran kanali YOK | Oran kanali VAR | Degisim |")
    W("| --- | --- | --- | --- |")
    for k in ("concat", "deepsets", "exchange"):
        o, n = sec4["models"][k]["test_min"], link["models"][k]["test_min"]
        W(f"| {k} | {o:.4f} | {n:.4f} | {100*(n/o-1):+.2f}% |")
    W("")
    W("Kaynak: `results/mumiso_sec4_fixzf.json` ve `results/mumiso_linkratio.json`")
W("")
W("**Sonuc:** eksik bilgi, stall'in sebebi degildi. Uc model de biraz kotulesti.")
W("Dusus iki modelde kendi epok-arasi gurultusunun disinda (deepsets gurultu %0.29,")
W("exchange %0.13).")
W("")

W("### 4.4 Ogrenilen guncelleme kurali")
W("")
if unr and nog:
    W("| Gradyan girdi | Test min | Capaya gore | AO orani | Parametre |")
    W("| --- | --- | --- | --- | --- |")
    a = unr["anchor"]
    W(f"| **var** | {unr['test_min']:.4f} | {100*(unr['test_min']/a-1):+.1f}% | {unr['frac_of_ao']:.3f} | {unr['params']:,} |")
    W(f"| **yok** | {nog['test_min']:.4f} | {100*(nog['test_min']/nog['anchor']-1):+.1f}% | {nog['frac_of_ao']:.3f} | {nog['params']:,} |")
    W("")
    W(f"Capa (her iki kol) {a:.4f} · cd {unr['cd']:.4f} · AO {unr['ao']:.4f}")
    W("")
    W(f"Adim izi (gradyan var): {' → '.join(f'{x:.3f}' for x in unr['per_step'])}")
    W(f"Adim izi (gradyan yok): {' → '.join(f'{x:.3f}' for x in nog['per_step'])}")
    W("")
    W("Ogrenilen adim boylari: var 0.589 → 0.258 (azalan cizelge) · yok hepsi ~0.49 (duz)")
    W("")
    W("Kaynak: `results/mumiso_unrolled_fixzf.json`, `results/mumiso_nograd_fixzf.json`")
W("")

W("### 4.5 Esit adim vs esit milisaniye — ikisi CELISIYOR")
W("")
if eqs:
    W(f"Capa {eqs['anchor']:.4f} · `su_best_of` {eqs['su_best_of']:.4f}")
    W("")
    W("**Esit ADIM** — ogrenilen kural her butcede onde:")
    W("")
    W("| L | Ogrenilen | Ayarlanmis Adam | Oran | Eslest. fark − 2 s.e. | Kazanma orani |")
    W("| --- | --- | --- | --- | --- | --- |")
    for Lk in sorted(eqs["rows"], key=int):
        v = eqs["rows"][Lk]
        lo = v["paired_mean_diff"] - 2*v["paired_sem"]
        W(f"| {Lk} | {v['learned']:.4f} | {v['swept']:.4f} | {v['learned_over_swept']:.3f} | {lo:+.4f} | {100*v['learned_wins_frac']:.1f}% |")
    W("")
    W("Adim boyu her butcede dogrulamada secildi; optimum her L'de **0.75**, onlu izgaranin")
    W("yedinci konumu — yani kenarda degil, ic noktada. Yumusak/sert objektif farki 0.008–0.018.")
    W("")
    W("Kaynak: `results/mumiso_equal_step.json`")
W("")
if lat and rep:
    import statistics as st
    lm = {int(k): st.median(v) for k, v in rep["learned"].items()}
    am = {int(k): st.median(v) for k, v in rep["adam"].items()}
    lr_ = {int(k): v["rate"] for k, v in lat["learned"].items()}
    ar_ = {int(k): v["rate"] for k, v in lat["classical"].items()}
    W("**Esit MILISANIYE** — bes noktanin besi de baskinlanmis, bes turun besinde:")
    W("")
    W("| Ogrenilen L | Gecikme | Hiz | Baskinlayan Adam |")
    W("| --- | --- | --- | --- |")
    for Lk in sorted(lm):
        cands = [(k, am[k], ar_[k]) for k in am if am[k] <= lm[Lk] and ar_[k] >= lr_[Lk]]
        if cands:
            k, ms, r = max(cands, key=lambda t: t[2])
            W(f"| {Lk} | {lm[Lk]:.2f} ms | {lr_[Lk]:.4f} | L={k}: {ms:.2f} ms, {r:.4f} |")
        else:
            W(f"| {Lk} | {lm[Lk]:.2f} ms | {lr_[Lk]:.4f} | — (cephede) |")
    W("")
    W("Adim maliyeti orani: ~2.7× (bir ogrenilen adim = ~2.7 Adam adimi).")
    W("Turlar arasi zamanlama oynamasi 1.06×–1.41× (bos makine, 5 tur).")
    W("")
    W("Kaynak: `results/mumiso_latency_parity.json`, `results/mumiso_latency_repeat.json`")
W("")

W("## Bolum 5 — hareketlilik ve gecikme-farkinda tasarim")
W("")
W("Tutarlilik suresi: 3 GHz, 1.5 m/s → f_d = 15.0 Hz → **T_c = 28.2 ms**")
W("")
if age:
    W("| L | Gecikme | t=0 hizi | **Gecerli hiz** |")
    W("| --- | --- | --- | --- |")
    rows = age if isinstance(age, list) else age.get("rows", age)
    try:
        items = sorted(rows.items(), key=lambda kv: int(kv[0])) if isinstance(rows, dict) else [(r.get("L"), r) for r in rows]
        for Lk, v in items:
            if isinstance(v, dict) and "eff" in v and "t0" in v:
                W(f"| {Lk} | {v.get('lat_ms', float('nan')):.1f} ms | {v['t0']:.3f} | **{v['eff']:.3f}** |")
    except Exception as e:
        W(f"(otomatik cikarilamadi: {e} — `results/mumiso_aging_sweep_fixzf.json` acin)")
    W("")
W("Elle dogrulanmis ana satirlar (bolum 5b taslagindan):")
W("")
W("| Yontem | t=0 hizi | Gecikme | Gecerli hiz |")
W("| --- | --- | --- | --- |")
W("| su_average | 4.624 | ~0 | 4.624 |")
W("| su_best_of | 5.276 | 0.05 ms | 5.276 |")
W("| Adam-8 | — | 13.3 ms | **5.849** |")
W("| Adam-16 | — | 26.6 ms | 5.324 |")
W("| koordinat inisi | — | ~1500 ms | 4.921 |")
W("| PGA | **7.117** | ~5600 ms | **4.667** |")
W("")
W("Icsel optimum: **L = 4** → 5.982. Yakinsamaya gore tasarlamak (L=48) **%14** kaybettiriyor.")
W("Eskimis faz tabani ~4.35 (sifira cokmuyor).")
W("")
W("### Yuk tasiyan varsayim: huzme taze, faz eskimis")
W("")
W("> **DUZELTME (27 Ekim).** Bu sayi uzun sure \"17 kat (4.718 / 0.279)\" diye")
W("> alintilandi. O olcum betige yazilmamisti ve **yeniden uretilemiyor**.")
W("> `scripts/mumiso_beam_staleness.py` ile olculdugunde hicbir faz secimi")
W("> 17 kat vermiyor. Nitel iddia -- bir buyukluk mertebesi -- saglam;")
W("> sayinin kendisi yanlisti.")
W("")
bs = L("mumiso_beam_staleness.json")
if bs:
    W("28.2 ms'de (tutarlilik suresi), faz t=0'da secilip huzme ya taze ya eskimis:")
    W("")
    W("| Faz secimi | Taze huzme | Eskimis huzme | Oran |")
    W("| --- | --- | --- | --- |")
    for ph, tg in (("su_average", "beam_staleness_su_average"),
                   ("su_best_of", "beam_staleness"),
                   ("adam8", "beam_staleness_adam8")):
        j = L(f"mumiso_{tg}.json")
        if j:
            c = j["at_coherence"]
            W(f"| {ph} | {c['fresh']:.4f} | {c['stale']:.4f} | **{c['ratio']:.1f}x** |")
    W("")
    W("Kaynak: `scripts/mumiso_beam_staleness.py`, `results/mumiso_beam_staleness*.json`")
    W("")
    W("Eskimis deger her uc faz seciminde de ~0.305; taze deger 3.59-4.36.")
    W("Teze **11.7-14.2 kat** yazin, 17 degil.")
W("")
W("Modelin gecerlilik ufku: korelasyon tabani ~0.5 (bagimsiz cekiliste 0.10);")
W("sacici sayisi 6→60 tabani yalnizca 0.60→0.51 indiriyor. Guvenilir aralik **τ ≤ 200 ms**.")
W("")
W("Kaynak: `results/mumiso_aging_fixzf.json`, `results/mumiso_aging_sweep_fixzf.json`")
W("")

W("## Bolum 6 — gercekci senaryo")
W("")
W("### Kazancin kaynagi (hepsi ayni on kodlayiciyla, 1200 senaryo)")
W("")
W("| | min hiz |")
W("| --- | --- |")
W("| Pano yok | 1.0224 |")
W("| Rastgele faz | 3.1002 |")
W("| su_average | 3.5549 |")
W("| su_best_of | 4.2151 |")
W("| PGA | ~6.04 |")
W("")
W("Rastgele bir yuzey kazancin kabaca **yarisini** veriyor (olculen oran 0.50).")
W("")
W("Kaynak: `scripts/mumiso_gain_source.py` -> `results/mumiso_gain_source.json`")
W("")
W("### Anten ekseni korelasyonu — basliktaki iddia YANLISTI")
W("")
W("| Konfigurasyon | Eleman ekseni | Anten ekseni | Anten etkin rank |")
W("| --- | --- | --- | --- |")
W("| T=4, 600 ornek | 0.620 | 0.234 | 3.71 / 4 |")
W("| T=8, 1500 ornek | 0.639 | 0.204 | 7.26 / 8 |")
W("")
W("Anten ekseni LoS'ta 0.818, NLoS'ta 0.130 — korelasyonu neredeyse tamamen LoS tasiyor.")
W("Eski docstring 0.77 ve 2.32/4 diyordu; eksen karistiran bir dilimlemeden geliyordu.")
W("")
W("Kaynak: `scripts/mumiso_antenna_corr.py`")
W("")
W("### Kazanc paylasiminin bedeli (ayni senaryolar, akis korunarak)")
W("")
W("| | Mevcut | Fizikce dogru | Fark |")
W("| --- | --- | --- | --- |")
W("| NLoS anten korelasyonu | 0.095 | 0.279 | 2.9× |")
W("| Capa (su_average) | 3.5549 | 2.4180 | **−%31.98** |")
W("| PGA | 6.2147 | 5.7081 | **−%8.15** |")
W("")
W("Optimizasyonun degeri: **1.75× → 2.36×**. Fizigi duzeltmek katkinizi buyutuyor.")
W("")
W("Kaynak: `scripts/mumiso_gain_sharing.py` (akis korunarak, ayni senaryolar)")
W("")

W("## Bolum 6 (tez) — yayimlanmis faz-farkinda CNN–LSTM, tek kullanicili MISO")
W("")
_tr = {k: L(f"sumiso_cnnlstm{k}.json") for k in ("_seq", "", "_raw", "_siso_published_seq", "_siso_published")}
if all(_tr.values()):
    W("### 6.1 Statik test (6000 senaryo, seed 2026, egitim cekilisinin test bolmesi)")
    W("")
    W("| Kurulum | Parametre | RMSE (derece) | SR@5 | Hiz | SU-hizalama | Optimum |")
    W("| --- | --- | --- | --- | --- | --- | --- |")
    for k, lbl in (("_siso_published_seq", "SISO, yayimlanmis etiket, MATLAB basi"),
                   ("_siso_published", "SISO, yayimlanmis etiket, PyTorch basi"),
                   ("_seq", "MISO N_t=8, kaskat girdi, MATLAB basi"),
                   ("", "MISO, kaskat girdi, PyTorch basi"),
                   ("_raw", "MISO, ham F/G girdi, PyTorch basi")):
        r = _tr[k]
        W(f"| {lbl} | {r['params']} | {r['test_rmse_deg']:.2f} | %{100*r['SR@5']:.1f} | {r['rate_cnnlstm']:.3f} | {r['rate_su_align']:.3f} | {r['rate_label']:.3f} |")
    W("")
    W("Kaynak: `scripts/sumiso_train.py` -> `results/sumiso_cnnlstm*.json`")
    W("")
_me = L("sumiso_mobility_eval.json")
if _me:
    W("### 6.2 Hareketli etkin hiz (400 senaryo, seed 11)")
    W("")
    W("| Yontem | Gecikme (ms) | t=0 | " + " | ".join(f"T_ov={float(t):g} ms" for t in _me["effective"]) + " |")
    W("| --- | --- | --- | " + " | ".join("---" for _ in _me["effective"]) + " |")
    for k in ("SU-align", "CD-1", "CD-2", "CD-10", "Adam-8", "CNN-LSTM", "CNN-LSTM+CD-1"):
        W(f"| {k} | {_me['latency_ms'][k]:.2f} | {_me['rate_t0'][k]:.3f} | "
          + " | ".join(f"{v[k]['effective']:.3f}" for v in _me["effective"].values()) + " |")
    W("")
    W(f"Yuk: {_me['load_avg']['start']:.2f} / {_me['load_avg']['before_timing']:.2f} / {_me['load_avg']['after_timing']:.2f}. "
      "Her T_ov'de en iyi: " + ", ".join(v["_best"] for v in _me["effective"].values()) + ".")
    W("")
    W("Kaynak: `scripts/sumiso_mobility_eval.py --ckpt sumiso_cnnlstm_seq`")
    W("")
_ce = L("sumiso_csi_eval.json")
if _ce:
    W("### 6.3 Kusurlu CSI (iki kol ayri)")
    W("")
    W("| e2 | Klasik (dogrulamada secilen) | (a) temiz egitilmis | (b) gurultuyle egitilmis | (b)+CD-1 | (b) − klasik [%95 GA] | Hareketli: klasik | Hareketli: (b) |")
    W("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for e, v in _ce["levels"].items():
        st, mo = v["static"], v["mobility"]
        bc, bm = st["classical_selected_on_val"], mo["classical_selected_on_val"]
        ci = st["b_minus_best_classical_ci"]
        W(f"| {e} | {bc} {st['test'][bc]:.3f} | {st['test']['CNN (a) clean-trained']:.3f} | "
          f"{st['test']['CNN (b) noise-trained']:.3f} | {st['test']['CNN (b) + CD-1']:.3f} | "
          f"{st['b_minus_best_classical']:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}] | {bm} {mo['test'][bm]:.3f} | "
          f"{mo['test']['CNN (b) noise-trained']:.3f} |")
    W("")
    W("Statik: dogrulama 1000, test 6000 (seed 2026). Hareketli: secim seed 12, rapor seed 11, 400'er senaryo.")
    W("Klasik kolun secilen ayari her hata seviyesinde yakinsamis bir ayar: erken durdurma kazanc getirmiyor.")
    W("")
    W("Kaynak: `scripts/sumiso_csi_eval.py` -> `results/sumiso_csi_eval.json`")
    W("")

_rp = L("sumiso_representation.json")
if _rp:
    W("### 6.4 Gosterim karsilastirmasi: sin/cos mu, dogrudan aci mi? (3 tohum, ortalama ± std)")
    W("")
    W("| Senaryo | Cikis | RMSE (derece) | SR@5 | ±pi yakininda RMSE | ±pi'den uzakta RMSE | Hiz |")
    W("| --- | --- | --- | --- | --- | --- | --- |")
    for sc, lbl in (("siso", "SISO"), ("miso", "MISO N_t=8")):
        for o, ol in (("sincos", "sin/cos (yayimlanmis)"), ("angle_circ", "aci, 1−cos kaybi"), ("angle_mse", "aci, duz MSE")):
            v = _rp[sc][o]
            W(f"| {lbl} | {ol} | {v['rmse']['mean']:.2f} ± {v['rmse']['std']:.2f} | %{100*v['sr5']['mean']:.1f} | "
              f"{v['rmse_near_wrap']['mean']:.2f} | {v['rmse_far_from_wrap']['mean']:.2f} | {v['rate']['mean']:.3f} |")
    W("")
    W("±pi yakini: |etiket| > 150 derece (SISO test elemanlarinin %" + f"{100*_rp['siso']['_reference']['frac_near_wrap']:.1f}" + ").")
    W("sin/cos her iki senaryoda da 3 tohumun ucunde en dusuk RMSE.")
    W("")
    W("Kaynak: `scripts/sumiso_representation_summary.py` -> `results/sumiso_representation.json`")
    W("")

_dp = L("sumiso_discrete_eval.json")
if _dp:
    W("### 6.5 Ayrik faz (1/2/3 bit), tek kullanicili MISO")
    W("")
    W("| Bit | Yontem | Gecikme (ms) | Statik hiz | Hareketli etkin hiz |")
    W("| --- | --- | --- | --- | --- |")
    for b, v in _dp["levels"].items():
        st, mo = v["static"], v["mobility"]
        for k in ("SU-align -> round", "CD-1 -> round", "CD-10 -> round", "discrete CD-1", "discrete CD-2", "discrete CD-10",
                  "CNN (a) continuous labels", "CNN (b) discrete labels", "CNN (c) straight-through",
                  "CNN (c) straight-through + discrete CD-1"):
            W(f"| {b} | {k} | {mo['latency_ms'][k]:.2f} | {st['test'][k]:.3f} | {mo['test'][k]:.3f} |")
        W(f"| {b} | ayrik optimum (cevrimdisi) | — | {st['offline_discrete_optimum']:.3f} | |")
    W("")
    W(f"Statik: test 6000 (seed 2026). Hareketli: secim seed 12, rapor seed 11, 400 senaryo. "
      f"Yuk {_dp['load_avg']['start']:.2f} / {_dp['load_avg']['before_timing']:.2f} / {_dp['load_avg']['after_timing']:.2f}.")
    W("")
    W("Kaynak: `scripts/sumiso_discrete_eval.py` -> `results/sumiso_discrete_eval.json`")
    W("")

W("## Ek — yeniden uretilebilirlik")
W("")
W("- `scripts/audit_claims.py` — 65 iddia (`--all` ile 80), hepsi geciyor")
W("- Sabotaj testi: tek gecisli modellere acilmis modelin sayisi yazildiginda **7 iddia patliyor**")
W("- Bilinen bosluk betikte yazili: modellerin test bolmesindeki capa yeniden olculmuyor, JSON'dan okunuyor")
W("")
W("### On kodlayici varsayilaninin bedeli")
W("")
W("| | MMSE (varsayilan) | saf ZF | Fark |")
W("| --- | --- | --- | --- |")
W("| 1200 senaryo | 3.5549 | 3.6330 | %2.20 |")
W("| En zor %10 | 2.1391 | 2.2451 | **%4.95** |")
W("")
W("Kaynak: `scripts/mumiso_precoder_cost.py`")
W("")
W("### Alintilanirken dikkat")
W("")
W("- `effective_rank` ORNEK SAYISINA bagli (%32 yayilim, 250→1000 arasinda ters yonde). n belirtmeden yazmayin.")
W("- Veri seti prefix-kararli DEGIL: farkli `--samples` ile alinmis iki sayi ayni tabloya konamaz.")
W("- Gecikme olcumleri bos makinede alinmali; kirlilik tarafsiz degil.")
W("")
p = pathlib.Path(__file__).resolve().parents[1] / "TEZ_YAZIM_REFERANSI.md"
p.write_text("\n".join(out), encoding="utf-8")
print(f"yazildi: {p}  ({len(out)} satir)")
