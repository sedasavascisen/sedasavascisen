# Jüri soruları 4 ve 2 — ön kayıtlı sonuçlar

Rapor commit'i `1267d39`, koşu `1267d39`. Ön kayıt `ON_KAYIT_S4_S2.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1, aynı oturumda ölçülmüş gecikmeler (`raw/arms.json` lat_meas). GA: eşli bootstrap 2000, %95.

## Kararlar (1.5 m/s)

- **S4-H1** (birlikte eskimede L = 48 < L*): **TUTTU** — **biçimsel**: L* = 1 ızgaranın alt ucunda (sansürlü), iç optimum yok; seed 12'de en iyi kol SU-average (4.472), SU-best-of (3.872) bile onun gerisinde. Ön kodlayıcı da eskirse optimizasyonun kendisi değer kaybediyor.
- **S4-H2** (birlikte eskimede ayarlı CD < SU-best-of): **TUTTU** — aynı nitelendirme: her iki kol da optimizasyonsuz SU-average'ın gerisinde.
- **S2-H1** (Clarke kanalında L = 48 < L* ve L* ≤ 200 ms): **TUTTU**
- **S2-H2** (Clarke kanalında ayarlı CD < SU-best-of): **TUTTU**

## Koşul × hız

| koşul | hız | L* seed 11 (gecikme ms) | L seçimi seed 12 | L* etkin hız | L=48 − L* [GA] | L=48 kaybı % | ayarlı CD − SU-best-of [GA] | seed 12'de en iyi kol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| taze ön kodlayıcı (Makale 2) | 3 km/h | 12 (13.3) | 12 | 6.372 | -0.945 [-1.034, -0.862] | 14.8 | CD-1 -0.238 [-0.328, -0.150] | Adam-12 (6.372) |
| taze ön kodlayıcı (Makale 2) | 1.5 m/s | 6 (6.6) | 6 | 6.151 | -0.912 [-1.003, -0.823] | 14.8 | CD-2 -0.265 [-0.365, -0.174] | Adam-6 (6.151) |
| taze ön kodlayıcı (Makale 2) | 10 km/h | 4 (4.5) | 4 | 5.913 | -0.797 [-0.893, -0.704] | 13.5 | CD-3 -0.269 [-0.363, -0.172] | Adam-4 (5.913) |
| birlikte eskime (Soru 4) | 3 km/h | 1 (1.2) | 1 | 4.612 | -4.316 [-4.501, -4.124] | 93.6 | CD-1 -4.204 [-4.400, -4.012] | Adam-1 (4.612) |
| birlikte eskime (Soru 4) | 1.5 m/s | 1 (1.2) | 1 | 4.026 | -3.797 [-3.988, -3.621] | 94.3 | CD-1 -3.665 [-3.843, -3.480] | SU-average (4.472) |
| birlikte eskime (Soru 4) | 10 km/h | 1 (1.2) | 1 | 3.215 | -3.029 [-3.195, -2.847] | 94.2 | CD-1 -2.883 [-3.049, -2.722] | SU-average (4.263) |
| Clarke kanalı (Soru 2) | 3 km/h | 8 (8.8) | 8 | 6.219 | -2.012 [-2.111, -1.911] | 32.4 | CD-1 -0.778 [-0.869, -0.693] | Adam-8 (6.219) |
| Clarke kanalı (Soru 2) | 1.5 m/s | 4 (4.5) | 5 | 5.962 | -1.688 [-1.783, -1.589] | 28.3 | CD-1 -0.959 [-1.056, -0.861] | Adam-5 (5.960) |
| Clarke kanalı (Soru 2) | 10 km/h | 3 (3.4) | 3 | 5.726 | -1.544 [-1.637, -1.454] | 27.0 | CD-1 -1.030 [-1.117, -0.941] | Adam-3 (5.726) |

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/s4_s2.py (1 dk) | kanal 12, 11; Clarke inovasyonu 1000·seed + hız indeksi | raw/s4_s2.json, raw/s4_s2.log |
| python3 thesis_exp/juri/s4_sanity.py | kanal 11 | raw/s4_sanity.json |
| python3 thesis_exp/juri/analyze_s4_s2.py | bootstrap 0 | raw/s4_s2_summary.json |

## Yorum (bulgulardan ayrı)

- **Soru 2'ye yanıt: iç optimum, korelasyon tabanı olmayan kanalda da var.**
  - Truong–Heath türü Clarke kanalında L* 3–8 adım (3.4–8.8 ms), yani güven ufkunun çok içinde. L = 48'in kaybı %27–32; bu oturumdaki taze ön kodlayıcı koşusunda bu kayıp %13.5–14.8.
  - İç optimum, sabit saçıcılı modelin bir yapaylığı değil: iki karşıt uç modelde de var.
  - Kaybın büyüklüğü ise modele bağlı. Bu iki uç, gerçek bir kanal için bir alt sınır kanıtı sayılmaz.
- **Soru 4'e yanıt: ön kodlayıcı RIS ile birlikte eskirse her şey ~1 ms içinde çöküyor** (`s4_sanity.py` → `raw/s4_sanity.json`).
  - τ = 0'da iki koşul birebir aynı (5.412).
  - 1.15 ms'de kanaldaki görece değişim yalnızca %0.53 (−23 dB). Bu kadarı bile bayat ZF'nin girişim bastırmasını bozuyor: hız 5.409'dan 4.030'a iniyor.
  - 10 ms'de görece değişim %38 ve hız 1.067.
- **Hipotezler biçimsel olarak tuttu, ama iç optimum yok.**
  - L* ızgaranın alt ucunda (L = 1); bu sansürlü bir değer.
  - 1.5 m/s ve 10 km/h'de en iyi kol optimizasyonsuz SU-average.
  - Sonuç: ön kodlayıcıyı her slotta (≤ 1 ms) tazelemek bir tercih değil, zorunluluk.
  - Makale 2'nin "BS ön kodlayıcıyı güncel kanaldan yeniden hesaplar" varsayımı, iki ayrı zaman ölçeğinin tasarım gereği olarak yazılmalı: ön kodlayıcı hızlı döngüde, RIS fazı yavaş döngüde.
- **Ara durum.** Pilot gecikmesi ve kestirim hatasıyla tazelenen ön kodlayıcı, `thesis_exp/p4/onkodlayici_pilot` ve `onkodlayici_csi` deneylerinde zaten ölçüldü. Bu iki uç o deneylerin yerini almaz.
- **Sınır.** Clarke kolu, t = 0 kanalının hızdan bağımsız olduğunu varsayıyor; bu, `common.Aging`'in ızgaradan bağımsızlık özelliğine dayanıyor.
