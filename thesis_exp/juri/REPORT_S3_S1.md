# Jüri soruları 3 ve 1 — ön kayıtlı sonuçlar

Rapor commit'i `1267d39`, kol koşusu `d75848d`. Ön kayıt `ON_KAYIT_S3_S1.md`. Sapma 1 (bütün gecikmeler bu oturumda yeniden ölçüldü) ve Sapma 2 (CD erken durmasız ölçüldü) uygulanmıştır. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1 (tam gecikmede, interpolasyonsuz). GA: eşli bootstrap 2000, %95.

## ⚠ En üstte: Makale 2'yi sınırlayan bulgu (Kural 10)

- **1.5 m/s: yalnızca CD derlenirse sıralama döner.** Yalnız derleme (aynı algoritma, ×63) 3.81 ms'de +0.514 [+0.477, +0.552]; derleme + rank-1 güncelleme (×206, algoritmik iyileştirme de içerir) 3.05 ms'de Python'daki Adam-6'yı +0.684 [+0.639, +0.728] geçiyor. Başa baş oranı r* ∈ (10, 15].
- **10 km/h: yalnızca CD derlenirse sıralama döner.** Yalnız derleme (aynı algoritma, ×62) 2.55 ms'de +0.602 [+0.559, +0.646]; derleme + rank-1 güncelleme (×183, algoritmik iyileştirme de içerir) 2.16 ms'de Python'daki Adam-4'yı +0.836 [+0.783, +0.887] geçiyor. Başa baş oranı r* ∈ (10, 15].
- Bu yüzden Makale 2'deki "speed beats precision" cümlesi bir gerçekleştirme varsayımına bağlıdır: CD'nin Python gerçekleştirmesi, makaledeki sıralamanın bir parçasıdır.
- **Ancak bütün kollar aynı oranda hızlandırıldığında** (ön kayıt dışı, §Soru 1b) ayarlı Adam, ayarlı CD'yi r = 1…1000 aralığının her noktasında anlamlı olarak geçiyor 1.5 m/s: CD − Adam -1.41 … -0.12, en kötü GA üst sınırı -0.098; 10 km/h: CD − Adam -1.43 … -0.13, en kötü GA üst sınırı -0.107.

## Soru 3 — Ryu tarzı uygulanabilirlik seçimi ile etkin hız seçimi

### 1.5 m/s — S3-H1 **TUTTU**

| bütçe (ms) | t = 0'a göre seçilen | etkin hıza göre seçilen | etkin hız (t = 0 seçimi) | etkin hız (bizim) | fark [GA] |
| --- | --- | --- | --- | --- | --- |
| 2 | Adam-1 | Adam-1 | 5.409 | 5.409 | +0.000 [+0.000, +0.000] |
| 5 | Adam-4 | Adam-4 | 6.059 | 6.059 | +0.000 [+0.000, +0.000] |
| 10 | Adam-8 | Adam-6 | 6.139 | 6.151 | -0.012 [-0.036, +0.014] |
| 20 | Adam-16 | Adam-6 | 5.720 | 6.151 | -0.431 [-0.494, -0.370] |
| 50 | Adam-32 | Adam-6 | 5.335 | 6.151 | -0.817 [-0.905, -0.728] |
| 100 | Adam-48 | Adam-6 | 5.239 | 6.151 | -0.912 [-1.009, -0.823] |
| 200 | Adam-48 | Adam-6 | 5.239 | 6.151 | -0.912 [-1.007, -0.823] |
| 1000 | Adam-48 | Adam-6 | 5.239 | 6.151 | -0.912 [-1.007, -0.816] |
| 6000 | Long-run Adam | Adam-6 | 4.737 | 6.151 | -1.414 [-1.563, -1.253] |

### 10 km/h — S3-H1 (raporlanır)

