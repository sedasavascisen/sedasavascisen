# Makale 2: gönderim öncesi son bağımsız denetim (16 Kasım 2026)

**Denetlenen:** `thesis_exp/makale2_revizyon/` (tex, `sections/`, `tables/`, derlenmiş PDF). Özgün `paper_mobility/` yalnızca okundu.

**Koşullar**
- Dal `thesis/p4-deneyler`, HEAD `1799123`. Çalışma ağacı denetim boyunca temiz kaldı; bu dosya dışında hiçbir dosya yazılmadı.
- `scripts/audit_claims.py --all`: 126/126.
- Yük ortalaması 0.09. Zamanlama ya da deney koşturulmadı.
- `make_tab_tracking_corrected.py` scratchpad'deki bir kopyada koşturuldu. Çıktısı `tables/tab_tracking.tex` ile bayt bayt aynı.
- `kaynak_farki.diff`, `git diff --no-index paper_mobility thesis_exp/makale2_revizyon` ile yeniden üretildi. Eklenen ve silinen satırlar birebir aynı, yani fark dosyası güncel.
- PDF, tex'ten sonra derlenmiş (07:26:27, `section_05` 07:26:26). `pdftotext` metni yeni §V ve §VI-H cümlelerini aynen içeriyor.

**Ham dosyalar ve commit'leri**

| Dosya | Commit |
|---|---|
| `p4/izgara_kontrol/raw/results_tab1.json` | d79ea55 |
| `p4/izgara_kontrol/raw/results.json` | 98ed4bd |
| `p4/onkodlayici_siralama/raw/results.json` | a0ac494 |
| `p4/onkodlayici_siralama/raw/results_win25.json` | 66aa57b |
| `p4/onkodlayici_siralama/raw/results_win100.json` | a6692d2 |
| `p4/kusurlu_csi/raw/results.json` | 06fc9d2 |
| `p4/onkodlayici_csi/raw/results.json` | 97e5e5c |
| `p4/ayrik_faz/raw/results_exact.json` | 1847597 |
| `p4/ayrik_faz/raw/results_3bit.json` | e9bf18b |
| `p4/takip_duzeltme/raw/fix1_tp*.json` | 238d846 |
| `origin/thesis/altyapi:thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json` | (dalda) |

---

## KRİTİK

### K1. §VI-H'nin $\bar R_W$ ölçütünde koordinat inişi SU-best-of'un gerisinde değil; bazı koşullarda anlamlı olarak önünde. Makale bunu söylemiyor, Özet ve Sonuç'un 1. maddesi ise tersini ima ediyor.

**Kural:** CLAUDE.md, 11 Kasım kuralı 10: makaledeki iddiayla çelişen bulgu yumuşatılmaz.

