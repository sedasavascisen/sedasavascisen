"""
Bagimsiz sayisal denetim: thesis_exp/genis_bant/REPORT.md (ve yorum.md, Makale 2 4. tur cumleleri).

Yalnizca ham ciktilardan yeniden hesaplar: raw/curves.json (senaryo basina diziler), raw/timing.json,
raw/g4.json, raw/sens200.json (yalniz kiyas icin), raw/results.json (yalniz t0 ve kiyas icin),
tasarim_kurali/raw/calibration.json (psi tablosunun araligi). run.py / sens200.py / common.boot KULLANILMAZ;
secim, fark, bootstrap (kendi RNG'si, 2000 yeniden ornekleme, %95 yuzdelik) ve gecikme uydurmasi burada
yeniden yazildi. Tek pahali olmayan kod cagrisi: zaman izgarasi degismezligi icin wb.WB (n = 8).

Cikti: thesis_exp/denetim_log/genis_bant_denetim_out.md (tablo) ve genis_bant_denetim.json.
Tohum: bootstrap np.random.default_rng(20261116).
"""
import json, re, sys, pathlib, subprocess
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
GB = ROOT / "thesis_exp/genis_bant"; R = GB / "raw"; OUT = pathlib.Path(__file__).resolve().parent
CV = json.load(open(R / "curves.json")); TM = json.load(open(R / "timing.json"))
RS = json.load(open(R / "results.json")); G4 = json.load(open(R / "g4.json")); S2 = json.load(open(R / "sens200.json"))
LATREF = json.load(open(ROOT / "thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json"))["median"]
CAL = json.load(open(ROOT / "thesis_exp/tasarim_kurali/raw/calibration.json"))
REP = (GB / "REPORT.md").read_text(); YOR = (GB / "yorum.md").read_text()
LSET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]; KS = [1, 4, 16, 64]
BWS = ["20", "50", "100"]; SPS = ["1.5mps", "10kmh"]; SPN = {"1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
HOR = 200.0
rng = np.random.default_rng(20261116)


def boot(d, n=2000):
    d = np.asarray(d, float)
    idx = rng.integers(0, len(d), (n, len(d)))
    m = d[idx].mean(1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


rows = []  # (bolum, kalem, rapor, yeniden, durum)


def chk(sec, item, rep, mine, tol=6e-4, ci=False):
    """rep: string from the report; mine: float / list / str."""
    if isinstance(mine, str) or rep is None:
        ok = (rep == mine)
        rows.append((sec, item, rep, mine, "OK" if ok else "HATA")); return ok
    rn = [float(x) for x in re.findall(r"[-+]?\d+\.\d+|[-+]?\d+", rep)]
    mv = mine if isinstance(mine, (list, tuple)) else [mine]
    ok = len(rn) == len(mv) and all(abs(a - b) <= (0.01 if ci else tol) for a, b in zip(rn, mv))
    rows.append((sec, item, rep, ", ".join(f"{x:+.4f}" for x in mv), "OK" if ok else "HATA")); return ok


def table(header_regex):
    """rows of the first markdown table after the header matching regex -> list of cell lists"""
    m = re.search(header_regex, REP, re.M); txt = REP[m.end():]
    out, started = [], False
    for line in txt.splitlines():
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("- "):
                continue
            out.append(cells)
        elif started:
            break
    return out[1:]  # drop header


# ---------------------------------------------------------------- 1) latency
T0 = LATREF["su_average"]
fit = {}
tab1 = table(r"^## 1\)")
for row, k in zip(tab1, KS):
    y = [TM["arms"][f"K{k}_L{L}"]["median_ms"] for L in (1, 4, 16)]
    y2 = [float(np.median(TM["arms"][f"K{k}_L{L}"]["rounds_ms"])) for L in (1, 4, 16)]
    b, a0 = np.polyfit([1, 4, 16], y2, 1); fit[k] = (a0, b)
    chk("§1", f"K{k} medyan L=1,4,16", " ".join(row[1:4]), y2, tol=0.006)
    chk("§1", f"K{k} uydurma", row[4], [a0, b], tol=0.006)
    chk("§1", f"K{k} L=48 gecikme", row[5], T0 + a0 + 48 * b, tol=0.06)
    chk("§1", f"K{k} uydurma == timing.json", f"{TM[f'fit_K{k}']['intercept_ms']:.6f} {TM[f'fit_K{k}']['per_step_ms']:.6f}", [a0, b], tol=1e-6)
lat = {"SU-best-of": LATREF["su_best_of"], "CD": LATREF["cd"]}
for k in KS:
    for L in LSET:
        lat[f"K{k}-L{L}"] = T0 + fit[k][0] + fit[k][1] * L
mx = max(abs(lat[a] - RS["latency_ms"][a]) for a in lat)
chk("§1", "tum kol gecikmeleri == results.json (max abs fark, ms)", "0", mx, tol=1e-6)
ld = TM["load"]
chk("§1", "yuk baslangic/once/sonra", "0.03 0.03 1.00", [ld["start"], ld["before"], ld["after"]], tol=0.006)
chk("§1", "SU-best-of / CD (ms)", "1.63 702.97", [lat["SU-best-of"], lat["CD"]], tol=0.006)
chk("yorum", "K16/K1 adim maliyeti orani (~9 kat)", "9", fit[16][1] / fit[1][1], tol=0.5)
# round spread (CLAUDE.md: medyan + tur-arasi yayilim)
spread = {f"K{k}_L{L}": (min(TM['arms'][f'K{k}_L{L}']['rounds_ms']), max(TM['arms'][f'K{k}_L{L}']['rounds_ms']))
          for k in KS for L in (1, 4, 16)}

# ---------------------------------------------------------------- 3) cells
A = lambda s, bw, sp: {k: np.asarray(v, float) for k, v in CV[f"{s}|{bw}|{sp}"].items()}
tab3 = table(r"^## 3\)"); tabK = table(r"^### K_opt"); i3 = 0; iK = 0
cells = {}; g1 = []; extra = {}
for bw in BWS:
    for sp in SPS:
        ev, et = A(12, bw, sp), A(11, bw, sp)
        assert all(len(v) == 400 for v in et.values()) and len(et) == 2 + 4 * 14
        best = max(ev, key=lambda a: ev[a].mean())
        nb = max([a for a in ev if a.startswith("K1-")], key=lambda a: ev[a].mean())
        row = tab3[i3]; i3 += 1
        chk("§3", f"{bw}/{sp} secilen (seed 12)", row[2], best)
        chk("§3", f"{bw}/{sp} etkin hiz", row[3], float(et[best].mean()))
        d1, d2, d3 = et[best] - et["SU-best-of"], et[best] - et[nb], et["CD"] - et[best]
        rp = lambda s: re.sub(r"\(.*\)", "", s)
        chk("§3", f"{bw}/{sp} - SU-best-of (nokta)", rp(row[4]).split("[")[0], d1.mean())
        chk("§3", f"{bw}/{sp} - SU-best-of GA", "[" + rp(row[4]).split("[")[1], boot(d1), ci=True)
        chk("§3", f"{bw}/{sp} dar bant kolu", re.search(r"dar bant: (\S+)\)", row[5]).group(1), nb)
        chk("§3", f"{bw}/{sp} - dar bant (nokta)", rp(row[5]).split("[")[0], d2.mean())
        chk("§3", f"{bw}/{sp} - dar bant GA", "[" + rp(row[5]).split("[")[1], boot(d2), ci=True)
        chk("§3", f"{bw}/{sp} CD - secilen (nokta)", row[6].split("[")[0], d3.mean())
        chk("§3", f"{bw}/{sp} CD - secilen GA", "[" + row[6].split("[")[1], boot(d3), ci=True)
        cells[(bw, sp)] = dict(best=best, nb=nb, cd=float(d3.mean()), cd_ci=boot(d3), nbd=float(d2.mean()))
        # extra: how firm is the K_opt choice (seed-12 margin; seed-11 paired diff vs best K<=4 arm chosen on seed 12)
        b4 = max([a for a in ev if a.startswith(("K1-", "K4-"))], key=lambda a: ev[a].mean())
        dd = et[best] - et[b4]
        extra[f"{bw}|{sp}"] = dict(best=best, best_Kle4=b4, margin_seed12=float(ev[best].mean() - ev[b4].mean()),
                                   seed11_diff=float(dd.mean()), seed11_ci=boot(dd))
        for k in KS:
            arms = [f"K{k}-L{L}" for L in LSET]
            Ls = max(arms, key=lambda a: et[a].mean())
            d48 = et[f"K{k}-L48"] - et[Ls]; c48 = boot(d48)
            loss = 100 * (1 - et[f"K{k}-L48"].mean() / et[Ls].mean())
            row = tabK[iK]; iK += 1
            nm = f"{bw}/{sp}/K{k}"
            chk("§3K", f"{nm} L*", row[3], Ls.split("-L")[1])
            chk("§3K", f"{nm} gecikme(L*)", row[4].split(" ")[0], lat[Ls], tol=0.06)
            chk("§3K", f"{nm} >200 ms bayragi", str("⚠" in row[4]), str(lat[Ls] > HOR))
            chk("§3K", f"{nm} etkin hiz(L*)", row[5], float(et[Ls].mean()))
            t0 = RS["cells"][f"{bw}MHz_{sp}"]["by_kopt"][str(k)]["t0_L_star"]
            chk("§3K", f"{nm} t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin)", row[6] if t0 >= et[Ls].mean() else "t0<etkin", f"{t0:.3f}")
            chk("§3K", f"{nm} L48-L* (nokta)", row[7].split("[")[0], d48.mean())
            chk("§3K", f"{nm} L48-L* GA", "[" + row[7].split("[")[1], c48, ci=True)
            chk("§3K", f"{nm} L48 kaybi %", row[8], loss, tol=0.006)
            g1.append(dict(bw=bw, sp=sp, k=k, Ls=int(Ls.split("-L")[1]), sig=c48[1] < 0, sig_orig=RS["cells"][f"{bw}MHz_{sp}"]["by_kopt"][str(k)]["ci"][1] < 0,
                           latLs=lat[Ls], hi=c48[1], m=float(et[Ls].mean())))

# ---------------------------------------------------------------- G1 count robustness to the bootstrap RNG
diffs = [x for x in g1 if x["sig"] != x["sig_orig"]]
rob = {}
for x in g1:
    if abs(x["hi"]) < 0.01:                      # borderline cells only
        et = A(11, x["bw"], x["sp"]); Lsn = f"K{x['k']}-L{x['Ls']}"
        d = et[f"K{x['k']}-L48"] - et[Lsn]
        his = []
        for s in range(20):
            r2 = np.random.default_rng(1000 + s); idx = r2.integers(0, 400, (2000, 400))
            his.append(float(np.percentile(d[idx].mean(1), 97.5)))
        rob[f"{x['bw']}|{x['sp']}|K{x['k']}"] = dict(frac_sig=float(np.mean(np.array(his) < 0)), hi_min=min(his), hi_max=max(his),
                                                     orig_hi=RS["cells"][f"{x['bw']}MHz_{x['sp']}"]["by_kopt"][str(x["k"])]["ci"][1])
print("G1 sinirdaki hucreler (20 bootstrap tohumu):", json.dumps(rob, indent=0))
print("G1 hukmu farkli cikan hucreler:", [(x["bw"], x["sp"], x["k"], x["hi"]) for x in diffs])

# ---------------------------------------------------------------- top / §2 counts and decisions
nsig = sum(x["sig"] for x in g1); n48 = sum(x["Ls"] == 48 for x in g1)
chk("ust", "G1: L=48 anlamli kotu hucre sayisi (7/24)", "7 24", [nsig, len(g1)], tol=0)
chk("ust", "G1: kendi GA ile results.json GA'si ayni hukum", "24", sum(x["sig"] == x["sig_orig"] for x in g1), tol=0)
chk("ust", "L* tam 48 olan hucre (6)", "6", n48, tol=0)
chk("ust", "G1 hukmu", "TUTMADI", "TUTTU" if nsig == len(g1) else "TUTMADI")
chk("DEGISIKLIKLER", "50-100 MHz'de anlamli hucre (3/16)", "3 16", [sum(x["sig"] for x in g1 if x["bw"] != "20"), 16], tol=0)
k1 = [x for x in g1 if x["k"] == 1]
chk("ust", "K1: 20 MHz iki hiz + 50 MHz 1.5 m/s korunuyor (anlamli), digerleri degil",
    "20/1.5mps:True 20/10kmh:True 50/1.5mps:True 50/10kmh:False 100/1.5mps:False 100/10kmh:False",
    " ".join(f"{x['bw']}/{x['sp']}:{x['sig']}" for x in k1))
kof = lambda a: int(a.split("-")[0][1:]) if a.startswith("K") else None
sel = {c: cells[c]["best"] for c in cells}
g2a = all(kof(sel[("20", sp)]) is not None and kof(sel[("20", sp)]) <= 4 for sp in SPS)
g2b = all((kof(sel[("100", sp)]) or 0) >= 16 for sp in SPS)
chk("§2", "G2 hukmu (20 MHz K<=4 ve 100 MHz K>=16)", "TUTTU", "TUTTU" if g2a and g2b else "TUTMADI")
chk("§2", "G2: secilen kol K64 degil (sapma 2)", "True", str(all(kof(v) != 64 for v in sel.values())))
n3 = sum(cells[c]["cd_ci"][1] < 0 for c in cells)
chk("§2", "G3: CD anlamli geride (6/6)", "6 6", [n3, 6], tol=0)
cdr = [-cells[c]["cd"] for c in cells]
chk("yorum", "G3 araligi 0.23-0.47", "0.23 0.47", [min(cdr), max(cdr)], tol=0.005)
chk("ust/yorum", "100 MHz secilen - dar bant (+0.28...+0.29; ~+0.28)", "0.28 0.29",
    [cells[("100", "1.5mps")]["nbd"], cells[("100", "10kmh")]["nbd"]], tol=0.005)

# ---------------------------------------------------------------- 4) sens200
tab4 = table(r"^## 4\)"); i4 = 0; g1s = []; g4s = []
for bw in BWS:
    for sp in SPS:
        ev, et = A(12, bw, sp), A(11, bw, sp)
        ok = [a for a in ev if lat[a] <= HOR and a != "CD"]
        best = max(ok, key=lambda a: ev[a].mean())
        nb = max([a for a in ok if a.startswith("K1-")], key=lambda a: ev[a].mean())
        d = et[best] - et[nb]; row = tab4[i4]; i4 += 1
        chk("§4", f"{bw}/{sp} secilen <=200", row[1], best)
        chk("§4", f"{bw}/{sp} gecikme", row[2], lat[best], tol=0.06)
        chk("§4", f"{bw}/{sp} etkin hiz", row[3], float(et[best].mean()))
        chk("§4", f"{bw}/{sp} dar bant kolu", re.search(r"\((K\S+)\)", row[4]).group(1), nb)
        chk("§4", f"{bw}/{sp} - dar bant (nokta)", row[4].split("[")[0], d.mean())
        chk("§4", f"{bw}/{sp} - dar bant GA", "[" + row[4].split("[")[1].split("]")[0] + "]", boot(d), ci=True)
        if bw == "100":
            chk("yorum", f"100/{sp} K16-L20 183.4 ms ve +0.24/+0.28", "183.4 0.24" if sp == "1.5mps" else "183.4 0.28",
                [lat[best] if best == "K16-L20" else -1, d.mean()], tol=0.06)
        for k in KS:
            arms = [f"K{k}-L{L}" for L in LSET if lat[f"K{k}-L{L}"] <= HOR]
            if not arms:
                continue
            Ls = max(arms, key=lambda a: et[a].mean()); Lm = max(arms, key=lambda a: lat[a])
            g1s.append(dict(edge=Ls == Lm, sig=boot(et[Lm] - et[Ls])[1] < 0))
nsel = sum(1 for _ in g1s)
chk("ust", "sens200: L* ufuk icindeki en buyuk L'de (15/24)", "15 24", [sum(x["edge"] for x in g1s), nsel], tol=0)
chk("ust", "sens200: ufuk icindeki en buyuk L anlamli kotu (4)", "4", sum(x["sig"] for x in g1s), tol=0)

# ---------------------------------------------------------------- 5) G4
tab5 = table(r"^## 5\)"); losses = []; i5 = 0; g4cells = []
for bw in BWS:
    for sp in SPS:
        et = A(11, bw, sp)
        for k in KS:
            key = f"{bw}MHz_{sp}_K{k}"; g = G4["cells"][key]
            m = {L: et[f"K{k}-L{L}"].mean() for L in LSET}; Ls = max(m, key=m.get)
            loss = 100 * (1 - m[g["L_rule"]] / m[Ls]); losses.append(loss)
            row = tab5[i5]; i5 += 1
            chk("§5", f"{key} adim / kural L", " ".join(row[1:3]), [fit[k][1], g["L_rule"]], tol=6e-4)
            chk("§5", f"{key} L* (curves)", row[3], str(Ls))
            chk("§5", f"{key} kayip % (curves'ten)", row[4], loss, tol=0.006)
            g4cells.append(dict(key=key, Lr=g["L_rule"], Ls=Ls, loss=loss, lat_rule=lat[f"K{k}-L{g['L_rule']}"], lat_Ls=lat[f"K{k}-L{Ls}"],
                                u_rule=(1.5 if sp == "1.5mps" else 10 / 3.6) * 3e9 / 299792458.0 * lat[f"K{k}-L{g['L_rule']}"] / 1000))
L = np.array(losses)
chk("§2", "G4 medyan/ortalama/en kotu %", "0.81 1.68 7.97", [np.median(L), L.mean(), L.max()], tol=0.006)
chk("§2", "G4 g4.json ile curves yeniden turetimi ayni (max abs fark, %)", "0",
    max(abs(a - G4["cells"][c["key"]]["loss_pct"]) for a, c in zip(losses, g4cells)), tol=1e-9)
inh = [c["loss"] for c in g4cells if c["lat_Ls"] <= HOR]
chk("§4", "G4 L* ufuk icinde: hucre / medyan / en kotu (12, 0.91, 4.95)", "12 0.91 4.95", [len(inh), np.median(inh), max(inh)], tol=0.006)
odd = [c for c in g4cells if "K16" in c["key"]]
umax = float(np.max(CAL["u"]))

# ---------------------------------------------------------------- yorum: 1.5 m/s vs 10 km/h L*
cmp = []
for bw in BWS:
    for k in KS:
        a = next(x for x in g1 if x["bw"] == bw and x["k"] == k and x["sp"] == "1.5mps")["Ls"]
        b = next(x for x in g1 if x["bw"] == bw and x["k"] == k and x["sp"] == "10kmh")["Ls"]
        cmp.append((bw, k, a, b))
chk("yorum", "50 MHz K1: L* 16 -> 48", "16 48", [cmp[4][2], cmp[4][3]], tol=0)

# ---------------------------------------------------------------- time-grid invariance of t = 0 (cheap, n = 8)
inv = None
try:
    sys.path.insert(0, str(GB)); sys.path.insert(0, str(ROOT))
    import torch, wb
    w1 = wb.WB(11, [0.0], 50e6, n=8); w2 = wb.WB(11, [0.0, 37.4, 438.8], 50e6, v=10 / 3.6, n=8)
    inv = max(float((w1.Gtf[:, 0] - w2.Gtf[:, 0]).abs().max()), float((w1.Htf[:, 0] - w2.Htf[:, 0]).abs().max()),
              float((w1.Ff - w2.Ff[..., :1] if w1.Ff.shape != w2.Ff.shape else w1.Ff - w2.Ff).abs().max()),
              float((w1.G0 - w2.G0).abs().max()))
    chk("kod", "t=0 kanali zaman izgarasi ve hizdan bagimsiz (max abs fark)", "0", inv, tol=0)
    sub = {k: wb.subset(k) for k in (4, 16, 64)}
    off = wb.offsets(1.0)
    chk("kod", "alt kume agirlik merkezi / B (K4, K16, K64)", "0.0078 0.0078 0.0",
        [float(np.mean(off[sub[k]])) for k in (4, 16, 64)], tol=1e-3)
    chk("kod", "K4 alt kumesi {8,24,40,56}", "[8, 24, 40, 56]", str(sub[4]))
except Exception as e:  # noqa
    rows.append(("kod", "zaman izgarasi degismezligi", "-", f"URETILEMEDI: {e!r}", "URETILEMEDI"))

# ---------------------------------------------------------------- write
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
lines = [f"Denetlenen commit `{commit}`; bootstrap tohumu 20261116 (2000, %95 yuzdelik).", "",
         "| bolum | kalem | rapor | yeniden hesap | durum |", "| --- | --- | --- | --- | --- |"]
lines += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows]
(OUT / "genis_bant_denetim_out.md").write_text("\n".join(lines) + "\n")
json.dump(dict(commit=commit, n_checks=len(rows), n_fail=sum(r[4] != "OK" for r in rows), rows=rows,
               extra_kopt_margin=extra, Lstar_15_vs_10kmh=cmp, g4_K16=odd, psi_table_u_max=umax,
               timing_round_spread_ms=spread, g1_borderline=rob, fit=fit, t0_invariance=inv),
          open(OUT / "genis_bant_denetim.json", "w"), indent=1, default=str)
print(f"{len(rows)} kontrol, {sum(r[4] != 'OK' for r in rows)} HATA/URETILEMEDI")
for r in rows:
    if r[4] != "OK":
        print("  ", r)
print("K secim marji:", json.dumps(extra, indent=0))
print("L* 1.5 m/s -> 10 km/h:", cmp)
print("G4 K16:", [(c["key"], c["Lr"], round(c["lat_rule"], 1), c["Ls"], round(c["lat_Ls"], 1), round(c["loss"], 2), round(c["u_rule"], 3)) for c in odd])
print("psi tablosu u araligi:", float(np.min(CAL["u"])), umax)
print("G4 tum u_rule max:", max(c["u_rule"] for c in g4cells))
