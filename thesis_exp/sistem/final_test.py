"""
SEALED TEST (PROTOKOL.md + Ek 1). Run ONCE, after FROZEN.md is committed. Calibration seed 12, test seed 41.
Fresh mode: system = controllers.v1b_carrier; baselines K1..K5; oracle K6.
  H1: for each Ki, mean over the 12 conditions of (system - Ki) > 0 (paired bootstrap over scenarios, CI lower > 0).
  H2: in every condition, system is not significantly worse than the best of K1..K5 in that condition (CI upper >= 0).
Periodic mode (P = 20 ms): system = periodic.V4; same baselines on the t = P fresh pipelines.
  H3: for each Ki, mean over conditions of (system - Ki) > 0.
Usage: python3 final_test.py   (expects cube/seed41.npz and cube/warm_seed41.npz built with --final)
-> FINAL.json, FINAL.md
"""
import json, pathlib, subprocess
import numpy as np
import controllers as C
import periodic as Pm
from common import boot
H = pathlib.Path(__file__).resolve().parent
vec = lambda r: np.mean([v[1] for v in r.values()], 0)
res = {}
for mode, (cal, test, sysfn) in {
        "fresh": (C.load(12), C.load(41), C.v1b_carrier),
        "periodic": (Pm.load("", 12), Pm.load("", 41), Pm.V4)}.items():
    m, z = test
    sr = C.evaluate(sysfn, m, z, cal); xs = vec(sr)
    base = {n: C.evaluate(f, m, z, cal) for n, f in C.BASE.items()}
    orc = C.oracle(m, z)
    overall = {n: dict(base_mean=float(vec(r).mean()), diff=float((xs - vec(r)).mean()), ci=boot(xs - vec(r))) for n, r in base.items()}
    per = {}
    for k in sr:
        bn = max(base, key=lambda n: base[n][k][1].mean())
        d = sr[k][1] - base[bn][k][1]
        per[k] = dict(system_pick=sr[k][0], system=float(sr[k][1].mean()), best_baseline=bn, best_baseline_pick=base[bn][k][0],
                      best_baseline_mean=float(base[bn][k][1].mean()), diff=float(d.mean()), ci=boot(d),
                      oracle=float(orc[k][1].mean()), oracle_pick=orc[k][0])
    res[mode] = dict(system_mean=float(xs.mean()), oracle_mean=float(np.mean([v[1].mean() for v in orc.values()])),
                     overall=overall, per_condition=per,
                     H_all_baselines=all(v["ci"][0] > 0 for v in overall.values()),
                     H2_no_condition_worse=all(v["ci"][1] >= 0 for v in per.values()))
res["commit"] = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
json.dump(res, open(H / "FINAL.json", "w"), indent=1)
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
o = ["# Gecikme farkındalıklı RIS denetleyicisi: mühürlü test sonucu (seed 41)", "",
     f"Commit `{res['commit'][:7]}`. Kalibrasyon seed 12, test seed 41 (gece hiç kullanılmadı). Dondurulan sürümler `FROZEN.md`'de. 12 koşul, 400 senaryo; eşli bootstrap 2000, %95.", ""]
for mode, name, hk in (("fresh", "Taze güncelleme kipi (birincil)", "H1"), ("periodic", "Periyodik kip, P = 20 ms (ikincil, Ek 1)", "H3")):
    r = res[mode]
    o += [f"## {name}", "", f"Sistem ortalaması {r['system_mean']:.4f}; kâhin {r['oracle_mean']:.4f} (açık {r['oracle_mean'] - r['system_mean']:.4f}).", "",
          "| Karşılaştırma | Ortalaması | Sistem − karşılaştırma [GA] |", "| --- | --- | --- |"]
    for n, v in r["overall"].items():
        o.append(f"| {n} | {v['base_mean']:.4f} | {v['diff']:+.4f} {ci(v['ci'])} |")
    o += ["", f"- **{hk}** (her karşılaştırmadan anlamlı olarak iyi): {yn(r['H_all_baselines'])}"]
    if mode == "fresh":
        o.append(f"- **H2** (hiçbir koşulda en iyi karşılaştırmadan anlamlı olarak kötü değil): {yn(r['H2_no_condition_worse'])}")
    o += ["", "| Koşul | Sistem seçimi | Sistem | En iyi karşılaştırma | Fark [GA] | Kâhin |", "| --- | --- | --- | --- | --- | --- |"]
    for k, v in r["per_condition"].items():
        o.append(f"| {k} | {v['system_pick']} | {v['system']:.4f} | {v['best_baseline']} ({v['best_baseline_pick']}) {v['best_baseline_mean']:.4f} | {v['diff']:+.4f} {ci(v['ci'])} | {v['oracle']:.4f} ({v['oracle_pick']}) |")
    o.append("")
(H / "FINAL.md").write_text("\n".join(o) + "\n"); print("\n".join(o))
