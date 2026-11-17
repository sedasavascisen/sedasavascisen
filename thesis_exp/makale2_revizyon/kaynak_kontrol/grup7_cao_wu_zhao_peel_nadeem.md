# Makale 2 — Kaynak kontrolü, Grup 7: Cao, Wu, Zhao, Peel, Nadeem

Tarih: 2026-11-17. Yöntem: metin `pdftotext -layout` ile çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Peel vd.'nin denklemleri metin olarak çıkmadığı için PDF s. 2 ve s. 5 sayfa görüntüsünden okundu. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`; dal `thesis/p4-deneyler`, commit `8eeb789`). Beş anahtarın her biri yalnızca bir cümlede geçiyor: Cao, Wu ve Zhao ilgili çalışmalarda (`section_02_related_work.tex`, satır 8), Peel ve Nadeem sistem modelinde (`section_03_system_model.tex`, satır 10). Özette ve tablolarda bu anahtarların hiçbiri geçmiyor.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI: Cao vd. ile yenilik cümlesi arasında çelişki var mı?

**Çelişki yok.** Ancak Cao vd. gecikmeyi ve eskimeyi açıkça modelliyor, bu yüzden ayrıntı önemli.

İlgili cümle (`section_02_related_work.tex`, satır 8): *"In these works the delay between channel acquisition and use, where modeled, is fixed, even where computation is named as a cause [Truong2013JCN]; the optimizer's own run time is at most checked for feasibility, as an operation count [Ryu2026arXiv] or a measured 2 ms against a 20 ms slot [Liu2021WCL], and does not enter the aging."*

Cao vd.'de bulunanlar şunlar:

1. **Eskime modelleniyor.** Kanal birinci dereceden AR süreci (denklem 6). Korelasyon katsayısı Jakes modelinden geliyor: ρ = J₀(2π f_d τ). Burada τ, CSI'ın ölçüldüğü an ile BS'nin ön kodlayıcıyı ürettiği an arasındaki gecikme (basılı s. 10426, PDF s. 3, §II-A).
2. **Gecikme sabit.** τ en fazla bir zaman dilimi (TDD) ya da en az bir zaman dilimi (FDD) olarak tanımlanıyor. Benzetimde ρ dışarıdan verilen bir parametre olarak taranıyor (Fig. 11, basılı s. 10435, PDF s. 12). τ'nun içinde hesaplama süresine ayrı bir terim yok.
3. **Çalışma süresi ölçülüyor ama eskimeye girmiyor.** Fig. 7 "Running time per iteration vs. the number of IRS elements" (basılı s. 10434, PDF s. 11). Ölçüm ortamı MATLAB R2018b, Intel Core i7-8700 (basılı s. 10433, PDF s. 10). Metin, LBO-PSO'nun 64'ten az eleman için "millisecond level" olduğunu söylüyor. Bu süre ne zaman dilimiyle ne de çerçeveyle karşılaştırılıyor, ρ'ya da girmiyor. FLOPS cinsinden karmaşıklık da veriliyor (basılı s. 10433, PDF s. 10).

Sonuç: Cao vd. yenilik cümlesinin üç parçasına da uyuyor. Gecikme sabit; çalışma süresi ölçülmüş ama uygulanabilirlik kontrolü olarak bile kullanılmamış; eskimeye girmiyor. Yenilik iddiası bu kaynakla **çürümüyor**.

Bir uyarı var: Cao, başlığında "fast-changing channels" diyen, kullanıcı hareketiyle gerekçelendirilen ve hem gecikme-eskime modelini hem ölçülmüş süreyi aynı makalede taşıyan bir çalışma. Jüri en yakın önceki çalışma olarak bunu gösterebilir. Bu nedenle cümlede adıyla anılması savunmayı güçlendirir (öneri [Cao] başlığı altında).

---

