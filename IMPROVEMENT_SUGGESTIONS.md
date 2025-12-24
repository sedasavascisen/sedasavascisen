# RIS Faz Tahmin Modeli İyileştirme Önerileri

## 🎯 Öncelikli İyileştirmeler

### 1. Veri Normalizasyonu (EN ÖNEMLİ!)

```matlab
% ŞU ANKİ KOD (Sorunlu):
X{i} = [real(F(i,:)); imag(F(i,:)); real(G(i,:)); imag(G(i,:))];

% ÖNERİLEN:
% Yöntem A: Amplitude normalizasyonu
F_norm = F ./ (abs(F) + 1e-10);
G_norm = G ./ (abs(G) + 1e-10);
X{i} = [real(F_norm(i,:)); imag(F_norm(i,:));
        real(G_norm(i,:)); imag(G_norm(i,:))];

% Yöntem B: Z-score normalizasyonu (tüm dataset üzerinden)
F_stack = [real(F(:)); imag(F(:))];
mu_F = mean(F_stack);
sigma_F = std(F_stack);
% G için de aynı şekilde
```

**Neden önemli?**
- LSTM'ler normalized input ile çok daha iyi çalışır
- Farklı mesafelerdeki amplitude farkları probleme yol açıyor

---

### 2. Model Kompleksitesini Ayarla

```matlab
% ŞU ANKİ (4x4 için fazla karmaşık):
lstm1_units = 32;
lstm2_units = 16;

% ÖNERİLEN:
if N <= 16
    lstm1_units = 16;   % 32 yerine 16
    lstm2_units = 8;    % 16 yerine 8
    conv_filters = 8;   % 16 yerine 8
    maxEpochs = 50;     % 20 yerine 50 (daha fazla)
elseif N <= 64
    lstm1_units = 64;
    lstm2_units = 32;
    conv_filters = 32;
    maxEpochs = 40;
else
    lstm1_units = 128;
    lstm2_units = 64;
    conv_filters = 64;
    maxEpochs = 30;
end
```

**Mantık**: Küçük input → Basit model + Daha fazla epoch

---

### 3. Early Stopping ve Validation

```matlab
% Validation split ekle
cv = cvpartition(numSamples, 'HoldOut', 0.3); % 20% yerine 30%
trainIdx = training(cv);
testIdx = test(cv);

% Train setini ikiye böl: train + validation
cv2 = cvpartition(sum(trainIdx), 'HoldOut', 0.2);
actualTrainIdx = find(trainIdx);
trainFinal = actualTrainIdx(training(cv2));
valFinal = actualTrainIdx(test(cv2));

Xtrain = X(trainFinal);
Ytrain = Y(trainFinal);
Xval = X(valFinal);
Yval = Y(valFinal);

% Training options güncelle
options = trainingOptions("adam", ...
    MaxEpochs=maxEpochs, ...
    MiniBatchSize=32, ...  % 64 yerine 32 (küçük dataset için)
    InitialLearnRate=1e-3, ...
    LearnRateSchedule='piecewise', ...
    LearnRateDropPeriod=10, ...
    LearnRateDropFactor=0.5, ...
    ValidationData={Xval, Yval}, ...
    ValidationFrequency=10, ...
    Plots="training-progress", ...  % Loss grafikleri gör!
    Verbose=1, ...  % Progress göster
    OutputNetwork='best-validation-loss');  % Best model kaydet
```

---

### 4. Veri Artırma (Data Augmentation)

```matlab
% Şu anki: 1000 sample (yetersiz)
% Öneri: En az 5000-10000 sample

numSamples = 5000;  % 1000 yerine

% VEYA mevcut veri üzerinde augmentation:
% - Gaussian noise ekleme
% - Phase perturbation
for s = 1:numSamples
    % ... mevcut kod ...

    % Augmentation: Küçük noise ekle
    if rand > 0.5
        F(s,:) = F(s,:) .* (1 + 0.05*randn(1,N));
        G(s,:) = G(s,:) .* (1 + 0.05*randn(1,N));
        % THETA'yı yeniden hesapla
        THETA(s,:) = wrapToPi(-angle(F(s,:)) - angle(G(s,:)));
    end
end
```

---

### 5. Regularization Güçlendir

```matlab
layers = [
    sequenceInputLayer(4)
    convolution1dLayer(3, conv_filters, 'Padding', 'same')
    batchNormalizationLayer
    reluLayer
    dropoutLayer(0.3)  % 0.2 yerine 0.3
    lstmLayer(lstm1_units, 'OutputMode', 'sequence')
    dropoutLayer(0.2)  % LSTM sonrasına da dropout ekle
    lstmLayer(lstm2_units, 'OutputMode', 'sequence')
    dropoutLayer(0.2)  % Buraya da
    fullyConnectedLayer(2)
    regressionLayer
];
```

