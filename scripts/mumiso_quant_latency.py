"""
Quantised phase and latency: the two places where a learned model and a
classical optimiser are genuinely not comparable on rate alone.

Quantisation -- the honest comparison is against DISCRETE coordinate
descent, which searches the actual 2^b grid, not against "optimise
continuously then round". On an earlier single-RIS experiment discrete CD
beat a straight-through network at 1 bit (5.600 vs 3.544). This script
measures whether that holds here.

Latency -- one forward pass versus thousands of objective evaluations. This
is where the learned model wins and it is the claim the thesis can defend.
"""
import sys, pathlib, json, time, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.mumiso.train import train_model, evaluate
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--samples", type=int, default=8000)
ap.add_argument("--epochs", type=int, default=20)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--mode", default="exchange")
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--eval-n", type=int, default=600)
ap.add_argument("--tag", default="quant")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
def say(*m): print(*m, flush=True)

panel, cfg = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=a.seed)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(a.samples)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd).numpy()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi))
tr, va, te = split_indices(a.samples, seed=0)
ev = te[:a.eval_n]
say(f"N={N} T={a.tx} K={a.users}  samples={a.samples}  eval on {len(ev)}\n")

res = dict(config=vars(a), quant={}, latency={})

# ------------------------------------------------------------- quantisation
say("=== quantised phase: discrete CD vs continuous-then-round vs learned ===")
say(f"{'bits':>5}{'suavg->rnd':>12}{'AO->rnd':>10}{'CD->rnd':>10}"
    f"{'discrete CD':>13}{'learned STE':>13}")
say("-" * 63)
for bits in (1, 2, 3):
    row = {}
    row["su_round"] = S.rate_metrics(
        B.su_average(F[ev], G[ev], hd[ev], pt, nv, bits=bits)[0])["min_rate"]
    _, th_ao = B.ao(F[ev], G[ev], hd[ev], pt, nv, bits=None)
    row["ao_round"] = S.rate_metrics(
        B._rate(F[ev], G[ev], hd[ev], th_ao, pt, nv, "zf", bits))["min_rate"]
    _, th_cd = B.coord_descent(F[ev], G[ev], hd[ev], pt, nv, bits=None)
    row["cd_round"] = S.rate_metrics(
        B._rate(F[ev], G[ev], hd[ev], th_cd, pt, nv, "zf", bits))["min_rate"]
    row["cd_discrete"] = S.rate_metrics(
        B.coord_descent(F[ev], G[ev], hd[ev], pt, nv, bits=bits)[0])["min_rate"]

    torch.manual_seed(a.seed)
    net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=a.mode)
    net, _ = train_model(net, X, F, G, hd, pt, nv, (tr, va, te),
                         epochs=a.epochs, seed=a.seed, bits=bits, log=None)
    row["learned_ste"] = evaluate(net, X, F, G, hd, pt, nv, ev, bits=bits)[0]
    res["quant"][bits] = row
    say(f"{bits:5d}{row['su_round']:12.4f}{row['ao_round']:10.4f}"
        f"{row['cd_round']:10.4f}{row['cd_discrete']:13.4f}"
        f"{row['learned_ste']:13.4f}")

best = {b: max(r, key=r.get) for b, r in res["quant"].items()}
say("\n  winner per bit depth: " + ", ".join(f"{b}-bit {w}" for b, w in best.items()))

# ----------------------------------------------------------------- latency
say("\n=== latency, single scenario (CPU, batch size 1) ===")
net = MuMisoNet(N=N, n_users=a.users, n_tx=a.tx, mode=a.mode)
sd = OUT / f"mumiso_main_{a.mode}.pt"
if sd.exists():
    net.load_state_dict(torch.load(sd)); say(f"  (loaded {sd.name})")
net.eval()
one = slice(0, 1)
with torch.no_grad():
    for _ in range(5):
        net.phases(X[one])
def timeit(fn, reps):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
    return np.array(ts) * 1e3
with torch.no_grad():
    t_net = timeit(lambda: net.phases(X[one]), 50)
t_cd = timeit(lambda: B.coord_descent(F[one], G[one], hd[one], pt, nv), 3)
t_ao = timeit(lambda: B.ao(F[one], G[one], hd[one], pt, nv), 3)
t_su = timeit(lambda: B.su_average(F[one], G[one], hd[one], pt, nv), 20)
for nm, t in [("learned (1 pass)", t_net), ("SU closed form", t_su),
              ("coord descent", t_cd), ("AO (CD+PGA)", t_ao)]:
    res["latency"][nm] = dict(p50=float(np.percentile(t, 50)),
                              p95=float(np.percentile(t, 95)))
    say(f"  {nm:>18}  p50 {np.percentile(t,50):9.3f} ms   "
        f"p95 {np.percentile(t,95):9.3f} ms")
sp = res["latency"]["AO (CD+PGA)"]["p50"] / res["latency"]["learned (1 pass)"]["p50"]
say(f"  -> learned model is {sp:.0f}x faster than AO at the median")

with open(OUT / f"mumiso_{a.tag}.json", "w") as f:
    json.dump(res, f, indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
