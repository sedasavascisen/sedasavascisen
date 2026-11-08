# RIS Phase-Aware CNN-LSTM Framework

> **Overcoming the Phase Discontinuity Problem in RIS Optimization:  
> A Robust and Scalable Phase-Aware Deep Regression Framework via Hybrid CNN-LSTM Architecture**  
> Seda Savaşçı Şen, Ali Çalhan, Murtaza Cicioğlu, Oğuzhan Demiryürek  
> *Advanced Intelligent Systems* — Manuscript ID: 2969054

---

## 📁 Repository Structure

```
ris-phase-aware-cnn-lstm/
│
├── data_generation/
│   ├── RIS_dataset_large_2D_UPDATED.m   # Veri seti üretici (N=32/64/128)
│   └── RIS_dataset_large_2D.mat         # [request] 40K örnek, N=32
│
├── baselines/
│   ├── ris_CD.m           # Coordinate Descent
│   ├── ris_AO.m           # Alternating Optimisation
│   ├── ris_PGD.m          # Projected Gradient Descent
│   ├── ris_PSO.m          # Particle Swarm Optimisation
│   ├── ris_SPA.m          # Successive Phase Alignment
│   └── ris_WMMSE.m        # Weighted MMSE
│
├── model/
│   ├── theta_NN_multioutput_UPDATED.m   # Ana CNN-LSTM modeli
│   ├── transformer_baseline.m           # Transformer karşılaştırması
│   └── cnn_lstm_ciz.m                  # Görselleştirme araçları
│
├── analysis/
│   ├── baseline_fairness_K_analysis.m   # K=5/20/50 hakaniyet analizi
│   ├── scalability_analysis.m           # N=32/64/128 ölçeklenebilirlik
│   └── theoretical_gradient_analysis.m  # Proposition 1 kanıtı
│
├── quantization/
│   ├── quant_aware_train_updated.m      # 2-bit niceleme eğitimi
│   ├── quant_aware_train_3bit.m         # 3-bit niceleme eğitimi
│   ├── quant_aware_test_updated.m       # 2-bit test
│   └── quant_aware_test_3bit.m          # 3-bit test
│
└── README.md
```

---

## 🚀 Quick Start

### 1. Veri Seti Üret
```matlab
% N=32 (makale ayarı)
N_target = 32;   % RIS_dataset_large_2D_UPDATED.m içinde
run('data_generation/RIS_dataset_large_2D_UPDATED.m')
```

### 2. CNN-LSTM Modeli Eğit
```matlab
run('model/theta_NN_multioutput_UPDATED.m')
% Beklenen çıktı: RMSE ≈ 2.77°, çıkarım ≈ 0.08 ms/örnek
```

### 3. Baseline Kıyaslaması
```matlab
load('RIS_dataset_large_2D.mat');
[Theta_CD,  ~, rmse_cd,  t_cd]  = ris_CD(F, G, h_d, 5);
[Theta_AO,  ~, rmse_ao,  t_ao]  = ris_AO(F, G, h_d, 5);
[Theta_PGD, ~, rmse_pgd, t_pgd] = ris_PGD(F, G, h_d, 0.2, 50);
```

### 4. K-İterasyonu Adalet Analizi (Hakem #3 Z5)
```matlab
run('analysis/baseline_fairness_K_analysis.m')
% K=5 → URLLC içi | K=50 → URLLC sınırı aşılır
```

### 5. Ölçeklenebilirlik Testi (Hakem #2 Y2)
```matlab
run('analysis/scalability_analysis.m')
% N=32: 0.08 ms | N=64: ~0.12 ms | N=128: ~0.19 ms (hepsi URLLC içi)
```

### 6. Teorik Analiz (Hakem #3 Z1, Proposition 1)
```matlab
run('analysis/theoretical_gradient_analysis.m')
% max|∇L_PA|∞ ≤ 4, L_PA ≈ ε², sınır hatası -%30
```

---

## 📊 Ana Sonuçlar

| Yöntem | RMSE [°] | SR@5° | Süre [ms] | Karmaşıklık |
|--------|----------|-------|-----------|-------------|
| **CNN-LSTM (önerilen)** | **2.77** | **95%** | **0.08** | O(N) |
| Transformer (4-baş, d=64) | 3.21 | — | 0.17 | O(N²) |
| CD (K=5) | 3.50 | — | 0.15 | O(KN²) |
| CD (K=20) | 3.31 | — | 0.60 | O(KN²) |
| CD (K=50) | 3.22 | — | 1.50 ✗ | O(KN²) |
| AO (K=5) | 3.50 | — | 0.18 | O(KN²) |
| AO (K=20) | 3.28 | — | 0.72 | O(KN²) |
| AO (K=50) | 3.21 | — | 1.80 ✗ | O(KN²) |
| PSO (P=20, K=30) | 4.50 | — | 15.0 | O(PIN) |
| SPA | 5.00 | — | 0.05 | O(N) |

> ✗ = 6G URLLC 1 ms latency limit exceeded

---

## ⚡ Ölçeklenebilirlik Projeksiyonu

| N | Konfigürasyon | CNN-LSTM [ms] | CD K=5 [ms] | URLLC? |
|---|---------------|--------------|-------------|--------|
| 32  | 8×4  | 0.08 | 0.15 | ✓ |
| 64  | 8×8  | 0.12 | 0.60 | ✓ |
| 128 | 16×8 | 0.19 | 2.40 ✗ | ✓ CNN / ✗ CD |

---

## 🔬 Niceleme Analizi (Discrete Hardware)

| Çözünürlük | Performans Kaybı |
|-----------|-----------------|
| Sürekli (ideal) | 0% (referans) |
| 3-bit (8 seviye) | < 4% RMSE artışı |
| 2-bit (4 seviye) | < 10% RMSE artışı |

---

## 📋 Gereksinimler

- MATLAB R2022b veya üstü
- Deep Learning Toolbox
- Statistics and Machine Learning Toolbox
- (İsteğe bağlı) Parallel Computing Toolbox + GPU

---

## 📜 Lisans

MIT License — Akademik kullanım için serbesttir.

---

## 📧 İletişim

Seda Savaşçı Şen  
`sedasavascisen@duzce.edu.tr`  
Düzce Üniversitesi, Elektrik-Elektronik Mühendisliği Bölümü
