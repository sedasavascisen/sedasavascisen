# Geniş bant OFDM — ön kayıtlı deney raporu

Rapor commit'i `f3652a6`, koşu commit'i `77d0b17`. Ön kayıt `ON_KAYIT.md` (sapmalar orada, koşudan önce). Seçim seed 12, rapor seed 11, 400 senaryo, 64 alt taşıyıcılı değerlendirme, min-kullanıcı hızı, Tanım 1 (kolun tam gecikmesinde). Fark ve GA'lar eşli bootstrap (2000, %95), seed 11 üzerinde.

## ⚠ En üstte: Makale 2'nin bulgusunu sınırlayan sonuç (Kural 10)

**G1 TUTMADI.** Makale 2'nin dar bant bulgusu "içsel optimum vardır; L = 48 anlamlı olarak kötüdür" geniş bantta genelleşmiyor: 24 (B, hız, K_opt) hücresinin yalnızca 7'sinde L = 48, L*'tan anlamlı olarak kötü. 6 hücrede L* tam olarak 48'dir, yani ızgaranın ucundadır.
Ön kayıt dışı duyarlılıkta (§4) seçim 200 ms'lik güven ufkuyla sınırlandırıldığında: 15/24 hücrede L*, ufuk içindeki en büyük L'dedir; ufkun içindeki en büyük L, 4 hücrede anlamlı olarak kötüdür.
Dar bant içsel optimumu (K_opt = 1) 20 MHz'de ve 1.5 m/s'de 50 MHz'de korunuyor. Daha geniş bantta ve 10 km/h'de optimum ızgaranın ucuna kayıyor ya da etkin hız eğrisi düzleşiyor. Bu tablo, makaledeki içsel optimum iddiasının dar bant ve bu kanal modeliyle sınırlı yazılması gerektiğini gösteriyor.

**G2 TUTTU ve ana sonuç bu:** geniş bantta optimizasyona alınan alt taşıyıcı sayısı ile süre arasındaki ödünleşim ölçülebiliyor. 20 MHz'de dar bant amaç fonksiyonu yetiyor; 100 MHz'de K_opt = 16 seçiliyor ve en iyi dar bant kolunu yaklaşık +0.28…+0.29 b/s/Hz geçiyor (§3). Bu hüküm 200 ms ufku içinde de değişmiyor (§4).

## 0) Önce okunmalı: sınırlar

- **CD ayarlanmadı.** Plan 1–8 tarama taraması öngörüyordu; ön kayıtta varsayılan taramaya indirildi (702.97 ms). Adam adım boyu 0.5 sabit. CLAUDE.md'deki zayıf taban çizgisi kuralı bakımından G3'ün hükmü bu yüzden zayıftır.
- **K_opt = 64 örneklem içidir** (değerlendirme ızgarasının kendisi); üst referans olarak okunmalı.
- **Güven ufku.** 200 ms'yi aşan gecikmeler (aşağıdaki tabloda) kanal modelinin korelasyon tabanının içine düşer; oradaki hızlar fiziksel olarak güvenilir değildir.
- Pilot, kestirim hatası ve ön kodlayıcı eskimesi yok (her alt taşıyıcıda taze ZF). Tek kanal modeli; genlik fc'de sabit.

## 1) Ölçülmüş gecikme (boş makine, tek iş parçacığı)

Yük: başlangıç 0.03, ölçüm öncesi 0.03, sonrası 1.00 (sonraki değer ölçümün kendi iş parçacığını içerir).

| K_opt | L=1 | L=4 | L=16 (ms, tur medyanı) | uydurma: sabit + adım (ms) | L = 48 gecikmesi (ms) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1.73 | 5.39 | 17.18 | +0.98 + 1.016·L | 50.1 |
| 4 | 3.40 | 12.38 | 40.35 | +1.73 + 2.426·L | 118.5 |
| 16 | 9.74 | 37.15 | 146.59 | +0.64 + 9.122·L | 438.8 |
| 64 | 31.46 | 139.96 | 593.33 | -7.93 + 37.550·L | 1794.8 |

