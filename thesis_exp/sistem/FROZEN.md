# Dondurulan sistem (17 Kasım 2026, mühürlü testten önce)

Kullanıcı mühürlü testi onayladı. Gece döngüsü (tur 0–6) burada sona erdi.

| Kip | Sürüm | Kod | Seed 14'teki geliştirme sonucu |
| --- | --- | --- | --- |
| Taze güncelleme (birincil, H1–H2) | `v1b_carrier`: 3 GHz'de tasarım kuralı, 28 GHz'de deneysel ψ; başlangıç SU-average ya da SU-best-of, Adam L ∈ {0,…,48} | `controllers.py` | 5.2930; kâhin açığı 0.0063 |
| Periyodik, P = 20 ms (ikincil, H3) | `V4`: v1b + sıcak başlangıç hatları | `periodic.py` | 5.3452; kâhin açığı 0.009 |

Seçim kuralı (PROTOKOL.md): seed 14'te en yüksek ortalama. Karşılaştırma yöntemleri, koşullar ve ölçüt protokoldeki gibi; değiştirilmedi. Analiz betiği `final_test.py` bu dosyayla birlikte, seed 41 koşulmadan önce commit'lenir.