**Makalenin iddiaları**
- **Özet:** *"First, coordinate descent and long-run Adam … lose to a 2.5 ms single-user heuristic."* Hemen ardından: *"Charging the pilots for a fresh precoder lowers rates but leaves the slow solvers behind."*
- **Sonuç 1:** *"Speed beats precision. The solvers with the best rate on paper lose to a single-user heuristic … even with a tuned number of coordinate sweeps."*
- **Sınırlılıklar:** *"Charging the effective-channel pilots lowers absolute rates by 17–32% without moving the slow solvers ahead."*
- **§VI-H:** *"coordinate descent and long-run Adam are significantly behind"* (seçilen Adam'a göre; bu kısım doğru).

**Ham veri** (`onkodlayici_siralama/raw/*.json`, satır `CD`, alan `minus_su_best_of` ve `_ci`; 400 senaryo, eşli bootstrap 2000):

| W | Kol | CD − SU-best-of | %95 GA | Sonuç |
|---|---|---|---|---|
| 50 ms | taze (pilotsuz) | **+0.100** | [+0.014, +0.190] | CD anlamlı olarak **önde** |
| 50 ms | 15 kHz | +0.001 | [−0.073, +0.071] | berabere |
| 50 ms | 30 kHz | +0.032 | [−0.043, +0.109] | berabere |
| 50 ms | 60 kHz | +0.035 | [−0.047, +0.115] | berabere |
| 100 ms | taze | **+0.184** | [+0.104, +0.263] | CD önde |
| 100 ms | 15 kHz | +0.052 | [−0.012, +0.117] | berabere |
| 100 ms | 30 kHz | **+0.090** | [+0.025, +0.159] | CD önde |
| 100 ms | 60 kHz | **+0.097** | [+0.030, +0.169] | CD önde |
| 25 ms | 15 kHz | −0.083 | [−0.168, −0.004] | CD geride |
| 25 ms | 30 / 60 kHz, taze | −0.07 / −0.07 / −0.04 | GA'ların hepsi sıfırı içeriyor | berabere |

- Uzun Adam yalnızca W = 100 ms'nin taze kolunda SU-best-of ile berabere: −0.142 [−0.311, +0.019]. Diğer kollarda geride.
- Makalenin kendi W = 50 ms tasarımında (taze ve üç numeroloji) koordinat inişi SU-best-of'un hiçbir kolda gerisinde değil.
- Makalenin ana bulgusu "koordinat inişi 2.5 ms'lik sezgisele kaybeder" (Tablo I: SU-best-of − CD = +0.297 [0.204, 0.390]). Faz bir süre tutulduğunda ve ortalama alındığında bu bulgu tersine dönüyor ya da kayboluyor.
- Fast yöntemlerin (Adam 3–20 adım) koordinat inişini yendiği doğru. Bu yüzden "latency decides which method is best" tezi ayakta kalıyor. Kaybolan şey, özetteki birinci bulgunun ve Sonuç 1'in "single-user heuristic" karşılaştırması.

**Aynı yönde ikinci bulgu: 1 bit** (`ayrik_faz/raw/results_exact.json`, `bits.1.lr0.5`)
- dCD-2…8 − SU-best-of→q değerlerinin GA'larının hepsi sıfırı içeriyor. Örnek: dCD-2 +0.064 [−0.037, +0.154], dCD-8 −0.018 [−0.115, +0.079].
- dCD-1 ise sezgiselin anlamlı olarak önünde: +0.25 [0.16, 0.33].
- Yani 1 bitte, "tuned number of coordinate sweeps" ile koordinat inişi yuvarlanmış sezgisele kaybetmiyor.
- §VI-H yalnızca dCD-1'i söylüyor. "Significantly behind … at b=3, and at b=2 with two or more sweeps" cümlesinin 1 bit için ne dediği okura bırakılmış.

**Hafifletici, ama makalede yazılmamış:** Koordinat inişi bu deneyde 703 ms'de devreye giriyor ve [703, 753/803] ms aralığında ortalanıyor. Bu, makalenin 200 ms "reliable horizon"unun ötesi. Sabit saçıcılar yüzünden değerler iyimser (Tablo I'deki † mantığı). Tersine dönüşün bir kısmı bu iyimserlikten geliyor olabilir. Bu ayrıştırma **ÜRETİLEMEDİ**: ham veride ufuk içi ya da dışı ayrımı yok.

**Gereken:** §VI-H'ye bir cümle eklenmeli. Önerilen metin:
> "On this metric coordinate descent is no longer behind SU-best-of (W = 50 ms: +0.00 to +0.10, significant only with free refresh; W = 100 ms: up to +0.18), although its window lies beyond the reliable horizon; only the fast Adam configurations stay ahead of it."

Sonuç 1 "with the phase evaluated at its deployment instant (Definition 1)" ile sınırlanmalı. Özetteki cümle de "leaves the slow solvers behind tuned Adam" biçiminde yazılmalı. Özet 200 kelimede olduğu için bu bir kelime çıkarmayı gerektirir (bkz. U1).

---

## UYARI

### U1. Özet tam 200 kelime; TWC'ye özgü sınır da 75–200, yani pay sıfır.
- Kaynakta (`\emph` açılmış, `~` boşluk sayılmış) 200 kelime. `pdftotext` ile de 200 ("Abstract—" ve "Index Terms" hariç).
- `DEGISIKLIKLER.md` "198 kelime" diyor. Benim sayımım 200.
- Gönderim formunun sayacı "0.9–5.9 s" ya da "2.5 ms" gibi ifadeleri farklı sayarsa sınır aşılabilir. K1 için yapılacak değişiklikte en az 2–3 kelime çıkarılmalı. Örneğin "in a standardized indoor-office" yerine "in an indoor-office" (−1).

### U2. "the sweep of Fig. 3 by at most 0.027": Şekil 3'ün Armijo eğrisi ve L = 3 noktası kontrol edilmemiş.
- **Kontrol edilenler:** `izgara_kontrol/run.py`'nin `STEPS` listesi {1, 2, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48}. Bu kollarda en büyük |tam − interp.| 0.0272 (Adam-32), yani doğru.
- **Kontrol edilmeyenler:**
  - Şekil 3 L = 3'ü de çiziyor (4.99 ms). Izgara noktası 5.0 ms'ye çok yakın olduğu için etki büyük olasılıkla küçük.
  - Şekil 3 Armijo eğrisini de çiziyor: 12 nokta, 2.09 ms/adım. Bunlar 53–100 ms'deki 25 ms'lik ızgara boşluklarına düşüyor.