| bütçe (ms) | t = 0'a göre seçilen | etkin hıza göre seçilen | etkin hız (t = 0 seçimi) | etkin hız (bizim) | fark [GA] |
| --- | --- | --- | --- | --- | --- |
| 2 | Adam-1 | Adam-1 | 5.402 | 5.402 | +0.000 [+0.000, +0.000] |
| 5 | Adam-4 | Adam-4 | 5.913 | 5.913 | +0.000 [+0.000, +0.000] |
| 10 | Adam-8 | Adam-4 | 5.651 | 5.913 | -0.262 [-0.320, -0.210] |
| 20 | Adam-16 | Adam-4 | 5.238 | 5.913 | -0.675 [-0.757, -0.591] |
| 50 | Adam-32 | Adam-4 | 5.153 | 5.913 | -0.760 [-0.852, -0.673] |
| 100 | Adam-48 | Adam-4 | 5.116 | 5.913 | -0.797 [-0.900, -0.704] |
| 200 | Adam-48 | Adam-4 | 5.116 | 5.913 | -0.797 [-0.888, -0.701] |
| 1000 | Adam-48 | Adam-4 | 5.116 | 5.913 | -0.797 [-0.897, -0.707] |
| 6000 | Long-run Adam | Adam-4 | 4.680 | 5.913 | -1.233 [-1.440, -1.030] |

### S3-E (keşifsel): FLOP'tan öngörülen gecikme ile ölçülmüş gecikme

Bir hız değerlendirmesi E = 11008 gerçel FLOP; ms/FLOP, Adam adımına kalibre (1.086 ms / 3E).

| hız | Kendall τ (sıralama) | seçilen: ölçülmüş | seçilen: FLOP | FLOP seçiminin ölçülmüş gecikmedeki etkin hızı | ölçülmüş seçimin |
| --- | --- | --- | --- | --- | --- |
| 1.5 m/s | 0.860 | Adam-6 | Adam-6 | 6.151 | 6.151 |
| 10 km/h | 0.873 | Adam-4 | Adam-4 | 5.913 | 5.913 |

Ölçülmüş / FLOP-öngörülen gecikme oranı (kol başına):

| kol | ölçülmüş (ms) | FLOP-öngörülen (ms) | oran |
| --- | --- | --- | --- |
| SU-average | 0.23 | 0.72 | 0.32 |
| SU-best-of | 1.24 | 2.90 | 0.43 |
| Adam-1 | 1.15 | 1.81 | 0.64 |
| Adam-8 | 8.80 | 9.41 | 0.94 |
| Adam-48 | 52.25 | 52.85 | 0.99 |
| CD-1 | 77.82 | 186.78 | 0.42 |
| CD-8 | 627.27 | 1484.13 | 0.42 |
| Long-run Adam | 3952.07 | 4346.32 | 0.91 |

## Soru 1 — CD kaç kat hızlanırsa sıralama değişir?

Zamanlama: yük başlangıç 0.06, ölçüm öncesi 0.06, sonrası 0.75; rerun dosyasına göre sapma adam1 ×0.862, adam48 ×0.775, CD-8 ×0.690.

Bu oturumdaki gecikmeler (ms; medyan, 5 turun en küçük–en büyük değeri):

| kol | medyan | tur aralığı |
| --- | --- | --- |
| su_average | 0.23 | 0.22–0.50 |
| su_best_of | 1.24 | 1.17–1.25 |
| adam1 | 1.15 | 0.95–1.28 |
| adam8 | 8.80 | 8.54–9.91 |
| adam48 | 52.25 | 49.69–78.21 |
| pga | 3952.07 | 3854.86–4247.43 |
| cd1 (erken durmasız) | 77.82 | 76.27–113.91 |
| cd8 (erken durmasız) | 627.27 | 620.65–685.43 |
| numba_direct8 (erken durmasız) | 10.04 | 9.89–10.48 |
| numba_incr8 (erken durmasız) | 3.45 | 3.29–3.54 |
Yük: timing2 0.28 → 0.74; timing3 0.46 → 0.85.

Erken durmasız (sapma 2) tarama başına süreler:

| tarama s | torch CD (ms) | numba doğrudan (ms) | numba artımlı (ms) | hızlanma doğrudan | hızlanma artımlı |
| --- | --- | --- | --- | --- | --- |
| 1 | 77.82 | 1.282 | 0.437 | 61× | 178× |
| 2 | 158.86 | 2.554 | 0.866 | 62× | 184× |
| 3 | 241.10 | 3.808 | 1.311 | 63× | 184× |
| 4 | 332.93 | 5.045 | 1.728 | 66× | 193× |
| 5 | 396.29 | 6.321 | 2.162 | 63× | 183× |
| 6 | 509.10 | 7.577 | 2.617 | 67× | 195× |
| 7 | 627.55 | 8.813 | 3.047 | 71× | 206× |
| 8 | 627.27 | 10.040 | 3.451 | 62× | 182× |

### 1.5 m/s — karşılaştırma kolu Adam-6 (6.63 ms, etkin hız 6.151)

- r*_eşit ∈ (10, 15]; r*_anlamlı ∈ (10, 15] (None: ızgarada ulaşılmadı)
- Derlenmiş CD (doğrudan), ayarlı CD-3, 3.81 ms (×63): etkin hız 6.665, − Adam-6 = +0.514 [+0.477, +0.552]
- Derlenmiş CD (artımlı), ayarlı CD-7, 3.05 ms (×206): etkin hız 6.835, − Adam-6 = +0.684 [+0.639, +0.728]

| r | ayarlı CD | gecikme (ms) | CD etkin hız | CD − hızlı kol [GA] |
| --- | --- | --- | --- | --- |
| 1 | CD-2 | 158.86 | 5.013 | -1.139 [-1.231, -1.046] |
| 1.5 | CD-3 | 160.74 | 5.044 | -1.108 [-1.198, -1.016] |
| 2 | CD-1 | 38.91 | 5.048 | -1.103 [-1.194, -1.010] |
| 3 | CD-1 | 25.94 | 5.150 | -1.002 [-1.079, -0.923] |
| 5 | CD-1 | 15.56 | 5.607 | -0.545 [-0.597, -0.489] |
| 7 | CD-1 | 11.12 | 5.871 | -0.281 [-0.324, -0.238] |
| 10 | CD-1 | 7.78 | 6.062 | -0.089 [-0.127, -0.051] |
| 15 | CD-1 | 5.19 | 6.188 | +0.036 [+0.001, +0.072] |
| 20 | CD-2 | 7.94 | 6.327 | +0.176 [+0.139, +0.214] |
| 30 | CD-2 | 5.30 | 6.486 | +0.334 [+0.300, +0.370] |
| 50 | CD-3 | 4.82 | 6.615 | +0.463 [+0.425, +0.499] |
| 70 | CD-3 | 3.44 | 6.682 | +0.530 [+0.490, +0.569] |
| 100 | CD-5 | 3.96 | 6.751 | +0.599 [+0.558, +0.640] |
| 150 | CD-5 | 2.64 | 6.809 | +0.658 [+0.617, +0.700] |
| 200 | CD-8 | 3.14 | 6.844 | +0.692 [+0.649, +0.736] |
| 300 | CD-8 | 2.09 | 6.885 | +0.733 [+0.689, +0.777] |
| 500 | CD-8 | 1.25 | 6.908 | +0.757 [+0.710, +0.804] |
| 1000 | CD-8 | 0.63 | 6.920 | +0.768 [+0.722, +0.816] |

### 10 km/h — karşılaştırma kolu Adam-4 (4.46 ms, etkin hız 5.913)

- r*_eşit ∈ (10, 15]; r*_anlamlı ∈ (10, 15] (None: ızgarada ulaşılmadı)
- Derlenmiş CD (doğrudan), ayarlı CD-2, 2.55 ms (×62): etkin hız 6.515, − Adam-4 = +0.602 [+0.559, +0.646]
- Derlenmiş CD (artımlı), ayarlı CD-5, 2.16 ms (×183): etkin hız 6.749, − Adam-4 = +0.836 [+0.783, +0.887]

