"""
Independent numerical audit of thesis_exp/juri/REPORT_S5.md (+ yorum_s5.md), jury question 5.
Recomputes ONLY from raw JSON (no channel generation, no training): s5/raw/eval.json (per-scenario arrays),
train_*.json, link_budget.json, ../raw/timing.json, ../raw/timing2.json; s5_summary.json only for a consistency
check. Untrained/trained checkpoints are loaded (weights only, no forward pass) to check "untrained is untrained".
Own bootstrap: numpy default_rng(20261116), 2000 paired resamples, percentile 95 %.
Reported values are parsed from REPORT_S5.md (tables and decision lines); yorum numbers are listed by hand.
Run: nice -n 19 python3 thesis_exp/denetim_log/juri_s5_denetim.py   (single process, a few seconds)
"""
import json, pathlib, re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
J = ROOT / "thesis_exp/juri"; R5 = J / "s5/raw"
rng = np.random.default_rng(20261116)
ROWS = []


def boot(d, n=2000):
    idx = rng.integers(0, len(d), (n, len(d)))
    m = d[idx].mean(1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


def chk(name, rep, got, tol):
    if isinstance(rep, str) or isinstance(got, str):
        ok = str(rep) == str(got)
    else:
        a, b = np.atleast_1d(rep).astype(float), np.atleast_1d(got).astype(float)
        ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= tol + 1e-12))
    fmt = lambda x: x if isinstance(x, str) else ("[" + ", ".join(f"{v:+.3f}" for v in x) + "]"
                                                   if isinstance(x, (list, tuple)) else f"{x:.4g}")
    ROWS.append((name, fmt(rep), fmt(got), "OK" if ok else "HATA"))
    return ok


D = json.load(open(R5 / "eval.json")); LAT = D["lat"]
T2 = json.load(open(J / "raw/timing2.json"))["median_ms"]; T1 = json.load(open(J / "raw/timing.json"))["median_ms"]
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
CLASSIC = ["SU-average", "SU-best-of"] + [f"Adam-{L}|{s}" for L in STEPS for s in ("avg", "best")] + \
          [f"CD-{s}" for s in range(1, 9)]
HYB = [f"NN+Adam-{L}" for L in STEPS]
SPN = {"1.5mps": "1.5 m/s", "3kmh": "3 km/h"}
e = lambda fc, s, sp, a: np.asarray(D["data"][f"{fc}|{s}|{sp}"]["eff"][a], float)
z = lambda fc, s, sp, a: np.asarray(D["data"][f"{fc}|{s}|{sp}"]["t0"][a], float)

# ---------------------------------------------------------------- structural sanity of the raw file
for k, c in D["data"].items():
    for a in c["eff"]:
        assert len(c["eff"][a]) == 400 and len(c["t0"][a]) == 400, (k, a)
for fc in (28, 3):
    for s in (12, 11):
        t1, t2 = D["data"][f"{fc}|{s}|1.5mps"]["t0"], D["data"][f"{fc}|{s}|3kmh"]["t0"]
        chk(f"t0 dizileri hızdan bağımsız ({fc} GHz, seed {s})", "aynı",
            "aynı" if all(t1[a] == t2[a] for a in t1) else "farklı", 0)

# ---------------------------------------------------------------- latencies
ML = {L: T2[f"adam{L}"] for L in (1, 2, 4, 8, 16, 32, 48)}
adam = lambda L: float(np.interp(L, sorted(ML), [ML[x] for x in sorted(ML)]))
NN = float(np.median(D["nn_latency"]["rounds_ms"]))
chk("NN gecikmesi (ms, tur medyanı)", 0.425, NN, 5e-4)
chk("NN turları (ms)", [0.463, 0.425, 0.418, 0.420, 0.440], D["nn_latency"]["rounds_ms"], 5e-4)
exp_lat = {"SU-average": T2["su_average"], "SU-best-of": T2["su_best_of"],
           **{f"Adam-{L}|avg": T2["su_average"] + adam(L) for L in STEPS},
           **{f"Adam-{L}|best": T2["su_best_of"] + adam(L) for L in STEPS},
           **{f"CD-{s}": T1[f"cd{s}"] for s in range(1, 9)},
           "NN-sincos": NN, "NN-angle": NN, "NN-untrained": NN, **{f"NN+Adam-{L}": NN + adam(L) for L in STEPS}}
bad = [k for k in exp_lat if abs(exp_lat[k] - LAT[k]) > 1e-9]
chk("eval.json gecikme defteri = başlangıç + adam(L) (tüm kollar)", "0 sapma", f"{len(bad)} sapma", 0)

