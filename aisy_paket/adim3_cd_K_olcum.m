% ADIM 3 - CD taban cizgisi, K = 5 / 20 / 50 (makale Sekil 2, tez Sekil 4)
%
% CD, CNN-LSTM ile AYNI test orneklerinde olculur (adim 2'nin testIdx'i).
% Orijinal betik (orijinal/baseline_fairness_K_analysis_v1_olcum.m) CD'yi
% verinin SON %15'inde, CNN'i ise rastgele %15'te olcuyordu; CNN degerleri de
% betige elle yazilmisti (2.77, 0.08). Burada hepsi dosyadan okunur.
%
% Gereken: RIS_dataset_large_2D.mat, cnn_lstm_test_results.mat, ris_CD_olc.m
% Cikti: fairness_K_results.mat  (adim 4 sekli bundan cizer)
% Sure: ~K toplamina orantili; 6000 ornekle K=50 birkac dakika.

clear; close all; clc;
S = load('RIS_dataset_large_2D.mat');
R = load('cnn_lstm_test_results.mat');
te = R.testIdx;
F_t = S.F(te,:);  G_t = S.G(te,:);  hd_t = S.h_d(te);
fprintf('Test: %d ornek (CNN-LSTM ile ayni)\n\n', numel(te));

K_vals = [5, 20, 50];
for i = 1:numel(K_vals)
    [~, s] = ris_CD_olc(F_t, G_t, hd_t, K_vals(i));
    if i == 1, CD = s; else, CD(i) = s; end %#ok<SAGROW>
end

CNN.rmse_pub_deg  = R.rmse_deg;
CNN.rmse_inv_deg  = R.rmse_inv_deg;
CNN.guc_db        = R.cnn_over_label_db;
CNN.t_batch_ms    = R.t_per_sample_batch;
CNN.t_single_ms   = R.t_single_cpu;
URLLC_ms = 1.0;

fprintf('\n%-10s %12s %14s %12s %12s\n', 'Yontem', 'RMSE makale', 'RMSE ortak.f.', 'Guc/etiket', 'Sure [ms]');
fprintf('%s\n', repmat('-', 1, 64));
fprintf('%-10s %12.2f %14.2f %+11.2f %12.3f (tek ornek; toplu %.3f)\n', 'CNN-LSTM', ...
        CNN.rmse_pub_deg, CNN.rmse_inv_deg, CNN.guc_db, CNN.t_single_ms, CNN.t_batch_ms);
for i = 1:numel(CD)
    fprintf('%-10s %12.2f %14.2f %+11.2f %12.3f\n', sprintf('CD K=%d', CD(i).K), ...
            CD(i).rmse_pub_deg, CD(i).rmse_inv_deg, CD(i).guc_db, CD(i).t_ms);
end
fprintf('\nOkuma: "RMSE makale" etikete uzaklik; etiket h_d''yi yok saydigi icin CD burada\n');
fprintf('cezalandirilir. Alinan guc (dB) dogrudan performans olcutudur.\n');

save('fairness_K_results.mat', 'K_vals', 'CD', 'CNN', 'URLLC_ms');
fprintf('Kaydedildi: fairness_K_results.mat\n');
