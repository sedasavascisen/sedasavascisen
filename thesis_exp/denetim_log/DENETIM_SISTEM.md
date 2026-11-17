# Bağımsız denetim: gecikme farkındalıklı RIS denetleyicisi, mühürlü test (seed 41)

Denetim tarihi 17 Kasım 2026. Dal `thesis/p4-deneyler`. Denetlenen sonuç commit'i `e974718`; denetim sırasında HEAD `6797f39`.
Betik: `thesis_exp/denetim_log/sistem_denetim.py`. Komut: `PYTHONDONTWRITEBYTECODE=1 nice -n 19 python3 -W ignore thesis_exp/denetim_log/sistem_denetim.py`. Süre yaklaşık 4 s. Yük ortalaması öncesinde 0.04. Kanal üretilmedi; yalnızca `thesis_exp/sistem/cube/*.npz` okundu. Bootstrap: 2000 yeniden örnekleme, %95, kendi RNG'si (`default_rng(20261117)`).

## Özet (en üstte)

1. **FINAL.md'deki her sayı kayıtlı küplerden yeniden üretildi.** Betik 362 denetim yaptı: 0 HATA. Ortalamalar ve seçilen hatlar birebir tuttu. GA'lar en fazla 0.0071 sapıyor (periyodik A3|W0 üst sınırı), bunun nedeni farklı bootstrap tohumu.
2. **H1, H2 ve H3 kararları yeniden üretildi; üçü de TUTTU.**
   - H1'de GA alt sınırlarının en küçüğü +0.076 (K4), H3'te +0.132.
   - H2'nin sınıra en yakın koşulu taze kipte B2|W20: GA üst sınırı +0.0037. 20 farklı bootstrap tohumunda bu sınır +0.0035 ile +0.0046 arasında kaldı ve hiçbirinde negatife düşmedi.
3. **Süreç bütünlüğü sağlam.** Sıralama şöyle:
   - PROTOKOL küplerden önce commit'lendi.
   - Ek 1, seed 41'den önce commit'lendi.
   - FROZEN.md ve final_test.py, seed 41'den önce commit'lendi.
   - Seed 41 küplerinin `commit` alanı `91a03dd` ve "+dirty" eki yok.
   - Seed 41 yalnızca bir kez, kullanıcının onayından 34 s sonra üretildi.
   - Gece günlüğü 0–6 arasındaki tüm turları, başarısız olanlarla birlikte yazıyor.
4. **Makaleyle ya da FINAL.md ile çelişen bir bulgu yok.** Ancak yorumu etkileyen dört ORTA bulgu var:
   - (O1) Ek 1'in istediği "sıcak hatların katkısı" FINAL.md'de raporlanmamış. Yeniden hesaplanan değer seed 41'de +0.051 [+0.037, +0.066].
   - (O2) Periyodik kipteki +0.15…+0.52'lik farkların çoğu sıcak başlangıçtan geliyor; denetleyicinin kendisinden gelen pay küçük. K4'e de sıcak başlangıç verilirse fark **+0.020 [+0.009, +0.030]**'a iniyor.
   - (O3) K4'ün başlangıcı SU-average'a sabit. SU-best-of başlangıçlı K4'e karşı taze kipteki fark +0.097'den **+0.040 [+0.029, +0.052]**'ye iniyor.
   - (O4) Ön kayıtlı seçim kuralına göre ("seed 14'te en yüksek ortalama") dondurulması gereken sürüm, tur 3'ün b = 1.1 sapmalı sürümüydü: 5.2946, v1b ise 5.2930. Seçilen v1b oldu ve FROZEN.md bunu "kurala göre" diye yazıyor. Seed 41'de etkisi yok: v1b − sapmalı = −0.0003 [−0.003, +0.003].

## 1. Süreç zaman çizelgesi

