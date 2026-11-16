# Tasarım kuralı — ön kayıtlı sınama raporu

Rapor commit'i `83482b3`, sınama commit'i `83482b3`, kalibrasyon commit'i `0f97e10`. Ön kayıt: `ON_KAYIT.md` (sınamadan önce commit'lendi, d840144). Kalibrasyon seed 12, sınama seed 13, 60 koşul, 400 senaryo. Kayıp = 1 − R(L seçilen) / R(L*), L* sınama çekilişindeki argmax.

## 1) Hipotez kararları

- **H1** (medyan kayıp ≤ %1, en kötü ≤ %3): medyan %0.08, en kötü %2.74 → **TUTTU**
- **H2** (kural, L = 48 ve L = 5'ten iyi; koşullar üzerinden ortalama kayıp farkı, eşli GA sıfırın üstünde): L = 48'e göre +3.34 puan [+2.89, +3.81], L = 5'e göre +2.72 puan [+2.22, +3.22] → **TUTTU**
- **H3** (W > 0'da kural, makalenin kapalı formundan iyi): +1.97 puan [+1.45, +2.49] → **TUTTU**

## 2) Koşul başına kayıp (%)

| km/h | ΔT (ms) | W (ms) | x | L* | kural L̂ | kayıp: kural | L=48 | L=5 | kapalı form |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 0.33 | 0 | 0.0028 | 24 | 32 | 0.27 | 2.64 | 9.33 | 0.00 (24) |
| 3 | 0.33 | 25 | 0.0028 | 20 | 24 | 0.15 | 3.83 | 6.33 | 0.15 (24) |
| 3 | 0.33 | 50 | 0.0028 | 20 | 24 | 0.00 | 2.21 | 5.12 | 0.00 (24) |
| 3 | 0.33 | 100 | 0.0028 | 32 | 24 | 0.06 | 0.78 | 5.11 | 0.06 (24) |
| 3 | 1.33 | 0 | 0.0111 | 10 | 10 | 0.00 | 15.59 | 2.71 | 0.43 (8) |
| 3 | 1.33 | 25 | 0.0111 | 8 | 8 | 0.00 | 9.58 | 0.77 | 0.00 (8) |
| 3 | 1.33 | 50 | 0.0111 | 8 | 10 | 0.18 | 5.38 | 0.60 | 0.00 (8) |
| 3 | 1.33 | 100 | 0.0111 | 12 | 12 | 0.00 | 2.59 | 1.46 | 0.39 (8) |
| 3 | 5.32 | 0 | 0.0444 | 3 | 3 | 0.00 | 12.86 | 2.64 | 0.00 (3) |
| 3 | 5.32 | 25 | 0.0444 | 3 | 3 | 0.00 | 7.47 | 2.33 | 0.00 (3) |
| 3 | 5.32 | 50 | 0.0444 | 3 | 3 | 0.00 | 3.98 | 1.14 | 0.00 (3) |
| 3 | 5.32 | 100 | 0.0444 | 3 | 12 | 0.29 | 0.85 | 0.22 | 0.00 (3) |
| 5.4 | 0.33 | 0 | 0.0050 | 20 | 20 | 0.00 | 8.93 | 6.87 | 0.07 (16) |
| 5.4 | 0.33 | 25 | 0.0050 | 16 | 16 | 0.00 | 5.01 | 3.32 | 0.00 (16) |
| 5.4 | 0.33 | 50 | 0.0050 | 20 | 20 | 0.00 | 2.17 | 3.60 | 0.02 (16) |
| 5.4 | 0.33 | 100 | 0.0050 | 32 | 24 | 0.12 | 0.62 | 3.74 | 0.32 (16) |
| 5.4 | 1.33 | 0 | 0.0200 | 6 | 6 | 0.00 | 16.38 | 0.37 | 0.00 (6) |
| 5.4 | 1.33 | 25 | 0.0200 | 5 | 5 | 0.00 | 6.89 | 0.00 | 0.20 (6) |
| 5.4 | 1.33 | 50 | 0.0200 | 6 | 8 | 0.02 | 2.89 | 0.23 | 0.00 (6) |
| 5.4 | 1.33 | 100 | 0.0200 | 32 | 24 | 0.25 | 0.31 | 1.13 | 0.69 (6) |
| 5.4 | 5.32 | 0 | 0.0799 | 2 | 2 | 0.00 | 11.64 | 7.15 | 0.00 (2) |
| 5.4 | 5.32 | 25 | 0.0799 | 2 | 2 | 0.00 | 2.79 | 1.96 | 0.00 (2) |
| 5.4 | 5.32 | 50 | 0.0799 | 48 | 24 | 0.31 | 0.00 | 0.48 | 0.15 (2) |
| 5.4 | 5.32 | 100 | 0.0799 | 24 | 24 | 0.00 | 0.08 | 1.86 | 2.46 (2) |
| 10 | 0.33 | 0 | 0.0092 | 12 | 12 | 0.00 | 15.23 | 3.54 | 0.13 (10) |
| 10 | 0.33 | 25 | 0.0092 | 12 | 16 | 0.03 | 3.12 | 1.80 | 0.26 (10) |
| 10 | 0.33 | 50 | 0.0092 | 16 | 20 | 0.02 | 0.90 | 2.36 | 0.58 (10) |
| 10 | 0.33 | 100 | 0.0092 | 48 | 32 | 0.16 | 0.00 | 3.69 | 1.60 (10) |
| 10 | 1.33 | 0 | 0.0370 | 3 | 3 | 0.00 | 13.96 | 1.27 | 0.20 (4) |
| 10 | 1.33 | 25 | 0.0370 | 3 | 5 | 0.21 | 1.75 | 0.21 | 0.05 (4) |
| 10 | 1.33 | 50 | 0.0370 | 48 | 32 | 0.16 | 0.00 | 1.07 | 1.16 (4) |
| 10 | 1.33 | 100 | 0.0370 | 48 | 32 | 0.53 | 0.00 | 3.17 | 3.44 (4) |
| 10 | 5.32 | 0 | 0.1479 | 1 | 1 | 0.00 | 6.34 | 5.11 | 1.17 (2) |
| 10 | 5.32 | 25 | 0.1479 | 20 | 24 | 1.22 | 0.96 | 1.74 | 1.70 (2) |
| 10 | 5.32 | 50 | 0.1479 | 20 | 24 | 0.53 | 0.50 | 2.25 | 2.85 (2) |
| 10 | 5.32 | 100 | 0.1479 | 48 | 24 | 1.08 | 0.00 | 2.94 | 4.14 (2) |
| 18 | 0.33 | 0 | 0.0165 | 6 | 6 | 0.00 | 15.09 | 0.63 | 0.00 (6) |
| 18 | 0.33 | 25 | 0.0165 | 12 | 16 | 0.10 | 1.03 | 1.11 | 0.65 (6) |
| 18 | 0.33 | 50 | 0.0165 | 48 | 32 | 0.12 | 0.00 | 2.92 | 2.26 (6) |
| 18 | 0.33 | 100 | 0.0165 | 48 | 48 | 0.00 | 0.00 | 3.98 | 3.40 (6) |
| 18 | 1.33 | 0 | 0.0665 | 2 | 2 | 0.00 | 9.85 | 5.81 | 1.03 (3) |
| 18 | 1.33 | 25 | 0.0665 | 48 | 20 | 0.55 | 0.00 | 1.61 | 1.51 (3) |
| 18 | 1.33 | 50 | 0.0665 | 48 | 32 | 0.04 | 0.00 | 2.74 | 3.01 (3) |
| 18 | 1.33 | 100 | 0.0665 | 48 | 32 | 0.40 | 0.00 | 3.38 | 3.91 (3) |
| 18 | 5.32 | 0 | 0.2662 | 1 | 16 | 1.74 | 0.55 | 3.11 | 0.00 (1) |
| 18 | 5.32 | 25 | 0.2662 | 48 | 16 | 2.74 | 0.00 | 4.27 | 6.41 (1) |
| 18 | 5.32 | 50 | 0.2662 | 48 | 48 | 0.00 | 0.00 | 4.39 | 7.08 (1) |
| 18 | 5.32 | 100 | 0.2662 | 48 | 48 | 0.00 | 0.00 | 4.73 | 7.64 (1) |
| 30 | 0.33 | 0 | 0.0275 | 4 | 5 | 0.20 | 14.01 | 0.20 | 0.20 (5) |
| 30 | 0.33 | 25 | 0.0275 | 48 | 24 | 0.71 | 0.00 | 2.51 | 2.51 (5) |
| 30 | 0.33 | 50 | 0.0275 | 48 | 32 | 0.37 | 0.00 | 3.69 | 3.69 (5) |
| 30 | 0.33 | 100 | 0.0275 | 48 | 48 | 0.00 | 0.00 | 4.43 | 4.43 (5) |
| 30 | 1.33 | 0 | 0.1109 | 2 | 2 | 0.00 | 7.53 | 5.98 | 0.00 (2) |
| 30 | 1.33 | 25 | 0.1109 | 20 | 32 | 0.27 | 0.69 | 2.46 | 3.42 (2) |
| 30 | 1.33 | 50 | 0.1109 | 48 | 24 | 0.43 | 0.00 | 2.94 | 4.25 (2) |
| 30 | 1.33 | 100 | 0.1109 | 48 | 32 | 0.66 | 0.00 | 4.27 | 5.87 (2) |
| 30 | 5.32 | 0 | 0.4436 | 32 | 24 | 0.93 | 1.10 | 3.41 | 3.94 (1) |
| 30 | 5.32 | 25 | 0.4436 | 48 | 32 | 1.22 | 0.00 | 4.62 | 7.20 (1) |
| 30 | 5.32 | 50 | 0.4436 | 48 | 32 | 0.95 | 0.00 | 5.03 | 7.63 (1) |
| 30 | 5.32 | 100 | 0.4436 | 48 | 32 | 0.64 | 0.00 | 4.81 | 8.25 (1) |

## 3) Kayıp özeti (60 koşul)

| Kural | medyan | ortalama | en kötü |
| --- | --- | --- | --- |
| tasarım kuralı | 0.08 | 0.29 | 2.74 |
| her zaman L = 48 | 0.93 | 3.63 | 16.38 |
| her zaman L = 5 | 2.93 | 3.01 | 9.33 |
| makalenin kapalı formu | 0.50 | 1.84 | 8.25 |

## 4) Kalibrasyon tanılaması

R_floor 3.883 b/s/Hz, f_d 15.01 Hz; ψ'nin L'ler arası en büyük yayılımı 0.110.

## 5) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/tasarim_kurali/calibrate.py | kanal 12 | raw/calibration.json, raw/calibrate.log |
| python3 thesis_exp/tasarim_kurali/validate.py (70 dk) | kanal 13, bootstrap 0 | raw/validation.json, raw/validate.log |

## 6) Yorum (bulgulardan ayrı)

- **Ön kayıtlı üç hipotezin üçü de tuttu.** Kural hiç görmediği bir çekilişte ve hiç görmediği hızlarda (yalnızca 1.5 m/s'de kalibre edildi) test edildi. 60 koşulda medyan kayıp %0.08, ortalama %0.29, en kötü %2.74. Sabit seçimler çok daha kötü: "hep L = 48" ortalama %3.63 (en kötü %16.4), "hep L = 5" ortalama %3.01 (en kötü %9.3). Makalenin kapalı formu ortalama %1.84 (en kötü %8.3).
- **Kuralın katkısı, fazın tutulma süresini hesaba katması.** H3, W > 0 koşullarında kapalı forma göre +1.97 puan [+1.45, +2.49]. Kapalı form yalnızca anlık etkin hız için kurulmuştu.
- **En kötü koşullar güven ufkunun ötesinde.** Kaybın en yüksek olduğu koşulların hepsi büyük ΔT'de (5.32 ms) ya da yüksek hızda (18–30 km/h). Buralarda L = 48 ile devreye girme 255 ms sürer ve 200 ms'lik güven ufkunu aşar. Sınamada bu koşullarda L* = 48 çıkıyor; bunun nedeni büyük olasılıkla sabit saçıcıların bıraktığı korelasyon tabanı (Makale 2'nin sınırlılığı). Bu koşullardaki L* fiziksel olarak güvenilir değil. Kural yine de burada en fazla %2.74 kaybediyor.
- **Kalibrasyon yaklaşıklığı.** ψ'nin L'ler arası yayılımı 0.11 idi. Buna rağmen sınama kaybı küçük, çünkü bu yayılım R̂(L) eğrisinin tepesinin yerini az kaydırıyor.
- **Sınırlar:**
  - Pilot ve kestirim hatası yok. Ön kayıtta keşifsel olarak bırakıldı ve henüz koşulmadı.
  - Tek kanal modeli; bütün koşullar aynı kurgunun farklı hız ve sürelerinde.
  - Kural, ψ'yi aynı modelden kalibre ediyor. Bu yüzden başka bir kanal modeline taşınabilirliği ayrıca sınanmalı; geniş bant deneyinde G4 bunun bir parçası.
