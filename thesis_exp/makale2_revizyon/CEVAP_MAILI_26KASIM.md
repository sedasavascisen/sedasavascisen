**Konu:** Makale 2 (TWC): yorumlarınıza göre revize edilmiş sürüm

Sayın Hocam,

Değerli yorumlarınız için teşekkür ederim. Altı noktanın hepsini makaleye işledim. Ayrıca makaleyi bir TWC editörünün gözüyle yeniden değerlendirip olası hakem itirazlarına karşı ek düzeltmeler yaptım (aşağıda 7. bölüm). Revize edilmiş PDF ve kısa bir ek belge (supplementary material) ektedir.

Hiçbir sonuç sayısı değişmedi. Değişiklikler metin, sunuş, iki yeni tablo ve tezde daha önce yapılıp denetlenmiş iki sağlamlık kontrolünden ibaret. Makale 9 sayfadan 10 sayfaya çıktı; TWC'nin ek ücret alınmayan 10 sayfa sınırı içinde kalıyor.

**1. Özet**

Özeti baştan yazdım. Sırasıyla şunları veriyor:
- **Problem:** yöntemler kendilerine verilen kanaldaki hızla karşılaştırılıyor, oysa kanal onlarca milisaniyede değişiyor.
- **Yenilik:** her yöntem, hesaplaması bittiğindeki kanalda ve ölçülmüş gecikmeyle değerlendiriliyor (etkin hız).
- **Teorik katkı:** küçük gecikme modeli (Önerme 1), model içinde, sıfırdan büyük her adım süresinde bir iç optimum bulunduğunu gösteriyor. Ölçümlere uydurulmuş sabitlerle de optimumun nasıl ölçeklendiğini açıklıyor.
- **Uyarlanabilirlik sonucu:** optimal adım sayısını adım süresinin Doppler frekansına oranı belirliyor; optimum 3 km/h'de 8 adımdan 30 km/h'de 1 adıma iniyor. Dolayısıyla adım sayısı kullanıcı hızına ve donanıma göre seçilmeli. Bu, katkılarda da açıkça yazılı.
- **Ana varsayımlar:** özet, kanal bilgisinin kusursuz olduğunu ve ön kodlayıcının güncel kanaldan hesaplandığını artık açıkça söylüyor.

Özet 197 kelime (TWC sınırı 200). Açılmamış kısaltma ve matematik sembolü içermiyor.

Bir not: kapalı formun ölçülen optimuma 1.27 kat yakınlığı bir örnek içi kontroldür; model ölçümleri bağımsız olarak öngörmüyor, açıklıyor. Bu yüzden kapalı formu özette "öngörücü bir kural" olarak sunmadım; bu, makalenin gövdesindeki kayıtlarla da tutarlı. Periyodik çalışma sonucu (güncelleme periyodunu pilot yükü belirliyor, güncelleme başına en fazla 8 adım yetiyor) kelime sınırı nedeniyle özete sığmadı; katkılarda ve sonuçta duruyor.

**2. Akademik üslup**

- Katkılar ve sonuç bölümündeki slogan biçimli başlıkları kaldırdım ("Speed beats precision.", "Learning on the clock." vb.). Maddeler artık düz akademik cümleler.
- Sonuç bölümünün "Practical rules" başlığı "Design guidelines" oldu.
- Bulgu bildiren alt bölüm başlıklarını betimleyici başlıklarla değiştirdim. Örneğin:
  - "One Number Sets the Optimum" → "Scaling of the Optimum with the Normalized Step Cost";
  - "The Fresh-Beam Assumption Matters" → "Sensitivity to the Fresh-Precoder Assumption".
- Girişteki gayriresmî ifadeler de yeniden yazıldı ("That comparison hides a race…", "the question has changed" vb.).
- Metindeki "cheap", "flatters", "nearly free", "pays off" gibi ifadeler akademik karşılıklarıyla değiştirildi.

**3. Literatür karşılaştırma tablosu (yeni Tablo I)**

