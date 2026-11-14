# Makale 2 ızgara kontrolü — interpolasyon mu, tam gecikme mi? (rapor)

Rapor commit'i `98ed4bd`, ölçüm commit'i `98ed4bd`. Makale 2'nin yaşlanma taraması ve karşılaştırması (scripts/mumiso_aging_sweep.py, mumiso_aging.py) etkin hızı düzensiz bir ızgarada (0, 1, 2, 5, 7.5, 10, 13.3, 15, 19.6, 20, 26.6, 28.2, 35, 42.9, 50, 75, 100, 150, 200, 500, 1500, 5600 ms) doğrusal interpolasyonla hesaplıyor. Burada aynı kurulumla (seed 11, 400 senaryo) her kol tam kendi gecikmesinde de değerlendirildi. Izgara üzerindeki değerler yayımlanmış `results/mumiso_aging_sweep_repro.json` ile en fazla 2.1e-06 farkla aynı (aynı senaryolar). Eşli bootstrap 2000, %95 GA.

## Gecikme kümesi: paper

L* (bu betiğin adım kümesi, 5 dahil): interpolasyonla Adam-5, tam Adam-4. Adam-48'in L*'a göre kaybı: interpolasyonla %13.99, tam %14.20.

| Kol | Gecikme (ms) | İnterpolasyon | Tam | Tam − interp. [%95 GA] |
| --- | --- | --- | --- | --- |
| SU-best-of | 0.05 | 5.2763 | 5.2764 | +0.0001 [+0.0000, +0.0001] |
| Adam-1 | 1.66 | 5.4056 | 5.4060 | +0.0004 [+0.0003, +0.0005] |
| Adam-2 | 3.33 | 5.7462 | 5.7517 | +0.0055 [+0.0048, +0.0064] |
| Adam-4 | 6.65 | 5.9798 | 5.9843 | +0.0045 [+0.0029, +0.0070] |
| Adam-5 | 8.31 | 5.9820 | 5.9838 | +0.0018 [+0.0011, +0.0025] |
| Adam-6 | 9.98 | 5.9700 | 5.9701 | +0.0001 [+0.0000, +0.0001] |
| Adam-8 | 13.30 | 5.8486 | 5.8486 | +0.0000 [+0.0000, +0.0000] |
| Adam-10 | 16.62 | 5.6832 | 5.6763 | -0.0069 [-0.0101, -0.0039] |
| Adam-12 | 19.95 | 5.5149 | 5.5149 | -0.0001 [-0.0001, -0.0000] |
| Adam-16 | 26.60 | 5.3244 | 5.3244 | +0.0000 [+0.0000, +0.0000] |
| Adam-20 | 33.25 | 5.2762 | 5.2701 | -0.0061 [-0.0120, -0.0007] |
| Adam-24 | 39.90 | 5.2824 | 5.2745 | -0.0080 [-0.0168, +0.0008] |
| Adam-32 | 53.20 | 5.2300 | 5.2027 | -0.0272 [-0.0486, -0.0061] |
| Adam-48 | 79.80 | 5.1451 | 5.1344 | -0.0107 [-0.0409, +0.0170] |
| CD | 1500.00 | 4.9212 | 4.9212 | +0.0000 [+0.0000, +0.0000] |
| PGA | 5600.00 | 4.6673 | 4.6673 | +0.0000 [+0.0000, +0.0000] |

| Karşılaştırma | İnterpolasyon [%95 GA] | Tam [%95 GA] |
| --- | --- | --- |
| SU-best-of - CD | +0.3551 [+0.2403, +0.4696] | +0.3552 [+0.2386, +0.4695] |
| SU-best-of - Adam-48 | +0.1312 [+0.0374, +0.2216] | +0.1420 [+0.0426, +0.2392] |
| SU-best-of - Adam-20 | +0.0001 [-0.0863, +0.0918] | +0.0062 [-0.0799, +0.0992] |

## Gecikme kümesi: rerun

L* (bu betiğin adım kümesi, 5 dahil): interpolasyonla Adam-6, tam Adam-6. Adam-48'in L*'a göre kaybı: interpolasyonla %14.40, tam %14.93.

