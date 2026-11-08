# Makale Rehberi — "Latency Can Reverse the Ranking"

*Makalenin son hali (9 sayfa) üzerinden, paragraf paragraf, sade Türkçe ile.
Sorular ve tez kurgusu en sonda.*

---

## 0. Makale tek cümlede

> Kullanıcı hareket ederken bir RIS faz yönteminin değeri, sonucu teslim
> ettiği andaki kanalda ne kazandırdığıdır. Bu ölçütle bakıldığında, yavaş ve
> "en iyi" yöntemler hızlı ve basit yöntemlere kaybeder, ve daha fazla
> iterasyon belli bir noktadan sonra zarar verir.

Bir benzetme: Hareket eden bir hedefe fotoğraf makinesiyle odaklanıyorsunuz.
Çok dikkatli odaklanırsanız (uzun süre), deklanşöre bastığınızda hedef çoktan
yer değiştirmiştir ve fotoğraf bulanık çıkar. Biraz daha kaba ama hızlı
odaklanırsanız net bir fotoğraf alırsınız. Makale bu dengeyi RIS için ölçüyor.

---

## 1. Makale, bölüm bölüm

### Başlık
**"Latency Can Reverse the Ranking: Effective-Rate Evaluation of RIS Phase
Optimization for Mobile Users"**
- *Latency can reverse the ranking* = "Gecikme sıralamayı tersine çevirebilir."
  Yani kâğıt üzerinde en iyi olan yöntem, süre hesaba katılınca en kötü
  olabilir.
- *Effective-rate evaluation* = "Etkin hız değerlendirmesi" — makalenin
  önerdiği ölçüt.
- *for Mobile Users* = hareketli kullanıcılar için.

### Yazarlar
Seda Savaşçı Şen (sorumlu yazar, Düzce Ün. Elektrik-Elektronik), Ali Çalhan
(Düzce Ün. Bilgisayar), Murtaza Cicioğlu (Bursa Uludağ Ün. Bilgisayar). AISY
makalenizle aynı ilk üç yazar.

### Özet (Abstract) — cümle cümle
1. *"Yürüyen bir kullanıcı radyo kanalını onlarca milisaniyede değiştirir;
   oysa RIS faz yöntemleri, kendilerine verilen kanalda ulaştıkları hızla
   karşılaştırılır."* → Problemin kendisi: literatürdeki karşılaştırma zamanı
   yok sayıyor.
2. *"Biz her yöntemi, işini bitirdiği andaki kanalda değerlendiriyoruz (etkin
   hız); gecikmeler ölçülüyor; senaryo 3GPP iç mekân ofisi, çok kullanıcılı
   MISO, 32 elemanlı RIS."* → Çözüm ve senaryo.
3. *"Birincisi: koordinat inişi ve uzun Adam, t=0'da en yüksek hızı veren
   yöntemler, 0.9–5.9 saniye sürüyor ve 2.5 ms'lik basit bir tek-kullanıcı
   yöntemine kaybediyor."* → 1. bulgu.
4. *"İkincisi: iterasyon belli bir noktaya kadar işe yarar. 1.5 m/s'de Adam'ın
   etkin hızı 4–6 adımda tepe yapar, 48 adıma kadar sürdürmek %14 kaybettirir;
   10 km/s'de tepe 3 adımdadır."* → 2. bulgu.
5. *"Optimumu, adım süresinin Doppler frekansına oranı belirler; basit bir
   model bu ölçeklenmeyi açıklar."* → 2. bulgunun nedeni.
6. *"Üçüncüsü: eşit adımda Adam'ı geçen öğrenilmiş bir güncelleme kuralı ve
   tek kullanıcıya taşınmış yayımlanmış CNN–LSTM, daha hızlı Adam
   ayarlarınca baskınlanır."* → 3. bulgu (öğrenme).
7. *"Tüm sonuçlar ön kodlayıcının güncel kanaldan yeniden hesaplandığını
   varsayar."* → Ana varsayım, dürüstçe.
8. *"Yaya kullanıcılar ve ölçülen adım maliyeti için, hangi yöntemin en iyi
   olduğuna yakınsama değil gecikme karar verir."* → Ana mesaj, kapsamıyla.

### Anahtar kelimeler
RIS, hareketlilik, hesaplama gecikmesi, etkin hız, kanal eskimesi, derin
açılım (deep unfolding), çok kullanıcılı MISO.

---

### I. Giriş

**1. paragraf — Neden RIS, sorun ne?**
RIS, binanın kör bir köşesini kapsama alanına çevirebilir ve prototiplerle
gösterildi. Ama işe yaraması için sinyali kullanıcının *şu an* bulunduğu yere
yönlendirmesi gerekir, *bulunduğu yere* değil. Fazları seçmek zor (dışbükey
olmayan) bir problem; yinelemeli çözücülerle ve son zamanlarda öğrenmeyle
çözülüyor. Ama hemen hepsi, kendilerine verilen kanaldaki hızla
karşılaştırılıyor.