## [Cao2022TWC] Cao vd., IEEE TWC 2022

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Yashuai Cao, Tiejun Lv, Wei Ni. Başlık: "Two-Timescale Optimization for Intelligent Reflecting Surface-Assisted MIMO Transmission in Fast-Changing Channels". Dergi: IEEE Transactions on Wireless Communications, VOL. 21, NO. 12, DECEMBER 2022. İlk sayfa 10424; PDF 14 sayfa olduğu için son sayfa 10437. DOI: 10.1109/TWC.2022.3184000. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar: "Two-timescale designs update the phases from channel statistics and the precoder from instantaneous channels [Zhao2021TWC, Cao2022TWC]." Aynı paragrafın son cümlesi ("In these works the delay … does not enter the aging") da bu kaynağı kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 10424, PDF s. 1, Özet: "…where the IRS is configured relatively infrequently based on statistical CSI (S-CSI) and the base station precoder and power allocation are updated frequently based on quickly outdated instantaneous CSI (I-CSI)."
  - Basılı s. 10426, PDF s. 3, §II-A: "Following the Jakes' model [34], the time correlation coefficient is ρ = J0(2πfdτ) = J0(2πf̄d). Here, … τ is the delay between the time when the CSI is measured and the time when the BS produces the precoders based on the CSI". Aynı sayfa: "τ can be up to a slot." ve "τ is no shorter than a slot."
  - Basılı s. 10426, PDF s. 3, Fig. 1 alt yazısı: "…the channels are fast-changing, e.g., due to the movement of the UE."
  - Basılı s. 10428, PDF s. 5: "…the power allocation of the BS is updated slot by slot, based on the outdated CSI available to the BS, due to the non-negligible delay between the I-CSI estimation (e.g., at the UE) and the power allocation."
  - Basılı s. 10433, PDF s. 10, §IV: "Our testing environment is MATLAB R2018b on a desktop computer with 3.20 GHz Intel Core i7-8700 CPU and 8 GB random access memory (RAM)."
  - Basılı s. 10434, PDF s. 11, §IV-A: "Fig. 7 shows that the running time of the proposed PSO algorithms is much shorter than that of the conventional PSO using full batch samples. Moreover, the processing speed of LBO-PSO is at a millisecond level when there are less than 64 IRS meta-atoms…"
  - Basılı s. 10435, PDF s. 12, §IV-C: "A larger temporal correlation coefficient ρ indicates a smaller time delay τ, thus resulting in smaller channel error between consecutive slots."
- **Değerlendirme:** Kaynak, IRS destekli noktadan noktaya (tek kullanıcılı) bir MIMO bağlantısı inceliyor. IRS fazları çerçeve başına bir kez, istatistiksel CSI'dan (mbs-PSO ya da LBO-PSO ile) seçiliyor. BS ön kodlayıcısı (bir önceki dilimin CSI'ının SVD'si, V[t−1]) ve güç dağılımı her dilimde güncelleniyor. "Phases from channel statistics" doğru.
  - "The precoder from instantaneous channels" kısmında bir nüans var: Cao'da ön kodlayıcı anlık CSI'dan hesaplanıyor ama bu CSI **bir dilim eskimiş** (V[t−1]). Makalenin ana fikri tam da bu. Makale 2'nin cümlesi yanlış değil, ama "instantaneous" tek başına Cao'nun eskimiş-CSI vurgusunu siliyor. Ayrıca Cao tek kullanıcılı MIMO, Makale 2 çok kullanıcılı MISO; atıf bir tasarım ilkesine yapıldığı için bu sorun değil.
  - Yenilik cümlesi için yukarıdaki bölüme bakın: çelişki yok. Cao, ölçülmüş çalışma süresinin eskimeye girmediği bir örnek daha. Cümle şu an yalnızca Ryu ve Liu'yu örnek veriyor; Cao'yu da eklemek iddiayı güçlendirir.
- **Karar:** **DOĞRU.** İsteğe bağlı iyileştirme (önerilir): "Two-timescale designs update the phases from channel statistics and the precoder from instantaneous, possibly outdated, channels [Zhao2021TWC, Cao2022TWC]." Son cümle için: "…the optimizer's own run time is at most checked for feasibility, as an operation count [Ryu2026arXiv] or a measured 2 ms against a 20 ms slot [Liu2021WCL], or measured without such a check [Cao2022TWC], and does not enter the aging."