| r | ayarlı CD | gecikme (ms) | CD etkin hız | CD − hızlı kol [GA] |
| --- | --- | --- | --- | --- |
| 1 | CD-3 | 241.10 | 5.006 | -0.906 [-1.007, -0.807] |
| 1.5 | CD-3 | 160.74 | 5.010 | -0.903 [-0.994, -0.809] |
| 2 | CD-2 | 79.43 | 5.055 | -0.858 [-0.951, -0.773] |
| 3 | CD-1 | 25.94 | 4.998 | -0.915 [-0.999, -0.826] |
| 5 | CD-1 | 15.56 | 5.097 | -0.816 [-0.904, -0.731] |
| 7 | CD-1 | 11.12 | 5.335 | -0.578 [-0.647, -0.514] |
| 10 | CD-1 | 7.78 | 5.675 | -0.237 [-0.286, -0.190] |
| 15 | CD-1 | 5.19 | 5.958 | +0.046 [+0.005, +0.085] |
| 20 | CD-1 | 3.89 | 6.093 | +0.181 [+0.142, +0.218] |
| 30 | CD-2 | 5.30 | 6.198 | +0.285 [+0.239, +0.331] |
| 50 | CD-2 | 3.18 | 6.453 | +0.541 [+0.496, +0.584] |
| 70 | CD-2 | 2.27 | 6.540 | +0.627 [+0.582, +0.676] |
| 100 | CD-3 | 2.41 | 6.633 | +0.721 [+0.674, +0.768] |
| 150 | CD-4 | 2.22 | 6.708 | +0.796 [+0.744, +0.846] |
| 200 | CD-5 | 1.98 | 6.765 | +0.852 [+0.797, +0.905] |
| 300 | CD-8 | 2.09 | 6.808 | +0.896 [+0.843, +0.947] |
| 500 | CD-8 | 1.25 | 6.877 | +0.964 [+0.905, +1.019] |
| 1000 | CD-8 | 0.63 | 6.910 | +0.998 [+0.942, +1.055] |

Not (ön kayıt): Adam derlenmedi; derlenmiş CD ile Python Adam karşılaştırması tezin aleyhine taraflıdır.

## Soru 1b — bütün kollar aynı oranda hızlandırılırsa (ÖN KAYIT DIŞI, sonuçlar görüldükten sonra yazıldı)

Kaynak `s1b_equal_speedup.py` → `raw/s1b.json`. Her kolun bu oturumdaki gecikmesi r'ye bölünür ve tam olarak değerlendirilir; aile içi en iyi kol seed 12'de seçilir.

### 1.5 m/s

| r | ayarlı Adam | Adam etkin hız | ayarlı CD | CD etkin hız | CD − Adam [GA] | genel en iyi |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Adam-6 | 6.151 | CD-2 | 5.013 | -1.139 [-1.228, -1.045] | Adam-6 |
| 1.5 | Adam-8 | 6.297 | CD-3 | 5.044 | -1.253 [-1.352, -1.156] | Adam-8 |
| 2 | Adam-12 | 6.416 | CD-1 | 5.048 | -1.367 [-1.468, -1.270] | Adam-12 |
| 3 | Adam-16 | 6.564 | CD-1 | 5.150 | -1.414 [-1.504, -1.324] | Adam-16 |
| 5 | Adam-24 | 6.717 | CD-1 | 5.607 | -1.110 [-1.185, -1.039] | Adam-24 |
| 7 | Adam-32 | 6.801 | CD-1 | 5.871 | -0.931 [-0.991, -0.868] | Adam-32 |
| 10 | Adam-32 | 6.880 | CD-1 | 6.062 | -0.818 [-0.867, -0.761] | Adam-32 |
| 15 | Adam-48 | 6.944 | CD-1 | 6.188 | -0.757 [-0.807, -0.705] | Adam-48 |
| 20 | Adam-48 | 6.982 | CD-2 | 6.327 | -0.655 [-0.707, -0.605] | Adam-48 |
| 30 | Adam-48 | 7.011 | CD-2 | 6.486 | -0.526 [-0.569, -0.484] | Adam-48 |
| 50 | Adam-48 | 7.027 | CD-3 | 6.615 | -0.413 [-0.453, -0.374] | Adam-48 |
| 70 | Adam-48 | 7.032 | CD-3 | 6.682 | -0.350 [-0.385, -0.318] | Adam-48 |
| 100 | Adam-48 | 7.034 | CD-5 | 6.751 | -0.284 [-0.315, -0.253] | Adam-48 |
| 150 | Adam-48 | 7.036 | CD-5 | 6.809 | -0.226 [-0.253, -0.199] | Adam-48 |
| 200 | Adam-48 | 7.036 | CD-8 | 6.844 | -0.192 [-0.220, -0.167] | Adam-48 |
| 300 | Adam-48 | 7.036 | CD-8 | 6.885 | -0.152 [-0.175, -0.130] | Adam-48 |
| 500 | Adam-48 | 7.037 | CD-8 | 6.908 | -0.128 [-0.149, -0.109] | Adam-48 |
| 1000 | Adam-48 | 7.037 | CD-8 | 6.920 | -0.117 [-0.138, -0.098] | Adam-48 |

