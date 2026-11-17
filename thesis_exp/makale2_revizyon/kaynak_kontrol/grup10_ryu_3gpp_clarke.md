# Makale 2 — Kaynak kontrolü, Grup 10: Ryu (arXiv), 3GPP TR 38.901, TR 38.913, TS 38.211, Clarke 1968

Tarih: 2026-11-17. Yöntem: metin içeren PDF'lerden `pdftotext` (`-layout` ve düz) ile metin çıkarıldı, ilgili tablolar `grep` ile bulundu ve her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. ETSI belgelerinde basılı sayfa = PDF sayfası − 1 (üst bilgiden okundu). Clarke 1968 taranmış bir PDF (metin katmanı yok, OCR aracı yok). Bu yüzden 44 sayfanın tamamı düşük çözünürlükte, ilgili sayfalar (PDF s. 9, 12, 13) ise yüksek çözünürlükte görüntü olarak okundu. Alıntılar kaynaktan olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`, dal `thesis/p4-deneyler`). **Uyarı:** Makale bu kontrol sırasında değişti: ilk okuma commit `a6b0c41`, son okuma commit `6f3c6b9`. Aşağıdaki "Makale 2'de nerede" alıntıları son hâle göre verildi. Değişen yerler ayrıca belirtildi. Özette (abstract) bu grubun hiçbir anahtarı geçmiyor.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI

1. **[Ryu2026arXiv], "at most a feasibility check" kısmen eksik.** Ryu vd.'de optimizasyon süresi T_opt yalnızca bir fizibilite kısıtı olarak geçmiyor. Kullanılabilir veri oranı γ(ℓ) = 1 − (T_sense + T_opt)/T_CSI üzerinden **amaç fonksiyonuna da giriyor** (denklem 14, 15 ve 18; s. 4). Kaynakta T_opt ölçülmüyor; büyüklüğü FLOP sayısından tahmin ediliyor. Kanal eskimesi ise yalnızca kontrol/geri besleme gecikmesi Δ ile modelleniyor. Bu yüzden "does not enter the aging" doğru, "at most a feasibility check" ise eksik. Düzeltme önerisi aşağıda.
2. **Eşevreli kalma süresi (coherence time) 0.423/f_d Clarke'ta yok.** Clarke 1968, zaman otokovaryansını ρ(τ) = J0(kVτ) olarak veriyor (denklem 18, s. 969). Eşevreli kalma süresi için bir sabit vermiyor. Son sürümde (`6f3c6b9`) §3'teki T_c cümlesinden atıf tamamen kaldırılmış: cümle artık hiçbir kaynağa dayanmıyor. Önceki sürümde (`a6b0c41`) cümle [Clarke1968BSTJ, rappaport_wireless] diyordu. 0.423 sayısı Clarke'a değil, Rappaport'a atfedilmeli. Rappaport kitabının PDF'i klasörde yok, bu yüzden **burada doğrulanmadı**.
3. **TS 38.211 sürümü:** Elimizdeki PDF V16.3.0 (ETSI, 2020-11). Bib ise V16.2.0'ı gösteriyor. Kullanılan büyüklükler (Table 4.2-1, 4.3.2-1, denklem 5.3.1) bu iki sürüm arasında değişmiyor; ama künye, elde olan belgeyle eşleşmiyor.
4. **Ryu künyesi eksik:** Bib'de yalnızca soyadları var. Tam künye aşağıda.

Makaledeki sayısal iddiaların hiçbiri kaynakla çelişmiyor: 10 m / 6 m, 15–19 küme, 3 km/h, 30 km/h, 3.43 / 1.71 / 0.86 ms ve 28.2 ms kaynaklarla uyuşuyor.

---

