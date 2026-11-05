# Tez Yazim Referansi — olculmus her sayi, kaynagiyla

Bu dosya `results/*.json` icinden **uretildi**, elle yazilmadi.
Her tablonun altinda hangi dosyadan geldigi yazili.

> Bir sayiyi teze koymadan once kaynak dosyasini acin. Bu dosya
> kolaylik icindir, otorite degil.

## Bolum 4 — cok kullanicili ogrenmenin sinirlari

### 4.1 Tek gecisli tahmin capada donuyor

Capa (`su_average`, modellerin puanlandigi **ayni** 1800 senaryoluk test bolmesi): **3.5363**  
`su_best_of` (bedava, K+1 adayin en iyisi): **4.1730**  
`su_weakest`: 3.6919

Hedef (en guclu klasik, olcumle secildi): **pga = 6.0783**

| Mimari | Test min hiz | Capa orani | Permutasyon yayilimi | Parametre |
| --- | --- | --- | --- | --- |
| concat | 3.5368 | 1.0001 | 1.17e-03 | 285,058 |
| deepsets | 3.5367 | 1.0001 | 5.93e-06 | 263,746 |
| exchange | 3.5260 | 0.9971 | 9.83e-07 | 272,066 |

Kaynak: `results/mumiso_sec4_fixzf.json`, capa `results/anchor_full_test.json`

Egitilmemis ag ile su_average, 400 senaryoda dort ondaliga kadar ayni: **3.7230 / 3.7230**.  
Artik kafasinin baslangic sapmasi: 0.013 derece.  
En iyi epok (12 epoktan): concat **4**, deepsets **9**, exchange **2**.

### 4.2 Nedeni: belirlenmis ama duzgun olmayan fonksiyon

| Olcum | Deger |
| --- | --- |
| Ayni senaryo, iki farkli baslangic — cos uyusmasi | +0.58 / +0.81 / +0.57 |
| Farkli senaryolar — cos uyusmasi | +0.005 / +0.009 / −0.003 |
| Oracle hizi (Adam, 600 adim) | 6.1619 |
| Capa (bu tanida) | 3.4350 |
| Gozetimli uyum, egitim MSE (son epok) | 0.8958 |
| Gozetimli uyum, dogrulama MSE | 0.9250 |
| Gozetimli modelin test hizi | 3.4064 (capanin ALTINDA) |

Kaynak: `results/learnability_fixzf.log`, `scripts/diagnose_learnability.py`

Komsuluk testi: en yakin oznitelik komsusuna **+0.0047**, rastgele senaryoya **+0.0089**.
Ikisi de sifirdan ayirt edilemez; aralarindaki sira gurultudur.

### 4.3 Temsil hipotezi kuruldu ve REDDEDILDI

Hipotez: `features.py` normalizasyonu RIS kaskadi / dogrudan yol guc oranini siliyor.

| | gercek | agin gordugu |
| --- | --- | --- |
| Oranin senaryolar arasi yayilimi | 9.4 milyon kat | 1.000 kat |
| Gercek oranla korelasyon | — | +0.031 |

Bilgi geri verildi (iki kanal, `features.link_ratio=True`), yeni korelasyon **+1.0000**.
Ayni kanal cekilisi, ayni epok sayisi, tek fark iki kanal:

| Mimari | Oran kanali YOK | Oran kanali VAR | Degisim |
| --- | --- | --- | --- |
| concat | 3.5368 | 3.4770 | -1.69% |
| deepsets | 3.5367 | 3.4233 | -3.21% |
| exchange | 3.5260 | 3.4459 | -2.27% |

Kaynak: `results/mumiso_sec4_fixzf.json` ve `results/mumiso_linkratio.json`

**Sonuc:** eksik bilgi, stall'in sebebi degildi. Uc model de biraz kotulesti.
Dusus iki modelde kendi epok-arasi gurultusunun disinda (deepsets gurultu %0.29,
exchange %0.13).

