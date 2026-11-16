"""
Wideband OFDM experiment (PLAN.md, ON_KAYIT.md). Two parts:

  --part timing  idle machine (load < 0.5), one thread, one scenario: Adam-L call time for K_opt in {1,4,16,64}
                 and L in {1, 4, 16} (linear fit a + b L, used for every L), 20 scenarios x 20 reps x 3 rounds,
                 median over scenarios, median over rounds; load before/after. -> raw/timing.json
  --part curves  for seed in (12 selection, 11 report), B in {20, 50, 100} MHz, speed in {1.5 m/s, 10 km/h}:
                 phases from the t = 0 channel (identical for every speed), then the minimum wideband user rate
                 at each arm's exact latency (Definition 1), evaluated on grids [0, tau_1..tau_8] (t = 0 first).
                 Arms: SU-best-of (fc; latency 1.63 ms, one-thread rerun), CD (fc, default sweeps; 702.97 ms),
                 SU-average + Adam-L on the K_opt objective (step 0.5), latency = 0.30 ms + fit(K_opt, L).
                 -> raw/curves.json (per-scenario arrays) and raw/results.json (summary, bootstrap)
"""
import sys, os, json, time, argparse, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np, torch
import wb as WBM
from wb import WB, KOPTS, commit
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
from common import LAT, boot
H = pathlib.Path(__file__).parent; OUT = H / "raw"; OUT.mkdir(exist_ok=True)
ap = argparse.ArgumentParser(); ap.add_argument("--part", choices=("timing", "curves"), required=True)
a = ap.parse_args()
LSET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
BWS = [20e6, 50e6, 100e6]
SPEEDS = {"1.5mps": 1.5, "10kmh": 10 / 3.6}
T0 = LAT["su_average"]

if a.part == "timing":
    load0 = os.getloadavg()[0]
    while os.getloadavg()[0] >= 0.5:
        time.sleep(15)
    load1 = os.getloadavg()[0]
    torch.set_num_threads(1)
    w = WB(11, [0.0], 50e6, n=20)

    class View:                                   # one-scenario view of w
        def __init__(s, i):
            sl = slice(i, i + 1)
            for k in ("F", "G0", "H0", "Ff"):
                setattr(s, k, getattr(w, k)[sl])
            s.Gtf, s.Htf, s.pt, s.nv = w.Gtf[sl], w.Htf[sl], w.pt, w.nv
        user_rates, _obj_rates, adam, su_average = WB.user_rates, WB._obj_rates, WB.adam, WB.su_average
    res = dict(commit=commit(), torch=torch.__version__, threads=1, load=dict(start=load0, before=load1), arms={})
    for k in KOPTS:
        for L in (1, 4, 16):
            rounds = []
            for r in range(3):
                per = []
                for i in range(20):
                    v_ = View(i)
                    f = lambda: v_.adam(v_.su_average(), L, k)
                    f(); f(); t = []
                    for _ in range(20):
                        t0 = time.perf_counter(); f(); t.append(time.perf_counter() - t0)
                    per.append(np.median(t) * 1e3)
                rounds.append(float(np.median(per)))
            res["arms"][f"K{k}_L{L}"] = dict(rounds_ms=rounds, median_ms=float(np.median(rounds)))
            print(f"K_opt {k} L {L}: {res['arms'][f'K{k}_L{L}']['median_ms']:.3f} ms {rounds}", flush=True)
        y = [res["arms"][f"K{k}_L{L}"]["median_ms"] for L in (1, 4, 16)]
        b, a0 = np.polyfit([1, 4, 16], y, 1)
        res[f"fit_K{k}"] = dict(intercept_ms=float(a0), per_step_ms=float(b))
    res["load"]["after"] = os.getloadavg()[0]
    json.dump(res, open(OUT / "timing.json", "w"), indent=1)
    print("wrote timing", flush=True)
    sys.exit(0)

