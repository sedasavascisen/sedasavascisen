# 08 — Siriwanitpong vd. (2025), 1D CNN ile HSR OFDM kanal kestirimi

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/08_Siriwanitpong_1DCNN_HSR.pdf` (15 sayfa, tamamı okundu).
Sayfa numaraları dergi sayfalarıdır (s. 13128–13142).
Kural: sayılar yalnızca PDF'ten alındı. PDF'te bulunmayanlar "YOK" diye işaretlendi. Kendi çıkarımlarım **Yorum** diye etiketli.
Şekilden okunan değerler "şekilden yaklaşık" diye işaretlendi; bunlar metinde sayı olarak verilmiyor.

---

## 1. Künye

- **Yazarlar:** Aphitchaya Siriwanitpong (Graduate Student Member, IEEE), Kosuke Sanada (Member, IEEE), Hiroyuki Hatano (Member, IEEE), Kazuo Mori (Member, IEEE), Pisit Boonsrimuang
- **Kurumlar:** Mie University (Japonya); King Mongkut's Institute of Technology Ladkrabang (KMITL, Tayland)
- **Başlık:** "Deep Learning-Based Channel Estimation With 1D CNN for OFDM Systems Under High-Speed Railway Environments"
- **Dergi:** IEEE Access, Vol. 13, s. 13128–13142, 2025 (Research Article)
- **DOI:** 10.1109/ACCESS.2025.3531009
- **Tarihler:** Alındı 10 Aralık 2024; kabul 13 Ocak 2025; yayın 17 Ocak 2025; güncel sürüm 23 Ocak 2025 (s. 13128)
- **Lisans:** CC BY 4.0

**RIS var mı? HAYIR.** Makalede RIS, yansıtıcı yüzey ya da faz optimizasyonu hiç geçmiyor. Konu, tek bağlantılı (SISO) bir OFDM alıcısında pilot tabanlı kanal kestirimi. RIS yalnızca kaynakçada bir kez geçiyor: [11] "RIS-assisted OFDM systems" başlıklı bir ELM çalışması (s. 13141). O çalışma da metinde RIS bağlamında anılmıyor.

---

## 2. Problem ve katkılar

**Problem (s. 13128–13129):** Yüksek hızlı demiryolunda (HSR) hızlı çok yollu sönümleme ve güçlü Doppler, LS kanal kestirimini bozuyor. Önceki derin öğrenme (DL) kestiricileri ise yüksek hesaplama karmaşıklığı taşıyor. Sabit güzergâh ve düzenli tren seferleri, kanalın "depolanmış büyük veriden" öğrenilebileceği gerekçesiyle kullanılıyor (s. 13129).

**Katkılar (s. 13129, madde listesi):**
1. HSR'de OFDM; WINNER II kanal modeli.
2. **Şema I:** 1D CNN, tam pilot (blok tipi) sembollerden LS-CFR alıyor ve **kanal sınıfını sınıflandırıyor**. "Predicting phase"de sınıfa karşılık gelen CFR'yi **bellekten** getiriyor.
3. **Şema II:** "Restructured 1D CNN". Seyrek (scattered) pilot kullanıyor, girdi daha küçük ve tek evrişim katmanı var. Amaç hem iletim verimliliğini artırmak hem karmaşıklığı düşürmek.
4. Benzetimde iki şema da NMSE ve BER'de LS'yi ve bi-GRU [17] tabanlı yöntemi geçiyor.
5. Üç DL yöntemi (1D CNN, restructured 1D CNN, bi-GRU) için "ayrıntılı hesaplama karmaşıklığı analizi". Bu analiz pratikte **yalnızca parametre sayısından** oluşuyor (bkz. §5).

---

## 3. Sistem modeli

| Büyüklük | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı fc | 3.5 GHz | Tablo 3, s. 13137 |
| Bant genişliği | 10 MHz | Tablo 3 |
| FFT noktası / alt taşıyıcı N | 64 | Tablo 3; Alg. 1–2 |
| Alt taşıyıcı aralığı | **YOK** (açıkça verilmiyor) | — |
| Alt çerçeve başına sembol | 14 (2 slot × 7 OFDM sembolü) | Tablo 3; Şekil 3, s. 13132 |
| Koruma aralığı (GI/CP) uzunluğu | **YOK** | — |
| Modülasyon | QPSK | Tablo 3 |
| SNR aralığı | 0–30 dB | Tablo 3 |
| Tren hızı | 50, 300, 500 km/h | Tablo 3; s. 13137 |
| Doppler kayması | "yaklaşık" 160 Hz, 970 Hz, 1620 Hz (sırasıyla) | s. 13137, sol sütun |
| Doppler formülü | f_dop = (v/c)·f_car, c = 3×10⁸ m/s | Denk. (7), s. 13132 |
| Kanal modeli | WINNER II senaryo D2a (Rician: LoS + yansımalar) | §III-B ve Tablo 1, s. 13132 |
| Gecikme profili (Tablo 1) | 8 yol; gecikmeler 0/50/60/85/105/115/130/210 ns; güçler 0/−20.1/−17.2/−16.5/−20.4/−15.7/−17.7/−17.3 dB | Tablo 1, s. 13132 |
| Profil sayısı | Üç profil: 8, 7 ve 6 yol | s. 13136–13137 |
| Rician K-faktörü | **YOK** | — |
| 3GPP HST (TS 38.101/36.104) kanalı | **YOK**: kullanılmıyor, WINNER II D2a kullanılıyor | — |
| Dalga biçimi | OFDM, LTE çerçeve yapısı [33]; LS + ZF eşitleme | §III-A, §III-C; Denk. (5)–(6) |
| Pilot düzeni | Şema I: her slotun 1. sembolü tam pilot (Z_pilot = 0). Şema II: seyrek pilot, I_pilot(p) = I_int + p(Z_pilot+1), N_pilot = N/(Z_pilot+1) | Denk. (8)–(9), s. 13133 |
| Varsayılan Z_pilot (Şema II) | 5 ("LTE standardına göre"), N_pilot = 11 | Alg. 2; s. 13137 |
| Anten sayısı | Tek anten (SISO); MIMO yok | Şekil 2, s. 13131 |
| Kanal modeli adı | Alıcı "linear wireless channel" | s. 13136 |

**Yorum:** 10 MHz / 64 = 156.25 kHz bir aralık *ima ediliyor* ama makalede yazmıyor. Bu durumda sembol süresi yaklaşık 6.4 µs + GI olur ve 14 sembollük "alt çerçeve" LTE'nin 1 ms'lik alt çerçevesine karşılık gelmez. Makale yalnızca LTE'nin *yapısını* ödünç alıyor, zaman ölçeğini almıyor. Doppler değerleri Denk. (7) ile tutarlı: 500 km/h ve 3.5 GHz için 1620 Hz.

---

## 4. Yöntem

**Ne kestiriliyor:** Frekans bölgesi kanal yanıtı (CFR) H[k,n]. Ağ **regresyon yapmıyor, sınıflandırma yapıyor**. Çıkışı bir kanal sınıfı C′_class; bu sınıf, eğitimde yüksek SNR'de kaydedilmiş bir CFR'ye (H_DLS ya da H_DLF) **bellekte eşleniyor** (s. 13134–13135, Şekil 5–6).

**1D CNN katmanları (§IV-A, s. 13133; Tablo 2, s. 13134):**

| Katman | Şema I | Şema II |
|---|---|---|
| Girdi | 1 × 2N | 2N_pilot × 1 |
| Evrişim | 9(64), 5(64), 5(32), 3(64), 3(32) | 1(64) |
| Aktivasyon | Tanh | Tanh |
| Havuzlama | Average | Average |
| Tam bağlı | Softmax | Softmax |
| Çıkış | Classification | Classification |

- Girdi, LS-CFR'nin Re/Im birleştirmesi (Denk. 15) ve [−1, 1] aralığına max-min normalizasyonu (Denk. 16). Şema I'de C^{1×64} → R^{1×128}; Şema II'de P̂_scatt ∈ C^{1×11} → R^{1×22} → R^{22×1} (Alg. 1–2).
- Kayıp: çapraz entropi (Denk. 14). Optimizasyon: Adam, lr 0.001, batch 15, 30 epoch (Tablo 3).
- **Eğitim verisi:** 25,920 örnek (Tablo 3). Veri %70 eğitim, %15 doğrulama, %15 test olarak bölünüyor (s. 13137). Örnekler kanal karakteristiklerinden ve "çeşitli SNR'lerden" üretiliyor; eğitim kümesi {H_IN, C_class, H_DLS} (Denk. 17) ya da {P_IN, C_class, H_DLF} (Denk. 19).
- **Sınıf sayısı:** **YOK** (verilmiyor). Sınıfların nasıl tanımlandığı da (konum mu, hız mı, profil mi) açık değil.
- **Şema I (Alg. 1, s. 13135):** Slot başına 1. OFDM sembolünden LS hesaplanıyor ve CNN sınıflandırıyor. "prediction probability ≥ 90" ise bellekteki CFR alınıp slotun 2.–7. sembolleri ZF ile eşitleniyor (Denk. 18). Aksi hâlde LS'ye dönülüyor.
- **Şema II (Alg. 2, s. 13136):** Eğitimde alt çerçevenin tamamı tam pilot gönderiliyor ve H_DLF ∈ C^{14×64} alt çerçevenin tüm sembolleri için saklanıyor. Kestirimde yalnızca 1. sembolün seyrek pilotlarıyla sınıflandırılıyor ve sınıfın 14×64'lük CFR'si bellekten okunuyor. Eşik ve LS'ye dönüş Şema I ile aynı.
- **Yeniden eğitim:** "approximately once a month" ve çevre değiştiğinde gerekiyor (s. 13135).
- LS taban çizgisinde seyrek pilotlar için kübik spline enterpolasyon kullanılıyor (Denk. 2, s. 13130).

---

## 5. Karmaşıklık / gecikme

- **Ölçülmüş duvar saati (wall-clock) çıkarım süresi: YOK.** Gecikme, ms, µs ya da işlem süresi hiçbir yerde ölçülmüyor.
- **Donanım: YOK.** CPU, GPU ya da platform belirtilmiyor.
- **FLOPs / MAC: YOK.**
- **Karmaşıklık ölçütü yalnızca parametre sayısı (§V-A, s. 13137):** "The computational complexity per model parameter and time step is O(1) [35]. Therefore, the overall complexity of each model can be evaluated based on the number of parameters in the deep learning architecture."
  - Evrişim katmanı parametresi (N_f × F + 1) × N_O; tam bağlı katman (N_FC × N_OC) + N_OC.
  - bi-GRU: 3N_I × (N_D × N_H + N_H × N_H + N_H); tam bağlı katman N_I × 2N_H × N_Io. Gizli birim sayısı 32, girdi/çıkış boyutu L = 14.
- **Tablo 4 (s. 13137), parametre sayısı:**

| Şema | Parametre |
|---|---|
| 1D CNN scheme I | 52,750 |
| 1D CNN scheme II | 19,022 |
| bi-GRU [17] | 28,544 |

- Metindeki iddia: Şema II, Şema I'e göre "approximately 60%", bi-GRU'ya göre "30%" daha az parametre kullanıyor (s. 13137). (Tablo 4'ten hesap: 1 − 19022/52750 ≈ %64; 1 − 19022/28544 ≈ %33. Metinle uyumlu.)
- Özetteki iddia: "simultaneously improve channel estimation performance, transmission efficiency, and reduce computational complexity" (s. 13128). Sonuç bölümünde: "the proposed scheme II provides less computational complexity than the existing bi-GRU-based channel estimation method" (s. 13141).
- LS'nin karmaşıklığı ve LS'ye göre ek maliyet sayısal olarak verilmiyor (**YOK**). LS için yalnızca "low computational complexity" deniyor (s. 13128, 13130).
- "Low latency" ifadesi geçmiyor. Kullanılan ifade "low computational complexity".

**Yorum:** "Düşük karmaşıklık" iddiası tamamen parametre sayısına dayanıyor. Evrişimde parametre sayısı FLOP'la orantılı değil, çünkü girdi uzunluğu çarpanı devreye giriyor. Bellekten okuma ve eşik kontrolü maliyeti de hesaba katılmıyor. Duvar saati yok. Tezin gecikme-farkında çerçevesi açısından bu iddia **gecikme kanıtı sayılmaz**.

---

## 6. Ana sayısal sonuçlar

Metinde sayı olarak verilenler:
- **Sınıflandırma doğruluğu (Şekil 7, s. 13137–13138):** Şema I (tam pilot, Z_pilot = 0) "approximately 96%". Şema II, Z_pilot = 1'de "approximately 93%". Doğruluk Z_pilot arttıkça "linearly" düşüyor ama Z_pilot = 15'e kadar "over 90%" kalıyor. Z_pilot = 5 seçimi "an accuracy exceeding 90%" veriyor. Şekilden yaklaşık: Z_pilot ≈ 30'da ~%70, ≈ 31'de ~%35.
- **NMSE tanımı:** Denk. (21), s. 13138. Referans H_ideal, "full pilot without AWGN" ile elde edilen CFR. "Ideal LS" ise gürültüsüz pilotlardan hesaplanan LS (s. 13138).

Şekillerden nitel ya da yaklaşık okunanlar (metinde sayı verilmiyor):
- **Şema I NMSE (Şekil 8):** 15 dB'nin altında hata belirgin. 15 dB'nin üstünde "stabilizes and becomes identical to the ideal LS estimation" (s. 13138). Şekilden yaklaşık: 1D CNN eğrileri ~15–16 dB'de 10⁻³'e iniyor; LS aynı NMSE'ye 30 dB'de ulaşıyor.
- **Şema I BER (Şekil 9, 50 km/h; Şekil 10, 300/500 km/h):** 15 dB'nin üstünde "about the same as the ideal channel estimation" (s. 13138–13139).
- **Şema II NMSE, Z_pilot = 2 (Şekil 11) ve Z_pilot = 5 (Şekil 12):** LS-scatt yüksek SNR'de taban yapıyor (enterpolasyon hatası). bi-GRU Z_pilot = 2'de LS'ye "nearly identical", Z_pilot = 5'te LS'den iyi. Re-1D CNN ikisini de geçiyor. Ancak 10 dB altında Z_pilot = 2'de "slightly greater error than conventional LS and bi-GRU" (s. 13139).
- **Şema II BER (Şekil 13–15):** 500 km/h'de Şema II "obviously superior" (Z_pilot = 2). Z_pilot = 5'te bi-GRU'yu özellikle 500 km/h'de geçiyor, LS ise enterpolasyon hatası nedeniyle başarısız (s. 13140).
- **BER ya da NMSE değerlerini veren bir tablo: YOK.** Bütün karşılaştırmalar şekil üzerinden.
- **Güven aralığı, tekrar sayısı, Monte Carlo sayısı: YOK.**

**Taban çizgileri ayarlanmış mı?**
- Kullanılan taban çizgileri: LS (tam pilot), LS-scatt (kübik spline), ideal LS ve bi-GRU [17]. **MMSE/LMMSE taban çizgisi sonuçlarda YOK** (MMSE yalnızca ilgili çalışmalarda anılıyor, s. 13130).
- Zaman ekseninde enterpolasyon ya da filtreleme yok: Şema I'de LS, slotun 1. sembolünden alınıp 7 sembol boyunca sabit tutuluyor. Doppler ile yaşlanmaya karşı herhangi bir izleme ya da tahmin yapılmıyor.
- Enterpolasyon türü (lineer, 2. derece, spline) **taranmıyor**: yalnızca spline kullanılıyor.
- bi-GRU'nun hiperparametreleri (32 gizli birim) sabit ve yeniden ayarlandığına dair bilgi **YOK**.
- **Sonuç:** Klasik kollar ayarlanmamış. "Zayıf taban çizgisi" riski yüksek (bkz. CLAUDE.md kuralı).

---

## 7. Varsayımlar ve sınırlar

1. **Kapalı küme sınıflandırma + bellek araması:** Çıkış, eğitimde görülmüş sonlu sayıda CFR'den biri. Test verisi aynı benzetim dağılımından (aynı 3 profil, aynı 3 hız) geliyor (s. 13137). Görülmemiş kanalda LS'ye dönülüyor (Alg. 1 satır 13; s. 13135, 13141).
2. Sabit güzergâh ve tekrar eden kanal varsayımı (s. 13129). Gerçek ölçüm verisi yok; tamamen benzetim.
3. "Ideal" referans, gürültüsüz tam pilot CFR. Yüksek SNR'de "ideal LS ile aynı" sonucu, bellekte saklanan CFR'nin zaten yüksek SNR'de alınmış olmasından kaynaklanıyor olabilir (**Yorum**).
4. Şema II, eğitimde tüm alt çerçevenin tam pilotla gönderilmesini gerektiriyor (s. 13136). Aylık yeniden eğitim varsayılıyor (s. 13135).
5. SISO, QPSK, N = 64. Gerçekçi bir LTE/NR boyutu değil. K-faktörü, GI, alt taşıyıcı aralığı ve ICI modeli verilmiyor. ICI'nin modellenip modellenmediği belirsiz (**YOK**).
6. **Tutarsızlık:** Sonuç bölümü "speeds up to 300 km/hr" diyor (s. 13141), oysa benzetimler 500 km/h'yi de içeriyor (Tablo 3).
7. Eşik "≥ 90" birimsiz yazılmış (Alg. 1–2). Büyük olasılıkla yüzde (**Yorum**).
8. Duvar saati, donanım ve FLOP verilmiyor (§5). Gelecek çalışma olarak mmWave ve "real-time, non-stable" uyarlanabilirlik anılıyor (s. 13141).

---

## 8. Tezle bağlantı

**Ön uç rolü (Yorum):**
- Gecikme-farkında RIS denetleyicisinin ön ucu, Doppler ve kanal durumunu üreten bir kestirici. Bu makale RIS içermediği için RIS'li kaskad kanal kestirimine doğrudan aktarılamaz. RIS'te kestirilmesi gereken şey eleman başına kaskad kanal; buradaki tek bağlantılı SISO CFR değil.
- Sınıflandırma + bellek yaklaşımı ancak "konum/sınıf → saklı kanal" eşlemesi olarak ön uca uyar. Bu durumda çıkış ayrık bir kod kitabı olur ve görülmemiş kanalda LS'ye geri düşülür. Tezin denetleyicisi Doppler ve adım maliyetini *ölçülmüş* değerlerden seçiyor. Bu makale ne Doppler kestirimi ne kestirim gecikmesi sağlıyor (Doppler bilinen hızdan hesaplanıyor, Denk. 7).

**Tezin olumsuz yapay zekâ bulgusunu destekleyenler (Yorum):**
- "Düşük karmaşıklık" iddiası duvar saatiyle **ölçülmemiş**, yalnızca parametre sayısıyla destekleniyor (Tablo 4). Tezin "adım başına kazanç ≠ milisaniye başına kazanç" bulgusu tam olarak bu boşluğa işaret ediyor. Makale, öğrenilen yöntemin klasiğe göre gecikmesini hiç raporlamıyor.
- Klasik taban çizgileri ayarlanmamış: MMSE yok, zaman enterpolasyonu yok, enterpolasyon türü taranmıyor. Tezin "zayıf taban çizgisi" uyarısının literatürdeki bir örneği.
- Ağ özünde bir **arama tablosu**: tek geçişli bir ağ, sonlu sayıda saklı çözümden birini seçiyor. Bu, tezdeki tek geçişli faz ağının bir çapa çözüme "donması" gözlemiyle kavramsal olarak akraba. Ağın kazancı, test kanalının eğitim kümesindeki bir sınıfla örtüşmesine bağlı.
- Gelecek çalışmada yazarlar, "real-time, non-stable" ortamlara uyarlanabilirliğin henüz çözülmediğini kabul ediyor (s. 13141).

**Tezle çelişebilecek ya da dikkat gerektirenler (Yorum):**
- Benzetimde, sabit güzergâh ve kapalı kanal kümesi varsayımı altında, DL yaklaşımı ayarsız LS'yi NMSE ve BER'de açıkça geçiyor (Şekil 8–15). Jüri "HSR'de DL kestirimi klasiği yeniyor" diye sorabilir. Yanıt: bu kazanç ayarsız LS'ye karşı ve ölçülmemiş gecikmeyle elde edilmiş; ayrıca faz optimizasyonu değil, kestirim.
- Kusurlu CSI işi (tez önceliği 2) için ilginç bir nokta: bellek yaklaşımı, düşük SNR'de LS'den bile kötü olabiliyor (Şekil 11, < 10 dB; s. 13139). "Gürültüyle eğitim ≠ gürültülü girdi" ayrımı burada da önemli.

**Yeniden kullanılabilir HSR parametreleri (yalnızca PDF'teki değerler):**
- fc = 3.5 GHz; BW = 10 MHz; N = 64; QPSK; SNR 0–30 dB (Tablo 3)
- v = 50/300/500 km/h → f_D ≈ 160/970/1620 Hz (s. 13137; Denk. 7)
- WINNER II D2a gecikme profili, 8 yol (Tablo 1)
- LTE benzeri çerçeve: 2 slot × 7 sembol; Z_pilot = 5 → N_pilot = 11 (Şekil 3; Alg. 2)
- **Yorum:** 500 km/h ve 3.5 GHz, tezin hareketlilik ekseni için gerçekçi bir üst Doppler sınırı (~1.6 kHz) olarak atıf yapılabilir. Ancak tezin sayıları kendi betiklerinden gelmeli; bu makaleden yalnızca senaryo parametresi olarak alıntı yapılabilir.
