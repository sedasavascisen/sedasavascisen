**Konu:** Tez durum raporu ve IEEE TWC makale gönderimi

Sayın Hocam,

Tezimin son durumunu, IEEE Transactions on Wireless Communications'a
göndermeye hazırladığım makaleyi ve önümüzdeki haftaların planını kısaca
özetlemek istiyorum. Ekte makalenin son halini ve kısa bir sunum
bulabilirsiniz.

**1. Tezin ana fikri.** Hareketli kullanıcılarda RIS faz optimizasyonu
yöntemlerini, işlerini bitirdikleri andaki kanalda değerlendiriyorum
("etkin hız"). Gecikmeleri gerçek işlemcide ölçüyorum. Savunu cümlem şu:
hesaplama gecikmesi ikincil bir ölçüt değil, yöntem sıralamasını
belirleyen birinci sınıf bir tasarım kısıtıdır.

**2. Hareketlilik ekseni (olumlu sonuç, tezin omurgası).**
- **Hızlı yöntem kazanıyor:** 0.9–5.9 s süren güçlü çözücüler, 2.5 ms'lik
  basit bir yönteme 3–30 km/h aralığının her hızında kaybediyor.
- **Az adım yeterli:** 1.5 m/s'de en iyi Adam adım sayısı 4–6. 48 adım
  koşmak etkin hızın %14.0'ına mal oluyor. ITU'nun kapalı alan hızı olan
  10 km/h'te en iyi adım sayısı 3.
- **Tek bir sayı belirleyici:** en iyi adım sayısını, adım süresi ile
  Doppler frekansının çarpımı belirliyor. Basit bir model bu ilişkiyi
  açıklıyor.
- **Sağlamlık:** 3GPP ve ITU standart hızlarında, koordinat inişinin
  tarama sayısı ayarlandığında ve fiziksel olarak doğru kanal modeli
  kullanıldığında sonuçlar değişmiyor.

**3. Makale.** Yeni başlık: *"Latency-Aware Phase Optimization for
Reconfigurable Intelligent Surfaces Serving Mobile Users"*.
- Makale 9 sayfa. Her sayısı bir betikten üretiliyor; kod ve veriler açık
  depoda yer alacak.
- CNN–LSTM bölümünü makaleden çıkarıp teze taşıdım. Böylece makale
  yalnızca gecikme çerçevesine odaklanıyor.
- Göndermeden önce makaleyi dört kez editör gözüyle satır satır okuttum,
  48 kaynağın her birini orijinal metinle tek tek doğruladım ve TWC'nin
  güncel yazar kurallarına göre kontrol listesinden geçirdim.
- Uygun görürseniz bu hafta göndermeyi planlıyorum.

**4. Öğrenme ekseni (titiz olumsuz sonuç).** Öğrenilen yöntemleri,
doğrulama kümesinde en iyi ayarıyla seçilen klasik rakiplerle eşit
milisaniyede karşılaştırdım. Öğrenilen güncelleme kuralı, CNN–LSTM,
kusurlu kanal bilgisi, ayrık faz ve az pilot (ön kayıtlı deney)
senaryolarının hepsinde klasik rakip önde. Buna karşılık AISY makalemdeki
sin/cos gösterimi, doğrudan açı tahminini her deneyde ve her tohumda
geçiyor. Bu katkı yeni problemlerde bağımsız olarak doğrulanmış oldu.

**5. AISY çalışmasının yeniden üretimi.** Tez için AISY makalesinin MATLAB
kodlarını beş adımlı temiz bir pakette topladım.
- Baseline karşılaştırma şeklini (iterasyon sayısına göre CD) okunaklı
  hale getirdim: iki panel, logaritmik gecikme ekseni, başlık altyazıda.
- Tezde bu karşılaştırmayı aynı test kümesinde ve aynı koşulda ölçerek
  sunacağım.

**6. Takvim.**
- Ölçüm fazını 20 Kasım'da kapatıyorum; bu tarihten sonra yeni deney
  açmayacağım.
- Ardından yazıma geçiyorum, yaklaşık haftada bir bölüm. Bölümler: giriş;
  AISY ve sin/cos; hareketlilik; öğrenme ekseni; gerçekçi senaryo; sonuç
  ve gelecek çalışma.

**Görüşünüzü almak istediğim konular:**
1. Makalenin başlığı ve bu haliyle TWC'ye gönderilmesi.
2. Öğrenme ekseninin tezde olumsuz sonuç olarak yazılması.
3. Bölüm yapısı ve takvim.
4. Jürinin sorabileceği konular.

Uygun olduğunuz bir zamanda kısa bir görüşme yapabilirsek çok sevinirim.

Saygılarımla,
Seda Savaşçı Şen
