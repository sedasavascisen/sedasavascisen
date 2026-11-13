# Deney 4.5 — 1 ve 2 bitlik ayrık faz: L* ve yavaş çözücü (rapor)

> **DÜZELTME (denetim K3, 12 Kasım):** İlk sürüm etkin hızı, 40 ms'den sonra 50/75/100/150 ms'ye atlayan kaba bir ızgarada doğrusal interpolasyonla hesaplıyordu (koherans süresi ~28 ms). Bu yüzden 40 ms'den yavaş her kolun (Adam-32/48→q, dCD-2…8) değeri ±0.055 b/s/Hz'e kadar yanlıştı. Bu rapor her kolu **tam kendi gecikme anında** değerlendiren `run_exact.py`'den (`raw/results_exact.json`). İlk sürümün `raw/results.json` dosyası yalnızca dCD zamanlamalarının kaynağı olarak duruyor.

Rapor commit'i `4b1989e`. Ölçüm commit'leri: değerlendirme `1847597` (results_exact.json), dCD zamanlaması `98ddad9` (results.json). Yaşlanma kümesi (seed 11, 400 senaryo), seçim doğrulama çekilişinde (seed 12). Fazlar t=0 kanalından; sürekli kollar system.quantise_phase ile yuvarlandı (yuvarlama bedava sayıldı). dCD-s: baselines.coord_descent(bits=b, iters=s), gerçek 2^b ızgarasında. SU-best-of ve Adam-L gecikmeleri tek iş parçacıklı yeniden ölçümden (thesis_exp/infra; Adam-L SU-average başlangıcını içermiyor, etkisi p4/gecikme_muhasebesi). dCD gecikmeleri boş makinede ölçüldü (tek iş parçacığı, 10 senaryo × 5 tekrarın medyanı, 3 tur). İki tasarım: **lr0.5** (Adam adım boyu 0.5, makalenin yaşlanma kümesi değeri) ve **lr-val** (adım boyu her L ve bit için doğrulamada {0.25, 0.5, 0.75, 1.0} içinden seçildi; denetim U20). Eşli bootstrap 2000, %95 GA.

## 1 bit

dCD zamanlaması yük ortalaması: başlangıç 4.08, ölçüm öncesi 0.49, sonrası 0.76.

### Tasarım lr0.5

Doğrulamada seçilen kol: **dCD-1**. L* (test, yuvarlanmış Adam kolları): **Adam-5->q**. Adam-48→q'nun L*'a göre kaybı: %9.5.

Eşli farklar (test): dCD-1 - Adam-5->q: -0.0444 [-0.1145, +0.0243]

| Kol | Gecikme (ms) | lr | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 0.5 | 4.8250 | 4.8213 [4.5901, 5.0589] | -0.0414 [-0.1179, +0.0291] |
| SU-best-of->q | 1.63 |  | 4.8682 | 4.8627 [4.6381, 5.0961] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 0.5 | 5.0701 | 5.0547 [4.8267, 5.2943] | +0.1920 [+0.1222, +0.2614] |
| Adam-3->q | 4.14 | 0.5 | 5.1684 | 5.1337 [4.8905, 5.3663] | +0.2710 [+0.1996, +0.3437] |
| Adam-4->q | 5.55 | 0.5 | 5.1511 | 5.0975 [4.8676, 5.3278] | +0.2348 [+0.1650, +0.3053] |
| Adam-5->q | 6.82 | 0.5 | 5.2317 | 5.1575 [4.9086, 5.3830] | +0.2948 [+0.2214, +0.3722] |
| Adam-6->q | 8.09 | 0.5 | 5.2619 | 5.1394 [4.9069, 5.3803] | +0.2767 [+0.1954, +0.3539] |
| Adam-8->q | 10.63 | 0.5 | 5.3181 | 5.1053 [4.8787, 5.3324] | +0.2426 [+0.1628, +0.3295] |
| Adam-10->q | 13.30 | 0.5 | 5.4004 | 5.0467 [4.8241, 5.2869] | +0.1840 [+0.1014, +0.2719] |
| Adam-12->q | 15.96 | 0.5 | 5.3985 | 4.9599 [4.7195, 5.1997] | +0.0972 [+0.0076, +0.1855] |
| dCD-1 | 16.22 |  | 5.6913 | 5.1132 [4.8799, 5.3495] | +0.2504 [+0.1639, +0.3298] |
| Adam-16->q | 21.28 | 0.5 | 5.4740 | 4.8436 [4.6041, 5.0721] | -0.0191 [-0.1162, +0.0749] |
| Adam-20->q | 26.57 | 0.5 | 5.5063 | 4.8107 [4.5747, 5.0403] | -0.0520 [-0.1385, +0.0416] |
| dCD-2 | 28.71 |  | 5.9440 | 4.9270 [4.7038, 5.1622] | +0.0642 [-0.0369, +0.1544] |
| Adam-24->q | 31.85 | 0.5 | 5.5353 | 4.7629 [4.5265, 5.0029] | -0.0998 [-0.1861, -0.0114] |
| Adam-32->q | 42.42 | 0.5 | 5.5772 | 4.7615 [4.5301, 4.9893] | -0.1013 [-0.1932, -0.0100] |
| dCD-3 | 48.84 |  | 6.0206 | 4.8681 [4.6201, 5.1112] | +0.0054 [-0.0874, +0.1035] |
| dCD-4 | 61.88 |  | 6.0502 | 4.7945 [4.5636, 5.0220] | -0.0682 [-0.1657, +0.0309] |
| Adam-48->q | 63.91 | 0.5 | 5.5724 | 4.6672 [4.4300, 4.8996] | -0.1955 [-0.2966, -0.1017] |
| dCD-8 | 73.44 |  | 6.0729 | 4.8451 [4.6062, 5.0788] | -0.0176 [-0.1153, +0.0786] |