### 4.4 Ogrenilen guncelleme kurali

| Gradyan girdi | Test min | Capaya gore | AO orani | Parametre |
| --- | --- | --- | --- | --- |
| **var** | 5.6359 | +57.6% | 0.880 | 272,842 |
| **yok** | 3.6160 | +1.1% | 0.565 | 272,650 |

Capa (her iki kol) 3.5758 · cd 6.1180 · AO 6.4020

Adim izi (gradyan var): 4.451 → 4.611 → 4.905 → 5.092 → 4.599 → 5.343 → 5.251 → 5.636
Adim izi (gradyan yok): 3.578 → 3.577 → 3.571 → 3.563 → 3.574 → 3.595 → 3.611 → 3.616

Ogrenilen adim boylari: var 0.589 → 0.258 (azalan cizelge) · yok hepsi ~0.49 (duz)

Kaynak: `results/mumiso_unrolled_fixzf.json`, `results/mumiso_nograd_fixzf.json`

### 4.5 Esit adim vs esit milisaniye — ikisi CELISIYOR

Capa 3.5386 · `su_best_of` 4.2371

**Esit ADIM** — ogrenilen kural her butcede onde:

| L | Ogrenilen | Ayarlanmis Adam | Oran | Eslest. fark − 2 s.e. | Kazanma orani |
| --- | --- | --- | --- | --- | --- |
| 1 | 4.4599 | 4.3810 | 1.018 | +0.0608 | 74.8% |
| 2 | 4.8792 | 4.6927 | 1.040 | +0.1602 | 83.2% |
| 4 | 5.2855 | 5.0253 | 1.052 | +0.2279 | 83.7% |
| 8 | 5.5932 | 5.3800 | 1.040 | +0.1840 | 83.2% |
| 16 | 5.8003 | 5.7389 | 1.011 | +0.0393 | 68.3% |

Adim boyu her butcede dogrulamada secildi; optimum her L'de **0.75**, onlu izgaranin
yedinci konumu — yani kenarda degil, ic noktada. Yumusak/sert objektif farki 0.008–0.018.

Kaynak: `results/mumiso_equal_step.json`

**Esit MILISANIYE** — bes noktanin besi de baskinlanmis, bes turun besinde:

| Ogrenilen L | Gecikme | Hiz | Baskinlayan Adam |
| --- | --- | --- | --- |
| 1 | 5.16 ms | 4.4599 | L=2: 3.20 ms, 4.6927 |
| 2 | 12.95 ms | 4.8792 | L=4: 6.49 ms, 5.0253 |
| 4 | 18.41 ms | 5.2855 | L=8: 13.48 ms, 5.3800 |
| 8 | 36.76 ms | 5.5932 | L=16: 27.31 ms, 5.7389 |
| 16 | 83.80 ms | 5.8003 | L=48: 78.77 ms, 6.1072 |

Adim maliyeti orani: ~2.7× (bir ogrenilen adim = ~2.7 Adam adimi).
Turlar arasi zamanlama oynamasi 1.06×–1.41× (bos makine, 5 tur).

Kaynak: `results/mumiso_latency_parity.json`, `results/mumiso_latency_repeat.json`

## Bolum 5 — hareketlilik ve gecikme-farkinda tasarim

Tutarlilik suresi: 3 GHz, 1.5 m/s → f_d = 15.0 Hz → **T_c = 28.2 ms**

| L | Gecikme | t=0 hizi | **Gecerli hiz** |
| --- | --- | --- | --- |

Elle dogrulanmis ana satirlar (bolum 5b taslagindan):

| Yontem | t=0 hizi | Gecikme | Gecerli hiz |
| --- | --- | --- | --- |
| su_average | 4.624 | ~0 | 4.624 |
| su_best_of | 5.276 | 0.05 ms | 5.276 |
| Adam-8 | — | 13.3 ms | **5.849** |
| Adam-16 | — | 26.6 ms | 5.324 |
| koordinat inisi | — | ~1500 ms | 4.921 |
| PGA | **7.117** | ~5600 ms | **4.667** |

