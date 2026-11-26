**Konu:** Re: Makale önerileri — revize edilmiş sürüm (v28)

Merhaba Hocam,

Güzel sözleriniz ve önerileriniz için çok teşekkür ederim. Önerilerinizin hepsini makaleye işledim; her birine aşağıda tek tek cevap verdim. Bunların yanında makaleyi olası hakem itirazlarına karşı da gözden geçirip bazı ek değişiklikler yaptım; onları en sonda ayrıca yazdım. Revize edilmiş makale (v28) ve kısa bir ek belge (supplementary material) ektedir.

Hiçbir sonuç sayısı değişmedi. Makale 9 sayfadan 10 sayfaya çıktı; TWC'nin ek ücret alınmayan 10 sayfa sınırı içinde kalıyor.

---

> *Özeti bence elden geçirelim (problem, yenilik, teorik katkı ve adaptif yöntem sonuçları daha net vurgulasak iyi olur).*

Özeti baştan yazdım (197 kelime; TWC sınırı 200). Artık şu sırayla ilerliyor:
- **Problem:** yöntemler kendilerine verilen kanaldaki hızla karşılaştırılıyor, oysa yürüyen bir kullanıcı kanalı onlarca milisaniyede değiştiriyor.
- **Yenilik:** her yöntem, hesaplaması bittiği andaki kanalda ve ölçülmüş gecikmeyle değerlendiriliyor (etkin hız).
- **Sonuçlar:**
  - yavaş çözücüler, dağıtım anında 2.5 ms süren tek kullanıcılı bir sezgisel yöntemin gerisinde kalıyor;
  - iterasyon sayısında bir iç optimum var: 1.5 m/s'de 4–6 Adam adımı; 48 adım %14 kaybettiriyor;
  - öğrenilen yöntem eşit adımda kazanıyor, ama eşit gecikmede baskınlanıyor.
- **Uyarlanabilir sonuç:** optimum adım sayısını, adım süresinin Doppler frekansına oranı belirliyor. Optimum 3 km/h'de 8 adımdan 30 km/h'de 1 adıma iniyor; yani adım sayısı kullanıcı hızına ve donanıma göre seçilmeli. Bu, katkılar bölümünde de açıkça yazılı.
- **Teorik katkı:** küçük gecikme modeli (Önerme 1), model içinde, sıfırdan büyük her adım süresinde bir iç optimum bulunduğunu gösteriyor. Ölçümlere uydurulmuş sabitlerle de optimumun nasıl ölçeklendiğini açıklıyor.

Bir noktayı bilerek temkinli yazdım: kapalı formun ölçülen optimuma 1.27 kat yakınlığı bir örnek içi kontrol. Model ölçümleri bağımsız olarak öngörmüyor, açıklıyor. Bu yüzden özette onu "öngörücü bir kural" olarak sunmadım; hakem gövdeyle özeti karşılaştırırsa çelişki görmesin istedim.

> *Metin daha akademik ifadelerle yazılmalı; mesela "1) Speed beats precision." gibi çok ifade var, bunlar yapay zekâ ifadeleri gibi duruyor.*

Haklısınız; düzelttim:
- Katkılar ve sonuç bölümündeki slogan biçimli başlıkları ("Speed beats precision.", "Learning on the clock." vb.) kaldırdım; maddeler artık düz akademik cümleler.
- "Practical rules" başlığı "Design guidelines" oldu.
- Bulgu bildiren sekiz alt bölüm başlığını betimleyici başlıklarla değiştirdim. Örneğin "One Number Sets the Optimum" artık "Scaling of the Optimum with the Normalized Step Cost".
- Girişteki ve metindeki gayriresmî ifadeleri ("That comparison hides a race…", "cheap", "flatters", "nearly free", "pays off" vb.) akademik karşılıklarıyla yeniden yazdım.

> *Literatüre bir karşılaştırma tablosu eklenmeli.*

Yeni Tablo I'i ekledim. On dört temsilî çalışmayı (10 satırda) ve bizim çalışmamızı dört eksende karşılaştırıyor:
- çözülen problem;
- kanal değişiminin modellenip modellenmediği;
- çalışma süresinin nasıl verildiği;
- sürenin değerlendirmedeki rolü.

Her hücre, kaynakların PDF'lerinden yaptığımız satır satır kontrole dayanıyor. Tablo farkımızı açıkça gösteriyor: diğer çalışmalarda süre ya hiç yok, ya sabit bir kanalda ölçülüyor, ya da yalnızca bir uygulanabilirlik koşulu olarak kullanılıyor. Bizde ise ölçülen süre kanal eskimesine giriyor ve yöntemler eşit gecikmede karşılaştırılıyor.

> *Modeller için hiperparametre tablosu (optimum iterasyon sayısı vb.)*

Yeni Tablo II'yi ekledim. Yedi yöntemin hepsi için ayarları ve hesaplama maliyetini veriyor:
- başlangıç noktası, amaç fonksiyonu, adım boyu;
- optimum iterasyon sayısı: Adam için 1.5 m/s'de 4–6, Armijo için 4;
- koordinat inişinin faz düzeyi ve tarama sayısı;
- uzun koşulu Adam'ın yineleme ve başlangıç sayısı;
- öğrenilen modelin eğitim ayarları (parametre sayısı, öğrenme oranı, yığın boyutu, epoch).

> *Öğrenme tabanlı algoritmanın girdileri ??*

Bu gerçekten eksikti. Yöntem bölümüne, koddan doğrulayarak ekledim:
- **Her kullanıcı ve RIS elemanı için 37 sabit girdi kanalı:**
  - RIS–kullanıcı, BS–RIS ve doğrudan kanalların gerçel ve sanal kısımları;
  - kullanıcının tek kullanıcılı hizalama fazının kosinüs ve sinüsü;
  - kullanıcının göreli kanal gücünün logaritması.