### Tasarım lr-val

Doğrulamada seçilen kol: **dCD-1**. L* (test, yuvarlanmış Adam kolları): **Adam-3->q**. Adam-48→q'nun L*'a göre kaybı: %9.1.

Eşli farklar (test): dCD-1 - Adam-5->q: -0.0175 [-0.0805, +0.0473]; dCD-1 - Adam-3->q: -0.0206 [-0.0933, +0.0509]

| Kol | Gecikme (ms) | lr | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 0.75 | 4.8785 | 4.8770 [4.6577, 5.1095] | +0.0143 [-0.0629, +0.0855] |
| SU-best-of->q | 1.63 |  | 4.8682 | 4.8627 [4.6162, 5.0888] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 0.5 | 5.0701 | 5.0547 [4.8123, 5.2956] | +0.1920 [+0.1201, +0.2632] |
| Adam-3->q | 4.14 | 0.5 | 5.1684 | 5.1337 [4.9053, 5.3620] | +0.2710 [+0.1979, +0.3413] |
| Adam-4->q | 5.55 | 0.5 | 5.1511 | 5.0975 [4.8641, 5.3411] | +0.2348 [+0.1657, +0.3027] |
| Adam-5->q | 6.82 | 0.25 | 5.2140 | 5.1306 [4.8944, 5.3544] | +0.2679 [+0.1971, +0.3391] |
| Adam-6->q | 8.09 | 0.25 | 5.2534 | 5.1326 [4.9075, 5.3617] | +0.2699 [+0.1970, +0.3452] |
| Adam-8->q | 10.63 | 0.25 | 5.2651 | 5.0544 [4.8185, 5.2757] | +0.1917 [+0.1105, +0.2675] |
| Adam-10->q | 13.30 | 1.0 | 5.2837 | 4.9793 [4.7550, 5.2038] | +0.1166 [+0.0269, +0.2025] |
| Adam-12->q | 15.96 | 1.0 | 5.3230 | 4.9287 [4.6870, 5.1702] | +0.0660 [-0.0203, +0.1552] |
| dCD-1 | 16.22 |  | 5.6913 | 5.1132 [4.8816, 5.3513] | +0.2504 [+0.1654, +0.3344] |
| Adam-16->q | 21.28 | 0.5 | 5.4740 | 4.8436 [4.6199, 5.0726] | -0.0191 [-0.1118, +0.0799] |
| Adam-20->q | 26.57 | 0.5 | 5.5063 | 4.8107 [4.5871, 5.0419] | -0.0520 [-0.1435, +0.0420] |
| dCD-2 | 28.71 |  | 5.9440 | 4.9270 [4.6991, 5.1504] | +0.0642 [-0.0311, +0.1582] |
| Adam-24->q | 31.85 | 0.5 | 5.5353 | 4.7629 [4.5299, 4.9821] | -0.0998 [-0.1914, -0.0095] |
| Adam-32->q | 42.42 | 0.5 | 5.5772 | 4.7615 [4.5276, 4.9911] | -0.1013 [-0.1916, -0.0122] |
| dCD-3 | 48.84 |  | 6.0206 | 4.8681 [4.6275, 5.1071] | +0.0054 [-0.0888, +0.1031] |
| dCD-4 | 61.88 |  | 6.0502 | 4.7945 [4.5620, 5.0283] | -0.0682 [-0.1624, +0.0282] |
| Adam-48->q | 63.91 | 0.5 | 5.5724 | 4.6672 [4.4312, 4.9054] | -0.1955 [-0.2914, -0.1047] |
| dCD-8 | 73.44 |  | 6.0729 | 4.8451 [4.6158, 5.0941] | -0.0176 [-0.1109, +0.0751] |

