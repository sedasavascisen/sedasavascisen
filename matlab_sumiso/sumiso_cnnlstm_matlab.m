% sumiso_cnnlstm_matlab.m
% Phase-aware CNN-LSTM (Savasci Sen et al., Adv. Intell. Syst. 2026) on the
% single-user MISO dataset of the thesis, in MATLAB. Independent check of
% the PyTorch results (scripts/sumiso_train.py, --head seq) and GPU timing.
%
% The architecture and training options are those of theta_NN_multioutput.m;
% only the input changes: per element, Re/Im of the cascaded channel
% b_n = g_n F_n (T values each) and Re/Im of the direct channel (T each),
% i.e. 4T input channels (SISO: T = 1 -> 4 channels, as published).
%
% This is a NEW file. It does not modify the published code.
%
% Data: export from the repository with
%   python3 scripts/sumiso_dataset.py --tag train          (MISO, N_t = 8)
%   python3 scripts/sumiso_dataset.py --tx 1 --tag siso    (SISO control)
%   python3 scripts/sumiso_export_mat.py --tag train --parts 2
%   python3 scripts/sumiso_export_mat.py --tag siso
% or use the .mat files committed in this folder.
%
% Output: printed block "=== SUMISO MATLAB RESULTS ===" (copy it back) and
% sumiso_matlab_results_<tag>.mat.
%
% Requires: Deep Learning Toolbox (R2021b or later). GPU optional.
% Note: MATLAB's GradientThreshold clips per parameter (L2 norm), PyTorch's clip_grad_norm_
% clips the global norm, so the two runs are close but not bit-identical.

clear; close all; clc;
rng(42);

%% settings ---------------------------------------------------------------
tag      = 'train';   % 'train' = MISO N_t = 8, 'siso' = single-antenna control
nEpochs  = 50;        % published recipe: 50. Capacity check: 150.
nTiming  = 200;       % single-scenario timing repetitions

%% 1) load -----------------------------------------------------------------
files = dir(sprintf('sumiso_%s*.mat', tag));
assert(~isempty(files), 'no sumiso_%s*.mat in the current folder', tag);
[~, order] = sort({files.name}); files = files(order);
Bre = []; Bim = []; Hre = []; Him = []; THL = []; THO = [];
for k = 1:numel(files)
    D = load(files(k).name);
    Bre = cat(1, Bre, D.B_re);  Bim = cat(1, Bim, D.B_im);
    Hre = cat(1, Hre, D.hd_re); Him = cat(1, Him, D.hd_im);
    THL = cat(1, THL, D.theta_label); THO = cat(1, THO, D.theta_opt);
end
snr   = double(D.snr_scale);
itr   = double(D.idx_tr(:));  ival = double(D.idx_val(:));  ite = double(D.idx_te(:));
B     = double(Bre) + 1j*double(Bim);      % [S, N, T]
hd    = double(Hre) + 1j*double(Him);      % [S, T]
THL   = double(THL); THO = double(THO);
[S, N, T] = size(B);
if T == 1, B = reshape(B, S, N, 1); end
fprintf('S = %d, N = %d, T = %d, train/val/test = %d/%d/%d\n', S, N, T, numel(itr), numel(ival), numel(ite));

%% 2) features: 4T x N per scenario, z-score with training statistics -----
X = zeros(4*T, N, S, 'single');
for i = 1:S
    Bi = reshape(B(i, :, :), N, T).';              % T x N
    hi = hd(i, :).';                                 % T x 1
    X(:, :, i) = single([real(Bi); imag(Bi); repmat(real(hi), 1, N); repmat(imag(hi), 1, N)]);
end
mu = mean(X(:, :, itr), 3);
sd = std(X(:, :, itr), 0, 3) + 1e-9;
X  = (X - mu) ./ sd;
Xc = squeeze(num2cell(X, [1 2]));                   % S x 1 cell of 4T x N
Yc = cell(S, 1);
for i = 1:S
    Yc{i} = single([sin(THL(i, :)); cos(THL(i, :))]);
end

%% 3) network: theta_NN_multioutput.m with 4T inputs -----------------------
layers = [
    sequenceInputLayer(4*T, 'Name', 'input')
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

opts = trainingOptions('adam', ...
    'MaxEpochs',           nEpochs, ...
    'MiniBatchSize',       256, ...
    'InitialLearnRate',    1e-3, ...
    'LearnRateSchedule',   'piecewise', ...
    'LearnRateDropFactor', 0.5, ...
    'LearnRateDropPeriod', 15, ...
    'Shuffle',             'every-epoch', ...
    'ValidationData',      {Xc(ival), Yc(ival)}, ...
    'ValidationFrequency', floor(numel(itr)/256), ...
    'OutputNetwork',       'best-validation-loss', ...
    'GradientThreshold',   1, ...                 % as the Python run (clip_grad_norm 1.0)
    'ExecutionEnvironment','auto', ...
    'Plots',               'none', ...
    'Verbose',             true, ...
    'VerboseFrequency',    floor(numel(itr)/256));

tTrain = tic;
net = trainNetwork(Xc(itr), Yc(itr), layers, opts);
trainMin = toc(tTrain)/60;

%% 4) test: phase error and rate -------------------------------------------
Yp  = predict(net, Xc(ite), 'MiniBatchSize', 1024);
THp = zeros(numel(ite), N);
for i = 1:numel(ite)
    THp(i, :) = atan2(Yp{i}(1, :), Yp{i}(2, :));
