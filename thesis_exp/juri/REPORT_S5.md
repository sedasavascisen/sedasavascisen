# Jüri sorusu 5 — öğrenmeye en elverişli rejimde kesin test (ön kayıtlı)

Rapor commit'i `0679077`, değerlendirme `19a5eb6`. Ön kayıt `ON_KAYIT_S5.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1. Ağ çıkarımı 0.425 ms (tek iş parçacığı, toplu 1; turlar 0.463, 0.425, 0.418, 0.420, 0.440). 28 GHz bağlantı bütçesi telafisi 30.79 dB (eğitim tohumu 21).

## ⚠ En üstte: aleyhte bulgular (Kural 10)

- **Ön kayıtlı H1 ve H2 tutmadı:** tek geçişli ağ ve ağ + Adam karması, en iyi klasik kolun gerisinde (aşağıda).
- **28 GHz, 1.5 m/s: eğitilmiş ağ − SU-average** (SU-average daha hızlı: 0.23 ms): etkin hızda +0.021 [-0.013, +0.055] — **anlamlı değil**
- **28 GHz, 3 km/h: eğitilmiş ağ − SU-average** (SU-average daha hızlı: 0.23 ms): etkin hızda +0.030 [-0.004, +0.064] — **anlamlı değil**
- **3 GHz, 1.5 m/s: eğitilmiş ağ − SU-average** (SU-average daha hızlı: 0.23 ms): etkin hızda +0.087 [+0.026, +0.144]
- **3 GHz, 3 km/h: eğitilmiş ağ − SU-average** (SU-average daha hızlı: 0.23 ms): etkin hızda +0.086 [+0.027, +0.145]
- Kapsam: tek mimari, tek model tohumu (0), 20 000 eğitim örneği, en çok 60 epoch. Hüküm bu mimari ve bu eğitim bütçesi içindir; daha büyük veri ya da başka mimari sınanmadı.

## Kararlar (28 GHz, 1.5 m/s)

