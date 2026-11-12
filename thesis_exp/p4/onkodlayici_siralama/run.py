"""
Follow-up to Prompt 4.3 — does the method RANKING survive when precoder-refresh pilots are charged?

Same model as thesis_exp/p4/onkodlayici_pilot/run.py (ZF refreshed every R ms from a perfect effective-
channel estimate, K = 4 pilot symbols per refresh charged as the data fraction 1 - t_p/R, RIS phase from
the t = 0 channel deployed at the arm's latency, time-averaged min-user rate over [lat, lat + 50 ms]),
now for EVERY arm of the paper's aging comparison:
  SU-average, SU-best-of, SU-average + Adam-L (L in STEPS, step 0.5), CD (baselines.coord_descent
  defaults), PGA (baselines.pga defaults).
Latencies: one-thread rerun (thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json); Adam-L
interpolated in L as in common.adam_latency.
No weak baseline: per arm and numerology, the refresh period R is chosen on the validation mobility draw
(seed 12) and reported on the aging set (seed 11). The best arm per numerology is also chosen on seed 12.
Paired bootstrap (2000, 95%) of every arm against SU-best-of and against the selected arm.
The 'fresh' column (W recomputed at every grid point, no pilot cost) reproduces the paper's assumption.
Scenarios: the mobile generator's random stream does not depend on the time grid when t = 0 is the first
entry (common.py), so each arm gets its own window grid [0] + [lat, lat + 50] at 0.1 ms, built separately to
bound memory; check_same_scenarios verifies the t = 0 scenario identity for every grid.
Output: thesis_exp/p4/onkodlayici_siralama/raw/results.json
"""
import sys, os, json, math, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, adam_latency, LAT, STEPS, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S, baselines as B
torch.set_num_threads(int(os.environ.get("THREADS", "2")))
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
DT, WIN = 0.1, 50.0
R_GRID = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
SYM_MS = {"15kHz": 3.43 / 48, "30kHz": 1.71 / 48, "60kHz": 0.86 / 48}
K_PILOTS = 4
PROBE = os.environ.get("PROBE") == "1"

ARMS = {"SU-average": LAT["su_average"], "SU-best-of": LAT["su_best_of"],
        **{f"Adam-{L}": adam_latency(L) for L in STEPS}, "CD": LAT["cd"], "PGA": LAT["pga"]}


def window(lat):
    t0 = math.floor(lat / DT) * DT
    w = [round(t0 + k * DT, 4) for k in range(int(round(WIN / DT)) + 2)]
    return [0.0] + [t for t in w if t > 0.0]


def evaluate(A, th, lat):
    """per-scenario arrays: fresh, never, and charged[num][R]."""
    idx = {t: A.idx(t) for t in A.times}
    sel = [t for t in A.times if lat - 1e-9 <= t <= lat + WIN + 1e-9 and (t > 0.0 or lat == 0.0)]
    near = lambda t: idx[min(A.times[1:] if len(A.times) > 1 else A.times, key=lambda s: abs(s - t))]
    c, s = torch.cos(th), torch.sin(th)
    He = {}
    def he(m):
        if m not in He:
            He[m] = S.effective_channel(A.F, A.G[m], A.H[m], c, s)
        return He[m]
    Wc = {}
    def W(m):
        if m not in Wc:
            Wc[m] = S.precode(he(m), A.pt, "zf", noise_var=A.nv)
        return Wc[m]
    rate = lambda m, mr: torch.log2(1.0 + S.sinr(he(m), W(mr), A.nv)).min(-1).values.numpy()
    m_dep = near(lat)
    fresh = np.stack([rate(idx[t], idx[t]) for t in sel], 1).mean(1)
    never = np.stack([rate(idx[t], m_dep) for t in sel], 1).mean(1)
    charged = {}
    for num, sym in SYM_MS.items():
        tp = K_PILOTS * sym
        charged[num] = {}
        for Rr in R_GRID:
            vals = [rate(idx[t], near(lat + math.floor((t - lat) / Rr + 1e-9) * Rr)) for t in sel]
            charged[num][Rr] = np.stack(vals, 1).mean(1) * max(0.0, 1.0 - tp / Rr)
    return dict(fresh=fresh, never=never, charged=charged)


