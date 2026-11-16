# Makale 2 revizyonu: sayısal denetim (16 Kasım 2026)

**Kapsam:** `kaynak_farki.diff` içindeki her yeni ya da değişmiş sayı, ham JSON'dan Python ile okundu. Ayrıca değişmeyen yerlerde artık çelişen sayılar arandı.

**Denetim koşulları:**
- Dal `thesis/p4-deneyler`, HEAD `aa0c28c`, çalışma ağacı temiz.
- `scripts/audit_claims.py --all`: 126/126.
- Yük ortalaması 0.14; yalnızca okuma yapıldı. Hiçbir deney koşturulmadı.
- `make_tab_tracking_corrected.py`, scratchpad'deki bir kopyada koşturuldu.

Satır numaraları `thesis_exp/makale2_revizyon/` altındaki dosyalara aittir.

---

## KRİTİK

### K1. "leaves $L^\star$ unchanged" ham veriyle çelişiyor
- **Yer:** `sections/section_05_methodology.tex:22`
- **Beklenen:** Tam gecikmede değerlendirmede $L^\star$ değişmemeli.
- **Bulunan:** `p4/izgara_kontrol/raw/results.json` → `sets.paper.L_star` = `{"interpolated": "Adam-5", "exact": "Adam-4"}`.
  - Adam-4 tam değeri 5.9843, Adam-5 tam değeri 5.9838.
- **Neden önemli:** Makale nokta $L^\star$'ı başka yerlerde 5 olarak kullanıyor:
  - §VI-C, `section_06_results.tex:44`: "(5.3 against 5 here)"
  - `paper_numbers.txt:17`: "best L=5"
  - `paper_numbers.txt:105`: "L*=5"
- Cümle yalnızca $L^\star$ "4–6 aralığı" anlamında okunursa savunulabilir.
  - Ancak tam değerlendirmede "4–6 dışındaki her adım sayısı anlamlı olarak düşük" (§VI-B) iddiasının eşli GA'ları hesaplanmamış.
  - `izgara_kontrol` en iyi kola karşı eşli GA hesaplamıyor.
- **Öneri:** "the point optimum moves from $L=5$ to $L=4$ (5.984 vs 5.984), within the 4–6 plateau" gibi bir ifade. Plato iddiası için de GA hesaplanmalı.

### K2. "at most 0.027 b/s/Hz" Tablo I'in yarısı için ölçülmedi
- **Yer:** `section_05_methodology.tex:22`
- **İddia:** "...changes the effective rates of Table I and Fig. 3 by at most 0.027 b/s/Hz"
- **Kanıt:** `izgara_kontrol/run.py`'deki "paper" gecikme kümesi şu:
  - `SU-best-of: 0.05`, `CD: 1500.0`, `PGA: 5600.0`, `Adam-L: L·13.3/8`
  - Tablo I'in gecikmeleri (`tables/tab_aging.tex`, `paper_numbers.txt:9-16`) ise SU-average 0.42, SU-best-of 2.54, CD 880.78 ve long-run Adam 5851.66 ms.
- **Sonuç:** Tablo I'in sekiz etkin hız satırından dördü kontrolün dışında: SU-average, SU-best-of (2.5 ms), coordinate descent ve long-run Adam.
  - Ham dosyadaki "SU-best-of − CD" değeri 0.355. Tablo I'in 0.297 değerine karşılık gelmiyor, çünkü CD 1500 ms'de değerlendirilmiş.
  - CD 880.8 ms ile ızgaranın 500–1500 ms boşluğuna düşüyor. Long-run Adam ise ızgaranın son noktasının (5600 ms) ötesinde; tablo bunu "value at last grid point" diye işaretliyor. Tam değerlendirmenin en çok değiştirebileceği satırlar bunlar.
  - Karşılaştırma için: yeniden ölçülen kümede CD 703 ms'de tam − interp. = +0.025 [−0.066, +0.118].
- Şekil 3'teki $L=3$ ve Armijo eğrisi de kontrol edilmedi: `STEPS` 3'ü içermiyor, Armijo kolu yok.
- **Kontrol edilen kollarda doğru olan:** En büyük |tam − interp.| = 0.0272 (Adam-32, 53.2 ms). Tablo I'in Adam satırlarında (L = 8/12/16/20) en büyük değer 0.0061.
- **Öneri:** Cümleyi "the Adam step sweep (Fig. 3) and the Adam rows of Table I" ile sınırla ya da CD ve long-run Adam'ı kendi gecikmelerinde değerlendir. Sayı yazılmadan önce bu ölçülmeli.