- Armijo'nun tam gecikmedeki farkı **ÜRETİLEMEDİ**.
- Ayrıca §VI-B'deki "two peaks are statistically tied (difference 0.033, CI −0.001 to 0.064)" ifadesinde GA'nın alt ucu sıfıra 0.001 uzaklıkta. Tam değerlendirmede Adam-4 +0.0045 kayıyor. Hüküm sınırda, ama değerlendirilmedi.
- **Öneri:** cümleyi "the Adam sweep of Fig. 3" ile sınırla ya da Armijo'yu `izgara_kontrol`'e ekle.

### U3. Kusurlu CSI'da hızlar çöküyor; makale yalnızca 30 dB değerini veriyor ve "tied" diyor.
- **Ham değerler** (`kusurlu_csi/raw/results.json`, seçilen kol, test):

| ρ | Seçilen kol | Hız (b/s/Hz) |
|---|---|---|
| kusursuz | Adam-6 | 6.08 |
| 30 dB | Adam-3 | 3.54 |
| 20 dB | Adam-5 | **1.40** |
| 10 dB | Adam-4 | **0.30** |
| 5 dB | Adam-20 | 0.16 |
| 0 dB | Adam-5 | 0.12 |

- 20 dB'de en iyi hız, makalenin "No RIS" değerinin (1.744, kusursuz CSI) altında. Pilot ve CSI birlikte uygulandığında (`onkodlayici_csi`) 20 dB'de 1.02–1.15.
- "At 10 dB and below Adam and SU-best-of are tied" doğru: −0.007 [−0.037, +0.024], −0.006 [−0.025, +0.014], −0.001 [−0.012, +0.011]. Ancak bu bir taban etkisi; bütün yöntemler 0.1–0.3 b/s/Hz'ye düşmüş.
- Editör denetiminin K5'te sorduğu fiziksel açıklama da metne girmemiş: 30 dB'de, yani 10⁻³ bağıl hatada, %42 kayıp. Büyük olasılıkla yüksek SNR'de ZF'nin artık girişimle sınırlı olmasından kaynaklanıyor, ama bu doğrulanmadı.
- Hakem bunu soracaktır. Bir yan cümle önerilir: "(rates at 20 and 10 dB: 1.40 and 0.30 b/s/Hz; residual inter-user interference of the zero-forcing precoder dominates)". Neden kısmı doğrulanmadan yazılmamalı.

### U4. "per-scenario median 22.6 dB at ρ = 30 dB" yalnızca RIS–kullanıcı kanalı G için geçerli.
- `denetim_log/scripts/u13_csi_rel_err.out`, seed 11, G kanalı: medyan 22.6 dB, %5 dilimi 11.5 dB.
- Aynı ölçekleme F için yaklaşık 25.3 dB (oran 2.92), doğrudan kanal için yaklaşık 23.7 dB (oran 4.31) verir. Bu iki değer dosyadaki oranlardan hesaplandı; dosyada dB olarak yazılı değil.
- Metin "(… for the RIS–user channels)" demeli.

### U5. W = 100 ms cümlesi: "at 100 ms six steps lie 0.02–0.04 b/s/Hz below"
- **Ham değerler** (`results_win100.json`, Adam-6 − seçilen):
  - 15 kHz: −0.0215 [−0.052, +0.008] (anlamlı değil)
  - 30 kHz: −0.0375 [−0.070, −0.004]
  - 60 kHz: −0.0406 [−0.076, −0.003]
- Bu üç değer için cümle doğru. Ancak aynı cümledeki parantez "(16–24 with free refresh)" taze kolu da anıyor. Taze kolda Adam-6, seçilen Adam-24'ün **0.069** gerisinde.
- "With pilots charged" eklenmeli. Sonuç 2'deki "moves the flat optimum to 16–20 steps" ifadesi de taze kolda 24.

### U6. "Data and Code Availability": "The scripts that generate every table and figure … are available at https://github.com/…/ris-latency-mobility"
- Tablo III ile §VI-H sayıları `thesis_exp/p4/` ve `thesis_exp/infra/` (dal `thesis/altyapi`) altındaki betiklerden geliyor.
- `make_paper_assets.py` hâlâ `results/mumiso_tracking.json`'u okuyor ve koşturulursa eski Tablo III'ü yazar.
- Genel depoda bu betiklerin bulunduğu buradan doğrulanamadı. Gönderimden önce depoya eklenmeli, yoksa bu cümle yanlış olur.

