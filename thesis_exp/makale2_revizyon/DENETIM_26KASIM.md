# Bağımsız denetim — 26 Kasım 2026 düzenlemeleri (Makale 2, IEEE TWC)

Kapsam: `git diff HEAD -- thesis_exp/makale2_revizyon/mobility_paper_ieee.tex thesis_exp/makale2_revizyon/sections/`
(özet, giriş + katkılar, §II Tablo I, §IV alt başlıklar, §V Tablo II + girdi paragrafı + Timing, §VI alt başlıklar ve ifade değişiklikleri, §VII).
Hiçbir kaynak dosya değiştirilmedi; yalnızca bu rapor yazıldı. Commit yapılmadı.

Ön koşul: `python3 scripts/audit_claims.py --all` → **126/126** (yük ortalaması 0.01).

---

## KRİTİK

### K1. Özet ve Katkı 2, kapalı biçimi "öngören, hıza uyarlanan bir kural" olarak sunuyor; makalenin kendi metni bunu açıkça reddediyor
- **Yer:** `mobility_paper_ieee.tex:31` (özet) — *"A small-delay model shows that this optimum exists for every nonzero step time and scales with …; its closed form, which adapts the step count to user speed and hardware, is within a factor of 1.27 of the measured optimum."*
  `sections/section_01_introduction.tex:13` — *"A small-delay model (Proposition~1) establishes that the optimum exists for every nonzero step time and predicts its scaling, which yields a closed-form, speed-adaptive choice of the step count."*
- **Kanıt (değişmemiş metin):**
  - `section_04_latency_analysis.tex:64`: *"With fitted constants, (Lstar) describes the measurements rather than predicting them independently; its value lies in explaining how the optimum shifts."*
  - `section_06_results.tex:44`: *"This is an in-sample check: κ_L is fitted over the delays (1.6–10 ms) at which the optima occur. The balance of Proposition 1 does not hold quantitatively (the ratio varies from 0.19 to 1.65), so the model explains where the optimum lies and why it moves, not how the two losses split."* ve *"the model thus pins the exponent down only to about ±0.08"*.
  - Önerme 1 κ_L = κ (sabit) varsayıyor; ölçülen κ_L 7.8'den 25.1'e çıkıyor (aynı satır). "Establishes … for every nonzero step time" yalnızca model içinde geçerli.
  - Eski özet: *"The optimum is set by the step time relative to the Doppler frequency, as a small-delay model explains."* Eski katkı: *"a small-delay model explains how it scales"*. Yeni metin "explains"i "shows/establishes/predicts/yields a speed-adaptive choice" düzeyine yükseltiyor ve "in-sample" kaydını düşürüyor. Bu, iddia gücünü değiştiren bir yeniden yazım ve makalenin gövdesiyle çelişiyor (CLAUDE.md kural 10).
- **Öneri:** Özet: *"A small-delay model explains this optimum and how it moves with the product of step time and Doppler frequency; with constants fitted to the same measurements, its closed form lies within a factor of 1.27 of the measured optimum."* Katkı 2: *"A small-delay model (Proposition~1) explains why the optimum exists and how it shifts; with fitted constants its closed form tracks the measured optimum within a factor of 1.27 (in-sample)."* "Speed-adaptive choice" ve "adapts … to hardware" ifadeleri ya çıkarılmalı ya da bağımsız (out-of-sample) bir doğrulamayla desteklenmeli; böyle bir betik/sonuç bulunmadı.

---

## ORTA

### O1. Özette "one thread" kaydı düştü
- **Yer:** `mobility_paper_ieee.tex:31` — *"…is dominated by faster Adam configurations at equal measured latency."*
- **Kanıt:** Eski: *"…once latency is measured on one thread."* `section_06_results.tex:87`: *"The cost ratio, however, is a property of this implementation on one CPU thread: on hardware that accelerates the network's matrix products more than Adam's step, the reversal could weaken."* Sonuç maddesi 5 kaydı koruyor ("static set, one CPU thread"); özet korumuyor. Ayrıca "at equal measured latency" Tanım 2'deki baskınlığı (daha hızlı **ve** daha iyi) tam anlatmıyor.
- **Öneri:** *"…is dominated by faster and better Adam configurations once each step is charged its latency measured on one CPU thread."*