# ---------------------------------------------------------------- link budget
lb = json.load(open(R5 / "link_budget.json"))
chk("telafi comp_db = 10 log10(P3/P28)", 30.79, 10 * np.log10(lb["P3"] / lb["P28"]), 0.005)
chk("telafi tohumu (eğitim)", "21", str(lb["seed"]), 0)

# ---------------------------------------------------------------- parse the report
rep = (J / "REPORT_S5.md").read_text()
cells = {}
for line in rep.splitlines():
    m = re.match(r"\| (\d+) GHz \| ([^|]+) \| (\d+) \| (\S+) \(([\d.]+)\) \| ([\d.]+) \| (\S+) \| ([\d.]+) \| ([\d.]+) \| "
                 r"([\d.]+) \| ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\] \|", line)
    if m:
        g = m.groups(); cells.setdefault((g[0], g[1]), []).append(g)
SPK = {"1.5 m/s": "1.5mps", "3 km/h": "3kmh"}
summ = {}
for (fcs, sps), rows in cells.items():
    fc, sp = int(fcs), SPK[sps]
    bc = max(CLASSIC, key=lambda a: e(fc, 12, sp, a).mean())
    bh = max(HYB, key=lambda a: e(fc, 12, sp, a).mean())
    ref = e(fc, 11, sp, bc)
    fd = D["data"][f"{fc}|11|{sp}"]["fd_hz"]
    summ[(fc, sp)] = dict(bc=bc, bh=bh, ref=ref)
    tag = f"{fc} GHz {sps}"
    chk(f"{tag}: f_d (Hz)", float(rows[0][2]), {28: 28e9, 3: 3e9}[fc] * {"1.5mps": 1.5, "3kmh": 3 / 3.6}[sp] / 299792458.0, 0.5)
    chk(f"{tag}: en iyi klasik (seed 12)", rows[0][3], bc, 0)
    chk(f"{tag}: en iyi klasik gecikme", float(rows[0][4]), LAT[bc], 0.005)
    chk(f"{tag}: en iyi klasik etkin hız (seed 11)", float(rows[0][5]), ref.mean(), 5e-4)
    hy = [r for r in rows if r[6].startswith("NN+Adam")]
    chk(f"{tag}: en iyi karma (seed 12)", hy[0][6] if hy else "-", bh, 0)
    for r in rows:
        a = r[6]
        chk(f"{tag} {a}: gecikme", float(r[7]), LAT[a], 0.005)
        chk(f"{tag} {a}: t=0", float(r[8]), z(fc, 11, sp, a).mean(), 5e-4)
        chk(f"{tag} {a}: etkin", float(r[9]), e(fc, 11, sp, a).mean(), 5e-4)
        d = e(fc, 11, sp, a) - ref
        chk(f"{tag} {a}: − en iyi klasik", float(r[10]), d.mean(), 5e-4)
        if np.any(d != 0):
            chk(f"{tag} {a}: GA", [float(r[11]), float(r[12])], boot(d), 0.01)
        else:
            chk(f"{tag} {a}: GA (özdeş kol)", [float(r[11]), float(r[12])], [0.0, 0.0], 0)
chk("tablo hücre sayısı", "4", str(len(cells)), 0)

# ---------------------------------------------------------------- decisions, E1, E2
def line_ci(pat):
    m = re.search(pat + r".*?([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", rep)
    return [float(m.group(1)), float(m.group(2)), float(m.group(3))]

