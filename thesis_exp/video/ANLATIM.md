# Savunma videosu: anlatım metni

## 1. Hareketli kullanıcılar için gecikme farkındalıklı RIS kontrolü

Sayın jüri üyeleri, bu tezde yeniden yapılandırılabilir akıllı yüzeylerin, yani RIS'in, hareketli kullanıcılar için nasıl kontrol edilmesi gerektiğini inceledim. Burada tasarım derken yüzeyin donanımını değil, fazlarını ne zaman ve nasıl hesapladığımızı, yani kontrolünü kastediyorum.
Tezin tek cümlelik iddiası şudur: hareketli RIS sistemlerinde hesaplama gecikmesi ikincil bir ölçüt değil, yöntemlerin sıralamasını belirleyen birinci sınıf bir tasarım kısıtıdır.
Bu videoda önce problemi ve senaryoyu, sonra kodları ve ölçümleri, en sonunda da bu kısıtı kullanan, tasarladığım denetleyiciyi anlatacağım.

## 2. Problem: kanal, karar verilene kadar değişir

Problem şu. Yürüyen bir kullanıcı kanalı onlarca milisaniyede değiştirir. Üç gigahertzde, saniyede bir buçuk metre hızla yürüyen bir kullanıcı için eşevreli kalma süresi yaklaşık yirmi sekiz milisaniyedir.
Oysa dikkatli bir optimizasyon algoritması saniyeler sürebilir. Cevap hazır olduğunda soru değişmiştir.
İlk makalemde fazı tek geçişte tahmin eden bir ağ kurdum ve başarıyı faz hatasıyla ölçtüm. Bu tez, o makalenin bıraktığı sorudan doğdu: faz hatasını azaltmak, hareketli bir kullanıcı için hızı da artırır mı? Bunu yanıtlamak için her yöntemi, işini bitirdiği anda var olan kanal üzerinde değerlendirdim.

## 3. Senaryo: kapalı ofis, yürüyen kullanıcılar

Senaryom kırk metreye yirmi metrelik, altı metre yüksekliğinde bir ofis. Duvarda otuz iki elemanlı bir RIS, karşısında sekiz antenli bir baz istasyonu var.
Dört kullanıcı saniyede bir buçuk metre hızla düz çizgiler boyunca yürüyor. Doğrudan yollar engellenmiş, yani kullanıcılara asıl katkı RIS üzerinden geliyor.
Büyük ölçekli kanal parametreleri 3GPP TR otuz sekiz dokuz yüz bir modelinden geliyor. Kullanıcılar hareket ettikçe kanal geometriden her an yeniden hesaplanıyor.

## 4. Temel tasarım ilkesi: iki zaman ölçeği

Sonuçlara geçmeden önce tezin temel tasarım ilkesini söylemek istiyorum: iki zaman ölçeği.
Baz istasyonundaki ön kodlayıcı her slotta, güncel kanaldan tazelenir. RIS fazı ise daha yavaş bir döngüde, gecikmesi ölçülmüş bir algoritmayla güncellenir; bu tezin konusu bu yavaş döngü.
Bunu bir varsayım olarak değil, ölçerek koydum. Ön kodlayıcı da RIS fazıyla birlikte eskirse, sistem yaklaşık bir milisaniyede çöküyor: hız beş virgül kırk birden dört virgül sıfır üçe düşüyor. Yani ön kodlayıcıyı hızlı döngüde tutmak bir tercih değil, zorunluluk. Tezin bütün sonuçları bu ilkenin içinde geçerli.

## 5. Kod 1: kanal zamanla nasıl eskiyor?

Kanalın nasıl eskidiğini bu sınıf modelliyor. Her senaryo için bir tohum ve bir zaman listesi veriyorum; üreteç, kullanıcıların o anlardaki konumlarına göre RIS–kullanıcı ve doğrudan kanalları yeniden hesaplıyor.
Saçıcılar, yol kazançları ve baz istasyonu ile RIS arasındaki kanal sabit tutuluyor. Değişen tek şey kullanıcıların konumu. Böylece kanal, rastgele değil, geometriye bağlı olarak sürekli değişiyor.
Bütün deneylerde aynı tohumları kullandım: seçim için on iki, rapor için on bir. Böylece her karşılaştırma aynı dört yüz senaryo üzerinde ve eşleştirilmiş olarak yapılıyor.

