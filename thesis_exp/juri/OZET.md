# Jüri soruları: beş soru, beş ön kayıtlı deney (16 Kasım 2026)

Bu sayfa bir özet; her sayı aşağıdaki raporlardan alındı ve her rapor kendi betiğine, ham çıktısına ve tohumuna bağlı. Tez metni değildir (Kural 9).

## ⚠ Önce: Makale 2'yi sınırlayan iki bulgu (Kural 10)

1. **Sıralama gerçekleştirmeye duyarlı (Soru 1).** Yalnızca CD derlenirse sıralama döner.
   - Yalnız derleme (aynı algoritma, ×62–63) Python Adam'ı 1.5 m/s'de +0.514, 10 km/h'de +0.602 farkla geçiyor.
   - Derleme ile rank-1 güncelleme birlikte +0.684 ve +0.836 farkla geçiyor.
   - Başa baş hızlanma 10–15 kat.
   - Makale 2 kopyasının "Sınırlar" bölümüne eklendi.
2. **İç optimum geniş bantta genelleşmiyor** (geniş bant deneyi, G1). 50–100 MHz'de 16 hücrenin yalnızca 3'ünde L = 48 anlamlı olarak kötü. Makale 2 kopyasına "dar bant" sınırlaması eklendi.

## Beş soru ve yanıtları

| # | Jürinin sorusu | Ölçülmüş yanıt | Rapor |
| --- | --- | --- | --- |
| 1 | "CD'yi C ile yazsaydınız?" | Yalnız CD derlenirse sıralama döner (yukarıda). **Bütün kollar aynı oranda hızlanırsa** (r = 1…1000), ayarlı Adam her noktada önde (CD − Adam −1.43 … −0.12). Sıralamayı dil değil, kolların gecikme oranı belirliyor. | `REPORT_S3_S1.md` |
| 2 | "L* = 48 fiziksel mi?" | Fiziksel optimum, güven ufku içindeki dar bant L*'ı (4–6 adım). Korelasyon tabanı olmayan Clarke kanalında da iç optimum var: L* 3–8 adım (3.4–8.8 ms), L = 48'in kaybı %27–32. Izgara ucundaki geniş bant değerleri "belirlenemez" olarak etiketli. | `REPORT_S4_S2.md` |
| 3 | "Ryu ve ark.'tan farkınız?" | FLOP ile milisaniye bu kurguda aynı kolu seçiyor (Kendall τ 0.86–0.87); fark bu değil. Fark, sürenin eskimeye katılması. Süreyi yalnızca uygulanabilirlik kısıtı yapan seçim, ≥ 20 ms bütçelerde 0.43–1.41 b/s/Hz kaybettiriyor (1.5 m/s; S3-H1 tuttu). | `REPORT_S3_S1.md` |
| 4 | "Ön kodlayıcı da eskirse?" | Her şey ~1 ms içinde çöküyor. 1.15 ms'de kanal yalnızca %0.53 değişiyor, ama bayat ZF hızı 5.41'den 4.03'e indiriyor. L* ızgaranın alt ucunda; en iyi kol optimizasyonsuz SU-average. Ön kodlayıcıyı her slotta tazelemek zorunlu; Makale 2'nin varsayımı bir tasarım gereği. | `REPORT_S4_S2.md` |
| 5 | "Yapay zekâdan geriye ne kalıyor?" | En elverişli rejimde bile olumsuz. 28 GHz'de 1.5 m/s'de (T_c ≈ 3 ms) 0.43 ms'lik tek geçişli ağ, SU-best-of'un 0.38 gerisinde (S5-H1 tutmadı); ağ + Adam karması 0.16 gerisinde. Ağ çapada donmuyor (eğitilmiş − eğitilmemiş +0.47; S5-H3 tuttu). sin/cos kafası doğrudan açıyı +0.04…+0.05 farkla geçiyor; Makale 1'in ablasyonu bu kurguda da tekrarlanıyor, küçük ama tutarlı bir etkiyle. | `REPORT_S5.md` |

## Süreç

- **Ön kayıt:** beş deneyin her biri, sonuç görülmeden önce ön kayda alındı (`ON_KAYIT_S3_S1.md`, `ON_KAYIT_S4_S2.md`, `ON_KAYIT_S5.md`).
- **Sapmalar:** iki sapma tarihli olarak kayıtlı.
  - Sapma 1: bütün gecikmeler bu oturumda yeniden ölçüldü, çünkü makine 0.69–0.86 kat daha hızlıydı.
  - Sapma 2: CD, bağımsız denetimin bulduğu bir sorun nedeniyle erken durmasız ölçüldü ve koşular tekrarlandı. Sonuçlar değişmedi; derlenmiş CD'nin üstünlüğü +0.717'den +0.684'e indi.
- **Ön kayıt dışı analiz:** tek bir ek analiz var: Soru 1b (bütün kollar eşit hızlandırılınca). Sonuçlar görüldükten sonra yazıldı ve raporda öyle etiketli.
- **Bağımsız denetimler:**
  - Soru 1–4: 392 kontrol tuttu; 1 hata, 1 üretilemedi; bulgular düzeltildi (`thesis_exp/denetim_log/DENETIM_JURI_S1_S4.md`).
  - Soru 5: `DENETIM_JURI_S5.md`.
- **İddia denetleyicisi:** 112/112 iddia tutuyor; sabotaj testi 11/11 (`thesis_exp/iddia_denetimi/check_claims.py`).
