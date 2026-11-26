# v27 iç tutarlılık denetimi (26 Kasım 2026)

Kapsam: `mobility_paper_ieee.tex` (özet), `sections/*.tex`, yalnızca `\input` edilen `tables/tab_aging.tex`, `tab_speeds.tex`, `tab_tracking.tex`, `supplementary.tex`. Numaralandırma `Latency-Aware_Phase_Optimization_v27.pdf` üzerinden kontrol edildi (pdftotext). Bu PDF, `mobility_paper_ieee.pdf` ile bayt bayt aynı. Sayıları doğrulamak için yalnızca `paper_numbers.txt`, `KEY_NUMBERS.md` ve birkaç ham dosya okundu. Hiçbir betik koşturulmadı, başka hiçbir dosya değiştirilmedi.

PDF'deki numaralandırma: Tablo I literatür (s.3), Tablo II yöntemler (s.5), Tablo III yaşlanma (s.6), Tablo IV hızlar (s.7), Tablo V periyodik (s.8). Şekil 1 senaryo, Şekil 2 yaşlanma, Şekil 3 adım taraması, Şekil 4 ölçekleme, Şekil 5 öğrenilen–Adam karşılaştırması. Bölüm VI-A…H sırasıyla şunlar: aging, optimum, scaling, sensitivity, tracking, reversal, beam, robust.

---

## KRİTİK

### K1. "Tek iş parçacığı" iddiası ile 1.66 ms'nin "iki iş parçacıklı" ölçümden gelmesi çelişiyor
- `section_05_methodology.tex:143` (PDF s.5, V-C): *"Latencies are wall-clock times … with one PyTorch thread"*. Aynı paragrafta: *"The aging-set results of Sections VI-A–VI-E use 1.66 ms … from an earlier two-thread measurement made before a precoder fix"*.
- `section_02_related_work.tex:45` (Tablo I, "This work" satırı): *"measured (one thread)"*.
- `supplementary.tex:9` *"All latencies … with one PyTorch thread"* ile `supplementary.tex:11` *"1.66 ms … comes from an earlier two-thread measurement"* de birbirini tutmuyor.
- Önemi: özetteki 4–6 adım ve %14 sonucu, Tablo III'teki Adam gecikmeleri ve Tablo IV'teki tüm x değerleri bu 1.66 ms'ye dayanıyor. "Tüm gecikmeler tek iş parçacığı" cümlesi bu sayılar için doğru değil.
- Öneri: İlk cümleyi şöyle değiştirin: "All latencies except Adam's aging-set step time (1.66 ms, two threads; see below) are …". Tablo I'de "measured (one thread; one Adam value two-thread)" yazın ya da yalnızca "measured" bırakın. Ek'teki ilk cümleyi de aynı biçimde düzeltin.

### K2. Özet ve Katkı 1, Bölüm VI-H'nin kendi bulgusundan daha geniş konuşuyor
- `mobility_paper_ieee.tex:32`: *"coordinate descent and long-run Adam … are outperformed by a single-user heuristic taking 2.5 ms"*. `section_01_introduction.tex:12` (Katkı 1) aynı iddiayı niteleme olmadan yapıyor.
- `section_06_results.tex:106` (VI-H): *"Against SU-best-of, however, coordinate descent … ties at W = 50 ms with pilots and leads by 0.09–0.18 b/s/Hz with free refresh or at W = 100 ms"*.
- Çelişki: "free refresh" durumu, özetin kendi varsayımlarının (kusursuz CSI, taze ön kodlayıcı) aynısıdır. Tek fark, ölçütün dağıtım anındaki değer yerine zaman ortalaması olması. Bu ölçütle CD, SU-best-of'u geçiyor. Sonuç bölümü 1. madde bunu söylüyor ("Over longer averaging windows…"); özet ve katkılar söylemiyor.
- Öneri: Özete "evaluated at the moment of deployment" ya da "at their completion time" nitelemesini ekleyin. Katkı 1'e "(over longer averaging windows coordinate descent can match it, but not tuned Adam; Section VI-H)" ekleyin.