### 10 km/h

| r | ayarlı Adam | Adam etkin hız | ayarlı CD | CD etkin hız | CD − Adam [GA] | genel en iyi |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Adam-4 | 5.913 | CD-3 | 5.006 | -0.906 [-1.000, -0.807] | Adam-4 |
| 1.5 | Adam-6 | 6.072 | CD-3 | 5.010 | -1.062 [-1.159, -0.969] | Adam-6 |
| 2 | Adam-8 | 6.179 | CD-2 | 5.055 | -1.124 [-1.217, -1.029] | Adam-8 |
| 3 | Adam-12 | 6.321 | CD-1 | 4.998 | -1.323 [-1.418, -1.234] | Adam-12 |
| 5 | Adam-16 | 6.529 | CD-1 | 5.097 | -1.432 [-1.524, -1.338] | Adam-16 |
| 7 | Adam-20 | 6.633 | CD-1 | 5.335 | -1.299 [-1.380, -1.215] | Adam-20 |
| 10 | Adam-24 | 6.739 | CD-1 | 5.675 | -1.063 [-1.127, -0.994] | Adam-24 |
| 15 | Adam-32 | 6.839 | CD-1 | 5.958 | -0.881 [-0.943, -0.821] | Adam-32 |
| 20 | Adam-32 | 6.892 | CD-1 | 6.093 | -0.798 [-0.850, -0.748] | Adam-32 |
| 30 | Adam-48 | 6.956 | CD-2 | 6.198 | -0.759 [-0.818, -0.703] | Adam-48 |
| 50 | Adam-48 | 7.006 | CD-2 | 6.453 | -0.552 [-0.596, -0.510] | Adam-48 |
| 70 | Adam-48 | 7.021 | CD-2 | 6.540 | -0.481 [-0.521, -0.441] | Adam-48 |
| 100 | Adam-48 | 7.029 | CD-3 | 6.633 | -0.395 [-0.433, -0.360] | Adam-48 |
| 150 | Adam-48 | 7.033 | CD-4 | 6.708 | -0.325 [-0.358, -0.294] | Adam-48 |
| 200 | Adam-48 | 7.035 | CD-5 | 6.765 | -0.270 [-0.300, -0.238] | Adam-48 |
| 300 | Adam-48 | 7.036 | CD-8 | 6.808 | -0.227 [-0.258, -0.200] | Adam-48 |
| 500 | Adam-48 | 7.036 | CD-8 | 6.877 | -0.160 [-0.185, -0.137] | Adam-48 |
| 1000 | Adam-48 | 7.037 | CD-8 | 6.910 | -0.126 [-0.147, -0.107] | Adam-48 |

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/timing.py | kanal 11, tek senaryo | raw/timing.json, raw/timing.log |
| python3 thesis_exp/juri/arms.py (3 dk) | kanal 12, 11 | raw/arms.json, raw/arms.log |
| python3 thesis_exp/juri/timing3.py (sapma 2) | kanal 11, tek senaryo | raw/timing3.json, raw/timing3.log |
| python3 thesis_exp/juri/timing2.py | kanal 11, tek senaryo | raw/timing2.json, raw/timing2.log |
| python3 thesis_exp/juri/analyze_s3_s1.py | bootstrap 0 | raw/s3_s1.json |
| python3 thesis_exp/juri/s1b_equal_speedup.py (ön kayıt dışı) | kanal 12, 11; bootstrap 0 | raw/s1b.json, raw/s1b.log |

