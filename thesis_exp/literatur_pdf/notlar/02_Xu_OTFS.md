# 02 — Xu vd., OTFS destekli RIS'li SAGIN (IEEE IoT-J 2023)

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/02_Xu_OTFS_SAGIN.pdf` (22 sayfa, tamamı okundu).
Sayfa atıfları **dergi sayfa numarasıdır** (PDF s. 1 = dergi s. 682; PDF sayfası = dergi sayfası − 681).
Şekillerden yapılan okumalar "şekilden okuma" diye işaretlidir; kesin sayısal tablo değildir.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Chao Xu (Senior Member, IEEE), Luping Xiang (Member, IEEE), Jiancheng An (Member, IEEE), Chen Dong, Shinya Sugiura (Senior Member, IEEE), Robert G. Maunder (Senior Member, IEEE), Lie-Liang Yang (Fellow, IEEE), Lajos Hanzo (Life Fellow, IEEE) (s. 682)
- **Başlık:** "OTFS-Aided RIS-Assisted SAGIN Systems Outperform Their OFDM Counterparts in Doubly Selective High-Doppler Scenarios" (s. 682)
- **Dergi:** IEEE Internet of Things Journal, Vol. 10, No. 1, 1 January 2023 (sayfa başlığı, s. 682)
- **Sayfalar:** 682–703 (ilk ve son sayfa başlıkları)
- **DOI:** 10.1109/JIOT.2022.3203895 (s. 682 dipnot: "Digital Object Identifier")
- **Durum:** "Manuscript received 31 July 2022; accepted 29 August 2022. Date of publication 1 September 2022; date of current version 22 December 2022." (s. 682 dipnot). Cilt/sayı/sayfa atanmış nihai sürüm; "early access" ibaresi YOK.
- Sorumlu yazar: Chen Dong (s. 682 dipnot).
- ISSN satırı: "2327-4662 © 2022 IEEE" (s. 682 alt bilgi).

## 2. Problem ve katkılar

- **Problem:** Uzay–hava–yer entegre ağlarda (SAGIN) yüksek Doppler, OFDM'de TD'de ISI ve FD'de ICI'ye, dolayısıyla hata tabanına yol açıyor; zamanla değişen TF-alanı kanallarında RIS yapılandırmak ve interpolasyon tabanlı TF-alanı kanal kestirimi yapmak pratik değil (Özet, s. 682; s. 684 "1)–3)" maddeleri).
- **Katkı 1 — Sistem modeli:** RIS destekli SAGIN'in çift seçici sönümlemeli kanalı hem TD hem DD alanında modelleniyor; OFDM ve OTFS tek platformda (s. 684, katkı 1; Bölüm II, denk. (1)–(17)). Yazarlar bunun literatürde ilk olduğunu belirtiyor (Özet, s. 682).
- **Katkı 2 — RIS yapılandırması:** Zamanla değişen RIS fazları, zamanla değişmeyen faz parametresi α̃ʳ ve "sanal Doppler" indisi k^RISʳ ile temsil ediliyor; RIS fazı Doppler'e uğramasa da faz değişimini bu sanal Doppler yönlendiriyor; istatistiksel CSI'ya (LoS) dayanıyor, RIS'te CSI kestirimi gerekmiyor (s. 685 katkı 2; denk. (22), (27), s. 689).
- **Katkı 3 — Kanal kestirimi:** OFDM ve OTFS'nin ikisinin de kullanabileceği, TF-alanı interpolasyonunu ortadan kaldıran DD-alanı RIS kanal kestirimi (s. 685 katkı 3; Bölüm IV-D, denk. (51)–(53), s. 694).
- **İddia:** OTFS tabanlı RIS'li SAGIN, BER, ulaşılabilir hız ve kapsama mesafesi bakımından OFDM karşılıklarını geçiyor; Ricean K, Doppler, gecikme yayılımı, kapsama mesafesi ve taşıyıcı frekans geniş aralığında (Özet, s. 682; s. 685 katkı 3c).

## 3. Sistem modeli

| Parametre | PDF'teki değer | Atıf |
|---|---|---|
| Dalga biçimi | OTFS (PS-OFDM tabanlı bi-ortogonal darbe; OFDM tabanlı dikdörtgen darbe, sembol-CP ve çerçeve-CP) ve OFDM | Şek. 4, s. 691; Bölüm IV-A/B, s. 691–692 |
| Alt taşıyıcı sayısı M, sembol sayısı N | M = 64, N = 32 (OFDM ve OTFS için) | Bölüm V-A, s. 694 |
| Alt taşıyıcı aralığı | SCS = 2^μ × 15 kHz (5G ölçeklenebilir numeroloji). Senaryo başına (Şek. 1): V2V FR1 15 kHz / FR2 60 kHz; Tren 15 / 120 kHz; Sivil havacılık 30 / 240 kHz; Süpersonik İHA 60 / 960 kHz; Hipersonik İHA 240 / 3840 kHz; LEO 480 / 7680 kHz | s. 694; Şek. 1, s. 685 |
| Bant genişliği | Açıkça Hz cinsinden verilmiyor (yalnızca MΔf ifadesi; verim = C_eff·MΔf bit/s) → **YOK** (sayısal değer) | s. 697 |
| Taşıyıcı frekans | UHF 0.8 GHz, L 1.5 GHz, S 2.6 GHz, C 4.7 GHz (FR1); K 26 GHz, Ka 28.5 GHz (FR2). Ana sonuçlar S-bant 2.6 GHz. Ayrıca örnek: Ka-bant f_c = 38.5 GHz (N = 3, M = 3 oyuncak örnek) | s. 694; Şek. 12, s. 698; s. 693 |
| BS anten sayısı | Kaynakta ve hedefte **tek anten** ("a single antenna is used both at the source and at the destination") | s. 686, Bölüm II-A |
| RIS eleman sayısı | R = R_y R_z, UPA, d = λ/2 (denk. (10)). Simülasyonlarda R = 4 (Şek. 8–13); Şek. 3(c)(d) 2–64; Şek. 14(a) R = 4, 16, 64; Şek. 14(b)(c) R = 64 ve 256; Şek. 14(d) R = 256 | s. 687–688; s. 690, 695–699 |
| Kullanıcı sayısı | Tek kullanıcı (tek kaynak–hedef bağlantısı); çok kullanıcı **YOK** | Bölüm II |
| Hız | V2V 100 mph; Tren 336 mph; Sivil havacılık 671 mph; Süpersonik İHA Mach 3; Hipersonik İHA Mach 12; LEO Mach 25 (Şek. 1). Tren hızı taraması 200 / 400 / 600 mph (Şek. 8, 11a, 13a); Şek. 13(e) hız 200–2600 mph ekseni. Oyuncak örnek 540 km/h | s. 685; s. 695–698; s. 693 |
| Doppler | f_D^i = v^i f_c / c (s. 687). Şek. 8: f_D^SD = f_D^SR = 778 Hz (200 mph), 1556 Hz (400 mph), 2334 Hz (600 mph), f_D^RD = 0 Hz (RIS trene monte, Şek. 7a). Şek. 10: f_D^SD = 8894 Hz (süpersonik İHA). Oyuncak örnek: ϑ_max = 19.25 kHz | Şek. 8 efsaneleri, s. 695; s. 696 metin ve Şek. 10, s. 697; s. 693 |
| Kanal modeli | Ricean TDL; LoS yolu l = 0'da, NLoS yollar [0, L^i−1] gecikme indisinde rastgele; Doppler indisleri [−k_max, k_max]'de rastgele, k_max = ⌈f_D N T⌉, L = ⌈τ_max M Δf⌉; NLoS kazanç varyansı 1/[(K+1)(P−1)]. Yol kaybı denk. (4), Tablo IV. Tam sayı (on-grid) gecikme/Doppler varsayımı | s. 687–688, denk. (4)–(13); Tablo IV, s. 687 |
| Ricean K (Şek. 1) | V2V: K^SD = −3, K^SR = −3, K^RD = 3 dB; Tren: −3/−3/3 dB; Sivil havacılık: 3/3/6 dB; Süpersonik İHA: −3/−3/6 dB; Hipersonik İHA: −3/−3/6 dB; LEO: 2/2/6 dB | Şek. 1, s. 685 |
| Gecikme yayılımı τ_max (Şek. 1, FR1 / FR2) | V2V 4000/800 ns; Tren 4000/800 ns; Sivil havacılık 600/250 ns; Süpersonik İHA 600/250 ns; Hipersonik İHA 400/120 ns; LEO 100/40 ns. Şek. 8, 10, 13a: τ_max = 4 μs | Şek. 1, s. 685; s. 695–698 |
| Mesafe (Şek. 1) | V2V 300 m; Tren 500 m; Sivil havacılık 10 km; Süpersonik/Hipersonik İHA 20 km; LEO 2000 km | Şek. 1, s. 685 |
| Yol sayısı | Şek. 3 (a)(c) S-bant P^i = 2L^i; (b)(d) K-bant P^i = 0.6L^i | Şek. 3, s. 690 |
| Yol kaybı parametreleri | Tablo V: Car (300,1,1), A_e^BS 80 cm², A_e^user 40 cm², γ^SD 3.64; Train (500,−2,1), 80 cm², 40 cm², 3.51; Airplane (200,100,10000), 16 dm², 1.6 dm², 3.02; Supersonic UAV (2000,1000,20000), 16 dm², 1.6 dm², 2.95; Hypersonic UAV (20000,10000,20000), 16 dm², 1.6 dm², 2.91; LEO (100000,10000,2000000), 60 cm yarıçap, 60 cm yarıçap, 2.65. γ^SRD = 2.0; RIS kullanıcıdan 1 m uzakta (x_R = x_D − 1) | Tablo V, s. 695; s. 694–695 |
| **RIS fazı alt taşıyıcıya göre** | **Ortak.** "the same phase rotation of each RIS element will be applied to all the channel impulse response (CIR) taps in the TD or equivalently to the channel frequency response (CFR) of all SCs in the FD. In other words, the RIS phase rotations can be time varying but remain strictly nonfrequency-selective." | s. 687; ayrıca s. 688 Bölüm III-A |
| RIS fazının zamana bağlılığı | Zamanla değişir: α_{n,m}^r = α̃ʳ ω_{MN}^{k^RISʳ(nM+m)} (denk. (22)); her örnek anında yeni faz (sanal Doppler'li doğrusal faz rampası) | s. 689 |

## 4. Yöntem

- **Optimize edilen:** RIS yansıma katsayıları.
  - TF-alanı genel problem: max Σ_l |h_{n,m,l}|² = max Σ_m |h̄_{n,m}|², |α| = 1 (denk. (18), s. 688). Dışbükey değil; SCA ile alt-optimal çözülebilir ama anlık tam CSI geri beslemesi gerektirir (s. 689).
  - Benimsenen düşük karmaşıklıklı çözüm: baskın LoS dokunuşunun gücünü maksimize et (denk. (19)–(20)), kapalı form faz hizalama (denk. (21), s. 689). İstatistiksel CSI'ya (LoS) dayanır.
  - DD-alanı: iki zamanla değişmeyen parametre — k^RISʳ = k_0^SD − k_0^SRʳ − k_0^RDʳ, ∠α̃ʳ = ∠h̃_0^SD − ∠h̃_0^SRʳ h̃_0^RDʳ (denk. (27), s. 689).
  - **İterasyon sayısı:** Benimsenen RIS yapılandırması kapalı formdur; iteratif algoritma ve iterasyon sayısı **YOK**.
- **Kestirilen:** Bileşik (doğrudan + RIS-yansımalı) DD-alanı kanal matrisi H̃ (sinyal tespiti için tam CSI); RIS yapılandırması için kanal kestirimi yapılmaz, LoS istatistiği (PL, AoA/AoD, hız) GPS'ten varsayılır (s. 690, Bölüm III-C).
- **Kanal kestirim yöntemleri (karşılaştırılan):**
  - FD interpolasyon (MMSE, "yatay tarak" + "dikey tarak"): pilot aralığı N_PS^FD ≤ M/L, en az N_p^FD = M/N_PS^FD ≥ L pilot (denk. (48), s. 693). Önceki çalışmaları [58]'den.
  - TD interpolasyon (MMSE): CP'ye Dirac darbe pilotu, koruma aralığı N_guard^TD ≥ L, güç Σ|s_{0,m}|² = 2N_cp^TD + 1 (denk. (49)–(50), s. 694).
  - **Önerilen DD-alanı:** DD ızgarasında darbe pilotu, koruma N_guard^DD ≥ P (denk. (51)); κ_p'inci sütun H̃ girişimsiz kestiriliyor (denk. (52)); yol sayısı P eşik T ile belirleniyor, eşik "T = (3/[N0])" olarak basılmış (s. 694); MSE = N0/ρ_p^DD (denk. (53)).
- **Pilot yükü:** DD-alanı için "an entire OTFS frame is dedicated to estimating the substantially increased number of paths in the RIS system" (s. 694). Yani bir tam OTFS çerçevesi (MN = 64×32 kaynak elemanı; çarpım Yorum) pilot için ayrılıyor. Pilot yükünün yüzdesi veya veri çerçevesine oranı **YOK**. FD/TD için yükler yukarıdaki eşitsizliklerle tanımlı; sayısal değerleri [58]'e havale ediliyor (s. 694).
- **Dedektör:** Adil karşılaştırma için hem OFDM hem OTFS'de MMSE dedektörü (s. 693); OFDM için ayrıca tek-dokunuşlu FDE (Şek. 13a).
- Pencere boyu N_w: Şek. 11(b)(c)'de 2–10 taranıyor; Şek. 11(a)'da N_w = 6 (s. 697).

## 5. Karmaşıklık / gecikme

- SCA için: "The SCA obtains a stationary point at the cost of polynomial complexity in terms of M and R." (s. 689). Kesin mertebe (O(·)) **YOK**.
- DD yapılandırmasının geri besleme avantajı: "In contrast, the DD-domain RIS configuration based on (22) only requires the pair of time-invariant DD-domain parameters of {α̃ʳ, k^RISʳ}_{r=1}^R optimized by (27), which substantially reduced the feedback complexity and overhead." (s. 690)
- Kanal kestirimi karmaşıklığı: "the complexities of the FD, TD, and DD-domain channel estimation techniques are compared in Fig. 11(c) in terms of the numbers of real-valued multiplications ... As expected, the FD and TD channel estimation techniques exhibit high complexities that grow with the interpolation window size N_w, while the proposed DD-domain channel estimation technique exhibits the lowest complexity, thanks to the elimination of the TF-domain interpolation." (s. 696). Sayısal değer yalnızca Şek. 11(c) log eksenli çubuk grafikte; şekilden okuma: DD ≈ 10² düzeyinde ve N_w'den bağımsız, FD/TD ≈ 10⁴–10⁵ arası (N_w = 2–10, 600 mph) — kesin sayı **YOK**.
- FLOP sayısı, çalışma süresi (ms), donanım: **YOK**.
- **Kontrol bağlantısı gecikmesi:** "The control information on RIS configuration can be conveyed by a separate link, such as Bluetooth, and the associated time duration has a negligible impact on the data rate compared to the pilot overhead, as assumed in [48], [49], [50], [51], and [52]." (s. 689)
- **Hesaplama sırasında kanal yaşlanması:** Hesaba katılmıyor → **YOK**. RIS fazları LoS istatistiğinden kapalı formda hesaplanıyor ve hesaplama/geri besleme gecikmesi ihmal edilebilir kabul ediliyor (yukarıdaki alıntı). Yaşlanmaya en yakın ifade, TD yapılandırmasının anlık geri besleme gerektirdiği için "impractical in time-varying SAGIN applications" olması (s. 689).

## 6. Ana sayısal sonuçlar

Makalede metin içi sayısal BER/NMSE tablosu yok; sonuçlar şekillerde. Metindeki nitel/sayısal ifadeler:

- **Hızın etkisi (Şek. 8, s. 695; tren, OFDM, f_c = 2.6 GHz, Δf = 15 kHz, M = 64, N = 32, τ_max = 4 μs, R = 4, P^i = 2L^i):** R = 4 ile bile büyük iyileşme; FD kestirimi 200 mph'de hata tabanına düşüyor, 400 ve 600 mph'de kötüleşiyor; TD 200 mph'de iyi, 400 ve 600 mph'de hata tabanı; DD-alanı tüm hızlarda güvenilir.
- **Şek. 9 (s. 696):** İnterpolasyonsuz TF yöntemleri (yalnızca LoS, DFT deseni, ON/OFF deseni) "suffer from error floors even at a modest vehicle speed of 200 mph".
- **SCS etkisi (Şek. 10, s. 696–697; süpersonik İHA, OTFS, f_D^SD = 8894 Hz, f_c = 2.6 GHz, τ_max = 4 μs, R = 4):** RIS'siz mükemmel CSI'da Δf = 15 kHz yeterli; RIS ile Δf = 30 kHz gerekli (Doppler indis aralığı genişliyor); gerçek DD kestiriminde OFDM tabanlı OTFS için 15 kHz yetmiyor çünkü f_D^SD > (1/2)Δf; doğrudan SD bağlantısı kestirimi için 30 kHz, yüksek kaliteli RIS kanal kestirimi için Δf = 60 kHz gerekli. PS-OFDM tabanlı (bi-ortogonal ideal) OTFS bundan etkilenmiyor.
- **NMSE (Şek. 11a–b, s. 696–697; tren):** FD en yüksek NMSE, sonra TD, DD-alanı en düşük. N_w artışı özellikle TD'yi iyileştiriyor; FD ICI nedeniyle bozuk kalıyor. Şekilden okuma: DD ≈ 10⁻⁵ düzeyinde (eksenin alt sınırı) — kesin değer **YOK**.
- **SAGIN senaryoları (Şek. 12, s. 696, 698; S-bant 2.6 GHz, R = 4, DD kestirimi):** DD kestirimi OFDM ve OTFS'de RIS'li/RIS'siz etkili; istatistiksel CSI ile RIS yapılandırması hem yalnız SD hem rastgele RIS'e göre belirgin üstün; rastgele RIS genişleyen Doppler aralığı nedeniyle hata tabanı yaratıyor; OTFS OFDM'yi geçiyor; Şek. 12(c)(f)'de (daha yüksek Ricean K) OTFS–OFDM farkı küçülüyor.
- **Etkin verim (Şek. 13, s. 697–698; K^SD = K^SR = −6 dB, K^RD = 6 dB, τ_max = 4 μs, 600 mph, QPSK):** C_eff üst sınırı 2 bit/s/Hz (denk. (54)); tek-dokunuşlu FDE'li OFDM RIS'li/RIS'siz kayıp yaşıyor; RIS'li OTFS 2 bit/s/Hz'e RIS'li OFDM'den daha düşük SNR'de ulaşıyor; RIS, Ricean K faktörü −6 dB kadar düşükken bile iyileştiriyor; OTFS her durumda OFDM'yi geçiyor; K^SD = K^SR arttıkça fark küçülüyor. Şek. 13(a) dBm farkları yalnız şekilde, metinde sayı **YOK**.
- **Yol kaybı (Şek. 14, s. 698–699; tren, Şek. 7b sabit RIS, (x_R, y_R, z_R) = (500, 4, 0), (x_D, −2, 0), A_e^BS = 80 cm², A_e^user = 40 cm², γ^SD = 3.8, γ^SR = γ^RD = 2.0, hedef BER = 10⁻⁴):** güç-verim kazancı kullanıcı RIS'e yakınken en büyük; R arttıkça yardım artıyor; γ^SD > 2.2 aralığında kazanç γ^SD ile artıyor (gerçekte γ^SD 2–6 arası olabilir); FR2 K ve Ka bantlarında R = 256 bile kazanç azalıyor; RIS trene monte ise K-bantta kapsama 10 km'ye kadar uzuyor, SD bağlantısı > 40 dBm gerektirdiğinde kapsam dışı sayılıyor.

## 7. Varsayımlar ve sınırlar

- Tek antenli BS ve kullanıcı; çok antenli durumda ON/OFF anten deseni önerilir ama pilot yükü anten sayısıyla büyür (s. 686).
- Tam sayı (on-grid) gecikme ve Doppler indisleri; kesirli indis girişimi "sufficient time duration and bandwidth" varsayımıyla ihmal ediliyor (s. 686). Sonuç bölümünde sınırlı bant genişlikli SAGIN kontrol bağlantılarında bu girişim "exceed the scope of this article" (s. 699–700).
- Tüm bileşen Doppler frekansları toplam bant genişliğinden çok küçük: ϑ_p ≪ MΔf (s. 686).
- RIS yapılandırması yalnızca LoS istatistiğine (PL, AoA/AoD, hız) dayanıyor ve BS'nin bunu GPS'ten bildiği varsayılıyor (s. 690). NLoS'u hesaba katmıyor.
- RIS kontrol bağlantısı gecikmesi ihmal edilebilir kabul ediliyor (s. 689); RIS fazının sürekli faz rampası (her örnek anında farklı faz, denk. (22)) ile güncellenebildiği varsayılıyor. Donanım güncelleme hızı tartışması **YOK**.
- Sürekli faz (ayrık faz/bit çözünürlüğü **YOK**); pasif RIS, |α| = 1.
- Küçük RIS (çoğu sonuç R = 4); tek kullanıcı; MMSE dedektörü.
- Yol kaybı parametreleri sabitlenerek diğer etkiler inceleniyor (s. 695).
- Yalnızca simülasyon; ölçüm veya prototip **YOK**.

## 8. Tezle bağlantı

**Doğrudan PDF'e dayanan noktalar:**
- RIS fazı alt taşıyıcılar arasında ortak ("strictly nonfrequency-selective", s. 687) — tezin geniş bantta "tüm alt taşıyıcılar için tek faz vektörü" varsayımıyla aynı.
- Makale RIS kontrol/hesaplama gecikmesini açıkça ihmal ediyor (s. 689 Bluetooth alıntısı) ve hesaplama sırasında kanal yaşlanmasını modellemiyor. Bu, tezin "gecikme birinci sınıf tasarım kısıtıdır" savıyla **çelişen bir varsayım**; tez bu varsayımın neden yetersiz olduğunu gösterebilir.
- TD yapılandırmasının "instantaneous CSI ... impractical in time-varying SAGIN applications" olduğunu söylüyor (s. 689) — tezin CSI'nın hızla eskidiği savını nitel olarak **destekliyor**.

**Yorum (benim çıkarımım):**
- *Ön uç kestirici olarak:* DD-alanı darbe pilotu kestiricisi (denk. (51)–(53)) Doppler indisleri k_p'yi ve dolayısıyla f_D ≈ k_p/(NT) değerini doğrudan veriyor. Bu, gecikme-farkında denetleyicinin ihtiyaç duyduğu "ölçülmüş Doppler" girdisini, x = ΔT·f_d'yi hesaplamak için sağlayabilir. Kısıt: tam sayı Doppler çözünürlüğü 1/(NT) = Δf/N (M = 64, N = 32, Δf = 15 kHz için ≈ 469 Hz; hesap Yorum). Şek. 8'deki 778 Hz'lik f_D bu çözünürlüğün yalnızca ~1.7 katı, yani tezin düşük-x rejimini çözmek için kaba kalabilir.
- *Optimizer / taban çizgisi olarak:* Kapalı form LoS faz hizalaması (denk. (21)) ve sanal-Doppler faz rampası (denk. (22), (27)) hesaplama maliyeti neredeyse sıfır olan bir **klasik taban çizgisi**. Tezin etkin-hız çerçevesinde "sıfır-gecikmeli ama yalnız LoS'a dayanan" bir kol olarak denenebilir. Sanal Doppler rampası aslında **öngörücü bir faz tasarımı** (faz zamanla doğrusal döner); CLAUDE.md'de öngörücü faz tasarımı "plan dışı" olduğu için bu yalnızca gelecek çalışma atfı olarak kullanılmalı, yeni deney açılmamalı.
- *Ön kayıtlı doğrulama senaryosu için yeniden kullanılabilir parametreler:* Şek. 1 tablosu (hız, mesafe, Ricean K, τ_max, Δf; FR1/FR2), Tablo V (konumlar, açıklıklar, PLE), Bölüm V-A (M = 64, N = 32, f_c = 2.6 GHz S-bant), Şek. 8 (200/400/600 mph → 778/1556/2334 Hz). Tren senaryosu (336 mph, 500 m, τ_max 4000 ns FR1) dış bir kaynaktan alınmış hareketlilik noktası olarak sabitlenebilir. Not: Bu parametreler tek antenli BS ve R = 4 içindir; tezin çok antenli/çok elemanlı kurulumuna aktarırken değişiklik açıkça belgelenmeli.
- *Tezle gerilim:* Makale, M = 64 alt taşıyıcının tümü için tek, kapalı formlu bir faz kullanıyor ve K_opt alt taşıyıcı alt kümesi ya da adım sayısı gibi bir ödünleşim tartışmıyor; tezin denetleyicisinin seçtiği değişkenlerin (yöntem, adım sayısı, alt taşıyıcı alt kümesi, güncelleme periyodu) hiçbiri burada yok. Karmaşıklık yalnızca kestirim için (gerçel çarpma sayısı, Şek. 11c) veriliyor; milisaniye düzeyinde gecikme yok, bu yüzden tezin ölçülmüş adım maliyetiyle doğrudan karşılaştırılamaz.
- *Tezi destekleyen dolaylı nokta:* Şek. 10'da Δf seçiminin f_D'ye göre (f_D^SD > Δf/2 olunca 15 kHz yetmiyor) belirlenmesi, tasarım parametresinin ölçülmüş Doppler'e göre seçilmesi gerektiği fikriyle uyumlu. Bu tezin "ölçülmüş Doppler'den parametre seçen denetleyici" fikrine nitel bir emsal.
