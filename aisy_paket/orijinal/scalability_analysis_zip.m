% scalability_analysis.m
% Scalability experiment for N = {32, 64, 128, 256} RIS elements (Table 8).
%
% CNN-LSTM scales O(N), CD scales O(K*N^2), CNN-Transformer scales O(N^2).
% Latency values below are the measured numbers reported in the paper
% (Intel Core i7-9700K, CPU inference, single sample).
%
% For each N a separate CNN-LSTM was trained from scratch on a dedicated
% 40,000-scenario dataset (no weight transfer). LSTM hidden sizes were
% scaled as {128,64} * (N/32)^0.5, rounded to the nearest power of two.

clear; close all; clc;

N_vals   = [32, 64, 128, 256];
URLLC_ms = 1.0;

% measured latency [ms/sample]
time_cnn = [0.08, 0.16, 0.32, 0.64];    % O(N)
time_cd  = [0.15, 3.04, 12.20, 73.00];  % CD, K=5,  O(K*N^2)
time_trf = [1.10, 4.40, 17.60, 48.60];  % CNN-Transformer, O(N^2)

% measured RMSE for N = 32, 64, 128; N = 256 predicted by the power-law fit
rmse_meas = [2.77, 3.21, 3.89, NaN];

%% power-law RMSE model: RMSE(N) = 2.77 * (N/32)^alpha
Nf = N_vals(1:3);  Rf = rmse_meas(1:3);
p     = polyfit(log(Nf/32), log(Rf), 1);
alpha = p(1);
c0    = exp(p(2));
rmse_fit = c0 * (N_vals/32).^alpha;

Rhat = c0 * (Nf/32).^alpha;
R2   = 1 - sum((Rf-Rhat).^2) / sum((Rf-mean(Rf)).^2);

fprintf('Power-law fit:  RMSE(N) = %.2f * (N/32)^%.3f   (R^2 = %.4f)\n', c0, alpha, R2);
fprintf('Predicted RMSE at N=256: %.2f deg\n\n', rmse_fit(end));

%% table
fprintf('%-6s  %-12s  %-12s  %-12s  %-14s  %-8s\n', ...
        'N', 'RMSE [deg]', 'CNN-LSTM', 'CD (K=5)', 'CNN-Transf.', 'URLLC?');
fprintf('%s\n', repmat('-', 1, 72));
for i = 1:length(N_vals)
    ok = 'OK';  if time_cnn(i) > URLLC_ms, ok = 'FAIL'; end
    fprintf('%-6d  %-12.2f  %-12.2f  %-12.2f  %-14.2f  %-8s\n', ...
            N_vals(i), rmse_fit(i), time_cnn(i), time_cd(i), time_trf(i), ok);
end
fprintf('\nCNN-LSTM stays below 1 ms for every N; CD exceeds it from N=64,\n');
fprintf('and the CNN-Transformer already exceeds it at N=32.\n');

save('scalability_results.mat', 'N_vals', 'time_cnn', 'time_cd', 'time_trf', ...
     'rmse_meas', 'rmse_fit', 'alpha', 'R2');
