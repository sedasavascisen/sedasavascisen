"""
Bağımsız denetim: thesis_exp/sistem mühürlü testi (seed 41) ve gece günlüğündeki geliştirme sayıları.
Yalnızca kayıtlı küplerden (cube/*.npz) yeniden hesaplar; kanal üretmez.

Bağımsız yeniden yazılanlar: K1-K5, kâhin (K6), 12 koşul ortalaması, eşli bootstrap (2000, %95, kendi RNG'si),
H1/H2/H3 kararları, ayrıca denetleyici seçimlerinin kendi yeniden yazımı (v1b_carrier, V4). Dondurulmuş
denetleyiciler (controllers.v1b_carrier, periodic.V4) de çağrılır ve seçimler karşılaştırılır.

Kullanım:  nice -n 19 python3 thesis_exp/denetim_log/sistem_denetim.py
-> stdout (denetim tablosu ve ek analizler); dosya yazmaz
"""
import sys, json, pathlib
sys.dont_write_bytecode = True          # sistem/__pycache__ (izlenen dosyalar) değişmesin
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = ROOT / "sistem"
sys.path.insert(0, str(S)); sys.path.insert(0, str(ROOT / "tasarim_kurali")); sys.path.insert(0, str(ROOT / "p4"))

C0 = 299792458.0
WS = (0, 20)
CAL = json.load(open(ROOT / "tasarim_kurali" / "raw" / "calibration.json"))
CU, CPSI, RF = np.asarray(CAL["u"]), np.asarray(CAL["psi"]), float(CAL["R_floor"])
RNG_SEED = 20261117


def cube(name):
    return json.load(open(S / "cube" / f"{name}.json")), np.load(S / "cube" / f"{name}.npz")


def fd(m, c):
    fc, v = m["cond"][c]
    return v * fc * 1e9 / C0


# ---------------------------------------------------------------- bootstrap (kendi)
def boot(x, n=2000, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), (n, len(x)))
    b = x[idx].mean(1)
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


# ---------------------------------------------------------------- karşılaştırma yöntemleri (kendi)
def closed_form_L(dT_ms, fdhz):
    lset = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
    x = dT_ms / 1000.0 * fdhz
    Lc = 5.0 * (x / 0.025) ** (-0.675)
    return lset[int(np.argmin([abs(np.log(L) - np.log(Lc)) for L in lset]))]


def baselines(m, cal, c, dT_mode="slope48"):
    mc, zc = cal
    if dT_mode == "slope48":
        dT = (m["lat"]["avg+48"] - m["lat"]["avg+0"]) / 48
    else:
        dT = float(dT_mode)
    fresh = [a for a in m["arms"] if not a.startswith("warm")]
    # K5: 10 ms içine sığan taze hatlar; seed 12'de t = 0 hızı en yüksek olan
    key = f"{c}_t0"
    t0 = zc[key]
    cand = [a for a in fresh if m["lat"][a] <= 10.0]
    k5 = max(cand, key=lambda a: float(t0[mc["arms"].index(a)].mean()))
    return {"K1": "best+0", "K2": "avg+5", "K3": "avg+48", "K4": f"avg+{closed_form_L(dT, fd(m, c))}", "K5": k5}


# ---------------------------------------------------------------- denetleyici (kendi yeniden yazım)
def psi_tab(u):
    return np.interp(u, CU, CPSI)


def psi_win(a, b, du):
    if b <= 0:
        return float(psi_tab(a))
    n = int(round(b / du))
    v = psi_tab(a + du * np.arange(n + 1))
    return float((v.sum() - 0.5 * (v[0] + v[-1])) / n)


_EMPC = {}