---

### 6. Performans Metrikleri Detaylandır

```matlab
% Sadece global metriklere bakma, element-wise de incele
phase_error = angle(exp(1j*(THETA_pred - THETA_true)));

% Element-wise statistics
elem_wise_mae = mean(abs(phase_error), 1);  % Her element için
[worst_elem_idx, ~] = max(elem_wise_mae);

fprintf('   Worst element index: %d (MAE: %.2f°)\n', ...
    worst_elem_idx, rad2deg(elem_wise_mae(worst_elem_idx)));

% Distribution analizi
fprintf('   Error percentiles:\n');
fprintf('     50%% (median): %.2f°\n', rad2deg(prctile(abs(phase_error(:)), 50)));
fprintf('     75%%: %.2f°\n', rad2deg(prctile(abs(phase_error(:)), 75)));
fprintf('     90%%: %.2f°\n', rad2deg(prctile(abs(phase_error(:)), 90)));
fprintf('     95%%: %.2f°\n', rad2deg(prctile(abs(phase_error(:)), 95)));
```

---

### 7. Farklı Model Mimarileri Dene

#### Opsiyon A: Sadece LSTM (CNN olmadan)
```matlab
layers = [
    sequenceInputLayer(4)
    lstmLayer(lstm1_units, 'OutputMode', 'sequence')
    dropoutLayer(0.3)
    lstmLayer(lstm2_units, 'OutputMode', 'sequence')
    fullyConnectedLayer(2)
    regressionLayer
];
```

#### Opsiyon B: Attention Mechanism
```matlab
% Self-attention layer ekle (R2020b+)
layers = [
    sequenceInputLayer(4)
    lstmLayer(lstm1_units, 'OutputMode', 'sequence')
    selfAttentionLayer(2, 8)  % 2 heads, 8 key dimension
    lstmLayer(lstm2_units, 'OutputMode', 'sequence')
    fullyConnectedLayer(2)
    regressionLayer
];
```

#### Opsiyon C: Basit DNN (LSTM yerine)
```matlab
% Sequence olmadan, flatten input
X_flat = zeros(numSamples, 4*N);
for i = 1:numSamples
    X_flat(i,:) = X{i}(:);
end

layers = [
    featureInputLayer(4*N)
    fullyConnectedLayer(128)
    batchNormalizationLayer
    reluLayer
    dropoutLayer(0.3)
    fullyConnectedLayer(64)
    reluLayer
    dropoutLayer(0.3)
    fullyConnectedLayer(2*N)
    regressionLayer
];
```

---

## 📊 Beklenen İyileşmeler

| İyileştirme | Tahmini RMSE Azalması |
|-------------|----------------------|
| Normalizasyon | 30-40% |
| Validation + Early Stop | 10-15% |
| Daha fazla veri (5000) | 20-30% |
| Model kompleksitesi ayarı | 10-20% |

**Hedef (16x16 için)**:
- RMSE: 22° → <10°
- <5° accuracy: 38% → >70%

---

## 🔬 Debugging Stratejisi

### 1. Training Loss Grafiği Kontrol Et
```matlab
options = trainingOptions("adam", ...
    ...
    Plots="training-progress");
```

**Ara**:
- Training loss düşüyor mu?
- Validation loss düşüyor mu yoksa artıyor mu? (overfitting)
- Epoch başına ne kadar iyileşme var?

### 2. Baseline Model
```matlab
% En basit tahmin: F ve G'nin ortalaması
THETA_baseline = wrapToPi(-angle(mean(F, 2)) - angle(mean(G, 2)));
```

Model bu baseline'dan kötüyse ciddi problem var!

### 3. Sanity Check
```matlab
% Aynı veri üzerinde train ve test yap (overfit yapabilmeli)
Xtrain_same = Xtrain(1:100);
Ytrain_same = Ytrain(1:100);
% Bu 100 sample'ı ezberlemeli → RMSE < 1°
```

Eğer bu testimde bile başarısız oluyorsa:
- Model mimarisi yanlış
- Loss function problemi var
- Input/output formatı hatalı

---

## 📝 Kod Değişiklikleri Özeti

1. ✅ **Hemen yap**:
   - Input normalizasyonu ekle
   - Validation split + early stopping
   - Training progress göster

2. ✅ **Kısa vadede**:
   - Veri sayısını artır (5000+)
   - Model kompleksitesini ayarla
   - Dropout artır

3. ✅ **Uzun vadede**:
   - Farklı mimariler dene
   - Hyperparameter search (grid/random)
   - Cross-validation ekle

---

## 🎓 Kaynaklar

- Phase prediction için sin/cos kullanımı: ✅ Doğru yaklaşım
- LSTM + CNN kombinasyonu: Sequence data için makul
- Alternatif: Transformer-based modeller (daha yeni, daha iyi olabilir)
