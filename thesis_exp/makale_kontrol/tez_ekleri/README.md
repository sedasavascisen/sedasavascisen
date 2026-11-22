# Tez ekleri: madde 8–14 için hazır tablo ve şekiller

Hepsi `make_tez_ekleri.py` ile, var olan ham dosyalardan üretildi; yeni ölçüm yok. Her dosyanın altında kaynağı yazılı. `.md` önizleme, `.tex` tez için (booktabs). Şekiller SVG, PDF ve PNG olarak var. Metin yazılmadı (Kural 9); başlıklar yalnızca içerik etiketi.

| Dosya | Madde | Ne için | Not |
| --- | --- | --- | --- |
| `T2_klasik` | 8 | Klasik yöntemlerin koddaki uygulaması | Yöntem bölümünün uygulama paragrafına dayanak |
| `T3_ortak_faz` | 8 | Ortak fazsız RMSE ve hız: CNN–LSTM ve CD | Bağımsız Python yeniden üretimi; MATLAB çekilişi değil |
| `S1_cdf` | 10 | \|Faz hatası\| CDF'i, iki ölçütle | `.mat` gelirse `audit/scripts/step9_mat_cdf.py` birebir MATLAB eğrisini verir |
| `T1_gosterim` | 11 | Aynı mimaride sin/cos ve doğrudan açı | Tablo 1'deki "doğrudan" satırının yerine önerilen, kodu olan karşılaştırma |
| `T4_parametre` | 12–13 | Koddan sayılabilen parametreler | Ablasyonun 5 varyantı ÜRETİLEMEDİ |
| `S2_csi`, `T5_csi` | 14 | CSI hatasına gürbüzlük, hata modeli açıkça tanımlı | Makaledeki Şekil 10'un yerine; makaledeki eğri ÜRETİLEMEDİ |

Madde 9 (eğitim eğrisi) için dosya yok: eğrinin sayısal verisi MATLAB'da kaydedilmemiş. Yapılabilecek tek şey eksen etiketlerinin düzeltilmesi (yineleme; birimsiz sin/cos RMSE).

Yeniden üretim: `python3 thesis_exp/makale_kontrol/tez_ekleri/make_tez_ekleri.py` (birkaç saniye).