**2. paragraf — Gizli yarış.**
Yürüyen bir insan kanalı onlarca milisaniyede değiştirir; dikkatli bir çözücü
saniyeler harcar. En iyi cevap hazır olduğunda soru değişmiştir. Zamanında
gelen kaba bir faz, geç gelen mükemmel bir fazı yenebilir; daha fazla
iterasyon sonucu iyileştirmek yerine kötüleştirebilir.

**3. paragraf — Bu makale ne yapıyor?**
Bu yarışı ölçüyor: her yöntemi işini bitirdiği andaki kanalda (etkin hız),
gerçek işlemcide ölçülmüş gecikmeyle değerlendiriyor. Baz istasyonunun
sorusu: *zaman sayılınca hangi yöntemi, ne kadar süre çalıştırmalıyım?*

**Katkılar (5 madde):**
1. Gecikmeyi hesaba katan ölçüt (etkin hız); kâğıt üzerinde en iyi çözücüler
   milisaniyelik bir yönteme kaybediyor.
2. En iyi iterasyon sayısı var; onu tek bir büyüklük belirliyor (adım
   süresi / Doppler); bir model ölçeklenmesini açıklıyor; başka bir klasik
   yöntem, daha büyük yüzey ve standart hızlarda da geçerli.
3. Sürekli çalışmada güncelleme sıklığını pilot yükü belirliyor; her
   güncelleme kısa olmalı.
4. Öğrenme saat karşısında: adım adım kazanan öğrenilmiş kural milisaniye
   başına kaybediyor; AISY'deki CNN–LSTM tek bir Adam adımına yeniliyor.
5. Ana varsayımın (ön kodlayıcının tazelendiği) değeri ölçülüyor.

### II. İlgili Çalışmalar
- **RIS faz optimizasyonu:** Literatürde birçok yöntem var (yarı tanımlı
  gevşetme, blok koordinat inişi, kesirli programlama, manifold, WMMSE).
  Hepsi ulaşılan amaç değerini raporluyor; çalışma süresini en fazla
  karmaşıklık mertebesi (O(N²) gibi) olarak veriyor, koherans süresine göre
  ölçülmüş gecikme olarak değil.
- **Öğrenme:** Pekiştirmeli öğrenme, doğrudan pilotlardan öğrenme, algoritma
  açılımı (deep unfolding), WMMSE'yi taklit eden ağlar. Faz-farkında regresyon
  (sizin AISY makaleniz) ±π süreksizliğini çözüyor. Öğrenme genellikle "hızlı"
  diye öneriliyor, ama bu hız kanalın değişim hızıyla ilişkilendirilmiyor ve
  klasik rakipler aynı koşullarda ayarlanıp zamanlanmıyor.
- **Hareketlilik ve eskimiş kanal:** RIS'i araca takmak, kanal eskimesi
  analizleri, tahmine dayalı ışın yönlendirme, iki zaman ölçekli tasarımlar.
  Hepsinde "kanalı ölçme ile kullanma arasındaki gecikme" sabit bir sistem
  parametresi; yöntemin kendi çalışma süresi modelde yok.
- **Boşluk:** Hiçbir RIS çalışması her yöntemi kendi ölçülmüş bitiş anında
  değerlendirmiyor, en iyi iterasyon sayısını göstermiyor, öğrenme ile klasik
  yöntemi hem eşit adımda hem eşit milisaniyede karşılaştırmıyor.

### III. Sistem ve Kanal Modeli

**A. Sinyal modeli.**
- 8 antenli baz istasyonu (BS), 4 tek antenli kullanıcı, 32 elemanlı RIS
  (8×4). 64 elemanlı RIS de denendi.
- Kullanıcının aldığı sinyal (Denklem 1): doğrudan yol + RIS üzerinden yol.
  RIS yolu = kullanıcı–RIS kanalı × RIS fazları × RIS–BS kanalı.
- Her kullanıcının hızı log₂(1+SINR); SINR = kendi sinyali / (diğer
  kullanıcıların girişimi + gürültü).
- Ön kodlayıcı: düzenlileştirilmiş sıfır-zorlamalı (RZF/MMSE) — standart ve
  güçlü bir seçim.
- Amaç (Denklem 2): **en zayıf kullanıcının hızını en büyütmek** (max-min).
  Bu bir adalet ölçütü.
- Adam ve öğrenilmiş kural bunun yumuşatılmış bir versiyonunu (soft-min)
  kullanıyor, çünkü "min" fonksiyonunun türevi sorunlu.

**B. Geometri ve yayılım (Şekil 1).**
- Oda 40×20×6 m. RIS duvarda (20; 0.1; 3) m, BS (20; 6; 4) m'de, RIS'in tam
  karşısında ve uzak alanında.
- 3 GHz, 20 MHz, 20 dBm.
- Kanal: 3GPP TR 38.901 iç mekân ofis modeli (yol kaybı, LoS olasılığı,
  Rice faktörü, gölgeleme).