dCD zamanlaması (tur medyanları, ms): dCD-1: 16.2 (17.2, 16.2, 15.7); dCD-2: 28.7 (29.2, 28.7, 28.5); dCD-3: 48.8 (42.4, 48.8, 50.6); dCD-4: 61.9 (63.2, 61.9, 57.6); dCD-8: 73.4 (75.8, 73.4, 70.9)

## 2 bit

dCD zamanlaması yük ortalaması: başlangıç 0.76, ölçüm öncesi 0.46, sonrası 0.86.

### Tasarım lr0.5

Doğrulamada seçilen kol: **Adam-6->q**. L* (test, yuvarlanmış Adam kolları): **Adam-6->q**. Adam-48→q'nun L*'a göre kaybı: %14.1.

Eşli farklar (test): dCD-1 - Adam-5->q: -0.7367 [-0.8256, -0.6564]; dCD-1 - Adam-6->q: -0.7580 [-0.8312, -0.6814]

| Kol | Gecikme (ms) | lr | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 0.5 | 5.2574 | 5.2529 [5.0201, 5.4941] | +0.1358 [+0.0721, +0.1978] |
| SU-best-of->q | 1.63 |  | 5.1157 | 5.1171 [4.8839, 5.3482] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 0.5 | 5.5814 | 5.5613 [5.3196, 5.7896] | +0.4442 [+0.3842, +0.5060] |
| Adam-3->q | 4.14 | 0.5 | 5.7449 | 5.6987 [5.4503, 5.9324] | +0.5816 [+0.5195, +0.6407] |
| Adam-4->q | 5.55 | 0.5 | 5.8542 | 5.7623 [5.5218, 6.0052] | +0.6452 [+0.5806, +0.7135] |
| Adam-5->q | 6.82 | 0.5 | 5.9401 | 5.7976 [5.5542, 6.0335] | +0.6805 [+0.6146, +0.7458] |
| Adam-6->q | 8.09 | 0.5 | 6.0100 | 5.8190 [5.5844, 6.0464] | +0.7018 [+0.6314, +0.7728] |
| Adam-8->q | 10.63 | 0.5 | 6.1068 | 5.7184 [5.4798, 5.9643] | +0.6012 [+0.5232, +0.6784] |
| Adam-10->q | 13.30 | 0.5 | 6.2207 | 5.6514 [5.4185, 5.8849] | +0.5342 [+0.4582, +0.6155] |
| Adam-12->q | 15.96 | 0.5 | 6.2767 | 5.5403 [5.2912, 5.7764] | +0.4232 [+0.3428, +0.5034] |
| Adam-16->q | 21.28 | 0.5 | 6.3619 | 5.2990 [5.0598, 5.5366] | +0.1819 [+0.0958, +0.2613] |
| Adam-20->q | 26.57 | 0.5 | 6.4398 | 5.1709 [4.9532, 5.4104] | +0.0538 [-0.0353, +0.1468] |
| dCD-1 | 27.07 |  | 6.1407 | 5.0609 [4.8321, 5.3063] | -0.0562 [-0.1402, +0.0344] |
| Adam-24->q | 31.85 | 0.5 | 6.4847 | 5.1559 [4.9218, 5.4039] | +0.0388 [-0.0568, +0.1322] |
| Adam-32->q | 42.42 | 0.5 | 6.5781 | 5.1087 [4.8656, 5.3602] | -0.0084 [-0.1116, +0.0951] |
| dCD-2 | 56.27 |  | 6.4447 | 4.9473 [4.7115, 5.1889] | -0.1698 [-0.2661, -0.0762] |
| Adam-48->q | 63.91 | 0.5 | 6.6166 | 4.9978 [4.7601, 5.2346] | -0.1194 [-0.2241, -0.0135] |
| dCD-3 | 86.19 |  | 6.5383 | 4.9797 [4.7242, 5.2321] | -0.1374 [-0.2281, -0.0446] |
| dCD-4 | 109.34 |  | 6.5781 | 4.9515 [4.7208, 5.1865] | -0.1656 [-0.2604, -0.0702] |
| dCD-8 | 129.49 |  | 6.6053 | 4.9526 [4.7096, 5.1897] | -0.1645 [-0.2652, -0.0562] |

