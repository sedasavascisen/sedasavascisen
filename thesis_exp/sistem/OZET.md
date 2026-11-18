# Gecikme farkındalıklı RIS denetleyicisi: tasarım ve mühürlü test

> Teknik rapor; tez metni değildir (Kural 9). Her sayı aşağıdaki dosyalara ve betiklere bağlıdır.

## Ne tasarlandı?

Hareketli bir kullanıcıya hizmet eden RIS için, her güncellemede faz hesaplama hattını seçen bir denetleyici.
- **Girdiler:** Doppler kestirimi, taşıyıcı frekansı, bu donanımda ölçülmüş gecikmeler, fazın tutulacağı süre (W) ve varsa önceki güncellemenin fazı.
- **Karar:** başlangıç noktası (SU-average, SU-best-of ya da önceki faz) ve Adam adım sayısı (0–48).
- **Yöntem:** her aday hattın etkin hızı öngörülür: R̂ = R_floor + (R0 − R_floor)·ψ̄(f_d·τ, f_d·W). Burada R0 kalibrasyon çekilişindeki t = 0 hızı, ψ ise eskime eğrisi. Eğri 3 GHz'de tasarım kuralından, 28 GHz'de deneysel kalibrasyondan geliyor. En yüksek öngörüyü veren hat seçilir.

## Mühürlü test (seed 41, bir kez; `FINAL.md`)

| Kip | Sistem | Kâhin | En iyi karşılaştırma yöntemine fark [GA] | Hipotezler |
| --- | --- | --- | --- | --- |
| Taze güncelleme (birincil) | 5.1241 | 5.1267 | K4 kapalı form: +0.097 [+0.077, +0.118] | H1 ve H2 tuttu |
| Periyodik, P = 20 ms (ikincil) | 5.1957 | 5.1979 | K4 kapalı form: +0.150 [+0.132, +0.170] | H3 tuttu |

## ⚠ Kazancın daha güçlü taban çizgilerine karşı boyutu (`FINAL_EK.md`, bağımsız denetim)

- **Başlangıç seçimi:** SU-best-of'tan başlayan kapalı forma karşı sistemin farkı +0.040 [+0.029, +0.052]. Yani K4'e karşı kazancın yaklaşık %59'u yalnızca başlangıç seçiminden geliyor.
- **Sabit tek hat:** seed 12'de seçilen ve her koşulda sabit tutulan en iyi tek hata karşı fark +0.087 [+0.072, +0.102].
- **Periyodik kip:** sıcak başlangıcın kendi katkısı +0.051 [+0.037, +0.066]. Kapalı forma da sıcak başlangıç verilince sistemin farkı +0.020 [+0.009, +0.030].
- **Sonuç:** kazanç üç tasarım kararının birleşiminden geliyor (başlangıç seçimi, sıcak başlangıç, adım sayısı seçimi) ve tezde bu üçü ayrı ayrı raporlanmalı.

## Kazancın kararlara ayrışması (mühürlü test; `katki_ayrisimi.py` → `katki_ayrisimi.json`)

| Karar | Katkı [%95 GA] | Yüzde |
| --- | --- | --- |
| Başlangıç seçimi (SU-average → SU-best-of) | +0.057 [+0.036, +0.079] | %1.14 |
| Koşula göre adım sayısı | +0.040 [+0.029, +0.052] | %0.79 |
| Toplam, kapalı forma göre | +0.097 [+0.077, +0.118] | %1.94 |
| En iyi sabit hatta göre | +0.087 [+0.072, +0.103] | %1.73 |
| Periyodik: sıcak başlangıcın değeri | +0.051 [+0.036, +0.066] | %0.99 |
| Periyodik: sıcak başlangıçlı kapalı forma göre | +0.020 [+0.010, +0.030] | %0.39 |

## Tasarım kuralları (geliştirme çekilişinde, `GUNLUK.md`)

- **Doppler kestirimi:** ±%20–25 hata zararsız. Yarı yarıya düşük kestirmek 0.09–0.11 kaybettiriyor; belirsizlikte kestirimi yukarı yönlü tutmak gerekir (tur 2–3).
- **Sıcak başlangıç:** yalnızca önceki faz tazeyken kazandırıyor. P = 20 ms'de +0.047, P = 50 ms'de anlamsız (tur 4–5).
- **CD:** bu hızlarda hiçbir koşulda rekabetçi değil (tur 6).

## Sınırlar

- Tek kanal modeli ve tek geometri.
- 28 GHz'deki ψ ayrımı, geliştirme sonucu görüldükten sonra seçildi.
- Tur 3'ün sapmalı sürümü seed 14'te 0.0016 daha yüksekti, ama v1b donduruldu (seçim kuralından sapma; seed 41'de etkisiz).
- H2 bir eşdeğerlik testi değil.
- Sağlamlık sonuçları yalnızca geliştirme çekilişinde alındı.
