# Ayrıntılı teknik rapor — 11–12 Kasım 2026 çalışmaları

Bu rapor iki günde yapılan bütün deneysel işi, kullanılan yöntemleri, bulunan ve düzeltilen hataları ve
açık kalan konuları tek yerde toplar. Tez ya da makale metni değildir (Kural 9). Her sayının kaynağı
parantez içinde verilen rapor ve ham çıktıdır; o rapor da betik + tohum + commit'e bağlıdır (Kural 3).
Bu raporun kendisi yeni ölçüm içermez.

**Denetim durumu:** Bu rapor ve atıf yaptığı bütün raporlar saat başı çalışan bağımsız bir denetim ajanıyla
ham dosyalara karşı sınanıyor; sonuçlar `thesis_exp/denetim_log/` altında.

---

## 0) Okuma kılavuzu

### 0.1 Dallar

| Dal | İçerik | Ana rapor |
| --- | --- | --- |
| `audit/makale1-denetim` | Makale 1 (AISY) bağımsız denetimi | `audit/AUDIT_REPORT.md` |
| `thesis/altyapi` | Tez deneyleri için ortak altyapı, bit-bit yeniden üretim, yeni gecikmeler | `thesis_exp/infra/REPORT.md` |
| `thesis/bridge` | Köprü: tek geçişli ağ, etkin hız ölçütünde | `thesis_exp/bridge/REPORT.md` |
| `thesis/p4-deneyler` | Altı karşılaştırma (4.1–4.6) + 4.3 devamı + toplu raporlar | `thesis_exp/p4/*/REPORT.md`, `thesis_exp/TOPLU_RAPOR.md`, bu dosya |

