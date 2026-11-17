# Makale 2 — Kaynak kontrolü, Grup 3: Huang2020JSAC, Yu2019ICCC, Shi2011TSP, Jiang2021JSAC, Monga2021SPM

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları, PDF'in üst ya da alt bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

Atıf yerleri `grep -rn <anahtar> --include=*.tex` ile tarandı (özet `mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`). Beş anahtar yalnızca iki dosyada geçiyor: `sections/section_01_introduction.tex` ve `sections/section_02_related_work.tex`. Özette ve tablolarda bu anahtarlara atıf yok.

**En üste yazılması gereken bulgu (CLAUDE.md kural 10):** İlgili çalışmalar bölümündeki "These works report the objective value reached; run time, when discussed, is a complexity order, not a latency measured against the coherence time." cümlesi iki kaynakta yanlış. Yu2019ICCC, Fig. 4'te saniye cinsinden ölçülmüş ortalama çalışma süresi veriyor. Shi2011TSP de Fig. 4'te ortalama CPU süresi veriyor. Cümlenin ikinci yarısı ("not a latency measured against the coherence time") iki kaynak için de doğru. Ayrıntı ve öneri [Yu2019ICCC] ile [Shi2011TSP] başlıklarında.

---

## [Huang2020JSAC] Huang, Mo, Yuen, IEEE JSAC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Chongwen Huang, Ronghong Mo, Chau Yuen. Başlık: "Reconfigurable Intelligent Surface Assisted Multiuser MISO Systems Exploiting Deep Reinforcement Learning". Dergi: IEEE Journal on Selected Areas in Communications, Vol. 38, No. 8, August 2020. İlk sayfa 1839; PDF 12 sayfa olduğu için son sayfa 1850 (PDF s. 11'in üst bilgisi 1849, tutarlı). DOI: 10.1109/JSAC.2020.3000835. **UYUŞUYOR.**
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) Giriş, birinci paragraf: "Choosing those phases is a hard, non-convex problem, attacked with iterative solvers [...] and, increasingly, with learned policies~\cite{Huang2020JSAC}."
  - (b) İlgili çalışmalar, "Learning" paragrafı: "Learned policies include deep reinforcement learning for joint precoding and phase design~\cite{Huang2020JSAC} and learning to reflect directly from pilots~\cite{Jiang2021JSAC}."
- **Kaynakta karşılığı:**
  - Basılı s. 1839, PDF s. 1, Özet: "In this paper, we investigate the joint design of transmit beamforming matrix at the base station and the phase shift matrix at the RIS, by leveraging recent advances in deep reinforcement learning (DRL)." Aynı özette: "Unlike the most reported works utilizing the alternating optimization techniques to alternatively obtain the transmit beamforming and phase shifts, the proposed DRL based algorithm obtains the joint design simultaneously as the output of the DRL neural network."
  - Kullanılan DRL yöntemi DDPG. Basılı s. 1841, PDF s. 3, §I: "...we resort to DDPG to develop our algorithm"; ayrıntısı §III-B "DDPG"de (basılı s. 1844, PDF s. 6).
  - Karşılaştırma tabanları: basılı s. 1846, PDF s. 8, §V-A "Setting and Benchmarks": WMMSE algoritması ve "an iterative algorithm based on fractional programming (FP) with the ZF". Sonuç: basılı s. 1847, PDF s. 9: "...the comparable sum-rate performance with these state-of-the-art benchmarks (WMMSE and FP optimization algorithm with ZF)".
  - Hız gerekçesi: basılı s. 1840, PDF s. 2, §I: "Actually, DL based approaches are able to significantly reduce the complexity and computation time utilizing the offline prediction, but often require an exhaustive sample library for online training."
  - Çalışma süresi: "running time", "run time", "CPU", "seconds" araması sonuç vermedi. Simülasyonlarda yakınsama yalnızca DRL "time steps" ekseninde gösteriliyor (Fig. 6–12, basılı s. 1847–1849). Duvar saati süresi ya da tabanlarla eşit koşulda zaman karşılaştırması **yok**.
