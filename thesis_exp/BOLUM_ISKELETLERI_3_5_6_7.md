# Bölüm iskeletleri: 3, 5, 6 ve 7 (yazımın 2.–3. haftası)

> Bu bir iskelet; tez metni değil (Kural 9). Her alt başlıkta o kısmın taşıması gereken iddia, sayılar ve sayıların kaynağı var. Sayılar Makale 2'nin son hâlinden ve denetlenmiş raporlardan birebir alındı. Yazarken sayıyı değiştirme; değiştirmen gerekiyorsa önce kaynağını kontrol et. Etkin rank gibi örnek sayısına bağlı büyüklüklerde n'yi her zaman yaz (CLAUDE.md).

Kısaltmalar:
- **M2:** Makale 2, `thesis_exp/makale2_revizyon/` (bölüm numarası §).
- **TK:** `thesis_exp/tasarim_kurali/REPORT.md`.
- **J:** `thesis_exp/juri/`.

---

## Bölüm 3. Sistem modeli

**Bölümün işi:** okuyucuya bütün sonuçların hangi dünyada geçerli olduğunu söylemek. Bölüm, temel tasarım ilkesiyle açılmalı (yol haritası, Düzeltme 4).

**3.0 Temel tasarım ilkesi: iki zaman ölçeği**
- Ön kodlayıcı her slotta güncel kanaldan tazelenir; RIS fazı daha yavaş, gecikmesi ölçülmüş bir döngüde güncellenir.
- Dayanak: ön kodlayıcı da eskirse hız 1.15 ms'de 5.41'den 4.03'e iniyor; kanal o sürede yalnızca %0.53 değişiyor (J `REPORT_S4_S2.md`). Taze ve bayat ön kodlayıcı arasındaki fark T_c'de 11.7–14.2 kat (M2 §VI-G).
- Ön kodlayıcıyı tazelemek ucuz: 0.12 ms, yani bir Adam adımından yaklaşık 13 kat kısa (M2 §VI-G).

**3.1 Sinyal modeli** (M2 §III-A, denklemler `eq:signal`, `eq:maxmin`)
- N_t = 8 antenli BS, K = 4 kullanıcı, N = 32 elemanlı RIS (8 × 4); ölçekleme deneyinde N = 64.
- Ön kodlayıcı: düzenlileştirilmiş ZF, λ = Kσ²/P.
- Amaç: en kötü kullanıcının hızı (max-min). Optimizasyonda soft-min vekili kullanılıyor (β = 8); CD ve uzun Adam doğrudan en kötü kullanıcıyı maksimize ediyor.

**3.2 Geometri ve yayılım** (M2 §III-B, Şekil `fig_scenario`)
- Ortam: 40 × 20 × 6 m ofis; RIS (20, 0.1, 3) m'de, BS (20, 6, 4) m'de; f_c = 3 GHz, 20 MHz bant genişliği, 20 dBm.
- Kanal: TR 38.901 iç mekân ofis modeli (mixed-office LoS olasılığı); kaskad genlik Tang ve ark.'ın modeli; 20 nokta saçıcı.
- **Yazılması gereken not, eleman kazancı:** kod 2(2q+1) = 6, Tang 2(q+1) = 4 kullanıyor. Tang'in kazancıyla mutlak hızlar yaklaşık %5 düşüyor (L*'da 6.151 → 5.845, 1.5 m/s); L*, L = 48 kaybı ve sıralamalar değişmiyor (`kazanc_duyarlilik/REPORT.md`).

**3.3 Hareketlilik** (M2 §III-C)
- Kullanıcılar 1.5 m/s (5.4 km/h) hızla yürüyor; f_d = 15 Hz; T_c = √(9/(16π))/f_d ≈ 0.423/f_d = 28.2 ms.
- Standart hızlarla ilişki: 3 km/h (3GPP iç mekân) ile 10 km/h (IMT-2020 yaya üst sınırı) arasında.

