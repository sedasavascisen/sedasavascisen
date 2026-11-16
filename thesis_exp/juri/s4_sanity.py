"""
Consistency check for jury question 4 (numbers quoted in yorum_s4_s2.md): Adam-1 phase (seed 11, 1.5 m/s), rate with
the fresh precoder and with the t = 0 precoder at t in {0, 1.15, 10} ms, and the relative channel change
||G(t) - G(0)||^2 / ||G(0)||^2 (mean over scenarios). -> raw/s4_sanity.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import torch
from common import Aging, commit
from ris_mu.mumiso import system as S
torch.set_num_threads(2)
A = Aging(11, [0.0, 1.15, 10.0]); F, G0, H0 = A.F, A.G[0], A.H[0]
th = A.adam(A.su_average(), 1)
W0 = S.zf(S.effective_channel(F, G0, H0, torch.cos(th), torch.sin(th)), A.pt, noise_var=A.nv)
rows = []
for m, t in enumerate(A.times):
    He = S.effective_channel(F, A.G[m], A.H[m], torch.cos(th), torch.sin(th))
    rows.append(dict(t_ms=t, fresh=float(A.minrate(th, m).mean()), joint=float(torch.log2(1 + S.sinr(He, W0, A.nv)).min(-1).values.mean()),
                     rel_change_G=float(((A.G[m] - G0).abs() ** 2).sum((-1, -2)).div((G0.abs() ** 2).sum((-1, -2))).mean())))
    print(rows[-1], flush=True)
json.dump(dict(commit=commit(), rows=rows), open(pathlib.Path(__file__).parent / "raw/s4_sanity.json", "w"), indent=1)
