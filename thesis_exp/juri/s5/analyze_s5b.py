"""Decisions for S5b, exactly as ON_KAYIT_S5b.md. s5/raw/eval_s5b.json + eval.json -> s5/raw/s5b_summary.json, ../REPORT_S5b.md"""
import sys, json, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "p4"))
import numpy as np
from common import boot
H = pathlib.Path(__file__).parent; R = H / "raw"
E0 = json.load(open(R / "eval.json")); E = json.load(open(R / "eval_s5b.json")); S5 = json.load(open(R / "s5_summary.json"))["summary"]
SPN = {"1.5mps": "1.5 m/s", "3kmh": "3 km/h"}
SIN = ["sincos_b0", "sincos_b1", "sincos_b2", "sincos_w128"]
c0 = lambda s, sp, a: np.asarray(E0["data"][f"28|{s}|{sp}"]["eff"][a])
n_ = lambda s, sp, a: np.asarray(E["data"][f"{s}|{sp}"]["eff"][a])
z_ = lambda s, sp, a: np.asarray(E["data"][f"{s}|{sp}"]["t0"][a])
out = {}
for sp in SPN:
    bc = S5[f"28|{sp}"]["best_classic"]; ref = c0(11, sp, bc); sa = c0(11, sp, "SU-average")
    sel = max(SIN, key=lambda k: n_(12, sp, k).mean())
    hy = max([k for k in E["data"][f"12|{sp}"]["eff"] if "+Adam-" in k], key=lambda k: n_(12, sp, k).mean())
    rows = {}
    for k in SIN + ["angle_b0", "angle_b1", "angle_b2", hy]:
        x = n_(11, sp, k)
        rows[k] = dict(latency=E["lat"][k], t0=float(z_(11, sp, k).mean()), eff=float(x.mean()),
                       minus_best_classic=float((x - ref).mean()), ci_bc=boot(x - ref), minus_su_average=float((x - sa).mean()), ci_sa=boot(x - sa))
    pairs = {}
    for s in range(3):
        d = n_(11, sp, f"sincos_b{s}") - n_(11, sp, f"angle_b{s}")
        dz = z_(11, sp, f"sincos_b{s}") - z_(11, sp, f"angle_b{s}")
        pairs[str(s)] = dict(eff=float(d.mean()), ci=boot(d), t0=float(dz.mean()), ci_t0=boot(dz))
    out[sp] = dict(best_classic=bc, best_classic_eff=float(ref.mean()), su_average_eff=float(sa.mean()), selected=sel, hybrid=hy, rows=rows, pairs=pairs)
m = out["1.5mps"]
dec = dict(S5b_H1=m["rows"][m["selected"]]["ci_bc"][0] > 0, S5b_H2=m["rows"][m["selected"]]["ci_sa"][0] > 0,
           S5b_H3=sum(p["ci"][0] > 0 for p in m["pairs"].values()) >= 2)
json.dump(dict(summary=out, decisions=dec, eval_commit=E["commit"], w128_latency=E["w128_latency"]), open(R / "s5b_summary.json", "w"), indent=1)
tr = {k: json.load(open(R / f"train_28_{k}.json")) for k in SIN + ["angle_b0", "angle_b1", "angle_b2"]}
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
o = []; W = o.append
W("# Soru 5b — daha büyük veri ve birden fazla tohumla sağlamlık (ön kayıtlı)"); W("")
W(f"Rapor commit'i `{commit}`, değerlendirme `{E['commit'][:7]}`. Ön kayıt `ON_KAYIT_S5b.md`. 28 GHz, eğitim n = 80 000, seçim seed 12, rapor seed 11, 400 senaryo, Tanım 1. "
  f"Genişlik-128 ağın gecikmesi {E['w128_latency']['median_ms']:.3f} ms (turlar {', '.join(f'{x:.3f}' for x in E['w128_latency']['rounds_ms'])}); genişlik 64 için {E0['nn_latency']['median_ms']:.3f} ms (S5).")
W(""); W("## Kararlar (28 GHz, 1.5 m/s)"); W("")
s = m["rows"][m["selected"]]
W(f"- **S5b-H1** (seçilen ağ {m['selected']} − en iyi klasik {m['best_classic']}): {s['minus_best_classic']:+.3f} {ci(s['ci_bc'])} → {yn(dec['S5b_H1'])}")
W(f"- **S5b-H2** (seçilen ağ − SU-average): {s['minus_su_average']:+.3f} {ci(s['ci_sa'])} → {yn(dec['S5b_H2'])}")
W(f"- **S5b-H3** (sin/cos − doğrudan açı, etkin hız; 3 tohumun ≥ 2'sinde anlamlı): " + "; ".join(f"tohum {k}: {p['eff']:+.3f} {ci(p['ci'])}" for k, p in m["pairs"].items()) + f" → {yn(dec['S5b_H3'])}")
for sp in SPN:
    x = out[sp]
    W(""); W(f"## {SPN[sp]} — en iyi klasik {x['best_classic']} ({x['best_classic_eff']:.3f}), SU-average ({x['su_average_eff']:.3f})"); W("")
    W("| ağ | gecikme (ms) | t = 0 | etkin hız | − en iyi klasik [GA] | − SU-average [GA] |"); W("| --- | --- | --- | --- | --- | --- |")
    for k, r in x["rows"].items():
        W(f"| {k}{' (seçilen)' if k == x['selected'] else ''} | {r['latency']:.2f} | {r['t0']:.3f} | {r['eff']:.3f} | {r['minus_best_classic']:+.3f} {ci(r['ci_bc'])} | {r['minus_su_average']:+.3f} {ci(r['ci_sa'])} |")
    W(""); W("sin/cos − doğrudan açı (aynı tohum): " + "; ".join(f"tohum {k}: t = 0 {p['t0']:+.3f} {ci(p['ci_t0'])}, etkin {p['eff']:+.3f} {ci(p['ci'])}" for k, p in x["pairs"].items()))
W(""); W("## Eğitim"); W("")
W("| model | en iyi doğrulama | epoch | süre (s) |"); W("| --- | --- | --- | --- |")
for k, t in tr.items():
    h = t["history"]; be = max(h, key=lambda r: r["val"])
    W(f"| {k} | {t['best_val']:.4f} | {be['epoch']} / {h[-1]['epoch']} | {h[-1].get('seconds', 0):.0f} |")
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| thesis_exp/juri/s5/chain_s5b.sh (train.py --fc 28 --n 80000 --seed {0,1,2} [--width 128]) | eğitim 21, doğrulama 12, model 0/1/2 | s5/raw/net_28_*_b*.pt, *_w128.pt, train_28_*.json/.log |")
W("| python3 thesis_exp/juri/s5/eval_s5b.py | kanal 12, 11 | s5/raw/eval_s5b.json, eval_s5b.log |")
W("| python3 thesis_exp/juri/s5/analyze_s5b.py | bootstrap 0 | s5/raw/s5b_summary.json |")
y = H.parent / "yorum_s5b.md"
if y.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H.parent / "REPORT_S5b.md").write_text("\n".join(o) + "\n"); print("wrote")