---

## [Wu2020TCOM] Wu ve Zhang, IEEE TCOM 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qingqing Wu, Rui Zhang. Başlık: "Beamforming Optimization for Wireless Network Aided by Intelligent Reflecting Surface With Discrete Phase Shifts". Dergi: IEEE Transactions on Communications, VOL. 68, NO. 3, MARCH 2020. İlk sayfa 1838; PDF 14 sayfa olduğu için son sayfa 1851. DOI: 10.1109/TCOMM.2019.2958916. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar: "Practical surfaces have a few bits of phase resolution [Wu2020TCOM, Zhao2024OJCOMS]; our main results use continuous phases, and Section~\ref{sec:res_robust} adds 1--3-bit phases."
- **Kaynakta karşılığı:**
  - Basılı s. 1838, PDF s. 1, Özet: "Prior works on IRS mainly consider continuous phase shifts at reflecting elements, which are practically difficult to implement due to the hardware limitation."
  - Basılı s. 1839, PDF s. 2, §I: "For example, to enable 16 levels of phase shifts, log2 16 = 4 PIN diodes need to be integrated to each element." Devamı: "…for practical IRSs with a large number of elements, it is more cost-effective to implement only discrete phase shifts with a small number of control bits for each element, e.g., 1-bit for two-level (0 or π) phase shifts [1], [11], [29]."
  - Basılı s. 1841, PDF s. 4, §II, denklem (2): "Let b denote the number of bits used to indicate the number of phase shift levels L where L = 2^b. For simplicity, we assume that such discrete phase-shift values are obtained by uniformly quantizing the interval [0, 2π)."
  - Benzetimler b = 1 ve b = 2 ile yapılıyor (basılı s. 1847, PDF s. 10, Fig. 4).
- **Değerlendirme:** Kaynak, kesikli faz kaydırmalı IRS ile AP gönderim gücünü SINR kısıtları altında en aza indiriyor. Sürekli fazın donanımda zor olduğunu, pratikte "a small number of control bits" kullanıldığını açıkça söylüyor ve 1 ile 2 bit üzerinde çalışıyor. "A few bits of phase resolution" bu kaynağı doğru özetliyor. Kaynağın tekdüze niceleme varsayımı (denklem 2), Makale 2'nin 1–3 bit deneyiyle de uyumlu.
  - Küçük bir nüans: Wu bir prototip makalesi değil, kuramsal bir optimizasyon makalesi. "Practical surfaces have…" iddiasını donanım gerekçesiyle (PIN diyot sayısı) destekliyor ve kendi kaynaklarına ([1], [11], [29]) dayandırıyor. Donanım kanıtını Zhao vd. sağladığı için ikili atıf yerinde.
- **Karar:** **DOĞRU.**

---

## [Zhao2024OJCOMS] Zhao vd., IEEE OJ-COMS 2024

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Yufei Zhao, Yuan Feng, Afkar Mohamed Ismail, Ziyue Wang, Yong Liang Guan, Yongxin Guo, Chau Yuen. Başlık: "2-Bit RIS Prototyping Enhancing Rapid-Response Space-Time Wavefront Manipulation for Wireless Communication: Experimental Studies". Dergi: IEEE Open Journal of the Communications Society, VOLUME 5, 2024. Sayfalar 4885–4901 (PDF 17 sayfa). DOI: 10.1109/OJCOMS.2024.3439558. **UYUŞUYOR.**
- **Makale 2'de nerede:** [Wu2020TCOM] ile aynı cümle.
- **Kaynakta karşılığı:**
  - Basılı s. 4885, PDF s. 1, Özet: "The practical 2-bit phase-shifting unit cell on the RIS is distinguished by its ability to maintain four stable phase states, each with 90° differences, and features an insertion loss of less than 0.6 dB across a bandwidth of 200 MHz."
  - Basılı s. 4886, PDF s. 2, §I: "…[9] and [10] pioneered practical RIS demonstration prototyping in 2020 with limited 1-bit phase modulation capability per unit, which may result in 3 dB energy loss in beamforming caused by the low bit quantization [11], [12]. A year later, [13] unveiled a 2-bit RIS system…"
  - Basılı s. 4889, PDF s. 5, §II-B: "…the current RIS prototyping contains 10 × 10 RF units with an amount of 300 PIN diodes…"
