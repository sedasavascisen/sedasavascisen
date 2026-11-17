# Makale 2: gönderim öncesi son bağımsız denetim (17 Kasım 2026)

Kapsam: `mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`, derlenmiş `mobility_paper_ieee.pdf` (pdftotext). Karşılaştırma: `KEY_NUMBERS.md`, `paper_numbers.txt`, `DEGISIKLIKLER.md` (1–16. turlar), `kaynak_kontrol/TOPLU_RAPOR.md`. Hiçbir dosya değiştirilmedi; bu dosya dışında yazım yok, commit yok. Satır numaraları her `.tex` dosyasının kendi satırlarıdır (paragraf başına bir satır).

## Hüküm

**Şu düzeltmelerle gönderilebilir.** KRİTİK bulgu yok. Sayılar tutarlı; kırık atıf ya da çıkarılmış kaynağa atıf yok; kaynak kontrolünün yasakladığı ifadeler metinde yok. Yedi ORTA bulgunun çoğu sıkıştırma sırasında ortaya çıktı. Bir hakem bunları hemen görür: iki iç çelişki, bir yanlış özet ifadesi, bir standart hız iddiası, bir bozuk cümle. Hepsi birkaç kelimelik düzeltmeyle, sayfa sayısı değişmeden giderilebilir.

## Temiz çıkan kontroller

- `\ref`/`\eqref`: 18 farklı hedefin hepsinin etiketi var. PDF'te "??" yok. Log'da tanımsız referans ya da atıf yok.
- Atıflar: 46 anahtar atıf alıyor ve `.bbl`'de 46 `\bibitem` var. `Gudmundson1991`, `rappaport_wireless` ve `Efron1993` hiçbir yerde atıf almıyor.
- Yasaklı genellemeler (TOPLU_RAPOR §1, §3) metinde yok: "never measured", "rarely timed", "fixed parameter" ve "3GPP indoor-office scenario" geçmiyor. Giriş "the 3GPP TR 38.901 channel model" diyor. Özette "standardized" yok.
- PDF 9 sayfa. Özet 197 kelime (sınır 200).
- Sayılar özet, metin, tablolar, sonuç ve `paper_numbers.txt` arasında karşılaştırıldı ve uyuştu:
  - Gecikme ve kayıp: 0.9–5.9 s, 2.5 ms, L* = 4–6, %14.0 (GA 12.5–15.5), 10 km/h'de 3 adım, 0.297 [0.204, 0.390], 0.604 [0.415, 0.805], 5.014 / 0.26.
  - Armijo: 1.26×, 2.09 ms, +0.147 … −0.197.
  - Ölçekleme: 96/48/24–32/12–16/4–6/2, %1.5, %21, −0.675 [−0.692, −0.655], 1.27×, 0.19–1.65.
  - Hız tablosu: tüm satırlar.
  - Tablo III: tüm hücreler.
  - Eşit adım / eşit süre: 2.7–4.0, 68–84%, 18.41/13.48 ms.
  - Hüzme: 11.7–14.2×, 0.12 ms ≈ 13×. 5.228 → 1.736 `results/mumiso_beam_staleness_adam8.json` içinde.
  - Pilot: %17–32 (5.21 → 3.54/4.00/4.33).
  - Kusurlu CSI: 6.08 → 3.54 → 1.40. Buradaki 3.54 (3.5367), pilot satırındaki 3.54 (3.539) ile yalnızca tesadüfen aynı; iki ham dosya ayrı.
  - Düz hesaplar: T_c = 0.4231/15 Hz = 28.2 ms; 42 mm; 48 pilot → 3.43/1.71/0.86 ms.
  - Geniş bant: "3 of 16" (`thesis_exp/genis_bant/REPORT.md` §3 ile uyumlu).

## Bulgular

### ORTA

**1. ORTA. Yöntem bölümü, sonucun kaldırdığı "daha hızlı kod" iddiasını hâlâ taşıyor (iç çelişki).**
`sections/section_05_methodology.tex:19`: *"These are latencies of unoptimized Python code; Section~\ref{sec:res_scaling} shows what changes for faster code."*
§VI-C yalnızca Adam'ın adım süresini ölçekliyor. Sonuç'taki sınırlılık cümlesi ise (`section_07_conclusion.tex:16`) daha hızlı kodda sıralamanın değişebildiğini söylüyor: *"compiled alone (62--63-fold faster), coordinate descent overtakes Python Adam"*. DEGISIKLIKLER 5. tur, "faster code" ifadesini bu bulguyla çeliştiği için Sonuç'tan çıkarmıştı. Yöntem bölümündeki eşi kalmış.
**Düzeltme:** "…Section~\ref{sec:res_scaling} scales Adam's step time, and Section~\ref{sec:conclusion} notes the effect of compiling coordinate descent."