def phases_and_eval(seed, arms):
    out = {}
    for name in arms:
        lat = ARMS[name]
        t1 = time.time()
        A = Aging(seed, window(lat))
        chk = check_same_scenarios(A) if seed == 11 else None
        m0 = A.idx(0.0)
        if name == "SU-average":
            th = A.su_average()
        elif name == "SU-best-of":
            th = A.su_best_of()
        elif name.startswith("Adam-"):
            th = A.adam(A.su_average(), int(name[5:]))
        elif name == "CD":
            th = B.coord_descent(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1]
        elif name == "PGA":
            th = B.pga(A.F, A.G[m0], A.H[m0], A.pt, A.nv)[1]
        out[name] = evaluate(A, th, lat)
        out[name]["check"] = chk
        print(f"  seed {seed} {name}: lat {lat:.2f} ms, fresh {out[name]['fresh'].mean():.4f}, {time.time() - t1:.1f} s", flush=True)
        del A
    return out


arms = ["SU-best-of", "Adam-6"] if PROBE else list(ARMS)
t_start = time.time()
val = phases_and_eval(12, arms)
test = phases_and_eval(11, arms)
res = dict(commit=commit(), window_ms=WIN, grid_ms=DT, pilots_per_refresh=K_PILOTS, symbol_ms=SYM_MS, R_grid=R_GRID,
           latency_ms=ARMS, threads=torch.get_num_threads(), probe=PROBE, numerologies={}, fresh={}, never={})
ref = "SU-best-of"
fr_v = {k: v["fresh"].mean() for k, v in val.items()}
best_fresh = max(fr_v, key=fr_v.get)
res["fresh"] = dict(selected_on_val=best_fresh,
                    rows={k: dict(rate=float(test[k]["fresh"].mean()), ci=boot(test[k]["fresh"]),
                                  minus_su_best_of=float((test[k]["fresh"] - test[ref]["fresh"]).mean()),
                                  minus_su_best_of_ci=boot(test[k]["fresh"] - test[ref]["fresh"])) for k in test})
res["never"] = {k: float(test[k]["never"].mean()) for k in test}
for num in SYM_MS:
    rows, pick_v = {}, {}
    for k in test:
        Rk = max(R_GRID, key=lambda r: val[k]["charged"][num][r].mean())
        pick_v[k] = (Rk, val[k]["charged"][num][Rk].mean())
        rows[k] = dict(R_selected_on_val=Rk, x=test[k]["charged"][num][Rk])
    best = max(pick_v, key=lambda k: pick_v[k][1])
    xb, xr = rows[best]["x"], rows[ref]["x"]
    res["numerologies"][num] = dict(
        selected_on_val=best,
        rows={k: dict(R_selected_on_val=r["R_selected_on_val"], rate=float(r["x"].mean()), ci=boot(r["x"]),
                      minus_su_best_of=float((r["x"] - xr).mean()), minus_su_best_of_ci=boot(r["x"] - xr),
                      minus_selected=float((r["x"] - xb).mean()), minus_selected_ci=boot(r["x"] - xb),
                      test_rate_by_R={str(R): float(test[k]["charged"][num][R].mean()) for R in R_GRID})
              for k, r in rows.items()})
    print(f"{num}: selected {best} (R {pick_v[best][0]} ms) test {xb.mean():.4f}; SU-best-of {xr.mean():.4f}", flush=True)
res["seconds"] = time.time() - t_start
json.dump(res, open(OUT / ("probe.json" if PROBE else "results.json"), "w"), indent=1)
print("wrote", flush=True)
