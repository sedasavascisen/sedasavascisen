# Makale 2 Tablo III — periyodik çalışmada pilot ve devreye alma yuvarlaması (denetim K4)

Rapor commit'i `238d846`. Yayımlanmış `scripts/mumiso_tracking.py` (Tablo III) 0.5 ms ızgarada pilot süresini `round(t_p/0.5)` örneğe, devreye alma anını en yakın ızgara noktasına yuvarlıyor; 0.86 / 1.71 / 3.43 ms pilotlar ızgara üstü döngülerde 1.0 / 1.5 / 3.5 ms ücretleniyor ve hata döngü uzunluğuna (kola) göre değişiyor. `run.py` bu betiğin kopyası (yayımlanmış betiğe dokunulmadı): `--fix 0` aynı mantık, `--fix 1` kesirli pilot ücreti ve tam devreye alma anı. **Yeniden üretim:** `--fix 0`, T_p = 0.86 ms'de yayımlanmış dosyayla en fazla 0.0e+00 fark (birebir). Diğer her şey (senaryolar, adımlar, periyotlar, 100–200 ms penceresi, bootstrap, seçimin raporlanan kümede yapılması) yayımlanmış betikle aynı.

## 1) Sıcak − soğuk (en iyi politika vs en iyi politika)

| T_p (ms) | Yayımlanmış [%95 GA] | Düzeltilmiş [%95 GA] | Fark |
| --- | --- | --- | --- |
| 0 | +0.5236 [+0.495, +0.554] | +0.5275 [+0.499, +0.557] | +0.0038 |
| 0.86 | +0.2224 [+0.192, +0.253] | +0.2760 [+0.244, +0.308] | +0.0536 |
| 1.71 | +0.1456 [+0.097, +0.198] | +0.0919 [+0.042, +0.145] | -0.0537 |
| 3.43 | +0.0077 [-0.035, +0.050] | +0.0077 [-0.027, +0.041] | +0.0000 |

## 2) En iyi politikalar

| T_p | Kip | Yayımlanmış: U, L, hız | Düzeltilmiş: U, L, hız [%95 GA] | Arka arkaya en iyi L (yay. / düz.) |
| --- | --- | --- | --- | --- |
| 0 | soğuk | b2b, 3, 5.8334 | b2b, 3, 5.8288 [5.6038, 6.0641] | 3 / 3 |
| 0 | sıcak | b2b, 2, 6.3570 | b2b, 2, 6.3563 [6.1258, 6.5949] | 2 / 2 |
| 0.86 | soğuk | 20.0, 4, 5.1997 | 20.0, 3, 5.2389 [5.0239, 5.4648] | 6 / 6 |
| 0.86 | sıcak | 10.0, 3, 5.4221 | 10.0, 3, 5.5149 [5.3065, 5.7314] | 6 / 4 |
| 1.71 | soğuk | b2b, 48, 5.0883 | b2b, 48, 5.0775 [4.8528, 5.3111] | 48 / 48 |
| 1.71 | sıcak | 20.0, 3, 5.2339 | 20.0, 3, 5.1694 [4.9587, 5.3845] | 48 / 48 |
| 3.43 | soğuk | b2b, 48, 4.9783 | b2b, 48, 4.9820 [4.7610, 5.2127] | 48 / 48 |
| 3.43 | sıcak | 80.0, 8, 4.9860 | 80.0, 24, 4.9898 [4.7696, 5.2269] | 48 / 48 |

## 3) Komut ve ham çıktı

`OMP_NUM_THREADS=1 python3 thesis_exp/p4/takip_duzeltme/run.py --fix {0,1} --pilot {0,0.86,1.71,3.43}` → raw/fix{0,1}_tp*.json, *.log. Betik koşudan önce commit'lendi.

## 4) Yorum (bulgulardan ayrı)

- **Makale 2 Tablo III'ün büyüklükleri değişiyor, hükümleri değişmiyor.**
  - Sıcak − soğuk, T_p = 0.86 ms: 0.222 → 0.276.
  - Sıcak − soğuk, T_p = 1.71 ms: 0.146 → 0.092.
  - T_p = 0 ve 3.43 ms'de fiilen aynı: 3.43 ms'de iki değer de 0.008 ve GA sıfırı içeriyor.
  - Sıcak başlangıcın üstünlüğünün işareti her T_p'de korunuyor. Pilot süresi arttıkça üstünlüğün küçülmesi örüntüsü de korunuyor.
  - 0.86 ve 1.71 ms'de büyüklük, yayımlanmış GA genişliği kadar ya da daha fazla kayıyor.
- **Kaynak:** Pilot süresinin ve devreye alma anının 0.5 ms ızgarasına yuvarlanması. Hata döngü uzunluğuna bağlı olduğu için kollar arasında tarafsız değil. Bu, Deney 4.3'te bulunan yuvarlama yanlılığıyla (H7) aynı sınıf.
- **Düzeltilmeyen ama not edilen (denetim U58):** Yayımlanmış betik en iyi politikayı raporlanan kümede seçiyor. Burada da karşılaştırılabilirlik için aynı yapıldı. Köprü raporundaki kopya seçimi seed 12'de yapıyor.
- **Etkilenen ama yeniden koşulmayan:** Köprü raporunun periyodik çalışma bölümündeki ağ kolu (thesis/bridge dalı, `bridge_tracking.py`) aynı yuvarlamayı kullanıyor. Eğitilmiş ağ başka bir dalda olduğu için bu gece yeniden koşulmadı; köprünün periyodik sayıları düzeltilmiş değil (ÜRETİLEMEDİ — henüz). Denetçinin analitik tahmini ölçüm olmadığı için burada aktarılmıyor.
- **Öneri:** Tezde Tablo III'ün düzeltilmiş değerleri kullanılmalı. Makale 2 hakem sürecindeyse, hakem sorarsa yanıt olarak bu kopya hazır.
