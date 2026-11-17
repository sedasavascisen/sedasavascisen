# 05 — Zhang, Yu, Zhao, Wang, Zhao: RIS destekli HSR'de derin transfer öğrenmeyle kanal kestirimi

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/05_Yu_DTL_HSR.pdf` (14 sayfa; tamamı okundu, s. 1–14).
Kural: sayılar yalnızca PDF'ten, sayfa/tablo/denklem referansıyla. PDF'te olmayan her şey **YOK**.
Kendi çıkarımlarım **Yorum** olarak işaretlendi.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar (tam liste, s. 1):** Qingmiao Zhang¹, Chenyang Yu¹, Yuhao Zhao¹, Bing Wang¹, and Junhui Zhao²
  - ¹ School of Information and Software Engineering, East China Jiaotong University, Nanchang, China.
  - ² School of Electronic and Information Engineering, Beijing Jiaotong University, Beijing, China
- **Başlık (s. 1):** "Channel estimation for RIS-aided communication in high-speed railway based on deep transfer learning"
- **Yayın yeri / dergi:** YOK
- **Cilt / sayı / sayfa:** YOK (yalnızca dosyanın kendi sayfa numaraları 1–14)
- **Yıl:** YOK (metinde basılı tarih yok). Not: PDF üst verisinde `CreationDate: Tue Mar 31 08:58:07 2026 UTC`, `Creator: LaTeX with hyperref` — bu basılı künye değil, dosya üst verisidir.
- **DOI:** YOK
- **Hakemli dergi mi, ön baskı mı?** PDF'te hiçbir dergi adı, cilt, DOI, "received/accepted" tarihi, telif notu ya da yayıncı şablonu yok; tek sütunlu özet + iki sütunlu genel LaTeX düzeni. **Yorum:** Belge biçim olarak bir **ön baskı (preprint)** görünümünde; hakemli dergide yayımlandığına dair PDF içinde kanıt **YOK**. Kullanıcının listesindeki "C. Yu et al." eşlemesi düzeltilmeli: Chenyang Yu **ikinci** yazar, ilk yazar Qingmiao Zhang. "Beijing Jiaotong University" yalnızca son yazarın (Junhui Zhao) kurumu; ilk dört yazar East China Jiaotong University'den. "ResearchGate/Preprints" bilgisi PDF'te yazmıyor (doğrulanamadı).

## 2. Problem ve katkılar

- **Problem (s. 1, s. 2):** RIS destekli HSR çok antenli sistemlerde trenin hızlı hareketi kanalı yüksek dinamikli ve zamanla değişken yapıyor; RIS kanal yapısını karmaşıklaştırıyor; doğru CSI zor. Ek olarak pilot yükü ile kestirim doğruluğu arasındaki denge (s. 2–3).
- **Katkılar (s. 3, "main innovations"):**
  1. HSR kanalı için dikkat (attention) mekanizmalı CNN — öznitelik çıkarma, öznitelik güçlendirme ve dikkat kalibrasyonu birleşimi.
  2. Parametre tabanlı + örnek (instance) tabanlı "dual-transfer" mekanizması: yüksek pilot yoğunluğundan düşük pilot yoğunluğuna bilgi aktarımı; pilot yükünü azaltıp doğruluğu artırma.
- **Sonuç bölümü (s. 12, §5):** (1) RIS ile sanal LoS bağlantısı, (2) dikkat tabanlı derin artık ağ, (3) transfer öğrenmeyle pilot yükünü azaltma.

## 3. Sistem modeli

| Öğe | PDF'teki değer | Referans |
|---|---|---|
| Taşıyıcı frekans | 3.5 GHz | Tablo 1, s. 9 |
| Bant genişliği | YOK (doğrudan verilmemiş). Verilen: alt taşıyıcı aralığı 60 kHz, alt taşıyıcı sayısı 624, kanal örnekleme hızı 62 MHz | Tablo 1, s. 9 |
| Alt taşıyıcı / RB | 52 RB; her RB 12 alt taşıyıcı × 14 OFDM sembolü; 624 alt taşıyıcı | s. 9 metin + Tablo 1 |
| BS anteni | K anten ULA (s. 3); simülasyonda 32 | s. 3; s. 9 |
| Tren anteni | M anten (s. 3); simülasyonda 64 | s. 3; s. 9 |
| RIS eleman sayısı | N = Nx × Ny UPA (s. 3); simülasyonda 64 | s. 3; s. 9 |
| Tren hızı | 300 km/h (tek değer) | Tablo 1, s. 9 |
| Doppler frekansı | YOK (sayısal değer yok; yalnızca nitel olarak "Doppler shifts" s. 2 ve yüksek hızdan kaynaklı frekans kayması s. 9) | — |
| Kanal modeli | CDL (Clustered Delay Line); küme sayısı 14; ilk kümenin Rician faktörü −10; MATLAB 5G Toolbox ile üretildi | s. 3; s. 9, Tablo 1 |
| Dalga biçimi | OFDM | s. 9 |
| SNR | 5, 10, 15, 20, 25 dB | Tablo 1, s. 9 |
| Pilot yoğunluğu | 26/52, 10/52, 6/52, 4/52; ρ = N_p/N_RB (Denk. 11); ρ_H = 0.5 üst sınır | Tablo 1; s. 6–7 |
| Kanal yapısı | BS–RIS G ∈ C^{K×N} sabit (Denk. 1/3), MR–BS H_{m,b}, MR–RIS H_{m,r}; LoS + L NLoS yol (Denk. 6–7), NLoS kazançları Rayleigh; LoS kazancı Denk. 8–9 | s. 3–5 |
| Alınan sinyal | Y^i_RIS = H^i_{r,b} Θ H^i_{m,r} X^i + N^i (Denk. 10) — kaskad kanal hedef | s. 5 |

**Yorum (hesap, PDF'te yok):** 624 × 60 kHz = 37.44 MHz kullanılan bant; f_d = v·f_c/c ≈ (83.3 m/s × 3.5e9)/3e8 ≈ 972 Hz. Bu değerler PDF'te **yazmıyor**, yalnızca Tablo 1'den türetilmiş.

**Tutarsızlıklar (PDF'te görülen):**
- s. 3: tren "single-antenna mobile relay (MR)" üzerinden haberleşiyor deniyor, ama tren M anten taşıyor ve simülasyonda "a train with 64 antennas" (s. 9).
- Denk. 1 ve Denk. 3 aynı denklem iki kez yazılmış (s. 3 ve s. 4); Denk. 2 ve 4'te "=" işareti eksik ("φ_BI 2d/λ cos…").
- s. 5: λ önce dalga boyu (s. 4), sonra "path loss exponent" olarak tanımlanıyor (Denk. 8–9 altı).
- s. 3: "train within a single time slot is negligible… large-scale channel parameters remain relatively stable within the observation time slot" — varsayım.
- Metin içi denklem atıfları kaymış: kaynak amaç fonksiyonu "Eq.(11)" diye anılıyor ama Denk. 12; hedef amaç "Eq.(14)" diye anılıyor ama Denk. 15 (s. 7–8).

## 4. Yöntem

- **Kestirilen nicelik:** kaskad kanal (s. 5: "This paper focuses on the cascaded channel"); ağ gürültülü pilot/kanal matrisinden gürültüyü kestirip çıkarıyor (artık öğrenme, s. 6).
- **Mimari (s. 5–6, Şekil 2):**
  - Giriş: alınan pilotun gerçel/sanal kısımları 2B gerçel matris olarak birleştirilir; doğrusal dönüşüm katmanı (Linear + Rearrange).
  - Katman 2–13: derin artık ağ, her katman 64 × 3 × 3 evrişim + BN + ReLU.
  - "Feature energy constraint mechanism" — her katman çıkışını düşük enerjili duruma kısıtlar (s. 5).
  - Öznitelik güçlendirme: katman 14–16 Conv2D-BN-ReLU, katman 17 Conv2D; katman 17 çıkışı orijinal kanal matrisiyle birleştirilip Tanh (s. 6).
  - Dikkat: katman 18 ve 19, kanal-uzamsal ikili dikkat (1×1 evrişim, global ortalama + maks havuzlama paralel; uzamsal ağırlık 1×1 evrişimle) (s. 6).
  - Çıkış: kestirilen gürültü matrisi H_R girişten çıkarılır → Ĥ (s. 6).
- **Transfer öğrenme (s. 7–8, Şekil 3):** üç aşama.
  1. Kaynak görev: yüksek yoğunluklu pilot Y_H ∈ C^{K×M×M_H}, etiket H^(i), MSE ile F_H eğitilir (Denk. 12).
  2. Hedef alanda örnek üretimi: Y_H'den N_L eleman seçilir (r_0, aralık I); Y_L1, Y_L2, Y_L3 kosinüs benzerliği (Denk. 13), ortalama benzerlik (Denk. 14) > 0.8 ise örnek ağırlığı olarak kaydedilip D_L'ye eklenir (s. 8; eşik [19]'a atıfla).
  3. Hedef görev: F_H başlangıç ağırlıklarıyla, ağırlıklı MSE (Denk. 15).
  - ρ_L = 6/52: r_0 = 2, I = 4, N_L = 6; ρ_L = 4/52: r_0 = 5, I = 5, N_L = 4 (s. 12).
- **Veri:** BS 10 dB SNR'de 26'dan fazla RB üzerinden pilot gönderir; yüksek yoğunluklu pilotlar (26/52) 10 ardışık çerçevede düzgün dağılmış 10 zaman diliminde kaydedilir (s. 9). Eğitim örneği sayısı = 20,000 (s. 10). Test kümesi boyutu: YOK. Eğitim/test ayrımı: YOK.
- **Eğitim:** PyCharm 2025.1, PyTorch, Adam, NVIDIA RTX 4070; batch 128, öğrenme oranı 0.0001 (s. 10).
- **Epok:** toplam epok sayısı açıkça YOK. Şekil 6'nın x ekseni ~350'ye kadar uzanıyor (şekilden). Metin: kaynak eğitim kaybı 170. epokta 0.98'e iner; hedef eğitim kaybı 98. epokta 0.51'e iner (s. 10).
- **Kayıp:** NMSE (Denk. 16, s. 10) "loss function" olarak tanıtılıyor; oysa Denk. 12/15 MSE. (Tutarsızlık.)

## 5. Karmaşıklık / gecikme

- Çıkarım (inference) süresi: **YOK**
- Parametre sayısı: **YOK**
- FLOPs: **YOK**
- Eğitim süresi: **YOK**
- Karmaşıklık analizi: **YOK** (yalnızca giriş bölümünde literatüre atıfla "computational complexity that scale linearly with the element count [8]", s. 2).
- **Hesaplama sırasında kanal eskimesi / kestirim gecikmesi:** hesaba katılmıyor (**YOK**). PDF'teki tek ilgili ifade bir varsayımdır (s. 3, aynen):
  > "When the communication distance between the BS and the train is large, the movement of the train within a single time slot is negligible compared to the overall propagation path, resulting in nearly unchanged large-scale fading characteristics. Therefore, this paper assumes that the large-scale channel parameters remain relatively stable within the observation time slot. This assumption can significantly reduce the update frequency of instantaneous CSI, thereby lowering the overhead of pilot signal transmission and improving the efficiency of system resource utilization."
- NMSE, kestirim anındaki gerçek kanala göre (Denk. 16); kestirim yaşlanması, öngörü ufku ya da faz tasarımı **YOK**.

## 6. Ana sayısal sonuçlar ve taban çizgileri

Metin **hiçbir sayısal NMSE değeri vermiyor**; sonuçlar yalnızca şekillerde. Aşağıdaki aralıklar şekillerden **göz kararı okunmuştur, yaklaşık** (±0.3 dB); alıntı için şekle atıf yapılmalı, sayı olarak kullanılmamalı.

- **Şekil 7 (s. 11), yüksek yoğunluk pilot (26/52), SNR 5–25 dB** — sıralama (en iyiden kötüye, metin s. 11 "proposed method outperforms all other comparison algorithms within the SNR range of 5 dB to 25 dB"): Proposed < CDRN < NA-proposed < CNN < FC-DNN < LS.
  - Şekilden yaklaşık: LS ≈ −9 dB (5 dB) → ≈ −10.5 dB (25 dB); FC-DNN ≈ −13 dB düz; CNN ≈ −15.7 → −16.9; NA-proposed ≈ −15.9 → −17.6; CDRN ≈ −16.3 → −18.6; Proposed ≈ −16.5 → −19.2.
  - NA-proposed = dikkat bloğunun standart SoftMax dikkatiyle değiştirildiği ablasyon (s. 11).
- **Şekil 8 (s. 12), ρ_L = 10/52:** TL-Proposed en iyi; ardından Proposed (10/52'de doğrudan eğitilmiş), CDRN, FC-DNN, LS.
  - Şekilden yaklaşık: LS ≈ −8.3 → −9.3; FC-DNN ≈ −11.6 → −12.2; CDRN ≈ −11.7 → −13.4; Proposed ≈ −12.0 → −13.7; TL-Proposed ≈ −12.2 → −13.8. **Yorum:** TL-Proposed ile Proposed farkı şekilde ~0.1–0.2 dB düzeyinde; güven aralığı/tekrar sayısı **YOK**.
- **Şekil 9 (s. 12), ρ_L = 6/52 ve 4/52:** metin: "TL-Proposed" 4/52'de, CDRN'in 6/52'deki performansına "comparable"; avantaj pilot yoğunluğu düştükçe büyüyor (s. 12). Şekilde y ekseni etiketleri kesik (eksi işaretleri görünmüyor).
  - Şekilden yaklaşık: CDRN ρ=4/52 ≈ −8.2 → −8.8; Proposed ρ=4/52 ≈ −9.5 → −11.1; CDRN ρ=6/52 ≈ −9.8 → −11.2; TL-Proposed ρ=4/52 ≈ −9.9 → −11.5; Proposed ρ=6/52 ≈ −10.7 → −12.4; TL-Proposed ρ=6/52 ≈ −11.0 → −12.9.
- **Eğitim kaybı (s. 10, Şekil 6):** kaynak 0.98 (170. epok), hedef 0.51 (98. epok).
- **Taban çizgileri (s. 11):** LS (klasik), FC-DNN [20], CDRN [21], CNN tabanlı [22]; Şekil 9'da yalnızca CDRN.
  - **Klasik taban çizgisi ayarlı mı?** Hayır/bilgi yok: tek klasik yöntem LS; LMMSE, OMP/sıkıştırılmış algılama, Kalman (girişte anılan [9]–[11] KF-OMP, KR-HBKF dahil) karşılaştırılmıyor. LS'nin pilot düzeni/enterpolasyonu **YOK**.
  - **DL taban çizgileri aynı veriyle/aynı ayar taramasıyla mı eğitildi?** **YOK**.
- İstatistik: tohum, Monte Carlo sayısı, güven aralığı **YOK**.
- Hız taraması (farklı v), Doppler taraması: **YOK** (yalnızca 300 km/h).

## 7. Varsayımlar ve sınırlar

- Büyük ölçekli parametreler gözlem zaman dilimi içinde sabit (s. 3); BS–RIS kanalı G sabit (s. 3).
- Tek hız (300 km/h), tek taşıyıcı (3.5 GHz), CDL simülasyonu; ölçüm verisi yok (Tablo 1, s. 9).
- Eğitim verisi tek SNR'de (10 dB) üretildiği yazılı (s. 9) ama test 5–25 dB (Tablo 1); SNR başına ayrı model mi tek model mi: **YOK**.
- Etiket olarak gerçek kanal H^(i) kullanılıyor (s. 7, Denk. 12) — denetimli öğrenme, gerçek CSI'ya erişim varsayımı.
- RIS faz matrisi Θ'nın pilot süresince ne olduğu (sabit/rastgele/eğitim deseni): **YOK**.
- Karmaşıklık, gecikme, gerçek zamanlılık analizi: **YOK**.
- Sistem modelinde iç tutarsızlıklar (tek antenli MR vs 64 antenli tren; λ'nın iki anlamı; tekrarlanan denklemler; kayan denklem numaraları) — §3'e bakınız.
- Hakem süreci belirtisi yok (§1).

## 8. Tezle bağlantı

- **Denetleyicinin ön-uç kestiricisi olabilir mi?**
  **Yorum:** Kavramsal olarak evet — çıktısı kaskad kanal kestirimi (s. 5) ve OFDM/RB yapısında çalışıyor (s. 9), tezdeki geniş bant OFDM + tek faz vektörü kurgusuna giriş verebilir. Ancak (i) gecikme/parametre/FLOP bilgisi YOK, dolayısıyla denetleyicinin "ölçülmüş adım maliyeti" girdisine sayı sağlamıyor; kendi ölçümümüz gerekir; (ii) NMSE kestirim anında ölçülüyor, kestirimin kendisinin süresi boyunca kanalın yaşlanması (tezdeki "effective rate" mantığı) hesaba katılmıyor; (iii) yalnızca 300 km/h — x = ΔT·f_d ekseni boyunca genelleme kanıtı YOK; (iv) Doppler kestirmiyor, oysa denetleyici ölçülmüş Doppler'e ihtiyaç duyuyor — bu makale o girdiyi üretmiyor.
- **Duvar saati gecikmesi ölçüyor mu?** **Hayır** — çıkarım süresi, parametre sayısı, FLOPs hepsi YOK (§5). Donanım (RTX 4070) yalnızca eğitim için anılmış (s. 10).
- **Tezin olumsuz yapay zekâ bulgusunu destekleyen/çelişen unsurlar:**
  - *Destekleyen (Yorum):* Makale DL'nin üstünlüğünü yalnızca NMSE üzerinden, ayarlanmamış tek klasik taban çizgisine (LS) karşı gösteriyor; zayıf taban çizgisi (LMMSE/OMP/Kalman yok) ve gecikme yokluğu, tezin "hesaplama gecikmesi sıralamayı belirler" savunusunun tam da ihmal ettiği boyut. Yüksek yoğunlukta önerilen ağ ile CDRN arasındaki fark şekilde ≤ ~0.6 dB (Şekil 7, yaklaşık), 10/52'de TL'nin doğrudan eğitime katkısı ~0.1–0.2 dB (Şekil 8, yaklaşık) — gecikme maliyeti eklendiğinde bu kazanımların korunacağına dair kanıt YOK.
  - *Çelişen değil ama ayrı rejim (Yorum):* Makale faz optimizasyonu değil kanal kestirimi yapıyor; tezin olumsuz bulgusu (tek geçişli CNN faz ağının basit sezgisele yenilmesi, öğrenilen güncelleme kuralının ms başına kaybetmesi) faz tasarımı içindir. Bu makale kestirim tarafında DL'nin LS'ye karşı NMSE kazancı bildiriyor; bu, tezin bulgusuyla doğrudan çelişmez, çünkü gecikme-ekseninde karşılaştırma yapmıyor.
  - *Yorum:* Teze alıntılanırken uygun çerçeve: "HSR RIS kanal kestirimi için DL önerileri NMSE'yi raporlar fakat çıkarım gecikmesi ve kestirim süresince kanal yaşlanması raporlanmaz (Zhang vd., s. 3, s. 10–12)". Ön baskı olduğu (bkz. §1) ve sayısal değerlerin yalnızca şekillerde bulunduğu belirtilmeli.