Icsel optimum: **L = 4** → 5.982. Yakinsamaya gore tasarlamak (L=48) **%14** kaybettiriyor.
Eskimis faz tabani ~4.35 (sifira cokmuyor).

### Yuk tasiyan varsayim: huzme taze, faz eskimis

> **DUZELTME (27 Ekim).** Bu sayi uzun sure "17 kat (4.718 / 0.279)" diye
> alintilandi. O olcum betige yazilmamisti ve **yeniden uretilemiyor**.
> `scripts/mumiso_beam_staleness.py` ile olculdugunde hicbir faz secimi
> 17 kat vermiyor. Nitel iddia -- bir buyukluk mertebesi -- saglam;
> sayinin kendisi yanlisti.

28.2 ms'de (tutarlilik suresi), faz t=0'da secilip huzme ya taze ya eskimis:

| Faz secimi | Taze huzme | Eskimis huzme | Oran |
| --- | --- | --- | --- |
| su_average | 3.5862 | 0.3060 | **11.7x** |
| su_best_of | 3.9243 | 0.3052 | **12.9x** |
| adam8 | 4.3584 | 0.3066 | **14.2x** |

Kaynak: `scripts/mumiso_beam_staleness.py`, `results/mumiso_beam_staleness*.json`

Eskimis deger her uc faz seciminde de ~0.305; taze deger 3.59-4.36.
Teze **11.7-14.2 kat** yazin, 17 degil.

Modelin gecerlilik ufku: korelasyon tabani ~0.5 (bagimsiz cekiliste 0.10);
sacici sayisi 6→60 tabani yalnizca 0.60→0.51 indiriyor. Guvenilir aralik **τ ≤ 200 ms**.

Kaynak: `results/mumiso_aging_fixzf.json`, `results/mumiso_aging_sweep_fixzf.json`

## Bolum 6 — gercekci senaryo

### Kazancin kaynagi (hepsi ayni on kodlayiciyla, 1200 senaryo)

| | min hiz |
| --- | --- |
| Pano yok | 1.0224 |
| Rastgele faz | 3.1002 |
| su_average | 3.5549 |
| su_best_of | 4.2151 |
| PGA | ~6.04 |

Rastgele bir yuzey kazancin kabaca **yarisini** veriyor (olculen oran 0.50).

Kaynak: `scripts/mumiso_gain_source.py` -> `results/mumiso_gain_source.json`

### Anten ekseni korelasyonu — basliktaki iddia YANLISTI

| Konfigurasyon | Eleman ekseni | Anten ekseni | Anten etkin rank |
| --- | --- | --- | --- |
| T=4, 600 ornek | 0.620 | 0.234 | 3.71 / 4 |
| T=8, 1500 ornek | 0.639 | 0.204 | 7.26 / 8 |

Anten ekseni LoS'ta 0.818, NLoS'ta 0.130 — korelasyonu neredeyse tamamen LoS tasiyor.
Eski docstring 0.77 ve 2.32/4 diyordu; eksen karistiran bir dilimlemeden geliyordu.

Kaynak: `scripts/mumiso_antenna_corr.py`

### Kazanc paylasiminin bedeli (ayni senaryolar, akis korunarak)

| | Mevcut | Fizikce dogru | Fark |
| --- | --- | --- | --- |
| NLoS anten korelasyonu | 0.095 | 0.279 | 2.9× |
| Capa (su_average) | 3.5549 | 2.4180 | **−%31.98** |
| PGA | 6.2147 | 5.7081 | **−%8.15** |

Optimizasyonun degeri: **1.75× → 2.36×**. Fizigi duzeltmek katkinizi buyutuyor.

Kaynak: `scripts/mumiso_gain_sharing.py` (akis korunarak, ayni senaryolar)

