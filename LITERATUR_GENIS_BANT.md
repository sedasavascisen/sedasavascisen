# Literatür taraması: geniş bant RIS faz tasarımı, gecikme ve hareketlilik

Tarih: 2026-11-09. Yöntem: her künye **Crossref API** üzerinden (başlık sorgusu → DOI, cilt, sayfa)
doğrulandı. Özetler ve alıntılar **arXiv export API**'sinden, arXiv'de bulunmayan iki makale için
Semantic Scholar Graph API'sinden alındı. Alıntılar özetten **kelimesi kelimesine** kopyalandı, makalenin
tam metni okunmadı. Bu yüzden "özet bunu söylüyor" ile "makale bunu yapıyor" arasındaki fark aşağıda
ayrıca belirtildi.

> Uyarı: Bu, anahtar kelime sorgularıyla yapılmış hedefli bir taramadır, sistematik bir derleme değildir.
> Google Scholar, IEEE Xplore tam metin araması ve atıf zinciri takibi yapılmadı. "Bulunamadı" ifadesi
> "yok" demek değildir.

---

## 1. IRS/RIS destekli OFDM: tüm alt taşıyıcılar için tek faz vektörü

**[1.1] B. Zheng, R. Zhang**, "Intelligent Reflecting Surface-Enhanced OFDM: Channel Estimation and
Reflection Optimization," *IEEE Wireless Communications Letters*, vol. 9, no. 4, pp. 518–522, Nisan 2020.
DOI: 10.1109/LWC.2019.2961357 · arXiv:1909.03272
- Kanal kestirimi ile yansıma optimizasyonunu ardışık yürüten bir IRS-OFDM protokolü önerir. Tek yansıma
  vektörü, zaman domeninde ayrıştırılan en güçlü yola göre, düşük karmaşıklıkla seçilir.
- Alıntı: *"the reflection coefficients are then optimized by a low-complexity algorithm based on the
  resolved strongest signal path in the time domain."*

**[1.2] Y. Yang, B. Zheng, S. Zhang, R. Zhang**, "Intelligent Reflecting Surface Meets OFDM: Protocol
Design and Rate Maximization," *IEEE Transactions on Communications*, vol. 68, no. 7, pp. 4522–4535,
Temmuz 2020. DOI: 10.1109/TCOMM.2020.2981458 · arXiv:1906.09956
- Seçici sönümlemeli kanalda alt taşıyıcı güç dağılımını ve IRS yansıma katsayılarını ardışık
  optimizasyonla birlikte tasarlayarak hızı en büyütür. Komşu elemanların ortak katsayı paylaştığı
  gruplama ile eğitim yükünü azaltır.
- Alıntı: *"we formulate the problem to maximize the achievable rate by jointly optimizing the transmit
  power allocation and the IRS passive array reflection coefficients."*

**[1.3] S. Lin, B. Zheng, G. C. Alexandropoulos, M. Wen, F. Chen, S. Mumtaz**, "Adaptive Transmission for
Reconfigurable Intelligent Surface-Assisted OFDM Wireless Communications," *IEEE Journal on Selected Areas
in Communications*, vol. 38, no. 11, pp. 2653–2665, Kasım 2020. DOI: 10.1109/JSAC.2020.3007038
- Geniş bant RIS-SIMO-OFDM için çerçeveyi alt çerçevelere bölen ve kanal kestirimini pasif hüzme
  oluşturmayla aynı anda yürüten bir protokol önerir. CSI tek seferde değil, alt çerçeveler boyunca
  parça parça elde edilir. Bu da tezdeki "CSI tazeliği" tartışmasına en yakın protokol düzeyindeki çalışmadır.
- Alıntı: *"each transmission frame is divided into multiple sub-frames to execute channel estimation
  simultaneously with passive beamforming."*

**[1.4] H. Li, W. Cai, Y. Liu, M. Li, Q. Liu, Q. Wu**, "Intelligent Reflecting Surface Enhanced Wideband
MIMO-OFDM Communications: From Practical Model to Reflection Optimization," *IEEE Transactions on
Communications*, vol. 69, no. 7, pp. 4807–4820, Temmuz 2021. DOI: 10.1109/TCOMM.2021.3069860 ·
arXiv:2007.14243
- Yansıma katsayısının frekansa bağlı faz ve genlik kaymasını (dual squint) modelleyip MU-MISO-OFDM'de
  ortalama toplam hızı WMMSE/BCD ile en büyütür. İdeal modelin geniş bantta ciddi kayıp verdiğini gösterir.
