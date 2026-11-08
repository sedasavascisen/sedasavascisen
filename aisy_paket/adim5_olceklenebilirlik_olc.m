% ADIM 5 - Olceklenebilirlik: gecikme, RIS eleman sayisi N'ye gore (OLCUM)
%
% Yayimlanan Sekil 1'in betikleri (orijinal/scalability_analysis_zip.m,
% orijinal/Scalability_Analysis_sekil.m) gecikmeleri ELLE YAZILMIS dizilerden
% cizer; olcen bir betik pakette yok ve iki surum birbirini tutmuyor (ornegin
% N = 256'da CD ile Transformer degerleri yer degistirmis). Bu betik ayni
% uc yontemi her N icin AYNI kosulda OLCER:
%   - tek senaryo, sirayla, CPU, medyan (dagitimdaki gercek durum)
%   - agirliklar gecikmeyi degistirmez; bu yuzden aglar egitilmeden,
%     ayni mimariyle olculur (dogruluk icin her N'de egitim gerekir; o ayri is)
% Gereken: Deep Learning Toolbox; Transformer icin R2023a+ (selfAttentionLayer).
% Cikti: scalability_results.mat, Sekil_olceklenebilirlik.pdf/.png

clear; close all; clc;
N_vals = [32 64 128 256];
nS   = 100;      % gecikme olcumu icin senaryo sayisi (medyan)
K_cd = 5;

t_cd = nan(size(N_vals));  t_cnn = t_cd;  t_trf = t_cd;
for j = 1:numel(N_vals)
    N = N_vals(j);
    D = ris_veri_uret(N, nS, 7);

    % CD, K = 5 (yayimlanan algoritma, ornek basina)
    tt = zeros(nS,1);
    ris_CD_olc(D.F(1,:), D.G(1,:), D.h_d(1), K_cd, true);    % isinma
    for s = 1:nS
        t1 = tic;  ris_CD_olc(D.F(s,:), D.G(s,:), D.h_d(s), K_cd, true);  tt(s) = toc(t1)*1e3;
    end
    t_cd(j) = median(tt);

    % CNN-LSTM (yayimlanan mimari), tek ornek
    lay = [sequenceInputLayer(4)
           convolution1dLayer(3,64,'Padding','same'); batchNormalizationLayer; reluLayer
           convolution1dLayer(3,64,'Padding','same'); batchNormalizationLayer; reluLayer
           dropoutLayer(0.2)
           lstmLayer(128,'OutputMode','sequence'); lstmLayer(64,'OutputMode','sequence')
           dropoutLayer(0.3); fullyConnectedLayer(2)];
    t_cnn(j) = tek_ornek_gecikme(dlnetwork(lay), D, nS);

    % CNN-Transformer (orijinal/transformer_baseline.m ile ayni katmanlar)
    try
        lg = layerGraph([sequenceInputLayer(4,'Name','in')
              fullyConnectedLayer(64,'Name','embed'); reluLayer('Name','relu_emb')
              selfAttentionLayer(4,16,'Name','attn1'); additionLayer(2,'Name','add1')
              layerNormalizationLayer('Name','ln1')
              fullyConnectedLayer(64,'Name','ff1'); reluLayer('Name','relu1')
              selfAttentionLayer(4,16,'Name','attn2'); additionLayer(2,'Name','add2')
              layerNormalizationLayer('Name','ln2')
              fullyConnectedLayer(64,'Name','ff2'); reluLayer('Name','relu2')
              fullyConnectedLayer(2,'Name','fc_out')]);
        lg = connectLayers(lg, 'relu_emb', 'add1/in2');
        lg = connectLayers(lg, 'ln1', 'add2/in2');
        t_trf(j) = tek_ornek_gecikme(dlnetwork(lg), D, nS);
    catch err
        fprintf('Transformer olculemedi (%s)\n', err.message);
    end
    fprintf('N = %3d | CD K=%d %.3f ms | CNN-LSTM %.3f ms | Transformer %.3f ms\n', ...
            N, K_cd, t_cd(j), t_cnn(j), t_trf(j));
end
save('scalability_results.mat', 'N_vals', 't_cd', 't_cnn', 't_trf', 'K_cd', 'nS');

%% sekil (log-log; yazilar eksen icinde, lejant disarida)
FN = 'Times New Roman';  FS = 12;
fig = figure('Color','w','Units','centimeters','Position',[2 2 16 10]);
ax = axes(fig);  hold(ax,'on');
h1 = loglog(ax, N_vals, t_cnn, '-o', 'LineWidth', 2, 'MarkerSize', 7, 'Color', [0.85 0.33 0.10], 'MarkerFaceColor', [0.85 0.33 0.10]);
h2 = loglog(ax, N_vals, t_cd,  '-^', 'LineWidth', 2, 'MarkerSize', 7, 'Color', [0.00 0.45 0.74], 'MarkerFaceColor', [0.00 0.45 0.74]);
hh = [h1 h2];  lab = {'CNN-LSTM', sprintf('CD (K = %d)', K_cd)};
if any(~isnan(t_trf))
    h3 = loglog(ax, N_vals, t_trf, '-s', 'LineWidth', 2, 'MarkerSize', 7, 'Color', [0.47 0.67 0.19], 'MarkerFaceColor', [0.47 0.67 0.19]);
    hh(end+1) = h3;  lab{end+1} = 'CNN-Transformer';
end
h4 = yline(ax, 1, '-.', 'Color', [0.25 0.25 0.25], 'LineWidth', 1.5);
hh(end+1) = h4;  lab{end+1} = '1 ms (URLLC user-plane target)';
set(ax, 'XScale','log', 'YScale','log', 'XTick', N_vals, 'XLim', [N_vals(1)/1.2, N_vals(end)*1.2], ...
    'FontName', FN, 'FontSize', FS, 'Box', 'on');
grid(ax,'on');
xlabel(ax, 'Number of RIS elements N', 'FontName', FN, 'FontSize', FS);
ylabel(ax, 'Latency per sample [ms]', 'FontName', FN, 'FontSize', FS);
legend(ax, hh, lab, 'Location', 'southoutside', 'NumColumns', 2, 'FontName', FN, 'FontSize', FS-1);
exportgraphics(fig, 'Sekil_olceklenebilirlik.pdf', 'ContentType', 'vector');
exportgraphics(fig, 'Sekil_olceklenebilirlik.png', 'Resolution', 300);

function t = tek_ornek_gecikme(net, D, nS)
    N = size(D.F, 2);
    x = @(s) dlarray(reshape(single([real(D.F(s,:)); imag(D.F(s,:)); real(D.G(s,:)); imag(D.G(s,:))]), 4, 1, N), 'CBT');
    predict(net, x(1));                                       % isinma
    tt = zeros(nS,1);
    for s = 1:nS
        xs = x(s);
        t1 = tic;  y = predict(net, xs);  y = extractdata(y);  tt(s) = toc(t1)*1e3; %#ok<NASGU>
    end
    t = median(tt);
end
