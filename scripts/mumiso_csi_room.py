"""
Is there room for a robust learner under imperfect CSI?

Before spending a training run on the hypothesis "a learned model is robust
to CSI error where a classical optimiser overfits it", measure whether the
room exists at all. Three things decide it:

  1. Does the achievable rate collapse with error? If a classical optimiser
     at its best setting still gets most of the perfect-CSI rate, nothing
     is left to win.
  2. Does the OPTIMAL number of gradient steps shrink as error grows? That
     is the signature of overfitting the estimate, and it is what a robust
     method would exploit.
  3. How big is the gap between optimising on the estimate and the
     unreachable oracle that optimises on the truth? That gap is the
     ceiling on any robustness gain.

If (1) and (2) say no, the hypothesis is dead and the training run is not
worth it. Reporting that is a result too.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.csi import add_error, rates_mismatched, db_to_e2

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--levels", default="None,-20,-15,-10,-5,0")
ap.add_argument("--steps", default="0,2,4,8,16,32,64")
ap.add_argument("--tag", default="csi_room")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.scenarios)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()

LEVELS = [None if x.strip() == "None" else float(x) for x in a.levels.split(",")]
STEPS = [int(x) for x in a.steps.split(",")]

say(f"N={N} T={a.tx} K={a.users}  {a.scenarios} scenarios")
say("phase AND precoder from the estimate; rate evaluated with the truth\n")


def adam_phase(Fe, Ge, He, start, L):
    """Optimise on whatever channel it is handed."""
    if L == 0:
        return start
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(Fe, Ge, He, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


res = {"levels": [], "steps": STEPS}
say(f"{'error':>8}" + "".join(f"{'L='+str(L):>9}" for L in STEPS)
    + f"{'best L':>8}{'oracle':>9}{'gap':>7}")
say("-" * (8 + 9 * len(STEPS) + 24))

for db in LEVELS:
    e2 = db_to_e2(db)
    Fe, Ge, He = add_error(F, G, hd, e2, seed=7)
    _, start = B.su_best_of(Fe, Ge, He, pt, nv)      # anchor from the estimate
    row, best = [], (-1, -np.inf)
    for L in STEPS:
        th = adam_phase(Fe, Ge, He, start, L)
        r = rates_mismatched(F, G, hd, Fe, Ge, He, torch.cos(th),
                             torch.sin(th), pt, nv).min(-1).values.mean().item()
        row.append(r)
        if r > best[1]:
            best = (L, r)
    # the unreachable oracle: optimise AND precode on the truth, 32 steps
    _, st_true = B.su_best_of(F, G, hd, pt, nv)
    th_o = adam_phase(F, G, hd, st_true, 32)
    orc = S.rates(F, G, hd, torch.cos(th_o), torch.sin(th_o), pt, nv,
                  "zf").min(-1).values.mean().item()
    lab = "perfect" if db is None else f"{db:.0f} dB"
    say(f"{lab:>8}" + "".join(f"{v:9.3f}" for v in row)
        + f"{best[0]:8d}{orc:9.3f}{best[1]/orc:7.2f}")
    res["levels"].append(dict(db=db, e2=e2, rates=row, best_L=best[0],
                              best_rate=best[1], oracle=orc,
                              frac_of_oracle=best[1] / orc))

say("")
say("=== reading ===")
bl = [r["best_L"] for r in res["levels"]]
fr = [r["frac_of_oracle"] for r in res["levels"]]
say(f"  best step count across error levels : {bl}")
shrinks = bl[-1] < bl[0]
say(f"  does the optimal step count shrink with error : {shrinks}")
say(f"  best achievable / oracle            : "
    + " ".join(f"{v:.2f}" for v in fr))
room = (1.0 - min(fr)) > 0.10
say(f"  is there >10% left on the table at the worst level : {room}")
if shrinks and room:
    say("  -> the hypothesis has room. A model trained ACROSS error")
    say("     realisations could plausibly recover part of that gap.")
else:
    say("  -> the hypothesis has little room here. Say so and move on;")
    say("     a training run would be spent confirming a null result.")

json.dump(res, open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