- Alıntı: *"we first study the dual phase- and amplitude-squint effect of reflected signals and present a
  simplified practical IRS reflection model for wideband signals."* / *"Complexity and convergence for
  both cases are analyzed or illustrated."*

**[1.5] W. Cai, H. Li, M. Li, Q. Liu**, "Practical Modeling and Beamforming for Intelligent Reflecting
Surface Aided Wideband Systems," *IEEE Communications Letters*, vol. 24, no. 7, pp. 1568–1571, Temmuz 2020.
DOI: 10.1109/LCOMM.2020.2987322 · arXiv:2006.01465
- Görevde geçen "Cai et al." büyük olasılıkla bu çalışmadır. Faz-genlik-frekans ilişkisini modelleyip
  OFDM'de alt taşıyıcı güç dağılımı ile IRS hüzme oluşturmayı birlikte tasarlar.
- Alıntı: *"we aim to investigate the phase-amplitude-frequency relationship of the reflected signals and
  propose a practical model of reflection coefficient for an IRS-aided wideband system."*

**[1.6] R. Ranjan, A. Bhattacharya, S. Mukhopadhyay, H. B. Mishra**, "A Gradient Ascent Based Low
Complexity Rate Maximization Algorithm for Intelligent Reflecting Surface-Aided OFDM Systems," *IEEE
Communications Letters*, vol. 27, no. 8, pp. 2083–2087, Ağustos 2023. DOI: 10.1109/LCOMM.2023.3289865
(özet: Semantic Scholar)
- IRS-OFDM hız maksimizasyonu için gerçel değişkenli, kutu kısıtlı bir gradyan yükselişi önerir.
  Gerekçesi açıkça hızdır: elemanlar çok olduğu için güncellemenin hızlı olması gerekir. Tezin PGD koluna
  en yakın klasik çalışmadır.
- Alıntı: *"it is crucial to update the reflection coefficients using a fast optimization algorithm."* /
  *"We demonstrate the efficacy of the proposed GA method over the state-of-the-art solutions in terms of
  convergence speed, computational complexity and achievable rate"*
- Belirsizlik: Tam metin kapalı erişimli. "Convergence speed" ifadesinin iterasyon sayısı mı, duvar saati
  mi olduğu doğrulanmadı. Hareketlilik ya da kanal eskimesi özette geçmiyor.

---

## 2. Beam squint / uzamsal geniş bant etkisi (mmWave/THz, büyük RIS)

**[2.1] Y. Chen, D. Chen, T. Jiang**, "Beam-Squint Mitigating in Reconfigurable Intelligent Surface Aided
Wideband MmWave Communications," *2021 IEEE WCNC*, pp. 1–6, 2021. DOI: 10.1109/WCNC49053.2021.9417413 ·
arXiv:2103.11105
- Pasif RIS'in faz kaymasının tüm frekanslarda aynı olmak zorunda olduğunu açıkça kısıt olarak koyar.
  Beam squint altında ortak fazı LoS için üst sınırla, NLoS için ortalama kanal kovaryansıyla (MCCM) seçer.
- Alıntı: *"Due to the intrinsic passive property, the phase shifts of all elements in RIS should be the
  same for all frequencies. However, in the wideband scenario, beam squint induced distinct path phases
  require designing different phase shifts for different frequencies."*

**[2.2] S. Ma, W. Shen, J. An, L. Hanzo**, "Wideband Channel Estimation for IRS-Aided Systems in the Face
of Beam Squint," *IEEE Transactions on Wireless Communications*, vol. 20, no. 10, pp. 6240–6253, Ekim 2021.
DOI: 10.1109/TWC.2021.3072694 · arXiv:2106.02883
- Görevdeki "Ma et al." budur. Beam squint'in kaskad kanalın korelasyonunda sahte bir açı tepesi
  ürettiğini gösterir ve bunu bastıran iki aşamalı OMP (TS-OMP) önerir. Faz tasarımı değil, kestirim çalışmasıdır.
