# Tez yol haritası (17 Kasım 2026)

> Bu bir plan; tez metni değil (Kural 9). Her bölüm, dayanağı olan rapora ve sayılara bağlı. Sayıların hepsi ölçülmüş, ön kayıtlı ve bağımsız olarak denetlenmiş. Ölçüm fazı kapandı; bundan sonrası yazım.

## Tezin tek cümlesi

**Hareketli RIS sistemlerinde hesaplama gecikmesi, yöntem sıralamasını belirleyen birinci sınıf bir tasarım kısıtıdır; bu tez bu kısıtı ölçer, yasasını çıkarır ve onu kullanan bir denetleyici tasarlar.**

"Ne tasarladın?" sorusunun cevabı:

> Hareketli kullanıcıya hizmet eden RIS için, ölçülen Doppler'e ve donanım gecikmesine bakarak her güncellemede başlangıcı ve adım sayısını seçen gecikme farkındalıklı bir denetleyici tasarladım. Hiç görülmemiş bir çekilişte, sabit ayarlı en güçlü taban çizgisini +0.087 b/s/Hz geçiyor ve olası en iyi seçime 0.003 b/s/Hz yaklaşıyor.

## Bölümler

| # | Bölüm | İçerik | Dayanak | Durum |
| --- | --- | --- | --- | --- |
| 1 | Giriş | Savunu cümlesi, katkılar, tezin hikâyesi | `thesis_exp/juri/HIKAYE.md` | İskelet hazır |
| 2 | Arka plan ve literatür | RIS, faz optimizasyonu, kanal eskimesi, öğrenme; literatür boşluğu | `literatur_pdf/TABLO.md`; `makale2_revizyon/kaynak_kontrol/TOPLU_RAPOR.md`; `reports/Geniş bant RIS tez tavsiyeleri.md` | Kaynaklar doğrulandı |
| 3 | Sistem modeli | Kanal (TR 38.901 + Tang), hareketlilik, etkin hız tanımı | Makale 2 §III–IV; `kazanc_duyarlilik/REPORT.md` | Hazır; eleman kazancı notu yazılmalı |
| 4 | Faz gösterimi (Makale 1) | sin/cos gösterimi, tek geçişli tahmin, faz hatası ölçütü | Makale 1; S5 ve S5b | Makale yayımlandı. Tezde etki tohuma bağlı diye yazılmalı. |
| 5 | Gecikme ve etkin hız (Makale 2) | Sıralamanın tersine dönmesi, içsel optimum L*, x = ΔT·f_d yasası, pilot, CSI, ayrık faz | Makale 2 (9 s., kaynakları kontrol edildi) | Gönderime hazır |
| 6 | Tasarım kuralı | L*'ı önceden seçen kural, ön kayıtlı sınama | `tasarim_kurali/REPORT.md` (medyan kayıp %0.08) | Hazır |
| 7 | Sağlamlık: jürinin soruları | Gerçekleştirme oranı (S1), Clarke kanalı (S2), Ryu farkı (S3), ön kodlayıcı eskimesi (S4) | `juri/REPORT_S3_S1.md`, `REPORT_S4_S2.md` | Hazır |
| 8 | Geniş bant OFDM | Kaç alt taşıyıcı kararı; 100 MHz'de K_opt = 16, +0.28; iç optimum dar banda özgü | `genis_bant/REPORT.md` | Hazır |
| 9 | **Tasarlanan sistem** | Gecikme farkındalıklı denetleyici, mühürlü test, üç tasarım kararının ayrı katkıları | `sistem/SISTEM_RAPORU.pdf`, `FINAL.md`, `FINAL_EK.md` | Hazır |
| 10 | Yapay zekâ ekseni | Öğrenilen güncelleme kuralı; 28 GHz testi; titiz olumsuz sonuç ve değerlendirme protokolü | `juri/REPORT_S5.md`, `REPORT_S5b.md`; Makale 2 | Hazır |
| 11 | Sonuç | Katkılar, tasarım kuralları, sınırlar, gelecek çalışma | Bu belge | Yazılacak |

## Bölüm 9 için öneri: "tasarım" nasıl anlatılmalı

Sistemin kazancı üç ayrı kararın birleşiminden geliyor. Her birini ayrı ölçülmüş katkı olarak anlatmak, jüri karşısında en savunulabilir yol:

1. **Başlangıç seçimi:** SU-best-of; kapalı forma karşı kazancın yaklaşık %59'u.
2. **Adım sayısı seçimi:** eskime eğrisinden; en güçlü sabit seçime karşı +0.040…+0.087.
3. **Sıcak başlangıç:** önceki fazdan; periyodik kipte +0.051; yalnızca periyot kısayken kazandırıyor.

Bunlara iki ek tasarım kuralı eşlik ediyor:
- **Doppler kestirimi:** ±%20 hata zararsız; düşük kestirmek daha pahalı.
- **Zaman ölçekleri:** ön kodlayıcı her slotta tazelenmeli; RIS fazı daha yavaş döngüde kalabilir.

## Zaman çizelgesi (yaklaşık 2 ay)

| Hafta | İş |
| --- | --- |
| 1 (17–23 Kasım) | Makale 2'nin son okuması ve gönderimi. Makale 1'in cilt ve sayısı. GitHub deposuna betiklerin eklenmesi. |
| 2–3 | Bölüm 3, 5, 6 ve 7. Makale 2'den genişletilerek; en hazır olanlar. |
| 4 | Bölüm 8 ve 9: geniş bant ve tasarlanan sistem. |
| 5 | Bölüm 4 ve 10: faz gösterimi ve yapay zekâ ekseni, olumsuz sonuçlar dürüstçe. |
| 6 | Bölüm 1, 2 ve 11: giriş, literatür, sonuç. |
| 7 | Danışman okuması ve düzeltmeler. |
| 8 | Savunma sunumu; jüri soru-cevap provası (`juri/JURI_RAPORU.pdf` hazır). |

## Açık kararlar ve riskler

| Konu | Durum | Öneri |
| --- | --- | --- |
| RIS eleman kazancı (kod 6, Tang 4) | Makalede belirtildi; etkisi küçük (mutlak hızlar ~%5 düşük, sıralama aynı) | Tezde de aynı notla yazılmalı; paket değiştirilmedi. |
| Tek geometri ve tek kanal modeli | En büyük sınır | Gelecek çalışma olarak yazılmalı. Clarke kanalı sağlamlık kontrolü olarak var. |
| Makale 1'in künyesi | Cilt ve sayı doğrulanmadı | Wiley sayfasından kontrol et. |
| Ölçüm fazı | Kapalı | Yeni deney açılmamalı. İstisna: jüri ikinci bir geometri isterse, aynı ön kayıtla tek bir genellenebilirlik testi. |
| Python gecikmesi | Sıralama gecikme oranına bağlı (S1) | Tezde "sıralamayı dil değil, gecikme oranı belirler" diye yazılmalı. |

## Jüriye en olası beş soru ve hazır cevapları

`juri/JURI_RAPORU.pdf` dosyasında her biri ölçülmüş cevapla yer alıyor:
1. Gerçekleştirme;
2. L*'ın fiziksel olup olmadığı;
3. Ryu ve ark.'tan fark;
4. Ön kodlayıcı eskimesi;
5. Yapay zekâdan geriye ne kaldığı.

Altıncı olası soru "ne tasarladın?". Cevabı yukarıda ve `sistem/SISTEM_RAPORU.pdf` dosyasında.