- **Değerlendirme:** Kaynak, 100 elemanlı, eleman başına 2 bitlik (dört faz durumu, 90° aralıklı) bir RIS prototipi sunuyor ve önceki prototiplerin 1 ve 2 bit olduğunu özetliyor. "Practical surfaces have a few bits of phase resolution" bu kaynakla doğrudan destekleniyor. Makale 2'nin 1–3 bit aralığı da kaynağın verdiği tabloyla uyumlu.
  - Bilgi notu: Kaynak, MCU tabanlı denetimle hızlı yeniden yapılandırmayı da vurguluyor (basılı s. 4890, PDF s. 6, §II-B: "the control system needs at least 0.72 ms to switch to a phase distribution corresponding to a new codebook"; 10 izleyici MCU, 1 Mbps SPI). Makale 2 RIS anahtarlama süresini modellemediğini kısıtlarda yazıyor (`section_07_conclusion.tex`, satır 16). Bu sayı orada bir mertebe göstergesi olarak kullanılabilir. Zorunlu değil.
- **Karar:** **DOĞRU.**

---

## [Peel2005TCOM] Peel vd., IEEE TCOM 2005

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Christian B. Peel, Bertrand M. Hochwald, A. Lee Swindlehurst. Başlık: "A Vector-Perturbation Technique for Near-Capacity Multiantenna Multiuser Communication—Part I: Channel Inversion and Regularization". Dergi: IEEE Transactions on Communications, VOL. 53, NO. 1, JANUARY 2005. Sayfalar 195–202 (PDF 8 sayfa). DOI: 10.1109/TCOMM.2004.840638. **UYUŞUYOR.**
- **Makale 2'de nerede:** Sistem modeli (`section_03_system_model.tex`, satır 10): "The precoder is regularized zero-forcing [Peel2005TCOM] on the effective channel, with regularizer λ = Kσ²/P and total power P."
- **Kaynakta karşılığı** (denklemler sayfa görüntüsünden okundu):
  - Basılı s. 196, PDF s. 2, §II "Model": y = Hx + w (2). "We assume that E ww* = σ²I and impose the power constraint E‖x‖² = 1." Denklem (5)'in hemen altında: "…and we define ρ = 1/σ²." ve "Although the total transmitted power is one, the quantity ρ is directly related to, but is not necessarily the same as, the SNR at each receiver." Kanal elemanları "zero-mean unit-variance complex-Gaussian".
  - Basılı s. 198, PDF s. 4, §IV "Regularizing the Inverse": "One technique often used to "regularize" an inverse is to add a multiple of the identity matrix before inverting." Denklem (19): s = H*(HH* + αI)⁻¹u.
  - Basılı s. 199, PDF s. 5, §IV: "Remarkably, the large-K approximation (30) is maximized for α ≥ 0 at α_opt = Kσ² = K/ρ, independently of λ1, …, λK." Devamı: "We see that α_opt is proportional to K and the noise variance."
- **Değerlendirme:** Regularized channel inversion (RZF) bu kaynağın ana katkısı; atıf yerinde. Düzenleme parametresi kaynakta α = Kσ² = K/ρ, toplam gönderim gücü 1 ve ρ = 1/σ² olarak veriliyor. Toplam güç P olduğunda ρ = P/σ² olur ve α = Kσ²/P çıkar. Makale 2'deki λ = Kσ²/P bununla **birebir aynı**.
  - Bir nüans var: Kaynakta bu değer, büyük-K yaklaşık SINR'ını (30) en büyüklüyor. Türetme, birim varyanslı ve dönme altında değişmez (izotropik) bir kanal dağılımına dayanıyor (s. 199: analiz Q'nun "isotropic distribution" taşımasını kullanıyor). Makale 2'nin etkin kanalı (LoS BS–RIS kanalı, yol kaybı, RIS fazına bağlı) bu varsayımları sağlamıyor. Bu yüzden Makale 2'de λ = Kσ²/P "en iyi" değil, kaynaktan alınmış standart bir seçim. Makale 2 en iyilik iddiasında bulunmadığı için bu bir hata değil; ama jüri sorarsa cevap bu.
  - Notasyon: Makale 2 düzenleyiciyi λ ile gösteriyor; Peel'de λ özdeğerleri, α ise düzenleyiciyi gösteriyor. Okur kaynağa dönerse karışabilir; zorunlu değişiklik değil.
