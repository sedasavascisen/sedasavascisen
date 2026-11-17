"""
Sensitivity of Paper 2's headline numbers to the RIS element gain (reference check group 8, Tang2021TWC eq. (2)):
the code uses G = 2(2q+1) = 6 for a cos^q POWER pattern (q = 1), Tang's formula gives G = 2(q+1) = 4.
The package is NOT modified: RISPanel.element_gain is patched in this process only. Aging set (seed 11, 400 scenarios),
speeds 1.5 m/s and 10 km/h, fresh precoder, same-session latencies (thesis_exp/juri/raw/timing2.json, start excluded as in
Paper 2). Arms: SU-average, SU-best-of, Adam-L (L in STEPS), CD (default). Reported for G = 6 (as published) and G = 4:
L*, L = 48 loss, best arm and the ranking SU-best-of vs CD. -> raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from common import commit, boot
import ris_mu.geometry as geo
from ris_mu.mumiso import baselines as B
from common import Aging
torch.set_num_threads(2)
H = pathlib.Path(__file__).parent
T2 = json.load(open(H.parent / "juri" / "raw" / "timing2.json"))["median_ms"]
T3 = json.load(open(H.parent / "juri" / "raw" / "timing3.json"))["median_ms"]
_ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam = lambda L: float(np.interp(L, sorted(_ML), [_ML[x] for x in sorted(_ML)]))
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
LAT = {"SU-average": T2["su_average"], "SU-best-of": T2["su_best_of"], "CD": T3["cd8"], **{f"Adam-{L}": adam(L) for L in STEPS}}
times = [0.0] + sorted({round(v, 9) for v in LAT.values()})
orig = geo.RISPanel.element_gain
out = dict(commit=commit(), latencies=LAT, gains={})
for gname, prop in (("G6_published", orig), ("G4_tang", property(lambda self: 2.0 * (self.q + 1.0)))):
    geo.RISPanel.element_gain = prop
    res = {}
    for sp, v in (("1.5mps", 1.5), ("10kmh", 10 / 3.6)):
        A = Aging(11, times, v=v); su = A.su_average()
        PH = {"SU-average": su, "SU-best-of": A.su_best_of(), "CD": B.coord_descent(A.F, A.G[0], A.H[0], A.pt, A.nv)[1],
              **{f"Adam-{L}": A.adam(su, L) for L in STEPS}}
        eff = {k: A.minrate(th, A.idx(round(LAT[k], 9))).numpy() for k, th in PH.items()}
        t0 = {k: float(A.minrate(th, 0).mean()) for k, th in PH.items()}
        Ls = max([f"Adam-{L}" for L in STEPS], key=lambda k: eff[k].mean())
        d48 = eff["Adam-48"] - eff[Ls]; dcd = eff["CD"] - eff["SU-best-of"]
        res[sp] = dict(L_star=Ls, eff_L_star=float(eff[Ls].mean()), loss48_pct=float(100 * (1 - eff["Adam-48"].mean() / eff[Ls].mean())),
                       ci48=boot(d48), cd_minus_sbo=float(dcd.mean()), ci_cd=boot(dcd), su_best_of=float(eff["SU-best-of"].mean()),
                       t0_su_average=t0["SU-average"], best_arm=max(eff, key=lambda k: eff[k].mean()))
        print(gname, sp, res[sp], flush=True)
        del A
    out["gains"][gname] = res
geo.RISPanel.element_gain = orig
json.dump(out, open(H / "raw" / "results.json", "w"), indent=1)
print("wrote", flush=True)
