**Konu:** Makale 2 (TWC): yorumlarınıza göre revize edilmiş sürüm

Sayın Hocam,

Değerli yorumlarınız için teşekkür ederim. Altı noktanın hepsini makaleye işledim; revize edilmiş PDF ektedir. Hiçbir sonuç sayısı değişmedi. Değişiklikler metin, sunuş ve iki yeni tablodan ibaret. Makale 9 sayfadan 10 sayfaya çıktı; TWC'nin ek ücret alınmayan 10 sayfa sınırı içinde kalıyor.

**1. Özet**

Özeti baştan yazdım. Sırasıyla şunları veriyor:
- **Problem:** yöntemler kendilerine verilen kanaldaki hızla karşılaştırılıyor, oysa kanal onlarca milisaniyede değişiyor.
- **Yenilik:** her yöntem, hesaplaması bittiğindeki kanalda ve ölçülmüş gecikmeyle değerlendiriliyor (etkin hız).
- **Teorik katkı:** küçük gecikme modeli (Önerme 1), sıfırdan büyük her adım süresinde bir iç optimum bulunduğunu ispatlıyor. Uydurulmuş sabitlerle de optimumun nasıl ölçeklendiğini açıklıyor.
- **Uyarlanabilirlik sonucu:** optimal adım sayısını adım süresinin Doppler frekansına oranı belirliyor; optimum 3 km/h'de 8 adımdan 30 km/h'de 1 adıma iniyor. Dolayısıyla adım sayısı kullanıcı hızına ve donanıma göre seçilmeli. Bu, katkılarda da açıkça yazılı.
- **Ana varsayım:** özet, ön kodlayıcının güncel kanaldan hesaplandığını artık açıkça söylüyor.

Özet 193 kelime (TWC sınırı 200). Açılmamış kısaltma ve matematik sembolü içermiyor.

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

Bütün değişiklikler, eski ve yeni hâlleriyle birlikte, revizyon kayıt dosyasında duruyor.

Ayrıca bir öneri: tezde, bu kapalı formu kullanan ve her güncellemede başlangıç noktasını ve adım sayısını seçen bir denetleyici var. Ön kayıtlı 60 koşullu sınamada doğru adım sayısına göre medyan kaybı %0.08. Bu sonuç şu an makalede yok. Uyarlanabilir yöntemi daha da öne çıkarmak isterseniz kısa bir paragraf olarak ekleyebilirim; makale yine 10 sayfada kalacak biçimde.

Saygılarımla,
Seda Savaşçı Şen

Ek: Latency-Aware_Phase_Optimization_v26.pdf