### K3. Sonuç bölümü, gövdede hiç geçmeyen yeni sonuçlar veriyor
- `section_07_conclusion.tex:16`:
  - *"if only coordinate descent is compiled (62–63-fold faster), it overtakes Python Adam, but an equal speed-up of all methods keeps tuned Adam ahead"*
  - *"In a first OFDM check the interior optimum held … at 20 MHz, but at 50–100 MHz 48 steps were significantly worse in only 3 of 16 configurations"*
- Bu sayılar (62–63×, 3/16, "equal speed-up of all methods") Bölüm VI'da, ekte (S2) ve `KEY_NUMBERS.md` kaynak tablosunda yok. VI-C yalnızca Adam'ın adım süresini ölçekliyor, tüm yöntemleri birlikte ölçeklemiyor. Okur bu sonuçların nereden geldiğini bulamaz.
- Öneri: İki seçenek var. Ya iki kontrolü kısa birer paragrafla VI-C/VI-D'ye (ya da Ek S2'ye, betik ve ham dosya yoluyla) taşıyın, ya da sonuçtan çıkarın. "Equal speed-up keeps tuned Adam ahead" ifadesi ancak bu ölçüm gösterilirse kalabilir.

---

## ORTA

### O1. "Adam'ın adım süresi üç değerle geçer" denmiş, metinde en az beş değer var
- `section_05_methodology.tex:143`: *"Adam's step time appears with three values"*. Tablo II dipnotu (`:136`) üç değeri bölümlere bağlıyor: VI-A–E, VI-F, VI-H.
- Metindeki diğer değerler:
  - VI-D Clarke (`section_06_results.tex:72`): *"3–8 steps (3.4–8.8 ms)"*. Bu adım başına yaklaşık 1.1 ms ediyor. Ek S2 bunun ayrı bir oturumda ölçüldüğünü söylüyor.
  - VI-G (`:100`): *"0.12 ms, about 13 times shorter than one Adam step"*. Ham veride (`paper_numbers.txt`) oran 13.4 ve Adam adımı 1597 µs; bu ne 1.66 ne de 1.33. Ayrıca 1.66/0.12 = 13.8, 1.33/0.12 = 11.
  - VI-C işlem sayısı kontrolü (`:46`) de kendi kalibrasyonunu kullanıyor.
- Dipnot VI-G'yi ve VI-C/VI-D'deki ayrı oturum ölçümlerini kapsamıyor.
- Öneri: Cümleyi "three values in the main results; the Clarke, operation-count and precoder checks have their own timings (supplementary S1–S2)" diye değiştirin. VI-G'ye "(0.12 ms against a 1.60 ms Adam step measured in the same session)" yazın.

### O2. Koordinat inişinin gecikmesi: 0.88 s mi, 0.70 s mi?
- Tablo III (`tab_aging.tex:14`) 880.8 ms veriyor; VI-A (`section_06_results.tex:10`) "0.88 s" diyor; özet "0.9 s".
- VI-H (`:106`): *"coordinate descent (deployed after 0.70 s …)"*. VI-H'nin girişi (`:104`) *"the re-measured latencies of Section V"* kullanıldığını söylüyor, ama Bölüm V (`section_05_methodology.tex:143`) yeniden ölçülmüş değer olarak yalnızca Adam'ın 1.33 ms'sini veriyor. CD için yeniden ölçüm yok.
- Ek olarak Bölüm V'teki *"SU-best-of stays ahead of coordinate descent by 0.26 b/s/Hz (CI 0.15–0.37)"* ile VI-A'daki *"stays 0.26 b/s/Hz below SU-best-of (CI 0.17–0.36)"* aynı nokta tahmini ama farklı güven aralıkları taşıyor. İlki hangi CD (8 tarama, yeniden ölçülmüş) ve hangi gecikmeyle hesaplandı, belli değil. İkincisi en iyi CD (2 tarama) ve 1.66 ms ile hesaplanmış.
- Öneri: Bölüm V'e "the re-measurement also gives 0.70 s for coordinate descent (8 sweeps)" ekleyin. Bölüm V'teki 0.26 için "(8 sweeps, re-measured latencies)" yazın.

