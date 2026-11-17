# 07 — Li, Sun, Tao (2023): RIS destekli mmWave MIMO-OFDM'de ergodik hız maksimizasyonu

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/07_Li_Ergodic_OFDM.pdf` (14 sayfa, dergi sayfaları 2171–2184; tamamı okundu).
Kural: Aşağıdaki her sayı PDF'ten, sayfa/tablo/denklem referansıyla alınmıştır. PDF'te bulunmayan bilgi "YOK" diye işaretlenmiştir. Şekilden göz kararıyla okunan değerler "(şekilden yaklaşık)" diye işaretlenmiştir. Kendi çıkarımlarım "Yorum" etiketini taşır.

---

## 1. Künye (PDF'te basıldığı haliyle)

- **Yazarlar:** Renwang Li, Shu Sun (Member, IEEE), Meixia Tao (Fellow, IEEE)
- **Başlık:** "Ergodic Achievable Rate Maximization of RIS-Assisted Millimeter-Wave MIMO-OFDM Communication Systems"
- **Dergi:** IEEE Transactions on Wireless Communications, **Vol. 22, No. 3**, March 2023
- **Sayfalar:** 2171–2184
- **DOI:** 10.1109/TWC.2022.3210227
- **Tarihler (s. 2171 dipnot):** alındı 21 Mart 2022; revize 6 Ağustos 2022; kabul 20 Eylül 2022; yayın 4 Ekim 2022; güncel sürüm 10 Mart 2023.
- **Kurum:** Department of Electronic Engineering, Shanghai Jiao Tong University. Destek: National Key R&D Program of China, Grant 2020YFB1406802.
- **Mekân notu:** Kullanıcı listesinde "IEEE TWC / ResearchGate" yazıyordu. Gerçek mekân **IEEE TWC**'dir. PDF'in kendisi IEEE Xplore'dan indirilmiş (alt bilgi: "Downloaded on November 16,2026 ... from IEEE Xplore"); ResearchGate'e ait bir iz yok.
- Önceki çalışma (dar bant, doğrudan bağlantı engelli): ref. [26], R. Li ve diğ., IEEE TWC early access 2022, DOI 10.1109/TWC.2022.3199991.

## 2. Problem ve katkılar

- **Problem (Denk. 14a–14d, s. 2174):** Noktadan noktaya RIS destekli mmWave MIMO-OFDM aşağı bağlantısında, **yalnızca istatistiksel CSI** kullanarak ergodik ulaşılabilir hızı R({Q_k}, Θ) (Denk. 13) maksimize etmek. Ortak optimizasyon değişkenleri: BS'deki alt taşıyıcı başına iletim kovaryansı Q_k ve RIS yansıma matrisi Θ. Kısıtlar: Σ_k tr(Q_k) ≤ 1, Q_k ⪰ 0 ve birim modül.
- Yazarlar problemi üç nedenle zor buluyor (s. 2174): ergodik hızın kapalı formu yok; birim modül kısıtı problemi dışbükey olmaktan çıkarıyor; RIS tüm alt taşıyıcılara aynı fazı uygulamak zorunda.
- **Katkılar (s. 2172, madde listesi):**
  1. Saleh-Valenzuela kanallı geniş bant RIS-mmWave MIMO-OFDM'de istatistiksel CSI'ı ele alan "ilk çaba" olduğunu söylüyor ("To the best of the authors' knowledge, this is the first effort...").
  2. Majorizasyon teorisi ve Jensen eşitsizliğiyle ergodik hız için kapalı formlu yaklaşıklar (Lemma 1, Denk. 16–17; Teorem 1, Denk. 20–21; Lemma 2, Denk. 22). Hız; BS ve kullanıcı anten sayısıyla, RIS eleman sayısıyla, güç dağılımıyla ve yönlendirme matrislerinin özdeğerleriyle logaritmik artıyor.
  3. Alternatif optimizasyon (AO): Q_k, uzay-frekans su doldurmaya (spatial-frequency water-filling) indirgenen bir güç dağılımı problemi olarak çözülüyor. Θ ise Riemannian eşlenik gradyan (RCG) ile optimize ediliyor.
- Önceki çalışmaya [26] göre farklar (s. 2172): doğrudan BS-kullanıcı bağlantısı modelde var (çapraz terim pozitif yarı-tanımlı olmadığı için asimptotik ortogonallikle çözülüyor) ve dar bant modeli geniş banda genişletiliyor. Makaleye göre "spatial- and frequency- wideband effects are mitigated in our proposed algorithm".
- Özet iddiası (s. 2172 ve Sonuç, s. 2181): optimizasyon sonrası ergodik hız "about 25 bps/Hz" artıyor.

## 3. Sistem modeli

| Parametre | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı f_c | 28 GHz | §III-C, s. 2176 |
| Bant genişliği f_s | 1 GHz | §III-C, s. 2176 |
| Alt taşıyıcı sayısı K | 24 | §III-C, s. 2176 |
| CP uzunluğu N_CP | 10 | §III-C, s. 2176 |
| BS anteni N_b | 100 (varsayılan); Şek. 2'de 256 ve 64 | §VI s. 2180; Tablo I |
| Kullanıcı anteni N_u | 16 | §VI s. 2180 |
| RIS elemanı N_r | 13×13 = 169 (varsayılan); Şek. 2'de 16×16 ve 10×10; Tablo III'te 10×5, 10×10, 10×20, 10×40 | §VI; Tablo I; Tablo III |
| Yol sayıları L_h = L_g = L_t | 6 (varsayılan); Şek. 3'te (1,1,6) ve (1,1,1) | §VI; Tablo I |
| Dizi geometrisi | BS ve kullanıcıda ULA, RIS'te UPA | §II-B, s. 2173 |
| Eleman aralığı | d = c/(2f_c) = λ/2; RIS'te d_r yarım dalga boyu | Denk. 8–9, s. 2174 |
| Açılar | ψ: [−π, π) içinde düzgün; RIS azimut φ: [−π/2, π/2]; yükseliş: [0, π] | §III-C, s. 2176 |
| Yol kazancı varyansları | σ_h² ~ exp(1); σ_g², σ_t² ~ exp(0.1) (doğrudan ve yansıyan bağlantının karşılaştırılabilir olması için) | §III-C, s. 2176 |
| Monte-Carlo | 100 bağımsız açı kümesi × her biri için 1000 yol kazancı gerçekleşmesi | §III-C, §VI |
| Güç kısıtı | Σ_k tr(Q_k) ≤ 1 (normalize edilmiş); SNR = P_T/σ² | Denk. 1, 13 |
| RIS genliği | ξ_i = 1 | s. 2173 |
| RIS fazı | sürekli, θ_i ∈ [0, 2π) | Denk. 3 |

- **Kanal modeli:** Saleh-Valenzuela (SV), geniş bant (Denk. 4–6). Frekans bölgesi kanalı H_k, G_k ve T_k'dir; her yolun α_i ~ CN(0, σ_i²) kazancı, τ_i gecikmesi ve f_k'ye bağlı dizi yanıtı a(ψ, f_k) vardır. Alt taşıyıcı frekansı f_k = f_c + (f_s/K)(k − 1 − (K−1)/2) (Denk. 7).
- **İstatistiksel ve anlık CSI:** Ergodik hızdaki beklenti "is taken over the complex channel gains" (s. 2174, Denk. 13'ün altı). Optimize edilen ifade (Denk. 21/24/26) açıları ve gecikmeleri (yönlendirme matrislerinin özdeğerleri d_·) ve kazanç varyanslarını (σ²) kullanıyor; anlık kazançları kullanmıyor. Karşılaştırılan PGA [20] ve T-SVD-BF [9] ise anlık CSI (I-CSI) kullanıyor (Tablo II).
  - Yorum: "İstatistiksel CSI" burada tam olarak açılar, gecikmeler ve yol kazancı varyanslarıdır. Bunların nasıl kestirildiği makalede ele alınmıyor (kestirim → YOK).
- **Tüm alt taşıyıcılarda ortak RIS fazı:** Var. "the RIS can only bring the same phase shift on different subcarriers due to the lack of the ability of digital signal processing" (s. 2173). RIS'in frekans yanıtı frekanstan bağımsız varsayılıyor (dipnot 3, s. 2173). Θ gradyanı **K alt taşıyıcının tamamı** üzerinden toplanıyor (Denk. 31b). Alt taşıyıcı alt kümesi seçimi → YOK.
- **Huzme kayması (beam squint):** Uzamsal-geniş bant etkisi, dizi yanıtının f_k'ye bağlı olmasıyla (Denk. 8–9) modelleniyor. Frekans-geniş bant etkisini dipnot 1 (s. 2172) şöyle anlatıyor: "the frequency-wideband effect which is also known as beam squint effect, there are no effective solutions thus far to the authors' best knowledge, especially for RIS" ve "a general method to address the beam squint effect is still absent." Squint'in hıza etkisini ayrıca ölçen bir sonuç → YOK.
- Hız ifadesinde 1/(K + N_cp) normalizasyonu var (Denk. 13). Yorum: Bu normalizasyon yüzünden makaledeki bps/Hz değerleri, CP payı olmayan hız tanımlarıyla doğrudan karşılaştırılamaz.

## 4. Yöntem

- **Yaklaşık amaç fonksiyonu:** N_b → ∞ iken G_k H_k^H → 0 (Önerme 1, Denk. 15), bu yüzden çapraz terim atılıyor. Q_k = U_{q,k} Λ_{q,k} U_{q,k}^H biçimi, A_bg,k ve A_bh,k'nin SVD'lerinden kuruluyor (Denk. 18–19). Jensen üst sınırı R_Jen ise Denk. 21'de.
- **Algoritma 2 (AO, s. 2179):** Başlangıçta q_{k,i}^(0) = 1/(K N_s) ve Θ^(0) [0, 2π)'de rastgele. Döngü şöyle: (i) Θ sabitken q, su doldurmayla güncellenir: q_{k,i} = max(0, 1/q_0 − 1/ζ_{k,i}) ve Σ q = 1 (Denk. 27; ζ, Denk. 26'da). (ii) q sabitken Θ, Algoritma 1 ile güncellenir. Amaçtaki artış ε'nin altına düşünce durur.
- **Algoritma 1 (RCG, s. 2179):** Adımlar: Armijo geri izlemeli adım boyu, Riemannian gradyan (Denk. 29), Polak-Ribière β ile arama yönü (Denk. 38), taşıma (Denk. 39) ve retraksiyon θ ← unt(θ + αη) (Denk. 40). ‖grad f‖₂ ≤ ε olunca durur. Öklid gradyanı özdeğer türevleriyle hesaplanıyor (Denk. 30–37) ve K alt taşıyıcı üzerinden toplanıyor (Denk. 31b). Makaleye göre durağan bir noktaya yakınsaması garanti.
- **İterasyon sayıları:**
  - Algoritma 1 "converges in around 10 iterations" (Şek. 5, s. 2180–2181; q_{k,i} = 1/(KN_s); SNR = 0, 5, 10 dB).
  - Algoritma 2 "converges in about 6 iterations" (Şek. 6, s. 2181).
  - ε'nin sayısal değeri → YOK.
- Yakınsama: amaç değeri iterasyonlar boyunca azalmıyor (non-decreasing), bu yüzden yakınsama garanti (§V-A, s. 2179).

## 5. Karmaşıklık ve gecikme

- **Karmaşıklık mertebeleri (§V-A, s. 2179, aynen):**
  - Denk. 34: O(N_r L_g²)
  - Denk. 31 (gradyan): O(K N_s1 N_r² L_g²)
  - Denk. 19: O(N_b(L_g² + L_h²)); "Q_k in (19) only needs to be calculated once"
  - Toplam: **O(I_1 I_2 K N_s1 N_r² L_g² + K N_b (L_g² + L_h²))**. I_1 ve I_2, sırasıyla Algoritma 1 ve 2'nin iterasyon sayılarıdır.
  - Su doldurma SVD'nin baskın olduğu bir adım; güç dağılımının karmaşıklığı "can be neglected".
- **Tablo II (s. 2180), N_b > N_u durumunda baskın karmaşıklık:**
  - Önerilen: O(I_1 I_2 K N_s1 N_r² L_g² + K N_b(L_g² + L_h²)), istatistiksel CSI
  - PGA [20]: O(KI(N_r N_b N_u + N_b² N_u)), anlık CSI. Genel ifadesi metinde: O(KI(N_r(N_u N_b + N_u²) + N_b N_u² + N_b² N_u + N_u³)).
  - T-SVD-BF [9]: O(K N_r L_1 + K N_u² N_b), anlık CSI. Metinde: O(K N_r L_1 + K N_b N_u min(N_b, N_u)).
- **Tablo III, çalışma süresi (s):** Koşullar: N_b = 100, N_u = 16, L_g = L_t = L_h = 6, Intel i7-7700 @ 3.60 GHz, 16 GB RAM (s. 2180).

| Algoritma | N_r = 10×5 | 10×10 | 10×20 | 10×40 |
|---|---|---|---|---|
| Önerilen | 1.88 | 7.47 | 27.67 | 107.80 |
| PGA [20] | 0.84 | 1.37 | 3.04 | 15.19 |
| T-SVD-BF [9] | 0.05 | 0.07 | 0.11 | 0.63 |

  - Makalenin kendi yorumu: "the complexity of T-SVD-BF in [9] is the lowest, while our proposed algorithm has the highest complexity because we have to calculate the element-wise gradient in Eq. (31)."
  - Sürenin tek bir açı gerçekleşmesi için mi, toplam için mi olduğu → YOK. Yazılım ortamı (MATLAB vb.), iş parçacığı sayısı ve tekrar/yayılım → YOK.
  - Varsayılan N_r = 13×13 = 169 için süre → YOK (tabloda yok).
- **İstatistiksel CSI altında RIS ne sıklıkta güncellenmeli:** **YOK.** Makale; koherens süresi, Doppler, hareketlilik, istatistiklerin değişim hızı ya da RIS güncelleme periyodu hakkında hiçbir sayı ve nicel ifade içermiyor. Bu konudaki tek nitel gerekçeler şunlar: "statistical CSI is more practical to obtain in realistic systems" (Özet) ve "instantaneous channel state information (CSI), which is pretty challenging to acquire in practice since RIS is usually nearly passive and composed of a large number of unit cells" (s. 2172). Sonuç bölümünde de genel bir değerlendirme var: "quite favorable in practice considering the performance and CSI feedback overhead" (s. 2181).

## 6. Ana sayısal sonuçlar

**Yaklaşıkların sıkılığı, Tablo I (s. 2176), SNR = 20 dB.** Normalize hata, Monte-Carlo R'ye göre:

| Durum | \|R_Jen − R\|/R | \|R̃ − R\|/R |
|---|---|---|
| Şek. 2: N_b=256, N_r=16×16, N_u=16 | 37.0% | 19.3% |
| Şek. 2: N_b=64, N_r=10×10, N_u=16 | 47.9% | 25.2% |
| Şek. 3: L_g=6, L_t=6, L_h=6 | 45.9% | 24.9% |
| Şek. 3: L_g=1, L_t=1, L_h=6 | 19.7% | 5.9% |
| Şek. 3: L_g=1, L_t=1, L_h=1 | 10.0% | 2.9% |
| Şek. 4: Q_1 (Denk. 19, Λ = I/(KN_s)) | 42.6% | 21.7% |
| Şek. 4: Q_2 = I/(KN_b) | 66.5% | 36.9% |

- Makale, yaklaşıkların gerçek hızdan **büyük** olduğunu (aşırı tahmin) kabul ediyor ve üç nedenini sayıyor (s. 2176): sonlu N_b'de G_k H_k^H ≠ 0; Q_k optimal değil; Jensen eşitsizliği yaklaşığı büyütüyor. Yaklaşıklar yalnızca L = 1'de gerçek hıza yakın.
- Yaklaşıkları sınayan bu Monte-Carlo karşılaştırmalarında Θ rastgele üretilmiş (s. 2176).

**Karşılaştırmalı sonuçlar, Şek. 7 (s. 2180–2181).** Varsayılan ayarlar kullanılıyor. Taban çizgileri: I-CSI PGA [20], I-CSI T-SVD-BF [9] ve "Not Optimized" (q = 1/(KN_s), Θ rastgele).
- "the PGA-based algorithm in [20] performs best". Fark SNR arttıkça daralıyor ve "When SNR is 40 dB, our proposed algorithm is about 2 bps/Hz worse than the PGA-based algorithm."
- Önerilen yöntem "outperforms T-SVD-BF when SNR is larger than 10 dB".
- Üç algoritma da "Not Optimized" eğrisine göre büyük kazanç sağlıyor. Şek. 7'de 40 dB'de yaklaşık PGA ~85, Önerilen ~83, T-SVD-BF ~73, Not Optimized ~52 bps/Hz (şekilden yaklaşık).

**Q ve Θ'nın katkısı, Şek. 8 (s. 2181):**
- Eşit güç dağılımı, SNR > 10 dB'de optimize edilmiş güç dağılımına yaklaşıyor.
- "Q_k = I/(KN_b), Random Θ" eğrisine göre: yalnızca Θ optimize edilince SNR > 30 dB'de ≈ **8 bps/Hz**; yalnızca Q optimize edilince ≈ **16 bps/Hz**; ikisi birlikte optimize edilince ≈ **25 bps/Hz** kazanç.

**Yakınsama:** Şek. 5'te Algoritma 1 yaklaşık 10 iterasyonda, Şek. 6'da Algoritma 2 yaklaşık 6 iterasyonda yakınsıyor. Şek. 6'nın son değerleri (şekilden yaklaşık):

| Durum | Son değer (bps/Hz) |
|---|---|
| N_b=256, N_r=256, SNR=10 dB | ~48 |
| N_b=100, N_r=169, SNR=10 dB | ~36 |
| N_b=256, N_r=256, SNR=0 dB | ~29 |
| N_b=100, N_r=169, SNR=0 dB | ~20 |

**Güven aralığı ve istatistiksel test:** YOK.

## 7. Varsayımlar ve sınırlar

- **Asimptotik varsayım:** N_b → ∞ (Önerme 1, Lemma 1, Teorem 1). Makale sonlu N_b'nin hata ürettiğini kendisi kabul ediyor (s. 2176).
- **Q_k optimal değil:** Q_k, Denk. 19'daki sabit yön yapısıyla sınırlı; Q'nun optimal biçimi anlık H_eff,k'ye bağlı (s. 2176, Ek B).
- **Amaç fonksiyonu bir üst sınır:** Optimize edilen R_Jen bir üst sınır. Gerçek hızdan %10.0–66.5 sapıyor (Tablo I).
- **RIS modeli:** Frekanstan bağımsız RIS (dipnot 3), ξ = 1 ve sürekli faz. Ayrık faz → YOK.
- **Senaryo:** Tek kullanıcılı, noktadan noktaya bağlantı.
- **Hareketlilik ve eskime:** Hareketlilik, Doppler, kanal eskimesi ve istatistiklerin zamanla değişimi → YOK. Açılar her gerçekleşmede bağımsız ve düzgün rastgele; zamansal korelasyon yok.
- **İstatistiksel CSI'ın elde edilmesi:** Kestirim maliyeti ve hatası → YOK. Kusursuz bilindiği varsayılıyor.
- **Taban çizgisi karşılaştırması:** Taban çizgileri (PGA, T-SVD-BF) anlık CSI ile ve hesaplama ya da CSI gecikmesi cezası olmadan değerlendiriliyor. Karşılaştırma eşit gecikme ya da eşit iş yükü üzerinden yapılmıyor. Tablo III süreleri yalnızca ayrı bir tablo olarak veriliyor.
- **Ölçeklenme:** Çalışma süresi N_r ile hızla artıyor. N_r = 400'de önerilen yöntem 107.80 s sürüyor (Tablo III); bu, gradyanın O(N_r²) teriminden kaynaklanıyor.
- **Squint:** Frekans-geniş bant (squint) etkisi için genel bir çözüm olmadığını makale kendisi söylüyor (dipnot 1).
- **Raporlama eksikleri:** ε değeri, kod ve tohumlar → YOK.

## 8. Tezle bağlantı

Bu bölümdeki her madde **Yorum**'dur. Makalede bu konularda nicel bir ifade yoktur.

- **Yorum, iki zaman ölçeği:** Makalenin yaklaşımı, gecikme farkında RIS denetleyicisi için doğal bir **yavaş döngü** adayı. Yavaş döngüde Θ, açılar, gecikmeler ve σ² ile tasarlanır. Hızlı döngüde tez yöntemleri (Adam/CD vb.) anlık eskimiş kanalla iyileştirme yapar. Bu yapı, Θ'nın anlık kazanç sönümlenmesine bağlı olmamasını sağlar; bu anlamda küçük ölçekli sönümlemeden kaynaklanan eskimeden kaçınır. Ancak hareketli kullanıcıda **açılar da değişir**. Makale bu değişimin hızını ve RIS'in ne sıklıkla yeniden tasarlanması gerektiğini vermiyor (§5: YOK). Yavaş döngünün periyodu tezde açısal değişim hızından (hız, mesafe) türetilmek zorunda; makaleden alınamaz.
- **Yorum, gecikme bütçesi uyumsuzluğu:** Tablo III'e göre önerilen RCG-AO, N_r = 100'de 7.47 s ve N_r = 200'de 27.67 s sürüyor. Bu, tezdeki milisaniye mertebesindeki adım maliyetlerinden birkaç büyüklük mertebesi yavaş. Makaledeki süreler farklı donanım, bilinmeyen dil ve bilinmeyen tekrar koşullarında ölçülmüş; bu yüzden tez ölçümleriyle **doğrudan karşılaştırılmamalı** (CLAUDE.md, kural 5). Kullanılacaksa yöntem tezin ortamında yeniden uygulanıp ölçülmeli; ölçülemezse "ÜRETİLEMEDİ" yazılmalı. Nitel sonuç şu: bu yöntem ancak periyodu saniyeler mertebesinde olan bir yavaş döngüye sığar.
- **Yorum, tezin savını destekleyen yönü:** Makale, anlık CSI'lı PGA'nın 40 dB'de yaklaşık 2 bps/Hz önde olduğunu söylüyor, ama bunu **sıfır gecikme ve eskimesiz** koşulda ölçüyor (§6–7). Tezin "etkin hız" çerçevesinde PGA'nın fazı kendi hesaplama gecikmesi sonunda eskimiş kanalda değerlendirilirse bu sıralama değişebilir. Bu, tezin "gecikme sıralamayı belirler" savının sınanabilir bir örneği; ama **henüz ölçülmüş bir sonuç değil**. Ayrıca makale çalışma sürelerini raporlayıp sıralamaya katmıyor; bu, tezin eleştirdiği "gecikme ikincil ölçüt" tutumunun bir örneği.
- **Yorum, alt taşıyıcı alt kümesi:** Makale ortak RIS fazını K = 24 alt taşıyıcının **tamamı** üzerinden optimize ediyor (Denk. 31b) ve gradyan maliyeti K ile doğrusal (O(K N_s1 N_r² L_g²)). Tezdeki "100 MHz'de 64 alt taşıyıcıdan 16'sı üzerinden optimize etmek karşılığını verdi" bulgusunu ne destekliyor ne çürütüyor; makale alt küme seçmeyi incelemiyor. Ama karmaşıklık ifadesindeki K çarpanı, alt küme seçiminin maliyet tarafındaki gerekçesiyle tutarlı.
- **Yorum, yeniden kullanılabilir parametreler:** f_c = 28 GHz, f_s = 1 GHz, K = 24, N_CP = 10, L = 6 yol, σ_h² ~ exp(1), σ_g², σ_t² ~ exp(0.1), N_b = 100, N_u = 16, N_r = 13×13 ve UPA RIS'te yarım dalga boyu aralık. Bunlar, tezin geniş bant senaryosunu literatürle hizalamak için referans olarak kullanılabilir. Dikkat: tezin bant genişliği 100 MHz, bu makalenin 1 GHz; squint etkisi bu makalede çok daha güçlü olmalı. Ayrıca makalenin hızı 1/(K+N_cp) ile normalize.
- **Yorum, denetleyici tasarımı için çıkarım:** Denetleyicinin yöntem kümesine "istatistiksel CSI ile tasarlanmış Θ" ayrı bir kol olarak eklenebilir; bu kol düşük Doppler ya da büyük ΔT·f_d rejiminde anlık yöntemlere karşı bir taban çizgisi olur. x = ΔT·f_d büyüdüğünde anlık fazın değeri azalırken istatistiksel tasarımın değeri, açılar sabit kaldığı sürece eskimeden etkilenmez. Bu hipotez tezde betikle ölçülmeden yazılamaz (altın kural). Ölçüm fazının 20 Kasım'da kapanacağı göz önüne alınırsa bu iş muhtemelen "gelecek çalışma" kapsamında kalır.
- **Yorum, çelişki:** Tezin herhangi bir iddiasıyla doğrudan çelişen bir bulgu yok. Makale ne hareketlilik ne de etkin hız ölçüyor.
