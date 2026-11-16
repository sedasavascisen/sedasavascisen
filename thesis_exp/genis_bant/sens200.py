"""
NOT PRE-REGISTERED sensitivity (written after seeing results.json): restrict every selection to arms whose latency
is <= 200 ms (the channel model's trusted horizon). Same data (raw/curves.json), same selection protocol
(argmax on seed 12, report on seed 11, paired bootstrap from common.boot). Also: G1 and G4 on the cells whose
L* (seed 11, restricted grid) is <= 200 ms. Writes raw/sens200.json.
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np
from common import boot, commit
H = pathlib.Path(__file__).parent; R = H / "raw"
CV = json.load(open(R / "curves.json")); RS = json.load(open(R / "results.json")); G4 = json.load(open(R / "g4.json"))
lat = RS["latency_ms"]; HOR = 200.0
LSET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
out = dict(commit=commit(), horizon_ms=HOR, note="not pre-registered", cells={}, g1=[], g4=[])
for bw in ("20", "50", "100"):
    for sp in ("1.5mps", "10kmh"):
        ev = {k: np.asarray(v) for k, v in CV[f"12|{bw}|{sp}"].items()}
        et = {k: np.asarray(v) for k, v in CV[f"11|{bw}|{sp}"].items()}
        ok = [a for a in ev if lat[a] <= HOR and a != "CD"]
        best = max(ok, key=lambda a: ev[a].mean())
        nb = max([a for a in ok if a.startswith("K1-")], key=lambda a: ev[a].mean())
        d = et[best] - et[nb]
        out["cells"][f"{bw}MHz_{sp}"] = dict(selected=best, latency_ms=lat[best], eff=float(et[best].mean()),
                                            narrowband=nb, minus_narrowband=float(d.mean()), ci=boot(d))
        for k in (1, 4, 16, 64):
            arms = [f"K{k}-L{L}" for L in LSET if lat[f"K{k}-L{L}"] <= HOR]
            if not arms:
                continue
            Ls = max(arms, key=lambda a: et[a].mean())
            Lmax = max(arms, key=lambda a: lat[a])
            dd = et[Lmax] - et[Ls]
            out["g1"].append(dict(cell=f"{bw}MHz_{sp}_K{k}", L_star=Ls, largest_in_horizon=Lmax, diff=float(dd.mean()), ci=boot(dd),
                                  L_star_at_edge=Ls == Lmax))
            g = G4["cells"][f"{bw}MHz_{sp}_K{k}"]
            if lat[f"K{k}-L{g['L_star_test']}"] <= HOR:
                out["g4"].append(dict(cell=f"{bw}MHz_{sp}_K{k}", L_rule=g["L_rule"], L_star=g["L_star_test"], loss_pct=g["loss_pct"],
                                      rule_in_horizon=lat[f"K{k}-L{g['L_rule']}"] <= HOR))
        c = out["cells"][f"{bw}MHz_{sp}"]
        print(f"{bw} MHz {sp}: selected<=200ms {c['selected']} ({c['latency_ms']:.1f} ms) {c['eff']:.3f}; "
              f"- narrowband {nb}: {c['minus_narrowband']:+.3f} {c['ci']}", flush=True)
L = [x["loss_pct"] for x in out["g4"]]
print("G4 on cells with L* <= 200 ms:", len(L), "median", np.median(L), "max", max(L))
print("G1 (largest in-horizon L vs L*):", sum(x["ci"][1] < 0 for x in out["g1"]), "/", len(out["g1"]), "significant;",
      sum(x["L_star_at_edge"] for x in out["g1"]), "at the in-horizon edge")
json.dump(out, open(R / "sens200.json", "w"), indent=1)
print("wrote", flush=True)
