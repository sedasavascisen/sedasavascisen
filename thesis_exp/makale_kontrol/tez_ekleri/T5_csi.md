**CSI hatasına gürbüzlük; hata modeli F̂ = F + √(x|F_n|²)·CN(0,1), Ĝ aynı; fazlar F̂, Ĝ'den, değerlendirme gerçek kanalda; son sütun bozuk CSI'dan hesaplanan h_d'li kapalı form, gerçek kanalın optimumu değil**

| x | CNN–LSTM RMSE (°) | Kapalı form RMSE (°) | CNN–LSTM hız | CD K = 5 hız | Kapalı form, h_d dahil, hız |
|---|---|---|---|---|---|
| 0.0 | 3.28 | 0.00 | 5.797 | 6.467 | 6.490 |
| 0.05 | 13.40 | 12.96 | 5.735 | 6.412 | 6.438 |
| 0.1 | 19.00 | 18.66 | 5.670 | 6.354 | 6.382 |
| 0.15 | 23.56 | 23.28 | 5.603 | 6.292 | 6.322 |
| 0.2 | 27.68 | 27.41 | 5.529 | 6.225 | 6.259 |

Kaynak: audit/raw/step6_eval.json, audit/raw/step2_baselines.json (hata modeli: audit/scripts/step2_baselines.py)