### O3. Sonuç 1. madde "ayarlı tarama sayısı" ile "her hız" iddiasını birleştiriyor
- `section_07_conclusion.tex:6`: *"… even with a tuned number of coordinate sweeps; without acquisition delay, this holds at every speed from 3 to 30 km/h"*.
- 1–8 tarama ayarı yalnızca 1.5 m/s'de yapıldı (VI-A, `:10`). Tablo IV'teki Δ sütunu 8 taramalı ve 880.8 ms'lik CD'yi kullanıyor (`scripts/mumiso_standard_speeds.py:55`: `LAT["cd"]`).
- Öneri: "… even with a tuned number of coordinate sweeps (at 1.5 m/s); without acquisition delay, the fixed-budget comparison holds at every speed …".

### O4. Sonuç: "2–3 bit fazlar yavaş çözücüleri ayarlı Adam'ın gerisinde bırakır" ifadesi VI-H'de böyle geçmiyor
- `section_07_conclusion.tex:16`: *"Pilot airtime …, estimation error and 2–3-bit phases leave the slow solvers behind tuned Adam"*.
- VI-H (`section_06_results.tex:110`): *"Discrete coordinate descent … is significantly behind rounded SU-best-of at b = 3, and at b = 2 with two or more sweeps"*.
- Karşılaştırma Adam'a karşı değil, SU-best-of'a karşı yapılmış. b = 2'de tek taramalı CD için hiçbir şeye karşı "geride" denmiyor.
- Öneri: Ya VI-H'ye b = 2 ve 3 için "discrete CD vs best rounded Adam" farkını ve güven aralığını ekleyin, ya da sonucu "2–3-bit phases leave discrete coordinate descent behind rounded SU-best-of (b = 2: from two sweeps)" diye daraltın.

### O5. Şekil 3'teki L = 0 noktası Adam'ın başlangıç noktası değil
- `section_06_results.tex:29`: *"Fig. 3 sweeps the number of Adam steps from SU-average (4.624 b/s/Hz)"*. Tablo II de "start SU-average" diyor.
- Şekil 3 açıklaması (`:36`): *"L = 0: SU-best-of at 0.05 ms (5.276; 5.272 at its measured 2.5 ms)"*. Betik de bunu doğruluyor (`scripts/mumiso_aging_sweep.py:80`): L = 0 SU-best-of, gecikme sabit 0.05 ms.
- Sorun iki katlı. Eğrinin L = 0 noktası taramanın gerçek başlangıcı olan 4.624 değil. Ayrıca SU-best-of, Tablo II/III'te 2.5 ms iken şekilde 0.05 ms'de çiziliyor.
- Öneri: L = 0 noktasını SU-average (4.624, 0.42 ms) yapın ve SU-best-of'u 2.5 ms'de ayrı bir işaretle gösterin. Şekil değiştirilmeyecekse açıklamaya "L = 0 is not Adam's starting point (SU-average, 4.624)" ekleyin.

