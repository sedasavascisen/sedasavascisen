"""
Pre-registered validation (ON_KAYIT.md, sections 3-5). Test draw seed 13 (never used before), 400 scenarios.
60 conditions: speed {3, 5.4, 10, 18, 30} km/h x dT {0.33, 1.33, 5.32} ms/step x W {0, 25, 50, 100} ms.
For each (speed, dT, L) a separate aging grid aligned to the deployment instant tau = L*dT + 0.30 ms:
times = [0] + [tau + 0.5 j, j = 0..200]  (t = 0 first -> same scenarios; no interpolation).
W = 0: rate at tau; W > 0: trapezoid mean over [tau, tau + W] on that grid.
Rules: design rule (rule.py, calibration only), (a) L = 48, (b) L = 5, (c) Paper 2 closed form.
Loss_c(rule) = 1 - R(L_rule) / R(L*_c), L*_c = argmax on the test draw.
Paired bootstrap over scenarios (2000, seed 0): mean over conditions of the loss difference.
Output: raw/validation.json
"""
import sys, json, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch
from common import Aging, commit
import rule as RULE
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"
cal = RULE.load()
LSET = cal["LSET"]
SPEEDS_KMH = [3.0, 5.4, 10.0, 18.0, 30.0]
DTS = [0.33, 1.33, 5.32]
WS = [0.0, 25.0, 50.0, 100.0]
lam = 299_792_458.0 / cal["fc_hz"]
t_start = time.time()
R = {}                                              # (kmh, dT, W) -> {L: per-scenario array}
for kmh in SPEEDS_KMH:
    v = kmh / 3.6
    for dT in DTS:
        for L in LSET:
            tau = L * dT + RULE.T0_MS
            times = [0.0] + [round(tau + RULE.GRID_MS * j, 6) for j in range(201)]
            A = Aging(13, times, v=v)
            th = A.adam(A.su_average(), L)
            c = np.stack([A.minrate(th, j + 1).numpy() for j in range(201)], 1)          # [S, 201]
            for W in WS:
                n = int(round(W / RULE.GRID_MS))
                val = c[:, 0] if n == 0 else np.trapezoid(c[:, :n + 1], dx=1.0, axis=1) / n
                R.setdefault((kmh, dT, W), {})[L] = val
            del A
        print(f"{kmh} km/h dT {dT}: done ({time.time() - t_start:.0f} s)", flush=True)

rng = np.random.default_rng(0)
S = len(next(iter(R.values()))[LSET[0]])
IDX = rng.integers(0, S, (2000, S))
conds, rows = list(R), []
for (kmh, dT, W) in conds:
    fd = (kmh / 3.6) / lam
    means = {L: float(R[(kmh, dT, W)][L].mean()) for L in LSET}
    Lstar = max(means, key=means.get)
    pick = {"rule": RULE.predict(cal, dT, fd, W)[0], "L48": 48, "L5": 5, "closed_form": RULE.closed_form(dT, fd, LSET)}
    rows.append(dict(kmh=kmh, dT_ms=dT, W_ms=W, x=dT / 1000 * fd, L_star=Lstar, means=means, pick=pick,
                     loss_pct={k: float(100 * (1 - means[L] / means[Lstar])) for k, L in pick.items()}))


def boot_mean_diff(other, subset):
    """mean over conditions in subset of loss(other) - loss(rule), bootstrap over scenarios (shared indices)."""
    vals = []
    for idx in np.vstack([np.arange(S)[None], IDX]):
        d = []
        for r in subset:
            arr = R[(r["kmh"], r["dT_ms"], r["W_ms"])]
            ref = arr[r["L_star"]][idx].mean()
            d.append(100 * (arr[r["pick"]["rule"]][idx].mean() - arr[r["pick"][other]][idx].mean()) / ref)
        vals.append(np.mean(d))
    return dict(mean=float(vals[0]), ci=[float(np.percentile(vals[1:], 2.5)), float(np.percentile(vals[1:], 97.5))])


losses = np.array([r["loss_pct"]["rule"] for r in rows])
res = dict(commit=commit(), seed=13, conditions=len(rows), rows=rows,
           H1=dict(median_loss_pct=float(np.median(losses)), worst_loss_pct=float(losses.max()),
                   holds=bool(np.median(losses) <= 1.0 and losses.max() <= 3.0)),
           H2={k: boot_mean_diff(k, rows) for k in ("L48", "L5")},
           H3=boot_mean_diff("closed_form", [r for r in rows if r["W_ms"] > 0]),
           seconds=time.time() - t_start)
res["H2"]["holds"] = all(res["H2"][k]["ci"][0] > 0 for k in ("L48", "L5"))
res["H3"]["holds"] = res["H3"]["ci"][0] > 0
json.dump(res, open(OUT / "validation.json", "w"), indent=1)
print("H1", res["H1"], "\nH2", res["H2"], "\nH3", res["H3"], flush=True)
