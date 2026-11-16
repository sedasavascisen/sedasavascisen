"""
Independent numerical audit of thesis_exp/juri/REPORT_S3_S1.md and REPORT_S4_S2.md (jury questions 3, 1, 4, 2).
Recomputes ONLY from raw JSON (no channel generation, no torch): raw/arms.json, timing.json, timing2.json,
s3_s1.json, s1b.json, s4_s2.json, s4_s2_summary.json. Own bootstrap (numpy default_rng(20261116), 2000 paired
resamples, percentile 95 %), own Kendall tau. Prints the check table consumed by DENETIM_JURI_S1_S4.md.
Run: python3 thesis_exp/denetim_log/juri_denetim.py   (single process, ~10 s, light CPU)
"""
import json, pathlib, itertools, re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
J = ROOT / "thesis_exp/juri"; R = J / "raw"
rng = np.random.default_rng(20261116)
ROWS = []


def boot(d, n=2000):
    idx = rng.integers(0, len(d), (n, len(d)))
    m = d[idx].mean(1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


def chk(name, rep, got, tol):
    """rep, got: float or list of floats or str. tol absolute."""
    if isinstance(rep, str) or isinstance(got, str):
        ok = str(rep) == str(got)
    else:
        a, b = np.atleast_1d(rep).astype(float), np.atleast_1d(got).astype(float)
        ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= tol + 1e-12))
    fmt = lambda x: x if isinstance(x, str) else ("[" + ", ".join(f"{v:+.3f}" for v in x) + "]" if isinstance(x, (list, tuple)) else f"{x:.4g}")
    ROWS.append((name, fmt(rep), fmt(got), "OK" if ok else "HATA"))
    return ok


def ktau_a(a, b):
    c = d = 0
    for i, j in itertools.combinations(range(len(a)), 2):
        s = np.sign(a[i] - a[j]) * np.sign(b[i] - b[j]); c += s > 0; d += s < 0
    return (c - d) / (len(a) * (len(a) - 1) / 2)


D = json.load(open(R / "arms.json")); TM = json.load(open(R / "timing.json")); T2 = json.load(open(R / "timing2.json"))
S31 = json.load(open(R / "s3_s1.json")); S1B = json.load(open(R / "s1b.json"))
rep3 = (J / "REPORT_S3_S1.md").read_text(); rep4 = (J / "REPORT_S4_S2.md").read_text()
tm, t2 = TM["median_ms"], T2["median_ms"]

# ------------------------------------------------------------- timing / latency bookkeeping
for k in tm:
    chk(f"timing.json median {k} = median(rounds)", tm[k], float(np.median(TM["rounds_ms"][k])), 1e-9)
for k in t2:
    chk(f"timing2.json median {k} = median(rounds)", t2[k], float(np.median(T2["rounds_ms"][k])), 1e-9)
steps7 = [1, 2, 4, 8, 16, 32, 48]
slope = float(np.polyfit(steps7, [t2[f"adam{L}"] for L in steps7], 1)[0])
chk("Adam eğimi (ms/adım, timing2 polyfit) = rapor 1.086", 1.086, slope, 5e-4)
LM = D["lat_meas"]
exp = {"SU-average": t2["su_average"], "SU-best-of": t2["su_best_of"], "Long-run Adam": t2["pga"],
       **{f"CD-{s}": tm[f"cd{s}"] for s in range(1, 9)}}
for L in [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]:
    exp[f"Adam-{L}"] = float(np.interp(L, steps7, [t2[f"adam{x}"] for x in steps7]))
chk("lat_meas = timing/timing2 medyanları (+ Adam interp), max |fark|", 0.0, max(abs(LM[k] - exp[k]) for k in LM), 1e-9)
K, N, T = 4, 32, 8
E = 8 * (K * N * T + 2 * K * K * T + K ** 3 + K * T)
chk("E (ON_KAYIT formülü) = 11008", 11008, E, 0)
chk("arms.json E_flops", float(D["E_flops"]), float(E), 0)
fl = {"SU-average": 2 * E, "SU-best-of": 8 * E, "Long-run Adam": 3 * (1 + 1000 * 4) * E + 4 * E,
      **{f"Adam-{L}": 2 * E + 3 * L * E for L in [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]},
      **{f"CD-{s}": 4 * E + s * N * 16 * E for s in range(1, 9)}}
