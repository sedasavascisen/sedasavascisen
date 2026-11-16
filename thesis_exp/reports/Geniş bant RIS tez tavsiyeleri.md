# Gecikme sıralamayı belirler, geniş bant bunu sınar

Literatür, hareketli RIS'te kanal eskimesini, hesaplama süresini ve geniş bant OFDM'yi üç ayrı küme olarak çalışıyor. Bu notların taradığı kaynaklarda bu üçünü birleştiren tek bir çalışma bulunamadı. Hiçbir çalışma her yöntemi, *kendi ölçülmüş duvar saati süresi dolduğunda* var olan eskimiş kanalda değerlendirmiyor. Hiçbiri de alt taşıyıcı sayısını hesaplama süresiyle uyum kalitesi arasında ayarlanabilir bir düğme olarak ele almıyor. Tezin boşluğu bu kesişimdir. Ama iki yenilik iddianız ciddi tehdit altında, bunu açıkça söylüyorum. **Birincisi, Makale 1'in sin/cos gösterimi RIS'te yeni değil.** Fondo-Ferreiro vd. (IEEE Access 2025) aynı kodlamayı aynı gerekçeyle kullanıyor. **İkincisi, en yakın rakip arXiv:2608.25393 (Ağustos 2026).** Bu çalışma hesaplama süresini bir uygulanabilirlik kısıtı olarak modele koyuyor. Makale 2 TWC'ye bu çalışmadan ayrışarak gitmek zorunda. Tezi tutarlı kılacak çerçeve bir ölçüt merdiveni. İlk basamak RMSE, ikincisi t = 0 hızı, üçüncüsü etkin hız. Her basamak bir öncekinin gözden kaçırdığını gösteriyor, ve bunu gösteren sayıların hepsi elinizdeki denetim ve köprü dosyalarında var. Geniş bant deneyi bu merdivenin dördüncü basamağını, yani bant genişliğini, aynı ölçüm protokolüyle ekliyor. Tezin kapanış katkısı olmaya en uygun aday bu. Ancak koşturmadan önce düzeltilmesi gereken iki küçük tasarım kusuru var: alt taşıyıcı alt kümesi bant merkezine göre kayık, ve K_opt = 64 değerlendirme ızgarasının kendisi. Bir de gecikme ölçümünün Python yüküne gömülme riski var. Aşağıda önce bu tehditleri, sonra literatürün haritasını, sonra on tavsiyeyi veriyorum.

## Önce kötü haber: beş bulgu yenilik iddialarını daraltıyor

**Sin/cos gösterimi RIS'te öncüllü.** Fondo-Ferreiro, Saghezchi, Gil-Castiñeira ve Rodriguez, her açıyı θ → (sin θ, cos θ) olarak kodluyor, gerekçe olarak da "açıların dairesel simetrisinin (2π periyodiklik) yarattığı sorunlardan kaçınmak" diyor. Çıkış arctan(y1/y2) ile çözülüyor, etiketler kusursuz CSI'dan hesaplanan kapalı form optimum. N ≥ 16 için optimuma %1'den az açık bildiriyorlar ([DOI 10.1109/ACCESS.2025.3552065](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)). Dairesel regresyon RIS dışında zaten oturmuş bir konu: biternion ağları ve von Mises kayıpları normalize edilmiş (cos, sin) çıktılar üzerinde bir kosinüs kaybına indirgeniyor ([arXiv:1805.03430](https://arxiv.org/abs/1805.03430)). Biternion'ın özgün makalesi (Beyer vd., GCPR 2015) getirilmedi, DOI'si UNVERIFIED. Etiketsiz, hız tabanlı eğitimde süreksizlik sorunu hiç doğmuyor. Gao vd. ham fazı e^{jθ} içinden negatif alınan güce veriyor ve kayıp yapı gereği 2π-periyodik ([arXiv:2001.02348](https://arxiv.org/abs/2001.02348)). Yani sin/cos düzeltmesi yalnızca faz etiketine karşı denetimli regresyonda anlam taşıyor. Makale 1'in sin/cos ile doğrudan açıyı aynı ağda karşılaştıran kontrollü bir ablasyonu varsa, bu notların bulduğu tek RIS örneği o. Ama makalenin yayıncı sayfası 403 döndürdü; "%29.9 RMSE iyileşmesi" yalnızca arama özetinden geliyor ve **UNVERIFIED**. Tezde bu sayıyı kendi `aisy_paket/` dosyanızdan doğrulamadan kullanmayın.

