# Makale 2 — Kaynak kontrolü, Grup 4: Liu2022TWC, Samuel2019TSP, Hu2021TWC, Sun2018TSP, Pellaco2022OJCOMS

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst ya da alt bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Metin olarak çıkmayan dört tablo (Liu Table V, Samuel Table I–II, Hu Table VIII, Sun Table I–II) sayfa görüntüsünden okundu. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep -rn <anahtar> --include=*.tex` ile tarandı (dal `thesis/p4-deneyler`, commit `08c0ee3`; özet `mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`). Beş anahtar yalnızca bir yerde geçiyor: `sections/section_02_related_work.tex`, satır 6, "Learning" paragrafı. Özette ve tablolarda bu anahtarlara atıf yok.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

Atıf cümleleri (satır 6):

> "Algorithm unrolling turns an optimizer's iterations into network layers~\cite{Monga2021SPM}; it has been applied to RIS beamforming~\cite{Liu2022TWC}, MIMO detection~\cite{Samuel2019TSP} and WMMSE precoding~\cite{Hu2021TWC,Pellaco2022OJCOMS}, and trained networks can approximate WMMSE at a fraction of its run time~\cite{Sun2018TSP}. […] Learned methods are usually motivated by speed, but that speed is rarely related to how fast the channel changes, and classical baselines are rarely tuned or timed under the same conditions."

Son cümle atıf taşımıyor, ama aynı paragrafta atıf yapılan beş kaynak bu genellemenin doğal sınama kümesi. Aşağıda her kaynak için ayrıca kontrol edildi.

---

## ÖNCE OKUNMALI: Makale 2'deki bir iddiayla çelişen bulgu

Paragrafın son cümlesindeki **"classical baselines are rarely … timed under the same conditions"** kısmı, bu paragrafta atıf yapılan kaynakların çoğu için **yanlış**. Beş kaynaktan dördü, öğrenilen yöntemi ve klasik taban çizgisini aynı makinede ölçüp saniye cinsinden tabloluyor:

- **Samuel2019TSP** (basılı s. 2560, PDF s. 7, §IV-E-1): "To ensure fairness, all the algorithms were tested on the same machine via python 2.7 environment using the Numpy package." Süreler Table I–II–III'te (s. 2561).
- **Sun2018TSP** (basılı s. 5444, PDF s. 7, §V-A): "The Python implementation is used to compare the computational performance under the same platform while the C implementation is used to achieve the best computational efficiency of WMMSE." Yani WMMSE'yi en hızlı haliyle (C) ölçmek için ayrıca çaba gösteriliyor. Süreler Table I–II'de (s. 5446).
- **Hu2021TWC** (basılı s. 1402, PDF s. 9): tüm sonuçlar "a desktop Intel (i5-8400) CPU running at 2.8 GHz with 8 GB RAM" üzerinde; WMMSE ve IAIDNN tahmin süresi Table VIII'de (s. 1406).
- **Liu2022TWC** (basılı s. 4792, PDF s. 9): "All the experiments are conducted on a desktop Intel CPU (i5-8400 with 6 cores) with 8GB RAM." SSCA ve öğrenilen ağların test süresi Table V'te (s. 4795).

Yalnızca **Pellaco2022OJCOMS** duvar saati süresi vermiyor (yalnızca karmaşıklık analizi, §VII).

Cümlenin diğer iki parçası **ayakta kalıyor**:

- **"rarely tuned":** Hiçbir kaynak klasik yöntemi aynı süre bütçesine göre ayarlamıyor. Klasik kol ya yakınsamaya kadar (Sun: "objnew − objold < 10⁻⁵ or number of iterations >500"; Liu: Imax = 100) ya da sabit bir ayarda koşuyor. En yakın iki örnek bile **eşit yineleme**, eşit süre değil: Pellaco, "WMMSE algorithm truncated to the same number of iterations" ile karşılaştırıyor; Hu Table X'te "WMMSE in 7 iterations" satırı var. Bu iki karşılaştırmada da kesilmiş WMMSE'nin süresi ölçülmüyor.
- **"rarely related to how fast the channel changes":** Hiçbir kaynak ölçülen süreyi eşevreli kalma süresiyle (coherence time) sayısal olarak karşılaştırmıyor. Ancak üç kaynak bağlantıyı **nitel olarak** kuruyor: Sun ("algorithms are typically executed in a time frame of milliseconds (due to the fast changing system parameters such as channel conditions …)", s. 5438), Pellaco ("Base stations must … respond to fast changing channel conditions", s. 66), Liu ("In each time slot (channel coherence time) i …", s. 4787). "Rarely related" bu nedenle savunulabilir ama "never" denmemeli.

Bu bulgu tezin ana iddiasını zayıflatmıyor, tersine destekliyor: ölçülen süreler çoğunlukla eşevreli kalma süresinden kat kat uzun (örneğin Liu'da SSCA 2.82–21.45 s, öğrenilen ağ 0.016–0.15 s; aynı makale 0.6 ms CSI gecikmesinin sonucu değiştirdiğini gösteriyor, Fig. 10). Ama "aynı koşullarda zamanlanmıyor" genellemesi bu haliyle savunulamaz. Önerilen düzeltme en altta, "Önerilen yeniden yazım" başlığında.

---

## [Liu2022TWC] Liu vd., IEEE TWC 2022

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Yanzhen Liu, Qiyu Hu, Yunlong Cai, Guanding Yu, Geoffrey Ye Li. Başlık: "Deep-Unfolding Beamforming for Intelligent Reflecting Surface Assisted Full-Duplex Systems". Dergi: IEEE Transactions on Wireless Communications, VOL. 21, NO. 7, JULY 2022. İlk sayfa 4784; PDF 17 sayfa olduğu için son sayfa 4800. DOI: 10.1109/TWC.2021.3133296. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 6: "it has been applied to RIS beamforming [Liu2022TWC]".
- **Kaynakta karşılığı:**
  - Basılı s. 4784, PDF s. 1, Özet: "Moreover, due to the high computational complexity caused by the matrix inversion computation in the SSCA-based optimization algorithm, we further develop a deep-unfolding neural network (NN) to address this issue. The proposed deep-unfolding NN maintains the structure of the SSCA-based algorithm but introduces a novel non-linear activation function and some learnable parameters induced by the first-order Taylor expansion to approximate the matrix inversion."
  - Aynı özet, problem: "We jointly optimize the active beamforming matrices at the access point (AP) and uplink users, and the passive beamforming matrix at the IRS to maximize the weighted sum-rate of the system."
  - Zaman ölçeği, basılı s. 4787, PDF s. 4, §II-B: "In each time slot (channel coherence time) i, the AP obtains the low-dimensional effective channels Hef (i) via conventional MIMO channel estimation methods and designs the active short-term beamforming matrices Pk and Fl accordingly." IRS faz matrisi ise uzun vadeli, kanal istatistiklerinden güncelleniyor.
  - Donanım, basılı s. 4792, PDF s. 9, §V: "All the experiments are conducted on a desktop Intel CPU (i5-8400 with 6 cores) with 8GB RAM." Aynı yerde SSCA için "Imax = 100, δ = 10⁻⁴" ve SSCA, deep-unfolding NN ve black-box NN için ortak "batch size … 5".
  - Süre, basılı s. 4795, PDF s. 12, Table V "The CPU Running Time of the Analyzed Schemes" (sayfa görüntüsünden okundu): (N, T) = (8,100)…(256,400) için CPU test süresi (s) SSCA 2.82–21.45, deep-unfolding 0.052–0.15, black-box 0.016–0.071, full CSI 18.62–1085.18. Eğitim süresi deep-unfolding 10.80–159.23 dk, black-box 35.77–343.77 dk. Sürenin kaç örnek üzerinden ölçüldüğü belirtilmemiş.
  - Basılı s. 4794, PDF s. 11, §V: "When the CSI delay is greater than 0.6 ms, the proposed SSCA-based mixed-timescale beamforming algorithm and deep-unfolding NN outperform the single-timescale algorithm."
- **Değerlendirme:** Kaynak, IRS destekli çok kullanıcılı MIMO tam çift yönlü (full-duplex) bir sistemde AP ve yukarı bağlantı kullanıcılarının aktif hüzmelemesi ile IRS'in pasif hüzmelemesini ortak tasarlıyor. Önerdiği SSCA tabanlı karma zaman ölçekli algoritmayı katmanlara açıyor (deep unfolding) ve matris tersini birinci dereceden Taylor açılımıyla yaklaştırıyor. "Algorithm unrolling … applied to RIS beamforming" ifadesi doğru. İsteğe bağlı bir kesinlik: kaynak full-duplex ve karma zaman ölçekli; "RIS-assisted full-duplex beamforming" demek daha kesin olur.
  - Zamanlama: Duvar saati süresi var (Table V), donanım belirtilmiş, klasik kol (SSCA) aynı makinede ölçülmüş. SSCA ayarlanmamış: varsayılan Imax = 100 ile zamanlanıyor, oysa Table III'e göre Imax = 10 zaten "90.21% performance" veriyor (basılı s. 4794, PDF s. 11). Kesilmiş SSCA'nın süresi verilmiyor. Süre eşevreli kalma süresiyle karşılaştırılmıyor; ilginç olarak makale 0–1.2 ms CSI gecikmesinin etkisini inceliyor (Fig. 10) ama 0.016–21.45 s'lik hesaplama süresini bu ölçekle ilişkilendirmiyor.
  - Bilgi notu: Liu, IRS fazını yalnızca kanal istatistiklerinden uzun vadeli güncelleyerek her yuvada faz hesaplamaktan kaçınıyor. Bu, Makale 2'nin "gecikme birinci sınıf kısıt" çerçevesine yakın bir tasarım kararı; ilgili çalışmalarda istenirse bir yarım cümleyle anılabilir. Zorunlu değil.
- **Karar:** Atıf **DOĞRU.** İsteğe bağlı: "…RIS-assisted full-duplex beamforming [Liu2022TWC]".

---

## [Samuel2019TSP] Samuel vd., IEEE TSP 2019

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Neev Samuel, Tzvi Diskin, Ami Wiesel. Başlık: "Learning to Detect". Dergi: IEEE Transactions on Signal Processing, VOL. 67, NO. 10, MAY 15, 2019. İlk sayfa 2554; PDF 11 sayfa olduğu için son sayfa 2564. DOI: 10.1109/TSP.2019.2899805. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 6: "…MIMO detection [Samuel2019TSP]".
- **Kaynakta karşılığı:**
  - Basılı s. 2554, PDF s. 1, Özet: "We introduce two different deep architectures: a standard fully connected multi-layer network, and a detection network (DetNet), which is specifically designed for the task. The structure of DetNet is obtained by unfolding the iterations of a projected gradient descent algorithm into a network."
  - Basılı s. 2557, PDF s. 4, §III-B: "Second, our construction is based on mimicking a projected gradient descent like solution for the maximum likelihood optimization." Aynı sayfa: "When computing qk at each layer, an explicit gradient descent is computed, with learnable step sizes."
  - Zamanlama, basılı s. 2560, PDF s. 7, §IV-E-1: "Comparing complexity is non-trivial due to many complicating factors as implementation details and platforms. To ensure fairness, all the algorithms were tested on the same machine via python 2.7 environment using the Numpy package."
  - Basılı s. 2561, PDF s. 8, Table I–III (sayfa görüntüsünden okundu; birim tabloda yazılmamış). Table I (0.55-Toeplitz 60×30, sabit kanal): batch 1'de FullyCon 4E-4, DetNet 5E-3, SDR 9E-3, AMP 5E-3, SD 0.001–0.01; batch 1000'de DetNet 1.1E-4. Table II (değişken kanal): BPSK 60×30, batch 1'de DetNet 0.0066, SDR 0.024, AMP 0.0093, SD 0.008–0.1.
  - Donanım: yalnızca eğitim için belirtilmiş, basılı s. 2558, PDF s. 5: "…took around 3 days on a standard Intel i7-6700 processor." Çalışma süresi ölçümünün makinesi adlandırılmamış ("the same machine").
- **Değerlendirme:** DetNet, ML tespitinin izdüşümlü gradyan iniş yinelemelerini öğrenilebilir adım boylu katmanlara açıyor. "Algorithm unrolling … applied to MIMO detection" ifadesi kaynağın kendi tanımıyla birebir örtüşüyor. Kaynakta ayrıca bir açma içermeyen tam bağlı ağ (FullyCon) var; cümle DetNet'i kastettiği için sorun yok.
  - Zamanlama: Duvar saati süresi var, tüm yöntemler bilinçli olarak aynı makine ve ortamda ölçülmüş, toplu işlem (batch) boyutunun etkisi ayrıca raporlanmış; Flops sayımı da var (Table IV). Klasik kollar (AMP, SDR, SD) sabit ayarlarla koşuyor, süre bütçesine göre ayarlanmıyor. Süre eşevreli kalma süresiyle ilişkilendirilmiyor. Bu kaynak, "rarely timed under the same conditions" ifadesine **açık bir karşı örnek**.
- **Karar:** Atıf **DOĞRU.** (Paragrafın son cümlesi için bkz. "ÖNCE OKUNMALI".)

---

## [Hu2021TWC] Hu vd., IEEE TWC 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qiyu Hu, Yunlong Cai, Qingjiang Shi, Kaidi Xu, Guanding Yu, Zhi Ding. Başlık: "Iterative Algorithm Induced Deep-Unfolding Neural Networks: Precoding Design for Multiuser MIMO Systems". Dergi: IEEE Transactions on Wireless Communications, VOL. 20, NO. 2, FEBRUARY 2021. İlk sayfa 1394; PDF 17 sayfa olduğu için son sayfa 1410. DOI: 10.1109/TWC.2020.3033334. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 6: "…and WMMSE precoding [Hu2021TWC, Pellaco2022OJCOMS]".
- **Kaynakta karşılığı:**
  - Basılı s. 1394, PDF s. 1, Özet: "An efficient IAIDNN based on the structure of the classic weighted minimum mean-square error (WMMSE) iterative algorithm is developed. Specifically, the iterative WMMSE algorithm is unfolded into a layer-wise structure, where a number of trainable parameters are introduced to replace the high-complexity operations in the forward propagation."
  - Motivasyon, aynı özet: "…they generally require considerable computational complexity, which gets in the way of their practical application in real-time systems."
  - Donanım ve klasik kol, basılı s. 1402, PDF s. 9, §VI-A: "We run the iterative WMMSE algorithm 20 times with different random initial values and then retain the best result as its performance, which is an approximation of the global optimal solution. […] The numerical results are simulated on a desktop Intel (i5-8400) CPU running at 2.8 GHz with 8 GB RAM."
  - Süre, basılı s. 1406, PDF s. 13, Table VIII "The CPU Running Time of the Analyzed Schemes" (sayfa görüntüsünden okundu): (Nt, K) = (8,4)…(256,120) için tahmin aşaması CPU süresi (s) IAIDNN 0.01–2.94, black-box 0.01–3.36, WMMSE 0.08–291.01. Eğitim süresi IAIDNN 8.71–9806.85 dk. Kaç kanal örneği üzerinden ölçüldüğü ve WMMSE süresine 20 rastgele başlatmanın dahil olup olmadığı belirtilmemiş.
  - Basılı s. 1405, PDF s. 12, §VI-C: "In the prediction stage, we can see that the IAIDNN requires shorter CPU time than that of the iterative WMMSE algorithm, where the superiority of our proposed IAIDNN lies in."
  - Eşit yinelemeli taban çizgisi, aynı sayfa 1406, Table X: "WMMSE in 7 iterations" 79.19–83.52%, IAIDNN 91.35–92.95% (WMMSE yakınsama değerine göre; yalnızca başarım, süre yok).
- **Değerlendirme:** Kaynak, MU-MIMO toplam hız ön kodlamasında WMMSE algoritmasını katmanlara açıyor ve matris terslerini öğrenilebilir parametrelerle değiştiriyor. "Unrolling … applied to WMMSE precoding" ifadesi doğru.
  - Zamanlama: Duvar saati süresi var, donanım belirtilmiş, WMMSE aynı makinede ölçülmüş (Table VIII). WMMSE yakınsamaya kadar koşuyor; süre bütçesine göre ayarlanmıyor. Table X'te eşit yineleme (7) karşılaştırması var ama süre ölçülmüyor. Eşevreli kalma süresiyle ilişki yok; "real-time systems" yalnızca genel motivasyon.
- **Karar:** Atıf **DOĞRU.**

---

## [Sun2018TSP] Sun vd., IEEE TSP 2018

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Haoran Sun, Xiangyi Chen, Qingjiang Shi, Mingyi Hong, Xiao Fu, Nicholas D. Sidiropoulos. Başlık: "Learning to Optimize: Training Deep Neural Networks for Interference Management". Dergi: IEEE Transactions on Signal Processing, VOL. 66, NO. 20, OCTOBER 15, 2018. İlk sayfa 5438; PDF 16 sayfa olduğu için son sayfa 5453. DOI: 10.1109/TSP.2018.2866382. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 6: "…and trained networks can approximate WMMSE at a fraction of its run time [Sun2018TSP]".
- **Kaynakta karşılığı:**
  - Basılı s. 5438, PDF s. 1, Özet: "…we apply it to approximate a popular interference management algorithm, namely, the WMMSE algorithm. […] It is shown that, in practice, only a small network is sufficient to obtain high approximation accuracy, and DNNs can achieve orders of magnitude speedup in computational time compared to the state-of-the-art interference management algorithm."
  - Kanal hızıyla nitel bağ, aynı sayfa, §I: "…for applications such as wireless transceiver design, algorithms are typically executed in a time frame of milliseconds (due to the fast changing system parameters such as channel conditions, number of users, etc.)."
  - Klasik kolun ayarı, basılı s. 5444, PDF s. 7, §IV: WMMSE "with vk0 = Pmax, ∀ k as initialization, and with objnew − objold < 10⁻⁵ or number of iterations >500 as termination criteria."
  - Donanım ve koşullar, aynı sayfa, §V-A: "The proposed DNN approach is implemented in Python 3.6.0 with TensorFlow 1.0.0 on one computer node with two 8-core Intel Haswell processors, two Nvidia K20 Graphical Processing Units (GPUs), and 128 GB of memory. The GPUs are used in the training stage to reduce the training time, but are not used in the testing stage." Devamı: "The Python implementation is used to compare the computational performance under the same platform while the C implementation is used to achieve the best computational efficiency of WMMSE."
  - Süre, basılı s. 5446, PDF s. 9, Table I–II (sayfa görüntüsünden okundu), başlık "total CPU time (sec.)":
    - Table I (Gaussian IC, K = 10/20/30): DNN 0.047 / 0.093 / 0.149; WMMSE (Python) 17.98 / 59.41 / 122.91; WMMSE (C) 0.355 / 1.937 / 5.103; DNN/WMMSE(C) %13.24 / %4.80 / %2.92. Toplam hız oranı DNN/WMMSE %98.33 / %92.04 / %84.29.
    - Table II (IMAC, (N, K) = (3,12)…(20,80)): DNN 0.021–0.141; WMMSE (MATLAB) 22.33–890.19; WMMSE (C) 0.27–23.0; DNN/WMMSE(C) %7.78–%0.61. Toplam hız oranı %98.30–%90.36.
  - Aynı sayfa, metin: "…compared with the IMAC WMMSE (which is implemented in C) with N = 20 and K = 80, the DNN obtains 90.36% sum-rate while achieving more than one hundred times (two orders of magnitude) speed up." Ortalamalar "10,000 test samples" üzerinden; tablodaki süre "total" olarak etiketli.
- **Değerlendirme:** Kaynak, WMMSE'nin girdi-çıktı eşlemesini tam bağlı bir DNN ile öğreniyor ve test aşamasında aynı CPU üzerinde, C ile yazılmış WMMSE'nin %0.61–%13.24'ü kadar sürede, WMMSE toplam hızının %84–%98'ine ulaşıyor. "Approximate WMMSE at a fraction of its run time" ifadesi doğru. Kaynaktaki DNN bir algoritma açma değil, kara kutu bir yaklaşım; Makale 2 cümleyi "and trained networks can…" diye ayırdığı için bu doğru yansıtılmış.
  - Zamanlama: Duvar saati süresi var; donanım belirtilmiş; GPU testte kapalı; WMMSE hem aynı platformda (Python) hem en verimli haliyle (C) ölçülmüş. Bu, "timed under the same conditions" için **güçlü bir karşı örnek**. Ancak WMMSE yakınsama ölçütüne (10⁻⁵ ya da 500 yineleme) kadar koşuyor; DNN ile aynı süre ya da aynı başarımda kesilmiş bir WMMSE yok. Yani "tuned" kısmı bu kaynak için de doğru. Kaynak, milisaniye ölçeğini kanalın hızlı değişmesine nitel olarak bağlıyor ama ölçülen süreyi bir eşevreli kalma süresiyle karşılaştırmıyor.
  - Kaynakta küçük bir iç tutarsızlık: metin "we have implemented the WMMSE in both Python and C" diyor, Table II başlığı ise "WMMSE (MATLAB)". Makale 2 bu sayıları kullanmadığı için etkisiz; sayı alıntılanacaksa C sütunu kullanılmalı.
- **Karar:** Atıf **DOĞRU.** Sayı eklenecekse önerilen biçim: "…approximate WMMSE at 0.6–13% of the CPU time of a C implementation of WMMSE, while reaching 84–98% of its sum rate [Sun2018TSP]."

---

## [Pellaco2022OJCOMS] Pellaco vd., IEEE OJ-COMS 2022

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Lissy Pellaco, Mats Bengtsson, Joakim Jaldén. Başlık: "Matrix-Inverse-Free Deep Unfolding of the Weighted MMSE Beamforming Algorithm". Dergi: IEEE Open Journal of the Communications Society, VOLUME 3, 2022. İlk sayfa 65 (PDF s. 1 alt bilgisi); PDF 17 sayfa olduğu için son sayfa 81. DOI: 10.1109/OJCOMS.2021.3139858. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 6: "…and WMMSE precoding [Hu2021TWC, Pellaco2022OJCOMS]".
- **Kaynakta karşılığı:**
  - Basılı s. 65, PDF s. 1, Özet: "In order to address this trade-off between complexity and performance, we propose to apply deep unfolding to the WMMSE algorithm for a MU-MISO downlink channel. The main idea consists of mapping a fixed number of iterations of the WMMSE into trainable neural network layers." Aynı özet: "…we present a variant of the WMMSE algorithm i) that circumvents these operations by applying a projected gradient descent…"
  - Kanal hızıyla nitel bağ, basılı s. 66, PDF s. 2, §I: "Base stations must comply with stringent cost and power specifications, respond to fast changing channel conditions, and accommodate latency requirements of newly 5G-supported real-time applications…"
  - Karmaşıklık, basılı s. 71, PDF s. 7, §VII: "However, this comparison is not entirely fair because it hides the fact that all the computations involved in the unfoldable WMMSE algorithm are highly parallelizable and thus suitable for implementation on standardized hardware optimized for deep learning."
  - Uygulama, aynı sayfa, §VIII-A: "The (accelerated) deep unfolded WMMSE algorithm was implemented in Python 3.6.8 with Tensorflow 1.13.1 and the original WMMSE algorithm was implemented in Python 3.6.8." Donanım ve süre ölçümü verilmiyor.
  - Karşılaştırma tabanı, basılı s. 65, PDF s. 1, Özet: "…the proposed network architecture i) performs on par with the WMMSE algorithm truncated to the same number of iterations, yet at a lower complexity…"
  - Süre araması: "seconds", "ms", "milliseconds", "runtime", "run time", "running time", "wall", "CPU", "GPU" (tam kelime) araması süre ölçümü bulmadı. "CPU/GPU" geçmiyor; "hardware" yalnızca paralellik bağlamında geçiyor.
- **Değerlendirme:** Kaynak, MU-MISO aşağı bağlantıda WSR'yi en büyükleyen WMMSE'yi, matris tersi, özayrışım ve ikiye bölme aramasını izdüşümlü gradyan inişiyle değiştirerek açıyor ve adım boylarını öğreniyor. "Beamforming" ile "precoding" burada aynı işlem; "WMMSE precoding" etiketi doğru. Hu2021TWC ile birlikte anılması da yerinde: Pellaco, IAIDNN'i doğrudan karşılaştırma tabanı olarak kullanıyor (basılı s. 74, PDF s. 10).
  - Zamanlama: Duvar saati süresi yok; yalnızca yineleme başına karmaşıklık analizi (§VII). Klasik taban çizgisi "WMMSE truncated to the same number of iterations": eşit yineleme, eşit süre değil. Yazarlar karmaşıklık karşılaştırmasının "not entirely fair" olduğunu kendileri belirtiyor. Eşevreli kalma süresiyle sayısal ilişki yok; bağ yalnızca girişte nitel. Bu kaynak Makale 2'nin genellemesiyle uyumlu.
- **Karar:** Atıf **DOĞRU.**

---

## Çalışma süresi / karmaşıklık raporlama özeti

Bu tablo, paragrafın son cümlesiyle ilgili: "that speed is rarely related to how fast the channel changes, and classical baselines are rarely tuned or timed under the same conditions."

| Kaynak | Duvar saati süresi | Donanım | Klasik kol aynı koşulda zamanlanmış mı | Klasik kol süre bütçesine göre ayarlanmış mı | Eşevreli kalma süresiyle ilişki |
|---|---|---|---|---|---|
| Liu2022TWC | **Var:** Table V, SSCA 2.82–21.45 s, ağ 0.016–0.15 s (s. 4795) | i5-8400, 8 GB (s. 4792) | **Evet** | Hayır (Imax = 100 sabit) | Yok; yuva = eşevreli kalma süresi tanımı var, 0–1.2 ms CSI gecikmesi inceleniyor, hesaplama süresiyle bağlanmıyor |
| Samuel2019TSP | **Var:** Table I–III, birim yazılmamış (s. 2561) | Adlandırılmamış ("the same machine", Python 2.7/Numpy) | **Evet, açıkça "to ensure fairness"** (s. 2560) | Hayır | Yok |
| Hu2021TWC | **Var:** Table VIII, WMMSE 0.08–291.01 s, IAIDNN 0.01–2.94 s (s. 1406) | i5-8400, 8 GB (s. 1402) | **Evet** | Hayır (yakınsamaya kadar; Table X'te 7 yinelemeli WMMSE yalnızca başarım) | Yok |
| Sun2018TSP | **Var:** Table I–II, DNN WMMSE(C)'nin %0.61–13.24'ü (s. 5446) | 2× 8 çekirdek Haswell, test GPU'suz (s. 5444) | **Evet** (Python aynı platform + en hızlı C) | Hayır (10⁻⁵ ya da 500 yineleme) | Nitel: "time frame of milliseconds" (s. 5438) |
| Pellaco2022OJCOMS | Yok (karmaşıklık, §VII) | Belirtilmemiş | Zamanlama yok | Eşit yineleme, eşit süre değil | Nitel: "fast changing channel conditions" (s. 66) |

---

## Önerilen yeniden yazım (paragrafın son cümlesi)

Mevcut: "Learned methods are usually motivated by speed, but that speed is rarely related to how fast the channel changes, and classical baselines are rarely tuned or timed under the same conditions."

Öneri: "Learned methods are usually motivated by speed, but that speed is rarely related to how fast the channel changes; even when learned and classical methods are timed on the same machine [Samuel2019TSP, Sun2018TSP, Hu2021TWC, Liu2022TWC], the classical baseline is run to convergence or for a fixed iteration count rather than tuned to the same latency budget."

Bu biçim kaynaklardaki her şeyle uyumlu: aynı makinede ölçüm var (4 kaynak), klasik kol hiçbirinde süre bütçesine göre ayarlanmıyor (5 kaynak), hiçbiri ölçülen süreyi eşevreli kalma süresiyle karşılaştırmıyor (5 kaynak).

---

## Özet tablo

| Kaynak | Karar | Gerekçe |
|---|---|---|
| Liu2022TWC | DOĞRU (isteğe bağlı: "full-duplex" eklenebilir) | Özet (s. 4784): IRS destekli full-duplex sistemde SSCA algoritmasının deep unfolding'i; Table V'te aynı i5-8400 üzerinde ölçülmüş süre (s. 4795); künye uyuşuyor |
| Samuel2019TSP | DOĞRU | Özet ve §III-B (s. 2554, 2557): DetNet, izdüşümlü gradyan inişinin açılmış hali; tüm dedektörler "to ensure fairness" aynı makinede zamanlanmış (s. 2560–2561); künye uyuşuyor |
| Hu2021TWC | DOĞRU | Özet (s. 1394): WMMSE ön kodlamasının katmanlara açılması (IAIDNN); Table VIII'de WMMSE ile aynı i5-8400 üzerinde CPU süresi (s. 1406); künye uyuşuyor |
| Sun2018TSP | DOĞRU | Özet ve Table I–II (s. 5438, 5446): DNN, WMMSE toplam hızının %84–98'ine, C ile yazılmış WMMSE'nin %0.61–13.24'ü kadar CPU süresinde ulaşıyor; aynı platform, test GPU'suz; künye uyuşuyor |
| Pellaco2022OJCOMS | DOĞRU | Özet (s. 65): matris tersi gerektirmeyen WMMSE deep unfolding'i, MU-MISO; süre ölçümü yok, eşit yinelemeli kesilmiş WMMSE ile karşılaştırma; künye uyuşuyor |
| Paragrafın son cümlesi ("…rarely tuned or timed under the same conditions") | **DÜZELTİLMELİ** | "Timed under the same conditions" kısmı Samuel, Sun, Hu ve Liu için yanlış: dördü de klasik kolu aynı makinede zamanlıyor. "Rarely tuned" ve "rarely related to how fast the channel changes" kısımları beş kaynakta da geçerli. Öneri yukarıda |

Künye uyuşmazlığı bulunmadı. ÇIKARILMALI kararı yok. Tek düzeltme, paragrafın son cümlesindeki "timed under the same conditions" genellemesi.
