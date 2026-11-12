# Deney 4.1 — Kanal öngörüsü (rapor)

Commit `38b25bd`. Yaşlanma kümesi (seed 11, 400 senaryo, 1.5 m/s); seçim seed 12. Gecikmeler: tek iş parçacıklı yeniden ölçüm (thesis_exp/infra). Ek anlık görüntü başına ek pilot: 48 sembol = 3.43 / 1.71 / 0.86 ms (15 / 30 / 60 kHz); 2 noktalı öngörücü 1, 3 noktalılar 2 ek anlık görüntü ister. Bu süre tek-atış etkin hıza **eklenmedi** (anlık görüntüler t=0'dan önce alınıyor); havada geçen süre olarak ayrıca raporlanmalı.

## 1) Bulgular (önce kısıtlar)

- **Kanal modeli öngörüyü kayırıyor:** saçıcılar sabit, kullanıcılar düz çizgide yürüyor; kanal zamanın düzgün bir fonksiyonu. Dönüşlü yörünge yok (CLAUDE.md: öngörücü tasarım için önkoşul eksik).
- **Kestirim hatası e2 = 0** (her anlık görüntü): öngörüsüz en iyi kol Adam-6 = 6.0770 b/s/Hz.
  - lin2, Δ = 1.0 ms (1 ek anlık görüntü): Adam-10 = 6.3958; öngörüsüze göre +0.3187 [+0.2722, +0.3668]
  - lin3, Δ = 1.0 ms (2 ek anlık görüntü): Adam-10 = 6.3701; öngörüsüze göre +0.2930 [+0.2452, +0.3376]
  - quad3, Δ = 1.0 ms (2 ek anlık görüntü): Adam-12 = 6.4920; öngörüsüze göre +0.4150 [+0.3645, +0.4670]
  - kalman3, Δ = 1.0 ms (2 ek anlık görüntü; q/r=100): Adam-10 = 6.3918; öngörüsüze göre +0.3148 [+0.2655, +0.3645]
  - lin2, Δ = 2.0 ms (1 ek anlık görüntü): Adam-10 = 6.3716; öngörüsüze göre +0.2946 [+0.2492, +0.3388]
  - lin3, Δ = 2.0 ms (2 ek anlık görüntü): Adam-10 = 6.3511; öngörüsüze göre +0.2740 [+0.2287, +0.3184]
  - quad3, Δ = 2.0 ms (2 ek anlık görüntü): Adam-12 = 6.4680; öngörüsüze göre +0.3910 [+0.3429, +0.4417]
  - kalman3, Δ = 2.0 ms (2 ek anlık görüntü; q/r=100): Adam-12 = 6.3798; öngörüsüze göre +0.3028 [+0.2531, +0.3525]
  - lin2, Δ = 5.0 ms (1 ek anlık görüntü): Adam-10 = 6.3260; öngörüsüze göre +0.2490 [+0.2050, +0.2944]
  - lin3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-8 = 6.2664; öngörüsüze göre +0.1894 [+0.1465, +0.2308]
  - quad3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-12 = 6.4039; öngörüsüze göre +0.3268 [+0.2744, +0.3808]
  - kalman3, Δ = 5.0 ms (2 ek anlık görüntü; q/r=100): Adam-10 = 6.3647; öngörüsüze göre +0.2877 [+0.2439, +0.3333]
- **Kestirim hatası e2 = 0.01** (her anlık görüntü): öngörüsüz en iyi kol Adam-6 = 5.6111 b/s/Hz.
  - lin2, Δ = 1.0 ms (1 ek anlık görüntü): Adam-1 = 4.6755; öngörüsüze göre -0.9356 [-1.0194, -0.8538]
  - lin3, Δ = 1.0 ms (2 ek anlık görüntü): Adam-2 = 4.8754; öngörüsüze göre -0.7357 [-0.8163, -0.6626]
  - quad3, Δ = 1.0 ms (2 ek anlık görüntü): Adam-1 = 4.3237; öngörüsüze göre -1.2874 [-1.3870, -1.1948]
  - kalman3, Δ = 1.0 ms (2 ek anlık görüntü; q/r=0.1): Adam-2 = 4.8770; öngörüsüze göre -0.7342 [-0.8095, -0.6566]
  - lin2, Δ = 2.0 ms (1 ek anlık görüntü): Adam-2 = 4.8418; öngörüsüze göre -0.7693 [-0.8513, -0.6932]
  - lin3, Δ = 2.0 ms (2 ek anlık görüntü): Adam-3 = 5.1641; öngörüsüze göre -0.4470 [-0.5162, -0.3823]
  - quad3, Δ = 2.0 ms (2 ek anlık görüntü): Adam-1 = 4.6478; öngörüsüze göre -0.9633 [-1.0459, -0.8807]
  - kalman3, Δ = 2.0 ms (2 ek anlık görüntü; q/r=0.001): Adam-3 = 5.1606; öngörüsüze göre -0.4505 [-0.5214, -0.3812]
  - lin2, Δ = 5.0 ms (1 ek anlık görüntü): Adam-5 = 5.1894; öngörüsüze göre -0.4217 [-0.4950, -0.3501]
  - lin3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-6 = 5.5137; öngörüsüze göre -0.0974 [-0.1540, -0.0445]
  - quad3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-2 = 4.9162; öngörüsüze göre -0.6949 [-0.7737, -0.6174]
  - kalman3, Δ = 5.0 ms (2 ek anlık görüntü; q/r=0.01): Adam-6 = 5.4525; öngörüsüze göre -0.1586 [-0.2140, -0.1017]
- **Kestirim hatası e2 = 0.1** (her anlık görüntü): öngörüsüz en iyi kol Adam-8 = 4.9443 b/s/Hz.
  - lin2, Δ = 1.0 ms (1 ek anlık görüntü): Adam-1 = 4.1772; öngörüsüze göre -0.7671 [-0.8722, -0.6690]
  - lin3, Δ = 1.0 ms (2 ek anlık görüntü): Adam-1 = 4.3575; öngörüsüze göre -0.5868 [-0.6719, -0.5002]
  - quad3, Δ = 1.0 ms (2 ek anlık görüntü): SU-best-of = 4.1114; öngörüsüze göre -0.8329 [-0.9362, -0.7338]
  - kalman3, Δ = 1.0 ms (2 ek anlık görüntü; q/r=1): Adam-1 = 4.3340; öngörüsüze göre -0.6103 [-0.6967, -0.5275]
  - lin2, Δ = 2.0 ms (1 ek anlık görüntü): Adam-1 = 4.3289; öngörüsüze göre -0.6154 [-0.7031, -0.5301]
  - lin3, Δ = 2.0 ms (2 ek anlık görüntü): Adam-3 = 4.4321; öngörüsüze göre -0.5122 [-0.5996, -0.4228]
  - quad3, Δ = 2.0 ms (2 ek anlık görüntü): SU-best-of = 4.1590; öngörüsüze göre -0.7853 [-0.8841, -0.6864]
  - kalman3, Δ = 2.0 ms (2 ek anlık görüntü; q/r=0.01): Adam-3 = 4.4423; öngörüsüze göre -0.5020 [-0.5900, -0.4158]
  - lin2, Δ = 5.0 ms (1 ek anlık görüntü): Adam-3 = 4.5106; öngörüsüze göre -0.4337 [-0.5161, -0.3533]
  - lin3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-3 = 4.7416; öngörüsüze göre -0.2027 [-0.2793, -0.1229]
  - quad3, Δ = 5.0 ms (2 ek anlık görüntü): Adam-1 = 4.4082; öngörüsüze göre -0.5361 [-0.6227, -0.4512]
  - kalman3, Δ = 5.0 ms (2 ek anlık görüntü; q/r=0.001): Adam-3 = 4.7376; öngörüsüze göre -0.2067 [-0.2832, -0.1333]

## 2) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/kanal_ongoru/run.py [--e2 0.01 / 0.1] | kanal 11 (rapor) / 12 (seçim), gürültü 3/4, bootstrap 0 | raw/results.json, raw/results_e2_*.json |

## 3) Yorum (bulgulardan ayrı)

- Gürültüsüz anlık görüntülerle öngörü belirgin kazanç sağlıyor ve en iyi adım sayısını sağa kaydırıyor (öngörü gecikmenin bedelini kısmen telafi ediyor).
- %1 kestirim hatasıyla (−20 dB) her öngörücü öngörüsüz Adam'ın altına düşüyor: fark alma gürültüyü büyütüyor. Bu modelde öngörü kazancı, kestirimin pratikte ulaşamayacağı bir doğruluğa bağlı.
