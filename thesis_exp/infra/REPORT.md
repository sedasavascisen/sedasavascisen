# Tez deneyleri için ortak altyapı — rapor

Dal `thesis/altyapi`, rapor commit'i `fb28944`. Mevcut dosyalara dokunulmadı: yeniden koşular `thesis_exp/infra/scripts/` altındaki, çıktısı `thesis_exp/infra/raw/`'a yönlendirilmiş kopyalarla yapıldı.

## 1) Makaledeki iddialarla çelişen ya da onları değiştiren bulgular

1. **Adam adım süresi 1.66 ms değil, 1.328 ms** (tek iş parçacığı, boş makine, yük 0.45 → 0.88; L başına 1.33–1.39 ms). Makalenin 1.66 ms'si eski iki iş parçacıklı Adam-8 ölçümünden (13.3/8) geliyor; yöntem bölümünde bu yazılı.
2. Yeni gecikmeyle **L\* = 6** (makale bu ızgarada 5; metin 4–6 diyor), %0.5 içindeki aralık [5, 6]; L=48'e koşmanın bedeli **%14.4** (makale %14.0). Bulgu korunuyor, sayılar değişiyor.
3. SU-best-of − CD: **0.286 [0.192, 0.382]** (makale 0.297 [0.204, 0.390]); SU-best-of − uzun Adam: **0.564 [0.393, 0.745]** (makale 0.604 [0.415, 0.805]). SU-best-of − Adam-20 artık -0.086 [-0.174, 0.002] (makale -0.004 [-0.095, 0.085]).
4. **Kullanılmayan senaryo sayısı 800 değil 700**: doğrulama kümesinin 500 senaryosu kullanılıyor (öğrenilen kuralın checkpoint seçimi va[:500]; makale 'doğrulama 400' diyor), testin 600'ü.

## 2) Tablo