| Zaman (UTC) | Olay | Kaynak |
| --- | --- | --- |
| 16 Kas 14:51:20 | `efc3924`: PROTOKOL.md, harness.py (seed 41 reddi dahil), GUNLUK başlığı | `git log` |
| 16 Kas 14:51:20 sonrası | Aynı komutla seed 12 küpü başlatıldı. Küp 14:54'te yazıldı, `commit` alanı efc3924. | cube/seed12.json, oturum kaydı |
| 16 Kas 14:51:25 | Oturum limiti doldu. İlk seed 14 koşusu tamamlanmadı. | oturum kaydı |
| 17 Kas 05:24 | Seed 14 yeniden üretildi (`commit` alanı dc5aa9f; harness.py değişmemişti). | cube/seed14.json, cube_14.log |
| 05:29 → 08:17 | Turlar 0–6, her biri ayrı commit'te: `961c462`, `aab7362`, `82baea0`, `458a24e`, `2bdaafd`, `47ca259`, `8e3e544`. | `git log` |
| 07:28:30 | `2bdaafd`: **Ek 1** (H3). Seed 41'den 55 dakika önce. | `git show 2bdaafd` |
| 07:57:09 | `687e2cf`: controllers.py'ye **son kod değişikliği** (K5 indeksi, taze kip için etkisiz; bkz. §3). periodic.py ve harness_warm.py'ye `--P` eklendi; P = 20 için davranış aynı. | `git show 687e2cf` |
| 08:22:26 | Kullanıcı: "mühürlü test için onaylıyorum" | oturum kaydı |
| 08:22:54 | `91a03dd`: FROZEN.md ve final_test.py. Gece döngüsünün cron işi silindi (CronDelete). | `git log`, oturum kaydı |
| 08:23:00 | Tek komut: `harness.py --seed 41 --final && harness_warm.py --seed 41 --final && final_test.py` | oturum kaydı |
| 08:26 / 08:32 | cube/seed41 ve cube/warm_seed41 yazıldı. İkisinin de `commit` alanı `91a03dd…` ve "+dirty" eki yok. | küp JSON'ları |
| 08:32:48 | `e974718`: FINAL.md, FINAL.json, küpler, kayıtlar | `git log` |

- **Kod değişmezliği:** `git diff 687e2cf 91a03dd -- thesis_exp/sistem` yalnızca FROZEN.md, GUNLUK.md, final_test.py, round6_cd.py ve P50 küpünü gösteriyor; controllers.py, periodic.py, harness*.py değişmemiş. Bağımlılıklar (`p4/`, `juri/s5/`, `tasarim_kurali/`, `juri/raw/timing2.json`, `ris_mu/`) için `git diff 961c462 e974718` boş. `e974718`'de de kod değişikliği yok, yalnızca sonuç dosyaları var.
- **Seed 41 başka yerde üretildi mi?**
  - Oturum kaydındaki tüm Bash çağrıları tarandı. `--final` ile ya da seed 41 ile yapılmış tek çalıştırma 08:23:00'teki komut.
  - `thesis_exp/` dışında `seed 41` ya da `seed41` geçen bir betik ya da kayıt yok.
  - Tasarım kuralı seed 12'de kalibre edilmiş, seed 13'te sınanmış (`tasarim_kurali/ON_KAYIT.md:36-37`).
  - Sonuç: hayır.
- **Ret mekanizması:** `harness.py:18-19` ve `harness_warm.py:15-16` `--final` olmadan seed 41'i reddediyor. `Aging` sınıfının kendisinde böyle bir koruma yok (bkz. K3).

## 2. Yeniden hesaplanan sayılar (seçme; tam liste betiğin çıktısında, 362 satır)

### 2a. Taze kip (birincil): FINAL.md ve yeniden hesap

| Kalem | Rapor | Yeniden | Durum |
| --- | --- | --- | --- |
| Senaryo sayısı | 400 | 400 | OK |
| Sistem ortalaması | 5.1241 | 5.12410 | OK |
| Kâhin / açık | 5.1267 / 0.0026 | 5.12668 / 0.00258 | OK |
| K1 / sistem − K1 [GA] | 4.6897 / +0.4344 [+0.397, +0.470] | 4.68974 / +0.43437 [+0.398, +0.474] | OK |
| K2 | 4.9568 / +0.1673 [+0.143, +0.194] | 4.95677 / +0.16733 [+0.142, +0.193] | OK |
| K3 | 4.6899 / +0.4342 [+0.393, +0.475] | 4.68994 / +0.43416 [+0.395, +0.476] | OK |
| K4 | 5.0268 / +0.0973 [+0.077, +0.118] | 5.02683 / +0.09727 [+0.076, +0.119] | OK |
| K5 | 5.0258 / +0.0983 [+0.080, +0.116] | 5.02581 / +0.09829 [+0.080, +0.116] | OK |
| H1 / H2 | TUTTU / TUTTU | TUTTU / TUTTU | OK |
| 12 koşulun her biri: sistem seçimi, değeri, en iyi karşılaştırma (yöntem, hat, değer), fark, GA, kâhin (değer, hat) | FINAL.md tablosu | 12 × 10 alan | hepsi OK; GA sapması ≤ 0.0033 |

