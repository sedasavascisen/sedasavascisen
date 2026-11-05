# Faz-farkında CNN–LSTM'in hareketli MISO senaryosuna taşınması — sonuçlar

*İlk sürüm 4 Kasım 2026. 5 Kasım 2026'da bağımsız denetim sonrası düzeltildi;
düzeltmelerin kaydı `DEGISIKLIKLER_2026-10-23.md` sonunda.*

Yayımlanmış model: Savaşçı Şen vd., *Adv. Intell. Syst.* 2026, doi:10.1002/aisy.70460.
Yazarların MATLAB koduyla (theta_NN_multioutput.m) aynı mimari kullanıldı. PyTorch kodundan
(train_cnn_lstm.py) üç tercih alındı: z-skor girdi, gradyan kırpma (1.0), en iyi doğrulama
checkpoint'i. Yalnızca girdi kanal sayısı değişti. 4 kanalla PyTorch sınıfı 822 976,
MATLAB yapısı 162 562 parametre veriyor; makaledeki 727K ikisine de uymuyor.

## Kurgu
- **Senaryo:** hareketlilik makalesinin yaşlanma kümesi, tek kullanıcıyla. 3GPP InH-Office,
  8 antenli BS, 8×4 RIS (N=32), 20 saçıcı, doğrudan bağlantı 40 dB bloklu, 3 GHz, 1.5 m/s.
- **Veri seti:** 40 000 statik anlık görüntü (seed 2026). 28 000'i eğitim, 6000'i
  checkpoint seçimi ve Adam ayarı, 6000'i statik test.
- **Etiket:** kesin eleman-bazlı koordinat yükselişi. 3 başlangıçlı, 1000 adımlı Adam
  etiketi senaryo başına en fazla 0.0048 b/s/Hz geçiyor (300 senaryo,
  `scripts/sumiso_label_check.py`).
- **Ortak faz:** MISO'da etiketin ortak fazı belirsiz (zayıf doğrudan bağlantı). Etiket 1.
  elemana göre sabitleniyor, ortak faz çıkarımda kapalı formda geri konuyor: φ = ∠(cᴴa).
- **Değerlendirme:** ayrı çekiliş (seed 11), 400 senaryo. En iyi yöntem üçüncü bir
  çekilişte (seed 12) seçiliyor.
- **Gecikme:** yük 0.5'in altına inene kadar beklendi; ölçüm 0.16'da başladı, 0.97'de
  bitti (betiğin kendi iş parçacığı). Tek iş parçacığı.

## Statik sonuçlar (test, 6000 senaryo) — `scripts/sumiso_train.py`
| Kurulum | Baş | RMSE (°) | SR@5° | Hız (b/s/Hz) | Kapalı form | Optimum |
|---|---|---|---|---|---|---|
| SISO (N_t=1), yayımlanmış etiket −∠(GₙFₙ) | MATLAB (dizi) | 14.99 | %72.1 | 10.334 | 10.349 | 10.349 |
| SISO, yayımlanmış etiket | PyTorch (düz) | 30.74 | %24.3 | 10.142 | 10.349 | 10.349 |
| MISO (N_t=8), kaskat girdi | MATLAB (dizi) | 61.32 | %24.9 | 12.490 | 12.431 | 12.893 |
| MISO, kaskat girdi | PyTorch (düz) | 66.45 | %14.3 | 12.241 | 12.431 | 12.893 |
| MISO, ham girdi (ayrı F, G) | PyTorch (düz) | 83.84 | %10.2 | 11.201 | 12.431 | 12.893 |

Ham girdi satırı PyTorch başıyla eğitildi, bu yüzden 66.45° ile karşılaştırılmalı.

