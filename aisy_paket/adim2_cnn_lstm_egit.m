% ADIM 2 - Faz-farkinda CNN-LSTM egitimi ve testi (makalenin ana sonucu)
%
% Yayimlanan theta_NN_multioutput.m'nin temizlenmis hali; mimari, egitim
% ayarlari, bolme (rng(42) + randperm) ve RMSE tanimi DEGISTIRILMEDI.
% Eklenenler: (1) GPU yoksa CPU secenegi, (2) test bolmesinin kaydi
% (adim 3 CD'yi AYNI test orneklerinde olcsun diye), (3) tek-ornek gecikme
% olcumu (CD ile ayni kosulda karsilastirma icin).
%
% Gereken: RIS_dataset_large_2D.mat (adim1), Deep Learning Toolbox.
% Cikti: cnn_lstm_trained_model.mat, cnn_lstm_test_results.mat

clear; close all; clc;
rng(42);

ORTAM = 'gpu';   % GPU yoksa 'cpu' yapin (GPU'da sonuc bit duzeyinde degisebilir)

%% 1) veri
S = load('RIS_dataset_large_2D.mat');
F = S.F;  G = S.G;  h_d = S.h_d;  THETA = S.THETA;
numSamples = size(F, 1);
timeSteps  = size(F, 2);

%% 2) girdi 4 x N: [Re F; Im F; Re G; Im G]   3) cikti 2 x N: [sin; cos]
X = cell(numSamples, 1);
Y = cell(numSamples, 1);
for i = 1:numSamples
    X{i} = [real(F(i,:)); imag(F(i,:)); real(G(i,:)); imag(G(i,:))];
    Y{i} = [sin(THETA(i,:)); cos(THETA(i,:))];
end

%% 4) bolme 70/15/15 (orijinal sira)
idx    = randperm(numSamples);
nTrain = round(0.70 * numSamples);
nVal   = round(0.15 * numSamples);
nTest  = numSamples - nTrain - nVal;
trainIdx = idx(1:nTrain);
valIdx   = idx(nTrain+1:nTrain+nVal);
testIdx  = idx(nTrain+nVal+1:end);
Xtrain = X(trainIdx);  Ytrain = Y(trainIdx);
Xval   = X(valIdx);    Yval   = Y(valIdx);
Xtest  = X(testIdx);
THETA_true = THETA(testIdx, :);
fprintf('Egitim %d | Dogrulama %d | Test %d\n', nTrain, nVal, nTest);

%% 5) mimari (orijinal)
layers = [
    sequenceInputLayer(4, 'Name', 'input')
    convolution1dLayer(3, 64, 'Padding', 'same', 'Name', 'conv1')
    batchNormalizationLayer('Name', 'bn1')
    reluLayer('Name', 'relu1')
    convolution1dLayer(3, 64, 'Padding', 'same', 'Name', 'conv2')
    batchNormalizationLayer('Name', 'bn2')
    reluLayer('Name', 'relu2')
    dropoutLayer(0.2, 'Name', 'drop1')
    lstmLayer(128, 'OutputMode', 'sequence', 'Name', 'lstm1')
    lstmLayer(64,  'OutputMode', 'sequence', 'Name', 'lstm2')
    dropoutLayer(0.3, 'Name', 'drop2')
    fullyConnectedLayer(2, 'Name', 'fc_out')
    regressionLayer('Name', 'output')
];

%% 6) egitim ayarlari (orijinal)
opts = trainingOptions('adam', ...
    'MaxEpochs', 50, 'MiniBatchSize', 256, ...
    'InitialLearnRate', 1e-3, 'LearnRateSchedule', 'piecewise', ...
    'LearnRateDropFactor', 0.5, 'LearnRateDropPeriod', 15, ...
    'Shuffle', 'every-epoch', 'Plots', 'training-progress', ...
    'ValidationData', {Xval, Yval}, 'ValidationFrequency', 50, ...
    'ExecutionEnvironment', ORTAM, 'Verbose', 1);

%% 7) egitim
t0  = tic;
net = trainNetwork(Xtrain, Ytrain, layers, opts);
fprintf('Egitim suresi: %.1f dk\n', toc(t0)/60);

%% 8) test: toplu tahmin (makaledeki 0.08 ms bu yontemle olculmustu:
%     toplam sure / ornek sayisi = toplu is hacmi, TEK-ORNEK gecikmesi DEGIL)
t_inf = tic;
Ypred = predict(net, Xtest);
t_per_sample_batch = toc(t_inf) / nTest * 1e3;
THETA_pred = zeros(nTest, timeSteps);
for i = 1:nTest
    THETA_pred(i,:) = atan2(Ypred{i}(1,:), Ypred{i}(2,:));
end

%% 8b) tek-ornek gecikme: CD ile ayni kosul (bir senaryo, sirayla), medyan
nLat = 200;  tl = zeros(nLat, 1);
predict(net, Xtest(1), 'ExecutionEnvironment', 'cpu');           % isinma
for i = 1:nLat
    t1 = tic;
    predict(net, Xtest(i), 'ExecutionEnvironment', 'cpu');
    tl(i) = toc(t1) * 1e3;
end
t_single_cpu = median(tl);

%% 9) faz-farkinda RMSE (makaledeki tanim) ve ortak fazdan bagimsiz RMSE
phase_err = angle(exp(1j * (THETA_pred - THETA_true)));
rmse_rad  = sqrt(mean(phase_err(:).^2));
rmse_deg  = rmse_rad * 180/pi;
phi = angle(mean(exp(1j*phase_err), 2));
e_inv = angle(exp(1j*(phase_err - phi)));
rmse_inv_deg = sqrt(mean(e_inv(:).^2)) * 180/pi;

% alinan guc: tahmin / etiket (dB) ve gercek optimum / etiket
F_t = F(testIdx,:);  G_t = G(testIdx,:);  hd_t = h_d(testIdx);
gucu = @(TH) abs(hd_t + sum(G_t .* exp(1j*TH) .* F_t, 2)).^2;
cnn_over_label_db = mean(10*log10(gucu(THETA_pred) ./ gucu(THETA_true)));

fprintf('\n--- Sonuclar ---\n');
fprintf('Faz-farkinda RMSE (makale tanimi) : %.2f derece\n', rmse_deg);
fprintf('Ortak fazdan bagimsiz RMSE        : %.2f derece\n', rmse_inv_deg);
for tau = [1 3 5 10]
    fprintf('SR@%2d derece : %.1f%%\n', tau, 100*mean(abs(phase_err(:)) < tau*pi/180));
end
fprintf('Gecikme, toplu (is hacmi)   : %.3f ms/ornek\n', t_per_sample_batch);
fprintf('Gecikme, tek ornek, CPU     : %.3f ms (medyan, %d olcum)\n', t_single_cpu, nLat);
fprintf('Alinan guc, CNN / etiket    : %+.2f dB (ortalama)\n', cnn_over_label_db);

%% 10) kayit
save('cnn_lstm_trained_model.mat', 'net', 'trainIdx', 'valIdx', 'testIdx', '-v7.3');
save('cnn_lstm_test_results.mat', 'THETA_pred', 'THETA_true', 'phase_err', ...
     'rmse_rad', 'rmse_deg', 'rmse_inv_deg', 't_per_sample_batch', 't_single_cpu', ...
     'cnn_over_label_db', 'testIdx', '-v7.3');
fprintf('Kaydedildi: cnn_lstm_trained_model.mat, cnn_lstm_test_results.mat\n');
