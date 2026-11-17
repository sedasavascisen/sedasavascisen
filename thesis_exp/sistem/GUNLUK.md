# Gece fikir günlüğü

Her fikir: ne, neden, kod, seed 14 sonucu, karar. Başarısız fikirler de yazılır. Seed 41 (mühürlü test) gece kullanılmaz.

## Tur 0 (17 Kasım, 05:40): v0_rule

- **Ne:** tasarım kuralı genelleştirildi. Her aday hat için öngörülen etkin hız R̂(a) = R_floor + (R0(a) − R_floor)·ψ̄(f_d·τ_a, f_d·W). Başlangıç noktası olarak hem SU-average hem SU-best-of aday. R0, seed 12'nin o taşıyıcıdaki t = 0 hızlarından; ψ ve R_floor, `tasarim_kurali` kalibrasyonundan (3 GHz, 1.5 m/s).
- **Neden:** ön kayıtlı sınamada zaten tutmuş bir kural; sistemin çekirdeği olmaya en uygun aday.
- **Seed 14 sonucu** (12 koşul ortalaması): v0 **5.2869**; kâhin 5.2994 (açık 0.0125).

| Karşılaştırma | Ortalama | v0 − karşılaştırma [GA] |
| --- | --- | --- |
| K1 SU-best-of | 4.8701 | +0.417 [+0.384, +0.448] |
| K2 Adam-5 | 5.1053 | +0.182 [+0.156, +0.210] |
| K3 Adam-48 | 4.8436 | +0.443 [+0.406, +0.481] |
| K4 kapalı form | 5.1751 | +0.112 [+0.090, +0.134] |
| K5 Ryu tarzı | 5.1889 | +0.098 [+0.079, +0.117] |

- **Açık nerede:**
  - B1, W = 0 (28 GHz, 3 km/h): v0 adım atmıyor, kâhin Adam-1 seçiyor; açık 0.051.
  - B2, W = 20: v0 12 adım, kâhin 24; açık 0.030.
  - A4, W = 20: v0 32 adım, kâhin 48; açık 0.027.
  - Yüksek Doppler ve uzun tutma koşullarında kâhin uzun L seçiyor. Bunun büyük olasılıkla sabit saçıcıların bıraktığı korelasyon tabanının etkisi olduğunu not ediyorum; fiziksel bir sonuç sayılmamalı.
- **Karar:** temel sistem v0. Bundan sonraki her fikir v0'a karşı ölçülecek.

### Fikir kuyruğu

1. **Taşıyıcıya özgü ψ:** ψ eğrisini her taşıyıcıda seed 12'de ayrı kalibre etmek. B1 ve B2'deki açığı hedefliyor.
2. **Deneysel ψ:** ψ'yi kanal korelasyonundan değil, doğrudan seed 12 küpündeki etkin ve t = 0 hızlarının oranından kalibre etmek.
3. **Ayarlı CD ve karma başlangıç hatları:** denetleyicinin seçebileceği hat kümesini genişletmek.
4. **Sıcak başlangıç:** önceki güncellemenin fazından başlamak (takip). Yeni bir hat türü; gecikme ölçümü gerekir.
5. **Geniş bant uzantısı:** K_opt kararını denetleyiciye eklemek; ölçülmüş adım maliyetleri `genis_bant` deneyinden alınır.
6. **Sağlamlık:** Doppler kestirimi hatalıyken (±%20) denetleyici ne kadar kaybediyor?