## Bolum 6 (tez) — yayimlanmis faz-farkinda CNN–LSTM, tek kullanicili MISO

### 6.1 Statik test (6000 senaryo, seed 2026, egitim cekilisinin test bolmesi)

| Kurulum | Parametre | RMSE (derece) | SR@5 | Hiz | SU-hizalama | Optimum |
| --- | --- | --- | --- | --- | --- | --- |
| SISO, yayimlanmis etiket, MATLAB basi | 162562 | 14.99 | %72.1 | 10.334 | 10.349 | 10.349 |
| SISO, yayimlanmis etiket, PyTorch basi | 822976 | 30.74 | %24.3 | 10.142 | 10.349 | 10.349 |
| MISO N_t=8, kaskat girdi, MATLAB basi | 167938 | 61.32 | %24.9 | 12.490 | 12.431 | 12.893 |
| MISO, kaskat girdi, PyTorch basi | 828352 | 66.45 | %14.3 | 12.241 | 12.431 | 12.893 |
| MISO, ham F/G girdi, PyTorch basi | 828736 | 83.84 | %10.2 | 11.201 | 12.431 | 12.893 |

Kaynak: `scripts/sumiso_train.py` -> `results/sumiso_cnnlstm*.json`

### 6.2 Hareketli etkin hiz (400 senaryo, seed 11)

| Yontem | Gecikme (ms) | t=0 | T_ov=0 ms | T_ov=1.71 ms | T_ov=3.43 ms | T_ov=10 ms |
| --- | --- | --- | --- | --- | --- | --- |
| SU-align | 0.04 | 12.389 | 12.389 | 12.385 | 12.369 | 12.249 |
| CD-1 | 2.48 | 12.709 | 12.698 | 12.681 | 12.656 | 12.491 |
| CD-2 | 4.76 | 12.736 | 12.701 | 12.673 | 12.638 | 12.441 |
| CD-10 | 23.06 | 12.742 | 12.152 | 12.099 | 12.047 | 11.984 |
| Adam-1 | 0.59 | 12.499 | 12.498 | 12.490 | 12.472 | 12.339 |
| Adam-8 | 3.89 | 12.690 | 12.664 | 12.642 | 12.611 | 12.427 |
| CNN-LSTM | 1.12 | 12.355 | 12.354 | 12.342 | 12.326 | 12.193 |
| CNN-LSTM+CD-1 | 4.26 | 12.700 | 12.671 | 12.646 | 12.614 | 12.424 |

Yuk: 0.01 / 0.16 / 0.97. Her T_ov'de en iyi: CD-1, CD-1, CD-1, CD-1.

En iyi yontem ayri bir cekiliste (seed 12) secildi. t=0'da eslestirilmis farklar (ortalama [%95 GA]):

- CNN-LSTM - SU-align: -0.034 [-0.094, +0.026]
- CNN-LSTM - Adam-1: -0.143 [-0.197, -0.089]
- CNN-LSTM+CD-1 - CD-1: -0.009 [-0.021, +0.004]
- 6000 senaryo, seed 11: CNN − SU-align +0.059 [+0.041, +0.077], CNN − Adam-1 -0.090 [-0.106, -0.074]
- 6000 senaryo, seed 13: CNN − SU-align +0.040 [+0.023, +0.059], CNN − Adam-1 -0.104 [-0.120, -0.088]

**Dikkat:** CNN'in kapalı formun ALTINDA oldugu YAZILMAMALI (400'de anlamsiz, 6000'de hafif USTUNDE). Dogru ifade: tek, daha hizli bir Adam adimi CNN'i baskinliyor.

Kaynak: `scripts/sumiso_mobility_eval.py` (varsayilan `--ckpt sumiso_cnnlstm_seq`), `scripts/sumiso_t0_robustness.py`

### 6.3 Kusurlu CSI (iki kol ayri)

