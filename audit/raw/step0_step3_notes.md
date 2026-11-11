# AISY 2026 (doi:10.1002/aisy.70460) — Adım 0 (eşleme) ve Adım 3 (sayıların kaynağı)

Tarih: 2026-11-11. **Salt okuma.** MATLAB yok; zip, GitHub klonu ve yüklenen
dosyalardan hiçbir şey çalıştırılmadı. Yalnızca `cat`/`grep`/`pdftotext`/`pdfimages`
kullanıldı. Makine okunur sürümler: `step0_mapping.json`, `step3_sources.json`.
Türetilmiş her sayı (oranlar, parametre sayıları, uyum) `step3_arith_check.py` ile
üretildi (`step3_arith_check.json`). Bunlar ölçüm değil. Yalnızca makalenin kendi
sayılarıyla yapılmış aritmetik ve kodun katmanlarından analitik sayım.

Yol kısaltmaları:

| Kısaltma | Yol |
|---|---|
| ZIP | `scratchpad/audit_zip/` (`RIS_phase_aware_code.zip`; girdiler 2026-09-03 tarihli) |
| REPO | `scratchpad/m1repo/` (GitHub, commit `61531b5`, 2026-08-12) |
| UPL | `/root/.claude/uploads/36a1538b-…/` |
| ORIJ | `aisy_paket/orijinal/` |

## 0. Veri seti

**`RIS_dataset_large_2D.mat` hiçbir yerde yok.** Dosya sistemi taraması, zip içeriği,
REPO `git ls-files` ve iki tar.gz incelendi. Eğitilmiş model, `cnn_lstm_test_results.mat`,
`fairness_K_results.mat`, `scalability_results.mat` ve `.pth` dosyaları da yok.
Makalenin "Data Availability" bölümü (s.17) veri setinin GitHub'da olduğunu söylüyor.
REPO'da yok.

Sonuç: "ölçüyor" olarak sınıflanan betikler de bugün yayımlanan sayıyı yeniden
üretemez, çünkü girdileri yok.

## 1. Adım 0 — Tablo/şekil → betik eşlemesi

| Öğe (sayfa) | Yayımlanan değerler | Betik(ler) | Girdi | Sınıf |
|---|---|---|---|---|
| **Tablo 1** (s.3) | Doğrudan 3.95°; sin/cos 2.77°; %29.9; "5 koşu, %95 GA ±0.07°" | 2.77: `ZIP/theta_NN_multioutput.m:101-113`. 3.95: `ZIP/transformer_baseline.m:112-145`, ama 512-512-256 MLP; makaledeki "aynı mimari" değil | `.mat` (yok) | 2.77 **ölçüyor**. "Aynı mimari doğrudan" taban çizgisi, 5 koşu ve GA için **betik yok**. %29.9 yalnızca aritmetik |
| **Tablo 3** (s.8) | 8 satır RMSE/Params/Time | 2.77 ve 2.91 için ölçen kod var. Diğer 6 mimari hiçbir sürümde tanımlı değil | — | **Betik yok** (parametre sütununun tamamı, 6 satır) |
| **Tablo 6** (s.11) | 11 yöntem RMSE±std, SR@5, ms | CNN-LSTM: `theta_NN_multioutput.m:101-123`. CD: `ris_CD.m:36-58`. FC-DNN(doğrudan) ve Transformer: `transformer_baseline.m`. Tablonun tamamı ayrıca `ZIP/Figure7_comparison.m:11-12`'de sabit olarak yazılı | `.mat` (yok) | **Karma.** 4 satır ölçüyor (veri yok). AO/PGD/WMMSE/PSO/SPA, FC-DNN sin/cos ve GCN için **betik yok**. ±std, SR@5 (CNN dışı) ve 5 koşu için **betik yok** |
| **Tablo 8** (s.15) | 2.77/3.21/3.89/4.6(tah.); 0.08/0.16/0.32/0.64 ms; CD 3.04/12.2/73.0; Tr 1.1/48.6 | `ZIP/scalability_analysis.m:18-23` (sabit diziler). `UPL/f2d4df3b…:116,128` (`0.08*(N/32)`, `0.15*(N/32)^2`; başlıkta "projeksiyon" yazıyor). `REPO/Scalability Analysis.m.txt:10-20` | — | **Elle yazılmış.** N>32 RMSE ve "vs CD" için **betik yok** |
| **Şekil 1** (s.4) | Altyazı: CD 73.0, Tr 48.6 (N=256) | Yayımlanan görüntüyle eşleşen: `UPL/62def4dd-Scalability_Analysis.m:11,14,17` (`time_cd_k5=[0.76,3.04,12.16,48.64]`, `time_transformer=[1.14,…,72.96]`) | — | **Elle yazılmış** |
| **Şekil 2** (s.5) | CD 3.50/3.49/3.20°; 0.15/0.60/1.50 ms | Yayımlanan görüntü: `UPL/e0d34584…:10,13` (= ORIJ `…_v2_sekil.m`). Ölçen sürümler: `UPL/d9cff4ea…:65-78`, `ZIP/baseline_fairness_K_analysis.m:34-36`, `REPO/…m.txt:33-38` | `.mat` (yok) | Yayımlanan şekil **elle yazılmış**. Ölçen sürümlerin girdisi yok |
| **Şekil 8** (s.11-12) | "%95'i 5°'nin altında" | `ZIP/plot_results.m:47-55` CNN-LSTM için CDF çizer, ama yayımlanan görüntüyle uyuşmuyor. REPO'daki `plot_results.m`'de CDF bölümü yok | `cnn_lstm_test_results.mat` (yok) | Yayımlanan şekil için **betik yok** |
| **Şekil 9** (s.13) | (0.08 ms, 0.554), PSO 15 ms | Hiçbir sürümde yok | — | **Betik yok** |
| **Şekil 10** (s.14) | 10% CSI'da 4.2° | Hiçbir sürümde CSI gürültüsü kodu yok | — | **Betik yok** |

