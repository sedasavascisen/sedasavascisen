# Soru 5b — daha büyük veri ve birden fazla tohumla sağlamlık (ön kayıtlı)

Rapor commit'i `0679077`, değerlendirme `0679077`. Ön kayıt `ON_KAYIT_S5b.md`. 28 GHz, eğitim n = 80 000, seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1. Genişlik-128 ağın gecikmesi 0.777 ms (turlar 0.717, 0.966, 0.784, 0.777, 0.746); genişlik 64 için 0.425 ms (S5).

## Kararlar (28 GHz, 1.5 m/s)

- **S5b-H1** (seçilen ağ sincos_b0 − en iyi klasik SU-best-of): -0.347 [-0.411, -0.281] → **TUTMADI**
- **S5b-H2** (seçilen ağ − SU-average): +0.055 [+0.021, +0.087] → **TUTTU**
- **S5b-H3** (sin/cos − doğrudan açı, etkin hız; 3 tohumun ≥ 2'sinde anlamlı): tohum 0: +0.008 [-0.021, +0.036]; tohum 1: +0.067 [+0.038, +0.095]; tohum 2: +0.013 [-0.016, +0.043] → **TUTMADI**

## 1.5 m/s — en iyi klasik SU-best-of (5.011), SU-average (4.610)

| ağ | gecikme (ms) | t = 0 | etkin hız | − en iyi klasik [GA] | − SU-average [GA] |
| --- | --- | --- | --- | --- | --- |
| sincos_b0 (seçilen) | 0.43 | 4.683 | 4.664 | -0.347 [-0.411, -0.281] | +0.055 [+0.021, +0.087] |
| sincos_b1 | 0.43 | 4.721 | 4.702 | -0.309 [-0.375, -0.249] | +0.092 [+0.058, +0.128] |
| sincos_b2 | 0.43 | 4.673 | 4.657 | -0.354 [-0.420, -0.288] | +0.047 [+0.013, +0.079] |
| sincos_w128 | 0.78 | 4.696 | 4.652 | -0.359 [-0.422, -0.301] | +0.042 [+0.005, +0.078] |
| angle_b0 | 0.43 | 4.675 | 4.657 | -0.355 [-0.419, -0.292] | +0.047 [+0.012, +0.081] |
| angle_b1 | 0.43 | 4.651 | 4.635 | -0.376 [-0.437, -0.310] | +0.025 [-0.007, +0.059] |
| angle_b2 | 0.43 | 4.662 | 4.644 | -0.367 [-0.433, -0.298] | +0.034 [-0.001, +0.070] |
| sincos_b0+Adam-1 | 1.58 | 5.077 | 4.887 | -0.124 [-0.168, -0.079] | +0.277 [+0.218, +0.336] |

sin/cos − doğrudan açı (aynı tohum): tohum 0: t = 0 +0.007 [-0.020, +0.037], etkin +0.008 [-0.021, +0.036]; tohum 1: t = 0 +0.070 [+0.041, +0.100], etkin +0.067 [+0.038, +0.095]; tohum 2: t = 0 +0.012 [-0.018, +0.042], etkin +0.013 [-0.016, +0.043]

## 3 km/h — en iyi klasik Adam-1|best (5.145), SU-average (4.611)

| ağ | gecikme (ms) | t = 0 | etkin hız | − en iyi klasik [GA] | − SU-average [GA] |
| --- | --- | --- | --- | --- | --- |
| sincos_b0 (seçilen) | 0.43 | 4.683 | 4.673 | -0.472 [-0.541, -0.408] | +0.062 [+0.028, +0.098] |
| sincos_b1 | 0.43 | 4.721 | 4.713 | -0.433 [-0.500, -0.371] | +0.102 [+0.067, +0.136] |
| sincos_b2 | 0.43 | 4.673 | 4.665 | -0.480 [-0.550, -0.413] | +0.055 [+0.022, +0.088] |
| sincos_w128 | 0.78 | 4.696 | 4.674 | -0.472 [-0.535, -0.409] | +0.063 [+0.030, +0.096] |
| angle_b0 | 0.43 | 4.675 | 4.666 | -0.479 [-0.539, -0.414] | +0.056 [+0.024, +0.089] |
| angle_b1 | 0.43 | 4.651 | 4.643 | -0.503 [-0.571, -0.437] | +0.032 [+0.000, +0.065] |
| angle_b2 | 0.43 | 4.662 | 4.653 | -0.493 [-0.565, -0.429] | +0.042 [+0.008, +0.076] |
| sincos_b0+Adam-2 | 2.71 | 5.283 | 5.052 | -0.094 [-0.126, -0.062] | +0.441 [+0.377, +0.507] |

sin/cos − doğrudan açı (aynı tohum): tohum 0: t = 0 +0.007 [-0.021, +0.035], etkin +0.007 [-0.023, +0.036]; tohum 1: t = 0 +0.070 [+0.043, +0.100], etkin +0.070 [+0.042, +0.099]; tohum 2: t = 0 +0.012 [-0.021, +0.042], etkin +0.013 [-0.018, +0.044]

## Eğitim

| model | en iyi doğrulama | epoch | süre (s) |
| --- | --- | --- | --- |
| sincos_b0 | 4.4384 | 21 / 60 | 677 |
| sincos_b1 | 4.4320 | 34 / 60 | 676 |
| sincos_b2 | 4.4300 | 21 / 60 | 644 |
| sincos_w128 | 4.4285 | 13 / 60 | 1485 |
| angle_b0 | 4.4127 | 17 / 60 | 651 |
| angle_b1 | 4.4107 | 22 / 60 | 639 |
| angle_b2 | 4.4071 | 29 / 60 | 637 |

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| thesis_exp/juri/s5/chain_s5b.sh (train.py --fc 28 --n 80000 --seed {0,1,2} [--width 128]) | eğitim 21, doğrulama 12, model 0/1/2 | s5/raw/net_28_*_b*.pt, *_w128.pt, train_28_*.json/.log |
| python3 thesis_exp/juri/s5/eval_s5b.py | kanal 12, 11 | s5/raw/eval_s5b.json, eval_s5b.log |
| python3 thesis_exp/juri/s5/analyze_s5b.py | bootstrap 0 | s5/raw/s5b_summary.json |

## Yorum (bulgulardan ayrı)

- **Daha büyük veri ve daha fazla tohum hükmü değiştirmedi.** 80 000 örnekle, 3 model tohumuyla ve 2 kat geniş bir ağla, 28 GHz'de 1.5 m/s'de bütün sin/cos ağları SU-best-of'un −0.31 ile −0.36 gerisinde. S5'teki −0.38'den az farklı; kaybın nedeni veri azlığı değil.
- **Veri artınca ağ, optimizasyonsuz SU-average'ı geçiyor.** Fark +0.04 ile +0.09 ve anlamlı (S5b-H2). S5'te (20 000 örnek) bu fark anlamlı değildi. Ağ öğreniyor, ama tavanı tek kullanıcı hizalamalarının en iyisinin (SU-best-of) altında kalıyor.
- **sin/cos avantajı tohuma bağlı (S5b-H3 tutmadı).** Aynı tohumla eşleştirilmiş üç çiftten yalnızca birinde (tohum 1: +0.067) anlamlı; diğer ikisinde +0.008 ve +0.013, ikisi de anlamsız.
  - S5'teki "+0.04…+0.05, anlamlı" bulgusu, tek bir eğitim koşusunun ürünüydü ve genellenemez.
  - Bu kurguda (çok kullanıcılı, etiketsiz, hız tabanlı eğitim) sin/cos kafasının doğrudan açıya üstünlüğü gösterilemedi. Makale 1'in kendi kurgusundaki ablasyon (etiketli faz regresyonu) bundan etkilenmez; ama bu deney onu desteklemiyor da.
- **Karma kol hâlâ en iyi klasik kolun gerisinde:** 1.5 m/s'de −0.12, 3 km/h'de −0.09.
- **Kapsam.** Tek mimari ailesi (CNN, iki genişlik), 80 000 örnek, 60 epoch. Bu deney yapay zekâ eksenini "bu mimari ailesiyle ve bu bütçeyle" kapatıyor; bütün öğrenme yöntemleri hakkında genel bir hüküm değil.
