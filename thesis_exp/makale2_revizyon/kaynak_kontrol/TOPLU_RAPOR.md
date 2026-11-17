# Makale 2 kaynak kontrolü: toplu rapor (17 Kasım 2026)

## Kısaca

- **Kapsam:** makalenin 49 kaynağının 46'sı kaynağın kendi PDF'ine karşı tek tek kontrol edildi. Her atıf cümlesi, kaynağın ilgili sayfasıyla karşılaştırıldı.
- **Çıkarılan kaynaklar:** PDF'ine ulaşılamayan 3 kaynak, senin talimatınla çıkarıldı. Atıf aldıkları cümleler, kaynağa gerek kalmayacak biçimde yeniden yazıldı.
- **Hatalı atıf yok:** hiçbir kaynak yanlış bir şey için gösterilmemiş. Künyelerin hepsi doğru; yalnızca dört künyede küçük tamamlama ya da düzeltme yapıldı.
- **Asıl düzeltmeler genellemelerde:** makalenin literatür hakkındaki bazı genel cümleleri, kaynakların gerçekte yaptığından daha kesin konuşuyordu. Bunlar düzeltildi.
- **Özgünlük iddiası ayakta:** hiçbir kaynak, optimizatörün ölçülmüş çalışma süresini kanal eskimesine katmıyor.
- **Makale:** 9 sayfa, 46 kaynak. Ayrıntılı değişiklikler `DEGISIKLIKLER.md` dosyasında (7.–16. turlar).

## 1. Literatürle ilgili düzeltilen genellemeler (en önemlisi)

| Makaledeki eski iddia | Kaynaklar ne gösterdi | Yeni ifade |
| --- | --- | --- |
| Çalışma süresi "ele alındığında bir karmaşıklık mertebesidir". | Abeywickrama, Yu, Shi ve Cao süreyi saniye ya da milisaniye olarak ölçüyor, ama sabit bir kanalda. | Süre çoğunlukla karmaşıklık mertebesi; ölçüldüğünde sabit kanalda ölçülüyor ve eşevreli kalma süresiyle karşılaştırılmıyor. |
| Klasik yöntemler "nadiren aynı koşullarda zamanlanıyor". | Samuel, Sun, Hu ve Liu (2022), öğrenme tabanlı yöntemi ve klasik yöntemi aynı makinede zamanlıyor. | Aynı makinede zamanlansalar bile klasik yöntem yakınsamaya ya da sabit bir yineleme sayısına kadar koşuyor, aynı gecikme bütçesine göre ayarlanmıyor. |
| Gecikme "sabit bir parametre" ve çalışma süresi modelde yok. | Truong ve Heath hesaplama gecikmesini eskimenin nedeni olarak adlandırıyor ama sabit alıyor. Liu (2021) süreyi ölçüyor (2 ms), yalnızca 20 ms'lik slota sığdığını kontrol ediyor. Ryu, süreyi FLOP'tan tahmin edip kısıt ya da sabit ek yük olarak kullanıyor. | Gecikme sabit, hesaplama bir neden olarak anılsa bile; çalışma süresi en çok bir uygulanabilirlik kontrolü ya da sabit ek yük, eskimeye girmiyor. |

Bu üç düzeltme tezin katkısını ortadan kaldırmıyor, ama daha kesin tanımlıyor. Katkı "literatür süreyi hiç ölçmüyor" değil; şu: **ölçülen süre, kanalın eskimesine ve aynı gecikme bütçesine bağlanmıyor.**

## 2. Modelle ilgili bir bulgu

**RIS eleman kazancı.** Kod, Tang ve ark.'ın formülünün verdiği 4 yerine 6 kullanıyor; RIS yolu 1.5 kat güçlü. Etkisi paketi değiştirmeden ölçüldü (`thesis_exp/kazanc_duyarlilik/REPORT.md`):
- mutlak hızlar yaklaşık %5 düşüyor;
- L*, kayıplar, CD'nin konumu ve en iyi yöntem değişmiyor.

Makaleye bu fark ve etkisi tek cümleyle yazıldı.

## 3. Küçük düzeltmeler

- **Coğrafi kapsam:**
  - "3GPP kapalı ofis senaryosu" ifadesi kaldırıldı. Bizim oda ve hızımız 3GPP'ninkinden farklı; yalnızca kanal modeli 3GPP'den geliyor.
  - "Standardized" kelimesi özetten çıkarıldı.
  - LoS olasılığının "mixed-office" tablosundan geldiği belirtildi.
