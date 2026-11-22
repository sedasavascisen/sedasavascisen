# Bağımsız denetim: d5249bf ve 7ccaeda (22 Kasım 2026)

Kapsam: `thesis_exp/makale_kontrol/RAPOR.md`, `tez_ekleri/*.md`, `audit/scripts/step8_invariant_rmse.py`, Makale 2 §V-A düzenlemesi ve Makale 1 MATLAB kodu hakkındaki kod okuma iddiaları. Hiçbir dosya değiştirilmedi; bu dosya dışında bir şey yazılmadı, commit yapılmadı. MATLAB çalıştırılmadı.

Denetim sırasında koşturulanlar:
- `scripts/audit_claims.py --all`: 126/126.
- `thesis_exp/iddia_denetimi/check_claims.py`: 120/120.
- `pdfinfo mobility_paper_ieee.pdf`: 9 sayfa. PDF metni yeni cümleyi içeriyor.
- Ortak fazsız RMSE ve "faz düzeltmesi" (seed 0) için scratchpad'de bağımsız bir kontrol betiği. Hiçbir sonuç dosyasına yazılmadı.

**Genel hüküm:** RAPOR.md'deki sayısal değerlerin tamamı, belirtilen ham dosyalarla (makul yuvarlamayla) eşleşiyor. Uydurulmuş ya da kaynaksız sayısal değer bulunamadı. Bulguların hepsi **ifade gücü / kapsam** ve **kaynak etiketi** düzeyinde. KRİTİK bulgu yok.

---

## ORTA

**O1. "Klasik yöntemler" genellemesi verinin desteklediğinden geniş.** (`RAPOR.md:28`, ayrıca `:79`)
- İfade: "CNN–LSTM klasik yöntemlerden daha doğru cümlesi bu ölçütle de, hızla da kurulamaz."
- Ham veri (`audit/raw/step2_baselines.json`, yayımlanan kodla, perfect_csi):

  | Yöntem | Ortak fazsız RMSE (°) | Hız (b/s/Hz) |
  | --- | --- | --- |
  | PSO | 71.65 | 5.527 |
  | PGD | 93.90 | 2.891 |
  | "WMMSE" | 93.67 | 3.003 |
  | CNN–LSTM | 2.72–3.85 | 5.797 |

- Sonuç: CNN–LSTM, PSO/PGD/WMMSE'yi her iki ölçütte de **geçiyor**. Çürütülen yalnızca CD, AO ve SPA'ya karşı üstünlük. (SPA tek geçişte tam optimumu veriyor: rmse_inv 0.0, hız 6.490.)
- Aynı sorun `:79`'da: "RMSE'nin onları cezalandırmasının nedeni bu [h_d]". Bu açıklama yalnızca CD, AO ve SPA için geçerli. PSO, PGD ve WMMSE ortak faz çıkarıldıktan sonra da 72–94°'de kalıyor; yani gerçekten kötü çalışıyorlar.
- Öneri: `:28` → "CNN–LSTM CD/AO/SPA'dan daha doğru … kurulamaz; yayımlanan PSO/PGD/WMMSE betiklerine karşı üstünlük ise korunuyor (ama bu betikler fazı hemen hiç hareket ettirmiyor ya da yakınsamıyor)". `:79`'a da aynı ayrım eklenmeli.

**O2. Ölçülmemiş bir dal "kurulabilecek doğru cümle" olarak sunulmuş.** (`RAPOR.md:31`)
- İfade: "etiket h_d'yi içerecek biçimde düzeltilirse ya da ortak faz sonradan hizalanırsa, optimuma çok yaklaşıyor."
- Ham veri: yalnızca sonradan hizalama ölçüldü (`rate_after_common_phase_fix_bpshz` 6.4880–6.4888). h_d'li etiketle yeniden eğitim **yapılmadı** (RAPOR:9 bunu kendisi söylüyor).
- Öneri: ilk dal çıkarılmalı ya da "ölçülmedi" diye işaretlenmeli (Kural 1).

**O3. Düzeltilmiş ağın h_d bilgisine ihtiyaç duyduğu yazılmamış.** (`RAPOR.md:25`, `:31`)
- `th_fix`, h_d'nin fazını kullanıyor; ağın girdisinde h_d yok. Kendi kontrolüm: etiket kullanmadan, kapalı formda en iyi ortak döndürme (∠h_d − ∠Σ b e^{jθ̂}) 6.48842 veriyor; betiğin değeri 6.48841. Yani düzeltme **adil**: klasik yöntemlerin de kullandığı CSI'yı kullanıyor ve etiket sızıntısı yok.
- Ancak F, G ve h_d elinde olan biri tam optimumu (closed_form_b / SPA) zaten kapalı formda, tek geçişte hesaplayabiliyor. "Ağ + düzeltme" bu durumda doğruluk açısından hiçbir şey kazandırmıyor.
- Öneri: `:25`'e bir cümle: "düzeltme h_d'yi gerektirir; aynı CSI ile kapalı form optimum zaten elde edilebilir."

