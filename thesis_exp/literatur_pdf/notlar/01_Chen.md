# 01 — Chen ve ark., RIS destekli mmWave IoV'de dağıtıcı yüksek-Doppler kanal kestirimi

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/01_Chen_HighDoppler_IoV.pdf` (15 PDF sayfası).
Sayfa göstergesi: "s. N" = PDF sayfası N; dergi sayfası = 676 + N (s. 1 = dergi s. 677).
Şekillerden okunan değerler "(şekilden, yaklaşık)" diye işaretlendi; bunlar metinde sayı olarak yazılmıyor, eğriden göz kararı okundu.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Jiaxin Chen, Wenqian Shen, Shixun Luo, Siqi Ma, Chengwen Xing (Member, IEEE), Lajos Hanzo (Life Fellow, IEEE) (s. 1)
- **Başlık:** "Estimation of Dispersive High-Doppler Channels in the RIS-Aided mmWave Internet of Vehicles" (s. 1)
- **Dergi:** IEEE Internet of Things Journal, Vol. 11, No. 1, 1 January 2024 (s. 1 üst bilgi)
- **Sayfalar:** 677–691 (ilk basılı sayfa 677, s. 1; son basılı sayfa 691, s. 15 — 690'da kaynakça biter, 691 yazar biyografileri)
- **Yıl:** 2024 (cilt tarihi); yayın tarihi 2023 (aşağıda)
- **DOI:** 10.1109/JIOT.2023.3286279 ("Digital Object Identifier", s. 1)
- **Durum (s. 1 dipnot):** "Manuscript received 15 May 2023; accepted 9 June 2023. Date of publication 14 June 2023; date of current version 25 December 2023." → Sayıya girmiş nihai sürüm (early-access değil; cilt/sayı/sayfa atanmış).
- ISSN satırı: "2327-4662 © 2023 IEEE" (s. 1 alt bilgi).
- Sorumlu yazar: Shixun Luo (s. 1).

## 2. Problem ve katkılar

- **Problem:** Mevcut RIS kanal kestirim yöntemleri çoğunlukla zamanla değişmeyen (quasi-static) kanallara odaklanıyor; yüksek hızlı araçların Doppler etkisini göz ardı etmek ciddi başarım kaybına yol açıyor (Özet, s. 1). Önceki yüksek-Doppler çalışmaları ([24]–[26]) BS–RIS arasında tek LoS yol varsayıyor; çok yollu BS–RIS ve RIS–kullanıcı bağlantılarında bir eşdeğer gecikme tap'i, farklı Doppler'lere sahip birden çok kaskad yolun toplamı olabiliyor (s. 2).
- **Katkı 1:** Her iki atlamada çok yol bulunan OFDM sistemi için, Doppler etkisini doğrudan içeren zamanla değişen kaskad kanal ifadesi; dönüşümlerle gecikme-alanı pilot/alınan sinyal ilişkisi (denk. (3)–(9), s. 4–5) ve her eşdeğer gecikme tap'inde kestirim (s. 2).
- **Katkı 2 (büyük BS dizisi):** İki aşamalı strateji — Aşama I'de rastgele RIS RC'leriyle BS AoA'ları CS (MMV-OMP) ile kestirilip yollar ayrıştırılır; Aşama II'de RIS RC'leri sabit tutularak ardışık semboller arası faz farkından her yolun Doppler'i hesaplanır; Doppler telafisi sonrası Aşama I sinyalleriyle RIS'teki eşdeğer AoD ve kazançlar kestirilir (s. 3, Bölüm III, s. 5–7).
- **Katkı 3 (küçük BS dizisi):** BS açısal çözünürlüğü yetmediğinde RIS yansıma örüntüleri, kaba kestirilen eşdeğer AoD'lere göre "interleaved" (serpiştirilmiş) biçimde tasarlanır; Doppler'i hesaba katarak AoD ve kazançlar gradyan inişi + LS ile rafine edilir (s. 3, Bölüm IV, s. 7–9).
- Literatürle karşılaştırma Tablo I'de (s. 2): önerilen yöntem geniş bant frekans-seçici + zamanla değişen + BS–RIS çok yollu + parametrik.

## 3. Sistem modeli

| Parametre | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekans f_c | 30 GHz | s. 9, Tablo II |
| Alt taşıyıcı aralığı | 240 KHz (tabloda "B" sembolüyle) | s. 9, Tablo II |
| Bant genişliği B | Sembolik (s. 3: "The signal bandwidth is B"); sayısal değer **YOK** | s. 3 |
| Alt taşıyıcı sayısı N | 256 | s. 9, Tablo II |
| Pilot alt taşıyıcı N_p | 16 (tarak yapısı, aralık Δ = N/N_p) | s. 9, Tablo II; s. 4 |
| OFDM sembol süresi | T_s = 1/Δf = 4.2 µs | s. 9 |
| Maks. kaskad gecikme τ_D | 250 ns → W_c = 1/(2τ_D) = 2000 KHz | s. 9, Tablo II; s. 9 metin |
| CP | T_cp maksimum yol gecikmesinden uzun varsayılır; sayısal değer **YOK** | s. 3 |
| BS anteni M_b | Büyük dizi senaryosu: 30 (s. 10); Şekil 13'te 10–60 taranır (s. 12). Küçük dizi: tek antenle anlatılır, paralel işlemle çok antene genişler (s. 7). | s. 10, s. 12, s. 7 |
| RIS elemanı M_r | 100 (ULA); Şekil 14/15'te 20–120 taranır | s. 9, Tablo II; s. 13 |
| Kullanıcı | Tek, tek antenli, hızlı hareket eden; uplink | s. 3, Şekil 1 |
| Yol sayıları | L_1 = 3 (BS–RIS), L_2 = 5 (RIS–kullanıcı) | s. 9, Tablo II |
| Hız | 80 km/h (ana senaryo); IoV'de tipik 50–100 km/h → 30 GHz'de maks. Doppler 1400–2800 Hz | s. 9, Tablo II; s. 9 metin |
| Doppler | f_m = v/λ, f_{l2} = f_m cos(γ_{l2}); D_s = 2 f_m; Tablo II'de D_s = 4500 Hz; T_c = 1/(4D_s) ≈ 55.6 µs | denk. (2), s. 4; s. 9 |
| Taranan Doppler | Büyük dizi: ~1700–2700 Hz (60–80 km/h), Şekil 8; küçük dizi: Şekil 11'de eksen ~1800–3200 Hz | s. 11; s. 12, Şekil 11 |
| "Relevance interval" | 300 OFDM sembolü (tek çerçeve; parametreler bu sürede sabit sayılır) | s. 9, Tablo II; s. 4 |
| Kanal modeli | Saleh–Valenzuela [32]; BS–RIS quasi-static, RIS–kullanıcı yollarına Doppler faz kayması eklenir | s. 3, denk. (1)–(2), s. 4 |
| Açı/kazanç üretimi | Fiziksel AoA/AoD [−π/2, π/2]'den rastgele, karmaşık kazançlar rastgele ve 1'e normalize | s. 9 |
| Gecikme yayılımı | τ_D ≈ 250 ns ([51] 3GPP TR 38.901'e atıf; blokajın DS'yi belirgin etkilemediği [50]) | s. 9 |
| RIS fazı alt taşıyıcı başına mı? | **Ortak.** "the RIS RCs are frequency insensitive within a certain bandwidth" → tüm alt taşıyıcılarda aynı θ^q (denk. (8)) | s. 5 |
| RIS genliği | α_{m_r} = 1 | s. 5 |
| Dalga biçimi | OFDM (OTFS yalnızca literatürde [26] anılıyor) | s. 3; s. 2 |
| Doğrudan kanal | İhmal (RIS kapatılarak klasik yöntemle kestirilebilir denir) | s. 3 |

## 4. Yöntem

- **Kestirilen nicelikler:** Her eşdeğer gecikme tap'i d için yol başına {c_s, f_s, φ^B_s, φ^R_s}: karmaşık kazanç, Doppler, BS'teki AoA, RIS'teki eşdeğer AoD (denk. (9)–(10), s. 5). Kanal sonra denk. (5) ile yeniden kurulur. **RIS faz optimizasyonu yapılmaz**; RIS RC'leri yalnızca eğitim (pilot) örüntüsü olarak tasarlanır.
- **Gecikme alanına geçiş:** N_p noktalı IDFT ile farklı gecikmeli yollar ayrışır (denk. (9), Ek A, s. 13).
- **Büyük BS dizisi (Bölüm III, s. 5–7):**
  - Aşama I (Q_1 sembol, rastgele RIS RC): BS AoA'ları MMV tabanlı OMP ile; sözlük açısal çözünürlüğü 1/M_b (denk. (12)–(15)).
  - Aşama II (Q_2 sembol, sabit θ): Doppler, ilk ve son Q_2−1 sembol toplamlarının faz oranından: f̂_s = ∠(r_2/r_1) / (2π(T+T_cp)) (denk. (17)–(20), s. 6–7).
  - Doppler telafisi sonrası RIS AoD + kazanç: OMP, çözünürlük 1/M_r (denk. (21)–(23), s. 7).
- **Küçük BS dizisi (Bölüm IV, s. 7–9):**
  - Aşama I: Doppler ihmal edilerek kaba RIS AoD'leri OMP ile (denk. (25)).
  - Aşama II: θ^q = a_{M_r}(φ̂^R_{s_d}) ile yansıma örüntüsü tasarımı; serpiştirilmiş düzen — Aşama II Q_2 bloğa bölünür, her blok L_1L_2 sembol; Doppler denk. (29): f̂ = ∠(r_{2,d}/r_{1,d}) / (2π L_1 L_2 (T+T_cp)) (s. 8).
  - Rafine: alternatif optimizasyon — c_d sabitken φ^R üzerinde gradyan inişi (adım η, denk. (34)–(36)), sonra LS ile c_d (denk. (37)); türev Ek B'de (s. 14).
- **Pilot yükü:**
  - Büyük dizi: Q_1 = 18, Q_2 = 12, toplam 30 eğitim sembolü; karşılaştırma [22]: N_s = 3 alt çerçeve × Q_s = 30 → N_sQ_s = 90 (s. 10).
  - Küçük dizi: toplam Q_1 + Q_2 L_1 L_2; ardışık yöntem Q_2 = 10 ile 170 OFDM sembolü (300'e göre "excessive"); serpiştirilmiş yöntem Q_2 = 2 ile 50 sembol, "16% of the number of total symbols during the relevance interval" (s. 12). Ardışık kullanımda yük L_1L_2Q_2, "Q_2 tends to be a dozen or so" (s. 8).
  - Q_1 küçük dizi için 20 (s. 11).
- **İterasyon sayıları:** Gradyan inişi iterasyon sayısı N_iter yalnızca sembolik (Tablo III); sayısal değer **YOK**. Adım boyu η değeri **YOK**. Durdurma ölçütü **YOK** ("After a number of iterations", s. 9).

## 5. Karmaşıklık / gecikme

- **Tablo III (s. 10), aynen:**
  - Benchmark [22]: O(L_1L_2(N_sQ_s)^2 M_b^2 + L_1L_2 M_r N_s Q_s)
  - Büyük BS dizisi için önerilen: O(L_1L_2 Q_1^2 M_b^2 + L_1L_2 Q_2 + L_1L_2 M_r Q_1)
  - Küçük BS dizisi için önerilen: O(Q_1 M_r L_1L_2 + L_1L_2 Q_2 + N_iter(M_r Q_1 + Q_1(L_1L_2)^2))
- OMP'nin seçilme gerekçesi nitel: dışbükey yöntemler "more complex", Bayesçi yöntemler "usually time consuming", açgözlü yöntemler "less complex" (s. 6).
- **FLOP sayısı:** YOK. **Ölçülmüş çalışma süresi / donanım:** YOK. **Hesaplama gecikmesi tartışması:** YOK.
- **Hesaplama sırasında kanal yaşlanması:** YOK. Makale yaşlanmayı yalnızca *eğitim sembolleri arası* Doppler faz dönüşü olarak modelliyor ("we explicitly take this variation among different OFDM blocks into consideration", s. 4–5). Kestirim algoritmasının kendi koşma süresi boyunca kanalın eskimesi ya da veri alt çerçevesinde kestirilen Doppler ile ileriye öngörü yapılması ele alınmıyor (veri alt çerçevesi yalnızca Şekil 3/4'te gösteriliyor, s. 5, s. 7).
- İlgili alıntılar:
  - "Note that it is different from the channel's coherence time, which is less than one OFDM symbol duration owing to the Doppler shift. Hence, the channel variation is merely attributed to the Doppler-induced phase shift." (s. 4)
  - "we assume furthermore that the Doppler-induced variation within the duration of a single OFDM symbol is neglected ... However, the Doppler-induced variation is explicitly considered when generating channels in Section V and our simulation results verify that the channel estimation performance is not sensitive to this assumption." (s. 5)

## 6. Ana sayısal sonuçlar

Metrik: kaskad kanal NMSE (denk. (38), s. 10); Doppler/AoA/AoD/kazanç NMSE'leri benzer tanımlı. SNR ekseni 0–20 dB.

**Büyük BS dizisi (M_b = 30, Q_1 = 18, Q_2 = 12, v = 80 km/h):**
- Şekil 6 (s. 10): Önerilen yöntem SNR arttıkça iyileşir; 20 dB'de ≈ −18 dB (şekilden, yaklaşık). [22] 60/70/80 km/h için ≈ −11.4 / −10.3 / −9.4 dB civarında düzleşir (şekilden, yaklaşık). "AoAs known" 20 dB'de ≈ −21 dB, "Doppler known" ≈ −18.5 dB (şekilden, yaklaşık). Metin: düşük SNR'de sınırlayıcı Doppler doğruluğu, yüksek SNR'de açı kestirim doğruluğu (s. 10).
- Şekil 7 (s. 10, Q = 30): Kanal NMSE önce iyileşip sonra kötüleşir; Q_1 ≤ 18 iken artan Q_1 yardımcı, Q_1 > 18 iken Doppler NMSE "higher than −10 dB" olur (s. 11). En iyi kanal NMSE Q_1 ≈ 18'de ≈ −18 dB (şekilden, yaklaşık).
- Şekil 8 (s. 11, SNR = 15 dB, f_m ≈ 1700–2700 Hz): Kanal NMSE ≈ −17.5 / −18 dB civarında kararlı; Doppler NMSE ≈ −7'den ≈ −11 dB'ye iyileşir (şekilden, yaklaşık). Metin: "the estimation of Doppler has little impact on the overall channel estimation, provided that the accuracy of Doppler estimation is within a certain limit" (s. 11).
- Şekil 13 (s. 12): M_b 10 → 60 arttıkça NMSE ≈ −5 dB'den ≈ −20.5 dB'ye (şekilden, yaklaşık); ~30'dan sonra doygunlaşma.
- Şekil 14 (s. 13): M_r 20 → 120 için ≈ −16.6 → −17.9 dB (şekilden, yaklaşık); metin: RIS boyutunun "modest impact".

**Küçük BS dizisi (Q_1 = 20):**
- Şekil 9 (s. 11): Açı kestirimi rafine öncesi/sonrası benzer; kazanç kestirimi rafine sonrası belirgin iyileşir (20 dB'de rafine öncesi ≈ −1.7, rafine ≈ −11.1, baseline ≈ −13.3 dB; şekilden, yaklaşık).
- Şekil 10 (s. 12, v = 80 km/h, [22] için Q_s = 20, N_s = 3): 20 dB'de önerilen ≈ −11.6, baseline (Doppler bilinen) ≈ −13.3, [22] ≈ −3.9 dB (şekilden, yaklaşık).
- Şekil 11 (s. 12, SNR = 15 dB): f_m arttıkça RIS AoD kestirimi kötüleşir; kanal NMSE "slightly deteriorated, remains generally low" (s. 11); ≈ −11 dB civarı (şekilden, yaklaşık).
- Şekil 12 (s. 12): Serpiştirilmiş Q_2 = 2/3, ardışık Q_2 = 10'u yener; ardışık Q_2 = 3/5 belirgin kötü.
- Şekil 15 (s. 13): M_r arttıkça rafine kanal NMSE "Doppler known" baseline'ına yaklaşır (120'de ≈ −14 dB; şekilden, yaklaşık).

BER / SE / erişilebilir hız sonuçları: **YOK** (yalnızca NMSE raporlanıyor).

## 7. Varsayımlar ve sınırlar

- BS–RIS kanalı quasi-static (statik BS, statik RIS) (s. 3); Doppler yalnızca RIS–kullanıcı bağlantısında.
- c_{l2}, φ^R_{l2}, f_{l2} bir çerçeve ("relevance interval", 300 sembol) boyunca sabit (s. 4; Tablo II).
- Tek OFDM sembolü içindeki Doppler değişimi kestirimde ihmal (simülasyonda dahil) (s. 5).
- BS AoA'lar çerçeve boyunca sabit (ortak destek, MMV) (s. 6).
- CP > maks. gecikme; N_p ≥ D (s. 3–4).
- Doğrudan kanal kestirimin dışında (s. 3).
- RIS yansıması frekanstan bağımsız, birim genlik (s. 5).
- Tek kullanıcı, tek antenli kullanıcı, uplink; RIS ULA (UPA'ya genişletilebilir denir, dipnot 1, s. 3).
- Küçük dizi Aşama I'de Doppler terimi zamanla sabit varsayılır (s. 8).
- Mükemmel CSI varsayımı yok (konu zaten CSI kestirimi); ama çalışma **yalnızca kestirim** yapar, kestirilen kanalla RIS faz tasarımı / hız sonucu yoktur.
- Çalışma süresi, gecikme ve hesaplama süresince yaşlanma yok (Bölüm 5).
- Yorum (iç tutarsızlıklar, alıntılamadan önce dikkat):
  - s. 4: T_c'nin "less than one OFDM symbol duration" olduğu söyleniyor; oysa s. 9'daki sayılarla T_c ≈ 55.6 µs ve sembol süresi 4.2 µs, yani T_c ≈ 13 sembol. Metin ile sayılar çelişiyor.
  - "B" hem bant genişliği (s. 3) hem Tablo II'de alt taşıyıcı aralığı (240 KHz) için kullanılıyor; T_s de hem 1/Δf (s. 4, s. 9) hem örnekleme aralığı 1/B (s. 4) için kullanılıyor.
  - 80 km/h, 30 GHz'de f_m = v/λ ≈ 2.22 kHz → D_s ≈ 4.44 kHz; Tablo II'deki 4500 Hz bununla tutarlı (yuvarlanmış). Bu hesap bana ait.

## 8. Tezle bağlantı

- **Kontrolcüdeki yeri — ön uç kestirici (Yorum):** Bu yöntem gecikme-farkında RIS kontrolcüsünün girişine, *ölçülmüş Doppler* kaynağı olarak oturabilir: yol başına f_s kestirimi (denk. (20)/(29)) doğrudan f_d'yi verir; tezdeki x = ΔT·f_d ölçeğini ve dolayısıyla Adam adım sayısını / güncelleme periyodunu seçmek için kullanılabilir. Optimize edici ya da taban çizgisi olarak **kullanılamaz** — RIS faz optimizasyonu içermiyor.
- **Kestirim gecikmesinin kendisi (Yorum):** Makale çalışma süresi vermediği için, kontrolcüye bağlanacaksa kestiricinin koşma süresi bizim tarafımızdan ölçülmeli; aksi hâlde "efektif hız" çerçevesinde bu gecikme hesaba girmez. Tablo III'teki küçük dizi karmaşıklığında N_iter(…Q_1(L_1L_2)^2) terimi iterasyon sayısına doğrusal büyüyor — tezdeki "adım sayısı × adım maliyeti" bakışıyla aynı yapı.
- **Pilot süresi = gecikme (Yorum):** Eğitim sembolleri de bir gecikme bütçesidir: büyük dizi 30 sembol × 4.2 µs ≈ 126 µs (CP hariç; hesap bana ait), bu T_c ≈ 55.6 µs'nin (s. 9) üzerinde. Yani bu senaryoda kestirim bittiğinde kanal T_c'nin ötesinde ilerlemiş oluyor; makale bunu Doppler'i açıkça kestirerek çözüyor ama kestirimin *veri alt çerçevesine* aktarılmasını (öngörü) göstermiyor. Bu, tez savıyla uyumlu bir boşluk: kestirim/hesaplama süresinin, Doppler ile birlikte sonuca giren birinci sınıf bir değişken olduğu.
- **Ön kayıtlı doğrulama senaryosu için yeniden kullanılabilir parametreler (hepsi PDF'ten):** f_c = 30 GHz; alt taşıyıcı aralığı 240 KHz; N = 256; N_p = 16; τ_D = 250 ns; v = 80 km/h (tarama 60–80 km/h, f_m ≈ 1700–2700 Hz); D_s = 4500 Hz; M_r = 100; L_1 = 3; L_2 = 5; çerçeve 300 OFDM sembolü; M_b = 30; SNR 0–20 dB; Saleh–Valenzuela, açılar [−π/2, π/2] (s. 9, Tablo II; s. 10).
  - Yorum: Tezin geniş bant modeliyle (tüm alt taşıyıcılara tek faz vektörü) doğrudan uyumlu, çünkü makale de RIS RC'sini alt taşıyıcıdan bağımsız alıyor (denk. (8), s. 5). Ancak N = 256 alt taşıyıcı ve 240 kHz aralık, tezdeki K_opt alt küme seçiminin anlamlı olacağı bir rejim; N·Δf ≈ 61.44 MHz (hesap bana ait), W_c = 2000 KHz → bant boyunca çok sayıda tutarlılık bandı, yani alt küme seçiminin maliyetli olabileceği bir senaryo.
  - Yorum: Tek kullanıcı ve uplink; tezin çok kullanıcılı eksenine doğrudan taşınamaz.
- **Tez iddialarıyla ilişki:**
  - Destekleyici: "A high Doppler makes the channel time varying, which may hence become outdated when relying on traditional methods and gravely degrades the performance." (s. 2) — eskimiş bilginin performansı düşürdüğü ve Doppler'in tasarım değişkeni olduğu yönünde.
  - Destekleyici: [22] (Doppler'i ihmal eden yöntem) hız 60 → 80 km/h arttıkça kötüleşiyor (Şekil 6, s. 10) — zamanlama/yaşlanmayı yok sayan yöntemin sıralamada geriye düştüğü bir örnek (Yorum: bu kestirim düzeyinde, hesaplama gecikmesi değil pilot zamanlaması üzerinden).
  - Nötr / sınırlayıcı: Makale hesaplama gecikmesinden hiç söz etmiyor; tezin "hesaplama gecikmesi birinci sınıf kısıt" savını ne doğruluyor ne çürütüyor. Karmaşıklık yalnızca O(·) düzeyinde.
  - Olası çelişki: Yok bulunmadı. (Yorum: Şekil 8'deki "Doppler kestirimi belli bir sınır içinde olduğu sürece genel kanal kestirimine az etki" ifadesi, tezde Doppler hassasiyetinin kontrolcü kararlarını ne kadar etkileyeceğini sorgulatabilir; kontrolcü x = ΔT·f_d'yi kaba bir Doppler ile seçiyorsa bu bir destek de sayılabilir.)
