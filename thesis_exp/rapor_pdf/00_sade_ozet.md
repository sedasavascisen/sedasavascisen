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

   Ana fikir hepsinde ayakta kaldı: en iyi sonucu çoğunlukla "az ama hızlı" hesap yapan yöntem veriyor (genellikle Adam'ın birkaç adımı; ölçüm hatası arttıkça en iyi adım sayısı 1 ile 6 arasında değişiyor). İstisna: 1 bitte tek turluk yavaş arama (dCD-1) Adam'la berabere ve doğrulamada o seçiliyor. Uzun ve yavaş yöntemler hiçbir durumda öne geçmiyor.
2. **İki makaleyi bağlayan bir bulgu çıktı.** Makale 1'in yapay zekâ modeli, Makale 2'nin ölçüsüyle (gecikmeyi hesaba katan etkin hız) bakınca klasik yöntemlerin gerisinde kalıyor. Bağlayıcı cümle: *ölçüyü değiştirirsen sonuç değişir.*
3. **Her iş ayrı bir denetçiye kontrol ettirildi.** Denetçi üç turda 300'den fazla sayıyı ham veriden yeniden okudu. Bulunan hataların ikisi dışında hepsi düzeltildi (açık kalan ikisi küçük); önemli sonuçların hiçbiri değişmedi.
4. **Makale 1:** Denetimde bazı sayıların tekrar elde edilemediği görüldü. 13 Kasım'da sizin isteğinizle Makale 1 üzerindeki çalışma durduruldu; o güne kadarki kayıt Ek'te.

**Bu gece eklenenler (14–15 Kasım)**

- **Fazın ne kadar süre kullanılacağı önemli.** Yüzeyin ayarı her 25–50 ms'de bir yenileniyorsa en iyisi birkaç adım (5–8). Ayar 100 ms boyunca tutulacaksa daha uzun hesap (16–20 adım) biraz daha iyi; ama fark çok küçük (en fazla 0.04 b/s/Hz). Çok yavaş yöntemler her durumda geride. Yani tezin cümlesi doğru, ama "her zaman birkaç adım" demek yanlış olur.
- **Ölçüm maliyeti ve ölçüm hatası birlikte:** En gerçekçi durumda hız çok düşüyor (30 dB'de 2.4–2.8, 20 dB'de 1.0–1.15 b/s/Hz). 20 dB'de hızlı yöntemler birbirinden ayırt edilemiyor; yavaş yöntemler yine geride.
- **Makale 2'nin sayıları tekrar kontrol edildi.** Ana taramadaki küçük bir yaklaşıklık (interpolasyon) hiçbir sonucu değiştirmiyor; makaledeki "%14" tam hesapla %14.2.

**Akılda kalacak üç sayı**

- **Ölçümün bedeli:** Sinyali ölçmenin maliyeti (pilot) hesaba katılınca hız %17–32 düşüyor. Ama en iyi yöntemler grubu (Adam'ın 4–8 adımı) değişmiyor; bu grubun içindeki sıra kesin değil.
- **Ölçüm hatası:** 30 dB'lik bir ölçüm kalitesinde bile hız 6.08'den 3.54 b/s/Hz'e iniyor.
- **Uzun düşünmenin bedeli:** 48 adım hesap yapmak, en iyi adım sayısına göre %14–15 kaybettiriyor (2 ve 3 bit).

**Sırada ne var?** Ölçüm fazı 20 Kasım'da kapanıyor. Ondan sonra yeni deney açılmıyor; yazım başlıyor.