### O6. Tablo V'te soğuk başlatmanın en iyisi L = 48; bu, özetteki "%14 kayıp" ile çelişiyor gibi görünüyor ve metin bunu açıklamıyor
- Tablo V (`tab_tracking.tex:8–9`): T_p = 1.71 ve 3.43 ms'de soğuk başlatmada en iyi politika "b2b, 48".
- Özet: *"48 steps lower it by 14%"*. Sonuç 2. madde: *"attains its maximum after a few steps and then decreases"*.
- VI-E (`section_06_results.tex:76`) yalnızca "short updates suffice" diyor. Sürekli (b2b) çalışmada L = 48'in neden en iyi çıktığı söylenmiyor: pilot zamanı, güncelleme sıklığı ve yeni fazın ortalamadaki ağırlığı.
- Öneri: VI-E'ye bir cümle ekleyin, örneğin "With long pilots, back-to-back updates spend less airtime on pilots when each update is longer, so a cold start favors many steps; the single-shot optimum of Section VI-B does not carry over". Ham veri (`paper_numbers.txt`, track satırları) her satırda ≤8 adımlı bir politikanın en iyiden anlamlı olarak düşük olmadığını doğruluyor; bunu tablo dipnotuna da yazın (O11'e bakın).

### O7. "Tüm zamanlamaların yük ortalaması ekte" deniyor, ek bunu karşılamıyor
- `section_05_methodology.tex:143`: *"Load averages, round counts and round-to-round spreads of all timings are listed in the supplementary material."*
- Ek S1'de durum şöyle:
  - Static set için "load average was not recorded".
  - Armijo, ön kodlayıcı (VI-G), Clarke ve işlem sayısı ölçümleri için yük ortalaması yok. Ham veride Armijo için 0.18/0.83, ön kodlayıcı için 0.46/0.46 var.
  - S1, 1.33 ms için "it is used in Section VI-H" diyor; oysa Bölüm V de bu değerle L* = 6, %14.9 ve 0.26 veriyor.
- Öneri: Ek S1'e Armijo, ön kodlayıcı ve ayrı oturum ölçümlerinin yük ve tur bilgilerini ekleyin. Ana metinde "all timings" yerine "all timings where recorded" yazın.

### O8. Yeniden üretilebilirlik cümlesindeki istisna listesi eksik
- `section_05_methodology.tex:150`: *"One script generates every table and figure … except Table V … and Section VI-H (separate scripts)"*.
- Ek S2'ye göre VI-C'deki işlem sayısı kontrolü ve VI-D'deki Clarke kontrolü de ayrı oturumda, ayrı betiklerle yapıldı. Sonuçtaki OFDM ve derlenmiş CD kontrolleri için hiçbir yerde betik adı yok (K3).
- Öneri: İstisna listesine "the operation-count and Clarke checks (Sections VI-C, VI-D; supplementary S2)" ekleyin.

---

## KÜÇÜK