- Saçıcılar odadaki noktalardan; doğrudan yola 40 dB ek kayıp (RIS'in
  kullanılma nedeni: doğrudan yol engelli).
- **Şekil 1:** (a) üstten görünüm: BS, RIS, 4 kullanıcı ve yürüyüş okları,
  20 saçıcı; (b) yandan görünüm; (c) RIS ve BS anten dizilimi. Bir koherans
  süresinde kullanıcı yalnızca 42 mm yürüyor.

**C. Hareketlilik.**
- Kullanıcılar 1.5 m/s (5.4 km/s) düz yürüyor, duvardan yansıyor.
- **Neden 1.5 m/s:** 3GPP iç mekân hızı (3 km/s) ile ITU iç mekân hareketlilik
  testi (10 km/s) arasında.
- Saçıcılar sabit; yalnızca kullanıcılar hareket ediyor, kanal her an
  geometriden yeniden hesaplanıyor.
- Doppler frekansı f_d = 15 Hz, koherans süresi T_c = 28.2 ms.

**Sınırlılıklar:** sabit saçıcılar uzun sürede iyimser; anten başına bağımsız
kazançlar tüm hızları iyimser yapıyor; kanal bilgisi kusursuz (bir istisna:
VI-G'de tek kullanıcılı kusurlu kanal testi); dar bant; N=32 için uzak alan.

### IV. Gecikmeyi Hesaba Katan Değerlendirme Çerçevesi

**A. Etkin hız (Tanım 1, Denklem 3).**
Yöntem A, t=0'daki kanalı alıyor, faz θ_A'yı τ_A sürede üretiyor. Etkin hız =
o fazın **τ_A anındaki kanalda** verdiği en düşük kullanıcı hızı. Ön kodlayıcı
o anki kanaldan yeniden hesaplanıyor. (Varsayım: ön kodlayıcı hızlı ve kapalı
form; RIS fazı ise yavaş, yinelemeli.)

**B. Neden en iyi bir adım sayısı var? (Denklem 4)**
L adım çalışan bir yöntem için:
- r₀(L): t=0'daki hız (adımla artar ama giderek daha az).
- Δ(L): kendi çalışma süresi boyunca eskimeden kaybedilen hız (süreyle artar).
- Etkin hız = r₀ − Δ.
Bir adım daha atmak, ancak kazancı (r₀ artışı) ek eskime kaybından büyükse
kârlıdır (Denklem 4). Bu eşitsizliğin bozulduğu yer **içsel optimum L\***.

**C. Eşit adım mı, eşit milisaniye mi? (Tanım 2 — Baskınlık)**
Bir öğrenilmiş adım c klasik adım ediyorsa, eşit adım karşılaştırması
öğrenilmiş yönteme c kat bütçe verir. Bu yüzden eşit zamanda da
karşılaştırıyoruz. **B, A'yı baskınlar:** B hem daha hızlı (ya da eşit) hem
daha iyi (ya da eşit), en az birinde kesin. Baskınlanan bir yöntem **hiçbir
zaman bütçesinde** tercih edilmez.

**D. Normalize adım maliyeti ve küçük gecikme modeli.**
- x = ΔT · f_d (Denklem 5): adım süresi × Doppler. "Bir adımda kullanıcı kaç
  dalga boyu yürüyor?" Adım süresini ölçeklemek, hızı ölçeklemekle aynı şey.
- İki deneysel yasa:
  - Yakınsama boşluğu güç yasasıyla azalıyor: R∞ − r₀(L) ≈ D·L^(−γ) (Denklem 6).
  - Küçük gecikmede eskime kaybı yürünen mesafenin karesiyle artıyor:
    Δ ≈ κ·u² (Denklem 7) — Clarke modelindeki J₀ fonksiyonunun ilk terimi.
- Birleştirince etkin hız (Denklem 8): R∞ − D·L^(−γ) − κ·x²·L².
- **Önerme 1:** Bunun tek bir maksimumu var: L\* ∝ x^(−2/(γ+2)) (Denklem 9).
  Kanıt: türevi sıfıra eşitlemek; ikinci türev negatif.
- Anlamı: hızlı işlemci → daha fazla adım, ama orantılı olarak daha az fazla.
  Model, ölçümü *açıklıyor*; bağımsız tahmin iddiası yok.

**E. Periyodik yeniden optimizasyon (Tanım 3, Denklem 10).**
BS her U ms'de bir: T_p süre pilot gönderir (veri yok), L adım optimize eder,
fazı yükler. Ölçüt: zaman ortalamalı etkin hız (pilot süreleri hariç).
Soğuk başlangıç (sıfırdan) ya da sıcak başlangıç (mevcut fazdan).

### V. Ölçüm Protokolü
- **Senaryo kümeleri:** Eskime kümesi (400 senaryo, 20 saçıcı; N=64
  versiyonu); ışın kümesi (400, 6 saçıcı); statik küme (6000; eğitim 4200,
  doğrulama 400, test 600); tek kullanıcı kümesi (400; CNN için 40 000'lik
  ayrı eğitim çekilişi, seçim için ayrı 400, sağlamlık için iki 6000'lik).
  Veri üreteci "önek-kararlı" değil, bu yüzden her model eğitildiği örnek
  sayısıyla değerlendiriliyor.
- **Yöntemler:** SU-average ve SU-best-of (kapalı form tek kullanıcı
  hizalaması), Adam, Armijo (adım boyu arayan dik iniş), koordinat inişi (her
  eleman için 16 seviye, 8 tarama), uzun Adam (1000 iterasyon, 3 başlangıç),
  öğrenilmiş güncelleme (derin açılım ağı).
- **Ayar:** Klasik yöntemlerin adım boyu her bütçede doğrulama kümesinde
  seçildi (zayıf rakip hatasına düşmemek için).
- **Zamanlama:** Tek Xeon çekirdeği, Python. Adam adımı 1.66 ms (önceki bir
  ölçümden, şimdiki ölçüm aralığında). Yük değerleri ve turlar arası yayılım
  raporlanıyor.
- **İstatistik:** Senaryolar arası fark büyük olduğundan eşleştirilmiş
  bootstrap (aynı senaryoda iki yöntemin farkı), %95 güven aralığı.
- **Pilotlar:** 4 kullanıcı için 48 pilot sembolü yeterli; 15/30/60 kHz alt
  taşıyıcıda 3.43/1.71/0.86 ms.
- **Yeniden üretilebilirlik:** Tek bir betik bütün tablo ve şekilleri üretiyor;
  denetim betiği 99 iddiayı sınıyor.

### VI. Sonuçlar

**A. Yavaş, güçlü çözücüler hızlı bir yönteme kaybeder.**
- RIS sinyalin çoğunu taşıyor: doğrudan yol 20.0 dB, RIS üzerinden 31.1 dB
  SNR. RIS yokken en zayıf kullanıcı 1.744 b/s/Hz; rastgele fazla 4.072.
- **Şekil 2:** Faz t=0'da sabitlenip kullanıcılar yürürken izleniyor. Hız ilk
  birkaç ms sabit, T_c civarında sert düşüyor, sonra "bayat taban" üstünde
  duruyor. Ne kadar iyi optimize edilmişse o kadar çok kaybediyor: uzun Adam
  7.117 → 5.473; SU-average 4.624 → 4.503.
- **Tablo I:** Her yöntem kendi gecikmesinde. Uzun Adam (5.9 s) ve koordinat
  inişi (0.88 s) t=0'da en iyi; ama etkin hızları (iyimser haliyle bile)
  2.5 ms'lik SU-best-of'un altında: fark 0.297 ve 0.604 b/s/Hz, güven
  aralıkları sıfırın üstünde.

**B. Birkaç adımdan sonra daha fazla iterasyon işe yaramaz.**
- **Şekil 3:** Adam'ın t=0 hızı her adımda artıyor (L=1'de 5.412, L=48'de
  7.037). Etkin hız ise 4–6 adımda tepe yapıyor (≈5.98); diğer her adım
  sayısı anlamlı olarak düşük. 48 adımda %14.0 daha düşük, oysa t=0 hızı
  %13.2 daha yüksek.
- Denklem 4 ile: 4'ten 6'ya geçmek 0.188 kazandırıyor ama eskime 0.198
  kaybettiriyor.
- Optimum Adam'a ya da adım boyuna özgü değil: farklı adım boylarında 4–6;
  Armijo'da da 4. Armijo adım başına 1.26 kat pahalı ve Adam'la istatistiksel
  berabere; maliyet oranı değiştikçe sıralama değişiyor → **iki klasik yöntem
  arasında bile sıralamayı gecikme belirliyor.**

**C. Optimumu tek bir sayı belirler.**
- **Şekil 4:** Adam'ın adım süresi 0.01× ile 3× arasında ölçekleniyor (x
  ekseni). En iyi adım sayısı düzenli düşüyor: 96 → 48 → 24–32 → 12–16 →
  4–6 (bizim nokta) → 2.
