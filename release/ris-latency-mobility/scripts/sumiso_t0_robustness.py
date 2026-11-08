"""
Is the ported CNN-LSTM above or below closed-form alignment at t=0, and is it
dominated by one Adam step? Checked on samples larger than the 400-scenario
single-user set, because on 400 scenarios the CNN - SU-alignment difference
is not significant (independent audit, 2026-11-05).

Static (t=0) single-user scenarios, the same generator as the single-user
set, drawn with seeds 11 and 13 at n = 6000 (not the 400-scenario set: the
generator is not prefix-stable). Paired bootstrap, 2000 resamples.
Adam-1 uses the step size selected in results/sumiso_mobility_eval.json.
No timing is involved.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features_ab, restore_common_phase

ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
ev = json.load(open(ROOT / "results" / "sumiso_mobility_eval.json"))
lr1 = ev["adam_lr"]["1"]
ck = torch.load(ROOT / "results" / "sumiso_cnnlstm_seq.pt")
net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck["head"], ck.get("n_out", 2))
net.load_state_dict(ck["state"]); net.eval()
rng = np.random.default_rng(0)


def paired(x, y):
    d = x - y
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    return dict(mean=float(d.mean()), ci95=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                frac_positive=float((d > 0).mean()))


res = dict(adam1_lr=lr1, draws={})
for seed in (11, 13):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,), "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(6000)
    snr = cfg.snr_scale()
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    A, B = SV.cascade(F, torch.as_tensor(d["G_t"][:, 0], dtype=torch.complex64),
                      torch.as_tensor(d["hd_t"][:, 0], dtype=torch.complex64))
    with torch.no_grad():
        th = torch.cat([phase(net((features_ab(A[i:i + 2000], B[i:i + 2000]) - ck["mu"]) / (ck["sd"] + 1e-9)))
                        for i in range(0, len(A), 2000)])
    th_cnn = restore_common_phase(th, A, B)
    th_al = SV.su_align(A, B)
    t = th_al.clone().requires_grad_(True)
    opt = torch.optim.Adam([t], lr=lr1)
    loss = -torch.log2(1 + SV.gain(t, A, B) * snr).sum(); opt.zero_grad(); loss.backward(); opt.step()
    r = lambda x: torch.log2(1 + snr * SV.gain(x, A, B)).detach().numpy()
    R = {"CNN-LSTM": r(th_cnn), "SU-align": r(th_al), "Adam-1": r(t.detach()),
         "CD-1": r(SV.coord_ascent(A, B, th_al, sweeps=1, tol=-1)[0]),
         "CNN-LSTM+CD-1": r(SV.coord_ascent(A, B, th_cnn, sweeps=1, tol=-1)[0])}
    res["draws"][str(seed)] = dict(n=6000, mean={k: float(v.mean()) for k, v in R.items()},
                                   cnn_minus_su_align=paired(R["CNN-LSTM"], R["SU-align"]),
                                   cnn_minus_adam1=paired(R["CNN-LSTM"], R["Adam-1"]),
                                   cnn_cd1_minus_cd1=paired(R["CNN-LSTM+CD-1"], R["CD-1"]))
    print(seed, json.dumps(res["draws"][str(seed)]), flush=True)
json.dump(res, open(ROOT / "results" / "sumiso_t0_robustness.json", "w"), indent=1)