- **S5-H1** (NN-sincos − en iyi klasik > 0): -0.381 [-0.444, -0.314] → **TUTMADI**
- **S5-H2** (en iyi NN+Adam-L − en iyi klasik > 0): NN+Adam-1 -0.158 [-0.203, -0.112] → **TUTMADI**
- **S5-H3** (t = 0'da eğitilmiş − eğitilmemiş > 0): +0.470 [+0.392, +0.548] → **TUTTU**
- En iyi klasik kol (seed 12): SU-best-of (1.24 ms), etkin hız 5.011

## Bütün hücreler

| fc | hız | f_d (Hz) | en iyi klasik (ms) | etkin hız | kol | gecikme (ms) | t = 0 hızı | etkin hız | − en iyi klasik [GA] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-sincos | 0.43 | 4.650 | 4.630 | -0.381 [-0.444, -0.314] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-angle | 0.43 | 4.601 | 4.587 | -0.424 [-0.496, -0.356] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-untrained | 0.43 | 4.181 | 4.171 | -0.840 [-0.944, -0.748] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN+Adam-1 | 1.58 | 5.043 | 4.853 | -0.158 [-0.203, -0.112] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | SU-best-of | 1.24 | 5.115 | 5.011 | +0.000 [+0.000, +0.000] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | SU-average | 0.23 | 4.611 | 4.610 | -0.401 [-0.471, -0.339] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-sincos | 0.43 | 4.650 | 4.640 | -0.505 [-0.572, -0.434] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-angle | 0.43 | 4.601 | 4.594 | -0.551 [-0.621, -0.480] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-untrained | 0.43 | 4.181 | 4.176 | -0.969 [-1.071, -0.871] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN+Adam-2 | 2.71 | 5.256 | 5.033 | -0.112 [-0.144, -0.081] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | SU-best-of | 1.24 | 5.115 | 5.077 | -0.068 [-0.101, -0.037] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | SU-average | 0.23 | 4.611 | 4.611 | -0.535 [-0.605, -0.463] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN-sincos | 0.43 | 4.710 | 4.711 | -1.523 [-1.620, -1.427] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN-untrained | 0.43 | 4.341 | 4.341 | -1.892 [-1.996, -1.783] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN+Adam-6 | 7.05 | 6.339 | 6.158 | -0.075 [-0.113, -0.037] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | SU-best-of | 1.24 | 5.276 | 5.278 | -0.956 [-1.024, -0.891] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | SU-average | 0.23 | 4.624 | 4.624 | -1.610 [-1.708, -1.506] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN-sincos | 0.43 | 4.710 | 4.710 | -1.732 [-1.830, -1.637] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN-untrained | 0.43 | 4.341 | 4.341 | -2.101 [-2.212, -1.998] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN+Adam-12 | 13.68 | 6.642 | 6.380 | -0.063 [-0.097, -0.031] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | SU-best-of | 1.24 | 5.276 | 5.278 | -1.165 [-1.233, -1.096] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | SU-average | 0.23 | 4.624 | 4.624 | -1.819 [-1.922, -1.718] |

## Keşifsel

- **S5-E1, 28 GHz 1.5 m/s** (sin/cos − doğrudan açı): t = 0'da +0.049 [+0.018, +0.080], etkin hızda +0.043 [+0.013, +0.074]
- **S5-E1, 28 GHz 3 km/h** (sin/cos − doğrudan açı): t = 0'da +0.049 [+0.020, +0.082], etkin hızda +0.046 [+0.015, +0.078]
- **S5-E2, 3 GHz 1.5 m/s:** NN-sincos − en iyi klasik -1.523 [-1.620, -1.427]; NN+Adam-6 − en iyi klasik -0.075 [-0.113, -0.037]; eğitilmiş − eğitilmemiş (t = 0) +0.369 [+0.284, +0.453]
- **S5-E2, 3 GHz 3 km/h:** NN-sincos − en iyi klasik -1.732 [-1.830, -1.637]; NN+Adam-12 − en iyi klasik -0.063 [-0.097, -0.031]; eğitilmiş − eğitilmemiş (t = 0) +0.369 [+0.275, +0.454]
- **S5-E2, 28 GHz 3 km/h:** NN-sincos − en iyi klasik -0.505 [-0.572, -0.434]; NN+Adam-2 − en iyi klasik -0.112 [-0.144, -0.081]; eğitilmiş − eğitilmemiş (t = 0) +0.470 [+0.398, +0.549]

## Eğitim

| model | en iyi doğrulama min-hızı | epoch | süre (s) |
| --- | --- | --- | --- |
| 28_sincos | 4.3960 | 10 / 60 | 165 |
| 28_angle | 4.3821 | 12 / 60 | 158 |
| 3_sincos | 4.3166 | 10 / 60 | 164 |

Notlar: Adam-L gecikmeleri L ∈ {1, 2, 4, 8, 16, 32, 48} ölçümlerinden doğrusal interpolasyonla. CD-s gecikmeleri `raw/timing.json`'dan (erken durmalı, sapma 2 öncesi); CD hiçbir hücrede en iyi klasik kol olmadığı için kararlar etkilenmez. Derlenmiş CD, ön kayıt gereği klasik kümede değil. NN zamanlamasında ölçüm sonrası yük kaydedilmedi.

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/s5/link_budget.py | kanal 21 | s5/raw/link_budget.json |
| python3 thesis_exp/juri/s5/train.py --fc {28,3} --head {sincos,angle} | eğitim 21, doğrulama 12, model 0 | s5/raw/net_*.pt, train_*.json, train_*.log |
| python3 thesis_exp/juri/s5/eval_s5.py (2 dk) | kanal 12, 11 | s5/raw/eval.json, eval.log |
| python3 thesis_exp/juri/s5/analyze_s5.py | bootstrap 0 | s5/raw/s5_summary.json |

## Yorum (bulgulardan ayrı)

- **Soru 5'e yanıt: bu mimari ve bu eğitim bütçesiyle, en elverişli rejimde de olumsuz.**
  - 28 GHz'de 1.5 m/s'de (T_c ≈ 3 ms) tek geçişli ağ 0.43 ms'de karar veriyor, ama 1.24 ms'lik SU-best-of'un 0.38 b/s/Hz gerisinde kalıyor.
  - Kendisinden de hızlı olan, optimizasyonsuz SU-average'ı (0.23 ms) bile 28 GHz'de anlamlı olarak geçemiyor; 3 GHz'de onu ancak +0.09 farkla geçiyor.
  - Bu hüküm tek mimariye, tek model tohumuna ve 20 000 örneğe dayanıyor. Doğrulama hızı 10–12. epoch'ta doruğa ulaşıp düştü (aşırı uyum). Daha büyük veri ya da başka bir mimari denenmedi.
- **Kaybı belirleyen gecikme değil, kalite tavanı.**
  - Ağın gecikmesi sıfır olsaydı bile, t = 0 hızı (4.650) en iyi klasik kolun t = 0 hızının (SU-best-of, 5.115) 0.47 altında kalırdı.
  - Gecikme bu karşılaştırmada ağın değil, klasik kollar arasındaki sıralamanın belirleyicisi: 28 GHz'de en iyi klasik kol SU-best-of (1.24 ms), 3 GHz'de Adam-6 (7.9 ms).
  - Ağın açığı 3 GHz'de −1.52, 28 GHz'de −0.38. Ancak başvuru kolları farklı olduğu için bu iki farkın oranı bir "daralma katsayısı" olarak okunmamalı.
- **"Çapada donma" bu ağda yok.** Eğitilmiş ağ, eğitilmemişten t = 0'da +0.47 (28 GHz) ve +0.37 (3 GHz) iyi. Ağ öğreniyor, ama öğrendiği, kapalı formdaki tek kullanıcı hizalamalarının en iyisini seçmek kadar iyi değil.
- **Karma (ağ + Adam).** 3 GHz'de en iyi klasik kolun 0.06–0.08, 28 GHz'de 0.11–0.16 gerisinde. Eşit adım sayısında, SU-best-of'tan başlayan Adam'dan t = 0'da anlamlı olarak daha kötü; örneğin L = 1'de −0.303 [−0.342, −0.263], bağımsız denetimin hesabı. Ağ, Adam için SU-best-of'tan daha kötü bir başlangıç.
- **Not (Soru 5b, sonradan):** Aşağıdaki sin/cos bulgusu üç tohumla tekrarlandı ve yalnızca bir tohumda anlamlı çıktı (`REPORT_S5b.md`); tek koşudan genellenemez.
- **Makale 1 ile bağ.** sin/cos kafası, doğrudan açı kafasını t = 0'da ve etkin hızda +0.04…+0.05 farkla, anlamlı biçimde geçiyor; Makale 1'deki ablasyonun yönü burada da görülüyor. Ancak her kafa tek bir eğitim koşusuyla eğitildi: güven aralığı yalnızca senaryo değişkenliğini içeriyor, eğitim tohumu değişkenliğini içermiyor.
- **Sınırlar.**
  - 28 GHz bağlantı bütçesi 30.79 dB telafiyle eşitlendi.
  - Ağın gecikmesi CPU'da ve Python'da ölçüldü. SU-best-of'un 1.24 ms'deki toplam eskime kaybı 0.104 (5.115 → 5.011). Ağ sıfır gecikmeli olsaydı bile bu kayıp, ağın t = 0 açığını kapatmaya yetmezdi.
