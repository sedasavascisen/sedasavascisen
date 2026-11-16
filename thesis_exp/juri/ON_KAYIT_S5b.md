# Ön kayıt — Soru 5b: daha büyük veri ve birden fazla tohumla sağlamlık (16 Kasım 2026)

Bu dosya, S5b eğitimleri başlamadan önce commit'lenir. Amaç, bağımsız denetimin işaret ettiği iki kapsam itirazını sınamak: "tek mimari ve tek koşu" ile "veri az".

## Kurgu (S5 ile aynı, yalnızca aşağıdakiler farklı)

- **Frekans ve hızlar:** 28 GHz; 1.5 m/s ve 3 km/h.
- **Eğitim verisi:** seed 21, n = **80 000** (S5'te 20 000). Seed 21 çekilişi n'e göre değiştiği için bu, yeni bir çekiliştir. Doğrulama seed 12, test seed 11; değişmedi.
- **Modeller** (her biri ayrı eğitim; 60 epoch ya da 25 dakika, en iyi doğrulama ağırlıkları saklanır):
  - sin/cos, genişlik 64, model tohumu 0, 1, 2 → `28_sincos_b{0,1,2}`;
  - doğrudan açı, genişlik 64, model tohumu 0, 1, 2 → `28_angle_b{0,1,2}`;
  - sin/cos, genişlik 128, model tohumu 0 → `28_sincos_w128`.
- **Gecikme:**
  - Genişlik 64 için S5'teki ölçüm (0.425 ms) kullanılır; mimari aynı.
  - Genişlik 128 için `eval_s5b.py` aynı protokolle ölçer: boş makine, tek iş parçacığı, toplu 1, 5 tur.
- **Klasik kollar:** S5'teki `s5/raw/eval.json`'dan alınır. Aynı kanal ve aynı tohumlar kullanıldığı için bu kollar yeniden hesaplanmaz. En iyi klasik kol, S5'teki gibi seed 12'de seçilir.
- **Seçilen ağ:** dört sin/cos ağı (b0, b1, b2, w128) arasından seed 12'de etkin hıza göre en iyisi seçilir, seed 11'de raporlanır.
- **Karma:** seçilen ağ + Adam-L; L seed 12'de seçilir.

## Hipotezler (28 GHz, 1.5 m/s)

- **S5b-H1:** seçilen ağ − en iyi klasik kol > 0 (GA alt sınırı > 0).
- **S5b-H2:** seçilen ağ − SU-average > 0 (GA alt sınırı > 0).
- **S5b-H3:** sin/cos − doğrudan açı, etkin hızda; aynı tohumla eşleştirilmiş 3 çiftin en az 2'sinde GA alt sınırı > 0.
- **Raporlanır:** her ağın ayrı ayrı sonuçları; 3 km/h; karma kol; tohumlar arası yayılım.

## Süre tahmini

Eğitim başına ~10–20 dakika. 7 eğitim, ikişer paralel koşulur (her biri 2 iş parçacığı). Ardından değerlendirme. Toplam ~1–1.5 saat.
