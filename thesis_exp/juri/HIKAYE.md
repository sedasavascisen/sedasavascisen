# Tezin hikâyesi: ölçülmüş bulgularla bir anlatı iskeleti

> Bu bölüm bir tez metni değildir (Kural 9). Tezin bölümlerini birbirine bağlayan neden-sonuç zincirini, her halkayı ölçülmüş ve denetlenmiş bir sayıya dayandırarak gösterir. Cümleler savunma ve yazım için bir iskelettir; tezdeki ifade sana aittir. Makale 1'in kendi sayıları burada kullanılmadı, çünkü Makale 1 bu çalışmanın denetim kapsamı dışında.

## Savunu cümlesi

**Hareketli RIS sistemlerinde hesaplama gecikmesi ikincil bir ölçüt değil; yöntemlerin sıralamasını belirleyen birinci sınıf bir tasarım kısıtıdır.**

## Zincir: altı halka

### 1. Başlangıç sorusu: daha doğru faz, daha iyi sistem mi? (Makale 1)

Makale 1, RIS fazını tek geçişte tahmin eden bir ağ kurar ve fazın ±π süreksizliğini sin/cos gösterimiyle giderir. Başarı ölçütü faz hatasıdır (RMSE). Bu, tezin ilk sorusunu doğurur: faz hatasını azaltmak sistemin hızını da artırır mı?

### 2. Kırılma: ölçüt merdiveni

Faz hatası, t = 0 hızı ve etkin hız aynı yöntemleri farklı sıralar.
- **Faz hatası:** iyi bir faz, ortak faz kayması kadar "yanlış" görünebilir.
- **t = 0 hızı:** fazı, verildiği kanal üzerinde değerlendirir.
- **Etkin hız:** fazı, yöntem işini bitirdiğinde var olan kanal üzerinde değerlendirir. Kullanıcı yürürken bu ikisi aynı kanal değildir.

Tezin dönüm noktası şu tespittir: hareketli bir kullanıcı için doğru ölçüt etkin hızdır, ve etkin hız gecikmeyi kaçınılmaz olarak içerir.

### 3. Ana sonuç: gecikme sıralamayı belirliyor (Makale 2)

Etkin hızla değerlendirildiğinde:
- t = 0'da en iyi olan yavaş çözücüler (koordinat inişi ve uzun koşulu Adam, 0.9–5.9 s) 2.5 ms'lik basit bir sezgisel yönteme kaybeder.
- Adam'ın bir **içsel optimumu** vardır: 1.5 m/s'de 4–6 adım. 48 adıma kadar koşmak %14 kaybettirir.
- Optimum tek bir sayıya, adım süresinin Doppler frekansına oranına (x = ΔT·f_d) bağlıdır.
- Öğrenilen bir güncelleme kuralı adım başına kazanır, milisaniye başına kaybeder.

### 4. Kural: optimumu önceden seçmek (tasarım kuralı)

İçsel optimum bir gözlem olarak kalmaz, önceden hesaplanabilir. 1.5 m/s'de kalibre edilen bir kural, hiç görmediği hızlarda ve çekilişte sınandı (ön kayıtlı, 60 koşul). Doğru L'yi seçmeye göre medyan kayıp **%0.08**, en kötü **%2.74**. Sabit bir L seçmek ise ortalama %3.0–3.6 kaybettiriyor.

### 5. Sağlamlık: jürinin beş sorusu (bu çalışma)

| Soru | Ölçülmüş yanıt |
| --- | --- |
| "Bu bir model yapaylığı mı?" | Korelasyon tabanı olmayan Clarke kanalında da içsel optimum var: 3–8 adım, güven ufkunun içinde. |
| "Ön kodlayıcı da eskirse?" | Her şey ~1 ms içinde çöküyor. Ön kodlayıcıyı her slotta tazelemek zorunlu. Ön kodlayıcı hızlı döngüde, RIS fazı yavaş döngüde: iki zaman ölçeği bir tasarım gereği. |
| "Ryu ve ark.'tan farkınız?" | Fark, hesaplama süresinin eskimeye katılması. Süreyi yalnızca bütçe kısıtı yapan seçim 0.43–1.41 b/s/Hz kaybettiriyor. |
| "C ile yazsaydınız?" | Yalnızca CD derlenirse sıralama döner (başa baş 10–15 kat). Bütün yöntemler eşit hızlanırsa Adam önde kalır. Sıralamayı dil değil, **gecikme oranı** belirler. Bu, savunu cümlesinin en keskin biçimi, ama "hız kesinliği yener" artık koşullu bir cümle. |
| "Yapay zekâdan ne kalıyor?" | Aşağıda, 6. halka. |

