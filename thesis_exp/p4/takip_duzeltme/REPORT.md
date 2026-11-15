# Makale 2 Tablo III — periyodik çalışmada pilot ve devreye alma yuvarlaması (denetim K4)

Rapor commit'i `c1ee010`. Yayımlanmış `scripts/mumiso_tracking.py` (Tablo III) 0.5 ms ızgarada pilot süresini `round(t_p/0.5)` örneğe, devreye alma anını en yakın ızgara noktasına yuvarlıyor; 0.86 / 1.71 / 3.43 ms pilotlar ızgara üstü döngülerde 1.0 / 1.5 / 3.5 ms ücretleniyor ve hata döngü uzunluğuna (kola) göre değişiyor. `run.py` bu betiğin kopyası (yayımlanmış betiğe dokunulmadı): `--fix 0` aynı mantık, `--fix 1` kesirli pilot ücreti ve tam devreye alma anı. **Yeniden üretim:** `--fix 0`, T_p = 0.86 ms'de yayımlanmış dosyayla en fazla 0.0e+00 fark (birebir). Diğer her şey (senaryolar, adımlar, periyotlar, 100–200 ms penceresi, bootstrap, seçimin raporlanan kümede yapılması) yayımlanmış betikle aynı.

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

## 2b) Köprü raporunun periyodik çalışması (thesis/bridge, bridge_tracking.py)

Aynı düzeltme, köprü betiğinin kopyasına (`bridge_tracking_fix.py`; girdiler thesis/bridge dalının salt okunur çalışma ağacından) uygulandı. Yeniden üretim (`--fix 0`, T_p = 0.86): birebir. Seçim seed 12, rapor seed 11 (köprü betiğindeki gibi).

| T_p | Ağ − soğuk: yayımlanmış [%95 GA] | düzeltilmiş [%95 GA] | Ağ − sıcak: yayımlanmış [%95 GA] | düzeltilmiş [%95 GA] |
| --- | --- | --- | --- | --- |
| 0 | -0.212 [-0.226, -0.197] | -0.204 [-0.218, -0.189] | -0.672 [-0.707, -0.638] | -0.669 [-0.704, -0.635] |
| 0.86 | -0.153 [-0.179, -0.129] | -0.120 [-0.138, -0.102] | -0.354 [-0.389, -0.320] | -0.391 [-0.426, -0.357] |
| 1.71 | -0.105 [-0.140, -0.069] | -0.129 [-0.172, -0.086] | -0.255 [-0.301, -0.210] | -0.225 [-0.270, -0.181] |
| 3.43 | -0.131 [-0.167, -0.095] | -0.128 [-0.164, -0.092] | -0.150 [-0.193, -0.108] | -0.150 [-0.193, -0.107] |

## 3) Komut ve ham çıktı

`OMP_NUM_THREADS=1 python3 thesis_exp/p4/takip_duzeltme/run.py --fix {0,1} --pilot {0,0.86,1.71,3.43}` → raw/fix{0,1}_tp*.json, *.log. Köprü: `OMP_NUM_THREADS=1 python3 thesis_exp/p4/takip_duzeltme/bridge_tracking_fix.py --fix {0,1} --pilot ...` → raw/bridge_fix*_tp*.json. Betikler koşudan önce commit'lendi.

## 4) Yorum (bulgulardan ayrı)

- **Makale 2 Tablo III'ün büyüklükleri değişiyor, hükümleri değişmiyor.**
  - Sıcak − soğuk, T_p = 0.86 ms: 0.222 → 0.276.
  - Sıcak − soğuk, T_p = 1.71 ms: 0.146 → 0.092.
  - T_p = 0'da +0.524 → +0.528 (makalenin iki basamaklı tablosunda 0.52 → 0.53; `tab_tracking.tex` ve §6'daki "up to 0.52" buna göre 0.53 olur). 3.43 ms'de iki değer de 0.008 ve GA sıfırı içeriyor.
  - Sıcak başlangıcın üstünlüğünün işareti her T_p'de korunuyor. Pilot süresi arttıkça üstünlüğün küçülmesi örüntüsü de korunuyor.
  - 0.86 ve 1.71 ms'de kayma (0.054) yayımlanmış GA'nın yarı genişliğinden (0.030 / 0.051) büyük, tam genişliğinden (0.061 / 0.101) küçük. Yayımlanmış ile düzeltilmiş arasındaki fark için eşli bir GA hesaplanmadı (denetim U60).
  - **Değişen tablo hücreleri (denetim U61; tam satırlar §2'de):** 0.86 ms soğukta seçilen L 4 → 3, 3.43 ms sıcakta L 8 → 24; hız hücreleri de değişiyor (örn. 0.86 ms sıcak 5.42 → 5.51). Makalenin §6'daki beş nitel iddiası düzeltilmiş veride de tutuyor.
- **Kaynak:** Pilot süresinin ve devreye alma anının 0.5 ms ızgarasına yuvarlanması. Hata döngü uzunluğuna bağlı olduğu için kollar arasında tarafsız değil. Bu, Deney 4.3'te bulunan yuvarlama yanlılığıyla (H7) aynı sınıf.
- **Düzeltilmeyen ama not edilen (denetim U58):** Yayımlanmış betik en iyi politikayı raporlanan kümede seçiyor. Burada da karşılaştırılabilirlik için aynı yapıldı. Köprü raporundaki kopya seçimi seed 12'de yapıyor.
- **Köprünün periyodik ağ kolu da düzeltildi (§2b):** Ağ her T_p'de hem soğuk hem sıcak başlangıçlı Adam'ın gerisinde; hüküm aynı. Ağ − soğuk: 0.86 ms'de −0.153 → −0.120, 1.71 ms'de −0.105 → −0.129; 0 ve 3.43 ms'de fiilen aynı. Denetçinin önceden verdiği analitik tahmin (0.86 ms'de ≈ −0.066) ölçümle tutmadı; bu yüzden tahminler ölçüm yerine kullanılmamalı.
- **Öneri:** Tezde Tablo III'ün düzeltilmiş değerleri kullanılmalı. Makale 2 hakem sürecindeyse, hakem sorarsa yanıt olarak bu kopya hazır.
- **Sağlamlık kontrolleri (denetim U59, U62; 15 Kasım):**
  - **Yeniden üretim:** `--fix 0` dört T_p'nin hepsinde, hem Tablo III betiğinde hem köprü betiğinde yayımlanmış sonuçlarla birebir (en büyük fark 0).
  - **Tam entegrasyon (U59):** `--fix 1` pilot ücretini, örnekteki eski ve yeni fazın karışımına orantılı düşüyor. Pilotun yalnızca veri zamanından düşüldüğü tam entegrasyonla (`exact_full_check.py` → `raw/exact_full_tp*.json`) politika başına en büyük fark 0.0072 b/s/Hz.
  - Seçilen politikalar ve ayırt edilemeyen kümeler aynı; sıcak − soğuk farkı en fazla 0.00006 değişiyor.
