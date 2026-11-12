# Deney 4.5 — 1 ve 2 bitlik ayrık faz: L* ve yavaş çözücü (rapor)

Commit `81b07dd`. Yaşlanma kümesi (seed 11, 400 senaryo), seçim doğrulama çekilişinde (seed 12). Fazlar t=0 kanalından; sürekli kollar system.quantise_phase ile yuvarlandı (yuvarlama bedava sayıldı). dCD-s: baselines.coord_descent(bits=b, iters=s), gerçek 2^b ızgarasında. SU-best-of ve Adam-L gecikmeleri tek iş parçacıklı yeniden ölçümden (thesis_exp/infra); dCD gecikmeleri bu deneyde boş makinede ölçüldü (tek iş parçacığı, tek senaryo, 10 senaryo × 5 tekrarın medyanı, 3 tur). Karşılaştırmalar SU-best-of→q'ya karşı eşli bootstrap (2000, %95 GA).

## 1 bit

Yük ortalaması: başlangıç 4.08, ölçüm öncesi 0.49, sonrası 0.76. Doğrulamada seçilen kol: **dCD-1**. L* (test, yuvarlanmış Adam kolları): **Adam-5->q**. Adam-48→q'nun L*'a göre kaybı: %9.3.

| Kol | Gecikme (ms) | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 4.8250 | 4.8212 [4.5900, 5.0588] | -0.0415 [-0.1180, +0.0291] |
| SU-best-of->q | 1.63 | 4.8682 | 4.8627 [4.6380, 5.0961] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 5.0701 | 5.0546 [4.8266, 5.2942] | +0.1919 [+0.1221, +0.2613] |
| Adam-3->q | 4.14 | 5.1684 | 5.1336 [4.8904, 5.3662] | +0.2709 [+0.1996, +0.3437] |
| Adam-4->q | 5.55 | 5.1511 | 5.0977 [4.8679, 5.3278] | +0.2350 [+0.1650, +0.3054] |
| Adam-5->q | 6.82 | 5.2317 | 5.1574 [4.9085, 5.3829] | +0.2947 [+0.2213, +0.3722] |
| Adam-6->q | 8.09 | 5.2619 | 5.1394 [4.9068, 5.3803] | +0.2767 [+0.1953, +0.3539] |
| Adam-8->q | 10.63 | 5.3181 | 5.1053 [4.8787, 5.3324] | +0.2426 [+0.1628, +0.3294] |
| Adam-10->q | 13.30 | 5.4004 | 5.0468 [4.8241, 5.2869] | +0.1840 [+0.1014, +0.2720] |
| Adam-12->q | 15.96 | 5.3985 | 4.9599 [4.7196, 5.1997] | +0.0972 [+0.0076, +0.1855] |
| dCD-1 | 16.22 | 5.6913 | 5.1132 [4.8800, 5.3496] | +0.2505 [+0.1640, +0.3299] |
| Adam-16->q | 21.28 | 5.4740 | 4.8437 [4.6042, 5.0722] | -0.0191 [-0.1161, +0.0750] |
| Adam-20->q | 26.57 | 5.5063 | 4.8108 [4.5747, 5.0404] | -0.0519 [-0.1385, +0.0416] |
| dCD-2 | 28.71 | 5.9440 | 4.9270 [4.7038, 5.1622] | +0.0643 [-0.0368, +0.1544] |
| Adam-24->q | 31.85 | 5.5353 | 4.7629 [4.5265, 5.0029] | -0.0998 [-0.1860, -0.0114] |
| Adam-32->q | 42.42 | 5.5772 | 4.7585 [4.5299, 4.9851] | -0.1042 [-0.1942, -0.0141] |
| dCD-3 | 48.84 | 6.0206 | 4.8642 [4.6183, 5.1127] | +0.0015 [-0.0908, +0.0995] |
| dCD-4 | 61.88 | 6.0502 | 4.8498 [4.6270, 5.0708] | -0.0130 [-0.1020, +0.0791] |
| Adam-48->q | 63.91 | 5.5724 | 4.6785 [4.4476, 4.9137] | -0.1842 [-0.2698, -0.1049] |
| dCD-8 | 73.44 | 6.0729 | 4.8497 [4.6097, 5.0838] | -0.0130 [-0.1104, +0.0823] |

dCD zamanlaması (tur medyanları, ms): dCD-1: 16.2 (17.2, 16.2, 15.7); dCD-2: 28.7 (29.2, 28.7, 28.5); dCD-3: 48.8 (42.4, 48.8, 50.6); dCD-4: 61.9 (63.2, 61.9, 57.6); dCD-8: 73.4 (75.8, 73.4, 70.9)

## 2 bit

Yük ortalaması: başlangıç 0.76, ölçüm öncesi 0.46, sonrası 0.86. Doğrulamada seçilen kol: **Adam-6->q**. L* (test, yuvarlanmış Adam kolları): **Adam-6->q**. Adam-48→q'nun L*'a göre kaybı: %13.6.