### 2b. Periyodik kip, P = 20 ms (ikincil)

| Kalem | Rapor | Yeniden | Durum |
| --- | --- | --- | --- |
| Sistem / kâhin / açık | 5.1957 / 5.1979 / 0.0022 | 5.19569 / 5.19790 / 0.00220 | OK |
| K1 | 4.7015 / +0.4942 [+0.458, +0.530] | 4.70152 / +0.49417 [+0.460, +0.533] | OK |
| K2 | 4.9729 / +0.2228 [+0.201, +0.244] | 4.97289 / +0.22280 [+0.201, +0.245] | OK |
| K3 | 4.6753 / +0.5204 [+0.482, +0.557] | 4.67532 / +0.52037 [+0.486, +0.559] | OK |
| K4 | 5.0453 / +0.1504 [+0.132, +0.170] | 5.04528 / +0.15041 [+0.132, +0.171] | OK |
| K5 | 5.0418 / +0.1539 [+0.133, +0.174] | 5.04184 / +0.15386 [+0.134, +0.174] | OK |
| H3 | TUTTU | TUTTU | OK |
| 12 koşul, tüm alanlar | FINAL.md tablosu | | hepsi OK; GA sapması ≤ 0.0071 |

- Dondurulmuş `controllers.v1b_carrier` ve `periodic.V4` ile kendi yeniden yazımımın seçimleri 24 durumun 24'ünde aynı.
- Dondurulmuş `C.BASE` ile kendi K1–K5 yazımımın seçimleri de 24 durumun 24'ünde aynı.

### 2c. Gece günlüğü (seed 14 ve seed 12) ile FROZEN.md

| Kalem | Rapor | Yeniden | Durum |
| --- | --- | --- | --- |
| Tur 0: v0 / kâhin / açık | 5.2869 / 5.2994 / 0.0125 | 5.28689 / 5.29936 / 0.01247 | OK |
| Tur 0: K1…K5 ortalamaları | 4.8701, 5.1053, 4.8436, 5.1751, 5.1889 | 4.87012, 5.10532, 4.84357, 5.17514, 5.18887 | OK |
| Tur 0: v0 − K1…K5 ve GA'ları | +0.417 … +0.098 | +0.4168 … +0.0980, GA sapması ≤ 0.002 | OK |
| Tur 0: koşul açıkları (B1 W0, B2 W20, A4 W20) | 0.051 / 0.030 / 0.027 | 0.0507 / 0.0302 / 0.0270 | OK |
| Tur 1: v1_emp; v1_emp − v0 | 5.2880; +0.0011 [−0.008, +0.010] | 5.28796; +0.00107 [−0.008, +0.010] | OK |
| Tur 1: v1_emp koşul açıkları (A4 W20, A2 W20, B1 W0) | 0.073 / 0.033 / 0 | 0.0732 / 0.0327 / 0.0000 | OK |
| Tur 1: v1b; v1b − v0; kâhin açığı (FROZEN) | 5.2930; +0.0062 [+0.0019, +0.0105]; 0.0063 | 5.29304; +0.00616 [+0.0019, +0.0105]; 0.00631 | OK |
| Tur 2: v1b, f_d ×0.5 / ×0.8 / ×1.25 / ×2 | −0.106 / −0.009 / −0.000 / −0.058 | −0.1062 / −0.0089 / −0.0004 / −0.0582 | OK |
| Tur 3: seed 12'de b = 1.0, 1.1, 1.25, 1.5, 2.0 | 5.1247, 5.1251, 5.1203, 5.1063, 5.058 | 5.12474, 5.12512, 5.12028, 5.10634, 5.05801 | OK |
| Tur 3: seed 14 farkları (hata yok, ×0.5, ×0.8, ×1.25, ×2) | +0.0016, +0.0083, +0.0007, −0.0066, −0.0154 | +0.00155, +0.00831, +0.00070, −0.00657, −0.01538 | OK |
| Tur 4, P = 20: v4 / yalnızca taze / fark [GA] / kâhin / açık | 5.3452 / 5.2987 / +0.0465 [+0.032, +0.062] / 5.3544 / 0.009 | 5.34518 / 5.29871 / +0.04647 [+0.032, +0.061] / 5.35438 / 0.0092 | OK |
| Tur 5, P = 50: v4 / yalnızca taze / fark [GA] / kâhin | 5.3103 / 5.3165 / −0.006 [−0.022, +0.009] / 5.3265 | 5.31025 / 5.31647 / −0.0062 [−0.021, +0.009] / 5.32649 | OK |
| Tur 5: v4 − en iyi karşılaştırma (P = 20 / P = 50) | +0.143 / +0.099 | +0.1430 / +0.0993 | OK |
| Tur 5: f_d·P (3 GHz, 1.5 m/s) | ≈ 0.3 / ≈ 0.75 | 15.0 Hz × 20 ms = 0.30; × 50 ms = 0.75 | OK |
| Tur 6: v1b'nin A1 seçimleri ve değerleri | best+10 6.222; best+8 5.871 | best+10 6.2217; best+8 5.8705 | OK |
| Tur 6: CD-1 değerleri (4.943, 4.892) ve farklar | | **ÜRETİLEMEDİ.** CD hattı küpte yok; kanal üretmek gerekir, bu denetimin kısıtı da kanal üretmemekti. | — |

