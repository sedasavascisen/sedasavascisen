# Tez için tavsiyeler — iki makaleden bir tez (12 Kasım 2026)

Bu bir mentorluk notu; tez metni değil. Sayılar denetimden geçmiş raporlardan (`AYRINTILI_RAPOR.md`,
tur 1: yanlış sayı yok). Kararlar sizin ve danışmanınızın.

---

## 1) İki makale tek bir hikâye anlatıyor — bunu bilinçli kurun

- **Makale 1 (AISY):** "Sin/cos gösterimi ±π süreksizliğini çözüyor; CNN–LSTM fazı ~2.8° hatayla tahmin ediyor."
- **Makale 2 (TWC):** "Hareketli RIS'te hesaplama gecikmesi yöntem sıralamasını belirliyor."

Bunlar iki ayrı konu gibi duruyor. Ama köprü deneyi (Görev 3) ikisini birleştiren bulguyu verdi: **Makale 1'in ağı kendi ölçütünde (RMSE) iyi görünüyor, etkin hız ölçütünde ise her hızda baskınlanıyor** (5.4 km/h'de en iyi klasik kola göre −1.418 b/s/Hz). Bu, Makale 1'i tezde yetim bırakmaz, savunu cümlesinin kanıtı yapar:

> *Ölçüt seçimi hükmü değiştirir. Doğruluk ölçütü gecikmeyi görmez; etkin hız görür.*

Önerim: Makale 1'i tezde "geleneksel değerlendirmenin" örnek olayı olarak konumlayın. Makale 2'nin çerçevesi bu olaya uygulanınca sonuç tersine dönüyor. Bu, tezin üç ekseninden "yapay zekâ / öğrenme" eksenini de kapatıyor:
- tek geçişli ağ baskınlanıyor;
- öğrenilen güncelleme kuralı adım başına kazanıp milisaniye başına kaybediyor (optimize edilmiş sürelerde de 2.8–3.1 kat yavaş);
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
3. İmkânsız nicemleme sayılarını ve Tablo 8 projeksiyonunu teze taşımayın. N=256 için ölçülen değer elinizde (2.25°, ek tohumlar sürüyor).
4. "Yeniden üretilebilirlik ve sınırlar" başlıklı kısa bir alt bölüm yazın. Jürinin bulacağı bir şeyi sizin önceden söylemeniz, savunmada güç kaybı değil, kazancıdır.
5. Bunu savunmadan önce danışmanınızla açıkça konuşun. Denetim raporu (`audit/AUDIT_REPORT.md`) bu görüşme için hazır.

## 3) Savunmanın güçlü yanı: jürinin soracağı her soruya ölçülmüş bir yanıt var

| Muhtemel soru | Yanıtınız | Kaynak |
| --- | --- | --- |
| "Gecikme donanıma bağlı, sonuçlarınız genellenir mi?" | Normalize adım maliyeti x = ΔT·f_d; hüküm mutlak ms'ye değil x'e bağlı. Yeniden ölçümde Adam 1.66 → 1.328 ms oldu, L* 5 → 6, bulgu korundu | infra/REPORT.md |
| "Pilot yükünü bedava saydınız" | Ücretlendirildi: mutlak hız %17–32 düşüyor, en iyi kol kümesi (Adam-4…8) ve yavaş çözücülerin yeri değişmiyor | p4/onkodlayici_siralama |
| "CSI kusursuz değil" | Pilot SNR'i 30 dB'de bile etkin hız 6.08 → 3.54; hata arttıkça L* küçülüyor; 10 dB altında yöntemler ayırt edilemiyor | p4/kusurlu_csi |
| "Gerçek RIS ayrık fazlı" | 1/2 bitte de içsel optimum var (L* = 5/6); yavaş ayrık CD 2 bitte kaybediyor | p4/ayrik_faz |
| "Kanalı öngörseniz?" | Gürültüsüz geçmişle +0.19…+0.42 kazanç; %1 kestirim hatasıyla bütün öngörücüler öngörüsüzün altında | p4/kanal_ongoru |
| "Konum biliniyorsa CSI'ya gerek var mı?" | Geometri tabanlı faz SU-best-of'un 0.83–0.86 altında | p4/konum_faz |
| "Öğrenilen yöntemi optimize etseydiniz?" | torch.compile hızlandırmadı; oran 2.8–3.1 kat | p4/optimize_sure |
| "GPU?" | **Ölçülmedi (ÜRETİLEMEDİ).** Dürüst yanıt: tek senaryoluk küçük işlemlerde çekirdek başlatma yükü baskın; ama bu iddia ölçümsüz | — |

Bu tabloyu savunma hazırlığının omurgası yapın. Her satır için tek bir şekil ve tek bir sayı yeterli.

## 4) Zayıf yanlar — sahiplenin, saklamayın

1. **Tek kanal modeli:** sabit saçıcılar, düz yörünge, iç mekân. Öngörü sonuçları bu yüzden iyimser. "Gerçekçi senaryo" ekseni kısmi; bunu tezde sınır olarak yazın.
2. **Etkin hız ölçütleri:** iki farklı ölçüt var. Tanım 1 anlık; pilot deneyi 50 ms ortalaması kullanıyor. Tezde ikisini karıştırmayın; 50 ms'nin duyarlılığı henüz denenmedi.
3. **Gecikme muhasebesi:** Adam-L gecikmesi SU-average başlangıcını (0.30 ms) içermiyor. Etkisi ~0.016 b/s/Hz. Dar farklarda bunu belirtin.
4. **GPU ölçümü yok.**
5. **3 bit çok kullanıcılı ayrık faz koşulmadı** (CLAUDE.md "jüri soracak" diyor).

## 5) Ölçüm fazının kalan 8 günü (20 Kasım'a kadar) — öncelik sırası

| # | İş | Neden | Maliyet |
| --- | --- | --- | --- |
| 1 | Süren eğitimlerin bitmesi (N=64/128/256, tohumlar) | RMSE–N eğrisi, tohum yayılımıyla | Sürüyor (~10 saat) |
| 2 | 3 bit ayrık faz (çok kullanıcılı) | Jüri sorusu; eğriler hazır altyapıda | Eğitimlerden sonra boş makinede ~1 saat |
| 3 | 50 ms pencere duyarlılığı (25/100 ms) | Pilot sonucunun sağlamlığı (§4.2) | ~1.5 saat |
| 4 | Pilot ücreti + kusurlu CSI birlikte | En gerçekçi rejim; iki etki birlikte hiç sınanmadı | ~2–3 saat; isteğe bağlı |
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
3. 20 Kasım'a kadar §5'teki 2–4 numaralı işlerden hangilerinin yapılacağı.
4. Bölüm iskeleti (§6) ve yazım takvimi.

## 8) Kişisel not

İki ayda bir tezi bitirmek sıkışık ama yapılabilir. Elinizdeki malzeme sandığınızdan güçlü. Ana sonuç pek çok sağlamlık testinden geçti:
- yeniden ölçülen gecikmeler;
- pilot yükü;
- kusurlu CSI;
- ayrık faz;
- optimize süreler.

Negatif sonuçlar (öğrenme ekseni) zayıflık değil; titizlikle yapıldıkları için tezin en savunulabilir kısmı. En büyük risk teknik değil, Makale 1'in jüri önünde hazırlıksız yakalanması. Onu önceden konuşmak sizin elinizde.
