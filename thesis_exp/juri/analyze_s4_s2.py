"""Decisions for jury questions 4 and 2, exactly as ON_KAYIT_S4_S2.md. raw/s4_s2.json -> raw/s4_s2_summary.json, REPORT_S4_S2.md"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np
from common import boot
H = pathlib.Path(__file__).parent; R = H / "raw"
D = json.load(open(R / "s4_s2.json")); LAT = D["lat"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
SPN = {"3kmh": "3 km/h", "1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
CN = {"fresh": "taze ön kodlayıcı (Makale 2)", "joint": "birlikte eskime (Soru 4)", "clarke": "Clarke kanalı (Soru 2)"}
g = lambda c, s, sp, a: np.asarray(D["data"][f"{c}|{s}|{sp}"][a])
summ = {}
for c in CN:
    for sp in SPN:
        adams = [f"Adam-{L}" for L in STEPS]
        Ls = max(adams, key=lambda a: g(c, 11, sp, a).mean()); Lsel = max(adams, key=lambda a: g(c, 12, sp, a).mean())
        d48 = g(c, 11, sp, "Adam-48") - g(c, 11, sp, Ls)
        cd = max([f"CD-{s}" for s in range(1, 9)], key=lambda a: g(c, 12, sp, a).mean())
        dcd = g(c, 11, sp, cd) - g(c, 11, sp, "SU-best-of")
        best = max(D["data"][f"{c}|12|{sp}"], key=lambda a: g(c, 12, sp, a).mean())
        summ[f"{c}|{sp}"] = dict(L_star=Ls, L_star_latency_ms=LAT[Ls], L_star_eff=float(g(c, 11, sp, Ls).mean()), L_selected_seed12=Lsel,
                                 L48_minus_Lstar=float(d48.mean()), ci48=boot(d48), loss48_pct=float(100 * (1 - g(c, 11, sp, "Adam-48").mean() / g(c, 11, sp, Ls).mean())),
                                 tuned_cd=cd, cd_latency_ms=LAT[cd], cd_minus_sbo=float(dcd.mean()), ci_cd=boot(dcd),
                                 su_best_of_eff=float(g(c, 11, sp, "SU-best-of").mean()), best_arm_seed12=best, best_arm_eff=float(g(c, 11, sp, best).mean()))
h = lambda c: summ[f"{c}|1.5mps"]
dec = dict(S4_H1=h("joint")["ci48"][1] < 0, S4_H2=h("joint")["ci_cd"][1] < 0,
           S2_H1=h("clarke")["ci48"][1] < 0 and h("clarke")["L_star_latency_ms"] <= 200, S2_H2=h("clarke")["ci_cd"][1] < 0)
json.dump(dict(summary=summ, decisions=dec, run_commit=D["commit"]), open(R / "s4_s2_summary.json", "w"), indent=1)
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
o = []; W = o.append
W("# Jüri soruları 4 ve 2 — ön kayıtlı sonuçlar"); W("")
W(f"Rapor commit'i `{commit}`, koşu `{D['commit'][:7]}`. Ön kayıt `ON_KAYIT_S4_S2.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1, "
  "aynı oturumda ölçülmüş gecikmeler (`raw/arms.json` lat_meas). GA: eşli bootstrap 2000, %95.")
W(""); W("## Kararlar (1.5 m/s)"); W("")
W(f"- **S4-H1** (birlikte eskimede L = 48 < L*): {yn(dec['S4_H1'])}")
W(f"- **S4-H2** (birlikte eskimede ayarlı CD < SU-best-of): {yn(dec['S4_H2'])}")
W(f"- **S2-H1** (Clarke kanalında L = 48 < L* ve L* ≤ 200 ms): {yn(dec['S2_H1'])}")
W(f"- **S2-H2** (Clarke kanalında ayarlı CD < SU-best-of): {yn(dec['S2_H2'])}")
W(""); W("## Koşul × hız"); W("")
W("| koşul | hız | L* (gecikme ms) | L* etkin hız | L=48 − L* [GA] | L=48 kaybı % | ayarlı CD − SU-best-of [GA] | seed 12'de en iyi kol |"); W("| --- | --- | --- | --- | --- | --- | --- | --- |")
for c in CN:
    for sp in SPN:
        x = summ[f"{c}|{sp}"]
        W(f"| {CN[c]} | {SPN[sp]} | {x['L_star'].split('-')[1]} ({x['L_star_latency_ms']:.1f}) | {x['L_star_eff']:.3f} | {x['L48_minus_Lstar']:+.3f} {ci(x['ci48'])} | "
          f"{x['loss48_pct']:.1f} | {x['tuned_cd']} {x['cd_minus_sbo']:+.3f} {ci(x['ci_cd'])} | {x['best_arm_seed12']} ({x['best_arm_eff']:.3f}) |")
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W(f"| python3 thesis_exp/juri/s4_s2.py ({D['seconds']/60:.0f} dk) | kanal 12, 11; Clarke inovasyonu 1000·seed + hız indeksi | raw/s4_s2.json, raw/s4_s2.log |")
W("| python3 thesis_exp/juri/analyze_s4_s2.py | bootstrap 0 | raw/s4_s2_summary.json |")
y = H / "yorum_s4_s2.md"
if y.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT_S4_S2.md").write_text("\n".join(o) + "\n"); print("wrote")
