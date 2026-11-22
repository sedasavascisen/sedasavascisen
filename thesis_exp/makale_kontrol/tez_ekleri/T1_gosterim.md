**Aynı mimaride çıkış gösterimi karşılaştırması (3 tohum, ortalama ± örneklem std; JSON'daki kayıtlı değerler)**

| Senaryo | Çıkış | RMSE (°) | SR@5° | ±π yakınında RMSE (°) | Hız (b/s/Hz) |
|---|---|---|---|---|---|
| SISO | sin/cos | 14.63 ± 0.38 | %72.7 | 16.00 | 10.334 |
| SISO | açı, 1−cos kaybı | 21.35 ± 0.30 | %61.6 | 28.82 | 10.310 |
| SISO | açı, düz MSE | 30.33 ± 0.02 | %56.2 | 62.65 | 10.239 |
| MISO, N_t = 8 | sin/cos | 61.49 ± 0.10 | %25.2 | 64.92 | 12.486 |
| MISO, N_t = 8 | açı, 1−cos kaybı | 63.67 ± 0.26 | %20.5 | 64.91 | 12.426 |
| MISO, N_t = 8 | açı, düz MSE | 73.76 ± 0.17 | %20.7 | 122.68 | 11.775 |

Kaynak: results/sumiso_representation.json (scripts/sumiso_representation_summary.py)
