# Sade özet — bilmeyen birine anlatır gibi

**İki makale var.**

- **Makale 1:** Bir yapay zekâ modeli, akıllı yüzeyin (RIS) ayarlarını tahmin ediyor.
- **Makale 2:** Kullanıcı yürürken sinyal sürekli değişir. Bu yüzden hesabı **hızlı** yapan yöntem, mükemmel ama yavaş olandan daha iyi sonuç verir. Tezin ana fikri bu: *hesaplama süresi, hangi yöntemin kazanacağını belirler.*

**Ne yapıldı?**

1. **Makale 2 gerçek hayatın zorluklarıyla sınandı.** Altı ek deney yapıldı:
   - kanalı önceden tahmin etmek,
   - yalnızca konumdan ayar hesaplamak,
   - sinyali ölçmenin maliyeti,
   - ölçüm hataları,
   - yüzeyin yalnızca 2, 4 ya da 8 farklı ayar alabilmesi (1/2/3 bit),
   - kodu hızlandırmak.

   Ana fikir hepsinde ayakta kaldı: yüzeyin ayarı sık yenilendiğinde en iyi sonucu "az ama hızlı" hesap yapan yöntem veriyor (genellikle Adam'ın birkaç adımı; ölçüm hatası arttıkça testteki en iyi adım sayısı 1 ile 6 arasında değişiyor (doğrulamada seçilenler 3–20); ayar uzun süre tutulursa en iyi adım sayısı artıyor, aşağıya bakın). İstisna: 1 bitte tek turluk yavaş arama (dCD-1) Adam'la berabere ve doğrulamada o seçiliyor. Çok yavaş yöntemler (CD yaklaşık 0.7 s, PGA yaklaşık 5 s) hiçbir durumda öne geçmiyor.
2. **İki makaleyi bağlayan bir bulgu çıktı.** Makale 1'in yaklaşımını (tek seferde tahmin eden yapay zekâ) çok kullanıcılı sisteme taşıyan bir ağ, Makale 2'nin ölçüsüyle (gecikmeyi hesaba katan etkin hız) bakınca klasik yöntemlerin gerisinde kalıyor; hızı, en basit kapalı form yöntemle aynı düzeyde. Bu ağ Makale 1'in ağının kendisi değil.
3. **Her iş ayrı bir denetçiye kontrol ettirildi.** Denetçi on bir turda yüzlerce sayıyı ham veriden yeniden okudu. Bulunan hataların büyük çoğunluğu düzeltildi; birkaç küçük not açık ya da yalnızca belgelendi (Bölüm C). Önemli sonuçların hiçbiri değişmedi.
4. **Makale 1:** Denetimde bazı sayıların tekrar elde edilemediği görüldü. 13 Kasım'da sizin isteğinizle Makale 1 üzerindeki çalışma durduruldu; o güne kadarki kayıt Ek'te.

**Bu gece eklenenler (14–15 Kasım)**

- **Fazın ne kadar süre kullanılacağı önemli.** Yüzeyin ayarı her 25 ms'de bir yenileniyorsa en iyisi birkaç adım (3–8; en yavaş numerolojide 2–8). 50 ms'de 6–8 adım seçiliyor, ama 3 ile 20 adım arası birbirinden ayırt edilemiyor. Ayar 100 ms boyunca tutulacaksa daha uzun hesap (16–20 adım) daha iyi; fark küçük (Adam-6 için 0.02–0.04, Adam-3 için 0.05–0.08 b/s/Hz; Adam-6 için fark 30 ve 60 kHz'de anlamlı, 15 kHz'de değil). Çok yavaş yöntemler her durumda geride. Yani tezin cümlesi doğru, ama "her zaman birkaç adım" demek yanlış olur.
- **Ölçüm maliyeti ve ölçüm hatası birlikte:** En gerçekçi durumda hız çok düşüyor (30 dB'de 2.4–2.8, 20 dB'de 1.0–1.15 b/s/Hz). 20 dB'de hızlı yöntemler arasındaki farklar çok küçülüyor (en fazla 0.03 b/s/Hz); yavaş yöntemler yine anlamlı biçimde geride.
- **Makale 2'nin Tablo III'ünde küçük bir hesap hatası bulundu ve düzeltildi.** Periyodik çalışmayı taklit eden program, ölçüm süresini yarım milisaniyeye yuvarlıyordu. Düzeltilince "sıcak başlangıcın" kazancı bir durumda büyüyor (0.22 → 0.28), bir durumda küçülüyor (0.15 → 0.09). Sonucun yönü ve anlamı değişmiyor. Tezde düzeltilmiş sayılar kullanılmalı.
- **Makale 2'nin sayıları tekrar kontrol edildi.** Ana taramadaki küçük bir yaklaşıklık (interpolasyon) ana sonuçları değiştirmiyor; makaledeki "%14" tam hesapla %14.2. Tek nitel değişiklik: yeni ölçülen sürelerle en basit kapalı form yöntemin (SU-best-of) 48 adımlık Adam'a üstünlüğü tam hesapta istatistiksel olarak anlamlı hâle geliyor; makale sürelerinde en iyi adım sayısı 5 ile 4 arasında fiilen berabere.

**Akılda kalacak üç sayı**

- **Ölçümün bedeli:** Sinyali ölçmenin maliyeti (pilot) hesaba katılınca hız %17–32 düşüyor. Ayar 50 ms'de bir yenilendiğinde, ölçüm maliyeti hesaba katılınca 3 ile 20 adım arası birbirinden ayırt edilemiyor (seçilen 6–8 adım); maliyetsiz durumla bu kümenin istatistiksel karşılaştırması yapılmadı, yalnızca sıralama aynı.
- **Ölçüm hatası:** 30 dB'lik bir ölçüm kalitesinde bile hız 6.08'den 3.54 b/s/Hz'e iniyor.
- **Uzun düşünmenin bedeli:** 48 adım hesap yapmak, en iyi adım sayısına göre %14–15 kaybettiriyor (2 ve 3 bit).

**Sırada ne var?** Ölçüm fazı 20 Kasım'da kapanıyor. Ondan sonra yeni deney açılmıyor; yazım başlıyor.
