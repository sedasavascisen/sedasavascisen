**Parametre sayıları: yalnızca kodu olan modeller sayılabildi**

| Model | Makalede | Koddan sayılan | Kod |
|---|---|---|---|
| CNN–LSTM (önerilen) | 727 360 | 161 794 (MATLAB); 162 562 (PyTorch) | theta_NN_multioutput.m |
| CNN-Transformer | 201 K | 17 442 | transformer_baseline.m (PyTorch aktarımı) |
| FC-DNN (doğrudan) | — | 470 304 | transformer_baseline.m (PyTorch aktarımı) |
| Diğer 5 ablasyon varyantı | 89 K … 680 K | ÜRETİLEMEDİ (kodu yok) | — |

Kaynak: audit/raw/step3_arith_check.json; audit/raw/train/{cnnlstm,transformer,fcdnn_direct}_N32_s0.json. PyTorch sayısı MATLAB'dan 768 fazla: PyTorch iki LSTM katmanında ek yanlılık vektörü taşıyor (4·128 + 4·64).
