# 06 — Abdallah vd. (2023), RIS destekli mmWave MIMO kanal kestirimi (DL + CS)

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/06_Abdallah_DL_CS.pdf` (19 PDF sayfası, tamamı okundu).
Sayfa gösterimi: "s. P / d. D" = PDF sayfası P, dergi sayfası D (PDF s. 1 = dergi s. 3503).
Kural: Aşağıdaki tüm sayılar PDF'ten alınmıştır; PDF'te olmayan bilgi "YOK" diye işaretlenmiştir. Kendi çıkarımlarım "Yorum" etiketlidir.

---

## 1. Künye

Basılı haliyle (s. 1 / d. 3503, başlık, sayfa üst bilgisi ve dipnot):

- **Yazarlar:** Asmaa Abdallah (Member, IEEE), Abdulkadir Celik (Senior Member, IEEE), Mohammad M. Mansour (Senior Member, IEEE), Ahmed M. Eltawil (Senior Member, IEEE)
- **Başlık:** "RIS-Aided mmWave MIMO Channel Estimation Using Deep Learning and Compressive Sensing"
- **Dergi:** IEEE Transactions on Wireless Communications
- **Cilt / sayı:** vol. 22, no. 5
- **Sayfalar:** 3503–3521 (ilk sayfa 3503, son sayfa 3521, s. 19)
- **Tarih:** May 2023
- **DOI:** 10.1109/TWC.2022.3219140
- Ek tarihler (s. 1 dipnot): alındı 6 Mart 2022; revize 5 Ağustos 2022 ve 18 Ekim 2022; kabul 20 Ekim 2022; yayım 9 Kasım 2022; güncel sürüm 10 Mayıs 2023. Destek: Ericsson AB ve KAUST.
- Konferans sürümü: ICC 2022 [37] (s. 3 dipnot 2). Yazarların önceki çalışmasının (RIS'siz frekans-seçici kanal kestirimi, [31]) uzantısı (s. 2 dipnot 1).

**Karşılaştırma ("IEEE TWC, vol. 22, no. 5, pp. 3503–3521, May 2023"):** Tüm alanlar **uyuşuyor** (dergi, cilt, sayı, sayfa aralığı, ay/yıl). Uyuşmazlık yok.

---

## 2. Problem ve katkılar

**Problem** (s. 1 özet): Pasif RIS pilot gönderip işleyemez; kaskat (UE–RIS–BS) kanalın boyutu RIS eleman sayısıyla büyür → yüksek pilot yükü ve hesaplama karmaşıklığı. Önceki çalışmalar çoğunlukla frekans-düz kanala odaklanmış.

**Katkılar** (s. 3 / d. 3505, madde 1–3):
1. **DD-FF-CE** (Data-Driven Frequency-Flat Cascaded Channel Estimation): Açısal kaskat kanalların "çift yapılı seyrekliği" (tüm kullanıcılarda ortak sıfır-olmayan satırlar + kullanıcıya özgü sütun destekleri) kullanılarak kestirim bir CS problemine dönüştürülür; destekler iki gürültü giderici CNN (DnCNN₁ satır, DnCNN₂ sütun) ile **eşzamanlı** bulunur, ardından LS ile kanal elde edilir. Frekans-seçici uzantısı **DD-FS-CE** alt taşıyıcılar arası ortak desteği de kullanır.
2. **DSOMP-FS-CE**: Eğitim verisi / hesaplama gücü yoksa, çift yapılı OMP (simultaneous OMP) tabanlı alternatif.
3. Benzetimle NMSE: "≈ 80-128 frames" pilotla düşük hata; veri güdümlü yöntemler Oracle LS'ye **0.5–1 dB** fark, DS-OMP [20] **5–6 dB** fark; karmaşıklık "more than two orders of magnitude" azalma. OMP tabanlı yaklaşım da 0.5–1 dB farka ulaşır ama veri güdümlüye göre "one order of magnitude increased complexity" (s. 3, madde 3). Veri güdümlü yaklaşım kullanıcı sayısı değişimine daha dayanıklı.

Not: Özette (s. 1) "NMSE gap of 5 to 6 dB" diğer OMP yöntemleri için, önerilen için "only 1 dB" yazıyor; katkı listesinde (s. 3) "0.5 − 1 dB". İki ifade bağlama göre (düz/seçici) farklı.

---

## 3. Sistem modeli

| Parametre | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı f_c | 28 GHz | s. 16 / d. 3516, Tablo VII |
| Bant genişliği | **YOK** (sayısal değer verilmemiş; yalnızca "bandwidth > coherence bandwidth" nitel ifadesi, s. 4) | — |
| Alt taşıyıcı sayısı K | 128 | Tablo VII |
| Kullanılan alt küme K_p | K/4 (Şekil 5b'de K_p = K ve K/4 de) | Tablo VII; s. 17 Şekil 5b |
| Alt taşıyıcı aralığı | **YOK** | — |
| Örnekleme periyodu T_s | sembolik (denk. 12), sayısal **YOK** | s. 5 / d. 3507 |
| Gecikme musluğu N_c | 16 | Tablo VII |
| Yükseltilmiş kosinüs roll-off | 0.8 | Tablo VII |
| BS anten | N_BS = 32 = 8 × 4 UPA (Tablo VII); **ancak** karmaşıklık şekli (Şekil 3) için N_BS = 64 kullanılmış | Tablo VII; s. 15 / d. 3515 metin |
| UE anten | 1 (tek antenli UE'ler) | s. 3–4 / d. 3505–3506, Şekil 1a |
| RIS eleman | N_RIS = 100 = 10 × 10 UPA | Tablo VII |
| Kullanıcı U | 16 (Şekil 5b/8'de U = 4 de) | Tablo VII; Şekil 5b, 8 |
| BS–RIS yol sayısı L_G | 5 (Şekil 9'da 2–7) | Tablo VII; Şekil 9 |
| RIS–kullanıcı yol sayısı L_u | 8 (Şekil 9'da 5–10) | Tablo VII; Şekil 9 |
| AoA/AoD dağılımı | U(0, π) | Tablo VII |
| Veri kümesi boyutu | 10,000 | Tablo VII; s. 16 metin |
| Kanal modeli | Saleh-Valenzuela geometrik (denk. 1, 4; frekans-seçici: denk. 12, 13), sanal açısal gösterim (denk. 5, 14) | s. 4–5 / d. 3506–3507 |
| Yön | Uplink; doğrudan BS–UE LoS bağlantıları engellenmiş | s. 3–4, Şekil 1a |
| Dupleks | TDD (karşılıklılık); FDD gelecek çalışma | s. 16 / d. 3516, Bölüm IV-E |
| Hareketlilik / Doppler | **YOK** — makalede hız, Doppler, zaman korelasyonu veya kanal eskimesi modeli yok | (tüm metin tarandı) |
| RIS fazı alt taşıyıcı başına mı ortak mı | **Ortak.** Denk. (16): y_{u,q}^{[k]} = H_u^{[k]} θ s_{u,q}^{[k]} + w — θ alt taşıyıcı indeksi taşımıyor; Θ_u = θ[s_{u,1},…,s_{u,Q}] (denk. 17'den sonra) | s. 6 / d. 3508 |
| Pilot yansıma deseni | "Each element of RIS reflecting vector θ is selected from {−1/N_RIS, +1/N_RIS} by considering discrete phase shifts" (görüntü çözünürlüğünde paydada karekök olup olmadığı kesin seçilemedi) | s. 16 / d. 3516 |
| SNR aralığı | −20 dB … 0 dB | s. 18 / d. 3518 |

Yorum: Denk. (8)'de Θ_u = θ[s_{u,1},…,s_{u,Q}] yazımı Q zaman diliminde tek bir θ önerir gibi; ancak duyarlılık matrisinin rankı için θ'nın zaman dilimine göre değişmesi gerekir. Makale bunu açıkça netleştirmiyor.

---

## 4. Yöntem

**Algoritmalar** (s. 9–14 / d. 3511–3514):
- **Algoritma 1 (DD-FF-CE):** korelasyon vektörü c_r (denk. 22) → DnCNN₁ ile ortak satır desteği Ω_r (L_G indeks, INDEXSORTDESCEND) → her (u, l_g) için c_{c,u,l_g} (denk. 28) → DnCNN₂ ile sütun desteği (L_u indeks) → LS (denk. 34) → H_u = U_BS Δ_u U_RISᵀ.
- **Algoritma 2 (DD-FS-CE):** önce her kullanıcı için en güçlü K_p alt taşıyıcı seçimi (‖s_u Ỹ_u^{[k]}‖² üzerinden), sonra aynı iki DnCNN adımı (denk. 35, 36), ardından alt taşıyıcı başına LS (denk. 37). Θ'nın sözde tersi tüm alt taşıyıcılar için bir kez hesaplanır.
- **Algoritma 3 (DSOMP-FS-CE):** en güçlü alt taşıyıcı seçimi + satır desteği güç toplamıyla + sütun destekleri OMP ile (L_u iterasyon) + LS.
- Temel öngörü: destekler alt taşıyıcıdan bağımsız (denk. 21) → K_p ≪ K alt taşıyıcı ile destek bulunabilir (s. 9, Bölüm III-C.3).

**Ağ mimarisi** (s. 7 / d. 3509 Şekil 2; s. 16 / d. 3516):
- DnCNN₁: L_C = 3 katman; DnCNN₂: L_C = 7 katman.
- İlk katman: 64 adet 3×3×1 filtre + ReLU; ara katmanlar: 64 adet 3×3×64 filtre + BN + ReLU; son katman: 1 adet 3×3×64 filtre. Artık (residual) öğrenme: ağ gürültüyü kestirir, G = C − R(C) (denk. 25, 31).
- Girdi: c_r → M_h × M_v matris (denk. 23); c_{c,u,l_g} → N_h × N_v matris (denk. 29).
- Kayıp: ortalama Frobenius karesel hata (denk. 25, 31).

**Eğitim verisi** (s. 9 / d. 3511 Bölüm III-C; s. 16 / d. 3516):
- SV geometrik modelden sentetik etiketler; veri kümesi 10,000; %70 eğitim / %30 doğrulama (rastgele bölme).
- Adam; 20 epoch; epoch başına 256 mini-batch; öğrenme oranı 10⁻⁴ (DnCNN₁), 10⁻² (DnCNN₂); doğrulama doğruluğu 10 ardışık iterasyonda iyileşmezse durdurma.
- Öğrenme oranı ve katman sayısı tarandı (Şekil 4a: l_r ∈ {10⁻⁴,10⁻³,10⁻²} / {10⁻²,10⁻¹,10⁻³}; Şekil 4b: L_C ∈ {3,7,15,20}) (s. 17 / d. 3517).
- Eğitimde kullanılan SNR değerleri: **YOK** (belirtilmemiş).

**Pilot yükü:**
- Q zaman dilimi; NMSE şekilleri Q = 128 (Şekil 6, 7). Şekil 8'de Q ∈ {32, 64, 96, 128}, SNR = −5 dB.
- "using Q > 80 frames does not significantly improve performance" (s. 18–19 / d. 3518–3519).
- Katkılar: "reasonably small pilot training frames (≈ 80-128 frames)" (s. 3).

---

## 5. Karmaşıklık / gecikme

- **Karmaşıklık mertebesi (Big-O) tabloları** (s. 15 / d. 3515):
  - Tablo II (DS-OMP [20]): FF: O(U N_BS Q + U L_G N_RIS (Q L_u²)); FS: O(K U N_BS Q + K U L_G N_RIS (Q L_u²)).
  - Tablo III (OMP [19]): FF: O(U N_BS Q (N_BS N_RIS + 2(L_u L_G)²)); FS: O(K U N_BS Q (N_BS N_RIS + 2(L_u L_G)²)).
  - Tablo IV (Alg. 1) toplam: O(U N_BS Q + U L_G N_RIS Q + U L_G (2Q L_u² + L_u³)) + DnCNN terimi (38).
  - Tablo V (Alg. 2) toplam: O(K U Q N_BS + K_p U Q N_RIS L_G + K U (L_G N_BS + L_u N_RIS)) + (38).
  - Tablo VI (Alg. 3) toplam: O(K U Q N_BS + (K + 2K_p) U Q N_RIS L_G L_u).
  - Denk. (38): DnCNN çevrimiçi karmaşıklığı O(Σ_l D_x D_y D_z b_x b_y c^{(l−1)} c^{(l)}).
- **Şekil 3** (s. 8 / d. 3510): Big-O "Operations" vs Q (20–130), N_RIS = 100, N_BS = 64, K = 128, K_p = K/4, L_G = 5, L_u = 8 için. Metin: önerilen DD yöntemler DS-OMP'den ve geleneksel OMP'den [19] "by more than two orders of magnitude" daha düşük (s. 15–16 / d. 3515–3516).
- **FLOPs:** **YOK** (yalnızca Big-O sayımı; Şekil 3 ekseni "Operations (Big-O)").
- **Ölçülmüş çalışma süresi (ms / s):** **YOK.** Donanım, CPU/GPU zamanlaması verilmemiş.
- **Çevrimdışı eğitim karmaşıklığı:** dahil edilmemiş — "the offline training complexity is still an open issue due to a more involved implementation of the backpropagation process during the training [42]. Therefore, we only consider the complexity of the online deployment which is based on simple matrix-vector multiplications." (s. 15 / d. 3515)
- GPU iddiası: "We should also note that DL enjoys the advantages of parallel processing virtues of graphics processing units (GPUs), and hence, the overall time complexity is dominated by the analytical operations performed in the proposed algorithms." (s. 15 / d. 3515)
- **Hesaplama sırasında kanal eskimesi:** **YOK.** Kanalın kestirim/hesaplama süresince değiştiği hiçbir yerde modellenmiyor. Tek ilgili ifade gelecek çalışma: "In our future work, we will extend the proposed approaches by taking channel extrapolation into account, which is shown to be a promising approach [48], [49] to estimate cascaded channels." (s. 17 / d. 3519, Bölüm VI). FDD bağlamında "angle coherence time which is much longer than the conventional channel coherence time [45]" ifadesi geçer (s. 16 / d. 3516) ama sayısal değer yok.

---

## 6. Ana sayısal sonuçlar

Tüm NMSE sonuçları grafikseldir; tablo halinde sayısal sonuç yok. Aşağıdaki dB değerleri metinde yazılı olanlardır (grafikten okuma yapılmadı).

| Sonuç | Koşul | Kaynak |
|---|---|---|
| DD-FF-CE, Oracle LS'ye "within a gap around 1 dB" | Frekans-düz, Q = 128, SNR −20…0 dB, Tablo VII | s. 18 / d. 3518, Şekil 6 |
| DD-FF-CE, frekans-düz DS-OMP ve geleneksel CS'den "approximately −5 dBs" daha düşük NMSE; ChannelNet [29]'den iyi | aynı | s. 18, Şekil 6 |
| DD-FS-CE, Oracle LS'ye "within a gap around 0.5 dB" | Frekans-seçici, Q = 128 | s. 18, Şekil 7 |
| DSOMP-FS-CE, Oracle LS'ye "within a gap around 1 dB" | aynı | s. 18, Şekil 7 |
| DD-FS-CE, frekans-seçici DS-OMP'den "approximately −4 dBs", FL-based ChannelNet [36]'dan "−3 dBs" daha düşük | aynı | s. 18, Şekil 7 |
| Q > 80 anlamlı iyileşme getirmiyor; DD-FS-CE ve DSOMP-FS-CE'nin pilot yükü DS-OMP [20]'den düşük | SNR = −5 dB, Q ∈ {32,64,96,128}, U ∈ {16, 4} | s. 19 / d. 3519, Şekil 8 |
| U = 16 → 4 azalınca DSOMP-FS-CE bozuluyor; DD-FS-CE (U = 16 ile eğitilmiş, U = 4'te test) dayanıklı | aynı | s. 19, Şekil 8; s. 17–18, Şekil 5b |
| K_p ≪ K destek tespitini etkilemiyor | Şekil 5b, K_p ∈ {K, K/4} | s. 17 / d. 3517 |
| Yol sayısı arttıkça tüm yöntemlerin NMSE'si kötüleşiyor; DD-FS-CE Oracle LS ile eşleşiyor, DS-OMP en duyarlı | SNR = −5 dB, Q = 128, [L_G, L_u] ∈ {[2,5] … [7,10]} | s. 19, Şekil 9 |
| Destek tespit olasılığı: DnCNN tüm SNR aralığında DS-OMP'yi geçiyor | −20…0 dB | s. 17, Şekil 5a/5b (sayısal değer metinde yok) |
| Karmaşıklık: DD yöntemler OMP [19]'dan >2 mertebe düşük; OMP tabanlı öneri DD'den ~1 mertebe yüksek | Şekil 3 parametreleri | s. 3; s. 15–16 |

**Taban çizgileri** (s. 16 / d. 3516): ChannelNet [29] (frekans-düz CNN), FL-based ChannelNet [36], DS-OMP [20] (alt taşıyıcı başına tekrarlanan), CS-based [19] (geleneksel OMP), Oracle LS (alt sınır, destekler bilinir).

**Klasik taban çizgileri ayarlanmış mı?** **Belirtilmemiş (YOK).** DS-OMP, geleneksel OMP ve ChannelNet için hiperparametre/ayar taraması anlatılmıyor. Buna karşılık önerilen DnCNN'lerin öğrenme oranı ve derinliği taranmış (Şekil 4). Yorum: Asimetrik ayar — tezin "zayıf taban çizgisi" uyarısına (CLAUDE.md) birebir uyan bir durum; makalenin "−4/−5 dB" üstünlüğü ayarlanmış klasik kola karşı kanıtlanmış değil. Ayrıca DS-OMP "per subcarrier" çalıştırılarak alt taşıyıcı ortak seyrekliğinden yararlanmıyor; bu bir tasarım farkı, ayar farkı değil.

---

## 7. Varsayımlar ve sınırlar

- Statik kanal: hareketlilik, Doppler, zamansal korelasyon yok; kestirim süresince kanal sabit varsayılıyor (açıkça söylenmiyor, ama hiçbir zaman değişim modeli yok).
- Destekler (AoA/AoD) tüm bant boyunca frekanstan bağımsız (denk. 21; "spatial propagation characteristics ... almost unchanged within the system bandwidth", s. 6–7). Işın eğilmesi (beam squint) yok — oysa konferans sürümü [37] başlığı "with beam squint".
- Açılar ızgarada değil U(0,π) — sanal açısal gösterim ızgara dışı sızıntıya açık; makale ele almıyor (Yorum).
- L_G ve L_u **bilindiği** varsayılıyor (INDEXSORTDESCEND L_G ve L_u indeks seçer; s. 6 "the number of paths (L_G and L_u) are known to be limited").
- Doğrudan BS–UE bağlantısı engelli.
- TDD karşılıklılığı; FDD gelecek çalışma.
- Pilotlar ortogonal (s_{u1} s_{u2}^H = 0), tek antenli UE'ler.
- Eğitim ve test aynı SV model dağılımından; gerçek ölçüm/ray-tracing verisi yok. Dipnot 3: başka parametrelere genelleme "needs experimental tuning of DnCNN hyperparameters" (s. 9).
- Karmaşıklık yalnızca çevrimiçi Big-O; eğitim maliyeti, ölçülmüş süre, donanım yok. Şekil 3'te N_BS = 64, benzetimde N_BS = 32 (tutarsızlık değil ama farklı yapılandırma).
- Makale yalnızca kanal kestirimi yapar; RIS faz optimizasyonu / hız sonucu yok.

---

## 8. Tezle bağlantı

**Rol:** Ön uç (front-end) kanal kestirici. Optimizatör değil, faz optimizasyonu için taban çizgisi de değil.

- Yorum — Ön uç: Algoritma 2/3'ün çıktısı alt taşıyıcı başına Ĥ_u^{[k]} (k = 0…K−1); bu, tezdeki geniş bant OFDM ortak-faz optimizasyonunun girdisiyle aynı türdendir. Planlanan gecikme-bilinçli RIS denetleyicisine kestirici bloğu olarak takılabilir. Ancak gecikme bütçesine **iki** ek kalem girer: (i) Q pilot zaman diliminin süresi (Q ≈ 80–128), (ii) kestirim hesaplama süresi. Makale ikisini de saniye cinsinden vermiyor; tezde ölçülmesi gerekir.
- Yorum — Alt taşıyıcı alt kümesi: Makalenin "K_p = K/4 strongest subcarriers" fikri (destek frekanstan bağımsız → az alt taşıyıcı yeter) tezdeki denetleyicinin "alt taşıyıcı alt kümesi" düğmesiyle kavramsal olarak örtüşür; kestirim tarafında bu indirgemenin destek tespitini bozmadığını gösteriyor (Şekil 5b). Faz optimizasyonu tarafında aynı indirgemenin hız kaybı ayrıca ölçülmelidir — makale bunu göstermez.
- Yorum — Ortak RIS fazı: Makale de tüm alt taşıyıcılar için tek θ varsayıyor (denk. 16) — tezin geniş bant modeliyle tutarlı.
- **Ön kayıtlı doğrulama senaryosu için yeniden kullanılabilir parametreler** (Tablo VII): f_c = 28 GHz, N_BS = 32 (8×4 UPA), N_RIS = 100 (10×10 UPA), U = 16, K = 128, K_p = K/4, L_G = 5, L_u = 8, N_c = 16, roll-off 0.8, AoA/AoD ~ U(0,π), SNR −20…0 dB, Q = 128 (veya 32–128). Bant genişliği ve alt taşıyıcı aralığı **YOK** → Doppler'i x = ΔT·f_d'ye bağlamak için tezde ayrıca seçilmeli ve öyle olduğu kayda geçmeli.
- Yorum — Destekler/çelişmez:
  - **Destekler (dolaylı):** Makale hesaplama karmaşıklığını birinci derece bir tasarım ölçütü olarak ele alıyor (Şekil 3, Tablo II–VI), ancak yalnızca Big-O düzeyinde. Tezin savunu cümlesi (gecikme yöntem sıralamasını belirler) bu ilgiyi ölçülmüş milisaniyeye ve kanal eskimesine taşıyor — makale bu boşluğu bırakıyor (kanal eskimesi YOK, ölçülmüş süre YOK; gelecek çalışma: "channel extrapolation", s. 17).
  - **Dikkat:** ">2 mertebe düşük karmaşıklık" iddiası Big-O sayımı + GPU paralelliği varsayımına dayanıyor; tezde "eşit adım ≠ eşit gecikme" bulgusu (öğrenilen adım ~2.7 Adam adımı) mertebe sayımının duvar saatiyle örtüşmeyebileceğini gösterdi. Makaleden "DL daha hızlı" diye alıntı yapılmamalı; yalnızca "mertebe olarak daha düşük" denebilir.
  - **Çelişmez:** Tezdeki tek geçişli CNN faz ağının basit sezgisele kaybetmesi bu makaleyle çelişmez: buradaki CNN bir **destek tespiti / gürültü giderici** (yapılandırılmış seyreklik + LS ile birlikte), faz kestirmiyor; ve klasik taban çizgileri ayar taraması görmemiş. Tezin negatif sonucu (ayarlanmış klasik kola karşı) farklı bir görev ve daha sıkı bir karşılaştırma protokolüdür.
- Yorum — Kullanım önerisi: Tezde atıf "literatürdeki kestiriciler (ör. Abdallah vd. 2023) gecikme-bilinçli denetleyicinin ön ucu olabilir; ancak bu kestiricilerin pilot ve hesaplama süreleri hareketli senaryoda ölçülmeli" biçiminde olmalı. Ön ucun bu tezde uygulanması 20 Kasım ölçüm kapanışından sonra plan dışı kalır (CLAUDE.md önceliği).