- Çok hızlı işlemcide (küçük x) yakınsamak neredeyse bedava (%1.5); bedel
  x ≈ 2.5×10⁻³ civarında %21 ile tepe yapıyor. Yani "yakınsamak zararlı"
  rejime bağlı bir ifade.
- GPU/NPU optimumu kaydırır ama kaldırmaz; ölçümde 100 kat hızlı adımda bile
  96 adımda iç optimum var.
- Model kontrolü: eskime karesel (R² ≥ 0.98); güç yasası yaklaşık (γ = 0.93,
  aralık 0.56–1.19); öngörülen üs −0.78 ile −0.63 arası; ölçülen −0.675
  (aralığın içinde). Kapalı form ölçülenin 1.27 katı içinde. Örneklem içi
  kontrol olduğu ve dengenin tutmadığı açıkça yazılı.
- 64 elemanlı RIS: daha yüksek hız (8.48 vs 7.10) ama aynı en iyi adım
  sayısı.

**D. Standart hızlar ve kanal edinim gecikmesi.**
- **Tablo II:** 3, 5.4, 10, 18, 30 km/s. Optimum: 8, 4, 3, 2, 1 adım. 48
  adımın bedeli: %14.5, %14.2, %10.5, %8.0†, %4.3† († güvenilir ufkun
  dışında). Hızlı yöntem CD'yi her hızda 0.25–0.42, uzun Adam'ı 0.45–0.69
  geçiyor.