## 6. Kod 2: etkin hız, yöntemin kendi gecikmesinde

Tezin ana ölçütü etkin hız. Faz, sıfır anındaki kanal üzerinde hesaplanıyor; ama hız, yöntemin işini bitirdiği andaki kanal üzerinde ölçülüyor.
Kodda bu iki satır: adam fonksiyonu fazı sıfır anındaki kanalda optimize ediyor; minrate fonksiyonu ise o fazı, gecikme kadar sonraki kanalda değerlendiriyor.
Önemli bir ayrıntı: değerlendirmeyi enterpolasyonla değil, her yöntemin tam gecikme anında yaptım. Kaba bir zaman ızgarasından enterpolasyon yapmanın sonuçları kaydırdığını denetimlerde gördüm ve düzelttim.

## 7. Kod 3: gecikme nasıl ölçüldü?

Gecikmeyi ölçmek bu tezde bir yan iş değil, ana ölçümün kendisi. Bu yüzden katı bir protokol kullandım.
Makine boşalana kadar bekledim, tek iş parçacığıyla çalıştım, ısınma turlarından sonra beş turun medyanını aldım ve ölçüm öncesi ile sonrası yükü kaydettim.
Bu önemli, çünkü bir ölçümde eğitim arka planda çalışırken alınan sayılar yanlış bir sonuç üretmişti. Ölçümü boş makinede tekrarladığımda sonuç tersine döndü. O günden sonra her gecikme bu protokolle ölçüldü.

## 8. Sonuç 1: kâğıt üzerindeki en iyi yöntemler kaybediyor

İlk sonuç. Tabloda soldan ikinci sütun yöntemlerin sıfır anındaki hızı. Bu sütuna bakarsanız en iyi yöntemler koordinat inişi ve uzun koşulu Adam.
Ama onlar sıfır virgül dokuz ve beş virgül dokuz saniye sürüyor. O sürede kullanıcılar metrelerce yürüyor. Etkin hızlarına baktığımızda iki buçuk milisaniyelik basit bir sezgisel yöntemin gerisine düşüyorlar.
Sıralama tersine dönüyor. Ve bu bir bütçe yapaylığı değil: koordinat inişinin tek bir taraması bile yüz yedi milisaniye, yani yaklaşık dört eşevreli kalma süresi.

## 9. Sonuç 2: bir içsel optimum var

İkinci sonuç: daha fazla iterasyon her zaman daha iyi değil. Adam'ın adım sayısı arttıkça sıfır anındaki hız yükseliyor ama gecikme de artıyor.
İkisi dengelendiğinde bir optimum çıkıyor. Saniyede bir buçuk metrede en iyi adım sayısı dört ile altı arası. Kırk sekiz adıma kadar koşmak yüzde on dört kaybettiriyor. Saatte on kilometrede optimum üç adıma iniyor.
Bu optimumu iç optimum diye adlandırdım. Daha sonra jüri sorusu olarak, korelasyon tabanı olmayan bir Clarke kanalında da var olduğunu gösterdim.

## 10. Sonuç 3: optimumu tek bir sayı belirler

Üçüncü sonuç, bir ölçekleme yasası. Optimumun yeri tek bir sayıya bağlı: adım süresi çarpı Doppler frekansı. Buna x dedim.
Küçük gecikme yaklaşımıyla en iyi adım sayısının x üzeri eksi iki bölü gama artı iki gibi ölçeklendiğini türettim; ölçtüğüm üs eksi sıfır virgül altı yüz yetmiş beş.
Bunun pratik anlamı şu: daha hızlı bir donanım optimumu kaydırır ama yok etmez. Adım zaman aldığı sürece bir optimum vardır.

## 11. Sonuç 4: öğrenilen kural adım başına kazanır, milisaniye başına kaybeder

Dördüncü sonuç yapay zekâ ekseniyle ilgili. Adam'ın adımlarını öğrenen bir ağ eğittim.
Eşit adım sayısında bu ağ Adam'ın önünde. Literatürde genellikle bu karşılaştırma raporlanır. Ama her adımı ölçülmüş süresiyle saydığımda, öğrenilen bütün yapılandırmalar Adam eğrisinin altında ve sağında kalıyor. Yani adım başına kazanıyor, milisaniye başına kaybediyor.
Bu tezin önemli olumsuz sonuçlarından biri ve bir değerlendirme protokolü öneriyor: öğrenilen yöntemler ölçülmüş süreyle, her bütçede ayarlanmış klasik rakiplere karşı sınanmalı.

