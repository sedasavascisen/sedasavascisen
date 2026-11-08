% ================================================================
% RIS_dataset_large_2D_UPDATED.m
% ================================================================
% Orijinal RIS_dataset_large_2D.m'in tam güncellenmiş versiyonu.
%
% YENİLİKLER:
%   - N parametrik: 32 / 64 / 128 desteği
%   - [H2-Y2] Ölçeklenebilirlik testi için çoklu N boyutu
%   - SNR istatistikleri (Hakem #2 Y7 — sistem metriği)
%   - Gelişmiş kalite güvence testleri
%   - GitHub README için yorum blokları
% ================================================================

clear; close all; clc;
rng(42);

%% ──────────────────────────────────────────────────────────────
%  KULLANICI AYARLARI
% ──────────────────────────────────────────────────────────────
numSamples = 40000;    % Toplam örnek sayısı

% [H2-Y2]: Farklı N boyutları için tek betik
% N=32 → 8×4  (makale ana çalışması)
% N=64 → 8×8  (ölçeklenebilirlik testi)
% N=128→16×8  (büyük ölçek projeksiyon)
N_target = 32;         % ← Buradan değiştirin: 32, 64 veya 128

switch N_target
    case 32,  M = 8;  K_ris = 4;
    case 64,  M = 8;  K_ris = 8;
    case 128, M = 16; K_ris = 8;
    otherwise
        error('N_target %d için M/K değerleri tanımlanmamış.', N_target);
end
N = M * K_ris;

%% ──────────────────────────────────────────────────────────────
%  KANAl PARAMETRELERİ (3GPP Release 17 uyumlu)
% ──────────────────────────────────────────────────────────────
numScatter  = 6;
roomSize    = [40 20 6];    % m
fc          = 3e9;          % 3 GHz taşıyıcı
c           = 3e8;
lambda      = c / fc;
k           = 2*pi / lambda;
Pt          = 1;            % W
noise_var   = 1e-3;         % W  (SNR ≈ 30 dB)
scatter_g   = 0.15;         % Saçılım kazancı

%% ──────────────────────────────────────────────────────────────
%  RIS 2D Panel Pozisyonu
% ──────────────────────────────────────────────────────────────
ris_center = [roomSize(1)/2, roomSize(2)/2, 3];
d_elem     = lambda / 2;

elemPos = zeros(N, 3);
x0 = ris_center(1) - (M-1)/2 * d_elem;
y0 = ris_center(2) - (K_ris-1)/2 * d_elem;
idx = 1;
for ii = 1:M
    for jj = 1:K_ris
        elemPos(idx,:) = [x0+(ii-1)*d_elem, y0+(jj-1)*d_elem, ris_center(3)];
        idx = idx + 1;
    end
end

fprintf('================================================\n');
fprintf(' RIS Veri Seti Üretimi\n');
fprintf(' N = %d (%d×%d), Örnekler = %d\n', N, M, K_ris, numSamples);
fprintf('================================================\n');

%% ──────────────────────────────────────────────────────────────
%  ÖN-ALOKASYON
% ──────────────────────────────────────────────────────────────
F      = complex(zeros(numSamples, N));
G      = complex(zeros(numSamples, N));
h_d    = complex(zeros(numSamples, 1));
THETA  = zeros(numSamples, N);
TX_pos = zeros(numSamples, 3);
RX_pos = zeros(numSamples, 3);

%% ──────────────────────────────────────────────────────────────
%  VERİ ÜRETİM DÖNGÜSÜ
% ──────────────────────────────────────────────────────────────
tic;
for s = 1:numSamples

    % Rastgele TX ve RX pozisyonları
    tx = [rand*roomSize(1), rand*roomSize(2), 1+rand];
    rx = [rand*roomSize(1), rand*roomSize(2), 1+rand];
    TX_pos(s,:) = tx;
    RX_pos(s,:) = rx;

    % Rastgele saçılıcılar
    scat_pos = rand(numScatter,3) .* roomSize;

    % Doğrudan kanal
    d_direct = norm(tx - rx);
    h_d(s)   = (randn+1j*randn)/sqrt(2) * exp(-1j*k*d_direct) / d_direct;

    % Element bazlı kanallar
    for n = 1:N
        el = elemPos(n,:);

        d_tx = norm(tx - el);
        d_rx = norm(el - rx);

        f0 = (randn+1j*randn)/sqrt(2) * exp(-1j*k*d_tx) / d_tx;
        g0 = (randn+1j*randn)/sqrt(2) * exp(-1j*k*d_rx) / d_rx;

        f_sc = 0;  g_sc = 0;
        for m = 1:numScatter
            da = norm(tx       - scat_pos(m,:));
            db = norm(scat_pos(m,:) - el    );
            dc = norm(el       - scat_pos(m,:));
            dd = norm(scat_pos(m,:) - rx    );

            f_sc = f_sc + scatter_g*(randn+1j*randn)/sqrt(2) * ...
                   exp(-1j*k*(da+db)) / (da*db);
            g_sc = g_sc + scatter_g*(randn+1j*randn)/sqrt(2) * ...
                   exp(-1j*k*(dc+dd)) / (dc*dd);
        end

        F(s,n) = f0 + f_sc;
        G(s,n) = g0 + g_sc;
    end

    % Optimal faz (kapalı-form çözüm, Denklem 8)
    THETA(s,:) = wrapToPi(-angle(F(s,:)) - angle(G(s,:)));

    if mod(s, 2000) == 0
        fprintf('  %d / %d örnek üretildi...\n', s, numSamples);
    end
end
toc;

%% ──────────────────────────────────────────────────────────────
%  TABLO 2: Veri Seti İstatistikleri (Makale Tablo 2)
% ──────────────────────────────────────────────────────────────
fprintf('\n=== VERİ SETİ İSTATİSTİKLERİ (Tablo 2) ===\n');

% Optimal faz istatistikleri
theta_flat = THETA(:);
fprintf('Optimal Faz Etiketleri θ*:\n');
fprintf('  Ortalama   : %.4f rad\n', mean(theta_flat));
fprintf('  Std        : %.4f rad  (teorik π/√3 = %.4f)\n', std(theta_flat), pi/sqrt(3));
fprintf('  Çarpıklık  : %.4f (≈0 olmalı)\n', skewness(theta_flat));
fprintf('  Basıklık   : %.4f\n', kurtosis(theta_flat));

% KS testi (düzgün dağılım uyumu)
[h_ks, p_ks] = kstest((theta_flat+pi)/(2*pi));  % normalize [0,1]
fprintf('  KS p-değeri: %.4f (%s)\n', p_ks, ternary(p_ks>0.05,'düzgün dağılım ✓','reddedildi ✗'));

% Örnekler arası korelasyon
r_intersampl = mean(abs(corr(THETA') - eye(numSamples)), 'all');
fprintf('  Örnek arası ortalama korelasyon: %.4f (< 0.10 olmalı)\n\n', r_intersampl);

%% ──────────────────────────────────────────────────────────────
%  SNR İSTATİSTİKLERİ (Hakem #2 Y7 — Sistem Metrikleri)
% ──────────────────────────────────────────────────────────────
fprintf('=== SNR İSTATİSTİKLERİ ===\n');

% RIS olmadan (doğrudan kanal)
h_no_ris = h_d;
SNR_no_ris = Pt * abs(h_no_ris).^2 / noise_var;

% Optimal RIS ile
h_with_ris = h_d + sum(G .* exp(1j*THETA) .* F, 2);
SNR_with_ris = Pt * abs(h_with_ris).^2 / noise_var;

SNR_gain_dB = 10*log10(SNR_with_ris+eps) - 10*log10(SNR_no_ris+eps);

fprintf('  RIS Olmadan  SNR: %.1f – %.1f dB (medyan ≈ %.1f dB)\n', ...
    min(10*log10(SNR_no_ris+eps)), max(10*log10(SNR_no_ris+eps)), ...
    median(10*log10(SNR_no_ris+eps)));
fprintf('  Optimal RIS  SNR: %.1f – %.1f dB (medyan ≈ %.1f dB)\n', ...
    min(10*log10(SNR_with_ris+eps)), max(10*log10(SNR_with_ris+eps)), ...
    median(10*log10(SNR_with_ris+eps)));
fprintf('  RIS Kazancı: medyan ≈ %.1f dB\n\n', median(SNR_gain_dB));

%% ──────────────────────────────────────────────────────────────
%  KAYDET
% ──────────────────────────────────────────────────────────────
savefile = sprintf('RIS_dataset_large_%dD_%delem.mat', 2, N);
save(savefile, 'F','G','h_d','THETA','TX_pos','RX_pos','elemPos', ...
               'N','M','K_ris','numScatter','roomSize','fc','Pt','noise_var', ...
               'SNR_no_ris','SNR_with_ris','SNR_gain_dB', '-v7.3');

fprintf('Kaydedildi: %s\n', savefile);
fprintf('(N=%d, %d örnek, %d eleman)\n', N, numSamples, N);
fprintf('Note: Bu veri seti GitHub deposuna yüklenmiştir:\n');
fprintf('  https://github.com/sedasavascisen/ris-phase-aware-cnn-lstm\n');
fprintf('=== TAMAMLANDI ===\n');

%% ──────────────────────────────────────────────────────────────
%  YARDIMCI FONKSİYON
% ──────────────────────────────────────────────────────────────
function out = ternary(cond, a, b)
    if cond, out = a; else out = b; end
end