- Dürüst sınır: 18 ve 30 km/s'de ek gecikme eklenince optimum
  belirlenemiyor.
- 0–10 ms kanal edinim gecikmesi optimumu az adıma kaydırıyor (1.5 m/s'de
  4–6 → 3–4). Hız tahmini yanlış olsa bile kayıp küçük (≤%0.5, en kötü %5.7).

**E. Periyodik çalışma: periyodu pilotlar belirler, güncellemeler kısa kalır.**
- **Tablo III:** Pilot bedavaysa arka arkaya 2 sıcak adım en iyi (6.36);
  0.86 ms pilotta 10–20 ms periyot; 3.43 ms pilotta 80 ms. Her durumda en fazla
  8 adımlık bir politika en iyiden anlamlı olarak kötü değil. Sıcak başlangıç
  0.52 b/s/Hz'e kadar kazandırıyor.

**F. Öğrenilmiş kural adım başına kazanır, milisaniye başına kaybeder.**
- **Şekil 5:** (a) Eşit adımda öğrenilmiş kural her bütçede ayarlı Adam'dan
  iyi (senaryoların %68–84'ünde). (b) Ama bir öğrenilmiş adım 2.7–4.0 Adam
  adımı ediyor; ölçülen zaman ekseninde her öğrenilmiş ayarı, daha hızlı ve
  daha iyi bir Adam ayarı baskınlıyor (5 ölçüm turunun hepsinde). Örnek:
  öğrenilmiş L=4 → 18.41 ms, 5.285; Adam L=8 → 13.48 ms, 5.380.
- Çekince: tek CPU çekirdeğinde ölçüldü; GPU'da oran değişebilir.

**G. Yayımlanmış faz tahmincisini tek bir gradyan adımı yener (sizin
modeliniz).**
- AISY'deki CNN–LSTM (sin/cos çıkışlı) aynı mimari ve eğitim reçetesiyle,
  çok antenli (8) tek kullanıcı senaryosuna taşındı. Ortak faz sorunu
  çözüldü (1. eleman sıfır, ortak faz kapalı formla geri konuyor).
- Statik test: faz hatası 61.32°, hız 12.490 (kapalı form 12.431, optimum
  12.893 arasında). Kontrol: tek antende 14.99° (sizin makalenizdeki 2.77°
  farklı bir veri üreteciyle; doğrudan karşılaştırılamaz).
- **Tablo IV:** Tek Adam adımı 0.59 ms'de, CNN 1.12 ms'de; Adam 0.143
  b/s/Hz daha iyi (büyük çekilişlerde 0.090 ve 0.104) → CNN baskınlanıyor.
  En iyi yöntem 1 CD taraması. Kusurlu kanal bilgisinde (hata gücü %1–30)
  gürültüyle eğitilmiş model de klasik yöntemin 0.42–0.65 altında.
- Neden: çok antende her elemanın en iyi fazı diğerlerinin oluşturduğu
  hüzmeye bağlı; ağ bu bağlaşımın küçük bir kısmını yakalıyor.

**H. Taze ışın varsayımı önemli.**
Ön kodlayıcı t=0'dakinde bırakılırsa hız onlarca milisaniyede çöküyor (T_c'de
11.7–14.2 kat düşük; 5 ms'lik ön kodlayıcı bile 5.228 → 1.736). Tazelemek
ucuz (0.12 ms) ama birkaç ms'de bir pilot gerektiriyor; bu pilotların süresi
hesaba katılmadı.

### VII. Sonuç
"BS hangi yöntemi, ne kadar süre çalıştırmalı?" sorusuna 5 cevap:
1. Hız hassasiyeti yener (3–30 km/s, ek gecikme yokken).
2. Birkaç adım en iyisi (1.5 m/s'de 4–6; 10 km/s'de 3).
3. Optimumu tek sayı (x) belirler; yaklaşık x^(−2/(γ+2)).
4. Güncelleme periyodunu pilotlar belirler.
5. Öğrenme saat karşısında kazanmak zorunda; iki öğrenme yöntemi de
   baskınlanıyor.

**Pratik kurallar:** adım sayısını x'ten ve gecikmeden seç; periyodu pilot
yükünden seç; yöntemleri ölçülmüş gecikmeyle, her bütçede ayarlı klasik
rakiple karşılaştır.
**Sınırlılıklar:** sabit saçıcılar, taze ön kodlayıcı varsayımı, Python/tek
çekirdek, sabit bütçeli yavaş yöntemler, tek kullanıcılı CNN testi.
**Sonraki adım:** geniş bant OFDM (beam squint), sonra çok kullanıcılı kusurlu
kanal ve ayrık faz.

### Teşekkür ve veri/kod
Yapay zekâ beyanı (seçenek B, iş birliği vurgulu) ve açık kod deposu:
github.com/sedasavascisen/ris-latency-mobility.

---

## 2. Terimler sözlüğü

| Terim | Anlamı |
|---|---|
| **Etkin hız (effective rate)** | Yöntemin fazının, yöntem bittiği andaki kanalda verdiği hız |
| **Koherans süresi T_c** | Kanalın "aynı kaldığı" süre; burada 28.2 ms |
| **Doppler frekansı f_d** | Hareketin kanalı değiştirme hızı; v·f_c/c = 15 Hz |
| **x = ΔT·f_d** | Bir adımda kullanıcının kaç dalga boyu yürüdüğü; optimumu belirleyen sayı |
| **L\* (içsel optimum)** | Etkin hızı en yüksek yapan adım sayısı |
| **Adam** | Uyarlamalı adım boyu kullanan gradyan yöntemi |
| **Koordinat inişi (CD)** | Fazları teker teker, diğerleri sabitken en iyiye ayarlama |
| **SU-average / SU-best-of** | Kapalı form, her kullanıcı için tek tek hizalamaya dayalı hızlı yöntemler |
| **RZF / MMSE ön kodlayıcı** | BS'nin kullanıcılar arası girişimi bastıran hüzme |
| **max-min (en zayıf kullanıcı)** | Amaç: en kötü durumdaki kullanıcının hızını büyütmek |
| **soft-min** | max-min'in türevlenebilir yaklaşığı |
| **Baskınlık (dominance)** | Hem daha hızlı hem daha iyi olmak |
| **Eşleştirilmiş bootstrap / %95 GA** | Aynı senaryoda iki yöntemin farkının güven aralığı |
| **Bayat taban (stale floor)** | Fazı tamamen bağımsız bir kanalda kullanmanın verdiği hız |
| **T_ov / T_p** | Kanal edinim gecikmesi / pilot süresi |
| **Sıcak / soğuk başlangıç** | Mevcut fazdan / sıfırdan başlamak |
| **Derin açılım (deep unfolding)** | Bir algoritmanın iterasyonlarını ağ katmanlarına çevirmek |

---

## 3. Olası sorular ve cevaplar

### Danışman / jüri soruları

**S1. Neden 1.5 m/s? Çok yavaş değil mi?**
C: 3GPP iç mekân değerlendirmesi 3 km/s (0.83 m/s), ITU iç mekân hareketlilik
testi 10 km/s (2.78 m/s) kullanıyor; 1.5 m/s arasında. Ayrıca 3, 10, 18 (5 m/s)
ve 30 km/s'de tekrarladık (Tablo II); bulgular her hızda geçerli. Hız arttıkça
optimum adım sayısı azalıyor, yani sonuç güçleniyor.

**S2. Gecikmeler Python'da ölçülmüş; C ya da GPU'da her şey değişmez mi?**
C: Değişen tek şey x (adım süresi × Doppler). Şekil 4 x'i 100 kat küçültüp 3
kat büyütüyor; her noktada optimum var. Daha hızlı donanım optimumu daha çok
adıma kaydırır ama ortadan kaldırmaz. Öğrenme–klasik karşılaştırmasında
donanım oranı değiştirebilir; bu açıkça sınırlılık olarak yazılı.

**S3. Neden SDR, WMMSE gibi yöntemler yok?**
C: Onlar koordinat inişinden ve uzun Adam'dan daha da yavaş; zamanlansalardı
aynı sonuca daha güçlü düşerlerdi. Zamanlanmadıkları sınırlılıklarda yazılı.

**S4. Kanal modeli gerçekçi mi?**
C: 3GPP TR 38.901 iç mekân ofis modeli: yol kaybı, LoS olasılığı, Rice
faktörü, gölgeleme. Sabit saçıcılar uzun süreli sonuçları iyimser yapıyor; bu
yavaş yöntemlerin lehine, yani sonuç muhafazakâr.

**S5. Ön kodlayıcının her an tazelendiği varsayımı gerçekçi mi?**
C: En büyük varsayım bu, ve makalede ölçüldü (VI-H): tazelenmezse hız çöküyor.
Tazelemek 0.12 ms sürüyor ama pilot gerektiriyor; pilot süresi hesaba
katılmadı. Bu, modern bir BS'nin çerçeve çerçeve yaptığı şey.

**S6. Kendi CNN–LSTM modeliniz neden kaybetti? AISY makaleniz yanlış mıydı?**
C: Hayır. AISY tek antenli, statik bir senaryoda faz doğruluğunu ölçtü; orada
optimum faz eleman başına kapalı formda. Çok antende her elemanın fazı diğer
elemanlara bağlanıyor ve problem zorlaşıyor. Ayrıca gecikme hesaba
katıldığında tek bir Adam adımı daha hızlı. Sin/cos gösteriminin katkısı ise
çok antende de geçerli (tezde gösterdik: doğrudan açı tahmininden her denemede
iyi).

**S7. 2.77° sonucunu neden burada elde edemediniz?**
C: Veri üreteci farklı (AISY'de Rayleigh + 6 saçıcı, burada 3GPP geometrisi
ve LoS). Mutlak hatalar iki çalışma arasında karşılaştırılamaz; makalede
açıkça yazılı.

**S8. "Etkin hız" yeni mi? Literatürde kanal eskimesi zaten yok mu?**
C: Eskime analizleri var, ama hepsinde gecikme sabit bir sistem parametresi.
Yenilik: gecikmenin yöntemden yönteme ve iterasyon sayısına göre değiştiğini
modele katmak ve ölçmek.

**S9. Önerme 1 gerçekten bir teori mi, yoksa eğri uydurma mı?**
C: Matematiksel olarak doğru bir sonuç (model içinde tek maksimum ve kapalı
form). Ama sabitleri ölçümden uydurulduğu için makale onu bağımsız bir tahmin
olarak değil, "optimumun neden böyle kaydığını açıklayan" bir model olarak
sunuyor. Ölçülen üs modelin aralığında.

**S10. 400 senaryo yeterli mi?**
C: Eşleştirilmiş bootstrap ile farkların güven aralıkları dar; ana farklar
anlamlı. CNN karşılaştırması 6000'lik iki ek çekilişle de doğrulandı.

**S11. Yapay zekâ kullanımı?**
C: Beyanda açıkça yazılı: metin taslağı, Python'a aktarım, betikler (sizinle iş
birliği içinde), şekiller, kaynak kontrolü. Tasarım, deney kararları ve yorum
sizde; her sayı betikten üretiliyor, kod açık.