### O2. Özet ana varsayımı (taze ön kodlayıcı, kusursuz CSI) artık hiç anmıyor
- **Yer:** `mobility_paper_ieee.tex:31`.
- **Kanıt:** Eski özette *"Charging the pilots for a fresh precoder lowers rates but leaves slow solvers behind tuned Adam."* ve kapsam cümlesi *"For pedestrian users at the measured step cost, latency, not convergence, decides…"* vardı; ikisi de silindi. `section_07_conclusion.tex:15` (Limitations) ana sonuçların "perfect knowledge" ve taze ön kodlayıcı varsaydığını söylüyor; §VI-G eski ön kodlayıcıyla oranın T_c'de 11.7–14.2 kat düştüğünü gösteriyor. Okur, özetten bu varsayımı çıkaramıyor.
- **Öneri:** Son cümleye kısa bir kayıt: *"…at most eight steps per update suffice. These results assume a precoder refreshed from the current channel; charging its pilots lowers all rates but leaves the slow solvers behind tuned Adam."* (Kelime sınırı için K1 önerisi birkaç kelime kazandırıyor.)

### O3. Özette "scales with the product of …" yönü yanlış okutuyor
- **Yer:** `mobility_paper_ieee.tex:31`.
- **Kanıt:** L* ∝ x^{-2/(γ+2)}, yani x = ΔT·f_d büyüdükçe **azalıyor** (`section_04_latency_analysis.tex:57`, ölçülen eğim −0.675). Akademik İngilizcede "scales with X" genelde X ile birlikte büyümeyi çağrıştırır.
- **Öneri:** *"…is governed by the product of step time and Doppler frequency and decreases as a power of it"* ya da yalnızca *"moves with"*.

### O4. Tablo II başlığı "aging set unless stated" diyor; öğrenilen güncelleme satırı statik kümeden ama belirtilmemiş
- **Yer:** `sections/section_05_methodology.tex:15` (başlık) ve `:29` (Learned update satırı).
- **Kanıt:** Öğrenilen ağlar yalnızca statik kümede eğitildi ve zamanlandı (`results/mumiso_eqstep_L*.json`, `results/mumiso_latency_repeat.json`; §VI-F "This comparison uses the static set"). "2.7–4.0 Adam steps per step" statik kümenin oranı.
- **Öneri:** Satıra "(static set)" ekleyin; ör. Cost hücresi: *"2.7–4.0 Adam steps per step (static set)"*.

### O5. Timing paragrafındaki yeni genelleme "so the conclusions do not depend on which value is used" fazla geniş
- **Yer:** `sections/section_05_methodology.tex:40`.
- **Kanıt:** 1.33 ms ile yalnızca üç şey yeniden kontrol edilmiş: L* = 6, L = 48 maliyeti %14.9, SU-best-of − CD = 0.26 (CI 0.15–0.37). Periyodik işletim (Tablo tracking), hız tablosu ve ölçekleme 1.33 ile yeniden koşturulmamış. Ayrıca SU-best-of − CD farkı Adam'ın adım süresine bağlı değil (iki yöntem ayrı zamanlanıyor; `DENETIM_EDITOR.md:50` aynı noktayı daha önce kaydetmiş), yani bu karşılaştırma "değerden bağımsızlık" kanıtı sayılmaz.
- **Öneri:** *"…so the optimum and the cost of running to L = 48 do not depend on which of the two aging-set values is used."*

---

## KÜÇÜK

### Tablo I (tab:literature, `sections/section_02_related_work.tex:10–31`)