**2. ORTA. Sonuç madde 1 koşulsuz konuşuyor, aynı bölümün sınırlılıkları tersini söylüyor.**
`sections/section_07_conclusion.tex:6`: *"The solvers with the best rate on paper lose to a single-user heuristic that takes milliseconds, even with a tuned number of coordinate sweeps"*.
`:16` ise *"compiled alone (62--63-fold faster), coordinate descent overtakes Python Adam"* diyor. Özet bu koşulu "at the measured step cost" ile veriyor, Giriş katkı 1 de veriyor; Sonuç madde 1 vermiyor. "compiled alone" ifadesi de belirsiz: neyin tek başına derlendiği anlaşılmıyor.
**Düzeltme:**
- madde 1: "…lose to a single-user heuristic that takes milliseconds at the measured (Python) step cost, even with…";
- `:16`: "if coordinate descent alone is compiled (62--63-fold faster), it overtakes Python Adam, but an equal speed-up of all methods keeps tuned Adam ahead".
(62–63×: `thesis_exp/juri/REPORT_S3_S1.md`, satır 7–8, 89.)

**3. ORTA. Sınırlılık cümlesi "behind" sözcüğünün neye göre olduğunu yitirmiş ve §VI-H ile çelişiyor.**
`sections/section_07_conclusion.tex:16`: *"Pilot airtime (17--32\% lower rates), estimation error and 2--3-bit phases leave the slow solvers behind;"*.
DEGISIKLIKLER 3. tur bu cümleyi "…behind tuned Adam" olarak yazmıştı. 5. turdaki sıkıştırmada "tuned Adam" düştü. Bu hâliyle "the heuristic'in de gerisinde" diye okunuyor. Oysa §VI-H (`section_06_results.tex:104`) tersini söylüyor: *"Against SU-best-of, however, coordinate descent … ties at $W=50$~ms with pilots and leads by 0.09--0.18~b/s/Hz with free refresh or at $W=100$~ms"*. 2 bitte de tek taramalı ayrık CD, SU-best-of'un anlamlı gerisinde değil (`:108`: *"at $b=2$ with two or more sweeps"*).
**Düzeltme:** "…leave the slow solvers behind tuned Adam;"

**4. ORTA. Özet ve katkı 1, iki yavaş çözücüyü "en yüksek ilk-kanal hızlı yöntemler" diye tanımlıyor; Şekil 3 ile uyuşmuyor.**
`mobility_paper_ieee.tex:31`: *"coordinate descent and long-run Adam, the methods with the highest initial-channel rate, need 0.9--5.9~s"*.
CD'nin t = 0 hızı 6.925. Adam L = 48 ise 7.037 (`section_06_results.tex:29`, `paper_numbers.txt` "t0 at L=48 7.0368"). Armijo L = 48 de 6.978 (`paper_numbers.txt`). §VI-A bunu doğru söylüyor: *"the best $t=0$ rates of the table"*. Aynı sorun `section_01_introduction.tex:12` ve `section_07_conclusion.tex:6` için de geçerli ("the best rate on paper"), ama orada daha hafif.
**Düzeltme (özet, kelime sayısı aynı kalır):** "coordinate descent and long-run Adam, the slowest high-rate solvers we time, need…" ya da "…, the highest-rate methods of Table~I, …". Katkı 1 ve Sonuç 1 için: "the slow solvers with the best rate on paper".

**5. ORTA. 18 km/h "standartların hızları" arasında sayılıyor; kaynak kontrolü ITU'da böyle bir değer olmadığını tespit etti.**
`sections/section_06_results.tex:57`: *"at the user speeds of the standards: 3~km/h, …; 10~km/h, …; and, beyond the pedestrian class, 18~km/h (5~m/s) and the 30~km/h of the dense-urban evaluation~\cite{3gpp_tr38913,itu_m2410}."*
14. turda yalnızca tablo satırı düzeltildi ("ours, ITU veh."); metin hâlâ 18 km/h'yi standart hızlar listesine koyuyor. TOPLU_RAPOR §3 bu konuda açık: "ITU'da 18 km/h değeri yok".
**Düzeltme:** "…; and, beyond the pedestrian class, the 30~km/h of the dense-urban evaluation~\cite{…} and an intermediate 18~km/h (5~m/s) of our choice, inside the IMT-2020 vehicular class."