## 12. Tasarım kuralı: optimumu önceden seçmek

Bu yasayı bir tasarım kuralına çevirdim. Kural, her aday adım sayısı için etkin hızı öngörüyor: sıfır anındaki hız, eskime eğrisiyle ağırlıklandırılıyor.
Eğriyi yalnızca bir hızda ve bir çekilişte kalibre ettim. Sonra kuralı, sonuçları görmeden önce kayda aldığım bir protokolle, hiç görmediği bir çekilişte ve hiç görmediği hızlarda sınadım.
Altmış koşulda doğru adım sayısını seçmeye göre medyan kayıp yüzde sıfır virgül sıfır sekiz, en kötü yüzde iki virgül yetmiş dört. Sabit bir adım sayısı seçmek ise ortalama yüzde üç ile üç virgül altı kaybettiriyor.

## 13. Jürinin olası soruları: ön kayıtlı deneylerle

Savunmaya hazırlanırken jürinin sorabileceği en zor soruları kendime sordum ve her birini ön kayıtlı bir deneyle yanıtladım.
Koordinat inişini C ile yazsaydım ne olurdu? Yalnız onu derlersem Python Adam'ı geçiyor; bunu açıkça yazıyorum. Ama bütün yöntemler eşit hızlandırılırsa Adam her noktada önde kalıyor. Yani sıralamayı programlama dili değil, gecikme oranı belirliyor.
İç optimum modelin bir yapaylığı mı? Hayır, korelasyon tabanı olmayan bir kanalda da var.
Ryu ve arkadaşlarından farkım ne? Süreyi yalnızca bir bütçe kısıtı olarak kullanmak bir virgül dörde kadar kaybettiriyor; benim katkım süreyi kanal eskimesine katmak.
Ön kodlayıcı da eskirse? O zaman her şey bir milisaniyede çöküyor. Bu, ön kodlayıcının her slotta tazelenmesinin bir tercih değil zorunluluk olduğunu gösteriyor.

## 14. Geniş bant OFDM: zaman bütçesinin ikinci ekseni

Tezin son deneysel adımı geniş bant. OFDM'de tek bir RIS faz vektörü bütün alt taşıyıcılara hizmet ediyor. Optimizasyona kaç alt taşıyıcı alacağım da bir karar, çünkü her ek alt taşıyıcı adımı pahalılaştırıyor.
Yirmi megahertzde dar bant amacı yetiyor. Yüz megahertzde ise on altı alt taşıyıcı üzerinden optimize etmek, adım dokuz kat pahalı olmasına rağmen en iyi dar bant kolunu sıfır virgül yirmi sekiz geçiyor.
Yani gecikme geniş bantta da kararı belirliyor, ama artık iki eksende: kaç adım ve kaç alt taşıyıcı. Burada dürüst bir sınır da var: dar banttaki iç optimum geniş bantta genelleşmiyor. Bunu makalede açıkça yazdım.

## 15. Tasarlanan sistem: gecikme farkındalıklı denetleyici

Şimdi tezin tasarım katkısına geliyorum. Yukarıdaki yasaları birleştirerek gecikme farkındalıklı bir denetleyici tasarladım.
Denetleyici her güncellemede aday hatları değerlendiriyor: başlangıç noktası olarak SU-average, SU-best-of ya da periyodik çalışmada bir önceki fazı alıyor, üzerine sıfır ile kırk sekiz arası Adam adımı ekliyor.
Her aday için ölçülmüş gecikmeyi ve Doppler kestirimini kullanarak etkin hızı öngörüyor ve en yüksek öngörüyü veren hattı seçiyor. Kod bu kadar kısa; çünkü işi yapan, daha önce ölçülen ve doğrulanan yasalar.

## 16. Mühürlü test: hiç görülmemiş çekilişte, tek sefer

