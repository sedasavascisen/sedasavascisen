"""
Throughput with pilot overhead: CSI-based versus position-based RIS phases
for walking users in a fixed site (the periodic controller of the mobility
paper, Definition 3, single user).

Users start at test (report) or validation (selection) positions, walk at
1.5 m/s in a straight line, channel on a 1 ms grid over 200 ms; the rate is
averaged over 100-200 ms and counted only outside pilot intervals.
Every policy re-optimizes every U ms (U selected per policy on the
validation users from U_GRID):
  CSI + CD-1 / CSI + SU-align   cascaded-channel pilots, N+1 = 33 symbols,
                                then the measured compute time; the phase
                                uses the channel at the update instant
  position + geometric / CNN    4 pilot symbols (common-phase candidates),
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

ap = argparse.ArgumentParser()
ap.add_argument("--sites", type=int, nargs="*", default=[1, 2, 3, 4, 5])
ap.add_argument("--users", type=int, default=300)
ap.add_argument("--scs", type=float, default=30.0, help="kHz")
ap.add_argument("--pos_err", type=float, default=0.0)
ap.add_argument("--tag", default="site_eval_dynamic")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(1)
GRID = np.arange(0, 201, 1.0)              # ms
U_GRID = [2, 5, 10, 20, 40, 80]
sym_ms = 15.0 / a.scs / 14.0
PILOTS = {"CSI + CD-1": 33, "CSI + SU-align": 33, "position + geometric": 4, "position + CNN": 4}
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
    return start[:, None, :] + v[:, None, :] * GRID[None, :, None] / 1e3       # [U,M,3]


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
    COMP = {"CSI + CD-1": lat_ev["CD-1"], "CSI + SU-align": lat_ev["SU-align"],
            "position + geometric": t_geo, "position + CNN": t_cnn}

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
                    if t % U == 0:                                  # update instant: compute from this snapshot
                        a_, b_ = A[:, m], B[:, m]
                        if pol == "CSI + CD-1":
                            th = SV.coord_ascent(a_, b_, SV.su_align(a_, b_), sweeps=1, tol=-1)[0]
                        elif pol == "CSI + SU-align":
                            th = SV.su_align(a_, b_)
                        else:
                            pos = traj[:, m] + a.pos_err * perr.standard_normal((U_, 3))
                            if pol == "position + geometric":
                                th = geometric_phase(site, pos)
                            else:
                                with torch.no_grad():
                                    th = phase(net((position_features(site, pos) - ck["mu"]) / ck["sd"]))
                            th = pick_common_phase(th, a_, b_)      # 4 pilots measure the 4 rotations
                        pending.append((t + tp + COMP[pol], th))
                    while pending and pending[0][0] <= t:
                        th_cur = pending.pop(0)[1]
                    in_pilot = (t % U) < tp
                    rates[:, m] = 0.0 if in_pilot else torch.log2(1 + snr * SV.gain(th_cur, A[:, m], B[:, m])).numpy()
                out[pol][U] = rates[:, (GRID >= 100) & (GRID <= 200)].mean(1)
        return out

    val = run(z["val_pos"][:a.users], 11 * s)
    test = run(z["test_pos"][:a.users], 13 * s)
    site_res = dict(load_before_timing=load_t, compute_ms=COMP, policies={})
    best_U = {pol: max(val[pol], key=lambda U: val[pol][U].mean()) for pol in PILOTS}
    for pol in PILOTS:
        site_res["policies"][pol] = dict(best_U_on_val=best_U[pol], test_by_U={str(U): float(v.mean()) for U, v in test[pol].items()},
                                         test=float(test[pol][best_U[pol]].mean()))
    ref = test["CSI + CD-1"][best_U["CSI + CD-1"]]
    for pol in ("position + geometric", "position + CNN", "CSI + SU-align"):
        d = test[pol][best_U[pol]] - ref
        bs = [d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        site_res["policies"][pol]["minus_csi_cd1"] = [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    d = test["position + CNN"][best_U["position + CNN"]] - test["position + geometric"][best_U["position + geometric"]]
    bs = [d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)]
    site_res["cnn_minus_geometric"] = [float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    res["sites"][str(s)] = site_res
    print(f"site {s}: " + " | ".join(f"{p} U={site_res['policies'][p]['best_U_on_val']} {site_res['policies'][p]['test']:.3f}"
                                     for p in PILOTS) + f" | CNN-geom {site_res['cnn_minus_geometric'][0]:+.3f}", flush=True)
    json.dump(res, open(ROOT / "results" / f"{a.tag}.json", "w"), indent=1)
