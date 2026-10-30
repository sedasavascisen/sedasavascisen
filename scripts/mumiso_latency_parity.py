"""
The comparison the thesis claim actually needs: EQUAL WALL CLOCK.

WHY THE EQUAL-STEP RESULT IS NOT ENOUGH
---------------------------------------
`mumiso_equal_step.py` gives the learned update rule L steps and gives
tuned Adam L steps, and the learned rule wins at every L (1.011x to 1.052x,
paired lower bound positive at all five budgets). That is a real result, but
it is NOT the thesis claim, because a learned step and an Adam step do not
cost the same.

Measured, single scenario, one thread, IDLE MACHINE, median over 5
independent rounds (results/mumiso_latency_repeat.json):

        L      Adam [ms]   learned [ms]   ratio
        1         2.54          6.71      2.64x
        2         4.48         14.59      3.26x
        4         9.30         25.79      2.77x
        8        17.48         52.34      2.99x
       16        36.62         99.15      2.71x

(An earlier table here came from a run taken while training was going and
had Adam L=8 at 29.70 ms instead of 17.48 -- see the dominance block at the
bottom for what that did to the verdict.)

A learned step costs about 3x an Adam step, and the reason is structural,
not an implementation detail: per step the learned rule evaluates `rates`
once for the bottleneck signal, once more forward-and-backward for the
gradient channel, and then runs the CNN+LSTM body (K times in `exchange`
mode). Adam does the forward-and-backward only.

So "equal L" silently hands the learned arm three times the compute. The
honest axis is milliseconds, and on that axis the classical arm gets
roughly three times as many steps for the same budget. This script asks
whether the step-parity win survives that -- and if it does not, says so.

WHAT IS MEASURED
----------------
Rate on the same 600-scenario test split as the equal-step run, for:
  - the learned model at each L it was trained for;
  - tuned Adam at a RANGE of L extending well past the learned budgets,
    with (step size x ascent objective) swept on validation at every L.
Latency for both, single scenario, one thread, median of many repeats, on a
machine checked for load. Then the Pareto frontier of (latency, rate) and
which arm is on it.

A result either way is publishable. A learned optimiser that wins per step
and loses per millisecond is a negative result about deployment, and it is
the one the mobility chapter needs to hear, because there the budget is
milliseconds against a 28.2 ms coherence time.
"""
import sys
import pathlib
import json
import time
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
ap.add_argument("--samples", type=int, default=6000)
ap.add_argument("--learned-budgets", default="1,2,4,8,16")
ap.add_argument("--classical-budgets", default="1,2,4,8,16,24,32,48,64")
ap.add_argument("--ckpt-fmt", default="results/mumiso_eqstep_L{L}.pt")
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--val-n", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--lrs", default="0.2,0.35,0.5,0.75,1.0,1.5")
ap.add_argument("--reps", type=int, default=40, help="timing repeats")
ap.add_argument("--max-load", type=float, default=1.5)
ap.add_argument("--tag", default="latency_parity")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
LB = [int(x) for x in a.learned_budgets.split(",")]
CB = [int(x) for x in a.classical_budgets.split(",")]
LRS = [float(x) for x in a.lrs.split(",")]
OBJS = ("soft", "hard")


def say(*m):
    print(*m, flush=True)


load0 = float(open("/proc/loadavg").read().split()[0])
say(f"load before: {load0:.2f}")
if load0 > a.max_load:
    say(f"  WARNING: machine is busy (>{a.max_load}); latencies will be "
        f"inflated and the frontier may flip. Treat timings as unusable.")

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
ev, vv = te[:a.eval_n], va[:a.val_n]
say(f"N={N} T={a.tx} K={a.users}  test {len(ev)}  val {len(vv)}")


def rate(th, ids):
    R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                pt, nv, "zf")
    return R.min(-1).values


def adam_steps(ids, L, lr, obj):
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        R = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                    pt, nv, "zf")
        loss = (-(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
                if obj == "soft" else -R.min(-1).values.mean())
        opt.zero_grad()
        loss.backward()
        opt.step()
    return TH0[ids] + dl.detach()


# ------------------------------------------------------------------ timing
one = slice(0, 1)
_nthreads = torch.get_num_threads()
torch.set_num_threads(1)          # a deployed RIS controller is not a cluster


def time_adam(L, lr, obj):
    ts = []
    for _ in range(a.reps):
        t0 = time.perf_counter()
        dl = torch.zeros(1, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = TH0[one] + dl
            R = S.rates(F[one], G[one], hd[one], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            loss = (-(-torch.logsumexp(-8.0 * R, dim=-1) / 8.0).mean()
                    if obj == "soft" else -R.min(-1).values.mean())
            opt.zero_grad()
            loss.backward()
            opt.step()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


def time_learned(net):
    with torch.no_grad():
        for _ in range(3):
            net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])
    ts = []
    for _ in range(a.reps):
        t0 = time.perf_counter()
        with torch.no_grad():
            net(X[one], F[one], G[one], hd[one], pt, nv, TH0[one])
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts) * 1e3)


res = dict(config=vars(a), load_before=load0,
           anchor=rate(TH0[ev], ev).mean().item(), learned={}, classical={})