- **ITU:** hız tablosundaki 18 km/h satırı "ours, ITU veh." oldu. ITU'da 18 km/h değeri yok.
- **Wang ve ark.:** 48 pilot sayısı doğru: 4 + 32 + max(3, 12) = 48. Yöntem yukarı bağlantı pilotlarına dayandığı için "TDD karşılıklılığı" varsayımı eklendi.
- **Dai ve ark.:** prototip, RIS'i verici anten olarak kullanıyor; cümle buna göre yazıldı.
- **Wu ve Zhang (2019):** "RIS kapsama sağlar" cümlesinden çıkarıldı; o cümleyi diğer üç kaynak doğrudan destekliyor.
- **Liu (2021):** sinir ağı hüzme yönünü değil, konumu öngörüyor; cümle düzeltildi.
- **Cao ve Zhao (2024):** ölçülmüş süre listesine Cao eklendi. RIS anahtarlama süresi için ölçek eklendi: en az 0.72 ms.
- **Eskimiş cümle:** "sabit saçıcıların optimum adım sayısına etkisi bilinmiyor" cümlesi kaldırıldı. Clarke kanalı deneyi bu soruyu yanıtladı.

## 4. Künye düzeltmeleri

| Kaynak | Düzeltme |
| --- | --- |
| Ryu ve ark. | Ön adlar eklendi: S. Ryu, S. Choi, H. J. Yang, J. M. Cioffi; arXiv v1, IEEE TWC'ye gönderilmiş. |
| Truong ve Heath | "R. W. Heath Jr." |
| 3GPP TS 38.211 | V16.2.0 → V16.3.0 (kontrol edilen sürüm; kullanılan tanımlar aynı). |
| Makale 1 | "Cilt 8, sayı 9" çıkarıldı; PDF "Early View", cilt ve sayı yok. Makale bir sayıya atandıysa Wiley sayfasından eklenmeli. |

## 5. Çıkarılan kaynaklar

| Kaynak | Ne için atıf alıyordu | Yerine |
| --- | --- | --- |
| Gudmundson (1991) | Gölgeleme korelasyon modeli | Model tarif edildi: "üstel uzamsal korelasyon". |
| Rappaport (kitap) | T_c = 0.423/f_d | Katsayı formülüyle yazıldı: √(9/(16π)) ≈ 0.423. Kaynağa gerek kalmadan doğrulanabiliyor. |
| Efron ve Tibshirani (kitap) | Bootstrap yöntemi | Atıf kaldırıldı; standart yöntem. |

## 6. Kaynak başına sonuç

Bütün kaynaklar **DOĞRU** çıktı. Bazılarında atfın geçtiği cümle netleştirildi ya da kaynak bir listeye eklendi; çıkarılması gereken kaynak yok.

| Grup | Kaynaklar | Sonuç |
| --- | --- | --- |
| 1 | Basar; Wu ve Zhang (2019); Di Renzo; Wu (2021); Dai | Doğru. Wu ve Zhang ilk cümleden çıktı; Dai cümlesi netleşti. |
| 2 | Pei; Abeywickrama; Pan; Guo; Choi | Doğru. Abeywickrama genellemenin düzeltilmesine yol açtı. |
| 3 | Huang (2020); Yu; Shi; Jiang; Monga | Doğru. Yu ve Shi genellemeye eklendi. |
| 4 | Liu (2022); Samuel; Hu; Sun; Pellaco | Doğru. "Aynı koşullarda zamanlanmıyor" genellemesi düzeltildi. |
| 5 | Papazafeiropoulos; Liu (2021); Makale 1; Zhang; Huang (2022) | Doğru. Liu (2021) cümlesi düzeltildi; Makale 1 künyesi düzeltildi. |
| 6 | Han; Truong; Chopra; Jindal; Zhao (2021) | Doğru. Özgünlük cümlesi Truong'a göre daraltıldı. |
| 7 | Cao; Wu (2020); Zhao (2024); Peel; Nadeem | Doğru. Cao ve Zhao (2024) eklemeleri yapıldı. |
| 8 | Kingma; ITU-R M.2410; Armijo; Tang | Doğru. Tang ile kazanç farkı ve ITU tablo satırı düzeltildi. |
| 9 | Zheng; Wang | Doğru. TDD varsayımı eklendi. |
| 10 | Ryu; 3GPP TR 38.901; TR 38.913; TS 38.211; Clarke | Doğru. 3GPP senaryo ifadesi, Ryu künyesi ve TS sürümü düzeltildi. |

Her kaynak için ayrıntılı kontrol (sayfa, alıntı, değerlendirme) `kaynak_kontrol/grup1…grup10` dosyalarında.

## 7. Senin yapman gerekenler

1. Makale 1 bir sayıya atandıysa, cilt ve sayıyı Wiley sayfasından ekle.
2. Makale 2'nin "Data Availability" bölümündeki GitHub deposuna düzeltilmiş betikleri ekle (daha önce not edilmişti).
3. Göndermeden önce makaleyi son bir kez oku. Bugünkü değişikliklerin hepsi `DEGISIKLIKLER.md` dosyasında, önce ve sonra hâlleriyle duruyor.