- **Karar:** **DOĞRU.** İsteğe bağlı kesinleştirme: "…with regularizer λ = Kσ²/P, the value that maximizes the large-system SINR for i.i.d. channels [Peel2005TCOM], and total power P."

---

## [Nadeem2020TWC] Nadeem vd., IEEE TWC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qurrat-Ul-Ain Nadeem, Abla Kammoun, Anas Chaaban, Mérouane Debbah, Mohamed-Slim Alouini. Başlık: "Asymptotic Max-Min SINR Analysis of Reconfigurable Intelligent Surface Assisted MISO Systems". Dergi: IEEE Transactions on Wireless Communications, VOL. 19, NO. 12, DECEMBER 2020. İlk sayfa 7748; PDF 17 sayfa olduğu için son sayfa 7764. DOI: 10.1109/TWC.2020.2986438. **UYUŞUYOR.**
- **Makale 2'de nerede:** Sistem modeli (`section_03_system_model.tex`, satır 10): "The objective is the minimum user rate, a fairness criterion also used for RIS-assisted multiple-input single-output (MISO) systems in [Nadeem2020TWC], …"
- **Kaynakta karşılığı:**
  - Basılı s. 7748, PDF s. 1, Özet: "We study the minimum signal-to-interference-plus-noise ratio (SINR) achieved by the optimal linear precoder (OLP), that maximizes the minimum SINR subject to a given power constraint for any given RIS phase matrix…"
  - Basılı s. 7749, PDF s. 2, §I: "MIMO precoding in literature is often based on two common optimization criteria - the transmit power minimization and the maximization of the minimum (max-min) SINR [20]. The first criteria has been the focus of [5], [12], while the latter has not been studied in the context of RIS design and is the focus and second novelty of this work."
  - Basılı s. 7751, PDF s. 4, §II-B "Optimal Linear Precoder", problem (P1): max_{P,G} min_k γ_k, s.t. (1/K)1ᵀp ≤ P_max/K, ‖g_k‖ = 1.
- **Değerlendirme:** Kaynak, RIS destekli tek hücreli çok kullanıcılı MISO aşağı bağlantıda en düşük SINR'ı en büyüklüyor. Hem ön kodlayıcı (OLP) hem RIS fazları (deterministik eşdeğer üzerinden projected gradient ascent) bu ölçüte göre seçiliyor. R_k = log₂(1 + SINR_k) tekdüze artan olduğundan en düşük hızı en büyüklemek ile en düşük SINR'ı en büyüklemek aynı problem. Makale 2'nin "also used for RIS-assisted MISO systems" ifadesi doğru.
  - "Fairness criterion" ifadesi kaynakta geçmiyor ("fair" araması sonuç vermedi). Ancak bu, max-min ölçütünün yerleşik nitelemesi ve kaynağa yüklenmiş bir iddia değil; sorun değil.
  - Fark: Nadeem'de ön kodlayıcı max-min için en iyi doğrusal ön kodlayıcı (OLP), Makale 2'de RZF. Atıf yalnızca ölçüte yapıldığı için bu sorun değil.
  - Bilgi notu: Nadeem'in faz tasarımı da yalnızca büyük ölçekli istatistiklere dayanıyor ("requires knowledge of only the channel's large-scale statistics", s. 7749) ve fazlar BS–RIS arasında "after several coherence intervals" paylaşılıyor (s. 7751). Yani bu da iki zaman ölçekli bir tasarım. İlgili çalışmalardaki "Two-timescale designs…" cümlesine eklenebilir; zorunlu değil.
