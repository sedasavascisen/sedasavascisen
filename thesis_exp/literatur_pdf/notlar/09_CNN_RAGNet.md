# 09 — CNN-RAGNet: RIS destekli MIMO-OFDM'de CFO kestirimi

Kaynak dosya: `thesis_exp/literatur_pdf/pdf/09_CNN_RAGNet_CFO.pdf` (5 sayfa, tamamı okundu).
Kural: sayılar yalnızca PDF'ten, sayfa/tablo/denklem referansıyla; PDF'te olmayan → **YOK**.
"Yorum" etiketli satırlar not yazarının çıkarımıdır, makalenin iddiası değildir.

---

## 1. Künye (PDF'te basıldığı gibi)

- **Yazarlar:** Shivani Singh (Graduate Student Member, IEEE), Sudhan Majhi (Senior Member, IEEE), Udit Satija (Senior Member, IEEE) — s. 1092.
- **Başlık:** "CNN-RAGNet Architecture for CFO Estimation in RIS-Assisted MIMO-OFDM Systems"
- **Yayın:** IEEE Communications Letters, Vol. 29, No. 5, May 2025, pp. 1092–1096.
- **DOI:** 10.1109/LCOMM.2025.3554345 (s. 1092 dipnot).
- Tarihler: alındı 26 Ocak 2025; revize 25 Şubat 2025; kabul 20 Mart 2025; yayın 24 Mart 2025; güncel sürüm 12 Mayıs 2025 (s. 1092 dipnot).
- Kurumlar: IIT Patna (Singh, Satija); IISc Bengaluru (Majhi) (s. 1092 dipnot).
- arXiv: **YOK** (PDF'te arXiv numarası basılı değil).

**Kullanıcı listesiyle uyuşmazlık:** Listede "M. M. Amri et al., IEEE SPL 2025/2026" yazıyordu. PDF'teki makalenin yazarları **Singh, Majhi, Satija**; dergi **IEEE Communications Letters (LCOMM)**, IEEE Signal Processing Letters değil; yıl 2025. Ya listedeki künye yanlış, ya da bu dosya listedeki makale değil — kullanıcı kontrol etmeli.

## 2. Problem ve katkılar

- Problem: RIS destekli MIMO-OFDM'de taşıyıcı frekans kayması (CFO) alt taşıyıcı dikliğini bozar, ICI üretir ve "degrades performance in high mobility environments" (s. 1092, Giriş). RIS faz kaydırmaları "assuming no CFO is present" tasarlanır; CFO zamanla değişen faz dönmesi üretip RIS fazları ile alıcı telafisi arasında uyumsuzluk yaratır (s. 1092).
- Amaç: **CSI'sız, pilotsuz (non-data aided)**, denetimli derin öğrenme ile CFO kestirimi (Özet; s. 1094 §III).
- Katkılar (s. 1093, (a)–(e)): (a) CNN + geliştirilmiş Res + Attention + dense GLU (D-GLU) = CNN-RAGNet; (b) Mish aktivasyonlu evrişim katmanları; (c) anten içi ve antenler arası korelasyonu yakalayan dikey/yatay filtreler; (d) 3GPP TR38.901 TDL zamanla değişen kanalda, farklı RIS eleman sayısı ve modülasyonlarda çalışma; (e) istatistiksel ve mevcut DL yöntemlerine göre daha iyi başarım ve "lower computational complexity".

## 3. Sistem modeli

| Öğe | Değer | Kaynak |
|---|---|---|
| Taşıyıcı frekansı fc | **YOK** | — |
| Bant genişliği | **YOK** | — |
| Alt taşıyıcı sayısı | N_c = 128 | s. 1095 §IV-A |
| Aşırı örnekleme | N = γN_c (denk. 2); eğitimde "ρ = 5" (sembol tutarsızlığı: denk. 2'de γ, §IV-A'da ρ) | s. 1093, s. 1095 |
| CP | N_cp = N/4 | s. 1093, s. 1095 |
| Antenler | N_t = 2, N_r = 2 | s. 1095 |
| RIS eleman sayısı K | Test: 20, 60, 80, 100 (Şekil 4(c)); varsayılan eğitim değeri metinde açık değil; s. 1095–1096: "the model is specifically trained for this configuration" (20 eleman) | s. 1095–1096 |
| RIS katsayısı | φ_k = β_k e^{jθ_k}, β_k ∈ [0,1], θ_k ∈ [0,2π); ideal RIS, |φ_k| = 1 | s. 1093 |
| Doğrudan bağlantı | Engelli varsayılıyor | s. 1093 |
| Kanal | 3GPP TR38.901 TDL zamanla değişen çok yollu; eğitim TDL-C, test TDL-A/B/C/D/E | s. 1093, s. 1095 |
| Eşdeğer kanal | h_{r,t} = Σ_k φ_k (h_{k,t} * h̃_{r,k}) ∈ C^{L×1}, L = L1 + L2 − 1 | denk. (1), s. 1093 |
| CFO | Normalize kesirli ε ∈ [−0.5, 0.5]; "time-varying CFO, which changes randomly with a uniform distribution" | s. 1093 |
| Modülasyon | Eğitim 16QAM; test QPSK, 16/64/256/512/1024QAM | s. 1095 |
| SNR | Eğitim 5–10 dB, adım 2 dB; test −15–10 dB, adım 2 dB | s. 1095 |
| Hareketlilik / Doppler | Sayısal Doppler, hız veya koherens süresi **YOK**; yalnızca "time-variant" TDL ve Girişte "high mobility" ifadesi | s. 1092–1093 |
| Ortak vs alt taşıyıcı başına RIS fazı | Denk. (1)'de φ_k alt taşıyıcıdan bağımsız (zaman bölgesi eşdeğer kanalda tek RIS katsayısı) → ortak faz. **RIS fazlarının nasıl seçildiği belirtilmemiş: YOK** | s. 1093 |
| Giriş verisi | Y_c ∈ C^{L_T×N_r} (denk. 5); iki kanal: [I; Q] ve [|·|; ∠·] (denk. 6); Y ∈ C^{2L_T×N_r×2}; Tablo I girişi 3200×2×2 | s. 1093, Tablo I s. 1095 |

## 4. Yöntem

- Mimari (s. 1094, Şekil 2(a), Tablo I s. 1095):
  - **Preblock:** 3 evrişim birimi (40 çekirdek, 6×1), ilk ikisinin ardından maxpool (3×1, adım 2×1); her birim Conv + BN + Mish (denk. 7).
  - **Res block (×3):** maxpool + iki yol (3×1 ve 1×3 filtre, 40 çekirdek), F_out = F_mish(F_out1 + F_out2) + F_in1 (denk. 8).
  - **Attention:** reshape 200×40 → global attention (çıkış 40).
  - **D-GLU (×2):** sigmoid ve doğrusal iki paralel dense katmanın çarpımı + dropout 0.5; nöronlar 880 ve 352.
  - **Dense:** 944, 96, çıkış 1 (CFO kestirimi).
- Hiperparametreler Bayes yöntemiyle arandı (Tablo II, s. 1095; ref. [18]); optimal: conv tekrarı 3, 40 çekirdek, çekirdek 6, Mish; pool 3 / adım 2; Res tekrarı 3, çekirdek 3; D-GLU 2 blok (880, 352); dense 2 katman (944, 96).
- Eğitim (s. 1095 §IV-A): MATLAB ile üretilen veri; Adam, "decay rate of 0.8", 150 epok, batch 100, öğrenme oranı ilk 50 epok 0.01, sonra 0.001.
- Eğitim örnek sayısı N_exm: **YOK** (sembol tanımlı, sayı verilmemiş). Doğrulama/test bölünmesi: **YOK**. Kayıp fonksiyonu: **YOK** (MSE ile raporlanıyor).
- Bu bir **kestirim** ağıdır; RIS faz optimizasyonu yapmaz, iterasyon/adım boyu kavramı yoktur (tek ileri geçiş).

## 5. Karmaşıklık / gecikme

Tablo III, s. 1096 ("Comparison of Complexity of Different Methods"):

| Yöntem | Flop | Parametre | Çıkarım süresi (ms/örnek) | Model boyutu |
|---|---|---|---|---|
| Proposed model | 143,411,673 | 1,180,993 | 63 | 4.51 MB |
| Kurtosis [4] | 94,618 | – | 900 | – |
| Oversampling [5] | 7,382,718 | – | 669 | – |
| LSTM with NN [8] | 52,563,649 | 26,281,601 | 95 | 100.26 MB |
| ResR model [9] | 835,751,345 | 52,621,537 | 164 | 200.74 MB |
| ELM model [12] | 209,764,353 | 8,421,377 | 92 | 32.13 MB |
| GRU with NN [11] | 46,684,465 | 23,341,345 | 350 | 89.04 MB |

- Donanım, iş parçacığı sayısı, yazılım, tur sayısı, yayılım: **YOK**.
- Karmaşıklık mertebesi (Big-O): **YOK**.
- Makalenin kendi kabulü (s. 1096 §IV-D): "While statistical methods, LSTM, and GRU with NN models have smaller flop counts, CNN-RAGNet outperforms them due to its efficient Res, attention, and D-GLU blocks. Its remarkably low inference time and lightweight design make it ideal for real-time deployment".
- Hesaplama sırasında kanal/CFO eskimesi: **YOK** — makale çıkarım süresini kanal veya CFO değişim hızıyla ilişkilendirmiyor.
- Yorum: Özetteki "lower computational complexity than the existing methods" iddiası Tablo III'e göre yalnızca parametre/model boyutu ve süre için geçerli; flop sayısında önerilen model Kurtosis, oversampling, LSTM ve GRU'dan **daha yüksek** (143.4 M flop). Ayrıca Kurtosis'in 94,618 flop ile 900 ms sürmesi, sürelerin farklı uygulama/platformlarda alındığını düşündürüyor; ölçüm koşulları verilmediği için süreler karşılaştırılabilir kabul edilmemeli.

## 6. Ana sayısal sonuçlar

- Metrik: CFO kestiriminde MSE vs SNR (Şekil 3, 4). Sonuçların çoğu yalnızca grafik olarak verilmiş; tablo halinde MSE değeri **YOK**. Grafikten okunmuş değer bu notta verilmiyor.
- Şekil 3(a) RIS ile, 3(b) RIS'siz: önerilen model tüm SNR aralığında (−15–9 dB) Kurtosis [4], Oversampling [5], LSTM+NN [8], ResR [9], GRU+NN [11], ELM [12] yöntemlerinden daha düşük MSE (s. 1095). Taban çizgileri "RIS-assisted MIMO-OFDM için tasarlanmamış", "adapted them for comparison purposes" (s. 1095).
- RIS'li durum RIS'siz durumdan daha iyi (ek yansıma yolları, çeşitleme) (s. 1095).
- Şekil 4(a): yalnızca TDL-C ile eğitilmesine rağmen TDL-A–E'de sağlam; TDL-D ve TDL-E (LOS) daha iyi (s. 1095).
- Şekil 4(b): QPSK–1024QAM arasında görece tutarlı başarım; eğitim yalnız 16QAM (s. 1095).
- Şekil 4(c): RIS eleman sayısı arttıkça MSE iyileşiyor; 20 elemanın ötesinde azalan getiri ("correlated reflections and diminishing diversity gains") (s. 1095–1096).
- Ablasyon (s. 1096 §IV-C, Şekil 4(d)): 10^−4 MSE'de attention'sız modele göre **8 dB**, GLU'suz modele göre **18 dB** kazanç.
- Karmaşıklık: bkz. §5 (Tablo III).

## 7. Varsayımlar ve sınırlar

- Doğrudan bağlantı engelli (s. 1093).
- İdeal RIS, |φ_k| = 1 (s. 1093); RIS fazlarının değeri/seçimi belirtilmemiş — CFO'nun RIS faz tasarımına etkisi modellenmiyor, yalnızca kestirim yapılıyor.
- CFO düzgün dağılımlı, rastgele zamanla değişen; Doppler kaynaklı bir model veya hız parametresi yok.
- fc, bant genişliği, örnek sayısı, kayıp fonksiyonu, donanım: YOK.
- Eğitim SNR'si 5–10 dB iken test −15–10 dB.
- Taban çizgileri RIS sistemi için tasarlanmamış, uyarlanmış (s. 1095) — zayıf taban çizgisi riski (Yorum; CLAUDE.md'deki "zayıf taban çizgisi" uyarısıyla aynı türden).
- Sembol tutarsızlığı: aşırı örnekleme denk. (2)'de γ, §IV-A'da ρ; K hem RIS eleman sayısı (s. 1093) olarak kullanılıyor.

## 8. Tezle bağlantı

- Doğrudan rol: **zayıf/çevresel.** Makale RIS faz optimizasyonu, gecikme-farkındalıklı denetim veya kanal eskimesi ele almıyor; bir alıcı tarafı senkronizasyon (CFO) kestiricisi.
- Yorum: Gecikme-farkındalıklı RIS denetleyicisinde CFO/Doppler kestirimi bir **ön koşul** olarak düşünülebilir (denetleyici ölçülmüş Doppler'e göre karar veriyor); ancak bu makale Doppler değil CFO kestiriyor ve hareketlilik parametresi vermiyor, bu yüzden Doppler girdisinin kaynağı olarak doğrudan alıntılanamaz.
- Yorum: Tablo III'teki 63 ms/örnek çıkarım süresi, bir DL bileşeninin denetim döngüsüne ekleyeceği gecikmenin büyüklük mertebesine dair bir literatür örneğidir; ama donanım ve ölçüm koşulları verilmediği için tezin ölçülmüş adım maliyetleriyle **aynı tabloya konmamalı**. Makale bu süreyi kanal koherens süresiyle kıyaslamıyor; "real-time deployment" iddiası koherens süresine bağlanmamış — tezin "gecikme birinci sınıf kısıt" savıyla bu boşluk vurgulanabilir.
- Yorum: Makale, "düşük karmaşıklık" iddiasını flop yerine parametre/süre üzerinden kuruyor ve flop'ta daha pahalı; tezin "adım başına kazanç ≠ milisaniye başına kazanç" bulgusuna benzer bir metrik seçimi sorununun örneği olarak anılabilir (destekleyici bağlam, kanıt değil).
- Yeniden kullanılabilir parametreler: 3GPP TR38.901 TDL-A…E kanal ailesi seçimi; N_c = 128, N_cp = N/4. RIS faz/optimizasyon parametresi yok.
- Tez iddialarıyla çelişki: **YOK** (aynı problemi çalışmıyor).
