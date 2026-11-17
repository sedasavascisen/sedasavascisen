# Makale 2 — Kaynak kontrolü, Grup 2: [6]–[10]

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Metin olarak çıkmayan iki tablo (Abeywickrama Table II, Choi Table II) sayfa görüntüsünden okundu. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex` ve `sections/*.tex`, dal `thesis/p4-deneyler`, commit `5cdb969`). Özette (abstract) bu beş anahtarın hiçbiri geçmiyor.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI: Makale 2'deki bir iddiayla çelişen bulgu

İlgili çalışmalar bölümünde (`sections/section_02_related_work.tex`, satır 4) şu cümle var: *"These works report the objective value reached; run time, when discussed, is a complexity order, not a latency measured against the coherence time."*

Bu cümle [7] Abeywickrama vd. için **yanlış**. O makale çalışma süresini ölçüyor ve saniye cinsinden raporluyor. Kaynak: basılı s. 5860, PDF s. 12, Table II "Convergence Time Comparison", ölçüm MATLAB R2017a ve Core i7-2600 üzerinde. Penalty-based yöntem 2.8–13.6 s, two-stage yöntem 0.04–0.51 s sürüyor. Cümlenin ikinci yarısı ("not a latency measured against the coherence time") doğru kalıyor: süre ölçülmüş ama eşevreli kalma süresiyle (coherence time) karşılaştırılmamış. Düzeltme önerisi [7] başlığı altında. Bu bulgu tezin ana iddiasını zayıflatmıyor, tersine destekliyor: ölçülen süreler saniye mertebesinde, yani hareketli bir kullanıcının eşevreli kalma süresinden kat kat uzun. Ama "literatürde süre yalnızca karmaşıklık mertebesi olarak veriliyor" genellemesi bu haliyle savunulamaz.

---

## [6] Pei vd., IEEE TCOM 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Xilong Pei, Haifan Yin, Li Tan, Lin Cao, Zhanpeng Li, Kai Wang, Kun Zhang, Emil Björnson. Başlık: "RIS-Aided Wireless Communications: Prototyping, Adaptive Beamforming, and Indoor/Outdoor Field Trials". Dergi: IEEE Transactions on Communications, VOL. 69, NO. 12, DECEMBER 2021. İlk sayfa 8627; PDF 14 sayfa olduğu için son sayfa 8640. DOI: 10.1109/TCOMM.2021.3116151. **UYUŞUYOR.**
- **Makale 2'de nerede:** Giriş, ilk paragraf: "…and another prototype has strengthened a link through a concrete wall [6]."
- **Kaynakta karşılığı:**
  - Basılı s. 8627, PDF s. 1, Özet: "In our indoor test, where the transmitter and receiver are separated by a 30 cm thick concrete wall, our RIS prototype provides a 26 dB power gain compared to the baseline case where the RIS is replaced by a copper plate."
  - Basılı s. 8636, PDF s. 10, §V-D "Indoor Over-the-Air Test": "The transmitter and receiver are separated by a 30 cm thick concrete wall, which includes a 53 cm thick pillar in the middle." Aynı sayfada: "The results show that an RIS configured using the proposed algorithm brings a power gain of around 26 dB."
  - Aynı sayfa, Fig. 15 alt yazısı: verici beton duvarın arkasında ve RIS'e yönelik, gönderim gücü −16 dBm. Alınan taban bant gücü RIS ile yaklaşık −23.75 dBFS, bakır plaka ile −49.38 dBFS.
  - Basılı s. 8638, PDF s. 12, §VI "Conclusion": "In the indoor scenario, the RIS provided a 26 dB power gain at the receiver, even when the signal is blocked by a 30 cm thick concrete wall."
- **Değerlendirme:** Kaynak, 5.8 GHz bandında çalışan 1100 elemanlı bir RIS prototipini anlatıyor. Kapalı alan deneyinde verici ile alıcı arasında 30 cm kalınlığında beton bir duvar var (ortasında 53 cm kalınlığında betonarme kolon). RIS, alıcıdaki gücü yaklaşık 26 dB artırıyor. "Strengthened a link through a concrete wall" ifadesi bu ölçümü doğru özetliyor.
  - Bir nüans var: 26 dB, RIS'siz durumla değil, **aynı boyutta bir bakır plakayla** karşılaştırıldığında elde ediliyor. Makale 2 bir sayı vermediği için bu bir hata değil. Sayı eklenecekse karşılaştırma tabanı da yazılmalı.
  - Çalışma süresi ve karmaşıklık: Algorithm 1 (basılı s. 8633, PDF s. 7, §IV) yalnızca karmaşıklık ve geri besleme turu sayısı olarak veriliyor: "Algorithm 1 determines the reflection coefficients using M + N feedback iterations … The computational complexity order is O(M + N)." Saniye ya da milisaniye cinsinden süre ölçümü yok ("CPU", "running time", "seconds", "ms", "MATLAB" araması sonuç vermedi).
- **Karar:** **DOĞRU.** Sayı eklenirse önerilen biçim: "…strengthened a link through a 30 cm concrete wall by 26 dB relative to a copper plate [6]."

---

## [7] Abeywickrama vd., IEEE TCOM 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Samith Abeywickrama, Rui Zhang, Qingqing Wu, Chau Yuen. Başlık: "Intelligent Reflecting Surface: Practical Phase Shift Model and Beamforming Optimization". Dergi: IEEE Transactions on Communications, VOL. 68, NO. 9, SEPTEMBER 2020. İlk sayfa 5849; PDF 15 sayfa olduğu için son sayfa 5863. DOI: 10.1109/TCOMM.2020.3001125. **UYUŞUYOR.**
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) Giriş: "Choosing those phases is a hard, non-convex problem, attacked with iterative solvers [2,7,8,9,10]…"
  - (b) İlgili çalışmalar: "Joint precoding and phase design has been addressed with … practical phase-dependent amplitude models [7], …" Hemen ardından gelen cümle de bu kaynağı kapsıyor: "These works report the objective value reached; run time, when discussed, is a complexity order, not a latency measured against the coherence time."
- **Kaynakta karşılığı:**
  - (a) Basılı s. 5850, PDF s. 2, §I (katkılar): "However, the problem in this case is non-convex and difficult to be optimally solved in general, for which we propose two iterative algorithms to find suboptimal solutions efficiently by utilizing the alternating optimization (AO) and penalty-based optimization techniques, respectively."
  - (b) Basılı s. 5852, PDF s. 4, §III-B "Proposed Phase Shift Model", denklem (5): β_n(θ_n) = (1 − β_min)((sin(θ_n − φ) + 1)/2)^α + β_min. Alıntı: "we propose in this subsection an analytical model for the phase shift which is in general applicable to a variety of semiconductor devices used for implementing IRS." Özette (basılı s. 5849, PDF s. 1): "we propose in this paper a practical phase shift model that captures the phase-dependent amplitude variation in the element-wise reflection design."
  - Çalışma süresi: Basılı s. 5860, PDF s. 12, §VI-B: "Next, in Table II, we compare the average central processing unit (CPU) running time of the extended penalty-based algorithm and two-stage algorithm for different (K, M) pairs and N. The simulations are implemented on MATLAB R2017a and tested on a PC with a Core i7-2600 CPU, 8-GB of RAM, and Windows 10." Table II, "Convergence Time Comparison" (sayfa görüntüsünden okundu): N = 10…50 ve (K, M) ∈ {(2,4), (4,8)} için penalty-based yöntem 2.8–13.6 s, two-stage yöntem 0.04–0.51 s. Karmaşıklık mertebeleri de veriliyor (basılı s. 5857, PDF s. 9, §V-B ve §V-C).
- **Değerlendirme:** Kaynak, eleman yansıma genliğinin faza bağlı olduğu pratik bir model öneriyor (denklem 5). Bu model altında, kullanıcı başına SINR kısıtlarıyla AP gönderim gücünü en aza indiren ortak aktif/pasif hüzmeleme problemini çözüyor. Çözüm yinelemeli: AO, penalty-based ve two-stage algoritmalar. Problemin dışbükey olmadığını açıkça söylüyor. Bu nedenle (a) ve (b)'deki atıflar doğru.
  - Küçük bir not (b) için: "phase-dependent amplitude models" bir çözüm yöntemi değil, bir donanım modeli. Cümle, yöntem listesi ("addressed with … block coordinate descent, fractional programming…") içinde bunu bir yöntem gibi sıralıyor. Anlam yine de anlaşılır; zorunlu değil ama "…under practical phase-dependent amplitude models with alternating and penalty-based optimization [7]" daha kesin olur.
  - **Asıl sorun ardından gelen cümlede.** Kaynak çalışma süresini yalnızca karmaşıklık mertebesi olarak vermiyor; CPU süresini saniye cinsinden ölçüp tabloluyor (Table II). Dolayısıyla "run time, when discussed, is a complexity order" genellemesi bu kaynak için yanlış. Ölçülen süre eşevreli kalma süresiyle karşılaştırılmıyor; o kısım doğru.
- **Karar:** (a) **DOĞRU.** (b) atıfın kendisi **DOĞRU**; ardından gelen genelleme **DÜZELTİLMELİ**. Önerilen biçim: "These works report the objective value reached; run time is usually given as a complexity order, and where it is measured (e.g., 0.04–13.6 s of MATLAB CPU time in [7]) it is not compared against the coherence time."

---

## [8] Pan vd., IEEE TWC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Cunhua Pan, Hong Ren, Kezhi Wang, Wei Xu, Maged Elkashlan, Arumugam Nallanathan, Lajos Hanzo. Başlık: "Multicell MIMO Communications Relying on Intelligent Reflecting Surfaces". Dergi: IEEE Transactions on Wireless Communications, VOL. 19, NO. 8, AUGUST 2020. İlk sayfa 5218; PDF 16 sayfa olduğu için son sayfa 5233. DOI: 10.1109/TWC.2020.2990766. **UYUŞUYOR.**
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) Giriş ("hard, non-convex problem, attacked with iterative solvers [2,7,8,9,10]").
  - (b) İlgili çalışmalar: "…block coordinate descent [8]…"
- **Kaynakta karşılığı:**
  - (a) ve (b) Basılı s. 5218, PDF s. 1, Özet: "Due to the non-convexity of the problem, we first reformulate it into an equivalent one, which is solved by using the block coordinate descent (BCD) algorithm, where the precoding matrices and phase shifts are alternately optimized." Aynı özet: "A pair of efficient algorithms are proposed for solving the phase shift optimization problem, namely the Majorization-Minimization (MM) Algorithm and the Complex Circle Manifold (CCM) Method."
  - Basılı s. 5219, PDF s. 2, §I (katkılar): "we first reformulate the original problem into an equivalent one by exploiting the equivalence between the data rate and the weighted minimum mean-square error (WMMSE). Then, the block coordinate descent (BCD) algorithm is proposed for alternately optimizing the TPC matrices at the BSs and the passive beamforming at the IRS."
  - Çalışma süresi: Basılı s. 5225, PDF s. 8, §III-C "3) Complexity Analysis": "The complexity of these algorithms is summarized in Table I. It can be observed that the complexity mainly depends on the number of iterations required for convergence." Basılı s. 5228, PDF s. 11, §V: "the proposed algorithms converge within 200 iterations". Saniye cinsinden süre ölçümü yok ("CPU", "running time", "seconds", "MATLAB" araması yalnızca kaynakçadaki CVX girdisini buldu).
- **Değerlendirme:** Kaynak, çok hücreli ve çok antenli bir sistemde, hücre kenarındaki bir IRS yardımıyla ağırlıklı toplam hızı (WSR) en büyüklüyor. Problem dışbükey değil. WMMSE eşdeğerliğiyle yeniden yazılıyor ve BCD ile çözülüyor. Faz alt problemi MM ya da karmaşık çember manifoldu (CCM) yöntemiyle çözülüyor. "Block coordinate descent [8]" etiketi doğru; (a) da doğru.
  - Bilgi notu: Bu kaynak aynı zamanda bir WMMSE tabanlı ve manifold tabanlı yöntem. Sonuç bölümündeki "WMMSE [10] and manifold methods were not timed" cümlesine, ilgili çalışmalardaki "fixed-point and manifold methods" listesine [8] eklenebilir. Zorunlu değil.
  - Karmaşıklık mertebe ve yineleme sayısı olarak veriliyor; Makale 2'nin "complexity order" genellemesine uyuyor.
- **Karar:** **DOĞRU.**

---

## [9] Guo vd., IEEE TWC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Huayan Guo, Ying-Chang Liang, Jie Chen, Erik G. Larsson. Başlık: "Weighted Sum-Rate Maximization for Reconfigurable Intelligent Surface Aided Wireless Networks". Dergi: IEEE Transactions on Wireless Communications, VOL. 19, NO. 5, MAY 2020. İlk sayfa 3064; PDF 13 sayfa olduğu için son sayfa 3076. DOI: 10.1109/TWC.2020.2970061. **UYUŞUYOR.**
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) Giriş ("hard, non-convex problem, attacked with iterative solvers [2,7,8,9,10]").
  - (b) İlgili çalışmalar: "…fractional programming [9]…"
- **Kaynakta karşılığı:**
  - (b) Basılı s. 3064, PDF s. 1, Özet: "For perfect CSI setup, a low-complexity algorithm is proposed to obtain the stationary solution for the joint design problem by utilizing the fractional programming technique." Basılı s. 3065, PDF s. 2, §I: "we decompose the original problem into four disjoint blocks by utilizing the fractional programming (FP) technique [30]. Subsequently, low-complexity algorithm is designed based on the non-convex block coordinate descent (BCD) method [31]."
  - (a) Basılı s. 3067, PDF s. 4: "…since the optimization variables W and θ are deeply coupled in the non-convex objective function."
  - Çalışma süresi: yalnızca karmaşıklık mertebesi. Basılı s. 3070, PDF s. 7: "total complexity of the proposed BCD method is O(I_O(2KNM + KM² + K²N²)), where I_O is the number of iterations." Yakınsama yineleme sayısı üzerinden gösteriliyor (basılı s. 3073, PDF s. 10). Saniye cinsinden süre yok ("CPU", "running time", "seconds", "MATLAB" araması yalnızca kaynakçadaki Manopt girdisini buldu).
- **Değerlendirme:** Kaynak, RIS destekli çok kullanıcılı MISO aşağı bağlantıda, kusursuz ve kusurlu CSI altında WSR'yi en büyüklüyor. Kusursuz CSI için FP ile dört bloğa ayırma ve dışbükey olmayan BCD kullanılıyor; kusurlu CSI için stokastik SCA. Karşılaştırma tabanı olarak Riemann eşlenik gradyanlı (manifold) bir alternating optimization da veriliyor (§III). "Fractional programming [9]" etiketi kaynağın ana katkısıyla birebir örtüşüyor; (a) da doğru.
- **Karar:** **DOĞRU.**

---

## [10] Choi vd., IEEE TCOM 2024

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Hyuckjin Choi, A. Lee Swindlehurst, Junil Choi. Başlık: "WMMSE-Based Rate Maximization for RIS-Assisted MU-MIMO Systems". Dergi: IEEE Transactions on Communications, VOL. 72, NO. 8, AUGUST 2024. İlk sayfa 5194; PDF 15 sayfa olduğu için son sayfa 5208. DOI: 10.1109/TCOMM.2024.3381707. **UYUŞUYOR.**
- **Makale 2'de nerede:** Üç yerde atıf var.
  - (a) Giriş ("hard, non-convex problem, attacked with iterative solvers [2,7,8,9,10]").
  - (b) İlgili çalışmalar: "…weighted minimum mean-square error (WMMSE) methods [10] built on the algorithm of [Shi2011TSP]."
  - (c) Sonuç/kısıtlar: "Semidefinite relaxation [2], WMMSE [10] and manifold methods were not timed, …"
- **Kaynakta karşılığı:**
  - (b) Basılı s. 5194, PDF s. 1, Özet: "This paper proposes rate maximization techniques for both single-user and multiuser MIMO systems, based on the well-known weighted minimum mean square error (WMMSE) criterion." Basılı s. 5197, PDF s. 4, §III: "The WMMSE algorithm is a popular approach for solving the sum-rate maximization problem [35], [36]." Kaynakçadaki [36]: "Q. Shi, M. Razaviyayn, Z.-Q. Luo, and C. He, 'An iteratively weighted …'" (PDF s. 15). Yani Shi vd. 2011 açıkça temel alınıyor.
  - (a) Basılı s. 5199, PDF s. 6, §III: "Since the sum-rate is a non-convex function, it is difficult to find the global optimum."
  - (c) Çalışma süresi: yalnızca karmaşıklık ifadeleri. Basılı s. 5203, PDF s. 10: "The computational complexity of the various techniques in the SU-MIMO case is detailed in Table I." Basılı s. 5205, PDF s. 12: "Finally, we analyze the complexity of the considered MU-MIMO techniques in Table II." Table II (sayfa görüntüsünden okundu) MaxR ve MinE için kapalı biçimli işlem sayısı ifadeleri veriyor, örneğin MinE: 3K²LN³ + 2K²MLN² + L³. Saniye cinsinden süre yok ("CPU", "running time", "seconds", "ms", "MATLAB" araması sonuç vermedi).
- **Değerlendirme:** Kaynak, tensör tabanlı bir RIS modeliyle SU- ve MU-MIMO'da toplam hızı en büyüklüyor. BS ön kodlayıcısı WMMSE ile güncelleniyor. RIS fazları ise toplam hızın (MaxR-WMMSE) ya da WMSE'nin (MinE-WMMSE) kapalı biçimli gradyanıyla güncelleniyor; bir CNN-WMMSE çeşidi de var. Yöntemi "WMMSE methods … built on the algorithm of [Shi2011TSP]" diye nitelemek doğru.
  - (c) için: WMMSE, Choi vd.'nin yöntemi; kaynak yalnızca karmaşıklık mertebesi veriyor, süre ölçmüyor. "Not timed" ifadesi Makale 2'nin kendi kısıtını anlatıyor ve kaynakla çelişmiyor.
  - Küçük bir nüans: Choi'deki RIS faz güncellemesi bir gradyan yöntemi; "WMMSE" etiketi, WMMSE çerçevesinde yürütülen ortak algoritmanın tamamını kastediyor. Bu kullanım kaynağın kendi adlandırmasıyla (MaxR-WMMSE, MinE-WMMSE) aynı.
- **Karar:** (a), (b), (c) **DOĞRU.**

---

## Çalışma süresi / karmaşıklık raporlama özeti

Bu tablo, tezin "literatür yöntemleri nadiren zamanlıyor" iddiasıyla ilgili.

| n | Karmaşıklık mertebesi | Ölçülmüş süre (saniye) | Eşevreli kalma süresiyle karşılaştırma |
|---|---|---|---|
| [6] | Var: O(M + N), M + N geri besleme turu (s. 8633) | Yok | Yok |
| [7] | Var (s. 5857) | **Var:** Table II, 0.04–13.6 s, MATLAB R2017a / i7-2600 (s. 5860) | Yok |
| [8] | Var: Table I; yakınsama ≤ 200 yineleme (s. 5225, 5228) | Yok | Yok |
| [9] | Var: O(I_O(2KNM + KM² + K²N²)) (s. 3070) | Yok | Yok |
| [10] | Var: Table I–II işlem sayısı ifadeleri (s. 5203, 5205) | Yok | Yok |

---

## Özet tablo

| n | Karar | Gerekçe |
|---|---|---|
| [6] | DOĞRU | §V-D (s. 8636): 30 cm beton duvar (53 cm kolonlu) arkasındaki vericiye karşı yaklaşık 26 dB güç kazancı, 5.8 GHz, 1100 eleman; taban bakır plaka; künye uyuşuyor |
| [7] | DOĞRU (atıf); ardından gelen cümle DÜZELTİLMELİ | Faza bağlı genlik modeli denklem (5) (s. 5852), dışbükey olmayan problem ve yinelemeli AO/penalty (s. 5850) var. Ancak kaynak CPU süresini **ölçüyor** (Table II, 0.04–13.6 s, s. 5860), bu yüzden "run time, when discussed, is a complexity order" genellemesi yanlış; künye uyuşuyor |
| [8] | DOĞRU | Özet (s. 5218): dışbükey olmayan problem, BCD; faz alt problemi MM ve CCM (manifold), WMMSE eşdeğerliği (s. 5219); süre yok, karmaşıklık var; künye uyuşuyor |
| [9] | DOĞRU | Özet ve §I (s. 3064–3065): FP + dışbükey olmayan BCD; dışbükey olmama (s. 3067); süre yok, karmaşıklık var; künye uyuşuyor |
| [10] | DOĞRU | Özet (s. 5194): WMMSE tabanlı; Shi vd. [36] temel alınıyor (s. 5197); dışbükey olmama (s. 5199); süre yok, karmaşıklık tabloları var (s. 5203, 5205); künye uyuşuyor |

Künye uyuşmazlığı bulunmadı. ÇIKARILMALI kararı yok. Tek düzeltme, ilgili çalışmalardaki çalışma süresi genellemesi ([7] nedeniyle).