### Hakem soruları (olası)

**S12. Neden max-min amaç? Toplam hız olsaydı?**
C: Adalet ölçütü, literatürde RIS–MISO için kullanılıyor. Etkin hız fikri
amaçtan bağımsız; toplam hızla da aynı mekanizma (kazanç vs eskime) işler.
(Gelecek çalışma olarak söylenebilir.)

**S13. İki zaman ölçekli tasarımlarla karşılaştırma?**
C: İlgili çalışmalarda tartışılıyor. Bizim çerçevemiz onları da kapsayabilir:
istatistiğe dayalı faz yavaş eskir, ama anlık optimuma ulaşamaz.

**S14. Pilot sayısı (48) neye dayanıyor?**
C: Wang vd. 2020 TWC'deki kaskat kanal kestirim şeması; K=4, N=32, N_t=8 için
48 sembol. Geri besleme ve işlem süresi dahil değil; bu yüzden gerçek gecikme
daha uzun, sonuç daha da güçlü.

**S15. Öğrenilmiş kural yaşlanma kümesinde neden test edilmedi?**
C: Karşılaştırma statik kümede, saf hesaplama verimliliğini izole etmek için
yapıldı. Öğrenilmiş ayar her çiftte daha yavaş olduğundan, eskime farkı
büyütür (beklenti; ölçülmedi, makalede yazılı).

