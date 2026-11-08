% ADIM 4 - Sekil: CD dogruluk ve gecikme, iterasyon sayisi K'ye gore
%
% Butun degerler fairness_K_results.mat'tan (adim 3) okunur; betikte elle
% yazilmis sayi YOKTUR. Eski sekildeki sorunlar ve cozumleri:
%   - iki y ekseni (yyaxis) uzerine binen yazilar  -> iki ayri panel
%   - gecikme ekseni [-0.5, 14] ms, veriler en altta sikisik -> log eksen
%   - eksen disina tasan, kesilen etiketler (x = 51.5) -> lejant asagida
%   - "K >= 20: URLLC Exceeded" golgesi, K = 20 (0.60 ms < 1 ms) icin
%     yanlisti -> golge yok; esik cizgisi ve olculen noktalar yeterli
%   - sekil ici baslik -> dergi stilinde baslik sekil altyazisinda olur
%     (BASLIK degiskenini doldurursaniz yine de yazilir)

clear; close all; clc;
L = load('fairness_K_results.mat');
K  = L.K_vals;  CD = L.CD;  CNN = L.CNN;  URLLC = L.URLLC_ms;

METRIK = 'inv';    % 'inv': ortak fazdan bagimsiz RMSE (onerilen), 'pub': makale tanimi
BASLIK = '';       % ornek: 'Coordinate descent: accuracy-latency trade-off'

if strcmp(METRIK, 'inv')
    r_cd = [CD.rmse_inv_deg];  r_cnn = CNN.rmse_inv_deg;
    ylab = 'Phase RMSE, common phase removed [\circ]';
else
    r_cd = [CD.rmse_pub_deg];  r_cnn = CNN.rmse_pub_deg;
    ylab = 'Phase-aware RMSE [\circ]';
end
t_cd = [CD.t_ms];

c_cd  = [0.00 0.45 0.74];   % CD
c_cnn = [0.85 0.33 0.10];   % CNN-LSTM
c_lim = [0.25 0.25 0.25];   % URLLC
FN = 'Times New Roman';  FS = 12;

fig = figure('Color', 'w', 'Units', 'centimeters', 'Position', [2 2 16 14]);
tl = tiledlayout(fig, 2, 1, 'TileSpacing', 'compact', 'Padding', 'compact');
if ~isempty(BASLIK), title(tl, BASLIK, 'FontName', FN, 'FontSize', FS+1, 'FontWeight', 'bold'); end

% ---- (a) dogruluk
ax1 = nexttile(tl);  hold(ax1, 'on');
p1 = plot(ax1, K, r_cd, '-s', 'Color', c_cd, 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', c_cd);
p2 = yline(ax1, r_cnn, '--', 'Color', c_cnn, 'LineWidth', 2);
for i = 1:numel(K)
    text(ax1, K(i), r_cd(i), sprintf('  %.2f\\circ', r_cd(i)), 'Color', c_cd, ...
        'FontName', FN, 'FontSize', FS-1, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left');
end
ylim(ax1, [0, 1.25*max([r_cd, r_cnn])]);
ylabel(ax1, ylab, 'FontName', FN, 'FontSize', FS);
title(ax1, '(a) Accuracy', 'FontName', FN, 'FontSize', FS, 'FontWeight', 'normal');
legend(ax1, [p1 p2], {'CD', sprintf('CNN-LSTM (%.2f\\circ)', r_cnn)}, ...
    'Location', 'northeast', 'FontName', FN, 'FontSize', FS-1);

% ---- (b) gecikme (log eksen)
ax2 = nexttile(tl);  hold(ax2, 'on');
q1 = semilogy(ax2, K, t_cd, '-o', 'Color', c_cd, 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', c_cd);
q2 = yline(ax2, CNN.t_single_ms, '--', 'Color', c_cnn, 'LineWidth', 2);
q3 = yline(ax2, CNN.t_batch_ms, ':', 'Color', c_cnn, 'LineWidth', 2);
q4 = yline(ax2, URLLC, '-.', 'Color', c_lim, 'LineWidth', 1.5);
set(ax2, 'YScale', 'log');
for i = 1:numel(K)
    text(ax2, K(i), t_cd(i), sprintf('  %.2f ms', t_cd(i)), 'Color', c_cd, ...
        'FontName', FN, 'FontSize', FS-1, 'VerticalAlignment', 'top', 'HorizontalAlignment', 'left');
end
yv = [t_cd, CNN.t_single_ms, CNN.t_batch_ms, URLLC];
ylim(ax2, [min(yv)/2, max(yv)*3]);
ylabel(ax2, 'Latency [ms] (log scale)', 'FontName', FN, 'FontSize', FS);
xlabel(ax2, 'CD iterations K', 'FontName', FN, 'FontSize', FS);
title(ax2, '(b) Latency per channel realisation', 'FontName', FN, 'FontSize', FS, 'FontWeight', 'normal');
legend(ax2, [q1 q2 q3 q4], {'CD (one sample)', ...
    sprintf('CNN-LSTM, one sample (%.2f ms)', CNN.t_single_ms), ...
    sprintf('CNN-LSTM, batch / sample (%.2f ms)', CNN.t_batch_ms), ...
    '1 ms (URLLC user-plane target)'}, 'Location', 'southoutside', 'NumColumns', 2, ...
    'FontName', FN, 'FontSize', FS-2);

for ax = [ax1 ax2]
    set(ax, 'FontName', FN, 'FontSize', FS, 'XLim', [0, max(K)+10], 'XTick', K, ...
        'Box', 'on', 'LineWidth', 1);
    grid(ax, 'on');  ax.GridAlpha = 0.25;
end
linkaxes([ax1 ax2], 'x');

exportgraphics(fig, 'Sekil_fairness_K.pdf', 'ContentType', 'vector');
exportgraphics(fig, 'Sekil_fairness_K.png', 'Resolution', 300);
fprintf('Kaydedildi: Sekil_fairness_K.pdf / .png\n');