**3.4 Etkin hız** (M2 §IV-A, `eq:effective_rate`)
- Faz, yöntemin işini bitirdiği andaki kanalda değerlendiriliyor. Tezin merkez tanımı bu.
- Ölçüt merdiveni burada kurulur: faz hatası → t = 0 hızı → etkin hız.

**3.5 Sınırlar** (M2 §III-C, "Limitations"; hepsi açıkça yazılmalı)
- Sabit saçıcılar: 200 ms'nin ötesindeki etkin hızlar iyimser.
- Saçılan yolların kazançları BS antenleri arasında bağımsız: mutlak hızlar iyimser. Paylaşılan kazançlarla bulgular korunuyor (M2 §VI-D).
- Dar bant (beam squint yok); N = 32 için uzak alan.

---

## Bölüm 5. Gecikme ve etkin hız (Makale 2'nin genişletilmiş hâli)

**Bölümün işi:** tezin ana sonucu. Gecikme hesaba katılınca yöntemlerin sıralaması değişiyor.

**5.1 Yavaş ve güçlü çözücüler hızlı bir sezgisel yönteme kaybediyor** (M2 §VI-A, Tablo `tab_aging`, Şekil `fig_aging`)
- Bağlam: RIS olmadan en kötü kullanıcının hızı 1.744 b/s/Hz, rastgele fazla 4.072.
- Eskime: uzun Adam'ın hızı T_c'de 7.117'den 5.473'e düşüyor; SU-average yalnızca 4.624'ten 4.503'e.
- Uzun Adam 5.9 s, CD 0.88 s sürüyor; SU-best-of 2.5 ms.
- SU-best-of − CD = 0.297 [0.204, 0.390]; SU-best-of − uzun Adam = 0.604 [0.415, 0.805].
- Bütçe meselesi değil: CD'nin tek taraması 107 ms sürüyor (yaklaşık 4 T_c). 1–8 taramanın en iyisi bile SU-best-of'un 0.26 [0.17, 0.36] altında.

**5.2 İçsel optimum** (M2 §VI-B, Şekil `fig_optimum`, `eq:marginal`)
- t = 0 hızı her adımda artıyor (L = 1'de 5.412, L = 48'de 7.037). Etkin hız ise L = 4–6'da tepe yapıyor: 5.980 / 5.982 / 5.970, 6.7–10.0 ms'de.
- L = 48 tepe noktasından %14.0 [12.5, 15.5] düşük.
- Optimizöre özgü değil:
  - Farklı adım boyları (0.25 / 0.75 / 1.0) optimumu L = 6 / 4 / 5'e koyuyor.
  - Armijo da L = 4'te tepe yapıyor; Adam'la istatistiksel olarak başa baş.
- Gecikmenin sıralamayı belirlediğinin en açık örneği: Armijo'nun adım maliyeti 1.0 → 2.0 kat Adam olunca, en iyi etkin hızı Adam'a göre +0.147'den −0.197'ye iniyor.

**5.3 Tek sayı: x = ΔT·f_d** (M2 §IV-D ve §VI-C, Önerme 1, Şekil `fig_scaling`)
- Adam'ın adım süresi 0.01 ile 3 kat arasında ölçeklendi. En iyi adım sayısı 96'dan 2'ye iniyor; bu kurgu x = 2.5 × 10⁻² noktasında.
- Ölçülen eğim −0.675 [−0.692, −0.655]; modelin öngördüğü aralık −0.78 ile −0.63 arası.
- Kapalı form, her x'te ölçülen optimumun 1.27 katı içinde (bu kurguda 5.3'e karşı 5). Bu bir örnek içi kontrol.
- Dürüst sınır: Önerme 1'in denge ifadesi nicel olarak tutmuyor (oran 0.19–1.65).
- N = 64 her çarpanda aynı en iyi adım sayısını veriyor; optimumu doğruluyor ama üsseli bağımsız olarak doğrulamıyor.