- Alıntı: *"The existing channel estimation methods conceived for wideband IRS-aided communication systems
  only consider the channel's frequency selectivity, but ignore the effect of beam squint"*

**[2.3] R. Su, L. Dai, D. W. K. Ng**, "Wideband Precoding for RIS-Aided THz Communications," *IEEE
Transactions on Communications*, vol. 71, no. 6, pp. 3592–3604, Haziran 2023. DOI: 10.1109/TCOMM.2023.3263230
(özet: Semantic Scholar)
- RIS'e zaman gecikmesi (TD) modülleri ekleyerek faz-tek ön kodlamayı faz+gecikme ön kodlamasına çevirir
  (alt bağlantılı RIS). BS ve RIS'teki "çift hüzme bölünmesi"nin ayrı ayrı çözülebildiğini kanıtlar.
- Alıntı: *"The crux is to introduce additional time-delay (TD) modules and phase shifters into RIS
  elements so as to convert the classical phase-only precoding to the joint phase and delay precoding."*

**[2.4] W. Hao, X. You, F. Zhou, Z. Chu, G. Sun, P. Xiao**, "The Far-/Near-Field Beam Squint and
Solutions for THz Intelligent Reflecting Surface Communications," *IEEE Transactions on Vehicular
Technology*, vol. 72, no. 8, pp. 10107–10118, Ağustos 2023. DOI: 10.1109/TVT.2023.3254153 · arXiv:2208.12385
- THz IRS'te uzak ve yakın alan beam squint'ini analiz eder. Gecikmesi ayarlanabilir metayüzey (DAM) ile
  faz ve gecikmeyi birlikte optimize eder.
- Alıntı: *"we propose to apply delay adjustable metasurface (DAM) to IRS, and develop a scheme of
  optimizing the reflecting phase shifts and time delays of IRS elements"*

**[2.5] J. Wang, J. Xiao, Y. Zou, W. Xie, Y. Liu**, "Wideband Beamforming for RIS Assisted Near-Field
Communications," *IEEE Transactions on Wireless Communications*, vol. 23, no. 11, pp. 16836–16851, Kasım 2024.
DOI: 10.1109/TWC.2024.3447570 · arXiv:2401.11141
- Yakın alan çift hüzme bölünmesi için TTD-RIS ve sanal alt dizi RIS mimarilerini, uçtan uca derin
  öğrenmeyle karşılaştırır. Kazanç ile donanım karmaşıklığı arasındaki ödünleşimi inceler.
- Alıntı: *"the tradeoff between the beamforming gain and the hardware complexity is investigated for
  different frequency-dependent RIS architectures"*

**[2.6] C. Qiu, Q. Wu, W. Chen, M. Hua, W. Hao, M. Jian, F. Hou**, "Beamforming Design for Intelligent
Reflecting Surface Aided Near-Field THz Communications," *IEEE Transactions on Vehicular Technology*,
vol. 75, no. 1, pp. 1551–1556, Ocak 2026. DOI: 10.1109/TVT.2025.3593875 · arXiv:2410.08459
- Mevcut gecikme tabanlı IRS şemalarının sınırsız gecikme aralığı varsaydığını eleştirir ve gerekli
  gecikme aralığını küçülten çift katmanlı delta-gecikme (DLDD) şeması önerir.
- Alıntı: *"While delay-based IRS has emerged as a potential solution, current beamforming schemes
  generally assume unbounded range time delays (TDs)."*

**[2.7] K. Dovelos, S. D. Assimonis, H. Q. Ngo, B. Bellalta, M. Matthaiou**, "Intelligent Reflecting
Surfaces at Terahertz Bands: Channel Modeling and Analysis," *2021 IEEE ICC Workshops*, pp. 1–6, 2021.
DOI: 10.1109/ICCWorkshops50388.2021.9473890 · arXiv:2103.15239
- THz'de büyük IRS için küresel dalga modelini kullanır ve uzak alan hüzme oluşturmanın metrelerce
  mesafede bile yetersiz kaldığını gösterir. Squint'e değil, yakın alan modellemesine odaklanır.
