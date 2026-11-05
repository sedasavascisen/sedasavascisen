"""
The paper's main measurements at standardised user speeds.

Why: the main results use v = 1.5 m/s (5.4 km/h). Reference speeds for an
indoor hotspot in the standards:
  3 km/h   3GPP TR 38.913, Table 6.1.1-1 (Indoor hotspot): "100% Indoor, 3km/h"
  10 km/h  ITU-R M.2410: upper end of the pedestrian mobility class (0-10 km/h);
           the Indoor Hotspot-eMBB mobility requirement is evaluated at 10 km/h
  30 km/h  ITU-R M.2410 Dense Urban-eMBB mobility evaluation speed; beyond
           the pedestrian class, used here only as a stress test
so this script repeats the aging measurements at 3, 5.4, 10 and 30 km/h on
the same 400 aging-set scenarios (seed 11, 4 users, 20 scatterers).

The t=0 channels do not depend on the speed (the generator draws the same
positions, headings and gains; speed only scales the displacement), so every
method's phase is computed once and aged at each speed; this is asserted.
The time grid is fine (0.5 ms up to 40 ms) so that the optimum is resolved at
30 km/h, where T_c = 5.1 ms. Latencies: SU heuristics, coordinate descent and
long-run Adam from results/mumiso_mobility_latency.json; Adam 13.3/8 ms per
step (the paper's convention). The trust horizon is the displacement at
200 ms and 1.5 m/s (0.3 m), i.e. 0.3 m / v.
At 1.5 m/s the t=0 rates must reproduce results/mumiso_aging_fixzf.json.
Writes results/mumiso_standard_speeds.json.
"""
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--kmh", default="3,5.4,10,30")
ap.add_argument("--steps", default="1,2,3,4,5,6,8,10,12,16,20,24,32,48")
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--threads", type=int, default=4)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(a.threads)
STEPS = [int(s) for s in a.steps.split(",")]
MS_PER_STEP = 13.3 / 8
ML = json.load(open(ROOT / "results" / "mumiso_mobility_latency.json"))["median"]
LAT = {"su_average": ML["su_average"], "su_best_of": ML["su_best_of"], "cd": ML["cd"], "pga": ML["pga"]}
TOVS = [0.0, 1.71, 3.43]                       # 48 pilot symbols at 30 / 15 kHz (Section V)
TIMES = np.unique(np.r_[np.arange(0, 40.01, 0.5), np.arange(45, 101, 5), 150, 200, 300, 500,
                        LAT["cd"], 1500, LAT["pga"], 6000])
v_of = lambda kmh: 1.5 if abs(kmh - 5.4) < 1e-9 else kmh / 3.6
rng = np.random.default_rng(0)


def gen(v):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": v, "times_ms": tuple(TIMES), "n_clusters": 20})
    return panel, cfg, MobileMuMisoChannel(panel, cfg).generate(a.scenarios)