| İddia | Yayımlanan | Üretilen | Durum | Kanıt |
| --- | --- | --- | --- | --- |
| Yeniden üretim: results/mumiso_aging_fixzf.json | — | 0 fark | DOĞRULANDI (bit-bit) | raw/bit_identity.json |
| Yeniden üretim: results/mumiso_aging_sweep_repro.json | — | 0 fark | DOĞRULANDI (bit-bit) | raw/bit_identity.json |
| Yeniden üretim: results/mumiso_aging_sweep_fixzf.json | — | 11 fark | FARKLI — betiği yok, makale kullanmıyor | raw/bit_identity.json |
| Yeniden üretim: results/mumiso_aging_sensitivity.json | — | 0 fark (config hariç) | DOĞRULANDI (bit-bit) | raw/mumiso_aging_sensitivity.json |
| Yeniden üretim: 9 tablo + paper_numbers.txt | — | `cmp` ile aynı | DOĞRULANDI (bit-bit) | raw/assets/ |
| Adam adım süresi | 1.66 ms | 1.328 ms | FARKLI | raw/mumiso_mobility_latency_rerun.json |
| su_best_of gecikmesi | 2.54 ms | 1.63 ms | FARKLI (yeniden ölçüm) | aynı |
| cd gecikmesi | 880.78 ms | 702.97 ms | FARKLI (yeniden ölçüm) | aynı |
| pga gecikmesi | 5851.66 ms | 4950.35 ms | FARKLI (yeniden ölçüm) | aynı |
| L\* (1.5 m/s, T_ov=0) | 5 (metin 4–6) | 6 (%0.5 içi [5, 6]) | FARKLI (aralık içinde) | raw/mumiso_aging_sweep_newlat.json |
| En iyi etkin hız | 5.982 | 6.075 | FARKLI | aynı |
| L=48 kaybı | %14.0 | %14.4 | FARKLI (küçük) | aynı |
| SU-best-of − CD | 0.297 [0.204, 0.390] | 0.286 [0.192, 0.382] | DOĞRULANDI (GA örtüşüyor) | raw/mumiso_aging_stats_newlat.json |
| SU-best-of − uzun Adam | 0.604 [0.415, 0.805] | 0.564 [0.393, 0.745] | DOĞRULANDI (GA örtüşüyor) | raw/mumiso_aging_stats_newlat.json |
| SU-best-of − Adam-20 | -0.004 [-0.095, 0.085] | -0.086 [-0.174, 0.002] | FARKLI | raw/mumiso_aging_stats_newlat.json |
| Tablo I adam8 etkin hız | 5.849 @ 13.30 ms | 6.022 @ 10.63 ms | FARKLI | aynı |
| Tablo I adam12 etkin hız | 5.515 @ 19.95 ms | 5.771 @ 15.96 ms | FARKLI | aynı |
| Tablo I adam16 etkin hız | 5.324 @ 26.60 ms | 5.524 @ 21.28 ms | FARKLI | aynı |
| Tablo I adam20 etkin hız | 5.276 @ 33.25 ms | 5.363 @ 26.57 ms | FARKLI | aynı |
| Statik küme kullanımı | 4200/400/600 (800 boşta) | 4200 / 500 / 600 (700 boşta) | FARKLI | raw/static_split_usage.json |
| 38.901, N_t=1: sin/cos CNN–LSTM (ham girdi) | — | RMSE 103.57°; hız 6.230 (optimum 10.349, makale etiketi (a) 9.908) b/s/Hz | ölçüldü | raw/m1_38901/sincos_raw_s*.json |
| 38.901, N_t=1: doğrudan açı eşleniği | — | RMSE 103.89°; hız 6.222 (optimum 10.349, makale etiketi (a) 9.908) b/s/Hz | ölçüldü | raw/m1_38901/angle_raw_s*.json |
| 38.901, N_t=1: sin/cos, ölçek-normalize | — | RMSE 59.66, 58.40, 59.81°; hız 9.302 (optimum 10.349, makale etiketi (a) 9.908) b/s/Hz | ölçüldü | raw/m1_38901/sincos_norm_s*.json |
| 38.901: eleman permütasyonu | — | RMSE 62.91, 59.08, 66.96° | ölçüldü | raw/m1_38901/*_perm.json |
| 38.901 tohum 0: sin/cos − doğrudan açı (hız, b/s/Hz) | — | +1.729 [+1.688, +1.771] | ölçüldü | raw/m1_38901/*_test_rate.npy |
| 38.901 tohum 0: özgün sıra − permütasyon (hız, b/s/Hz) | — | +0.106 [+0.089, +0.124] | ölçüldü | raw/m1_38901/*_test_rate.npy |
| 38.901 tohum 1: sin/cos − doğrudan açı (hız, b/s/Hz) | — | +1.626 [+1.585, +1.669] | ölçüldü | raw/m1_38901/*_test_rate.npy |
| 38.901 tohum 1: özgün sıra − permütasyon (hız, b/s/Hz) | — | +0.094 [+0.074, +0.114] | ölçüldü | raw/m1_38901/*_test_rate.npy |
| 38.901 tohum 2: sin/cos − doğrudan açı (hız, b/s/Hz) | — | +1.862 [+1.819, +1.906] | ölçüldü | raw/m1_38901/*_test_rate.npy |
| 38.901 tohum 2: özgün sıra − permütasyon (hız, b/s/Hz) | — | +0.417 [+0.393, +0.440] | ölçüldü | raw/m1_38901/*_test_rate.npy |

Not: ham girdili kollar (Makale 1'deki gibi normalizasyonsuz) öğrenmedi (RMSE ≈ 104°, rastgele düzey); bu yüzden kalan tohumlar ölçek-normalize girdiyle koşturuldu (plandan sapma; ham kollar tohum 0 ile kayıtlı). N_t = 1'de kapalı form (etiket b) optimumdur; ağın hızı bu optimumun altında.

## 3) Komutlar, tohumlar, ham çıktılar

| Adım | Komut | Tohum | Ham çıktı |
| --- | --- | --- | --- |
| 1 | thesis_exp/infra/scripts/mumiso_aging.py --no-learned --tag aging_fixzf; mumiso_aging_sweep.py --tag aging_sweep_fixzf; mumiso_aging_sensitivity.py; make_paper_assets.py (yönlendirilmiş kopyalar); bit_identity.py | kanal 11, torch 0 | raw/bit_identity.json, raw/assets/ |
| 2 | mumiso_mobility_latency.py --tag mobility_latency_rerun (yük < 0.5 beklendi); aging_sweep_newlat.py --steps 1,…,48; mumiso_aging_stats_newlat.py | kanal 11, bootstrap betikteki gibi | raw/mumiso_mobility_latency_rerun.json, raw/mumiso_aging_sweep_newlat.json, raw/mumiso_aging_stats_newlat.json |
| 3 | static_split_usage.py | split seed 0 | raw/static_split_usage.json |
| 4 | m1_on_38901.py --head {sincos,angle} --scale {raw,norm} --seed {0,1,2} [--permute] | veri 2026 (data_sumiso/sumiso_siso.npz, md5 9958f6b7…), bölme 0, permütasyon 7 | raw/m1_38901/ |

## 4) Açık sorular

1. Makale 2 gönderildi; yeni adım süresiyle değişen sayılar (L\* 5→6, %14.0→%14.4, Tablo I satırları) düzeltme/revizyonda mı güncellensin?
2. Tablo II hızları ve periyodik çalışma (Tablo III) da 1.66 ms ile hesaplandı; yeni süreyle yeniden üretilsin mi?
3. 38.901 arayüzünde h_d girdi kanalları Makale 1'den sapma; tezde böyle mi anlatılsın?

## 5) Yorum (bulgulardan ayrı)

- Makalenin yayımlanan sayılarının kaynak dosyaları bugünkü kodla bit-bit üretiliyor; değişen tek girdi ölçülen adım süresi.
- Adam'ın daha hızlı ölçülmesi optimumu biraz sağa kaydırıyor ve Adam kollarını iyileştiriyor; 'yavaş çözücü kaybeder' ve 'iç optimum' bulguları korunuyor.