### U7. §VI-H'nin "independent mobility draw" tohumu metinde yok.
- §V-A "All sets use seed 11 unless stated otherwise" diyor. Bağımsız çekiliş seed 12 (`run.py` docstring'leri), ama metinde yazmıyor.
- "(seed 12)" eklenmesi bir sözcük tutar.

### U8. Kalan dil ve tutarlılık sorunları (küçük)
- **§VI-H:** "Adam with 3–20 steps is tied with it (6–8 steps)". "It" ile parantezin ilişkisi belirsiz. Öneri: "the selected configuration (Adam, 6–8 steps) is tied with Adam at 3–20 steps".
- **§VI-H:** "at 15, 30 and 60 kHz". §V-D ile tutarlılık için "subcarrier spacing" eklenmeli.
- **§VI-H:** "four data-free pilot symbols" olağandışı bir ifade. Öneri: "four pilot symbols (no data)".
- **§VI-H:** "the phase computed from the $t=0$ estimate and the precoder from a fresh one" mutlak yapısı ağır okunuyor. Editör denetiminin KÜÇÜK 5. maddesi giderilmemiş.
- **§V-C:** "this value lies within the 1.49–2.02 ms measured here. A later … re-measurement … gives 1.33 ms". 1.33'ün bu aralığın dışında kaldığı ve ana sonuçların neden 1.66 ile verildiği söylenmiyor. Hakem bunu sorar (editör KÜÇÜK 6).
- **Tablo III:** 0.86 ms satırında 5.51 − 5.24 = 0.27, fark sütunu +0.28 (ham değer 0.2760). Bilinçli olarak bırakılmış, not olarak duruyor.

---

## DOĞRULANDI

**§V, Tablo I tam gecikme notu** (`results_tab1.json`)
- Interpolasyon yayımlanmış Tablo I'i veriyor: en büyük fark 0.0005, SU-best-of 5.2718 karşısında 5.272.
- Güven ufkunun içindeki tam − interp. farkları: SU-average +0.00003, SU-best-of +0.0024, Adam-8 0, Adam-12 −0.0001, Adam-16 0, Adam-20 **−0.0061**. "At most 0.006" doğru (0.00606).
- Ufkun ötesi: koordinat inişi −0.0081 [−0.093, +0.073], uzun Adam −0.0374 [−0.125, +0.061]. "0.008 and 0.037" doğru.
- Not: Bu tam değerlerle SU-best-of − CD 0.307, SU-best-of − uzun Adam 0.644 oluyor. Metindeki 0.297 ve 0.604 bunların GA'ları içinde. Cümle bu farklardan söz etmiyor.

**§V, Şekil 3 taraması ve optimum** (`results.json`, `paper` kümesi)
- Ölçülen kollarda en büyük fark 0.0272 (Adam-32).
- $L^\star$ interpolasyonla Adam-5, tam değerle Adam-4. "Stays at 4–6" doğru.
- L = 48'in maliyeti 13.99 → **14.20%**. "14.2%" doğru; Özetteki "14%" doğru.
- Önceki sayısal denetimin K1'i (L* değişmiyor iddiası) giderilmiş.

**§V, yeniden ölçüm** (`mumiso_mobility_latency_rerun.json`)
- 1 iş parçacığı, `load_before` 0.45, eğim 1.328 ms/adım → 1.33 doğru.
- `rerun` kümesinde tam değerlerle: $L^\star$ = Adam-6, %14.93, SU-best-of − CD 0.2616 [0.147, 0.373] → "L*=6, 14.9%, 0.26 (0.15–0.37)" doğru.
- CD 703 ms ufkun ötesinde; "optimistic for coordinate descent" uyarısı eklenmiş.
- §VI-H girişindeki 0.70 s (702.97 ms) ve 4.95 s (4950.35 ms) doğru.

**Tablo III ve §VI-E** (`fix1_tp*.json`, `fix = 1`, 1.6625 ms/adım, pencere 100–200 ms)
- Tablo, betiğin kopyasıyla bayt bayt yeniden üretildi.
- Hücreler:
  - 0 ms: 5.8288 / 6.3563 / +0.5275 [0.499, 0.557]
  - 0.86 ms: 20/3/5.2389, 10/3/5.5149, +0.2760 [0.244, 0.308]
  - 1.71 ms: b2b/48/5.0775, 20/3/5.1694, +0.0919 [0.042, 0.145]
  - 3.43 ms: b2b/48/4.9820, 80/24/4.9898, +0.0077 [−0.027, +0.041], § işareti doğru
- "Every row some policy with ≤ 8 steps not significantly below the best": her satırda ve her kipte near-best kümesinde L ≤ 8 var. Doğru.
- "Best period 10–20 ms", "statistically tied", "up to 0.53", "nothing significant with 3.43 ms": hepsi doğru.
- `paper_numbers.txt` satır 124–136 düzeltilmiş veriyle güncellenmiş (önceki K3 giderilmiş).

**§VI-H, ön kodlayıcı pilotları** (W = 50)
- Seçilen kollar Adam-6/8/8. Test değerleri 3.5385 / 4.0034 / 4.3341, taze kolda Adam-8 5.2133. Doğru.
- $T_r$ = 2/1/1 ms → "1–2 ms" doğru.
- Seçilenden ayırt edilemeyen küme her numerolojide tam olarak Adam-3…20. Doğru.
- Koordinat inişi ve uzun Adam'ın seçilene göre GA'larının hepsi sıfırın altında. Doğru.
- Seçilen adım sayıları: W = 25 → 5 (dört kolun hepsinde); W = 50 → 6–8; W = 100 → 16/20/20 (taze 24). Doğru.
- Sınırlılıklar'daki "17–32%": 1 − 4.334/5.213 = %16.9, 1 − 3.539/5.213 = %32.1. Doğru.

**§VI-H, kusurlu CSI**
- 6.0770 → 3.5367 (30 dB; doğrulamada seçilen = testte en iyi). Doğru.
- ≤ 10 dB'de "tied" doğru (U3'teki GA'lar).
- Pilot ve CSI birlikte, 30 dB: seçilen − SU-best-of = +0.049 [0.015, 0.084], +0.053 [0.016, 0.092], +0.065 [0.026, 0.105] → "0.05–0.06" doğru.
- 20 dB'de üç GA da sıfırı içeriyor ("ties") doğru.
- Koordinat inişi ve uzun Adam iki ρ düzeyinde ve üç numerolojide hem SU-best-of'a hem seçilene göre anlamlı olarak geride. Doğru.

**§VI-H, ayrık faz**
- $L^\star$ = Adam-5/6/6 doğru.
- L = 48'in maliyeti 9.51 / 14.11 / 14.92% doğru.
- dCD gecikmeleri 16.22–501.18 ms doğru.
- 3 bitte dCD-1…8'in hepsi anlamlı olarak geride. 2 bitte dCD-2…8 geride, dCD-1'in GA'sı [−0.140, +0.034]. Doğru.
- **1 bit cümlesi:**
  - İki tasarımda da doğrulamada seçilen dCD-1.
  - dCD-1 − SU-best-of→q = +0.2504 [0.164, 0.330] → "0.25 (0.16–0.33)" doğru.
  - dCD-1 − Adam-5→q = −0.0444 [−0.1145, +0.0243] → "−0.04, CI −0.11 to 0.02" doğru. Adam-5→q testteki en iyi yuvarlanmış Adam.
  - Önceki K5 giderilmiş; Sınırlılıklar'a da eklenmiş.
- Zamanlama öncesi yük 0.488 / 0.459 / 0.486, yani 0.5'in altında. Başlangıç yükü 4.08 ve 3.62'ydi; betik düşmesini beklemiş.

**Önceki denetimlerin KRİTİK bulguları**

| Bulgu | Durum |
|---|---|
| Sayısal K1 | Giderildi |
| Sayısal K2 (Tablo I) | Giderildi. Şekil 3'ün Armijo kısmı açık (U2) |
| Sayısal K3, K4 | Giderildi (126 iddia, tekrar üretilebilirlik cümlesi, `KEY_NUMBERS.md` kaynak tablosu) |
| Sayısal K5 | Giderildi |
| Editör K1 | Giderildi (Sınırlılıklar artık ≤ 10 dB'yi ve 1 biti söylüyor) |
| Editör K2 | Giderildi (Özet, Katkı 5, İlgili Çalışmalar, Sistem Modeli, §IV atfı, §VI-G) |
| Editör K3 | Giderildi (metinde "PGA" yok) |
| Editör K4 | Giderildi ($T_{\mathrm r}$; ρ tanımlı) |
| Editör K5 | Kısmen. $\bar R_W$ tanımlandı, ama düşüşün açıklaması yok (U3) |
| Editör K6, K7 | Giderildi |

**Biçim**
- `pdfinfo`: 9 sayfa, letter. TWC ücretsiz sınırı 10.
- Log'da tanımsız referans ya da atıf yok. Yalnızca 4 underfull hbox var.
- `sec:res_robust` ve `sec:method` doğru çözülüyor (VI-H, V).
- Anahtar kelime sayısı 5.
