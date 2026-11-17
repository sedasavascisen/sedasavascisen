# Makale 2 — Kaynak kontrolü, Grup 6: [27]–[31] (Han, Truong, Chopra, Jindal, Zhao)

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`; dal `thesis/p4-deneyler`, commit `e974718`). Özette (abstract) ve tablolarda bu beş anahtarın hiçbiri geçmiyor. Atıflar iki yerde:

- `sections/section_02_related_work.tex`, satır 8 ("Mobility and outdated channels" paragrafı): beş anahtarın beşi.
- `sections/section_04_latency_analysis.tex`, satır 14: yalnızca `Zhao2021TWC`.

`Truong2013JCN` başka yerde geçmiyor. Gecikme bölümündeki J0 (Clarke) korelasyonu `Clarke1968BSTJ` ve `rappaport_wireless`'a atfedilmiş (section_04, satır 49); Truong orada kullanılmamış.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI: Yenilik cümlesiyle ilgili durum

İlgili cümle (section_02, satır 8): *"In these works the delay between channel acquisition and use, where modeled, is a fixed parameter; the optimizer's own run time is at most checked for feasibility, … and does not enter the aging."*

**Bu beş kaynağın hiçbiri optimizasyon algoritmasının ölçülmüş çalışma süresini eskime gecikmesine katmıyor.** Hiçbirinde saniye ya da milisaniye cinsinden süre ölçümü yok ("CPU", "running time", "run time", "seconds", "ms", "MATLAB" araması). Yenilik cümlesi bu grup için çürütülmüyor.

Ancak bir nüans var ve jüri sorabilir. **Truong ve Heath [28] hesaplama gecikmesini eskimenin nedenlerinden biri olarak açıkça adlandırıyor.**
- Basılı s. 338, PDF s. 1, §I: "Due to time variation of the propagation channel and delays in the computation, the channel varies between when it is learned at the base station and when it is used for beamforming or detection."
- Basılı s. 341, PDF s. 4, §III: "…mobility and processing delay affect the aging error e_bbu[n + 1]."

Truong bu gecikmeyi ölçmüyor. Gecikmeyi sabit bir parametre olarak alıyor: D = 1 çerçeve (s. 341) ve Table 1'de "CSI delay 1ms to 10 ms" (s. 348). Bu yüzden "does not enter the aging" ifadesi teknik olarak doğru kalıyor: kavram olarak hesaplama gecikmesi Truong'da var, ama ölçülmüş bir çalışma süresi olarak yok. Yine de cümle, "hesaplama gecikmesini eskimeye ilk kez biz bağlıyoruz" diye okunabilir. Bu okuma Truong karşısında savunulamaz. Önerilen düzeltme [28] başlığı altında.

---

## [27] Han vd., IEEE TWC 2025

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Han Han, Tao Jiang, Wei Yu. Başlık: "Active Sensing for Multiuser Beam Tracking With Reconfigurable Intelligent Surface". Dergi: IEEE Transactions on Wireless Communications, VOL. 24, NO. 1, JANUARY 2025. İlk sayfa 540; PDF 15 sayfa olduğu için son sayfa 554. DOI: 10.1109/TWC.2024.3496393. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 8: "…and active sensing tracks mobile users [Han2025TWC]." Aynı paragrafın son cümlesi (sabit gecikme, çalışma süresi eskimeye girmiyor) bu kaynağı da kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 540, PDF s. 1, Özet: "This paper studies a beam tracking problem in which an access point (AP), in collaboration with a reconfigurable intelligent surface (RIS), dynamically adjusts its downlink beamformers and the reflection pattern at the RIS in order to maintain reliable communications with multiple mobile user equipments (UEs)." Aynı özet: "we propose a deep learning framework utilizing a recurrent neural network (RNN) to automatically summarize the time-varying CSI obtained from the periodically received pilots into state vectors."
  - Gecikme modeli: Basılı s. 542, PDF s. 3, §II-A: "We model the time-varying channel in the discrete-time domain, where the continuous evolution of the channel is approximated by dividing time into a sequence of fixed-length blocks." Aynı yerde, çerçeve içindeki değişim ihmal ediliyor: "…assume that channel variation is not significant within the frame so a fixed beamforming strategy across all the blocks within the frame can be used without incurring substantial performance loss."
  - Benzetim değerleri: Basılı s. 547–548, PDF s. 8–9, §V-A: kullanıcı hızı 10 m/s, f_max = 33.3 Hz, blok süresi "Tb = 1/2fmax". Doğrudan bağlantı Gauss–Markov süreciyle güncelleniyor ve korelasyon sabit: "where the correlation coefficient ρ = 0.9995" (s. 548, denklem 20).
  - Çalışma süresi: Basılı s. 551, PDF s. 12, §V-E "Scalability and Complexity Analysis": "In terms of computational complexity, it is important to note that the proposed learning-based approach is trained offline, so the main concern is inference complexity." Yalnızca karmaşıklık mertebesi veriliyor, O(Kd² + Kdη + (K + N_r L)κ + (K + 2)²ςD). Süre için yalnızca nitel bir ifade var: "…the inference process is highly parallelizable using modern graphic process units (GPUs), so that in practice the proposed approach can be executed very efficiently." Ölçülmüş süre yok.
- **Değerlendirme:** Kaynak, RIS destekli çok kullanıcılı bir aşağı bağlantıda hüzme takibi yapıyor. Öğrenilen bir yöntem kullanıyor: RNN (LSTM) geçmiş pilotları bir durum vektörüne özetliyor. GNN bu vektörden hem algılama hem veri iletimi için RIS katsayılarını ve AP hüzmelerini üretiyor. Algılama aşamasındaki RIS deseni de önceki pilotlara göre uyarlanıyor; "active sensing" adı buradan geliyor. "Active sensing tracks mobile users" ifadesi kaynağı doğru özetliyor.
  - Gecikme sabit bir blok süresiyle (Tb = 1/2f_max) ve sabit bir korelasyonla (ρ = 0.9995) modelleniyor. Ağın çıkarım süresi ölçülmüyor ve eskimeye girmiyor. Paragrafın son cümlesi bu kaynak için doğru.
  - Bilgi notu: Kaynak öğrenilen bir yöntem. Makale 2'nin cümlesi bunu söylemiyor. Tezin yapay zekâ ekseniyle karşılaştırma yapılacaksa "learned active sensing" demek daha bilgilendirici olur. Zorunlu değil.
- **Karar:** **DOĞRU.** İsteğe bağlı biçim: "…and learned active sensing (RNN and GNN) tracks multiple mobile users [Han2025TWC]."

---

## [28] Truong ve Heath, JCN 2013

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Kien T. Truong, Robert W. Heath Jr. Başlık: "Effects of Channel Aging in Massive MIMO Systems". Dergi: Journal of Communications and Networks, VOL. 15, NO. 4, AUGUST 2013. İlk sayfa 338; PDF 14 sayfa olduğu için son sayfa 351. DOI: 10.1109/JCN.2013.000065. **UYUŞUYOR.** Bib'deki "R. W. Heath" PDF'te "Robert W. Heath Jr." olarak yazılmış. "Jr." eklenebilir; bu bir hata değil.
- **Makale 2'de nerede:** İlgili çalışmalar, satır 8: "Aging is classical in massive MIMO [Truong2013JCN, Chopra2018TWC]…" Paragrafın son cümlesi de kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 338, PDF s. 1, Özet: "This paper considers the impact of channel aging on the performance of massive MIMO systems."
  - J0 korelasyonu: Basılı s. 341, PDF s. 4, §III-A, denklem (14): r_h[k] = J0(2π f_D T_s |k|). Alıntı: "A commonly-used autocorrelation function is the Clarke-Gans model, which is often called the Jakes model…" Analiz için AR(1) kullanılıyor: "We denote α = J0(2πf_D T_s) as a temporal correlation parameter that corresponds to r_h[1] in (14)."
  - Sabit gecikme: Basılı s. 341, PDF s. 4: "For illustration, we assume that the CSI at the base stations is outdated by a channel sample duration, i.e., D = 1. We refer to this as a one frame delay; extensions to larger delays, i.e., D > 1, are straightforward." Basılı s. 348, PDF s. 11, Table 1 "Simulation parameters": "CSI delay 1ms to 10 ms", "UE speed 3 to 120 km/h".
  - Hesaplama gecikmesi bir neden olarak: Basılı s. 338, PDF s. 1, §I: "Due to time variation of the propagation channel and delays in the computation, the channel varies between when it is learned at the base station and when it is used for beamforming or detection." Basılı s. 341, PDF s. 4: "…mobility and processing delay affect the aging error e_bbu[n + 1]."
  - Çalışma süresi ölçümü yok ("CPU", "running time", "seconds", "MATLAB" araması sonuç vermedi).
- **Değerlendirme:** Kaynak, kanal eskimesini massive MIMO'da yukarı ve aşağı bağlantı için deterministik eşdeğerlerle inceleyen temel bir çalışma. Jakes/Clarke J0 korelasyonunu ve AR(1) (Gauss–Markov) yaklaşımını kullanıyor; kanal kestirimi (Wiener tahmincisi) öneriyor. "Aging is classical in massive MIMO" atfı doğru.
  - Gecikme sabit bir parametre (D = 1, benzetimde 1–10 ms). Paragrafın "where modeled, is a fixed parameter" kısmı doğru. Ancak kaynak hesaplama ve işleme gecikmesini eskimenin nedeni olarak açıkça sayıyor (yukarıdaki "ÖNCE OKUNMALI" bölümü). Makale 2'nin yeniliği "hesaplama gecikmesi eskimeye neden olur" fikri değil. Yenilik, optimizasyon algoritmasının **ölçülmüş** süresinin eskime gecikmesine yazılması ve bu yüzden yöntem sıralamasının değişmesi. Cümle bu ayrımı açıkça yapmalı; yoksa Truong'u okuyan bir hakem itiraz eder.
- **Karar:** Atıf **DOĞRU**. Paragrafın son cümlesi **DÜZELTİLMELİ** (Truong nedeniyle kesinleştirilmeli). Önerilen biçim: "In these works the delay between channel acquisition and use, where modeled, is a fixed parameter; even where computation is named as a cause of aging~\cite{Truong2013JCN}, it is folded into a fixed delay. The optimizer's own run time is at most checked for feasibility, …, and does not enter the aging."

---

## [29] Chopra vd., IEEE TWC 2018

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Ribhu Chopra, Chandra R. Murthy, Himal A. Suraweera, Erik G. Larsson. Başlık: "Performance Analysis of FDD Massive MIMO Systems Under Channel Aging". Dergi: IEEE Transactions on Wireless Communications, VOL. 17, NO. 2, FEBRUARY 2018. İlk sayfa 1094; PDF 15 sayfa olduğu için son sayfa 1108. DOI: 10.1109/TWC.2017.2775629. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 8: "Aging is classical in massive MIMO [Truong2013JCN, Chopra2018TWC]…" Paragrafın son cümlesi de kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 1094, PDF s. 1, Özet: "In this paper, we study the effect of channel aging on the uplink and downlink performance of an FDD massive MIMO system, as the system dimension increases. Since the training duration scales linearly with the number of transmit dimensions, channel estimates become increasingly outdated in the communication phase, leading to performance degradation."
  - J0 korelasyonu: Basılı s. 1096, PDF s. 3, §II: "If the channel is assumed to age according to the Jakes' model [27], ρ[n] = J0(2π f_d T_s n)…" Alternatif olarak AR(1) modeli de veriliyor.
  - Gecikme nereden geliyor: Basılı s. 1096, PDF s. 3: "The quality of the channel estimate will worsen with an increase in the delay between training and transmission, hence, we consider the channel estimates at n = K + 1…" Geri besleme gecikmesi yok sayılıyor: "We assume an ideal delay and error free feedback channel for ease of analysis and also to isolate the effect of channel aging and estimation error on the system performance."
  - Gecikme bir tasarım değişkeni olarak: Özet (s. 1094): "We show that the effect of channel aging can be mitigated by optimally choosing the frame duration." Sonuç (basılı s. 1105, PDF s. 12): "We also optimized the frame duration to maximize the per user achivable rate."
  - Çalışma süresi ölçümü yok ("CPU", "running time", "seconds", "MATLAB" araması sonuç vermedi).
- **Değerlendirme:** Kaynak, FDD massive MIMO'da eskimeyi inceliyor. Eğitim süresi anten sayısıyla doğrusal büyüdüğü için kestirimler iletim aşamasında eskiyor. Kanal Jakes (J0) ya da AR(1) ile evriliyor. "Aging is classical in massive MIMO" atfı doğru; ayrıca FDD tarafını temsil ettiği için Truong'u (TDD) iyi tamamlıyor.
  - Küçük bir nüans: Chopra'da gecikme tek bir sabit sayı değil. Eğitim süresinden ve sembolün çerçevedeki konumundan doğuyor; çerçeve süresi de en iyilenen bir değişken. "Fixed parameter" ifadesi tam olarak "sistem yapısından gelen, algoritmadan bağımsız gecikme" anlamında doğru. Hesaplama süresi hiç girmiyor. Cümleyi değiştirmek zorunlu değil. Kesinlik istenirse "fixed or set by the training and frame structure" yazılabilir.
- **Karar:** **DOĞRU.** İsteğe bağlı: "…where modeled, is a fixed parameter or set by the training and frame structure [Chopra2018TWC]…"

---

## [30] Jindal, IEEE TIT 2006

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazar: Nihar Jindal. Başlık: "MIMO Broadcast Channels With Finite-Rate Feedback". Dergi: IEEE Transactions on Information Theory, VOL. 52, NO. 11, NOVEMBER 2006, "Correspondence" bölümü. İlk sayfa 5045. DOI: 10.1109/TIT.2006.883550. PDF 16 sayfa (5045–5060); son sayfada sonraki makalenin (DOI 10.1109/TIT.2006.883613) başı da var. Bib'deki 5045–5060 bununla uyuşuyor. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, satır 8: "…as is limited channel feedback in broadcast channels [Jindal2006IT]."
- **Kaynakta karşılığı:**
  - Basılı s. 5045, PDF s. 1, Özet: "In this correspondence, a system where each receiver has perfect channel knowledge, but the transmitter only receives quantized information regarding the channel instantiation is analyzed." Aynı özet: "A key finding is that the feedback rate per mobile must be increased linearly with the signal-to-noise ratio (SNR) (in decibels) in order to achieve the full multiplexing gain."
  - Gecikme yok: Basılı s. 5046, PDF s. 2, §II: "…each receiver quantizes its channel to B bits and feeds back the bits perfectly and instantaneously to the AP…" Kanal i.i.d. Rayleigh blok sönümlemeli (s. 5045, §I).
  - Gecikme yalnızca gelecek çalışma olarak geçiyor: Basılı s. 5056, PDF s. 12, §VIII "Conclusion": "Of course, there will be some nonzero delay associated with transmitting feedback bits from the mobiles to the AP, and this delay can be quite significant in fast fading (large Doppler spread) channels."
- **Değerlendirme:** Kaynak, MIMO yayın (aşağı bağlantı) kanalında sonlu hızlı (B bit) geri beslemeyi ve RVQ ile sıfır-zorlamalı ön kodlamayı inceliyor. "Limited channel feedback in broadcast channels" ifadesi doğru; kaynağın anahtar kelimeleri de "Broadcast channel, finite rate feedback".
  - Nüans: Bu kaynakta CSI kusuru niceleme hatasından geliyor, eskimeden değil. Geri besleme anlık kabul ediliyor, kanal bloklar arasında bağımsız. Gecikme yalnızca sonuçta bir sınırlama olarak anılıyor. Cümle "Mobility and outdated channels" başlıklı paragrafta duruyor ve "as is" ile eskimeye bağlanıyor. Bu yüzden okuyucu Jindal'ın gecikmeyi de modellediğini sanabilir. Ardından gelen "where modeled" ifadesi bu kaynağı doğru biçimde dışarıda bırakıyor; yine de ayrımı açık yazmak daha güvenli.
- **Karar:** **DOĞRU.** İsteğe bağlı kesinleştirme: "…as is CSI quantization by finite-rate feedback in MIMO broadcast channels, there with instantaneous feedback [Jindal2006IT]."

---

## [31] Zhao vd., IEEE TWC 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Ming-Min Zhao, Qingqing Wu, Min-Jian Zhao, Rui Zhang. Başlık: "Intelligent Reflecting Surface Enhanced Wireless Networks: Two-Timescale Beamforming Optimization". Dergi: IEEE Transactions on Wireless Communications, VOL. 20, NO. 1, JANUARY 2021. İlk sayfa 2; PDF 16 sayfa olduğu için son sayfa 17. DOI: 10.1109/TWC.2020.3022297. **UYUŞUYOR.**
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) İlgili çalışmalar, satır 8: "Two-timescale designs update the phases from channel statistics and the precoder from instantaneous channels [Zhao2021TWC, Cao2022TWC]." Paragrafın son cümlesi de kapsıyor.
  - (b) Gecikme analizi, `section_04_latency_analysis.tex` satır 14: "Definition~1 therefore lets the phase age and keeps the beam fresh, a split similar to that of two-timescale designs [Zhao2021TWC]."
- **Kaynakta karşılığı:**
  - (a) Basılı s. 2, PDF s. 1, Özet: "Specifically, the passive IRS phase shifts are first optimized based on the statistical CSI (S-CSI) of all links, which varies much slowly as compared to their I-CSI; while the transmit beamforming/precoding vectors at the AP are then designed to cater to the I-CSI of the users' effective fading channels with the optimized IRS phase shifts…"
  - (b) Basılı s. 8, PDF s. 7, §IV-A: "At each time slot m ∈ [1, T_s], the AP first acquires the effective fading channel H(m) … with fixed phase shifts v. Then, the AP designs the short-term transmit precoding vectors {w_k}, by applying the WMMSE method…" Basılı s. 6, PDF s. 5, §II: "Besides, for fast-varying channels, using I-CSI may not be helpful as previously acquired I-CSI will become outdated quickly, which renders the proposed S-CSI-based protocol more suitable."
  - Çalışma süresi: Basılı s. 8, PDF s. 7, §III-B "Complexity Analysis": "Thus, the overall complexity of Algorithm 1 is O(I_o I_i N²)…" Süre yalnızca nitel olarak anılıyor (basılı s. 3, PDF s. 2): "…enables updating the optimization variables in parallel and thus can potentially reduce the computational time substantially as compared to the algorithms in [5], [6] if a multi-core processor with parallel computing capability is available." Ölçülmüş süre yok ("CPU", "running time", "seconds", "MATLAB" araması sonuç vermedi).
- **Değerlendirme:** (a) Kaynak, IRS fazlarını istatistiksel CSI'dan (uzun vadeli), AP ön kodlayıcısını anlık etkin kanaldan (her zaman diliminde) tasarlayan iki zaman ölçekli bir protokol öneriyor. Fazlar ayrık. Tek kullanıcıda PDD, çok kullanıcıda TTS-SSCA kullanılıyor. Cümle kaynağı doğru özetliyor. Kaynakta eskime gecikmesi modeli yok: S-CSI aralık boyunca sabit kabul ediliyor. Paragrafın son cümlesi ("where modeled") bununla çelişmiyor.
  - (b) Benzerlik yapısal olarak doğru: iki yapıda da ön kodlayıcı her yeni kanal ölçümünde güncelleniyor, faz daha seyrek güncelleniyor. İki fark var ama ikisi de "similar" kelimesiyle uyumlu. Birincisi, Zhao'da faz eskimiş bir anlık kanaldan değil, istatistikten hesaplanıyor; yani faz "eskimiyor", baştan ortalamaya göre seçiliyor. İkincisi, Zhao'nun çok kullanıcılı ön kodlayıcısı WMMSE ile yinelemeli; Makale 2'deki gibi kapalı biçimli değil (tek kullanıcıda MRT kapalı biçimli). Makale 2'nin cümlesi ön kodlayıcıyı kendi sistemi için kapalı biçimli diye niteliyor, Zhao için değil; hata yok.
- **Karar:** (a) **DOĞRU.** (b) **DOĞRU.** İsteğe bağlı kesinleştirme (b) için: "…a split similar to that of two-timescale designs, which however compute the phase from channel statistics rather than from an aged channel [Zhao2021TWC]."

---

## Çalışma süresi / gecikme modelleme özeti

Bu tablo, paragrafın son cümlesiyle ("delay … is a fixed parameter; … run time … does not enter the aging") ilgili.

| n | Eskime / gecikme modeli | Gecikmenin kaynağı | Ölçülmüş çalışma süresi | Süre eskimeye giriyor mu |
|---|---|---|---|---|
| [27] Han | Gauss–Markov, ρ = 0.9995; blok Tb = 1/2f_max (s. 542, 548) | Sabit blok süresi | Yok; yalnızca çıkarım karmaşıklığı (s. 551) | Hayır |
| [28] Truong | J0 (Jakes), AR(1); D = 1, 1–10 ms (s. 341, 348) | Sabit; hesaplama/işleme gecikmesi **neden olarak adlandırılıyor** (s. 338, 341) | Yok | Hayır (sabit D içinde) |
| [29] Chopra | J0 (Jakes) ya da AR(1) (s. 1096) | Eğitim süresi ve çerçeve yapısı; çerçeve süresi en iyileniyor | Yok | Hayır |
| [30] Jindal | Yok; i.i.d. blok sönümleme, anlık geri besleme (s. 5046) | Gecikme yok; yalnızca gelecek çalışma (s. 5056) | Yok | Hayır |
| [31] Zhao | Yok; S-CSI aralık boyunca sabit | — | Yok; O(I_o I_i N²) ve nitel "paralel daha hızlı" (s. 3, 8) | Hayır |

---

## Özet tablo

| n | Karar | Gerekçe |
|---|---|---|
| [27] Han2025TWC | DOĞRU | Özet (s. 540): RIS ile çok kullanıcılı hüzme takibi, RNN+GNN ile öğrenilen aktif algılama; gecikme sabit blok ve ρ = 0.9995 (s. 542, 548); süre ölçümü yok, yalnızca karmaşıklık (s. 551); künye uyuşuyor. İsteğe bağlı: "learned active sensing" |
| [28] Truong2013JCN | DOĞRU (atıf); paragrafın son cümlesi DÜZELTİLMELİ | Massive MIMO'da eskime, J0 (denklem 14) ve AR(1), sabit D = 1 ve 1–10 ms (s. 341, 348). Ancak kaynak "delays in the computation" ve "processing delay"i eskimenin nedeni olarak adlandırıyor (s. 338, 341). Yenilik cümlesi "ölçülmüş optimizasyon süresi" ile "sabit hesaplama gecikmesi" ayrımını açıkça yapmalı; künye uyuşuyor ("Jr." eklenebilir) |
| [29] Chopra2018TWC | DOĞRU | FDD massive MIMO'da eskime, Jakes J0 (s. 1094, 1096); gecikme eğitim süresinden ve çerçeve yapısından, çerçeve süresi en iyileniyor; geri besleme gecikmesiz; süre ölçümü yok; künye uyuşuyor |
| [30] Jindal2006IT | DOĞRU | MIMO yayın kanalında sonlu hızlı geri besleme (s. 5045); geri besleme anlık, gecikme modellenmiyor (s. 5046, 5056). İsteğe bağlı: gecikmesiz olduğunu belirtmek; künye uyuşuyor |
| [31] Zhao2021TWC | (a) DOĞRU, (b) DOĞRU | Özet (s. 2): fazlar S-CSI'dan, ön kodlayıcı I-CSI'dan; her dilimde WMMSE ön kodlayıcı (s. 8); eskime modeli yok; süre ölçümü yok, karmaşıklık O(I_o I_i N²) (s. 8); künye uyuşuyor |

Künye uyuşmazlığı bulunmadı. ÇIKARILMALI kararı yok. Ölçülmüş optimizasyon süresini eskime gecikmesine katan kaynak yok. Tek gerekli düzeltme, paragrafın son cümlesinin Truong'a göre kesinleştirilmesi.
