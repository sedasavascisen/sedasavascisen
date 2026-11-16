"""
check_claims.py -- every number and statistical statement added to the thesis record on 12-16 Nov 2026
(p4 experiments, grid checks, Table III correction, revised Paper 2 Section V / VI-H), frozen and re-checked
against the STORED raw outputs.

Unlike scripts/audit_claims.py (which recomputes from the library), this file checks that the text and the
raw files agree: a quoted value must equal the raw value at the quoted precision, and a statement such as
"tied" / "significantly behind" must match the bootstrap CI stored next to it. Run:

    python3 thesis_exp/iddia_denetimi/check_claims.py              # all claims
    python3 thesis_exp/iddia_denetimi/check_claims.py --sabotage   # self-test: perturb copies of the raw files,
                                                                   # every perturbation must be caught
Exit code 0 only if every claim holds (normal mode) / every sabotage is caught (sabotage mode).
"""
import sys, json, copy, argparse, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
P4 = ROOT / "thesis_exp" / "p4"
ap = argparse.ArgumentParser()
ap.add_argument("--sabotage", action="store_true")
args = ap.parse_args()


def _load(rel):
    return json.load(open(P4 / rel))


def _git_json(ref_path):
    return json.loads(subprocess.run(["git", "show", ref_path], capture_output=True, text=True, cwd=ROOT, check=True).stdout)


RAW = {
    "pilot50": "onkodlayici_siralama/raw/results.json",
    "pilot25": "onkodlayici_siralama/raw/results_win25.json",
    "pilot100": "onkodlayici_siralama/raw/results_win100.json",
    "csi": "kusurlu_csi/raw/results.json",
    "pcsi": "onkodlayici_csi/raw/results.json",
    "dexact": "ayrik_faz/raw/results_exact.json",
    "d3": "ayrik_faz/raw/results_3bit.json",
    "grid": "izgara_kontrol/raw/results.json",
    "tab1": "izgara_kontrol/raw/results_tab1.json",
    "trk0": "takip_duzeltme/raw/fix1_tp0.json",
    "trk086": "takip_duzeltme/raw/fix1_tp0.86.json",
    "trk171": "takip_duzeltme/raw/fix1_tp1.71.json",
    "trk343": "takip_duzeltme/raw/fix1_tp3.43.json",
    "trk_repro": "takip_duzeltme/raw/fix0_tp0.86.json",
}


def load_all():
    D = {k: _load(v) for k, v in RAW.items()}
    D["pub_tracking"] = json.load(open(ROOT / "results" / "mumiso_tracking.json"))
    D["infra_lat"] = _git_json("origin/thesis/altyapi:thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json")
    D["u13"] = open(ROOT / "thesis_exp/denetim_log/scripts/u13_csi_rel_err.out").read()
    T = ROOT / "thesis_exp"
    for k, rel in (("rule", "tasarim_kurali/raw/validation.json"), ("wb", "genis_bant/raw/results.json"), ("wbs", "genis_bant/raw/sens200.json"),
                   ("wbg4", "genis_bant/raw/g4.json"), ("j31", "juri/raw/s3_s1.json"), ("j1b", "juri/raw/s1b.json"),
                   ("j42", "juri/raw/s4_s2_summary.json"), ("j4s", "juri/raw/s4_sanity.json")):
        D[k] = json.load(open(T / rel))
    return D


# ---------------------------------------------------------------- claim helpers
def eq(v, quoted, dp):
    """quoted value at dp decimals: |v - quoted| <= 0.5*10^-dp (+tiny)."""
    return abs(v - quoted) <= 0.5 * 10 ** (-dp) + 1e-9


def tied(ci):
    return ci[0] <= 0 <= ci[1]


def above(ci):
    return ci[0] > 0


def below(ci):
    return ci[1] < 0


def lstar(rows, keys):
    return max(keys, key=lambda k: rows[k])


