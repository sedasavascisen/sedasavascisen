# AISY 2026 makalesinin sonuçlarını üreten temiz paket

Makale: *Overcoming the Phase Discontinuity Problem in RIS Optimization…*,
Adv. Intell. Syst. 2026, doi:10.1002/aisy.70460.

`orijinal/` klasörü, yüklenen dosyaların **değiştirilmemiş** kopyalarını
içerir. Bu klasördeki yeni betikler yayımlanmış kodu güncellemez; onun
üzerine kurulur (CLAUDE.md, "mutlak kısıt").

## Hangi dosya hangi sonucu üretiyor?

| Makaledeki sonuç | Üreten orijinal dosya | Temiz karşılığı |
|---|---|---|
| Veri seti (40 000 senaryo, N = 32) | `RIS_dataset_large_2D.m` (zip ile aynı; `dataset.m` yalnızca yorumları fazla, rastgele sayı sırası aynı) | `adim1_veri_seti.m` + `ris_veri_uret.m` |
| CNN–LSTM RMSE 2.77°, SR@5°, çıkarım süresi | `theta_NN_multioutput.m` | `adim2_cnn_lstm_egit.m` |
| CD karşılaştırması (Tablo, K = 5) | `ris_CD.m` | `ris_CD_olc.m` |
| Şekil 2 (tezde Şekil 4): CD, K = 5/20/50 | Ölçüm: `baseline_fairness_K_analysis_v1_olcum.m`; şekil: `…_v2_sekil.m` (sayılar elle yazılı) | `adim3_cd_K_olcum.m` → `adim4_sekil_fairness.m` |
| Şekil 1: ölçeklenebilirlik (N = 32…256) | **Ölçen betik yok.** `scalability_analysis_zip.m` ve `Scalability_Analysis_sekil.m` elle yazılmış dizileri çizer | `adim5_olceklenebilirlik_olc.m` (gerçekten ölçer) |

`RIS_dataset_large_2D_UPDATED.m`, `pic.m` (patent çizimi) ve
`demo_results.mat` makalenin sonuçlarını üretmiyor. `demo_results.mat`,
Aralık 2025 tarihli kısa bir demo koşusu: N = 16/64/256 için RMSE
66.0° / 26.7° / 21.5°.

## Çalıştırma sırası (MATLAB, Deep Learning Toolbox)

1. `adim1_veri_seti` → `RIS_dataset_large_2D.mat` (~10–15 dk). Orijinal betikle aynı veri.
2. `adim2_cnn_lstm_egit` → model + test sonuçları. GPU yoksa `ORTAM = 'cpu'`.
   Toplu ve tek-örnek gecikmenin ikisini de ölçer.
3. `adim3_cd_K_olcum` → `fairness_K_results.mat`. CD, CNN ile **aynı** test örneklerinde ölçülür.
4. `adim4_sekil_fairness` → `Sekil_fairness_K.pdf/.png`. Sayılar dosyadan okunur, betikte elle yazılmış sayı yok.
5. `adim5_olceklenebilirlik_olc` → `Sekil_olceklenebilirlik.pdf/.png`. Gecikme her N'de ölçülür.

Not: Bu ortamda MATLAB yok; betikler elle denetlendi ama çalıştırılmadı.
Hata verirlerse, çıktıyı gönderin.

`onizleme_sekil_fairness.png` yalnızca **düzen** önizlemesidir. CD RMSE
değerleri Python denetiminden (`scripts/aisy_cd_k_check.py`), gecikmeler
makaleden alınmıştır. Teze girecek şekil adım 4'ün çıktısıdır.

## Şekil 4 neden bozuktu ve ne değişti

| Sorun | Çözüm |
|---|---|
| İki y ekseni (`yyaxis`); yazılar eğrilerin üstüne biniyordu | İki ayrı panel: (a) doğruluk, (b) gecikme |
| Gecikme ekseni [−0.5, 14] ms; bütün noktalar en altta sıkışmıştı | Logaritmik gecikme ekseni |
| `x = 51.5`'e yazılan etiketler eksen dışına taşıyor ve kesiliyordu | Etiketler lejantta; lejant şeklin altında |
| "K ≥ 20: URLLC Exceeded" gölgesi; oysa K = 20'de 0.60 ms < 1 ms | Gölge kaldırıldı; yalnızca 1 ms çizgisi var |
| Şeklin içinde başlık var | Dergi biçimine uygun olarak başlık altyazıya taşındı (`BASLIK` değişkeniyle isteğe bağlı) |

### Başlık (altyazı) önerileri

İngilizce (makale/dergi):
1. *Accuracy and latency of coordinate descent versus the number of iterations K, compared with the CNN–LSTM.*
2. *Iteration budget of the classical baseline: (a) phase error and (b) per-sample latency of coordinate descent.*
3. *How many iterations does coordinate descent need? Phase error and latency versus K.*