R_b, _ = B.su_best_of(F[ev], G[ev], hd[ev], pt, nv)
res["su_best_of"] = S.rate_metrics(R_b)["min_rate"]
say(f"\nanchor {res['anchor']:.4f}   su_best_of {res['su_best_of']:.4f}")

# ------------------------------------------------------- the learned arm
say(f"\n=== learned arm ===")
say(f"{'L':>3}{'rate':>9}{'latency [ms]':>14}")
for L in LB:
    ck = pathlib.Path(a.ckpt_fmt.format(L=L))
    if not ck.exists():
        say(f"{L:3d}   (ckpt yok)")
        continue
    net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=L,
                         mode=a.mode, use_grad=True)
    net.load_state_dict(torch.load(ck))
    net.eval()
    with torch.no_grad():
        th = net(X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
    th = th[0] if isinstance(th, tuple) else th
    r = rate(th, ev)
    ms = time_learned(net)
    res["learned"][L] = dict(rate=r.mean().item(), ms=ms,
                             per_scenario=r.tolist())
    say(f"{L:3d}{r.mean().item():9.4f}{ms:14.3f}")

# ----------------------------------------------------- the classical arm
say(f"\n=== classical arm: (lr x objective) swept on validation at each L ===")
say(f"{'L':>3}{'rate':>9}{'latency [ms]':>14}{'lr/obj':>12}")
for L in CB:
    best, bl, bo = -np.inf, None, None
    for ob in OBJS:
        for lr in LRS:
            v = rate(adam_steps(vv, L, lr, ob), vv).mean().item()
            if v > best:
                best, bl, bo = v, lr, ob
    r = rate(adam_steps(ev, L, bl, bo), ev)
    ms = time_adam(L, bl, bo)
    res["classical"][L] = dict(rate=r.mean().item(), ms=ms, lr=bl, obj=bo,
                               per_scenario=r.tolist())
    say(f"{L:3d}{r.mean().item():9.4f}{ms:14.3f}{bl:9.2f}/{bo:4}")

torch.set_num_threads(_nthreads)

# ----------------------------------------------------------- the frontier
# DOMINANCE, NOT INTERPOLATION. The first version of this block compared
# the learned rate against Adam's curve linearly interpolated at the same
# millisecond. That is wrong in a direction that matters: the rate-latency
# curve is CONCAVE (diminishing returns per step), so a straight line
# between two measured Adam points lies BELOW the true curve, which
# understates Adam and flatters the learned arm. On the 23 Oct run that
# artefact is what let learned L=4 appear to survive on the frontier.
#
# A learned point is dominated when some measured Adam setting is BOTH
# no slower AND no worse. That needs no interpolation and no assumption
# about the curve's shape.
say(f"\n=== dominance: is some Adam setting both FASTER and BETTER? ===")
say(f"{'learned L':>10}{'ms':>9}{'rate':>10}   {'dominated by':<30}{'verdict':>14}")
verdict = {}
for L, v in sorted(res["learned"].items()):
    ms, r = v["ms"], v["rate"]
    cands = [(k, c) for k, c in res["classical"].items()
             if c["ms"] <= ms and c["rate"] >= r]
    if cands:
        k, c = max(cands, key=lambda kc: kc[1]["rate"])
        txt = f"L={k}: {c['ms']:.1f} ms, {c['rate']:.4f}"
        verdict[L] = dict(ms=ms, learned=r, dominated=True,
                          by=dict(L=k, ms=c["ms"], rate=c["rate"]))
        say(f"{L:10d}{ms:9.1f}{r:10.4f}   {txt:<30}{'DOMINATED':>14}")
    else:
        faster = [c for c in res["classical"].values() if c["ms"] <= ms]
        bf = max(faster, key=lambda c: c["rate"])["rate"] if faster else None
        txt = f"best faster Adam: {bf:.4f}" if bf else "-"
        verdict[L] = dict(ms=ms, learned=r, dominated=False)
        say(f"{L:10d}{ms:9.1f}{r:10.4f}   {txt:<30}{'ON FRONTIER':>14}")
res["latency_verdict"] = verdict

loses = [L for L, v in verdict.items() if v["dominated"]]
wins = [L for L, v in verdict.items() if not v["dominated"]]
say(f"\n  learned on the frontier at: {wins}")
say(f"  strictly dominated at     : {loses}")
say(f"\n  Timings are only as good as the machine was quiet. Measured on an"
    f"\n  idle box over 5 independent rounds, round-to-round spread is"
    f"\n  1.06x-1.41x and all five learned points are dominated in 5/5"
    f"\n  rounds (results/mumiso_latency_repeat.json). A run taken while"
    f"\n  training was going inflated Adam L=8 from 17.5 ms to 29.7 ms and"
    f"\n  flipped one row -- contamination is not neutral, it favours"
    f"\n  whichever arm it slows down less.")
say("\n  Equal STEPS said the learned rule wins at every budget. Equal")
say("  MILLISECONDS is the axis the thesis claim lives on, because the")
say("  coherence time is 28.2 ms and not 28.2 steps. Report whichever")
say("  this table says, and report that the two axes disagree if they do.")

(OUT / f"mumiso_{a.tag}.json").write_text(json.dumps(res, indent=1))
say(f"\nwrote results/mumiso_{a.tag}.json")
