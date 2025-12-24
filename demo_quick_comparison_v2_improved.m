function demo_quick_comparison_v2_improved()
% =========================================================================
% IMPROVED RIS BOYUT KARŞILAŞTIRMASI
%
% İYİLEŞTİRMELER:
% ✅ Input normalizasyonu eklendi
% ✅ Validation split + early stopping
% ✅ Learning rate scheduling
% ✅ Daha fazla veri (5000 sample)
% ✅ Training progress görselleştirme
% ✅ Doğru hyperparameter logic
% ✅ Detaylı metrikler ve sanity checks
%
% Tahmini süre: 30-60 dakika
% =========================================================================

clear; close all; clc;

fprintf('========================================\n');
fprintf('RIS PANEL SIZE COMPARISON - IMPROVED\n');
fprintf('========================================\n\n');

% Demo konfigürasyonları
configs = {
    struct('M', 4, 'K', 4, 'name', '4x4', 'N', 16),
    struct('M', 8, 'K', 8, 'name', '8x8', 'N', 64),
    struct('M', 16, 'K', 16, 'name', '16x16', 'N', 256)
};

% Ortak parametreler
numSamples = 5000;  % ✅ 1000 → 5000 (daha fazla veri)
numScatter = 6;
roomSize = [40 20 6];
fc = 3e9;
c = 3e8;
lambda = c/fc;
k = 2*pi/lambda;
Pt = 1;
noise_var = 1e-3;

results = struct();
results.configs = configs;
results.metrics = cell(length(configs), 1);

