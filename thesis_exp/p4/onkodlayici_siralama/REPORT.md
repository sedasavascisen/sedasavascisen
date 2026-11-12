# Deney 4.3 devamı — Pilot ücreti altında bütün kolların sıralaması (rapor)

Commit `f413f63` (ölçüm commit'i `a0ac494`). Model Deney 4.3 ile aynı: ZF her R ms'de bir kusursuz etkin kanal kestiriminden tazeleniyor, tazeleme başına 4 pilot sembolü veri oranı 1 − t_p/R ile ücretlendiriliyor, faz t=0 kanalından ve kolun gecikmesinde devreye giriyor, hız [gecikme, gecikme + 50 ms] üzerinde ortalanıyor. Tazeleme periyodu R her kol ve numeroloji için doğrulama çekilişinde (seed 12) seçildi; en iyi kol da orada seçildi; rapor yaşlanma kümesi (seed 11, 400 senaryo). Eşli bootstrap 2000, %95 GA. Gecikmeler tek iş parçacıklı yeniden ölçümden (thesis_exp/infra).

## 1) Özet: seçilen kol

| Ücretlendirme | Doğrulamada seçilen | Testte hızı | SU-best-of | Fark [%95 GA] |
| --- | --- | --- | --- | --- |
| yok (makalenin varsayımı, taze W) | Adam-8 | 5.2133 | 4.9108 | +0.3025 [+0.242, +0.366] |
| 15kHz | Adam-6 (R = 2 ms) | 3.5385 | 3.3852 | +0.1534 [+0.101, +0.204] |
| 30kHz | Adam-8 (R = 1 ms) | 4.0034 | 3.8108 | +0.1927 [+0.141, +0.245] |
| 60kHz | Adam-8 (R = 1 ms) | 4.3341 | 4.1255 | +0.2086 [+0.153, +0.262] |

## 2) Bütün kollar (test, b/s/Hz)

| Kol | Gecikme (ms) | Taze W | 15kHz: hız (R) | 15kHz: − seçilen [%95 GA] | 30kHz: hız (R) | 30kHz: − seçilen [%95 GA] | 60kHz: hız (R) | 60kHz: − seçilen [%95 GA] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SU-average | 0.30 | 4.5357 | 3.1465 (2) | -0.3920 [-0.453, -0.333] | 3.5348 (1) | -0.4686 [-0.535, -0.407] | 3.8268 (1) | -0.5073 [-0.580, -0.439] |
| Adam-1 | 1.33 | 4.9311 | 3.3833 (2) | -0.1553 [-0.205, -0.110] | 3.8147 (1) | -0.1887 [-0.239, -0.139] | 4.1298 (1) | -0.2043 [-0.260, -0.151] |
| SU-best-of | 1.63 | 4.9108 | 3.3852 (2) | -0.1534 [-0.204, -0.104] | 3.8108 (1) | -0.1927 [-0.244, -0.143] | 4.1255 (1) | -0.2086 [-0.260, -0.151] |
| Adam-2 | 2.74 | 5.1038 | 3.4846 (2) | -0.0539 [-0.091, -0.015] | 3.9397 (1) | -0.0637 [-0.107, -0.020] | 4.2652 (1) | -0.0689 [-0.116, -0.021] |
| Adam-3 | 4.14 | 5.1838 | 3.5205 (2) | -0.0180 [-0.052, +0.016] | 3.9890 (1) | -0.0144 [-0.053, +0.024] | 4.3185 (1) | -0.0156 [-0.055, +0.024] |
| Adam-4 | 5.55 | 5.2102 | 3.5236 (2) | -0.0150 [-0.038, +0.007] | 3.9995 (1) | -0.0039 [-0.035, +0.029] | 4.3299 (1) | -0.0042 [-0.039, +0.030] |
| Adam-5 | 6.82 | 5.2182 | 3.5337 (2) | -0.0048 [-0.018, +0.007] | 4.0079 (1) | +0.0045 [-0.023, +0.032] | 4.3390 (1) | +0.0049 [-0.023, +0.036] |
| Adam-6 | 8.09 | 5.2248 | 3.5385 (2) | +0.0000 [+0.000, +0.000] | 4.0132 (1) | +0.0098 [-0.011, +0.031] | 4.3447 (1) | +0.0106 [-0.009, +0.032] |
| Adam-8 | 10.63 | 5.2133 | 3.5286 (2) | -0.0099 [-0.031, +0.012] | 4.0034 (1) | +0.0000 [+0.000, +0.000] | 4.3341 (1) | +0.0000 [+0.000, +0.000] |
| Adam-10 | 13.30 | 5.1914 | 3.5178 (2) | -0.0207 [-0.050, +0.010] | 3.9892 (1) | -0.0142 [-0.031, +0.002] | 4.3187 (1) | -0.0154 [-0.034, +0.002] |
| Adam-12 | 15.96 | 5.1855 | 3.5118 (2) | -0.0268 [-0.062, +0.007] | 3.9830 (1) | -0.0204 [-0.046, +0.004] | 4.3120 (1) | -0.0221 [-0.048, +0.005] |
| Adam-16 | 21.28 | 5.1737 | 3.5029 (2) | -0.0357 [-0.075, +0.005] | 3.9744 (1) | -0.0290 [-0.063, +0.004] | 4.3027 (1) | -0.0314 [-0.067, +0.005] |
| Adam-20 | 26.57 | 5.1779 | 3.4961 (2) | -0.0425 [-0.087, +0.003] | 3.9707 (1) | -0.0327 [-0.072, +0.006] | 4.2987 (1) | -0.0354 [-0.078, +0.006] |
| Adam-24 | 31.85 | 5.1852 | 3.4759 (2) | -0.0627 [-0.110, -0.015] | 3.9596 (1) | -0.0438 [-0.088, -0.003] | 4.2867 (1) | -0.0474 [-0.092, -0.002] |
| Adam-32 | 42.42 | 5.1654 | 3.4510 (2) | -0.0875 [-0.139, -0.036] | 3.9371 (1) | -0.0663 [-0.114, -0.019] | 4.2623 (1) | -0.0718 [-0.123, -0.021] |
| Adam-48 | 63.91 | 5.1361 | 3.4397 (2) | -0.0988 [-0.156, -0.045] | 3.9230 (1) | -0.0804 [-0.139, -0.024] | 4.2471 (1) | -0.0870 [-0.147, -0.026] |
| CD | 702.97 | 5.0112 | 3.3866 (2) | -0.1520 [-0.226, -0.082] | 3.8429 (1) | -0.1605 [-0.232, -0.092] | 4.1603 (1) | -0.1738 [-0.252, -0.100] |
| PGA | 4950.35 | 4.7066 | 3.1550 (2) | -0.3835 [-0.536, -0.241] | 3.5880 (1) | -0.4154 [-0.563, -0.265] | 3.8843 (1) | -0.4498 [-0.610, -0.290] |

## 3) Sıralama karşılaştırması (testteki ortalamaya göre, ilk 6)

| Sıra | Taze W | 15kHz | 30kHz | 60kHz |
| --- | --- | --- | --- | --- |
| 1 | Adam-6 | Adam-6 | Adam-6 | Adam-6 |
| 2 | Adam-5 | Adam-5 | Adam-5 | Adam-5 |
| 3 | Adam-8 | Adam-8 | Adam-8 | Adam-8 |
| 4 | Adam-4 | Adam-4 | Adam-4 | Adam-4 |
| 5 | Adam-10 | Adam-3 | Adam-10 | Adam-10 |
| 6 | Adam-12 | Adam-10 | Adam-3 | Adam-3 |

## 4) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| THREADS=2 python3 thesis_exp/p4/onkodlayici_siralama/run.py (35 dk) | kanal 12 (doğrulama) / 11 (test), bootstrap 0 | raw/results.json, raw/run.log; deneme: PROBE=1 → raw/probe_aligned.json (koşulmadı); raw/probe_v1_grid_bias.json yanlı ilk sürümün denemesi |

## 5) Yorum (bulgulardan ayrı)

- **En iyi kol kümesi pilot ücretinden etkilenmiyor.**
  - Nokta tahminleriyle ilk dört kol (Adam-6, 5, 8, 4) taze W'de ve üç numerolojinin hepsinde aynı sırada; ama aralarındaki farkların GA'sı sıfırı içeriyor, bu yüzden kesin olan sıra değil, en iyi kümenin (Adam-4…8) korunması. 5. ve 6. sıra numerolojiye göre değişiyor.
  - Doğrulamada seçilen kol Adam-6 ya da Adam-8. Seçilen kol ile Adam-4…Adam-8 arasındaki farkların GA'sı sıfırı içeriyor.
  - İçsel optimum (L ≈ 5–8) pilot ücretinde de korunuyor.
- **Ölçüt:** devreye girdikten sonraki 50 ms'nin zaman ortalaması (Tanım 1'in anlık etkin hızı değil). 50 ms'nin duyarlılığı denenmedi. Doğrulama çekilişinde (seed 12) senaryo kimliği ayrıca sınanmadı (denetim U11); test çekilişinde her ızgara için sınandı.
- **Mutlak hızlar düşüyor.** En iyi kol taze W'de 5.213 b/s/Hz. Pilot ücretiyle 3.539 (15 kHz), 4.003 (30 kHz) ve 4.334 (60 kHz). Kayıp sırasıyla %32, %23 ve %17.
- **SU-best-of'a karşı üstünlük küçülüyor ama anlamlı kalıyor.** Taze W'de +0.303 [+0.242, +0.366]. Pilot ücretiyle +0.153 [+0.101, +0.204], +0.193 [+0.141, +0.245] ve +0.209 [+0.153, +0.262].
- **Yavaş çözücüler yine en altta.** CD her numerolojide seçilen koldan 0.15–0.17, PGA 0.38–0.45 b/s/Hz geride. GA'ların hepsi sıfırın altında.
- **Yanlılık düzeltmesi.** İlk koşu tazeleme anlarını mutlak 0.1 ms ızgarasına yuvarlıyordu. Gecikmesi yukarı yuvarlanan kollar (Adam-6/10/12/16/20/24) yapay olarak öne geçti ve sıralama testere dişi biçimini aldı. Bu koşu kolun devreye girme anına hizalı ızgara kullanıyor. Yanlı çıktılar raw/*_v1_grid_bias.* adıyla saklandı.
  - Aynı yanlılık Deney 4.3'te de var; o raporun başına düzeltme notu eklendi.
  - Taze W sütunu bu düzeltmeden etkilenmiyor. Yalnızca örnekleme anları kaydı için 4.3 ile arasında ≤0.001 fark var.
- **Kapsam dışı kalanlar.** Kestirim kusursuz kabul edildi; pilot SNR'ı (Deney 4.4) ve tazeleme ile kestirimin birlikte etkisi modellenmedi. Pilot sayısı K = 4 (kullanıcı başına bir dik sembol).
