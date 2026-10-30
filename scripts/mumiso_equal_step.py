"""
The comparison that decides whether the learned update rule earns a chapter.

WHAT WAS WRONG WITH THE EARLIER VERSION
---------------------------------------
`mumiso_budget.py` compares L learned steps against L Adam steps at two
HARDCODED learning rates (0.05 and 0.5). That is not an equal-budget
comparison, it is a comparison against two arbitrary settings. Two separate
unfairnesses, pulling in OPPOSITE directions:

  (a) Against the classical side: the best step size depends on L. At L=1
      the right step is large (one shot at it); at L=32 it is small. Fixing
      lr=0.5 for every L hands the learned model a win at the budgets where
      0.5 happens to be wrong. This project has already made the
      weak-baseline mistake four times; "the learned model beats 32-step
      Adam" is the fifth version of it.

  (b) Against the learned side: the checkpoint was trained with steps=8 and
      then TRUNCATED to L steps. A model trained to deliver its answer on
      step 8 has no reason to be good on step 3 -- its learned step sizes
      are a schedule for 8 steps, not for 3. Judging it at L != 8 judges a
      model nobody trained.

So this script fixes both:

  - the classical arm's step size is swept and chosen on the VALIDATION
    split, then reported on TEST, separately FOR EACH L;
  - the learned arm is a model TRAINED at that same L (one checkpoint per
    budget, written by scripts/mumiso_unrolled.py --steps L).

The two corrections cut in opposite directions, which is the point: the
experiment is not rigged either way, and neither outcome was known when it
was written.

THE UPPER BOUND ON TUNING
-------------------------
A sweep picks one lr for the whole test set. A sceptic can always say a
better schedule exists. So the script also reports PER-SCENARIO ORACLE lr:
for each scenario, the best rate over the whole lr grid, chosen with
knowledge of the answer. No deployable classical method can do better than
that at this budget, so if the learned model beats the oracle column the
claim is safe, and if it loses to the swept column the claim is dead.

WHAT IS HELD EQUAL
------------------
Same scenarios, same anchor (su_average), same objective (max-min via the
stabilised softmin), same precoder (regularised ZF with the MMSE
regulariser), same test split. "L steps" means L objective-and-gradient
evaluations on both sides. What is NOT equal, and is reported rather than
hidden: the learned arm pays a one-off training cost and carries 270k
parameters; the classical arm needs the lr sweep, which is itself a cost
paid offline.
"""
import sys
import pathlib
import json
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=6000,
                help="MUST match the training runs, or the draw differs")
ap.add_argument("--budgets", default="1,2,4,8,16")
ap.add_argument("--ckpt-fmt", default="results/mumiso_eqstep_L{L}.pt")
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--val-n", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--lrs", default="0.02,0.05,0.1,0.2,0.35,0.5,0.75,1.0,1.5,2.0")
ap.add_argument("--ref-n", type=int, default=300,
                help="scenarios for the unbudgeted classical references")
ap.add_argument("--tag", default="equal_step")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
BUDGETS = [int(x) for x in a.budgets.split(",")]
LRS = [float(x) for x in a.lrs.split(",")]


def say(*m):
    print(*m, flush=True)


torch.manual_seed(a.seed)
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(a.samples, seed=0)
_, TH0 = B.su_average(F, G, hd, pt, nv)

ev = te[:a.eval_n]          # test:       what every number below is reported on
vv = va[:a.val_n]           # validation: what the lr is chosen on
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}")
say(f"test {len(ev)} scenarios (reporting)  |  val {len(vv)} (lr choice)")


def rate(th, ids):
    """Mean over scenarios of the per-scenario WORST user rate (max-min)."""
    R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                pt, nv, "zf")
    return R.min(-1).values