### Görüntülerden okunan çelişkiler (pdfimages ile görsel okuma)

- **Şekil 1:** Çizilen veride N=256'da CD 48.6 ms, Transformer 73.0 ms. Altyazı
  bunların tersini söylüyor. CD, N=32'de 0.76 ms olarak çizilmiş; Tablo 6'da 0.15 ms.
- **Şekil 2:** "K ≥ 20: URLLC Exceeded" diye gölgelenmiş, oysa K=20'de 0.60 ms < 1 ms.
- **Şekil 8:** Tek eğri var (yöntem başına eğri yok). 5°'de CDF ≈ 0.87. "5°" etiketli
  kesikli çizgi aslında x ≈ 6.7°'de.
- **Şekil 9:** x ekseni doğrusal ve 0–100 ms, altyazı log diyor. "Proposed" ≈ (4.5 ms,
  0.09) noktasında, PSO ≈ (95 ms, 0.92) noktasında. Grafikte ~20 etiketsiz gri nokta
  var (makalede 11 yöntem).
- **Şekil 10:** x ekseni "CSI Error Variance (σ²)". σ²=0.10'da ≈3.5°, 4.2° ise
  σ²=0.15'te.

### Sürüm farkları (md5)

| Dosya | ZIP | REPO | UPL / ORIJ | Fark |
|---|---|---|---|---|
| `theta_NN_multioutput.m` | 35f31d6e | **YOK** (README:23 listeliyor) | d3d64015 = ORIJ, aynı | — |
| `ris_CD.m` | 70668dcc (61 satır) | 4d45faa5 (78 satır) | 709bea43 = ORIJ = REPO | Yalnızca yorumlar (EN/TR); algoritma ve RMSE referansı aynı |
| `train_cnn_lstm.py` | 1676a2db | 38b871e5 | 91ee6a59 = ZIP | Yorum ve print metinleri (°/deg, Section 3.1/3.3) |
| `RIS_dataset_large_2D.m` | 98cdc170 | 5e080402 | 0d92cf48 = ORIJ = ZIP | REPO'da yalnızca 14. satırdaki yorum farklı |
| `github RIS_dataset_large_2D.m` | — | 5b24e369 | 715b085f `dataset.m` aynı | X_feat/Y_sincos/idx bölünmesi ve istatistikler eklenmiş; `-v7.3` |
| `…_UPDATED.m` | — | — | da19f647 = ORIJ | N=32/64/128 (256 yok). Çıktı adı farklı. `corr(THETA')` 40000² |
| `baseline_fairness_K_analysis` | d93068ea (ölçer, son %15) | 59aec6ee (.m.txt, 2000 örnek + makale sabitleri satır 41-42) | v1 eadc7d68 (ölçer, CD+AO) / v2 269ee8ef (sabit, yayımlanan şekil) | 4 farklı sürüm |
| Ölçeklenebilirlik | ec97516a (sabit) | 7ac4765d (.m.txt, sabit + enterpolasyon) | 62def4dd (sabit, **yayımlanan şekil**) / f2d4df3b (projeksiyon formülü) | Üç farklı sayı seti |
| `plot_results.m` | bdc4f6f0 (CDF var) | 7ba9b01d (CDF yok) | — | — |
| `ris_PGD` | maxIter=50 (satır 13) | maxIter=10 (.m.txt satır 11) | — | Varsayılan farklı |
| `transformer_baseline.m` | 1bd9042b | df76ed7c | — | Etiket metinleri. REPO'da kullanılmayan `Y_flat` var. İkisinde de `RMSE_cnn=2.77` sabit yazılı |