| Kol | Gecikme (ms) | İnterpolasyon | Tam | Tam − interp. [%95 GA] |
| --- | --- | --- | --- | --- |
| Adam-1 | 1.33 | 5.4076 | 5.4080 | +0.0004 [+0.0003, +0.0005] |
| SU-best-of | 1.63 | 5.2768 | 5.2772 | +0.0004 [+0.0002, +0.0005] |
| Adam-2 | 2.74 | 5.7573 | 5.7615 | +0.0042 [+0.0037, +0.0049] |
| Adam-4 | 5.55 | 6.0216 | 6.0236 | +0.0020 [+0.0003, +0.0031] |
| Adam-5 | 6.82 | 6.0521 | 6.0562 | +0.0041 [+0.0028, +0.0064] |
| Adam-6 | 8.09 | 6.0753 | 6.0771 | +0.0018 [+0.0011, +0.0024] |
| Adam-8 | 10.63 | 6.0223 | 6.0227 | +0.0004 [-0.0021, +0.0021] |
| Adam-10 | 13.30 | 5.9049 | 5.9049 | +0.0000 [-0.0000, +0.0000] |
| Adam-12 | 15.96 | 5.7707 | 5.7641 | -0.0066 [-0.0095, -0.0041] |
| Adam-16 | 21.28 | 5.5244 | 5.5040 | -0.0204 [-0.0273, -0.0143] |
| Adam-20 | 26.57 | 5.3627 | 5.3622 | -0.0005 [-0.0007, -0.0003] |
| Adam-24 | 31.85 | 5.3332 | 5.3287 | -0.0044 [-0.0122, +0.0036] |
| Adam-32 | 42.42 | 5.2924 | 5.2900 | -0.0024 [-0.0049, +0.0001] |
| Adam-48 | 63.91 | 5.2007 | 5.1696 | -0.0312 [-0.0750, +0.0124] |
| CD | 702.97 | 4.9903 | 5.0156 | +0.0252 [-0.0655, +0.1180] |
| PGA | 4950.35 | 4.7125 | 4.7050 | -0.0075 [-0.1027, +0.0870] |

| Karşılaştırma | İnterpolasyon [%95 GA] | Tam [%95 GA] |
| --- | --- | --- |
| SU-best-of - CD | +0.2865 [+0.1910, +0.3779] | +0.2616 [+0.1470, +0.3727] |
| SU-best-of - Adam-48 | +0.0761 [-0.0058, +0.1657] | +0.1076 [+0.0146, +0.2012] |
| SU-best-of - Adam-20 | -0.0859 [-0.1777, +0.0096] | -0.0850 [-0.1772, +0.0064] |

Komut: `python3 thesis_exp/p4/izgara_kontrol/run.py` (betik koşudan önce commit'lendi). Ham çıktı: raw/results.json, raw/run.log.

## Yorum (bulgulardan ayrı)

- **Makale 2'nin hükümleri interpolasyondan etkilenmiyor.** Tam değerle interpolasyon arasındaki fark kol başına en fazla 0.031 b/s/Hz (yeniden ölçülen gecikmelerle Adam-48; ızgarada 50 → 75 ms boşluğu).
- **Makalenin kendi adım kümesiyle (2, 4, 6, 8, …, 48) ve makaledeki gecikmelerle:**
  - En iyi adım sayısı tam değerde de L* = 4; en iyi etkin hız 5.9798 → 5.9843.
  - L=48'in kaybı %13.96 → %14.20; makale "%14" diyor.
  - Bu betik L=5'i de içeriyor; o zaman interpolasyonla L* = 5, tam değerde L* = 4. Makalenin metnindeki "4–6" aralığı her iki durumda da tutuyor.
- **Yeniden ölçülen tek iş parçacıklı gecikmelerle:** L* = 6 (değişmiyor). L48 kaybı %14.40 → %14.93. SU-best-of − Adam-48 farkı 0.076 [−0.006, +0.166] → 0.108 [+0.015, +0.201]; tam değerde GA sıfırı dışlıyor.
- **SU-best-of − CD (yeniden ölçülen gecikmeler):** 0.287 → 0.262; GA sıfırın üstünde kalıyor. CD'nin 703 ms'si ızgarada 500 ile 1500 ms arasına düşüyor. Ancak bu gecikmeler, mumiso_aging.py'deki TRUST_MS = 200 ms güven sınırının ötesinde; bu bölgede model zaten iyimser.
- **Öneri (tez yazımı için):** Tez tablolarında etkin hızın tam gecikmede hesaplanmış değeri kullanılmalı (bu betik ya da `p4/gecikme_muhasebesi`). Makale metnindeki %14 ve L* = 4 bu kontrolle tutarlı.
