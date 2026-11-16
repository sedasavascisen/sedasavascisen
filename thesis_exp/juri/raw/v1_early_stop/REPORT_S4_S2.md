# Jüri soruları 4 ve 2 — ön kayıtlı sonuçlar

Rapor commit'i `d7ac933`, koşu `bdcd899`. Ön kayıt `ON_KAYIT_S4_S2.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1, aynı oturumda ölçülmüş gecikmeler (`raw/arms.json` lat_meas). GA: eşli bootstrap 2000, %95.

## Kararlar (1.5 m/s)

- **S4-H1** (birlikte eskimede L = 48 < L*): **TUTTU**
- **S4-H2** (birlikte eskimede ayarlı CD < SU-best-of): **TUTTU**
- **S2-H1** (Clarke kanalında L = 48 < L* ve L* ≤ 200 ms): **TUTTU**
- **S2-H2** (Clarke kanalında ayarlı CD < SU-best-of): **TUTTU**

## Koşul × hız

| koşul | hız | L* (gecikme ms) | L* etkin hız | L=48 − L* [GA] | L=48 kaybı % | ayarlı CD − SU-best-of [GA] | seed 12'de en iyi kol |
| --- | --- | --- | --- | --- | --- | --- | --- |
| taze ön kodlayıcı (Makale 2) | 3 km/h | 12 (13.3) | 6.372 | -0.945 [-1.034, -0.862] | 14.8 | CD-1 -0.234 [-0.324, -0.143] | Adam-12 (6.372) |
| taze ön kodlayıcı (Makale 2) | 1.5 m/s | 6 (6.6) | 6.151 | -0.912 [-1.003, -0.823] | 14.8 | CD-2 -0.310 [-0.411, -0.215] | Adam-6 (6.151) |
| taze ön kodlayıcı (Makale 2) | 10 km/h | 4 (4.5) | 5.913 | -0.797 [-0.893, -0.704] | 13.5 | CD-2 -0.303 [-0.403, -0.204] | Adam-4 (5.913) |
| birlikte eskime (Soru 4) | 3 km/h | 1 (1.2) | 4.612 | -4.316 [-4.501, -4.124] | 93.6 | CD-1 -4.202 [-4.399, -4.010] | Adam-1 (4.612) |
| birlikte eskime (Soru 4) | 1.5 m/s | 1 (1.2) | 4.026 | -3.797 [-3.988, -3.621] | 94.3 | CD-1 -3.665 [-3.843, -3.479] | SU-average (4.472) |
| birlikte eskime (Soru 4) | 10 km/h | 1 (1.2) | 3.215 | -3.029 [-3.195, -2.847] | 94.2 | CD-1 -2.884 [-3.050, -2.724] | SU-average (4.263) |
| Clarke kanalı (Soru 2) | 3 km/h | 8 (8.8) | 6.219 | -2.012 [-2.111, -1.911] | 32.4 | CD-1 -0.765 [-0.856, -0.680] | Adam-8 (6.219) |
| Clarke kanalı (Soru 2) | 1.5 m/s | 4 (4.5) | 5.962 | -1.688 [-1.783, -1.589] | 28.3 | CD-1 -0.944 [-1.040, -0.846] | Adam-5 (5.960) |
| Clarke kanalı (Soru 2) | 10 km/h | 3 (3.4) | 5.726 | -1.544 [-1.637, -1.454] | 27.0 | CD-1 -1.024 [-1.112, -0.934] | Adam-3 (5.726) |

## Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/juri/s4_s2.py (1 dk) | kanal 12, 11; Clarke inovasyonu 1000·seed + hız indeksi | raw/s4_s2.json, raw/s4_s2.log |
| python3 thesis_exp/juri/analyze_s4_s2.py | bootstrap 0 | raw/s4_s2_summary.json |

## Yorum (bulgulardan ayrı)

- **Soru 2'ye yanıt: iç optimum, korelasyon tabanı olmayan kanalda da var.** Truong–Heath türü Clarke kanalında L* 3–8 adım (3.4–8.8 ms), yani güven ufkunun çok içinde. L = 48'in kaybı %27–32; bu, makaledeki kanaldaki %13.5–14.8'in yaklaşık iki katı. Sabit saçıcıların bıraktığı taban, kaybı küçültüyordu. Makaledeki sonuç modelin bir yapaylığı değil; muhafazakâr bir alt sınır.
- **Soru 4'e yanıt: ön kodlayıcı RIS'le birlikte eskirse her şey ~1 ms içinde çöküyor.** τ = 0'da iki koşul birebir aynı (5.412). 1.15 ms'de kanaldaki görece değişim yalnızca %0.5 (−23 dB), ama bayat ZF'nin girişim bastırması bozuluyor ve %25 kaybediliyor. 10 ms'de görece değişim %38'e çıkıyor ve hız 1.07'ye iniyor.
- Hipotezler biçimsel olarak tuttu, ama iç optimum burada yok: L* ızgaranın alt ucunda (L = 1). 1.5 m/s ve 10 km/h'de en iyi kol optimizasyonsuz SU-average.
- Sonuç: ön kodlayıcının her slotta (≤ 1 ms) tazelenmesi bir tercih değil, zorunluluk. Makale 2'nin "BS ön kodlayıcıyı güncel kanaldan yeniden hesaplar" varsayımı, iki ayrı zaman ölçeğinin tasarım gereği olarak yazılmalı: ön kodlayıcı hızlı döngüde, RIS fazı yavaş döngüde.
- **Arası.** Pilot gecikmesi ve kestirim hatasıyla tazelenen ön kodlayıcı ara durumdur ve `thesis_exp/p4/onkodlayici_pilot`, `onkodlayici_csi` deneylerinde zaten ölçüldü. Bu iki uç, o deneylerin yerini almaz.