## Hareketli etkin hız (400 senaryo, seed 11) — `scripts/sumiso_mobility_eval.py`
| Yöntem | Gecikme (ms) | R(t=0) | T_ov=0 | 1.71 ms | 3.43 ms | 10 ms |
|---|---|---|---|---|---|---|
| SU-hizalama (kapalı form) | 0.04 | 12.389 | 12.389 | 12.385 | 12.369 | 12.249 |
| **CD-1** (1 tarama) | 2.48 | 12.709 | **12.698** | **12.681** | **12.656** | **12.491** |
| CD-2 | 4.76 | 12.736 | 12.701 | 12.673 | 12.638 | 12.441 |
| CD-10 | 23.06 | 12.742 | 12.152 | 12.099 | 12.047 | 11.984 |
| **Adam-1** (tek adım) | 0.59 | 12.499 | 12.498 | 12.490 | 12.472 | 12.339 |
| Adam-8 | 3.89 | 12.690 | 12.664 | 12.642 | 12.611 | 12.427 |
| CNN–LSTM (tek geçiş) | 1.12 | 12.355 | 12.354 | 12.342 | 12.326 | 12.193 |
| CNN–LSTM + CD-1 | 4.26 | 12.700 | 12.671 | 12.646 | 12.614 | 12.424 |
| CD yakınsamış (çevrimdışı tavan) | — | 12.745 | | | | |

Kalın: seed 12'de seçilen en iyi yöntem (her T_ov'de CD-1). T_ov=0'da test kümesinde CD-2
ile CD-1 arasındaki fark 0.003 b/s/Hz, yani pratikte beraberlik.

**t=0'da eşleştirilmiş farklar** (ortalama [%95 GA]):

| Karşılaştırma | 400 senaryo (seed 11) | 6000 senaryo (seed 11) | 6000 senaryo (seed 13) |
|---|---|---|---|
| CNN − kapalı form | −0.034 [−0.094, +0.026] | +0.059 [+0.041, +0.077] | +0.040 [+0.023, +0.059] |
| CNN − Adam-1 | −0.143 [−0.197, −0.089] | −0.090 [−0.106, −0.074] | −0.104 [−0.120, −0.088] |
| (CNN + CD-1) − CD-1 | −0.009 [−0.021, +0.004] | — | — |

6000 senaryoluk sütunlar `scripts/sumiso_t0_robustness.py`'den geliyor.

## Hüküm
1. **Tek geçişli CNN–LSTM'i, tek bir Adam adımı baskınlıyor.** Adam-1 daha hızlı
   (0.59 ms, CNN 1.12 ms) ve her üç çekilişte anlamlı biçimde daha iyi.
2. **CNN, kapalı formun altında DEĞİL.** 400 senaryoda fark anlamsız; 6000 senaryoda
   ağ, kapalı formun biraz **üstünde** (+0.04 ile +0.06). Kapalı formla optimum
   arasındaki farkın %12.8'ini kapatıyor.
3. **CNN, CD için iyi bir başlangıç değil.** t=0'da hiçbir şey eklemiyor (fark anlamsız).
   Gecikmesi daha yüksek olduğu için (4.26 ms'ye 2.48 ms) etkin hızda her T_ov'de en iyinin
   0.028–0.066 b/s/Hz altında kalıyor.
4. **Gecikme sıralamayı yine belirliyor.** CD-10 t=0'da 12.742 iken 23 ms gecikmeyle
   12.152'ye düşüyor; en iyisi tek tarama.
5. **Mekanizma:** MISO'da her elemanın en iyi fazı, diğer elemanların oluşturduğu BS
   hüzmesine bağlı. Ağ bu bağlaşımın küçük bir kısmını yakalıyor.

Bu sonuç, tezdeki "yapay zekâ ekseni olumsuz" bulgusunu yayımlanmış modelle tek
kullanıcılı MISO'ya genişletiyor. Yeniden "çalışıyor" diye çerçevelenmemelidir.

## Uyarılar
- **SISO kontrolü:** makaledeki 2.77° yeniden üretilemedi (en iyi 14.99°). Veri üreteci
  farklı (3GPP geometrisi ve LoS; makalede Rayleigh ve 6 saçıcı), yani mutlak hata iki
  çalışma arasında karşılaştırılamaz. SISO'da kapalı form zaten kesin optimum.
- **Ölçüm yükü:** ilk ölçümde (4 Kasım) yük 0.66'dan başlamıştı. 5 Kasım'da yük 0.5'in
  altına inene kadar beklenerek yeniden ölçüldü; bu dosyadaki gecikmeler yeni ölçüm.
- **Gecikme ortamı:** Python/PyTorch, tek iş parçacığı, 20 senaryo × 25 tekrar × 3 tur.

## Makaleye eklenme
Hareketlilik makalesi §VI-G ve Tablo VII (`tables/tab_cnnlstm.tex`, `make_paper_assets.py`
tarafından üretiliyor).
