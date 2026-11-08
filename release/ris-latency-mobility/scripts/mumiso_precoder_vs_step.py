"""
Is the fresh-beam assumption cheap? Time the precoder against an Adam step.

The effective rate keeps the BS precoder fresh: at the moment the phase is
applied, regularised ZF is recomputed from the current effective channel.
That is only a fair assumption if computing the precoder is cheap next to
the phase optimisation. This script times, on ONE machine, single thread,
one scenario, median of many repetitions:

    precoder   effective channel + regularised ZF for a given phase
    adam step  one Adam step on the soft-min rate (forward + backward + step)

Only the RATIO is meant to be compared with the paper's latency figures,
which were measured on a different machine. Run on an idle box.
"""
import sys
import time
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
torch.set_num_threads(1)
load0 = float(open("/proc/loadavg").read().split()[0])

panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(64)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
_, TH0 = B.su_average(F, G, hd, pt, nv)
one = slice(0, 1)
th = TH0[one]


def med_ms(fn, reps):
    for _ in range(20):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


def precoder():
    with torch.no_grad():
        He = S.effective_channel(F[one], G[one], hd[one], torch.cos(th), torch.sin(th))
        S.precode(He, pt, "zf", noise_var=nv)


dl = torch.zeros(1, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.75)


def adam_step():
    t = th + dl
    R = S.rates(F[one], G[one], hd[one], torch.cos(t), torch.sin(t), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()


rounds = []
for r in range(5):
    p = med_ms(precoder, 500)
    s = med_ms(adam_step, 200)
    rounds.append(dict(precoder_ms=p, adam_step_ms=s, ratio=s / p))
    print(f"round {r+1}: precoder {p*1e3:7.1f} us   adam step {s*1e3:7.1f} us   "
          f"step/precoder {s/p:5.1f}x", flush=True)
load1 = float(open("/proc/loadavg").read().split()[0])
med = {k: float(np.median([x[k] for x in rounds])) for k in rounds[0]}
print(f"\nmedian: precoder {med['precoder_ms']*1e3:.1f} us, adam step "
      f"{med['adam_step_ms']*1e3:.1f} us, ratio {med['ratio']:.1f}x   "
      f"(load {load0:.2f} -> {load1:.2f})")
json.dump(dict(load_before=load0, load_after=load1, rounds=rounds, median=med,
               N=N, T=8, K=4), open(OUT / "mumiso_precoder_vs_step.json", "w"), indent=1)
print("wrote results/mumiso_precoder_vs_step.json")