| e2 | Klasik (dogrulamada secilen) | (a) temiz egitilmis | (b) gurultuyle egitilmis | (b)+CD-1 | (b) − klasik [%95 GA] | Hareketli: klasik | Hareketli: (b) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | Adam-64 12.892 | 12.490 | 12.490 | 12.855 | -0.402 [-0.415, -0.390] | CD-1 12.698 | 12.354 |
| 0.01 | Adam-64 12.886 | 12.475 | 12.469 | 12.849 | -0.417 [-0.430, -0.404] | CD-1 12.691 | 12.331 |
| 0.03 | Adam-64 12.876 | 12.447 | 12.437 | 12.837 | -0.439 [-0.453, -0.425] | CD-1 12.674 | 12.296 |
| 0.1 | CD-30 12.833 | 12.345 | 12.334 | 12.790 | -0.500 [-0.516, -0.484] | CD-2 12.639 | 12.188 |
| 0.3 | Adam-64 12.675 | 12.017 | 12.026 | 12.612 | -0.649 [-0.669, -0.628] | CD-2 12.463 | 11.885 |

Statik: dogrulama 1000, test 6000 (seed 2026). Hareketli: secim seed 12, rapor seed 11, 400'er senaryo.
Klasik kolun secilen ayari her hata seviyesinde yakinsamis bir ayar: erken durdurma kazanc getirmiyor.

Kaynak: `scripts/sumiso_csi_eval.py` -> `results/sumiso_csi_eval.json`

### 6.4 Gosterim karsilastirmasi: sin/cos mu, dogrudan aci mi? (3 tohum, ortalama ± std)

| Senaryo | Cikis | RMSE (derece) | SR@5 | ±pi yakininda RMSE | ±pi'den uzakta RMSE | Hiz |
| --- | --- | --- | --- | --- | --- | --- |
| SISO | sin/cos (yayimlanmis) | 14.63 ± 0.38 | %72.7 | 16.00 | 13.46 | 10.334 |
| SISO | aci, 1−cos kaybi | 21.35 ± 0.30 | %61.6 | 28.82 | 18.41 | 10.310 |
| SISO | aci, duz MSE | 30.33 ± 0.02 | %56.2 | 62.65 | 12.37 | 10.239 |
| MISO N_t=8 | sin/cos (yayimlanmis) | 61.49 ± 0.10 | %25.2 | 64.92 | 59.22 | 12.486 |
| MISO N_t=8 | aci, 1−cos kaybi | 63.67 ± 0.26 | %20.5 | 64.91 | 62.62 | 12.426 |
| MISO N_t=8 | aci, duz MSE | 73.76 ± 0.17 | %20.7 | 122.68 | 38.52 | 11.775 |

±pi yakini: |etiket| > 150 derece (SISO test elemanlarinin %16.7).
sin/cos her iki senaryoda da 3 tohumun ucunde en dusuk RMSE.

Kaynak: `scripts/sumiso_representation_summary.py` -> `results/sumiso_representation.json`

### 6.5 Ayrik faz (1/2/3 bit), tek kullanicili MISO