- **Değerlendirme:** Kaynak, çok kullanıcılı MISO aşağı bağlantıda baz istasyonu hüzmeleme matrisi G ile RIS faz matrisi Φ'yi birlikte, DDPG tabanlı bir DRL ajanıyla tasarlıyor; ödül toplam hız. Yani gerçekten DRL ve gerçekten ortak "transmit beamforming + phase" tasarımı. (a)'daki "learned policies" ifadesi de bir RL politikası için tam yerinde. "Joint precoding and phase design" ifadesi kaynaktaki "joint design of transmit beamforming matrix ... and the phase shift matrix" ile örtüşüyor.
  - Makale 2'nin "Learned methods are usually motivated by speed, but ... classical baselines are rarely tuned or timed under the same conditions" savını bu kaynak doğrudan destekliyor: girişte DL'nin "computation time"ı düşürdüğünü gerekçe olarak anıyor, ama WMMSE ve FP tabanlarına karşı hiçbir süre ölçümü vermiyor; yalnızca toplam hızın "comparable" olduğunu söylüyor. Bu, jüri sorusuna karşı iyi bir örnek. İstenirse bu cümleye de [Huang2020JSAC] eklenebilir (zorunlu değil).
  - Küçük not: kaynağın DRL'i kanal durumunu (CSI) gözlem olarak alıyor ve kanal bilgisi doğru varsayılıyor; hareketlilik ya da kanal yaşlanması incelenmiyor. Atıf cümleleri bunun aksini iddia etmediği için sorun yok.
- **Karar:** (a) ve (b) **DOĞRU.**

---

## [Yu2019ICCC] Yu, Xu, Schober, IEEE/CIC ICCC 2019

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Xianghao Yu, Dongfang Xu, Robert Schober. Başlık: "MISO Wireless Communication Systems via Intelligent Reflecting Surfaces", altında "(Invited Paper)". Yayın yeri: 2019 IEEE/CIC International Conference on Communications in China (ICCC). Sayfalar: PDF s. 1'in alt bilgisi 735, PDF s. 6'nın alt bilgisi 740, yani 735–740. **UYUŞUYOR.**
  - DOI PDF'te basılı değil ("doi", "Digital Object" araması boş). Kaynakçadaki 10.1109/ICCChina.2019.8855810 PDF'ten doğrulanamadı; IEEE Xplore'dan bir kez kontrol edilmesi önerilir.
  - Kaynakçada "(Invited Paper)" başlığın içine yazılmış. PDF'te başlıktan ayrı bir not olarak duruyor. Kalabilir; IEEE biçiminde genelde başlıktan çıkarılır (isteğe bağlı).
- **Makale 2'de nerede:** İlgili çalışmalar, "RIS phase optimization" paragrafı: "Joint precoding and phase design has been addressed with [...] fixed-point and manifold methods~\cite{Yu2019ICCC} [...]. These works report the objective value reached; run time, when discussed, is a complexity order, not a latency measured against the coherence time."
- **Kaynakta karşılığı:**
  - Basılı s. 735, PDF s. 1, Özet: "Two efficient algorithms exploiting fixed point iteration and manifold optimization techniques, respectively, are developed for solving the resulting non-convex optimization problem. The proposed algorithms not only achieve a higher spectral efficiency but also lead to a lower computational complexity than the state-of-the-art approach."
  - Basılı s. 737, PDF s. 3: §III-B "Fixed Point Iteration" (Algorithm 1 "Fixed Point Iteration") ve §III-C "Manifold Optimization"; Algorithm 2 "CG Method Based Manifold Optimization" basılı s. 738, PDF s. 4.
  - Ortak tasarımın yapısı: basılı s. 736, PDF s. 2, §II: "Once the solution for v in P1 is obtained, the corresponding beamforming vector f is optimally given by the maximum ratio transmission (MRT) strategy".
  - Karmaşıklık mertebesi: basılı s. 739, PDF s. 5, §III-D "(2) Computational complexity": CG yöntemi için O(M^1.5), SDR için O((M+1)^6).
  - **Ölçülmüş çalışma süresi:** basılı s. 739, PDF s. 5, Fig. 4 başlığı: "Average spectral efficiency and run time for different numbers of IRS reflecting elements when Nt = 5, rAI = rAu = 60 m, and rIu = 10 m." Fig. 4'ün y ekseni: "Average run time (s)". Basılı s. 740, PDF s. 6, §IV-B: "In addition, in Fig. 4 (right hand side), we plot the average run time of the proposed algorithms. As can be observed, the proposed algorithms require much less run time than the SDR method, which confirms the discussion at the end of Section III-D."