chk("FLOP tablosu = ON_KAYIT tablosu, max |fark|", 0.0, max(abs(D["flops"][k] - fl[k]) for k in fl), 0)
mpf = slope / (3 * E)
chk("ms_per_flop", D["ms_per_flop"] * 1e9, mpf * 1e9, 1e-6)
for a, (m_, f_, r_) in {"SU-average": (0.23, 0.72, 0.32), "SU-best-of": (1.24, 2.90, 0.43), "Adam-1": (1.15, 1.81, 0.64),
                         "Adam-8": (8.80, 9.41, 0.94), "Adam-48": (52.25, 52.85, 0.99), "CD-1": (75.72, 186.78, 0.41),
                         "CD-8": (485.06, 1484.13, 0.33), "Long-run Adam": (3952.07, 4346.32, 0.91)}.items():
    chk(f"S3-E {a} ölçülmüş/FLOP/oran", [m_, f_, r_], [LM[a], fl[a] * mpf, LM[a] / (fl[a] * mpf)], 0.0051)
ratios = [LM[a] / (fl[a] * mpf) for a in LM]
chk("oran aralığı (bütün 25 kol) min,max = 0.32–0.99", [0.32, 0.99], [min(ratios), max(ratios)], 0.0051)
ref = json.load(open(ROOT / "thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json"))["median"]
chk("sapma adam1/adam48/CD-8", [0.862, 0.775, 0.690], [tm["adam1"] / ref["adam1"], tm["adam48"] / ref["adam48"], tm["cd8"] / ref["cd"]], 5e-4)
chk("yük başlangıç/öncesi/sonrası (timing.json)", [0.06, 0.06, 0.75], [TM["load"]["start"], TM["load"]["before"], TM["load"]["after"]], 0.005)
tor = {s: tm[f"cd{s}"] for s in range(1, 9)}
for s in range(1, 9):
    chk(f"S1 zamanlama s={s} torch/nd/ni/×d/×i", [None or float(x) for x in re.search(rf"\| {s} \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| (\d+)× \| (\d+)× \|", rep3).groups()],
        [tor[s], tm[f"numba_direct{s}"], tm[f"numba_incr{s}"], round(tor[s] / tm[f"numba_direct{s}"]), round(tor[s] / tm[f"numba_incr{s}"])], 0.0051)