Türkçe (tez):
1. *Koordinat inişinin iterasyon sayısı K'ye göre (a) faz hatası ve (b) örnek başına gecikmesi; CNN–LSTM ile karşılaştırma.*
2. *Klasik taban çizgisinin iterasyon bütçesi: doğruluk ve gecikme.*

Altyazıda şunlar mutlaka belirtilmeli: RMSE'nin hangi tanımla
hesaplandığı, gecikmenin tek örnek mi yoksa toplu iş hacmi mi olduğu ve
donanım. 1 ms çizgisi de "URLLC kullanıcı düzlemi hedefi" olarak
adlandırılmalı; bu bir faz hesaplama bütçesi değildir.

## ÖNEMLİ: Paketi temizlerken bulunan tutarsızlıklar

Bunlar yayımlanmış makaleyi ilgilendiriyor. Kesin hükmü MATLAB'da adım
2–5'i çalıştırdıktan sonra verin. Ardından danışmanınız ve ortak
yazarlarla konuşun. Sonuç değişirse, derginin düzeltme (correction)
sürecini kullanmak doğru yoldur.

1. **CD'nin RMSE'si yayımlanan kodla 3.50° çıkmıyor.**
   - Yayımlanan `ris_CD.m`'yi aynı üretecin NumPy kopyasında, 6000
     örnekle koşturdum (`scripts/aisy_cd_k_check.py`,
     `results/aisy_cd_k_check.json`). Makaledeki tanımla RMSE K =
     5/20/50 için **103.8° / 103.6° / 103.5°** çıkıyor.
   - Nedeni: etiket (−∠G − ∠F) doğrudan bağlantıyı yok sayıyor. CD ise
     gerçek optimuma yakınsıyor; bu optimum etiketten yalnızca bir ortak
     faz kadar farklı.
   - Ortak faz çıkarılınca CD'nin hatası **1.10° / 0.26° / 0.05°**. Yani
     K = 5'te bile CNN–LSTM'in 2.77°'sinden daha iyi.
   - h_d = 0 alınsa da sonuç ~104° kalıyor. Yayımlanan 3.50 / 3.49 / 3.20
     değerlerini bu kodla üretmenin bir yolunu bulamadım.
2. **Etiket optimum değil.** CD'nin alınan gücü, etiketinkinden ortalama
   **+2.1 dB** yüksek (K = 20'de örneklerin %98'inde). Bu yüzden "etikete
   RMSE", CD'yi doğru olduğu için cezalandırıyor.
3. **CNN ve CD farklı test kümelerinde ölçülmüş.** CNN rastgele %15'te
   (`randperm`), CD verinin son %15'inde.
4. **Gecikmeler aynı şeyi ölçmüyor.** CNN'in 0.08 ms'si, GPU'da toplu
   tahminin örnek sayısına bölünmesiyle elde edilmiş (iş hacmi). CD'nin
   süresi ise örnek örnek sıralı ölçülmüş (tek-örnek gecikmesi).
5. **Ölçeklenebilirlik şeklinin ölçüm betiği yok.**
   - Değerler tam katlar: CNN 0.08 × N/32; CD ve Transformer her
     ikiye katlamada ×4.
   - Üç sürüm birbirini tutmuyor:
     - zip: CD N = 32'de 0.15 ms, N = 256'da 73.0 ms;
     - yeni betik: CD 0.76 ms ve 48.64 ms. N = 256'da CD ile Transformer
       yer değiştirmiş; makale altyazısı CD = 73.0 diyor;
     - README: N = 64/128 için 0.12 / 0.19 ms.
   - Transformer gecikmesi makalede üç farklı değerle geçiyor: Şekil 1'de
     1.1 ms, tabloda 0.11 ms, metinde 0.17 ms.
6. **`RIS_dataset_large_2D_UPDATED.m` büyük olasılıkla belleği aşar.**
   `corr(THETA')` satırı 40 000 × 40 000'lik bir matris kurar (~12.8 GB).
7. **Parametre sayısı tutmuyor** (önceden biliniyordu, `README.md`): MATLAB
   yığını 162 562 parametre; makalede 727 360 yazıyor.

**Tez için öneri:** Şekil 4 ve ölçeklenebilirlik şekli teze, adım 3–5'te
**ölçülen** değerlerle girmeli. Yayımlanan sayılar, kaynağı gösterilmeden
ve yeniden üretilmeden kullanılmamalı. Sin/cos gösteriminin katkısı bu
sorunlardan etkilenmiyor. O katkı tezde bağımsız olarak doğrulandı
(`TEZ_YAZIM_REFERANSI.md` §6.4 ve §6.7).