m = summ[(28, "1.5mps")]
d1 = e(28, 11, "1.5mps", "NN-sincos") - m["ref"]; c1 = boot(d1)
d2 = e(28, 11, "1.5mps", m["bh"]) - m["ref"]; c2 = boot(d2)
d3 = z(28, 11, "1.5mps", "NN-sincos") - z(28, 11, "1.5mps", "NN-untrained"); c3 = boot(d3)
r1, r2, r3 = line_ci(r"\*\*S5-H1\*\*"), line_ci(r"\*\*S5-H2\*\*.*?NN\+Adam-\d+"), line_ci(r"\*\*S5-H3\*\*")
chk("S5-H1 fark", r1[0], d1.mean(), 5e-4); chk("S5-H1 GA", r1[1:], c1, 0.01)
chk("S5-H1 karar", "TUTMADI", "TUTTU" if c1[0] > 0 else "TUTMADI", 0)
chk("S5-H2 kol", re.search(r"S5-H2\*\*.*?(NN\+Adam-\d+)", rep).group(1), m["bh"], 0)
chk("S5-H2 fark", r2[0], d2.mean(), 5e-4); chk("S5-H2 GA", r2[1:], c2, 0.01)
chk("S5-H2 karar", "TUTMADI", "TUTTU" if c2[0] > 0 else "TUTMADI", 0)
chk("S5-H3 fark", r3[0], d3.mean(), 5e-4); chk("S5-H3 GA", r3[1:], c3, 0.01)
chk("S5-H3 karar", "TUTTU", "TUTTU" if c3[0] > 0 else "TUTMADI", 0)
for sp, lab in SPN.items():
    for kind, f in (("t0", z), ("eff", e)):
        d = f(28, 11, sp, "NN-sincos") - f(28, 11, sp, "NN-angle")
        mm = re.search(r"S5-E1, 28 GHz " + re.escape(lab) + r".*?t = 0'da ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\], "
                       r"etkin hızda ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", rep).groups()
        rr = [float(x) for x in (mm[:3] if kind == "t0" else mm[3:])]
        chk(f"S5-E1 {lab} {kind}: fark", rr[0], d.mean(), 5e-4); chk(f"S5-E1 {lab} {kind}: GA", rr[1:], boot(d), 0.01)
for fc, sp in ((3, "1.5mps"), (3, "3kmh"), (28, "3kmh")):
    lab = f"S5-E2, {fc} GHz {SPN[sp]}"
    s = summ[(fc, sp)]
    mm = re.search(re.escape(lab) + r":\*\* NN-sincos − en iyi klasik ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]; "
                   r"(NN\+Adam-\d+) − en iyi klasik ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]; eğitilmiş − eğitilmemiş "
                   r"\(t = 0\) ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", rep).groups()
    dn = e(fc, 11, sp, "NN-sincos") - s["ref"]; dh = e(fc, 11, sp, s["bh"]) - s["ref"]
    dt = z(fc, 11, sp, "NN-sincos") - z(fc, 11, sp, "NN-untrained")
    chk(f"{lab}: NN fark", float(mm[0]), dn.mean(), 5e-4); chk(f"{lab}: NN GA", [float(mm[1]), float(mm[2])], boot(dn), 0.01)
    chk(f"{lab}: karma kol", mm[3], s["bh"], 0)
    chk(f"{lab}: karma fark", float(mm[4]), dh.mean(), 5e-4); chk(f"{lab}: karma GA", [float(mm[5]), float(mm[6])], boot(dh), 0.01)
    chk(f"{lab}: eğitilmiş−eğitilmemiş", float(mm[7]), dt.mean(), 5e-4)
    chk(f"{lab}: eğitilmiş−eğitilmemiş GA", [float(mm[8]), float(mm[9])], boot(dt), 0.01)

# ---------------------------------------------------------------- training table
for k in ("28_sincos", "28_angle", "3_sincos"):
    t = json.load(open(R5 / f"train_{k}.json")); h = t["history"]; be = max(h, key=lambda r: r["val"])
    mm = re.search(r"\| " + k + r" \| ([\d.]+) \| (\d+) / (\d+) \| (\d+) \|", rep).groups()
    chk(f"eğitim {k}: en iyi doğrulama", float(mm[0]), max(r["val"] for r in h), 5e-5)
    chk(f"eğitim {k}: best_val = max(history)", t["best_val"], max(r["val"] for r in h), 1e-12)
    chk(f"eğitim {k}: en iyi epoch", int(mm[1]), be["epoch"], 0); chk(f"eğitim {k}: son epoch", int(mm[2]), h[-1]["epoch"], 0)
    chk(f"eğitim {k}: süre (s)", int(mm[3]), h[-1]["seconds"], 0.5)
    chk(f"eğitim {k}: n_train", 20000, t["n_train"], 0)
    chk(f"eğitim {k}: son epoch doğrulaması en iyiden düşük", "evet", "evet" if h[-1]["val"] < be["val"] else "hayır", 0)
    ROWS.append((f"  (bilgi) {k}: epoch-0 doğrulama / en iyi / son", "-",
                 f"{h[0]['val']:.4f} / {be['val']:.4f} / {h[-1]['val']:.4f}", "bilgi"))