- **Karar:** **DOĞRU.**

---

## Gecikme / çalışma süresi özeti

Bu tablo, yenilik cümlesiyle ("the delay … where modeled, is fixed; … run time … does not enter the aging") ilgili.

| Kaynak | Eskime/gecikme modeli | Ölçülmüş süre | Süre eskimeye giriyor mu |
|---|---|---|---|
| Cao2022TWC | Var: AR(1), ρ = J₀(2π f_d τ), τ sabit (≤ ya da ≥ bir dilim), ρ taranıyor (s. 10426, 10435) | **Var:** Fig. 7, yineleme başına süre; LBO-PSO "millisecond level" (< 64 eleman), MATLAB R2018b / i7-8700 (s. 10433–10434); FLOPS da var | Hayır |
| Wu2020TCOM | Yok (kusursuz CSI) | Yok (aranmadı; atıfla ilgisiz) | — |
| Zhao2024OJCOMS | Yok (prototip) | RIS denetim gecikmesi var (en az 0.72 ms, s. 4890), optimizasyon süresi değil | — |
| Peel2005TCOM | Yok; H'nin bir aralık boyunca sabit olduğu varsayılıyor (s. 196) | Yok | — |
| Nadeem2020TWC | Yok; BS'de kusursuz CSI varsayılıyor (s. 7751) | Yok (aranmadı; atıfla ilgisiz) | — |

---

## Özet tablo

| Kaynak | Karar | Gerekçe |
|---|---|---|
| Cao2022TWC | DOĞRU (isteğe bağlı iyileştirme) | Özet (s. 10424): fazlar S-CSI'dan çerçeve başına, ön kodlayıcı ve güç eskimiş I-CSI'dan dilim başına. Ön kodlayıcının CSI'ı bir dilim eski (V[t−1]); "instantaneous, possibly outdated" daha kesin olur. Eskime modelli (ρ = J₀(2π f_d τ), τ sabit, s. 10426), süre ölçülmüş (Fig. 7, s. 10434) ama eskimeye girmiyor; **yenilik cümlesiyle çelişmiyor**, Cao'yu örnek olarak eklemek önerilir. Künye uyuşuyor |
| Wu2020TCOM | DOĞRU | §I (s. 1839): "a small number of control bits for each element, e.g., 1-bit"; §II denklem (2) (s. 1841): L = 2^b tekdüze niceleme; b = 1, 2 benzetimleri. Künye uyuşuyor |
| Zhao2024OJCOMS | DOĞRU | Özet (s. 4885): 2 bitlik birim hücre, dört durum, 90° aralık; §I (s. 4886): önceki prototipler 1 ve 2 bit. Künye uyuşuyor |
| Peel2005TCOM | DOĞRU (isteğe bağlı kesinleştirme) | Denklem (19) (s. 198) RZF; α_opt = Kσ² = K/ρ (s. 199), birim toplam güç ve ρ = 1/σ² (s. 196). P'ye ölçeklenince λ = Kσ²/P ile birebir aynı. En iyilik yalnızca büyük-K ve i.i.d./izotropik kanal için geçerli; Makale 2 en iyilik iddia etmiyor. Künye uyuşuyor |
| Nadeem2020TWC | DOĞRU | Özet (s. 7748) ve problem (P1) (s. 7751): RIS destekli MISO'da max-min SINR; log₂(1+·) tekdüze olduğu için en düşük hızla eşdeğer. "Fairness" kelimesi kaynakta yok ama yerleşik niteleme. Künye uyuşuyor |

Künye uyuşmazlığı bulunmadı. DÜZELTİLMELİ ya da ÇIKARILMALI kararı yok. Önerilen iki iyileştirme isteğe bağlı: Cao'nun eskimiş CSI'ını ve ölçülmüş süresini cümleye yansıtmak, Peel'in λ seçiminin hangi varsayım altında en iyi olduğunu belirtmek.