**5.4 Standart hızlar ve kanal edinme gecikmesi** (M2 §VI-D, Tablo `tab_speeds`)
- Optimum 3 km/h'de 8 adım, 10 km/h'de 3, 18 km/h'de 2, 30 km/h'de 1.
- L = 48'in maliyeti: 3 km/h'de %14.5, 10 km/h'de %10.5.
- SU-best-of − CD her hızda 0.25–0.42 b/s/Hz.
- Hız varsayımı yanlış olunca: 1.5 m/s için seçilip 1.8 m/s'de kullanılırsa kayıp < %0.5; ızgaradaki en kötü durum %5.7.

**5.5 Periyodik çalışma** (M2 §VI-E, Tablo `tab_tracking`)
- Pilotlar bedavaysa: art arda güncelleme ve iki sıcak başlangıçlı adım en iyi (6.36).
- 0.86 ms pilotla en iyi periyot 10–20 ms.
- Her satırda en çok 8 adımlı bir politika en iyiyle istatistiksel olarak aynı.

**5.6 Öğrenilen güncelleme kuralı** (M2 §VI-F, Şekil `fig_eqms`)
- Adım başına öğrenilen kural önde: her L'de kazanıyor, senaryoların %68–84'ünde.
- Milisaniye başına geride: öğrenilen bir adım 2.7–4.0 Adam adımı sürüyor ve beş turun beşinde de baskınlanıyor. Örnek: öğrenilen L = 4, 18.41 ms'de 5.285; Adam L = 8, 13.48 ms'de 5.380.
- Doğrulama alt kümesinin sonuca etkisi yok (`veri_bolme/saglamlik_900.json`).

**5.7 Sağlamlık: pilotlar, kestirim hatası, ayrık faz** (M2 §VI-H)
- **Pilotlar:** pilot maliyeti düşülünce 5.21 → 3.54 / 4.00 / 4.33 (15 / 30 / 60 kHz). Seçilen 6–8 adım; 3–20 adım başa baş.
- **Kusurlu CSI:** 30 dB'de en iyi etkin hız 6.08'den 3.54'e iniyor. Pilotlar da düşülünce Adam SU-best-of'u 30 dB'de 0.05–0.06 geçiyor, 20 dB'de başa baş.
- **Ayrık faz:** iç optimum korunuyor (1/2/3 bitte L* = 5 / 6 / 6). 1 bitte ayrık CD seçiliyor: Adam'la başa baş, −0.04 [−0.11, 0.02].

**5.8 Bölümün sınırları** (M2 Sonuç; J `REPORT_S3_S1.md`)
- Gecikmeler optimize edilmemiş Python ile ölçüldü. Yalnızca CD derlenirse sıralama dönüyor (Bölüm 7.1).
- İç optimum dar banda özgü (Bölüm 8).

---

## Bölüm 6. Tasarım kuralı

**Bölümün işi:** içsel optimumu bir gözlemden önceden hesaplanabilir bir kurala çevirmek. Tezin "tasarım" katkısının ilk ayağı bu.

**6.1 Kural** (TK; M2 Önerme 1)
- R̂ = R_floor + (R0 − R_floor)·ψ̄(f_d τ, f_d W). Kural 1.5 m/s'de, seed 12 ile kalibre edildi.