# ---------------------------------------------------------------- checkpoints (weights only, no forward pass)
try:
    import torch
    sd = {k: torch.load(R5 / f"net_{k}.pt", weights_only=True) for k in
          ("28_sincos", "28_sincos_untrained", "3_sincos_untrained", "28_angle", "28_angle_untrained", "3_sincos")}
    same = lambda a, b: all(torch.equal(sd[a][p], sd[b][p]) for p in sd[a])
    chk("eğitilmemiş 28 = eğitilmemiş 3 (aynı tohum 0 başlangıcı)", "evet", "evet" if same("28_sincos_untrained", "3_sincos_untrained") else "hayır", 0)
    chk("eğitilmiş 28 sincos ≠ eğitilmemiş", "evet", "evet" if not same("28_sincos", "28_sincos_untrained") else "hayır", 0)
    torch.manual_seed(0)
    sys_path = str(J / "s5"); import sys; sys.path.insert(0, sys_path)
    from model import PhaseNet
    fresh = PhaseNet("sincos").state_dict()
    chk("eğitilmemiş = PhaseNet(seed 0) taze başlangıç", "evet",
        "evet" if all(torch.equal(fresh[p], sd["28_sincos_untrained"][p]) for p in fresh) else "hayır", 0)
    dmax = max(float((sd["28_sincos"][p] - sd["28_sincos_untrained"][p]).abs().max()) for p in fresh)
    ROWS.append(("  (bilgi) eğitilmiş − eğitilmemiş en büyük ağırlık farkı", "-", f"{dmax:.3g}", "bilgi"))
except Exception as ex:                                                  # noqa: BLE001
    ROWS.append(("checkpoint denetimi", "-", f"ÜRETİLEMEDİ ({ex})", "ÜRETİLEMEDİ"))

# ---------------------------------------------------------------- yorum numbers
c28, c3, c28w = summ[(28, "1.5mps")], summ[(3, "1.5mps")], summ[(28, "3kmh")]
nn28 = (e(28, 11, "1.5mps", "NN-sincos") - c28["ref"]).mean(); nn3 = (e(3, 11, "1.5mps", "NN-sincos") - c3["ref"]).mean()
chk("yorum: ağ 0.43 ms", 0.43, NN, 0.005)
chk("yorum: SU-best-of 1.24 ms", 1.24, LAT["SU-best-of"], 0.005)
chk("yorum: 0.38 gerisinde", -0.38, nn28, 0.005)
chk("yorum: ağ t=0 4.65", 4.65, z(28, 11, "1.5mps", "NN-sincos").mean(), 0.005)
chk("yorum: SU-best-of t=0 5.12", 5.12, z(28, 11, "1.5mps", "SU-best-of").mean(), 0.005)
chk("yorum: 0.8 ms gecikme farkı", 0.8, LAT["SU-best-of"] - NN, 0.05)
chk("yorum: 5.115 → 5.011", [5.115, 5.011], [z(28, 11, "1.5mps", "SU-best-of").mean(), e(28, 11, "1.5mps", "SU-best-of").mean()], 5e-4)
chk("yorum: ~0.1 kayıp", 0.1, z(28, 11, "1.5mps", "SU-best-of").mean() - e(28, 11, "1.5mps", "SU-best-of").mean(), 0.05)
need = c28["ref"].mean() + (z(28, 11, "1.5mps", "NN-sincos").mean() - e(28, 11, "1.5mps", "NN-sincos").mean())
chk("yorum: kazanmak için t=0 ~5.0 üstü (gereken t0 = 5.011 + ağın yaşlanma kaybı)", 5.0, need, 0.05)
chk("yorum: 3 GHz −1.52", -1.52, nn3, 0.005); chk("yorum: 28 GHz −0.38", -0.38, nn28, 0.005)
chk("yorum: 4 kat daralma", 4.0, nn3 / nn28, 0.05)
chk("yorum: +0.47 (28 GHz)", 0.47, (z(28, 11, "1.5mps", "NN-sincos") - z(28, 11, "1.5mps", "NN-untrained")).mean(), 0.005)
chk("yorum: +0.37 (3 GHz)", 0.37, (z(3, 11, "1.5mps", "NN-sincos") - z(3, 11, "1.5mps", "NN-untrained")).mean(), 0.005)
h3 = [-(e(3, 11, sp, summ[(3, sp)]["bh"]) - summ[(3, sp)]["ref"]).mean() for sp in SPN]
h28 = [-(e(28, 11, sp, summ[(28, sp)]["bh"]) - summ[(28, sp)]["ref"]).mean() for sp in SPN]
chk("yorum: 3 GHz karma 0.06–0.08 gerisinde", [0.06, 0.08], sorted(h3), 0.005)
chk("yorum: 28 GHz karma 0.11–0.16 gerisinde", [0.11, 0.16], sorted(h28), 0.005)
e1 = [(f(28, 11, sp, "NN-sincos") - f(28, 11, sp, "NN-angle")).mean() for sp in SPN for f in (z, e)]
chk("yorum: E1 +0.04…+0.05", [0.04, 0.05], [min(e1), max(e1)], 0.005)
be = [max(json.load(open(R5 / f"train_{k}.json"))["history"], key=lambda r: r["val"])["epoch"] for k in ("28_sincos", "28_angle", "3_sincos")]
chk("yorum: doruk 10–20. epoch'ta", "10–20 içinde", "10–20 içinde" if all(10 <= b <= 20 for b in be) else str(be), 0)
chk("yorum: T_c ≈ 3 ms (0.423/f_d)", 3.0, 0.423 / D["data"]["28|11|1.5mps"]["fd_hz"] * 1e3, 0.1)