end
err  = angle(exp(1j*(THp - THL(ite, :)))) * 180/pi;
rmse = sqrt(mean(err(:).^2));
sr   = @(t) mean(abs(err(:)) < t);

Bt = B(ite, :, :); ht = hd(ite, :);
THn  = restore_common_phase(THp, Bt, ht);
r_net   = mean(rate_of(THn, Bt, ht, snr));
r_lab   = mean(rate_of(THO(ite, :), Bt, ht, snr));
TH_al   = su_align(Bt, ht);
r_al    = mean(rate_of(TH_al, Bt, ht, snr));
r_cd1   = mean(rate_of(cd_sweep(TH_al, Bt, ht), Bt, ht, snr));
r_netcd = mean(rate_of(cd_sweep(THn, Bt, ht), Bt, ht, snr));

%% 5) single-scenario latency ----------------------------------------------
x1 = Xc(ite(1));
lat = struct();
lat.cnn_cpu_ms = time_ms(@() predict(net, x1, 'ExecutionEnvironment', 'cpu'), nTiming);
try
    gpuDevice;
    lat.cnn_gpu_ms = time_ms(@() predict(net, x1, 'ExecutionEnvironment', 'gpu'), nTiming);
catch
    lat.cnn_gpu_ms = NaN;
end
B1 = Bt(1, :, :); h1 = ht(1, :);
lat.su_align_ms = time_ms(@() su_align(B1, h1), nTiming);
lat.cd1_ms      = time_ms(@() cd_sweep(su_align(B1, h1), B1, h1), nTiming);

%% 6) report -----------------------------------------------------------------
fprintf('\n=== SUMISO MATLAB RESULTS ===\n');
fprintf('tag %s  S %d  N %d  T %d  epochs %d  release %s\n', tag, S, N, T, nEpochs, version('-release'));
fprintf('params %d\n', count_params(net));
fprintf('test RMSE %.4f deg  SR@1 %.4f  SR@3 %.4f  SR@5 %.4f  SR@10 %.4f\n', rmse, sr(1), sr(3), sr(5), sr(10));
fprintf('rate: label %.4f  su_align %.4f  CD-1 %.4f  CNN %.4f  CNN+CD-1 %.4f\n', r_lab, r_al, r_cd1, r_net, r_netcd);
fprintf('latency ms (median of %d): CNN cpu %.4f  CNN gpu %.4f  su_align %.4f  CD-1 %.4f\n', ...
        nTiming, lat.cnn_cpu_ms, lat.cnn_gpu_ms, lat.su_align_ms, lat.cd1_ms);
fprintf('training time %.1f min\n', trainMin);
try, g = gpuDevice; fprintf('gpu %s\n', g.Name); catch, fprintf('gpu none\n'); end
fprintf('cpu %s\n', getenv('PROCESSOR_IDENTIFIER'));
fprintf('=== END ===\n');
save(sprintf('sumiso_matlab_results_%s.mat', tag), 'rmse', 'r_lab', 'r_al', 'r_cd1', 'r_net', 'r_netcd', 'lat', 'nEpochs', 'trainMin');

%% helpers --------------------------------------------------------------------
function r = rate_of(TH, B, hd, snr)
    C = cascade_sum(TH, B);
    r = log2(1 + snr * sum(abs(hd + C).^2, 2));
end

function C = cascade_sum(TH, B)
    [S, N, T] = size(B);
    C = reshape(sum(B .* exp(1j*TH), 2), S, T);     % exp(1j*TH) is S x N, expands over T
end

function TH = restore_common_phase(TH, B, hd)
    C   = cascade_sum(TH, B);
    phi = angle(sum(conj(C) .* hd, 2));
    TH  = TH + phi;
end

function TH = su_align(B, hd)
    [S, N, T] = size(B);
    ref = hd ./ vecnorm(hd, 2, 2);
    TH  = -angle(sum(B .* reshape(conj(ref), S, 1, T), 3));
end

function TH = cd_sweep(TH, B, hd)
    % one sweep of exact element-wise coordinate ascent
    [S, N, T] = size(B);
    V = exp(1j*TH);
    h = hd + cascade_sum(TH, B);
    for n = 1:N
        Bn = reshape(B(:, n, :), S, T);
        c  = h - V(:, n) .* Bn;
        z  = sum(Bn .* conj(c), 2);
        TH(:, n) = -angle(z);
        V(:, n)  = exp(1j*TH(:, n));
        h  = c + V(:, n) .* Bn;
    end
end

function ms = time_ms(f, n)
    f(); f(); f();                                   % warm-up
    t = zeros(n, 1);
    for k = 1:n
        t0 = tic; f(); t(k) = toc(t0);
    end
    ms = median(t) * 1e3;
end

function p = count_params(net)
    p = 0;
    for L = net.Layers'
        props = properties(L);
        for q = {'Weights', 'Bias', 'InputWeights', 'RecurrentWeights', 'Offset', 'Scale'}
            if any(strcmp(props, q{1})), p = p + numel(L.(q{1})); end
        end
    end
end