Tüm hücreler `kaynak_kontrol/grup2, grup3, grup4, grup5, grup6, grup7, grup10` özet tablolarıyla tek tek karşılaştırıldı; atıf anahtarları `references/references.bib` ile eşlendi. **Çürütülen ya da desteksiz hücre yok.** Aşağıdakiler kesinlik/tutarlılık düzeltmeleri:

- **T1 — `:20` Abeywickrama/Yu, "RIS phases":** Abeywickrama ortak aktif/pasif hüzmeleme (SINR kısıtlı güç en küçükleme, AO/penalty/two-stage; grup2 [7]); Yu tek kullanıcılı MISO, f = MRT (grup3). "RIS phases" Abeywickrama için eksik. Öneri: *"RIS precoding and phases (practical amplitude model; fixed-point, manifold)"*. "measured on a fixed channel" → *"measured on static channel realizations"* (Abeywickrama: ortalama CPU süresi; Yu: ortalama çalışma süresi).
- **T2 — `:21` Sun/Liu2022, "learned WMMSE":** Sun bir açılmış (unfolded) WMMSE değil, WMMSE'yi kara kutu DNN ile taklit ediyor, girişim kanalında, RIS'siz (grup4). Öneri: *"DNN approximating WMMSE; unfolded RIS full-duplex design"*.
- **T3 — `:21` "fixed CSI delay of 0–1.2 ms":** Liu2022'de 0–1.2 ms CSI gecikmesi **taranıyor** (Fig. 10), tek bir sabit değil. Öneri: *"CSI delay swept over 0–1.2 ms"*. Aynı satırın "Role of run time" hücresi klasik kolun ayarını anlatıyor, rolünü değil; grup4'ün asıl bulgusu ölçülen sürenin (0.016–21.45 s) CSI gecikmesiyle ilişkilendirilmemesi. Öneri: *"compared between methods, not with the CSI delay; classical method at convergence or fixed iterations"*.
- **T4 — `:23` Papazafeiropoulos, "fixed delay":** Gecikme n·T_s, çerçeve içinde n ile büyüyor ve şekillerde taranıyor (grup5: "kabaca doğru; daha kesin ifade: a model parameter set by the frame structure"). Zhang için "fixed" tam doğru. Öneri: *"Jakes correlation; delay set by frame structure or fixed"*.
- **T5 — `:25` Han, "Gauss–Markov":** Grup6'ya göre Gauss–Markov (ρ = 0.9995) doğrudan bağlantı için; blok süresi sabit. Hücre kabul edilebilir; isteğe bağlı *"Gauss–Markov (direct link), fixed block"*.
- **T6 — Tanımlanmamış kısaltma/sembol:** `:19` "BCD, FP" kısaltmaları metinde açılmıyor (§II'de "block coordinate descent", "fractional programming" kısaltmasız geçiyor); `:26` "UAVs" metinde açılmıyor ("fast drones"); `:20` "$T_c$" §III'te tanımlanıyor, Tablo I okuma sırasında ondan önce geliyor. Öneri: hücrelerde açık yazım ya da metinde ilk geçişte kısaltma; "$T_c$" yerine *"coherence time"*.
- Doğrulanan hücreler (değişiklik gerekmez): Pan/Guo/Choi "none / complexity order / none" (grup2 [8]–[10]); Cao "first-order aging, fixed delay / measured per iteration / not part of the delay" (grup7: AR(1), ρ = J₀(2πf_dτ), τ sabit; Fig. 7); Truong "fixed delay (1–10 ms); computation named as a cause / not measured" (grup6: D = 1, Table 1, s. 338/341); Liu2021WCL "one 20 ms slot / measured (2 ms) / feasibility check" (grup5); Ryu "fixed delay (Δ) / estimated from operation counts (3.869 GFLOP, 0.774 TFLOP/s) / constraint and fixed overhead (13)–(15)" (grup10); Zhang "Jakes, fixed ρ / closed form" (grup5).

### Tablo II ve yöntem metni (`sections/section_05_methodology.tex`)

Kodla ve sonuç dosyalarıyla doğrulandı (hepsi **tutarlı**):
- 37 statik kanal = `n_channels(T=8) = 5+4T` (`ris_mu/mumiso/features.py`): Re/Im g (2), Re/Im F her N_t = 8 anten (16), Re/Im h_d (16), cos/sin φ_su (2), log göreli güç (1). +4 dinamik (`unrolled.py` forward: cos/sin θ, (R−ort)/std, `use_grad` ile normalize soft-min gradyanı, β = 8) → **41** ✓.
- Mimari: `_Backbone` (Conv1d×2 + 2 katmanlı LSTM + Linear), iki `_Exchange` (stage1 ve stage2 sonrası), kullanıcı ortalaması, `_LocalHead` (genişlik-1 conv), adım başına öğrenilen `log_step`, ağırlıklar adımlar arasında ortak ✓.
- Parametre: 272835 / 272836 / 272838 / 272842 / 272850 (L = 1/2/4/8/16; `results/mumiso_eqstep_L*.json`) ✓.
- Eğitim (`scripts/mumiso_unrolled.py` + json config): Adam lr 1e-3, `CosineAnnealingLR`, bs 32, 12 epoch, kayıp `S.maxmin_loss` (soft-min, β = 8), etiketsiz ✓.
- SU-average = K hizalama fazörünün toplamının fazı; SU-best-of = K hizalama + SU-average içinden en iyisi (`baselines.py`) ✓.
- Adam (yaşlanma kümesi): lr 0.5, soft-min β = 8 (`scripts/mumiso_mobility_latency.py:39,86`) ✓; CD 16 seviye, hard min, ≤ 8 tarama; uzun koşulu Adam 1000 yineleme, 3 rastgele başlangıç, hard min (`baselines.pga`) ✓.
- 0.42 ms, 2.5 ms, 13.3 ms (8 adım → 1.66), 880.8 ms, 5851.7 ms (→ 5.85 s): `results/mumiso_mobility_latency.json` medyanları ve `tables/tab_aging.tex` ✓. Aynı dosyada adım başına 1.49–2.02 ms, yük 0.20 → 0.86 ✓ ("later rounds on the aging set" doğru).
- Armijo a0 = 3, L* = 4, oran 1.2553 × 1.66 = 2.087 ms ✓ (`results/mumiso_step_scaling.json`).
- Statik küme Adam: beş tur medyanı / L = 1.600–1.707 ms (`results/mumiso_latency_repeat.json`) → "1.60–1.71" ✓; öğrenilen/Adam medyan oranı 2.73–4.05 → "2.7–4.0" ✓; 18.41 ms ve 13.48 ms ✓.
- 107 ms/tarama, "best: 2", L* = 4–6, 0.75 (statik, seçilmiş), 1.33 ms: §VI'daki değişmemiş metinle tutarlı ✓.

Küçük noktalar:
- **H1 — `:25` "(static set: 0.75, selected)":** Tuning paragrafına göre 0.75 yalnızca L ≤ 16 için her seferinde seçiliyor; L = 24–64 için ayrı bir altı değerlik ızgara var ve seçilen değer belirtilmiyor. Öneri: *"(static set: 0.75 for L ≤ 16, selected)"*.
- **H2 — Eksik hiperparametreler:** Uzun koşulu Adam'ın adım boyu 0.05; öğrenilen ağın eğitim örnek sayısı (6000), gradyan kırpma (1.0), en iyi doğrulama epoch'unun seçilmesi, başlangıç adım boyu 0.5 tabloda yok. Bir "settings" tablosu için eklenmesi önerilir (kodda: `baselines.pga`, `scripts/mumiso_unrolled.py`).
- **H3 — `:35` "the user's relative channel power":** Kodda **log10** göreli güç. Öneri: *"the logarithm of the user's relative channel power"*.
- **H4 — `:40` "three values, each tied to one measurement session":** §VI-G'deki "about 13 times shorter than one Adam step" kendi oturumundan (precoder-vs-step ölçümü) geliyor; üç değerin dışında kalıyor. İsteğe bağlı bir yan cümle.

### Özet, giriş, sonuç — dil ve anlam

- **D1 — Özet kelime sayısı:** `.tex` belirteçleriyle 198, PDF metninde (sayı ve birim ayrı sayılınca) **201**. 200 sınırının üstünde ya da tam sınırda. K1/O2 önerileri uygulanırken birkaç kelime kısaltılmalı (ör. "termed", "In periodic operation," → "Periodically,"). Özette açılmamış kısaltma ya da matematik sembolü **yok** (RISs açılmış; "multiple-input single-output" açık yazılmış; "%", "m/s", "ms" birim).
- **D2 — `mobility_paper_ieee.tex:31` "We evaluate each method on the channel that exists when its computation ends, termed the effective rate":** "termed the effective rate" dilbilgisel olarak "channel"a bağlanıyor. Öneri: *"We evaluate the rate of each method on the channel that exists when its computation ends, termed the effective rate"*.
- **D3 — `:31` "48 steps cost 14%":** Neye göre olduğu belirsiz. Öneri: *"running to 48 steps costs 14% relative to the peak"*.
- **D4 — `section_01_introduction.tex:6` "the channel for which it was computed no longer exists":** Abartılı; kanal değişmiş ama "yok" değil. Öneri: *"has already changed"*.
- **D5 — `section_01_introduction.tex:8`:** "accounted for" iki ardışık cümlede tekrarlanıyor. Öneri: ikincisinde *"once run time is charged"*.
- **D6 — `section_06_results.tex:98` "Its computation is inexpensive":** "Its" öncülü belirsiz (önceki cümlenin öznesi "a precoder only 5 ms old"). Öneri: *"Recomputing the precoder is inexpensive"*. Aynı paragrafta "fresh beam" geçiyor, alt başlık "Fresh-Precoder" diyor; terim birleştirilebilir.
- Anlam kontrolü (sorun yok): Katkı 1, 3, 4, 5; sonuç maddeleri 1–5 ("tie or pass" → "match or exceed", "nearly free" → "costs little", "decides" → "determines … preferable") ve tüm alt başlıklar eski anlamı koruyor; "preferable" biraz daha yumuşak, kabul edilebilir. Yeni ifadeler genel olarak deyimsel akademik İngilizce.

### PDF ve log

- `pdfinfo mobility_paper_ieee.pdf`: **10 sayfa** ✓; PDF 05:59:12'de, tüm bölüm dosyalarından sonra derlenmiş.
- `mobility_paper_ieee.log`: **Overfull yok, undefined reference/citation yok**, LaTeX Warning yok ✓.
- **P1:** Yeni tablolarda Underfull \hbox var: Tablo I `:21`, `:28`; Tablo II `:28` ("Long-run", badness 10000), `:29` ("2.7–4.0 Adam", badness 10000). Görsel; `p{}` sütunlarına `>{\raggedright\arraybackslash}` (array paketi) eklemek giderir.
- Tablo II PDF'te §IV'ün olduğu 4. sayfada üstte basılıyor (referansı §V-B'de, aynı sayfada); sorun değil.

---

## Kontrol edilenler (özet)
1. Tablo I'in 10 satırı × 4 hücresi, 7 kaynak kontrol dosyasının özet ve ayrıntı bölümlerine karşı.
2. Tablo II'nin her hücresi, girdi paragrafı ve Timing paragrafı; `features.py`, `unrolled.py`, `models.py`, `baselines.py`, `scripts/mumiso_unrolled.py`, `scripts/mumiso_mobility_latency.py`, `results/mumiso_eqstep_L*.json`, `results/mumiso_latency_repeat.json`, `results/mumiso_mobility_latency.json`, `results/mumiso_step_scaling.json`, `tables/tab_aging.tex` ve §IV–§VI'nın değişmemiş metni.
3. Özet, katkılar, sonuç maddeleri, giriş ve alt başlıklar; eski metinle anlam/güç karşılaştırması, kelime sayısı, kısaltmalar.
4. `pdfinfo`, log taraması.
