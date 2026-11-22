# Makale 2 revizyonu — değişiklik listesi (16 Kasım 2026)

**Kapsam:** Bu klasör, `paper_mobility/`'nin (dal `claude/review-ris-comparison-J8TI0`, TWC'ye hazırlanan sürüm) bir kopyası. Özgün `paper_mobility/`'ye dokunulmadı.

**Kuralla ilişkisi:** 11 Kasım kurallarının 2. ve 9. maddeleri makale metnine dokunmayı yasaklıyor. Bu revizyon, kullanıcının 16 Kasım'daki açık isteğiyle ("makale 2'yi tekrar gözden geçir düzeltmeleri yap") yapıldı. Yayımlanmış/gönderilmiş dosyaları korumak için kopyada çalışıldı.

**Sonuç:** Derlenmiş PDF `mobility_paper_ieee.pdf`, 9 sayfa (TWC ücretsiz sınırı 10). Hata ya da tanımsız referans yok.

## Değişiklikler

| # | Yer | Ne değişti | Neden | Kaynak |
| --- | --- | --- | --- | --- |
| 1 | `tables/tab_tracking.tex` (Tablo III) | 0.86 ms soğuk: L 4 → 3, hız 5.20 → 5.24; sıcak 5.42 → 5.51; fark +0.22 → +0.28. 1.71 ms: soğuk 5.09 → 5.08, sıcak 5.23 → 5.17, fark +0.15 → +0.09. 3.43 ms sıcak: L 8 → 24. 0 ms fark +0.52 → +0.53. | Benzetim pilot süresini ve devreye alma anını 0.5 ms ızgarasına yuvarlıyordu (denetim K4). Tablo, makalenin kendi tablo kodu ile düzeltilmiş veriden üretildi (`make_tab_tracking_corrected.py`). Yayımlanmış mantık dört T_p'de birebir yeniden üretildi. | `thesis_exp/p4/takip_duzeltme/` |
| 2 | §VI-E metni | "Warm starting gains up to 0.52" → 0.53 | Tablo III ile uyum. Bölümdeki diğer nitel iddiaların hepsi düzeltilmiş veride tutuyor; örneğin her satırda en fazla 8 adımlık bir politika en iyiden ayırt edilemiyor. | aynı |
| 3 | §V (yöntem), periyodik benzetim | "pilot airtime is charged as the fraction of each grid step it occupies, and each phase takes effect at its exact deployment instant" eklendi | Düzeltilmiş yöntemin tanımı | aynı |
| 4 | §V (yöntem), istatistik | Tam gecikmede değerlendirmenin etkisi eklendi: en fazla 0.027 b/s/Hz, L* aynı, L=48 maliyeti %14.0 → %14.2 | Denetim K3 sonrası Makale 2 kontrolü | `thesis_exp/p4/izgara_kontrol/` |
| 5 | §V (yöntem), gecikme | Boş makinede tek iş parçacıklı yeniden ölçüm (1.33 ms/adım) ve yeni bölüme atıf eklendi | "1.49–2.02 ms aralığında" cümlesinin yanında daha düşük bir ölçüm var; açıkça belirtildi | `thesis_exp/infra/` (dal thesis/altyapi) |
| 6 | **Yeni §VI-H "Robustness to the Remaining Assumptions"** | Beş paragraf: adım süresi, ön kodlayıcı pilotları (ve faz tutma süresi), kusurlu kanal bilgisi (pilotla birlikte), ayrık faz (1/2/3 bit) | Makalenin sınırlılık olarak bıraktığı varsayımlar artık ölçüldü | `p4/izgara_kontrol`, `p4/onkodlayici_siralama` (+ W = 25/100 ms), `p4/kusurlu_csi`, `p4/onkodlayici_csi`, `p4/ayrik_faz` |
| 7 | §VI-G "Fresh-Beam" | "whose airtime we do not charge" → "Section VI-H charges their airtime" | Artık ücretlendirildi | `p4/onkodlayici_siralama` |
| 8 | §VII Sonuç, sınırlılıklar | Ön kodlayıcı/CSI cümlesi güncellendi; faz tutma süresiyle en iyi adım sayısının arttığı eklendi; "imperfect channel knowledge and discrete phases … follow" kaldırıldı | Bu ikisi yapıldı | yukarıdakiler |
| 9 | Özet | "costs 14.0%" → "costs 14%" | Grid yöntemiyle %14.0, tam değerlendirmeyle %14.2; ikisi de "14%" | `p4/izgara_kontrol` |

## Değiştirilmeyenler (bilinçli)