Denetleyiciyi bir gece boyunca geliştirdim, her fikri yalnızca geliştirme çekilişinde sınadım ve başarısız olanlar dahil bütün denemeleri günlüğe yazdım. Sonra son sürümü dondurdum ve gece hiç dokunulmayan bir çekilişte tek bir kez test ettim. Ön kayıtlı üç hipotezin üçü de tuttu.
Kazancı abartmadan, kararlara ayırarak veriyorum. Başlangıç noktasını doğru seçmek yüzde bir virgül on dört kazandırıyor; adım sayısını koşula göre seçmek yüzde sıfır virgül yetmiş dokuz daha. En iyi sabit ayara karşı toplam kazanç yüzde bir virgül yetmiş üç; periyodik çalışmada önceki fazdan başlamak yaklaşık yüzde bir daha ekliyor.
Bu büyük bir kazanç değil. Denetleyicinin asıl değeri, ayarsız çalışması: elle hiçbir ayar yapmadan, hız, taşıyıcı ve tutma süresi değiştikçe olası en iyi seçime sıfır virgül sıfır sıfır üç yakın kalıyor. Sabit bir ayar ise yalnızca kalibre edildiği koşullarda iyi.

## 17. Yapay zekâ ekseni: en elverişli rejimde de olumsuz

Yapay zekâ eksenini de dürüstçe kapattım. Öğrenmenin klasiği yenme şansının en yüksek olduğu rejimi bilerek aradım: yirmi sekiz gigahertz, eşevreli kalma süresi yaklaşık üç milisaniye.
Sıfır virgül kırk üç milisaniyede karar veren tek geçişli ağ, bir virgül yirmi dört milisaniyelik basit sezgiselin gerisinde kaldı. Veriyi dört katına çıkardım, üç farklı tohum ve iki kat geniş bir ağ denedim; açık daraldı ama kapanmadı.
Ağ gerçekten öğreniyor, ama kalite tavanı basit yöntemin altında. Bu sonuç bu mimari ailesi ve bu bütçe için geçerli. Tezde öğrenmenin katkısı bir yöntem olarak değil, bir değerlendirme protokolü olarak kalıyor.

## 18. Dürüst sınırlar

Her tez gibi bu tezin de sınırları var ve bunları açıkça yazdım.
Tek bir geometri ve tek bir kanal modeli kullandım; Clarke kanalı yalnızca bir sağlamlık kontrolü. Gecikmeleri tek iş parçacıklı Python'da ölçtüm; bu yüzden sıralamanın gecikme oranına bağlı olduğunu ayrıca gösterdim.
Kaynak kontrolünde, RIS eleman kazancının Tang ve arkadaşlarının formülünden farklı olduğunu buldum. Etkisini ölçtüm: mutlak hızlar yaklaşık yüzde beş yüksek, ama optimum adım sayısı ve en iyi yöntem değişmiyor. Makalede bunu tek cümleyle belirttim.
Ön kayıt, mühürlü test ve bağımsız denetimler, bu sınırların sonuçları nerede etkilediğini görmemi sağladı.

## 19. Gelecek çalışma: sınırları kapatacak deneyler

Bu sınırların her biri için somut bir deney planım var.
Tek geometri sınırını, farklı bir oda, farklı bir RIS konumu ve altmış dört elemanlı bir yüzeyle, aynı ön kayıtlı hipotezlerle kapatabilirim. Ölçüt açık: tasarım kuralı yeni geometride optimum adım sayısını yüzde birden az kayıpla öngörebiliyor mu?
Simülasyon sınırını ölçülmüş bir kanalla, Python sınırını bütün yöntemleri aynı düzeyde derleyerek ya da bir hızlandırıcı üzerinde koşturarak kapatabilirim. RIS'in anahtarlama süresini gecikmeye eklemek ve ön kodlayıcı döngüsünü pilot ve kestirim hatasıyla birlikte ana sonuca katmak da sıradaki adımlar.

## 20. Sonuç

Özetle: hareketli RIS sistemlerinde hesaplama gecikmesi yöntem sıralamasını belirliyor.
Etkin hız ölçütüyle kâğıt üzerindeki en iyi yöntemlerin kaybettiğini gösterdim. Bir iç optimum ve onun ölçekleme yasasını buldum, bunu ön kayıtlı olarak doğrulanmış bir tasarım kuralına çevirdim. Bu yasaları kullanan bir denetleyici tasarladım; hiç görülmemiş bir çekilişte olası en iyi seçime çok yakın çalışıyor. Geniş bantta zaman bütçesinin ikinci eksenini ortaya koydum. Ve yapay zekâ ekseninde titiz bir olumsuz sonuç ve bir değerlendirme protokolü bıraktım.
Bütün sayılar betiklere, ham verilere ve tohumlara bağlı; her biri bağımsız olarak denetlendi. Dinlediğiniz için teşekkür ederim.
