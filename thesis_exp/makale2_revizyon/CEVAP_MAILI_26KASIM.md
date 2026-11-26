**Konu:** Makale 2 (TWC): yorumlarınıza göre revize edilmiş sürüm (v28)

Sayın Hocam,

Değerli yorumlarınız için teşekkür ederim. Altı noktanın hepsini makaleye işledim. Ayrıca makaleyi bir TWC editörünün gözüyle değerlendirip olası hakem itirazlarına karşı ek düzeltmeler yaptım, ardından makalenin baştan sona tutarlılık ve kaynak kontrolünü tamamladım. Revize edilmiş makale (v28) ve kısa bir ek belge (supplementary material) ektedir.

Hiçbir sonuç sayısı değişmedi. Makale 9 sayfadan 10 sayfaya çıktı; TWC'nin ek ücret alınmayan 10 sayfa sınırı içinde kalıyor.

## A. Yorumlarınız ve yapılanlar

**1. Özet**
- **İstenen:** problem, yenilik, teorik katkı ve uyarlanabilir yöntemin sonuçları daha net vurgulanmalı.
- **Yapılan:** özet baştan yazıldı (197 kelime; TWC sınırı 200). Sırasıyla şunları veriyor:
  - **Problem:** yöntemler kendilerine verilen kanaldaki hızla karşılaştırılıyor, oysa kanal onlarca milisaniyede değişiyor.
  - **Yenilik:** her yöntem, hesaplaması bittiğindeki kanalda ve ölçülmüş gecikmeyle değerlendiriliyor (etkin hız).
  - **Sonuçlar:**
    - yavaş çözücüler, dağıtım anında 2.5 ms süren bir sezgisel yöntemin gerisinde kalıyor;
    - iterasyon sayısında bir iç optimum var: 1.5 m/s'de 4–6 Adam adımı; 48 adım %14 kaybettiriyor;
    - öğrenilen yöntem eşit adımda kazanıyor, ama eşit gecikmede baskınlanıyor.
  - **Uyarlanabilirlik:** optimumu adım süresinin Doppler frekansına oranı belirliyor. Optimum 3 km/h'de 8 adımdan 30 km/h'de 1 adıma iniyor; yani adım sayısı kullanıcı hızına ve donanıma göre seçilmeli.
  - **Teorik katkı:** küçük gecikme modeli (Önerme 1), model içinde, sıfırdan büyük her adım süresinde bir iç optimum bulunduğunu gösteriyor. Ölçümlere uydurulmuş sabitlerle de optimumun ölçeklenmesini açıklıyor.
  - **Varsayımlar:** kusursuz kanal bilgisi ve güncel kanaldan hesaplanan ön kodlayıcı özette açıkça yazılı.
- **Not:** kapalı formun ölçülen optimuma 1.27 kat yakınlığı bir örnek içi kontrol; model ölçümleri öngörmüyor, açıklıyor. Bu yüzden özette onu öngörücü bir kural olarak sunmadım.

**2. Akademik üslup**
- **İstenen:** "Speed beats precision." gibi yapay zekâ üslubu taşıyan ifadeler akademik ifadelerle değiştirilmeli.
- **Yapılan:**
  - Katkılar ve sonuç bölümündeki slogan biçimli başlıklar kaldırıldı; maddeler düz akademik cümleler oldu.
  - "Practical rules" başlığı "Design guidelines" oldu.
  - Bulgu bildiren sekiz alt bölüm başlığı betimleyici başlıklarla değiştirildi.
  - Girişteki ve metindeki gayriresmî ifadeler yeniden yazıldı ("hides a race", "cheap", "flatters", "nearly free", "pays off" vb.).

**3. Literatür karşılaştırma tablosu**
- **İstenen:** literatürle karşılaştırma tablosu eklenmeli.
- **Yapılan:** yeni Tablo I. On dört temsilî çalışma (10 satırda) ve bu çalışma dört eksende karşılaştırılıyor:
  - çözülen problem;
  - kanal değişimi;
  - çalışma süresinin nasıl verildiği;
  - sürenin değerlendirmedeki rolü.

  Her hücre, kaynakların PDF'lerinden yaptığımız kontrole dayanıyor. Tablo farkı açıkça gösteriyor: diğer çalışmalarda süre ya hiç yok, ya sabit bir kanalda ölçülüyor, ya da yalnızca bir uygulanabilirlik koşulu. Bu çalışmada ölçülen süre kanal eskimesine giriyor ve yöntemler eşit gecikmede karşılaştırılıyor.

**4. Hiperparametre tablosu**
- **İstenen:** modeller için hiperparametre tablosu (optimum iterasyon sayısı vb.).
- **Yapılan:** yeni Tablo II. Yedi yöntemin ayarları ve hesaplama maliyeti tek tabloda:
  - başlangıç noktası, amaç fonksiyonu, adım boyu;
  - optimum iterasyon sayısı: Adam için 1.5 m/s'de 4–6, Armijo için 4;
  - koordinat inişinin faz düzeyi ve tarama sayısı;
  - uzun koşulu Adam'ın ayarları;
  - öğrenilen modelin eğitim ayarları.

**5. Öğrenme tabanlı algoritmanın girdileri**
- **İstenen:** girdiler açıkça yazılmalı.
- **Yapılan:** Yöntem bölümüne, koddan doğrulanarak eklendi:
  - **Her kullanıcı ve RIS elemanı için 37 sabit girdi kanalı:** RIS–kullanıcı, BS–RIS ve doğrudan kanalların gerçel ve sanal kısımları; tek kullanıcılı hizalama fazının kosinüs ve sinüsü; göreli kanal gücünün logaritması.
  - **Her adımda eklenen 4 dinamik kanal:** güncel fazın kosinüs ve sinüsü, standartlaştırılmış kullanıcı hızı ve yumuşak minimum hızın normalize gradyanı.
  - **Mimari ve eğitim:** mimari tarif edildi; eğitim etiketsiz ve ayarları Tablo II'de.