def emp_psi(fresh12, fc, W):
    if (fc, W) in _EMPC:
        return _EMPC[(fc, W)]
    m, z = fresh12; lu, ps = [], []
    for c in m["cond"]:
        if m["cond"][c][0] != fc:
            continue
        e, t = z[f"{c}_eff{W}"].mean(1), z[f"{c}_t0"].mean(1)
        for i, a in enumerate(m["arms"]):
            lu.append(np.log(fd(m, c) * m["lat"][a] / 1000)); ps.append((e[i] - RF) / (t[i] - RF))
    lu, ps = np.array(lu), np.array(ps)
    ed = np.linspace(lu.min(), lu.max() + 1e-9, 26)
    cen, med = [], []
    for j in range(25):
        s = (lu >= ed[j]) & (lu < ed[j + 1])
        if s.any():
            cen.append(lu[s].mean()); med.append(np.median(ps[s]))
    _EMPC[(fc, W)] = (np.array(cen), np.array(med))
    return _EMPC[(fc, W)]


def my_pick(m, cal, fresh12, c, W, allowed, same_cond_t0, fd_scale=1.0):
    mc, zc = cal; fc = m["cond"][c][0]; f = fd(m, c) * fd_scale
    ref = c if same_cond_t0 else [k for k in mc["cond"] if mc["cond"][k][0] == fc][0]
    t0 = zc[f"{ref}_t0"].mean(1)
    best, bv = None, -np.inf
    for a in m["arms"]:
        if a.split("+")[0] not in allowed:
            continue
        u = f * m["lat"][a] / 1000
        if fc == 3:
            p = psi_win(u, f * W / 1000, f * 2.0 / 1000)
        else:
            cen, med = emp_psi(fresh12, 28, W); p = float(np.interp(np.log(max(u, 1e-6)), cen, med))
        r = RF + (t0[mc["arms"].index(a)] - RF) * p
        if r > bv:
            best, bv = a, r
    return best


def my_pick_v0(m, cal, c, W):
    """Tur 0: her iki taşıyıcıda tasarım kuralı ψ'si."""
    mc, zc = cal; fc = m["cond"][c][0]; f = fd(m, c)
    ref = [k for k in mc["cond"] if mc["cond"][k][0] == fc][0]; t0 = zc[f"{ref}_t0"].mean(1)
    sc = [RF + (t0[i] - RF) * psi_win(f * m["lat"][a] / 1000, f * W / 1000, f * 2.0 / 1000) for i, a in enumerate(m["arms"])]
    return m["arms"][int(np.argmax(sc))]


def my_pick_v1emp(m, cal, fresh12, c, W):
    mc, zc = cal; fc = m["cond"][c][0]; f = fd(m, c)
    ref = [k for k in mc["cond"] if mc["cond"][k][0] == fc][0]; t0 = zc[f"{ref}_t0"].mean(1)
    cen, med = emp_psi(fresh12, fc, W)
    sc = [RF + (t0[i] - RF) * float(np.interp(np.log(f * m["lat"][a] / 1000), cen, med)) for i, a in enumerate(m["arms"])]
    return m["arms"][int(np.argmax(sc))]


# ---------------------------------------------------------------- değerlendirme
def eff(z, m, c, W, arm):
    return z[f"{c}_eff{W}"][m["arms"].index(arm)].astype(np.float64)


def keys(m):
    return [(c, W) for c in m["cond"] for W in WS]