## 3. Mantık ve adillik

- **K1–K5 protokoldeki gibi tanımlanmış:**
  - K1 = best+0, K2 = avg+5, K3 = avg+48.
  - K4 = `rule.closed_form`. Ölçülmüş adım süresi `(lat[avg+48] − lat[avg+0])/48` = 1.0885 ms. timing2'deki `adam_slope_ms` (1.0859) ya da `adam1` (1.1539) kullanılınca K4'ün seçimleri değişmiyor (A1 10, A2 6, A3 4, A4 2, B1 2, B2 2), dolayısıyla K4 adım süresinin tanımına duyarsız.
  - K5 = 10 ms içine sığan taze hatlar arasından seed 12'de t = 0 hızı en yüksek olan; her koşulda best+6 (7.87 ms) seçiliyor. Periyodik kipte sıcak hatlar K5'ten dışlanmış (`controllers.py:48`).
  - `687e2cf`'deki K5 değişikliğinin taze kipte etkisiz olduğu doğrulandı: taze küplerde t = 0 hızları aynı taşıyıcının tüm koşullarında birebir aynı (seed 12, 14 ve 41'de `array_equal` doğru), kol listeleri de aynı.
- **Gecikme kaynağı ortak:** bütün kollar `juri/raw/timing2.json`'dan, tek iş parçacığıyla alınmış değerleri kullanıyor. Başlangıç süresi ekleniyor: SU-average 0.231 ms, SU-best-of 1.238 ms.
  - timing2'de Adam süresi başlangıcı içermiyor (`juri/timing2.py:30-37`, TH0 önceden hesaplanmış). Böylece çift sayım yok.
- **Sıcak başlangıca 0 ms başlangıç süresi verilmesi savunulabilir:**
  - Önceki faz bellekte duruyor ve Adam adımının süresi ilk noktadan bağımsız.
  - CSI edinme süresi hiçbir kola yüklenmiyor; bu herkes için eşit.
  - Önceki fazın (best+6, 7.87 ms) P = 20 ms'den önce hazır olduğu da doğru.
  - Sınır: kurgu tek bir güncelleme adımı ve önceki faz sabit (SU-best-of + Adam-6). Denetleyicinin kendi önceki çıktısıyla çok periyotlu bir kararlı durum simüle edilmedi (bkz. K5).
- **Seed 14'e uyum:** v1b'nin taşıyıcı ayrımı v1_emp'in seed 14 sonucu görüldükten sonra seçildi (`GUNLUK.md:43`, dürüstçe not edilmiş). Ampirik ψ'nin 25 kutusu ve tur 4'ün tasarımı da geliştirme verisi görülerek yapıldı.
  - Seed 41 bu seçimlerin hiçbirinde kullanılmadığı için mühürlü test bu uyumu yakalar. Kabul edilebilir.
  - Keşifsel kontrol (protokolde yok): v1b, seed 41'de v0'ı +0.011 [+0.007, +0.015], v1_emp'i +0.015 [+0.007, +0.023] geçiyor. Seed 14'te yapılan seçim yeni çekilişte de doğrulanıyor.
