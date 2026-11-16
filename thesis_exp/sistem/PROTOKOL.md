# Gecikme farkındalıklı RIS denetleyicisi: geliştirme ve mühürlü test protokolü (16 Kasım 2026, gece)

Bu dosya gece çalışması başlamadan commit'lenir. Amaç, bir gece boyunca serbestçe fikir denemek, ama sabah raporlanacak sayıyı sonuç avcılığından korumak.

## Sistem

Denetleyici, her güncellemede ölçülen girdilerden bir faz hesaplama hattı seçer.
- **Girdiler:** kullanıcı hızı ya da Doppler kestirimi, taşıyıcı f_c, bant genişliği B, bu makinede ölçülmüş adım maliyetleri, fazın tutulacağı süre W.
- **Hat:** başlangıç (SU-average ya da SU-best-of, gerekirse başka) + yöntem + adım sayısı L (+ geniş bantta K_opt).
- Çıktı, seçilen hattın ürettiği faz; hat, kendi ölçülmüş gecikmesinde devreye girer.

## Koşul ızgarası (sabit)

| Kod | f_c | Hız | B | W (ms) |
| --- | --- | --- | --- | --- |
| A1–A4 | 3 GHz | 3, 5.4, 10, 30 km/h | dar bant | 0 ve 20 |
| B1–B2 | 28 GHz (telafili, `juri/s5/ch28.py`) | 3, 5.4 km/h | dar bant | 0 ve 20 |

Toplam 6 hız koşulu × 2 W = 12 koşul. Geniş bant koşulları gece fikri olarak eklenebilir, ama **mühürlü testin birincil sonucu bu 12 koşuldur.**

## Ölçüt

Etkin hız: hat, kendi gecikmesi τ'da devreye girer; [τ, τ + W] aralığında, 2 ms aralıklı ızgarada ortalama min-kullanıcı hızı alınır. W = 0 ise yalnızca τ anı (Tanım 1). Gecikmeler: `thesis_exp/juri/raw/timing2.json` (bu makine, tek iş parçacığı).

## Çekilişler

| Tohum | Kullanım |
| --- | --- |
| 12 | Denetleyicinin kalibrasyonu ve parametre seçimi |
| 14 | Gece boyunca fikirlerin karşılaştırılması (geliştirme testi) |
| **41** | **Mühürlü test.** Gece hiçbir betik bu tohumu üretmez (`harness.py` bunu `--final` olmadan reddeder). Sabah yalnızca seçilen son sistemle, bir kez koşulur. |

## Karşılaştırma yöntemleri (sabit)

| Kod | Yöntem |
| --- | --- |
| K1 | SU-best-of (optimizasyonsuz en iyi sezgisel) |
| K2 | SU-average + Adam-5 (makalenin ana noktasındaki sabit seçim) |
| K3 | SU-average + Adam-48 (gecikmeyi yok sayan "yakınsamaya kadar koş") |
| K4 | Makalenin kapalı formu, L(x) (`tasarim_kurali/rule.py` closed_form) |
| K5 | Ryu tarzı: 10 ms bütçeye sığan hatlar arasında t = 0'da en iyi olan (seed 12'de seçilir) |
| K6 | Kâhin: her koşulda, test çekilişinde geriye dönük en iyi hat. Yalnızca üst sınır; hipotezlerde kullanılmaz. |

## Mühürlü testin hipotezleri (seed 41)

- **H1:** 12 koşul üzerinden ortalama etkin hız farkı (sistem − Ki), K1…K5'in her biri için > 0. Ölçüt: koşullar ve senaryolar üzerinden eşli bootstrap GA'sının alt sınırı > 0.
- **H2:** Koşul başına, sistem hiçbir koşulda K1…K5'in en iyisinden anlamlı olarak kötü değildir (GA üst sınırı ≥ 0).
- **Raporlanır:** kâhine göre kayıp; koşul başına tablo; seçilen hatlar.

## Gece kuralları

1. **Fikir günlüğü:** her fikir `GUNLUK.md`'ye yazılır: ne, neden, kod, seed 14 sonucu, karar. Başarısız fikirler de yazılır.
2. **Seçim:** sabah, seed 14'te ortalama etkin hızı en yüksek olan sürüm dondurulur, commit'lenir, sonra seed 41 bir kez koşulur. Sonuç ne çıkarsa raporlanır.
3. **Yeni hat türleri:** öngörü, sıcak başlangıç, geniş bant ve benzerleri, gecikmeleri bu makinede aynı protokolle ölçülmeden kullanılamaz.
4. **Yasak:** seed 41'e bakmak; ızgarayı ya da karşılaştırma yöntemlerini sonuçlara göre değiştirmek.