**6. Adam'ın işlem süresinin farklı değerlerle verilmesi**
- **İstenen:** neden farklı değerler var?
- **Yapılan:** değerler farklı ölçüm oturumlarından geliyor ve her biri bir deneye bağlı. Bunu metinde, Tablo II'nin dipnotunda ve ek belgede açıkça yazdım:

| Değer | Nereden | Nerede kullanılıyor |
| --- | --- | --- |
| 1.66 ms | İlk ölçüm (iki iş parçacığı, ön kodlayıcı düzeltmesinden önce); sonraki turların 1.49–2.02 ms aralığında | Ana sonuçlar (VI-A–E) |
| 1.60–1.71 ms | Statik kümenin kendi ölçümü (beş tur) | Öğrenilen kuralla karşılaştırma (VI-F) |
| 1.33 ms | Tek iş parçacığıyla, boş makinede yeniden ölçüm | Sağlamlık analizleri (VI-H) |

Ek kontrollerin ayrı oturumları (1.086 ms ve 1.60 ms) ek belgede listeleniyor. Optimum ve 48 adımın maliyeti, eskime kümesindeki iki değerden hangisinin kullanıldığına bağlı değil: 1.33 ms ile L* = 6 ve %14.9, 1.66 ms ile L* = 4–6 ve %14.0.

## B. Ek olarak yaptıklarımız

**7. Editör gözüyle değerlendirme ve olası hakem itirazlarına karşı düzeltmeler**
- **Teorinin kapsamı:** özette "proves" yerine "shows"; modelin sabitlerinin ölçümlere uydurulduğu yazıldı.
- **Yeniliğin tanımı:** katkının yalnızca yeni bir ölçüt değil, bu ölçütün ortaya çıkardığı davranış olduğu girişte açıkça yazıldı: iç optimum ve onu belirleyen tek normalize nicelik.
- **Sonucun gerçekleştirmeye bağlılığı:** Bölüm VI-C'ye tezde yapılmış bir kontrol eklendi. İşlem sayısına (FLOP) dayalı bir maliyet modeli, ölçülen süreyle aynı adım sayısını seçiyor (Kendall τ = 0.86–0.87).
- **Tek kanal modeli:** Bölüm VI-D'ye Clarke kanalı kontrolü eklendi. Optimum 3–8 adım (3.4–8.8 ms); 48 adım %27–32 kaybettiriyor.
- **RIS anahtarlama süresi:** ek bir sabit gecikme gibi davrandığı ve incelenen 0–10 ms'lik gecikme aralığına düştüğü yazıldı.
- **Öğrenilen yöntemin kapsamı:** karşılaştırmanın hesaplama maliyetini ayırmak için statik kanalda yapıldığı belirtildi.
- **Sunuş:** zamanlama ayrıntıları (yük ortalamaları, tur sayıları, turlar arası farklar) bir sayfalık ek belgeye taşındı. Hiçbir bilgi silinmedi; ana metin ek belgeye başvuruyor.
- **Gelecek çalışma:** ikinci bir geometri, CDL kanal modeli ve SDR ile WMMSE'nin zamanlanması sonuç bölümünde gelecek çalışma olarak yer aldı.

**8. Tutarlılık ve kaynak kontrolü**
- **Kaynaklar:** 46 kaynağın hepsi PDF'lerinden tek tek kontrol edilmiş; kontrol edilmemiş kaynak yok. Sonradan eklenen atıflar (Tablo I, Clarke) da doğrulandı.
- **Tutarlılık:** makalenin bölümleri arasında bağımsız bir tutarlılık okuması yapıldı. Bulunan çelişkiler giderildi. Önemlileri:
  - "bütün gecikmeler tek iş parçacığıyla" ifadesindeki istisna (1.66 ms) açıkça yazıldı;
  - yavaş çözücülerin kaybının "dağıtım anında" olduğu özette ve katkılarda belirtildi;
  - sonuç bölümünde gövdede olmayan sayılar (derlenmiş koordinat inişi, OFDM kontrolü) kaynaklarıyla ek belgeye kondu;
  - ayrık faz ve tarama sayısı ifadeleri sonuçlar bölümünün kapsamına indirildi.
- **Son durum:** derleme uyarısı yok; makalenin sayısal iddiaları otomatik denetleyicilerden geçiyor.

**Ertelenen iş:** bütün tablo ve şekillerin tek bir temiz zamanlama oturumuyla yeniden üretilmesi. Bu oturumun ölçümleri hazır, ama geçiş yaklaşık 60 sayıyı değiştiriyor ve 1–2 iş günü sürüyor. Şimdilik üç değeri açıkça anlatmayı ve sonuçların 1.33 ms ile de korunduğunu göstermeyi tercih ettim; hakem isterse revizyonda yapılabilir.

Bütün değişiklikler, eski ve yeni hâlleriyle, revizyon kayıt dosyasında duruyor.

Ayrıca bir öneri: tezde, adım sayısını önceden seçen bir tasarım kuralı ve bunu kullanan bir denetleyici var. Kural, ön kayıtlı 60 koşullu bağımsız sınamada doğru adım sayısına göre medyan %0.08 kaybettiriyor. Uyarlanabilir yöntemi daha da öne çıkarmak isterseniz kısa bir paragraf olarak ekleyebilirim.

Saygılarımla,
Seda Savaşçı Şen

Ekler:
- Latency-Aware_Phase_Optimization_v28.pdf
- supplementary.pdf
