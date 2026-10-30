"""
The assumption Chapter 5 rests on: the beamformer stays fresh.

WHY THIS FILE EXISTS
--------------------
Every mobility number in this package holds the PHASE fixed from t=0 and
evaluates it on the channel at t=tau, while the beamformer W is recomputed
from the channel that exists at t=tau. That split -- "phase ages, beam does
not" -- is a modelling choice, and it is the single assumption the whole
chapter leans on.

Its size was quoted as "17x at 28.2 ms (4.718 against 0.279)" in the
chapter draft, the advisor assessment and the writing reference. That
number was measured once, inline, and never written to a script. This
project has already been bitten by exactly that: an earlier report's
"95% in budget" column came from an unsaved one-liner, an audit measured
85-90% instead, and nobody could rerun the original. The rule that came out
of it is in `mumiso_budget_fraction.py`:

    A number that carries a conclusion and has no script behind it is not
    a measurement.

So this script measures it properly, and whatever it prints replaces the
quoted figure.

WHAT IS COMPARED
----------------
One phase configuration chosen at t = 0, then at each later time:

    fresh beam   W from the TRUE channel at t = tau, phase from t = 0
    stale beam   W from the channel at t = 0,        phase from t = 0

Both are evaluated on the true channel at t = tau. The gap between them is
the cost of letting the beamformer age at the same rate as the surface.

The physical argument for the split is that the two are updated by
different machinery at different cost: W is a digital computation at the
base station, refreshed per frame from pilots; theta needs the joint
optimisation of N passive elements, which is what the latency column
measures. This script does not defend that argument -- it prices it.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileMuMisoChannel, MobileConfig
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--phase", default="su_best_of",
                choices=("su_average", "su_best_of", "adam8"))
ap.add_argument("--tag", default="beam_staleness")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
TIMES = (0.0, 5.0, 10.0, 20.0, 28.2, 50.0, 100.0, 200.0)


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, _ = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                seed=a.seed)
cfg = MobileConfig(n_users=a.users, n_bs_antennas=a.tx, seed=a.seed,
                   velocity=a.velocity, times_ms=TIMES)
d = MobileMuMisoChannel(panel, cfg).generate(a.scenarios, chunk=200)

F = torch.as_tensor(d["F"], dtype=torch.complex64)
G_t = torch.as_tensor(d["G_t"], dtype=torch.complex64)      # [S,M,K,N]
H_t = torch.as_tensor(d["hd_t"], dtype=torch.complex64)     # [S,M,K,T]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
G0, H0 = G_t[:, 0], H_t[:, 0]
say(f"N={F.shape[1]} T={a.tx} K={a.users}  {a.scenarios} scenarios  "
    f"v={a.velocity} m/s  phase={a.phase}")

# ---- the phase, chosen once at t = 0 -----------------------------------
if a.phase == "adam8":
    _, th0 = B.su_average(F, G0, H0, pt, nv)
    dl = torch.zeros_like(th0, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for _ in range(8):
        th = th0 + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    theta = (th0 + dl.detach())
else:
    _, theta = B._DISPATCH[a.phase](F, G0, H0, pt, nv, precoder="zf")

cos_t, sin_t = torch.cos(theta), torch.sin(theta)

# W computed ONCE at t = 0, then frozen -- the stale arm
He0 = S.effective_channel(F, G0, H0, cos_t, sin_t)
W_stale = S.precode(He0, pt, "zf", noise_var=nv)


def min_rate(He, W):
    return torch.log2(1.0 + S.sinr(He, W, nv)).min(-1).values.mean().item()


say(f"\n{'t [ms]':>8}{'fresh beam':>13}{'stale beam':>13}{'ratio':>9}")
say("-" * 43)
rows = []
for m, t in enumerate(TIMES):
    He = S.effective_channel(F, G_t[:, m], H_t[:, m], cos_t, sin_t)
    W_fresh = S.precode(He, pt, "zf", noise_var=nv)
    fr, st = min_rate(He, W_fresh), min_rate(He, W_stale)
    rows.append(dict(t_ms=t, fresh=fr, stale=st,
                     ratio=(fr / st if st > 1e-9 else float("inf"))))
    say(f"{t:8.1f}{fr:13.4f}{st:13.4f}{rows[-1]['ratio']:9.1f}x")

tc = next(r for r in rows if abs(r["t_ms"] - 28.2) < 1e-6)
say(f"\nAt the coherence time (28.2 ms): fresh {tc['fresh']:.4f}, "
    f"stale {tc['stale']:.4f}  ->  {tc['ratio']:.1f}x")
say("\nRead it straight: this is the price of the chapter's assumption, not")
say("evidence for it. If a deployment cannot refresh W faster than theta,")
say("the chapter's method ranking does not transfer -- every method")
say("collapses together and the discriminator is beam latency, not phase")
say("latency. That belongs in the chapter's limitations, stated with this")
say("number.")

res = dict(config=vars(a), times_ms=list(TIMES), rows=rows,
           at_coherence=tc)
(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