**O4. Nicemleme satırı fazla kesin.** (`RAPOR.md:220`, Ek A)
- İfade: "Matematiksel olarak imkânsız."
- Kaynak (`audit/raw/step3_sources.json`, quant_1bit_4.12): "…floor … unless the RMSE is defined differently (e.g. vs a quantised label) — the paper does not say which." Kaynak kendisi çekince koyuyor.
- Öneri: "Sürekli etikete karşı RMSE tanımıyla imkânsız (alt sınır 52/26/13°); makale başka bir tanım vermiyor."

---

## KÜÇÜK

**K1. T3 ile RAPOR arasında yuvarlama tutarsızlığı.** (`tez_ekleri/T3_ortak_faz.md`, CD K = 20 satırı)
- T3 "%100.0" yazıyor; ham sr5_inv 0.999839. RAPOR:17 ise doğru olarak %99.98 diyor.
- Öneri: SR sütununu 2 ondalıkla yaz (`make_tez_ekleri.py:55`) ya da kesin 1.0 olmayan değere "%100" yazma.

**K2. T5'teki "Optimum hız" sütununun adı yanlış.** (`tez_ekleri/T5_csi.md`, `make_tez_ekleri.py:86,109`)
- x > 0 için bu sütun, bozuk F̂, Ĝ'den hesaplanan closed_form_b'nin hızı. Gerçek kanalın optimumu değil (x = 0.1'de 6.382; gerçek optimum 6.490). S2 şeklindeki etiket "(aynı girdi)" diyerek bunu doğru veriyor.
- Öneri: sütun adı "Kapalı form (h_d dahil, aynı bozuk girdi)".

**K3. T4 ve RAPOR'da parametre kaynakları karışık.** (`tez_ekleri/T4_parametre.md`, `RAPOR.md:133,138`)
- 17 442 (CNN-Transformer) ve 470 304 (FC-DNN) PyTorch aktarımının sayıları (`audit/raw/train/*.json`). Tabloda ise "Kod: transformer_baseline.m" ve "koddan sayılan" yazıyor; MATLAB'da sayılmadı.
- "768 fark: ikinci LSTM yanlılığı" ifadesi yanlış anlaşılabilir. 768 = 4·128 + 4·64: **her iki** LSTM katmanında PyTorch'un ek b_hh vektörü. "İkinci LSTM katmanının yanlılığı" değil.
- Öneri: "(PyTorch aktarımı)" etiketi ekle; yanlılık cümlesini "PyTorch her LSTM katmanında ikinci bir yanlılık vektörü (b_hh) taşır: 512 + 256" diye yaz.

**K4. "700'ü hiç kullanılmadı" kesin olarak doğru değil.** (`RAPOR.md:49`, `DEGISIKLIKLER.md` 18. tur)
- `scripts/mumiso_unrolled.py:141`, `run_eval(te)` ile 900 test senaryosunun **hepsini** değerlendiriyor ve sonucu `results/mumiso_eqstep_L*.json` (`test_min`) içine yazıyor. Kalan 300 test senaryosu seçimde kullanılmıyor ve makaledeki hiçbir sayıya girmiyor; ama değerlendiriliyor.
- `va[500:900]` gerçekten kullanılmıyor.
- Öneri: "makalede raporlanan ya da seçimde kullanılan hiçbir sayıya girmedi".

**K5. Makale 2 §V-A cümlesi doğru; küçük bir kapsam notu var.** (`section_05_methodology.tex:9`)
- Doğrulananlar:
  - `split_indices(6000, seed=0)` → 4200/900/900.
  - `mumiso_unrolled.py:128`, en iyi epoch'u `va[:500]` ile seçiyor.
  - `mumiso_equal_step.py:107-108` ve `mumiso_latency_parity.py:113`: `vv = va[:400]` (adım boyu **ve** amaç), `ev = te[:600]`.
  - `results/mumiso_equal_step.json` ve `mumiso_latency_parity.json` config: samples 6000, eval_n 600, val_n 400. Beş checkpoint de samples 6000.
  - 400, 500'ün öneki.
  - Şekil 5'in hız değerlerinin tamamı (learned, swept, oracle) 600 test senaryosunda.
- Kapsam notu (bu düzenlemeden önce de vardı): Şekil 5(b)'nin **zamanlamaları** `mumiso_latency_repeat.py` ile ölçülüyor. Bu betik ayrı bir `generate(64)` çekilişinin 0. senaryosunu kullanıyor; `latency_parity` ise 6000'lik çekilişin 0. senaryosunu. Gecikme içerikten neredeyse bağımsız olduğu için sonuç değişmez. Yine de "results use 600 test scenarios" yalnızca hız değerleri için kelimesi kelimesine doğru.
- Öneri: isteğe bağlı olarak "rates use 600 test scenarios".

**K6. Kısaltılan dört cümlenin anlamı korunmuş, iki küçük kayıp var.** (`section_05_methodology.tex`, 3 ve 4)
- "most are repeated in several rounds": "most"un öznesi belirsizleşti; önceki metinde "most measurements"tı.
- "timed in three rounds (load average 0.45)": önceki metindeki "from a load average of 0.45" ölçümün *öncesindeki* yükü belirtiyordu; parantez içinde bu bilgi kayboldu.
- Öneri: "most measurements …" ve "(load average 0.45 before timing)". Sayfa sınırı sorun olursa ikisi de birkaç karakterlik değişiklik.

**K7. AO/CD süre farkı tek başına kanıt değil.** (`RAPOR.md:81`)
- ±1.38 / ±1.42 farkı aynı veride deterministik olarak imkânsız; çünkü `baseline_fairness_K_analysis_v1_olcum.m:159-193` içindeki `ris_AO_timed`, CD ile aynı güncellemeyi yapıyor ve varsayılanı K = 5. Bu kısım doğru.
- Ama 0.18 / 0.15 ms farkı ayrı tic/toc ölçümlerinden gelebilir. Denetimin kendi notu da bunu söylüyor (`step0_mapping.json:91`, "unless timing noise").
- Ayrıca: Ek A'daki AO = 103.75°, `ris_AO.m` varsayılanı K = 1 ile hesaplandı. Makaledeki AO satırı K = 5'li `ris_AO_timed`'dan geldiyse, kod sonucu CD ile aynı, yani 104.02° olur.
- Öneri: kanıtı ± değerine dayandır; Ek A'da AO için "K = 1 (ris_AO.m varsayılanı); K = 5'te 104.02°" yaz.

**K8. Kaynak zinciri: commit ve gitignore.** (`RAPOR.md:21`, `step8_invariant_rmse.json`, `veri_bolme.json`)
- İki JSON'da da commit `e5af163` kayıtlı. Oysa `step8_invariant_rmse.py` ve `kontrol_bolme.py` ilk kez d5249bf'de commit edildi; koşu sırasında commit edilmemiş çalışma ağacıydı.
- `audit/raw/step8_abs_err_deg.npz`, yani S1/step8 CDF şekillerinin ham verisi, `.gitignore`'a eklenmiş ve depoda yok. Betik ~40 s'de yeniden üretiyor.
- Öneri: RAPOR'da "betik d5249bf'de commit edildi, kayıtlı commit koşu anındaki HEAD" notu; npz için yeniden üretim komutunun yeterli olduğunu açıkça yaz.

**K9. "Tamamen" ifadesi biraz güçlü.** (`RAPOR.md:25`)
- İfade: "hız kaybı (0.69) tamamen ortak fazdan."
- Ham değer: düzeltmeden sonra kalan kayıp 0.0019–0.0023 b/s/Hz, yani kaybın ~%99.7'si.
- Öneri: "neredeyse tamamen (%99.7)".

**K10. Bilgi notu: PGD betiğinde eşlenik ters.** (`RAPOR.md` tablosu, "Gradyan adımı 0.2")
- `ris_PGD.m`'deki güncelleme `z + step·conj(h)·a`. |h|²'nin yükseliş yönü ise conj(a)·h; yani betik eşleniği ters alıyor.
- Kendi kontrolüm: yönü düzeltmek sonucu değiştirmiyor. Faz yine ortalama < 1° hareket ediyor, çünkü |a| ~ 5e-3 ve adım çok küçük. RAPOR'un "fazı neredeyse hiç hareket ettirmiyor" ifadesi doğru (script_rmse 0.050; WMMSE 0.0045).
- Öneri: tabloya "(eşlenik ters; adım ölçeği çok küçük)" notu eklenebilir.

---

## Eşleştiği doğrulananlar (hata yok)

**Bölüm 1 tablosu** (`step8_invariant_rmse.json`)
- Bütün hücreler eşleşiyor: 3.18/3.13/%95.0/5.797/0.693; 2.77/2.72/%96.4/0.693; 3.90/3.85/%93.0/0.694; CD 104.02/1.10/%99.2/6.467/0.024; 104.50/0.25/%99.98/6.488/0.003; 104.79/0.05/%100/6.490/0.0002; optimum 104.85/0/6.490.
- Oranlar: "2.5–3.5 kat" (2.48–3.50). Etiket hızı 5.799.

**step8 betiği**
- φ = ∠ mean exp(j e), yani dairesel ortalama. Tam minimizasyon değil ama fark ihmal edilebilir: seed 0'da 3.1308° karşı ızgarayla tam min 3.1269°. Hesap minimuma göre üst sınır veriyor, yön güvenli.
- Etiket = −∠(G F), 1e-15 hassasiyetle doğrulandı.
- CD aktarımı `ris_CD.m` ile algoritma düzeyinde aynı: Gauss–Seidel, θ = 0 başlangıcı, mod sarma. ZIP sürümüyle de yalnızca yorum ve değişken adları farklı.
- Hız formülü step2 ile aynı.

**Bölüm 3, kod okuma iddiaları**
- Klasik yöntemler (ZIP sha256 cd176f4b… doğrulandı):
  - CD/AO: h_d var, başlangıç 0, sabit K, yakınsama testi yok.
  - AO: varsayılan K = 1.
  - SPA: H_acc = h_d, tek geçiş.
  - PGD: 0.2 / 50, birim modüle izdüşüm.
  - WMMSE: eleman başına tek adım, 0.1, K = 1; WMMSE değil.
  - PSO: 20 parçacık, 30 yineleme, tekdüze [0, 2π), w = 0.7, c = 1.5.
  - Hepsi `step2_baselines.py` ile satır satır uyumlu.
- `theta_NN_multioutput.m`:
  - `'Plots','training-progress'` (88), `ValidationFrequency 50` (90), `MiniBatchSize 256` (82).
  - nTrain = round(0.7·40000) = 28000 → floor(28000/256) = 109 yineleme/epoch.
  - Çıkış [sin; cos] (31); `net = trainNetwork(...)`, info yok (97).
  - `cnn_lstm_test_results.mat`, phase_err'i kaydediyor (131-133). THETA_pred ve THETA_true de kaydediliyor.
  - "Eksen yineleme" ve "yarım-MSE" iddiaları MATLAB belgelerine dayanıyor, koddan değil; MATLAB olmadan doğrulanamaz ama standart davranış.

**Diğer RAPOR değerleri**
- Klasik yöntemler: 103.8–104.9°; AO/PSO/SPA 103.75/104.15/104.85; PGD/WMMSE −10.30/−9.90 dB (`step2_baselines.json`).
- CDF: %92.9/94.8/96.3; p95 4.4–5.8° (`step6_eval.json`). CD'nin (a) panelinde 5°'de %3'ü (0.0296).
- CDF şekli (b): CD her K'de, 0–30° aralığında CNN'in solunda (npz'den kontrol edildi).
- CSI, x = 0.1: CNN–LSTM 19.0° (3 tohum ortalaması 18.996), kapalı form 18.66°. Hız farkı ~0.7.
- Nicemleme: 52.06/26.17/13.39 (3 tohum ortalaması); etiketin kendisi nicemlenince 51.95/25.98/12.98.
- Etiket kazancı 2.20 dB; std 0.58 (örneklem std).
- Parametreler: 727 360/565 696/161 794/162 562/13 440.
- FC-DNN 83.85°; gecikme 0.80 ms; kaynakça 7 bulunamayan / 1 geri çekilmiş.
- Tablo 6 ve Tablo 3 değerleri `step0_mapping.json` ile eşleşiyor.
- `veri_bolme.json`'daki bütün alanlar.

**T1** (`sumiso_representation.json`)
- 18 hücrenin hepsi eşleşiyor.
- 0.38 örneklem std'si; popülasyon std'si 0.31, RAPOR:185'teki açıklama doğru.

**T2, T5**
- T2: kodla uyumlu.
- T5: değerler doğru (3 tohum ortalaması); yalnızca K2'deki sütun adı sorunu var.

**Makale 2**
- 9 sayfa, 46 kaynak.
- Yeni cümle PDF'te var.
- 126/126 ve 120/120 yeniden koşturuldu, tuttu.
