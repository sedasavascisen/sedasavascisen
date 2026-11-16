"""
Single-pass phase network for jury question 5. Input: a 3D tensor per scenario on the panel grid
[C = 72, 8, 4] (rows x columns of the 32-element RIS):
  - 8 channels: Re/Im of the single-user alignment terms a_{k,n} = g_{k,n} (f_n^H u_k), u_k = h_d,k/||h_d,k|| (K = 4),
    each user normalised by its rms over n;
  - 64 channels: Re/Im of the cascade g_{k,n} f_{n,t} (K = 4 users x T = 8 antennas), normalised by the scenario rms.
Body: 3 x [Conv3x3 -> ReLU] + global-context (mean-pooled features broadcast and concatenated) -> Conv1x1.
Heads: "sincos" (2 outputs, L2-normalised, theta = atan2(sin, cos)) or "angle" (1 output, theta = pi * tanh(x)).
Trained without labels on the soft-min (beta = 8) user rate with fresh regularised ZF, as in Paper 2.
"""
import torch, torch.nn as nn

ROWS, COLS = 8, 4                       # panel grid; element index n = r * COLS + c (verified against RISPanel.positions)


def features(F, G, H):
    """F [S,N,T], G [S,K,N], H [S,K,T] (complex) -> [S, 72, 8, 4] float."""
    nrm = torch.linalg.norm(H, dim=-1, keepdim=True).clamp_min(1e-30)
    u = H / nrm
    proj = torch.einsum("bnt,bkt->bkn", F, u.conj())
    a = G * proj                                                       # [S,K,N]
    a = a / (a.abs().pow(2).mean(-1, keepdim=True).sqrt().clamp_min(1e-30))
    C = G.unsqueeze(-1) * F.unsqueeze(1)                               # [S,K,N,T]
    C = C / (C.abs().pow(2).mean((1, 2, 3), keepdim=True).sqrt().clamp_min(1e-30))
    S_, K, N, T = C.shape
    C = C.permute(0, 1, 3, 2).reshape(S_, K * T, N)                    # [S,KT,N]
    x = torch.cat([a.real, a.imag, C.real, C.imag], 1)                 # [S, 2K + 2KT, N]
    return x.reshape(S_, x.shape[1], ROWS, COLS).float()


class PhaseNet(nn.Module):
    def __init__(self, head="sincos", cin=72, w=64):
        super().__init__()
        self.head = head
        self.body = nn.Sequential(nn.Conv2d(cin, w, 3, padding=1), nn.ReLU(), nn.Conv2d(w, w, 3, padding=1), nn.ReLU(),
                                  nn.Conv2d(w, w, 3, padding=1), nn.ReLU())
        self.out = nn.Conv2d(2 * w, 2 if head == "sincos" else 1, 1)

    def forward(self, x):
        h = self.body(x)
        g = h.mean((2, 3), keepdim=True).expand_as(h)
        o = self.out(torch.cat([h, g], 1)).flatten(2)                    # [S, 1|2, N]
        if self.head == "sincos":
            o = o / o.norm(dim=1, keepdim=True).clamp_min(1e-12)
            return torch.atan2(o[:, 0], o[:, 1])
        return torch.pi * torch.tanh(o[:, 0])
