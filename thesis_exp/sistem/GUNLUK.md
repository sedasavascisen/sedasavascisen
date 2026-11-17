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

## Tur 1 (17 Kasım, ~05:50): deneysel ψ (fikir 1 ve 2)

- **v1_emp:** ψ, seed 12 küpünden taşıyıcıya ve W'ya özgü olarak kalibre edildi. Her hat için ψ_i = (etkin − R_floor)/(t = 0 − R_floor) hesaplandı; log u ekseninde 25 kutunun medyanı alındı ve bu medyanlar arasında enterpolasyon yapıldı.
  - Seed 14 sonucu: 5.2880; v0'a fark +0.0011 [−0.008, +0.010], **anlamsız**.
  - 28 GHz açığını kapatıyor (B1, W = 0: 0.051 → 0), ama 3 GHz'de bozuyor (A4, W = 20: 0.027 → 0.073; A2, W = 20: 0.019 → 0.033).
- **v1b_carrier:** 3 GHz'de doğrulanmış tasarım kuralı (v0), 28 GHz'de deneysel ψ (v1).
  - Gerekçe: kuralın ψ'si 3 GHz'de kalibre edildi, orada geçerli; başka bir taşıyıcıda o taşıyıcının ölçümü gerekir.
  - Seed 14 sonucu: **5.2930**, kâhin açığı 0.0063; v0'a fark **+0.0062 [+0.0019, +0.0105], anlamlı**.
- **Dürüstlük notu:** v1b'nin "hangi taşıyıcıda hangi ψ" seçimi, v1'in seed 14 sonucu görüldükten sonra yapıldı. Yani bu seçim seed 14'e bir ölçüde uyduruldu; sabahki mühürlü test bunu sınayacak.
- **Karar:** yeni aday v1b_carrier. Sıradaki fikir: kuyruktaki 3 (ayarlı CD ve karma hatlar) ve 6 (Doppler kestirim hatasına karşı sağlamlık).

## Tur 2 (17 Kasım): Doppler kestirim hatasına karşı sağlamlık (fikir 6)

- **Ne:** denetleyiciye yanlış f_d verildi (×0.5, ×0.8, ×1.25, ×2); etkin hız yine gerçek kanalda okundu. Kod `robust_fd.py`, ham çıktı `robust_fd.json` (seed 14, kalibrasyon seed 12).
- **Sonuç** (doğru f_d'ye göre kayıp, b/s/Hz):

| f_d çarpanı | v0 | v1b |
| --- | --- | --- |
| ×0.5 | −0.093 [−0.109, −0.077] | −0.106 [−0.122, −0.090] |
| ×0.8 | −0.003 (anlamsız) | −0.009 [−0.015, −0.003] |
| ×1.25 | −0.003 (anlamsız) | −0.000 (anlamsız) |
| ×2 | −0.052 [−0.065, −0.040] | −0.058 [−0.072, −0.044] |

- **Bulgu:**
  - ±%20–25'lik kestirim hatası pratikte zararsız: kayıp ≤ 0.009.
  - Hata asimetrik: Doppler'i yarı yarıya küçük kestirmek, iki kat büyük kestirmekten yaklaşık iki kat pahalı. Küçük kestirilen f_d, denetleyiciye fazla adım attırıyor.
  - ×0.5'te bile v1b (5.187), en iyi karşılaştırma yöntemi K5 (5.189) ile başa baş.
- **Tasarım sonucu:** belirsizlik varsa f_d kestirimini yukarı yönlü tutmak gerekir. Bu, denetleyiciye bir "temkinli sapma" parametresi olarak eklenebilir (yeni fikir 7).
- **Karar:** aday değişmedi (v1b). Sağlamlık sonucu sistemin raporunda yer alacak. Fikir 7 kuyruğa eklendi; sıradaki fikir 3 (ayarlı CD ve karma hatlar).