# ------------------------------------------------------------------------------------------- curves
torch.set_num_threads(2)
TM = json.load(open(OUT / "timing.json"))
lat = {"SU-best-of": LAT["su_best_of"], "CD": LAT["cd"]}
for k in KOPTS:
    f = TM[f"fit_K{k}"]
    for L in LSET:
        lat[f"K{k}-L{L}"] = T0 + f["intercept_ms"] + f["per_step_ms"] * L
t_start = time.time()
EFF = {}                                                   # (seed, bw, speed) -> {arm: per-scenario array}
for seed in (12, 11):
    for bw in BWS:
        w0 = WB(seed, [0.0], bw)
        su = w0.su_average()
        PH = {"SU-best-of": w0.su_best_of(), "CD": w0.cd(8)}
        for k in KOPTS:
            for L in LSET:
                PH[f"K{k}-L{L}"] = w0.adam(su, L, k)
        T0rate = {arm: float(w0.minrate(th, 0).mean()) for arm, th in PH.items()}
        del w0
        print(f"seed {seed} B {bw/1e6:g} MHz: phases done ({time.time() - t_start:.0f} s)", flush=True)
        arms = sorted(PH, key=lambda x: lat[x])
        for sp, v in SPEEDS.items():
            out = {}
            for i in range(0, len(arms), 8):
                grp = arms[i:i + 8]
                times = [0.0] + [lat[x] for x in grp]
                w = WB(seed, times, bw, v=v)
                for j, x in enumerate(grp):
                    out[x] = w.minrate(PH[x], j + 1).numpy()
                del w
            EFF[(seed, bw, sp)] = dict(eff=out, t0=T0rate)
            print(f"  {sp}: done ({time.time() - t_start:.0f} s)", flush=True)

summary = dict(commit=commit(), latency_ms=lat, timing_source="raw/timing.json", cells={})
for bw in BWS:
    for sp in SPEEDS:
        ev, et = EFF[(12, bw, sp)]["eff"], EFF[(11, bw, sp)]["eff"]
        best = max(ev, key=lambda x: ev[x].mean())
        nb_best = max([x for x in ev if x.startswith("K1-")], key=lambda x: ev[x].mean())
        ref = et["SU-best-of"]
        cell = dict(selected_on_val=best, narrowband_selected_on_val=nb_best,
                    selected=dict(eff=float(et[best].mean()), minus_su_best_of=float((et[best] - ref).mean()), ci=boot(et[best] - ref)),
                    selected_minus_narrowband=dict(diff=float((et[best] - et[nb_best]).mean()), ci=boot(et[best] - et[nb_best])),
                    cd_minus_selected=dict(diff=float((et["CD"] - et[best]).mean()), ci=boot(et["CD"] - et[best])),
                    by_kopt={})
        for k in KOPTS:
            arms = [f"K{k}-L{L}" for L in LSET]
            Ls = max(arms, key=lambda x: et[x].mean())
            d48 = et[f"K{k}-L48"] - et[Ls]
            cell["by_kopt"][str(k)] = dict(L_star_test=Ls, eff_L_star=float(et[Ls].mean()), latency_L_star=lat[Ls],
                                           L48_minus_Lstar=float(d48.mean()), ci=boot(d48),
                                           loss_L48_pct=float(100 * (1 - et[f"K{k}-L48"].mean() / et[Ls].mean())),
                                           t0_L_star=EFF[(11, bw, sp)]["t0"][Ls])
        summary["cells"][f"{bw/1e6:g}MHz_{sp}"] = cell
        print(f"B {bw/1e6:g} MHz {sp}: selected {best} {et[best].mean():.4f}; narrowband {nb_best}; "
              f"sel-nb {cell['selected_minus_narrowband']['diff']:+.4f} {cell['selected_minus_narrowband']['ci']}", flush=True)
summary["seconds"] = time.time() - t_start
json.dump(summary, open(OUT / "results.json", "w"), indent=1)
json.dump({f"{s}|{bw/1e6:g}|{sp}": {k: v.tolist() for k, v in d["eff"].items()} for (s, bw, sp), d in EFF.items()},
          open(OUT / "curves.json", "w"))
print("wrote", flush=True)
