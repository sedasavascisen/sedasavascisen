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

   Ana fikir hepsinde ayakta kaldı: en iyi sonucu veren, "az ama hızlı" hesap yapan yöntem (Adam'ın 5–8 adımı). Uzun ve yavaş yöntemler her durumda geride.
2. **İki makaleyi bağlayan bir bulgu çıktı.** Makale 1'in yapay zekâ modeli, Makale 2'nin ölçüsüyle (gecikmeyi hesaba katan etkin hız) bakınca klasik yöntemlerin gerisinde kalıyor. Bağlayıcı cümle: *ölçüyü değiştirirsen sonuç değişir.*
3. **Her iş ayrı bir denetçiye kontrol ettirildi.** Denetçi üç turda 300'den fazla sayıyı ham veriden yeniden okudu. Bulunan hataların hepsi düzeltildi; önemli sonuçların hiçbiri değişmedi.
4. **Makale 1:** Denetimde bazı sayıların tekrar elde edilemediği görüldü. 13 Kasım'da sizin isteğinizle Makale 1 üzerindeki çalışma durduruldu; o güne kadarki kayıt Ek'te.

**Akılda kalacak üç sayı**

- **Ölçümün bedeli:** Sinyali ölçmenin maliyeti (pilot) hesaba katılınca hız %17–32 düşüyor. Ama hangi yöntemin en iyi olduğu değişmiyor.
- **Ölçüm hatası:** 30 dB'lik bir ölçüm kalitesinde bile hız 6.08'den 3.54 b/s/Hz'e iniyor.
- **Uzun düşünmenin bedeli:** 48 adım hesap yapmak, en iyi adım sayısına göre %14–15 kaybettiriyor (2 ve 3 bit).

**Sırada ne var?** Ölçüm fazı 20 Kasım'da kapanıyor. Ondan sonra yeni deney açılmıyor; yazım başlıyor.
