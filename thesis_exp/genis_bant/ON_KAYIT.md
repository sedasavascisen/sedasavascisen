# Ön kayıt — Geniş bant OFDM (16 Kasım 2026)

Bu dosya `run.py --part curves` koşulmadan önce commit'lenir. Kurgunun ayrıntısı `PLAN.md`'de; aşağıda yalnızca plandan sapmalar ve kesinleşen ayarlar var.

## Kesinleşen ayarlar ve plandan sapmalar

| Öğe | Plan | Kesin | Neden |
| --- | --- | --- | --- |
| Adam adım boyu | doğrulamada seçilecek | **0.5 sabit** (makalenin değeri) | Seçim hesap maliyetini 3–4 katına çıkarırdı. Bilinen etki: 4.5'te seçim hükmü değiştirmedi (U20). |
| Pencere W = 50 ms | ek ölçüt | **çıkarıldı**; yalnızca Tanım 1 | 64 alt taşıyıcı × 100 zaman noktası × 400 senaryo bellek sınırını aşıyor |
| CD | 1–8 tarama | **varsayılan tarama** (`baselines.coord_descent`, 702.97 ms, tek iş parçacıklı yeniden ölçüm) | Sürekli fazda tarama başına süre ölçülmedi |
| Gecikme | — | `0.30 ms (SU-average) + a_K + b_K·L`; a_K, b_K, L ∈ {1, 4, 16} ölçümlerine doğrusal uydurma (`raw/timing.json`) | |
| Değerlendirme | — | min-kullanıcı geniş bant hızı, 64 alt taşıyıcı, her biri taze ZF; her kolun tam gecikmesinde (t = 0 ilk nokta, 8 gecikmelik gruplar) | interpolasyon yok |
| Senaryolar | — | 400; seçim seed 12, rapor seed 11 | |

## Hipotezler (değişmedi)

- **G1:** Her (B, K_opt) için içsel optimum vardır. Ölçüt: testte L = 48 ile L* arasındaki eşli farkın GA'sı sıfırın altında.
- **G2:** 20 MHz'de doğrulamada seçilen K_opt ≤ 4, 100 MHz'de ≥ 16 (her iki hızda). Ayrıca seçilen kol ile en iyi dar bant (K_opt = 1) kolu arasındaki eşli fark raporlanır.
- **G3:** CD, her B'de ve her hızda seçilen kolun anlamlı olarak gerisindedir.
- **G4 (keşifsel):** ΔT(K_opt) ile tasarım kuralının öngördüğü L ve kaybı.

## Sıra

1. `run.py --part timing`: boş makine bekler.
2. Bu dosya ve `raw/timing.json` commit'lenir.
3. `run.py --part curves`.
4. Rapor.
