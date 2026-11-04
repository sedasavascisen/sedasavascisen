# Faz-farkında CNN–LSTM'in hareketli MISO senaryosuna taşınması — sonuçlar (4 Kasım 2026)

Yayımlanmış model: Savaşçı Şen vd., *Adv. Intell. Syst.* 2026, doi:10.1002/aisy.70460.
Yazarların kodundan (train_cnn_lstm.py ve theta_NN_multioutput.m) birebir taşındı;
yalnızca girdi kanal sayısı değişti. 4 kanalla PyTorch portu yazarların sınıfıyla
aynı parametre sayısını verir (822 976).

## Kurgu
- Senaryo: hareketlilik makalesinin yaşlanma kümesi, tek kullanıcı. 3GPP InH-Office,
  8 antenli BS, 8×4 RIS (N=32), 20 saçıcı, doğrudan bağlantı 40 dB bloklu, 3 GHz, 1.5 m/s.
- Veri seti: 40 000 statik anlık görüntü (seed 2026), %70/15/15. Etiket: kesin
  eleman-bazlı koordinat yükselişi (1000 adımlı Adam'la 1.3e-3 b/s/Hz içinde).
  Üretici: `scripts/sumiso_dataset.py` (veri depoya konmadı, yeniden üretilir).
- MISO'da etiketin ortak fazı belirsizdir (zayıf doğrudan bağlantı). Etiket 1. elemana
  göre sabitlenir, ortak faz çıkarımda kapalı formda geri konur: φ = ∠(cᴴa).
- Değerlendirme: ayrı çekiliş (seed 11), 400 senaryo; her yöntemin fazı, kendi
  ölçülen gecikmesindeki kanalda değerlendirilir (etkin hız). Boş makine
  (yük 0.66 / 0.81 / 1.02), tek iş parçacığı.

## Statik sonuçlar (test, 6000 senaryo) — `scripts/sumiso_train.py`
| Kurulum | Baş | RMSE (°) | SR@5° | Hız (b/s/Hz) | Kapalı form | Optimum |
|---|---|---|---|---|---|---|
| SISO (N_t=1), yayımlanmış etiket −∠(GₙFₙ) | MATLAB (dizi) | 14.99 | %72.1 | 10.334 | 10.349 | 10.349 |
| SISO, yayımlanmış etiket | PyTorch (düz) | 30.74 | %24.3 | 10.142 | 10.349 | 10.349 |
| MISO (N_t=8), kaskat girdi | MATLAB (dizi) | 61.32 | %24.9 | 12.490 | 12.431 | 12.893 |
| MISO, kaskat girdi | PyTorch (düz) | 66.45 | %14.3 | 12.241 | 12.431 | 12.893 |
| MISO, ham girdi (ayrı F, G) | PyTorch (düz) | 83.84 | %10.2 | 11.201 | 12.431 | 12.893 |

## Hareketli etkin hız (400 senaryo, seed 11) — `scripts/sumiso_mobility_eval.py`
Adam adım boyu her L için doğrulamada 10 değerden ([0.02, 2.0]) seçildi; seçimler ızgara içinde.
Yük: 0.66 (başta) / 0.81 / 1.02 (ölçüm sonunda; betiğin kendi iş parçacığı).

| Yöntem | Gecikme (ms) | R(t=0) | T_ov=0 | 1.71 ms | 3.43 ms | 10 ms |
|---|---|---|---|---|---|---|
| SU-hizalama (kapalı form) | 0.038 | 12.389 | 12.389 | 12.385 | 12.369 | 12.249 |
| **CD-1** (1 tarama) | 2.26 | 12.709 | 12.701 | **12.683** | **12.660** | **12.497** |
| **CD-2** | 4.72 | 12.736 | **12.702** | 12.673 | 12.639 | 12.442 |
| CD-10 | 22.55 | 12.742 | 12.167 | 12.115 | 12.063 | 11.987 |
| Adam-8 (en iyi Adam, T_ov=0) | 4.17 | 12.690 | 12.661 | 12.637 | 12.606 | 12.417 |
| CNN–LSTM (tek geçiş) | 1.18 | 12.355 | 12.354 | 12.342 | 12.325 | 12.192 |
| CNN–LSTM + CD-1 | 4.15 | 12.700 | 12.672 | 12.648 | 12.616 | 12.428 |
| CD yakınsamış (çevrimdışı tavan) | — | 12.745 | | | | |

En iyiye göre eşleştirilmiş fark (%95 GA sıfırı dışlıyor): CNN–LSTM −0.306…−0.348,
CNN–LSTM + CD-1 −0.030…−0.069 b/s/Hz.

## Hüküm
1. Tek geçişli CNN–LSTM, 0.04 ms'lik kapalı formun **altında** kalıyor (12.355 < 12.389).
2. CNN–LSTM + CD-1, SU-hizalamadan başlayan CD-1'in hem hızında hem gecikmesinde altında.
   Ağ, iyileştirme için de iyi bir başlangıç vermiyor.
3. Her T_ov'de en iyi yöntem klasik (CD-1/CD-2). Gecikme sıralamayı yine belirliyor:
   CD-10 t=0'da 12.742 iken 23 ms gecikmeyle 12.154'e düşüyor.
4. Mekanizma: SISO'da optimum eleman başına kapalı formdadır (−∠bₙ + ∠a); ağ, 0.04 ms'de
   kesin hesaplanan bir fonksiyonu yaklaşık öğreniyor. MISO'da optimum BS hüzmesi
   üzerinden tüm elemanlara bağlı (küresel) hale geliyor ve yayımlanmış mimariler bunu
   yakalayamıyor. Ham F, G girdisiyle ağ gₙ·Fₙ çarpımını kendisi kuramıyor.

Bu, tezdeki "yapay zekâ ekseni kapandı ve olumsuz" sonucunu yayımlanmış modelle ve tek
kullanıcılı MISO'ya genişletir. Yeniden "çalışıyor" diye çerçevelenmemelidir.

## Uyarılar
- SISO kontrolünde 2.77° yeniden üretilemedi (en iyi 14.99°). Veri üreteci farklı
  (3GPP geometrisi + LoS vs. makaledeki Rayleigh + 6 saçıcı), yani bu bir çelişki
  değil, ama jüri sorabilir.
- Makalede 727K parametre yazıyor; yazarların PyTorch sınıfı N=32'de 822 976 veriyor,
  MATLAB yapısı ~162K. Hangi modelin raporlandığı kontrol edilmeli.
- MISO test kümesinde (seed 2026) CNN–LSTM SU-hizalamanın üstünde (12.490 > 12.431),
  değerlendirme kümesinde (seed 11) altında (12.355 < 12.389). Fark küçük, işaret kararsız.
- Gecikme: Python/PyTorch, tek iş parçacığı, 20 senaryo × 25 tekrar × 3 tur.

## Makaleye eklenme
Hareketlilik makalesi §VI-G ve Tablo VII (`tables/tab_cnnlstm.tex`, make_paper_assets.py üretir).