**6. ORTA. İlgili Çalışmalar'da sıkıştırmadan bozulan cümle.**
`sections/section_02_related_work.tex:4`: *"run time is usually a complexity order, and where measured, on fixed channel realizations~\cite{Abeywickrama2020TCOM,Yu2019ICCC,Shi2011TSP,Cao2022TWC}, it is not compared with the coherence time."*
"where measured, on fixed channel realizations" bir yüklem taşımıyor. Hakem "measured on fixed realizations" ile "not compared" arasındaki ilişkiyi kuramaz.
**Düzeltme:** "run time is usually a complexity order; where it is measured~\cite{…}, it is measured on fixed channel realizations and not compared with the coherence time."

**7. ORTA. Katkı 3 ve Sonuç 4'teki "updates should still be short", Tablo III'ün en iyi soğuk politikalarıyla çelişiyor görünüyor.**
- `sections/section_01_introduction.tex:14`: *"each update should still be short."*
- `section_07_conclusion.tex:9`: *"each update should still be short."*
- Başlık, `section_06_results.tex:72`: *"Updates Stay Short"*.
Tablo III'te T_p = 1.71 ve 3.43 ms için en iyi soğuk politika b2b ve **L = 48**. Sonuç bölümü bunu doğru söylüyor (`:74`): *"short updates suffice: in every row some policy with at most 8 steps is not significantly below the best"*. Hakem tabloya bakıp "48 adım en iyi" diyecek.
**Düzeltme:** Giriş ve Sonuç'ta "…, and short updates (at most 8 steps) suffice." Başlıkta "Short Updates Suffice".

### KÜÇÜK

**8. KÜÇÜK.** `section_01_introduction.tex:13`: *"In the narrowband model it holds for a second classical optimizer, a larger surface and every standardized indoor speed."*
"it" bir önceki cümledeki "the best number of steps is set by a single quantity … and a small-delay model explains how it scales" ifadesine bağlanıyor. Böyle okununca x-ölçekleme yasasının Armijo için de sınandığı sanılıyor; sınanmadı. 4. turdan önceki ifade "The optimum persists" idi. "Every standardized indoor speed" (3 ve 10 km/h) ise doğru, korunabilir.
**Düzeltme:** "In the narrowband model an interior optimum persists for a second classical optimizer, a larger surface and every standardized indoor speed."

**9. KÜÇÜK.** `section_02_related_work.tex:6`: *"even when both are timed on one machine~\cite{…}"*. "both" sözcüğünün bağlandığı ad yok (önceki yan cümlede "speed" ve "channel" geçiyor).
**Düzeltme:** "even when the learned method and its classical baseline are timed on one machine".

**10. KÜÇÜK.** `section_01_introduction.tex:8`: *"It continues our single-pass phase predictor…"*. "It" bir önceki cümledeki "The question" sözcüğüne bağlanıyor.
**Düzeltme:** "This work continues…".

**11. KÜÇÜK.** `section_07_conclusion.tex:16`: *"Semidefinite relaxation~\cite{Wu2019TWC}, WMMSE~\cite{Choi2024TCOM} and manifold methods were not timed"*. "manifold methods" atıfsız kalmış.
**Düzeltme:** "manifold methods~\cite{Yu2019ICCC}".

**12. KÜÇÜK.** `section_07_conclusion.tex:16`: *"centre-frequency optimization"*. Metnin geri kalanı Amerikan yazımında ("centered").
**Düzeltme:** "center-frequency".

**13. KÜÇÜK.** `section_05_methodology.tex:26`: *"A separate audit script checks 126 assertions about the learning experiments of the underlying thesis; among the results here it covers those of Section~\ref{sec:res_sensitivity}."*
`scripts/audit_claims.py` yalnızca öğrenme deneylerini denetlemiyor. Kanal tanıları, standart hızlar ve CD tarama bütçesi de kapsamında (bölümler satır 676 ve 704). Kapsadığı makale sonuçları da yalnızca §VI-D değil, §VI-A'daki 1–8 tarama sonucunu da içeriyor. Ayrıca aynı satırdaki "rerunning the aging sweeps reproduces them" ifadesinde "them" belirsiz.
**Düzeltme:** "…checks 126 assertions about the experiments of the underlying thesis; among the results here it covers the coordinate-descent budget of Section~\ref{sec:res_aging} and Section~\ref{sec:res_sensitivity}." İkinci cümle için: "…reproduces these tables bit for bit."

**14. KÜÇÜK.** `section_03_system_model.tex:24`: *"the BS is at $(20, 6, 4)$~m, in the panel's boresight and beyond its Fraunhofer distance."* Aynı bölümün `:29` satırı N = 64 için tersini söylüyor: *"the BS (6.0~m away) lies just inside the 6.4~m Fraunhofer distance"*.
**Düzeltme:** "beyond its Fraunhofer distance for $N=32$".