- Alıntı: *"as the IRS size grows, the conventional far-field assumption starts becoming invalid and the
  spherical wavefront of the radiated waves should be taken into account."*

---

## 3. Optimizasyon süresi/gecikme ölçümü ve geniş bant RIS'te kanal eskimesi

Bu başlıkta **doğrudan isabet bulunamadı**. Yakın çalışmalar:

**[3.1] B. Matthiesen, E. Björnson, E. De Carvalho, P. Popovski**, "Intelligent Reflecting Surface
Operation Under Predictable Receiver Mobility: A Continuous Time Propagation Model," *IEEE Wireless
Communications Letters*, vol. 10, no. 2, pp. 216–220, Şubat 2021. DOI: 10.1109/LWC.2020.3024781 ·
arXiv:2006.06991
- Hareketli alıcı için sürekli zamanlı çok yollu modelde IRS yapılandırmasını güç, Doppler yayılımı ve
  gecikme yayılımı açısından inceler. Hesaplama gecikmesini modellemez.
- Alıntı: *"We develop a continuous time system model for multipath channels and discuss the optimal IRS
  configuration with respect to received power, Doppler spread, and delay spread."*

**[3.2] Z. Huang, B. Zheng, R. Zhang**, "Transforming Fading Channel From Fast to Slow: Intelligent
Refracting Surface Aided High-Mobility Communication," *IEEE Transactions on Wireless Communications*,
vol. 21, no. 7, pp. 4989–5003, Temmuz 2022. DOI: 10.1109/TWC.2021.3135685 · arXiv:2106.02274
(konferans sürümü: ICC 2021, DOI 10.1109/ICC42927.2021.9500699)
- IRS'i araca monte ederek IRS–kullanıcı kanalını yarı-statik hale getirir ve hızlı sönümlemeyi yavaşa
  çevirir. Hareketlilik sorununu fiziksel yerleşimle çözer, optimizasyon süresiyle ilgilenmez.
- Alıntı: *"a rapidly time-varying channel is typically resulted between the static BS and fast-moving
  IRS/user, which renders the channel estimation for IRS with a large number of elements more challenging."*

**[3.3] T. Song, E. Shi, Y. Lu, Y. Zhu, J. Zhang, B. Ai**, "Performance Analysis of RIS-Aided MISO
Systems with EMI and Channel Aging," *2024 IEEE VTC2024-Spring*, pp. 1–5, 2024.
DOI: 10.1109/VTC2024-Spring62846.2024.10683661 · arXiv:2405.09200
- Dar bantlı RIS-MISO'da kanal eskimesi ve EMI altında kapalı form spektral verim türetir. Geniş bant
  ya da optimizer süresi yoktur.
- Alıntı: *"RIS can be deployed to compensate for SE degradation caused by channel aging effects."*

**[3.4]** (Ranjan vd. 2023, [1.6]): Hızlı güncellemeyi gerekçe olarak koyan tek IRS-OFDM optimizer
çalışmasıdır. Ancak özetten anlaşıldığı kadarıyla hızı gecikme bütçesine ya da kanal eskimesine bağlamaz.

**Bulunamayanlar (sorgulandı, isabet yok):** arXiv'de `"running time" AND IRS AND OFDM`,
`outdated AND IRS AND OFDM` ve `wideband AND RIS AND "channel aging"` sorguları **sıfır sonuç** döndü.
Crossref'te "channel aging reconfigurable intelligent surface OFDM mobility" sorgusu ilgisiz sonuçlar
döndürdü.

---

## 4. RIS faz tasarımı için derin açılım (deep unfolding): alan ne kadar kalabalık?

**[4.1] Q. Hu, Y. Cai, Q. Shi, K. Xu, G. Yu, Z. Ding**, "Iterative Algorithm Induced Deep-Unfolding
Neural Networks: Precoding Design for Multiuser MIMO Systems," *IEEE Transactions on Wireless
Communications*, vol. 20, no. 2, pp. 1394–1410, Şubat 2021. DOI: 10.1109/TWC.2020.3033334 · arXiv:2006.08099
- RIS değil, ama alanın temel referansıdır. WMMSE'yi katmanlara açar ve motivasyonunu açıkça gerçek
  zaman sistemleri olarak koyar.