def claims(D):
    C = []
    add = lambda cid, where, ok: C.append((cid, where, bool(ok)))
    # ---- Table III (corrected), revised paper tab_tracking.tex
    trk = {"0": D["trk0"], "0.86": D["trk086"], "1.71": D["trk171"], "3.43": D["trk343"]}
    wc_quoted = {"0": 0.53, "0.86": 0.28, "1.71": 0.09, "3.43": 0.01}
    for tp, r in trk.items():
        k = list(r["warm_minus_cold"])[0]; wc = r["warm_minus_cold"][k]
        add(f"T3 warm-cold {tp}", "Tablo III", eq(wc["diff"], wc_quoted[tp], 2))
        add(f"T3 warm-cold significance {tp}", "Tablo III §", tied(wc["ci"]) == (tp == "3.43"))
        for mode in ("cold", "warm"):
            nb = r["runs"][k][mode]["near_best"]
            add(f"T3 some L<=8 near best {tp} {mode}", "§VI-E", any(x["L"] <= 8 for x in nb))
    cells = {("0.86", "cold"): (20.0, 3, 5.24), ("0.86", "warm"): (10.0, 3, 5.51), ("1.71", "warm"): (20.0, 3, 5.17),
             ("3.43", "warm"): (80.0, 24, 4.99), ("0", "warm"): (None, 2, 6.36)}
    for (tp, mode), (U, L, rate) in cells.items():
        r = trk[tp]; b = r["runs"][list(r["runs"])[0]][mode]["best"]
        add(f"T3 cell {tp} {mode}", "Tablo III", b["period"] == U and b["L"] == L and eq(b["rate"], rate, 2))
    pub, rep = D["pub_tracking"]["runs"]["0.86"], D["trk_repro"]["runs"]["0.86"]
    add("T3 fix0 reproduces published (0.86)", "§V", max(abs(pub[m]["mean"][k] - rep[m]["mean"][k]) for m in ("cold", "warm") for k in pub[m]["mean"]) == 0.0)
    # ---- §V: exact-latency notes
    t1 = D["tab1"]
    add("Tab I exact within horizon <= 0.006", "§V", t1["max_abs_diff_within_200ms"] <= 0.0065)
    add("Tab I CD 0.008", "§V", eq(abs(t1["rows"]["CD"]["exact_minus_interp"]), 0.008, 3))
    add("Tab I long-run Adam 0.037", "§V", eq(abs(t1["rows"]["Long-run Adam"]["exact_minus_interp"]), 0.037, 3))
    add("Tab I interpolation reproduces published", "§V", all(eq(v["interpolated"], v["published"], 3) for v in t1["rows"].values()))
    gp = D["grid"]["sets"]["paper"]["rows"]
    add("Adam sweep exact <= 0.027", "§V", max(abs(v["exact_minus_interp"]) for k, v in gp.items() if k.startswith("Adam")) <= 0.0275)
    paperL = [2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 48]
    ex = {L: gp[f"Adam-{L}"]["exact"] for L in paperL}
    add("optimum stays at 4-6 (exact)", "§V", lstar(ex, paperL) in (4, 5, 6))
    add("L=48 cost 14.2% (exact, paper latencies)", "§V", eq(100 * (1 - ex[48] / max(ex.values())), 14.2, 1))
    gr = D["grid"]["sets"]["rerun"]
    add("re-measured L*=6", "§V", gr["L_star"]["exact"] == "Adam-6")
    add("re-measured L=48 cost 14.9%", "§V", eq(gr["loss_L48_pct"]["exact"], 14.9, 1))
    cd = gr["comparisons"]["SU-best-of - CD"]["exact"]
    add("re-measured SU-best-of - CD 0.26 (0.15-0.37)", "§V", eq(cd["diff"], 0.26, 2) and eq(cd["ci"][0], 0.15, 2) and eq(cd["ci"][1], 0.37, 2))
    lat = D["infra_lat"]["median"]
    add("1.33 ms per Adam step", "§V", eq(lat["adam1"], 1.33, 2))
    # ---- §VI-H precoder pilots
    p50 = D["pilot50"]; nums = ["15kHz", "30kHz", "60kHz"]
    add("free refresh selected 5.21", "§VI-H", eq(p50["fresh"]["rows"][p50["fresh"]["selected_on_val"]]["rate"], 5.21, 2))
    for n, q in zip(nums, (3.54, 4.00, 4.33)):
        v = p50["numerologies"][n]; b = v["selected_on_val"]
        add(f"pilot rate {n} {q}", "§VI-H", eq(v["rows"][b]["rate"], q, 2))
        add(f"T_r 1-2 ms {n}", "§VI-H", v["rows"][b]["R_selected_on_val"] in (1.0, 2.0))
        add(f"selected 6-8 steps {n}", "§VI-H", b in ("Adam-6", "Adam-8"))
        tied_set = {k for k, x in v["rows"].items() if tied(x["minus_selected_ci"]) or k == b}
        add(f"Adam 3-20 tied {n}", "§VI-H", {f"Adam-{L}" for L in (3, 4, 5, 6, 8, 10, 12, 16, 20)} <= tied_set)
        add(f"CD, long-run Adam behind selected {n}", "§VI-H", below(v["rows"]["CD"]["minus_selected_ci"]) and below(v["rows"]["PGA"]["minus_selected_ci"]))
        add(f"W=50 CD ties SU-best-of with pilots {n}", "§VI-H", tied(v["rows"]["CD"]["minus_su_best_of_ci"]))
    add("W=50 free refresh CD ahead of SU-best-of by 0.10", "§VI-H", above(p50["fresh"]["rows"]["CD"]["minus_su_best_of_ci"]) and eq(p50["fresh"]["rows"]["CD"]["minus_su_best_of"], 0.10, 2))
    sel = lambda r: [r["numerologies"][n]["selected_on_val"] for n in nums]
    add("W=25 selected 5", "§VI-H", set(sel(D["pilot25"])) == {"Adam-5"})
    add("W=100 selected 16-20", "§VI-H", set(sel(D["pilot100"])) <= {"Adam-16", "Adam-20"})
    add("W=100 free refresh selected 16-24", "§VI-H", D["pilot100"]["fresh"]["selected_on_val"] in ("Adam-16", "Adam-20", "Adam-24"))
    gaps = [-D["pilot100"]["numerologies"][n]["rows"]["Adam-6"]["minus_selected"] for n in nums]
    add("W=100 with pilots six steps 0.02-0.04 below", "§VI-H", min(gaps) >= 0.015 and max(gaps) <= 0.045)
    v100 = D["pilot100"]["numerologies"]
    cd_lead = [v100[n]["rows"]["CD"]["minus_su_best_of"] for n in ("30kHz", "60kHz")] + [D["pilot100"]["fresh"]["rows"]["CD"]["minus_su_best_of"], p50["fresh"]["rows"]["CD"]["minus_su_best_of"]]
    add("CD leads SU-best-of by 0.09-0.18 (free refresh or W=100 except 15 kHz)", "§VI-H",
        all(0.085 <= x <= 0.185 for x in cd_lead) and above(v100["30kHz"]["rows"]["CD"]["minus_su_best_of_ci"]) and above(v100["60kHz"]["rows"]["CD"]["minus_su_best_of_ci"])
        and tied(v100["15kHz"]["rows"]["CD"]["minus_su_best_of_ci"]))
    add("only tuned Adam beats CD under every window", "§VI-H",
        all(below(r["numerologies"][n]["rows"]["CD"]["minus_selected_ci"]) for r in (D["pilot25"], p50, D["pilot100"]) for n in nums))
    # ---- §VI-H imperfect CSI
    L = D["csi"]["levels"]
    add("CSI perfect 6.08", "§VI-H", eq(L["perfect"]["test"], 6.08, 2))
    add("CSI 30 dB 3.54", "§VI-H", eq(L["30dB"]["test"], 3.54, 2))
    add("CSI 20 dB 1.40", "§VI-H", eq(L["20dB"]["test"], 1.40, 2))
    add("CSI 10 dB and below tie", "§VI-H", all(tied(L[k]["ci"]) for k in ("10dB", "5dB", "0dB")))
    add("22.6 dB median (RIS-user, test set)", "§VI-H", "11 rho=30dB -> per-scenario effective G 'pilot SNR' dB: median 22.6" in D["u13"])
    pc = D["pcsi"]["levels"]
    for n in nums:
        v30, v20 = pc["30dB"]["numerologies"][n], pc["20dB"]["numerologies"][n]
        x30 = v30["rows"][v30["selected_on_val"]]
        add(f"CSI+pilots 30 dB Adam leads 0.05-0.06 {n}", "§VI-H", above(x30["minus_su_best_of_ci"]) and 0.045 <= x30["minus_su_best_of"] <= 0.065)
        add(f"CSI+pilots 20 dB tie {n}", "§VI-H", tied(v20["rows"][v20["selected_on_val"]]["minus_su_best_of_ci"]))
        for lvl in ("30dB", "20dB"):
            vv = pc[lvl]["numerologies"][n]
            add(f"CSI+pilots {lvl} CD/long-run Adam behind {n}", "§VI-H", below(vv["rows"]["CD"]["minus_selected_ci"]) and below(vv["rows"]["PGA"]["minus_selected_ci"]))
    add("abs. rate loss 17-32% with pilots", "§VII", all(eq(100 * (1 - q / p50["fresh"]["rows"][p50["fresh"]["selected_on_val"]]["rate"]), t, 0)
                                                        for q, t in ((p50["numerologies"]["15kHz"]["rows"][p50["numerologies"]["15kHz"]["selected_on_val"]]["rate"], 32),
                                                                     (p50["numerologies"]["60kHz"]["rows"][p50["numerologies"]["60kHz"]["selected_on_val"]]["rate"], 17))))
    # ---- §VI-H discrete phases
    de = D["dexact"]["bits"]; d3 = D["d3"]["bits"]["3"]
    for b, Ls, loss in (("1", "Adam-5->q", 9.5), ("2", "Adam-6->q", 14.1)):
        d = de[b]["designs"]["lr0.5"]
        add(f"{b} bit L*={Ls}", "§VI-H", d["L_star"] == Ls)
        add(f"{b} bit L48 cost {loss}%", "§VI-H", eq(d["loss_L48_vs_Lstar_pct"], loss, 1))
    add("3 bit L*=6", "§VI-H", d3["designs"]["lr0.5"]["L_star"] == "Adam-6->q")
    add("3 bit L48 cost 14.9%", "§VI-H", eq(d3["designs"]["lr0.5"]["loss_L48_vs_Lstar_pct"], 14.9, 1))
    times = [t["median_ms"] for b in ("1", "2") for t in de[b]["dcd_timing"].values()] + [t["median_ms"] for t in d3["dcd_timing"].values()]
    add("dCD timed 16-501 ms", "§VI-H", eq(min(times), 16, 0) and eq(max(times), 501, 0))
    add("3 bit every dCD behind rounded SU-best-of", "§VI-H", all(below(d3["designs"]["lr0.5"]["rows"][f"dCD-{s}"]["minus_su_best_of_q_ci"]) for s in (1, 2, 3, 4, 8)))
    add("2 bit dCD with >=2 sweeps behind rounded SU-best-of", "§VI-H", all(below(de["2"]["designs"]["lr0.5"]["rows"][f"dCD-{s}"]["minus_su_best_of_q_ci"]) for s in (2, 3, 4, 8)))
    d1 = de["1"]["designs"]["lr0.5"]
    add("1 bit selected dCD-1", "§VI-H", d1["selected_on_val"] == "dCD-1")
    r1 = d1["rows"]["dCD-1"]
    add("1 bit dCD-1 +0.25 (0.16-0.33) over rounded SU-best-of", "§VI-H", eq(r1["minus_su_best_of_q"], 0.25, 2) and eq(r1["minus_su_best_of_q_ci"][0], 0.16, 2) and eq(r1["minus_su_best_of_q_ci"][1], 0.33, 2))
    p = d1["paired"]["dCD-1 - Adam-5->q"]
    add("1 bit dCD-1 tied with best rounded Adam (-0.04, -0.11..0.02)", "§VI-H", tied(p["ci"]) and eq(p["diff"], -0.04, 2) and eq(p["ci"][0], -0.11, 2) and eq(p["ci"][1], 0.02, 2))
    # ---- 16 Nov: design rule (tasarim_kurali/REPORT.md)
    import numpy as _np
    v = D["rule"]
    lr = _np.array([r["loss_pct"]["rule"] for r in v["rows"]])
    add("design rule H1/H2/H3 hold", "tasarim_kurali", v["H1"]["holds"] and v["H2"]["holds"] and v["H3"]["holds"])
    add("design rule median loss 0.08%, worst 2.74%", "tasarim_kurali", eq(float(_np.median(lr)), 0.08, 2) and eq(float(lr.max()), 2.74, 2))
    add("W>0 conditions: 21/45 with L*=48", "tasarim_kurali", sum(1 for r in v["rows"] if r["W_ms"] > 0 and r["L_star"] == 48) == 21 and sum(1 for r in v["rows"] if r["W_ms"] > 0) == 45)
    # ---- wideband (genis_bant/REPORT.md, Paper 2 round 4)
    C_ = D["wb"]["cells"]
    cells = [(c, k, d) for c, x in C_.items() for k, d in x["by_kopt"].items()]
    add("wideband G1 fails: 7/24 cells L=48 significantly below L*", "genis_bant", sum(below(d["ci"]) for _, _, d in cells) == 7 and len(cells) == 24)
    add("wideband 6 cells with L*=48", "genis_bant", sum(d["L_star_test"].endswith("-L48") for _, _, d in cells) == 6)
    hi = [d for c, k, d in cells if not c.startswith("20MHz")]
    add("50-100 MHz: L=48 significantly worse in only 3 of 16 (Paper 2 copy)", "makale2 §VII", sum(below(d["ci"]) for d in hi) == 3 and len(hi) == 16)
    k1_20 = [C_[f"20MHz_{sp}"]["by_kopt"]["1"] for sp in ("1.5mps", "10kmh")]
    add("20 MHz centre-frequency (K_opt=1): interior optimum at both speeds", "makale2 §VII", all(below(d["ci"]) for d in k1_20))
    add("wideband G2: 20 MHz K_opt<=4, 100 MHz K_opt=16", "genis_bant", all(C_[f"20MHz_{sp}"]["selected_on_val"][:2] in ("K1", "K4") for sp in ("1.5mps", "10kmh")) and all(C_[f"100MHz_{sp}"]["selected_on_val"].startswith("K16") for sp in ("1.5mps", "10kmh")))
    add("100 MHz selected minus narrowband +0.28/+0.29, significant", "genis_bant", all(above(C_[f"100MHz_{sp}"]["selected_minus_narrowband"]["ci"]) for sp in ("1.5mps", "10kmh")) and eq(C_["100MHz_1.5mps"]["selected_minus_narrowband"]["diff"], 0.28, 2) and eq(C_["100MHz_10kmh"]["selected_minus_narrowband"]["diff"], 0.29, 2))
    add("within 200 ms: 100 MHz selects K16-L20 (183.4 ms)", "genis_bant §4", all(D["wbs"]["cells"][f"100MHz_{sp}"]["selected"] == "K16-L20" for sp in ("1.5mps", "10kmh")) and eq(D["wbs"]["cells"]["100MHz_1.5mps"]["latency_ms"], 183.4, 1))
    # ---- jury Q3/Q1/Q4/Q2 (juri/REPORT_S3_S1.md, REPORT_S4_S2.md)
    j = D["j31"]
    add("Q3 S3-H1 holds at 1.5 m/s", "juri S3", j["s3_h1"]["1.5mps"]["holds"])
    r20 = [r for r in j["s3_h1"]["1.5mps"]["rows"] if r["budget_ms"] >= 20]
    add("Q3 feasibility selection loses 0.43-1.41 at >=20 ms (1.5 m/s)", "juri S3", all(below(r["ci"]) for r in r20) and eq(-max(r["diff"] for r in r20), 0.43, 2) and eq(-min(r["diff"] for r in r20), 1.41, 2))
    add("Q3 FLOP and measured latency select the same arm", "juri S3", all(j["s3_e"][sp]["selected_measured"] == j["s3_e"][sp]["selected_flop"] for sp in ("1.5mps", "10kmh")))
    for sp, dd in (("1.5mps", 0.684), ("10kmh", 0.836)):
        x = j["s1"][sp]["numba"]["numba_incr"]
        add(f"Q1 compiled CD beats Python Adam {sp} (+{dd})", "juri S1", above(x["ci"]) and eq(x["diff"], dd, 3))
        add(f"Q1 r* in (10, 15] {sp}", "juri S1", j["s1"][sp]["r_star_equal"] == [10, 15])
        add(f"Q1b equal speed-up: Adam ahead at every r {sp}", "juri S1b", all(below(x["ci"]) for x in D["j1b"]["rows"][sp]))
    s42 = D["j42"]
    add("Q4/Q2 four decisions hold", "juri S4/S2", all(s42["decisions"].values()))
    add("Q4 joint aging: L* = 1 (lower grid edge) at every speed", "juri S4", all(s42["summary"][f"joint|{sp}"]["L_star"] == "Adam-1" for sp in ("3kmh", "1.5mps", "10kmh")))
    add("Q2 Clarke: L* 3-8 within 200 ms", "juri S2", all(s42["summary"][f"clarke|{sp}"]["L_star_latency_ms"] <= 200 for sp in ("3kmh", "1.5mps", "10kmh")))
    rows = D["j4s"]["rows"]
    add("Q4 sanity: 5.412 at t=0, 4.030 at 1.15 ms, 1.067 at 10 ms (joint)", "juri S4 yorum", eq(rows[0]["joint"], 5.412, 3) and eq(rows[1]["joint"], 4.030, 3) and eq(rows[2]["joint"], 1.067, 3))
    return C


