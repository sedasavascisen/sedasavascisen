"""
Jury questions 4 and 2 (ON_KAYIT_S4_S2.md). Conditions: "fresh" (Paper 2), "joint" (precoder from t = 0 CSI, applied
with theta at tau), "clarke" (Truong-Heath aging, rho = J0(2 pi f_d t), one innovation draw per scenario, fresh precoder).
-> raw/s4_s2.json (per-scenario effective rates per (condition, seed, speed, arm))
"""
import sys, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np, torch
from scipy_free_j0 import j0
from common import Aging, commit
from ris_mu.mumiso import baselines as B, system as S
torch.set_num_threads(2)
H = pathlib.Path(__file__).parent; R = H / "raw"
LATM = json.load(open(R / "arms.json"))["lat_meas"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
ARMS = ["SU-average", "SU-best-of"] + [f"Adam-{L}" for L in STEPS] + [f"CD-{s}" for s in range(1, 9)]
SPEEDS = {"3kmh": 3 / 3.6, "1.5mps": 1.5, "10kmh": 10 / 3.6}
times = [0.0] + sorted({round(LATM[a], 9) for a in ARMS})
FC, C0 = 3e9, 299792458.0


def rate_with(F, Gt, Ht, th, W, pt, nv):
    He = S.effective_channel(F, Gt, Ht, torch.cos(th), torch.sin(th))
    return torch.log2(1.0 + S.sinr(He, W, nv)).min(-1).values


t_start = time.time()
out = dict(commit=commit(), lat=LATM, times=times, data={})
for seed in (12, 11):
    A0 = Aging(seed, [0.0])
    F, G0, H0, pt, nv = A0.F, A0.G[0], A0.H[0], A0.pt, A0.nv
    su = A0.su_average()
    PH = {"SU-average": su, "SU-best-of": A0.su_best_of(), **{f"Adam-{L}": A0.adam(su, L) for L in STEPS},
          **{f"CD-{s}": B.coord_descent(F, G0, H0, pt, nv, iters=s)[1] for s in range(1, 9)}}
    W0 = {a: S.zf(S.effective_channel(F, G0, H0, torch.cos(th), torch.sin(th)), pt, noise_var=nv) for a, th in PH.items()}
    pG = (G0.abs() ** 2).mean(-1, keepdim=True); pH = (H0.abs() ** 2).mean(-1, keepdim=True)
    print(f"seed {seed}: phases ({time.time() - t_start:.0f} s)", flush=True)
    for si, (sp, v) in enumerate(SPEEDS.items()):
        A = Aging(seed, times, v=v)
        fresh, joint = {}, {}
        for a in ARMS:
            m = A.idx(round(LATM[a], 9))
            fresh[a] = A.minrate(PH[a], m).numpy().tolist()
            joint[a] = rate_with(F, A.G[m], A.H[m], PH[a], W0[a], pt, nv).numpy().tolist()
        del A
        g = torch.Generator().manual_seed(1000 * seed + si)
        cn = lambda shape: torch.complex(torch.randn(shape, generator=g), torch.randn(shape, generator=g)) / 2 ** 0.5
        EG = cn(G0.shape) * pG.sqrt(); EH = cn(H0.shape) * pH.sqrt()
        fd = v * FC / C0
        clarke = {}
        for a in ARMS:
            rho = float(j0(2 * np.pi * fd * LATM[a] / 1000.0)); s_ = (1 - rho ** 2) ** 0.5
            Gt, Ht = rho * G0 + s_ * EG, rho * H0 + s_ * EH
            clarke[a] = A0.minrate(PH[a], 0, G=Gt, H=Ht).numpy().tolist()
        for cond, d in (("fresh", fresh), ("joint", joint), ("clarke", clarke)):
            out["data"][f"{cond}|{seed}|{sp}"] = d
        print(f"  {sp} ({time.time() - t_start:.0f} s)", flush=True)
    del A0
out["seconds"] = time.time() - t_start
json.dump(out, open(R / "s4_s2.json", "w"))
print("wrote", flush=True)
