# Deney 4.3 — Ön kodlayıcı tazeleme pilotlarının ücretlendirilmesi (rapor)

> **DÜZELTME — bu raporun pilot ücretli sayıları yanlı.** Tazeleme anları mutlak 0.1 ms ızgarasına yuvarlanıyor; yuvarlamanın yönü kolun gecikmesine bağlı. SU-best-of (1.63 ms) aşağı yuvarlandığı için her örneği 0.1 ms fazla eskimiş bir W ile ölçüldü; Adam-6 (8.09 ms) yukarı yuvarlandı. Bu da SU-best-of'u cezalandırıp aradaki farkı şişirdi. Kolun kendi devreye girme anına hizalanmış ızgarayla düzeltilmiş değerler (thesis_exp/p4/onkodlayici_siralama, R doğrulamada seçildi):
>
> | Kol | Taze W | 15 kHz | 30 kHz | 60 kHz | Hiç tazelenmeyen |
> | --- | --- | --- | --- | --- | --- |
> | SU-best-of | 4.9108 | 3.3852 (R 2 ms) | 3.8108 (R 1 ms) | 4.1255 (R 1 ms) | 0.7606 |
> | Adam-6 | 5.2248 | 3.5385 (R 2 ms) | 4.0132 (R 1 ms) | 4.3447 (R 1 ms) | 0.7639 |
>
> Aşağıdaki tablolar ilk (yanlı) koşunun kaydı olarak bırakıldı; taze W ve hiç tazelenmeyen W sütunları yuvarlamadan etkilenmiyor (ikincisi ≤0.01 b/s/Hz). Bütün kolların sıralaması için onkodlayici_siralama/REPORT.md.

Rapor commit'i `f413f63`, ölçüm commit'i `98ddad9` (results.json). Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s), 0.1 ms ızgara. Faz t=0'da hesaplanıp kolun gecikmesinde devreye alınıyor; ZF ön kodlayıcı her R ms'de bir, o anın (kusursuz) etkin kanal kestiriminden yeniden hesaplanıyor ve arada eski haliyle kullanılıyor. Her tazeleme 4 pilot sembolü (kullanıcı başına bir), veri yok: veri oranı 1 − t_p/R ile ücretlendirildi. Ortalama penceresi devreye almadan sonraki 50 ms.

## 1) Bulgular

**SU-best-of:** makalenin varsayımı (her an taze ve bedava W) 4.9104; hiç tazelenmeyen W 0.7516 b/s/Hz.

| R (ms) | 15kHz hız [taze'ye göre] | 30kHz hız [taze'ye göre] | 60kHz hız [taze'ye göre] |
| --- | --- | --- | --- |
| 0.5 | 1.981 [-2.930] | 3.306 [-1.604] | 3.962 [-0.949] |
| 1.0 | 3.096 [-1.814] | 3.718 [-1.193] | 4.025 [-0.886] |
| 2.0 | 3.303 [-1.607] | 3.579 [-1.331] | 3.716 [-1.195] |
| 5.0 | 2.758 [-2.152] | 2.842 [-2.068] | 2.883 [-2.027] |
| 10.0 | 2.059 [-2.852] | 2.089 [-2.821] | 2.104 [-2.806] |
| 20.0 | 1.503 [-3.407] | 1.514 [-3.396] | 1.520 [-3.391] |
| 50.0 | 0.747 [-4.163] | 0.749 [-4.161] | 0.751 [-4.160] |
| en iyi R | 2 ms | 1 ms | 1 ms |

**Adam-6:** makalenin varsayımı (her an taze ve bedava W) 5.2252; hiç tazelenmeyen W 0.7649 b/s/Hz.

| R (ms) | 15kHz hız [taze'ye göre] | 30kHz hız [taze'ye göre] | 60kHz hız [taze'ye göre] |
| --- | --- | --- | --- |
| 0.5 | 2.144 [-3.081] | 3.579 [-1.647] | 4.288 [-0.938] |
| 1.0 | 3.342 [-1.883] | 4.013 [-1.213] | 4.344 [-0.881] |
| 2.0 | 3.537 [-1.688] | 3.833 [-1.392] | 3.979 [-1.246] |
| 5.0 | 2.903 [-2.323] | 2.991 [-2.234] | 3.035 [-2.191] |
| 10.0 | 2.135 [-3.090] | 2.166 [-3.059] | 2.182 [-3.043] |
| 20.0 | 1.544 [-3.681] | 1.555 [-3.670] | 1.561 [-3.664] |
| 50.0 | 0.760 [-4.465] | 0.763 [-4.463] | 0.764 [-4.461] |
| en iyi R | 2 ms | 1 ms | 1 ms |

## 2) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/onkodlayici_pilot/run.py | kanal 11, bootstrap 0 | raw/results.json |

## 3) Yorum (bulgulardan ayrı)

- Makale 2'nin bütün etkin hızları 'taze ve bedava ön kodlayıcı' varsayımına dayanıyor (makalede sınırlılık olarak yazılı). Pilot süresi ücretlendirilince en iyi tazeleme periyodu 1–2 ms çıkıyor ve hız belirgin düşüyor: ZF girişim sıfırlaması kanal değişimine çok duyarlı.
- Bu, mutlak hızları ve muhtemelen öğrenilen/klasik farklarının büyüklüğünü etkiler; yöntem sıralamasının bu ücretlendirme altında değişip değişmediği ayrı bir deneyle sınanmalı (bu deney yalnızca iki fazla yapıldı).
