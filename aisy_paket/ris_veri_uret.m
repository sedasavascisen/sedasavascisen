function D = ris_veri_uret(N_target, numSamples, seed)
% RIS_VERI_URET  Yayimlanan RIS_dataset_large_2D.m'nin fonksiyon hali.
%
%   D = ris_veri_uret(32, 40000, 42)
%
% Kanal modeli, parametreler ve RASTGELE SAYI SIRASI orijinal betikle
% (orijinal/RIS_dataset_large_2D.m) birebir aynidir: rng(seed) sonrasinda
% randn/rand cagrilari ayni sirada yapilir. Bu yuzden N = 32, 40000 ornek,
% seed = 42 ile makaledeki veri seti aynen uretilir.
%
% N_target: 32 (8x4, makale), 64 (8x8), 128 (16x8), 256 (16x16).
% Cikti D: F, G, h_d, THETA, TX_pos, RX_pos, elemPos ve parametreler.
%
% NOT (bilinen ozellik, degistirilmedi): eleman basina bagimsiz Rayleigh
% katsayisi cekilir, yani komsu elemanlar arasinda uzamsal korelasyon
% yoktur; THETA etiketi dogrudan baglantiyi (h_d) yok sayar.

if nargin < 3, seed = 42; end
rng(seed);

switch N_target
    case 32,  M = 8;  K = 4;
    case 64,  M = 8;  K = 8;
    case 128, M = 16; K = 8;
    case 256, M = 16; K = 16;
    otherwise, error('N_target 32, 64, 128 ya da 256 olmali');
end
N = M*K;

fc = 3e9;  c = 3e8;  lambda = c/fc;  kwave = 2*pi/lambda;
numScatter = 6;  roomSize = [40 20 6];  scatter_g = 0.15;
Pt = 1;  noise_var = 1e-3;

% RIS eleman konumlari (lambda/2 aralik, satir oncelikli siralama)
ris_center = [roomSize(1)/2, roomSize(2)/2, 3];
d  = lambda/2;
x0 = ris_center(1) - (M-1)/2*d;
y0 = ris_center(2) - (K-1)/2*d;
elemPos = zeros(N, 3);
idx = 1;
for ii = 1:M
    for jj = 1:K
        elemPos(idx,:) = [x0+(ii-1)*d, y0+(jj-1)*d, ris_center(3)];
        idx = idx + 1;
    end
end

F = complex(zeros(numSamples, N));
G = complex(zeros(numSamples, N));
h_d = complex(zeros(numSamples, 1));
THETA  = zeros(numSamples, N);
TX_pos = zeros(numSamples, 3);
RX_pos = zeros(numSamples, 3);

for s = 1:numSamples
    tx = [rand*roomSize(1), rand*roomSize(2), 1+rand];
    rx = [rand*roomSize(1), rand*roomSize(2), 1+rand];
    TX_pos(s,:) = tx;  RX_pos(s,:) = rx;
    scat_pos = rand(numScatter, 3) .* roomSize;

    d_dir  = norm(tx - rx);
    h_d(s) = (randn+1j*randn)/sqrt(2) * exp(-1j*kwave*d_dir) / d_dir;

    for n = 1:N
        el = elemPos(n,:);
        d_tx = norm(tx - el);
        d_rx = norm(el - rx);
        f0 = (randn+1j*randn)/sqrt(2) * exp(-1j*kwave*d_tx) / d_tx;
        g0 = (randn+1j*randn)/sqrt(2) * exp(-1j*kwave*d_rx) / d_rx;
        fs = 0;  gs = 0;
        for m = 1:numScatter
            da = norm(tx - scat_pos(m,:));  db = norm(scat_pos(m,:) - el);
            dc = norm(el - scat_pos(m,:));  dd = norm(scat_pos(m,:) - rx);
            fs = fs + scatter_g*(randn+1j*randn)/sqrt(2)*exp(-1j*kwave*(da+db))/(da*db);
            gs = gs + scatter_g*(randn+1j*randn)/sqrt(2)*exp(-1j*kwave*(dc+dd))/(dc*dd);
        end
        F(s,n) = f0 + fs;
        G(s,n) = g0 + gs;
    end
    THETA(s,:) = wrapToPi(-angle(F(s,:)) - angle(G(s,:)));   % makaledeki Denklem 8
end

D = struct('F',F,'G',G,'h_d',h_d,'THETA',THETA,'TX_pos',TX_pos,'RX_pos',RX_pos, ...
           'elemPos',elemPos,'N',N,'M',M,'K',K,'numScatter',numScatter, ...
           'roomSize',roomSize,'fc',fc,'Pt',Pt,'noise_var',noise_var,'seed',seed);
end