**15. KÜÇÜK.** `section_05_methodology.tex:9`: *"6000 scenarios without mobility, of which 4200 are used for training, 400 for validation and 600 for testing."* Toplam 5200 ediyor. Kodda bölme 70/15/15 (`ris_mu/features.py:101`), yani 900 doğrulama ve 900 test senaryosundan ilk 400 ve 600'ü kullanılıyor. Hakem eksik 800 senaryoyu soracak.
**Düzeltme:** "…, split 4200/900/900; the first 400 validation and 600 test scenarios are used."

**16. KÜÇÜK.** Şekil 3 başlangıç noktası ile L = 0 noktası farklı yöntemler:
- `section_06_results.tex:29`: *"sweeps the number of Adam steps from SU-average (4.624~b/s/Hz)"*.
- Altyazı, `:36`: *"$L=0$: SU-best-of at 0.05~ms (5.276; …)"*.
Eğride L = 0 noktası 5.276, L = 1 noktası 5.41. Okuyucu Adam'ın SU-best-of'tan başladığını sanıyor (`scripts/mumiso_aging_sweep.py:75–83`: Adam SU-average'tan başlıyor, L = 0 SU-best-of).
**Düzeltme (altyazı):** "$L=0$: SU-best-of for reference (Adam starts from SU-average, 4.624)…".

**17. KÜÇÜK.** `section_06_results.tex:104`: *"coordinate descent (deployed after 0.70~s, …)"*. Tablo I'de CD 0.88 s. §VI-H yeniden ölçülmüş gecikmeleri §V'e bağlıyor, ama §V (`section_05_methodology.tex:19`) yalnızca Adam için 1.33 ms veriyor; CD'nin 0.70 s'lik yeniden ölçümü tanıtılmıyor. Değer doğru (DENETIM_SON: 702.97 ms).
**Düzeltme:** §V'deki yeniden ölçüm cümlesine "(coordinate descent: 0.70~s)" ekle.

**18. KÜÇÜK.** `section_05_methodology.tex:19`: *"Latencies are wall-clock times for one scenario … with one PyTorch thread"*. Hemen ardından: *"The Adam rows use 13.3/8 = 1.66~ms per step, from an earlier two-thread measurement made before a precoder fix"*. Genel cümle istisnayı dışlıyor.
**Düzeltme:** "Unless noted, latencies are…".

**19. KÜÇÜK.** `section_06_results.tex:106`: 30 dB pilot SNR'sinde (hata gücü 10⁻³) etkin hız 6.08'den 3.54'e düşüyor. Hakem nedenini soracak. Metin yalnızca 22.6 dB'lik medyanı veriyor. `thesis_exp/p4/kusurlu_csi/REPORT.md`, hata ölçeğinin 400 senaryonun **ortalama** gücünden alındığını ve %5 diliminin 11.5 dB olduğunu söylüyor. Max-min hızı bu zayıf senaryolar belirliyor.
**Düzeltme (sayfa izin verirse):** "(error scaled to the mean power over scenarios; per-scenario median 22.6~dB, 5th percentile 11.5~dB, for the RIS–user channel at 30~dB)".

**20. KÜÇÜK (kaynakça).** `references.bib:347`: SavasciSen2026AISY girdisinde `doi` var, ama IEEEtran bu alanı basmıyor. PDF'teki [13]'te yalnızca "p. e70460, 2026" görünüyor. Cilt ve sayı çıkarıldığı için, Early View makaleyi bulmanın tek yolu DOI.
**Düzeltme:** `note={doi: 10.1002/aisy.70460}` ekle.

**21. KÜÇÜK (iç belge, makaleye girmez).** `KEY_NUMBERS.md` güncel değil:
- Şu sayıların kaynak satırı yok: 62–63× (`thesis_exp/juri/REPORT_S3_S1.md`), "3 of 16" (`thesis_exp/genis_bant/REPORT.md`), eleman kazancıyla gelen "about 5%" (`thesis_exp/kazanc_duyarlilik/REPORT.md`), CD 0.70 s.
- Eski satırlar kalmış: "Published CNN-LSTM … (Sec. VI-G)" ve "Table VII". Bunlar artık makalede yok; §VI-G şimdi hüzme bölümü.
Kural 3 için bu satırlar eklenmeli.

## Gönderimden önce (metin dışı, TOPLU_RAPOR §7 ve DEGISIKLIKLER 3. tur U6'dan açık kalanlar)

- Düzeltilmiş Tablo III betiği (`make_tab_tracking_corrected.py`, `thesis_exp/p4/takip_duzeltme/run.py`) ve §VI-H betikleri, "Data and Code Availability" bölümündeki GitHub deposuna eklenmeli. `make_paper_assets.py` hâlâ eski Tablo III'ü yazıyor. Depo bu hâliyle "every table" iddiasını yeniden üretmez.
- Makale 1 bir sayıya atandıysa cilt ve sayı eklenmeli.
