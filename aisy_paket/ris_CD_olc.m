function [Theta_all, sonuc] = ris_CD_olc(F, G, h_d, maxIter, sessiz)
% RIS_CD_OLC  Yayimlanan ris_CD.m ile AYNI algoritma (theta = 0'dan baslar,
% eleman eleman kapali-form guncelleme, maxIter tarama, ornek basina tic/toc),
% ama sonucu iki RMSE ile ve alinan gucle birlikte raporlar.
%
%   sonuc.rmse_pub_deg : makaledeki tanim, referans -angle(G)-angle(F)
%   sonuc.rmse_inv_deg : her ornegin ortak fazi cikarildiktan sonra RMSE
%   sonuc.guc_db       : CD / etiket alinan guc orani, ortalama dB
%   sonuc.t_ms         : ortalama sure, ms/ornek
%
% Neden iki RMSE: etiket dogrudan baglantiyi (h_d) yok sayar. CD gercek
% optimuma, yani tum yansimalari h_eff fazina hizalayan cozume yakinsar;
% bu, etiketten yalnizca bir ORTAK FAZ kadar farklidir. Ortak faz alinan
% gucu degistirmez ama makale tanimindaki RMSE'yi ~100 dereceye cikarir.

if nargin < 4 || isempty(maxIter), maxIter = 5; end
if nargin < 5, sessiz = false; end
[numSamples, N] = size(F);
Theta_all = ones(numSamples, N);
t_total = 0;
for s = 1:numSamples
    Fs = F(s,:);  Gs = G(s,:);  hd = h_d(s);
    Th = ones(1, N);
    t0 = tic;
    for it = 1:maxIter
        for n = 1:N
            mask = true(1, N);  mask(n) = false;
            Hm = hd + sum(Gs(mask) .* (Th(mask) .* Fs(mask)));
            th = angle(Hm) - angle(Gs(n) * Fs(n));
            th = mod(th + pi, 2*pi) - pi;
            Th(n) = exp(1j * th);
        end
    end
    t_total = t_total + toc(t0);
    Theta_all(s,:) = Th;
end

TH_pred = angle(Theta_all);
TH_ref  = -angle(G) - angle(F);
e   = angle(exp(1j * (TH_pred - TH_ref)));
phi = angle(mean(exp(1j*e), 2));
ei  = angle(exp(1j * (e - phi)));
guc = @(TH) abs(h_d + sum(G .* exp(1j*TH) .* F, 2)).^2;

sonuc.K            = maxIter;
sonuc.rmse_pub_deg = sqrt(mean(e(:).^2))  * 180/pi;
sonuc.rmse_inv_deg = sqrt(mean(ei(:).^2)) * 180/pi;
sonuc.guc_db       = mean(10*log10(guc(TH_pred) ./ guc(TH_ref)));
sonuc.t_ms         = t_total / numSamples * 1e3;
if ~sessiz, fprintf('CD K=%-3d | RMSE makale %.2f | ortak fazsiz %.2f derece | guc/etiket %+.2f dB | %.3f ms/ornek\n', ...
        maxIter, sonuc.rmse_pub_deg, sonuc.rmse_inv_deg, sonuc.guc_db, sonuc.t_ms); end
end
