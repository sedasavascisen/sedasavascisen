# Beş "son nokta" önerisinin değerlendirmesi (9 Kasım 2026)

Kaynak: kullanıcının yapıştırdığı, başka bir yapay zekâ aracının ürettiği metin. Değerlendirmenin
ölçütleri tezin kendi kuralları (`CLAUDE.md`): betiksiz sayı yok, ayarlı klasik rakip, yapay zekâ
eksenini "çalışıyor" diye yeniden çerçevelememe, ölçüm fazının 20 Kasım'da kapanması.

## Önce metindeki düzeltilmesi gereken iddialar

| Metindeki ifade | Gerçek durum |
|---|---|
| "Kütüphanenizdeki 251 kaynağı inceledim" | Bu oturumda böyle bir kütüphane yok. Metni üreten araç da göremezdi. |
| CNN–LSTM "0.08 ms", "2.77° RMSE" | 0.08 ms, toplu GPU iş hacminin örnek başına payı. Bizim tek-örnek ölçümümüz 1.12 ms. 2.77°, AISY'nin kendi veri üretecinde elde edildi; bizim senaryomuzda tek antende 14.99°, çok antende 61.3°. |
| "Patentli buluşum Sin/Cos Öklid Manifold Kafası" | Sin/cos regresyonu literatürde bilinen bir teknik. Katkınız onu RIS faz süreksizliğine uygulayıp gerekçelendirmek; patent iddiası belgelenmeden yazılmamalı. |
| "L* ≈ 4–8 içsel optimumu" CNN–LSTM bölümünün sonucu gibi sunuluyor | L*, Adam'ın adım sayısı için hareketlilik çalışmasının bulgusu. CNN–LSTM ile ilgisi yok. |
| "3GPP Rel-19/20 ile %100 uyumlu" | Bir simülasyon bir standarda "%100 uyumlu" olamaz. En fazla standardın kanal modelini ya da parametrelerini kullanır. |
| Unrolled PGD + CNN–LSTM "jüriyi ikna eder, mat eder" | Derin açılımlı öğrenilmiş güncelleme kuralı tezde zaten var: adım başına klasiği geçiyor, milisaniye başına her noktada kaybediyor. |

## Öneri öneri değerlendirme

| # | Öneri | Durum | Karar |
|---|---|---|---|
| 1 | Geniş bant OFDM, hüzme sapması (beam squint) | Hareketlilik makalesinin "sıradaki adım" olarak yazdığı konu. Tezin çerçevesine doğrudan oturuyor: geniş bantta adım maliyeti alt taşıyıcı sayısıyla artar, yani x = ΔT·f_d büyür ve modelimiz L*'ın nereye kayacağını önceden söyler. | **Fizibilitesi bu gece ölçülüyor.** Not: 3 GHz'de 32 elemanlı bir RIS için hüzme sapması büyük olasılıkla ihmal edilebilir (açıklık ≈ 0.4 m). Asıl geniş bant etkisi, odadaki çok yollu yayılımın yarattığı frekans seçiciliği. |
| 2 | Derin açılım (Unrolled PGD) + sin/cos, CNN–LSTM'e karşı | **Zaten yapıldı ve olumsuz** (makale Bölüm VI-F, tez §4.4–4.5). Ayrıca sin/cos kafası açılımlı bir yöntemde işlev görmez: faz gradyan adımıyla güncellenir, ±π süreksizliği oluşmaz. | Yeniden yapılmamalı; mevcut sonuç tezde "fizik tabanlı öğrenme de denendi" diye zaten anlatılıyor. |
| 3 | STAR-RIS + ISAC, hareketli hedef takibi | Yeni sistem modeli, yeni algılama metriği, yeni rakipler. 11 günde titizlikle yapılamaz. | Gelecek çalışma. |
| 4 | GAT-LSTM, yeniden eğitmeden N ölçekleme | Kısmi kanal deneyinde 2B mimari değişikliği (B) bir şey kazandırmadı; kanal yatayda neredeyse ilişkisiz (|ρ| = 0.055). Çizge dikkatinin bu kanalda yakalayacağı uzamsal yapı az. | Önerilmez; gelecek çalışma olarak anılabilir. |
| 5 | INT8 FPGA/MCU donanım prototipi | Donanım yok; ölçüm fazı 11 gün. | Gelecek çalışma. |

## Bu gece yapılan

1. Kanal üretecine, varsayılan çıktıyı bit düzeyinde değiştirmeyen bir geniş bant seçeneği ekleniyor.
2. Senaryomuzdaki gecikme yayılımı, koherans bant genişliği, tek faz vektörünün 1–100 MHz'te
   alt taşıyıcı başına optimuma göre kaybı ve adım maliyetinin alt taşıyıcı sayısıyla artışı ölçülüyor
   (`scripts/wideband_feasibility.py`).
3. Geniş bant RIS, hüzme sapması ve derin açılım literatürü doğrulanmış künyelerle taranıyor
   (`LITERATUR_GENIS_BANT.md`).

Sabah karar: etki anlamlıysa, 20 Kasım'dan önce bitecek, ön kayıtlı küçük bir deney
("L*, alt taşıyıcı sayısı arttıkça x = ΔT·f_d'nin öngördüğü gibi kayıyor mu?"). Değilse,
tezde "geniş bant etkisi bu senaryoda küçük" diye tek paragraf ve gelecek çalışma.
