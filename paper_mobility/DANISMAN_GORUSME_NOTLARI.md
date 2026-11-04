# Danışman görüşmesi — mobilite makalesi

Makale: *Latency Can Reverse the Ranking: Effective-Rate Evaluation of RIS
Phase Optimization for Mobile Users* (11 sayfa, IEEE TWC formatı).
Tüm sayılar `paper_mobility/paper_numbers.txt` içinde, betiklerden üretildi.

---

## 1. Açılış (1 dakika)

"Hocam, mobilite bölümünü bir dergi makalesine dönüştürdüm. Tek cümlelik
mesajı şu: hareketli kullanıcıda bir yöntemi, hesabını bitirdiği anda var
olan kanalda değerlendirmek gerekir, ve böyle değerlendirince yöntem
sıralaması değişebilir. Ne zaman değiştiğini de tek bir boyutsuz sayı
belirliyor: adım süresi çarpı Doppler frekansı."

## 2. Ana bulgular (5 dakika, sayılarla)

Senaryo: 3GPP InH-Office, 32 elemanlı RIS, 8 antenli BS, 4 kullanıcı,
1.5 m/s, 3 GHz, T_c = 28.2 ms.

1. **Yavaş ama en iyi yöntemler kaybediyor.** t=0'da en yüksek hızı veren
   uzun Adam koşusu (7.117) 5.9 s, koordinat inişi 0.88 s sürüyor. Etkin
   hızları, 2.5 ms süren SU-best-of'un altında kalıyor. Fark eşleştirilmiş
   testte 0.30 ve 0.60 b/s/Hz, ikisi de anlamlı.
2. **İçsel optimum.** Adam'ın etkin hızı 4–6 adımda tepe yapıyor (5.98).
   48 adım %14.0 kaybettiriyor (%95 GA 12.5–15.5), oysa t=0 hızı %13 daha
   yüksek. Optimum adım boyundan bağımsız ve Armijo'da da var.
3. **Ölçekleme yasası (en önemli yeni katkı).** Optimum x = ΔT·f_d ile
   belirleniyor. x 2.5·10⁻⁴'ten 7.5·10⁻²'ye çıkınca L* 96'dan 2'ye iniyor.
   100 kat hızlı bir uygulamada yakınsamanın bedeli %1.5. Yani "yakınsamak
   zararlı" bir yasa değil, bir rejim sonucu, ve rejimi ölçtük.
4. **Periyodik çalışma.** Pilot süresi veri iletiminden düşülünce güncelleme
   periyodunu pilot maliyeti belirliyor (arka arkaya ile 80 ms arası). Her
   güncellemede yine az adım (warm start ile 2–8) yeterli.
5. **Öğrenilen ve klasik yöntem.** Hareketsiz kümede, eşit adım sayısında
   öğrenilen kural 5/5 kazanıyor. Ölçülen milisaniye ekseninde 5/5
   baskınlanıyor. Bir öğrenilen adım 2.7–4.0 Adam adımı ediyor.
6. **Hüzme varsayımının bedeli.** Ön kodlayıcı fazla birlikte eskiseydi,
   T_c'deki hız 11.7–14.2 kat düşük olurdu. Ön kodlayıcıyı yenilemek bir
   Adam adımından yaklaşık 13 kat ucuz.

## 3. Açıkça söylemem gerekenler (dürüstlük)

- **Önceki taslaklardaki hatalar.** Makalenin ilk taslakları bir yapay
  zeka asistanıyla yazıldı ve ciddi hatalar içeriyordu: 23 kaynağın 14'ü
  uydurmaydı, birkaç sayı ve sistem modeli koda uymuyordu, teorem
  ispatları hatalıydı. Hepsi kaldırıldı. Şu an her kaynak Crossref'te, her
  sayı betikte doğrulanmış durumda, ve iki ayrı bağımsız denetimden geçti.
  Hocaya önceki bir taslak gösterildiyse, ondaki "L*≈8", "17 kat",
  "Lemma/Teorem" gibi ifadelerin geçersiz olduğunu söylemeliyim.
- **Tez referansında güncellenmesi gereken satırlar.**
  `TEZ_YAZIM_REFERANSI.md` içinde SU-best-of 0.05 ms, koordinat inişi
  ~1500 ms, "PGA" ~5600 ms yazıyor. Bu satırlar elle yazılmış, betikle
  üretilmemiş. Ölçülen değerler 2.5 ms, 0.88 s ve 5.9 s. Ayrıca "PGA" adlı
  yöntem aslında 3 başlangıçlı ve 1000 adımlı Adam. Tezde adı ve sayılar
  düzeltilmeli.
- **Sonuçların değiştiği yerler.** Bağımsız denetim pilot süresinin bedava
  sayıldığını gösterdi. Düzeltince "her zaman çok sık güncelle" önerisi
  "periyodu pilot belirler, adım sayısı az kalır" haline geldi. Armijo
  ayarlanınca "Adam açık ara iyi" sonucu "berabere, sıralama orana bağlı"
  oldu.

