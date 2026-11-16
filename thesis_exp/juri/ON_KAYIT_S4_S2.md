# Ön kayıt — Jüri soruları 4 ve 2 (16 Kasım 2026)

Bu dosya, `s4_s2.py` koşulmadan önce commit'lenir. Hiçbir sonuç görülmedi.

## Ortak kurgu

- **Kanal ve seçim:** yaşlanma kurgusu (`common.Aging`). Seçim seed 12, rapor seed 11, 400 senaryo.
- **Hızlar:** 3 km/h, 1.5 m/s (5.4 km/h) ve 10 km/h.
- **Kollar:**
  - SU-average;
  - SU-best-of;
  - Adam-L, L ∈ {1, …, 48} (14 değer), adım boyu 0.5;
  - ayarlanmış CD: s ∈ {1, …, 8} arasından, seed 12'de her koşul için seçilir.
- **Gecikmeler:** `raw/arms.json`'daki ölçülmüş küme (`lat_meas`).
- **Ölçüt:** Tanım 1, tam gecikmede, interpolasyon yok. L*, Makale 2'deki gibi seed 11'deki argmax; seed 12 seçimi de ayrıca raporlanır.
- **İstatistik:** eşli bootstrap 2000, %95 (`common.boot`).

## Soru 4 — Ön kodlayıcı da eskirse

**Koşul "birlikte eskime":** BS, t = 0 CSI'ı ile hem θ'yı hem de ZF ön kodlayıcıyı W0 = ZF(H_eff(0; θ)) hesaplar. İkisi τ anında birlikte devreye girer. Hız, H_eff(τ; θ) ile W0 kullanılarak hesaplanır; MMSE düzenleyicisi aynı, güç aynı. Karşılaştırma koşulu, Makale 2'deki taze ön kodlayıcı.

- **S4-H1:** 1.5 m/s'de birlikte eskimede L = 48, L*'ın anlamlı olarak altında (GA üst sınırı < 0).
- **S4-H2:** 1.5 m/s'de birlikte eskimede ayarlanmış CD, SU-best-of'un anlamlı olarak gerisinde.
- **Raporlanır:** her hızda L* (taze ve birlikte eskime), seçilen kol, L = 48 kaybı.

## Soru 2 — Korelasyon tabanı olmayan kanal

**Koşul "Clarke":** Truong & Heath (2013) türü eskime modeli. G(t) = ρ(t)·G(0) + √(1 − ρ²)·E_G ve h_d(t) = ρ(t)·h_d(0) + √(1 − ρ²)·E_h; burada ρ(t) = J0(2π f_d t).
- E'nin her girdisi CN(0, p) dağılımlı. p, aynı senaryonun t = 0 kanalında o kullanıcının elemanlar (ya da antenler) üzerinden ortalama gücü.
- E, senaryo başına tek bir çekiliştir ve bütün t'ler için aynıdır. Tohum: 1000·seed + hız indeksi.
- F sabittir. Ön kodlayıcı taze.
- Korelasyon sıfıra iner (J0 salınımları dışında). Sabit saçıcıların bıraktığı taban yoktur.

Hipotezler:
- **S2-H1:** 1.5 m/s'de Clarke kanalında L = 48, L*'ın anlamlı olarak altında, ve L*'ın gecikmesi ≤ 200 ms.
- **S2-H2:** 1.5 m/s'de ayarlanmış CD, SU-best-of'un anlamlı olarak gerisinde.
- **Raporlanır:** her hızda L* ve seçilen kol.

## Sınırlar (önceden)

- Clarke inovasyonu elemanlar arasında bağımsız (i.i.d.); dizi korelasyonu yok. Saçılma zengin bir NLoS varsayımına karşılık gelir ve LoS bileşenini de eskitir. Bu nedenle mevcut modelin tersi yönde bir uç olarak okunmalı.
- Birlikte eskimede pilot süresi yok; t = 0 CSI kusursuz.