### Tasarım lr-val

Doğrulamada seçilen kol: **Adam-6->q**. L* (test, yuvarlanmış Adam kolları): **Adam-6->q**. Adam-48→q'nun L*'a göre kaybı: %14.2.

Eşli farklar (test): dCD-1 - Adam-5->q: -0.7367 [-0.8156, -0.6557]; dCD-1 - Adam-6->q: -0.7580 [-0.8362, -0.6795]

| Kol | Gecikme (ms) | lr | t=0 hızı | Etkin hız [%95 GA] | − SU-best-of→q [%95 GA] |
| --- | --- | --- | --- | --- | --- |
| Adam-1->q | 1.33 | 0.75 | 5.3003 | 5.2962 [5.0685, 5.5296] | +0.1791 [+0.1156, +0.2385] |
| SU-best-of->q | 1.63 |  | 5.1157 | 5.1171 [4.8778, 5.3425] | +0.0000 [+0.0000, +0.0000] |
| Adam-2->q | 2.74 | 0.75 | 5.6116 | 5.5951 [5.3622, 5.8352] | +0.4780 [+0.4162, +0.5384] |
| Adam-3->q | 4.14 | 0.5 | 5.7449 | 5.6987 [5.4652, 5.9298] | +0.5816 [+0.5201, +0.6433] |
| Adam-4->q | 5.55 | 0.5 | 5.8542 | 5.7623 [5.5351, 6.0065] | +0.6452 [+0.5806, +0.7134] |
| Adam-5->q | 6.82 | 0.5 | 5.9401 | 5.7976 [5.5661, 6.0444] | +0.6805 [+0.6138, +0.7460] |
| Adam-6->q | 8.09 | 0.5 | 6.0100 | 5.8190 [5.5927, 6.0575] | +0.7018 [+0.6286, +0.7739] |
| Adam-8->q | 10.63 | 0.75 | 6.0954 | 5.7174 [5.4753, 5.9512] | +0.6003 [+0.5283, +0.6737] |
| Adam-10->q | 13.30 | 0.75 | 6.2056 | 5.6602 [5.4320, 5.9030] | +0.5430 [+0.4646, +0.6243] |
| Adam-12->q | 15.96 | 0.75 | 6.2781 | 5.5532 [5.3157, 5.7739] | +0.4361 [+0.3513, +0.5129] |
| Adam-16->q | 21.28 | 0.5 | 6.3619 | 5.2990 [5.0507, 5.5312] | +0.1819 [+0.0977, +0.2653] |
| Adam-20->q | 26.57 | 0.75 | 6.4658 | 5.2299 [4.9968, 5.4688] | +0.1128 [+0.0183, +0.2035] |
| dCD-1 | 27.07 |  | 6.1407 | 5.0609 [4.8398, 5.3005] | -0.0562 [-0.1464, +0.0279] |
| Adam-24->q | 31.85 | 0.75 | 6.5038 | 5.1675 [4.9446, 5.3976] | +0.0504 [-0.0449, +0.1418] |
| Adam-32->q | 42.42 | 0.75 | 6.5570 | 5.1330 [4.8940, 5.3737] | +0.0158 [-0.0835, +0.1125] |
| dCD-2 | 56.27 |  | 6.4447 | 4.9473 [4.7061, 5.1944] | -0.1698 [-0.2644, -0.0768] |
| Adam-48->q | 63.91 | 0.25 | 6.5766 | 4.9956 [4.7578, 5.2358] | -0.1216 [-0.2147, -0.0271] |
| dCD-3 | 86.19 |  | 6.5383 | 4.9797 [4.7382, 5.2215] | -0.1374 [-0.2297, -0.0394] |
| dCD-4 | 109.34 |  | 6.5781 | 4.9515 [4.7109, 5.1841] | -0.1656 [-0.2629, -0.0695] |
| dCD-8 | 129.49 |  | 6.6053 | 4.9526 [4.7266, 5.1956] | -0.1645 [-0.2694, -0.0686] |

