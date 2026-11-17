# 03 — Xu vd. (2023), RIS destekli yüksek hareketlilikte kanal kestirimi

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/03_Xu_HighMobility_CE.pdf` (17 sayfa, tamamı okundu).
Sayfa atıfları **derginin basılı sayfa numaralarıdır** (s. 718–734); PDF sayfa indeksi = basılı sayfa − 717.
PDF'te geçmeyen her bilgi "YOK" olarak yazıldı. Kendi çıkarımlarım "Yorum" etiketlidir.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Chao Xu, Jiancheng An, Tong Bai, Shinya Sugiura, Robert G. Maunder, Zhaocheng Wang, Lie-Liang Yang, Lajos Hanzo (s. 718)
- **Başlık:** "Channel Estimation for Reconfigurable Intelligent Surface Assisted High-Mobility Wireless Systems" (s. 718)
- **Dergi:** IEEE Transactions on Vehicular Technology, Vol. 72, No. 1, January 2023 (s. 718 üst bilgi)
- **Sayfalar:** 718–734 (ilk sayfa üst bilgisi "718", son sayfa "734")
- **DOI:** 10.1109/TVT.2022.3203818 (s. 718, "Digital Object Identifier")
- Tarihler: alındı 10 Şubat 2022; revize 18 Temmuz 2022; kabul 29 Ağustos 2022; yayın 2 Eylül 2022; güncel sürüm 16 Ocak 2023 (s. 718 dipnot)

**Verilen künyeyle karşılaştırma** ("IEEE TVT, vol. 72, no. 1, pp. 642–658, Jan. 2023"):
- Dergi, cilt (72), sayı (1), ay/yıl (Ocak 2023): **UYUŞUYOR**
- Sayfalar: **UYUŞMUYOR** — PDF'te 718–734 (17 sayfa); verilen 642–658 (o da 17 sayfa ama farklı aralık). Tezde **718–734** kullanılmalı.

---

## 2. Problem ve katkılar

- Problem: Mevcut RIS kanal kestirimi teknikleri blok sönümleme (çerçeve boyunca sabit kanal) varsayıyor; yüksek Doppler'de bu "irreducible error floors"a yol açıyor (s. 718 Özet; s. 719).
- Katkı 1 — "New RIS-aided high-mobility system design": zamanla değişen Ricean sönümleme; LoS bileşeninde AoA/AoD ve Doppler kayması Δf_LOS, NLoS bileşeni Clarke modeli (s. 720).
- Katkı 2 — "Novel ON/OFF-based MMSE CSI estimation technique": (1+M) pilot zaman dilimi; yalnız geçmiş (N_w − 1) çerçeve + mevcut çerçevenin pilotları kullanılıyor (gelecek çerçeveler değil), çünkü RIS faz yapılandırması için "instantaneous CSI" gerekiyor; çarpımsal RIS sönümleme korelasyon fonksiyonları "for the first time in the literature" modelleniyor (s. 720).
- Katkı 3 — Analitik + sayısal doğrulama: Lemma 1/2, Önerme 1/2 ile ulaşılabilir hız ifadeleri (Tablo II, s. 724); "for a vehicle travelling at a speed as high as 90 mph, employing a low-complexity RIS at the cell-edge using as few as 16 RIS elements is sufficient" (s. 718 Özet; s. 720).
- Tablo I'de (s. 720) kendi yöntemini "Narrowband single-user", "ON/OFF-based MMSE" olarak, AoA/AoD, Δf_LOS ve yüksek f_d'ye uyumlu tek çalışma olarak konumluyor.

---

## 3. Sistem modeli

| Öğe | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı | 2.6 GHz (S-band) | s. 721 §II-A; s. 727 Tablo III |
| Bant genişliği | 100 kHz | s. 721; Tablo III |
| Sembol hızı | f_s = 100 kHz ("C&C link") | s. 721 |
| Alt taşıyıcı sayısı | **YOK** (dar bant, düz sönümleme: "assumed to be flat") | s. 721 |
| Alt taşıyıcı aralığı | **YOK** | — |
| Dalga biçimi | Tek taşıyıcılı dar bant; LPSK/QAM (QPSK, 16QAM, 64QAM) ve Gauss girdi; OFDM **YOK** | s. 723 Lemma 2; s. 729–730 Şek. 7–9 |
| BS anteni | 1 ("a single antenna is used both at the source and at the destination") | s. 721 §II-A |
| Kullanıcı anteni / sayısı | 1 anten, tek kullanıcı ("Narrowband single-user") | s. 721; s. 720 Tablo I |
| RIS eleman sayısı | M = M_y M_z, UPA, d = λ/2; incelenen M = 4, 8, 16, 32 | s. 722 Den. (6); s. 729 Şek. 6(c); s. 730 Şek. 9 |
| Hız(lar) | 45, 90, 135 mph (Şek. 6(d)); 40 mph (Şek. 9 başlığı — aynı şeklin içinde "v=90 mph" yazıyor, metin de 90 mph diyor: **PDF'te iç tutarsızlık**) | s. 729; s. 730 |
| Doppler | Normalize: f_d^SD = f_d^RD = v f_c /(c f_s), f_d^SR = 0. **Sayısal Doppler değeri PDF'te YOK.** | s. 721 Den. (3) sonrası; s. 727 Tablo III |
| Uyum zamanı örneği | 90 mph'de korelasyonun 0.5 üstünde kaldığı süre "only 51 symbols" | s. 721 §II-A |
| Şek. 4(b) lejantı | "Coherence time=20 symbol periods at 0.95 correlation"; "40 symbol periods at 0.82 correlation" | s. 728 Şek. 4(b) |
| Kanal modeli | Zamanla değişen Ricean: LoS (Doppler kaymalı, 3B koordinatlardan) + NLoS (Clarke, korelasyon J_0(2π f_d |n−n'|)); kaskad BS-RIS-kullanıcı çarpımsal | s. 721 Den. (2)–(5); s. 722 Den. (7)–(8); s. 726 Den. (30) |
| Ricean K | K^SD = −6 dB, K^SR = 0 dB, K^RD = 0 dB | Tablo III |
| Yol kaybı | γ^SD = 3.8, γ^SR = γ^RD = 2.0, PL_0 = 30 dB | Tablo III |
| Koordinatlar | S (0,0,0), R (300,10,0), D başlangıç (290,−10,0); x_D = 290 − v n / f_s | Tablo III; s. 727 §IV-A |
| Gürültü | −174 dBm/Hz; gürültü gücü −174 + 50 = −124 dBm | Tablo III; s. 727 |
| Gecikme yayılımı | **YOK** (düz sönümleme; RIS yansımalı gecikme α/(2πf_c) ≤ 1/f_c ihmal edilebilir) | s. 721 |
| RIS fazı alt taşıyıcı başına mı ortak mı | Alt taşıyıcı yok → **YOK/uygulanamaz**. Faz, sembol indeksine göre α_{u,t} olarak yazılıyor (sembol başına) | s. 722 Den. (10); s. 723 Den. (13) |
| Faz modeli | Sürekli birim genlik |α|=1; ayrıca 1-bit ve 2-bit kuantalama (Şek. 9(c)) | s. 722; s. 730 |

---

## 4. Yöntem

- **Kestirilen:** doğrudan bağlantı h^SD ve M adet kaskad yansımalı bağlantı h^SRD_m (eleman başına skaler) (s. 723 Önerme 1; s. 725–726).
- **Pilot deseni (ON/OFF):** her çerçevenin ilk (1+M) sembolü pilot; ilk dilimde RIS kapalı → h^SD; sonraki M dilimde elemanlar tek tek açılır, doğrudan bağlantı kestirimi çıkarılır (Den. 17, 28) (s. 724; s. 726).
- **Pilot oranı:** η_p = (M+1)/N_f (s. 722); çerçeve uzunluğu N_f = ⌈(M+1)/η_p⌉ (s. 727). RIS olmadan η_p = 1/N_f (s. 730).
- **MMSE interpolasyon:** pencere N_w çerçeve; ağırlıklar (w)^* = C^{-1} e (Den. 24, SD; Den. 31, SRD), ağırlıklar "different for each symbol in each frame" (s. 725–727). MSE ifadeleri Den. (25), (32); blok sönümleme alt sınırı Den. (26), (32) (CRB ile ilişkili).
- **Pencere seçimi:** "the choice of (N_w = 10) is assumed in the rest of this paper" (s. 728 §IV-C).
- **Karşılaştırılan tabanlar:** ON/OFF-LS (Den. 18) ve DFT-LS (Den. 19–20; DFT eğitim matrisi) — durağan sistem için; ayrıca doğrudan-bağlantı-yalnız geleneksel MMSE (geçmiş ⌊N_w/2⌋ + gelecek çerçeveler) (s. 724–725, Şek. 3).
- **Neden DFT değil ON/OFF:** DFT deseni kanalın (M+1) sembol boyunca sabit olmasını gerektiriyor; Clarke zamanla değişimi için ON/OFF seçiliyor (s. 725 §III-B).
- **Faz optimizasyonu:** kapalı biçim eş-fazlama, α̂^m = ĥ^SD (ĥ^SRD_m)^* / |ĥ^SD ĥ^SRD_m| (s. 723 Önerme 1; s. 732 Ek A). Yinelemeli optimizasyon yok.
- **Yineleme sayısı:** **YOK** (yöntem yinelemeli değil).
- **Simülasyon:** "at least 10^3 frames … at least 100 b-errors" (s. 727); kod: github.com/cx1g08/RIS_Ricean [70] (s. 727; s. 734).

---

## 5. Karmaşıklık / gecikme

- Karmaşıklık mertebesi (O(·)), FLOP, çalışma süresi: **YOK**. "Low-complexity RIS" ifadesi eleman sayısına (M=16) atıf, hesaplamaya değil (s. 718 Özet).
- Gecikmeye ilişkin birebir alıntılar:
  - "the recent developments in micro-electromechanical systems have enabled the RIS phase shifts to be adjusted near-instantaneously [7], which prevents energy-efficiency loss due to the phase-tuning latency." (s. 718 §I)
  - "In the absence of active RF chains, the RIS does not impose signal processing latency." (s. 722 §II-E) — yayılım/yansıma bağlamında.
  - "upon obtaining the estimated CSI of the u-th frame, a short interval is required for RIS configuration before data transmission. This control information can be conveyed by a separate link such as bluetooth, and the associated time duration has negligible impact on the data rate compared to the pilot overhead, as assumed in [27], [28], [29], [30], [31]." (s. 724 §III)
- **Hesaplama sırasında kanal eskimesi:** **hesaba katılmıyor.** Kestirim/yapılandırma süresi ihmal edilebilir kabul ediliyor (yukarıdaki s. 724 alıntısı). Pilot→veri arası eskime ise MMSE interpolasyonunun sembol başına ağırlıklarıyla modelleniyor (s. 725 Den. 21) — bu, *pilot gecikmesi*ni ele alır, *hesaplama gecikmesi*ni değil.
- Yorum: Her sembol ve her eleman için N_w×N_w kovaryans tersi (Den. 24, 31) gerekiyor; makale bunun maliyetini tartışmıyor.

---

## 6. Ana sayısal sonuçlar

- **NMSE vs N_w (Şek. 5(a)-(b), s. 728):** şekil üzerindeki işaretler — v=45 mph, η_p=20%: "3.2 times" (N_w 2→10) ve "1.3 times" (10'un ötesi); v=90 mph, η_p=40%: "6.4 times" ve "1.2 times". Metin: N_w=10'un ötesindeki iyileşme "substantially smaller" (s. 728).
- **NMSE sıralaması (Şek. 5(c)-(d)):** MMSE < DFT-LS < ON/OFF-LS; 90 mph'de blok-sönümleme CRB'ye boşluk büyüyor (s. 728). Ayarlar: P_t=26 dBm, N_w=10, M=16 (Şek. 5 başlığı).
- **BER=10^-4 güç-verimliliği kazancı (Şek. 8, s. 729–730):**

| Senaryo | Kusursuz CSI | Önerilen MMSE | η_p (Şek. 8 lejantı) |
|---|---|---|---|
| M=4, 16QAM, 45 mph | 13 dB | 14 dB | 15% |
| M=16, 16QAM, 45 mph | 18 dB | 20 dB | 25% |
| M=16, 16QAM, 90 mph | 17 dB | 24 dB | 40% |
| M=16, 64QAM, 45 mph | 17 dB | 18 dB | 30% |

  (Şek. 8(d) panelindeki etiket "8 dB" okunuyor; metin "18 dB" diyor — metin esas alındı.)
- ON/OFF-LS ve DFT-LS: Şek. 8(a)–(d)'de hata tabanı, hedef BER'e hiç ulaşamıyor (s. 730–731).
- **Eleman sayısı (Şek. 9, s. 730):** N_f = 35, QPSK; η_p: SD-yalnız 2.9%, M=4 14.3%, M=8 25.7%, M=16 48.6%, M=32 94.3%. Normalize güçte M=32, M=16'dan kötü. M=16 ile 90 mph'de 23.8 dB kazanç; 26.1 − 23.8 = 2.3 dB fark "relatively insignificant".
- **Kuantalama (Şek. 9(c)):** 1-bit ile 16.9 dB kazanç; 2-bit "similar performance to the case of idealistic continuous-phase RIS" (s. 730).
- **Ulaşılabilir hız (Şek. 7, s. 729):** tepe (1−η_p)BPS: 3.6 / 3.2 (Şek. 7(b)), 3.2 (Şek. 7(c), η_p=20%), 2.67 (Şek. 7(d), η_p=1/3, 90 mph). ON/OFF/DFT-LS tam (1−η_p)BPS'e ulaşamıyor.
- **Kullanıcı konumu (Şek. 10, s. 731):** referans kapsama P_t = 40 dBm; N_f = 68 (45 mph), N_f = 42 (90 mph); 45 mph'de RIS ile kapsama x_D = 470 m'ye kadar; 90 mph'de SD-yalnız x_D > 190 m'de kapsama dışı, RIS ile x_D = 430 m'ye kadar.
- **Yol kaybı üssü (Şek. 11, s. 731–732):** 45 mph'de kazanç γ^SD > 2.2 için artıyor, SD-yalnız γ^SD > 3.8'de kapsama dışı; 90 mph'de SD-yalnız γ^SD > 3.6'da kapsama dışı, RIS 2.4 < γ^SD ≤ 4.4 aralığında kapsamayı sürdürüyor.
- Giriş bağlamı (sonuç değil): 5G 140 km/h araç, 500 km/h tren; uçak 1080 km/h; alçak irtifa İHA 108 km/h (s. 719).

---

## 7. Varsayımlar ve sınırlar

- Tek anten BS ve kullanıcı, tek kullanıcı, dar bant düz sönümleme (s. 721; Tablo I). Çok antenli BS'ye "directly applied" denebileceği ama pilot yükü ve pencerenin büyüyeceği belirtiliyor (s. 721).
- Kestirim + RIS yapılandırma süresi ve kontrol bağlantısı ihmal edilebilir (s. 724).
- Bütün RIS elemanları aynı maksimum Doppler'i paylaşıyor (s. 722 §II-D).
- İstatistikler (K, yol kaybı, f_d, koordinatlar) MMSE ağırlıkları için biliniyor kabul ediliyor (Den. 23, 30 kovaryansları model parametrelerinden kuruluyor) — Yorum: kovaryans bilgisinin nasıl elde edileceği tartışılmıyor; bu yüzden "genie" istatistik varsayımı var.
- Uzaysal korelasyon (d < λ/2) yöntem açısından etkisiz sayılıyor; d = λ/2 (s. 722).
- f_d^SR = 0 (BS ve RIS sabit) (Tablo III).
- Pilot sayısı M ile doğrusal büyüyor; M=32'de η_p = 94.3% (N_f=35) — büyük RIS'te ölçeklenmiyor (s. 730).
- Düşük SNR'de MMSE, DFT-LS'den daha iyi MSE garanti etmiyor (Remark 1, s. 727).
- Gerçek ölçüm/deney **YOK**; yalnız simülasyon.

---

## 8. Tezle bağlantı

**Gecikme-farkında kontrolcüye nereye takılır**
- Yorum — **Ön uç kestirici:** ON/OFF-MMSE interpolatörü, ölçülen Doppler'e (f_d, Clarke J_0 korelasyonu) dayalı Wiener ağırlıklarıyla sembol başına ĥ üretiyor; kontrolcünün "ölçülen Doppler" girdisini zaten kullanan doğal bir ön uç. Ağırlıklar her t için ayrı olduğundan, ölçülen hesaplama gecikmesi ΔT kadar ilerideki sembol için de ağırlık kurulabilir (bu, makalede **yapılmıyor**).
- Yorum — **Optimizasyon kolu olarak:** Tek antenli kapalı biçim eş-fazlama (s. 732) tezin MU-MISO/geniş bant ortamına doğrudan taşınmaz; tezde yalnız "sıfır maliyetli tek-kullanıcı üst referans" olarak anılabilir.
- Yorum — **Taban çizgisi olarak:** Blok-sönümleme varsayan ON/OFF-LS / DFT-LS (Den. 18–20) hata tabanına çarpıyor; tezde "eskime-kör kestirim" tabanı olarak yeniden üretilebilir. CLAUDE.md'deki "zayıf taban" kuralı gereği, karşılaştırmada kestiricinin N_w ve η_p ayarları da taranmalı.
- Yorum — **Güncelleme periyodu ile ilişki:** η_p = (M+1)/N_f ve N_f seçimi (Şek. 6(a), 7(b): η_p arttıkça hız düşüyor; yüksek Doppler'de daha yüksek η_p gerekli, s. 729) kontrolcünün "güncelleme periyodu" ekseniyle aynı ödünleşimi pilot tarafında gösteriyor.

**Ön kayıtlı doğrulama senaryosu için yeniden kullanılabilir parametreler** (hepsi Tablo III ve §IV-A, s. 727)
- f_c = 2.6 GHz, B = f_s = 100 kHz, gürültü −174 dBm/Hz, S(0,0,0), R(300,10,0), D(290,−10,0), γ^SD=3.8, γ^SR=γ^RD=2.0, PL_0=30 dB, K^SD=−6 dB, K^SR=K^RD=0 dB, v ∈ {45, 90, 135} mph, M ∈ {4, 8, 16, 32}, N_w=10, N_f ∈ {35, 42, 68}, hedef BER 10^-4, P_t referansı 40 dBm. Açık kod: github.com/cx1g08/RIS_Ricean (s. 727 [70]).
- Yorum (hesap, PDF'te yok): Bu parametrelerle normalize Doppler f_d = v f_c/(c f_s) yaklaşık 45 mph → 1.74×10^-3, 90 mph → 3.49×10^-3 (c = 3×10^8 m/s, 1 mph = 0.44704 m/s varsayımıyla; mutlak Doppler ≈ 174 Hz ve ≈ 349 Hz). Tezdeki x = ΔT·f_d ile sembol cinsinden doğrudan eşlenebilir; teze girmeden önce bir betikle (`thesis_exp/` altında) üretilmeli.
- Yorum — Uyumsuzluk: senaryo dar bant, tek anten, tek kullanıcı; tezin OFDM (K_opt alt taşıyıcı) ve çok kullanıcılı ekseniyle birebir değil. Doğrulama senaryosu ancak "tek kullanıcı, tek alt taşıyıcı" alt durumu olarak kullanılabilir.

**Tez iddialarını destekleyen / çelişen ifadeler**
- Destekler: blok-sönümleme varsayımının yüksek Doppler'de "irreducible error floors" ürettiği (s. 718–719; Şek. 4(b), 8) — kanal yaşlanmasının sonucu belirlediği iddiasıyla uyumlu.
- Destekler: "the coherence time over which the time correlation function is higher than 0.5 is estimated to cover only 51 symbols" (s. 721) — 90 mph'de bütçenin sembol ölçeğinde olduğunu gösteriyor.
- Çelişir/göz ardı eder: Hesaplama ve yapılandırma süresi "negligible impact on the data rate compared to the pilot overhead" (s. 724) kabul ediliyor; faz kaydırıcıların "near-instantaneously" ayarlandığı vurgulanıyor (s. 718). Yorum: Bu, tezin "hesaplama gecikmesi birinci sınıf kısıttır" savının tam karşısındaki varsayım; makale yalnız kapalı-biçim (O(M)) faz kullandığı için bu varsayım orada tutarlı, ama yinelemeli MISO/OFDM optimizasyonuna genellenemez. Tezde "literatürün örtük sıfır-gecikme varsayımı" örneği olarak alıntılanabilir.
- Nötr: 1-bit kuantalama ile 16.9 dB, 2-bit ≈ sürekli (s. 730) — tezin ayrık faz (1/2/3 bit) işi için tek-kullanıcı dar bant referans noktası; ama farklı sistem olduğundan doğrudan karşılaştırma yapılmamalı (Yorum).