Dallar zincirli: `thesis/p4-deneyler`, `thesis/bridge` üstünde; `thesis/bridge`, `thesis/altyapi` üstünde kuruldu
(uzak `thesis/altyapi` ucu köprü commit'lerini de içeriyor). `main`/`master`'a hiçbir şey yazılmadı (Kural 6).

### 0.2 Uyulan kurallar ve nasıl uygulandıkları

| Kural | Uygulama |
| --- | --- |
| 1 Uydurma yok | Yeniden üretilemeyen her şey "ÜRETİLEMEDİ" (bkz. §7). |
| 2 Mevcut dosyalara dokunma | `results/`, `paper_mobility/` değişmedi; yeniden koşular çıktısı `thesis_exp/` altına yönlendirilmiş kopyalarla yapıldı; `results/mumiso_aging_*.json` md5 ile doğrulandı. |
| 3 Sayı ↔ betik ↔ ham çıktı | Her deney klasöründe `run.py` → `raw/results.json` → `make_report.py` → `REPORT.md`. |
| 4 Tohum, eşli bootstrap | Kanal 11 (test, yaşlanma kümesi), 12 (doğrulama/seçim); bootstrap tohumu 0, 2000 yeniden örnekleme, %95 GA. |
| 5 Zamanlama | Gecikme ölçen her betik yük < 0.5 bekliyor, tek iş parçacığı, medyan + tur değerleri, yük öncesi/sonrası kayıtlı. |
| 7 30 dk üstü onay | Görev 4 ve ek eğitimler için onay alındı; süre tahminleri iletildi. |
| 8 MATLAB yok | MATLAB çalıştırılmadı; aktarımlar NumPy/PyTorch, kayıtlı `.mat` olmadığından birebir doğrulanamadı. |
| 10 Çelişkiler üstte | Her raporda ve aşağıda §1'de. |

---

## 1) Yayımlanmış iddialarla çelişen bulgular

### 1.1 Makale 1 (AISY, doi:10.1002/aisy.70460) — `audit/AUDIT_REPORT.md`

Bütün yeniden üretimler **bağımsız bir çekilişte** (NumPy aktarımı, `audit/scripts/m1_data.py`), MATLAB'ın
`rng(42)` örnekleriyle değil.

1. **Etiket optimum değil (Denklem 8).** −∠(G_nF_n) etiketi, doğrudan bağlantıyı yok sayıyor; ∠h_d − ∠(G_nF_n) hiçbir örnekte daha kötü değil. (step1_label_optimality.json)
2. **Nicemleme RMSE'leri imkânsız.** Makale 1/2/3 bit için 4.12/3.08/2.81° diyor; etiketin kendisi nicemlendiğinde bile 51.95/25.98/12.98° (tekdüze nicemleme hatası adım/√12); eğitilmiş modelle 52.06/26.17/13.39°. (step6_eval.json)
3. **CSI hatasında 4.2° tutmuyor.** Göreli hata varyansı 0.10'da model 19.00° (3 tohum ort.), kapalı form 18.66°. (step6_eval.json, step2_baselines.json)
4. **Klasik yöntemlerin RMSE'leri yayımlanan kodla üretilemiyor.** CD (K=5) 104.02° (makale 3.50°); ortak faz çıkarılınca 1.10°. Bu yöntemler gerçek optimuma gidiyor, etiketten ortak bir faz kadar ayrılıyor. (step2_baselines.json)
5. **Tablo 6, Tablo 8, Şekil 1–2 elle yazılmış; Şekil 8–10 için betik yok.** (step0_mapping.json, step0_step3_notes.md)
6. **N=256 projeksiyonu tutmuyor.** Tablo 8'deki 4.6° elle yazılmış bir tahmin. Ölçülen 2.25° (tek tohum, gizli boyut √(N/32) ile ölçekli, 870 018 parametre, SR@5 %98.1); N=32'nin üç tohumunun (3.18/2.77/3.90°) hepsinden düşük. Ek tohumlar ve N=64/128 sürüyor (§8). (train/cnnlstm_N256_sqrt_s0.json)
7. **Tohum yayılımı** 3 tohumda std 0.58°; makale 5 koşu için ±0.09° GA diyor. (train/cnnlstm_N32_s*.json)
8. **Uzamsal komşuluk kullanılmıyor.** Komşu eleman korelasyonu |ρ| ≤ 0.007; permütasyonla 3.28° → 3.41° (tohum yayılımından küçük). (step5_*.json)
9. **Parametre sayısı** 162 562 (makale 727 K); doğrudan faz FC-DNN 83.85° (makale 3.95°); CNN-Transformer 4.46° (makale 2.91°).
10. **Kaynakça:** 64 kaynağın ilk turda 33'ü "major"; [26] geri çekilmiş; basılı 54 DOI'nin 30'u kayıtlı değil. (step7_*.json)

Not: Makale 1 için kullanıcının kararı "düzeltmeye gerek yok"; bu bulgular denetim kaydı olarak duruyor.

### 1.2 Makale 2 (hareketlilik) — `thesis_exp/infra/REPORT.md`, `thesis_exp/p4/onkodlayici_*/REPORT.md`

11. **Ön kodlayıcı tazeleme pilotları ücretlendirilince mutlak etkin hız büyük ölçüde düşüyor; en iyi kol kümesi değişmiyor.**
    - En iyi kol taze ve bedava W varsayımıyla (makalenin varsayımı) 5.213 b/s/Hz. Bu deneyin ölçütü devreye girdikten sonraki 50 ms'nin zaman ortalaması; madde 12'deki 6.075 ise Tanım 1'in anlık etkin hızı, ikisi doğrudan karşılaştırılmaz. 50 ms penceresinin duyarlılığı denenmedi. pilot ücretiyle 3.539 (15 kHz), 4.003 (30 kHz), 4.334 (60 kHz): %32/%23/%17 kayıp.
    - Nokta tahminleriyle ilk dört kol (Adam-6, 5, 8, 4) her durumda aynı sırada; aralarındaki farkların GA'sı sıfırı içeriyor (kesin olan, en iyi kümenin Adam-4…8 olarak kalması); 5. ve 6. sıra numerolojiye göre değişiyor; en iyi kolun SU-best-of'a üstünlüğü +0.303 [+0.242, +0.366] → +0.153 / +0.193 / +0.209 (GA'lar sıfırın üstünde). (p4/onkodlayici_siralama/raw/results.json)
12. **Adam adımı 1.66 değil 1.328 ms** (tek iş parçacığı, boş makine). Bununla L* = 6 (makale 5; metin 4–6), L=48 kaybı %14.4 (makale %14.0), en iyi etkin hız 6.075 (makale 5.982). SU-best-of − Adam-20: −0.086 [−0.174, 0.002] (makale −0.004 [−0.095, 0.085]). Ana bulgular korunuyor. (infra/raw/mumiso_aging_sweep_newlat.json, mumiso_aging_stats_newlat.json)
13. **Kullanılmayan senaryo sayısı 800 değil 700** (doğrulamanın 500'ü kullanılıyor). (infra/raw/static_split_usage.json)

---

## 2) Görev 1 — Makale 1 denetimi (ayrıntı)

**Amaç:** Makale 1'in tablo ve şekillerini bağımsız olarak yeniden üretmek, kaynağı olmayan sayıları bulmak.

**Adımlar ve betikler** (hepsi `audit/scripts/`, çıktılar `audit/raw/`):

| Adım | Ne yapıldı | Betik | Ham çıktı |
| --- | --- | --- | --- |
| 0 | Tablo/şekil ↔ kod eşlemesi (MATLAB paketleri, depo, yüklenen dosyalar) | ajan taraması | step0_mapping.json, step0_step3_notes.md |
| 1 | Etiket (a) −∠(G_nF_n) ile (b) ∠h_d − ∠(G_nF_n) güç karşılaştırması, 6000 örnek | step1_label_optimality.py | step1_label_optimality.json |
| 2 | Klasik yöntemlerin Python aktarımı (CD, AO, PGD, PSO, SPA, "WMMSE") ve CSI hatalı girdiler | step2_baselines.py | step2_baselines.json, step2_csi_inputs_x*.npz |
| 2, 5 | CNN-LSTM, doğrudan faz FC-DNN, CNN-Transformer eğitimi (MATLAB varsayılanları: girdi normalizasyonu yok, L2 1e-4, son epok ağı, yarım-MSE, zaman adımı başına FC) | m1_train.py | train/*.json, *.pt |
| 3 | Kaynaksız sayılar | ajan + step3_arith_check.py | step3_sources.json, step3_arith_check.json |
| 4 | Parametre sayısı ve tek-örnek/toplu gecikme (N=32…256) | step4_latency.py | step4_latency.json |
| 5 | Komşu eleman korelasyonu ve permütasyon kontrolü | step5_correlation.py, step5_permutation.py | step5_*.json |
| 6 | Nicemleme, faz gürültüsü, CSI hatası değerlendirmesi | step6_eval.py | step6_eval.json |
| 7 | 64 kaynak: Crossref/doi.org/arXiv; bağımsız ikinci tur | ajan | step7_references.json/.md, step7_doublecheck.json |
| N=256 | Tek tohum, √N gizli ölçekleme, 2 iş parçacığı, 264.7 dk | m1_train.py --N 256 --hidden_scale sqrt | train/cnnlstm_N256_sqrt_s0.json, train_N256_run2.log |

**Doğrulananlar:** CNN-LSTM SR@5 %94.7 (makale %95); Şekil 8'de %95'e ulaşılan hata 5.09° (makale 5°).

**Yorum (bulgulardan ayrı):** Modelin kendisi çalışıyor (2.8–3.9°); sorunlar etiket tanımında, karşılaştırma
protokolünde (etiket-RMSE'si, gerçek optimuma giden yöntemleri ortak faz nedeniyle cezalandırıyor) ve kaynaksız sayılarda.

**N=256 kayıt notu:** JSON'daki commit `81b07dd` o sırada çalışma ağacının HEAD'i (tez dalı); koşulan betik denetim dalındaki
`m1_train.py`'nin yalnızca ROOT yolu sabitlenmiş kopyası (fark `diff` ile doğrulandı). Ek eğitimler (§8) doğrudan denetim
dalının çalışma ağacından koşuyor, commit alanı doğru dalı gösterecek.

---

## 3) Görev 2 — Ortak altyapı (ayrıntı) — `thesis_exp/infra/REPORT.md`

1. **Bit-bit yeniden üretim:** `results/mumiso_aging_fixzf.json`, `mumiso_aging_sweep_repro.json`, `mumiso_aging_sensitivity.json` (config hariç) ve 9 tablo + `paper_numbers.txt`, çıktısı yönlendirilmiş kopyalarla 0 farkla üretildi. `mumiso_aging_sweep_fixzf.json` 11 farkla üretilemedi; betiği yok ve makale onu kullanmıyor (makale `_repro` dosyasını kullanıyor).
2. **Gecikmelerin yeniden ölçümü** (tek iş parçacığı, boş makine): Adam 1.328 ms/adım, SU-best-of 1.63 ms, CD 702.97 ms, PGA 4950.35 ms (makale: 1.66 / 2.54 / 880.78 / 5851.66 ms). Tablo I ve Şekil 3 bu gecikmelerle `thesis_exp/infra/` altında yeniden üretildi (§1.2 madde 12).
3. **Kullanılmayan senaryolar:** 700 (madde 13).
4. **Makale 1 modeli 38.901 arayüzünde (N_t = 1):**
   - Ham girdili kollar öğrenmedi (RMSE ≈ 104°). Plan dışı olarak kalan tohumlar için ölçek-normalize kollara geçildi; raporda kayıtlı.
   - Ölçek-normalize sin/cos: RMSE 58.4–59.8°, hız 9.302 b/s/Hz (optimum 10.349; makale etiketi (a) 9.908).
   - sin/cos − doğrudan açı farkı üç tohumda +1.63…+1.86 b/s/Hz; özgün sıra − permütasyon +0.09…+0.42 b/s/Hz (GA'lar sıfırın üstünde).

---

## 4) Görev 3 — Köprü (ayrıntı) — `thesis_exp/bridge/REPORT.md`

**Soru:** Makale 1'in tek geçişli faz-farkında ağı, Makale 2'nin etkin hız ölçütünde klasik yöntemleri geçebilir mi?

**Kurulum:** Eğitim verisi yaşlanma kümesinin yapısıyla (20 saçıcı, t=0) üretilen statik küme, seed 2027, 6000 senaryo
(4200/900/900). Seçimler yalnızca statik doğrulama kümesinde ve seed 12 hareketlilik çekilişinde; rapor seed 11.

**Sonuç:** Her yerde baskınlanıyor.
- 5.4 km/h'de ağ (2.847 ms) 4.620 b/s/Hz; en iyi klasik Adam-5 6.038; fark −1.418 [−1.503, −1.336].
- ağ+Adam-1/2/3 kolları da baskınlanıyor.
- 3–30 km/h'nin hepsinde 4/4 öğrenilen kol baskınlanıyor.
- Periyodik çalışmada (T_p = 0…3.43 ms) ağ hem soğuk hem sıcak başlangıçlı Adam'ın gerisinde.

Bu, CLAUDE.md'deki "yapay zekâ ekseni kapandı ve olumsuz" hükmüyle tutarlı.

---

## 5) Görev 4 — Altı karşılaştırma (ayrıntı)

Ortak kurulum (`thesis_exp/p4/common.py`):
- Yaşlanma kümesi `scripts/mumiso_aging.py` ile aynı (seed 11, 400 senaryo, 20 saçıcı, 1.5 m/s), ZF, min-kullanıcı hızı, soft-min Adam (β = 8).
- `check_same_scenarios` her deneyde t=0 SU-average değerini `results/mumiso_aging_fixzf.json` ile 1e-4 içinde doğruluyor.
- Gecikmeler Görev 2'nin tek iş parçacıklı ölçümünden. Adam-L gecikmesi SU-average başlangıcını (0.30 ms) içermiyor (makalenin kuralı); bu Adam kollarını ~0.016 b/s/Hz kayırır (denetim U3).
- Adam-6 etkin hızı Görev 2'de 6.075, burada 6.077: aynı eğrinin farklı zaman ızgaralarında doğrusal interpolasyonu (denetim U9).

### 5.1 Kanal öngörüsü — `p4/kanal_ongoru/REPORT.md`
- Öngörücüler: lin2, lin3, quad3, kalman3; Δ ∈ {1, 2, 5} ms; e2 ∈ {0, 0.01, 0.1}.
- **e2 = 0:** öngörüsüz en iyi Adam-6 6.077; öngörüyle +0.19 … +0.42 b/s/Hz, en iyi L 8–12'ye kayıyor.
- **e2 = 0.01:** bütün birleşimler öngörüsüzün (5.611) altında, −0.10 … −1.29.
- **e2 = 0.1:** hepsi öngörüsüzün (4.944) altında, −0.20 … −0.83.
- Sınır: model öngörüyü kayırıyor (saçıcılar sabit, düz yörünge); ek anlık görüntülerin pilot süresi tek-atış etkin hıza eklenmedi.

### 5.2 Konum (LoS geometrisi) tabanlı faz — `p4/konum_faz/REPORT.md`
- Geometri tabanlı faz, kanal tabanlı SU-best-of'un (5.277) 0.83–0.86 b/s/Hz altında (4.415–4.449).
- Konum hatası 0–1 m sonucu değiştirmiyor.
- Rastgele faz 4.072; yani geometri rastgelenin yalnızca 0.34–0.38 üstünde.
- Konum edinme gecikmesi modellenmedi.

### 5.3 Ön kodlayıcı tazeleme pilotları — `p4/onkodlayici_pilot/REPORT.md` + devamı `p4/onkodlayici_siralama/REPORT.md`
- ZF her R ms'de bir tazeleniyor; K = 4 pilot sembolü 1 − t_p/R ile ücretlendiriliyor; R ∈ {0.5…50} ms; 15/30/60 kHz.
- **Düzeltilmiş sonuç:** §1.2 madde 11. En iyi R 1–2 ms; hiç tazelenmeyen W ≈ 0.76 b/s/Hz.
- **Düzeltme:** 4.3'ün ilk sürümü tazeleme anlarını mutlak 0.1 ms ızgarasına yuvarlıyordu (§6, H7). Raporun başına düzeltme notu kondu; yanlı çıktılar `_v1_grid_bias` adıyla saklı.

### 5.4 Pilot SNR'ine bağlı kusurlu CSI — `p4/kusurlu_csi/REPORT.md`
- e2 = 1/(1+ρ).
- **Etkin hız:** kusursuz 6.077 → 30 dB 3.537 → 20 dB 1.402 → 10 dB 0.295.
- **SU-best-of'a göre:** +0.800 / +0.344 / +0.134; 10 dB ve altında GA sıfırı içeriyor.
- **Testte en iyi Adam-L:** 6 → 3 → 5.
- **Sınır:** ρ serbest parametre, pilot bütçesine bağlanmadı.

### 5.5 Ayrık faz (1/2 bit) — `p4/ayrik_faz/REPORT.md`
- **L\*:** 1 bitte Adam-5→q, 2 bitte Adam-6→q.
- **Adam-48→q kaybı:** %9.3 / %13.6.
- **dCD gecikmeleri** (boş makine, tek iş parçacığı):
  - 1 bit: 16.2 / 28.7 / 48.8 / 61.9 / 73.4 ms (1/2/3/4/8 tarama).
  - 2 bit: 27.1 / 56.3 / 86.2 / 109.3 / 129.5 ms.
- **2 bit:** her dCD kolu SU-best-of→q'dan kötü ya da ayırt edilemez.
- **1 bit:** doğrulamada dCD-1 seçildi (testte 5.113). Adam-5→q 5.157. Aralarındaki eşli fark hesaplanmadı.
- **Sınır:** yuvarlama bedava sayıldı.

### 5.6 Optimize edilmiş süreler — `p4/optimize_sure/REPORT.md`
- **eager:** Adam-1 1.703, öğrenilen-1 3.544, Adam-8 10.405, öğrenilen-8 29.178 ms.
- **torch.compile:** 2.184 / 4.220 / 13.487 / 41.679 ms.
- **Öğrenilen/Adam oranı:** L=8'de 2.80 (eager) ve 3.09 (compile).
- **torch.compile iki kolu da yavaşlattı:** Inductor karmaşık sayılarda kod üretmiyor; öğrenilen kol yeniden derleme sınırına (256) takıldı.
- **jit.trace ve GPU:** ÜRETİLEMEDİ.
- **Sınır:** eğitilmemiş ağırlıklar kullanıldı (süre ağırlığa bağlı değil). Adam-1 süresi SU-average başlangıcını da içeriyor.

---

## 6) Süreçte bulunan ve düzeltilen hatalar

| # | Hata | Etkisi | Düzeltme |
| --- | --- | --- | --- |
| H1 | Arka plan işi çalışırken dal değiştirmek betik dosyalarını sildi, iş öldü | Sonuç yok, yanlış sonuç da yok | Yeniden koşuldu; uzun işler için ayrı çalışma ağacı (`git worktree`) kullanılıyor |
| H2 | `pgrep -f` ile bekleyen döngü kendi komut satırını buldu, kilitlendi | Gecikme | Kuyruk doğrudan başlatıldı |
| H3 | Yaşlanma üretecinde ilk zaman t=0 değilken LoS/K-faktörü farklı senaryo üretti | `check_same_scenarios` yakaladı; sonuç raporlanmadı | t=0 her ızgarada ilk eleman; common.py'de belgelendi |
| H4 | Pilot süresi 0.1 ms ızgarasına yuvarlandı (30 ve 60 kHz aynı çıktı) | Raporlanmadan yakalandı | Kesirli ücretlendirme 1 − t_p/R |
| H5 | `mumiso_aging_stats` kopyası `results/`'a yazacaktı | Önlendi; md5 ile dosyanın değişmediği doğrulandı | Çıktı `thesis_exp/` altına |
| H6 | Oturum yeniden başlaması N=256 eğitimini 2. epokta öldürdü | Gecikme | Kesik günlük saklandı; yeniden başlatıldı; artık kuyruklar biten işi atlıyor |
| **H7** | **Tazeleme anları mutlak 0.1 ms ızgarasına yuvarlandı; yön kolun gecikmesine bağlı** | **4.3'ün pilot ücretli sayıları ve ilk sıralama koşusu yanlıydı (SU-best-of ~0.08–0.10 düşük; testere dişi sıralama)** | **Kolun devreye girme anına hizalı ızgara; 4.3 raporuna düzeltme notu; yanlı çıktılar saklandı; toplu rapor düzeltildi** |
| H8 | 38.901 ham girdili kol öğrenmedi | Plan sapması | Ölçek-normalize kola geçildi, raporda kayıtlı |
| H9 | Sweep bit-kimliği için yanlış eski dosya (`_fixzf`) seçildi | Yanlış "FARKLI" | Makalenin kullandığı `_repro` dosyası ile 0 fark |
| H10 | Optimize süre raporunda çok satırlı hata mesajı tabloyu bozdu | Biçim | Boşluklar tek satıra indirildi |
| H11 | (Denetim K1) kanal_ongoru ve kusurlu_csi koşuldukları anda betikleri commit'lenmemişti; results.json'daki commit'te run.py yok (Kural 3) | İzlenebilirlik; sayılar çürütülmedi | Commit'li koddan (f413f63) yeniden koşuldu: commit alanı dışında bütün değerler birebir aynı (thesis_exp/denetim_log/k1_rerun.md); raporlar artık ölçüm commit'ini de yazıyor |
| H12 | (Denetim U1) 4.3'ün ilk sürümü en iyi R'yi test kümesinde seçiyordu | Yalnızca yanlı v1 tabloları; devam deneyi R'yi doğrulamada seçiyor ve aynı R'leri buluyor | Devam deneyi esas |
| H13 | (Denetim U5/U6) özet raporlarda iki yanlış genelleme: 'dCD t=0'da her kolu geçiyor' (2 bitte yanlış), 'L* 10–12' (8–12) | Metin | Düzeltildi |

Not: H7, kullanıcıya önce bildirilmiş bir sayıyı değiştirdi (4.3: 3.303/3.718/4.025 → 3.385/3.811/4.126).

---

## 7) ÜRETİLEMEDİ

| Ne | Neden |
| --- | --- |
| Makale 1'in birebir yeniden üretimi | MATLAB ve `RIS_dataset_large_2D.mat` yok |
| Makale 1 Şekil 9 PSO gecikmesi (15 ms) | MATLAB yok; Python süresi karşılaştırılamaz |
| `results/mumiso_aging_sweep_fixzf.json` | Üreten betik yok (makale kullanmıyor) |
| 4.6 torch.jit.trace (Adam ve öğrenilen) | Optimizasyon adımı / iç gradyan izlenemiyor |
| 4.6 GPU | Bu makinede CUDA yok |
| 4.5 için 3 bit | Koşulmadı (istem 1/2 bit); boş makine gerektiriyor, eğitimlerden sonra eklenebilir |

---

## 8) Sürmekte olan işler (12 Kasım)

| İş | Durum | Tahmin |
| --- | --- | --- |
| N=256 tohum 1, 2 (√N, 2 iş parçacığı) | Kuyruk A | ~4.5–5 saat/tohum |
| N=64 tohum 0–2, N=128 tohum 0–2 | Kuyruk B | N=64 ~1 saat/tohum; N=128 ölçülecek |

Bitince `audit/AUDIT_REPORT.md` güncellenecek (RMSE–N eğrisi, tohum yayılımıyla).

---

## 9) Sınırlar ve riskler

- **Kanal modeli:** Hareketlilik sonuçları tek bir kanal modeline (sabit saçıcılar, düz yörünge, iç mekân) dayanıyor. Öngörü (4.1) bu yüzden iyimser.
- **Pilot ücreti (4.3):** Kusursuz kestirimle ücretlendirildi. Kestirim hatasıyla (4.4) birlikte modellenmedi; ikisinin birlikte etkisi daha büyük olabilir.
- **Zamanlama:** Gecikmeler tek bir CPU'da (Intel Xeon @ 2.10 GHz). Başka donanımda mutlak sayılar değişir; Makale 2'nin hükmü göreli sıralamaya dayanıyor.
- **Makale 1:** Bağımsız çekiliş; MATLAB örnekleriyle birebir değil.
- **Ölçüm fazı:** 20 Kasım'da kapanıyor; §8 bu tarihten önce bitecek.

---

## 10) Yeniden üretim

```bash
python3 scripts/audit_claims.py --all                       # 126/126 (her oturumun ilk komutu)
# Görev 2 (dal thesis/altyapi):    thesis_exp/infra/scripts/*.py, make_infra_report.py
# Görev 3 (dal thesis/bridge):     thesis_exp/bridge/scripts/bridge_{train,eval,tracking}.py, make_bridge_report.py
# Görev 4 (dal thesis/p4-deneyler):
for d in kanal_ongoru konum_faz onkodlayici_pilot kusurlu_csi ayrik_faz optimize_sure onkodlayici_siralama; do
  python3 thesis_exp/p4/$d/run.py && python3 thesis_exp/p4/$d/make_report.py
done   # ayrik_faz ve optimize_sure boş makine bekler
# Görev 1 (dal audit/makale1-denetim): audit/scripts/step*.py, m1_train.py, make_audit_report.py
```