- Alıntı: *"they generally require considerable computational complexity, which gets in the way of their
  practical application in real-time systems."*

**[4.2] Y. Liu, Q. Hu, Y. Cai, G. Yu, G. Y. Li**, "Deep-Unfolding Beamforming for Intelligent Reflecting
Surface Assisted Full-Duplex Systems," *IEEE Transactions on Wireless Communications*, vol. 21, no. 7,
pp. 4784–4800, Temmuz 2022. DOI: 10.1109/TWC.2021.3133296 · arXiv:2112.02305
- IRS destekli FD-MIMO'da SSCA algoritmasını açar ve matris tersini öğrenilen parametrelerle yaklaşıklar.
  Karışık zaman ölçeklidir: IRS fazı istatistikle, aktif hüzme anlık CSI ile güncellenir.
- Alıntı: *"due to the high computational complexity caused by the matrix inversion computation in the
  SSCA-based optimization algorithm, we further develop a deep-unfolding neural network (NN) to address
  this issue."*

**[4.3] O. Lavi, N. Shlezinger**, "Learn to Rapidly and Robustly Optimize Hybrid Precoding," *IEEE
Transactions on Communications*, vol. 71, no. 10, pp. 5814–5830, Ekim 2023. DOI: 10.1109/TCOMM.2023.3292472
· arXiv:2301.00369 (öncülü: O. Agiv, N. Shlezinger, SPAWC 2022, DOI 10.1109/SPAWC51304.2022.9833923)
- RIS değil, hibrit ön kodlama. Ama yöntem tezdeki "açılmış PGD + öğrenilen adım" ile **neredeyse
  aynıdır**: iterasyona bağlı adım boyları öğrenilir ve hızlı değişen kanal açıkça motivasyon olarak
  konur. Kazanımı iterasyon sayısı ekseninde raporlar.
- Alıntı: *"We leverage data to learn iteration-dependent hyperparameter settings of projected gradient
  sum-rate optimization with a predefined number of iterations."* / *"our approach allows using over ten
  times less iterations compared to that required by conventional optimization with shared
  hyperparameters"*
- Tez için önemi: Buradaki taban çizgisi "paylaşılan hiperparametreli" PGD'dir. Tezin CLAUDE.md'deki
  "zayıf taban çizgisi" uyarısı (her bütçede klasik kolun en iyi ayarını taramak) tam olarak bu
  karşılaştırmayı hedef alır. Lavi & Shlezinger klasik kolun adımını iterasyon bütçesine göre ayarlayıp
  ayarlamadığı tam metinden kontrol edilmeli (**doğrulanmadı**).

**[4.4] I. R. Koralege, A. S. de Sena, N. H. Mahmood, F. Karim, D. Lesthuruge, S. Gunarathne**, "A
Deep-Unfolding Approach to RIS Phase Shift Optimization Via Transformer-Based Channel Prediction,"
*Linköping Electronic Conference Proceedings*, vol. 211, 2025. DOI: 10.3384/ecp212.060 · arXiv:2502.18280
- Transformer ile RIS kanalını öngörür, öngörülen kanalla fazı optimize eder. Kanal eskimesi ile RIS faz
  tasarımını birleştirir ama dar bantlıdır ve özet gecikme ölçümünden söz etmez.
- Alıntı: *"The predicted channel coefficients are then used to optimize the RIS phase shifts."*

**[4.5] T. Shaked, P. del Hougne, G. C. Alexandropoulos, N. Shlezinger**, "AI-Aided Annealed Langevin
Dynamics for Rapid Optimization of Programmable Channels," *2025 IEEE SPAWC*, pp. 1–5, 2025.
DOI: 10.1109/SPAWC66079.2025.11143453 · arXiv:2510.18978
- RIS'te kullanıcılar hareket ettikçe yeniden ayarlama motivasyonuyla açılmış Langevin dinamiği önerir.
  "Sınırlı gecikme" iddiası özette var, ama ölçülmüş bir gecikme bütçesine karşı hız eğrisi olup olmadığı
  doğrulanmadı.
- Alıntı: *"re-tuning the parameters each time the users move"* / *"enables rapid and reliable channel
  parameter tuning with limited latency."*