**6.2 Ön kayıtlı sınama** (TK, `ON_KAYIT.md` sınamadan önce commit'lendi)
- 60 koşul (hız × adım süresi × pencere W), seed 13, 400 senaryo.
- **H1 (tuttu):** doğru L'ye göre kayıp medyanı %0.08, en kötüsü %2.74.
- **H2 (tuttu):** kural, sabit L = 48'den +3.34 puan [+2.89, +3.81], sabit L = 5'ten +2.72 puan [+2.22, +3.22] iyi.
- **H3 (tuttu):** W > 0'da kural, makalenin kapalı formundan +1.97 puan [+1.45, +2.49] iyi.
- Koşul başına tablo: TK §2. En kötü koşullar 18 km/h, ΔT = 5.32 ms, yani en büyük x değerleri.

**6.3 Ek kurallar**
- Doppler kestirimi: ±%20 hata zararsız; düşük kestirmek daha pahalı (`sistem/` raporları).
- Zaman ölçekleri: ön kodlayıcı her slotta tazelenmeli (Bölüm 3.0).

**6.4 Sınırlar**
- Tek geometri. Kalibrasyon 1.5 m/s'de yapıldı; en kötü durum yüksek x'te.

---

## Bölüm 7. Sağlamlık: jürinin soruları

**Bölümün işi:** sonucun nerede dayandığını, nerede koşullu olduğunu ölçülmüş olarak göstermek. Her alt bölüm bir ön kayıtla başlamalı; ön kayıt dosyaları J altında.

**7.1 Gerçekleştirme oranı: "C ile yazsaydınız?"** (J `REPORT_S3_S1.md`)
- **Önce olumsuz sonuç (Kural 10):** yalnızca CD derlenirse (×62–63) sıralama dönüyor; Python Adam'ı 1.5 m/s'de +0.514, 10 km/h'de +0.602 geçiyor. Başa baş hızlanma oranı 10–15 kat.
- Bütün kollar aynı oranda hızlanırsa (r = 1…1000) ayarlı Adam her noktada önde: CD − Adam −1.43 … −0.12. Bu analiz ön kayıt dışı ve raporda öyle etiketli.
- Bölümün cümlesi: sıralamayı dil değil, kolların gecikme oranı belirliyor.

**7.2 L* fiziksel mi? Clarke kanalı** (J `REPORT_S4_S2.md`)
- Korelasyon tabanı olmayan Clarke kanalında da iç optimum var: L* 3–8 adım (3.4–8.8 ms), L = 48'in kaybı %27–32.

**7.3 Ryu ve ark.'tan fark** (J `REPORT_S3_S1.md`)
- FLOP ile milisaniye aynı kolu seçiyor (Kendall τ 0.86–0.87); fark bu değil.
- Fark, sürenin eskimeye katılması: süreyi yalnızca uygulanabilirlik kısıtı yapmak ≥ 20 ms bütçelerde 0.43–1.41 b/s/Hz kaybettiriyor (S3-H1 tuttu).

**7.4 Ön kodlayıcı da eskirse** (J `REPORT_S4_S2.md`)
- Sistem yaklaşık 1 ms içinde çöküyor (Bölüm 3.0 ile aynı sayılar). Bu bölüm, ilkenin ölçümle kanıtı.

**7.5 Süreç**
- Ön kayıt, iki tarihli sapma ve bağımsız denetimler:
  - Soru 1–4: 392 kontrol tuttu; 1 hata, 1 üretilemedi.
  - Soru 5: 202 kontrolün hepsi tuttu.
- Kaynak: J `OZET.md` "Süreç".

---

## Her bölümde kullanılacak şekil ve tablolar

| Bölüm | Şekil / tablo | Dosya |
| --- | --- | --- |
| 3 | Senaryo şekli | `makale2_revizyon/figures/fig_scenario.pdf` |
| 5 | Tablo I–III, Şekil 2–5 | `makale2_revizyon/tables/`, `figures/` |
| 6 | Koşul başına kayıp tablosu | `tasarim_kurali/REPORT.md` §2 (ham: `tasarim_kurali/raw/`) |
| 7 | S1 ve S2 şekilleri | `juri/` raporlarının şekilleri |

**Yazarken iki kural:**
- Bir sayıyı başka bir sayıyla birleştiriyorsan (oran, fark), bunu kendin hesaplama; kaynağında var mı bak.
- Teze giren her sayıyı iddia denetleyicisine (`thesis_exp/iddia_denetimi/check_claims.py`) bir satır olarak ekletebilirsin; o zaman sayının kaynakla tutup tutmadığı otomatik denetlenir. Denetleyici bugün raporlardaki iddiaları denetliyor, tez metnini değil.