dCD zamanlaması (tur medyanları, ms): dCD-1: 27.1 (31.2, 27.1, 26.7); dCD-2: 56.3 (52.1, 72.0, 56.3); dCD-3: 86.2 (88.6, 86.2, 81.1); dCD-4: 109.3 (106.9, 109.3, 110.5); dCD-8: 129.5 (129.5, 132.4, 121.8)

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/ayrik_faz/run.py (dCD zamanlaması; boş makine) | kanal 11/12, bootstrap 0 | raw/results.json, raw/run.log |
| python3 thesis_exp/p4/ayrik_faz/run_3bit.py (3 bit: boş makinede dCD zamanlaması + tam gecikmede değerlendirme) | kanal 11/12, bootstrap 0 | raw/results_3bit.json, raw/run_3bit.log |
| python3 thesis_exp/p4/ayrik_faz/run_exact.py (tam gecikmede değerlendirme, iki lr tasarımı) | kanal 11 (test) / 12 (doğrulama), bootstrap 0 | raw/results_exact.json, raw/run_exact.log |

## Yorum (bulgulardan ayrı)

- **İçsel optimum ayrık fazda da var.** lr0.5 tasarımında yuvarlanmış Adam kollarında L* 1 bitte 5, 2 bitte 6. Adam-48→q, L*'a göre 1 bitte %9.5, 2 bitte %14.1 kaybediyor. (İlk sürümdeki %9.3 / %13.6 kaba ızgaradan geliyordu; denetim K3.) Adım boyu doğrulamada seçilince (lr-val) 1 bitte L* = 3 ve kayıp %9.1; 2 bitte L* = 6 ve kayıp %14.2.
- **1 bitte sıfır gecikmede dCD her kolu geçiyor, 2 bitte geçmiyor.**
  - 1 bit: dCD-8 6.07, en iyi Adam→q 5.58.
  - 2 bit: dCD-8 (6.61) Adam-48→q'nun (6.62) altında. dCD-1 (6.14) Adam-10…48→q'nun altında, Adam-8→q'nun (6.11) üstünde.
- **Etkin hızda 2 bitte yavaş çözücü kaybediyor.** dCD-2/3/4/8, SU-best-of→q'nun 0.137–0.170 b/s/Hz altında; dördünün de GA'sı sıfırın altında. dCD-1 ondan ayırt edilemiyor. En iyi Adam→q'ya (Adam-6→q) karşı dCD-1'in farkı −0.758 [−0.831, −0.681].
- **1 bitte tek taramalı dCD, en iyi yuvarlanmış Adam'la aynı düzeyde.** Doğrulamada seçilen kol dCD-1 (16.2 ms).
  - Testte dCD-1 − Adam-5→q = −0.044 [−0.114, +0.024] (lr0.5).
  - lr-val tasarımında dCD-1 − Adam-3→q = −0.021 [−0.093, +0.051].
  - İki GA da sıfırı içeriyor. Tarama sayısı arttıkça kazanç kayboluyor: dCD-4 ve dCD-8 SU-best-of→q'dan ayırt edilemiyor.
- **Tek-RIS'teki "1 bitte ayrık CD kazanıyor" sonucuyla ilişki:** Çok kullanıcılı yaşlanma kümesinde bu sonuç yalnızca tek taramada ve yalnızca berabere düzeyinde tekrarlanıyor.
- **Adım boyu (denetim U20):** lr-val, lr0.5'e göre hükmü değiştirmiyor. 1 bitte doğrulamada seçilen adım boyu bazı L'lerde testte daha düşük hız verdi (Adam-5→q 5.158 → 5.131); doğrulama ile test arasındaki fark, GA genişliğinin içinde.
- **Gecikme muhasebesi:** Adam-L→q gecikmesi SU-average başlangıcını (0.30 ms) içermiyor (common.adam_latency; makalenin kuralı). Başlangıç gecikmeye eklenince etkin hız kol başına 0.0001–0.021 b/s/Hz düşüyor; 1 bitte Adam-5→q için 0.0069. Bu, dCD-1 ile Adam-5→q arasındaki 0.044'lük farkı kapatmıyor; ama fark zaten anlamlı değil [p4/gecikme_muhasebesi/raw/results.json].
- **3 bit kapsam dışı:** İstem (Görev 4.5) 1/2 bit istiyordu; CLAUDE.md'nin ayrık faz maddesi 1/2/3 bit diyor. 3 bit, dCD zamanlaması boş makine gerektirdiği için eğitimler bittikten sonra eklenebilir; henüz koşulmadı.
- **Yuvarlama bedava sayıldı.** Sürekli kollar için bu iyimser bir varsayım ve dCD'nin aleyhine bir eğilim yaratır. Yuvarlamanın gerçek maliyeti 2^b'lik bir arama tablosu düzeyinde, ölçülmedi.
- **dCD zamanlaması sonrası yük ortalaması 0.76 / 0.86.** Bu değere ölçülen tek iş parçacıklı süreç de katkı veriyor. Ölçüm öncesi yük ortalaması 0.49 / 0.46 idi.