1. **xL* ≤ 0.16 sınırı** (`section_04_latency_analysis.tex:93`): *"which holds over our range (xL* ≤ 0.16)"*. Tablo IV'te 18 km/h için x = 0.083 ve L* = 2, çarpım 0.166 ≈ 0.17. Ham veride `u* max 0.150/0.156` yalnızca ölçekleme taramasını kapsıyor. Öneri: "≤ 0.17" yazın ya da "over the step-time sweep" diye daraltın.
2. **"Do not depend" fazla kesin** (`section_05_methodology.tex:143`). 1.66 ms ile L* = 4–6 (tepe 5) ve %14.0; 1.33 ms ile L* = 6 ve %14.9 çıkıyor. Değerler güven aralığı içinde, ama "do not depend" yerine "barely depend (L* 5 vs 6; 14.0 vs 14.9%)" daha doğru. Ayrıca 1.33 ms, aynı cümlede verilen "later rounds 1.49–2.02 ms" aralığının dışında kalıyor; bu bir cümleyle açıklanmalı (tek iş parçacığı, boş makine).
3. **Tablo III'teki Adam gecikmeleri doğrusal model.** 13.3 / 20.0 / 26.6 / 33.2 ms değerleri tam olarak L × 1.6625; L başına ölçülmedi (`scripts/mumiso_aging_sweep.py`, docstring). Özetteki "with measured latencies" ifadesi bunu örtüyor. Öneri: Tablo III başlığına "Adam: L × 1.66 ms" ekleyin.
4. **Tablo III'teki CD satırında tarama sayısı yok.** 880.8 ms, 8 taramaya karşılık geliyor; Tablo II'de "1–8 sweeps (best: 2)" yazıyor. Özetteki "0.9–5.9 s" de 8 taramalı CD'ye ait; ayarlı CD (2 tarama, ~0.21 s) bu aralığın dışında. Öneri: Tablo III'te "Coord. descent (8 sweeps)" yazın.
5. **VI-D'deki zaman ızgarası eksik tanımlanmış** (`section_06_results.tex:57`): *"0.5 ms spacing up to 40 ms"*. L = 48 (79.8 ms), CD ve uzun Adam bu ızgaranın dışında. Betikte 40 ms'den sonra 5 ms aralıklı bir ızgara 100 ms'ye kadar sürüyor, ardından seyrek noktalar geliyor. Öneri: "0.5 ms up to 40 ms, 5 ms up to 100 ms, sparse beyond".
6. **Güvenilir ufuk hıza göre ölçekleniyor ama bu söylenmiyor.** Bölüm III'te ufuk 200 ms; VI-D'de *"(60 and 36 ms)"*. Bu değerler f_d·τ = 3'ün sabit tutulmasından geliyor, ama metin bunu açıklamıyor. Öneri: "(the 200 ms horizon scaled to the same distance, f_d τ = 3)".
7. **Tablo IV'teki Δ sütunu.** CD her hızda ufkun ötesinde, ama sütunda † işareti yok. Bu yalnızca metinde söyleniyor ("optimistic values for the slow solvers"). Öneri: Başlığa "Δ uses coordinate descent beyond the horizon (optimistic)" ekleyin. Kaynak sütunu 30 km/h için yalnızca ITU yazıyor; metin 3GPP ve ITU'nun ikisine de atıf yapıyor.
8. **Terim birliği.**
   - "fresh beam" (`section_04:43`, `section_06:100`) ile "fresh/freshly computed precoder" (özet, VI-G başlığı) karışık kullanılıyor; "precoder"da birleştirin.
   - "intrinsic optimum" (`section_04:51`, `section_06:110`) ile "interior optimum/maximum" (özet, katkılar, VI-C, sonuç) karışık; birini seçin.
   - Tablo III'te "Coord. descent" kısaltması var, metinde her yerde tam ad geçiyor; bu kabul edilebilir.
9. **Sembol çakışmaları.**
   - Δ üç anlamda kullanılıyor: Δ(L) yaşlanma kaybı (Denk. 5–6), ΔT adım süresi, Tablo IV'teki Δ (SU-best-of eksi CD). Tablo IV için "Δ_CD" ya da "gap" önerilir.
   - τ hem gecikme (τ_A, τ(L)) hem Kendall τ (VI-C) için kullanılıyor; Kendall için "Kendall rank correlation 0.86–0.87" yazılabilir.
   - Tanım 3'te pencere 𝒲 bir küme; VI-H'de W bir süre (ms). Bu ilişki açıkça yazılmalı.
   - Önerme 1'de κ_L = κ varsayılıyor, VI-C'de κ_L 7.8'den 25.1'e çıkıyor. Bu farkın bilindiği söylenmiş, ama Önerme 1'in kapalı formunda hangi κ'nın kullanıldığı (ortalama κ̄ = 18.8) belirtilmemiş.
