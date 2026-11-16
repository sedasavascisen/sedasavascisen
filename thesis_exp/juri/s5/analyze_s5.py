"""Decisions for jury question 5, exactly as ON_KAYIT_S5.md. s5/raw/eval.json -> s5/raw/s5_summary.json, ../REPORT_S5.md"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "p4"))
import numpy as np
from common import boot
H = pathlib.Path(__file__).parent; R = H / "raw"
D = json.load(open(R / "eval.json")); LAT = D["lat"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
CLASSIC = ["SU-average", "SU-best-of"] + [f"Adam-{L}|{s}" for L in STEPS for s in ("avg", "best")] + [f"CD-{s}" for s in range(1, 9)]
HYB = [f"NN+Adam-{L}" for L in STEPS]
SPN = {"1.5mps": "1.5 m/s", "3kmh": "3 km/h"}
e = lambda fc, s, sp, a: np.asarray(D["data"][f"{fc}|{s}|{sp}"]["eff"][a])
z = lambda fc, s, sp, a: np.asarray(D["data"][f"{fc}|{s}|{sp}"]["t0"][a])
out = {}
for fc in (28, 3):
    for sp in SPN:
        bc = max(CLASSIC, key=lambda a: e(fc, 12, sp, a).mean()); bh = max(HYB, key=lambda a: e(fc, 12, sp, a).mean())
        ref = e(fc, 11, sp, bc)
        c = dict(best_classic=bc, best_classic_latency=LAT[bc], best_classic_eff=float(ref.mean()), best_hybrid=bh, hybrid_latency=LAT[bh],
                 fd_hz=D["data"][f"{fc}|11|{sp}"]["fd_hz"], arms={})
        for a in ["NN-sincos", "NN-angle", "NN-untrained", bh, "SU-best-of"]:
            if a in D["data"][f"{fc}|11|{sp}"]["eff"]:
                d = e(fc, 11, sp, a) - ref
                c["arms"][a] = dict(eff=float(e(fc, 11, sp, a).mean()), t0=float(z(fc, 11, sp, a).mean()), latency=LAT[a],
                                    minus_best_classic=float(d.mean()), ci=boot(d))
        dz = z(fc, 11, sp, "NN-sincos") - z(fc, 11, sp, "NN-untrained")
        c["trained_minus_untrained_t0"] = dict(diff=float(dz.mean()), ci=boot(dz))
        if fc == 28:
            for kind, f in (("t0", z), ("eff", e)):
                d = f(fc, 11, sp, "NN-sincos") - f(fc, 11, sp, "NN-angle")
                c[f"sincos_minus_angle_{kind}"] = dict(diff=float(d.mean()), ci=boot(d))
        out[f"{fc}|{sp}"] = c
m = out["28|1.5mps"]
dec = dict(S5_H1=m["arms"]["NN-sincos"]["ci"][0] > 0, S5_H2=m["arms"][m["best_hybrid"]]["ci"][0] > 0,
           S5_H3=m["trained_minus_untrained_t0"]["ci"][0] > 0)
json.dump(dict(summary=out, decisions=dec, eval_commit=D["commit"], nn_latency=D["nn_latency"]), open(R / "s5_summary.json", "w"), indent=1)
tr = {k: json.load(open(R / f"train_{k}.json")) for k in ("28_sincos", "28_angle", "3_sincos")}
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
o = []; W = o.append
W("# Jüri sorusu 5 — öğrenmeye en elverişli rejimde kesin test (ön kayıtlı)"); W("")
W(f"Rapor commit'i `{commit}`, değerlendirme `{D['commit'][:7]}`. Ön kayıt `ON_KAYIT_S5.md`. Seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1. "
  f"Ağ çıkarımı {D['nn_latency']['median_ms']:.3f} ms (tek iş parçacığı, toplu 1; turlar {', '.join(f'{x:.3f}' for x in D['nn_latency']['rounds_ms'])}). "
  f"28 GHz bağlantı bütçesi telafisi {json.load(open(R / 'link_budget.json'))['comp_db']:.2f} dB (eğitim tohumu 21).")
W(""); W("## Kararlar (28 GHz, 1.5 m/s)"); W("")
a = m["arms"]
W(f"- **S5-H1** (NN-sincos − en iyi klasik > 0): {a['NN-sincos']['minus_best_classic']:+.3f} {ci(a['NN-sincos']['ci'])} → {yn(dec['S5_H1'])}")
W(f"- **S5-H2** (en iyi NN+Adam-L − en iyi klasik > 0): {m['best_hybrid']} {a[m['best_hybrid']]['minus_best_classic']:+.3f} {ci(a[m['best_hybrid']]['ci'])} → {yn(dec['S5_H2'])}")
W(f"- **S5-H3** (t = 0'da eğitilmiş − eğitilmemiş > 0): {m['trained_minus_untrained_t0']['diff']:+.3f} {ci(m['trained_minus_untrained_t0']['ci'])} → {yn(dec['S5_H3'])}")
W(f"- En iyi klasik kol (seed 12): {m['best_classic']} ({m['best_classic_latency']:.2f} ms), etkin hız {m['best_classic_eff']:.3f}")
W(""); W("## Bütün hücreler"); W("")
W("| fc | hız | f_d (Hz) | en iyi klasik (ms) | etkin hız | kol | gecikme (ms) | t = 0 hızı | etkin hız | − en iyi klasik [GA] |"); W("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for k, c in out.items():
    fc, sp = k.split("|")
    for arm, x in c["arms"].items():
        W(f"| {fc} GHz | {SPN[sp]} | {c['fd_hz']:.0f} | {c['best_classic']} ({c['best_classic_latency']:.2f}) | {c['best_classic_eff']:.3f} | {arm} | {x['latency']:.2f} | {x['t0']:.3f} | {x['eff']:.3f} | {x['minus_best_classic']:+.3f} {ci(x['ci'])} |")
W(""); W("## Keşifsel"); W("")
for sp in SPN:
    c = out[f"28|{sp}"]
    W(f"- **S5-E1, 28 GHz {SPN[sp]}** (sin/cos − doğrudan açı): t = 0'da {c['sincos_minus_angle_t0']['diff']:+.3f} {ci(c['sincos_minus_angle_t0']['ci'])}, "
      f"etkin hızda {c['sincos_minus_angle_eff']['diff']:+.3f} {ci(c['sincos_minus_angle_eff']['ci'])}")
for k in ("3|1.5mps", "3|3kmh", "28|3kmh"):
    c = out[k]; x = c["arms"]["NN-sincos"]; y = c["arms"][c["best_hybrid"]]
    W(f"- **S5-E2, {k.split('|')[0]} GHz {SPN[k.split('|')[1]]}:** NN-sincos − en iyi klasik {x['minus_best_classic']:+.3f} {ci(x['ci'])}; "
      f"{c['best_hybrid']} − en iyi klasik {y['minus_best_classic']:+.3f} {ci(y['ci'])}; eğitilmiş − eğitilmemiş (t = 0) {c['trained_minus_untrained_t0']['diff']:+.3f} {ci(c['trained_minus_untrained_t0']['ci'])}")
W(""); W("## Eğitim"); W("")
W("| model | en iyi doğrulama min-hızı | epoch | süre (s) |"); W("| --- | --- | --- | --- |")
for k, t in tr.items():
    h = t["history"]; be = max(h, key=lambda r: r["val"])
    W(f"| {k} | {t['best_val']:.4f} | {be['epoch']} / {h[-1]['epoch']} | {h[-1].get('seconds', 0):.0f} |")
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/juri/s5/link_budget.py | kanal 21 | s5/raw/link_budget.json |")
W("| python3 thesis_exp/juri/s5/train.py --fc {28,3} --head {sincos,angle} | eğitim 21, doğrulama 12, model 0 | s5/raw/net_*.pt, train_*.json, train_*.log |")
W(f"| python3 thesis_exp/juri/s5/eval_s5.py ({D['seconds']/60:.0f} dk) | kanal 12, 11 | s5/raw/eval.json, eval.log |")
W("| python3 thesis_exp/juri/s5/analyze_s5.py | bootstrap 0 | s5/raw/s5_summary.json |")
y = H.parent / "yorum_s5.md"
if y.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H.parent / "REPORT_S5.md").write_text("\n".join(o) + "\n"); print("wrote")
