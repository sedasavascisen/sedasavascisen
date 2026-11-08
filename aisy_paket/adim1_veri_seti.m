% ADIM 1 - Veri seti (makaledeki 40 000 senaryo, N = 32)
%
% Yayimlanan RIS_dataset_large_2D.m ile ayni veriyi uretir (ayni rng(42),
% ayni cagri sirasi; bkz. ris_veri_uret.m). Sure: ~10-15 dk.
% Cikti: RIS_dataset_large_2D.mat  (orijinal betikle ayni degisken adlari)

clear; close all; clc;
t0 = tic;
D = ris_veri_uret(32, 40000, 42);
fprintf('Uretim suresi: %.1f dk\n', toc(t0)/60);

F = D.F;  G = D.G;  h_d = D.h_d;  THETA = D.THETA;
TX_pos = D.TX_pos;  RX_pos = D.RX_pos;  elemPos = D.elemPos;
N = D.N;  M = D.M;  K = D.K;  numScatter = D.numScatter;
roomSize = D.roomSize;  fc = D.fc;  Pt = D.Pt;  noise_var = D.noise_var;

fprintf('Faz etiketi: ortalama %.4f (beklenen ~0), std %.4f (beklenen %.4f)\n', ...
        mean(THETA(:)), std(THETA(:)), pi/sqrt(3));
h_ris   = h_d + sum(G .* exp(1j*THETA) .* F, 2);
snr_no  = 10*log10(Pt*abs(h_d).^2   / noise_var);
snr_ris = 10*log10(Pt*abs(h_ris).^2 / noise_var);
fprintf('SNR medyani: RIS yok %.1f dB, RIS ile %.1f dB\n', median(snr_no), median(snr_ris));

save('RIS_dataset_large_2D.mat', 'F','G','h_d','THETA','TX_pos','RX_pos','elemPos', ...
     'N','M','K','numScatter','roomSize','fc','Pt','noise_var','-v7.3');
fprintf('Kaydedildi: RIS_dataset_large_2D.mat\n');