- Tablo, 14 temsilî çalışmayı (10 satırda) ve bu çalışmayı dört eksende karşılaştırıyor: çözülen problem, kanal değişiminin modellenip modellenmediği, çalışma süresinin nasıl verildiği ve sürenin değerlendirmede oynadığı rol.
- Her hücre, daha önce kaynakların PDF'lerinden yaptığım satır satır kontrole dayanıyor.
- Tablo, çalışmanın farkını açıkça gösteriyor: diğer çalışmalarda süre ya hiç yok, ya sabit bir kanalda ölçülüyor, ya da yalnızca bir uygulanabilirlik koşulu olarak kullanılıyor. Bu çalışmada ise ölçülen süre kanal eskimesine giriyor ve yöntemler eşit gecikmede karşılaştırılıyor.

**4. Hiperparametre tablosu (yeni Tablo II)**

Yedi yöntemin hepsi için ayarlar ve hesaplama maliyeti tek tabloda:
- başlangıç noktası, amaç fonksiyonu (yumuşak minimum, β = 8), adım boyu;
- optimum iterasyon sayısı: Adam için 1.5 m/s'de L* = 4–6, Armijo için L* = 4;
- koordinat inişinin faz düzeyi sayısı ve tarama sayısı;
- uzun koşulu Adam'ın yineleme ve başlangıç sayısı;
- öğrenilen modelin eğitim ayarları (parametre sayısı, öğrenme oranı, yığın boyutu, epoch).

**5. Öğrenme tabanlı algoritmanın girdileri**

Yöntem bölümüne bunları koddan doğrulayarak açıkça yazdım:
- **Her kullanıcı ve RIS elemanı için 37 sabit girdi kanalı:**
  - normalize RIS–kullanıcı kanalının gerçel ve sanal kısımları;
  - 8 BS antenindeki BS–RIS kanalı;
  - doğrudan kanal;
  - kullanıcının tek kullanıcılı hizalama fazının kosinüs ve sinüsü;
  - kullanıcının göreli kanal gücü.
- **Her adımda eklenen 4 dinamik kanal:**
  - güncel fazın kosinüs ve sinüsü;
  - kullanıcının standartlaştırılmış hızı;
  - yumuşak minimum hızın normalize gradyanı.
- **Mimari:** elemanlar boyunca evrişimli ve LSTM katmanları, kullanıcılar arasında bilgi paylaşan iki katman ve faz güncellemesini üreten eleman başına bir çıkış katmanı. Ağırlıklar adımlar arasında ortak; adım boyu öğreniliyor. Eğitim etiketsiz.

**6. Adam'ın işlem süresinin farklı değerlerle verilmesi**

Haklısınız; metin bunu yeterince açık anlatmıyordu. Adam'ın adım süresi makalede üç farklı ölçüm oturumundan geliyor ve her biri bir deneye bağlı:

| Değer | Nereden | Nerede kullanılıyor |
| --- | --- | --- |
| 1.66 ms | Eskime kümesinde yapılan ilk ölçüm (8 adım 13.3 ms; iki iş parçacığı, ön kodlayıcı düzeltmesinden önce). Sonraki turların 1.49–2.02 ms aralığının içinde. | Ana sonuçlar (Bölüm VI-A–E) |
| 1.60–1.71 ms | Statik kümedeki karşılaştırmanın kendi ölçümü (beş turun medyanları) | Öğrenilen kuralla karşılaştırma (Bölüm VI-F) |
| 1.33 ms | Tek iş parçacığıyla, boş makinede yapılan yeniden ölçüm | Sağlamlık analizleri (Bölüm VI-H) |

Farklar ölçüm koşullarından ve zamanlama değişkenliğinden kaynaklanıyor; aynı kod, farklı oturumlar. Ana sonuç, eskime kümesindeki iki değerden hangisinin kullanıldığına bağlı değil: 1.33 ms ile optimum L* = 6 ve 48 adımın kaybı %14.9; 1.66 ms ile L* = 4–6 ve %14.0. Makaledeki cümleyi de bu kapsamla sınırladım.

Değişiklikler:
- Zamanlama paragrafını üç değeri ve kullanıldıkları bölümleri açıkça sayacak biçimde yeniden yazdım.
- Tablo II'ye bunu gösteren bir dipnot ekledim.

**7. Ek olarak yaptığımız çalışmalar ve değişiklikler**

Yorumlarınızı işledikten sonra makaleyi bir TWC editörünün gözüyle değerlendirdim. Hakemlerin en olası itirazlarını listeleyip makalede şu değişiklikleri yaptım:

- **Teorinin kapsamı:** özette "proves" yerine "shows" kullandım. Katkılarda, modelin sabitlerinin ölçümlere uydurulduğunu ve modelin ölçümleri öngörmekten çok açıkladığını yazdım. Bu, Bölüm VI-C'deki mevcut kayıtlarla tutarlı.
- **Yeniliğin tanımı:** girişe, katkının yalnızca yeni bir ölçüt değil, bu ölçütün ortaya çıkardığı davranış olduğunu ekledim: iterasyon sayısında bir iç optimum ve bu optimumun tek bir normalize nicelikle belirlenmesi.
- **Sonucun gerçekleştirmeye bağlılığı** (gecikmeler Python'da ölçüldüğü için hakem soracaktır): Bölüm VI-C'ye, tezde yapılmış bir kontrolü ekledim. Kayan noktalı işlem sayısına dayanan bir maliyet modeli, ölçülen süreyle aynı adım sayısını seçiyor (1.5 m/s'de 6, 10 km/h'de 4 adım) ve iki sıralama arasında Kendall τ = 0.86–0.87. Bütün yöntemlerin eşit hızlandırıldığı durumda ayarlı Adam'ın önde kaldığı sonucu zaten sonuç bölümündeydi.
- **Tek kanal modeli:** Bölüm VI-D'ye tezdeki Clarke kanalı kontrolünü ekledim. Sabit saçıcıların korelasyon tabanı olmayan bu kanalda da iç optimum var: 3–10 km/h'de 3–8 adım (3.4–8.8 ms) ve 48 adım %27–32 kaybettiriyor.
- **RIS anahtarlama süresi:** sınırlar bölümüne, bu sürenin (≥ 0.72 ms) ek bir sabit gecikme gibi davrandığını ve Bölüm VI-D'de incelenen 0–10 ms'lik kanal edinme gecikmesi aralığına düştüğünü yazdım.
- **Öğrenilen yöntemin kapsamı:** katkılarda, karşılaştırmanın hesaplama maliyetini ayırmak için statik kanallarda yapıldığını açıkça belirttim.
- **Sunuş:** Zamanlama bölümü bir ölçüm günlüğü gibi okunuyordu. Yük ortalamalarını, tur sayılarını ve turlar arası farkları bir sayfalık ek belgeye taşıdım; ana metin oraya başvuruyor, hiçbir bilgi silinmedi.
- **Gelecek çalışma:** ikinci bir geometri, CDL (clustered delay-line) kanalı ve SDR ile WMMSE'nin zamanlanması sonuç bölümünde gelecek çalışma olarak yer alıyor.

Ertelediğimiz bir iş var: bütün tablo ve şekilleri tek bir temiz zamanlama oturumuyla (Adam adımı 1.33 ms) yeniden üretmek. Bu oturumun ölçümleri hazır, ama geçiş yaklaşık 60 sayıyı değiştiriyor ve 1–2 iş günü sürüyor. Şimdilik üç değeri açıkça anlatmayı ve sonuçların 1.33 ms ile de korunduğunu göstermeyi tercih ettim. Hakem isterse revizyonda yapılabilir; plan hazır.

Bu kontrollerin hepsi daha önce bağımsız olarak denetlendi; makalenin sayısal iddiaları otomatik denetleyicilerden de geçiyor.

Bütün değişiklikler, eski ve yeni hâlleriyle birlikte, revizyon kayıt dosyasında duruyor.

Ayrıca bir öneri: tezde, adım sayısını önceden seçen bir tasarım kuralı ve bunu kullanan, her güncellemede başlangıç noktasını ve adım sayısını seçen bir denetleyici var. Kural, ön kayıtlı 60 koşullu bağımsız sınamada doğru adım sayısına göre medyan %0.08 kaybettiriyor. Bu sonuç şu an makalede yok. Uyarlanabilir yöntemi daha da öne çıkarmak isterseniz kısa bir paragraf olarak ekleyebilirim; makale yine 10 sayfada kalacak biçimde.

Saygılarımla,
Seda Savaşçı Şen

Ekler:
- Latency-Aware_Phase_Optimization_v27.pdf
- supplementary.pdf