- **Günlüğün eksiksizliği:**
  - Cron tetiklemeleri (05:46, 06:16, 06:46, 07:16, 07:46, 08:16) 1–6 numaralı turlara, 05:29 da tur 0'a karşılık geliyor.
  - Oturum kaydında GUNLUK'a girmemiş bir seed 14 değerlendirmesi bulunmadı.
  - Başarısız ve anlamsız sonuçlar da yazılmış: v1_emp anlamsız, tur 3 reddedildi, tur 5'te P = 50'de kazanç yok, tur 6 reddedildi. Fikir 5 (geniş bant) "kalan" olarak bırakılmış.

## 4. Bulgular

### KRİTİK

Yok.

### ORTA

- **O1. Ek 1'in istediği rapor eksik.**
  - Sorun: `PROTOKOL.md` Ek 1, "Ayrıca raporlanır: sıcak hatların taze-yalnız sisteme katkısı" diyor; `final_test.py` bu katkıyı hesaplamıyor, `FINAL.md` de vermiyor.
  - Yeniden hesap (seed 41, P = 20): V4 5.1957, yalnızca taze 5.1445, fark **+0.0511 [+0.037, +0.066]**.
  - Düzeltme: bu satır ayrı bir ek rapor olarak eklenmeli. FINAL.md'ye dokunulmaz.
- **O2. H3'teki büyük farklar sıcak başlangıçtan geliyor; denetleyicinin kendisinden gelen pay küçük.**
  - Sorun: Ek 1'e göre K1–K5 yalnızca taze hatlarla çalışıyor. Bu yüzden periyodik kipteki "+0.15…+0.52" (commit `e974718` mesajı, FINAL.md:39-45) büyük ölçüde sıcak başlangıcın değeri.
  - Keşifsel ölçüm (ön kayıtlı değil): aynı karşılaştırma yöntemlerine sıcak başlangıç verilince fark K4'te (warm+L_K4) **+0.020 [+0.009, +0.030]**, K2'de (warm+5) +0.101 [+0.086, +0.117], K5'te (warm+6) +0.121 [+0.104, +0.137].
  - Düzeltme: H3 "denetleyici artı sıcak başlangıç, sıcak başlangıçsız karşılaştırma yöntemlerini geçiyor" diye okunmalı. Denetleyicinin kendi katkısı O1'deki ve buradaki rakamlarla birlikte verilmeli.