def run_mode(m, z, cal, fresh12, sys_allowed, same_cond_t0):
    K = keys(m)
    picks = {f"{c}|W{W}": my_pick(m, cal, fresh12, c, W, sys_allowed, same_cond_t0) for c, W in K}
    bpk = {f"{c}|W{W}": baselines(m, cal, c) for c, W in K}
    orc = {}
    for c, W in K:
        e = z[f"{c}_eff{W}"].astype(np.float64); i = int(e.mean(1).argmax()); orc[f"{c}|W{W}"] = (m["arms"][i], e[i])
    xs = np.mean([eff(z, m, c, W, picks[f"{c}|W{W}"]) for c, W in K], 0)
    out = dict(S=int(len(xs)), system_mean=float(xs.mean()), oracle_mean=float(np.mean([v[1].mean() for v in orc.values()])),
               picks=picks, overall={}, per={})
    for n in ("K1", "K2", "K3", "K4", "K5"):
        xb = np.mean([eff(z, m, c, W, bpk[f"{c}|W{W}"][n]) for c, W in K], 0)
        d = xs - xb
        out["overall"][n] = dict(base_mean=float(xb.mean()), diff=float(d.mean()), ci=boot(d))
    for c, W in K:
        k = f"{c}|W{W}"; s = eff(z, m, c, W, picks[k])
        bn = max(("K1", "K2", "K3", "K4", "K5"), key=lambda n: eff(z, m, c, W, bpk[k][n]).mean())
        d = s - eff(z, m, c, W, bpk[k][bn])
        out["per"][k] = dict(system_pick=picks[k], system=float(s.mean()), best_baseline=bn, best_baseline_pick=bpk[k][bn],
                             best_baseline_mean=float(eff(z, m, c, W, bpk[k][bn]).mean()), diff=float(d.mean()), ci=boot(d),
                             oracle=float(orc[k][1].mean()), oracle_pick=orc[k][0])
    out["H_all"] = all(v["ci"][0] > 0 for v in out["overall"].values())
    out["H2"] = all(v["ci"][1] >= 0 for v in out["per"].values())
    out["_xs"] = xs; out["_bpk"] = bpk
    return out


def frozen_picks(fn, m, cal):
    return {f"{c}|W{W}": fn(m, cal, c, W) for c, W in keys(m)}


