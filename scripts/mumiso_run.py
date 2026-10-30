"""
Full MU-MISO experiment: dataset, baselines, three architectures,
permutation test, quantisation. Writes results/mumiso_*.json
"""
import sys, pathlib, json, time, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank, neighbour_corr)
from ris_mu.mumiso.features import mumiso_features, n_channels
from ris_mu.mumiso.models import MuMisoNet, count_params, MODES
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.train import train_model, evaluate
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=12000)
ap.add_argument("--epochs", type=int, default=30)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--M", type=int, default=8)
ap.add_argument("--K", type=int, default=4)
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--tag", default="main")
ap.add_argument("--no-residual", action="store_true",
                help="predict absolute phase instead of a rotation on the "
                     "su_average anchor (ablation)")
ap.add_argument("--link-ratio", action="store_true",
                help="append the two link-scale channels the "
                     "normalisation removes (features.link_ratio); C goes "
                     "from 5+4T to 7+4T, so a run with this flag is NOT "
                     "comparable to a checkpoint without it")
ap.add_argument("--baseline-n", type=int, default=1200,
                help="test scenarios used for the classical baselines; AO "
                     "runs 3 starts x 400 Adam steps and is the slow part")
a = ap.parse_args()

OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)
res = dict(config=vars(a))
t_all = time.time()

def say(*m): print(*m, flush=True)

# ---------------------------------------------------------------- dataset
say(f"=== dataset: {a.samples} scenarios, T={a.tx}, K={a.users} ===")
panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx,
                                  M=a.M, K=a.K, seed=a.seed)
N = panel.positions.shape[0]
t0 = time.time()
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, rdt = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
say(f"  N={N} C={n_channels(a.tx, a.link_ratio)}  "
    f"link_ratio={a.link_ratio}  generated in {time.time()-t0:.1f}s")

phi = S.su_align_phase(F, G, hd).numpy()
t0 = time.time()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi,
                                     link_ratio=a.link_ratio))
say(f"  features {tuple(X.shape)}  {X.element_size()*X.nelement()/1e6:.0f} MB"
    f"  in {time.time()-t0:.1f}s")

res["channel"] = dict(
    N=N, n_channels=n_channels(a.tx, a.link_ratio),
    snr_scale=cfg.snr_scale(),
    g_rank_pooled=effective_rank(d["G"].reshape(-1, N)),
    g_rank_user0=effective_rank(d["G"][:, 0]),
    f_rank_ant0=effective_rank(d["F"][:, :, 0]),
    g_neigh_corr=neighbour_corr(d["G"].reshape(-1, N)),
    ant_neigh_corr=neighbour_corr(d["F"].transpose(0, 2, 1).reshape(-1, a.tx)),
    los_frac=dict(bs=float(d["los_ris_bs"].mean()),
                  ue=float(d["los_ris_ue"].mean()),
                  direct=float(d["los_direct"].mean())))
say("  G rank(pooled) {g_rank_pooled:.2f}  G rank(user0) {g_rank_user0:.2f}  "
    "F rank {f_rank_ant0:.2f}  G neigh {g_neigh_corr:.3f}".format(**res["channel"]))

tr, va, te = split_indices(a.samples, seed=0)
say(f"  split  train {len(tr)}  val {len(va)}  test {len(te)}")

# -------------------------------------------------------------- baselines
bte = te[:a.baseline_n]
say(f"\n=== baselines on {len(bte)} test scenarios ===")
meth = ("no_ris", "random", "su_weakest", "su_average", "su_best_of",
        "cd", "pga", "ao")
res["baselines"] = {}
for m in meth:
    t0 = time.time()
    R, th = B._DISPATCH[m](F[bte], G[bte], hd[bte], pt, nv, precoder="zf")
    mt = S.rate_metrics(R)
    res["baselines"][m] = mt | {"sec": time.time() - t0}
    say(f"  {m:>11}  min {mt['min_rate']:7.4f}  sum {mt['sum_rate']:8.3f}"
        f"   ({time.time()-t0:.1f}s)")
# The strongest classical, not AO by assumption. PGA (3 random restarts)
# and AO (cd + su_average + random) differ by well under a percent and
# which one wins varies run to run, so naming one of them in advance was
# how an earlier version of this project ended up reporting the weaker of
# the two as "the number to beat".
_cands = {m: res["baselines"][m]["min_rate"]
          for m in ("cd", "pga", "ao") if m in res["baselines"]}
_best = max(_cands, key=_cands.get)
target = _cands[_best]
say(f"  -> the number to beat is {_best}: {target:.4f}   "
    f"(others: {', '.join(f'{k} {v:.4f}' for k, v in _cands.items() if k != _best)})")
res["target"] = dict(method=_best, rate=target)

# ------------------------------------------------------------------ train
res["models"] = {}
for mode in MODES:
    say(f"\n=== train mode={mode} ===")
    torch.manual_seed(a.seed)
    net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=mode,
                    residual=not a.no_residual, link_ratio=a.link_ratio)
    say(f"  parameters: {count_params(net)}")
    t0 = time.time()
    net, hist = train_model(net, X, F, G, hd, pt, nv, (tr, va, te),
                            epochs=a.epochs, seed=a.seed, log=say)
    t_min, t_sum = evaluate(net, X, F, G, hd, pt, nv, te)
    say(f"  TEST  min {t_min:.4f}  sum {t_sum:.3f}   "
        f"({t_min/target:.3f}x of AO)   [{time.time()-t0:.0f}s]")

    # order sensitivity, measured on the RATE
    chk = te[:2000]
    vals = []
    rng = np.random.default_rng(0)
    for r in range(6):
        p = np.arange(a.users) if r == 0 else rng.permutation(a.users)
        pt_ = torch.as_tensor(p)
        v, _ = evaluate(net, X[:, pt_], F, G[:, pt_], hd[:, pt_], pt, nv, chk)
        vals.append(v)
    spread = float(np.max(vals) - np.min(vals))
    say(f"  user-order spread over 6 permutations: {spread:.2e}  "
        f"(mean {np.mean(vals):.4f})")

    res["models"][mode] = dict(params=count_params(net), test_min=t_min,
                               residual=not a.no_residual,
                               test_sum=t_sum, frac_of_ao=t_min / target,
                               perm_spread=spread, perm_mean=float(np.mean(vals)),
                               history=hist, sec=time.time() - t0)
    torch.save(net.state_dict(), OUT / f"mumiso_{a.tag}_{mode}.pt")

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\n=== done in {(time.time()-t_all)/60:.1f} min -> "
    f"results/mumiso_{a.tag}.json ===")