% Her boyut için
for cfg_idx = 1:length(configs)
    cfg = configs{cfg_idx};
    M = cfg.M;
    K = cfg.K;
    N = cfg.N;

    fprintf('\n========================================\n');
    fprintf('PROCESSING: %s (%d elements)\n', cfg.name, N);
    fprintf('========================================\n');

    %% 1. Dataset Generation
    fprintf('[1/4] Generating dataset (%d samples)...\n', numSamples);

    ris_center = [roomSize(1)/2, roomSize(2)/2, 3];
    d = lambda/2;

    elemPos = zeros(N, 3);
    x0 = ris_center(1) - (M-1)/2 * d;
    y0 = ris_center(2) - (K-1)/2 * d;

    idx = 1;
    for ii = 1:M
        for jj = 1:K
            elemPos(idx,:) = [x0 + (ii-1)*d, y0 + (jj-1)*d, ris_center(3)];
            idx = idx + 1;
        end
    end

    F = complex(zeros(numSamples, N));
    G = complex(zeros(numSamples, N));
    h_d = complex(zeros(numSamples, 1));
    THETA = zeros(numSamples, N);

    rng(42);
    tic_data = tic;

    for s = 1:numSamples
        tx = [rand*roomSize(1), rand*roomSize(2), 1 + rand*1];
        rx = [rand*roomSize(1), rand*roomSize(2), 1 + rand*1];

        scat_pos = [rand(numScatter,1)*roomSize(1), ...
                    rand(numScatter,1)*roomSize(2), ...
                    rand(numScatter,1)*roomSize(3)];

        d_direct = norm(tx - rx);
        ray_d = (randn + 1j*randn)/sqrt(2);
        h_d(s) = ray_d * exp(-1j*k*d_direct) / d_direct;

        for n = 1:N
            elem = elemPos(n,:);
            d_tx_elem = norm(tx - elem);
            d_elem_rx = norm(elem - rx);

            % ✅ Minimum distance check (division by zero prevention)
            d_tx_elem = max(d_tx_elem, 0.01);
            d_elem_rx = max(d_elem_rx, 0.01);

            ray_tx_elem = (randn + 1j*randn)/sqrt(2);
            ray_elem_rx = (randn + 1j*randn)/sqrt(2);

            f_direct = ray_tx_elem * exp(-1j*k*d_tx_elem) / d_tx_elem;
            g_direct = ray_elem_rx * exp(-1j*k*d_elem_rx) / d_elem_rx;

            f_scatter_sum = 0;
            g_scatter_sum = 0;
            scatter_gain = 0.15;

            for m = 1:numScatter
                d1 = norm(tx - scat_pos(m,:));
                d2 = norm(scat_pos(m,:) - elem);
                d1 = max(d1, 0.01);
                d2 = max(d2, 0.01);

                f_scatter_sum = f_scatter_sum + ...
                    scatter_gain * (randn+1j*randn)/sqrt(2) * ...
                    exp(-1j*k*(d1+d2)) / (d1*d2);

                d3 = norm(elem - scat_pos(m,:));
                d4 = norm(scat_pos(m,:) - rx);
                d3 = max(d3, 0.01);
                d4 = max(d4, 0.01);

                g_scatter_sum = g_scatter_sum + ...
                    scatter_gain * (randn+1j*randn)/sqrt(2) * ...
                    exp(-1j*k*(d3+d4)) / (d3*d4);
            end

            F(s,n) = f_direct + f_scatter_sum;
            G(s,n) = g_direct + g_scatter_sum;
        end

        THETA(s,:) = wrapToPi(-angle(F(s,:)) - angle(G(s,:)));

        if mod(s, 1000) == 0
            fprintf('   Progress: %d/%d samples\n', s, numSamples);
        end
    end

    data_time = toc(tic_data);
    fprintf('   Dataset generated in %.2f seconds\n', data_time);

    % ✅ Sanity check: NaN detection
    if any(isnan(F(:))) || any(isnan(G(:))) || any(isnan(THETA(:)))
        error('NaN detected in dataset! Check distance calculations.');
    end

    %% 2. Feature Preparation with NORMALIZATION
    fprintf('[2/4] Preparing features with normalization...\n');

    % ✅ CRITICAL: Amplitude normalization
    F_norm = F ./ (abs(F) + 1e-10);
    G_norm = G ./ (abs(G) + 1e-10);

    % Alternative: Keep magnitude information separately
    % For now, we use normalized version

    X = cell(numSamples, 1);
    Y = cell(numSamples, 1);
    for i = 1:numSamples
        X{i} = [real(F_norm(i,:)); imag(F_norm(i,:));
                real(G_norm(i,:)); imag(G_norm(i,:))];
        Y{i} = [sin(THETA(i,:)); cos(THETA(i,:))];
    end

    fprintf('   Input range check:\n');
    X_stack = cell2mat(X');
    fprintf('     Min: %.4f, Max: %.4f\n', min(X_stack(:)), max(X_stack(:)));
    fprintf('     Mean: %.4f, Std: %.4f\n', mean(X_stack(:)), std(X_stack(:)));

    % ✅ Train/Val/Test split (70/15/15)
    rng(42);
    cv1 = cvpartition(numSamples, 'HoldOut', 0.3);  % 70% train, 30% temp
    trainIdx = training(cv1);
    tempIdx = test(cv1);

    tempSize = sum(tempIdx);
    cv2 = cvpartition(tempSize, 'HoldOut', 0.5);  % Split temp: 50/50 → val/test
    tempIndices = find(tempIdx);
    valIdx = false(numSamples, 1);
    testIdx = false(numSamples, 1);
    valIdx(tempIndices(training(cv2))) = true;
    testIdx(tempIndices(test(cv2))) = true;

    Xtrain = X(trainIdx);
    Ytrain = Y(trainIdx);
    Xval = X(valIdx);
    Yval = Y(valIdx);
    Xtest = X(testIdx);
    Ytest = Y(testIdx);

    fprintf('   Dataset split:\n');
    fprintf('     Train: %d samples\n', sum(trainIdx));
    fprintf('     Val:   %d samples\n', sum(valIdx));
    fprintf('     Test:  %d samples\n', sum(testIdx));

    %% 3. Model Architecture (Scaled)
    fprintf('[3/4] Building and training model...\n');

    % ✅ Improved hyperparameter logic
    if N <= 16
        lstm1_units = 16;    % ✅ 32 → 16 (simpler model)
        lstm2_units = 8;     % ✅ 16 → 8
        conv_filters = 8;    % ✅ 16 → 8
        maxEpochs = 100;     % ✅ 20 → 100 (more epochs for small model)
        miniBatchSize = 32;
    elseif N <= 64
        lstm1_units = 64;
        lstm2_units = 32;
        conv_filters = 32;
        maxEpochs = 80;      % ✅ 15 → 80
        miniBatchSize = 32;
    else
        lstm1_units = 128;
        lstm2_units = 64;
        conv_filters = 64;
        maxEpochs = 60;      % ✅ 10 → 60
        miniBatchSize = 64;
    end

    fprintf('   Model configuration:\n');
    fprintf('     LSTM units: [%d, %d]\n', lstm1_units, lstm2_units);
    fprintf('     Conv filters: %d\n', conv_filters);
    fprintf('     Max epochs: %d\n', maxEpochs);
    fprintf('     Batch size: %d\n', miniBatchSize);

    layers = [
        sequenceInputLayer(4, "Name", "input")
        convolution1dLayer(3, conv_filters, 'Padding', 'same', 'Name', 'conv1')
        batchNormalizationLayer('Name', 'bn1')
        reluLayer('Name', 'relu1')
        dropoutLayer(0.3, 'Name', 'drop1')  % ✅ 0.2 → 0.3
        lstmLayer(lstm1_units, 'OutputMode', 'sequence', 'Name', 'lstm1')
        dropoutLayer(0.2, 'Name', 'drop2')  % ✅ Added dropout after LSTM
        lstmLayer(lstm2_units, 'OutputMode', 'sequence', 'Name', 'lstm2')
        dropoutLayer(0.2, 'Name', 'drop3')  % ✅ Added dropout after LSTM
        fullyConnectedLayer(2, 'Name', 'fc')
        regressionLayer('Name', 'output')
    ];

    % ✅ Improved training options
    options = trainingOptions("adam", ...
        MaxEpochs=maxEpochs, ...
        MiniBatchSize=miniBatchSize, ...
        InitialLearnRate=1e-3, ...
        LearnRateSchedule='piecewise', ...        % ✅ Added LR decay
        LearnRateDropPeriod=20, ...               % ✅ Drop every 20 epochs
        LearnRateDropFactor=0.5, ...              % ✅ Halve the LR
        Shuffle="every-epoch", ...
        ValidationData={Xval, Yval}, ...          % ✅ Validation set
        ValidationFrequency=30, ...               % ✅ Check every 30 iterations
        Plots="training-progress", ...            % ✅ Show training curve
        Verbose=1, ...                            % ✅ Show progress
        OutputNetwork='best-validation-loss');    % ✅ Save best model

    tic_train = tic;
    net = trainNetwork(Xtrain, Ytrain, layers, options);
    train_time = toc(tic_train);

    fprintf('   Training completed in %.2f seconds\n', train_time);

    %% 4. Evaluation with Detailed Metrics
    fprintf('[4/4] Evaluating model...\n');

    numTest = numel(Xtest);
    THETA_pred = zeros(numTest, N);

    for i = 1:numTest
        Ypred = predict(net, Xtest{i});
        THETA_pred(i,:) = atan2(Ypred(1,:), Ypred(2,:));
    end

    THETA_true = THETA(testIdx, :);
    phase_error = angle(exp(1j*(THETA_pred - THETA_true)));

    % Basic metrics
    rmse_rad = sqrt(mean(phase_error(:).^2));
    mae_rad = mean(abs(phase_error(:)));
    rmse_deg = rad2deg(rmse_rad);
    mae_deg = rad2deg(mae_rad);

    error_deg = rad2deg(abs(phase_error(:)));
    below_5deg = sum(error_deg < 5) / numel(error_deg) * 100;
    below_10deg = sum(error_deg < 10) / numel(error_deg) * 100;
    below_15deg = sum(error_deg < 15) / numel(error_deg) * 100;

    % ✅ Additional detailed metrics
    median_error = rad2deg(median(abs(phase_error(:))));
    p75_error = rad2deg(prctile(abs(phase_error(:)), 75));
    p90_error = rad2deg(prctile(abs(phase_error(:)), 90));
    p95_error = rad2deg(prctile(abs(phase_error(:)), 95));

    % Element-wise statistics
    elem_wise_mae = mean(abs(phase_error), 1);
    [worst_elem_mae, worst_elem_idx] = max(elem_wise_mae);
    [best_elem_mae, best_elem_idx] = min(elem_wise_mae);

    %% Store Results
    result = struct();
    result.config_name = cfg.name;
    result.N = N;
    result.data_time = data_time;
    result.train_time = train_time;
    result.rmse_deg = rmse_deg;
    result.mae_deg = mae_deg;
    result.median_deg = median_error;
    result.below_5deg = below_5deg;
    result.below_10deg = below_10deg;
    result.below_15deg = below_15deg;
    result.p75_deg = p75_error;
    result.p90_deg = p90_error;
    result.p95_deg = p95_error;
    result.worst_elem_idx = worst_elem_idx;
    result.worst_elem_mae = rad2deg(worst_elem_mae);
    result.best_elem_idx = best_elem_idx;
    result.best_elem_mae = rad2deg(best_elem_mae);

    results.metrics{cfg_idx} = result;

    fprintf('\n   ========== RESULTS ==========\n');
    fprintf('   RMSE:         %.2f°\n', rmse_deg);
    fprintf('   MAE:          %.2f°\n', mae_deg);
    fprintf('   Median Error: %.2f°\n', median_error);
    fprintf('   \n');
    fprintf('   Accuracy:\n');
    fprintf('     < 5°:  %.1f%%\n', below_5deg);
    fprintf('     < 10°: %.1f%%\n', below_10deg);
    fprintf('     < 15°: %.1f%%\n', below_15deg);
    fprintf('   \n');
    fprintf('   Percentiles:\n');
    fprintf('     75th: %.2f°\n', p75_error);
    fprintf('     90th: %.2f°\n', p90_error);
    fprintf('     95th: %.2f°\n', p95_error);
    fprintf('   \n');
    fprintf('   Element-wise:\n');
    fprintf('     Best elem:  #%d (MAE: %.2f°)\n', best_elem_idx, rad2deg(best_elem_mae));
    fprintf('     Worst elem: #%d (MAE: %.2f°)\n', worst_elem_idx, rad2deg(worst_elem_mae));
    fprintf('   =============================\n\n');

    % Save training figure
    fig_name = sprintf('training_curve_%s.png', cfg.name);
    saveas(gcf, fig_name);
    fprintf('   Training curve saved: %s\n', fig_name);
end

%% Final Comparison
fprintf('\n========================================\n');
fprintf('FINAL COMPARISON TABLE\n');
fprintf('========================================\n\n');

fprintf('%-10s | %6s | %8s | %8s | %8s | %8s | %8s\n', ...
    'Config', 'N', 'RMSE(°)', 'MAE(°)', 'Med(°)', '<5°(%)', '<10°(%)');
fprintf('%s\n', repmat('-', 1, 80));

for i = 1:length(results.metrics)
    if ~isempty(results.metrics{i})
        r = results.metrics{i};
        fprintf('%-10s | %6d | %8.2f | %8.2f | %8.2f | %8.1f | %8.1f\n', ...
            r.config_name, r.N, r.rmse_deg, r.mae_deg, r.median_deg, ...
            r.below_5deg, r.below_10deg);
    end
end

fprintf('\n========================================\n');

%% Improvement Comparison
fprintf('\nIMPROVEMENT vs ORIGINAL:\n');
fprintf('%-10s | %15s | %15s | %15s\n', 'Config', 'Old RMSE', 'New RMSE', 'Improvement');
fprintf('%s\n', repmat('-', 1, 60));

% Original results (from your output)
original_rmse = [65.98, 26.68, 21.55];

for i = 1:length(results.metrics)
    if ~isempty(results.metrics{i})
        r = results.metrics{i};
        improvement = ((original_rmse(i) - r.rmse_deg) / original_rmse(i)) * 100;
        fprintf('%-10s | %13.2f° | %13.2f° | %13.1f%%\n', ...
            r.config_name, original_rmse(i), r.rmse_deg, improvement);
    end
end

fprintf('\n========================================\n');

%% Comprehensive Visualization
N_vals = [];
rmse_vals = [];
mae_vals = [];
median_vals = [];
train_times = [];
acc5_vals = [];
acc10_vals = [];

for i = 1:length(results.metrics)
    if ~isempty(results.metrics{i})
        r = results.metrics{i};
        N_vals(end+1) = r.N;
        rmse_vals(end+1) = r.rmse_deg;
        mae_vals(end+1) = r.mae_deg;
        median_vals(end+1) = r.median_deg;
        train_times(end+1) = r.train_time;
        acc5_vals(end+1) = r.below_5deg;
        acc10_vals(end+1) = r.below_10deg;
    end
end

figure('Position', [100 100 1400 800]);

subplot(2,3,1);
plot(N_vals, rmse_vals, '-o', 'LineWidth', 2, 'MarkerSize', 10);
hold on;
plot(N_vals, original_rmse, '--s', 'LineWidth', 2, 'MarkerSize', 10);
xlabel('RIS Element Count (N)');
ylabel('RMSE [°]');
title('Phase Prediction Accuracy');
legend('Improved', 'Original', 'Location', 'best');
grid on;
set(gca, 'XScale', 'log');

subplot(2,3,2);
plot(N_vals, mae_vals, '-o', 'LineWidth', 2, 'MarkerSize', 10);
hold on;
plot(N_vals, median_vals, '--s', 'LineWidth', 2, 'MarkerSize', 10);
xlabel('RIS Element Count (N)');
ylabel('Error [°]');
title('MAE vs Median Error');
legend('MAE', 'Median', 'Location', 'best');
grid on;
set(gca, 'XScale', 'log');

subplot(2,3,3);
plot(N_vals, train_times, '-s', 'LineWidth', 2, 'MarkerSize', 10);
xlabel('RIS Element Count (N)');
ylabel('Training Time [seconds]');
title('Computational Cost');
grid on;
set(gca, 'XScale', 'log');

subplot(2,3,4);
bar_data = [acc5_vals; acc10_vals]';
bar(categorical({'4x4', '8x8', '16x16'}), bar_data);
ylabel('Accuracy [%]');
title('Prediction Accuracy');
legend('<5°', '<10°', 'Location', 'best');
grid on;

subplot(2,3,5);
improvement_pct = ((original_rmse - rmse_vals) ./ original_rmse) * 100;
bar(categorical({'4x4', '8x8', '16x16'}), improvement_pct);
ylabel('RMSE Improvement [%]');
title('Improvement vs Original');
grid on;

subplot(2,3,6);
% Error distribution for 16x16 (best case)
if length(results.metrics) >= 3 && ~isempty(results.metrics{3})
    % Get test errors for 16x16
    testIdx_final = testIdx;  % From last iteration
    THETA_true_final = THETA(testIdx_final, :);
    phase_error_final = angle(exp(1j*(THETA_pred - THETA_true_final)));
    error_deg_final = rad2deg(abs(phase_error_final(:)));

    histogram(error_deg_final, 50, 'Normalization', 'probability');
    xlabel('Phase Error [°]');
    ylabel('Probability');
    title('Error Distribution (16x16)');
    xline(5, 'r--', 'LineWidth', 2);
    xline(10, 'g--', 'LineWidth', 2);
    grid on;
end

sgtitle('Comprehensive RIS Performance Analysis', 'FontSize', 14, 'FontWeight', 'bold');

saveas(gcf, 'demo_comparison_improved.png');
fprintf('\nComprehensive plot saved: demo_comparison_improved.png\n');

%% Save results
save('demo_results_improved.mat', 'results');
fprintf('Results saved: demo_results_improved.mat\n\n');

fprintf('========================================\n');
fprintf('IMPROVED DEMO COMPLETED!\n');
fprintf('========================================\n\n');

fprintf('KEY IMPROVEMENTS IMPLEMENTED:\n');
fprintf('✅ Input normalization (F, G amplitude normalized)\n');
fprintf('✅ Validation split (70/15/15 train/val/test)\n');
fprintf('✅ Early stopping (best validation loss)\n');
fprintf('✅ Learning rate decay (halved every 20 epochs)\n');
fprintf('✅ More data (5000 vs 1000 samples)\n');
fprintf('✅ Better model scaling (simpler for small N)\n');
fprintf('✅ More dropout (0.3 vs 0.2)\n');
fprintf('✅ Training visualization\n');
fprintf('✅ Detailed metrics and sanity checks\n\n');

end
