# Tez yol haritası (17 Kasım 2026)

> Bu bir plan; tez metni değil (Kural 9). Her bölüm, dayanağı olan rapora ve sayılara bağlı. Sayıların hepsi ölçülmüş, ön kayıtlı ve bağımsız olarak denetlenmiş. Ölçüm fazı kapandı; bundan sonrası yazım.

## Düzeltme 1: başlık ve kapsam

Tasarlanan şey bir yüzey değil, yüzeyin **kontrolü**. Başlık ya da ilk paragraf bunu açıkça söylemeli. Öneriler (son karar sende ve enstitünün kurallarında):
- "Hareketli Kullanıcılar için Gecikme Farkındalıklı Yeniden Yapılandırılabilir Akıllı Yüzey Kontrolü"
- "Yeniden Yapılandırılabilir Akıllı Yüzeylerde Zaman Bütçeli Faz Kontrolü: Ölçüm, Yasa ve Denetleyici Tasarımı"

Başlık değiştirilemiyorsa ilk paragraf şöyle sınırlanmalı: "Bu tezde 'RIS tasarımı', yüzeyin donanımı değil, hareketli kullanıcılar için faz kontrolünün tasarımı anlamında kullanılmıştır."

## Düzeltme 4: temel tasarım ilkesi (tezin başında, sınırlar bölümünde değil)

**İki zaman ölçeği:** ön kodlayıcı her slotta (≤ 1 ms) güncel kanaldan tazelenir; RIS fazı daha yavaş, gecikmesi ölçülmüş bir döngüde güncellenir. Bu bir varsayım değil, ölçülmüş bir zorunluluk: ön kodlayıcı RIS fazıyla birlikte eskirse sistem yaklaşık 1 ms içinde çöküyor (1.15 ms'de 5.41 → 4.03 b/s/Hz; `juri/REPORT_S4_S2.md`). Tezin bütün sonuçları bu ilkenin içinde geçerlidir. Bölüm 3, bu ilkeyle açılmalı.

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
| 4 | Faz hatası ölçütünün sınırı (Makale 1) | Tek geçişli tahminle faz hatasını küçültmek; ama faz hatası, hareketli sistemde başarıyı ölçmüyor. Bu bölüm, tezin ölçüt merdiveninin ilk basamağı: faz hatası → t = 0 hızı → etkin hız. | Makale 1; S5 ve S5b | Düzeltme 3'e göre yeniden konumlandırılmalı (aşağıda). |
| 5 | Gecikme ve etkin hız (Makale 2) | Sıralamanın tersine dönmesi, içsel optimum L*, x = ΔT·f_d yasası, pilot, CSI, ayrık faz | Makale 2 (9 s., kaynakları kontrol edildi) | Gönderime hazır |
| 6 | Tasarım kuralı | L*'ı önceden seçen kural, ön kayıtlı sınama | `tasarim_kurali/REPORT.md` (medyan kayıp %0.08) | Hazır |
| 7 | Sağlamlık: jürinin soruları | Gerçekleştirme oranı (S1), Clarke kanalı (S2), Ryu farkı (S3), ön kodlayıcı eskimesi (S4) | `juri/REPORT_S3_S1.md`, `REPORT_S4_S2.md` | Hazır |
| 8 | Geniş bant OFDM | Kaç alt taşıyıcı kararı; 100 MHz'de K_opt = 16, +0.28; iç optimum dar banda özgü | `genis_bant/REPORT.md` | Hazır |
| 9 | **Tasarlanan sistem** | Gecikme farkındalıklı denetleyici, mühürlü test, üç tasarım kararının ayrı katkıları | `sistem/SISTEM_RAPORU.pdf`, `FINAL.md`, `FINAL_EK.md` | Hazır |
| 10 | Yapay zekâ ekseni | Öğrenilen güncelleme kuralı; 28 GHz testi; titiz olumsuz sonuç ve değerlendirme protokolü | `juri/REPORT_S5.md`, `REPORT_S5b.md`; Makale 2 | Hazır |
| 11 | Sonuç | Katkılar, tasarım kuralları, sınırlar, gelecek çalışma | Bu belge | Yazılacak |

## Düzeltme 3: Makale 1'in yeri

Makale 1, tezde **yöntemin yeniliği olarak değil, başlangıç noktası olarak** anlatılmalı.
- sin/cos gösterimi RIS'te ve başka alanlarda daha önce kullanıldı (Fondo-Ferreiro ve ark.; Makale 1'in kendi "Note on Novelty" bölümü).
- Bu tezin kendi deneyinde, çok kullanıcılı ve hız tabanlı eğitimde avantajı tohuma bağlı çıktı: 3 tohumdan 1'inde anlamlı (`juri/REPORT_S5b.md`).
- Makale 1'in teze katkısı: faz tahminini tek geçişe indirmek ve başarıyı faz hatasıyla ölçmek. Tezin geri kalanı, bu ölçütün hareketli kullanıcıda yetmediğini gösteriyor; anlatıyı başlatan soru buradan doğuyor.

