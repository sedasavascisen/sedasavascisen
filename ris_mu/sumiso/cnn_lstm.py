"""
The phase-aware CNN-LSTM of Savaşçı Şen et al. (Adv. Intell. Syst. 2026,
doi:10.1002/aisy.70460), ported from the authors' PyTorch code
(train_cnn_lstm.py) with only the number of input channels changed.

  input X [B, C, N] per-element features (published, SISO: C = 4)
  Conv1D(C->64,k=3)+BN+ReLU+Dropout(0.2), Conv1D(64->64,k=3)+BN+ReLU
  LSTM(64->128, 2 layers, dropout 0.2) over the N elements, Linear(128->64)
  flatten (64 N) -> FC256+ReLU+Dropout(0.3) -> FC128+ReLU+Dropout(0.2)
  -> FC64+ReLU -> FC 2N  = (sin, cos) per element
Loss: MSE on (sin, cos) (Eq. 17). Inference: atan2 (Eqs. 12-13).

Multi-antenna BS (MISO): the SISO label -angle(G_n F_n) has its common phase
fixed by convention; for MISO the optimum's common phase is set by the weak
direct link and is close to arbitrary, which a regression network cannot
learn (a first run stayed at the zero predictor, loss 1.0). Labels are
therefore given a canonical common phase (element 1 at zero), and the
common phase is restored after inference in closed form, phi = angle(c^H a)
with c the cascaded channel of the predicted phases (`restore_common_phase`).
"""
import torch
import torch.nn as nn


class PhaseAwareCNNLSTM(nn.Module):
    """head='flat': the authors' PyTorch code (train_cnn_lstm.py).
    head='seq' : the authors' MATLAB code (theta_NN_multioutput.m): Conv+BN+ReLU
                 x2, Dropout(0.2), LSTM(128), LSTM(64), Dropout(0.3), and a
                 per-element FC(64->2) on the sequence output (no flattening)."""
    def __init__(self, c_in, n_elem, head="flat"):
        super().__init__()
        self.n = n_elem
        self.head = head
        if head == "seq":
            self.cnn = nn.Sequential(
                nn.Conv1d(c_in, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
            self.lstm1 = nn.LSTM(64, 128, batch_first=True)
            self.lstm2 = nn.LSTM(128, 64, batch_first=True)
            self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, 2))
            return
        self.cnn = nn.Sequential(
            nn.Conv1d(c_in, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2),
            nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU())
        self.lstm = nn.LSTM(64, 128, num_layers=2, batch_first=True, dropout=0.2)
        self.lstm_proj = nn.Linear(128, 64)
        self.fc = nn.Sequential(
            nn.Linear(64 * n_elem, 256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 2 * n_elem))

    def forward(self, x):
        h = self.cnn(x).transpose(1, 2)
        if self.head == "seq":
            h, _ = self.lstm1(h)
            h, _ = self.lstm2(h)
            return self.out(h)
        h, _ = self.lstm(h)
        h = self.lstm_proj(h)
        return self.fc(h.reshape(h.shape[0], -1)).view(-1, self.n, 2)


def phase(out):
    return torch.atan2(out[..., 0], out[..., 1])


def phase_aware_loss(out, theta):
    return ((out[..., 0] - torch.sin(theta)) ** 2 + (out[..., 1] - torch.cos(theta)) ** 2).mean()


def canonical(theta):
    """Remove the common phase by referencing element 1: theta_n - theta_1.

    (A circular-mean reference was tried first and is unstable: the median
    |mean(exp(j theta))| of the labels is 0.13, so its angle is ill-defined.)
    """
    return torch.angle(torch.exp(1j * (theta - theta[..., :1]).to(torch.complex64)))


def restore_common_phase(theta, a, B):
    """Best common rotation of theta for |a + e^{j phi} B^T v|^2: phi = angle(c^H a)."""
    c = (torch.exp(1j * theta.to(torch.complex64))[..., None] * B).sum(1)
    phi = torch.angle((c.conj() * a).sum(-1, keepdim=True))
    return theta + phi


def features(F, G, hd, kind="cascade"):
    """
    'raw'     : Re/Im g_n, F_n, h_d (broadcast)  -> 2 + 4T channels
    'cascade' : Re/Im b_n = g_n F_n, h_d (broadcast) -> 4T channels.
                The cascaded channel is what RIS channel estimation provides,
                and the published SISO label depends on F, G only via G_n F_n.
    """
    S, N, T = F.shape
    g = G[:, 0, :]
    hdb = hd[:, 0, :][:, None, :].expand(S, N, T)
    if kind == "raw":
        parts = [g.real[..., None], g.imag[..., None], F.real, F.imag, hdb.real, hdb.imag]
    else:
        b = g[..., None] * F
        parts = [b.real, b.imag, hdb.real, hdb.imag]
    return torch.cat(parts, -1).transpose(1, 2).contiguous().float()


def features_ab(a, B):
    """Cascade features from (a [S,T], B [S,N,T]); equals features(..., 'cascade')."""
    S, N, T = B.shape
    ab = a[:, None, :].expand(S, N, T)
    return torch.cat([B.real, B.imag, ab.real, ab.imag], -1).transpose(1, 2).contiguous().float()