- **Değerlendirme:** "Fixed-point and manifold methods" atfı **doğru**: kaynak, yanlış atıf için klasik bir yer olsa da burada gerçekten iki yöntem öneriyor, bir sabit nokta yinelemesi (Algorithm 1) ve karmaşık çember manifoldu üzerinde eşlenik gradyan (Algorithm 2). Bir nüans var: sistem tek kullanıcılı, noktadan noktaya MISO. Hüzmeleyici f, fazlar bulunduktan sonra kapalı biçimde MRT ile veriliyor; yani "joint precoding and phase design" problemi fiilen faz vektörü v üzerinde bir optimizasyona indirgeniyor. "Joint precoding and phase design has been addressed with ..." cümlesi bunu yanlış göstermiyor (kaynak da "jointly optimized" diyor).
  - Sorun, paragrafın kapanış cümlesinde. "Run time, when discussed, is a complexity order" ifadesi bu kaynak için **yanlış**: kaynak karmaşıklık mertebesinin yanında, Fig. 4'te saniye cinsinden ölçülmüş ortalama çalışma süresini de veriyor ve SDR'ye karşı karşılaştırıyor. Doğru olan kısım şu: bu süre statik bir kanal realizasyonunda ölçülüyor ve kanal uyum süresiyle (coherence time) ya da hareketlilikle ilişkilendirilmiyor. Makale 2'nin asıl savı ("not a latency measured against the coherence time") ayakta kalıyor; yalnızca "complexity order" genellemesi düzeltilmeli. Shi2011TSP için de aynı durum var (aşağıda).
- **Karar:** Atıf ("fixed-point and manifold methods") **DOĞRU**. Kapanış cümlesi **DÜZELTİLMELİ.** Öneri: "These works report the objective value reached; run time, when discussed, is a complexity order or a CPU time on a fixed channel realization~\cite{Yu2019ICCC,Shi2011TSP}, never a latency measured against the coherence time."

---

## [Shi2011TSP] Shi, Razaviyayn, Luo, He, IEEE TSP 2011

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qingjiang Shi, Meisam Razaviyayn, Zhi-Quan Luo, Chen He. Başlık: "An Iteratively Weighted MMSE Approach to Distributed Sum-Utility Maximization for a MIMO Interfering Broadcast Channel". Dergi: IEEE Transactions on Signal Processing, Vol. 59, No. 9, September 2011. İlk sayfa 4331; PDF 10 sayfa olduğu için son sayfa 4340. DOI: 10.1109/TSP.2011.2147784. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, "RIS phase optimization" paragrafı: "[...] and weighted minimum mean-square error (WMMSE) methods~\cite{Choi2024TCOM} built on the algorithm of~\cite{Shi2011TSP}. These works report the objective value reached; run time, when discussed, is a complexity order, not a latency measured against the coherence time."
- **Kaynakta karşılığı:**
  - Basılı s. 4331, PDF s. 1, Özet: "In this paper, we propose a linear transceiver design algorithm for weighted sum-rate maximization that is based on iterative minimization of weighted mean-square error (MSE). The proposed algorithm only needs local channel knowledge and converges to a stationary point of the weighted sum-rate maximization problem."
  - Algoritma: basılı s. 4334–4335, PDF s. 4–5, §III "WMMSE Algorithm for Sum-Utility Maximization"; Table I "Pseudo code of the proposed WMMSE algorithm for MIMO-IBC". Yöntem blok koordinat inişi: PDF s. 5, "we propose to use the block coordinate descent method".
  - Karmaşıklık: §IV "Complexity Analysis" (basılı s. 4335–4336, PDF s. 5–6), iterasyon başına mertebe.
  - **Ölçülmüş süre:** basılı s. 4337, PDF s. 7, §V: "Fig. 4 represents the average CPU time comparison of the two algorithms under the same termination criterion. It can be observed that the WMMSE algorithm significantly outperform the ILA algorithm when the number of users is large." (Fig. 4: "Average CPU time versus the number of users in the MIMO IFC case".)
- **Değerlendirme:** Kaynak, WMMSE algoritmasının özgün makalesi: ağırlıklı toplam hız maksimizasyonunu ağırlıklı MSE minimizasyonuna denk kılıyor ve alıcı, ağırlık ve verici üzerinde blok koordinat inişiyle durağan bir noktaya yakınsıyor. Kaynakta RIS yok (2011, MIMO girişimli yayın kanalı). Makale 2 de onu RIS yöntemi olarak değil, RIS için kullanılan WMMSE yöntemlerinin "üzerine kurulduğu algoritma" olarak anıyor. Bu doğru ve yerinde. "Weighted minimum mean-square error (WMMSE)" açılımı da doğru.
  - Kapanış cümlesi için: bu kaynak, aynı sonlandırma ölçütü altında iki algoritmanın ortalama CPU süresini karşılaştırıyor (Fig. 4). Yani "run time ... is a complexity order" bu kaynak için de yanlış. Burada eşit koşulda zamanlanmış bir klasik-klasik karşılaştırma var; bu, Makale 2'nin "rarely timed under the same conditions" savıyla çelişmiyor (o sav öğrenilen ve klasik yöntemler arası), ama "complexity order" genellemesiyle çelişiyor. Süre yine statik kanal realizasyonlarında ölçülüyor; uyum süresiyle ilişki yok.
