# Jüri soruları 3 ve 1 — ön kayıtlı sonuçlar

Rapor commit'i `bdcd899`, kol koşusu `bdcd899`. Ön kayıt `ON_KAYIT_S3_S1.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1 (tam gecikmede, interpolasyonsuz). GA: eşli bootstrap 2000, %95.

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
| 1.5 m/s | 0.900 | Adam-6 | Adam-6 | 6.151 | 6.151 |
| 10 km/h | 0.873 | Adam-4 | Adam-4 | 5.913 | 5.913 |

Ölçülmüş / FLOP-öngörülen gecikme oranı (kol başına):

| kol | ölçülmüş (ms) | FLOP-öngörülen (ms) | oran |
| --- | --- | --- | --- |
| SU-average | 0.23 | 0.72 | 0.32 |
| SU-best-of | 1.24 | 2.90 | 0.43 |
| Adam-1 | 1.15 | 1.81 | 0.64 |
| Adam-8 | 8.80 | 9.41 | 0.94 |
| Adam-48 | 52.25 | 52.85 | 0.99 |
| CD-1 | 75.72 | 186.78 | 0.41 |
| CD-8 | 485.06 | 1484.13 | 0.33 |
| Long-run Adam | 3952.07 | 4346.32 | 0.91 |

## Soru 1 — CD kaç kat hızlanırsa sıralama değişir?

Zamanlama: yük başlangıç 0.06, ölçüm öncesi 0.06, sonrası 0.75; rerun dosyasına göre sapma adam1 ×0.862, adam48 ×0.775, CD-8 ×0.690.

| tarama s | torch CD (ms) | numba doğrudan (ms) | numba artımlı (ms) | hızlanma doğrudan | hızlanma artımlı |
| --- | --- | --- | --- | --- | --- |
| 1 | 75.72 | 1.283 | 0.448 | 59× | 169× |
| 2 | 163.05 | 2.544 | 0.850 | 64× | 192× |
| 3 | 263.79 | 3.804 | 1.271 | 69× | 208× |
| 4 | 335.62 | 5.112 | 1.714 | 66× | 196× |
| 5 | 428.96 | 6.368 | 2.124 | 67× | 202× |
| 6 | 485.59 | 7.586 | 2.541 | 64× | 191× |
| 7 | 460.73 | 7.595 | 2.539 | 61× | 181× |
| 8 | 485.06 | 7.602 | 2.543 | 64× | 191× |

### 1.5 m/s — karşılaştırma kolu Adam-6 (6.63 ms, etkin hız 6.151)

- r*_eşit ∈ (10, 15]; r*_anlamlı ∈ (10, 15] (None: ızgarada ulaşılmadı)
- Derlenmiş CD (doğrudan), ayarlı CD-3, 3.80 ms (×69): etkin hız 6.666, − Adam-6 = +0.514 [+0.478, +0.552]
- Derlenmiş CD (artımlı), ayarlı CD-8, 2.54 ms (×191): etkin hız 6.868, − Adam-6 = +0.717 [+0.670, +0.762]

| r | ayarlı CD | gecikme (ms) | CD etkin hız | CD − hızlı kol [GA] |
| --- | --- | --- | --- | --- |
| 1 | CD-2 | 163.05 | 4.968 | -1.183 [-1.277, -1.087] |
| 1.5 | CD-1 | 50.48 | 4.967 | -1.185 [-1.276, -1.100] |
| 2 | CD-1 | 37.86 | 5.049 | -1.103 [-1.194, -1.009] |
| 3 | CD-1 | 25.24 | 5.167 | -0.985 [-1.062, -0.908] |
| 5 | CD-1 | 15.14 | 5.632 | -0.520 [-0.571, -0.465] |
| 7 | CD-1 | 10.82 | 5.888 | -0.263 [-0.307, -0.221] |
| 10 | CD-1 | 7.57 | 6.074 | -0.078 [-0.115, -0.040] |
| 15 | CD-1 | 5.05 | 6.194 | +0.042 [+0.007, +0.078] |
| 20 | CD-2 | 8.15 | 6.313 | +0.162 [+0.124, +0.200] |
| 30 | CD-2 | 5.44 | 6.478 | +0.327 [+0.292, +0.362] |
| 50 | CD-3 | 5.28 | 6.589 | +0.438 [+0.399, +0.474] |
| 70 | CD-4 | 4.79 | 6.672 | +0.521 [+0.480, +0.561] |
| 100 | CD-8 | 4.85 | 6.755 | +0.604 [+0.562, +0.646] |
| 150 | CD-8 | 3.23 | 6.839 | +0.688 [+0.646, +0.730] |
| 200 | CD-8 | 2.43 | 6.873 | +0.721 [+0.677, +0.767] |
| 300 | CD-8 | 1.62 | 6.899 | +0.748 [+0.704, +0.791] |
| 500 | CD-8 | 0.97 | 6.914 | +0.763 [+0.716, +0.810] |
| 1000 | CD-8 | 0.49 | 6.922 | +0.770 [+0.723, +0.818] |