**[4.6] P. Mobaraki, A. Zakeri, M. Di Renzo, M. Juntti, N. T. Nguyen**, "Energy Efficiency Maximization
for Hybrid RIS-Aided Communications via Deep Unfolding," arXiv:2607.04889, 2026. **Hakemli yayın
olarak Crossref'te bulunamadı, yalnızca arXiv ön baskısıdır.** Aynı grubun önceki çalışması Crossref'te
doğrulandı: P. Mobaraki, N. T. Nguyen, M. Juntti, "Deep Unfolding-Empowered Energy Efficiency Optimization
in RIS-Assisted Wireless Communications," *Proc. 14th Int. Conf. Internet of Things (ACM)*, pp. 238–243,
2024, DOI 10.1145/3703790.3703830 (özeti okunmadı).
- Hibrit RIS'te RIS alt problemini derin açılımla çözer ve daha hızlı yakınsama bildirir.
- Alıntı: *"Numerical results show that the proposed method achieves faster convergence and higher EE
  than the considered benchmark schemes."*

**Kalabalık değerlendirmesi:** "Açılmış iteratif algoritma + öğrenilen parametre" RIS/MIMO'da **kalabalık
ve olgun** bir alan (2020'den beri TWC/TCOM düzeyinde düzenli yayın var). Tezin yapay zekâ ekseninin
olumsuz sonucu (adım başına kazanç, milisaniye başına kayıp) bu literatüre karşı **ayırt edici** olabilir.
Çünkü taranan özetlerin hiçbiri kazancı **ölçülmüş duvar saati** ile **ayarı taranmış** klasik taban
çizgisine karşı raporlamıyor. Ancak bu yalnızca özetlere dayanıyor; tam metinlerde süre tabloları olabilir.

---

## 5. Uygulanabilirlik için: STAR-RIS ISAC (hareketli hedef) ve FPGA/gerçek zaman RIS denetleyicileri

### 5a. STAR-RIS ISAC, hareketli hedef

**[5.1] M. Li, S. Zhang, Y. Ge, Z. Li, F. Gao, P. Fan**, "STAR-RIS Aided Integrated Sensing and
Communication Over High Mobility Scenario," *IEEE Transactions on Communications*, vol. 72, no. 8,
pp. 4788–4802, Ağustos 2024. DOI: 10.1109/TCOMM.2024.3381725 · arXiv:2403.11452
- Araca monte STAR-RIS ile araç içi kullanıcıya hizmet verirken aynı anda yol kenarı birimleriyle aracın
  konum ve hızını kestirir. Zaman-frekans seçici kanal modeli kullanır.
- Alıntı: *"the vehicle localization and its velocity measurement can be acquired by jointly utilizing
  these extracted cascaded channel parameters of all RSUs."*

**[5.2] M. Li, S. Zhang, Y. Ge, C. Yuen**, "STAR-RIS Aided Dynamic Scatterers Tracking for Integrated
Sensing and Communications," *IEEE Transactions on Vehicular Technology*, vol. 74, no. 5, pp. 7760–7773,
Mayıs 2025. DOI: 10.1109/TVT.2025.3527753 · arXiv:2501.03793
- Dış ortamdaki dinamik saçıcıları GM-PHD filtresiyle izler ve izlenen konumlarla STAR-RIS kırılma
  fazını **öngörür**. Tezde plan dışı bırakılan "öngörücü faz tasarımı"nın STAR-RIS'teki örneğidir.
- Alıntı: *"With the tracked locations of the outdoor scatterers, a beam prediction strategy for both the
  precoder of BS and the refraction phase shift vector of STAR-RIS is developed"*

**[5.3] H. Taremizadeh, E. Grossi, L. Venturino**, "STAR-RIS Transceivers: Integrated Sensing and
Communication with Pulsed Signals," *2025 EUSIPCO*, pp. 2262–2266, 2025.
DOI: 10.23919/EUSIPCO63237.2025.11226036 · arXiv:2507.02346 (uzun sürüm: OJ-COMS vol. 6, pp. 9569–9586,
2025, DOI 10.1109/OJCOMS.2025.3632145, özeti okunmadı)
- STAR-RIS'te uzay ve zaman modülasyonuyla iki yarı uzayda hareketli hedefleri algılarken mesaj gömer.
- Alıntı: *"a time modulation to distinguish the corresponding echoes from prospective moving targets and
  embed communication messages."*

Değerlendirme: STAR-RIS ISAC + hareketlilik aktif bir alan (2024–2025'te TCOM/TVT). Ama 20 Kasım ölçüm
kapanışına göre yeni bir eksen açmak **uygulanabilir görünmüyor**. Ancak gelecek çalışma olarak anılabilir.

### 5b. FPGA / gerçek zaman RIS denetleyicileri

**[5.4] X. Pei, H. Yin, L. Tan, L. Cao, Z. Li, K. Wang, K. Zhang, E. Björnson**, "RIS-Aided Wireless
Communications: Prototyping, Adaptive Beamforming, and Indoor/Outdoor Field Trials," *IEEE Transactions on
Communications*, vol. 69, no. 12, pp. 8627–8640, Aralık 2021. DOI: 10.1109/TCOMM.2021.3116151 ·
arXiv:2103.00534
- 5.8 GHz'de 1100 elemanlı prototip kurar ve RIS'i alıcı geri beslemesiyle havadan yapılandırır.
  Gerçek donanımda yapılandırma döngüsünün varlığını gösterir.
- Alıntı: *"we describe a new RIS prototype consisting of 1100 controllable elements working at 5.8 GHz
  band."*

**[5.5] M. Rossanese, P. Mursia, A. Garcia-Saavedra, V. Sciancalepore, A. Asadi, X. Costa-Perez**,
"Designing, building, and characterizing RF switch-based reconfigurable intelligent surfaces," *Proc. 16th
ACM WiNTECH Workshop*, pp. 69–76, 2022. DOI: 10.1145/3556564.3558236 · arXiv:2207.07121
- RF anahtar ve gecikme hattı tabanlı RIS'i PCB ile üretip karakterize eder ve veri setini yayımlar.
- Alıntı: *"Our RIS design comprises arrays of patch antennas, delay lines and programmable
  radio-frequency (RF) switches that enable passive 3D beamforming"*

**[5.6] J. Wang, W. Tang, J. C. Liang, L. Zhang, J. Y. Dai, X. Li, S. Jin, Q. Cheng, T. J. Cui**,
"Reconfigurable Intelligent Surface: Power Consumption Modeling and Practical Measurement Validation,"
*IEEE Transactions on Communications*, vol. 72, no. 9, pp. 5720–5734, Eylül 2024.
DOI: 10.1109/TCOMM.2024.3382332 · arXiv:2211.00323
- RIS donanımını FPGA kontrol kartı, sürücü devreler ve birim hücreler olarak ayırır ve beş farklı RIS
  üzerinde güç modelini doğrular. Denetleyicinin FPGA olduğu standart mimariyi belgeler.
- Alıntı: *"The RIS hardware is divided into three basic parts: the FPGA control board, the drive
  circuits, and the RIS unit cells."*

Değerlendirme: Taranan prototip makaleleri yapılandırma **süresini** (faz yükleme gecikmesi) özette
raporlamıyor. Tezde "donanımın faz uygulama gecikmesi" bir terim olarak kullanılacaksa sayısal bir
kaynak bulmak için tam metin taraması gerekir (**açık**).

---

## Doğrulanamadı / kapsam dışı bırakılanlar

- **"Cai et al." beam squint/THz hiyerarşik kod kitabı makalesi:** Crossref'te bu tanıma uyan bir Cai
  makalesi bulunamadı. Bulunan Cai, [1.5]'tir (pratik model, squint değil). Görevdeki referans başka bir
  makaleyi kastediyorsa doğrulanamadı.
- **"Delay-adaptation RIS" adlı belirli bir makale:** Bu adla bulunamadı. Aynı fikri [2.3], [2.4] ve
  [2.6] karşılıyor.
- **Yang vd. [1.2] ve Zheng & Zhang [1.1]'de "tek faz vektörü tüm alt taşıyıcılar için" kısıtı:** Özetler
  bunu **açıkça söylemiyor**. Kısıt problemin yapısından gelir ve tam metinde vardır (bilinen model), ama
  burada özetten doğrulanmadı. Bunu açıkça söyleyen özet [2.1]'dir. Tezde atıf için [2.1] alıntısı
  güvenlidir.
- Geniş bant RIS'te kanal eskimesini optimizer süresiyle birlikte modelleyen makale **bulunamadı**.
- Wanming Hao vd. "Beam-Division Multiple Access ..." ve W. Jiang'ın TechRxiv ön baskıları: hakemli
  değil, kapsam dışı bırakıldı.

---

## Boşluk (gap)

**Soru:** Geniş bant RIS faz optimizasyon yöntemlerini hareketlilik altında **ölçülmüş gecikmede etkin
hız** ya da **en uygun iterasyon sayısı** ile değerlendiren yayımlanmış çalışma var mı?

**Bulgu (bu taramanın sınırları içinde): doğrudan bu kesişimde bir çalışma bulunamadı.** Literatür dört
ayrı kümede kalıyor ve kümeler birbirine değmiyor:

1. **Geniş bant/OFDM RIS faz tasarımı** ([1.1]–[1.6], [2.1]–[2.6]) hızı statik kanalda raporluyor.
   Karmaşıklık en fazla asimptotik (O-notasyonu) ya da yakınsama eğrisi olarak veriliyor. [1.6] "hızlı
   güncelleme gerekli" diyor ama bunu bir gecikme bütçesine bağladığı özette görünmüyor.
2. **Hareketlilik** ([3.1], [3.2], [5.1]) Doppler'i fiziksel yerleşim, protokol ya da kestirim
   düzeyinde ele alıyor. Hesaplama süresinin CSI'ı eskittiği bir model yok.
3. **Kanal eskimesi** ([3.3], [4.4]) dar bantlı ve analitik ya da öngörü tabanlı. Optimizer'ın kendi
   süresi eskimeye katkı olarak modellenmiyor.
4. **Derin açılım** ([4.1]–[4.6]) motivasyonu açıkça "gerçek zaman/hızlı değişen kanal" olarak koyuyor.
   Ama kazancı **iterasyon/katman sayısı** ekseninde raporluyor ([4.3]: "ten times less iterations"). Tezin
   ölçtüğü gibi bir öğrenilen adımın birden fazla klasik adım ettiği ve kazancın milisaniye ekseninde
   tersine döndüğü bir sonuç, taranan özetlerde yok.

**Tezin olası katkısı:** "Gecikme bütçesi → en uygun iterasyon sayısı → eskimiş CSI ile etkin hız"
zincirini **geniş bantta (tek faz vektörü, çok alt taşıyıcı)**, **hareketli kullanıcıyla** ve **ölçülmüş
duvar saatiyle** kuran ve klasik kolun ayarını her bütçede tarayan bir değerlendirme, taranan literatürde
karşılığı olmayan bir kesişim gibi görünüyor.

**Belirsizlik, açıkça:**
- Tarama yalnızca Crossref başlık eşleşmesi ve arXiv özet aramasıyla yapıldı. IEEE Xplore tam metni,
  Google Scholar ve ileri/geri atıf zinciri **taranmadı**. Özellikle şu tür çalışmalar kaçmış olabilir:
  "age of CSI" / "AoI" + RIS, "anytime algorithm" + beamforming, "computation-aware" / "processing delay"
  + IRS, ve araçsal (V2X) RIS makaleleri.
- Gecikme tartışması dar bantlı RIS ya da klasik MIMO ön kodlaması için var olabilir (ör. açılım
  literatüründe tam metin içi süre tabloları). Bu, kesişimin "boş" değil yalnızca "geniş bant + hareketlilik
  + ölçülmüş gecikme" üçlüsünde boş olduğu anlamına gelir.
- Savunmadan önce önerilen kontrol: [1.6], [4.3] ve [4.5]'in tam metninde (a) duvar saati ölçümü,
  (b) klasik kolun bütçeye göre ayarlanıp ayarlanmadığı, (c) hareketlilik ya da eskime modeli olup olmadığı
  okunmalı. Bu üçü, tezin "ilk biz" iddiasını en çok zorlayabilecek adaylardır.
- Önerilen ifade: "bilgimiz dahilinde" kalıbı, "ilk" iddiasından daha güvenlidir.
