% theta_NN_multioutput.m
% Phase-aware CNN-LSTM for RIS phase optimization.
%
% Model: two Conv1D blocks + two LSTM layers + FC output.
% Output representation: [sin(theta), cos(theta)] per element
%   -> avoids the +-pi discontinuity in direct phase regression.
% Phase recovery: atan2(sin_pred, cos_pred)
%
% Requires: RIS_dataset_large_2D.mat  (run RIS_dataset_large_2D.m first)
% GPU recommended; set ExecutionEnvironment='cpu' if needed.

clear; close all; clc;
rng(42);

%% 1) load data
S = load('RIS_dataset_large_2D.mat');
F = S.F;  G = S.G;  h_d = S.h_d;  THETA = S.THETA;

numSamples = size(F, 1);   % 40000
timeSteps  = size(F, 2);   % 32

%% 2) build input sequences: 4 x N  [re(F); im(F); re(G); im(G)]
X = cell(numSamples, 1);
for i = 1:numSamples
    X{i} = [real(F(i,:)); imag(F(i,:)); real(G(i,:)); imag(G(i,:))];
end

%% 3) build sin/cos output: 2 x N
Y = cell(numSamples, 1);
for i = 1:numSamples
    Y{i} = [sin(THETA(i,:)); cos(THETA(i,:))];
end

%% 4) train / val / test split  (70 / 15 / 15)
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

fprintf('Train: %d  |  Val: %d  |  Test: %d\n', nTrain, nVal, nTest);

%% 5) network architecture
inputSize  = 4;
outputSize = 2;

layers = [
    sequenceInputLayer(inputSize, 'Name', 'input')

    % CNN block - local feature extraction
    convolution1dLayer(3, 64, 'Padding', 'same', 'Name', 'conv1')
    batchNormalizationLayer('Name', 'bn1')
    reluLayer('Name', 'relu1')

    convolution1dLayer(3, 64, 'Padding', 'same', 'Name', 'conv2')
    batchNormalizationLayer('Name', 'bn2')
    reluLayer('Name', 'relu2')
    dropoutLayer(0.2, 'Name', 'drop1')

    % LSTM block - inter-element dependencies
    lstmLayer(128, 'OutputMode', 'sequence', 'Name', 'lstm1')
    lstmLayer(64,  'OutputMode', 'sequence', 'Name', 'lstm2')
    dropoutLayer(0.3, 'Name', 'drop2')

    % output: sin and cos
    fullyConnectedLayer(outputSize, 'Name', 'fc_out')
    regressionLayer('Name', 'output')
];

%% 6) training options
opts = trainingOptions('adam', ...
    'MaxEpochs',           50, ...
    'MiniBatchSize',       256, ...
    'InitialLearnRate',    1e-3, ...
    'LearnRateSchedule',   'piecewise', ...
    'LearnRateDropFactor', 0.5, ...
    'LearnRateDropPeriod', 15, ...
    'Shuffle',             'every-epoch', ...
    'Plots',               'training-progress', ...
    'ValidationData',      {Xval, Yval}, ...
    'ValidationFrequency', 50, ...
    'ExecutionEnvironment','gpu', ...
    'Verbose',             1);

%% 7) train
fprintf('\nStarting training...\n');
t0  = tic;
net = trainNetwork(Xtrain, Ytrain, layers, opts);
fprintf('Training time: %.1f min\n', toc(t0)/60);

%% 8) predict on test set + phase recovery via atan2
t_inf = tic;
Ypred = predict(net, Xtest);
t_per_sample = toc(t_inf) / nTest * 1e3;  % ms

THETA_pred = zeros(nTest, timeSteps);
for i = 1:nTest
    THETA_pred(i,:) = atan2(Ypred{i}(1,:), Ypred{i}(2,:));
end

%% 9) phase-aware RMSE
phase_err = angle(exp(1j * (THETA_pred - THETA_true)));  % wrapped difference
rmse_rad  = sqrt(mean(phase_err(:).^2));
rmse_deg  = rmse_rad * (180/pi);

fprintf('\n--- Results ---\n');
fprintf('Phase-aware RMSE : %.4f rad  =  %.2f deg\n', rmse_rad, rmse_deg);
fprintf('Avg inference    : %.3f ms/sample\n', t_per_sample);

% success rates
for tau = [1 3 5 10]
    sr = mean(abs(phase_err(:)) < tau*pi/180);
    fprintf('SR@%2d deg        : %.1f%%\n', tau, sr*100);
end

%% 10) per-element RMSE (useful for debugging spatial pattern)
rmse_elem = sqrt(mean(phase_err.^2, 1)) * (180/pi);
fprintf('\nPer-element RMSE range: %.2f - %.2f deg\n', min(rmse_elem), max(rmse_elem));

%% 11) save results
save('cnn_lstm_trained_model.mat',  'net', 'trainIdx', 'valIdx', 'testIdx', '-v7.3');
save('cnn_lstm_test_results.mat', ...
     'THETA_pred', 'THETA_true', 'phase_err', 'rmse_rad', 'rmse_deg', 't_per_sample', '-v7.3');

fprintf('\nSaved: cnn_lstm_trained_model.mat,  cnn_lstm_test_results.mat\n');

%% 12) quick plot - first 5 test samples
figure;
for i = 1:5
    plot(THETA_true(i,:)*180/pi,  '-b', 'LineWidth', 1.2);  hold on;
    plot(THETA_pred(i,:)*180/pi,  '-r', 'LineWidth', 1.2);
end
legend('True', 'Predicted');
xlabel('RIS element index');
ylabel('Phase [deg]');
title(sprintf('CNN-LSTM predictions (5 samples) - RMSE=%.2f deg', rmse_deg));
grid on;