## 4. Hakemlerin saldıracağı noktalar ve cevaplarım

| Muhtemel itiraz | Cevabım |
|---|---|
| "Gecikmeler Python'a bağlı." | Evet, o yüzden sonuçları x = ΔT·f_d ile verdik. Hangi donanımda olursa olsun okunabilir |
| "Öğrenilen yöntem hareketli kümede denenmedi." | Doğru. Ağırlık arşiviyle yapılabilir, 20 Kasım'a kadar eklenebilir |
| "SDR/WMMSE yok." | Doğru, ölçmedik ve sınırlılık olarak yazdık. Klasik yöntemler arasında bile sıralamanın adım maliyetine bağlı olduğunu Adam–Armijo karşılaştırması gösteriyor |
| "Tek senaryo, N=32, 3 GHz." | x ile hız ve adım süresi kesin, frekans yaklaşık olarak genellenir. N ölçekleme yok |
| "Kanal modeli iyimser." | İki yanlılık açıkça yazılı. Dondurulmuş saçıcılar yavaş yöntemlerin lehine, yani onlar aleyhine olan sonucumuz muhafazakâr. Anten başına bağımsız kazançlar ise tüm hızları iyimser yapıyor |
| "Kusursuz CSI." | Edinme gecikmesi ve pilot maliyeti eklendi. Gürültülü CSI tezde Görev 2 |
| "İç optimum sezgisel." | Katkı varlığı değil, nicel haritası: x'e göre ölçekleme ve pilot maliyetiyle etkileşim |

## 5. Hocaya soracağım kararlar

1. **Dergi.** IEEE TWC mi (11 sayfa, ama kapsam itirazı riski var), yoksa
   daha odaklı bir kısa versiyonla IEEE Wireless Communications Letters
   mı? TVT de seçenek.
2. **Yazarlar ve sıra.** Hoca ortak yazar olacak mı? Başka katkı yapan var
   mı? Fon ve teşekkür metni ne olacak?
3. **20 Kasım'a kadar hangi ölçümler?**
   - Öğrenilen modeli hareketli kümede değerlendirmek (ağırlık arşivi gerekli)
   - Eşit-milisaniye zamanlamasını yük kaydıyla tekrarlamak
     (`scripts/mumiso_latency_replicate.py`)
   - Kusurlu CSI (tez Görev 2) ve ayrık faz (tez Görev 3): bu makaleye mi,
     tezin ayrı bölümüne mi?
4. **Kod ve veri.** Depo makaleyle birlikte açık mı olacak (veri erişimi
   bölümü buna göre doldurulacak)?
5. **Tez senkronizasyonu.** Tezin mobilite bölümünü makalenin sayılarıyla
   güncellememi onaylıyor mu?

## 6. Hocanın sorabileceği kısa sorular

- **"x nedir, neden önemli?"** Adım süresinin, kanalın değişme süresine
  oranı. Kanal kullanıcının dalga boyu cinsinden yer değiştirmesiyle
  değiştiği için, 10 kat hızlı bir kod 10 kat yavaş bir kullanıcıyla aynı
  sonucu verir.
- **"Neden tek bir L* değil de 4–6?"** Tepe düz. Aradaki farklar
  ara değer bulma çözünürlüğünün altında ve eşleştirilmiş testte ayırt
  edilemiyor.
- **"Öğrenilen yöntem neden kaybediyor?"** Adım başına daha çok
  kazanıyor, ama adımı 2.7–4 kat pahalı. Aynı milisaniyede Adam daha çok
  adım atıyor ve daha erken bitiriyor.
- **"Bu yüzden derin öğrenme işe yaramaz mı diyoruz?"** Hayır. Bu
  uygulamada ve bu maliyet oranında baskınlanıyor diyoruz. Oran hızlandırıcı
  donanımda değişebilir, bunu da yazdık.
- **"Pilot süresi gerçekçi mi?"** Wang ve diğerleri (TWC 2020) şemasıyla 48
  sembol, 5G NR'de 0.86–3.43 ms. Basit kullanıcı-başı kestirimle 132 sembol,
  2.36–9.43 ms.

## 7. Görüşmeden sonra yapılacaklar

- [ ] Kırmızı alanları doldur: yazarlar, kurum, fon bilgisi, teşekkür,
      repo bağlantısı, 3GPP sürümleri
- [ ] Hocanın dergi kararına göre formatı ve uzunluğu ayarla
- [ ] Onaylanan ölçümleri 20 Kasım'dan önce koştur
- [ ] Tez referansındaki elle yazılmış satırları betikli değerlerle değiştir
- [ ] Gönderimden önce son bir bağımsız denetim yaptır