## Bölüm 9 için öneri: "tasarım" nasıl anlatılmalı

**Düzeltme 2:** kazanç yüzde olarak ve ayrı kararlar hâlinde verilmeli. Kaynak: mühürlü test, seed 41; `sistem/katki_ayrisimi.py` → `katki_ayrisimi.json`.

| Karar | Katkı [%95 GA] | Yüzde |
| --- | --- | --- |
| Başlangıç seçimi (SU-average → SU-best-of) | +0.057 [+0.036, +0.079] | %1.14 |
| Koşula göre adım sayısı (kapalı form → denetleyici) | +0.040 [+0.029, +0.052] | %0.79 |
| Toplam, makalenin kapalı formuna göre | +0.097 [+0.077, +0.118] | %1.94 |
| En iyi sabit hatta göre | +0.087 [+0.072, +0.103] | %1.73 |
| Periyodik kip: sıcak başlangıcın değeri | +0.051 [+0.036, +0.066] | %0.99 |
| Periyodik kip: sıcak başlangıçlı kapalı forma göre | +0.020 [+0.010, +0.030] | %0.39 |

**Nasıl söylenmeli:** "Denetleyici, en güçlü sabit seçimi %1–2 geçiyor ve kâhine 0.003 b/s/Hz yaklaşıyor. Bunun değeri büyük bir kazanç değil, ayarsız çalışması: hiçbir koşul için elle ayar gerekmeden, hız, taşıyıcı ve tutma süresi değiştikçe en iyiye yakın kalıyor. Sabit bir ayar ise yalnızca kalibre edildiği koşullarda iyi."


Bunlara iki ek tasarım kuralı eşlik ediyor:
- **Doppler kestirimi:** ±%20 hata zararsız; düşük kestirmek daha pahalı.
- **Zaman ölçekleri:** ön kodlayıcı her slotta tazelenmeli; RIS fazı daha yavaş döngüde kalabilir.

## Düzeltme 5: gelecek çalışma, somut deney planıyla

| # | Deney | Neyi kapatır | Ölçüt |
| --- | --- | --- | --- |
| 1 | İkinci geometri (farklı oda boyutu, RIS konumu, N = 64), aynı ön kayıtlı hipotezlerle | Tek geometri itirazı | L* tasarım kuralıyla öngörülüyor mu (medyan kayıp ≤ %1)? |
| 2 | Ölçülmüş kanal (RIS'li bir ölçüm veri seti ya da test yatağı) | Simülasyon itirazı | Etkin hız sıralaması ve iç optimum korunuyor mu? |
| 3 | Gerçek donanım gecikmesi (GPU, FPGA ya da derlenmiş C; bütün yöntemler aynı düzeyde) | Python gecikmesi itirazı | Gecikme oranları ve başa baş oranı r* |
| 4 | RIS anahtarlama süresini (≥ 0.72 ms) gecikmeye eklemek | Eksik gecikme bileşeni | 28 GHz'de denetleyicinin seçimi değişiyor mu? |
| 5 | Ön kodlayıcı döngüsünü pilot ve kestirim hatasıyla birlikte ana sonuca katmak | Kusursuz CSI varsayımı | Denetleyicinin kâhine uzaklığı |

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
