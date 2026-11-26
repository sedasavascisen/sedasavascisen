# Editör eleştirilerine göre düzeltme planı (26 Kasım 2026)

**Gruplar**
- **A:** yalnızca metin.
- **B:** eldeki, denetlenmiş ölçümlerle; yeni ölçüm yok.
- **C:** yeni deney. Ölçüm fazı kapalı (20 Kasım); bunlar için süre tahmini ve onay gerekiyor (Kural 7).

**Sayfa bütçesi:** 10 sayfa (TWC'de ek ücret 10 sayfanın üstünde başlıyor). Eklenen metin, ayrıntıların ek belgeye taşınmasıyla dengelenecek.

| # | Eleştiri | Yapılacak | Grup | Kaynak | Durum |
| --- | --- | --- | --- | --- | --- |
| E1 | 4. Teori ince; özette "proves" | Özette "shows, within the model,"; Katkı 2'de modelin açıklayıcı (öngörücü değil) rolü | A | §IV, §VI-C | **yapıldı** |
| E2 | 7. Yenilik algısı | Girişte yeniliğin yalnızca ölçüt değil, ölçülen olgu (içsel optimum ve x yasası) olduğunu açıkça yazmak | A | — | **yapıldı** |
| E3 | 1. Gerçekleştirme bağımlılığı | §VI-C: FLOP tabanlı maliyet modeli ölçülmüş süreyle aynı adım sayısını seçiyor (τ = 0.86–0.87; 1.5 m/s'de Adam-6, 10 km/h'de Adam-4). Eşit hızlanma sonucu sonuçta zaten var. | B | `juri/REPORT_S3_S1.md` S3-E | **yapıldı** |
| E4 | 3. Tek senaryo | §VI-D: korelasyon tabanı olmayan Clarke kanalında da iç optimum (3–8 adım, 3.4–8.8 ms; L = 48 %27–32 kaybettiriyor) | B | `juri/REPORT_S4_S2.md` | **yapıldı** |
| E5 | 5. Kusursuz CSI | Özete "perfect channel knowledge" varsayımı; girişte kusurlu CSI etkisinin büyüklüğü | A | §VI-H | **yapıldı** |
| E6 | 11. RIS anahtarlama süresi | Sınırlar: anahtarlama süresi (≥ 0.72 ms) ek bir sabit gecikme gibi davranır ve §VI-D'nin 0–10 ms edinme gecikmesi aralığına düşer | A | §VI-D | **yapıldı** |
| E7 | 9. Sunuş yoğun | §V-C ve §V-D'deki ölçüm günlüğü ayrıntılarını (yük ortalamaları, tur sayıları, tur arası farklar) ek belgeye taşımak; ana metinde özet | A | — | **yapıldı** |
| E8 | 6. Öğrenilen kol t = 0'da | §VI-F'de ve sınırlarda karşılaştırmanın t = 0 ve statik kümede olduğunu açıkça yazmak (gerekçesiyle) | A | §VI-F | **yapıldı** |
| E9 | 2. Dağınık zamanlama | Bütün gecikmeleri tek, temiz bir oturumda (tek iş parçacığı, boş makine) yeniden ölçmek ve ana tabloları o değerlerle yeniden üretmek | C | — | **onay gerekiyor**; süre tahmini aşağıda |
| E10 | 3. Tek senaryo (tam çözüm) | İkinci bir geometri ya da CDL kanalı | C | — | onay gerekiyor; gelecek çalışma önerisi |
| E11 | 6. Karşılaştırma kümesi | SDR ve WMMSE'nin zamanlanması; öğrenilen kolun eskimeyle değerlendirilmesi (ağırlık arşivi gerekli) | C | — | onay gerekiyor |
| E12 | 10. Ağırlıklar | Ağırlık arşivini bulmak ya da beş modeli yeniden eğitmek (yaklaşık 2.5 saat) | C | `HAKEM_HAZIRLIK.md` | kullanıcıda |
| E13 | 8. İstatistik | §VI-H zaten bağımsız çekilişte (seed 12) seçiyor; ana tabloların seçim/rapor ayrımı metinde zaten kayıtlı. Ek iş: yok; kapak mektubunda vurgulanacak | A | §V-D | yapılacak (kapak) |

**E9 için süre tahmini:** zamanlama betiklerinin ölçülmüş süreleri `NASIL_CALISTIRILIR.md`'de. Gecikme ölçümleri birkaç dakika sürüyor. Asıl yük, yeni gecikmelerle eskime tablolarının, adım taramasının ve hız tablosunun yeniden üretilmesi: 30 dakikayı aşar. Ayrıca makaledeki birçok sayıyı değiştirir ve bütün paketin yeniden denetlenmesini gerektirir. Bu yüzden E9 ayrı bir karar.

## 26 Kasım: uygulananlar
- **E1–E8 yapıldı.** Makale 10 sayfa, özet 197 kelime; denetleyiciler 126/126 ve 120/120.
- **E7:** ölçüm günlüğü ayrıntıları `supplementary.tex` / `supplementary.pdf` dosyasına taşındı (1 sayfa). Ana metin oraya başvuruyor; hiçbir bilgi silinmedi.

## E9 için bulunan seçenek
Tek iş parçacıklı, temiz bir zamanlama oturumu zaten var:
- `thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json`: yük 0.45, SU, CD ve uzun koşulu Adam süreleri, Adam adımı 1.33 ms.
- Bu sürelerle tam gecikmede yapılmış değerlendirme: `p4/izgara_kontrol/raw/results.json`, `results_tab1.json`.

Ana tablo ve adım taraması bu oturuma geçirilirse makale tek bir Adam adım süresi kullanır. Yeni gecikme ölçümü gerekmez, ama sayıların çoğu (Tablo III, Şekil 3, metindeki L* ve yüzdeler) değişir; bütün paket yeniden denetlenmeli. Statik küme (Şekil 5) için yeniden zamanlama ağırlık arşivi gerektiriyor.