## Yorum (bulgulardan ayrı)

- **Soru 3'e yanıt.** Katkı "FLOP yerine milisaniye" değil. Bu kurguda FLOP'tan öngörülen gecikme ile ölçülmüş gecikme aynı kolu seçiyor (Kendall τ 0.86–0.87). Fark yaratan, hesaplama süresinin kanal eskimesine katılması.
  - Süreyi yalnızca uygulanabilirlik kısıtı olarak kullanan seçim ("bütçeye sığan ve t = 0'da en iyi olan") büyük bütçelerde kaybettiriyor: 1.5 m/s'de ≥ 20 ms bütçelerde 0.43–1.41 b/s/Hz, 10 km/h'de ≥ 10 ms bütçelerde 0.26–1.23 b/s/Hz.
  - Gecikme bir bütçe kısıtı olarak değil, amacın içinde yer almalı.
- **FLOP sayımının sınırı.** Ölçülmüş / FLOP-öngörülen oranı kollar arasında 0.32 ile 0.99 arasında değişiyor; CD ve SU kolları FLOP'tan beklenenden 2–3 kat hızlı. Bu kurguda seçimi değiştirmiyor, ama FLOP'un gerçekleştirmeye bağlı süreyi ancak 3 kat içinde öngördüğünü gösteriyor.
- **Soru 1'e yanıt (iki katmanlı).**
  - (i) **Yalnızca CD derlenirse sıralama döner.** Başa baş oranı 10–15 kat. Yalnız derleme bile (aynı algoritma, ×62–63) yetiyor; rank-1 güncelleme, buna bir de algoritmik iyileştirme ekliyor. Bu bulgu, Makale 2'nin sıralamasının gerçekleştirmeye duyarlı olduğunu gösteriyor ve yumuşatılmamalı.
  - (ii) **Bütün yığın aynı oranda hızlanırsa** (r = 1…1000; ön kayıt dışı) ayarlı Adam her noktada önde. Hızlanma arttıkça Adam'ın L*'ı 1.5 m/s'de 6'dan 48'e çıkıyor. Fark en büyük hâlinde 1.5 m/s'de 1.41 (r = 3), 10 km/h'de 1.43 (r = 5); r = 1000'de 0.12–0.13. Nedeni, t = 0'da Adam-48'in (7.04) CD-8'den (6.93) daha iyi olması.
- **Savunu cümlesine etkisi.** Bu sonuç "gecikme sıralamayı belirler" cümlesini destekliyor: sıralamayı programlama dili değil, kolların gecikme oranı belirliyor. Buna karşılık "hız kesinliği yener" cümlesi, gecikme oranlarına koşullu yazılmalı.
- **Ölçüm notları.**
  - Bu oturumdaki makine, rerun ölçümlerinden 0.69–0.86 kat daha hızlıydı. Bütün kollar bu oturumda yeniden ölçüldü (sapma 1).
  - CD erken durmasız ölçüldü (sapma 2; bağımsız denetimin bulgusu). Bu düzeltme, derlenmiş CD'nin üstünlüğünü 1.5 m/s'de +0.717'den +0.684'e indirdi; yön değişmedi.
  - Seçilen kollar: 1.5 m/s'de Adam-6 (makalede 4–6), 10 km/h'de Adam-4 (makale özetinde 3). Bu farklar bu oturumun gecikmelerinden geliyor.
- **Not.** Adam-L gecikmesi, Makale 2'nin kuralına uygun olarak SU-average başlangıcını (0.23 ms) içermiyor; torch CD ise içeriyor. Karar etkisi yaklaşık 0.001.