### 10 km/h — karşılaştırma kolu Adam-4 (4.46 ms, etkin hız 5.913)

- r*_eşit ∈ (10, 15]; r*_anlamlı ∈ (10, 15] (None: ızgarada ulaşılmadı)
- Derlenmiş CD (doğrudan), ayarlı CD-2, 2.54 ms (×64): etkin hız 6.516, − Adam-4 = +0.603 [+0.560, +0.647]
- Derlenmiş CD (artımlı), ayarlı CD-8, 2.54 ms (×191): etkin hız 6.763, − Adam-4 = +0.850 [+0.795, +0.905]

| r | ayarlı CD | gecikme (ms) | CD etkin hız | CD − hızlı kol [GA] |
| --- | --- | --- | --- | --- |
| 1 | CD-2 | 163.05 | 4.972 | -0.941 [-1.043, -0.850] |
| 1.5 | CD-3 | 175.86 | 4.999 | -0.914 [-1.007, -0.813] |
| 2 | CD-2 | 81.53 | 5.048 | -0.865 [-0.959, -0.776] |
| 3 | CD-1 | 25.24 | 5.013 | -0.900 [-0.986, -0.811] |
| 5 | CD-1 | 15.14 | 5.108 | -0.804 [-0.889, -0.721] |
| 7 | CD-1 | 10.82 | 5.361 | -0.552 [-0.619, -0.489] |
| 10 | CD-1 | 7.57 | 5.699 | -0.214 [-0.262, -0.168] |
| 15 | CD-1 | 5.05 | 5.973 | +0.061 [+0.021, +0.101] |
| 20 | CD-1 | 3.79 | 6.104 | +0.191 [+0.152, +0.229] |
| 30 | CD-1 | 2.52 | 6.209 | +0.296 [+0.257, +0.336] |
| 50 | CD-2 | 3.26 | 6.447 | +0.534 [+0.491, +0.577] |
| 70 | CD-2 | 2.33 | 6.535 | +0.622 [+0.577, +0.671] |
| 100 | CD-3 | 2.64 | 6.611 | +0.698 [+0.652, +0.745] |
| 150 | CD-4 | 2.24 | 6.707 | +0.794 [+0.742, +0.844] |
| 200 | CD-8 | 2.43 | 6.776 | +0.863 [+0.809, +0.915] |
| 300 | CD-8 | 1.62 | 6.850 | +0.937 [+0.882, +0.991] |
| 500 | CD-8 | 0.97 | 6.894 | +0.981 [+0.921, +1.037] |
| 1000 | CD-8 | 0.49 | 6.916 | +1.003 [+0.946, +1.060] |

Not (ön kayıt): Adam derlenmedi; derlenmiş CD ile Python Adam karşılaştırması tezin aleyhine taraflıdır.

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/timing.py | kanal 11, tek senaryo | raw/timing.json, raw/timing.log |
| python3 thesis_exp/juri/arms.py (3 dk) | kanal 12, 11 | raw/arms.json, raw/arms.log |
| python3 thesis_exp/juri/analyze_s3_s1.py | bootstrap 0 | raw/s3_s1.json |