10. **"Effective rate" tanımı.** Özette "the rate on the channel at the end of its computation" deniyor; Tanım 1 bunu minimum kullanıcı hızı olarak tanımlıyor. Bölüm V-D'de τ_A'ya T_ov ekleniyor, Tanım 1'de T_ov yok. Öneri: Özette "minimum user rate" yazın; Tanım 1'e "(plus any acquisition delay T_ov)" ekleyin.
11. **Tablo V ile metin.** VI-E'deki *"in every row some policy with at most 8 steps is not significantly below the best"* iddiası tablodan görülemiyor: T_p = 3.43 satırındaki en iyi politikalar 24 ve 48 adım. Ham veri iddiayı doğruluyor, okur doğrulayamıyor. Öneri: Tabloya "best L ≤ 8" sütunu ya da dipnotu ekleyin.
12. **Giriş: "We evaluate every method on the channel that exists when it finishes"** (`section_01:8`). VI-F bilinçli olarak t = 0 hızlarını kullanıyor. Öneri: "every method except in the compute-efficiency comparison of Section VI-F".
13. **Bölüm II ile Tablo I'de Cao2022.** Metin (`section_02:21`) Cao2022'yi "measured … on fixed channel realizations" grubuna koyuyor; Tablo I aynı çalışma için "first-order aging, fixed delay" yazıyor. Bu çelişki değil, çünkü zamanlama sabit gerçekleşmede yapılmış, ama okur karıştırabilir.
14. **VI-H'de iki farklı "en iyi" değer.** 5.21 (serbest yenileme, R̄₅₀) ve 6.08 (kusursuz CSI, anlık etkin hız) aynı 1.33 ms ayarından geliyor, ama farklı ölçütlerle. Bunu bir parantezle belirtin.
15. **Ekteki elle yazılmış bölüm numaraları** (`supplementary.tex:11,19`: "Section VI-H", "VI-C", "VI-D"). Şu an doğrular: işlem sayısı kontrolü VI-C'de, Clarke VI-D'de, sağlamlık VI-H'de. Ancak ek ayrı bir belge olduğu için \ref ile bağlanamıyor; ana metinde bölüm sırası değişirse ek elle güncellenmeli.
16. **Tablo sırası.** Tablo III (`tab:aging`) ilk kez Bölüm III'te (`section_03:29`) anılıyor, Tablo II ise Bölüm V'te. IEEE numarayı yüzen nesne sırasına göre verdiği için PDF tutarlı. Yine de ilk atıf sırası Tablo III → Tablo II. Bölüm III'teki atıf "the stale floor (Section VI-A)" yapılırsa sıra düzelir; bu isteğe bağlı.

---

## Kontrol edilen ve tutarlı bulunanlar (tek tek listelenmedi)