| Bit | Yontem | Gecikme (ms) | Statik hiz | Hareketli etkin hiz |
| --- | --- | --- | --- | --- |
| 1 | SU-align -> round | 0.05 | 11.547 | 11.523 |
| 1 | CD-1 -> round | 2.38 | 11.894 | 11.776 |
| 1 | CD-10 -> round | 22.54 | 11.922 | 11.285 |
| 1 | discrete CD-1 | 2.83 | 11.998 | 11.872 |
| 1 | discrete CD-2 | 5.56 | 12.053 | 11.894 |
| 1 | discrete CD-10 | 26.80 | 12.074 | 11.334 |
| 1 | CNN (a) continuous labels | 1.69 | 11.718 | 11.634 |
| 1 | CNN (b) discrete labels | 1.69 | 11.589 | 11.484 |
| 1 | CNN (c) straight-through | 1.69 | 11.589 | 11.484 |
| 1 | CNN (c) straight-through + discrete CD-1 | 5.01 | 11.997 | 11.849 |
| 1 | ayrik optimum (cevrimdisi) | — | 12.084 | |
| 2 | SU-align -> round | 0.05 | 12.209 | 12.178 |
| 2 | CD-1 -> round | 2.35 | 12.620 | 12.477 |
| 2 | CD-10 -> round | 22.30 | 12.653 | 11.979 |
| 2 | discrete CD-1 | 2.80 | 12.633 | 12.478 |
| 2 | discrete CD-2 | 5.53 | 12.668 | 12.483 |
| 2 | discrete CD-10 | 27.12 | 12.681 | 11.867 |
| 2 | CNN (a) continuous labels | 2.08 | 12.306 | 12.177 |
| 2 | CNN (b) discrete labels | 2.08 | 12.295 | 12.148 |
| 2 | CNN (c) straight-through | 2.08 | 12.311 | 12.166 |
| 2 | CNN (c) straight-through + discrete CD-1 | 5.38 | 12.640 | 12.452 |
| 2 | ayrik optimum (cevrimdisi) | — | 12.688 | |
| 3 | SU-align -> round | 0.05 | 12.377 | 12.335 |
| 3 | CD-1 -> round | 2.33 | 12.799 | 12.643 |
| 3 | CD-10 -> round | 22.13 | 12.833 | 12.129 |
| 3 | discrete CD-1 | 2.79 | 12.802 | 12.642 |
| 3 | discrete CD-2 | 5.50 | 12.830 | 12.637 |
| 3 | discrete CD-10 | 26.85 | 12.839 | 12.000 |
| 3 | CNN (a) continuous labels | 2.52 | 12.453 | 12.307 |
| 3 | CNN (b) discrete labels | 2.52 | 12.446 | 12.299 |
| 3 | CNN (c) straight-through | 2.52 | 12.460 | 12.318 |
| 3 | CNN (c) straight-through + discrete CD-1 | 5.81 | 12.801 | 12.597 |
| 3 | ayrik optimum (cevrimdisi) | — | 12.842 | |

Statik: test 6000 (seed 2026). Hareketli: secim seed 12, rapor seed 11, 400 senaryo. Yuk 0.98 / 0.43 / 1.00.

Not: 1 bitte straight-through ince ayar dogrulamada iyilestirme bulmadi; (c) satirlari (b) ile ayni model. Baskinlik listeleri ortalamaya dayali; 'kapali form + yuvarlama ag'i baskinliyor' farklari gurultu icinde, guclu iddia olarak yazmayin. 1 bitte surekli egitilmis CNN (a) baskinlanmiyor ama secilen klasigin altinda (GA sifiri disliyor).

Kaynak: `scripts/sumiso_discrete_eval.py` -> `results/sumiso_discrete_eval.json`

## Ek — yeniden uretilebilirlik

- `scripts/audit_claims.py` — 70 iddia (`--all` ile 85), hepsi geciyor
- Sabotaj testi: tek gecisli modellere acilmis modelin sayisi yazildiginda **7 iddia patliyor**
- Bilinen bosluk betikte yazili: modellerin test bolmesindeki capa yeniden olculmuyor, JSON'dan okunuyor

### On kodlayici varsayilaninin bedeli

| | MMSE (varsayilan) | saf ZF | Fark |
| --- | --- | --- | --- |
| 1200 senaryo | 3.5549 | 3.6330 | %2.20 |
| En zor %10 | 2.1391 | 2.2451 | **%4.95** |

Kaynak: `scripts/mumiso_precoder_cost.py`

### Alintilanirken dikkat

- `effective_rank` ORNEK SAYISINA bagli (%32 yayilim, 250→1000 arasinda ters yonde). n belirtmeden yazmayin.
- Veri seti prefix-kararli DEGIL: farkli `--samples` ile alinmis iki sayi ayni tabloya konamaz.
- Gecikme olcumleri bos makinede alinmali; kirlilik tarafsiz degil.