**Hesaplama süresini modele koyan en yakın rakip yeni ve TWC düzeyinde.** Ryu, Choi, Yang ve Cioffi'nin tam metni okundu. Çalışma "T_sense(ℓ) + T_opt < T_CSI" kısıtını koyuyor ve veri fazını algılama ile optimizasyon süresi kadar kısaltıyor. Ağırlıklı toplam hızın "algılama–optimizasyon döngüsü 5 ms içinde tamamlandığı sürece" kararlı kaldığını söylüyor. Yöntemleri %99 yakınsamaya kadar gereken FLOP ile karşılaştırıyor (M = 32, K = 16'da SCRPA 3.867, AO-SPR 0.514, RMO-LS 54.997, WMMSE-GRAD 0.093 GFLOP) ([arXiv:2608.25393](https://arxiv.org/abs/2608.25393)). Makale 2'nin ayrışma noktaları üç ve hepsi tam metinden doğrulandı. Ryu vd. **duvar saati süresi vermiyor**. T_opt'u **eskime gecikmesine eklemiyor**; geri besleme gecikmesi Δ ayrı tanımlı. Ve süre bir **evet/hayır uygulanabilirlik kısıtı**, her yöntemin kendi bitiş anındaki hızı değil. Metindeki "55 ms bütçe" ifadesi 5 ms ile çelişiyor, muhtemelen bir yazım hatası. Bu ayrımı Makale 2'nin giriş ve ilgili çalışmalar bölümüne açıkça yazmazsanız, hakem bu makaleyi size karşı kullanır.

**"Süre hesaba katılınca optimum iterasyon azalır" fikrinin RIS dışında bir öncülü var.** Guo, Makki ve Svensson genetik algoritmalı bir hüzme oluşturucuda algoritmanın çalışma süresini dilim verimine dahil ediyor ([arXiv:1703.03792](https://arxiv.org/abs/1703.03792)). Bir arama özetine göre en iyi verimi erken durdurulan, alt-optimal bir hüzme oluşturucu veriyor ve süre maliyeti sayılınca gereken iterasyon sayısı düşüyor. Bu ayrıntılar özet sayfasında görülmedi, yalnızca PDF parçasında geçiyor, dolayısıyla **UNVERIFIED in detail**. Bağlam milimetre dalgada ilk erişim; RIS de eskime de yok. İçsel optimum L* fikrini "ilk" diye sunmayın. Bunu "eskiyen kanalda, ölçülmüş duvar saatiyle ve yöntem sıralamasını değiştiren bir büyüklük olarak ilk kez" diye daraltın.

**Öğrenilen güncelleme kuralının mimarisi yeni değil, ama olumsuz sonucunuz ayırt edici.** Lavi ve Shlezinger, sabit sayıda iterasyonlu izdüşümlü gradyan için iterasyona bağlı hiperparametreler öğreniyor ve "on kattan fazla daha az iterasyon" bildiriyor; kazanç iterasyon ekseninde ([arXiv:2301.00369](https://arxiv.org/abs/2301.00369)). Klasik kolu iterasyon bütçesine göre ayarlayıp ayarlamadıkları doğrulanmadı. Makine öğrenmesi literatürü uyarıyı zaten yapmış: Metz vd. öğrenilen optimize edicilerin "elle tasarlanmış optimize edicilere göre henüz duvar saati hızlanması göstermediğini" yazıyor ([arXiv:1810.10180](https://arxiv.org/abs/1810.10180)). "Adım başına kazanır, milisaniye başına kaybeder" bulgunuz genel optimizasyon literatüründe şaşırtıcı değil. Kablosuz literatürde ise notların taradığı hiçbir makalede açıkça raporlanmamış. Sonucu "bilinen bir tehlikenin RIS'te ilk ölçülmüş örneği" olarak sunun, "beklenmedik keşif" olarak değil.

**L* için kapalı form iddiasında kontrol edilmemiş bir öncül alanı var.** Eskime altında optimum iterasyon sayısı için kapalı form bulunamadı. Bulunanlar pilot aralığı ve çerçeve boyu için kapalı formlar. Örneğin Daei, Fodor ve Skoglund'un çerçeve boyu formülü ([arXiv:2405.07882](https://arxiv.org/abs/2405.07882), [DOI 10.1109/TWC.2025.3637076](https://doi.org/10.1109/TWC.2025.3637076)) arama özetlerine göre esas olarak kullanıcı hızına bağlı; tam metinde doğrulanmadı. Klasik uyarlamalı filtre literatürünün (LMS/RLS izleme; Gauss-Markov hedefte gecikme hatası ile gradyan gürültüsü arasındaki ödünleşim) kapalı form "izleme ve yakınsama" sonuçları içerdiği bilinir. Haykin'in *Adaptive Filter Theory* kitabı bunun standart kaynağı, ama bu oturumda bellekten anıldı: **UNVERIFIED**. Savunmadan önce bu literatüre bakılmazsa, sinyal işlemeci bir jüri üyesi "bu, adım boyu–izleme ödünleşiminin iterasyon sayısı versiyonu değil mi?" diye sorar.

## Literatür dört kümede duruyor ve kümeler birbirine değmiyor

**Eskime kümesi** neredeyse tek tip bir model kullanıyor: bağlantı başına birinci dereceden Gauss-Markov, korelasyonu ρ = J0(2π f_D τ). BS–RIS bağlantısı yarı-statik kabul ediliyor ([arXiv:2209.04171](https://arxiv.org/abs/2209.04171); [arXiv:2405.09200](https://arxiv.org/abs/2405.09200)). Bu kümedeki τ her zaman pilot–veri ya da geri besleme gecikmesi. Deb ve Ghosh kestirim aralığını kullanıcı başına bir tasarım değişkeni yapıyor, ama eskimeye yalnızca kanal kestirim süresi giriyor ([arXiv:2408.17128](https://arxiv.org/abs/2408.17128)). Haider Shah vd. "kanal bilgisi yaşını" gizlilik kapasitesine bağlıyor ve hafif eskimiş CSI'nın yeterli olduğu, yani RIS'in daha seyrek yapılandırılabileceği sonucuna varıyor ([DOI 10.1109/VTC2024-Spring62846.2024.10683291](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683291)). Zappone vd. kestirim ve geri besleme süresini dilimden düşüyor; özetlere göre optimize edicinin süresi modelde yok, tam metin okunmadı ([arXiv:2003.02538](https://arxiv.org/abs/2003.02538)). Tezin modeli bu kümede azınlıkta: sabit saçıcılar ve düz yörüngeyle geometrik bir model. Geometrik ya da yörünge tabanlı modeller daha çok yüksek hızlı tren ve kırıcı yüzey çalışmalarında görülüyor ([arXiv:2106.02274](https://arxiv.org/abs/2106.02274)). Bu hem güç hem zayıflık. Açı kayması deterministik olduğu için öngörü iyimser çıkıyor; denetim raporunuz da bunu zaten yazıyor (`thesis_exp/AYRINTILI_RAPOR.md` §9).

**Hesaplama kümesi** sorunu adlandırıyor ama ölçmüyor. Xia vd. iteratif optimizasyonun "yüksek hesaplama gecikmesi" yüzünden gerçek zamana uygun olmadığını söylüyor, ama özette süre sayısı yok ([arXiv:1901.00354](https://arxiv.org/abs/1901.00354)). Dai grubunun JSAC makalesi temel bant işleme gecikmesini eskimeyi kötüleştiren bir etken olarak açıkça anıyor; RIS'e özgü değil ([PDF](https://oa.ee.tsinghua.edu.cn/dailinglong/publications/paper/Accurate_Channel_Prediction_Based_on_Transformer_Making_Mobility_Negligible.pdf)). Mathias vd. RIS'te "hüzme fiilen güncellendiğinde kanalın değişmiş olabileceğini" yazıyor ve kinematik öngörüyle telafi ediyor. Gecikme orada veri olarak alınıyor, algoritmanın karmaşıklığına bağlanmıyor ([arXiv:2508.16980](https://arxiv.org/abs/2508.16980)). Derin açılım makaleleri tipik olarak 10–25 kat hızlanma bildiriyor. DUNet alternatif optimizasyona göre "yaklaşık 25.6 kat daha hızlı" ([arXiv:2401.00192](https://arxiv.org/abs/2401.00192)). Ama taban çizgisi neredeyse her zaman yakınsamaya kadar koşturulan ya da eşit iterasyonlu klasik algoritma; Pellaco vd. örneğin eşit iterasyonda karşılaştırıyor ([arXiv:2006.08448](https://arxiv.org/abs/2006.08448)). **Notların bulduğu hiçbir makale, klasik kolun adım boyunu ve objektifini her duvar saati bütçesinde yeniden ayarlamıyor.** Tezin protokolü yayımlanmış normdan sıkı. Notların çıkarımına göre bu protokol altında bildirilen hızlanmalar küçülürdü; bu ölçülmüş bir şey değil, çıkarım.

**Geniş bant kümesi**, 2019'dan beri tüm alt taşıyıcılara ortak tek bir yansıma vektörü kullanıyor. Chen vd. bunu açıkça kısıt olarak koyuyor: pasif RIS'in faz kaymaları "tüm frekanslar için aynı olmalı" ([arXiv:2103.11105](https://arxiv.org/abs/2103.11105)). Tezin kurgusuna en yakın çapa Li vd.: MU-MISO-OFDM, tek faz vektörü, ortalama toplam hız, WMMSE/BCD ([arXiv:2007.14243](https://arxiv.org/abs/2007.14243)). Kaplan'ın 78 çalışmalık derlemesi de çoğu çalışmanın RIS'i frekansa göre düz kabul ettiğini söylüyor. Aynı derlemede alt küme, alt bant gruplama ya da frekans sıkıştırma yöntemi listelenmiyor ([arXiv:2606.31334](https://arxiv.org/abs/2606.31334)). Yakın analoglar şunlar. Zheng ve Zhang en güçlü zaman tapıyla sıkıştırıyor ([arXiv:1909.03272](https://arxiv.org/abs/1909.03272)). Chen vd. alt taşıyıcılar üzerinden ortalama kovaryans kullanıyor. An, Wu ve Yuen eğitim yükünü uyum süresine göre ayarlıyor ([arXiv:2110.12799](https://arxiv.org/abs/2110.12799)). Yang vd. eleman gruplamasında bir optimum grup boyu buluyor ([arXiv:1906.09956](https://arxiv.org/abs/1906.09956)). **K_opt'u hesaplama/uyum düğmesi olarak tarayan bir çalışma bulunamadı.** Bu, yaklaşık 16 sorguya dayanan bir yokluk kanıtı, ispat değil. Hüzme sapması (beam squint) ağırlıkla mmWave/THz ve büyük açıklıklarda çalışılıyor ([arXiv:2208.12385](https://arxiv.org/abs/2208.12385); [arXiv:2110.15768](https://arxiv.org/abs/2110.15768)). Gecikmesi ayarlanabilir metayüzey ve TTD tasarımları değişken kümesini değiştiriyor (N faz artı N gecikme), bu yüzden doğrudan taban çizgisi değiller ([arXiv:2110.09291](https://arxiv.org/abs/2110.09291); [arXiv:2401.11141](https://arxiv.org/abs/2401.11141)).

**Öğrenme kümesi** latansı "ağın süresi uyum süresinin çok altında" diye savunuyor, ama hızı tahminin yapıldığı kanalda hesaplıyor. Gao vd. aynı CPU'da 0.0399 ms'ye karşı SDR için 199.2 ms ölçüyor ve 13.77 ms'lik uyum süresiyle kıyaslıyor; ama ağın hızını eskimiş kanalda değerlendirmiyor ([arXiv:2001.02348](https://arxiv.org/abs/2001.02348)). Taha vd. geniş bantta tek ψ'yi kod kitabı üzerinde hız regresyonuyla seçiyor ve çıkarım süresi vermiyor ([arXiv:1904.10136](https://arxiv.org/abs/1904.10136)). **Tek geçişli bir RIS faz tahmincisini gecikme sonrası kanaldaki etkin hızla değerlendiren bir çalışma bulunamadı.**

**Standartlar** tezin çerçevesine destek veriyor ama sayı vermiyor. ETSI GR RIS 003, RIS katsayılarını ayarlama gecikmesinin sistem düzeyi benzetimlerde "uygun tek bir parametreyle" modellenmesini istiyor ve bir RIS eleman durumunun "belirli bir bant genişliğindeki tüm alt taşıyıcılara uygulanabilir" olduğunu varsayıyor ([GR RIS 003 V1.1.1](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)). GR RIS 004 örnek olarak FR1 ve 15 kHz SCS için toplam sistem gecikmesinin 1 ms'nin altında olması gerektiğini yazıyor. Aynı rapora göre PIN, varaktör ve FET anahtarlama "nanosaniye", sıvı kristal ve MEMS "milisaniye" bölgesinde ([GR RIS 004 V1.1.1](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)). O-RAN'da yakın-gerçek-zamanlı RIC 10 ms–1 s ölçeğinde çalışıyor; DU/CU'da koşan dApp'ler ise 450 µs altı döngü bildiriyor ([arXiv:2501.16502](https://arxiv.org/abs/2501.16502)). RIS'in 3GPP Rel-18 ve Rel-19'da çalışma maddesi olmadı ([arXiv:2404.04753](https://arxiv.org/abs/2404.04753)).

## On tavsiye: ölçüt merdiveninden geniş bant kapanışına

İlk üç tavsiye iki makaleyi aşırı iddiaya kaçmadan tek hikâyeye bağlıyor. Dördüncü ile yedinci arası Makale 2'nin çekirdeğini rakiplere karşı sağlamlaştırıyor. Son üçü geniş bant deneyini tezin kapanışı yapıyor. Yeni deney gerektirenler bunu açıkça söylüyor. Ölçüm fazı 20 Kasım'da kapanıyor, yani dört gününüz var.

### Tavsiye 1 — Tezi "ölçüt merdiveni" üzerine kurun: RMSE → t = 0 hızı → etkin hız

**Ne:** Giriş ve sonuç bölümleri tek bir yöntembilim iddiası etrafında örülsün: her ölçüt, bir öncekinin görmediği bir maliyeti görünür kılar ve bu, yöntem sıralamasını değiştirir. Basamak 1 RMSE'nin hızla hizalı olmadığını, basamak 2 t = 0 hızının gecikmeyi görmediğini, basamak 3 etkin hızın bu ikisini düzelttiğini göstersin. Basamak 4 bant genişliğini eklesin.

**Neden:** Her basamağın kanıtı elinizde ve hiçbiri yeni deney gerektirmiyor. Basamak 1: yayımlanmış kodla klasik CD'nin RMSE'si 104.02°, ama ortak faz çıkarılınca 1.10°. Yani gerçek optimuma giden yöntem etiket RMSE'siyle cezalandırılıyor. 38.901 arayüzünde ölçek-normalize sin/cos kolu 58.4–59.8° RMSE'ye rağmen 9.302 b/s/Hz veriyor; optimum 10.349 (`thesis_exp/AYRINTILI_RAPOR.md` §1.1 madde 4, §3 madde 4). Basamak 2→3: köprü ağının t = 0 hızı SU-average ile fiilen aynı (4.626'ya 4.624), ama etkin hızda en iyi klasik kola göre −1.418 [−1.503, −1.336] b/s/Hz geride (`thesis_exp/bridge/REPORT.md`). Yakınsamaya kadar koşan Adam-48 ise L*'a göre %14.4 kaybediyor (`thesis_exp/infra/REPORT.md`).

**Literatüre dayanak:** Notlar, öğrenme literatürünün ya RMSE'yi ya da aynı kanaldaki hızı raporladığını, RMSE–hız ilişkisini hiç raporlamadığını tespit ediyor ([arXiv:2001.02348](https://arxiv.org/abs/2001.02348); [DOI 10.1109/ACCESS.2025.3552065](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)). Notların çıkarımına göre, doğrudan bağlantı yokken ortak faz dönmesi hızı değiştirmiyor, dolayısıyla optimum etiket tek değil. Bu bir çıkarım; hiçbir makale açıkça söylemiyor. Sizin CD 104° → 1.10° ölçümünüz bu çıkarımın ampirik gösterimi.

**Tezdeki yeri:** Bölüm 1 (savunu cümlesi), Bölüm 3 (Makale 1) ile Bölüm 4 (etkin hız) arasındaki geçiş, Bölüm 8 (sonuç).

**Maliyet ve risk:** Yalnızca yazım. Risk aşırı iddia. Basamaklar farklı sistemlerde gösterildi: basamak 1 statik tek kullanıcılı Makale 1 kurgusunda, basamak 2–3 çok kullanıcılı hareketli kurguda. Aynı ağın üç ölçütte üç farklı sırada çıktığını gösteren tek bir deney yok. Bu cümleyi tezde açıkça yazın; `TEZ_TAVSIYELERI.md` §1'deki uyarı da aynı noktayı yapıyor.

### Tavsiye 2 — Makale 1'in katkısını "kodlama fikri" değil "ablasyon ve sınırlar" olarak yeniden konumlayın

**Ne:** Tezin Makale 1 bölümünde Fondo-Ferreiro vd.'yi, biternion/von Mises literatürünü ve hız tabanlı etiketsiz eğitimi (Gao vd.) açıkça anın. Katkıyı üç şey olarak koyun: CNN–LSTM mimarisi, sin/cos ile doğrudan açının kontrollü karşılaştırması, ve süreksizliğin yalnızca denetimli regresyonda var olduğu tespiti. Etiket (b)'yi, tohum yayılımıyla bağımsız yeniden üretimi (3.18/2.77/3.90°) ve N = 256'da ölçülen 2.25°'yi (tek tohum) kullanın.

**Neden:** Bir jüri üyesinin Fondo-Ferreiro'yu sizden önce anması, sizin anmanızdan çok daha pahalıya gelir. Elinizde güçlü bir ablasyon kanıtı da var. 38.901 arayüzünde sin/cos ile doğrudan açı arasındaki fark üç tohumda +1.63…+1.86 b/s/Hz ve GA'lar sıfırın üstünde (`thesis_exp/AYRINTILI_RAPOR.md` §3 madde 4). Notlara göre bu, sistem ölçütünde raporlanmış ilk kontrollü sin/cos ablasyonu olabilir. Fondo-Ferreiro'nun kazancı kodlamadan değil, kusurlu CSI'nın gürültüsünün temizlenmesinden geliyor; kodlamanın etkisini ayrıca yalıtmıyorlar.

**Literatüre dayanak:** [DOI 10.1109/ACCESS.2025.3552065](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf); [arXiv:1805.03430](https://arxiv.org/abs/1805.03430); [arXiv:2001.02348](https://arxiv.org/abs/2001.02348); birim modül normalizasyon katmanı için [arXiv:2009.14404](https://arxiv.org/abs/2009.14404) ve [arXiv:2002.10072](https://arxiv.org/abs/2002.10072).

**Tezdeki yeri:** Bölüm 3, "Yeniden üretilebilirlik ve sınırlar" alt bölümüyle birlikte (`TEZ_TAVSIYELERI.md` §2).

**Maliyet ve risk:** Yazım ve bir kaynak kontrolü: Makale 1 Fondo-Ferreiro'yu anıyor mu? Anmıyorsa tezde bunu sessizce geçmeyin. 38.901 ablasyonu ölçek-normalize kolda ve plan dışı bir geçişle yapıldı (H8); bu sapma metinde görünür olmalı. Makale için verdiğiniz "düzeltme gerekmiyor" kararını değiştirmiyor; tez ayrı bir belge.

### Tavsiye 3 — Köprüyü "Makale 1'in yaklaşımı" diye, dar ve kesin adlandırın

**Ne:** Köprü deneyini tezde tam olarak ne ise öyle anlatın. Değerlendirilen ağ MuMisoNet: çok kullanıcılı, etiketsiz eğitilmiş, Makale 1 ile yalnızca sin/cos gövdesini paylaşan tek geçişli bir ağ. RMSE ile değerlendirilmedi. Hüküm cümlesi şu olsun: "tek geçişli faz-farkında yaklaşım, çok kullanıcılı hareketli senaryoda etkin hız ölçütünde her hızda baskınlanıyor."

**Neden:** "Makale 1'in ağı başarısız oldu" demek hem yanlış, hem de jüriye Makale 1'i savunmanız için gereksiz bir cephe açıyor. Kesin çerçeve, olumsuz sonucu tezin en sağlam parçası yapar. 3–30 km/h'nin hepsinde dört öğrenilen kolun dördü de baskınlanıyor; periyodik çalışmada ağ soğuk ve sıcak başlangıçlı Adam'ın gerisinde (`thesis_exp/AYRINTILI_RAPOR.md` §4, §5.10).

**Literatüre dayanak:** Gao vd. ve Ma vd. tek geçişli ağın hızını "tek ileri geçiş" ile açıklıyor ve uyum süresine karşı savunuyor, ama eskimiş kanalda ölçmüyor ([arXiv:2001.02348](https://arxiv.org/abs/2001.02348); [arXiv:2506.22448](https://arxiv.org/abs/2506.22448)). Köprü, bu standart argümanın etkin hız altında çöktüğünü gösteriyor.

**Tezdeki yeri:** Bölüm 6 (öğrenmenin sınırları), Bölüm 3'ün son paragrafı.

**Maliyet ve risk:** Yazım. Ağı RMSE ile değerlendirmek için yeni deney önermiyorum. Çok kullanıcılı ve ZF'li kurguda tek bir optimum etiket yok, bu yüzden RMSE iyi tanımlı değil; bu deney yeni bir tartışma açar ve 20 Kasım'a sığmaz.

### Tavsiye 4 — Makale 2'nin yenilik cümlesini Ryu vd.'ye karşı üç ayrımla yeniden yazın

**Ne:** TWC gönderiminden önce ilgili çalışmalar bölümüne bir paragraf ve bir karşılaştırma tablosu ekleyin. Sütunlar: süre ölçüsü (FLOP / duvar saati), sürenin rolü (kısıt / eskime gecikmesine eklenen terim), değerlendirme anı (sabit / her yöntemin kendi bitiş anı), klasik kolun ayarı (sabit / bütçe başına taranmış). Satırlar: Ryu vd., Zappone vd., Guo–Makki–Svensson, Mathias vd., Makale 2. "İlk" yerine "bilgimiz dahilinde" kalıbını kullanın.

**Neden:** Bu notlarda en yakın ve en yeni rakip Ryu vd. ve TWC hakemi onu bulacak. Ayrımlar gerçek ve tam metinden doğrulandı (yukarıdaki bölüm). Çekici ama ölçülmemiş bir hipotezi tezde soru olarak bırakın, sonuç olarak değil. Notların hipotezine göre, Ryu vd.'nin yakınsamış hızdaki SCRPA > AO-SPR sıralaması, SCRPA'nın M = 32'deki yaklaşık 7.5 kat fazla FLOP'u ek eskimeye çevrilince tersine dönebilir. Bu sizin çerçevenizin doğrudan bir uygulaması.

**Literatüre dayanak:** [arXiv:2608.25393](https://arxiv.org/abs/2608.25393); [arXiv:2003.02538](https://arxiv.org/abs/2003.02538); [arXiv:1703.03792](https://arxiv.org/abs/1703.03792) (iterasyon iddiası UNVERIFIED); [arXiv:2508.16980](https://arxiv.org/abs/2508.16980); kanal bilgisi yaşı için [arXiv:1707.09093](https://arxiv.org/abs/1707.09093) (yayın yeri UNVERIFIED) ve [arXiv:2408.17128](https://arxiv.org/abs/2408.17128).

**Tezdeki yeri:** Makale 2'nin giriş ve ilgili çalışmalar bölümü; tez Bölüm 2 ve 4.

**Maliyet ve risk:** Bir gün yazım ve hedefli arama. Notların önerdiği sorgular: "computation delay" + "channel aging" + "reconfigurable intelligent surface"; "latency-aware" + "WMMSE"; "anytime algorithm beamforming"; Google Scholar ve IEEE Xplore tam metinde. Risk: bu aramada daha yakın bir çalışma çıkabilir. O zaman yenilik cümlesi daha da daralır, ama bunu hakemden önce öğrenmiş olursunuz.

### Tavsiye 5 — L*'ı ve tasarım kuralını "tutma süresine bağlı iç optimum" olarak, sınırıyla birlikte sunun

**Ne:** Makale 2'nin "birkaç adım yeter" hükmünü tezde koşullu hâle getirin: anlık etkin hızda (Tanım 1) iç optimum var; faz uzun tutuldukça optimum yakınsamaya kayıyor. Bunu, ön kayıtlı tasarım kuralının sınamasıyla (H1–H3) birlikte, pratik bir kural olarak verin.

**Neden:** Sınama tamamlandı ve ön kayıttaki üç hipotez de tuttu. Kuralın 60 koşuldaki medyan kaybı %0.08, en kötüsü %2.74. Koşullar üzerinden ortalama kayıp farkı L = 48'e göre +3.34 puan [+2.89, +3.81], makalenin kapalı formuna göre W > 0'da +1.97 puan [+1.45, +2.49] (`thesis_exp/tasarim_kurali/REPORT.md` §1). Aynı tablo bir sınırı da gösteriyor. **W = 0'daki 15 koşulun hiçbirinde L* ızgaranın ucunda değil. W > 0'daki 45 koşulun 21'inde L* = 48, yani taranan ızgaranın ucu** (aynı rapor §2). Uzun tutmada "iç optimum" iddiası çoğu zaman geçerli değil. Makalenin kapalı formu W'yi yok saydığı için en kötü koşulda %8.25 kaybediyor. Bu kuralın tutma süresini içermesi gerektiğinin ölçülmüş gerekçesi.

**Literatüre dayanak:** Kapalı form optimum iterasyon sayısı bulunamadı. En yakınlar çerçeve boyu ve CSI güncelleme aralığı ([arXiv:2405.07882](https://arxiv.org/abs/2405.07882); [arXiv:1707.09093](https://arxiv.org/abs/1707.09093)). Uyarlamalı filtre izleme literatürü (Haykin, UNVERIFIED) kontrol edilmeli.

**Tezdeki yeri:** Bölüm 4 (L*, x = ΔT·f_d), Bölüm 5 (pencere duyarlılığı).

**Maliyet ve risk:** Yeni deney yok. `REPORT.md` ve `raw/validation.json` şu an commit'lenmemiş görünüyor (`git status` izlenmeyen dosya gösteriyor); Kural 3 için önce commit. Risk: x ölçekleme yasası bu denetimde yeniden sınanmadı (`TEZ_TAVSIYELERI.md` §3). Kural ψ'yi yalnızca 1.5 m/s'de kalibre ediyor ve ψ'nin L'ler arası yayılımı 0.11. Tezde bunu kuralın bilinen yaklaşıklığı olarak yazın.

### Tavsiye 6 — Öğrenme eksenini "değerlendirme protokolü" katkısına dönüştürün

**Ne:** Öğrenilen güncelleme kuralının olumsuz sonucunu, literatüre önerilen bir protokolle birlikte sunun. Protokolün öğeleri: eşit duvar saati; klasik kolun her bütçede adım boyu ve objektif üzerinden taranması; doğrulamada seçim, testte rapor; boş makine, tek iş parçacığı, medyan ve tur-arası yayılım; ve oran değerinin süre tanımından bağımsız olduğunun gösterilmesi.

**Neden:** L = 8'de öğrenilen adım, Adam adımının 2.67–2.81 katı süre tutuyor ve bu oran üç farklı süre tanımında da korunuyor (`thesis_exp/AYRINTILI_RAPOR.md` §5.6). Sonuç sağlam, ama tek başına "bizim kurgumuzda kaybetti" diye okunabilir. Protokol olarak sunulursa başka çalışmalara uygulanabilir bir katkıya dönüşüyor. Bildirilen hızlanmalar donanım, iş parçacığı ve yük bilgisi olmadan veriliyor. Sizin projeniz yük kirliliğinin hükmü çevirdiğini zaten yaşadı (CLAUDE.md: Adam 17.5 → 29.7 ms).

**Literatüre dayanak:** Eşit iterasyon [arXiv:2006.08448](https://arxiv.org/abs/2006.08448); iterasyon ekseninde kazanç [arXiv:2301.00369](https://arxiv.org/abs/2301.00369); yakınsamış tabana karşı hızlanma [arXiv:2401.00192](https://arxiv.org/abs/2401.00192); genel uyarı [arXiv:1810.10180](https://arxiv.org/abs/1810.10180). UWMMSE (yaklaşık 24 kat) ve DeepFP sayıları yalnızca arama özetlerinden geliyor, UNVERIFIED; tezde sayı olarak alıntılamayın ([arXiv:2304.00446](https://arxiv.org/abs/2304.00446); [arXiv:2601.02822](https://arxiv.org/abs/2601.02822)).

**Tezdeki yeri:** Bölüm 6; Makale 2'nin tartışma bölümü.

**Maliyet ve risk:** Yazım. GPU ölçümü yok (ÜRETİLEMEDİ) ve torch.compile satırı optimize sürüm sayılamaz. Jüri "GPU'da tersine döner mi?" diye sorarsa dürüst yanıt "ölçülmedi". Bunu bir sınır olarak yazın, ölçümsüz bir tahminle kapatmayın.

### Tavsiye 7 — Gecikmeyi standartların zaman ölçeklerine yerleştirin; donanım anahtarlamasını ayırın

**Ne:** Bölüm 2'ye bir "gecikme bütçesi" tablosu ekleyin. İçeriği: bir yuva (15 kHz'de 1 ms), GR RIS 004'ün 1 ms altı örneği, dApp (450 µs altı), yakın-gerçek-zamanlı RIC (10 ms–1 s), PIN/varaktör anahtarlama (ns), sıvı kristal (ms) ve sizin ölçtüğünüz optimize edici süreleri. Köprünün kendi ölçümünde başlangıç dahil Adam-6 8.700 ms (`thesis_exp/AYRINTILI_RAPOR.md` §9). CD 702.97 ms, PGA 4950.35 ms. Ardından W bulgusunu (25 / 50 / 100 ms → Adam-5 / 6–8 / 16–20) bu tabloya bağlayın: W, fiilen kontrol döngüsünün yeniden hesaplama aralığıdır.

**Neden:** "Gecikme birinci sınıf tasarım kısıtıdır" cümlesi, standardın bu gecikmeyi "uygun tek bir parametreyle" modellemeyi istediği gösterilince havada kalmaz. Ölçtüğünüz milisaniye ölçeğindeki optimize edici süreleri PIN anahtarlamasından kat kat büyük. Notların çıkarımına göre hareketlilikte eskime bütçesinin baskın ve kontrol edilebilir terimi bu. İstisna sıvı kristal RIS: orada anahtarlama da milisaniyeler sürüyor ([arXiv:2402.05469](https://arxiv.org/abs/2402.05469)).

**Literatüre dayanak:** [GR RIS 003](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf); [GR RIS 004](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf); [arXiv:2501.16502](https://arxiv.org/abs/2501.16502). İki zaman ölçekli tasarımlar yapısal bir alternatif olarak anılmalı: RIS istatistikle, ön kodlayıcı her blokta ([arXiv:1912.01818](https://arxiv.org/abs/1912.01818); hızla eskiyen anlık CSI ile [arXiv:2206.07276](https://arxiv.org/abs/2206.07276)).

**Tezdeki yeri:** Bölüm 2 ve Bölüm 5; Bölüm 8'in gelecek çalışma kısmı (iki zaman ölçekli taban çizgisi, öngörücü faz tasarımı [arXiv:2508.16980](https://arxiv.org/abs/2508.16980)).

**Maliyet ve risk:** Yazım. İki zaman ölçekli taban çizgisini 20 Kasım'dan önce koşturmayın; jüri sorarsa "gelecek çalışma" meşru bir yanıt. Ölçülen süreler tek bir Xeon'da ve Python'da; mutlak ms'yi standart bütçesiyle doğrudan kıyaslarken bunu belirtin. Asıl taşıyıcı x ekseni.

### Tavsiye 8 — Geniş bant kurgusunun fiziksel rejimini koşudan önce bir betikle sabitleyin

**Ne:** `thesis_exp/genis_bant/` altına küçük, analitik bir betik ekleyin. Betik iki şeyi tek tabloya yazsın: tezin kanal modelinin gecikme yayılımı ve uyum bant genişliği (mevcut `results/wideband_feasibility.json`'dan, tanımı açıkça seçilerek), ve 38.901 InH-Office tablosundan formülle hesaplanan karşılıkları. B = 20/50/100 MHz'i de uyum bant genişliğinin katları olarak versin.

**Neden:** Fizibilite betiği (`scripts/wideband_feasibility.py`) tezin modelinde birkaç şey ölçüyor. Kaskad bağlantıların τ_rms medyanı yaklaşık 21 ns; %50 uyum bant genişliği kullanıcıya göre 9–23 MHz (`thesis_exp/genis_bant/PLAN.md`). Ama aynı JSON birden çok tanım taşıyor: kaskad bağlantılar, θ_c'deki etkin kanal ve 1/(5τ) kuralı. Etkin kanaldaki Bc50 tek kullanıcıda 75 MHz'e çıkıyor. Tezde hangisini kullandığınızı tek bir tanımla sabitlemezseniz, "100 MHz kaç uyum bandı eder?" sorusunun yanıtı tanıma göre birkaç kat değişir. Hüzme sapması bu geometride ihmal edilebilir. Aynı betiğin uç-yayın en kötü durum hesabı 3 GHz, D = 0.4 m, 100 MHz'de bant kenarında 0.06–0.26 dB kazanç kaybı veriyor. Yani geniş bant etkisi çok yollu frekans seçiciliği, hüzme sapması değil. Bu, notların alt-6 GHz için yaptığı çıkarımla örtüşüyor. **Literatür tarafındaki sayılar ise ölçüm değil, araştırmacının kendi aritmetiği.** 38.901 tablosundan InH LOS için yaklaşık 20 ns medyan, NLOS için yaklaşık 39 ns, ve bunlardan Bc,0.5 ≈ 5–10 MHz hesaplanmış. Ders kitabı kuralı Bc ≈ 1/(5·DS) da yeniden doğrulanmadı. Bunlar betikle yeniden üretilmesi gereken tahminler.

**Literatüre dayanak:** [TR 38.901 V16.1.0, Tablo 7.5-6 ve 7.7.3-2](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/16.01.00_60/tr_138901v160100p.pdf); GR RIS 003'ün iç mekân RIS–UE sıçraması için CDL-E, 30 ns ([GR RIS 003](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)); büyük bant ölçütü B > c/D (38.901 §7.6.2); hüzme sapmasının büyük açıklık ve THz'e özgü olduğu [arXiv:2103.11105](https://arxiv.org/abs/2103.11105).

**Tezdeki yeri:** Bölüm 7 (gerçekçi senaryo) ve geniş bant bölümünün "kurgu" alt bölümü.

**Maliyet ve risk:** Yeni kanal çekilişi gerektirmeyen birkaç saatlik bir betik; boş makine gerekmez. Risk: tezin iç mekân modelinin InH'den belirgin biçimde dar ya da geniş çıkması. Çıkarsa bu bir sınır olarak yazılır, model değiştirilmez (CLAUDE.md "Değiştirme" tablosu). TS 38.211 numeroloji değerleri bu oturumda yeniden getirilmedi (UNVERIFIED); alıntılamadan önce sürüm ve madde numarasını sabitleyin.

### Tavsiye 9 — Geniş bant deneyini koşmadan önce üç tasarım ayrıntısını düzeltin ya da kayda geçirin

**Ne:** Ön kayıt commit'lendi (`2da84ad`), ama eğriler henüz koşmadı. Aşağıdakileri tarihli bir "sapma" notuyla `ON_KAYIT.md`'ye ekleyin, sonra koşun.

(i) **Alt küme kayık.** `wb.py` K_opt ∈ {4, 16} için değerlendirme ızgarasının her (64/K_opt)'ıncı alt taşıyıcısını 0. indisten başlayarak alıyor. K_opt = 4'te bu 0, 16, 32, 48 indisleri demek; bu noktaların ağırlık merkezi kod okumasına göre bant merkezinden yaklaşık 0.12·B aşağıda. Merkezlenmiş bir alt küme (8, 24, 40, 56 gibi) K_opt'un etkisini kaymadan ayırır.

(ii) **K_opt = 64 örneklem-içi.** K_opt = 64, değerlendirme ızgarasının kendisi. Bu kolun avantajı kısmen değerlendirme noktalarını doğrudan optimize etmesinden geliyor. Ya yarım aralık kaydırılmış ikinci bir 64'lük değerlendirme ızgarası ekleyin, ya da bunu bilinen bir sınır olarak yazın.

(iii) **Gecikmeyi Python yüküyle birlikte okuyun.** Fizibilite betiğinin yapay zamanlamasında tek senaryoda gradyan adımı K = 1'den K = 64'e yalnızca 0.21 → 0.31 ms çıkıyor. 300'lük toplu işte ise 0.57 → 12.48 ms (`results/wideband_feasibility.json`, `cost.timing`). İşlem sayısı K'yla doğrusal artıyor, ama tek senaryolu duvar saati yorumlayıcı yüküne gömülü olabilir. O zaman G2'nin öngördüğü ödünleşim ölçümde kaybolur ve büyük K_opt her yerde kazanır. Bu algoritmanın değil, uygulamanın sonucu olur. Gecikme tablosunun yanında işlem sayılarını da raporlayın.

**Neden:** Üçü de jürinin ya da hakemin bir bakışta göreceği türden. (iii) ayrıca tezin "FLOP değil duvar saati" tutumunu (Ryu vd.'ye karşı) kendi aleyhinize çevirebilir. Dürüst yanıt ikisini yan yana vermek. Duvar saati sıralamayı belirleyen ölçüt, işlem sayısı ise donanımdan bağımsız alt sınır.

**Literatüre dayanak:** Geniş bant optimize edicilerin adım maliyetinin alt taşıyıcıyla doğrusal arttığı notlarda bir çıkarım, hiçbir özette ölçekleme yasası olarak yazılmamış (genis_bant_ris notu, Q1). Kaplan'ın derlemesindeki 138 → 733 ms ölçümü eleman sayısına göre, alt taşıyıcıya göre değil ([arXiv:2606.31334](https://arxiv.org/abs/2606.31334)).

**Tezdeki yeri:** Geniş bant bölümünün "kurgu ve sınırlar" alt bölümü.

**Maliyet ve risk:** (i) bir satırlık kod değişikliği ve dokunulmamış bir ön kayıt sapması notu. (ii) değerlendirme maliyetini artırır; bellek W = 50 ms penceresini zaten düşürttü (`ON_KAYIT.md`). Sığmazsa yalnızca B = 100 MHz için yapın. Bu benim tahminim, betikle ölçün. (iii) ek ölçüm gerektirmez, işlem sayıları JSON'da var. Bir not: Adam adım boyunun 0.5'te sabit tutulması (ön kayıttaki sapma) K_opt'lar arasında yanlılık riski taşıyor. Ama `wb.py`'de amaç alt taşıyıcılar üzerinden **ortalama**, toplam değil; gradyan ölçeği K_opt ile büyümüyor ve bu riski azaltıyor. Tasarım kuralı sınaması bittiği için işlemci artık boş; plandaki "tasarım kuralı bitmeden başlatılmaz" koşulu karşılandı.

### Tavsiye 10 — Geniş bant deneyini tezin kapanışı yapın: her iki sonucu önceden yorumlayın, G4'ü x yasasına bağlayın

**Ne:** Tezin son deney bölümü tek bir soruya yanıt versin: "Bant genişliği, hesaplama gecikmesi ve hareketlilik birlikte (K_opt, L) seçimini nasıl belirler?" Koşmadan önce, ön kayda iki yorum ekleyin.

Birinci yorum, **G2 tutarsa:** geniş bant uyumu ancak bant uyum bandının birkaç katına çıkınca hesaplama süresine değiyor. Bu durumda tezin savunu cümlesi bant genişliği eksenine genelleşir.

İkinci yorum, **G2 tutmaz ve K_opt = 1 her B'de seçilirse:** bu da tez için güçlü bir sonuç. Statik ölçümde uyum kazancı küçük. Tek geniş bant fazının alt taşıyıcı başına optimuma göre kaybı 20/100 MHz'de %2.0/%4.1, merkez frekans fazınınki %3.1/%7.1 (`thesis_exp/genis_bant/PLAN.md`). Bu fark hareketlilikte hesaplama süresinin getirdiği eskimeyle yutuluyorsa, "gecikme sıralamayı belirler" hükmü geniş bantta da geçerli demektir.

G4'te ise K_opt'u x = ΔT·f_d'nin ΔT bileşenini değiştiren bir düğme olarak okuyun. Aynı Doppler'de dört farklı ΔT, tasarım kuralının narrowband kalibrasyonuyla ne kadar kayıp verdiğinin doğal bir dış sınamasıdır.

**Neden:** Makale 2'nin sonucu bu deneyi zaten vaat ediyor: "Our next step is wideband OFDM operation, where beam squint makes the best phase depend on frequency and adds a further trade-off between quality and time" (`PLAN.md`). Bunu yaparken bir düzeltme gerekiyor. Tavsiye 8'deki ölçüme göre bu geometride hüzme sapması ihmal edilebilir. Tezde "beam squint" yerine **"frekans seçiciliği"** deyin; Makale 2'deki cümleyle çelişkiyi sessizce geçmeyin. Notların sınanabilir çıkarımına göre, bant genişliği başına yalnızca etkin tap sayısı kadar serbestlik derecesi var. K_opt'tan gelen kazanç, örnekleme aralığı uyum bant genişliğinin altına inince doymalı. Düzgün aralıklı alt taşıyıcılar da bitişik olanlardan iyi olmalı. Bu, G2'ye fiziksel bir okuma verir. Ölçüm değil, hipotez olarak sunun.

**Literatüre dayanak:** Tek faz kısıtı [arXiv:2103.11105](https://arxiv.org/abs/2103.11105), [arXiv:1904.10136](https://arxiv.org/abs/1904.10136), [arXiv:2106.04280](https://arxiv.org/abs/2106.04280); MU-MISO-OFDM çapası [arXiv:2007.14243](https://arxiv.org/abs/2007.14243); "optimum indirgeme düzeyi" analogları [arXiv:1906.09956](https://arxiv.org/abs/1906.09956) ve [arXiv:2110.12799](https://arxiv.org/abs/2110.12799); K_opt boşluğu ve "çoğu çalışma RIS'i frekansa göre düz kabul ediyor" tespiti [arXiv:2606.31334](https://arxiv.org/abs/2606.31334). Geniş bant RIS'te hareketlilik ve optimize edici süresini birlikte modelleyen bir çalışma, önceki taramada da bu notlarda da bulunamadı. Tezin kapanış katkısı tam bu kesişimde duruyor.

**Tezdeki yeri:** Yeni bir Bölüm 7a ya da Bölüm 7'nin ana kısmı (gerçekçi senaryo eksenini "kısmi"den bir adım öteye taşır); Bölüm 8'in sonuç cümlesi. Makale 2'nin TWC sürümüne girmesini önermiyorum. Makale gönderime hazır, geniş bant ayrı bir kısa makale ya da tezin özgün bölümü olsun.

**Maliyet ve risk:** **Yeni deney gerektirir:** yaklaşık bir gün. Gecikme ölçümü 30 dk (boş makine), eğriler 3–4 saat, rapor ve denetim 2 saat (`PLAN.md` §4). 20 Kasım'a sığıyor, ama tek bir yeniden koşuya yer bırakıyor, ikinciye değil. Riskler şunlar. Gecikme ölçümü Tavsiye 9(iii)'deki yüke gömülebilir. Kusurlu CSI ve alt taşıyıcı başına pilot kapsam dışı, yani ZF her alt taşıyıcıda taze ve bedava; bu sınırı başlığa yakın yazın. CD ön kayıtta varsayılan taramayla tek gecikmede koşuyor, bu yüzden G3 "yavaş çözücünün en iyi ayarı" değil. CLAUDE.md'nin zayıf taban çizgisi uyarısı burada sıralamayı değiştirmez, çünkü CD'nin 702.97 ms'si en kısa taramada bile etkin hız ekseninde çok geride kalır. Yine de bunu raporda belirtin. Son olarak genlik ve yol kaybı fc'de tutuluyor; B/fc ≤ %3.3 için plan bunu kabul edilebilir sayıyor.

### On tavsiyenin özeti

| # | Tavsiye | Yeni deney? | Tahmini maliyet | En büyük risk |
| --- | --- | --- | --- | --- |
| 1 | Ölçüt merdiveni | Hayır | Yazım | Basamakların farklı sistemlerde gösterildiğini gizlemek |
| 2 | Makale 1'i yeniden konumlama | Hayır | Yazım + kaynak kontrolü | Fondo-Ferreiro'yu jüri getirirse |
| 3 | Köprünün dar adı | Hayır | Yazım | "Makale 1 başarısız" okuması |
| 4 | Ryu vd.'ye karşı yenilik | Hayır | ~1 gün yazım + arama | Daha yakın bir rakip çıkabilir |
| 5 | L* ve tasarım kuralı | Hayır (bitti) | Commit + yazım | W > 0'da L* sıkça ızgaranın ucunda |
| 6 | Protokol katkısı | Hayır | Yazım | GPU ölçülmedi |
| 7 | Standart zaman ölçekleri | Hayır | Yazım | Mutlak ms donanıma bağlı |
| 8 | Fiziksel rejim betiği | Analitik betik | Birkaç saat | Model InH'den sapabilir |
| 9 | Üç tasarım düzeltmesi | Koşudan önce | Saatler | Gecikmenin Python yüküne gömülmesi |
| 10 | Geniş bant kapanışı | **Evet** | ~1 gün | Tek yeniden koşu payı |

## Boşluklar ve doğrulanması gerekenler

Aşağıdaki maddeler savunmadan önce kapatılmalı. Çoğu "bulunamadı" türünden yokluk kanıtı ya da okunmamış tam metin.

| Ne | Neden açık | Ne yapılmalı |
| --- | --- | --- |
| "Gecikmeyi yöntem bağımlı eskime olarak modelleyen ilk çalışma" | ~17 + ~15 sorguluk hedefli arama; Scholar ve Xplore tam metin yok | Tavsiye 4'teki sorgular; "bilgimiz dahilinde" kalıbı |
| Zappone vd. 2021'de hesaplama süresinin yokluğu | Tam metin okunmadı | Tam metin ([arXiv:2003.02538](https://arxiv.org/abs/2003.02538)) |
| Guo–Makki–Svensson iterasyon iddiası | Yalnızca PDF parçası; UNVERIFIED | Tam metin ([arXiv:1703.03792](https://arxiv.org/abs/1703.03792)) |
| Lavi & Shlezinger'de klasik kolun bütçe başına ayarı | Doğrulanmadı | Tam metin ([arXiv:2301.00369](https://arxiv.org/abs/2301.00369)) |
| Ranjan vd. "convergence speed" iterasyon mu duvar saati mi | Kapalı erişim ([DOI 10.1109/LCOMM.2023.3289865](https://doi.org/10.1109/LCOMM.2023.3289865)) | Tam metin; PGD koluna en yakın klasik çalışma |
| Shaked vd. "limited latency" ölçülmüş bir bütçeye karşı mı | Yalnızca özet ([arXiv:2510.18978](https://arxiv.org/abs/2510.18978)) | Tam metin |
| Lin vd. JSAC 2020 alt çerçeve protokolünün ayrıntıları | İkincil özetler; UNVERIFIED ([DOI 10.1109/JSAC.2020.3007038](https://doi.org/10.1109/JSAC.2020.3007038)) | Özet ve tam metin |
| Optimum iterasyon için uyarlamalı filtre öncülü | Haykin bellekten; UNVERIFIED | LMS/RLS izleme literatürü taranmalı |
| K_opt alt kümesiyle RIS faz tasarımı yapan çalışma yokluğu | ~16 sorgu; Xplore tam metin yok | Savunmada "bulunamadı" deyin, "yok" değil |
| Makale 1'in "%29.9 RMSE iyileşmesi" | Yayıncı sayfası 403; arama özeti; UNVERIFIED | `aisy_paket/` ve makalenin kendisi |
| Makale 1 Fondo-Ferreiro'yu anıyor mu | Kontrol edilmedi | Makale 1 kaynakçası |
| 38.901 InH DS ve Bc değerleri (≈20/39 ns, 5–10 MHz) | Araştırmacı aritmetiği; ders kitabı kuralı yeniden doğrulanmadı | Tavsiye 8 betiği |
| TS 38.211 numerolojisi ve DMRS | Bu oturumda getirilmedi; UNVERIFIED | Sürüm ve madde sabitlenmeli |
| GR RIS 001/003 V1.2.1 ve GR RIS 005 | İndirilemedi; 2025 değişiklikleri UNVERIFIED | Alıntılar V1.1.1'e göre etiketlenmeli |
| Urbinati vd. MCU gecikme–hız cephesi | Tam metin okunmadı; UNVERIFIED | Alıntılamayın ya da tam metni okuyun |
| x = ΔT·f_d ölçekleme yasası | Bu denetimde yeniden sınanmadı (`TEZ_TAVSIYELERI.md` §3) | Geniş bant G4 kısmen sınar; tezde kapsamı belirtilmeli |
| Tasarım kuralı raporu | `REPORT.md`, `raw/validation.json` izlenmeyen dosya | Commit (Kural 3) |

## Sonuç

Bu taramadan çıkan ders şu: tezin özgünlüğü tek tek bileşenlerde değil, bileşenlerin birlikte ölçülmesinde. Gauss-Markov eskime, FLOP sayımı, eşit iterasyonda karşılaştırma ve tek fazlı OFDM tasarımı alanda ayrı ayrı var. Hiçbiri, her yöntemi kendi ölçülmüş süresi sonundaki kanalda ve klasik kolu her bütçede yeniden ayarlayarak değerlendirmiyor. Bu yüzden tezin en savunulabilir katkısı tek bir algoritma değil, bir ölçüm protokolü. Protokolün gücü de kendi sonuçlarınızı tersine çevirebilmesinden geliyor: L = 48'in kaybı, öğrenilen kuralın milisaniye başına yenilgisi, uzun tutmada iç optimumun ızgaranın ucuna kayması.

Geniş bant deneyi bu protokolü dördüncü bir eksene taşıyor. Sonucu ne çıkarsa çıksın tezi kapatır, çünkü iki olası sonucun yorumu koşudan önce yazılabilir. Gerçek risk deney sonucunda değil, ölçümün kendisinde. Tek senaryolu Python zamanlaması alt taşıyıcı maliyetini gizlerse, tezin "duvar saati" tutumu tam kapanış bölümünde zayıf düşer. Bu yüzden önümüzdeki dört günün en değerli saati, geniş bant gecikme tablosunun yanına işlem sayılarını koyup ikisinin aynı hikâyeyi anlatıp anlatmadığına bakmakla geçer.