- **Karar:** Atıf (WMMSE'nin kaynağı) **DOĞRU**. Kapanış cümlesi **DÜZELTİLMELİ**; öneri [Yu2019ICCC] başlığında.

---

## [Jiang2021JSAC] Jiang, Cheng, Yu, IEEE JSAC 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Tao Jiang, Hei Victor Cheng, Wei Yu. Başlık: "Learning to Reflect and to Beamform for Intelligent Reflecting Surface With Implicit Channel Estimation". Dergi: IEEE Journal on Selected Areas in Communications, Vol. 39, No. 7, July 2021. İlk sayfa 1931; PDF 15 sayfa olduğu için son sayfa 1945. DOI: 10.1109/JSAC.2021.3078502. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, "Learning" paragrafı: "Learned policies include deep reinforcement learning for joint precoding and phase design~\cite{Huang2020JSAC} and learning to reflect directly from pilots~\cite{Jiang2021JSAC}."
- **Kaynakta karşılığı:**
  - Basılı s. 1931, PDF s. 1, Özet: "This is achieved by using a deep neural network to parameterize the mapping from the received pilots (plus any additional information, such as the user locations) to an optimized system configuration, and by adopting a permutation invariant/equivariant graph neural network (GNN) architecture to capture the interactions among the different users in the cellular network."
  - Aynı sayfa, §I: "We advocate the use of machine learning techniques to bypass explicit channel estimation and to directly design the beamforming and reflective patterns to optimize a system-wide objective."
  - Çalışma süresi: basılı s. 1938, PDF s. 8: "We remark that the training of the neural network is done offline, so it does not affect the run-time complexity of the proposed approach." "running time", "CPU", "seconds" araması sonuç vermedi; ölçülmüş süre **yok**. Karşılaştırma tabanları (LMMSE ya da derin öğrenmeyle kanal kestirimi + BCD/SDR) yalnızca hız/oran ekseninde karşılaştırılıyor (§VI, basılı s. 1940–1942). SDR için yalnızca nitel not var, basılı s. 1942, PDF s. 12: "The complexity of SDR is high; this is why we choose a simulation setting with N = 20."
  - Kanal varsayımı: basılı s. 1934, PDF s. 4, §II: IRS katsayıları "remain constant during a coherence block".
- **Değerlendirme:** Kaynak, alınan pilotlardan doğrudan BS hüzmeleyicilerine ve IRS yansıma katsayılarına giden eşlemeyi bir GNN ile öğreniyor ve açık kanal kestirimini atlıyor ("implicit channel estimation"). Hem toplam hız hem en küçük hız maksimizasyonu inceleniyor. "Learning to reflect directly from pilots" ifadesi kaynağın başlığını ve yöntemini doğru özetliyor. Kaynak BS hüzmelemesini de öğreniyor ("and to beamform"); cümle bunu dışlamıyor, eksik ama yanlış değil.
  - "Learned policies include ..." ifadesi bu kaynak için tam terim değil: kaynak bir RL politikası değil, gözetimsiz (yardımcı fayda üzerinden) eğitilmiş bir eşleme (GNN). Gevşek bir kullanım; yanıltıcı değil. Çalışma süresi açısından kaynak Makale 2'nin savını destekliyor: eğitimin çevrim dışı olduğunu ve "run-time complexity"yi etkilemediğini söylüyor, ama çıkarım süresini ölçmüyor ve tabanlarla eşit koşulda zamanlama yapmıyor.
- **Karar:** **DOĞRU.** İsteğe bağlı netleştirme: "...and learning to reflect and beamform directly from received pilots with a graph neural network~\cite{Jiang2021JSAC}."

---

## [Monga2021SPM] Monga, Li, Eldar, IEEE SPM 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Vishal Monga, Yuelong Li, Yonina C. Eldar. Başlık: "Algorithm Unrolling", alt başlık "Interpretable, efficient deep learning for signal and image processing". Dergi: IEEE Signal Processing Magazine, March 2021. İlk sayfa 18 (PDF s. 1 alt bilgisi), son sayfa 44 (PDF s. 27 alt bilgisi). DOI: 10.1109/MSP.2020.3016905. **UYUŞUYOR.**
  - Cilt ve sayı (Vol. 38, No. 2) PDF'te basılı değil; dergi alt bilgisinde yalnızca "March 2021" var. Mart 2021 sayısı için 38(2) beklenen değer, ama PDF'ten doğrulanamadı.
- **Makale 2'de nerede:** İlgili çalışmalar, "Learning" paragrafı: "Algorithm unrolling turns an optimizer's iterations into network layers~\cite{Monga2021SPM}; it has been applied to RIS beamforming [...]".
- **Kaynakta karşılığı:**
  - Basılı s. 20, PDF s. 3, Giriş: "Specifically, each iteration of the algorithm step is represented as one layer of the network. Concatenating these layers forms a deep neural network."
  - Basılı s. 23, PDF s. 6: "...a deep network by mapping each iteration into a single network layer and stacking a finite number of layers together."
  - Süre: basılı s. 34, PDF s. 17, Table 2 "Selected results for the running time and the parameter count"; metinde: "Compared to its iterative counterpart, unrolling often dramatically boosts the computational speed. For instance, it was reported in [18] that the LISTA may be 20 times faster than the ISTA after training".
- **Değerlendirme:** Kaynak, algoritma açmanın (unrolling/unfolding) bir derleme makalesi ve tanımı tam olarak atıf cümlesindeki gibi veriyor: yinelemeli algoritmanın her adımı bir ağ katmanı olur, katmanlar art arda eklenir. "Optimizer" kelimesi biraz dar (kaynak genel "iterative algorithms" diyor; ISTA gibi optimizasyon algoritmaları en tipik örnek), ama yanlış değil. Kaynak süreyi de raporluyor (Table 2), ancak bunlar başka çalışmalardan derlenmiş sonuçlar ve sinyal/görüntü işleme alanında; RIS ya da kanal değişim hızıyla ilgisi yok. Makale 2'nin "learned methods are usually motivated by speed" savını bu kaynak açıkça destekliyor.
- **Karar:** **DOĞRU.**

---

## Özet tablo

| Anahtar | Karar | Gerekçe |
|---|---|---|
| Huang2020JSAC | DOĞRU | DDPG tabanlı DRL ile BS hüzmeleme matrisi ve RIS fazları birlikte tasarlanıyor (Özet, s. 1839); WMMSE ve FP tabanlarına karşı yalnızca toplam hız var, süre ölçümü yok; girişte DL'yi "computation time" ile gerekçelendiriyor (s. 1840), bu da Makale 2'nin savını destekliyor; künye uyuşuyor |
| Yu2019ICCC | Atıf DOĞRU; kapanış cümlesi DÜZELTİLMELİ | Sabit nokta yinelemesi (Alg. 1) ve manifold optimizasyonu (Alg. 2) gerçekten var (s. 735, 737–738); tek kullanıcılı MISO, f = MRT. Fig. 4 saniye cinsinden ölçülmüş çalışma süresi veriyor (s. 739–740); "run time ... is a complexity order" bu kaynak için yanlış. Künye uyuşuyor; DOI PDF'te basılı değil |
| Shi2011TSP | Atıf DOĞRU; kapanış cümlesi DÜZELTİLMELİ | WMMSE'nin özgün makalesi, ağırlıklı MSE ile toplam hız denkliği ve BCD (Özet, s. 4331; §III); Fig. 4 aynı sonlandırma ölçütüyle ortalama CPU süresi veriyor (s. 4337); künye uyuşuyor |
| Jiang2021JSAC | DOĞRU (netleştirme isteğe bağlı) | Alınan pilotlardan hüzmeleyici ve yansıma katsayılarına GNN ile doğrudan eşleme, açık kanal kestirimi atlanıyor (Özet, s. 1931); RL değil, "policy" gevşek bir kullanım; ölçülmüş süre yok, yalnızca "offline training ... does not affect the run-time complexity" (s. 1938); künye uyuşuyor |
| Monga2021SPM | DOĞRU | "each iteration of the algorithm step is represented as one layer of the network" (s. 20); Table 2'de derlenmiş süreler var (s. 34); künye uyuşuyor; cilt/sayı PDF'te basılı değil |

Künye uyuşmazlığı bulunmadı. Yu2019ICCC'nin DOI'si ve Monga2021SPM'nin cilt/sayısı PDF'ten doğrulanamadı. ÇIKARILMALI kararı yok.

Düzeltilmesi gereken tek cümle (`sections/section_02_related_work.tex`, "RIS phase optimization" paragrafının son cümlesi). Önerilen biçim: "These works report the objective value reached; run time, when discussed, is a complexity order or a CPU time on a fixed channel realization~\cite{Yu2019ICCC,Shi2011TSP}, never a latency measured against the coherence time."