- **O3. K4'ün başlangıcı SU-average'a sabit.**
  - Protokole uygun, ama sistem SU-best-of'tan başlamayı seçebiliyor.
  - Aynı kapalı form SU-best-of'tan başlatılırsa fark taze kipte **+0.040 [+0.029, +0.052]**, periyodik kipte +0.097 [+0.078, +0.116] oluyor. K4'e karşı kazancın yaklaşık %59'u yalnızca başlangıç seçiminden geliyor.
  - Ek olarak: seed 12'de seçilip her koşulda sabit tutulan tek hat (best+3) seed 41'de 5.0370 veriyor. Bu, K4 ve K5'ten güçlü bir taban çizgisi; sistem onu da +0.087 [+0.072, +0.102] geçiyor.
  - Düzeltme: bu iki güçlü taban çizgisi keşifsel ek olarak raporlanmalı (CLAUDE.md'deki "zayıf taban çizgisi" kuralı). H1 bunlara karşı da sağlanıyor, ama farkın büyüklüğü daha küçük.
- **O4. Ön kayıtlı seçim kuralından sapma.**
  - Sorun: `PROTOKOL.md` gece kuralı 2 "seed 14'te ortalaması en yüksek olan sürüm dondurulur" diyor. Tur 3'ün sapmalı sürümü (b = 1.1) seed 14'te 5.2946, v1b ise 5.2930. v1b "anlamlı kazanç yok" gerekçesiyle seçildi (`GUNLUK.md:79`), ama `FROZEN.md:10` seçimi "kurala göre" diye sunuyor.
  - Etkisi: seed 41'de v1b − sapmalı = −0.0003 [−0.003, +0.003], yani sonuçları değiştirmiyor.
  - Düzeltme: sapma, gerekçesiyle birlikte açıkça not edilmeli.

### KÜÇÜK

- **K1. Bootstrap'ın tanımı.**
  - Sorun: protokol (`PROTOKOL.md`, H1) "koşullar ve senaryolar üzerinden" bootstrap diyor. Uygulama (`controllers.py:144-148`, `final_test.py:26`) koşulları sabit tutuyor ve yalnızca 400 senaryoyu eşli olarak yeniden örnekliyor. Bootstrap tohumu `p4/common.py:90`'da modül düzeyinde (0) ve çağrı sırasına bağlı.
  - Düzeltme: protokol metnine uygun bir açıklama eklenmeli ve tohumun kaydı açıkça tutulmalı.
- **K2. H2 bir eşdeğerlik kanıtı değil.**
  - Sorun: H2 "anlamlı olarak kötü değil" diyor; marjı olan bir eşdeğerlik testi değil. A4|W20'nin GA'sı [−0.048, +0.040] geniş. H2'nin sınıra en yakın koşulu B2|W20: üst sınır +0.0037.
  - Düzeltme: metin "eşit ya da daha iyi" diye yazılmamalı.
- **K3. Seed 41'e karşı koruma yalnızca harness betiklerinde.**
  - Sorun: koruma harness.py ve harness_warm.py'de var. `p4/common.Aging` seed 41'i kabul ediyor; `round6_cd.py` gibi doğrudan kanal üreten betikler korumasız.
  - Durum: oturum kaydına göre ihlal yok.
- **K4. Gecikme ölçümüyle ilgili iki zayıflık.**
  - Ara L değerlerinin (3, 5, 6, 10, 12, 20, 24) Adam süresi ölçülmemiş, doğrusal enterpolasyonla bulunmuş (`harness.py:22-23`).
  - timing2 ölçümünde turlar boyunca yük 0.28'den 0.74'e çıkmış; CLAUDE.md eşiği 0.5. Yük tüm kolları birlikte etkiliyor.
  - Bunlar önceden var olan durumlar; raporda belirtilmeli.
- **K5. Periyodik kipin kurgusu tek adımlı.**
  - Kurguda tek bir güncelleme var ve önceki faz sabit (`harness_warm.py:35`).
  - Ölçüt (Tanım 1) [P, P + τ] aralığında hâlâ geçerli olan eski fazı saymıyor. Bu, protokolün tanımı ve bütün kollar için aynı, ama "periyodik çalışma" genellemesinin bir sınırı.
- **K6. Kayıt izlenebilirliği.**
  - `warm_seed12/14` küplerinin `commit` alanı `577fd91`, oysa harness_warm.py o anda izlenmiyordu. İlk kez `2bdaafd`'de commit'lendi; kod aynı, oturum kaydındaki Write içeriğiyle karşılaştırılarak doğrulandı. `commit()` izlenmeyen dosyaları "+dirty" saymıyor.
  - `__pycache__/*.pyc` dosyaları commit'lenmiş.
  - Mühürlü koşu sırasında çıktılar geçici olarak `.git/info/exclude`'a eklenmiş (oturum kaydı, 08:23:14), sonra kaldırılmış. Bunun sonuca etkisi yok.
- **K7. GUNLUK'ta veriyle sınırlı ifadeler.**
  - `GUNLUK.md:60`, "küçük kestirilen f_d fazla adım attırıyor": mekanizma seçimlerle gösterilmemiş.
  - `GUNLUK.md:123-124`, "daha hızlı koşullarda CD'nin konumu ancak kötüleşir" ve "hiçbir koşulda rekabetçi değil": yalnızca A1'de sınandı, gerisi çıkarım ya da Makale 2'ye atıf.
  - `GUNLUK.md:59`, "±%20–25 zararsız": yalnızca iki noktaya (×0.8, ×1.25) ve geliştirme verisine (seed 14) dayanıyor.
  - Sağlamlık sonuçları seed 41'de sınanmadı. Mühürlü sonuç gerçek f_d'nin bilindiği varsayımına dayanıyor.

## 5. Aşırı iddia denetimi

- **FINAL.md:** yalnızca sayılar ve kararlar var, hepsi doğru. Abartı yok; tek eksik O1. "Gece hiç kullanılmadı" ifadesi oturum kaydıyla doğrulandı.
- **Commit `e974718` mesajı** ("+0.10..+0.43", "+0.15..+0.52"): sayılar doğru. Periyodik kip için O2'deki çerçeve uyarısı geçerli.
- **FROZEN.md:** sayılar doğru (5.2930 / 0.0063 ve 5.3452 / 0.009). Seçim kuralına ilişkin cümle için O4 geçerli.
- **GUNLUK.md:** tüm sayılar doğru; ifade sınırları K7'de.
