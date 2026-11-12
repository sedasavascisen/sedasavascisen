# Deney 4.2 — Konum (LoS geometrisi) tabanlı faz (rapor)

Rapor commit'i `f413f63`, ölçüm commit'i `06fc9d2` (results.json). Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s). Faz yalnızca LoS geometrisinden (BS anten, RIS eleman ve kullanıcı konumları; genlik ~1/d, saçıcı/gölgelenme/örüntü yok, doğrudan yol 0) SU-average / SU-best-of ile hesaplandı; gerçek kanalda (taze ZF) değerlendirildi. Konum hatası σ (yatay eksenlerde, tohum 5). Konum edinme gecikmesi modellenmedi.

## 1) Bulgular

- channel SU-best-of: gecikme 1.63 ms, t=0 5.2762, etkin 5.2771 b/s/Hz
- channel Adam-6 (best on this set, optimistic): gecikme 8.09 ms, t=0 6.3162, etkin 6.0770 b/s/Hz

| Kol | σ (m) | Gecikme (ms) | t=0 hız | Etkin hız [%95 GA] | Kanal SU-best-of'a göre [%95 GA] | Her an konumdan yeniden (0–200 ms ort.) |
| --- | --- | --- | --- | --- | --- | --- |
| geom-avg | 0.0 | 0.30 | 4.4474 | 4.4477 [4.2224, 4.6710] | -0.8294 [-0.9125, -0.7486] | 4.3929 |
| geom-best | 0.0 | 1.63 | 4.4342 | 4.4354 [4.2048, 4.6696] | -0.8418 [-0.9253, -0.7659] | 4.3887 |
| geom-avg | 0.5 | 0.30 | 4.4324 | 4.4325 [4.2079, 4.6900] | -0.8446 [-0.9320, -0.7561] | 4.4009 |
| geom-best | 0.5 | 1.63 | 4.4469 | 4.4488 [4.2032, 4.6831] | -0.8283 [-0.9127, -0.7431] | 4.4018 |
| geom-avg | 1.0 | 0.30 | 4.4149 | 4.4149 [4.1945, 4.6457] | -0.8622 [-0.9490, -0.7756] | 4.4092 |
| geom-best | 1.0 | 1.63 | 4.4220 | 4.4183 [4.1830, 4.6391] | -0.8588 [-0.9481, -0.7727] | 4.4105 |

Rastgele faz bu kümede 4.072 b/s/Hz (results/mumiso_aging_stats.json).

## 2) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/konum_faz/run.py | kanal 11, konum hatası 5, bootstrap 0 | raw/results.json |

## 3) Yorum (bulgulardan ayrı)

- Bu iç mekân modelinde (20 saçıcı, LoS olasılığı 3GPP InH) yalnızca LoS geometrisine dayanan faz, kanal tabanlı SU-best-of'un 0.83–0.86 b/s/Hz altında kalıyor; konum hatası sonucu değiştirmiyor, çünkü sınır geometrinin kendisinde.
- Konumdan her an yeniden hesaplamak yaşlanmayı ortadan kaldırıyor ama düşük taban değeri yükseltmiyor.