### K3. `paper_numbers.txt` hâlâ eski Tablo III'ü taşıyor
- **Yer:** `paper_numbers.txt:124-135`. Dosya özgün kopyayla birebir aynı.
- **Bulunan (eski):**
  - 0.86 ms soğuk: `L=4 5.200`, sıcak `5.422`, fark `0.222`
  - 1.71 ms: soğuk `5.088`, sıcak `5.234`, fark `0.146`
  - 3.43 ms sıcak: `L=8 4.986`
  - 0 ms fark: `0.524`
- **Beklenen (`fix1_tp*.json`):**
  - 0.86 ms: soğuk L=3 5.239, sıcak 5.515, fark 0.276
  - 1.71 ms: 5.077, 5.169, fark 0.092
  - 3.43 ms sıcak: L=24 4.990
  - 0 ms fark: 0.5275
- Near-best kümeleri de değişti. Örneğin 0.86 ms soğukta [3, 4, 6] → [3, 4]; 0.86 ms sıcakta [2, 3] → [3].
- `KEY_NUMBERS.md:26` Tablo III'ün kaynağını hâlâ `scripts/mumiso_tracking.py` → `results/mumiso_tracking.json` olarak veriyor (yayımlanmış, düzeltilmemiş sürüm).
- Yeni §VI-H'nin hiçbir sayısının kaynağı ne `KEY_NUMBERS.md`'de ne `paper_numbers.txt`'de var.

### K4. "Reproducibility" cümlesi revize kopyada artık doğru değil
- **Yer:** `section_05_methodology.tex:26`
- **İddia:** "One script generates every table and figure from stored result files; rerunning the aging sweeps reproduces them bit for bit."
- **Kanıt:**
  - Tablo III artık ayrı bir betikten (`make_tab_tracking_corrected.py`) ve `thesis_exp/p4/` altındaki verilerden üretiliyor.
  - `make_paper_assets.py` özgünüyle aynı. Satır 450'de `mumiso_tracking.json` okunuyor, 472'de `tab_tracking.tex` yazılıyor. Koşturulursa eski Tablo III'ü geri yazar.
  - §VI-H'nin sayıları hiçbir tablo/şekil betiğinden gelmiyor; elle metne kopyalanmış.
- Aynı satırdaki "123 assertions" sayısı değişikliklerden önce de vardı. Bugünkü denetim betiği 126 iddia sayıyor (111 + §5). Değişiklik kaynaklı değil, ama yanlış.

### K5. Ayrık fazda 1 bitte doğrulamada seçilen yöntem koordinat inişi; metin bunu söylemiyor
- **Yer:** `section_06_results.tex:110`, ayrıca `:102`
- **Kural:** CLAUDE.md, 11 Kasım kuralı 10: makaledeki iddiayla çelişen bulgu yumuşatılmaz.
- **Kanıt:** `ayrik_faz/raw/results_exact.json`, `bits.1`:
  - Her iki tasarımda (`lr0.5`, `lr-val`) `selected_on_val = "dCD-1"`.
  - dCD-1 − SU-best-of→q = **+0.250 [+0.164, +0.330]**, yani yuvarlanmış sezgiselin anlamlı olarak önünde.
  - dCD-2…8, SU-best-of→q'dan ayırt edilemiyor; GA'ların hepsi sıfırı içeriyor.
- **Metnin söyledikleri:**
  - "falls significantly behind the rounded SU-best-of at 3 bits and, with two or more sweeps, at 2 bits; it ties the best rounded Adam only at 1 bit with a single sweep"
  - §VI-H'nin girişi: "where a configuration is selected (... best method), it is selected on an independent mobility draw"
- **Çelişki:** Bağımsız çekilişte seçilen en iyi yöntem 1 bitte dCD-1, ama metin onun yerine testte argmax ile bulunan "$L^\star=5$" yuvarlanmış Adam'ı raporluyor.
  - Bu, Sonuç 1. maddedeki "Speed beats precision" ile 1 bit rejiminde çelişiyor. Bu rejimde tek taramalı ayrık CD 16 ms ile hem hızlı hem en iyi.
- **Yeniden üretilemeyen kısım:** "Ties ... only at 1 bit with a single sweep" iddiasının dışlama tarafı için ham veride eşli GA yok.
  - Yani dCD-2…8'in 1 ve 2 bitte en iyi Adam→q'dan anlamlı olarak geride olduğu gösterilmemiş.
  - Ham dosyadaki tek eşli farklar: `dCD-1 − Adam-5→q` ve `dCD-1 − Adam-6→q`.
  - Nokta tahminleri farkın büyük olduğunu gösteriyor (örneğin 1 bitte dCD-2 4.927, Adam-5→q 5.158). Ancak bu tarafın GA'sı **ÜRETİLEMEDİ**: ham dosyada yok.

