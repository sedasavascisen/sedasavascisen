# Makale 2 — Kaynak kontrolü, Grup 5: kanal eskimesi, İHA, AISY, eskimiş CSI, Huang

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). AISY makalesinde sayfalar "N of 19" biçiminde, PDF sayfasıyla aynı. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`; dal `thesis/p4-deneyler`, commit `c2b391d`). Özette (abstract) ve tablolarda bu beş anahtarın hiçbiri geçmiyor. `unused/section_cnn_lstm_tez.tex` içindeki AISY atıfları makaleye girmediği için kapsam dışı bırakıldı.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

Bib anahtarları: Papazafeiropoulos2023TVT, Liu2021WCL, SavasciSen2026AISY, Zhang2022TCOM, Huang2022TWC.

---

## ÖNCE OKUNMALI

### 1. Yenilik cümlesiyle çelişki yok, ama bir nüans var

İlgili çalışmalar bölümündeki (`sections/section_02_related_work.tex`, satır 8) yenilik cümlesi şu: *"In these works the delay between channel acquisition and use, where modeled, is a fixed parameter; the optimizer's own run time, at most a feasibility constraint on its operation count [Ryu2026arXiv], does not enter the aging."*

Bu gruptaki dört kaynağın **hiçbiri** optimizasyon ya da tahmin süresini eskime gecikmesine katmıyor. Cümlenin ana iddiası bu dört kaynak için doğru.

Ancak [Liu2021WCL] çalışma süresini **ölçüyor** ve bir uygulanabilirlik koşulu olarak kullanıyor. Basılı s. 672, PDF s. 5, §IV: LRNet'in tahmin süresi i7-6700 CPU ve GTX 1080 GPU üzerinde τc = 2 ms ölçülüyor ve ΔT = 20 ms'lik zaman diliminden kısa olduğu gösteriliyor ("the BS can complete the prediction task before the next time instant"). Bu süre eskimeye girmiyor: hüzme her durumda bir sonraki dilim için kuruluyor, gecikme sabit bir ΔT. Yani cümlenin "does not enter the aging" kısmı Liu için de doğru. Ama "at most a feasibility constraint on its operation count" ifadesi literatürde yalnızca işlem sayısına dayalı bir koşul varmış gibi okunuyor. Liu ise ölçülmüş duvar saati süresini kullanıyor. Düzeltme önerisi [Liu2021WCL] başlığı altında.

### 2. AISY (Makale 1) künyesinde basılı PDF'te olmayan cilt/sayı

Bib girdisi `volume={8}, number={9}` diyor. Elimizdeki PDF'te cilt ve sayı yok. Wiley indirme şeridi "26404567, 0, Downloaded from …" diyor (cilt yerine 0) ve PDF üst verisi "Advanced Intelligent Systems 0.0:e70460". Bu, makalenin bir sayıya atanmadan çevrimiçi yayımlandığını (Early View, kesinleşmiş sürüm) gösteriyor. 8(9) bilgisi bu PDF'ten doğrulanamıyor. Ayrıntı [SavasciSen2026AISY] başlığı altında.

---

## [Papazafeiropoulos2023TVT] Papazafeiropoulos vd., IEEE TVT 2023

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Anastasios Papazafeiropoulos, Ioannis Krikidis, Pandelis Kourtessis. Başlık: "Impact of Channel Aging on Reconfigurable Intelligent Surface Aided Massive MIMO Systems With Statistical CSI". Dergi: IEEE Transactions on Vehicular Technology, VOL. 72, NO. 1, JANUARY 2023. İlk sayfa 689; PDF 15 sayfa olduğu için son sayfa 703. DOI: 10.1109/TVT.2022.3203796. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, "Mobility and outdated channels" paragrafı: "Channel aging [Papazafeiropoulos2023TVT] and outdated channel knowledge [Zhang2022TCOM] have been analyzed for RIS, …" Paragrafın sonundaki yenilik cümlesi de bu kaynağı kapsıyor ("In these works the delay … is a fixed parameter; the optimizer's own run time … does not enter the aging").
- **Kaynakta karşılığı:**
  - Basılı s. 689, PDF s. 1, Özet: "Hence, in this work, we investigate the impact of channel aging on the performance of RIS-assisted mMIMO systems under both spatial correlation and imperfect CSI conditions." Aynı özet: "Subsequently, we present the attractive optimization of the achievable sum SE with respect to the phase shifts and the total transmit power that can be performed every several coherence intervals due to the slow variation of the large-scale statistics."
  - Eskime modeli: basılı s. 692, PDF s. 4, §II-B "Channel Aging", denklem (4): h_{k,n} = α_{k,n} h_{k,0} + ᾱ_{k,n} e_{k,n}. Alıntı: "αk,n = J0(2πfD Ts n) is the temporal correlation coefficient of UE k between the channel realizations at time 0 and n with J0(·) being the zeroth-order Bessel function of the first kind, Ts being the channel sampling duration, and fD = vfc/c being the maximum Doppler shift."
  - Sayısal değerler: basılı s. 698, PDF s. 10, §VI: "The Doppler spread, corresponding to a relative velocity of 135 km/h between the BS and the UEs, is fD = 250 Hz. Moreover, if we assume that the bandwidth is W = 20 MHz, the symbol time is Ts = 1/(2W) = 0.025 μs." Fig. 3 fD·Ts'yi n = 160'ta tarıyor, Fig. 4 zaman indisi n'yi tarıyor.
  - Çalışma süresi: yalnızca karmaşıklık mertebesi. Basılı s. 696, PDF s. 8: "the complexity of Algorithm 1 is O(MN² + N + M)". Yakınsama yineleme sayısına göre çiziliyor (Fig. 7, basılı s. 699). "CPU", "running time", "seconds", "execution" araması süre ölçümü bulmadı.
- **Değerlendirme:** Kaynak, RIS destekli büyük MIMO'da kanal eskimesini hem yukarı bağlantı eğitiminde hem aşağı bağlantı veri iletiminde modelliyor. MMSE kestirimi, RZF ön kodlamayla kapalı biçimli bir toplam SE ifadesi ve istatistiksel CSI'ya dayalı faz/güç optimizasyonu var. "Channel aging … analyzed for RIS" atfı doğru.
  - Yenilik cümlesi açısından: gecikme, TDD çerçevesindeki sembol indisi n ile örnekleme süresi Ts'nin çarpımı (n·Ts). Bu, çerçeve yapısının belirlediği ve şekillerde taranan bir model parametresi. Faz optimizasyonu istatistiksel CSI ile "every several coherence intervals" yapılıyor. Optimizasyonun süresi eskimeye girmiyor. "Fixed parameter" nitelemesi kabaca doğru; daha kesin ifade "a model parameter set by the frame structure" olurdu. Gecikme tek bir sabit değil, çerçeve içinde n ile büyüyor. Bu bir hata değil, yalnızca bir incelik.
- **Karar:** **DOĞRU.**

---

## [Liu2021WCL] Liu vd., IEEE WCL 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Chang Liu, Weijie Yuan, Zhiqiang Wei, Xuemeng Liu, Derrick Wing Kwan Ng. Başlık: "Location-Aware Predictive Beamforming for UAV Communications: A Deep Learning Approach". Dergi: IEEE Wireless Communications Letters, VOL. 10, NO. 3, MARCH 2021. İlk sayfa 668; PDF 5 sayfa olduğu için son sayfa 672. DOI: 10.1109/LWC.2020.3045150. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, "Mobility and outdated channels" paragrafı: "…predictive beamforming forecasts the position and beam direction of fast unmanned aerial vehicles [Liu2021WCL], …" Ardından gelen yenilik cümlesi de bu kaynağı kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 668, PDF s. 1, Özet: "Specifically, a long short-term memory (LSTM)-based recurrent neural network (LRNet) is designed for UAV location prediction. Based on the predicted location, a predicted angle between the UAV and the BS can be determined for effective and fast beam alignment in the next time slot, which enables reliable communications between the UAV and the BS."
  - Hız: basılı s. 671, PDF s. 4, §IV: "we set a = 0.4 m/ΔT, b = 0.7 m/ΔT, c = −π/6, and d = π/6, i.e., the UAV has an equivalent speed around 20∼35 m/s [13]." Aynı yerde: "the duration for each time instant is ΔT = 0.02 s."
  - Çalışma süresi: basılı s. 672, PDF s. 5, §IV: "its computation time on a desktop computer with an i7-6700 3.4 GHz central processing unit (CPU) and a Nvidia GeForce GTX 1080 GPU is τc = 2 ms which is less than the observation time duration ΔT = 20 ms. … Therefore, the BS can complete the prediction task before the next time instant…" Table II karmaşıklık mertebelerini veriyor.
- **Değerlendirme:** Kaynak RIS içermiyor. Yalnızca LoS kanallı, ULA'lı bir İHA–BS bağlantısında, LSTM ile bir sonraki dilimin konumunu tahmin ediyor ve açıyı bu konumdan geometrik olarak hesaplıyor (denklem 1). Makale 2'deki paragraf RIS demeden "predictive beamforming" diyor; bu yerinde.
  - "Forecasts the position and beam direction" ifadesi büyük ölçüde doğru. Ağ yalnızca konumu tahmin ediyor; hüzme yönü ayrı bir tahmin değil, tahmin edilen konumdan türetilen açı. "Fast" nitelemesi 20–35 m/s ile destekleniyor.
  - Yenilik cümlesi açısından: gecikme sabit bir zaman dilimi (ΔT = 20 ms, bir adım ileri). Tahmin süresi ölçülüyor (2 ms) ama yalnızca τc < ΔT koşulu olarak kullanılıyor, eskimeye girmiyor. Cümlenin "does not enter the aging" kısmı doğru. "At most a feasibility constraint on its operation count [Ryu2026arXiv]" kısmı ise eksik: Liu ölçülmüş bir duvar saati süresini koşul olarak kullanıyor. Bu, tezin "süre ölçülse bile eskimeye katılmıyor" iddiasını destekleyen iyi bir örnek, atlanmamalı.
- **Karar:** Atıf **DOĞRU**, küçük bir netleştirme önerilir: "…predictive beamforming forecasts the position of fast unmanned aerial vehicles and points the beam at it [Liu2021WCL]…". Yenilik cümlesi **DÜZELTİLMELİ**. Önerilen biçim: "…the optimizer's own run time is at most checked for feasibility, as an operation count [Ryu2026arXiv] or as a measured 2 ms prediction time against a 20 ms slot [Liu2021WCL], and does not enter the aging."

---

## [SavasciSen2026AISY] Savaşçı Şen vd., Advanced Intelligent Systems 2026 (Makale 1)

Görev gereği yalnızca künye ve iki cümlenin doğruluğu kontrol edildi. Makale 1'in sonuçları denetlenmedi.

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Seda Savaşçı Şen, Ali Çalhan, Murtaza Cicioğlu, Oğuzhan Demiryürek. Başlık: "Overcoming the Phase Discontinuity Problem in RIS Optimization: A Robust and Scalable Phase-Aware Deep Regression Framework via Hybrid CNN–LSTM Architecture". Dergi: Advanced Intelligent Systems. Alt bilgi: "Advanced Intelligent Systems, 2026; e70460", "https://doi.org/10.1002/aisy.70460". Tarihler: "Received: 24 February 2026 | Revised: 3 June 2026 | Accepted: 12 June 2026". Açık erişim (CC BY), "RESEARCH ARTICLE". Yazarlar, başlık, dergi, yıl, makale numarası (e70460) ve DOI **UYUŞUYOR**.
  - **Cilt/sayı uyuşmuyor.** Bib `volume={8}, number={9}` diyor; PDF'te cilt ve sayı yok. Her sayfanın kenarındaki Wiley şeridi "26404567, 0, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.70460 … on [10/08/2026]" diyor (ISSN'den sonra cilt yerine 0). PDF üst verisi (`pdfinfo` Subject): "Advanced Intelligent Systems 0.0:e70460". Bu biçim Wiley'nin Early View sürümüdür. Dizgisi tamamlanmış, DOI'li kesinleşmiş sürümdür (yalnızca "Accepted" el yazması değil), ama henüz bir sayıya atanmamış. PDF 10 Ağustos 2026'da indirilmiş, sonradan sayıya atanmış olabilir. Bu PDF'ten 8(9) doğrulanamıyor.
- **Makale 2'de nerede:** İki yerde atıf var.
  - (a) Giriş, üçüncü paragraf: "It continues our single-pass phase predictor with a sine–cosine representation [SavasciSen2026AISY] by asking when such speed pays off once run time is charged."
  - (b) İlgili çalışmalar, "Learning" paragrafı: "Predicting the sine and cosine of each phase removes the ±π discontinuity of direct phase regression [SavasciSen2026AISY]."
- **Kaynakta karşılığı:**
  - (a) ve (b) s. 1, Özet: "To overcome this, we propose a robust, phase-aware hybrid CNN–LSTM framework that maps the cyclic phase-space onto continuous Euclidean coordinates via orthogonal sine–cosine projections." Aynı özet: "…data-driven RIS optimizers suffer from the phase discontinuity problem, where estimation collapses near ± π boundaries…"
  - (b) s. 3: "Instead of directly predicting θn ∈ [−π, π], the network separately predicts sin(θn) and cos(θn) as continuous functions on [−1, 1], enabling seamless phase recovery via θn = atan2(sin θn, cos θn). This representation eliminates discontinuity-induced errors and reduces RMSE by 29.9% over a direct phase prediction baseline with identical architecture (ablation, Table 1)." Çıkış biçimi s. 6, denklem (11)–(12); birim çembere izdüşüm denklem (13).
  - (a) "single-pass": s. 6: "a trained CNN–LSTM consolidates both steps into a single 0.08 ms forward pass." s. 2, §1.2.2: "a trained network maps any channel instance to a near-optimal phase configuration in a single forward pass."
  - Özgünlük sınırı: s. 2, §1.2.3: "Note on Novelty: Sine–cosine decomposition of angular outputs is established in computer vision (orientation/pose regression) and signal processing (circular statistics)." Aynı bölüm: "Phase-aware learning strategies [36] have been applied in MIMO-OFDM channel estimation, where projecting phase information onto its sine–cosine components yields measurably sharper predictions."
- **Değerlendirme:** (a) Kaynak, kanaldan faz vektörünü tek ileri geçişte veren bir CNN–LSTM regresörü; çıkışı her eleman için (sin θ, cos θ), faz atan2 ile geri kazanılıyor. "Single-pass phase predictor with a sine–cosine representation" nitelemesi doğru.
  - (b) Teknik içerik doğru: kaynak, doğrudan faz regresyonunun ±π sınırındaki süreksizliğini tanımlıyor ve sinüs–kosinüs çıkışıyla gideriyor (ablasyonda %29.9 RMSE azalması). Ancak cümle genel bir olguyu yalnızca yazarların kendi makalesine bağlıyor. Makale 1 ise kendi "Note on Novelty" kısmında tekniğin bilgisayarlı görü ve dairesel istatistikte yerleşik olduğunu, ayrıca MIMO-OFDM kestiriminde [36] uygulandığını söylüyor. Yanlış değil, ama bir hakem bunu öz-atıfla sahiplenme olarak okuyabilir. Önerilen biçim: "Predicting the sine and cosine of each phase, an established remedy for angular regression, removes the ±π discontinuity of direct phase regression and was applied to RIS phases in our earlier work [SavasciSen2026AISY]."
- **Karar:** Künye **DÜZELTİLMELİ**: Wiley sayfasında güncel cilt/sayı doğrulanmalı. Hâlâ Early View ise `volume` ve `number` kaldırılmalı, gerekirse `note={Early View}` eklenmeli. Atıf (a) **DOĞRU**. Atıf (b) **DOĞRU**; yukarıdaki biçim önerilir ama zorunlu değil.

---

## [Zhang2022TCOM] Zhang vd., IEEE TCOM 2022

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Yan Zhang, Jiayi Zhang, Marco Di Renzo, Huahua Xiao, Bo Ai. Başlık: "Reconfigurable Intelligent Surfaces With Outdated Channel State Information: Centralized vs. Distributed Deployments". Dergi: IEEE Transactions on Communications, VOL. 70, NO. 4, APRIL 2022. İlk sayfa 2742; PDF 15 sayfa olduğu için son sayfa 2756. DOI: 10.1109/TCOMM.2022.3146344. **UYUŞUYOR.**
- **Makale 2'de nerede:** İlgili çalışmalar, "Mobility and outdated channels" paragrafı: "Channel aging [Papazafeiropoulos2023TVT] and outdated channel knowledge [Zhang2022TCOM] have been analyzed for RIS, …" Ardından gelen yenilik cümlesi de bu kaynağı kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 2742, PDF s. 1, Özet: "In this paper, we investigate the performance of an RIS-aided wireless communication system subject to outdated channel state information that may operate in both the near- and far-field regions."
  - Eskimiş CSI modeli: basılı s. 2744, PDF s. 3, §II, denklem (1)–(2): h0 = ρ0 ĥ0 + ρ̄0 ω0, gC = ρC ĝC + ρ̄C ωC. Alıntı: "…which can be calculated as ρ0 = J0(2πfd Ts0) based on Clarke's fading spectrum [43], where … Ts0 is the estimation delay between the actual channel and the outdated channel." Gerekçe aynı sayfada: "Due to the user mobility, it is not usually possible to perfectly estimate the CSI at the BS and the RIS (e.g., due to the acquisition delay and the feedback overhead)."
  - Faz seçimi: basılı s. 2745, PDF s. 4: "The phase shifts at the RIS can be designed such that the outdated direct channel (from the BS to the user) and the outdated cascaded channel (from the BS to the RIS and from the RIS to the user) are co-phased, i.e., φCm = φĥ0 − (φĝCm + φhCm) for m = 1, …, M [39]…"
  - Sayısal değerler: basılı s. 2750, PDF s. 9, §IV: şekiller doğrudan ρ ile çiziliyor (ör. "ρ0 = 0.95, ρC = 0.9"); "the EC decreases as ρ decreases (i.e., the CSI becomes more outdated)".
  - Çalışma süresi: yöntem kapalı biçimli eş-fazlama, yinelemeli bir optimizasyon yok. "CPU", "running time", "complexity" araması süre ölçümü bulmadı.
- **Değerlendirme:** Kaynak, eskimiş CSI altında tek ve dağıtık RIS yerleşimlerinin ergodik kapasitesini analitik olarak inceliyor; yakın ve uzak alanı kapsıyor. "Outdated channel knowledge … analyzed for RIS" atfı doğru.
  - Yenilik cümlesi açısından: gecikme Ts0 (ve TsC) bir model parametresi; sonuçlarda ise doğrudan sabit korelasyon katsayıları (ρ0 = 0.95, ρC = 0.9) olarak giriyor. Faz kapalı biçimde eskimiş kestirime göre ayarlandığı için ortada bir optimizasyon süresi bile yok. "Fixed parameter" nitelemesi bu kaynak için tam olarak doğru.
- **Karar:** **DOĞRU.**

---

## [Huang2022TWC] Huang vd., IEEE TWC 2022

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Zixuan Huang, Beixiong Zheng, Rui Zhang. Başlık: "Transforming Fading Channel From Fast to Slow: Intelligent Refracting Surface Aided High-Mobility Communication". Dergi: IEEE Transactions on Wireless Communications, VOL. 21, NO. 7, JULY 2022. İlk sayfa 4989; PDF 15 sayfa olduğu için son sayfa 5003. DOI: 10.1109/TWC.2021.3135685. **UYUŞUYOR.** (Erken sürümü ICC 2021'de sunulmuş; bib dergi sürümünü veriyor, doğru.)
- **Makale 2'de nerede:** İlgili çalışmalar, "Mobility and outdated channels" paragrafının ilk cümlesi: "A vehicle-mounted intelligent refracting surface, combined with a two-stage channel estimation and refraction design, converts the end-to-end channel from fast to slow fading [Huang2022TWC]." Ardından gelen yenilik cümlesi de bu kaynağı kapsıyor.
- **Kaynakta karşılığı:**
  - Basılı s. 4989, PDF s. 1, Özet: "In this paper, we study a new IRS-aided high-mobility communication system by employing the intelligent refracting surface with a high-speed vehicle to aid its passenger's communication with a remote base station (BS)." Aynı özet: "…we propose a new and efficient two-stage transmission protocol to achieve both IRS channel estimation and refraction optimization for data transmission." Ve: "Simulation results show that the proposed design can efficiently achieve the full IRS passive beamforming gain in the high-mobility communication scenario, which also converts the overall BS-user channel from fast to slow fading for more reliable transmission."
  - Gecikme varsayımı: basılı s. 4994, PDF s. 6, §III: "For simplicity, we assume that the control link is reliable with negligible delay." Dipnot 4: "The proposed protocol can be modified to accommodate small but non-negligible feedback delay, for which the performance will be investigated by simulation in Section IV."
  - Gecikmeli çeşit: basılı s. 4997, PDF s. 9, §IV-B: "Modified Scheme with Feedback Delay (FD): … We assume that the IRS can only adjust its refraction at each block based on the user feedback in the previous block due to the feedback delay." Basılı s. 4998, PDF s. 10: Fig. 8 için "Tb = 0.2 ms"; FD altında hızın artmasıyla hız düşüyor.
  - Çalışma süresi: yalnızca karmaşıklık mertebesi. Basılı s. 4994, PDF s. 6: "the overall complexity for the proposed two-step algorithm is given by O(τ1(AxAy + Iit))." "CPU", "running time", "seconds" araması süre ölçümü bulmadı.
- **Değerlendirme:** Kaynak, yüksek hızlı bir aracın üzerine yerleştirilen kırıcı (refracting) bir IRS öneriyor. IRS ile yolcu arasındaki kanal yarı-durağan, BS–IRS kanalı LoS ağırlıklı. Stage I'de basamaklı kanalın LoS bileşeni kestirilip kırılma tasarlanıyor; Stage II'de ortak bir faz kaydırmasıyla IRS'li ve IRS'siz bağlantılar hizalanıyor. Sonuç olarak BS–kullanıcı kanalı hızlı sönümlemeden yavaş sönümlemeye dönüşüyor. Makale 2'deki cümle (araca monte kırıcı yüzey, iki aşamalı kestirim ve kırılma tasarımı, hızlıdan yavaşa dönüşüm) kaynağın özetiyle birebir örtüşüyor. "End-to-end channel" ile kaynaktaki "overall BS-user channel" aynı şey.
  - Yenilik cümlesi açısından: temel tasarımda gecikme ihmal ediliyor. Gecikmeli çeşitte gecikme sabit bir blok (Tb = 0.2 ms). Kestirim algoritmasının süresi eskimeye girmiyor. "Where modeled, is a fixed parameter" nitelemesi doğru.
- **Karar:** **DOĞRU.**

---

## Gecikme / çalışma süresi modelleme özeti

Bu tablo, yenilik cümlesiyle ("the delay … is a fixed parameter; the optimizer's own run time … does not enter the aging") ilgili.

| Kaynak | Gecikme nasıl modelleniyor | Çalışma süresi ölçülüyor mu | Süre eskimeye giriyor mu |
|---|---|---|---|
| Papazafeiropoulos2023TVT | α = J0(2πfD Ts n), çerçeve içindeki sembol indisi n; Ts = 0.025 μs, fD = 250 Hz (s. 692, 698) | Hayır; O(MN² + N + M) (s. 696) | Hayır |
| Liu2021WCL | Bir dilim ileri tahmin, ΔT = 20 ms (s. 671) | **Evet:** τc = 2 ms, i7-6700 + GTX 1080; yalnızca τc < ΔT koşulu (s. 672) | Hayır |
| SavasciSen2026AISY | Durağan kanal (kapsam dışı) | — (denetlenmedi) | — |
| Zhang2022TCOM | ρ = J0(2πfd Ts0), Ts0 kestirim gecikmesi; sonuçlarda sabit ρ0 = 0.95, ρC = 0.9 (s. 2744, 2750) | Hayır; kapalı biçimli eş-fazlama (s. 2745) | Hayır (optimizasyon yok) |
| Huang2022TWC | Temel tasarımda ihmal; FD çeşidinde bir blok, Tb = 0.2 ms (s. 4994, 4997–4998) | Hayır; O(τ1(AxAy + Iit)) (s. 4994) | Hayır |

---

## Özet tablo

| Kaynak | Karar | Gerekçe |
|---|---|---|
| Papazafeiropoulos2023TVT | DOĞRU | RIS'li büyük MIMO'da kanal eskimesi (s. 689); gecikme n·Ts, çerçeve yapısıyla belirlenen bir model parametresi (s. 692); süre ölçümü yok; künye uyuşuyor |
| Liu2021WCL | Atıf DOĞRU (küçük netleştirme önerilir); yenilik cümlesi DÜZELTİLMELİ | LSTM konumu tahmin ediyor, açı konumdan türetiliyor (s. 668); 20–35 m/s (s. 671). Tahmin süresi **ölçülüyor** (2 ms < 20 ms, s. 672) ama eskimeye girmiyor; "operation count" ifadesi bu örneği dışarıda bırakıyor; künye uyuşuyor |
| SavasciSen2026AISY | Künye DÜZELTİLMELİ; (a) DOĞRU; (b) DOĞRU (öz-atıf biçimi yumuşatılabilir) | Tek ileri geçiş (s. 6), sin/cos çıkış + atan2 (s. 3, 6), ±π süreksizliği (s. 1). Basılı PDF Early View: cilt/sayı yok ("26404567, 0", "0.0:e70460"); bib'deki 8(9) doğrulanamadı |
| Zhang2022TCOM | DOĞRU | RIS'te eskimiş CSI, ρ = J0(2πfd Ts0) (s. 2744); sonuçlarda sabit ρ (s. 2750); kapalı biçimli faz, optimizasyon süresi yok; künye uyuşuyor |
| Huang2022TWC | DOĞRU | Araca monte kırıcı IRS, iki aşamalı protokol, hızlıdan yavaşa dönüşüm (s. 4989); gecikme ihmal ya da bir blok (Tb = 0.2 ms) (s. 4994, 4997–4998); künye uyuşuyor |

ÇIKARILMALI kararı yok. Hiçbir kaynak optimizasyon ya da tahmin süresini eskime gecikmesine katmıyor; Makale 2'nin yenilik iddiası bu grupta çürütülmedi. Düzeltmeler iki tane: yenilik cümlesindeki "operation count" ifadesi Liu'nun ölçülmüş süre koşulunu da kapsayacak biçimde genişletilmeli, AISY künyesindeki cilt/sayı doğrulanmalı ya da kaldırılmalı.