# ---------------------------------------------------------------- additional logic checks (not in the report)
X = []
for fc, sp in ((28, "1.5mps"), (28, "3kmh"), (3, "1.5mps"), (3, "3kmh")):
    rk = sorted(CLASSIC, key=lambda a: -e(fc, 12, sp, a).mean())[:3]
    X.append(f"{fc} GHz {SPN[sp]}: seed-12 ilk üç klasik {', '.join(f'{a} {e(fc, 12, sp, a).mean():.3f}' for a in rk)}")
    best_on_11 = max(CLASSIC, key=lambda a: e(fc, 11, sp, a).mean())
    X.append(f"   seed 11'de en iyi klasik {best_on_11} {e(fc, 11, sp, best_on_11).mean():.3f} (seçilen {summ[(fc, sp)]['bc']} {summ[(fc, sp)]['ref'].mean():.3f})")
    su = "SU-average"
    X.append(f"   SU-average {LAT[su]:.3f} ms: t0 {z(fc, 11, sp, su).mean():.3f}, etkin {e(fc, 11, sp, su).mean():.3f}; "
             f"NN-sincos t0 {z(fc, 11, sp, 'NN-sincos').mean():.3f}; NN−SU-average etkin "
             f"{(e(fc, 11, sp, 'NN-sincos') - e(fc, 11, sp, su)).mean():+.3f} {boot(e(fc, 11, sp, 'NN-sincos') - e(fc, 11, sp, su))}")
    for L in (1, 2, 6, 12):
        dd = z(fc, 11, sp, f"NN+Adam-{L}") - z(fc, 11, sp, f"Adam-{L}|best")
        de = e(fc, 11, sp, f"NN+Adam-{L}") - e(fc, 11, sp, f"Adam-{L}|best")
        X.append(f"   NN+Adam-{L} − Adam-{L}|best: t0 {dd.mean():+.3f} {[round(v, 3) for v in boot(dd)]}, etkin {de.mean():+.3f} {[round(v, 3) for v in boot(de)]}")
    dz = z(fc, 11, sp, "NN-sincos") - z(fc, 11, sp, "SU-best-of")
    X.append(f"   NN-sincos − SU-best-of t0 {dz.mean():+.3f} {[round(v, 3) for v in boot(dz)]}; "
             f"NN-sincos t0 − en iyi klasik etkin {(z(fc, 11, sp, 'NN-sincos') - summ[(fc, sp)]['ref']).mean():+.3f}")
    X.append(f"   en iyi klasik kol CD mi? {summ[(fc, sp)]['bc'].startswith('CD')}; en iyi CD etkin (seed 11) "
             f"{max(e(fc, 11, sp, f'CD-{s}').mean() for s in range(1, 9)):.3f}")
S = json.load(open(R5 / "s5_summary.json"))
X.append(f"s5_summary.json kararları {S['decisions']}; NN load_start {D['nn_latency']['load_start']:.2f} (sonrası kaydedilmedi)")

print("| denetlenen | rapor | yeniden hesap | durum |\n| --- | --- | --- | --- |")
for r in ROWS:
    print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
n_ok = sum(r[3] == "OK" for r in ROWS); n_bad = sum(r[3] == "HATA" for r in ROWS)
print(f"\nOK {n_ok}, HATA {n_bad}, ÜRETİLEMEDİ {sum(r[3] == 'ÜRETİLEMEDİ' for r in ROWS)}")
for r in ROWS:
    if r[3] == "HATA":
        print("HATA:", r)
print("\n## Ek mantık denetimleri\n" + "\n".join(X))
