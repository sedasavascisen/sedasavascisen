# 04 — Li ve ark., Double IRSs Aided Massive MIMO Channel Estimation and SEM for HSR

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/04_Li_DoubleIRS_HSR.pdf` (16 sayfa, tamamı okundu).
Sayfa atıfları dergi sayfa numarasıyla verilir (PDF s.1 = s. 8630, PDF s.16 = s. 8645).
Şekillerden göz kararı değer okunmadı; yalnızca metinde ya da tabloda yazan sayılar alıntılandı.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Tianyou Li (Student Member, IEEE), Huawei Tong (Student Member, IEEE), Youyun Xu (Senior Member, IEEE), Xinzhong Su, Guopeng Qiao (s. 8630)
- **Başlık:** "Double IRSs Aided Massive MIMO Channel Estimation and Spectrum Efficiency Maximization for High-Speed Railway Communications" (s. 8630)
- **Dergi:** IEEE Transactions on Vehicular Technology, Vol. 71, No. 8, August 2022 (s. 8630 üst bilgi)
- **Sayfalar:** 8630–8645 (ilk sayfa 8630, son sayfa 8645)
- **DOI:** 10.1109/TVT.2022.3174420 (s. 8630, dipnot)
- **Tarihler:** Alındı 21 Eylül 2021; revizyonlar 24 Ocak, 11 Mart, 5 Nisan 2022; kabul 29 Nisan 2022; yayın 11 Mayıs 2022; güncel sürüm 15 Ağustos 2022 (s. 8630, dipnot)
- **Sorumlu yazar:** Youyun Xu (s. 8630, dipnot)

**Kontrol:** Verilen "IEEE TVT, vol. 71, no. 8, pp. 8630–8645, Aug. 2022" bilgisiyle **uyumlu**. Uyumsuzluk yok.

---

## 2. Problem ve katkılar

- Doğrudan BS–tren bağlantısının (dağ, tünel, U-şekilli hat vb.) engellendiği HSR senaryosunda biri BS tarafında tepe üstünde (IRS2), diğeri tren çatısında MCR (mobil iletişim rölesi) yanında (IRS1) olan **çift IRS** ile kör noktaları doldurmak (s. 8631, Şekil 1; s. 8632).
- Uplink'te çift IRS'li MIMO için **kanal kestirimi**: büyük zaman ölçekli (yarı-durağan G₂, H₁) ve küçük zaman ölçekli (G₁, H₂, D) iki aşama; PARAFAC'ın üç-doğrusallığıyla 3B tensörü matrise indirgeme; kaskat kanal değil **her bir kanalın ayrı ayrı** kestirimi (s. 8631–8632, katkılar; s. 8633–8635, Bölüm III).
- **Konum destekli Doppler frekans ofseti telafisi** ve **Kalman filtresi tabanlı kanal izleme**/öngörü ile pilot yükünü azaltma (s. 8636–8637, Bölüm III-D, denk. (27)–(34)).
- Downlink'te spektral verim maksimizasyonunu MMSE (WMMSE türü) probleme çevirip **BCD** ile çözme; çift IRS faz problemini iki tek-IRS alt problemine ayırıp **MM** algoritmasıyla çözme; yerel optimuma yakınsama garantisi iddiası (s. 8632, katkılar; s. 8637–8640, Bölüm IV, Algoritma 1).
- Sayısal sonuçlar: MCR gücü arttıkça NMSE düşer; çift IRS, tek IRS ve rastgele faz karşılaştırmalarına göre en yüksek hız kazancı (s. 8632, katkılar; Bölüm V).

---

## 3. Sistem modeli

| Parametre | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı | f_c = 1.9 GHz | s. 8640, Bölüm V |
| Bant genişliği | 10 MHz | s. 8640, Bölüm V |
| Alt taşıyıcı sayısı | **YOK** (OFDM yok; dar bant, blok sönümlü model) | denk. (1)–(4) |
| Dalga biçimi | TDD; dar bant MIMO, pilot matrisi X yarı-üniter (DFT önerilir). OFDM/geniş bant **YOK** | s. 8632, II-A; s. 8635, III-C |
| BS anten sayısı L | Uplink NMSE: L = 16; Şekil 6: L = 36; Şekil 7: L ekseni 10–60; Downlink: L = 16; Şekil 13: L = 20 | s. 8640; s. 8641; s. 8642; s. 8643 |
| MCR anten sayısı N | Uplink: N = 9; Şekil 6–7: N = 36; Downlink: N = 9; Şekil 13: N = 20 | s. 8640; s. 8641; s. 8642; s. 8643 |
| IRS1 (tren çatısı) eleman sayısı M₁ | Uplink: 36; Şekil 6: 10→60; Şekil 7: 36; Şekil 8: 16/25/36; Downlink: 16; Şekil 11: 20→80; Şekil 12: M₁+M₂ = 100; Şekil 13: 10…60 | s. 8640–8643 |
| IRS2 (BS tarafı tepe) eleman sayısı M₂ | Uplink: 16; Şekil 6: 50; Şekil 7: 36; Şekil 8: 16/25/36; Downlink: 16; Şekil 11: 16 sabit; Şekil 13: M₁ = M₂ | s. 8640–8643 |
| Kullanıcı | Tek MCR (N antenli röle; yolcular MCR'ye bağlanır, iki atlamalı mimari, 3GPP). Çok kullanıcı **YOK**; l veri akışı | s. 8632, II-A; denk. (3) |
| Tren hızı | Giriş örneği: 300 km/h (hücre yarıçapı ~500 m, her 12 s'de bir el değiştirme). Şekil 13: 50–150 m/s ekseni; metin 100 m/s eşiğini anıyor | s. 8630; s. 8643, Şekil 13 |
| Doppler değerleri | Sayısal Doppler değeri **YOK**. Yalnızca formül: f_{D,l,n} = (v/λ) cos(θ_{AoA,l,n}) | s. 8636 |
| Kanal modeli | Rician: H = √(β/(β+1)) H_LoS + √(1/(β+1)) H_NLoS, ULA yönlendirme vektörleri (denk. (20)–(21)); zaman evrimi h_{n+1} = ρ T_n h_n + √(1−ρ²) c_{n+1} (denk. (26)); NLoS yolları ihmal edilerek (25). Rician faktörü 6 (uplink ve downlink); Şekil 10'da β = 1…10 | s. 8636–8637; s. 8640; s. 8642 |
| Yol kaybı | PL = PL₀ (d/d₀)^α, PL₀ = −20 dB, d₀ = 1 m, α = 2.2; eleman/anten aralığı d = λ/2 | s. 8640, denk. (62) |
| Geometri (uplink) | BS–IRS2 d₁ = 20 m, IRS2–IRS1 d₂ = 100 m, IRS1–MCR d₃ = 5 m, BS–IRS1 d₄ = 110 m, IRS2–MCR d₅ = 103 m | s. 8640 |
| Geometri (downlink) | d₁ = 60 m, d₂ = 300 m, d₃ = 5 m, d₄ = 330 m, d₅ = 309 m | s. 8641 |
| Doğrudan bağlantı | BS–MCR doğrudan yolu engellenmiş varsayılır | s. 8632, II-A |
| IRS fazı | Sürekli faz θ ∈ [0, 2π), genlik β ∈ [0,1] (optimizasyonda β* = 1). Alt taşıyıcı olmadığı için "ortak / alt taşıyıcı başına" ayrımı **YOK** (tek dar bant faz vektörü). Ayrık faz **YOK** | s. 8633, denk. (4a)–(4d); s. 8637, Bölüm IV |
| Hedef fonksiyon | max ((1 − T_t)/T_c) B log₂ det(I_N + (1/σ²) H̄ᵀ F Fᴴ H̄*), T_t: uplink eğitim süresi, T_c: uyumluluk süresi | s. 8633, denk. (4) |

Not: Denk. (4)'teki çarpan PDF'te "(1 − T_t)/T_c" olarak basılmıştır; anlamca (1 − T_t/T_c) olması beklenir, ancak metin olduğu gibi aktarıldı.

---

## 4. Yöntem

**Uplink kanal kestirimi (Bölüm III, s. 8633–8637)**
- İki zaman ölçeği: T_L = α T_s, α ≫ 1; ortalama pilot yükü τ = (T_s/T_L)·τ₁ + τ₂ (s. 8633–8634).
- Büyük zaman ölçeği: yarı-durağan G₂ (BS–IRS2) ve H₁ (MCR–IRS1), [29]'daki çift-bağlantı pilot şemasıyla, tam çift yönlü BS/MCR varsayımı ve koordinat inişi tabanlı iteratif iyileştirme ile (s. 8633).
- Küçük zaman ölçeği: uyumluluk süresi I bloka, her blok T slota ayrılır (Şekil 3, denk. (5)–(6)); IRS2 fazı blok içinde ortak bir Ψ₂ⁱ ile ölçeklenir (s. 8634).
  - **Durum I (L ≥ M₂):** PARAFAC üç-doğrusallığıyla alınan tensör (10a)–(10c), (12) biçiminde ayrıştırılır; LS kestirim Â = (Ξᵀ)† Ȳ (denk. (13)); G₁, H₂, G₂D, D sırasıyla (15a)–(15d). Koşullar: I ≥ 2M₁ + 1, T ≥ N; en az (2M₁ + 1)N pilot (s. 8634–8635).
  - **Durum II (L < M₂):** IRS2'de bir seferde L eleman açılarak ⌈M₂/L⌉ kestirim (s. 8635, denk. (16)).
- Eğitim fazları ve pilotlar: X yarı-üniter (XᴴX = I_N), DFT önerilir; Ξ₁, Ψ₂, Ξ₃ bir I×I DFT matrisinden (satırı kaydırılmış W̃) seçilir, MSE (17)'yi küçültmek için (s. 8635–8636, denk. (17)–(19)).
- **Pilot yükü (s. 8635, Tablo I):**

| Durum | Yük |
|---|---|
| (L ≥ M₂) & (N ≥ M₁) | min((2M₁+1)N, (2M₂+1)N) |
| (L ≥ M₂) & (N < M₁) | min((2M₁+1)N, ⌈M₁/N⌉(2M₂+1)N) |
| (L < M₂) & (N ≥ M₁) | min(⌈M₂/L⌉(2M₁+1)N, (2M₂+1)N) |
| (L < M₂) & (N < M₁) | min(⌈M₂/L⌉(2M₁+1)N, ⌈M₁/N⌉(2M₂+1)N) |

**Doppler telafisi ve izleme (Bölüm III-D, s. 8636–8637)**
- Doppler ofseti yalnızca G₁, H₂, D'de (trenle hareket eden uçlar) var sayılır (s. 8636).
- BS ve IRS2 sabit/bilinen; MCR ve IRS1 konumu CBTC (iletişim tabanlı tren kontrolü) sisteminden alınır → açısal bilgi gerçek zamanlı bilinir; mutlak ve göreli faz kaymaları denk. (27) ile telafi edilir (s. 8637).
- Zaman korelasyonu ρ = (β/(β+1)) exp(−j2π f_D T + j 2πd/λ) (denk. (28)).
- Kalman filtresi: öngörü (29)–(30), düzeltme (31)–(33), bir sonraki uyumluluk süresine öngörü (34).
- n_c parametresi: ilk uyumluluk süresinde tam küçük-ölçek kestirim, sonraki n_c sürede yalnızca (29) ile öngörü, sonra ek pilot çerçeve ile yenileme (s. 8637). Simülasyonda n_c = 5 (s. 8641, Şekil 5).

**Downlink optimizasyon (Bölüm IV, s. 8637–8640, Algoritma 1)**
- Optimize edilenler: ön kodlayıcı F, faz vektörleri θ₁, θ₂ (genlikler 1).
- F: verilen θ'lar için su doldurma, F* = V diag{p₁*,…,p_r*}^{1/2} (denk. (36), s. 8637–8638).
- Hız maksimizasyonu ↔ MMSE eşdeğerliği (denk. (39)): W = E⁻¹ (40), U kapalı form (41).
- θ₁ ve θ₂ dönüşümlü (BCD); her biri MM ile: φ^{t+1} = exp(j arg(−q̃ᵗ)) (denk. (56), (58)).
- Başlatma: N_ini rastgele faz gerçekleşmesinden en yüksek amaçlıyı seçme (Algoritma 1, adım 1–2; s. 8640).
- Yakınsama: iç ve dış döngü için göreli değişim ≤ ε (denk. (60)–(61)); simülasyonda ε = 10⁻⁶ (s. 8641).
- Yineleme sayısı: 100 bağımsız gerçekleşme ortalamasında düşük hata toleransına ulaşmak için toplam yineleme sayısı M₁ = M₂ = 16, 25, 36 için "yaklaşık 10, 20, 40" (s. 8642; Şekil 8). N_ini, T_MM, T_BCD için sayısal değer **YOK**.

---

## 5. Karmaşıklık / gecikme

- Tek karmaşıklık analizi BCD (Algoritma 1) için, M₁ ≤ M₂ varsayımıyla (s. 8640):
  - Alıntı: *"the complexity of computing the decoding matrix U^(n+1) is O(N³)"*; *"the complexity of calculating the auxiliary matrix W^(n+1) is given by O(l³)"*; *"the complexity of MM algorithm is O(M₂³ + T_MM M₂²)"*; F için *"O(max{L³, L²N})"*; toplam *"O(T_BCD max{N³, l³, M₂² + T_MM M₂², L³, L²N})"* (s. 8640).
  - Not: MM terimi adım bazında M₂³ + T_MM M₂², toplam ifadede M₂² + T_MM M₂² olarak basılmış görünüyor; PDF'teki tutarsızlık olduğu gibi aktarıldı.
- Kanal kestirimi (PARAFAC/LS, Kalman) için karmaşıklık mertebesi **YOK**.
- FLOP sayısı **YOK**. Çalışma süresi / ms ölçümü **YOK**. Donanım/platform bilgisi **YOK**.
- Hesaplama gecikmesi sırasında kanal eskimesi: **YOK**. Makale zaman maliyetini yalnızca **pilot (eğitim) süresi** üzerinden hesaba katar: denk. (4)'teki T_t/T_c çarpanı ve Şekil 13 açıklaması — *"With the speed of train increases, the data rates all decrease since the coherence time becomes shorter, which results in the shorter time in downlink data transmission phase."* (s. 8643). BCD/MM'nin çalışma süresi bu zaman bütçesine dahil edilmez; optimize edilen faz, hesaplandığı CSI ile değerlendirilir.
- Kalman izlemesindeki eskime yalnızca uyumluluk-süresi ölçeğinde (n → n+1) ele alınır (denk. (29)–(34)); hesaplama süresi kadar ileriye öngörü **YOK**.
- Şekil 13 için: *"Considering the performance loss due to the error caused by channel tracking, we multiplied a factor on the performance of each curve to equalize the loss over all coherence times."* (s. 8643). Çarpanın değeri **YOK**.

---

## 6. Ana sayısal sonuçlar (yalnızca metindeki sayılar)

- **NMSE vs P_tMCR (Şekil 4, s. 8640–8641):** Ĥ₂ NMSE'si 40 dBm'de 10⁻⁶'ya iner; Ĝ₁ NMSE'si Ĥ₂'den bir mertebe küçük; D̂ NMSE'si P_tMCR = 40 dBm'de 10⁻⁴'e iner; H̄ NMSE'si 10⁻¹⁰'a iner (s. 8641).
- **Kanal izleme (Şekil 5, s. 8641):** n_c = 5; son 5 uyumluluk süresinde izleme hatası büyür, ek pilot çerçeveyle NMSE tekrar düşer. Sayısal hata değeri metinde **YOK**.
- **Pilot yükü (Şekil 6–7, s. 8641):** L = 36, N = 36, M₂ = 50, M₁ = 10→60: M₁ < N iken önerilen şema [21]'den üstün; M₁ > N olunca Tablo I'deki ifade değiştiği için sıçrama. Şekil 7 (M₁ = M₂ = N = 36): L arttıkça önerilen şemanın yükü [21]'dekinden yavaş artar.
- **Yakınsama (Şekil 8, s. 8642):** ~10 / 20 / 40 yineleme (M₁ = M₂ = 16 / 25 / 36), monoton yakınsama.
- **Hız vs P_tBS (Şekil 9, s. 8642):** Kıyas kurulumu P_tBS = 40 dBm, β = 6, L = 16, N = 9, M₁ = M₂ = 16. P_tBS = 0 dBm'de önerilen şema, çift IRS rastgele faz ve tek IRS1 optimal faz "0'a yakın"; 40 dBm'de rastgele fazlı tek IRS1'e göre kazanç "yaklaşık 10 bps/Hz'e kadar". Metin ayrıca rastgele faza göre kazancın "10 bps/Hz'ten 5 bps/Hz'e düştüğünü" yazıyor (bağlam: düşük güç/yüksek kestirim hatası); P_tBS = 0 dBm'de IRS eklemenin anlamlı kazancı yok.
- **Hız vs Rician β (Şekil 10, s. 8642–8643):** P = 40 dBm; β 1→10 iken önerilen şemanın hızı 75 → 48 bps/Hz; çift IRS ile tek IRS arasındaki fark β ile artar.
- **Hız vs M₁ (Şekil 11, s. 8643):** M₂ = 16, β = 6, P_tBS = 40 dBm; M₁ 20→80 iken hız kazancı 13 bps/Hz; kestirilen CSI ile optimal faz, mükemmel CSI üst sınırına göre "ihmal edilebilir" kayıp.
- **Eleman paylaşımı (Şekil 12, s. 8643):** M₁ + M₂ = 100 sabit; en iyi nokta M₁ = 55, M₂ = 45.
- **Hız vs tren hızı (Şekil 13, s. 8643):** L = N = 20; hız arttıkça tüm hızlar düşer; M₁ = M₂ 10 → 20 hızı artırır; M₁ = M₂ = 20 trenin hızına daha duyarlı; 100 m/s'de daha fazla eleman pilot yükünü artırıp performansı düşürür; M₁ = M₂ = 50'de bozulma başlar; M₁ = M₂ = 60 en düşük performans. Sonuç: eleman sayısı "mümkün olduğunca büyük" değil, tren hızına göre seçilmeli (s. 8643–8644, Sonuç).

---

## 7. Varsayımlar ve sınırlar

- BS–MCR doğrudan yolu engellenmiş; kestirim yalnızca yansıma kanalları için (s. 8632).
- Blok sönümlü kanal; uyumluluk süresi içinde sabit (s. 8633, (1)); uplink-downlink karşılıklılığı (TDD) (s. 8633, (3)).
- Büyük ölçekte BS/MCR **tam çift yönlü** (pilot gönderip alabiliyor) varsayımı (s. 8633).
- G₂, H₁ yarı-durağan; büyük-ölçek aşamasında "mükemmel G₂ ve H₁" varsayılarak küçük-ölçek denklemleri türetilir (s. 8635, (14) öncesi).
- Doppler yalnızca hareketli uçları içeren kanallarda; LoS baskın, NLoS ihmal (s. 8636–8637); MCR/IRS1 konumu CBTC'den hatasız biliniyor gibi kullanılıyor (s. 8637).
- IRS fazı sürekli, genlik 1; ayrık faz, donanım kusuru **YOK**.
- Tek kullanıcı (MCR); dar bant; OFDM/geniş bant **YOK**.
- Hesaplama süresi, işlemci, gerçek zamanlı uygulanabilirlik **YOK**; Şekil 13'te izleme kaybı için eğrilere değeri verilmeyen bir çarpan uygulanmış (s. 8643).
- Simülasyonlar: Şekil 8 100 bağımsız gerçekleşme; diğer şekiller için Monte Carlo sayısı ve güven aralığı **YOK**. Tohum/kod paylaşımı **YOK**.
- Geometri küçük ölçekli ve sabit (d₃ = 5 m vb.); trenin konumunun mesafe/açıyı değiştirmesi zaman boyunca simüle edilmiyor (yalnızca Doppler fazı).

---

## 8. Tezle bağlantı

**Gecikme-farkında RIS denetleyicisine bağlanma noktaları**
- *Ön uç kestirici:* İki zaman ölçekli kestirim + konum destekli Doppler telafisi + Kalman öngörüsü (denk. (27)–(34)), denetleyicinin "ölçülmüş Doppler" girdisinin ve eskime öngörüsünün bir kaynağı olabilir. **Yorum:** Denk. (28)'deki ρ, f_D ve T üzerinden tanımlı; tezin x = ΔT·f_d değişkeniyle doğrudan aynı kavramsal ekseni kullanıyor (ΔT ↔ T). Kalman öngörüsünü uyumluluk süresi yerine "ölçülmüş hesaplama gecikmesi" kadar ileriye kurmak, makalede olmayan, tezin katkısıyla uyumlu bir uzantı olur.
- *Optimizatör / taban çizgisi:* BCD + MM (Algoritma 1) klasik kol olarak eklenebilir. **Yorum:** CLAUDE.md'deki zayıf taban çizgisi kuralı gereği, eklenirse T_MM, T_BCD, ε ve N_ini doğrulama kümesinde taranmalı; makalede bu değerlerin çoğu (T_MM, T_BCD, N_ini) **YOK**, yalnızca ε = 10⁻⁶ verilmiş.
- *Karmaşıklık modeli:* O(T_BCD max{…}) ifadesi (s. 8640) gecikme bütçesi için kaba bir ön tahmin sağlar; ancak tez ölçülmüş adım maliyeti kullandığı için **Yorum:** yalnızca ölçeklenme yönü için referans; ms değeri makalede yok, ölçülmesi gerekir.

**Ön kayıtlı doğrulama senaryosu için yeniden kullanılabilir parametreler**
- f_c = 1.9 GHz, B = 10 MHz, PL₀ = −20 dB @ 1 m, α = 2.2, d = λ/2 (s. 8640).
- Uplink geometri d₁…d₅ = 20/100/5/110/103 m; downlink geometri 60/300/5/330/309 m (s. 8640–8641).
- Rician β = 6 (taban), tarama β = 1…10 (s. 8642); LoS ULA modeli (20)–(21).
- Tren hızı ekseni 50–150 m/s (Şekil 13) ve giriş örneği 300 km/h (s. 8630).
- Anten/eleman: L = 16, N = 9, M₁ = M₂ = 16 (downlink kıyas, s. 8642).
- **Yorum:** Makalede sayısal Doppler değeri yok; f_c = 1.9 GHz ve v ∈ [50,150] m/s'den f_D = v/λ türetilebilir, ancak bu türetilmiş değer makale sayısı değildir ve tezde betikle hesaplanmalıdır. Model dar bant olduğundan tezin OFDM/K_opt eksenine doğrudan karşılık yok; bu senaryo tek alt taşıyıcılı (K = 1) özel durum olarak kullanılabilir.

**Tez iddialarını destekleyen / zıt düşen ifadeler**
- *Destekleyen (kısmen):* Zaman maliyeti hız arttıkça sıralamayı değiştiriyor: Şekil 13'te en çok elemanlı yapılandırma (M₁ = M₂ = 60) yüksek hızda en kötü; *"the numbers of elements on the IRSs are not as large as possible considering the pilot overhead, but needs to be designed according to the train speed"* (s. 8644). **Yorum:** Bu, tezin "gecikme yöntem sıralamasını belirler" ve "hız/Doppler ile ölçeklenen içsel optimum" savıyla aynı yapıda bir bulgu; ancak makalede maliyet **pilot yükü**, tezde **hesaplama gecikmesi**. Tez bu boşluğu dolduruyor: makale hesaplama süresini hiç hesaba katmıyor.
- *Destekleyen:* Denk. (4)'teki (eğitim süresi / uyumluluk süresi) çarpanı, zamanın hız ifadesine doğrudan girdiğini kabul ediyor. **Yorum:** Hesaplama süresi aynı çarpana ya da eskime üzerinden etkin hıza eklenebilir; makale eklemiyor.
- *Zıt düşebilecek:* Makale BCD/MM'nin ~10–40 yinelemede yakınsamasını sorun olarak görmüyor ve hız kaybını yalnızca pilot yüküne bağlıyor (s. 8642–8643). **Yorum:** Tez ölçülmüş gecikme altında bu yineleme sayılarının eskime nedeniyle etkin hızı düşürebileceğini gösterirse, bu makalenin hesaplamayı "bedava" sayan çerçevesiyle çelişir; bu bir çürütme değil, makalenin incelemediği bir eksen.
- Mükemmel CSI ile kestirilen CSI arasındaki farkın yüksek güçte "ihmal edilebilir" olması (s. 8643) **Yorum:** kusurlu CSI kolunda, kestirim hatasının bu kurulumda baskın olmadığını öne sürer; ancak bu, hesaplama sırasında eskime olmayan bir değerlendirmedir.