Ek gözlemler:

- Klasik `ris_AO/PGD/WMMSE/PSO/SPA` fonksiyonları faz RMSE'si (°) hesaplamıyor.
  Hesapladıkları, h_eff ile tüm fazları 1 olan konfigürasyon arasındaki kanal MSE'si.
  Süre ölçümü de yok.
- REPO'da klasik algoritmalar `.m.txt` uzantılı. README'de geçen `Figure5_comparison.m`,
  `Figure9_fairness.m` ve `Figure10_scalability.m` hiçbir sürümde yok.
- `README_GitHub_3.md:37-41`'de listelenen dört `quant_aware_*.m` niceleme betiği
  hiçbir yerde yok.

## 2. Adım 3 — Sayıların kaynağı

| Sayı | Makale (sayfa) | Kaynak | Not / çelişki |
|---|---|---|---|
| SNR kazancı **18.4 dB** (model) | s.4, s.14-15 | **KAYNAK BULUNAMADI** | Veri seti betikleri yalnızca etiketin medyan kazancını yazdırıyor (ZIP:114-119). Modelin SNR'si hiçbir yerde hesaplanmıyor |
| **17.9 dB** (optimal kapalı form) | s.15 | **KAYNAK BULUNAMADI** | Aynı büyüklük Tablo 4'te (s.10) **17 dB**. Model 18.4 > optimal 17.9 çelişkili. Etiket h_d'yi yok sayıyor, yani optimum değil (CD etiketten ~+2.1 dB güçlü: `results/aisy_cd_k_check.json`) |
| Kapalı form RMSE **2.70°** | s.13, s.15 | **KAYNAK BULUNAMADI** | **İç çelişki:** RMSE etikete göre ölçülüyor ve etiket kapalı formun kendisi (Eş. 8; s.9; ZIP:100). Kusursuz CSI'da tanım gereği 0°. Metin "yüksek SNR (30 dB), kestirim hatası ihmal edilebilir" diyor, ama 2.70°'yi verecek bir tanım ya da CSI hata düzeyi vermiyor |
| **0.31 b/s/Hz** optimal sınıra | s.4, s.15 | **KAYNAK BULUNAMADI** | Hiçbir sürümde log2(1+SNR) yok. 2-bit artışı da 0.31° (s.16): aynı rakam |
| CD **0.89 b/s/Hz** | s.15 | **KAYNAK BULUNAMADI** | Bu kodla CD etiketten daha güçlü konfigürasyon buluyor; CD'nin açığının daha büyük olması tutarsız |
| **%312** SE kazancı (klasik %287–298) | s.4, s.15 | **KAYNAK BULUNAMADI** | Rastgele faz taban çizgisi kodu yok |
| 1-bit **4.12°**, 2-bit **3.08°**, 3-bit **2.81°** | s.14 (3.08 ayrıca s.3, s.16, s.17) | **KAYNAK BULUNAMADI** | `quant_aware_*.m` README'de var, dosyalar yok. Sürekli etikete karşı b-bit nicelemenin RMSE tabanı 52°/26°/13° (`step3_arith_check.json`). Yani 4.12° ancak farklı bir tanımla (ör. nicelenmiş etiket) mümkün. Makale tanımı vermiyor |
| Faz gürültüsü σφ ∈ {1°,3°,5°} | s.3, s.14, s.16 | **KAYNAK BULUNAMADI** | Sayısal RMSE değeri bile verilmemiş. Genlik modeli "<%5" (s.14) için de kaynak yok |
| Şekil 9 normalize RMSE **0.554** | s.13 | Yalnızca aritmetik (2.77/5). Çizim betiği **yok** | Görüntüde Proposed ≈0.09 ve ≈4.5 ms |
| PSO **15 ms** | s.11, s.13, s.16 | **Elle yazılmış** (README tabloları: ZIP README:151, REPO README:132). `ris_PSO.m`'de süre ölçümü yok | Şekil 9'da ≈95 ms. 187× = 15/0.08 |
| Şekil 10 **10% CSI'da 4.2°** ve "PSO'ya %15 üstünlük" | s.1, s.3, s.13, s.16 | **KAYNAK BULUNAMADI** | Görüntüde 4.2° σ²=0.15'te. Makaledeki tek PSO sayısı kusursuz CSI'daki 4.50°; (4.50−4.2)/4.50 = **%6.7**, %15 değil. Kapalı form, AO ve PSO için gürültülü-CSI sonucu yok |
| Tablo 3 parametreleri | s.8, s.9 | 727K: makalenin analitik toplamı (s.9) ve `UPL/f2d4df3b:57` sabiti. Diğer 7 değer (89K/680K/520K/156K/231K/213K/201K): **KAYNAK BULUNAMADI** | Kod modelleri 727K değil: MATLAB `theta_NN_multioutput.m` = **161 794**, PyTorch `train_cnn_lstm.py` = **822 976**. Katman eklenince parametre 727K→231K/213K düşüyor; mimarilerle tutarsız |