**S16. N büyüdükçe ne olur?**
C: N=64'te aynı optimum. Bizim kodda adım maliyeti N'ye neredeyse bağlı değil
(1.04 kat); maliyeti N ile büyüyen bir uygulamada optimum daha az adıma kayar.

---

## 4. Tezin kurgusu

### Tezin ana fikri (savunu cümlesi)
> *Hesaplama gecikmesi, hareketli RIS sistemlerinde ikincil bir ölçüt değil,
> yöntem sıralamasını belirleyen birinci sınıf bir tasarım kısıtıdır.
> Faz-farkında gösterim öğrenmeyi iyileştirir; ama gecikme hesaba
> katıldığında klasik yöntemler önde kalır.*

### Önerilen başlık
**"Yeniden Yapılandırılabilir Akıllı Yüzeylerde Faz Tasarımı: Faz-Farkında
Derin Öğrenme ve Hesaplama Gecikmesinin Rolü"**

### Bölüm planı

| Bölüm | İçerik | Kaynak |
|---|---|---|
| 1. Giriş | RIS, faz problemi, iki zorluk: ±π süreksizliği ve gecikme; tezin katkıları; yayınlar | Yeni yazılacak |
| 2. Temel bilgiler ve literatür | RIS kanal modelleri, faz optimizasyonu, öğrenme, hareketlilik | İki makalenin literatür bölümleri |
| 3. **Faz-farkında öğrenme (tek anten, statik)** | sin/cos gösterimi, kanıtlar, CNN–LSTM, sonuçlar | **AISY makalesi (yayımlandı)** |
| 4. **Faz-farkında öğrenmenin çok antene genişletilmesi** | Ortak faz sorunu, sin/cos vs açı (61.5° vs 73.8°, ±π'de 122.7°), elemanlar arası bağlaşım | Tez deneyleri (`TEZ_YAZIM_REFERANSI.md` 6.1, 6.4) |
| 5. **Gecikme ve hareketlilik: etkin hız** | Çerçeve, içsel optimum, ölçekleme yasası, standart hızlar, periyodik çalışma, öğrenme vs klasik | **Bu makale (TWC'ye gönderilecek)** |
| 6. **Gerçekçi koşullar** | Kusurlu CSI, ayrık faz (1/2/3 bit), konumdan faz tahmini (radyo haritası) | Tez deneyleri (6.3, 6.5, 6.6) |
| 7. Sonuç ve gelecek çalışma | Katkılar, sınırlar, geniş bant OFDM, çok kullanıcı | Yeni yazılacak |

### AISY makalesini (ilk yayın) nasıl kurgulamalı?
- **3. bölümün çekirdeği.** Makaleyi olduğu gibi kopyalamayın; teze uygun
  genişletilmiş bir anlatım yapın: problemin motivasyonu, sin/cos'un
  matematiksel gerekçesi, deneyler, tartışma.
- **Bölüm sonunda köprü cümlesi:** *"Bu bölüm tek antenli, statik bir
  senaryoda faz-farkında öğrenmenin süreksizliği çözdüğünü gösterdi. İki soru
  açık kaldı: (1) çok antende geçerli mi, (2) kullanıcı hareket ederken
  hesaplama süresi hesaba katılınca ne olur? 4. ve 5. bölümler bunları
  cevaplıyor."*
- Böylece ilk yayın tezin **başlangıç noktası**, sonraki bölümler onun
  **doğal devamı** olur.

### Bu makaleyi (ikinci yayın) nasıl kurgulamalı?
- **5. bölüm, tezin omurgası.** Makalenin 9 sayfası tezde 25–35 sayfaya
  genişler: kısaltılan ayrıntılar (çıkarılan tablolar, ölçüm tuzakları eki,
  zamanlama ayrıntıları, Armijo ve model kontrolleri) burada yer alır.
- Bölüm girişinde 3. ve 4. bölüme bağlanın: *"Faz-farkında model doğru fazı
  öğrenebiliyor; ama hareketli kullanıcıda doğru faz yetmez, zamanında da
  gelmelidir."*

### Sonuç bölümünü nasıl yazmalı?
**1. Katkılar listesi:**
1. Faz-farkında regresyon ile ±π süreksizliğinin çözümü (AISY, yayımlandı).
2. Bu gösterimin çok antende de doğrudan açı tahmininden üstün olduğu.
3. Gecikmeyi hesaba katan etkin hız ölçütü ve içsel optimum (TWC'ye gönderildi).
4. Optimumun normalize adım maliyetiyle ölçeklenmesi ve küçük gecikme modeli.
5. Öğrenme ile klasik yöntemlerin eşit milisaniyede karşılaştırılmasının
   gerekliliği; kusurlu CSI, ayrık faz ve konum tabanlı tasarımda sistematik
   değerlendirme.

**2. Dürüst değerlendirme paragrafı:**
*"Öğrenme, faz gösteriminde gerçek bir kazanç sağladı; ancak gecikme ve
maliyet hesaba katıldığında incelenen hiçbir senaryoda klasik ya da eğitimsiz
yöntemlerin önüne geçemedi. Bu, olumsuz ama titizlikle gösterilmiş bir
sonuçtur: öğrenme tabanlı RIS yöntemleri milisaniye ekseninde ve ayarlı
klasik rakiplere karşı değerlendirilmelidir."*

**3. Gelecek çalışma:** geniş bant OFDM ve beam squint; çok kullanıcılı
kusurlu kanal ve ayrık faz; öngörücü faz tasarımı (dönüşlü yörüngelerle);
donanımda (GPU/FPGA) gecikme ölçümü; gerçek ölçüm verisiyle doğrulama.

### Yazım sırası (önerilen)
1. **5. bölüm** (makale hazır, genişletmek kolay) → 1 hafta
2. **4. ve 6. bölüm** (sonuçlar `TEZ_YAZIM_REFERANSI.md`'de hazır) → 1.5 hafta
3. **3. bölüm** (AISY'den uyarlama) → 1 hafta
4. **2. bölüm** (literatür) → 1 hafta
5. **1. ve 7. bölüm** (en son; ne iddia ettiğinizi artık biliyorsunuz) → 1 hafta

### Savunma sunumunun akışı (öneri, ~30 dk)
1. Problem: hareket eden kullanıcı ve RIS (2 slayt)
2. ±π süreksizliği ve sin/cos çözümü (AISY) (4 slayt)
3. Çok antene genişleme: gösterim üstün, bağlaşım zor (3 slayt)
4. Etkin hız: gizli yarış, içsel optimum, x yasası, standart hızlar (6 slayt)
5. Öğrenme saat karşısında (3 slayt)
6. Gerçekçi koşullar: kusurlu CSI, ayrık faz, konum (3 slayt)
7. Sonuç: katkılar, sınırlar, gelecek (2 slayt)
