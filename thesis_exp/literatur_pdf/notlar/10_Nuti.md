# 10 — Nuti, Balti, Evans: mmWave geniş bantlı MIMO RIS'te spektral verimlilik optimizasyonu (PGA)

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/10_Nuti_SE_Wideband.pdf` (6 sayfa, tamamı okundu).
Kural: sayılar yalnızca PDF'ten, sayfa/tablo/denklem referansıyla; PDF'te olmayan → **YOK**.
"Yorum" etiketli satırlar not yazarının çıkarımıdır, makalenin iddiası değildir.
PDF'te sayfa numarası basılı değil; "s. n" PDF'in n'inci sayfasıdır.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Pooja Nuti, Elyes Balti, Brian L. Evans — Wireless Networking and Communications Group, The University of Texas at Austin (s. 1).
- **Başlık:** "Spectral Efficiency Optimization for mmWave Wideband MIMO RIS-assisted Communication"
- **Yayın (s. 1 sol kenar baskısı):** "2022 IEEE 95th Vehicular Technology Conference (VTC2022-Spring) | 978-1-6654-8243-1/22/$31.00 ©2022 IEEE"
- **DOI:** 10.1109/VTC2022-Spring54318.2022.9860779 (s. 1 sol kenar).
- Sayfa aralığı: **YOK** (PDF'te basılı değil).
- arXiv: **YOK** (PDF'te arXiv numarası yok).

**Kullanıcı listesiyle uyuşmazlık:** Listede "GLOBECOM / arXiv:2112.08316" yazıyordu. PDF'e göre yayın yeri **GLOBECOM değil, IEEE VTC2022-Spring**'dir. arXiv:2112.08316 numarası PDF'te geçmediği için bu dosyadan **doğrulanamadı** (aynı çalışmanın arXiv ön baskısı olabilir; ayrıca kontrol edilmeli).

## 2. Problem ve katkılar

- Problem: mmWave (28 GHz) aşağı bağlantı geniş bantlı MIMO-OFDM'de, BS–UE doğrudan yolu ve RIS üzerinden dolaylı yol varken, **alt taşıyıcı başına güç tahsisi matrisleri Q[k]** ile **çok elemanlı RIS faz kaydırmalarının Φ** ortak tasarımı; amaç spektral verimliliğin maksimizasyonu (Özet; denk. 8, s. 3).
- Katkılar (Özet, s. 1): (1) yol kaybı ve tıkanma (blockage) modellemesi, düzgün dikdörtgen dizi (URA) ile geliştirilmiş sistem modeli; (2) gradyan çıkışlı (gradient ascent) ortak tasarım algoritması; (3) asimptotik Big-O karmaşıklık analizi ve çalışma süresi değerlendirmesi.
- Ref. [15]'in (Perović vd., dar bant sub-6 GHz MIMO PGA) geniş bant mmWave'e uzantısı (s. 2).

## 3. Sistem modeli

| Öğe | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı fc | 28 GHz | Tablo I, s. 4 |
| Bant genişliği | 850 MHz | Tablo I |
| Alt taşıyıcı sayısı K | 24 | Tablo I |
| Kanal tap sayıları (L1, L2, L3) | 3, 4, 5 | Tablo I |
| BS anten sayısı | 64 (URA) | Tablo I; s. 2 |
| UE anten sayısı | 4 (URA) | Tablo I |
| Akış sayısı N_s | **YOK** (sembol var, değer verilmemiş) | s. 2 |
| RIS eleman sayısı N_RIS | 64 (varsayılan); Şekil 2'de 64 ve 256; Tablo II'de 4–400 | Tablo I, Şekil 2, Tablo II |
| RIS katsayısı | Birim genlik, faz [0, 2π) sürekli | s. 2 |
| Anten kazancı | 62 dB | Tablo I |
| SNR | −5, 10 dB (Tablo I); Şekil 2'de −10…20 dB | Tablo I, Şekil 2 |
| Kanal modeli | Rician (denk. 1), K̃ Rician faktörü (sayısal değeri **YOK**); LOS kısmı geometrik kümeli çok ışınlı model (denk. 2, ref. [16]) | s. 2 |
| Küme/ışın | N_c = 8; doğrudan LOS 1 küme / 1 ışın; dolaylı NLOS 5 küme / 10 ışın; N_ray = 10 | Tablo I |
| Açısal yayılım | 10° | Tablo I |
| Yol kaybı üsteli | LOS 2, NLOS 4 | Tablo I |
| Dolaylı yol kaybı | ρ_indirect = 256 G_t G_r π² d1² d2² / (λ⁴ (l_t/d1 + l_r/d2)²) | denk. (4), s. 2 |
| Tıkanma | P_LOS = exp(−(√(D² + (l_t − l_r)²) − 10)/50) (denk. 5); Bernoulli yol kaybı (denk. 6) | s. 3 |
| Geometri | D = 200 m, l_r = 1.8 m (Tablo I); deneylere göre l_t, d_ris değişiyor (bkz. §6) | Tablo I, s. 4–5 |
| Eşdeğer kanal | H_eq[k] = √ρ_direct H3[k] + √ρ_indirect H2[k] Φ H1[k] | denk. (3), s. 2 |
| **Ortak vs alt taşıyıcı başına faz** | **Ortak.** "Note that Φ is common across subcarriers k in (3), due to the passive nature of the RIS not including baseband processing [2]." | s. 2 |
| Hareketlilik / Doppler / kanal eskimesi | **YOK** — statik, mükemmel CSI ("The rate optimization for the considered system with perfect CSI", s. 3) | s. 3 |
| Monte Carlo | 500 iterasyon | Tablo I |

## 4. Yöntem

- Amaç (denk. 8, s. 3): max_{Φ, {Q[k]}} (1/K) Σ_{k=1}^{K} log2 det(I_Nr + (1/σn²) H_eq[k] Q[k] H_eq[k]^H), kısıtlar |e_i^T Φ e_i| = 1, Σ_k Σ_g P_{k,g} ≤ P_t, Q[k] ⪰ 0. **Tüm K alt taşıyıcı amaçta** (alt küme seçimi yok).
- Gradyan (denk. 9–13, s. 3): Φ alt taşıyıcıdan bağımsız olduğundan toplam gradyan, alt taşıyıcı gradyanlarının toplamı. A_k(Φ) = I + (1/σ²)H_eq Q H_eq^H; ∂log2 det(A_k)/∂Φ_{i,j} = Trace[A_k⁻¹ ∂A_k/∂Φ_{i,j}] (denk. 11); köşegen için ∂A_k/∂Φ_{i,i} = X_k diag(e_i)(Y_k + Z_k) (denk. 13), X_k = (1/σ²)H2[k], Y_k = H1[k]Q[k]H3[k]^H, Z_k = H1[k]Q[k]H1[k]^H Φ^H H2[k]^H.
- Not: gradyan **karmaşık köşegen elemanlar** üzerinde alınıyor, faz açısı üzerinde değil; güncelleme sonrası birim modüle izdüşüm P(φ_i) = φ_i/|φ_i| (denk. 14).
- Güç tahsisi: uzay-frekans su doldurma, P_{k,g} = max(0, 1/λ_sf − 1/λ_{k,g}) (denk. 15, s. 3–4; ref. [18]); her iterasyonda Q[k] güncelleniyor.
- **Algoritma 1** (s. 4):
  1. Φ'yi U(0, 2π) rastgele fazlarla başlat.
  2. n = 0; R_n hesapla.
  3. while |R_{n+1} − R_n| ≥ ε: ∇_Φ R hesapla; diag(Φ_{n+1}) = diag(Φ_n) + μ diag(∇_{Φn} R); uygulanabilir kümeye izdüşür; Q_{n+1}[k] güncelle; R_{n+1} hesapla; **eğer R_{n+1} ≤ R_n ise μ = μ/10**.
- Adım boyu: başlangıç öğrenme oranı **0.1** (Tablo I); iyileşme olmazsa 10'a bölünüyor (Alg. 1 satır 11–12). Momentum/Adam yok.
- Yakınsama eşiği ε = **0.001** (Tablo I).
- Başlatma: rastgele faz U(0, 2π) (Alg. 1 satır 1). Çoklu başlatma: **YOK**.

## 5. Karmaşıklık / gecikme

- Big-O (s. 5–6): Φ ve Q[k]'nin ortak optimizasyonu için
  O(K(2N_RIS³ + 2N_t³ + (N_RIS+1)N_r³ + (2N_r + N_r² + N_t + 1)N_RIS² + (2N_r + 2N_RIS)N_t² + (3/2)N_t N_r² + (2 + 2N_r + 3N_t N_r)N_RIS)).
  Bileşenler: H_eq hesabı K(N_r N_RIS + N_r N_t N_RIS); Y[k] K(N_RIS N_t² + N_r N_t N_RIS); Z[k] K(N_RIS N_t² + N_RIS² N_t + N_RIS² + N_RIS² N_r); A_k K(N_t N_r + (3/2) N_t N_r² + N_r³); denk. (11) K(N_r N_RIS + N_r² N_RIS + N_r³); gradyan güncellemesi + izdüşüm N_RIS; SVD K·O(2N_t³); Q[k] K(2N_RIS³) karmaşık çarpma (s. 5).
- Uniform güç tahsisiyle karmaşıklığın düşürülebileceği belirtilmiş, karşılaştırma "will be presented in future work" (s. 6).
- FLOP sayımı Lightspeed MATLAB araç kutusu [20] ile; karmaşık çarpma 6 FLOP, karmaşık bölme 8 FLOP (s. 6).
- **Tablo II (s. 6)** — SNR = −5 dB, N_RIS'e göre:

| N_RIS | İter. sayısı | FLOP | Çalışma süresi (s) |
|---|---|---|---|
| 4 | 6 | 1.70e+10 | 0.1742 |
| 16 | 8 | 6.17e+10 | 0.2646 |
| 36 | 10 | 1.28e+11 | 0.4617 |
| 144 | 11 | 1.88e+12 | 1.5274 |
| 196 | 12 | 2.28e+12 | 2.9407 |
| 324 | 16 | 6.61e+11 | 12.0429 |
| 400 | 17 | 5.6e+11 | 22.8954 |

- Makale: "as N_RIS increases the runtime and number of iterations for convergence increases. We observe for N_RIS = 324, 400, the number of FLOPs decreases despite the number of iterations increasing. We observe the same general trends when we run this experiment for SNR = 5dB." (s. 6). SNR = 5 dB tablosu: **YOK**.
- Donanım, iş parçacığı, MATLAB sürümü, tekrar sayısı/yayılım: **YOK**. Süre tek koşu mu ortalama mı: **YOK**.
- Hesaplama sırasında kanal eskimesi: **YOK** — süre koherens süresiyle ilişkilendirilmiyor; mükemmel ve statik CSI.
- Yorum: Tablo II'de N_RIS = 324 ve 400'de FLOP düşerken süre ~4–8 kat artıyor; FLOP ve süre birbiriyle tutarsız. Makale bunu açıklamıyor. FLOP sayısı gecikmenin güvenilir vekili değil — tezin "ölçülmüş gecikme" yaklaşımını destekleyen bir örnek.

## 6. Ana sayısal sonuçlar

Karşılaştırma kolları: önerilen PGA; rastgele RIS fazları; RIS'siz (yalnız doğrudan yol). Hepsinde tıkanma modeli açık (s. 4). Sonuçlar yalnızca grafik; tablo halinde SE değeri **YOK**; grafikten okunmuş değer bu notta verilmiyor.

- **Şekil 2** (l_t = 10 m, d_ris = 2.2 m; SNR −10…20 dB; N_RIS = 64 ve 256): PGA hem RIS'sizden hem rastgele fazdan belirgin kazanç; SNR arttıkça PGA ve rastgele fazın RIS'size göre kazancı "marginally" büyüyor; **N_RIS = 64 PGA ≈ N_RIS = 256 rastgele faz** (s. 4).
- **Şekil 3** (D = 200 m, l_t = 5 m, d_ris = 2.2 m; SNR −5 ve 10 dB; P_LOS 0…1): P_LOS arttıkça rastgele faz PGA'ya yaklaşıyor (güçlü doğrudan yol). 10 dB'de RIS'siz sistem RIS'li sistemlere yaklaşıyor; −5 dB'de RIS'siz sistem tutarlı biçimde daha düşük (s. 4–5).
- **Şekil 4** (metin: l_t = 20 m, d_ris = 30 m, SNR = 5 dB, D = 100–250 m; şekil başlıkları "BS-RIS Distance: 10 m" ve "30 m"): d1 = 10 m'de PGA > rastgele > RIS'siz, d2 arttıkça RIS'in faydası artıyor; d1 = 30 m'de RIS'in kazancı yok denecek kadar az — RIS BS'ye veya UE'ye yakın konmalı (s. 5).
  - Not: Metin tek bir d_ris = 30 m verirken şekilde iki ayar (10 m ve 30 m) var; ayrıca Şekil 4 eksen etiketi "RIS-UE Distance", başlık ise "Distance between BS and UE (d2)" diyor — makale içi tutarsızlık.
- Karmaşıklık: §5, Tablo II (6–17 iterasyon, 0.17–22.9 s).

## 7. Varsayımlar ve sınırlar

- Mükemmel CSI (s. 3), statik kanal; hareketlilik yok. Gelecek çalışma (s. 6): "Immediate future work will consist of studying the current system with more practical simulation settings under the impact of imperfect CSI on spectral efficiency during mobility and comparing the performance of our proposed approach to the AO algorithm proposed in [2]."
- Tek kullanıcı, tek RIS; sürekli faz (ayrık faz yok); birim genlik.
- Tek rastgele başlatma; yerel optimum analizi yok.
- AO [2] ile karşılaştırma yapılmamış (gelecek çalışma); taban çizgileri yalnız rastgele faz ve RIS'siz — Yorum: güçlü klasik taban çizgisi eksik.
- Rician faktörü K̃, N_s, P_t, σ_n² sayısal değerleri **YOK**.
- Çalışma süresi ölçüm koşulları **YOK**; FLOP–süre tutarsızlığı açıklanmamış.

## 8. Tezle bağlantı

- **Doğrudan karşılaştırılabilir optimizer.** Ortak (tüm alt taşıyıcılar için tek) RIS faz vektörü, toplam/ortalama hız amacı (1/K Σ log det) ve gradyan + birim modül izdüşümü — tezin geniş bant kurulumuyla (tek faz vektörü, amaçta K_opt alt taşıyıcı) aynı yapı.
- Yorum — fark: Nuti'nin PGA'sı karmaşık katsayı üzerinde sabit+geri izlemeli (μ0 = 0.1, iyileşme yoksa /10) adım ve |ΔR| < 0.001 durdurma kullanıyor; tez faz açısı üzerinde Adam kullanıyor. Tezde Nuti tarzı PGA'yı bir **klasik kol** olarak kullanırken CLAUDE.md'deki kural gereği adım boyu ve durdurma ölçütü her gecikme bütçesinde taranmalı; makaledeki μ0 = 0.1 / ε = 0.001 yalnızca başlangıç noktası.
- Yorum — gecikme: Tablo II, makalenin kendi ölçümüyle PGA'nın 6–17 iterasyonda ve 0.17–22.9 s'de yakınsadığını gösteriyor (N_RIS = 4–400, K = 24, 64×4 MIMO, su doldurma dahil). 28 GHz'de bu süreler, makalenin hiç ele almadığı hareketli senaryolarda kanal koherens süresi ile kıyaslanmalıdır; makale bunu yapmıyor. Tezin "hesaplama gecikmesi yöntem sıralamasını belirleyen birinci sınıf kısıttır" savı için **motivasyon** olarak alıntılanabilir (makale çalışma süresini raporlayıp eskimeyi modellemiyor). Sayıları tezin ölçümleriyle aynı tabloya koymak doğru olmaz (donanım/koşul YOK, su doldurma dahil).
- Yorum — iterasyon sayısı: "Yakınsamaya kadar iterasyon" (6–17) ölçütü, tezdeki "içsel optimum Adam adım sayısı" kavramının (eskimiş kanalda efektif hızı maksimize eden adım sayısı) tersine bir yaklaşım; Nuti yakınsamayı hedefliyor, tez yakınsamadan önce durmanın efektif hızda daha iyi olabileceğini ölçüyor. Çelişki değil, kapsam farkı.
- Yorum — denetleyiciye girdi: Big-O ifadesi ve Tablo II, denetleyicinin "adım maliyeti" modeline literatür referansı olarak kullanılabilir (maliyet ~K·N_RIS³ ölçekli; alt taşıyıcı alt kümesi K_opt seçmek doğrusal tasarruf sağlar — Big-O'daki K çarpanı). Ancak denetleyici için ölçülmüş adım maliyeti esas alınmalı; Tablo II FLOP–süre tutarsızlığı bunun gerekçesi.
- Yorum — alt taşıyıcı alt kümesi: Makale tüm K = 24 alt taşıyıcıyı kullanıyor; alt küme seçimi incelenmemiş — tezin K_opt ekseni bu çalışmanın kapsamadığı bir boyut.
- Yorum — rastgele faz bulgusu: N_RIS = 64 PGA ≈ N_RIS = 256 rastgele faz ve yüksek P_LOS'ta rastgele fazın PGA'ya yaklaşması, faz optimizasyonunun değerinin senaryoya bağlı olduğunu gösteriyor; tezdeki "faz optimizasyonunun değeri (ör. 1.75× / 2.36×)" oranlarının senaryo koşullarıyla birlikte raporlanması gerektiğini destekler.
- Yeniden kullanılabilir parametreler: fc = 28 GHz, BW = 850 MHz, K = 24, taps 3/4/5, BS 64 / UE 4 anten, N_RIS = 64, açısal yayılım 10°, μ0 = 0.1, ε = 0.001, U(0, 2π) başlatma, 500 Monte Carlo (Tablo I).
- Tez iddialarıyla doğrudan çelişki: **YOK** (makale hareketlilik/gecikme içermiyor).
