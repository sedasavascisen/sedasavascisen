"""
Throughput with pilot overhead: CSI-based versus position-based RIS phases
for walking users in a fixed site (the periodic controller of the mobility
paper, Definition 3, single user).

Users start at test (report) or validation (selection) positions, walk at
1.5 m/s in a straight line, channel on a 0.5 ms grid over 400 ms; the rate is
averaged over 200-400 ms, each grid cell weighted by the fraction of it that
is not pilot time (pilot intervals are shorter than a cell for 4 symbols).
(The scatterers are fixed objects of the site, so long horizons are
consistent here, unlike the mobility generator.)
Every policy re-optimizes every U ms (U selected per policy on the
validation users from U_GRID):
  CSI + CD-1 / CSI + SU-align   P pilot symbols, P in {33 (N+1, unstructured
                                cascaded estimation), 17, 9, 5 (F known for the
                                site: only g and h_d; 5 = noiseless minimum)},
                                then the measured compute time; the phase
                                uses the channel at the update instant
  position + geometric / CNN / radio map (training-free kNN map from the same
  survey, ris_mu.sumiso.radio_map)   4 pilot symbols (common-phase candidates),
                                then the compute time; position known at the
                                update instant (optionally with error)
Symbols: 5G NR, 14 per slot of 15/SCS ms (SCS = 30 kHz unless --scs).
Compute times: CD-1 and SU-align from results/sumiso_mobility_eval.json;
the position network and the geometric phase are timed here (one thread,
single position, waits for load < 0.5). The beam is maximum-ratio on the
current channel for every policy (fresh-beam assumption of the paper).
Writes results/site_eval_dynamic.json.
"""
import sys
import os
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.site import Site
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase
from ris_mu.sumiso.position import geometric_phase, position_features, pick_common_phase
from ris_mu.sumiso.radio_map import RadioMap

ap = argparse.ArgumentParser()
ap.add_argument("--sites", type=int, nargs="*", default=[1, 2, 3, 4, 5])
ap.add_argument("--users", type=int, default=300)
ap.add_argument("--scs", type=float, default=30.0, help="kHz")
ap.add_argument("--pos_err", type=float, default=0.0)
ap.add_argument("--tag", default="site_eval_dynamic")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(1)
DT = 0.5                                    # ms, as in the mobility paper
GRID = np.arange(0, 400 + DT / 2, DT)
WIN = (GRID >= 200) & (GRID < 400)
U_GRID = [2, 5, 10, 20, 40, 80, 160]
sym_ms = 15.0 / a.scs / 14.0
PILOTS = {"CSI + CD-1 (33 pilots)": 33, "CSI + CD-1 (17 pilots)": 17, "CSI + CD-1 (9 pilots)": 9,
          "CSI + CD-1 (5 pilots)": 5, "CSI + SU-align (33 pilots)": 33,
          "position + geometric": 4, "position + CNN": 4, "position + radio map": 4}
lat_ev = json.load(open(ROOT / "results" / "sumiso_mobility_eval.json"))["latency_ms"]


def timeit(f, reps=50):
    f(); f()
    t = []
    for _ in range(reps):
        t0 = time.perf_counter(); f(); t.append(time.perf_counter() - t0)
    return float(np.median(t) * 1e3)


def trajectories(site, start, rng):
    ang = rng.uniform(0, 2 * np.pi, len(start))
    v = 1.5 * np.c_[np.cos(ang), np.sin(ang), np.zeros_like(ang)]
    p = start[:, None, :] + v[:, None, :] * GRID[None, :, None] / 1e3       # [U,M,3]
    for ax in (0, 1):                     # reflect at the room walls (obstacles are not avoided)
        lo, hi = 0.5, site.room[ax] - 0.5
        x = np.mod(p[..., ax] - lo, 2 * (hi - lo))
        p[..., ax] = lo + np.where(x > hi - lo, 2 * (hi - lo) - x, x)
    return p


