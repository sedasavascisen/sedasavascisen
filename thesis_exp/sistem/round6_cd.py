"""Round 6 (idea 3), cheap pre-test: tuned CD (s = 1..3 sweeps, from SU-best-of) in the slowest condition A1 (3 GHz,
3 km/h), seeds 12 (select s) and 14 (dev), W in {0, 20}. CD-s latency = SU-best-of + s sweeps without early stop
(juri/raw/timing3.json, same machine/protocol). Compared with the v1b pick on the same draw (from the fresh cube)."""
import sys, json, pathlib
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "p4"))
import numpy as np, torch
from common import Aging, boot
from ris_mu.mumiso import baselines as B
import controllers as C
torch.set_num_threads(2)
T3 = json.load(open(H.parent / "juri" / "raw" / "timing3.json"))["median_ms"]
T2 = json.load(open(H.parent / "juri" / "raw" / "timing2.json"))["median_ms"]
v = 3 / 3.6; W = np.arange(0, 21, 2.0)
lat = {s: T2["su_best_of"] + (T3[f"cd{s}"] - T2["su_average"]) for s in (1, 2, 3)}   # timing3 cd includes an SU-average start
out = {}
for seed in (12, 14):
    times = [0.0] + sorted({round(lat[s] + w, 9) for s in lat for w in W})
    A = Aging(seed, times, v=v); sb = A.su_best_of()
    th = {s: B.coord_descent(A.F, A.G[0], A.H[0], A.pt, A.nv, iters=s, theta0=sb)[1] for s in lat}
    out[seed] = {s: (np.mean([A.minrate(th[s], A.idx(round(lat[s] + w, 9))).numpy() for w in W[:1]], 0),
                     np.mean([A.minrate(th[s], A.idx(round(lat[s] + w, 9))).numpy() for w in W], 0)) for s in lat}
cal = C.load(12); m, z = C.load(14)
for wi, Wn in enumerate((0, 20)):
    s_best = max(lat, key=lambda s: out[12][s][wi].mean())
    pick = C.v1b_carrier(m, cal, "A1", Wn); vb = z[f"A1_eff{Wn}"][m["arms"].index(pick)]
    d = out[14][s_best][wi] - vb
    print(f"A1 W{Wn}: CD-{s_best} ({lat[s_best]:.1f} ms) {out[14][s_best][wi].mean():.4f} vs v1b {pick} {vb.mean():.4f}: {d.mean():+.4f} {boot(d)}")