SU-best-of 1.63 ms, CD 702.97 ms (dar bant, tek iş parçacıklı yeniden ölçüm; geniş bantta da fc'de optimize ettikleri için aynı).

## 2) Hipotez kararları

- **G1** (her (B, K_opt) için L = 48, L*'tan anlamlı düşük): 7/24 hücrede GA sıfırın altında → **TUTMADI** (tutmayan hücreler §3 tabloda)
- **G2** (20 MHz'de seçilen K_opt ≤ 4, 100 MHz'de ≥ 16, her iki hızda): seçilenler 20 MHz 1.5 m/s: K4-L4; 20 MHz 10 km/h: K1-L4; 50 MHz 1.5 m/s: K4-L4; 50 MHz 10 km/h: K4-L32; 100 MHz 1.5 m/s: K16-L32; 100 MHz 10 km/h: K16-L32 → 20 MHz kısmı **TUTTU**, 100 MHz kısmı **TUTTU**; bütün olarak **TUTTU**
- **G3** (CD, seçilen kolun anlamlı gerisinde, her B ve hızda): 6/6 → **TUTTU** (sınır: CD ayarlanmadı, §0)
- **G4** (keşifsel; dar bantta kalibre edilmiş tasarım kuralı, yalnızca ölçülen adım maliyetiyle): 24 hücrede kayıp medyan %0.81, ortalama %1.68, en kötü %7.97 (ayrıntı §5)

## 3) Hücre başına sonuç (seed 11)

| B | hız | seçilen (seed 12) | etkin hız | − SU-best-of [GA] | − en iyi dar bant [GA] | CD − seçilen [GA] |
| --- | --- | --- | --- | --- | --- | --- |
| 20 MHz | 1.5 m/s | K4-L4 | 5.398 | +0.448 [+0.396, +0.501] | +0.013 [-0.025, +0.050] (dar bant: K1-L8) | -0.473 [-0.557, -0.386] |
| 20 MHz | 10 km/h | K1-L4 | 5.218 | +0.272 [+0.217, +0.325] | +0.000 [+0.000, +0.000] (dar bant: K1-L4) | -0.365 [-0.459, -0.271] |
| 50 MHz | 1.5 m/s | K4-L4 | 5.136 | +0.341 [+0.298, +0.385] | +0.078 [+0.039, +0.115] (dar bant: K1-L12) | -0.227 [-0.301, -0.154] |
| 50 MHz | 10 km/h | K4-L32 | 5.119 | +0.326 [+0.256, +0.395] | +0.176 [+0.116, +0.236] (dar bant: K1-L24) | -0.300 [-0.382, -0.219] |
| 100 MHz | 1.5 m/s | K16-L32 | 5.228 | +0.496 [+0.420, +0.577] | +0.281 [+0.220, +0.342] (dar bant: K1-L48) | -0.331 [-0.390, -0.273] |
| 100 MHz | 10 km/h | K16-L32 | 5.188 | +0.457 [+0.378, +0.541] | +0.294 [+0.229, +0.362] (dar bant: K1-L24) | -0.385 [-0.444, -0.323] |

### K_opt başına içsel optimum (seed 11 argmax; G1)

| B | hız | K_opt | L* | gecikme (ms) | etkin hız | t = 0 hızı | L=48 − L* [GA] | L=48 kaybı (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20 MHz | 1.5 m/s | 1 | 8 | 9.4 | 5.385 | 5.545 | -0.304 [-0.369, -0.239] | 5.64 |
| 20 MHz | 1.5 m/s | 4 | 4 | 11.7 | 5.398 | 5.649 | -0.205 [-0.275, -0.135] | 3.81 |
| 20 MHz | 1.5 m/s | 16 | 32 | 292.8 ⚠ >200 ms | 5.118 | 6.386 | -0.069 [-0.138, +0.001] | 1.34 |
| 20 MHz | 1.5 m/s | 64 | 16 | 593.2 ⚠ >200 ms | 5.078 | 6.205 | -0.088 [-0.179, +0.003] | 1.74 |
| 20 MHz | 10 km/h | 1 | 5 | 6.4 | 5.218 | 5.406 | -0.186 [-0.256, -0.116] | 3.56 |
| 20 MHz | 10 km/h | 4 | 32 | 79.7 | 5.162 | 6.369 | -0.025 [-0.086, +0.034] | 0.48 |
| 20 MHz | 10 km/h | 16 | 32 | 292.8 ⚠ >200 ms | 5.075 | 6.386 | -0.012 [-0.084, +0.060] | 0.23 |
| 20 MHz | 10 km/h | 64 | 10 | 367.9 ⚠ >200 ms | 4.975 | 6.020 | -0.194 [-0.308, -0.075] | 3.90 |
| 50 MHz | 1.5 m/s | 1 | 16 | 17.5 | 5.061 | 5.250 | -0.065 [-0.114, -0.020] | 1.29 |
| 50 MHz | 1.5 m/s | 4 | 48 | 118.5 | 5.155 | 5.878 | +0.000 [+0.000, +0.000] | 0.00 |
| 50 MHz | 1.5 m/s | 16 | 32 | 292.8 ⚠ >200 ms | 5.181 | 6.016 | -0.039 [-0.100, +0.023] | 0.76 |
| 50 MHz | 1.5 m/s | 64 | 16 | 593.2 ⚠ >200 ms | 5.097 | 5.867 | -0.034 [-0.114, +0.042] | 0.67 |
| 50 MHz | 10 km/h | 1 | 48 | 50.1 | 4.976 | 5.375 | +0.000 [+0.000, +0.000] | 0.00 |
| 50 MHz | 10 km/h | 4 | 32 | 79.7 | 5.119 | 5.829 | -0.000 [-0.045, +0.046] | 0.00 |
| 50 MHz | 10 km/h | 16 | 48 | 438.8 ⚠ >200 ms | 5.128 | 6.073 | +0.000 [+0.000, +0.000] | 0.00 |
| 50 MHz | 10 km/h | 64 | 16 | 593.2 ⚠ >200 ms | 5.035 | 5.867 | -0.189 [-0.286, -0.091] | 3.75 |
| 100 MHz | 1.5 m/s | 1 | 16 | 17.5 | 4.952 | 5.035 | -0.005 [-0.042, +0.033] | 0.09 |
| 100 MHz | 1.5 m/s | 4 | 32 | 79.7 | 5.130 | 5.494 | -0.011 [-0.045, +0.022] | 0.22 |
| 100 MHz | 1.5 m/s | 16 | 32 | 292.8 ⚠ >200 ms | 5.228 | 5.786 | -0.040 [-0.094, +0.013] | 0.77 |
| 100 MHz | 1.5 m/s | 64 | 16 | 593.2 ⚠ >200 ms | 5.154 | 5.671 | -0.023 [-0.104, +0.052] | 0.45 |
| 100 MHz | 10 km/h | 1 | 48 | 50.1 | 4.934 | 5.139 | +0.000 [+0.000, +0.000] | 0.00 |
| 100 MHz | 10 km/h | 4 | 48 | 118.5 | 5.119 | 5.530 | +0.000 [+0.000, +0.000] | 0.00 |
| 100 MHz | 10 km/h | 16 | 48 | 438.8 ⚠ >200 ms | 5.192 | 5.826 | +0.000 [+0.000, +0.000] | 0.00 |
| 100 MHz | 10 km/h | 64 | 16 | 593.2 ⚠ >200 ms | 5.110 | 5.671 | -0.203 [-0.303, -0.110] | 3.98 |

## 4) Duyarlılık: seçim 200 ms ufkuyla sınırlı (ÖN KAYIT DIŞI, sonuçlar görüldükten sonra yazıldı)

Kaynak `sens200.py` → `raw/sens200.json`. Aynı veri, aynı seçim protokolü; yalnızca gecikmesi 200 ms'yi aşan kollar dışarıda.

| hücre | seçilen (≤ 200 ms) | gecikme (ms) | etkin hız | − en iyi dar bant [GA] |
| --- | --- | --- | --- | --- |
| 20MHz_1.5mps | K4-L4 | 11.7 | 5.398 | +0.013 [-0.023, +0.049] (K1-L8) |
| 20MHz_10kmh | K1-L4 | 5.3 | 5.218 | +0.000 [+0.000, +0.000] (K1-L4) |
| 50MHz_1.5mps | K4-L4 | 11.7 | 5.136 | +0.078 [+0.040, +0.116] (K1-L12) |
| 50MHz_10kmh | K4-L32 | 79.7 | 5.119 | +0.176 [+0.114, +0.240] (K1-L24) |
| 100MHz_1.5mps | K16-L20 | 183.4 | 5.187 | +0.239 [+0.188, +0.294] (K1-L48) |
| 100MHz_10kmh | K16-L20 | 183.4 | 5.172 | +0.277 [+0.219, +0.341] (K1-L24) |

G4, yalnızca L*'ı ufuk içinde olan 12 hücrede: kayıp medyan %0.91, en kötü %4.95.

## 5) G4 — tasarım kuralı geniş bant kollarında

| hücre | adım (ms) | kural L | L* (seed 11) | kayıp (%) |
| --- | --- | --- | --- | --- |
| 20MHz_1.5mps_K1 | 1.016 | 8 | 8 | 0.00 |
| 20MHz_1.5mps_K4 | 2.426 | 4 | 4 | 0.00 |
| 20MHz_1.5mps_K16 | 9.122 | 1 | 32 | 2.95 |
| 20MHz_1.5mps_K64 | 37.550 | 24 | 16 | 1.72 |
| 20MHz_10kmh_K1 | 1.016 | 3 | 5 | 0.60 |
| 20MHz_10kmh_K4 | 2.426 | 2 | 32 | 0.02 |
| 20MHz_10kmh_K16 | 9.122 | 24 | 32 | 0.54 |
| 20MHz_10kmh_K64 | 37.550 | 16 | 10 | 0.23 |
| 50MHz_1.5mps_K1 | 1.016 | 8 | 16 | 0.52 |
| 50MHz_1.5mps_K4 | 2.426 | 3 | 48 | 0.78 |
| 50MHz_1.5mps_K16 | 9.122 | 1 | 32 | 6.25 |
| 50MHz_1.5mps_K64 | 37.550 | 24 | 16 | 0.81 |
| 50MHz_10kmh_K1 | 1.016 | 3 | 48 | 1.51 |
| 50MHz_10kmh_K4 | 2.426 | 2 | 32 | 3.18 |
| 50MHz_10kmh_K16 | 9.122 | 24 | 48 | 0.81 |
| 50MHz_10kmh_K64 | 37.550 | 16 | 16 | 0.00 |
| 100MHz_1.5mps_K1 | 1.016 | 8 | 16 | 1.05 |
| 100MHz_1.5mps_K4 | 2.426 | 4 | 32 | 2.11 |
| 100MHz_1.5mps_K16 | 9.122 | 1 | 32 | 7.97 |
| 100MHz_1.5mps_K64 | 37.550 | 24 | 16 | 0.23 |
| 100MHz_10kmh_K1 | 1.016 | 3 | 48 | 3.00 |
| 100MHz_10kmh_K4 | 2.426 | 2 | 48 | 4.95 |
| 100MHz_10kmh_K16 | 9.122 | 24 | 48 | 1.00 |
| 100MHz_10kmh_K64 | 37.550 | 16 | 16 | 0.00 |

## 6) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/genis_bant/run.py --part timing | kanal 11, 20 senaryo | raw/timing.json, raw/timing.log |
| python3 thesis_exp/genis_bant/run.py --part curves (58 dk) | kanal 12 seçim, 11 rapor; bootstrap 0 | raw/results.json, raw/curves.json, raw/curves.log |
| python3 thesis_exp/genis_bant/g4.py | kanal 12 (R0), 11 (kayıp) | raw/g4.json, raw/g4.log |
| python3 thesis_exp/genis_bant/sens200.py (ön kayıt dışı) | yeni çekiliş yok; bootstrap common.boot | raw/sens200.json, raw/sens200.log |

## 7) Yorum (bulgulardan ayrı)

- **Tezin kapanışı için ne söylüyor.** Hesaplama gecikmesi geniş bantta da yöntem seçimini belirliyor, ama yeni bir eksende: kaç adım (L) atılacağının yanında, *kaç alt taşıyıcı üzerinden* optimize edileceği (K_opt) de bir zaman bütçesi kararı. 20 MHz'de ek alt taşıyıcının maliyeti kazancını aşıyor ve dar bant yetiyor. 100 MHz'de K_opt = 16'nın adım başına ~9 kat maliyeti, ~+0.28 b/s/Hz ile karşılığını veriyor. Bu, Makale 2'nin Sonuç bölümündeki "kalite ile zaman arasındaki ek ödünleşim" öngörüsünün ölçülmüş hâli.
- **Neden G1 tutmadı (hipotez, sınanmadı).** Etkin hız alt taşıyıcılar üzerinden ortalanınca eskimenin etkisi yumuşuyor. Ayrıca 10 km/h'de kanal birkaç on ms'de sabit saçıcıların bıraktığı korelasyon tabanına iniyor; bundan sonra ek bekleme pek bir şey kaybettirmiyor, ek adım ise t = 0 kalitesini artırmaya devam ediyor. Bu, 10 km/h'de L*'ın 1.5 m/s'dekinden *büyük* çıkmasını açıklayabilir (örneğin 50 MHz, K_opt = 1: 16 → 48). Taban modelin bir özelliği olduğu için bu davranış fiziksel bir sonuç olarak okunmamalı.
- **G4.** Dar bantta 1.5 m/s'de kalibre edilmiş kural, geniş bant kollarına yalnızca ölçülmüş adım maliyetiyle taşındı. Medyan kayıp %0.81, ancak kural bazı hücrelerde ψ'nin salınımlı bölgesinden yararlanıp tuhaf seçimler yapıyor (K_opt = 16'da 1.5 m/s'de L = 1, 10 km/h'de L = 24). Bu seçimlerin çoğu 200 ms ufkunun dışındaki bölgeye düşüyor. Ufuk içinde kalan hücrelerde en kötü kayıp %4.95.
- **G3, ayarlanmamış CD'ye karşı.** CD her hücrede seçilen kolun 0.23–0.47 b/s/Hz gerisinde; ama 702.97 ms'lik gecikmesi tek başına güven ufkunun dışında. Hüküm "varsayılan CD geride" olarak okunmalı, "CD geride" olarak değil.
- **Seçilen kollar ve güven ufku.** 100 MHz'deki seçilen kol K16-L32 (292.8 ms) ufkun dışında. Duyarlılık analizi ufuk içinde K16-L20'yi (183.4 ms) seçiyor ve dar bant farkı +0.24/+0.28 olarak kalıyor. Hüküm değişmiyor, ancak seçilen kol ufkun kenarında.