res = dict(config=vars(a), symbol_ms=sym_ms, pilots=PILOTS, U_grid=U_GRID, sites={})
rng_bs = np.random.default_rng(0)
for s in a.sites:
    site = Site(seed=s)
    z = np.load(ROOT / "data_site" / f"site{s}.npz")
    snr = site.snr_scale
    ck = torch.load(ROOT / "results" / f"site{s}_cnn_err{a.pos_err:g}.pt") if \
        (ROOT / "results" / f"site{s}_cnn_err{a.pos_err:g}.pt").exists() else torch.load(ROOT / "results" / f"site{s}_cnn_err0.pt")
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], "seq"); net.load_state_dict(ck["state"]); net.eval()
    perr = np.random.default_rng(500 + s)

    # --- compute latency of the position arms (idle gate) -------------------
    while os.getloadavg()[0] >= 0.5:
        time.sleep(10)
    load_t = os.getloadavg()[0]
    p1 = z["test_pos"][:1]
    F1, G1, H1 = (torch.as_tensor(x) for x in site.channels(p1))
    a1, b1 = SV.cascade(F1, G1, H1)
    t_geo = timeit(lambda: geometric_phase(site, p1))
    with torch.no_grad():
        t_cnn = timeit(lambda: phase(net((position_features(site, p1) - ck["mu"]) / ck["sd"])))
    Fm = torch.as_tensor(z["F"])
    Atr, Btr = SV.cascade(Fm.expand(len(z["train_G"]), *Fm.shape), torch.as_tensor(z["train_G"]), torch.as_tensor(z["train_hd"]))
    rmap = RadioMap(z["train_pos"], Atr, Btr)               # offline, from the same survey
    t_rm = timeit(lambda: rmap.lookup(p1))
    COMP = {k: lat_ev["CD-1"] for k in PILOTS if k.startswith("CSI + CD-1")}
    COMP.update({"CSI + SU-align (33 pilots)": lat_ev["SU-align"], "position + geometric": t_geo,
                 "position + CNN": t_cnn, "position + radio map": t_rm})

    def run(start, seed):
        traj = trajectories(site, start, np.random.default_rng(seed))
        U_, M = traj.shape[:2]
        flat = traj.reshape(-1, 3)
        F, G, H = (torch.as_tensor(x) for x in site.channels(flat))
        A, B = SV.cascade(F, G, H)
        A = A.reshape(U_, M, -1); B = B.reshape(U_, M, B.shape[1], B.shape[2])
        out = {}
        for pol in PILOTS:
            out[pol] = {}
            for U in U_GRID:
                tp = PILOTS[pol] * sym_ms
                if tp + COMP[pol] > U:
                    continue
                th_cur = SV.su_align(A[:, 0], B[:, 0])           # before the first deployment
                rates = np.zeros((U_, M))
                pending = []
                for m, t in enumerate(GRID):
                    if abs(t / U - round(t / U)) < 1e-9:                                  # update instant: compute from this snapshot
                        a_, b_ = A[:, m], B[:, m]
                        if pol.startswith("CSI + CD-1"):
                            th = SV.coord_ascent(a_, b_, SV.su_align(a_, b_), sweeps=1, tol=-1)[0]
                        elif pol.startswith("CSI + SU-align"):
                            th = SV.su_align(a_, b_)
                        else:
                            pos = traj[:, m] + a.pos_err * perr.standard_normal((U_, 3))
                            if pol == "position + geometric":
                                th = geometric_phase(site, pos)
                            elif pol == "position + radio map":
                                th = rmap.lookup(pos)
                            else:
                                with torch.no_grad():
                                    th = phase(net((position_features(site, pos) - ck["mu"]) / ck["sd"]))
                            th = pick_common_phase(th, a_, b_)      # 4 pilots measure the 4 rotations
                        pending.append((t + tp + COMP[pol], th))
                    while pending and pending[0][0] <= t:
                        th_cur = pending.pop(0)[1]
                    k0 = np.floor(t / U + 1e-9) * U                     # last update instant
                    pilot = max(0.0, min(t + DT, k0 + tp) - max(t, k0)) # pilot time inside [t, t+DT)
                    w = 1.0 - pilot / DT
                    rates[:, m] = w * torch.log2(1 + snr * SV.gain(th_cur, A[:, m], B[:, m])).numpy()
                out[pol][U] = rates[:, WIN].mean(1)
        return out

    val = run(z["val_pos"][:a.users], 11 * s)
    test = run(z["test_pos"][:a.users], 13 * s)
    site_res = dict(load_before_timing=load_t, compute_ms=COMP, policies={})
    best_U = {pol: max(val[pol], key=lambda U: val[pol][U].mean()) for pol in PILOTS}
    for pol in PILOTS:
        site_res["policies"][pol] = dict(best_U_on_val=best_U[pol], test_by_U={str(U): float(v.mean()) for U, v in test[pol].items()},
                                         test=float(test[pol][best_U[pol]].mean()))
    def pd(x, y):
        d = test[x][best_U[x]] - test[y][best_U[y]]
        bs = [d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        return [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    site_res["cnn_minus"] = {y: pd("position + CNN", y) for y in PILOTS if y != "position + CNN"}
    site_res["radio_map_minus"] = {y: pd("position + radio map", y) for y in PILOTS if y.startswith("CSI")}
    site_res["cnn_minus_geometric"] = site_res["cnn_minus"]["position + geometric"]
    res["sites"][str(s)] = site_res
    print(f"site {s}: " + " | ".join(f"{p} U={site_res['policies'][p]['best_U_on_val']} {site_res['policies'][p]['test']:.3f}"
                                     for p in PILOTS), flush=True)
    json.dump(res, open(ROOT / "results" / f"{a.tag}.json", "w"), indent=1)