### 6. Taç: geniş bant OFDM, yeni bir zaman bütçesi ekseni (geniş bant deneyi)

Tek bir RIS faz vektörü bütün alt taşıyıcılara hizmet eder. Bu, yeni bir karar doğurur: optimizasyona kaç alt taşıyıcı (K_opt) alınacak? Her ek alt taşıyıcı adımı pahalılaştırır.
- 20 MHz'de dar bant amacı yetiyor.
- 100 MHz'de 16 alt taşıyıcı üzerinden optimize etmek, ~9 kat adım maliyetine rağmen en iyi dar bant kolunu **+0.28…+0.29 b/s/Hz** geçiyor. Bu sonuç 200 ms güven ufku içinde de geçerli.
- Gecikme geniş bantta da kararı belirliyor; bu kez iki eksende: kaç adım, kaç alt taşıyıcı.
- Dürüst sınır: dar banttaki içsel optimum geniş bantta genelleşmiyor (50–100 MHz'de 16 hücrenin yalnızca 3'ünde).

## Yapay zekâ ekseninin kapanışı

Tez, öğrenmeye en elverişli rejimi bilerek aradı: 28 GHz, 1.5 m/s, T_c ≈ 3 ms.
- **Kalite tavanı:** 0.43 ms'de karar veren ağ, 1.24 ms'lik SU-best-of'un 0.38 gerisinde. 4 kat veri, 3 tohum ve 2 kat geniş ağla bu açık −0.31…−0.36'ya iniyor ama kapanmıyor.
- **Ağ öğreniyor:** veri artınca optimizasyonsuz SU-average'ı +0.04…+0.09 geçiyor. Ama tavanı, tek kullanıcı hizalamalarının en iyisinin altında.
- **Makale 1'le bağ:** sin/cos avantajı bu kurguda tohuma bağlı; üç tohumdan yalnızca birinde anlamlı.

Bu, yapay zekâ ekseninin titiz bir olumsuz sonuçla kapanması demek. Kapsamı: bu mimari ailesi ve bu eğitim bütçesi. Tezde öğrenmenin katkısı bir yöntem olarak değil, bir **değerlendirme protokolü** olarak kalıyor: öğrenilen her yöntem, ölçülmüş gecikmede ve her bütçede ayarlanmış klasik bir rakibe karşı değerlendirilmeli.

## Harmoni: iki makale ve geniş bant tek cümlede

Makale 1, fazı doğru tahmin etmeyi sordu. Makale 2, doğru sorunun "fazın ne zaman hazır olduğu" olduğunu gösterdi. Tasarım kuralı bunu önceden hesaplanabilir yaptı. Geniş bant deneyi, zaman bütçesinin ikinci bir eksenini (kaç alt taşıyıcı) ekledi. Jüri deneyleri de sonucun kanal modeline, ön kodlayıcı varsayımına ve gerçekleştirme diline karşı nerede dayanıp nerede koşullu olduğunu ölçtü.

## Tezde açıkça yazılması gereken sınırlar

- Sıralama, gerçekleştirmenin gecikme oranına bağlı. Python ölçümü bu oranın bir örneği; donanım ve derleyici oranı değiştirir.
- Tek geometri; sabit saçıcılı model. Clarke modeli, karşıt bir uç olarak yalnızca bir sağlamlık kontrolü.
- Ön kodlayıcının taze olduğu varsayımı zorunlu bir tasarım gereği; ihlal edilirse sonuçlar geçersiz.
- Geniş bant deneyinde CD ayarlanmadı. İçsel optimum dar banda özgü.
- Yapay zekâ hükmü tek mimari ailesiyle sınırlı.

## Dayanaklar

| Halka | Rapor |
| --- | --- |
| 3 | Makale 2 revize kopyası, `thesis_exp/makale2_revizyon/` |
| 4 | `thesis_exp/tasarim_kurali/REPORT.md` |
| 5 | `thesis_exp/juri/REPORT_S3_S1.md`, `REPORT_S4_S2.md` (bu PDF) |
| 6 | `thesis_exp/genis_bant/REPORT.md` (ayrıca gönderildi) |
| YZ kapanışı | `thesis_exp/juri/REPORT_S5.md`, `REPORT_S5b.md` (bu PDF) |
