# Makale 1 bağımsız denetim raporu

Makale: Savaşçı Şen ve ark., *Overcoming the Phase Discontinuity Problem in RIS Optimization…*, Adv. Intell. Syst. 2026, doi:10.1002/aisy.70460. Dal `audit/makale1-denetim`, rapor commit'i `089c578` (rapor bu commit'teki ham dosyalardan üretildi).

**Önemli sınır:** MATLAB ve makalenin veri kümesi (`RIS_dataset_large_2D.mat`) yok. Bütün yeniden üretimler, aynı üretecin NumPy aktarımıyla (`audit/scripts/m1_data.py`) alınmış **bağımsız bir çekilişte** yapıldı. MATLAB'ın `rng(42)` örnekleriyle birebir aynı değildir; aktarım kayıtlı bir MATLAB çıktısıyla doğrulanamadı (Kural 8). Eğitim, MATLAB varsayılanlarına göre PyTorch'a aktarıldı (`audit/scripts/m1_train.py`, docstring).

## 1) Makaledeki iddialarla çelişen bulgular (önem sırasıyla)

1. **Etiket optimum değil (Denklem 8).** Makale −∠(G_nF_n) etiketini alınan gücün kapalı form maksimizörü diye tanımlıyor. Doğrudan bağlantıyı hesaba katan ∠h_d − ∠(G_nF_n) etiketi hiçbir örnekte daha kötü değil ve ortalama **2.20 dB** (%95 GA 2.13–2.28; medyan 1.23 dB; %95 dilim 7.73 dB) daha fazla güç alıyor; örneklerin %86.2'inde fark 0.1 dB'den büyük. |h_d|/|ΣG_nF_n| medyanı 1.42: doğrudan bağlantı ihmal edilebilir değil. [step1_label_optimality.json]
2. **Nicemleme sonuçları matematiksel olarak imkânsız.** Sürekli etikete göre faz RMSE'si, etiketin kendisi nicemlendiğinde bile 1/2/3 bitte 51.95°/25.98°/12.98° (tekdüze nicemleme hatası adım/√12). Eğitilmiş modelle 52.06°/26.17°/13.39°. Makale 4.12°/3.08°/2.81° diyor ve betiği yok. [step6_eval.json]
3. **CSI hatasında 4.2° iddiası tutmuyor.** Göreli hata varyansı 0.10'da model 19.00° (3 tohum ort.), aynı girdiyle kapalı form 18.66°. Makale 4.2° ve kapalı formdan belirgin üstünlük diyor; Şekil 10'un betiği ve hata modeli tanımı yok (burada varsayılan model, step2_baselines.py). [step6_eval.json, step2_baselines.json]
4. **Klasik yöntemlerin RMSE'leri yayımlanan kodla üretilemiyor.** Yayımlanan RMSE tanımıyla CD (K=5) 104.02° (makale 3.50°), AO 103.75° (3.50°), PSO 104.15° (4.50°), SPA 104.85° (5.00°). Sebep: bu yöntemler h_d'ye hizalanan gerçek optimuma gidiyor ve etiketten ortak bir faz kadar farklı. Ortak faz çıkarılınca CD 1.10°, SPA 1.3e-14° (SPA tam optimum = etiket (b)). Alınan güçte CD ve SPA etiketten 2.14 / 2.21 dB önde. PGD ve 'WMMSE' betikleri fazı neredeyse hiç hareket ettirmiyor (etikete göre -10.30 / -9.90 dB). [step2_baselines.json]
5. **Tablo 6, Tablo 8, Şekil 1 ve 2'deki sayılar elle yazılmış; Şekil 8, 9, 10 için betik yok.** Ayrıntı ve satır numaraları [step0_mapping.json, step0_step3_notes.md].
6. **Kaynağı bulunamayan sayılar:** 18.4/17.9 dB, kapalı formun 2.70° RMSE'si (etiketin kendisine göre tanım gereği 0°; burada 0.00°), 0.31/0.89 b/s/Hz, %312, Tablo 3 parametre sayıları. [step3_sources.json]
7. **Gecikme ve ölçekleme.** Yayımlanan mimarinin parametre sayısı koddan 162,562 (PyTorch; MATLAB 161 794, aradaki 768 ikinci LSTM bias'ı); makale 727 K. Tek-örnek CPU gecikmesi N=32/256'da 0.80/2.66 ms, toplu iş 0.158/1.66 ms; makale 0.08/0.64 ms (farklı işlemci: i7-9700K). Ölçekleme oranı 256/32: tek-örnek 3.3×, gizli boyut √N ölçeklemeli 13.6× (makale tam 8×). [step4_latency.json]
8. **N=256 projeksiyonu ölçümle tutmuyor.** Tablo 8'deki N=256 RMSE'si 4.6° elle yazılmış bir tahmin (betik yok). Aynı üreteç, aynı örnek sayısı (40 000) ve 50 epokla eğitilen N=256 modeli (gizli boyutlar √(N/32) ile ölçeklendi; 870,018 parametre; son epok ağı) test kümesinde **2.25°** (SR@5 %98.1, %95 dilim 3.39°) veriyor; bu, N=32'nin üç tohumunun (3.18, 2.77, 3.90°) hepsinden düşük. Makalenin N arttıkça RMSE'nin arttığı projeksiyonu bu ölçümde desteklenmiyor. Aynı kurulumla ölçülen dizi (tohum başına; √N ölçekli): N=64: 3.05°; N=128: 2.58°; N=256: 2.25°; makale Tablo 8: 2.77/3.21/3.89/4.6(tahmin)°. Sınır: ek tohumlar sürüyor; mimarinin N ile ölçeklenmesi makalede tanımlı değil (√N bizim seçimimiz). [train/cnnlstm_N256_sqrt_s0.json, train_N256_run2.log]
9. **Tohum yayılımı makalenin GA'sından çok büyük.** Aynı ayarla 3 tohum: 3.18, 2.77, 3.90° (std 0.58°); makale 5 koşu için ±0.09° GA diyor. [train/cnnlstm_N32_s*.json]
10. **Uzamsal komşuluk kullanılmıyor.** Komşu elemanların kanal korelasyonu |ρ| ≤ 0.007; eleman sırası rastgele karıştırılınca RMSE 3.28° → 3.41° (fark tohum yayılımından küçük). Makalenin CNN'in 'uzamsal korelasyonu yakaladığı' anlatısı bu veride desteklenmiyor. [step5_correlation.json, step5_permutation.json]
11. **Doğrudan faz (FC-DNN) 83.85°, CNN-Transformer 4.46°** (makale 3.95° / 2.91°). Transformer parametresi 17,442 (makale 201 K). [train/*.json]
12. **Kaynakça (64 kaynak):** ilk tur {'major': 33, 'ok': 18, 'not_verifiable': 8, 'minor': 5}. Bağımsız ikinci kontrol 63 kaynakta ilk turla aynı fikirde; [29] bulundu (başlığı yanlış basılmış gerçek bir makale: Kim ve ark., IEEE TCCN 2024, doi:10.1109/TCCN.2024.3375523). Basılı 54 DOI'nin 30'u kayıtlı değil; 3'ü ([31], [33], [43]) başka makalelere çıkıyor. 7 kaynak ([15], [33], [37], [41], [43], [44], [59]) hiçbir kayıtta bulunamadı ([33] ve [43] için aynı yazarların farklı başlıklı gerçek çalışmaları var: bozuk atıf olabilir). [26] geri çekilmiş (doi:10.52866/2788-7421.1361, 5 Şubat 2026). [27] TWC değil IEEE WCL. [28]'in PixelRNN iddiasını ve [38]'in bit genişliği iddiasını kaynak desteklemiyor. [step7_references.json, step7_doublecheck.json]

## 2) İddia tablosu

| İddia | Yayımlanan | Üretilen (bağımsız çekiliş) | Durum | Kanıt |
| --- | --- | --- | --- | --- |
| CNN-LSTM RMSE | 2.77° | 3.18, 2.77, 3.90° (3 tohum) | FARKLI (yayılım) | train/cnnlstm_N32_s*.json |
| CNN-LSTM SR@5 | %95 | %94.7 | DOĞRULANDI (yakın) | train/*.json |
| Doğrudan faz RMSE | 3.95° | 83.85° | FARKLI | train/fcdnn_direct_N32_s0.json |
| CNN-Transformer RMSE | 2.91° | 4.46° | FARKLI | train/transformer_N32_s0.json |
| CD (K=5) RMSE | 3.50° | 104.02° (ortak fazsız 1.10°) | FARKLI | step2_baselines.json |
| CD (K=20/50) RMSE | 3.49/3.20° | 104.50/104.79° | FARKLI | step2_baselines.json |
| AO / PGD / WMMSE / PSO / SPA | 3.50/4.00/4.00/4.50/5.00° | 103.75/103.86/103.85/104.15/104.85° | FARKLI | step2_baselines.json |
| Kapalı form RMSE | 2.70° | 0.00° (tanım gereği) | KAYNAK BULUNAMADI | step3_sources.json |
| Şekil 8: %95'e ulaşılan hata | 5° | 5.09° (CDF(5°) = %94.7) | DOĞRULANDI (yakın); yayımlanan görüntü 5°'de ≈%87 gösteriyor | step6_eval.json, step0_step3_notes.md |
| Şekil 9: normalize RMSE | 0.554 | 2.77/5 aritmetiği; şeklin betiği yok | KAYNAK BULUNAMADI | step3_arith_check.json |
| Şekil 9: PSO gecikmesi | 15 ms | MATLAB yok; Python süresi karşılaştırılamaz | ÜRETİLEMEDİ | — |
| Şekil 10: %10 CSI hatası | 4.2° | 19.00° (x=0.15: 23.56°) | FARKLI | step6_eval.json |
| Şekil 10: kapalı form / PSO, %10 | model üstün | 18.66° / 103.99° | FARKLI | step2_baselines.json |
| 1/2/3 bit nicemleme | 4.12/3.08/2.81° | 52.06/26.17/13.39° (hız kaybı 0.999/0.247/0.063 b/s/Hz) | FARKLI | step6_eval.json |
| Faz gürültüsü σ=1/3/5° | 3°'de taban çizgisine yakın | 3.44/4.47/5.99° (hız kaybı 0.006 b/s/Hz @3°) | FARKLI (RMSE) / hız kaybı küçük | step6_eval.json |
| Parametre (önerilen) | 727 K | 162,562 | FARKLI | train/cnnlstm_N32_s0.json |
| Diğer Tablo 3 parametreleri | 89K…201K | mimari tanımı yok | KAYNAK BULUNAMADI | step3_sources.json |
| Gecikme N=32/64/128/256 | 0.08/0.16/0.32/0.64 ms | 0.80/1.11/1.64/2.66 ms (tek örnek, CPU) | FARKLI (farklı işlemci) | step4_latency.json |
| RMSE N=64 / N=128 | 3.21° / 3.89° | 3.05° / 2.58° (tohum başına, √N ölçekli) | FARKLI (makaleden düşük; tohumlar sürüyor) | train/cnnlstm_N{64,128}_sqrt_s*.json |
| RMSE N=256 | 4.6° (tahmin) | 2.25° (1 tohum, gizli boyut √N ölçekli, SR@5 %98.1) | FARKLI (makaleden düşük; tek tohum) | train/cnnlstm_N256_sqrt_s0.json |
| SNR kazancı model / optimal | 18.4 / 17.9 dB | etiket (a) medyan 12.39 dB, (b) 14.03 dB (doğrudan bağlantıya göre) | KAYNAK BULUNAMADI | step1, step3 |
| 0.31 / 0.89 b/s/Hz, %312 | — | betik yok | KAYNAK BULUNAMADI | step3_sources.json |

## 3) Adımlar: komut, tohum, ham çıktı

| Adım | Komut | Tohum | Ham çıktı (audit/raw/) |
| --- | --- | --- | --- |
| 0, 3 | ajan taraması (yalnızca okuma) | — | step0_mapping.json, step3_sources.json, step0_step3_notes.md, step3_arith_check.json |
| 1 | python3 audit/scripts/step1_label_optimality.py --n 6000 --seed 42 | veri 42, bootstrap 0 | step1_label_optimality.json |
| 2 | python3 audit/scripts/step2_baselines.py | veri 42, PSO 0, CSI gürültüsü 5 | step2_baselines.json, step2_csi_inputs_x*.npz |
| 2, 5 | python3 audit/scripts/m1_train.py --arch {cnnlstm,fcdnn_direct,transformer} --seed {0,1,2} [--permute] | veri 42, eğitim 0/1/2, permütasyon 7 | train/*.json, *.pt, *_test_abs_err_deg.npy |
| 2 (N=256) | python3 audit/scripts/m1_train.py --arch cnnlstm --seed 0 --N 256 --hidden_scale sqrt --tag cnnlstm_N256_sqrt_s0 --threads 2 (betiğin bu daldaki hâli, yalnızca ROOT yolu sabitlenmiş kopyadan; JSON'daki commit 81b07dd çalışma ağacının HEAD'i) | veri 42, eğitim 0 | train/cnnlstm_N256_sqrt_s0.*, train_N256_run2.log (ilk deneme yeniden başlatmayla kesildi: train_N256.log) |
| 4 | python3 audit/scripts/step4_latency.py | veri 123 | step4_latency.json |
| 5 | python3 audit/scripts/step5_correlation.py; step5_permutation.py | bootstrap 0 | step5_correlation.json, step5_permutation.json |
| 6 | python3 audit/scripts/step6_eval.py | faz gürültüsü 11 | step6_eval.json |
| 7 | ajan: Crossref/doi.org/arXiv | — | step7_references.json/.md, step7_doublecheck.json |

Ortam: Python 3.11.17, PyTorch 2.15.0+cu132, NumPy 2.4.6, Intel(R) Xeon(R) Processor @ 2.10GHz, 4 çekirdek; MATLAB yok. Gecikme ölçümü tek iş parçacığı, yük 0.45 → 1.03.

## 4) Karar vermeniz gereken açık sorular

1. Veri kümesi `RIS_dataset_large_2D.mat` (ya da `aisy_paket/adim1` çıktısı) yüklenirse yeniden üretim birebir yapılabilir; aktarım doğrulanır.
2. Nicemleme, CSI hatası ve kapalı form 2.70° gibi tanımı belirsiz sayıların makalede hangi tanımla üretildiği yazarlardan öğrenilmeli.
3. Etiket formülü: tezde (b) ∠h_d − ∠(G_nF_n) kullanılsın mı? (Altyapı görevinde onaylandı.)
4. Bu bulguların yayımlanmış makale için ne anlama geldiği (düzeltme/erratum) danışmanla birlikte değerlendirilmeli.
5. N=64/128/256 için ek tohumlar (1, 2) sürüyor (2 iş parçacığı; N=64 ~53 dk, N=128 ~101 dk, N=256 ~265 dk/tohum). Konteyner yeniden başlamaları koşuları kesebiliyor; kesik günlükler saklanıyor.

## 5) Yorum (bulgulardan ayrı)

- Bağımsız çekilişte CNN–LSTM'in faz doğruluğu makaledekiyle aynı mertebede (2.8–3.9°), yani modelin kendisi çalışıyor; sorunlar etiket tanımında, karşılaştırma protokolünde ve kaynağı olmayan sayılarda.
- Klasik yöntemlerin 'kötü' görünmesi, gerçek optimuma gitmelerinin etiket-RMSE'si tarafından cezalandırılmasından kaynaklanıyor; alınan güç ölçütünde CD ve SPA etiketin önünde.
- Sin/cos gösteriminin ±π süreksizliğini gidermesi bu bulgulardan bağımsız; tezde ayrıca doğrulandı.
