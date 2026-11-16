# Jüri sorusu 5 — öğrenmeye en elverişli rejimde kesin test (ön kayıtlı)

Rapor commit'i `37cd1a9`, değerlendirme `19a5eb6`. Ön kayıt `ON_KAYIT_S5.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1. Ağ çıkarımı 0.425 ms (tek iş parçacığı, toplu 1; turlar 0.463, 0.425, 0.418, 0.420, 0.440). 28 GHz bağlantı bütçesi telafisi 30.79 dB (eğitim tohumu 21).

## Kararlar (28 GHz, 1.5 m/s)

- **S5-H1** (NN-sincos − en iyi klasik > 0): -0.381 [-0.444, -0.314] → **TUTMADI**
- **S5-H2** (en iyi NN+Adam-L − en iyi klasik > 0): NN+Adam-1 -0.158 [-0.203, -0.112] → **TUTMADI**
- **S5-H3** (t = 0'da eğitilmiş − eğitilmemiş > 0): +0.470 [+0.396, +0.552] → **TUTTU**
- En iyi klasik kol (seed 12): SU-best-of (1.24 ms), etkin hız 5.011

## Bütün hücreler

| fc | hız | f_d (Hz) | en iyi klasik (ms) | etkin hız | kol | gecikme (ms) | t = 0 hızı | etkin hız | − en iyi klasik [GA] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-sincos | 0.43 | 4.650 | 4.630 | -0.381 [-0.444, -0.314] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-angle | 0.43 | 4.601 | 4.587 | -0.424 [-0.496, -0.356] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN-untrained | 0.43 | 4.181 | 4.171 | -0.840 [-0.944, -0.748] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | NN+Adam-1 | 1.58 | 5.043 | 4.853 | -0.158 [-0.203, -0.112] |
| 28 GHz | 1.5 m/s | 140 | SU-best-of (1.24) | 5.011 | SU-best-of | 1.24 | 5.115 | 5.011 | +0.000 [+0.000, +0.000] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-sincos | 0.43 | 4.650 | 4.640 | -0.505 [-0.574, -0.440] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-angle | 0.43 | 4.601 | 4.594 | -0.551 [-0.623, -0.484] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN-untrained | 0.43 | 4.181 | 4.176 | -0.969 [-1.073, -0.867] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | NN+Adam-2 | 2.71 | 5.256 | 5.033 | -0.112 [-0.146, -0.082] |
| 28 GHz | 3 km/h | 78 | Adam-1|best (2.39) | 5.145 | SU-best-of | 1.24 | 5.115 | 5.077 | -0.068 [-0.099, -0.037] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN-sincos | 0.43 | 4.710 | 4.711 | -1.523 [-1.617, -1.433] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN-untrained | 0.43 | 4.341 | 4.341 | -1.892 [-1.994, -1.790] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | NN+Adam-6 | 7.05 | 6.339 | 6.158 | -0.075 [-0.115, -0.037] |
| 3 GHz | 1.5 m/s | 15 | Adam-6|best (7.87) | 6.234 | SU-best-of | 1.24 | 5.276 | 5.278 | -0.956 [-1.021, -0.892] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN-sincos | 0.43 | 4.710 | 4.710 | -1.732 [-1.833, -1.634] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN-untrained | 0.43 | 4.341 | 4.341 | -2.101 [-2.209, -1.995] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | NN+Adam-12 | 13.68 | 6.642 | 6.380 | -0.063 [-0.095, -0.032] |
| 3 GHz | 3 km/h | 8 | Adam-10|best (12.27) | 6.442 | SU-best-of | 1.24 | 5.276 | 5.278 | -1.165 [-1.234, -1.094] |

## Keşifsel

- **S5-E1, 28 GHz 1.5 m/s** (sin/cos − doğrudan açı): t = 0'da +0.049 [+0.018, +0.080], etkin hızda +0.043 [+0.014, +0.072]
- **S5-E1, 28 GHz 3 km/h** (sin/cos − doğrudan açı): t = 0'da +0.049 [+0.019, +0.082], etkin hızda +0.046 [+0.016, +0.076]
- **S5-E2, 3 GHz 1.5 m/s:** NN-sincos − en iyi klasik -1.523 [-1.617, -1.433]; NN+Adam-6 − en iyi klasik -0.075 [-0.115, -0.037]; eğitilmiş − eğitilmemiş (t = 0) +0.369 [+0.280, +0.462]
- **S5-E2, 3 GHz 3 km/h:** NN-sincos − en iyi klasik -1.732 [-1.833, -1.634]; NN+Adam-12 − en iyi klasik -0.063 [-0.095, -0.032]; eğitilmiş − eğitilmemiş (t = 0) +0.369 [+0.275, +0.461]
- **S5-E2, 28 GHz 3 km/h:** NN-sincos − en iyi klasik -0.505 [-0.574, -0.440]; NN+Adam-2 − en iyi klasik -0.112 [-0.146, -0.082]; eğitilmiş − eğitilmemiş (t = 0) +0.470 [+0.394, +0.547]

## Eğitim

| model | en iyi doğrulama min-hızı | epoch | süre (s) |
| --- | --- | --- | --- |
| 28_sincos | 4.3960 | 10 / 60 | 165 |
| 28_angle | 4.3821 | 12 / 60 | 158 |
| 3_sincos | 4.3166 | 10 / 60 | 164 |

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/s5/link_budget.py | kanal 21 | s5/raw/link_budget.json |
| python3 thesis_exp/juri/s5/train.py --fc {28,3} --head {sincos,angle} | eğitim 21, doğrulama 12, model 0 | s5/raw/net_*.pt, train_*.json, train_*.log |
| python3 thesis_exp/juri/s5/eval_s5.py (2 dk) | kanal 12, 11 | s5/raw/eval.json, eval.log |
| python3 thesis_exp/juri/s5/analyze_s5.py | bootstrap 0 | s5/raw/s5_summary.json |

## Yorum (bulgulardan ayrı)

- **Soru 5'e yanıt: yapay zekâ ekseni, en elverişli rejimde de olumsuz kapanıyor.** 28 GHz'de 1.5 m/s'de (T_c ≈ 3 ms) tek geçişli ağ 0.43 ms'de karar veriyor. Buna rağmen 1.24 ms'lik SU-best-of'un 0.38 b/s/Hz gerisinde kalıyor. Ağın faz kalitesi t = 0'da 4.65; SU-best-of'unki 5.12. Bu rejimde 0.8 ms'lik gecikme farkı SU-best-of'a yalnızca ~0.1 b/s/Hz'e mal oluyor (5.115 → 5.011). Ağ ancak t = 0'da ~5.0'ın üstüne çıksaydı kazanabilirdi.
- **Gecikmenin rolü doğrulanıyor.** Ağın en iyi klasik kola göre açığı 3 GHz'de −1.52, 28 GHz'de −0.38. Gecikme baskınlaştıkça açık 4 kat daralıyor, ama kapanmıyor. Savunu cümlesi ("gecikme sıralamayı belirler") burada da işliyor: kazananı gecikme değil, tek geçişli ağın kalite tavanı belirliyor.
- **"Çapada donma" bu ağda yok.** Eğitilmiş ağ, eğitilmemişten t = 0'da +0.47 (28 GHz) ve +0.37 (3 GHz) iyi. Eski bulgudaki donma, o modelin bir özelliğiydi. Ağ öğreniyor, ama öğrendiği, kapalı formdaki tek kullanıcı hizalamalarının en iyisini seçmek kadar iyi değil.
- **Karma (ağ + Adam) en yakın kol.** 3 GHz'de en iyi klasik kolun yalnızca 0.06–0.08 gerisinde, 28 GHz'de 0.11–0.16 gerisinde. Ağı, Adam için bir başlangıç noktası olarak kullanmak işe yarıyor; ama SU-best-of başlangıcından daha iyi bir başlangıç değil.
- **Makale 1 ile bağ.** sin/cos kafası, doğrudan açı kafasını t = 0'da ve etkin hızda +0.04…+0.05 farkla, anlamlı biçimde geçiyor. Makale 1'deki ablasyonun yönü bu çok kullanıcılı, hız tabanlı ve etiketsiz eğitimde de tekrarlanıyor; büyüklüğü ise küçük. Tezde Makale 1'in katkısı bu ölçülmüş, küçük ama tutarlı etki üzerinden konumlandırılabilir.
- **Sınırlar (jürinin soracağı).**
  - Tek mimari, 20 000 eğitim örneği, en çok 60 epoch. Doğrulama hızı 10–20. epoch'ta doruğa ulaşıp düştü (aşırı uyum). Daha büyük veri ya da başka bir mimari sonucu değiştirebilir; burada sınanmadı.
  - 28 GHz bağlantı bütçesi 30.79 dB telafiyle eşitlendi.
  - Ağın gecikmesi CPU'da ve Python'da ölçüldü. Ağ 10 kat hızlansaydı bile, SU-best-of'un gecikme kaybı (~0.1) açığı (0.38) kapatmaya yetmezdi. Bu bir çıkarım; ölçülmedi.