## [Ryu2026arXiv] Ryu vd., arXiv 2026

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar.
  - Yazarlar (PDF s. 1'de basıldığı gibi): **Sehyun Ryu, Seungmin Choi, Hyun Jong Yang, Senior Member, IEEE, and John M. Cioffi, Life Fellow, IEEE.** PDF meta verisi de aynı: "Sehyun Ryu; Seungmin Choi; Hyun Jong Yang; John M. Cioffi".
  - Başlık: "End-to-End Mobility-Aware Multi-RIS Optimization via Blockage Detection and Closed-Form Riemannian Updates".
  - Kenar damgası: "arXiv:2608.25393v1 [eess.SP] 26 Aug 2026", yani **sürüm v1, 26 Ağustos 2026**, eess.SP. Üst bilgi: "SUBMITTED TO IEEE TRANSACTIONS ON WIRELESS COMMUNICATIONS". 13 sayfa.
  - Kaynak, yazarların GLOBECOM 2026 bildirisinin genişletilmiş sürümü. Bildiri arXiv'de: "This work is an extended version of our GLOBECOM 2026 paper and is available on arXiv [57]" (s. 2).
  - Bib'deki başlık ve arXiv numarası **UYUŞUYOR**; yazar alanı **EKSİK**. Önerilen girdi:
    ```
    @misc{Ryu2026arXiv,
      author={S. Ryu and S. Choi and H. J. Yang and J. M. Cioffi},
      title={End-to-End Mobility-Aware Multi-{RIS} Optimization via Blockage Detection and Closed-Form {R}iemannian Updates},
      howpublished={arXiv:2608.25393v1 [eess.SP]},
      month=aug, year={2026}, note={Submitted to IEEE Trans. Wireless Commun.}
    }
    ```
- **Makale 2'de nerede:** İlgili çalışmalar, `section_02_related_work.tex` satır 8: "In these works the delay between channel acquisition and use, where modeled, is fixed, even where computation is named as a cause [Truong2013JCN]; the optimizer's own run time is at most a feasibility check [Ryu2026arXiv, Liu2021WCL] and does not enter the aging."
- **Kaynakta karşılığı:**
  - s. 4, §II (zamanlama kısıtı): "Timing constraint. Let Topt denote the BS/RIS optimization runtime and TCSI the CSI update interval set by the NR system. The detect–optimize–transmit cycle must satisfy Tsense(ℓ) + Topt < TCSI. (13)"
  - s. 4, denklem (14)–(15): "Tdata = TCSI − Tsense(ℓ) − Topt" ve "γ(ℓ) = 1 − (Tsense(ℓ) + Topt)/TCSI". Problem (18)'in amacı γ(ℓ) Σ_k E[r_k]; kısıtları arasında "timing constraint (13)" var.
  - s. 3 (eskime modeli): "Due to the control/feedback delay ∆, the true channels at t0 +∆ deviate from their estimates." Aynı sayfa: "The residual term Ẽk follows the standard Gauss–Markov channel aging model, where mobility and delay-induced phase distortion are modeled as additive complex Gaussian noise [62]." Kestirim H^pred = ρ(∆)Ĥ (denklem 5–6) yalnızca ∆'ya bağlı. T_opt bu ifadelerde geçmiyor.
  - s. 10, §V-B: "For the largest evaluated configuration with M = 32 RIS panels and K = 16 UEs, the total computational cost of SCRPA is approximately 3.869 GFLOPs. To complete the proposed end-to-end processing within a 5 ms budget, a sustained FP32 throughput of approximately 0.774 TFLOPs/s is required." s. 9, Table I: "Average computational FLOPs … required for each algorithm to reach 99% of its convergence value". Tabloda saniye cinsinden süre yok.
  - s. 11, §V-B sonu: "…can be reliably executed within the CSI update interval, thereby satisfying the timing constraint in (13) and validating the practical feasibility of the proposed end-to-end framework."
  - s. 10, Fig. 9 metni: "…as long as the detection–optimization loop can be completed within 5 ms, the proposed method maintains a stable and high WSR…"
- **Değerlendirme:**
  - "Does not enter the aging": **doğru.** Eskime gecikmesi ∆ "control/feedback delay" olarak tanımlanıyor; T_opt ∆'ya eklenmiyor.
  - "At most a feasibility check": özünde doğru ama **eksik.** T_opt, (13)'te bir fizibilite kısıtı. Bunun yanında γ(ℓ) üzerinden amaçta veri süresini kısaltan sabit bir ek yük olarak da yer alıyor. Ayrıca T_opt hiçbir yerde ölçülmüyor. Fizibilite, FLOP sayısının varsayılan bir işlem hızına (yaklaşık 1 TFLOP/s) bölünmesiyle gösteriliyor. Makale 2'nin "ölçmüyorlar, en fazla kontrol ediyorlar" mesajını bu bilgi güçlendiriyor ve cümleye eklenmeye değer.
- **Karar:** **DÜZELTİLMELİ** (küçük). Önerilen biçim: "…the optimizer's own run time is at most a feasibility check or a fixed airtime overhead, estimated from operation counts rather than measured [Ryu2026arXiv, Liu2021WCL], and does not enter the aging." ([Liu2021WCL] başka grupta kontrol edildi; ona uyup uymadığına o rapordan bakılmalı.) Bib'in yazar alanı tamamlanmalı.

---

## [3gpp_channel] 3GPP TR 38.901 V16.1.0 (ETSI TR 138 901 V16.1.0)

- **Künye karşılaştırması:** PDF: "ETSI TR 138 901 V16.1.0 (2020-11) … 5G; Study on channel model for frequencies from 0.5 to 100 GHz (3GPP TR 38.901 version 16.1.0 Release 16)". 3GPP değişiklik tablosunda V16.1.0'ın tarihi 2019-12 (RAN#86, RP-192629). Bib: TR 38.901, V16.1.0 (Release 16), aralık 2019, aynı başlık. **UYUŞUYOR.** Bib'deki "TODO(author): confirm the TR 38.901 version" notu kapatılabilir; kodun parametreleri de bu sürümle birebir aynı (aşağıya bakın). İstenirse ETSI yayını not olarak eklenebilir.
- **Makale 2'de nerede:**
  - (a) Giriş, `section_01_introduction.tex` satır 8: "…in the 3GPP indoor-office scenario with walking users [3gpp_channel]."
  - (b) Sistem modeli, `section_03_system_model.tex` satır 24: "All links follow the 3GPP TR 38.901 indoor-office model [3gpp_channel]: its path loss, LoS probability, Rician factor and log-normal shadowing with exponential spatial correlation at 5 m (TR 38.901 specifies 10 m for LoS and 6 m for non-LoS)." `a6b0c41`'de cümle "with Gudmundson correlation [Gudmundson1991] at 5 m" diyordu.
  - (c) Aynı paragraf: "we add the TR 38.901 excess loss and shadowing to each hop."
  - (d) Yöntem, `section_05_methodology.tex` satır 7 (atıfsız): "…20 point scatterers, close to the 15–19 clusters of the 3GPP indoor-office model".
- **Kaynakta karşılığı:**
  - **Yol kaybı:** Table 7.4.1-1 (§7.4.1, basılı s. 29, PDF s. 30), InH-Office. LOS: "PLInH−LOS = 32.4 + 17.3 log10(d3D) + 20 log10(fc)", σSF = 3, 1 m ≤ d3D ≤ 150 m. NLOS: "PLInH−NLOS = max(PLInH−LOS, PL′InH−NLOS)", PL′ = 38.3 log10(d3D) + 17.30 + 24.9 log10(fc), σSF = 8.03.
  - **LoS olasılığı:** Table 7.4.2-1 (§7.4.2, basılı s. 30, PDF s. 31). Indoor – Mixed office: 1 (d ≤ 1.2 m); exp(−(d − 1.2)/4.7) (1.2 < d < 6.5 m); exp(−(d − 6.5)/32.6)·0.32 (d ≥ 6.5 m). Indoor – Open office için ayrı bir ifade var (5 m / 70.8 / 211.7 · 0.54).
  - **Rice K çarpanı:** Table 7.5-6 Part-2 (§7.5, basılı s. 45, PDF s. 46), Indoor-Office LOS: μK = 7 dB, σK = 4 dB; NLOS: N/A.
  - **Gölgeleme ve ilinti mesafesi:** Aynı tablonun devamı (basılı s. 47, PDF s. 48), satır "Correlation distance in the horizontal plane [m]", SF: Indoor-Office **LOS 10, NLOS 6**. σSF için tablo Table 7.4.1-1'e yönlendiriyor: "See Table 7.4.1-1".
  - **Küme sayısı:** Aynı tablo (basılı s. 46, PDF s. 47): "Number of clusters N", Indoor-Office **LOS 15, NLOS 19**.
  - **Senaryo ve hız:** Table 7.2-2 "Evaluation parameters for indoor-office scenarios" (§7.2, basılı s. 20, PDF s. 21): "Room size (WxLxH) 120mx50mx3m", "BS antenna height hBS 3 m (ceiling)", "Height hUT 1m", "UT mobility (horizontal plane only) 3 km/h".
  - Table 7.6.3.1-2 (basılı s. 54, PDF s. 55): Indoor için LOS/NLOS durumu ilinti mesafesi 10 m. Bu gölgeleme ilinti mesafesinden ayrı bir büyüklük.
- **Değerlendirme:**
  - (b) Yol kaybı, LoS olasılığı, K çarpanı ve log-normal gölgeleme bu tablolarda var. Kodda (`ris_mu/pathloss.py`, `ris_mu/channel.py`) değerler birebir aynı: 32.4/17.3/20, σ 3.0; 38.3/17.30/24.9, σ 8.03; K ~ N(7, 4) dB.
  - Kodun kullandığı LoS olasılığı **Mixed office** ifadesi. TR 38.901'e göre iki InH alt senaryosu arasındaki tek fark bu: "The only difference between the open office and mixed office models in this TR is the line of sight probability" (Table 7.2-2 notu). Bu yüzden makale "indoor-office (mixed office)" demeli. Yazılmazsa okur hangi LoS olasılığının kullanıldığını bilemez.
  - "10 m for LoS and 6 m for non-LoS" **doğru** (Table 7.5-6 Part-2, SF satırı).
  - "Exponential spatial correlation at 5 m" makalenin kendi seçimi. TR 38.901'e atfedilmiyor ve sapma açıkça yazılmış; sorun yok.
  - (d) "15–19 clusters" **doğru** (LOS 15, NLOS 19).
  - (a) "Indoor-office scenario with walking users" yol kaybı ve kanal parametreleri açısından doğru. Ancak senaryo geometrisi TR 38.901'in değerlendirme yerleşiminden farklı: 40×20×6 m oda (3GPP'de 120×50×3 m), BS 4 m (3GPP'de 3 m tavan), kullanıcı yüksekliği 1–2 m (3GPP'de 1 m), hız 5.4 km/h (3GPP'de 3 km/h). Makale bu geometriyi 3GPP'ye atfetmiyor, ama "the 3GPP indoor-office scenario" ifadesi tüm senaryonun 3GPP'den geldiğini düşündürebilir.
- **Karar:**
  - (b), (c), (d) **DOĞRU**. Önerilen ufak ekleme: "…the 3GPP TR 38.901 indoor-office (mixed-office) model [3gpp_channel]…".
  - (a) **DÜZELTİLMELİ** (küçük). Önerilen biçim: "…in an indoor office with walking users, with the large-scale channel model of 3GPP TR 38.901 [3gpp_channel]."

---

## [3gpp_tr38913] 3GPP TR 38.913 V16.0.0 (ETSI TR 138 913 V16.0.0)

- **Künye karşılaştırması:** PDF: "ETSI TR 138 913 V16.0.0 (2020-07) … 5G; Study on scenarios and requirements for next generation access technologies (3GPP TR 38.913 version 16.0.0 Release 16)". Değişiklik tablosu: "2020-07 RP-88e … Upgraded to Release 16 - without technical change 15.0.0 16.0.0". Bib: TR 38.913, V16.0.0 (Release 16), temmuz 2020. **UYUŞUYOR.**
- **Makale 2'de nerede:**
  - (a) `section_03_system_model.tex` satır 27: "This lies between the 3 km/h of the 3GPP indoor-hotspot evaluation [3gpp_tr38913] and the 10 km/h upper end of the IMT-2020 pedestrian class…"
  - (b) `section_06_results.tex` satır 57: "3 km/h, used in the 3GPP indoor-hotspot evaluation [3gpp_tr38913]; … and the 30 km/h of the dense-urban evaluation [3gpp_tr38913, itu_m2410]."
  - (c) `tables/tab_speeds.tex` satır 5: "3 & 3GPP [3gpp_tr38913] & 50.8 …". Ayrıca satır 30: "ITU, urban".
- **Kaynakta karşılığı:**
  - §6.1.1 "Indoor hotspot", Table 6.1.1-1 (basılı s. 10, PDF s. 11): "User distribution and UE speed: 100% Indoor, 3km/h, 10 users per TRxP". Aynı tablo: "Layout: Single layer: - Indoor floor (Open office)", "Carrier Frequency: … Around 4 GHz".
  - §6.1.2 "Dense urban", Table 6.1.2-1 (basılı s. 11, PDF s. 12): "80% indoor (3km/h), 20% outdoor (30km/h)".
- **Değerlendirme:** Kapalı alan hotspot senaryosunda UE hızı 3 km/h; (a), (b) ve tablonun 3 km/h satırı doğru. Yoğun kentsel senaryoda 30 km/h, dışarıdaki %20'lik kullanıcıların hızı; (b)'deki "the 30 km/h of the dense-urban evaluation" ifadesi bu kaynak için doğru. ([itu_m2410] başka grupta kontrol edildi.) Türetilmiş değer de tutarlı: 3 km/h, 3 GHz → f_d = 8.33 Hz → 0.423/f_d = 50.8 ms. Bu değer 0.423 sabitine bağlı (Clarke maddesine bakın).
- **Karar:** **DOĞRU.**

---

## [3gpp_nr_phy] 3GPP TS 38.211 (bib: V16.2.0; PDF: V16.3.0)

- **Künye karşılaştırması:** PDF: "ETSI TS 138 211 V16.3.0 (2020-11) … 5G; NR; Physical channels and modulation (3GPP TS 38.211 version 16.3.0 Release 16)". ETSI geçmişi: "V16.2.0 July 2020 Publication; V16.3.0 November 2020 Publication". Bib: TS 38.211 **V16.2.0** (Release 16), 2020, "NR; Physical Channels and Modulation". Başlık ve seri **UYUŞUYOR**; **sürüm UYUŞMUYOR**. Kullanılan büyüklükler iki sürümde aynı kalan temel tanımlar, yani sonuç değişmez. Yine de ya bib V16.3.0 olarak güncellenmeli ya da V16.2.0'ın PDF'i edinilmeli.
- **Makale 2'de nerede:** `section_05_methodology.tex` satır 24: "With 5G New Radio (NR) numerology [3gpp_nr_phy] and one orthogonal frequency-division multiplexing (OFDM) symbol per pilot they last 3.43, 1.71 and 0.86 ms at 15, 30 and 60 kHz subcarrier spacing". 48 pilot sembolü [Wang2020TWC]'den geliyor ve bu grupta kontrol edilmedi.
- **Kaynakta karşılığı:**
  - §4.2, Table 4.2-1 "Supported transmission numerologies" (basılı s. 12, PDF s. 13): μ = 0, 1, 2 için Δf = 15, 30, 60 kHz. Normal CP üçünde de var; 60 kHz'te genişletilmiş CP de var.
  - §4.3.1 (aynı sayfa): "…ten subframes of Tsf = (Δfmax Nf /1000)·Tc = 1 ms duration."
  - §4.3.2, Table 4.3.2-1 (normal CP, basılı s. 13, PDF s. 14): N_symb^slot = 14; μ = 0, 1, 2 için alt çerçeve başına 1, 2, 4 slot.
  - §5.3.1 (basılı s. 26, PDF s. 27): "N_CP,l = 144κ·2^−μ + 16κ (normal cyclic prefix, l = 0 or l = 7·2^μ); 144κ·2^−μ (l ≠ 0 and l ≠ 7·2^μ)".
- **Değerlendirme:** Ortalama sembol süresi = 1 ms / (14·2^μ). Buna göre 48 sembol 15 kHz'te 48/14 = 3.4286 ms, 30 kHz'te 1.7143 ms, 60 kHz'te 0.8571 ms sürer. CP uzunlukları tam alınıp alt çerçeve başından sayıldığında sonuç 3.4286, 1.7146 ve 0.8573 ms. Yuvarlanınca 3.43, 1.71 ve 0.86 ms. Makaledeki sayılar **doğru** ve normal CP varsayımına dayanıyor (60 kHz'te genişletilmiş CP seçilseydi sonuç farklı olurdu). Makale bu kaynaktan DMRS yükü ya da slot yapısı gibi başka bir sayı almıyor.
- **Karar:** Atıf **DOĞRU**; künye **DÜZELTİLMELİ**: `number={TS 38.211 V16.3.0 (Release 16)}, year={2020}`. 3GPP değişiklik tablosunda V16.3.0 girdileri 2020-09 (RAN#89-e) tarihli; ETSI yayını Kasım 2020. Ya da V16.2.0'ın PDF'i bulunup bib korunmalı. İsteğe bağlı netleştirme: "…with 5G NR numerology and normal cyclic prefix [3gpp_nr_phy]…".

---

## [Clarke1968BSTJ] Clarke, Bell System Technical Journal 1968 (+ [rappaport_wireless])

- **Künye karşılaştırması:** PDF (taranmış): "A Statistical Theory of Mobile-Radio Reception, By R. H. Clarke". Üst bilgi: "THE BELL SYSTEM TECHNICAL JOURNAL, JULY–AUGUST 1968". İlk sayfa 957, son sayfa 1000 (kaynakça), 44 sayfa. Cilt ve sayı numarası okunan sayfalarda basılı değil. Bib: vol. 47, no. 6, pp. 957–1000, 1968, DOI 10.1002/j.1538-7305.1968.tb00069.x. Sayfa aralığı, yıl, başlık ve yazar **UYUŞUYOR**; cilt/sayı PDF'ten doğrulanamadı ama Temmuz–Ağustos 1968 sayısıyla tutarlı. [rappaport_wireless] PDF'i klasörde **yok**; bu kaynak doğrulanamadı.
- **Makale 2'de nerede:**
  - (a) `section_03_system_model.tex` satır 27, son hâl (`6f3c6b9`): "The reference time scale is the Doppler frequency f_d = v f_c/c = 15 Hz, with coherence time T_c = √(9/(16π))/f_d ≈ 0.423/f_d = 28.2 ms." **Atıf yok.** `a6b0c41`'de aynı cümle "T_c = 0.423/f_d = 28.2 ms [Clarke1968BSTJ, rappaport_wireless]" biçimindeydi.
  - (b) `section_04_latency_analysis.tex` satır 49: "…for small delays the aging loss is quadratic in the distance moved, u = f_d τ, … as in the leading term of the Clarke correlation, J0(2πu) ≈ 1 − π²u² [Clarke1968BSTJ]." `a6b0c41`'de atıf "[Clarke1968BSTJ, rappaport_wireless]" idi.
- **Kaynakta karşılığı:**
  - s. 965 (PDF s. 9), §3.1, denklem (9): "the spatial autocovariance function of the electric field becomes R_Ez(ξ) = ⟨E_z* E_z′⟩av = N E0² J0(kξ)". Koşul (8): açılar −π ≤ α ≤ π aralığında düzgün, p(α) = 1/2π; k = 2π/λ (s. 964).
  - s. 968 (PDF s. 12), §3.2.3, denklem (17): "If the mobile receiving vehicle is moving with velocity V in the x direction, the spatial displacement ξ and the corresponding time displacement τ are related by ξ = Vτ."
  - s. 969 (PDF s. 13), denklem (18): "…equations (9) and (17) give the normalized time autocovariance function as ρ_Ez(τ) = J0(kVτ)." Denklem (20): spektrum (1/πf_m)[1 − f²/f_m²]^−½. Denklem (21): "f_m = V/λ is the maximum Doppler frequency shift."
  - Eşevreli kalma süresi: 44 sayfa görüntü olarak tarandı. "Coherence time" diye bir tanım ya da 0.423, 9/(16π) gibi bir sabit **BULUNAMADI**. Kaynak yalnızca frekans yönünde "coherent bandwidth" tanımlıyor (§V, s. 979–981): "the correlation falls off significantly for frequency separations Δω > 1/T, the inverse of the measure of the spread in time delays" (s. 981).
- **Değerlendirme:**
  - (b) **Doğru.** kVτ = 2π(V/λ)τ = 2π f_m τ olduğundan Clarke'ın (18)'i J0(2π f_d τ) = J0(2πu) ile aynı. Matematiksel olarak J0(x) ≈ 1 − x²/4 açılımından J0(2πu) ≈ 1 − π²u² çıkıyor. Açılımın kendisi Clarke'ta yazılı değil, ama "leading term of the Clarke correlation" ifadesi bunu Clarke'a değil, Clarke ilintisinin açılımına bağlıyor; kabul edilebilir. Bir nüans: J0 sonucu yalnızca izotropik saçılım (düzgün p(α)) ve düşey elektrik alan bileşeni E_z için geçerli. Makalenin kanalı 20 nokta saçıcılı geometrik bir model; makale bu sonucu bir "örnekseme" ("as in") olarak kullandığı için sorun yok.
  - (a) 0.423/f_d = √(9/(16π))/f_d (√(9/16π) = 0.4231). Bu sayı Clarke'ta yok. Literatürde yaygın olarak Rappaport'un ders kitabındaki pratik kurala atfediliyor; kitap elimizde olmadığı için bölüm ve denklem numarası **burada doğrulanmadı**. Aritmetik doğru: f_d = 1.5 · 3·10⁹ / 3·10⁸ = 15 Hz; 0.423/15 = 28.2 ms. Son sürümde cümle tamamen atıfsız; 28.2 ms makalenin referans zaman ölçeği olduğu için bir kaynak gerekli.
- **Karar:**
  - (b) **DOĞRU.**
  - (a) **DÜZELTİLMELİ.** Atıf [rappaport_wireless] olarak geri eklenmeli, Clarke eklenmemeli. Önerilen biçim: "…with coherence time T_c = √(9/(16π))/f_d ≈ 0.423/f_d = 28.2 ms [rappaport_wireless]." Kitaptaki bölüm ve denklem numarası kitaptan kontrol edilip eklenmeli. Clarke burada istenirse yalnızca J0 ilintisi için kullanılabilir: "…Doppler frequency f_d = v f_c/c = 15 Hz of the Clarke spectrum [Clarke1968BSTJ]".

---

## Özet tablo

| Kaynak | Karar | Gerekçe |
|---|---|---|
| [Ryu2026arXiv] | DÜZELTİLMELİ (küçük) + künye eksik | T_opt (13)'te fizibilite kısıtı **ve** (14)–(15) üzerinden amaçta ek yük (s. 4). Yalnızca FLOP'tan tahmin ediliyor: 3.869 GFLOP, 0.774 TFLOP/s, 5 ms (s. 10). Eskime yalnızca ∆ ile modelleniyor (s. 3), bu yüzden "does not enter the aging" doğru. Yazarlar: Sehyun Ryu, Seungmin Choi, Hyun Jong Yang, John M. Cioffi; v1, 26 Ağu 2026, eess.SP |
| [3gpp_channel] | DOĞRU (b, c, d); DÜZELTİLMELİ (a, küçük) | InH yol kaybı, σSF 3/8.03 (Table 7.4.1-1, s. 29); LoS olasılığı (Table 7.4.2-1, s. 30; kod Mixed office kullanıyor); K 7±4 dB, SF ilinti mesafesi 10/6 m, küme sayısı 15/19 (Table 7.5-6 Part-2, s. 45–47); 3 km/h, 120×50×3 m (Table 7.2-2, s. 20). "3GPP indoor-office scenario" geometrinin de 3GPP'den geldiğini düşündürüyor; künye uyuşuyor |
| [3gpp_tr38913] | DOĞRU | Table 6.1.1-1: "100% Indoor, 3km/h" (s. 10); Table 6.1.2-1: "20% outdoor (30km/h)" (s. 11); künye uyuşuyor |
| [3gpp_nr_phy] | DOĞRU (atıf); künye DÜZELTİLMELİ | Table 4.2-1, 4.3.2-1 ve 1 ms alt çerçeveden 48 sembol: 3.4286 / 1.7143 / 0.8571 ms (normal CP). PDF V16.3.0, bib V16.2.0 |
| [Clarke1968BSTJ] | DOĞRU (§4, J0); §3'teki T_c cümlesi DÜZELTİLMELİ | Denklem (18), s. 969: ρ(τ) = J0(kVτ) = J0(2π f_m τ); (21): f_m = V/λ. 0.423/f_d Clarke'ta BULUNAMADI (44 sayfa tarandı). Son sürümde T_c cümlesi atıfsız; [rappaport_wireless] eklenmeli (kitap PDF'i yok, doğrulanmadı) |

ÇIKARILMALI kararı yok. Sayısal uyuşmazlık yok. Düzeltmeler: Ryu cümlesinin tamamlanması ve künyesi, TS 38.211 sürümü, T_c için Rappaport atfı, giriş cümlesinde senaryo ile kanal modelinin ayrılması.