---

## UYARI

### U1. §VI-H girişindeki seçim kuralı her paragraf için geçerli değil
- **Yer:** `section_06_results.tex:102`
- **İddia:** Seçim bağımsız çekilişte yapılıyor.
- **Gerçekte bağımsız çekilişte seçilenler:** Ön kodlayıcı pilotları (R ve kol, seed 12) ile kusurlu CSI (adım boyu ve kol, seed 12).
- **Gerçekte raporlanan kümede seçilenler:**
  - "Step time" paragrafında $L^\star=6$ (`izgara_kontrol`'de doğrulama kümesi yok).
  - "Discrete phases" paragrafında $L^\star=5/6/6$ (testte argmax).
- Ayrık fazda raporlanan tasarım `lr0.5`, yani sabit adım boyu. Doğrulamada adım boyu seçilen `lr-val` tasarımında 1 bitte $L^\star=3$ ve kayıp %9.1; metindeki değerler %9.5 ve $L^\star=5$.

### U2. "averaged over 25, 50 and 100 ms ... 5, 6–8 and 16–20, with differences of at most 0.04 b/s/Hz to six steps at 100 ms"
- **Yer:** `section_06_results.tex:106`
- **Ham değerler:** `results_win100.json`, Adam-6 − seçilen:
  - 15 kHz: −0.0215 [−0.052, +0.008]
  - 30 kHz: **−0.0375 [−0.070, −0.004]**
  - 60 kHz: **−0.0406 [−0.076, −0.003]**
- 30 ve 60 kHz'de fark anlamlı. "At most 0.04" yalnızca yuvarlamayla tutuyor (0.0406), anlamlılık da söylenmiyor.
- **Taze W (pilotsuz) kolu:**
  - W = 100'de seçilen Adam-24; Adam-6 bunun 0.069 gerisinde.
  - W = 25 ve 50'deki aralıklar taze W'yi de kapsadığı hâlde 100 ms aralığı (16–20) onu dışlıyor. Taze W dahil edilirse aralık 16–24 olur, fark da 0.069'a çıkar.
  - Cümle hangi kolları kapsadığını belirtmeli.

### U3. "the best rate falls from 5.21 (free refresh)"
- **Ham değer:** `onkodlayici_siralama/raw/results.json`. Taze W'de doğrulamada seçilen Adam-8 testte 5.2133; testteki en yüksek değer ise Adam-6'nın 5.2248'i.
- Pilotlu satırlarda doğrulamada seçilen kolların testteki değerleri metinle aynı: 3.5385, 4.0034, 4.3341.
- "Best", "selected" anlamında kullanılıyor; tutarlı ama belirsiz.
- Aynı alt bölümdeki kusurlu CSI paragrafında "best" 6.08, ama bu farklı bir ölçüt: 50 ms ortalaması değil, tanım 1'in anlık etkin hızı. Yan yana okununca karışabilir.

### U4. "at 10 dB and below the methods cannot be told apart" yalnızca bir karşılaştırmaya dayanıyor
- **Yer:** `section_06_results.tex:108`
- **Ham değerler:** `kusurlu_csi/raw/results.json`. Bu deneyde CD ve PGA kolu yok. Tek eşli GA, doğrulamada seçilen Adam − SU-best-of:
  - 10 dB: −0.0067 [−0.037, +0.024]
  - 5 dB: −0.0061 [−0.025, +0.014]
  - 0 dB: −0.0006 [−0.012, +0.011]
- "The methods" ifadesi yalnızca Adam-L ve SU-best-of için geçerli.
- **ρ'nun anlamı:** Hata ölçeği 400 senaryonun ortalama gücünden alınıyor (`REPORT.md`). Bu yüzden ρ = 30 dB'de senaryo başına etkin SNR'nin medyanı 22.6 dB, %5 dilimi 11.5 dB.
  - "Normalized power $1/(1+\rho)$" ifadesi senaryo başına SNR diye okunabilir. Bir yan tümceyle belirtilmeli.
- **İzlenebilirlik:** `results.json`'un ölçüm commit'i (06fc9d2) `run.py`'yi içermiyor. Bit bit yeniden üretim `denetim_log/k1_rerun.md`'de kayıtlı.

### U5. Sonuç bölümü kusurlu CSI bulgusunu genelliyor
- **Yer:** `sections/section_07_conclusion.tex:16`
- **İddia:** "adding estimation error ... leave the slow solvers behind"
- **Ölçülen:** CD ve PGA yalnızca pilot + CSI deneyinde, ρ = 30 ve 20 dB'de ölçüldü (`onkodlayici_csi`). Orada gerçekten anlamlı olarak gerideler.
- ρ ≤ 10 dB'de yavaş çözücü ölçülmedi.
- Ayrık fazdaki 1 bit sonucu (K5) da sınırlılıklarda geçmiyor.

### U6. Özet ve giriş, yeni bölümle çelişiyor
- **Özet** (`mobility_paper_ieee.tex:31`): "All results assume the precoder is recomputed from the current channel." Oysa §VI-H artık pilot ücretini ve kestirim hatasını hesaba katan sonuçlar veriyor.
- **Giriş** (`section_01_introduction.tex:16`) ve §VI-G (`section_06_results.tex:98`) aynı cümleyi taşıyor. §VI-G'nin sonu değiştirildi, giriş değiştirilmedi.

### U7. §VI-H yalnızca "re-measured step time of 1.33 ms" diyor; aslında bütün kolların gecikmesi değişti
- **Ham değerler:** `infra/raw/mumiso_mobility_latency_rerun.json`, `median`:
  - SU-best-of 1.63 ms (Tablo I'de 2.54)
  - CD 703 ms (880.8)
  - Long-run Adam ("pga") 4950 ms (5851.7)
  - SU-average 0.30 ms (0.42)
- Adam-L için adım başına düz 1.33 ms kullanılmıyor; her L'nin kendi medyanı kullanılıyor. Örneğin L = 4'te adım başına 1.386 ms.
- "SU-best-of stays ahead of coordinate descent by 0.26 (CI 0.15–0.37)" değerinde CD 703 ms ile 200 ms'lik güven ufkunun ötesinde, yani iyimser. Tablo I'deki † işareti burada yok.

### U8. "A later re-measurement on an idle machine"
- **Yer:** `section_05_methodology.tex:19`
- **Ham değerler:** Aynı JSON:
  - `load_before` 0.45, `load_after` 0.88
  - Turlar boyunca yük: 0.45, 0.61, 0.69, 0.78, 0.83
- Başlangıç CLAUDE.md'deki 0.5 eşiğinin altında, ama "idle" tam doğru değil. "Load average 0.45 before and 0.88 after" diye yazılabilir; §V'in geri kalanı da yükü bu biçimde raporluyor.
- 1.33 değeri doğru: eğim 1.328 ms/adım, L ≥ 8 için adım başına 1.33.

### U9. "PGA" makalede tanımlı değil
- **Yer:** `section_06_results.tex:106` ve `:108`
- Makalenin geri kalanı bu kola "long-run Adam" diyor (`section_05_methodology.tex:14`). Kod adı (`baselines.pga`) metne sızmış.

### U10. Tablo III'te 0.86 ms satırında yuvarlama
- Görünen hızlardan 5.51 − 5.24 = 0.27 çıkıyor, fark sütununda +0.28 yazıyor (ham değer 0.2760).
- Değer doğru, ama okuyucu soracaktır. Dipnot ya da üç basamak düşünülebilir.

### U11. Tablo III'te seçim kuralı
- En iyi politika raporlanan kümede seçiliyor (`run.py`, yayımlanmış betikle aynı). §V'deki genel "selected and reported on the same scenarios unless stated" cümlesi bunu kapsıyor.
- Ancak §VI-H aynı sayfada tersini, yani bağımsız çekilişte seçimi vurguluyor. Tablo III başlığında ayrıca belirtilmesi iyi olur.
- Düzeltilmiş benzetimde kanal anlık görüntüsü hâlâ en yakın ızgara noktasından alınıyor (`run.py` docstring'i: "Snapshot instants keep the published rounding"). Yeni §V cümlesi bunu söylemiyor.
- Tam entegrasyon kontrolünde politika başına fark en fazla 0.0072.

---

## DOĞRULANDI

**Tablo III** (`tables/tab_tracking.tex`)
- `make_tab_tracking_corrected.py` geçici kopyada (`fix1_tp*.json` okunarak) koşturuldu. Çıktı `tables/tab_tracking.tex` ile bayt bayt aynı.
- Bütün hücreler ham değerle tutuyor:
  - 0 ms: 5.8288 / 6.3563 / +0.5275
  - 0.86 ms: U = 20, L = 3, 5.2389 / U = 10, L = 3, 5.5149 / +0.2760
  - 1.71 ms: b2b, 48, 5.0775 / 20, 3, 5.1694 / +0.0919
  - 3.43 ms: b2b, 48, 4.9820 / 80, 24, 4.9898 / +0.0077, GA [−0.027, +0.041] sıfırı içeriyor, § işareti doğru
- Ham dosyalar: ms/adım 1.6625, pencere 100–200 ms, commit 238d846, `fix = 1`.
- `fix0_tp*.json`, `results/mumiso_tracking.json` ile bütün politikaların ortalamalarında birebir aynı (en büyük fark 0).

**§VI-E metni** (`section_06_results.tex:74`)
- "6.36" doğru.
- "0.86 ms: best period 10–20 ms" doğru (sıcak 10, soğuk 20).
- 3.43 ms'de sıcak 80 ms ile soğuk b2b 48 adım "statistically tied": GA [−0.027, +0.041].
- "In every row some policy with at most 8 steps is not significantly below the best": her T_p'de ve her kipte near-best kümesinde L ≤ 8 var. Satırın en iyisi her satırda sıcak kip; onun near-best kümesinde de L ≤ 8 var.
- "Up to 0.53": 0.5275 doğru.
- "Nothing significant with 3.43 ms" doğru.

**§V, ızgara ile tam değerlendirme** (`izgara_kontrol/raw/results.json`)
- "14.0% → 14.2%": 13.99 → 14.20 doğru.
- Özetteki "14%" doğru.
- Kontrol edilen kolların en büyük farkı 0.0272 doğru. Kapsam sorunu için K2'ye bakınız.

**1.33 ms** (`origin/thesis/altyapi:thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json`)
- Yerel kopyayla aynı.
- Tek iş parçacığı, eğim 1.328 ms/adım, adım başına 1.33–1.39 ms.

**§VI-H, adım süresi**
- $L^\star=6$ (`rerun.L_star.exact`) doğru.
- %14.93 → 14.9% doğru.
- SU-best-of − CD (tam) 0.2616 [0.1470, 0.3727] → 0.26 (0.15–0.37) doğru.

**§VI-H, ön kodlayıcı pilotları** (`onkodlayici_siralama/raw/results.json`)
- Pilot sayısı 4, pencere 50 ms.
- 3.5385 / 4.0034 / 4.3341 → 3.54 / 4.00 / 4.33 doğru.
- Seçilen R değerleri 2 / 1 / 1 ms → "1–2 ms" doğru.
- Üç numerolojide seçilenden ayırt edilemeyen küme tam olarak Adam-3…Adam-20 doğru; seçilenler 6 / 8 / 8.
- CD ve PGA'nın GA'larının hepsi sıfırın altında doğru.
- Pencere 25 ms'de dört kolun hepsinde seçilen Adam-5 doğru. Pencere 50 ms'de seçilenler 8 / 6 / 8 / 8 → 6–8 doğru.

**§VI-H, kusurlu CSI** (`kusurlu_csi/raw/results.json`)
- Kusursuz CSI'da 6.0770, 30 dB'de 3.5367 → 6.08 ve 3.54 doğru. Doğrulamada seçilen ile testteki en iyi aynı.

**§VI-H, pilot ve CSI birlikte** (`onkodlayici_csi/raw/results.json`)
- 30 dB'de seçilen − SU-best-of: +0.0487, +0.0528, +0.0649 → 0.05–0.06 doğru; üçünün de GA'sı sıfırın üstünde.
- 20 dB'de üçünün de GA'sı sıfırı içeriyor ("tied") doğru.
- CD ve PGA − seçilen: iki düzeyde ve üç numerolojide GA'ların hepsi sıfırın altında doğru.

**§VI-H, ayrık faz**
- `results_exact.json`, `lr0.5`:
  - 1 bit: $L^\star$ = Adam-5, %9.51 doğru.
  - 2 bit: Adam-6, %14.11 doğru.
- `results_3bit.json`: Adam-6, %14.92 doğru.
- dCD gecikmeleri 16.22–501.18 ms → "16–501 ms" doğru.
- 3 bitte dCD-1…8 − SU-best-of→q GA'larının hepsi sıfırın altında doğru.
- 2 bitte dCD-2…8 sıfırın altında, dCD-1 GA'sı [−0.140, +0.034] doğru.
- 1 bitte dCD-1 − Adam-5→q = −0.044 [−0.114, +0.024] ("ties") doğru.
- Zamanlama öncesi yük: 0.49 / 0.46 / 0.49.

**Diğer**
- Derlenmiş PDF, `.tex` ile aynı sayıları taşıyor (pdftotext ile kontrol edildi).
- `sections/` dosyaları PDF'ten önce değiştirilmiş.
- `KEY_NUMBERS.md` ve `paper_numbers.txt` özgün kopyayla birebir aynı, yani güncellenmemiş (K3).