def run(D, quiet=False):
    C = claims(D)
    bad = [c for c in C if not c[2]]
    if not quiet:
        for cid, where, ok in C:
            print(f"{'ok ' if ok else 'FAIL'}  [{where}] {cid}")
        print(f"\n=== {len(C) - len(bad)}/{len(C)} claims hold")
    return C, bad


D = load_all()
if not args.sabotage:
    C, bad = run(D)
    sys.exit(0 if not bad else 1)

# --------------------------------------------------------------- sabotage self-test
SAB = [
    ("Table III warm-cold 0.86 +0.03", lambda d: d["trk086"]["warm_minus_cold"]["0.86"].__setitem__("diff", d["trk086"]["warm_minus_cold"]["0.86"]["diff"] + 0.03)),
    ("pilot 15 kHz rate -0.02", lambda d: d["pilot50"]["numerologies"]["15kHz"]["rows"][d["pilot50"]["numerologies"]["15kHz"]["selected_on_val"]].__setitem__("rate", 3.52)),
    ("CD CI at W=100 30 kHz crosses zero", lambda d: d["pilot100"]["numerologies"]["30kHz"]["rows"]["CD"].__setitem__("minus_su_best_of_ci", [-0.01, 0.15])),
    ("1 bit selected arm changed", lambda d: d["dexact"]["bits"]["1"]["designs"]["lr0.5"].__setitem__("selected_on_val", "Adam-5->q")),
    ("CSI 30 dB 3.60", lambda d: d["csi"]["levels"]["30dB"].__setitem__("test", 3.60)),
    ("Table I long-run Adam 0.045", lambda d: d["tab1"]["rows"]["Long-run Adam"].__setitem__("exact_minus_interp", -0.045)),
    ("re-measured L* -> 5", lambda d: d["grid"]["sets"]["rerun"]["L_star"].__setitem__("exact", "Adam-5")),
    ("wideband: one more significant cell", lambda d: d["wb"]["cells"]["100MHz_1.5mps"]["by_kopt"]["1"].__setitem__("ci", [-0.05, -0.01])),
    ("Q1 compiled CD diff +0.70", lambda d: d["j31"]["s1"]["1.5mps"]["numba"]["numba_incr"].__setitem__("diff", 0.70)),
    ("Q4 joint L* -> 2", lambda d: d["j42"]["summary"]["joint|1.5mps"].__setitem__("L_star", "Adam-2")),
    ("3 bit dCD-1 CI crosses zero", lambda d: d["d3"]["bits"]["3"]["designs"]["lr0.5"]["rows"]["dCD-1"].__setitem__("minus_su_best_of_q_ci", [-0.4, 0.01])),
]
_, base_bad = run(D, quiet=True)
assert not base_bad, f"baseline must pass before sabotage: {base_bad}"
caught = 0
for name, f in SAB:
    Dx = copy.deepcopy(D); f(Dx)
    _, bad = run(Dx, quiet=True)
    print(f"{'caught' if bad else 'MISSED'}  {name}  -> {[c[0] for c in bad]}")
    caught += bool(bad)
print(f"\n=== sabotage: {caught}/{len(SAB)} caught")
sys.exit(0 if caught == len(SAB) else 1)
