# Ön kayıt — Jüri soruları 3 ve 1 (16 Kasım 2026)

Bu dosya, `timing.py` ve `arms.py` koşulmadan önce commit'lenir. Hiçbir sonuç görülmedi.

## Ortak kurgu

- **Kanal:** yaşlanma kurgusu (`thesis_exp/p4/common.Aging`, Makale 2 ile aynı). Seçim seed 12, rapor seed 11. Hızlar 1.5 m/s ve 10 km/h. Her biri 400 senaryo.
- **Ölçüt:** Tanım 1, yani min-kullanıcı hızı kolun tam gecikmesinde. Her gecikme kendi zaman noktasında doğrudan değerlendirilir, interpolasyon yok.
- **Kollar** (fazlar t = 0 kanalında):
  - SU-average;
  - SU-best-of;
  - Adam-L, L ∈ {1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48}, adım boyu 0.5, SU-average'tan başlar;
  - CD-s, s ∈ {1, …, 8} tarama (`baselines.coord_descent`, iters = s);
  - uzun koşulu Adam (`baselines.pga`).
- **Ölçülmüş gecikme:**
  - `thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json` (tek iş parçacığı, boş makine). Adam-L için `common.adam_latency`.
  - CD-s (s = 1…8) ile derlenmiş CD (`cd_fast.py`, numba; doğrudan ve rank-1 artımlı) bu çalışmada aynı protokolle ölçülür (`timing.py`): seed 11, tek senaryo, tek iş parçacığı, 5 tur medyanı, yük öncesi/sonrası.
  - Kontrol olarak `adam1`, `adam48` ve torch CD yeniden ölçülür; rerun dosyasından sapma raporlanır.
- **Derlenmiş CD'nin geçerliliği:** küçük örnekte (n = 24) torch CD ile fazların %75–92'si birebir aynı, ortalama hız farkı ≤ 0.003. Fark, kayan nokta eşitliklerinden geliyor. Etkin hız hesabında torch CD fazları kullanılır; derlenmiş sürümden yalnızca gecikme alınır.
- **İstatistik:** eşli bootstrap 2000, %95 GA (`common.boot`, tohum 0).

## Soru 3 — "Ryu ve ark.'tan farkınız yalnızca milisaniye mi?"

**FLOP modeli** (analitik; `arms.py` içinde formül olarak yazılır). Bir hız değerlendirmesi E = 8·(KNT + 2K²T + K³ + KT) gerçel FLOP. Burada K = 4 kullanıcı, N = 32 eleman, T = 8 BS anteni. Kollar:

| Kol | FLOP |
| --- | --- |
| Adam adımı | 3E (ileri + geri) |
| SU-average | 2E |
| SU-best-of | 8E |
| Adam-L | 2E + 3L·E |
| CD-s | 4E + s·N·16·E (erken durma yok sayılır) |
| Uzun koşulu Adam | 3·(1 + 1000·4)·E + 4E |

FLOP'tan öngörülen gecikme = FLOP / (3E) × 1.328 ms; yani Adam adımına kalibre edilir.

- **S3-H1 (ön kayıtlı):** Bütçeler B ∈ {2, 5, 10, 20, 50, 100, 200, 1000, 6000} ms, ölçülmüş gecikme. Ryu tarzı seçim, bütçeye sığan kollar arasından seed 12'de en yüksek **t = 0** hızına sahip kolu alır. Etkin hız seçimi, aynı kümeden seed 12'de en yüksek **etkin hızı** veren kolu alır. Seed 11'de fark = etkin hız (Ryu) − etkin hız (bizim). **Hipotez:** 1.5 m/s'de en az bir bütçede GA üst sınırı < 0. Bütün bütçeler ve 10 km/h da raporlanır.
- **S3-E (keşifsel):** Etkin hız sıralaması iki gecikme modeli altında karşılaştırılır: ölçülmüş gecikme ve FLOP'tan öngörülen gecikme. Raporlananlar: kollar üzerinden Kendall τ, seçilen kolun değişip değişmediği, kol başına ölçülmüş / FLOP-öngörülen gecikme oranı.

## Soru 1 — "CD'yi C ile yazsaydınız?"

- **Başa baş oranı r*.** Her r ∈ {1, 1.5, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 1000} için CD-s'nin gecikmesi T_s / r alınır ve kol bu gecikmede tam olarak değerlendirilir. s, seed 12'de her r için ayrı seçilir; bu, ayarlanmış CD demek. Karşılaştırma kolu, seed 12'de etkin hıza göre seçilen en iyi hızlı kol: SU-best-of ya da Adam-L, ölçülmüş gecikmesinde.
  - r*_eşit: seed 11'de CD ortalamasının en iyi hızlı kola ilk eriştiği r.
  - r*_anlamlı: CD − hızlı kol GA alt sınırının ilk kez > 0 olduğu r.
  - Izgara ayrık olduğu için r* bir aralık olarak verilir (önceki r, bu r).
- **Ölçülmüş hızlanma:** s_ölç = T_torch / T_numba, doğrudan ve artımlı sürümler için ayrı ayrı. Ayarlanmış CD, ölçülmüş numba gecikmesinde değerlendirilip hızlı kolla karşılaştırılır.
- **Not (önceden):** Adam derlenmedi; Python'da kalıyor. Bu karşılaştırma tezin aleyhine taraflıdır. Sonuç bu kayıtla yazılır.

## Sınırlar (önceden)

- FLOP modeli bir yaklaşıklıktır: geri yayılımın ileri geçişin 2 katı olduğu varsayılıyor; trigonometrik ve log işlemleri sayılmıyor.
- Ryu ve ark.'ın tam formülasyonu doğrulanmadı. Literatür notlarında "derleme süresini yalnızca uygulanabilirlik kısıtı olarak kullanıyor" diye geçiyor. Burada bu fikrin en sade biçimi sınanıyor.
- 200 ms'yi aşan gecikmeler (CD, uzun koşulu Adam) güven ufkunun dışında kalıyor.

## Sapma 1 (16 Kasım 2026, `arms.py` koşulmadan önce)

`timing.py`, bu makinenin rerun dosyasındaki sürelerden belirgin biçimde hızlı olduğunu gösterdi (adam1 ×0.86, adam48 ×0.78, CD-8 ×0.69). Yeni CD süreleri eski Adam süreleriyle karıştırılırsa CD haksız avantaj kazanır ve "aynı makine" kuralı (Kural 5) ihlal edilir.

Bu yüzden bütün kolların gecikmesi bu oturumda, aynı protokolle yeniden ölçülür (`timing2.py`): SU-average, SU-best-of, Adam L ∈ {1, 2, 4, 8, 16, 32, 48} (aradaki L'ler doğrusal interpolasyonla), uzun koşulu Adam ve CD (`timing.py`). FLOP kalibrasyonu da bu oturumun Adam eğimiyle yapılır. Rerun dosyası kullanılmaz.