- **Gecikmeler.** Özetteki 0.9–5.9 s; 880.8 / 5851.7 ms; Tablo II'deki 5.85 s ve VI-A'daki 5.9 s / 0.88 s; SU-best-of 2.5 ms (ölçüm 2.541); SU-average 0.42 ms; 107 ms/tarama (yaklaşık 4 T_c); Armijo 2.09 ms = 1.26 × 1.66; Tablo II dipnotundaki 1.66 / 1.60–1.71 / 1.33 ile Bölüm V ve Ek S1; Tablo III'te 13.3 ms = 8 × 1.66; VI-F'de 18.41 / 13.48 ms ve 2.7–4.0 oranı (ham 2.73–4.05); dört ve altı adımın 6.7–10.0 ms'si.
- **Optimum.** Her yerde 4–6 (özet, Tablo II, VI-B, VI-D, V-D). Tepe L = 5 (5.982); Tablo IV'teki "4 (4–6)" farklı ızgarada, bu başlıkta belirtilmiş. Hıza göre 8/3/2/1 (özet, VI-D, Tablo IV, sonuç 2). Adım boyları 0.25/0.75/1.0 için 6/4/5 ve %11.5/13.7/11.3. Armijo L* = 4 ve 6.015; fark 0.033 (−0.001…0.064); maliyet oranı taraması +0.147…−0.197.
- **Kayıplar.** %14 / 14.0 (12.5–15.5); tam gecikmede 14.2; ince ızgarada 14.2; 1.33 ms ile 14.9; 3 km/h'de 14.5 (13.1–16.1); 10 km/h'de 10.5 (9.0–11.9); ortak kazançla 17.7 ve 14.2; gecikmeli durumda 2.9–14.7; Clarke kanalında 27–32 (yalnızca VI-D, tek kaynak); L = 256 için 1.5 (1.3–1.8) ve yaklaşık %21 (ham 21.1).
- **CD ile SU-best-of farkları.** 0.297 (0.204–0.390) = 5.272 − 4.975; 0.604 (0.415–0.805); en iyi tarama 5.014 ve 0.26 (0.17–0.36); hız tablosunda 0.25–0.42 (ham 0.246–0.423); uzun Adam'a karşı 0.45–0.69 (ham 0.448–0.693); 30 km/h ve 3.43 ms'de anlamsız (ham −0.028…0.312).
- **Pilotlar.** 48 sembol; 3.43 / 1.71 / 0.86 ms (Bölüm V, Tablo V, VI-D). Sonuçtaki %17–32 = 1 − {4.33, 4.00, 3.54}/5.21, yani %16.9–32.1; VI-H ile tutarlı. Doğrudan bağlantı 1.744 / 1.74.
- **Model.** γ = 0.93 (0.56–1.19) → −0.78…−0.63; ölçülen −0.675 (−0.692…−0.655); ±0.08; çarpan 1.27 (5.3'e karşı 5); κ_L 7.8–25.1; R² ≥ 0.98; denge oranı 0.19–1.65; τ* 1.6–10 ms; N = 64 için 8.48 / 7.10 ve 1.04; Fraunhofer mesafeleri 4.0 / 6.4 m, BS 5.98 m; işlem sayısı kontrolünde 11,008 FLOP ve Kendall 0.86–0.87 (VI-C ile Ek S2).
- **Hızlar.** T_c ve x değerleri (Tablo IV, f_d = v f_c / c, 0.423/f_d); 1.5 m/s'de f_d = 15 Hz, T_c = 28.2 ms, 42 mm (Şekil 1).
- **Periyodik.** Tablo V ile VI-E metni (6.36, 10–20 ms, 80 ms / b2b-48 bağlı, +0.53, anlamsız +0.01); katkı 3 ve sonuç 4'teki "≤8 adım".
- **Ön kodlayıcı.** 11.7–14.2× (ham 11.72–14.21).
- **Öğrenilen.** %68–84 (ham 68.3–83.7); beş turun beşinde de baskınlanmış; 600 test senaryosu; 41 = 37 + 4 kanal (2 + 16 + 16 + 2 + 1).
- **Atıflar.** Tüm tablo, şekil ve bölüm atıfları \ref ile yapılmış ve tanımsız etiket yok. "Tables III–V" (Bölüm V, aging set) gerçekten yaşlanma, hız ve periyodik tablolarını kapsıyor; hepsi aging set. "Figs. 2–4" yaşlanma, tarama ve ölçekleme şekillerini kapsıyor. Tablo IV başlığındaki "Table III and Fig. 3" doğru. Tablo II dipnotundaki VI-A–E / VI-F / VI-H doğru. Ana metinde elle yazılmış tablo, şekil ya da bölüm numarası yok; elle yazılmış numaralar yalnızca ekte (KÜÇÜK 15).
- **Kapsam ifadeleri.** "Every standardized indoor speed" (katkı 2) yalnızca 3 ve 10 km/h için söylenmiş ve doğru. VI-D'deki "every speed" gecikmesiz durumla sınırlandırılmış. "Only tuned Adam beats CD under every window" VI-H ile tutarlı. Sonuçtaki 1 bit / 10 dB ifadeleri VI-H ile tutarlı.
- **Ek ile ana metin.** 1.66 / 1.49–2.02 / 1.33 / 0.45 / 0.20→0.86 / 1.15–3.66, beş tur ve 1.60–1.71, 1.04, Armijo 1.26 (0.81–1.97) aynı. Fark yalnızca K1 ve O7'de.
- **Tesadüf kontrolü.** 3.54 değerinin iki deneyde görünmesi tesadüf: ham değerler 3.537 (CSI) ve 3.54 (15 kHz pilot). Bu bir kopyalama hatası değil.