- **Tablo I ve Şekil 3 (gecikmeler):** Makalenin 1.66 ms/adım gecikmesiyle bırakıldı. Yeni gecikmeyle yeniden üretim tezde var; makalede yalnızca §VI-H'de özetlendi. Tablo III de 1.66 ms ile düzeltildi; yeni gecikmeyle yeniden üretim yapılmadı.
- **Tablo III'teki seçim kuralı:** Makale zaten "best configurations are selected and reported on the same scenarios unless stated" diyor; dokunulmadı.
- **Sonuç maddesi 2 ("A few steps are optimal"):** Sınırlılıklar paragrafına "the best step count also grows when a phase is held for longer" eklendi; madde metni değişmedi.

## Gönderim notu

Makale TWC'ye gönderildiyse bu değişiklikler bir revizyon turunda ya da hakem yanıtında kullanılabilir. Gönderilmediyse doğrudan bu sürüm gönderilebilir.

Yeni bölümdeki sayıların hepsi yukarıdaki raporlara bağlıdır. Bu sayılar 11 denetim turunun kapsamındaki raporlardan alındı; denetim, sayıları bu makale metnine kopyalanmış hâliyle ayrıca sınamadı.

Sözcük ve dil kontrolünü, özellikle yeni §VI-H'yi, ortak yazarlarla birlikte yapmanız önerilir.

---

## İkinci tur (16 Kasım, iki bağımsız denetimden sonra)

Denetim raporları: `DENETIM_SAYISAL.md` ve `DENETIM_EDITOR.md`. Bütün KRİTİK bulgular ana oturumda doğrulandı ve düzeltildi.