### Ayrıca kaynaksız görülenler

- OOD 3.12° ve bootstrap GA [3.04, 3.20].
- t-testleri (p<10⁻⁴⁰ ve p<10⁻¹²).
- Norm 1.003±0.012, "10 000 test örneği" üzerinden. Oysa test kümesi 6000 örnek.
- GCN 3.12° ve FC-DNN sin/cos 3.41°.
- Şekil 8 metnindeki CD/AO/PSO/SPA yüzdelikleri.
- Transformer gecikmesi üç farklı değerle geçiyor: 0.17 / 0.11 / 1.1 ms.
- Eş. 19: makalenin kendi üç noktasından uyum yeniden hesaplanınca c₀=2.749, α=0.245,
  **R²=0.994** çıkıyor (makale 0.9998 diyor). 2.77·8^0.245 = 4.61 (makale 4.58).

## 3. Özet sınıflama

- **Ölçen kod var ama girdisi yok:** CNN-LSTM 2.77° / SR / süre; CD RMSE ve süre
  (bu tanımla ~104° beklenir); FC-DNN doğrudan (farklı mimari); Transformer.
- **Elle yazılmış:** Şekil 1, Şekil 2 (yayımlanan), Tablo 8 gecikmeleri, Şekil 7,
  PSO 15 ms, 727K (`f2d4df3b`).
- **Betik yok:** Tablo 3'ün 6 satırı ve tüm parametreleri; Tablo 6'da AO/PGD/WMMSE/PSO/
  SPA/FC-DNN sin/cos/GCN; ±std, 5 koşu, GA; Şekil 8 (yayımlanan), 9, 10; 18.4/17.9 dB;
  2.70°; 0.31/0.89 b/s/Hz; %312; niceleme 4.12/3.08/2.81°; faz gürültüsü; 4.2° ve %15.
