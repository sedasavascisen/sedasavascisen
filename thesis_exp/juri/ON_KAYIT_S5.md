# Ön kayıt — Jüri sorusu 5: öğrenmeye en elverişli rejimde kesin test (16 Kasım 2026)

Bu dosya, `s5/train.py` ve `s5/eval_s5.py` koşulmadan önce commit'lenir. Hiçbir eğitim ya da değerlendirme sonucu görülmedi.

## Soru

Tek geçişli, sin/cos çıkışlı bir ağ, gecikmenin baskın olduğu rejimde (28 GHz, 1.5 m/s, f_d ≈ 140 Hz, T_c ≈ 3 ms) her bütçede ayarlanmış klasik yöntemleri yener mi? Aynı ağ 3 GHz'de (f_d ≈ 15 Hz) de eğitilir; bu karşılaştırma için kullanılır.

## Kurgu

### Kanal
- **28 GHz:** yaşlanma kurgusunun aynısı; RIS paneli fc = 28 GHz ile kurulur (`s5/ch28.py`, paket değiştirilmez).
- **Bağlantı bütçesi telafisi:** Aynı bütçeyle 28 GHz'de min-kullanıcı hızı ~0.05 b/s/Hz'e çöküyor. Bu yüzden gürültü, ortalama tutarsız alınan gücü 3 GHz ile eşitleyen sabit bir telafiyle ölçeklenir: **comp = 30.79 dB**. Bu değer yalnızca eğitim tohumu 21'den hesaplandı (`s5/link_budget.py` → `s5/raw/link_budget.json`). Daha yüksek verici gücü ya da anten kazancına eşdeğerdir.

### Veri ve eğitim
- **Veri:** eğitim seed 21 (n = 20000, t = 0); doğrulama seed 12 (n = 400, yalnızca epoch seçimi); test seed 11 (eğitimde hiç görülmez). Her frekansta ayrı eğitim.
- **Model** (`s5/model.py`):
  - girdi, panel ızgarasında 3D tensör [72, 8, 4]: tek kullanıcı hizalama terimleri ve kaskat kanal;
  - gövde: 3 × Conv3x3 + global bağlam;
  - kafa: sin/cos (L2 normalizasyonu, atan2) ya da doğrudan açı (π·tanh).
  - LSTM yok, çünkü tek anlık görüntüde zaman dizisi yok.
- **Eğitim:** etiketsiz; soft-min (β = 8) hız, taze ZF ile. Adam 1e-3, toplu 256, en çok 60 epoch ya da 25 dakika; en iyi doğrulama ağırlıkları saklanır. Model başlangıç tohumu 0.
- **Eğitim süresi tahmini:** her model ~15–25 dk, toplam 3 model (28 GHz sin/cos, 28 GHz açı, 3 GHz sin/cos).

### Değerlendirme
- **Gecikme:** bu makinede, tek iş parçacığı.
  - Ağın çıkarımı (öznitelik + ileri geçiş, toplu 1) burada ölçülür.
  - Diğerleri `raw/timing2.json` ve `raw/timing.json`'dan alınır.
  - Her kolun gecikmesine başlangıcı dahildir: Adam-L(başlangıç) = başlangıç + adam(L); NN+Adam-L = NN + adam(L).
- **Kollar:**
  - SU-average, SU-best-of;
  - Adam-L, SU-average'tan ve SU-best-of'tan başlayarak, L ∈ {1, …, 48};
  - CD-s, s = 1…8;
  - NN-sincos, NN-angle (yalnızca 28 GHz), NN-untrained (eğitilmemiş sin/cos ağı);
  - NN+Adam-L (karma).
- **Ölçüt ve seçim:** Tanım 1, tam gecikmede. Hızlar 1.5 m/s ve 3 km/h. Seçim seed 12, rapor seed 11. Eşli bootstrap 2000, %95.
- **En iyi klasik kol:** klasik kollar (SU-average, SU-best-of, iki başlangıçtan Adam-L, CD-s) arasından seed 12'de etkin hıza göre seçilen.

## Hipotezler (28 GHz, 1.5 m/s)

- **S5-H1:** NN-sincos − en iyi klasik kol > 0 (GA alt sınırı > 0).
- **S5-H2:** en iyi NN+Adam-L (L seed 12'de seçilir) − en iyi klasik kol > 0 (GA alt sınırı > 0).
- **S5-H3** (çapada donma kontrolü): t = 0 hızında NN-sincos (eğitilmiş) − NN-untrained > 0 (GA alt sınırı > 0).
- **S5-E1** (keşifsel): sin/cos − doğrudan açı kafası, t = 0'da ve etkin hızda; Makale 1 ablasyonunun bu kurgudaki karşılığı.
- **S5-E2** (keşifsel): aynı H1/H2 farkları 3 GHz'de ve 3 km/h'de.

## Sınırlar (önceden)

- Telafi, gerçekçi bir mmWave bağlantı bütçesinin yerine geçen bir eşitlemedir; 32 elemanlı panel 28 GHz'de çok küçüktür.
- Ağ CPU'da ve Python'da çalışıyor; aynı haksızlık klasik kollar için de geçerli.
- Tek ağ mimarisi; mimari taraması yok.
