# Bağımsız sayısal denetim — Jüri sorusu 5 (REPORT_S5.md + yorum_s5.md)

Denetim tarihi 16 Kasım 2026. Dal `thesis/p4-deneyler`. Denetlenen: `thesis_exp/juri/REPORT_S5.md` (rapor commit'i `37cd1a9`, değerlendirme `19a5eb6`), `thesis_exp/juri/yorum_s5.md`, ön kayıt `thesis_exp/juri/ON_KAYIT_S5.md`.
Betik: `thesis_exp/denetim_log/juri_s5_denetim.py` (`nice -n 19 python3 thesis_exp/denetim_log/juri_s5_denetim.py`; tek süreç, birkaç saniye; kanal üretimi yok, eğitim yok, ileri geçiş yok). Kaynak yalnızca ham JSON: `s5/raw/eval.json` (senaryo başına diziler), `train_*.json`, `link_budget.json`, `../raw/timing.json`, `../raw/timing2.json`; checkpoint'ler yalnızca ağırlık karşılaştırması için yüklendi. Bootstrap: `numpy.default_rng(20261116)`, 2000 eşli yeniden örnekleme, yüzdelik %95. Ölçüm öncesi yük 0.29.

## Özet

- **202 sayı denetlendi: 202 OK, 0 HATA, 0 ÜRETİLEMEDİ.** Rapordaki her tablo hücresi (en iyi klasik kol seçimi, gecikmeler, t = 0 ve etkin hızlar, farklar, GA'lar), S5-H1/H2/H3 kararları, S5-E1/E2, eğitim tablosu, bağlantı bütçesi telafisi ve yorumdaki her sayı ("4 kat", "5.115 → 5.011", "0.06–0.08", "0.11–0.16", "+0.37", "+0.47", "+0.04…+0.05", "~5.0", "0.8 ms", "T_c ≈ 3 ms") ham veriden yeniden üretildi. GA'lar 0.01 içinde.
- **Kararlar ön kayda birebir uyuyor:** H1 TUTMADI (−0.381), H2 TUTMADI (NN+Adam-1, −0.158), H3 TUTTU (+0.470). Ön kayıt (`d7ac933`, 12:36:32) eğitimden önce commit'lenmiş; telafi yalnızca eğitim tohumu 21'den, sonuçlardan önce (`bdcd899`, 12:32) hesaplanmış. Test tohumu 11 eğitim betiğinde hiç yok.
- **Sonuç değiştiren kod hatası bulunmadı.** KRİTİK bulgu yok.
- **Raporda olmayan, aleyhte bir bulgu (ORTA, Kural 10 gereği yukarı yazılmalı):** 28 GHz'de eğitilmiş ağ, kapalı formdaki en ucuz kol SU-average'ı (0.23 ms, ağdan daha hızlı) **anlamlı biçimde geçemiyor**: 1.5 m/s'de NN-sincos − SU-average etkin hızda +0.021 [−0.015, +0.056], 3 km/h'de +0.030 [−0.004, +0.065]. t = 0'da 4.650'ye 4.611. "Ağ öğreniyor" cümlesi yalnızca eğitilmemiş ağa göre doğru; en basit klasik başlangıca göre ağın katkısı 28 GHz'de istatistiksel olarak sıfırdan ayırt edilemiyor (3 GHz'de +0.087 [+0.029, +0.148]).
- Yorumda dört ifade düzeltilmeli (iki ORTA, ikisi KÜÇÜK): başlıktaki genelleme, savunu cümlesiyle çelişen gerekçe, tek eğitim koşusuna dayanan "tutarlı etki" ifadesi ve karma kolun "daha iyi değil" diye yumuşatılması (aslında eşit L'de anlamlı biçimde daha kötü).

## Bulgular

### KRİTİK

Yok.

### ORTA

1. **Ağ ile SU-average arasındaki fark raporlanmamış ve 28 GHz'de anlamsız** (`analyze_s5.py:98` — kol listesi yalnızca NN-sincos, NN-angle, NN-untrained, en iyi karma, SU-best-of). Yeniden hesap (`juri_s5_denetim.py`, "Ek mantık denetimleri"): 28 GHz 1.5 m/s +0.021 [−0.015, +0.056]; 28 GHz 3 km/h +0.030 [−0.004, +0.065]; 3 GHz her iki hızda ≈ +0.087 [+0.03, +0.15]. Ağın gecikmesi (0.43 ms) SU-average'ınkinden (0.23 ms) büyük olduğu için, gecikmenin daha da baskın olduğu (daha hızlı) bir rejimde ağın en iyi olasılığı SU-average ile başa baş kalmaktır. **Düzeltme:** SU-average'ı `analyze_s5.py:98` listesine ekleyip raporu yeniden üret; yorumda "Ağ öğreniyor" cümlesine "eğitilmemiş ağa göre; 28 GHz'de SU-average'tan anlamlı biçimde iyi değil" kaydı eklensin.
2. **Başlıktaki genelleme tek mimariyi aşıyor** (`yorum_s5.md`, 1. madde: "yapay zekâ ekseni, en elverişli rejimde de olumsuz kapanıyor"). Sınanan: tek mimari, tek model başlangıç tohumu (0), 20 000 örnek. Eğitim günlükleri bu rejimin veri kısıtlı olduğunu gösteriyor: eğitim soft-min'i 60. epoch'a kadar artarken (28_sincos 4.70) doğrulama 10.–12. epoch'ta doruğa ulaşıp düşüyor (4.396 → 4.313). Her model ~2.7 dakikada bitti; ön kayıttaki bütçe 25 dakikaydı ve 20 000 örneğin üretimi 13–14 s sürdü. Yani daha büyük veri ucuzdu ve denenmedi. "Sınırlar" maddesi bunu söylüyor, ama başlık söylemiyor. Ayrıca "en elverişli rejim" yalnızca 1.5 m/s ve 3 km/h ile sınandı; 28 GHz'de daha yüksek hız ölçülmedi (bkz. madde 1: orada bile ağın tavanı SU-average ile başa baş). **Düzeltme:** başlığı "bu mimari ve bu eğitim bütçesiyle" diye daralt. Olumsuz hükmü yumuşatma; kapsamını doğru yaz.
3. **Gerekçe savunu cümlesiyle çelişiyor** (`yorum_s5.md`, 2. madde): "Savunu cümlesi … burada da işliyor: kazananı gecikme değil, tek geçişli ağın kalite tavanı belirliyor." İkinci yarı birinciyi çürütüyor. Veri ikinci yarıyı destekliyor: ağın gecikmesi sıfır olsaydı bile etkin hızı t = 0 değerini (4.650) aşamazdı ve bu, en iyi klasik koldan 0.361 düşük. Yani NN-klasik sıralamasını bu hücrede gecikme değil kalite belirliyor. Gecikme ise klasik kollar arasındaki sıralamayı belirliyor (28 GHz 1.5 m/s'de SU-best-of, 3 km/h'de Adam-1|best, 3 GHz'de Adam-6/10). **Düzeltme:** "savunu cümlesi burada da işliyor" ifadesini kaldır ya da yalnızca klasik kollar arasındaki sıralamayla sınırla. "4 kat daralıyor" sayısı doğru (−1.523 / −0.381 = 4.0); ama iki uç farklı başvuru kollarına ve farklı (telafili) kanallara göre ölçülüyor. Bu bir oran değil, iki ayrı farkın yan yana konması.
4. **S5-E1 "tutarlı etki" tek eğitim koşusuna dayanıyor** (`yorum_s5.md`, 5. madde). +0.043…+0.049 farkının GA'sı senaryo üzerinden alınıyor. Model başlangıç tohumu ve toplu sıra tohumu her kafa için tek (0). Eğitim koşuları arasındaki değişkenlik GA'ya girmiyor. Bu büyüklükteki (doğrulamada 4.396'ya 4.382) bir farkın başka tohumlarda yön değiştirip değiştirmediği bilinmiyor. "Anlamlı biçimde geçiyor" ve "Makale 1'in katkısı bu … tutarlı etki üzerinden konumlandırılabilir" ifadeleri yapay zekâ lehine bir genelleme. Bu durumda Kural 10'un tersi geçerli. **Düzeltme:** "tek eğitim koşusu (model tohumu 0); eğitim tohumu değişkenliği ölçülmedi" kaydını ekle, "tutarlı" kelimesini kaldır. Keşifsel olduğu zaten yazılı.

### KÜÇÜK

5. **Karma kol yumuşatılmış** (`yorum_s5.md`, 4. madde: "SU-best-of başlangıcından daha iyi bir başlangıç değil"). Eşit L'de NN+Adam-L − Adam-L|best farkı t = 0'da her hücrede ve her denetlenen L'de (1, 2, 6, 12) anlamlı biçimde negatif. Örneğin 28 GHz'de L = 1 için −0.303 [−0.342, −0.263], 3 GHz'de L = 1 için −0.353 [−0.408, −0.300]. Etkin hızda ağın 0.81 ms'lik avantajına rağmen fark çoğunlukla negatif. **Düzeltme:** "daha kötü bir başlangıç" yaz.
6. **"0.8 ms'lik gecikme farkı … ~0.1'e mal oluyor"** (`yorum_s5.md`, 1. madde). 0.104 (5.115 → 5.011), SU-best-of'un 1.24 ms'lik **tüm** yaşlanma kaybıdır; 0.81 ms'lik farka düşen pay bundan küçüktür. SU-best-of'un 0.43 ms'deki değeri `eval.json`'da yok: payın kendisi ÜRETİLEMEDİ, yalnızca üst sınırı (0.104) biliniyor. **Düzeltme:** "1.24 ms'lik gecikmenin tamamı ~0.1'e mal oluyor" yaz.
7. **"Doğrulama hızı 10–20. epoch'ta doruğa ulaştı"**: gerçekte 10, 12, 10. Doğru ama gevşek; "10.–12." yaz.
8. **Eski zamanlama dosyası** (`s5/eval_s5.py:15`). CD-s gecikmeleri, Sapma 2'de erken durma yanlılığı bulunan `raw/timing.json`'dan alınıyor (`timing3.json` 12:58'de, S5 değerlendirmesinden sonra geldi). Yanlılık CD lehine. CD hiçbir hücrede en iyi klasik değil (en iyi CD seed 11'de 4.812–5.080, en iyi klasik 5.011–6.442). Bu yüzden düzeltme seçimi ve kararları değiştiremez. Ayrıca derlenmiş CD (S1'de 3 GHz 1.5 m/s'de Python Adam'ı +0.684 geçen kol) ön kayıt gereği klasik kümede yok. 3 GHz'deki NN ve karma açıkları bu yüzden yalnızca **Python klasik kümesine** göredir; derlenmiş CD'ye göre büyüklükleri ÜRETİLEMEDİ (o gecikmede değerlendirme ham veride yok). Hüküm yönünü değiştirmez, ancak "karma 3 GHz'de en iyi klasiğin yalnızca 0.06–0.08 gerisinde" cümlesine "Python gerçekleştirmeli klasik kollar arasında" kaydı eklenmeli.
9. **Zamanlama protokolü (Kural 5).** NN gecikmesi için yalnızca başlangıç yükü (2.32; betik < 0.5'i bekledi) kaydedilmiş, ölçüm sonrası yük kaydedilmemiş (`s5/eval_s5.py:26-43`). Klasik gecikmeler (`timing2.json`) ayrı bir oturumda ölçüldü ve turlar sırasında yük 0.53–0.74'e çıktı. Kararlara etkisi yok: ağın gecikmesi sıfır olsa da H1 tutmaz (t = 0 hızı 4.650 < 5.011).
10. **Gecikme defteri doğru, ama interpolasyon raporda belirtilmemiş.** Bütün kolların gecikmesi `başlangıç + adam(L)` ve `NN + adam(L)` ile birebir yeniden üretildi (0 sapma). Ancak L ∈ {3, 5, 6, 10, 12, 20, 24} için adam(L), ölçülmüş L ∈ {1, 2, 4, 8, 16, 32, 48} arasında doğrusal interpolasyondur. Ön kayıt "L ∈ {1, …, 48}" diyor; kullanılan küme 14 değerli bir alt küme (`eval_s5.py:16`; ön kayıt commit'inde kodda sabit). Bu bir sapma değil, bir belirsizlik; ama raporda bir cümleyle yazılmalı.
11. **Ölü başvuru:** `s5/model.py:13` "see check_layout" diyor; böyle bir işlev yok. Yerleşim elle doğrulandı: `RISPanel` `index = i*K + j` (i ∈ 0..7 e1 boyunca, j ∈ 0..3 e2 boyunca; `ris_mu/geometry.py:48-51`). `features` ise `[S, C, N] → [S, C, 8, 4]` (n = r·4 + c). Izgara komşuları fiziksel komşular; yerleşim doğru.
12. **Fraunhofer denetimi atlanmış:** `s5/ch28.py:20-25`, `make_mumiso_scenario`'nun uzak alan denetimini kopyalamıyor. Zararsız: 28 GHz'de 2(M·d)²/λ = 0.34 m, 3 GHz'deki 3.2 m'den küçük, ve aynı BS konumu 3 GHz'de bu denetimi geçiyor.
13. **Commit kaydı:** `train.py:163` commit'i eğitim **sonunda** yazıyor (`train_28_sincos.json`: `bc1e636+dirty`, analiz betiği commit'i); `eval.json`'ın commit'i `19a5eb6` bir denetim betiği commit'i. `git diff d7ac933 HEAD` S5 kodunda (`ch28.py`, `model.py`, `train.py`, `eval_s5.py`, `p4/common.py`) değişiklik göstermiyor, yani koşan kod ön kayıttaki kod. Yine de commit, koşunun başında alınmalı.

## Kod incelemesi (sonuç değiştiren hata aranarak)

| Konu | Durum | Not |
| --- | --- | --- |
| Öznitelikler ve panel yerleşimi | doğru | a_{k,n} = g_{k,n}(f_nᴴu_k), kullanıcı başına rms; kaskat [K·T = 32] kanal, senaryo rms'i; n = r·COLS + c, `RISPanel` sırasıyla aynı |
| sin/cos kafası | doğru | `o / ‖o‖` kanal ekseninde (dim 1), θ = atan2(o₀, o₁); açı kafası π·tanh |
| Gecikme defteri | doğru | her kol başlangıcını içeriyor; NN+Adam-L = NN + adam(L); 0 sapma |
| Tam gecikme indeksleme | doğru | `times = [0] + sorted(round(LAT, 9))`, `A.idx(round(LAT[k], 9))`; interpolasyon yok |
| t = 0 fazları ↔ zaman ızgarası | doğru | üreteç rastgele akışı ızgaradan ve hızdan bağımsız (sabit chunk 500, t = 0 ilk eleman); t0 dizileri iki hızda birebir aynı |
| 28 GHz kanalı | doğru | `RISPanel(fc = 28 GHz)` → d = λ/2, k, BS ULA aralığı 0.5λ (`channel.py:113`), `PathLoss(panel.fc)` (`channel.py:96`), Doppler konumdan kendiliğinden; f_d 140.1 / 77.8 Hz |
| Telafi nv'ye | doğru | `nv = 10^(−comp/10) / snr_scale` (`ch28.py:43`), eğitimde ve değerlendirmede aynı (compensate = True); günlükte snr 3.007e14 / 2.506e11 = 30.79 dB |
| Telafi yalnızca eğitim tohumu | doğru | `link_budget.py`: seed 21, n = 2000 (eğitimle aynı tohum, farklı n; test tohumu yok) |
| Doğrulama yalnızca epoch seçimi | doğru | `train.py` yalnızca seed 21 (eğitim) ve 12 (doğrulama); seed 11 hiç geçmiyor |
| Eğitilmemiş checkpoint | doğru | `net_28_sincos_untrained.pt` = taze `PhaseNet(seed 0)` = `net_3_sincos_untrained.pt`; eğitilmiş ağırlıklardan farklı (en büyük fark 0.19) |
| Eğitilmiş checkpoint = en iyi epoch | kısmen | `best_val = max(history)` doğrulandı; ağırlıkların o epoch'a ait olduğu ileri geçiş gerektirir: ÜRETİLEMEDİ (kanal üretimi yasak) |

## Mantık denetimi

- **Ön kayıt sırası:** `d7ac933` (12:36:32), ON_KAYIT_S5 + `ch28/model/train/eval_s5/link_budget.py` + `link_budget.json`. İlk eğitim 12:45'te 165 s sonra bitti, yani ~12:42'de başladı. Değerlendirme 12:55. Karar betiği `analyze_s5.py` 12:45:22'de (`bc1e636`) commit'lendi: ilk modelin doğrulama günlüğü görülmüş, test sonucu görülmemişti. Karar kuralları ön kayda birebir uyuyor.
- **En iyi klasik seçimi:** seed 12'de etkin hıza göre, ön kayıttaki küme üzerinden (SU-average, SU-best-of, iki başlangıçtan Adam-L, CD-1..8). Seçilenler seed 11'in en iyileriyle aynı; yalnızca 3 GHz 1.5 m/s'de seed 11'in en iyisi Adam-5|best (6.236, seçilen Adam-6|best 6.234).
- **Sağlamlık:** H1, ağın gecikmesinden bağımsız olarak tutmaz (NN t = 0 hızı − en iyi klasik etkin hız = −0.361, 28 GHz 1.5 m/s). "Ağ 10 kat hızlansaydı bile" cümlesi bu yüzden doğru, hatta daha güçlü yazılabilir.
- **Aleyhte bulguların konumu:** H1/H2'nin tutmaması raporun en üstünde ve yumuşatılmamış. Karşı yönde (ORTA 2, 4) olumsuz hüküm tek mimarinin ötesine taşınmış, olumlu keşifsel bulgu tek eğitim koşusunun ötesine taşınmış.

## Denetlenen sayılar (betik çıktısı)

| denetlenen | rapor | yeniden hesap | durum |
| --- | --- | --- | --- |
| t0 dizileri hızdan bağımsız (28 GHz, seed 12) | aynı | aynı | OK |
| t0 dizileri hızdan bağımsız (28 GHz, seed 11) | aynı | aynı | OK |
| t0 dizileri hızdan bağımsız (3 GHz, seed 12) | aynı | aynı | OK |
| t0 dizileri hızdan bağımsız (3 GHz, seed 11) | aynı | aynı | OK |
| NN gecikmesi (ms, tur medyanı) | 0.425 | 0.4255 | OK |
| NN turları (ms) | [+0.463, +0.425, +0.418, +0.420, +0.440] | [+0.463, +0.425, +0.418, +0.420, +0.440] | OK |
| eval.json gecikme defteri = başlangıç + adam(L) (tüm kollar) | 0 sapma | 0 sapma | OK |
| telafi comp_db = 10 log10(P3/P28) | 30.79 | 30.79 | OK |
| telafi tohumu (eğitim) | 21 | 21 | OK |
| 28 GHz 1.5 m/s: f_d (Hz) | 140 | 140.1 | OK |
| 28 GHz 1.5 m/s: en iyi klasik (seed 12) | SU-best-of | SU-best-of | OK |
| 28 GHz 1.5 m/s: en iyi klasik gecikme | 1.24 | 1.238 | OK |
| 28 GHz 1.5 m/s: en iyi klasik etkin hız (seed 11) | 5.011 | 5.011 | OK |
| 28 GHz 1.5 m/s: en iyi karma (seed 12) | NN+Adam-1 | NN+Adam-1 | OK |
| 28 GHz 1.5 m/s NN-sincos: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 1.5 m/s NN-sincos: t=0 | 4.65 | 4.65 | OK |
| 28 GHz 1.5 m/s NN-sincos: etkin | 4.63 | 4.63 | OK |
| 28 GHz 1.5 m/s NN-sincos: − en iyi klasik | -0.381 | -0.3808 | OK |
| 28 GHz 1.5 m/s NN-sincos: GA | [-0.444, -0.314] | [-0.445, -0.318] | OK |
| 28 GHz 1.5 m/s NN-angle: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 1.5 m/s NN-angle: t=0 | 4.601 | 4.601 | OK |
| 28 GHz 1.5 m/s NN-angle: etkin | 4.587 | 4.587 | OK |
| 28 GHz 1.5 m/s NN-angle: − en iyi klasik | -0.424 | -0.424 | OK |
| 28 GHz 1.5 m/s NN-angle: GA | [-0.496, -0.356] | [-0.496, -0.357] | OK |
| 28 GHz 1.5 m/s NN-untrained: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 1.5 m/s NN-untrained: t=0 | 4.181 | 4.181 | OK |
| 28 GHz 1.5 m/s NN-untrained: etkin | 4.171 | 4.171 | OK |
| 28 GHz 1.5 m/s NN-untrained: − en iyi klasik | -0.84 | -0.8405 | OK |
| 28 GHz 1.5 m/s NN-untrained: GA | [-0.944, -0.748] | [-0.940, -0.747] | OK |
| 28 GHz 1.5 m/s NN+Adam-1: gecikme | 1.58 | 1.579 | OK |
| 28 GHz 1.5 m/s NN+Adam-1: t=0 | 5.043 | 5.043 | OK |
| 28 GHz 1.5 m/s NN+Adam-1: etkin | 4.853 | 4.853 | OK |
| 28 GHz 1.5 m/s NN+Adam-1: − en iyi klasik | -0.158 | -0.1581 | OK |
| 28 GHz 1.5 m/s NN+Adam-1: GA | [-0.203, -0.112] | [-0.207, -0.112] | OK |
| 28 GHz 1.5 m/s SU-best-of: gecikme | 1.24 | 1.238 | OK |
| 28 GHz 1.5 m/s SU-best-of: t=0 | 5.115 | 5.115 | OK |
| 28 GHz 1.5 m/s SU-best-of: etkin | 5.011 | 5.011 | OK |
| 28 GHz 1.5 m/s SU-best-of: − en iyi klasik | 0 | 0 | OK |
| 28 GHz 1.5 m/s SU-best-of: GA (özdeş kol) | [+0.000, +0.000] | [+0.000, +0.000] | OK |
| 28 GHz 3 km/h: f_d (Hz) | 78 | 77.83 | OK |
| 28 GHz 3 km/h: en iyi klasik (seed 12) | Adam-1|best | Adam-1|best | OK |
| 28 GHz 3 km/h: en iyi klasik gecikme | 2.39 | 2.392 | OK |
| 28 GHz 3 km/h: en iyi klasik etkin hız (seed 11) | 5.145 | 5.145 | OK |
| 28 GHz 3 km/h: en iyi karma (seed 12) | NN+Adam-2 | NN+Adam-2 | OK |
| 28 GHz 3 km/h NN-sincos: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 3 km/h NN-sincos: t=0 | 4.65 | 4.65 | OK |
| 28 GHz 3 km/h NN-sincos: etkin | 4.64 | 4.64 | OK |
| 28 GHz 3 km/h NN-sincos: − en iyi klasik | -0.505 | -0.5048 | OK |
| 28 GHz 3 km/h NN-sincos: GA | [-0.574, -0.440] | [-0.574, -0.439] | OK |
| 28 GHz 3 km/h NN-angle: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 3 km/h NN-angle: t=0 | 4.601 | 4.601 | OK |
| 28 GHz 3 km/h NN-angle: etkin | 4.594 | 4.594 | OK |
| 28 GHz 3 km/h NN-angle: − en iyi klasik | -0.551 | -0.5509 | OK |
| 28 GHz 3 km/h NN-angle: GA | [-0.623, -0.484] | [-0.622, -0.481] | OK |
| 28 GHz 3 km/h NN-untrained: gecikme | 0.43 | 0.4255 | OK |
| 28 GHz 3 km/h NN-untrained: t=0 | 4.181 | 4.181 | OK |
| 28 GHz 3 km/h NN-untrained: etkin | 4.176 | 4.176 | OK |
| 28 GHz 3 km/h NN-untrained: − en iyi klasik | -0.969 | -0.9692 | OK |
| 28 GHz 3 km/h NN-untrained: GA | [-1.073, -0.867] | [-1.071, -0.875] | OK |
| 28 GHz 3 km/h NN+Adam-2: gecikme | 2.71 | 2.706 | OK |
| 28 GHz 3 km/h NN+Adam-2: t=0 | 5.256 | 5.256 | OK |
| 28 GHz 3 km/h NN+Adam-2: etkin | 5.033 | 5.033 | OK |
| 28 GHz 3 km/h NN+Adam-2: − en iyi klasik | -0.112 | -0.1122 | OK |
| 28 GHz 3 km/h NN+Adam-2: GA | [-0.146, -0.082] | [-0.144, -0.079] | OK |
| 28 GHz 3 km/h SU-best-of: gecikme | 1.24 | 1.238 | OK |
| 28 GHz 3 km/h SU-best-of: t=0 | 5.115 | 5.115 | OK |
| 28 GHz 3 km/h SU-best-of: etkin | 5.077 | 5.077 | OK |
| 28 GHz 3 km/h SU-best-of: − en iyi klasik | -0.068 | -0.06817 | OK |
| 28 GHz 3 km/h SU-best-of: GA | [-0.099, -0.037] | [-0.099, -0.035] | OK |
| 3 GHz 1.5 m/s: f_d (Hz) | 15 | 15.01 | OK |
| 3 GHz 1.5 m/s: en iyi klasik (seed 12) | Adam-6|best | Adam-6|best | OK |
| 3 GHz 1.5 m/s: en iyi klasik gecikme | 7.87 | 7.868 | OK |
| 3 GHz 1.5 m/s: en iyi klasik etkin hız (seed 11) | 6.234 | 6.234 | OK |
| 3 GHz 1.5 m/s: en iyi karma (seed 12) | NN+Adam-6 | NN+Adam-6 | OK |
| 3 GHz 1.5 m/s NN-sincos: gecikme | 0.43 | 0.4255 | OK |
| 3 GHz 1.5 m/s NN-sincos: t=0 | 4.71 | 4.71 | OK |
| 3 GHz 1.5 m/s NN-sincos: etkin | 4.711 | 4.711 | OK |
| 3 GHz 1.5 m/s NN-sincos: − en iyi klasik | -1.523 | -1.523 | OK |
| 3 GHz 1.5 m/s NN-sincos: GA | [-1.617, -1.433] | [-1.614, -1.428] | OK |
| 3 GHz 1.5 m/s NN-untrained: gecikme | 0.43 | 0.4255 | OK |
| 3 GHz 1.5 m/s NN-untrained: t=0 | 4.341 | 4.341 | OK |
| 3 GHz 1.5 m/s NN-untrained: etkin | 4.341 | 4.341 | OK |
| 3 GHz 1.5 m/s NN-untrained: − en iyi klasik | -1.892 | -1.892 | OK |
| 3 GHz 1.5 m/s NN-untrained: GA | [-1.994, -1.790] | [-1.995, -1.789] | OK |
| 3 GHz 1.5 m/s NN+Adam-6: gecikme | 7.05 | 7.055 | OK |
| 3 GHz 1.5 m/s NN+Adam-6: t=0 | 6.339 | 6.339 | OK |
| 3 GHz 1.5 m/s NN+Adam-6: etkin | 6.158 | 6.158 | OK |
| 3 GHz 1.5 m/s NN+Adam-6: − en iyi klasik | -0.075 | -0.07533 | OK |
| 3 GHz 1.5 m/s NN+Adam-6: GA | [-0.115, -0.037] | [-0.116, -0.037] | OK |
| 3 GHz 1.5 m/s SU-best-of: gecikme | 1.24 | 1.238 | OK |
| 3 GHz 1.5 m/s SU-best-of: t=0 | 5.276 | 5.276 | OK |
| 3 GHz 1.5 m/s SU-best-of: etkin | 5.278 | 5.278 | OK |
| 3 GHz 1.5 m/s SU-best-of: − en iyi klasik | -0.956 | -0.956 | OK |
| 3 GHz 1.5 m/s SU-best-of: GA | [-1.021, -0.892] | [-1.024, -0.889] | OK |
| 3 GHz 3 km/h: f_d (Hz) | 8 | 8.339 | OK |
| 3 GHz 3 km/h: en iyi klasik (seed 12) | Adam-10|best | Adam-10|best | OK |
| 3 GHz 3 km/h: en iyi klasik gecikme | 12.27 | 12.27 | OK |
| 3 GHz 3 km/h: en iyi klasik etkin hız (seed 11) | 6.442 | 6.442 | OK |
| 3 GHz 3 km/h: en iyi karma (seed 12) | NN+Adam-12 | NN+Adam-12 | OK |
| 3 GHz 3 km/h NN-sincos: gecikme | 0.43 | 0.4255 | OK |
| 3 GHz 3 km/h NN-sincos: t=0 | 4.71 | 4.71 | OK |
| 3 GHz 3 km/h NN-sincos: etkin | 4.71 | 4.71 | OK |
| 3 GHz 3 km/h NN-sincos: − en iyi klasik | -1.732 | -1.732 | OK |
| 3 GHz 3 km/h NN-sincos: GA | [-1.833, -1.634] | [-1.832, -1.637] | OK |
| 3 GHz 3 km/h NN-untrained: gecikme | 0.43 | 0.4255 | OK |
| 3 GHz 3 km/h NN-untrained: t=0 | 4.341 | 4.341 | OK |
| 3 GHz 3 km/h NN-untrained: etkin | 4.341 | 4.341 | OK |
| 3 GHz 3 km/h NN-untrained: − en iyi klasik | -2.101 | -2.101 | OK |
| 3 GHz 3 km/h NN-untrained: GA | [-2.209, -1.995] | [-2.212, -1.998] | OK |
| 3 GHz 3 km/h NN+Adam-12: gecikme | 13.68 | 13.68 | OK |
| 3 GHz 3 km/h NN+Adam-12: t=0 | 6.642 | 6.642 | OK |
| 3 GHz 3 km/h NN+Adam-12: etkin | 6.38 | 6.38 | OK |
| 3 GHz 3 km/h NN+Adam-12: − en iyi klasik | -0.063 | -0.06276 | OK |
| 3 GHz 3 km/h NN+Adam-12: GA | [-0.095, -0.032] | [-0.096, -0.028] | OK |
| 3 GHz 3 km/h SU-best-of: gecikme | 1.24 | 1.238 | OK |
| 3 GHz 3 km/h SU-best-of: t=0 | 5.276 | 5.276 | OK |
| 3 GHz 3 km/h SU-best-of: etkin | 5.278 | 5.278 | OK |
| 3 GHz 3 km/h SU-best-of: − en iyi klasik | -1.165 | -1.165 | OK |
| 3 GHz 3 km/h SU-best-of: GA | [-1.234, -1.094] | [-1.236, -1.097] | OK |
| tablo hücre sayısı | 4 | 4 | OK |
| S5-H1 fark | -0.381 | -0.3808 | OK |
| S5-H1 GA | [-0.444, -0.314] | [-0.445, -0.321] | OK |
| S5-H1 karar | TUTMADI | TUTMADI | OK |
| S5-H2 kol | NN+Adam-1 | NN+Adam-1 | OK |
| S5-H2 fark | -0.158 | -0.1581 | OK |
| S5-H2 GA | [-0.203, -0.112] | [-0.202, -0.112] | OK |
| S5-H2 karar | TUTMADI | TUTMADI | OK |
| S5-H3 fark | 0.47 | 0.4698 | OK |
| S5-H3 GA | [+0.396, +0.552] | [+0.398, +0.548] | OK |
| S5-H3 karar | TUTTU | TUTTU | OK |
| S5-E1 1.5 m/s t0: fark | 0.049 | 0.04919 | OK |
| S5-E1 1.5 m/s t0: GA | [+0.018, +0.080] | [+0.019, +0.081] | OK |
| S5-E1 1.5 m/s eff: fark | 0.043 | 0.04322 | OK |
| S5-E1 1.5 m/s eff: GA | [+0.014, +0.072] | [+0.012, +0.074] | OK |
| S5-E1 3 km/h t0: fark | 0.049 | 0.04919 | OK |
| S5-E1 3 km/h t0: GA | [+0.019, +0.082] | [+0.020, +0.082] | OK |
| S5-E1 3 km/h eff: fark | 0.046 | 0.04601 | OK |
| S5-E1 3 km/h eff: GA | [+0.016, +0.076] | [+0.015, +0.075] | OK |
| S5-E2, 3 GHz 1.5 m/s: NN fark | -1.523 | -1.523 | OK |
| S5-E2, 3 GHz 1.5 m/s: NN GA | [-1.617, -1.433] | [-1.624, -1.428] | OK |
| S5-E2, 3 GHz 1.5 m/s: karma kol | NN+Adam-6 | NN+Adam-6 | OK |
| S5-E2, 3 GHz 1.5 m/s: karma fark | -0.075 | -0.07533 | OK |
| S5-E2, 3 GHz 1.5 m/s: karma GA | [-0.115, -0.037] | [-0.115, -0.035] | OK |
| S5-E2, 3 GHz 1.5 m/s: eğitilmiş−eğitilmemiş | 0.369 | 0.3687 | OK |
| S5-E2, 3 GHz 1.5 m/s: eğitilmiş−eğitilmemiş GA | [+0.280, +0.462] | [+0.275, +0.459] | OK |
| S5-E2, 3 GHz 3 km/h: NN fark | -1.732 | -1.732 | OK |
| S5-E2, 3 GHz 3 km/h: NN GA | [-1.833, -1.634] | [-1.834, -1.633] | OK |
| S5-E2, 3 GHz 3 km/h: karma kol | NN+Adam-12 | NN+Adam-12 | OK |
| S5-E2, 3 GHz 3 km/h: karma fark | -0.063 | -0.06276 | OK |
| S5-E2, 3 GHz 3 km/h: karma GA | [-0.095, -0.032] | [-0.095, -0.029] | OK |
| S5-E2, 3 GHz 3 km/h: eğitilmiş−eğitilmemiş | 0.369 | 0.3687 | OK |
| S5-E2, 3 GHz 3 km/h: eğitilmiş−eğitilmemiş GA | [+0.275, +0.461] | [+0.283, +0.466] | OK |
| S5-E2, 28 GHz 3 km/h: NN fark | -0.505 | -0.5048 | OK |
| S5-E2, 28 GHz 3 km/h: NN GA | [-0.574, -0.440] | [-0.575, -0.436] | OK |
| S5-E2, 28 GHz 3 km/h: karma kol | NN+Adam-2 | NN+Adam-2 | OK |
| S5-E2, 28 GHz 3 km/h: karma fark | -0.112 | -0.1122 | OK |
| S5-E2, 28 GHz 3 km/h: karma GA | [-0.146, -0.082] | [-0.145, -0.079] | OK |
| S5-E2, 28 GHz 3 km/h: eğitilmiş−eğitilmemiş | 0.47 | 0.4698 | OK |
| S5-E2, 28 GHz 3 km/h: eğitilmiş−eğitilmemiş GA | [+0.394, +0.547] | [+0.400, +0.549] | OK |
| eğitim 28_sincos: en iyi doğrulama | 4.396 | 4.396 | OK |
| eğitim 28_sincos: best_val = max(history) | 4.396 | 4.396 | OK |
| eğitim 28_sincos: en iyi epoch | 10 | 10 | OK |
| eğitim 28_sincos: son epoch | 60 | 60 | OK |
| eğitim 28_sincos: süre (s) | 165 | 164.6 | OK |
| eğitim 28_sincos: n_train | 2e+04 | 2e+04 | OK |
| eğitim 28_sincos: son epoch doğrulaması en iyiden düşük | evet | evet | OK |
|   (bilgi) 28_sincos: epoch-0 doğrulama / en iyi / son | - | 3.9374 / 4.3960 / 4.3129 | bilgi |
| eğitim 28_angle: en iyi doğrulama | 4.382 | 4.382 | OK |
| eğitim 28_angle: best_val = max(history) | 4.382 | 4.382 | OK |
| eğitim 28_angle: en iyi epoch | 12 | 12 | OK |
| eğitim 28_angle: son epoch | 60 | 60 | OK |
| eğitim 28_angle: süre (s) | 158 | 158.3 | OK |
| eğitim 28_angle: n_train | 2e+04 | 2e+04 | OK |
| eğitim 28_angle: son epoch doğrulaması en iyiden düşük | evet | evet | OK |
|   (bilgi) 28_angle: epoch-0 doğrulama / en iyi / son | - | 3.9134 / 4.3821 / 4.2900 | bilgi |
| eğitim 3_sincos: en iyi doğrulama | 4.317 | 4.317 | OK |
| eğitim 3_sincos: best_val = max(history) | 4.317 | 4.317 | OK |
| eğitim 3_sincos: en iyi epoch | 10 | 10 | OK |
| eğitim 3_sincos: son epoch | 60 | 60 | OK |
| eğitim 3_sincos: süre (s) | 164 | 163.8 | OK |
| eğitim 3_sincos: n_train | 2e+04 | 2e+04 | OK |
| eğitim 3_sincos: son epoch doğrulaması en iyiden düşük | evet | evet | OK |
|   (bilgi) 3_sincos: epoch-0 doğrulama / en iyi / son | - | 3.9700 / 4.3166 / 4.2593 | bilgi |
| eğitilmemiş 28 = eğitilmemiş 3 (aynı tohum 0 başlangıcı) | evet | evet | OK |
| eğitilmiş 28 sincos ≠ eğitilmemiş | evet | evet | OK |
| eğitilmemiş = PhaseNet(seed 0) taze başlangıç | evet | evet | OK |
|   (bilgi) eğitilmiş − eğitilmemiş en büyük ağırlık farkı | - | 0.19 | bilgi |
| yorum: ağ 0.43 ms | 0.43 | 0.4255 | OK |
| yorum: SU-best-of 1.24 ms | 1.24 | 1.238 | OK |
| yorum: 0.38 gerisinde | -0.38 | -0.3808 | OK |
| yorum: ağ t=0 4.65 | 4.65 | 4.65 | OK |
| yorum: SU-best-of t=0 5.12 | 5.12 | 5.115 | OK |
| yorum: 0.8 ms gecikme farkı | 0.8 | 0.813 | OK |
| yorum: 5.115 → 5.011 | [+5.115, +5.011] | [+5.115, +5.011] | OK |
| yorum: ~0.1 kayıp | 0.1 | 0.1039 | OK |
| yorum: kazanmak için t=0 ~5.0 üstü (gereken t0 = 5.011 + ağın yaşlanma kaybı) | 5 | 5.031 | OK |
| yorum: 3 GHz −1.52 | -1.52 | -1.523 | OK |
| yorum: 28 GHz −0.38 | -0.38 | -0.3808 | OK |
| yorum: 4 kat daralma | 4 | 4 | OK |
| yorum: +0.47 (28 GHz) | 0.47 | 0.4698 | OK |
| yorum: +0.37 (3 GHz) | 0.37 | 0.3687 | OK |
| yorum: 3 GHz karma 0.06–0.08 gerisinde | [+0.060, +0.080] | [+0.063, +0.075] | OK |
| yorum: 28 GHz karma 0.11–0.16 gerisinde | [+0.110, +0.160] | [+0.112, +0.158] | OK |
| yorum: E1 +0.04…+0.05 | [+0.040, +0.050] | [+0.043, +0.049] | OK |
| yorum: doruk 10–20. epoch'ta | 10–20 içinde | 10–20 içinde | OK |
| yorum: T_c ≈ 3 ms (0.423/f_d) | 3 | 3.019 | OK |

OK 202, HATA 0, ÜRETİLEMEDİ 0

## Ek mantık denetimleri
28 GHz 1.5 m/s: seed-12 ilk üç klasik SU-best-of 4.765, Adam-1|best 4.681, Adam-1|avg 4.595
   seed 11'de en iyi klasik SU-best-of 5.011 (seçilen SU-best-of 5.011)
   SU-average 0.231 ms: t0 4.611, etkin 4.610; NN-sincos t0 4.650; NN−SU-average etkin +0.021 [-0.014592036494985222, 0.0557124210949987]
   NN+Adam-1 − Adam-1|best: t0 -0.303 [-0.342, -0.263], etkin -0.082 [-0.126, -0.042]
   NN+Adam-2 − Adam-2|best: t0 -0.191 [-0.223, -0.163], etkin -0.006 [-0.052, 0.041]
   NN+Adam-6 − Adam-6|best: t0 -0.088 [-0.104, -0.071], etkin -0.063 [-0.107, -0.017]
   NN+Adam-12 − Adam-12|best: t0 -0.057 [-0.067, -0.047], etkin -0.046 [-0.087, -0.007]
   NN-sincos − SU-best-of t0 -0.465 [-0.523, -0.406]; NN-sincos t0 − en iyi klasik etkin -0.361
   en iyi klasik kol CD mi? False; en iyi CD etkin (seed 11) 4.858
28 GHz 3 km/h: seed-12 ilk üç klasik Adam-1|best 4.887, SU-best-of 4.826, Adam-2|best 4.812
   seed 11'de en iyi klasik Adam-1|best 5.145 (seçilen Adam-1|best 5.145)
   SU-average 0.231 ms: t0 4.611, etkin 4.611; NN-sincos t0 4.650; NN−SU-average etkin +0.030 [-0.004340608466416597, 0.06545858946442602]
   NN+Adam-1 − Adam-1|best: t0 -0.303 [-0.342, -0.263], etkin -0.185 [-0.227, -0.145]
   NN+Adam-2 − Adam-2|best: t0 -0.191 [-0.222, -0.162], etkin -0.020 [-0.055, 0.018]
   NN+Adam-6 − Adam-6|best: t0 -0.088 [-0.105, -0.072], etkin -0.048 [-0.083, -0.014]
   NN+Adam-12 − Adam-12|best: t0 -0.057 [-0.068, -0.047], etkin -0.047 [-0.077, -0.015]
   NN-sincos − SU-best-of t0 -0.465 [-0.525, -0.406]; NN-sincos t0 − en iyi klasik etkin -0.495
   en iyi klasik kol CD mi? False; en iyi CD etkin (seed 11) 4.812
3 GHz 1.5 m/s: seed-12 ilk üç klasik Adam-6|best 5.785, Adam-5|best 5.776, Adam-4|best 5.749
   seed 11'de en iyi klasik Adam-5|best 6.236 (seçilen Adam-6|best 6.234)
   SU-average 0.231 ms: t0 4.624, etkin 4.624; NN-sincos t0 4.710; NN−SU-average etkin +0.087 [0.0294900711432565, 0.14777869286551135]
   NN+Adam-1 − Adam-1|best: t0 -0.353 [-0.408, -0.3], etkin -0.342 [-0.398, -0.286]
   NN+Adam-2 − Adam-2|best: t0 -0.241 [-0.289, -0.193], etkin -0.225 [-0.273, -0.178]
   NN+Adam-6 − Adam-6|best: t0 -0.136 [-0.171, -0.101], etkin -0.075 [-0.116, -0.037]
   NN+Adam-12 − Adam-12|best: t0 -0.080 [-0.106, -0.053], etkin +0.024 [-0.023, 0.073]
   NN-sincos − SU-best-of t0 -0.567 [-0.636, -0.494]; NN-sincos t0 − en iyi klasik etkin -1.524
   en iyi klasik kol CD mi? False; en iyi CD etkin (seed 11) 5.042
3 GHz 3 km/h: seed-12 ilk üç klasik Adam-10|best 5.982, Adam-8|best 5.966, Adam-12|best 5.959
   seed 11'de en iyi klasik Adam-10|best 6.442 (seçilen Adam-10|best 6.442)
   SU-average 0.231 ms: t0 4.624, etkin 4.624; NN-sincos t0 4.710; NN−SU-average etkin +0.086 [0.03033298900164664, 0.14685079558566205]
   NN+Adam-1 − Adam-1|best: t0 -0.353 [-0.411, -0.298], etkin -0.349 [-0.405, -0.294]
   NN+Adam-2 − Adam-2|best: t0 -0.241 [-0.285, -0.194], etkin -0.237 [-0.288, -0.189]
   NN+Adam-6 − Adam-6|best: t0 -0.136 [-0.171, -0.103], etkin -0.115 [-0.15, -0.079]
   NN+Adam-12 − Adam-12|best: t0 -0.080 [-0.105, -0.055], etkin -0.044 [-0.075, -0.011]
   NN-sincos − SU-best-of t0 -0.567 [-0.642, -0.493]; NN-sincos t0 − en iyi klasik etkin -1.733
   en iyi klasik kol CD mi? False; en iyi CD etkin (seed 11) 5.080
s5_summary.json kararları {'S5_H1': False, 'S5_H2': False, 'S5_H3': True}; NN load_start 2.32 (sonrası kaydedilmedi)