# ------------------------------------------------------------- S3-H1, S3-E, S1
g = lambda seed, sp, key: np.asarray(D["data"][f"{seed}|{sp}"]["eval"][key])
t0 = lambda seed, sp, a: np.asarray(D["data"][f"{seed}|{sp}"]["t0"][a])
ARMS = list(LM); SP = {"1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
BUD = [2, 5, 10, 20, 50, 100, 200, 1000, 6000]
for sp in SP:
    sec = rep3.split(f"### {SP[sp]} — S3-H1")[1].split("###")[0]
    rows = re.findall(r"\| (\d+) \| ([\w\- ]+?) \| ([\w\- ]+?) \| ([\d.]+) \| ([\d.]+) \| ([+\-][\d.]+) \[([+\-][\d.]+), ([+\-][\d.]+)\] \|", sec)
    holds = False
    for (b, ryu_r, ours_r, re_, oe_, d_, lo, hi), B in zip(rows, BUD):
        cand = [a for a in ARMS if LM[a] <= B]
        ryu = max(cand, key=lambda a: t0(12, sp, a).mean()); ours = max(cand, key=lambda a: g(12, sp, f"{a}@meas").mean())
        d = g(11, sp, f"{ryu}@meas") - g(11, sp, f"{ours}@meas")
        ci = boot(d) if ryu != ours else [0.0, 0.0]; holds |= ci[1] < 0
        chk(f"S3-H1 {SP[sp]} B={B} seçimler", f"{ryu_r}/{ours_r}", f"{ryu}/{ours}", 0)
        chk(f"S3-H1 {SP[sp]} B={B} etkinler, fark", [float(re_), float(oe_), float(d_)],
            [g(11, sp, f"{ryu}@meas").mean(), g(11, sp, f"{ours}@meas").mean(), d.mean()], 0.0006)
        chk(f"S3-H1 {SP[sp]} B={B} GA", [float(lo), float(hi)], ci, 0.01)
    if sp == "1.5mps":
        chk("S3-H1 1.5 m/s karar", "TUTTU", "TUTTU" if holds else "TUTMADI", 0)
    em = np.array([g(11, sp, f"{a}@meas").mean() for a in ARMS]); ef = np.array([g(11, sp, f"{a}@flop").mean() for a in ARMS])
    selm = max(ARMS, key=lambda a: g(12, sp, f"{a}@meas").mean()); self_ = max(ARMS, key=lambda a: g(12, sp, f"{a}@flop").mean())
    m = re.search(rf"\| {SP[sp]} \| ([\d.]+) \| ([\w\-]+) \| ([\w\-]+) \| ([\d.]+) \| ([\d.]+) \|", rep3)
    chk(f"S3-E {SP[sp]} Kendall tau (tau-a, 25 kol)", float(m.group(1)), ktau_a(em, ef), 0.0006)
    chk(f"S3-E {SP[sp]} seçilen ölç/FLOP", f"{m.group(2)}/{m.group(3)}", f"{selm}/{self_}", 0)
    chk(f"S3-E {SP[sp]} etkinler", [float(m.group(4)), float(m.group(5))], [g(11, sp, f"{self_}@meas").mean(), g(11, sp, f"{selm}@meas").mean()], 0.0006)
    # S1
    FAST = ["SU-average", "SU-best-of"] + [a for a in ARMS if a.startswith("Adam-")]
    refa = max(FAST, key=lambda a: g(12, sp, f"{a}@meas").mean()); rv = g(11, sp, f"{refa}@meas")
    hdr = re.search(rf"### {SP[sp]} — karşılaştırma kolu ([\w\-]+) \(([\d.]+) ms, etkin hız ([\d.]+)\)", rep3)
    chk(f"S1 {SP[sp]} karşılaştırma kolu", hdr.group(1), refa, 0)
    chk(f"S1 {SP[sp]} kol gecikmesi, etkin", [float(hdr.group(2)), float(hdr.group(3))], [LM[refa], rv.mean()], 0.0051)
    sec = rep3.split(f"### {SP[sp]} — karşılaştırma kolu")[1].split("###")[0].split("## Soru 1b")[0]
    r_eq = r_sig = None
    for (r, cd, lat, eff, d_, lo, hi) in re.findall(r"\| ([\d.]+) \| (CD-\d) \| ([\d.]+) \| ([\d.]+) \| ([+\-][\d.]+) \[([+\-][\d.]+), ([+\-][\d.]+)\] \|", sec):
        r = float(r); keys = [f"CD-{s}@r{r:g}" for s in range(1, 9)]
        k = max(keys, key=lambda x: g(12, sp, x).mean()); d = g(11, sp, k) - rv; ci = boot(d)
        if r_eq is None and d.mean() >= 0: r_eq = r
        if r_sig is None and ci[0] > 0: r_sig = r
        chk(f"S1 {SP[sp]} r={r:g} ayarlı CD", cd, k.split("@")[0], 0)
        chk(f"S1 {SP[sp]} r={r:g} gecikme, CD etkin, fark", [float(lat), float(eff), float(d_)], [D["lat_s1"][k], g(11, sp, k).mean(), d.mean()], 0.0051)
        chk(f"S1 {SP[sp]} r={r:g} GA", [float(lo), float(hi)], ci, 0.01)
    chk(f"S1 {SP[sp]} r*_eşit, r*_anlamlı üst uç", [15.0, 15.0], [r_eq, r_sig], 0)
    for impl, nm in (("numba_direct", "doğrudan"), ("numba_incr", "artımlı")):
        mm = re.search(rf"Derlenmiş CD \({nm}\), ayarlı (CD-\d), ([\d.]+) ms \(×(\d+)\): etkin hız ([\d.]+), − [\w\-]+ = ([+\-][\d.]+) \[([+\-][\d.]+), ([+\-][\d.]+)\]", sec)
        keys = [f"CD-{s}@{impl}" for s in range(1, 9)]
        k = max(keys, key=lambda x: g(12, sp, x).mean()); s = int(k[3]); d = g(11, sp, k) - rv
        chk(f"S1 {SP[sp]} {nm} kol", mm.group(1), k.split("@")[0], 0)
        chk(f"S1 {SP[sp]} {nm} gecikme, ×, etkin, fark", [float(mm.group(2)), float(mm.group(3)), float(mm.group(4)), float(mm.group(5))],
            [D["lat_numba"][k], round(tm[f"cd{s}"] / tm[f"{impl}{s}"]), g(11, sp, k).mean(), d.mean()], 0.0051)
        chk(f"S1 {SP[sp]} {nm} GA", [float(mm.group(6)), float(mm.group(7))], boot(d), 0.01)
    # s1b: only CD part and r = 1 Adam part are recomputable from arms.json (Adam at latency/r not stored)
    for x in S1B["rows"][sp]:
        r = x["r"]; k = max([f"CD-{s}@r{r:g}" for s in range(1, 9)], key=lambda z: g(12, sp, z).mean())
        chk(f"s1b {SP[sp]} r={r:g} ayarlı CD + CD etkin (arms.json'dan)", [x["cd_eff"]], [g(11, sp, k).mean()], 0.0006)
        chk(f"s1b {SP[sp]} r={r:g} ayarlı CD adı", x["best_cd"], k.split("@")[0], 0)
    x = S1B["rows"][sp][0]
    d = g(11, sp, f"{x['best_cd']}@r1") - g(11, sp, f"{x['best_adam']}@meas")
    chk(f"s1b {SP[sp]} r=1 Adam etkin, CD−Adam, GA", [x["adam_eff"], x["cd_minus_adam"]] + x["ci"], [g(11, sp, f"{x['best_adam']}@meas").mean(), d.mean()] + boot(d), 0.01)
    rr = S1B["rows"][sp]
    chk(f"s1b {SP[sp]} üst bölüm aralığı min,max,en kötü üst GA", [float(v) for v in re.search(rf"{SP[sp]}: CD − Adam ([+\-][\d.]+) … ([+\-][\d.]+), en kötü GA üst sınırı ([+\-]\d+\.\d+)", rep3).groups()],
        [min(z["cd_minus_adam"] for z in rr), max(z["cd_minus_adam"] for z in rr), max(z["ci"][1] for z in rr)], 0.0051)
    chk(f"s1b {SP[sp]} bütün r'lerde GA üst < 0", "evet", "evet" if all(z["ci"][1] < 0 for z in rr) else "hayır", 0)
    chk(f"s1b {SP[sp]} rapor tablosu = s1b.json (satır sayısı eşleşen)", len(rr),
        sum(1 for z in rr if f"| {z['r']:g} | {z['best_adam']} | {z['adam_eff']:.3f} | {z['best_cd']} | {z['cd_eff']:.3f} | {z['cd_minus_adam']:+.3f}" in rep3), 0)
# yorum S3 numbers
chk("yorum: t0 Adam-48 seed 11 1.5 m/s (7.04)", 7.04, t0(11, "1.5mps", "Adam-48").mean(), 0.005)
chk("yorum: t0 CD-8 seed 11 1.5 m/s (6.93)", 6.93, t0(11, "1.5mps", "CD-8").mean(), 0.005)
chk("yorum: 'fark en büyük 1.40 (r=3)' 1.5 m/s", [1.40, 3], [max(-z["cd_minus_adam"] for z in S1B["rows"]["1.5mps"]), max(S1B["rows"]["1.5mps"], key=lambda z: -z["cd_minus_adam"])["r"]], 0.005)
chk("yorum: aynı ifade 10 km/h için (rapor 1.40, r=3)", [1.40, 3], [max(-z["cd_minus_adam"] for z in S1B["rows"]["10kmh"]), max(S1B["rows"]["10kmh"], key=lambda z: -z["cd_minus_adam"])["r"]], 0.005)
# s3_s1.json = report (spot)
chk("s3_s1.json s1 1.5 m/s numba_incr diff", 0.717, S31["s1"]["1.5mps"]["numba"]["numba_incr"]["diff"], 0.0006)

# ------------------------------------------------------------- CD early stop on the timed scenario
for seed in (11, 12):
    for a, b in (("CD-5", "CD-6"), ("CD-6", "CD-7"), ("CD-6", "CD-8"), ("CD-7", "CD-8")):
        n = int(np.sum(np.abs(t0(seed, "1.5mps", a) - t0(seed, "1.5mps", b)) > 1e-6))
        ROWS.append((f"[bilgi] seed {seed}: t0 {a} ≠ {b} olan senaryo sayısı (/400)", "—", str(n), "bilgi"))
for impl in ("numba_direct", "numba_incr", "cd"):
    per = [tm[f"{impl}{s}"] for s in range(1, 9)]
    ROWS.append((f"[bilgi] {impl} s=1..8 ms", "—", " ".join(f"{v:.2f}" for v in per), "bilgi"))
for k in ("cd1", "cd2", "cd5", "cd6", "cd8"):
    v = TM["rounds_ms"][k]; ROWS.append((f"[bilgi] {k} tur-arası max/min", "—", f"{max(v) / min(v):.2f}", "bilgi"))
for sp in SP:  # impact bound: CD-8 at 8/6 of its numba_incr latency ~ r grid point with nearest latency
    ROWS.append((f"[bilgi] {SP[sp]} CD-8 etkin @2.54 ms (numba_incr) / @3.23 ms (r=150)", "—",
                 f"{g(11, sp, 'CD-8@numba_incr').mean():.3f} / {g(11, sp, 'CD-8@r150').mean():.3f}", "bilgi"))
    ROWS.append((f"[bilgi] {SP[sp]} Adam ref @meas vs +SU-average (0.23 ms) yok — en yakın: Adam-6/Adam-8 etkin", "—",
                 f"{g(11, sp, 'Adam-6@meas').mean():.3f} / {g(11, sp, 'Adam-8@meas').mean():.3f}", "bilgi"))

# ------------------------------------------------------------- S4 / S2
D4 = json.load(open(R / "s4_s2.json")); SUMM = json.load(open(R / "s4_s2_summary.json"))
L4 = D4["lat"]
G4 = lambda c, s, sp, a: np.asarray(D4["data"][f"{c}|{s}|{sp}"][a])
chk("s4_s2.json lat = arms.json lat_meas (max |fark|)", 0.0, max(abs(L4[k] - LM[k]) for k in L4), 1e-12)
for sp in SP:  # fresh condition must equal arms.json @meas exactly (independent runs with different time grids)
    md = max(float(np.max(np.abs(G4("fresh", s, sp, a) - g(s, sp, f"{a}@meas")))) for s in (11, 12) for a in D4["data"][f"fresh|11|{sp}"])
    chk(f"tutarlılık: fresh|{SP[sp]} = arms.json @meas (max |fark|, 2 seed × 24 kol)", 0.0, md, 1e-5)
SPN = {"3kmh": "3 km/h", "1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
CN = {"fresh": "taze ön kodlayıcı (Makale 2)", "joint": "birlikte eskime (Soru 4)", "clarke": "Clarke kanalı (Soru 2)"}
adams = [f"Adam-{L}" for L in [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]]
mine = {}
for c in CN:
    for sp in SPN:
        row = re.search(rf"\| {re.escape(CN[c])} \| {SPN[sp]} \| (\d+) \(([\d.]+)\) \| ([\d.]+) \| ([+\-][\d.]+) \[([+\-][\d.]+), ([+\-][\d.]+)\] \| ([\d.]+) \| (CD-\d) ([+\-][\d.]+) \[([+\-][\d.]+), ([+\-][\d.]+)\] \| ([\w\-]+) \(([\d.]+)\) \|", rep4).groups()
        Ls = max(adams, key=lambda a: G4(c, 11, sp, a).mean()); Lsel = max(adams, key=lambda a: G4(c, 12, sp, a).mean())
        d48 = G4(c, 11, sp, "Adam-48") - G4(c, 11, sp, Ls)
        cd = max([f"CD-{s}" for s in range(1, 9)], key=lambda a: G4(c, 12, sp, a).mean())
        dcd = G4(c, 11, sp, cd) - G4(c, 11, sp, "SU-best-of")
        best = max(D4["data"][f"{c}|12|{sp}"], key=lambda a: G4(c, 12, sp, a).mean())
        ci48, cicd = boot(d48), boot(dcd)
        mine[(c, sp)] = dict(ci48=ci48, cicd=cicd, Ls=Ls, Llat=L4[Ls])
        tag = f"S4/S2 {c} {SPN[sp]}"
        chk(f"{tag} L*, CD, en iyi kol", f"Adam-{row[0]}/{row[7]}/{row[11]}", f"{Ls}/{cd}/{best}", 0)
        chk(f"{tag} L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin",
            [float(row[1]), float(row[2]), float(row[3]), float(row[6]), float(row[8]), float(row[12])],
            [L4[Ls], G4(c, 11, sp, Ls).mean(), d48.mean(), 100 * (1 - G4(c, 11, sp, "Adam-48").mean() / G4(c, 11, sp, Ls).mean()),
             dcd.mean(), G4(c, 11, sp, best).mean()], 0.051)
        chk(f"{tag} GA L48−L*", [float(row[4]), float(row[5])], ci48, 0.01)
        chk(f"{tag} GA CD−SBO", [float(row[9]), float(row[10])], cicd, 0.01)
        ROWS.append((f"[bilgi] {tag} seed-12 L seçimi; SU-average etkin; SU-best-of etkin", "—",
                     f"{Lsel}; {G4(c, 11, sp, 'SU-average').mean():.3f}; {G4(c, 11, sp, 'SU-best-of').mean():.3f}", "bilgi"))
h = lambda c: mine[(c, "1.5mps")]
dec = dict(S4_H1=h("joint")["ci48"][1] < 0, S4_H2=h("joint")["cicd"][1] < 0,
           S2_H1=h("clarke")["ci48"][1] < 0 and h("clarke")["Llat"] <= 200, S2_H2=h("clarke")["cicd"][1] < 0)
for k, v in dec.items():
    chk(f"karar {k}", "TUTTU" if SUMM["decisions"][k] else "TUTMADI", "TUTTU" if v else "TUTMADI", 0)
# S4 commentary numbers
chk("yorum S4: τ=0 değeri 5.412 = t0 SU-average seed 11 (arms.json)", 5.412, t0(11, "1.5mps", "SU-average").mean(), 0.0006)
chk("yorum S4: 1.15 ms'de ~%25 kayıp (joint Adam-1 / fresh Adam-1, 1.5 m/s)", 25.0,
    100 * (1 - G4("joint", 11, "1.5mps", "Adam-1").mean() / G4("fresh", 11, "1.5mps", "Adam-1").mean()), 1.0)
chk("yorum S4: joint Adam-1 gecikmesi 1.15 ms", 1.15, L4["Adam-1"], 0.005)
lat10 = min(L4, key=lambda a: abs(L4[a] - 10.0))
ROWS.append(("yorum S4: '10 ms'de hız 1.07' ve 'görece değişim %0.5 / %38'", "1.07; %0.5; %38", f"ÜRETİLEMEDİ (s4_s2.json'da 10 ms noktası yok; en yakın kol {lat10} @ {L4[lat10]:.2f} ms joint 1.5 m/s = {G4('joint', 11, '1.5mps', lat10).mean():.3f}; kanal değişimi ham veride yok)", "ÜRETİLEMEDİ"))
cl = [mine[("clarke", s)] for s in SPN]; fr = [100 * (1 - G4("fresh", 11, s, "Adam-48").mean() / G4("fresh", 11, s, mine[("fresh", s)]["Ls"]).mean()) for s in SPN]
ck = [100 * (1 - G4("clarke", 11, s, "Adam-48").mean() / G4("clarke", 11, s, mine[("clarke", s)]["Ls"]).mean()) for s in SPN]
chk("yorum S2: L* gecikmeleri 3.4–8.8 ms", [3.4, 8.8], [min(x["Llat"] for x in cl), max(x["Llat"] for x in cl)], 0.051)
chk("yorum S2: Clarke kayıp %27–32", [27, 32], [min(ck), max(ck)], 0.51)
chk("yorum S2: taze kayıp %13.5–14.8", [13.5, 14.8], [min(fr), max(fr)], 0.051)
best = {sp: max(D4["data"][f"joint|12|{sp}"], key=lambda a: G4("joint", 12, sp, a).mean()) for sp in SPN}
chk("yorum S4: 1.5 m/s ve 10 km/h'de en iyi kol SU-average", "SU-average/SU-average", f"{best['1.5mps']}/{best['10kmh']}", 0)

# ------------------------------------------------------------- J0
from math import factorial
import sys; sys.path.insert(0, str(J))
from scipy_free_j0 import j0
ser = lambda x: sum((-1) ** m * (x / 2) ** (2 * m) / factorial(m) ** 2 for m in range(60))
xs = [0.0, 0.3, 1.0, 2.404825557695773, 5.0, 2 * np.pi * (10 / 3.6) * 3e9 / 299792458.0 * 0.05225]
chk("J0 (trapez) − J0 (seri), max |fark|, x ≤ 5", 0.0, max(abs(j0(x) - ser(x)) for x in xs), 1e-9)

# ------------------------------------------------------------- print
ok = sum(r[3] == "OK" for r in ROWS); bad = [r for r in ROWS if r[3] == "HATA"]
print(f"kontrol: {ok} OK, {len(bad)} HATA, {sum(r[3] == 'ÜRETİLEMEDİ' for r in ROWS)} ÜRETİLEMEDİ, {sum(r[3] == 'bilgi' for r in ROWS)} bilgi")
print("| kontrol | rapor | yeniden hesap | durum |\n| --- | --- | --- | --- |")
for r in ROWS:
    print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
