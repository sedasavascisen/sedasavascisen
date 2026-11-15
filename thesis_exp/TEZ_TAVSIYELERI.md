# Tez için tavsiyeler — iki makaleden bir tez (12 Kasım 2026; 15 Kasım'da güncellendi)

Bu bir mentorluk notu; tez metni değil. Sayılar denetimden geçmiş raporlardan (`AYRINTILI_RAPOR.md`,
denetim turları 1–11. Tur 3 ayrık faz deneyinde kaba ızgara hatası (K3), tur 7 Makale 2 Tablo III'te yuvarlama hatası (K4) buldu; ikisi de düzeltildi, hükümler değişmedi. Özet metinlerdeki genelleme hataları da düzeltildi). Kararlar sizin ve danışmanınızın.

---

## 1) İki makale tek bir hikâye anlatıyor — bunu bilinçli kurun

- **Makale 1 (AISY):** "Sin/cos gösterimi ±π süreksizliğini çözüyor; CNN–LSTM fazı ~2.8° hatayla tahmin ediyor."
- **Makale 2 (TWC):** "Hareketli RIS'te hesaplama gecikmesi yöntem sıralamasını belirliyor."

Bunlar iki ayrı konu gibi duruyor. Köprü deneyi (Görev 3) ikisini birleştirebilecek bir bulgu verdi, ama doğru çerçevelenmeli (denetim U52). Değerlendirilen ağ Makale 1'in ağının kendisi değil: Makale 1'in tek geçişli, faz-farkında (sin/cos) yaklaşımını çok kullanıcılı sisteme taşıyan, etiketsiz eğitilmiş bir ağ (MuMisoNet). RMSE ile değerlendirilmedi. Bulgu: **tek geçişli öğrenilen tahmin, etkin hız ölçütünde her hızda klasik kollarca baskınlanıyor** (5.4 km/h'de en iyi klasik kola göre −1.418 b/s/Hz). t=0 hızı fiilen SU-average düzeyinde (4.626'ya 4.624). Bu, Makale 1'in *yaklaşımının* çok kullanıcılı ve hareketli senaryoda karşılığını vermediğini gösteriyor, Makale 1'in kendi sonuçlarını değil:

> *Ölçüt seçimi hükmü değiştirir. Doğruluk ölçütü gecikmeyi görmez; etkin hız görür.* (Not: bu cümle, aynı ağın iki ölçütte farklı sıralandığını göstermiyor; köprüde RMSE ölçülmedi. Cümle çerçeve olarak kullanılacaksa bunun ayrıca gösterilmesi gerekir.)

Önerim: Makale 1'i tezde "geleneksel değerlendirmenin" örnek olayı olarak konumlayın. Makale 2'nin çerçevesi bu olaya uygulanınca sonuç tersine dönüyor. Bu, tezin üç ekseninden "yapay zekâ / öğrenme" eksenini de kapatıyor:
- tek geçişli ağ baskınlanıyor;
- öğrenilen güncelleme kuralı adım başına kazanıp milisaniye başına kaybediyor (adım başına süre oranı L=8'de 2.7–2.8 kat; tanımdan bağımsız, p4/optimize_sure);
- bu titiz bir negatif sonuç.

## 2) Açık konuşmam gereken risk: Makale 1'in denetim bulguları

Makale için "düzeltme gerekmiyor" kararınızı yeniden tartışmıyorum. Ama **tez ayrı bir belge** ve jüri iki makaleyi de okuyacak. Denetimde, yumuşatmadan yazıyorum (Kural 10), bir jüri üyesinin kolayca yakalayabileceği şunlar çıktı:

| Bulgu | Neden jüri yakalar |
| --- | --- |
| Denklem 8'deki etiket, doğrudan bağlantıyı yok sayıyor; optimum değil | Tek satırlık bir türetmeyle gösterilebiliyor |
| 1/2/3 bit RMSE'leri (4.12/3.08/2.81°) matematiksel olarak imkânsız (alt sınır 51.95/25.98/12.98°) | Nicemleme hatası adım/√12; ders kitabı bilgisi |
| Klasik yöntemlerin ~104° RMSE'si ortak faz farkından geliyor | Ortak faz çıkarılınca CD 1.10° |
| Tablo 8 ve bazı şekiller elle yazılmış | Kod paketi incelenirse görülür |

**Tavsiye (tez için, makale için değil):**
1. Tezin Makale 1 bölümünde etiket (b)'yi kullanın.
2. Bağımsız yeniden üretimi tohum yayılımıyla verin (3.18/2.77/3.90°).
3. İmkânsız nicemleme sayılarını ve Tablo 8 projeksiyonunu teze taşımayın. N=256 için ölçülen değer elinizde (2.25°, tek tohum; ek tohumlar 13 Kasım'da sizin isteğinizle durduruldu).
4. "Yeniden üretilebilirlik ve sınırlar" başlıklı kısa bir alt bölüm yazın. Jürinin bulacağı bir şeyi sizin önceden söylemeniz, savunmada güç kaybı değil, kazancıdır.
5. Bunu savunmadan önce danışmanınızla açıkça konuşun. Denetim raporu (`audit/AUDIT_REPORT.md`) bu görüşme için hazır.

## 3) Savunmanın güçlü yanı: jürinin soracağı her soruya ölçülmüş bir yanıt var

| Muhtemel soru | Yanıtınız | Kaynak |
| --- | --- | --- |
| "Gecikme donanıma bağlı, sonuçlarınız genellenir mi?" | Normalize adım maliyeti x = ΔT·f_d; hüküm mutlak ms'ye değil x'e bağlı. Yeniden ölçümde Adam 1.66 → 1.328 ms oldu, L* 5 → 6, bulgu korundu | x'in tanımı: MAKALE_REHBERI.md:348, paper_mobility/DANISMAN_GORUSME_NOTLARI.md:29 (ölçekleme yasası bu denetimde yeniden sınanmadı); yeniden ölçüm: infra/REPORT.md |
| "Pilot yükünü bedava saydınız" | Ücretlendirildi: mutlak hız %17–32 düşüyor, 50 ms pencerede pilot ücretli seçilen koldan ayırt edilemeyen küme Adam-3…20 (seçilen Adam-6/8), yavaş çözücüler en altta; taze W ile eşli karşılaştırma yapılmadı (pencere uzunluğu için bir alt satır) | p4/onkodlayici_siralama |
| "Fazı ne sıklıkla yeniden hesaplıyorsunuz? Optimum buna bağlı değil mi?" | **Evet, bağlı — bunu siz söyleyin.** Faz 25 / 50 / 100 ms tutulursa doğrulamada seçilen kol Adam-5 / 6–8 / 16–20; seçilen koldan ayırt edilemeyen küme Adam-3…8 / Adam-3…20 / Adam-10…48 (15 kHz'de 25 ms'de Adam-2 de, 100 ms'de Adam-5…48). Bu okuma yalnızca gecikmesi pencereden kısa kollar için geçerli (CD/PGA'da değil). 100 ms'de farklar küçük (Adam-6 0.02–0.04 geride; 15 kHz'de anlamlı değil; Adam-3 0.05–0.08 geride). Yavaş çözücü her durumda geride. Tez cümlesi "gecikme sıralamayı belirler" korunuyor, ama "birkaç adım her zaman en iyidir" denmemeli: optimum, gecikme ile yeniden hesaplama aralığının birlikte fonksiyonu. | p4/onkodlayici_siralama §3b |
| "Pilot ve kestirim hatası birlikte?" | 30 dB'de hızlı yöntemin üstünlüğü küçülüyor ama sürüyor; 20 dB'de seçilen Adam-2 SU-best-of'tan ayırt edilemiyor; Adam-48 SU-best-of'u küçük ama anlamlı farkla (+0.03) geçiyor; yavaş çözücüler her iki düzeyde de geride. | p4/onkodlayici_csi |
| "Tablo III'teki sıcak başlangıç kazancı ne kadar güvenilir?" | Benzetim pilot süresini ızgaraya yuvarlıyordu; düzeltilmiş kopyada kazanç 0.86 ms'de 0.276, 1.71 ms'de 0.092 (makale 0.222 / 0.146). İşaret ve hüküm aynı. Tezde düzeltilmiş değerleri kullanın; bunlar makalenin 1.6625 ms/adım gecikmesiyle hesaplandı, yeni 1.328 ms ile değil (tam satırlar p4/takip_duzeltme REPORT §2; T_p = 0'da da 0.52 → 0.53 ve iki hücrede seçilen L değişiyor); hakem sorarsa bu kopya hazır. | p4/takip_duzeltme |
| "CSI kusursuz değil" | Pilot SNR'i 30 dB'de bile etkin hız 6.08 → 3.54; en iyi L hatayla tekdüze değişmiyor; 10 dB ve altında yöntemler ayırt edilemiyor. Dikkat: ρ kümenin ortalama gücüne göre, senaryo başına etkin SNR daha düşük (30 dB → medyan 22.6 dB) | p4/kusurlu_csi |
| "Gerçek RIS ayrık fazlı" | 1/2/3 bitte de içsel optimum var (L* = 5/6/6); yavaş ayrık CD 2 ve 3 bitte kaybediyor, 1 bitte berabere | p4/ayrik_faz |
| "Kanalı öngörseniz?" | Gürültüsüz geçmişle +0.19…+0.42 kazanç; %1 kestirim hatasıyla bütün öngörücüler öngörüsüzün altında | p4/kanal_ongoru |
| "Konum biliniyorsa CSI'ya gerek var mı?" | Geometri tabanlı faz SU-best-of'un 0.83–0.86 altında | p4/konum_faz |
| "Öğrenilen yöntemi optimize etseydiniz?" | L=8'de öğrenilen adım Adam'dan 2.67–2.81 kat yavaş (üç farklı süre tanımında da). torch.compile bu kodda optimize bir sürüm sayılamaz (yeniden derleme sınırı, karmaşık sayılar); GPU ölçülmedi | p4/optimize_sure |
| "GPU?" | **Ölçülmedi (ÜRETİLEMEDİ).** Dürüst yanıt: tek senaryoluk küçük işlemlerde çekirdek başlatma yükü baskın; ama bu iddia ölçümsüz | — |

Bu tabloyu savunma hazırlığının omurgası yapın. Her satır için tek bir şekil ve tek bir sayı yeterli.

## 4) Zayıf yanlar — sahiplenin, saklamayın

1. **Tek kanal modeli:** sabit saçıcılar, düz yörünge, iç mekân. Öngörü sonuçları bu yüzden iyimser. "Gerçekçi senaryo" ekseni kısmi; bunu tezde sınır olarak yazın.
2. **Etkin hız ölçütleri:** iki farklı ölçüt var. Tanım 1 anlık; pilot deneyi 50 ms ortalaması kullanıyor. Tezde ikisini karıştırmayın. Pencere uzunluğu en iyi adım sayısını değiştiriyor (25 / 50 / 100 ms → Adam-5 / 6–8 / 16–20).
3. **Gecikme muhasebesi:** Adam-L gecikmesi SU-average başlangıcını (0.30 ms) içermiyor. Eklenince etkin hız kol başına 0.0001–0.021 b/s/Hz düşüyor (p4/gecikme_muhasebesi). Dar farklarda bunu belirtin.
4. **GPU ölçümü yok.**
5. **(Kapandı) 3 bit çok kullanıcılı ayrık faz 13 Kasım'da koşuldu:** L* = 6, yavaş ayrık CD belirgin geride (p4/ayrik_faz).

## 5) Ölçüm fazının kalan günleri (20 Kasım'a kadar, 15 Kasım itibarıyla 5 gün) — öncelik sırası

| # | İş | Neden | Maliyet |
| --- | --- | --- | --- |
| 1 | ~~Makale 1 eğitimleri~~ — 13 Kasım'da kullanıcı isteğiyle durduruldu | — | — |
| 2 | ~~3 bit ayrık faz~~ — yapıldı (13 Kasım) | — | — |
| 3 | ~~50 ms pencere duyarlılığı~~ — yapıldı (14–15 Kasım); sonuç savunma için önemli (yukarıdaki tablo) | Pilot sonucunun sağlamlığı (§4.2) | ~1.5 saat |
| 4 | ~~Pilot ücreti + kusurlu CSI birlikte~~ — yapıldı (14–15 Kasım) | En gerçekçi rejim; 14–15 Kasım'da sınandı (p4/onkodlayici_csi) | ~2–3 saat; isteğe bağlı |
| 5 | Yeni p4 sayılarını bir iddia denetleyicisine bağlamak | `audit_claims.py` gibi; sabotaj testiyle | Küçük. Kural 2 gereği `thesis_exp/` altında ayrı bir betik olmalı; onayınızı ister |

**Açmayın:** öngörücü faz tasarımı (dönüşlü yörünge yok), yeni öğrenilen modeller, GPU arayışı. 20 Kasım'dan sonra yeni deney açılmıyor; bu tarihten sonra eksik kalan her şey "gelecek çalışma" olur ve bu meşrudur.

## 6) Yazım fazı için yapı önerisi (yalnızca iskelet)

1. Giriş: savunu cümlesi ve üç eksen
2. Arka plan: RIS, hareketlilik, eskime, faz optimizasyonu
3. Faz süreksizliği ve tek geçişli öğrenme (Makale 1; etiket (b), bağımsız yeniden üretim, sınırlar)
4. Etkin hız çerçevesi: Tanım 1–2, içsel optimum L*, normalize maliyet (Makale 2'nin çekirdeği)
5. Sağlamlık: pilot yükü, kusurlu CSI, ayrık faz, öngörü, konum (Görev 4)
6. Öğrenmenin sınırları: köprü, öğrenilen güncelleme kuralı, optimize süreler (titiz negatif sonuç)
7. Gerçekçi senaryo (38.901, kısmi) ve sınırlar
8. Sonuç ve gelecek çalışma

Her bölümün başına "bu bölümün tek iddiası" ve "onu taşıyan sayı + kaynak dosya" yazın. `TEZ_YAZIM_REFERANSI.md` tek doğruluk kaynağı olsun. Docstring'ten ya da hafızadan sayı almayın; CLAUDE.md'deki "17 kat → 11.7–14.2 kat" dersi bunun için var.

## 7) Danışman görüşmesi için gündem önerisi

1. Makale 1 denetim bulgularının **tezde** nasıl ele alınacağı (§2).
2. Makale 2 hakem sürecinde pilot yükü sorulursa elinizdeki yanıt (§3, satır 2).
3. §5'teki 2–4 numaralı işler yapıldı (15 Kasım); kalan tek madde 5 (iddia denetleyicisi). Ayrıca Tablo III'ün düzeltilmiş değerlerinin makale hakem sürecinde nasıl ele alınacağı (p4/takip_duzeltme).
4. Bölüm iskeleti (§6) ve yazım takvimi.

## 8) Kişisel not

İki ayda bir tezi bitirmek sıkışık ama yapılabilir. Elinizdeki malzeme sandığınızdan güçlü. Ana sonuç pek çok sağlamlık testinden geçti:
- yeniden ölçülen gecikmeler;
- pilot yükü;
- kusurlu CSI (orta-yüksek SNR'de; 10 dB ve altında yöntemler ayırt edilemiyor, yani orada hüküm yok);
- ayrık faz;
- optimize süreler.

Negatif sonuçlar (öğrenme ekseni) zayıflık değil; titizlikle yapıldıkları için tezin en savunulabilir kısmı. En büyük risk teknik değil, Makale 1'in jüri önünde hazırlıksız yakalanması. Onu önceden konuşmak sizin elinizde.