def adam_steps(ids, L, lr, obj="soft"):
    """
    L Adam steps on the phase offset from the su_average anchor.

    THE ASCENT OBJECTIVE IS ALSO A TUNING KNOB, so it is swept, not chosen.
    Two reasonable choices and no a-priori winner at small L:

      "soft"  the stabilised softmin (beta = 8), what the learned model
              trains on. Spreads gradient over all users; the naive
              -log(sum(exp(-beta R)))/beta form overflows in float32 once
              R reaches about 16 b/s/Hz, hence the logsumexp shift.
      "hard"  the true min, what `baselines._pga_from` uses and what every
              number is REPORTED on. Hands the gradient to one user per
              scenario.

    An earlier version of this script hardcoded "soft" -- which quietly
    handicapped the classical arm with the learned model's own objective
    while the package's own PGA uses "hard". Picking one by hand is the
    weak-baseline mistake wearing a different hat, so both are swept on
    validation alongside the step size and the better one is reported.
    """
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        if obj == "soft":
            loss = -(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
        else:
            loss = -R.min(-1).values.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


res = dict(config=vars(a), anchor=rate(TH0[ev], ev).mean().item(), rows={})
say(f"\nanchor (su_average) on test : {res['anchor']:.4f}")
R_b, TH_b = B.su_best_of(F[ev], G[ev], hd[ev], pt, nv)
res["su_best_of"] = S.rate_metrics(R_b)["min_rate"]
say(f"su_best_of (free, 0 steps)  : {res['su_best_of']:.4f}")

# ----------------------------------------------------------- the comparison
say(f"\n=== equal step budget: learned(L) vs best-tuned Adam(L) ===")
say(f"{'L':>3} {'learned':>9} {'Adam swept':>11} {'(lr/obj)':>11} "
    f"{'Adam oracle':>12} {'L/swept':>9} {'L/oracle':>9}")
say("-" * 71)

OBJS = ("soft", "hard")

for L in BUDGETS:
    # ---- classical arm: (lr, objective) chosen on VALIDATION, reported
    #      on TEST. Both knobs swept; see adam_steps for why the objective
    #      is a knob and not a constant.
    val_scores = {}
    for ob in OBJS:
        for lr in LRS:
            val_scores[(lr, ob)] = rate(adam_steps(vv, L, lr, ob),
                                        vv).mean().item()
    best_lr, best_ob = max(val_scores, key=val_scores.get)
    swept = rate(adam_steps(ev, L, best_lr, best_ob), ev)

    # ---- the upper bound on tuning: best (lr, objective) PER SCENARIO,
    #      chosen on TEST with knowledge of the answer. No deployable
    #      classical method can beat this at this budget.
    per_cfg = torch.stack([rate(adam_steps(ev, L, lr, ob), ev)
                           for ob in OBJS for lr in LRS])
    oracle = per_cfg.max(0).values

    # ---- learned arm: a model TRAINED at this L
    ck = pathlib.Path(a.ckpt_fmt.format(L=L))
    if not ck.exists():
        say(f"{L:3d} {'(ckpt yok)':>9} {swept.mean().item():11.4f} "
            f"{best_lr:6.2f}/{best_ob:4} {oracle.mean().item():12.4f}")
        res["rows"][L] = dict(learned=None, swept=swept.mean().item(),
                              best_lr=best_lr, best_obj=best_ob,
                              oracle=oracle.mean().item(),
                              val_curve={f"{k[0]}|{k[1]}": v
                                         for k, v in val_scores.items()})
        continue
    net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=L,
                         mode=a.mode, use_grad=True)
    net.load_state_dict(torch.load(ck))
    net.eval()
    with torch.no_grad():
        th_l = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
    th_l = th_l[0] if isinstance(th_l, tuple) else th_l
    learned = rate(th_l, ev)

    # paired difference: the same scenarios, so report the spread of the
    # DIFFERENCE rather than two independent means
    dif = (learned - swept)
    res["rows"][L] = dict(
        learned=learned.mean().item(), swept=swept.mean().item(),
        best_lr=best_lr, best_obj=best_ob, oracle=oracle.mean().item(),
        learned_over_swept=(learned.mean() / swept.mean()).item(),
        learned_over_oracle=(learned.mean() / oracle.mean()).item(),
        paired_mean_diff=dif.mean().item(),
        paired_sem=(dif.std(unbiased=True) / len(dif) ** 0.5).item(),
        learned_wins_frac=(dif > 0).float().mean().item(),
        val_curve={f"{k[0]}|{k[1]}": v for k, v in val_scores.items()})
    r = res["rows"][L]
    say(f"{L:3d} {r['learned']:9.4f} {r['swept']:11.4f} "
        f"{best_lr:6.2f}/{best_ob:4} {r['oracle']:12.4f} "
        f"{r['learned_over_swept']:9.3f} {r['learned_over_oracle']:9.3f}")

# ------------------------------------------------- unbudgeted references
say(f"\n=== unbudgeted classical, same channel, {a.ref_n} scenarios ===")
rf = te[:a.ref_n]
for nm in ("cd", "pga", "ao"):
    R, _ = B._DISPATCH[nm](F[rf], G[rf], hd[rf], pt, nv, precoder="zf")
    res[nm] = S.rate_metrics(R)["min_rate"]
    say(f"  {nm:>4} : {res[nm]:.4f}")

# ------------------------------------------------------------- the verdict
say("\n=== verdict ===")
rows = {L: v for L, v in res["rows"].items() if v.get("learned") is not None}
if not rows:
    say("  no learned checkpoints found -- train them first")
else:
    beats_swept = [L for L, v in rows.items()
                   if v["paired_mean_diff"] - 2 * v["paired_sem"] > 0]
    loses_swept = [L for L, v in rows.items()
                   if v["paired_mean_diff"] + 2 * v["paired_sem"] < 0]
    tied = [L for L in rows if L not in beats_swept and L not in loses_swept]
    say(f"  budgets where learned BEATS tuned Adam (2 s.e.) : {beats_swept}")
    say(f"  budgets where learned LOSES  (2 s.e.)           : {loses_swept}")
    say(f"  statistically tied                              : {tied}")
    res["verdict"] = dict(beats=beats_swept, loses=loses_swept, tied=tied)
    say("\n  Read it straight: a learned update rule that does not beat the")
    say("  best-tuned classical step at ANY equal budget has no latency")
    say("  argument left, because the tuning is paid offline, once.")

(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