def paired(x, y):
    d = x - y
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    return [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


# ---- phases on the (speed-independent) t=0 channel ---------------------------
t0 = time.time()
panel, cfg, d0 = gen(1.5)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
N = panel.positions.shape[0]
F = torch.as_tensor(d0["F"], dtype=torch.complex64)
G0 = torch.as_tensor(d0["G_t"][:, 0], dtype=torch.complex64)
H0 = torch.as_tensor(d0["hd_t"][:, 0], dtype=torch.complex64)


def adam_phase(L, start):
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step(); opt.zero_grad()
    return start + dl.detach()


_, TH_SU = B.su_average(F, G0, H0, pt, nv)
_, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
phases = {"su_average": TH_SU, "su_best_of": TH_BEST}
for L in STEPS:
    phases[f"adam{L}"] = adam_phase(L, TH_SU)
    LAT[f"adam{L}"] = L * MS_PER_STEP
_, phases["cd"] = B.coord_descent(F, G0, H0, pt, nv)
_, phases["pga"] = B.pga(F, G0, H0, pt, nv)
print(f"phases computed in {time.time()-t0:.0f}s", flush=True)

ref = json.load(open(ROOT / "results" / "mumiso_aging_fixzf.json"))
res = dict(config=vars(a), times_ms=TIMES.tolist(), latency_ms=LAT, t_ov_ms=TOVS,
           sources={"3": "3GPP TR 38.913 Table 6.1.1-1 (Indoor hotspot, 3 km/h)",
                    "10": "ITU-R M.2410: pedestrian class 0-10 km/h; Indoor Hotspot-eMBB mobility at 10 km/h",
                    "30": "ITU-R M.2410: Dense Urban-eMBB mobility at 30 km/h (stress test, not indoor)",
                    "5.4": "this paper (1.5 m/s)"}, speeds={})
for kmh in [float(x) for x in a.kmh.split(",")]:
    v = v_of(kmh)
    _, _, d = gen(v)
    assert np.array_equal(d["G_t"][:, 0], d0["G_t"][:, 0]) and np.array_equal(d["F"], d0["F"]), "t=0 channel depends on v"
    fd = v * 3e9 / 3e8
    Tc = 0.423 / fd * 1e3
    trust = 0.3 / v * 1e3
    Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    curves = {k: np.stack([S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv, "zf").min(-1).values.numpy()
                           for m in range(len(TIMES))], 1) for k, th in phases.items()}
    if abs(v - 1.5) < 1e-9:
        for k_ref, k in (("su_best_of", "su_best_of"), ("cd", "cd"), ("pga", "pga"), ("adam8", "adam8")):
            assert abs(curves[k][:, 0].mean() - ref["curve"][k_ref][0]) < 1e-3, f"t=0 rate of {k} does not reproduce"
    eff = lambda k, ov: np.array([np.interp(LAT[k] + ov, TIMES, row) for row in curves[k]])
    blk = dict(v_ms=v, f_d_hz=fd, coherence_ms=Tc, x=MS_PER_STEP * 1e-3 * fd, trust_ms=trust, by_t_ov={})
    for ov in TOVS:
        E = {k: eff(k, ov) for k in phases}
        adam = {L: E[f"adam{L}"].mean() for L in STEPS}
        Lb = max(adam, key=adam.get)
        within = [L for L in STEPS if adam[L] >= 0.995 * adam[Lb]]
        loss48 = paired(E[f"adam{Lb}"], E["adam48"])
        blk["by_t_ov"][str(ov)] = dict(
            methods={k: dict(t0=float(curves[k][:, 0].mean()), latency_ms=LAT[k] + ov, effective=float(E[k].mean()),
                             trusted=bool(LAT[k] + ov <= trust)) for k in phases},
            best_L=Lb, within_half_percent=within, best_eff=float(adam[Lb]),
            loss_L48_pct=[100 * x / adam[Lb] for x in loss48],
            su_best_minus_cd=paired(E["su_best_of"], E["cd"]),
            su_best_minus_pga=paired(E["su_best_of"], E["pga"]),
            adam_best_minus_su_best=paired(E[f"adam{Lb}"], E["su_best_of"]))
    res["speeds"][f"{kmh:g}"] = blk
    b0 = blk["by_t_ov"]["0.0"]
    print(f"{kmh:>5g} km/h (v={v:.3f} m/s, T_c={Tc:5.1f} ms, x={blk['x']:.4f}): L*={b0['best_L']} "
          f"(within 0.5%: {b0['within_half_percent']}) eff {b0['best_eff']:.3f}; L=48 costs {b0['loss_L48_pct'][0]:.1f}% "
          f"[{b0['loss_L48_pct'][1]:.1f},{b0['loss_L48_pct'][2]:.1f}]; SU-best {b0['methods']['su_best_of']['effective']:.3f} "
          f"CD {b0['methods']['cd']['effective']:.3f} long-Adam {b0['methods']['pga']['effective']:.3f}", flush=True)
    json.dump(res, open(ROOT / "results" / "mumiso_standard_speeds.json", "w"), indent=1)
print("wrote results/mumiso_standard_speeds.json")
