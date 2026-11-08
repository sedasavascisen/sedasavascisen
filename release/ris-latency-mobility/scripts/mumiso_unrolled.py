"""
Does learning the UPDATE RULE work where learning the solution does not?

Trains the unrolled model on the final rate and compares against the anchor
it starts from and the strong classical baseline it is trying to approach.
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
from ris_mu.mumiso.unrolled import UnrolledMuMiso, count_params
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=8000)
ap.add_argument("--epochs", type=int, default=25)
ap.add_argument("--steps", type=int, default=6)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--use-grad", action="store_true")
ap.add_argument("--bs", type=int, default=32)
ap.add_argument("--lr", type=float, default=1e-3)
ap.add_argument("--baseline-n", type=int, default=600)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="unrolled")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)


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
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}  steps={a.steps}  "
    f"mode={a.mode}  use_grad={a.use_grad}")

# anchor the unrolling starts from
_, TH0 = B.su_average(F, G, hd, pt, nv)


def mr(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th),
                   pt, nv, "zf").min(-1).values.mean().item()


bte = te[:a.baseline_n]
say(f"\nanchor su_average on test : {mr(TH0[te], te):.4f}")
t0 = time.time()
R_ao, _ = B.ao(F[bte], G[bte], hd[bte], pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
R_cd, _ = B.coord_descent(F[bte], G[bte], hd[bte], pt, nv)
cd = S.rate_metrics(R_cd)["min_rate"]
say(f"coord descent on {len(bte)}    : {cd:.4f}")
say(f"AO (strong) on {len(bte)}      : {ao:.4f}   ({time.time()-t0:.0f}s)")

net = UnrolledMuMiso(N=N, n_users=a.users, n_tx=a.tx, steps=a.steps,
                     mode=a.mode, use_grad=a.use_grad)
say(f"\nparameters: {count_params(net)}")


def run_eval(ids, bs=256, trace=False):
    net.eval()
    tot_min = tot_sum = 0.0
    tr_acc = None
    with torch.no_grad():
        for i in range(0, len(ids), bs):
            j = ids[i:i + bs]
            out = net(X[j], F[j], G[j], hd[j], pt, nv, TH0[j],
                      return_trace=trace)
            th, tc = out if trace else (out, None)
            R = S.rates(F[j], G[j], hd[j], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            tot_min += R.min(-1).values.sum().item()
            tot_sum += R.sum(-1).sum().item()
            if trace:
                tr_acc = np.array(tc) * len(j) if tr_acc is None \
                    else tr_acc + np.array(tc) * len(j)
    out = (tot_min / len(ids), tot_sum / len(ids))
    return out + ((tr_acc / len(ids),) if trace else ())


say(f"before training, val min : {run_eval(va[:500])[0]:.4f}  "
    f"(should sit at the anchor)")

opt = torch.optim.Adam(net.parameters(), lr=a.lr)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.epochs)
rng = np.random.default_rng(a.seed)
best, best_state, hist = -np.inf, None, []
for ep in range(1, a.epochs + 1):
    net.train()
    t0, run, nb = time.time(), 0.0, 0
    perm = tr[rng.permutation(len(tr))]
    for i in range(0, len(perm), a.bs):
        j = perm[i:i + a.bs]
        th = net(X[j], F[j], G[j], hd[j], pt, nv, TH0[j])
        R = S.rates(F[j], G[j], hd[j], torch.cos(th), torch.sin(th), pt, nv,
                    "zf")
        loss = S.maxmin_loss(R)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        run += loss.item()
        nb += 1
    sched.step()
    v_min, v_sum = run_eval(va[:500])
    hist.append(dict(epoch=ep, loss=run / nb, val_min=v_min, val_sum=v_sum))
    mark = ""
    if v_min > best:
        best = v_min
        best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
        mark = "  *"
    say(f"  epoch {ep:3d}/{a.epochs}  loss {run/nb:8.4f}  val min {v_min:7.4f}"
        f"  sum {v_sum:8.3f}  ({time.time()-t0:.0f}s){mark}")

if best_state is not None:
    net.load_state_dict(best_state)

t_min, t_sum, trace = run_eval(te, trace=True)
say(f"\nTEST  min {t_min:.4f}  sum {t_sum:.3f}")
say(f"  anchor {mr(TH0[te], te):.4f}   cd {cd:.4f}   AO {ao:.4f}")
say(f"  fraction of AO : {t_min/ao:.3f}")
say("  per-step min rate: " + " -> ".join(f"{v:.3f}" for v in trace))
say("  learned step sizes: "
    + " ".join(f"{v:.3f}" for v in torch.exp(net.log_step).detach().tolist()))

res = dict(config=vars(a), anchor=mr(TH0[te], te), cd=cd, ao=ao,
           test_min=t_min, test_sum=t_sum, frac_of_ao=t_min / ao,
           per_step=[float(v) for v in trace], history=hist,
           params=count_params(net))
with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
torch.save(net.state_dict(), OUT / f"mumiso_{a.tag}.pt")
say(f"\nwrote results/mumiso_{a.tag}.json")