if __name__ == "__main__":
    rows, rep = [], {}

    def chk(label, rv, mine, tol):
        ok = (rv == mine) if isinstance(rv, str) else abs(rv - mine) <= tol
        rows.append((label, rv, mine, "OK" if ok else "HATA"))

    F12, F41, F14 = cube("seed12"), cube("seed41"), cube("seed14")
    W12, W41, W14 = cube("warm_seed12"), cube("warm_seed41"), cube("warm_seed14")
    # yapısal denetimler
    for nm, (m, z) in {"seed41": F41, "warm_seed41": W41}.items():
        rep[f"{nm}_meta"] = dict(commit=m["commit"], seed=m["seed"], S=int(z["A1_eff0"].shape[1]))
    rep["fresh_t0_same_across_conditions_per_carrier"] = {
        s: all(np.array_equal(z["A1_t0"], z[f"{c}_t0"]) for c in ("A2", "A3", "A4")) and np.array_equal(z["B1_t0"], z["B2_t0"])
        for s, (m, z) in {"12": F12, "14": F14, "41": F41}.items()}

    FJ = json.load(open(S / "FINAL.json"))
    import controllers as C, periodic as Pm
    for mode, (test, cal, allowed, same) in {"fresh": (F41, F12, ("avg", "best"), False),
                                             "periodic": (W41, W12, ("avg", "best", "warm"), True)}.items():
        m, z = test
        r = run_mode(m, z, cal, F12, allowed, same)
        fz = frozen_picks(C.v1b_carrier if mode == "fresh" else Pm.V4, m, cal)
        rep[f"{mode}_frozen_vs_mine_picks_equal"] = fz == r["picks"]
        fb = {k: {n: f(m, cal, *k.split("|W")[:1], int(k.split("|W")[1])) for n, f in C.BASE.items()} for k in r["picks"]}
        rep[f"{mode}_frozen_vs_mine_baselines_equal"] = fb == r["_bpk"]
        J = FJ[mode]
        chk(f"{mode}: S (senaryo)", 400, r["S"], 0)
        chk(f"{mode}: sistem ortalaması", J["system_mean"], r["system_mean"], 5e-5)
        chk(f"{mode}: kâhin ortalaması", J["oracle_mean"], r["oracle_mean"], 5e-5)
        chk(f"{mode}: kâhin açığı", J["oracle_mean"] - J["system_mean"], r["oracle_mean"] - r["system_mean"], 5e-5)
        for n, v in J["overall"].items():
            mv = r["overall"][n]
            chk(f"{mode}: {n} ortalaması", v["base_mean"], mv["base_mean"], 5e-5)
            chk(f"{mode}: sistem−{n}", v["diff"], mv["diff"], 5e-5)
            chk(f"{mode}: sistem−{n} GA alt", v["ci"][0], mv["ci"][0], 0.01)
            chk(f"{mode}: sistem−{n} GA üst", v["ci"][1], mv["ci"][1], 0.01)
        for k, v in J["per_condition"].items():
            mv = r["per"][k]
            for f_ in ("system_pick", "best_baseline", "best_baseline_pick", "oracle_pick"):
                chk(f"{mode} {k}: {f_}", v[f_], mv[f_], 0)
            for f_ in ("system", "best_baseline_mean", "diff", "oracle"):
                chk(f"{mode} {k}: {f_}", v[f_], mv[f_], 5e-5)
            chk(f"{mode} {k}: GA alt", v["ci"][0], mv["ci"][0], 0.01)
            chk(f"{mode} {k}: GA üst", v["ci"][1], mv["ci"][1], 0.01)
        hk = "H1" if mode == "fresh" else "H3"
        chk(f"{mode}: {hk} kararı", str(J["H_all_baselines"]), str(r["H_all"]), 0)
        if mode == "fresh":
            chk("fresh: H2 kararı", str(J["H2_no_condition_worse"]), str(r["H2"]), 0)
        rep[mode] = {k: v for k, v in r.items() if not k.startswith("_")}
        rep[mode]["min_ci_low_overall"] = min(v["ci"][0] for v in r["overall"].values())
        rep[mode]["max_per_cond_ci_upper_neg"] = [k for k, v in r["per"].items() if v["ci"][1] < 0]
        # H2 sınırına en yakın koşul: bootstrap tohumuna duyarlılık (20 farklı tohum)
        kmin = min([k for k in r["per"] if r["per"][k]["system_pick"] != r["per"][k]["best_baseline_pick"]], key=lambda k: r["per"][k]["ci"][1])
        cc, WW = kmin.split("|W")[0], int(kmin.split("|W")[1])
        dd = eff(z, m, cc, WW, r["per"][kmin]["system_pick"]) - eff(z, m, cc, WW, r["per"][kmin]["best_baseline_pick"])
        ups = [boot(dd, seed=s)[1] for s in range(20)]
        rep[f"{mode}_H2_closest"] = dict(cond=kmin, upper_min=min(ups), upper_max=max(ups), n_neg=sum(u < 0 for u in ups))
        if mode == "periodic":
            # Ek 1: "sıcak hatların taze-yalnız sisteme katkısı" (FINAL.md'de yok)
            rf = run_mode(m, z, cal, F12, ("avg", "best"), True)
            d = r["_xs"] - rf["_xs"]
            rep["periodic_warm_contribution_seed41"] = dict(v4=r["system_mean"], fresh_only=rf["system_mean"], diff=float(d.mean()), ci=boot(d))
        # K4 duyarlılığı: adım süresinin farklı ölçülmüş tanımları
        T2 = json.load(open(ROOT / "juri" / "raw" / "timing2.json"))
        sens = {}
        for lab, dT in (("adam_slope_ms", T2["adam_slope_ms"]), ("adam1", T2["median_ms"]["adam1"])):
            K = keys(m); xs = r["_xs"]
            xb = np.mean([eff(z, m, c, W, f"avg+{closed_form_L(dT, fd(m, c))}") for c, W in K], 0)
            sens[lab] = dict(dT=dT, K4_mean=float(xb.mean()), diff=float((xs - xb).mean()), ci=boot(xs - xb),
                             picks={c: closed_form_L(dT, fd(m, c)) for c in m["cond"]})
        rep[f"{mode}_K4_sensitivity"] = sens
        # K4 ile aynı kapalı form, ama SU-best-of başlangıcıyla (zayıf taban çizgisi denetimi)
        K = keys(m); xs = r["_xs"]
        xb = np.mean([eff(z, m, c, W, r["_bpk"][f"{c}|W{W}"]["K4"].replace("avg", "best")) for c, W in K], 0)
        rep[f"{mode}_K4_bestStart"] = dict(mean=float(xb.mean()), diff=float((xs - xb).mean()), ci=boot(xs - xb))
        # Sabit en iyi tek hat (tüm koşullarda aynı), seed 12'de seçilir -> seed 41
        mc, zc = cal; fresh_arms = [a for a in m["arms"] if not a.startswith("warm")]
        sel = max(fresh_arms, key=lambda a: np.mean([zc[f"{c}_eff{W}"][mc["arms"].index(a)].mean() for c, W in keys(mc)]))
        xb = np.mean([eff(z, m, c, W, sel) for c, W in K], 0)
        rep[f"{mode}_best_fixed_arm_seed12"] = dict(arm=sel, mean=float(xb.mean()), diff=float((xs - xb).mean()), ci=boot(xs - xb))
        if mode == "periodic":
            # aynı ölçüt, ama karşılaştırma yöntemlerine de sıcak başlangıç verilirse (K2w = warm+5, K4w = warm+L4)
            for n, f_ in (("K2_warm", lambda c, W: "warm+5"), ("K4_warm", lambda c, W: r["_bpk"][f"{c}|W{W}"]["K4"].replace("avg", "warm")),
                          ("K5_warm", lambda c, W: r["_bpk"][f"{c}|W{W}"]["K5"].replace("best", "warm").replace("avg", "warm"))):
                xb = np.mean([eff(z, m, c, W, f_(c, W)) for c, W in K], 0)
                rep[f"periodic_{n}"] = dict(mean=float(xb.mean()), diff=float((xs - xb).mean()), ci=boot(xs - xb))

    # ---------------------------------------------------------------- GÜNLÜK (seed 14) sayıları
    m, z = F14; K = keys(m)
    vec = lambda pk: np.mean([eff(z, m, c, W, pk(c, W)) for c, W in K], 0)
    bp = {(c, W): baselines(m, F12, c) for c, W in K}
    x0 = vec(lambda c, W: my_pick_v0(m, F12, c, W))
    x1 = vec(lambda c, W: my_pick_v1emp(m, F12, F12, c, W))
    x1b = vec(lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False))
    orc14 = float(np.mean([z[f"{c}_eff{W}"].mean(1).max() for c, W in K]))
    G = {}
    chk("GÜNLÜK tur0: v0 (seed 14)", 5.2869, float(x0.mean()), 5e-5)
    chk("GÜNLÜK tur0: kâhin", 5.2994, orc14, 5e-5)
    chk("GÜNLÜK tur0: açık", 0.0125, orc14 - float(x0.mean()), 1e-4)
    for n, rv, d, lo, hi in (("K1", 4.8701, .417, .384, .448), ("K2", 5.1053, .182, .156, .210), ("K3", 4.8436, .443, .406, .481),
                             ("K4", 5.1751, .112, .090, .134), ("K5", 5.1889, .098, .079, .117)):
        xb = vec(lambda c, W: bp[(c, W)][n]); ci = boot(x0 - xb)
        chk(f"GÜNLÜK tur0: {n} ortalaması", rv, float(xb.mean()), 5e-5)
        chk(f"GÜNLÜK tur0: v0−{n}", d, float((x0 - xb).mean()), 5e-4)
        chk(f"GÜNLÜK tur0: v0−{n} GA alt", lo, ci[0], 0.01); chk(f"GÜNLÜK tur0: v0−{n} GA üst", hi, ci[1], 0.01)
    chk("GÜNLÜK tur1: v1_emp", 5.2880, float(x1.mean()), 5e-5)
    ci = boot(x1 - x0); chk("GÜNLÜK tur1: v1_emp−v0", 0.0011, float((x1 - x0).mean()), 5e-5)
    chk("GÜNLÜK tur1: v1_emp−v0 GA alt", -0.008, ci[0], 0.01); chk("GÜNLÜK tur1: v1_emp−v0 GA üst", 0.010, ci[1], 0.01)
    chk("GÜNLÜK tur1: v1b", 5.2930, float(x1b.mean()), 5e-5)
    chk("GÜNLÜK tur1 / FROZEN: v1b kâhin açığı", 0.0063, orc14 - float(x1b.mean()), 5e-5)
    ci = boot(x1b - x0); chk("GÜNLÜK tur1: v1b−v0", 0.0062, float((x1b - x0).mean()), 5e-5)
    chk("GÜNLÜK tur1: v1b−v0 GA alt", 0.0019, ci[0], 0.003); chk("GÜNLÜK tur1: v1b−v0 GA üst", 0.0105, ci[1], 0.003)
    # tur 1 koşul başına açıklar
    def gap(pick, c, W):
        return float(z[f"{c}_eff{W}"].mean(1).max() - eff(z, m, c, W, pick(c, W)).mean())
    chk("GÜNLÜK tur0: B1 W0 v0 açığı", 0.051, gap(lambda c, W: my_pick_v0(m, F12, c, W), "B1", 0), 5e-4)
    chk("GÜNLÜK tur0: B2 W20 v0 açığı", 0.030, gap(lambda c, W: my_pick_v0(m, F12, c, W), "B2", 20), 5e-4)
    chk("GÜNLÜK tur0: A4 W20 v0 açığı", 0.027, gap(lambda c, W: my_pick_v0(m, F12, c, W), "A4", 20), 5e-4)
    chk("GÜNLÜK tur1: A4 W20 v1_emp açığı", 0.073, gap(lambda c, W: my_pick_v1emp(m, F12, F12, c, W), "A4", 20), 5e-4)
    chk("GÜNLÜK tur1: A2 W20 v1_emp açığı", 0.033, gap(lambda c, W: my_pick_v1emp(m, F12, F12, c, W), "A2", 20), 5e-4)
    chk("GÜNLÜK tur1: B1 W0 v1_emp açığı", 0.0, gap(lambda c, W: my_pick_v1emp(m, F12, F12, c, W), "B1", 0), 5e-4)
    # tur 2 (Doppler hatası): kendi seçicimle, f_d çarpanı yalnızca denetleyicide
    for s, rv in ((0.5, -0.106), (0.8, -0.009), (1.25, -0.000), (2.0, -0.058)):
        xs_ = vec(lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False, fd_scale=s))
        chk(f"GÜNLÜK tur2: v1b f_d×{s} kaybı", rv, float((xs_ - x1b).mean()), 5e-4)
    # tur 6: v1b'nin A1 seçimlerinin değerleri
    chk("GÜNLÜK tur6: A1 W0 v1b seçimi", "best+10", my_pick(m, F12, F12, "A1", 0, ("avg", "best"), False), 0)
    chk("GÜNLÜK tur6: A1 W0 v1b değeri", 6.222, float(eff(z, m, "A1", 0, "best+10").mean()), 5e-4)
    chk("GÜNLÜK tur6: A1 W20 v1b seçimi", "best+8", my_pick(m, F12, F12, "A1", 20, ("avg", "best"), False), 0)
    chk("GÜNLÜK tur6: A1 W20 v1b değeri", 5.871, float(eff(z, m, "A1", 20, "best+8").mean()), 5e-4)
    # tur 4 / 5: periyodik, seed 14
    for tag, rv in (("", dict(v4=5.3452, fr=5.2987, d=0.0465, lo=0.032, hi=0.062, orc=5.3544, best=0.143)),
                    ("_P50", dict(v4=5.3103, fr=5.3165, d=-0.006, lo=-0.022, hi=0.009, orc=5.3265, best=0.099))):
        mw, zw = cube(f"warm{tag}_seed14"); calw = cube(f"warm{tag}_seed12"); Kw = keys(mw)
        a = run_mode(mw, zw, calw, F12, ("avg", "best", "warm"), True); b = run_mode(mw, zw, calw, F12, ("avg", "best"), True)
        ci = boot(a["_xs"] - b["_xs"]); P = "P20" if tag == "" else "P50"
        chk(f"GÜNLÜK {P}: v4", rv["v4"], a["system_mean"], 5e-5)
        chk(f"GÜNLÜK {P}: yalnızca taze", rv["fr"], b["system_mean"], 5e-5)
        chk(f"GÜNLÜK {P}: v4−taze", rv["d"], a["system_mean"] - b["system_mean"], 5e-4)
        chk(f"GÜNLÜK {P}: v4−taze GA alt", rv["lo"], ci[0], 0.01); chk(f"GÜNLÜK {P}: v4−taze GA üst", rv["hi"], ci[1], 0.01)
        chk(f"GÜNLÜK {P}: kâhin", rv["orc"], a["oracle_mean"], 5e-5)
        chk(f"GÜNLÜK {P}: v4 − en iyi karşılaştırma", rv["best"], min(v["diff"] for v in a["overall"].values()), 5e-4)
        if tag == "":
            chk("FROZEN/GÜNLÜK tur4: kâhin açığı 0.009", 0.009, a["oracle_mean"] - a["system_mean"], 5e-4)
            rep["dev_P20_overall"] = a["overall"]
        else:
            rep["dev_P50_overall"] = a["overall"]
    # tur 3 (temkinli sapma) seed 12 seçim ortalamaları
    m12, z12 = F12
    for bfac, rv in ((1.0, 5.1247), (1.1, 5.1251), (1.25, 5.1203), (1.5, 5.1063), (2.0, 5.058)):
        xs_ = np.mean([eff(z12, m12, c, W, my_pick(m12, F12, F12, c, W, ("avg", "best"), False, fd_scale=bfac)) for c, W in keys(m12)], 0)
        chk(f"GÜNLÜK tur3: seed 12 b={bfac}", rv, float(xs_.mean()), 5e-4 if bfac != 2.0 else 5e-4)

    # tur 3 geliştirme farkları (b* = 1.1 − sapmasız), seed 14
    for s, rv in ((1.0, 0.0016), (0.5, 0.0083), (0.8, 0.0007), (1.25, -0.0066), (2.0, -0.0154)):
        xa = vec(lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False, fd_scale=s * 1.1))
        xb_ = vec(lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False, fd_scale=s))
        chk(f"GÜNLÜK tur3: seed 14 sapma farkı, hata ×{s}", rv, float((xa - xb_).mean()), 1e-4)
        if s == 1.0:
            rep["dev14_bias11_mean"] = float(xa.mean()); rep["dev14_v1b_mean"] = float(xb_.mean())
    # KEŞİFSEL (protokolde yok): seed 14'e göre yapılan seçimlerin seed 41'de sonucu
    m, z = F41; K = keys(m)
    vec41 = lambda pk: np.mean([eff(z, m, c, W, pk(c, W)) for c, W in K], 0)
    x1b41 = vec41(lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False))
    for n, pk in (("v0_rule", lambda c, W: my_pick_v0(m, F12, c, W)),
                  ("v1_emp", lambda c, W: my_pick_v1emp(m, F12, F12, c, W)),
                  ("v1b_bias1.1", lambda c, W: my_pick(m, F12, F12, c, W, ("avg", "best"), False, fd_scale=1.1))):
        x = vec41(pk); d = x1b41 - x
        rep[f"explore41_v1b_minus_{n}"] = dict(other_mean=float(x.mean()), diff=float(d.mean()), ci=boot(d))

    w = max(len(r[0]) for r in rows)
    for r in rows:
        print(f"{r[0]:<{w}}  rapor {r[1]!s:>12}  yeniden {r[2] if isinstance(r[2], str) else f'{r[2]:.5f}':>12}  {r[3]}")
    nh = sum(r[3] == "HATA" for r in rows)
    print(f"\n{len(rows)} denetim, {nh} HATA")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("fresh", "periodic")}, indent=1, default=str))
    for mode in ("fresh", "periodic"):
        print(mode, "H:", rep[mode]["H_all"], "H2:", rep[mode]["H2"], "min GA alt:", round(rep[mode]["min_ci_low_overall"], 4))