- **Her adımda eklenen 4 dinamik kanal:** güncel fazın kosinüs ve sinüsü, kullanıcının standartlaştırılmış hızı ve yumuşak minimum hızın normalize gradyanı.
- **Mimari:** elemanlar boyunca evrişimli ve LSTM katmanları, kullanıcılar arasında bilgi paylaşan iki katman ve eleman başına bir çıkış katmanı. Ağırlıklar adımlar arasında ortak, adım boyu öğreniliyor ve eğitim etiketsiz.

> *Adam algoritmasının işlem süresi farklı farklı ifade edilmiş, neden?*

Haklısınız, metin bunu açık anlatmıyordu. Değerler farklı ölçüm oturumlarından geliyor ve her biri belirli bir deneye bağlı:

| Değer | Nereden geliyor | Nerede kullanılıyor |
| --- | --- | --- |
| 1.66 ms | İlk ölçüm (iki iş parçacığı, ön kodlayıcı düzeltmesinden önce); sonraki turların 1.49–2.02 ms aralığında | Ana sonuçlar (Bölüm VI-A–E) |
| 1.60–1.71 ms | Statik kümedeki karşılaştırmanın kendi ölçümü (beş tur) | Öğrenilen kuralla karşılaştırma (VI-F) |
| 1.33 ms | Tek iş parçacığıyla, boş makinede yeniden ölçüm | Sağlamlık analizleri (VI-H) |

Farklar ölçüm koşullarından ve zamanlama değişkenliğinden kaynaklanıyor; kod aynı. Önemli olan, sonucun bu değerlere bağlı olmaması: 1.33 ms ile optimum 6 adım ve 48 adımın kaybı %14.9; 1.66 ms ile optimum 4–6 adım ve kayıp %14.0.

Değişiklikler:
- Zamanlama paragrafını üç değeri ve kullanıldıkları bölümleri açıkça sayacak biçimde yeniden yazdım.
- Tablo II'ye bir dipnot ekledim.
- Ayrıntıları (yük ortalamaları, tur sayıları) ek belgeye koydum.

---

**Ek olarak yaptığım değişiklikler**

Önerilerinizi işledikten sonra makaleyi bir TWC editörünün gözüyle değerlendirdim ve hakemlerin en olası itirazlarına karşı şunları yaptım:

1. **Teorinin kapsamı:** özette "proves" yerine "shows" kullandım. Katkılarda modelin sabitlerinin ölçümlere uydurulduğunu belirttim.
2. **Yeniliğin tanımı:** girişte katkının yalnızca yeni bir ölçüt olmadığını, bu ölçütün ortaya çıkardığı davranış olduğunu yazdım: iç optimum ve onu belirleyen tek normalize nicelik.
3. **Python'da ölçülen gecikmeler** (hakemin ilk soracağı şey): tezde yapılmış bir kontrolü Bölüm VI-C'ye ekledim. İşlem sayısına (FLOP) dayalı bir maliyet modeli, ölçülen süreyle aynı adım sayısını seçiyor (Kendall τ = 0.86–0.87).
4. **Tek kanal modeli:** tezdeki Clarke kanalı kontrolünü Bölüm VI-D'ye ekledim. Orada da iç optimum var: 3–8 adım; 48 adım %27–32 kaybettiriyor.
5. **RIS anahtarlama süresi:** sınırlar bölümüne, ek bir sabit gecikme gibi davrandığını ve incelediğimiz 0–10 ms'lik gecikme aralığına düştüğünü yazdım.
6. **Öğrenilen yöntemin kapsamı:** karşılaştırmanın hesaplama maliyetini ayırmak için statik kanalda yapıldığını belirttim.
7. **Ek belge:** ölçüm günlüğü ayrıntılarını bir sayfalık ek belgeye taşıdım. Ana metin sadeleşti, hiçbir bilgi silinmedi.
8. **Gelecek çalışma:** ikinci bir geometri, CDL kanal modeli ve SDR ile WMMSE'nin zamanlanması sonuç bölümüne eklendi.
9. **Kaynak ve tutarlılık kontrolü:**
   - 46 kaynağın hepsi PDF'lerinden tek tek kontrol edilmiş; kontrol edilmemiş kaynak kalmadı.
   - Makalenin bölümleri arasında bağımsız bir tutarlılık okuması yaptım ve bulunan çelişkileri giderdim. Örneğin yavaş çözücülerin kaybının "dağıtım anında" olduğu artık özette de yazıyor; sonuç bölümünde gövdede olmayan birkaç sayı kaynaklarıyla ek belgeye kondu.

Bir işi bilerek erteledim: bütün tablo ve şekilleri tek bir temiz zamanlama oturumuyla yeniden üretmek. Ölçümler hazır, ama geçiş yaklaşık 60 sayıyı değiştiriyor ve 1–2 iş günü sürüyor. Hakem isterse revizyonda yapabiliriz.

Son olarak bir öneri: tezde, adım sayısını önceden seçen bir tasarım kuralı ve bunu kullanan bir denetleyici var. Kural, ön kayıtlı 60 koşullu bağımsız sınamada doğru adım sayısına göre medyan %0.08 kaybettiriyor. Uyarlanabilir yöntemi daha da öne çıkarmak isterseniz bunu kısa bir paragraf olarak ekleyebilirim.

Bütün değişiklikler, eski ve yeni hâlleriyle bir revizyon kayıt dosyasında duruyor; isterseniz onu da gönderebilirim.

Saygılarımla,
Seda

Ekler:
- Latency-Aware_Phase_Optimization_v28.pdf
- supplementary.pdf
