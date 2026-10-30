"""How much is there to learn? Baseline spread for several (T, K) scenarios."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank)
from ris_mu.mumiso import baselines as B

torch.manual_seed(0)
S_N = 200
cfgs = [(4, 4), (8, 4), (8, 6), (16, 4)]
meth = ("no_ris", "random", "su_weakest", "su_average", "cd", "pga", "ao")

print(f"{S_N} scenarios each, N=32, ZF, continuous phase, max-min [b/s/Hz]\n")
hdr = f"{'T x K':>7}" + "".join(f"{m:>12}" for m in meth) + f"{'Grank':>8}{'sec':>7}"
print(hdr); print("-" * len(hdr))
rows = {}
for T, K in cfgs:
    t0 = time.time()
    panel, cfg = make_mumiso_scenario(n_users=K, n_bs_antennas=T, seed=11)
    d = MuMisoChannel(panel, cfg).generate(S_N)
    F, G, hd, _ = to_torch(d)
    nv = 1.0 / cfg.snr_scale()
    r = B.run_all(F, G, hd, 1.0, nv, methods=meth, precoder="zf")
    gr = effective_rank(d["G"].reshape(-1, 32))
    rows[(T, K)] = {m: r[m]["min_rate"] for m in meth}
    print(f"{T:3d} x{K:3d}" + "".join(f"{r[m]['min_rate']:12.3f}" for m in meth)
          + f"{gr:8.2f}{time.time()-t0:7.1f}")

print("\n=== checks ===")
for k, v in rows.items():
    strongest = max(("cd", "pga", "ao"), key=lambda m: v[m])
    ok_ord = (max(v["cd"], v["pga"], v["ao"]) > v["su_average"]
              > v["random"] > v["no_ris"])
    head = v[strongest] / max(v["su_average"], 1e-9)
    print(f"  T={k[0]:2d} K={k[1]}:  strongest={strongest} ({v[strongest]:.3f})   "
          f"ordering {ok_ord}   headroom over su_average {head:5.2f}x")

print("\n=== CD monotone? (T=8, K=4, 40 scenarios) ===")
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=3)
d = MuMisoChannel(panel, cfg).generate(40)
F, G, hd, _ = to_torch(d); nv = 1.0 / cfg.snr_scale()
th = B.su_average(F, G, hd, 1.0, nv)[1]
prev = B._obj(F, G, hd, th, 1.0, nv, "zf", "maxmin").mean().item()
hist = [prev]
for it in range(6):
    _, th = B.coord_descent(F, G, hd, 1.0, nv, iters=1, theta0=th)
    v = B._obj(F, G, hd, th, 1.0, nv, "zf", "maxmin").mean().item()
    hist.append(v)
d_ = np.diff(hist)
print("  " + " -> ".join(f"{h:.4f}" for h in hist))
print(f"  monotone: {bool((d_ >= -1e-6).all())}   min step {d_.min():+.2e}")