| Kol | Gecikme (ms) | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 5.2574 | 5.2528 [5.0238, 5.4836] | +0.1357 [+0.0716, +0.1958] |
| SU-best-of->q | 1.63 | 5.1157 | 5.1171 [4.8746, 5.3540] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 5.5814 | 5.5612 [5.3147, 5.7986] | +0.4441 [+0.3843, +0.5089] |
| Adam-3->q | 4.14 | 5.7449 | 5.6986 [5.4645, 5.9417] | +0.5815 [+0.5196, +0.6435] |
| Adam-4->q | 5.55 | 5.8542 | 5.7625 [5.5275, 6.0141] | +0.6454 [+0.5783, +0.7106] |
| Adam-5->q | 6.82 | 5.9401 | 5.7975 [5.5594, 6.0346] | +0.6805 [+0.6159, +0.7468] |
| Adam-6->q | 8.09 | 6.0100 | 5.8189 [5.5862, 6.0536] | +0.7018 [+0.6340, +0.7724] |
| Adam-8->q | 10.63 | 6.1068 | 5.7184 [5.4858, 5.9411] | +0.6013 [+0.5204, +0.6792] |
| Adam-10->q | 13.30 | 6.2207 | 5.6514 [5.4093, 5.8905] | +0.5343 [+0.4553, +0.6176] |
| Adam-12->q | 15.96 | 6.2767 | 5.5403 [5.3058, 5.7872] | +0.4233 [+0.3459, +0.5057] |
| Adam-16->q | 21.28 | 6.3619 | 5.2992 [5.0674, 5.5467] | +0.1821 [+0.1019, +0.2627] |
| Adam-20->q | 26.57 | 6.4398 | 5.1710 [4.9418, 5.4080] | +0.0539 [-0.0355, +0.1426] |
| dCD-1 | 27.07 | 6.1407 | 5.0610 [4.8373, 5.2921] | -0.0561 [-0.1427, +0.0333] |
| Adam-24->q | 31.85 | 6.4847 | 5.1560 [4.9069, 5.3956] | +0.0389 [-0.0544, +0.1366] |
| Adam-32->q | 42.42 | 6.5781 | 5.1054 [4.8506, 5.3423] | -0.0117 [-0.1127, +0.0835] |
| dCD-2 | 56.27 | 6.4447 | 4.9836 [4.7499, 5.2141] | -0.1335 [-0.2173, -0.0446] |
| Adam-48->q | 63.91 | 6.6166 | 5.0257 [4.7960, 5.2524] | -0.0914 [-0.1784, -0.0040] |
| dCD-3 | 86.19 | 6.5383 | 4.9555 [4.7272, 5.1978] | -0.1616 [-0.2474, -0.0761] |
| dCD-4 | 109.34 | 6.5781 | 4.9575 [4.7268, 5.2028] | -0.1596 [-0.2508, -0.0607] |
| dCD-8 | 129.49 | 6.6053 | 4.9892 [4.7501, 5.2304] | -0.1279 [-0.2175, -0.0414] |

dCD zamanlaması (tur medyanları, ms): dCD-1: 27.1 (31.2, 27.1, 26.7); dCD-2: 56.3 (52.1, 72.0, 56.3); dCD-3: 86.2 (88.6, 86.2, 81.1); dCD-4: 109.3 (106.9, 109.3, 110.5); dCD-8: 129.5 (129.5, 132.4, 121.8)

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/ayrik_faz/run.py | kanal 11 (test) / 12 (doğrulama), bootstrap 0 | raw/results.json, raw/run.log |

## Yorum (bulgulardan ayrı)

- **İçsel optimum ayrık fazda da var.** Yuvarlanmış Adam kollarında L* = 5 (1 bit) ve 6 (2 bit); Adam-48→q, L*'a göre %9.3 (1 bit) ve %13.6 (2 bit) kaybediyor. Sürekli fazdaki tek iş parçacıklı L* = 6 ile aynı bölgede.
- **Yavaş çözücü kaybetmeye devam ediyor, 1 bitte istisnasıyla.** dCD t=0 hızında her kolu geçiyor (1 bit dCD-8: 6.07, en iyi Adam→q 5.57; 2 bit dCD-8: 6.61, Adam-48→q 6.62 ile aynı). Etkin hızda 2 bitte her dCD kolu SU-best-of→q'nun altında ya da ondan ayırt edilemez; bunların dördünde GA sıfırı dışlıyor.
- **1 bit istisnası:** doğrulamada seçilen kol dCD-1 (16.2 ms, tek tarama). Testte dCD-1 = 5.113, Adam-5→q = 5.157. İkisinin SU-best-of→q'ya karşı GA'ları örtüşüyor. dCD-1 ile Adam-5→q arasındaki eşli fark bu betikte hesaplanmadı; bu nedenle aralarında sıralama iddia edilemez. Yani 1 bitte tek taramalı ayrık CD, yuvarlanmış Adam'ın en iyisiyle aynı düzeyde.
- **Tek-RIS'teki "1 bitte ayrık CD kazanıyor" sonucuyla ilişki:** çok kullanıcılı yaşlanma kümesinde bu sonuç yalnızca tek taramada ve yalnızca berabere düzeyinde tekrarlanıyor. Tarama sayısı arttıkça gecikme kazancı yiyor.
- **Yuvarlama bedava sayıldı.** Sürekli kollar için bu iyimser bir varsayım, dCD'nin aleyhine bir eğilim yaratır; ama yuvarlamanın gerçek maliyeti 2^b'lik bir arama tablosu düzeyinde, ölçülmedi.
- **Ölçüm sonrası yük ortalaması 0.76 / 0.86.** Bu değere ölçülen tek iş parçacıklı süreç de katkı veriyor. Ölçüm öncesi yük ortalaması 0.49 / 0.46 idi.
