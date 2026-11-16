# Geniş bant OFDM — deney planı ve süre tahmini (16 Kasım 2026)

**Dayanak:**
- `LITERATUR_GENIS_BANT.md` §Boşluk: "gecikme bütçesi → en uygun iterasyon → eskimiş CSI ile etkin hız" zinciri geniş bantta, hareketli kullanıcıyla ve ölçülmüş duvar saatiyle kurulmamış.
- `results/wideband_feasibility.json` (tek kullanıcı, statik):
  - gecikme yayılımı ~21 ns; %50 uyum bant genişliği 9–23 MHz;
  - merkez frekanstaki fazın, alt taşıyıcı başına optimuma göre hız kaybı 20 MHz'de %3.1, 100 MHz'de %7.1;
  - tek geniş bant fazının kaybı 20 MHz'de %2.0, 100 MHz'de %4.1;
  - adım maliyeti alt taşıyıcı sayısıyla doğrusal.
- Makale 2 Sonuç: "Our next step is wideband OFDM operation, where beam squint makes the best phase depend on frequency and adds a further trade-off between quality and time."

## 1) Ana soru

Tek bir RIS faz vektörü bütün alt taşıyıcılara hizmet eder. Optimizasyon K_opt alt taşıyıcı üzerinden yapılır: K_opt = 1 merkez frekans demek, yani ucuz ama bant kenarında kötü. K_opt büyüdükçe adım pahalılaşır, faz bütün banda daha iyi uyar. **Hareketli kullanıcıda, ölçülmüş gecikmeyle hangi K_opt ve kaç adım (L) en iyi etkin hızı verir?** Bu, "kalite ile zaman arasındaki ek ödünleşim"in ölçümüdür.

## 2) Kurgu

| Öğe | Değer |
| --- | --- |
| Kanal | Yaşlanma kurgusu (4 kullanıcı, 8 BS anteni, 32 elemanlı RIS, 20 saçıcı, 3 GHz). Alt taşıyıcılar `MobileMuMisoChannel.generate(freq_offsets_hz=…)` ile: aynı çekilişler, yalnızca faz yeniden değerlendirilir (bit-bit uyumu `scripts/wideband_bitidentity_check.py` ile sınanmış). |
| Bant genişliği B | 20, 50, 100 MHz |
| Değerlendirme | K_eval = 64 eşit aralıklı alt taşıyıcı. Kullanıcı hızı = alt taşıyıcılar üzerinden ortalama log2(1 + SINR_f); ölçüt min-kullanıcı. Her alt taşıyıcıda ZF (taze, makalenin varsayımı). |
| Optimizasyon kolları | SU-average ve SU-best-of (fc'de, kapalı form); Adam-L, aynı amaç fonksiyonunun K_opt ∈ {1, 4, 16, 64} alt taşıyıcı üzerinden soft-min (β = 8) yüzeyinde; CD (fc'de, `baselines.coord_descent`, 1–8 tarama). |
| L | {1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48} |
| Hız | 1.5 m/s ve 10 km/h |
| Etkin hız | Tanım 1: kolun tam gecikmesinde. Her kol için t = 0 ile τ'dan oluşan ayrı ızgara; interpolasyon yok. Ek olarak W = 50 ms penceresi, 0.5 ms hizalı ızgarada. |
| Gecikme | Boş makinede, tek iş parçacığı, tek senaryo: K_opt ∈ {1, 4, 16, 64} için Adam adımı, SU-best-of ve CD (b = sürekli). 20 senaryo × 20 tekrar × 3 tur; yük öncesi ve sonrası kaydedilir. |
| Seçim / rapor | Adım boyu ve en iyi (K_opt, L) seed 12'de seçilir, seed 11'de raporlanır. Eşli bootstrap 2000, %95. |

## 3) Hipotezler (ön kayıt; koşudan önce commit'lenir)

- **G1:** Her (B, K_opt) için içsel optimum vardır: L = 48, L*'tan anlamlı olarak düşüktür.
- **G2:** Geniş bant uyumu ile zaman ödünleşimi: 20 MHz'de doğrulamada seçilen K_opt ≤ 4, 100 MHz'de ≥ 16. Tutmazsa nasıl tutmadığı raporlanır.
- **G3:** Yavaş çözücü (CD), her B'de seçilen hızlı kolun anlamlı olarak gerisindedir.
- **G4 (tasarım kuralıyla bağ):** ΔT(K_opt) ölçülen adım süresi alınarak, x = ΔT·f_d kuralının (tasarım kuralı çalışması) öngördüğü L ile ölçülen L* arasındaki kayıp raporlanır. Keşifsel.

## 4) Süre tahmini

| İş | Tahmin |
| --- | --- |
| Gecikme ölçümü (boş makine) | ~30 dk |
| Kanal ve eğriler: 2 hız × 3 B × 4 K_opt × 14 L × 2 çekiliş | ~3–4 saat (2 iş parçacığı). Her kol için 2 zaman noktalı ayrı ızgara; W = 50 ms için 101 noktalı ayrı ızgara. |
| CD kolları | ~20 dk |
| Rapor, denetim turu | ~2 saat |
| **Toplam** | **~1 gün** |

20 Kasım öncesine sığar. Tasarım kuralı sınaması bitmeden başlatılmaz, çünkü ikisi aynı işlemciyi paylaşır.

## 5) Sınırlar (önceden)

- **Genlik yaklaşımı:** Genlik ve yol kaybı fc'de tutulur, alt taşıyıcıda yalnızca faz değişir. B/fc ≤ %3.3 olduğu için bu kabul edilebilir.
- **Kapsam dışı:** Alt taşıyıcı başına pilot ve kestirim hatası bu planda yok; dar bant sonuçlarıyla aynı varsayımlar korunur.
- **Gecikme:** Python ve tek iş parçacığı. Mutlak süreler donanıma bağlıdır; x ekseni bunu taşır.