| Bulgu | Düzeltme |
| --- | --- |
| Sayısal K1: "leaves L* unchanged" yanlıştı (tam değerde L = 4 ile 5 arasındaki fark < 0.001) | "the optimum stays at 4–6 steps" |
| Sayısal K2: "at most 0.027" Tablo I'in Adam dışı kollarını kapsamıyordu | Tablo I'in kendi gecikmeleriyle ölçüldü (`p4/izgara_kontrol/run_tab1.py`; interpolasyon yayımlanmış Tablo I'i birebir veriyor). Güven ufkunun içinde ≤ 0.006, ufkun ötesinde CD 0.008 ve uzun Adam 0.037; Adam taraması ≤ 0.027. |
| Sayısal K3: sayı kaynak dosyaları eskiydi | `paper_numbers.txt`'deki Tablo III satırları düzeltilmiş veriden yeniden yazıldı; `KEY_NUMBERS.md`'ye kaynak satırı ve §VI-H kaynak tablosu eklendi |
| Sayısal K4: "one script generates every table" ve "123 assertions" | Tablo III ile §VI-H'nin ayrı betiklerden geldiği yazıldı; 126 iddia |
| Sayısal K5: 1 bitte dCD-1'in seçildiği yumuşatılmıştı | Açıkça yazıldı: tek taramalı ayrık CD seçiliyor, yuvarlanmış SU-best-of'u +0.25 (0.16–0.33) geçiyor, en iyi yuvarlanmış Adam'la berabere. Desteklenmeyen "yalnızca" ifadesi kaldırıldı. Sınırlılıklar'a da eklendi. |
| Editör 1, 2: "All results assume" ve eskimiş cümleler | Özet, Giriş katkı 5, İlgili Çalışmalar ("continuous phases"), Sistem Modeli ("channel knowledge is perfect"), §IV atfı, §VI-G ve Sonuç güncellendi |
| Editör 3, sayısal U9: PGA tanımsız | "long-run Adam" kullanıldı |
| Editör 4: R sembolü çakışıyordu, ρ tanımsızdı | $T_{\mathrm{r}}$ kullanıldı, ρ tanımlandı |
| Editör 5, sayısal U3: farklı taban değerleri | $\bar R_W$ (W ms ortalaması, pilot net) tanımlandı; 6.08 için "effective rate (Definition 1)" denildi |
| Editör 6: "the findings hold" aşırı genel | §V'de hangi sayıların yeniden hesaplandığı tek tek yazıldı (L* = 6, %14.9, 0.26) |
| Editör 7: Practical rules | "how long the phase will be held" eklendi; Sonuç maddesi 2'ye 100 ms tutmada düz optimum (16–20) eklendi |
| Editör: alt bölüm başlığı | "Robustness to Pilots, Estimation Error and Phase Resolution" |
| Sayısal U4, U7, U8, U11 | ρ'nun ortalama güce göre olduğu ve 30 dB'de senaryo başına medyan 22.6 dB; gecikme seti; "idle" yerine yük ortalaması 0.45; Tablo III başlığına "selected on the reported scenarios"; anlık görüntülerin en yakın ızgara noktasından alındığı yazıldı |
| Sayfa | İkinci turdan sonra 10 sayfaya çıkan metin, bilgi çıkarılmadan sıkılaştırılarak yeniden **9 sayfaya** indirildi. Özet 198 kelime (TWC'ye özgü sınır 75–200). |

**Değiştirilmeyenler:** Tablo III'teki 0.86 ms satırında görünen hızlardan 0.27 çıkıyor, fark sütunu +0.28 diyor (ham fark 0.2760, yuvarlama). Fark sütunu eşli farkın kendisi olduğu için bırakıldı.

## Üçüncü tur (son denetim, `DENETIM_SON.md`)

| Bulgu | Düzeltme |
| --- | --- |
| **K1:** pencere ölçütünde ($\bar R_W$) CD, SU-best-of ile berabere ya da önünde; özet ve Sonuç 1 bunun tersini düşündürüyordu | Ana oturumda ham veriden doğrulandı. W = 50 ms pilotlu: berabere (+0.00 / +0.03 / +0.03, GA'lar sıfırı içeriyor). Taze ön kodlayıcı: +0.100 [0.014, 0.190]. W = 100 ms: 30/60 kHz +0.090 / +0.097 (anlamlı), 15 kHz +0.052 (berabere), taze +0.184. §VI-H'ye cümle eklendi (CD 0.70 s'de, güven ufkunun ötesinde devreye giriyor; model onu kayırıyor; yalnızca ayarlı Adam her pencerede önde). Sonuç 1'e kısıt cümlesi eklendi. Özet: "leaves slow solvers behind tuned Adam". Sınırlılıklar: "ahead of tuned Adam". |
| U1: özet tam 200 kelime | "on one processor thread" → "on one thread". Özet 200 kelime, sınırın içinde. |
| U2: Armijo yeniden sınanmadı | §V: "the Adam sweep of Fig. 3" (kapsam yalnızca Adam; sayfa için ayrıca not düşülmedi). Armijo için tam gecikme değeri: ÜRETİLEMEDİ (koşulmadı). |
| U3: kusurlu CSI'da hızlar çöküyor | 20 dB'de 1.40 b/s/Hz, doğrudan bağlantının (1.74) altında; 10 dB ve altında hızlar sıfıra yakın, beraberlik bir taban etkisi. Metne eklendi. |
| U4: 22.6 dB yalnızca G için | "for the RIS–user channel" |
| U5: 0.02–0.04 yalnızca pilotlu kollar için | "with pilots" eklendi |
| U6: veri ve kod bölümü (GitHub) | **Kullanıcı kararı:** Düzeltilmiş Tablo III betiği ve §VI-H betikleri gönderimden önce genel depoya eklenmeli; ayrıca `make_paper_assets.py` eski Tablo III'ü yazıyor. Metin değiştirilmedi. |
| U7: tohum | "independent mobility draw (seed 12)" |
| U8: dil | "four pilot symbols that carry no data", "subcarrier spacing", "1.33 ms … below that range" |
| Sınırlılıklar cümlesi | Yeniden yazıldı: pilot (%17–32) ve kestirim hatası yavaş çözücüleri ayarlı Adam'ın gerisinde bırakıyor; 2–3 bitte çok taramalı ayrık arama yuvarlanmış sezgisele yeniliyor; 1 bitte tek taramalı arama en iyi yuvarlanmış Adam'la berabere; 10 dB ve altında hızlı yöntemler ayırt edilemiyor. Her parça ham veriyle kontrol edildi. |
| Sayfa | 9 sayfaya indirmek için: Tablo III başlığındaki seçim cümlesi çıkarıldı (§V'de zaten yazıyor), tekrarlanabilirlik cümlesi ve §VI-H girişi kısaltıldı, Sonuç maddesi 2'deki parantez kısaltıldı (16–20 adım §VI-H'de duruyor). Son hâl: 9 sayfa, özet 200 kelime. |

## 4. tur (16 Kasım 2026): "dar bant" sınırlaması — kullanıcı onayıyla

Gerekçe: geniş bant OFDM deneyinde G1 TUTMADI (`thesis_exp/genis_bant/REPORT.md`, en üst bölüm). 24 hücrenin yalnızca 7'sinde L = 48, L*'tan anlamlı olarak kötü. 50–100 MHz'deki 16 hücrenin yalnızca 3'ünde öyle.

| Yer | Önce | Sonra |
| --- | --- | --- |
| Özet | "standardized indoor-office multi-user … downlink"; "the highest rate on the initial channel" | "… narrowband multi-user … downlink"; "the highest initial-channel rate" (kelime sayısını korumak için) |
| Giriş, katkı 2 | "The optimum persists for … every standardized indoor user speed." | "In the narrowband model it holds for … every standardized indoor speed." |
| Sonuç, madde 2 | "Adam's effective rate peaks … and falls with further iterations when" | "Adam's narrowband effective rate peaks … and then falls when" |
| Sınırlar | "…, and the model is narrowband with one geometry." ve "Our next step is wideband OFDM operation, where beam squint …" | "…, and there is one geometry." ve "The interior optimum is narrowband: a first OFDM check kept it for centre-frequency optimization at 20 MHz, but at 50–100 MHz running 48 steps was significantly worse in only 3 of 16 configurations." (Bağımsız denetimden sonra: "often flattened" yerine açık sayı, Kural 10.) |

Not: beam squint cümlesi kaldırıldı. Literatür raporunun tavsiye 8'ine göre bu kurguda beam squint ihmal edilebilir; belirleyici etki frekans seçiciliği. Makale 9 sayfa kaldı.

## 5. tur (16 Kasım 2026): jüri soruları deneylerinden gelen iki ek — kullanıcının "onay bekleme, devam et" talimatıyla

| Yer | Değişiklik | Kaynak |
| --- | --- | --- |
| İlgili çalışmalar, son cümle | "…run time … is not part of the model" → "…the optimizer's own run time, at most a feasibility constraint on its operation count~[Ryu2026], does not enter the aging." Önceki cümle Ryu ve ark. ile çelişiyordu. | `thesis_exp/reports/Geniş bant RIS tez tavsiyeleri.md`; `thesis_exp/juri/REPORT_S3_S1.md` (Soru 3) |
| Kaynakça | `Ryu2026arXiv` eklendi. **DOĞRULANMALI:** yazarların ön adları notlarda yok; künye arXiv sayfasından tamamlanmalı. | araştırma notları |
| Sınırlar | "Latencies come from single-threaded Python. Faster hardware … remains to be measured." → "Latencies come from single-threaded Python: compiled alone (62–63-fold faster), coordinate descent overtakes Python Adam, but an equal speed-up of all methods keeps tuned Adam ahead; …" (Kural 10: makaleyi sınırlayan bulgu) | `thesis_exp/juri/REPORT_S3_S1.md` (Soru 1, sapma 2 sonrası) |
| Sınırlar, yer için | Anlamı korunarak sıkıştırıldı: sabit saçıcılar/anten kazançları cümlesi; pilot/CSI/ayrık faz cümlesi tek cümle ("leave the slow solvers behind"); "1–8 tarama" (Yöntem bölümünde var) ve "keep each update short" (madde 4'te var) çıkarıldı; "faster code" ifadesi kaldırıldı (yeni bulguyla çelişiyordu). | — |

Makale 9 sayfa.

## 6. tur (17 Kasım 2026): Makale 1 ile bağlantı (danışmanın isteği)

| Yer | Değişiklik |
| --- | --- |
| Giriş, 3. paragrafın sonu | Eklendi: "It continues our single-pass phase predictor with a sine–cosine representation~[SavasciSen2026AISY] by asking when such speed pays off once run time is charged." |
| İlgili çalışmalar, "Learning" | Kısaltıldı: "Predicting the sine and cosine of each phase removes the ±π discontinuity of direct phase regression~[SavasciSen2026AISY]." Anlam aynı. |

Makale 9 sayfa. Kaynak listesi: `KAYNAK_LISTESI.md` (49 kaynak; kullanıcı PDF'leri gönderecek, her biri tek tek kontrol edilecek).

## 7. tur (17 Kasım 2026): kaynak kontrolü grup 1'in önerileri (kullanıcı onayıyla)

| Yer | Önce | Sonra | Gerekçe |
| --- | --- | --- | --- |
| Giriş, 1. cümle | "…covered one~[Basar, Wu2019TWC, DiRenzo, Wu2021]" | "…covered one~[Basar, DiRenzo, Wu2021]" | Wu ve Zhang (2019) bir optimizasyon makalesi; kapsama iddiasını zayıf destekliyor. Diğer üçü açıkça destekliyor (`kaynak_kontrol/grup1_kaynak_01_05.md`). |
| Giriş, prototip cümlesi | "RIS hardware has been prototyped~[Dai], and one prototype has strengthened…" | "a 256-element RIS has served as a transmit antenna~[Dai], and another prototype has strengthened…" | Dai ve ark. RIS'i verici anten olarak kullanıyor, yansıtıcı olarak değil (dipnot 1, s. 45914). |
| Sonuç, enumerate sonrası | "latency is therefore not a secondary metric" | "latency is not a secondary metric" | Yer kazanmak için; anlam aynı. |

Makale 9 sayfa. Kaynak numaraları değişti: Wu2019TWC artık ilk cümlede değil.

## 8. tur (17 Kasım 2026): kaynak kontrolü grup 2'nin bulgusu

| Yer | Önce | Sonra | Gerekçe |
| --- | --- | --- | --- |
| İlgili çalışmalar, "RIS phase optimization" paragrafının sonu | "run time, when discussed, is a complexity order, not a latency measured against the coherence time." | "run time is usually a complexity order, and where measured (0.04–13.6 s of CPU time in [Abeywickrama]) it is not compared with the coherence time." | Abeywickrama ve ark., Tablo II'de (s. 5860) MATLAB CPU süresini saniye olarak ölçüyor: ceza yöntemi 2.8–13.6 s, iki aşamalı yöntem 0.04–0.51 s. Eski cümle bu kaynak için yanlıştı (`kaynak_kontrol/grup2_kaynak_06_10.md`). |

Makale 9 sayfa.

## 9. tur (17 Kasım 2026): kaynak kontrolü grup 3'ün bulgusu

| Yer | Önce (8. tur) | Sonra | Gerekçe |
| --- | --- | --- | --- |
| İlgili çalışmalar, aynı cümle | "…and where measured (0.04–13.6 s of CPU time in [Abeywickrama]) it is not compared with the coherence time." | "…and where measured, on fixed channel realizations [Abeywickrama, Yu2019ICCC, Shi2011TSP], it is not compared with the coherence time." | Yu ve ark. (Şekil 4, s. 739–740) ve Shi ve ark. (Şekil 4, s. 4337) de çalışma süresini ölçüyor, ama sabit kanal üzerinde (`kaynak_kontrol/grup3_huang_yu_shi_jiang_monga.md`). |

Grup 3'ün isteğe bağlı önerileri uygulanmadı:
- Jiang'ı "policies" yerine "pilotlardan grafik sinir ağı ile" diye anmak;
- Yu2019ICCC başlığındaki "(Invited Paper)" ibaresi.

Doğrulanamayanlar: Yu2019ICCC'nin DOI'si ve Monga2021SPM'nin cilt/sayısı PDF'te basılı değil. Makale 9 sayfa.

## 10. tur (17 Kasım 2026): kaynak kontrolü grup 4'ün bulgusu (Kural 10: makalenin iddiasını sınırlıyor)

| Yer | Önce | Sonra | Gerekçe |
| --- | --- | --- | --- |
| İlgili çalışmalar, "Learning" paragrafının sonu | "…and classical baselines are rarely tuned or timed under the same conditions." | "…; even when both are timed on one machine [Samuel, Sun, Hu, Liu2022], the classical baseline runs to convergence or a fixed iteration count, not to the same latency." | Dört kaynak, öğrenme tabanlı ve klasik yöntemi aynı makinede saniye cinsinden zamanlıyor (Samuel s. 2560–2561; Sun s. 5444, 5446; Hu Tablo VIII s. 1406; Liu Tablo V s. 4795). Bu yüzden "timed under the same conditions" yanlıştı. Doğru kalan: klasik yöntem aynı gecikme bütçesine ayarlanmıyor ve süre eşevreli kalma süresiyle ilişkilendirilmiyor (`kaynak_kontrol/grup4_liu_samuel_hu_sun_pellaco.md`). |

Makale 9 sayfa. Bu düzeltme makalenin katkısını daraltıyor ama ortadan kaldırmıyor. Katkı artık "süre ölçülmüyor" değil, "süre aynı gecikme bütçesine ve kanal hızına bağlanmıyor".

## 11. tur (17 Kasım 2026): kaynak kontrolü grup 5'in bulguları

| Yer | Önce | Sonra | Gerekçe |
| --- | --- | --- | --- |
| İlgili çalışmalar, "Mobility" paragrafı | "forecasts the position and beam direction of fast unmanned aerial vehicles [Liu2021WCL]" | "forecasts the position of fast unmanned aerial vehicles and points the beam at it [Liu2021WCL]" | LSTM yalnızca konumu öngörüyor; hüzme açısı konumdan hesaplanıyor (s. 668). |
| Aynı paragraf, özgünlük cümlesi | "the optimizer's own run time, at most a feasibility constraint on its operation count [Ryu], does not enter the aging." | "the optimizer's own run time is at most checked for feasibility, as an operation count [Ryu] or a measured 2 ms against a 20 ms slot [Liu2021WCL], and does not enter the aging." | Liu ve ark. öngörü süresini ölçüyor (τc = 2 ms, i7-6700 ve GTX 1080) ve yalnızca 20 ms'lik zaman diliminden kısa olduğunu kontrol ediyor (s. 672). Süre eskimeye girmiyor; özgünlük cümlesi geçerli, kapsamı genişletildi. |

**Açık konu (kullanıcının kararı):** Makale 1'in kaynakça girdisindeki `volume={8}, number={9}`, PDF'ten doğrulanamıyor. PDF "Early View" sürümü: DOI var, cilt ve sayı yok. Wiley şeridinde "0" yazıyor, üst veride "0.0:e70460" var. Makale bir sayıya atandıysa cilt ve sayı doğrulanmalı; atanmadıysa bu alanlar kaldırılmalı. Makale 9 sayfa.

## 12. tur (17 Kasım 2026): kaynak kontrolü grup 6'nın bulgusu

| Yer | Önce | Sonra | Gerekçe |
| --- | --- | --- | --- |
| İlgili çalışmalar, özgünlük cümlesi | "…where modeled, is a fixed parameter;" | "…where modeled, is fixed, even where computation is named as a cause [Truong2013JCN];" | Truong ve Heath hesaplama gecikmesini eskimenin nedenleri arasında açıkça sayıyor (s. 338, 341), ama gecikmeyi sabit alıyor (D = 1 çerçeve; Tablo 1'de 1–10 ms). Cümle, "hesaplama gecikmesini eskimeye ilk biz bağlıyoruz" diye okunmasın diye daraltıldı. Katkı: süre ölçülmüş ve yönteme bağlı, sabit değil. |
| Kaynakça | Truong2013JCN: "R. W. Heath" | "R. W. Heath Jr." | PDF'te basılı hâli. |

Makale 9 sayfa (`kaynak_kontrol/grup6_han_truong_chopra_jindal_zhao.md`).

## 13. tur (17 Kasım 2026): kaynak kontrolü grup 7'nin önerileri

| Yer | Değişiklik | Gerekçe |
| --- | --- | --- |
| İlgili çalışmalar, çalışma süresi cümlesi | "where measured, on fixed channel realizations [Abeywickrama, Yu, Shi]" → "[…, Cao2022TWC]" | Cao ve ark. iterasyon başına süreyi MATLAB'da ölçüyor ("millisecond level", s. 10433–10434; Şekil 7), ama slot ya da çerçeve süresiyle karşılaştırmıyor; süre eskime gecikmesine girmiyor. |
| Sonuç, sınırlar | "RIS switching time is not modeled" → "RIS switching time (≥0.72 ms in [Zhao2024OJCOMS]) is not modeled" | 2 bitlik prototipte yeni faz desenine geçiş en az 0.72 ms (s. 4890). Sınırlamaya ölçek veriyor. |

Peel (düzenlileştirilmiş ZF, λ = Kσ²/P) ve Nadeem (maks-min SINR) doğru; künyelerin hepsi uyuşuyor. Makale 9 sayfa (`kaynak_kontrol/grup7_cao_wu_zhao_peel_nadeem.md`).

## 14. tur (17 Kasım 2026): eleman kazancı, Tang ve ITU (kullanıcı onayıyla); 9 sayfa için sıkıştırma

| Yer | Değişiklik | Gerekçe |
| --- | --- | --- |
| Sistem modeli, Tang cümlesi | "follows the two-hop model of [Tang] with a cos^q element pattern." → "follows the free-space two-hop model of [Tang] with a cos^q power pattern (q = 1); we add the TR 38.901 excess loss and shadowing to each hop. Our element gain, 2(2q+1), exceeds Tang's 2(q+1); the latter lowers absolute rates by about 5% and leaves L* and the best method unchanged." | Kaynak kontrolü grup 8 ve `thesis_exp/kazanc_duyarlilik/REPORT.md`. Seed 11'de L*'daki etkin hız 6.151 → 5.845 (1.5 m/s) ve 5.913 → 5.622 (10 km/h); L* 6 ve 4, en iyi kol değişmiyor. |
| Hız tablosu | "18 & ITU, veh." → "18 & ours, ITU veh." | ITU'da 18 km/h değeri yok; 10–120 km/h araç sınıfının içinde bizim seçtiğimiz bir hız. |
| Sistem modeli, sınırlar | "The effect of fixed scatterers on the optimal step count is not known." kaldırıldı | Artık doğru değil. Jüri S2: korelasyon tabanı olmayan Clarke kanalında da iç optimum var (`thesis_exp/juri/REPORT_S4_S2.md`). |
| Sonuç, sınırlar | "Fixed scatterers make long-horizon rates, and independent per-antenna gains absolute rates, optimistic; the findings hold with shared gains." kaldırıldı | Sistem modeli bölümünün sınırlar paragrafını tekrar ediyordu. |
| İlgili çalışmalar | Üç cümle aynı anlamla kısaltıldı: Huang, Liu2021WCL, ayrık faz. Özgünlük cümlesindeki örnekler bir atıf listesine indirildi: "is at most a feasibility check [Ryu, Liu2021WCL]". | Yer için. |
| Şekil 1 altyazısı | "showing the first scenario of the aging set as produced by the channel generator" → "(first scenario of the aging set)" | Yer için. |

Makale 9 sayfa.

## 15. tur (17 Kasım 2026): bulunamayan kaynaklar çıkarıldı (kullanıcının talimatı: "riske gerek yok, çıkar"); grup 9

| Yer | Önce | Sonra |
| --- | --- | --- |
| Sistem modeli | "log-normal shadowing with Gudmundson correlation [Gudmundson1991] at 5 m" | "log-normal shadowing with exponential spatial correlation at 5 m" |
| Hareketlilik | "T_c = 0.423/f_d = 28.2 ms [Clarke, Rappaport]" | "T_c = √(9/(16π))/f_d ≈ 0.423/f_d = 28.2 ms" (katsayı kendi başına doğrulanabilir: √(9/(16π)) = 0.4231; 0.4231/15.01 Hz = 28.19 ms) |
| Gecikme analizi | "J0(2πu) ≈ 1 − π²u² [Clarke, Rappaport]" | "… [Clarke]" (J0'ın Taylor açılımı) |
| Yöntem | "paired bootstrap confidence intervals (CIs) [Efron1993]" | atıfsız |
| Yöntem, pilot | "With the scheme of [Wang2020TWC], 48 pilot symbols suffice…" | "With the uplink scheme of [Wang2020TWC] and TDD reciprocity, 48 pilot symbols suffice…" (grup 9: kaynak yukarı bağlantı pilotlarına dayanıyor; 48 = 4 + 32 + max(3, 12), denklem 62) |

Kaynakça 49 → 46 (Gudmundson1991, rappaport_wireless, Efron1993 artık atıf almıyor). Makale 9 sayfa.

## 16. tur (17 Kasım 2026): kaynak kontrolü grup 10 ve künye düzeltmeleri

| Yer | Değişiklik | Gerekçe |
| --- | --- | --- |
| Özet | "in a standardized indoor-office…" → "in an indoor-office…" | 3GPP'nin InH senaryosu 120×50×3 m, 3 km/h (TR 38.901 Tablo 7.2-2). Bizim oda ve hız farklı; yalnızca kanal modeli 3GPP'den. |
| Giriş | "in the 3GPP indoor-office scenario with walking users [3gpp_channel]" → "in an indoor office with walking users and the 3GPP TR 38.901 channel model [3gpp_channel]" | Aynı gerekçe. |
| Sistem modeli | "LoS probability" → "mixed-office LoS probability" | Kod, TR 38.901 Tablo 7.4.2-1'in mixed-office satırını kullanıyor. |
| İlgili çalışmalar | "is at most a feasibility check [Ryu, Liu]" → "is at most a feasibility check or a fixed overhead [Ryu, Liu]" | Ryu ve ark. T_opt'u amaçta sabit bir ek yük olarak da kullanıyor (denklem 13–15); süre FLOP'tan tahmin ediliyor, eskimeye girmiyor. |
| Kaynakça, Ryu2026arXiv | yalnızca soyadlar → "S. Ryu, S. Choi, H. J. Yang, J. M. Cioffi"; "arXiv:2608.25393v1, submitted to IEEE Trans. Wireless Commun." | PDF'te basılı hâli. |
| Kaynakça, 3gpp_nr_phy | V16.2.0 → V16.3.0 | Kontrol edilen belge V16.3.0. Kullanılan tanımlar (Tablo 4.2-1, 4.3.2-1) aynı. |
| Kaynakça, SavasciSen2026AISY | "volume={8}, number={9}" kaldırıldı | PDF "Early View": cilt ve sayı yok. Doğrulanamayan alanlar risk olmasın diye çıkarıldı; e70460 ve DOI kaldı. Makale bir sayıya atandıysa yeniden eklenmeli. |

Makale 9 sayfa, 46 kaynak.

## 17. tur (17 Kasım 2026): son okuma denetiminin bulguları (`DENETIM_FINAL.md`; 7 orta bulgu ve 3 küçük bulgu)

| Yer | Önce | Sonra |
| --- | --- | --- |
| Yöntem | "…shows what changes for faster code." | "…shows what changes for a faster Adam step." (§VI-C yalnızca Adam adımını ölçekliyor; derlenmiş CD bulgusuyla çelişmesin) |
| Sonuç, madde 1 | "The solvers with the best rate on paper lose to…" | "At the measured step costs, the slow solvers lose to…" |
| Sonuç, sınırlar | "…leave the slow solvers behind;" | "…leave the slow solvers behind tuned Adam;" (§VI-H ile uyum) |
| Sonuç, sınırlar | "compiled alone (62–63-fold faster), coordinate descent overtakes Python Adam" | "if only coordinate descent is compiled (62–63-fold faster), it overtakes Python Adam" |
| Özet | "…long-run Adam, the methods with the highest initial-channel rate," | "…long-run Adam, two solvers with high initial-channel rates," (Adam-48'in t = 0 hızı CD'ninkinden yüksek) |
| Sonuçlar, §VI-D | "at the user speeds of the standards: …18 km/h (5 m/s)…" | "at the speeds of the standards and two higher ones: …18 km/h (5 m/s, our choice in the vehicular class)…" |
| İlgili çalışmalar | "and where measured, on fixed channel realizations […], it is not compared…" (yüklemsiz) | "and where it is measured, on fixed channel realizations […], it is not compared…" |
| Giriş, Sonuç, §VI-E başlığı | "each update should still be short" / "Updates Stay Short" | "short updates (at most 8 steps) suffice" / "Short Updates Suffice" (§VI-E'nin kendi metniyle ve Tablo III ile uyumlu) |
| Giriş, katkı 2 | "In the narrowband model it holds for…" | "In the narrowband model the optimum persists for…" |
| Sonuç | "centre-frequency" | "center-frequency" (ABD yazımı) |

Uygulanmayan küçük bulgular `DENETIM_FINAL.md`'de listeli ve isteğe bağlı: Şekil 3 altyazısı, statik küme toplamı, §VI-H'deki CD 0.70 s, iş parçacığı cümlesi, 30 dB CSI açıklaması. Makale 9 sayfa.

## 18. tur (22 Kasım 2026): statik kümenin bölmesi (madde 19)

Kaynak: `veri_bolme/kontrol_bolme.py` → `veri_bolme/veri_bolme.json`. Kod 6000 senaryoyu rastgele 70/15/15 böler (`ris_mu/features.py:split_indices`, tohum 0): 4200/900/900. Öğrenilen güncelleme kuralı en iyi epoch'unu 500 doğrulama senaryosunda seçer (`scripts/mumiso_unrolled.py`). Adam bunların ilk 400'ünde ayarlanır. Sonuçlar 900 test senaryosunun 600'ünde raporlanır (`mumiso_equal_step.py`, `mumiso_latency_parity.py`). Makaledeki 4200 + 400 + 600 = 5200 bu yüzden eksikti. Kalan 800 senaryonun 100'ü yalnızca öğrenilen kuralın epoch seçiminde kullanıldı; 700'ü ne seçimde ne makaledeki sayılarda kullanıldı (eğitim betiği 900 test senaryosunun hepsinde bir `test_min` yazıyor, ama bu değer hiçbir yerde kullanılmıyor). Sonuçlarda hiçbir sayı değişmedi.

| Yer | Önce | Sonra |
| --- | --- | --- |
| §V-A, statik küme | "6000 scenarios without mobility, of which 4200 are used for training, 400 for validation and 600 for testing." | "6000 scenarios without mobility, split at random 4200/900/900 (training/validation/test); the learned update is validated on 500, Adam on 400 of these, and results use 600 test scenarios." |
| §V-A, ışın kümesi | "400 further scenarios with 6 scatterers." | "400 more scenarios, 6 scatterers." (yer kazanmak için; bilgi aynı) |
| §V-A | "The generator is not prefix-stable, so every trained model is evaluated with the sample count it was trained with." | "The generator is not prefix-stable; trained models are evaluated at their training sample count." (aynı) |
| §V-C | "and most measurements are repeated in several rounds. These are latencies of unoptimized Python code (…)" | "and most are repeated in several rounds; the code is unoptimized Python (…)" (aynı) |
| §V-C | "The $N=64$ step-time ratio of 1.04 comes from one round on 20 scenarios." | "The $N=64$ step-time ratio (1.04) is from one round on 20 scenarios." (aynı; bağımsız denetimden sonra, "from a load average of 0.45" ifadesi yükün ölçüm öncesinde alındığını korumak için geri getirildi) |

Makale 9 sayfa, 46 kaynak; `audit_claims.py --all` 126/126, `check_claims.py` 120/120. `DENETIM_FINAL.md` madde 15 bununla kapandı.

## 19. tur (22 Kasım 2026): doğrulama alt kümesinin sağlamlığı

Kullanıcının onayıyla, kapanmış ölçüm fazına istisna; yalnızca hızlar, zamanlama yok. Betik `veri_bolme/saglamlik_900.py` → `saglamlik_900.json`, `saglamlik_900.log`.
- **V0 (Adam 400 doğrulama, 600 test):** yayımlanan sayıları birebir üretti (fark 0). Betik doğru çalışıyor.
- **V1a (Adam 500 doğrulama, 600 test):** Adam her bütçede (L = 1…64) yine 0.75 / soft-min seçiyor. Bütün sonuçlar ve iddialar aynı: öğrenilen kural her L'de önde, kazanma oranı %68–84, her öğrenilen nokta 5 zamanlama turunun 5'inde baskınlanıyor.
- **V1 (500 doğrulama, 900 test):** Adam tarafı hesaplandı. Öğrenilen kural için ağırlık arşivi (`ris_mu_agirliklar_2026-10-27.tar.gz`) gerekiyor; arşiv bu ortamda olmadığı için **ÜRETİLEMEDİ**.

| Yer | Önce | Sonra |
| --- | --- | --- |
| §V-A, statik küme | "6000 scenarios without mobility, split at random 4200/900/900 (training/validation/test); the learned update is validated on 500, Adam on 400 of these, and results use 600 test scenarios." | "6000 static scenarios, randomly split 4200/900/900 (training/validation/test); the learned update is validated on 500, Adam on 400 of these (all 500 give the same choice); results use 600 test scenarios." |

Makale 9 sayfa.
