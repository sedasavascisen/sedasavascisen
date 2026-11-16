"""
Decisions for jury questions 3 and 1, exactly as ON_KAYIT_S3_S1.md. Reads raw/arms.json and raw/timing.json,
writes raw/s3_s1.json and REPORT_S3_S1.md (+ yorum_s3_s1.md appended if present).
"""
import sys, json, pathlib, subprocess, itertools
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "p4"))
import numpy as np
from common import boot
H = pathlib.Path(__file__).parent; R = H / "raw"
D = json.load(open(R / "arms.json")); TMJ = json.load(open(R / "timing.json")); TM = TMJ["median_ms"]
BUDGETS = [2, 5, 10, 20, 50, 100, 200, 1000, 6000]
SP = {"1.5mps": "1.5 m/s", "10kmh": "10 km/h"}
FAST = ["SU-average", "SU-best-of"] + [k for k in D["lat_meas"] if k.startswith("Adam-")]
ARMS = list(D["lat_meas"])
res = dict(arms_commit=D["commit"], s3_h1={}, s3_e={}, s1={})


def get(seed, sp, key):
    return np.asarray(D["data"][f"{seed}|{sp}"]["eval"][key])


def t0(seed, sp, arm):
    return np.asarray(D["data"][f"{seed}|{sp}"]["t0"][arm])


def ktau(a, b):
    n = len(a); c = d = 0
    for i, j in itertools.combinations(range(n), 2):
        s = np.sign(a[i] - a[j]) * np.sign(b[i] - b[j])
        c += s > 0; d += s < 0
    return float((c - d) / (n * (n - 1) / 2))


for sp in SP:
    # ---- S3-H1: feasibility (t = 0) selection vs effective-rate selection, same budget
    rows = []
    for Bms in BUDGETS:
        cand = [a for a in ARMS if D["lat_meas"][a] <= Bms]
        ryu = max(cand, key=lambda a: t0(12, sp, a).mean())
        ours = max(cand, key=lambda a: get(12, sp, f"{a}@meas").mean())
        d = get(11, sp, f"{ryu}@meas") - get(11, sp, f"{ours}@meas")
        rows.append(dict(budget_ms=Bms, ryu=ryu, ours=ours, ryu_eff=float(get(11, sp, f"{ryu}@meas").mean()),
                         ours_eff=float(get(11, sp, f"{ours}@meas").mean()), diff=float(d.mean()),
                         ci=boot(d) if ryu != ours else [0.0, 0.0]))
    res["s3_h1"][sp] = dict(rows=rows, holds=any(r["ci"][1] < 0 for r in rows))
    # ---- S3-E: measured vs FLOP-predicted latency
    em = np.array([get(11, sp, f"{a}@meas").mean() for a in ARMS]); ef = np.array([get(11, sp, f"{a}@flop").mean() for a in ARMS])
    sel_m = max(ARMS, key=lambda a: get(12, sp, f"{a}@meas").mean()); sel_f = max(ARMS, key=lambda a: get(12, sp, f"{a}@flop").mean())
    res["s3_e"][sp] = dict(kendall_tau=ktau(em, ef), selected_measured=sel_m, selected_flop=sel_f,
                           eff_selected_measured_at_measured=float(get(11, sp, f"{sel_m}@meas").mean()),
                           eff_selected_flop_at_measured=float(get(11, sp, f"{sel_f}@meas").mean()),
                           ratio_meas_over_flop={a: D["lat_meas"][a] / D["lat_flop"][a] for a in ARMS})
    # ---- S1: break-even speed-up of tuned CD against the best fast arm
    ref = max(FAST, key=lambda a: get(12, sp, f"{a}@meas").mean()); rv = get(11, sp, f"{ref}@meas")
    s1 = []
    for r in D["rgrid"]:
        keys = [f"CD-{s}@r{r:g}" for s in range(1, 9)]
        k = max(keys, key=lambda x: get(12, sp, x).mean()); d = get(11, sp, k) - rv
        s1.append(dict(r=r, cd=k.split("@")[0], latency_ms=D["lat_s1"][k], cd_eff=float(get(11, sp, k).mean()), diff=float(d.mean()), ci=boot(d)))
    r_eq = next((x["r"] for x in s1 if x["diff"] >= 0), None); r_sig = next((x["r"] for x in s1 if x["ci"][0] > 0), None)
    prev = lambda r: None if r is None or D["rgrid"].index(r) == 0 else D["rgrid"][D["rgrid"].index(r) - 1]
    nb = {}
    for impl in ("numba_direct", "numba_incr"):
        keys = [f"CD-{s}@{impl}" for s in range(1, 9)]
        k = max(keys, key=lambda x: get(12, sp, x).mean()); d = get(11, sp, k) - rv
        s = int(k.split("@")[0][3:])
        nb[impl] = dict(cd=k.split("@")[0], latency_ms=D["lat_numba"][k], speedup_vs_torch=TM[f"cd{s}"] / TM[f"{impl}{s}"],
                        cd_eff=float(get(11, sp, k).mean()), diff=float(d.mean()), ci=boot(d))
    res["s1"][sp] = dict(reference=ref, ref_latency_ms=D["lat_meas"][ref], ref_eff=float(rv.mean()), rows=s1,
                         r_star_equal=[prev(r_eq), r_eq], r_star_significant=[prev(r_sig), r_sig], numba=nb)
json.dump(res, open(R / "s3_s1.json", "w"), indent=1)

# ------------------------------------------------------------------ report
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
yn = lambda b: "**TUTTU**" if b else "**TUTMADI**"
W("# Jüri soruları 3 ve 1 — ön kayıtlı sonuçlar"); W("")
W(f"Rapor commit'i `{commit}`, kol koşusu `{D['commit'][:7]}`. Ön kayıt `ON_KAYIT_S3_S1.md`. Seçim seed 12, rapor seed 11, 400 senaryo, "
  "Tanım 1 (tam gecikmede, interpolasyonsuz). GA: eşli bootstrap 2000, %95.")
W(""); W("## Soru 3 — Ryu tarzı uygulanabilirlik seçimi ile etkin hız seçimi"); W("")
for sp in SP:
    h = res["s3_h1"][sp]
    W(f"### {SP[sp]} — S3-H1 {yn(h['holds']) if sp == '1.5mps' else '(raporlanır)'}"); W("")
    W("| bütçe (ms) | t = 0'a göre seçilen | etkin hıza göre seçilen | etkin hız (t = 0 seçimi) | etkin hız (bizim) | fark [GA] |"); W("| --- | --- | --- | --- | --- | --- |")
    for r in h["rows"]:
        W(f"| {r['budget_ms']:g} | {r['ryu']} | {r['ours']} | {r['ryu_eff']:.3f} | {r['ours_eff']:.3f} | {r['diff']:+.3f} {ci(r['ci'])} |")
    W("")
W("### S3-E (keşifsel): FLOP'tan öngörülen gecikme ile ölçülmüş gecikme"); W("")
W(f"Bir hız değerlendirmesi E = {D['E_flops']} gerçel FLOP; ms/FLOP, Adam adımına kalibre ({D['ms_per_flop']*3*D['E_flops']:.3f} ms / 3E).")
W(""); W("| hız | Kendall τ (sıralama) | seçilen: ölçülmüş | seçilen: FLOP | FLOP seçiminin ölçülmüş gecikmedeki etkin hızı | ölçülmüş seçimin |"); W("| --- | --- | --- | --- | --- | --- |")
for sp in SP:
    e = res["s3_e"][sp]
    W(f"| {SP[sp]} | {e['kendall_tau']:.3f} | {e['selected_measured']} | {e['selected_flop']} | {e['eff_selected_flop_at_measured']:.3f} | {e['eff_selected_measured_at_measured']:.3f} |")
W(""); W("Ölçülmüş / FLOP-öngörülen gecikme oranı (kol başına):"); W("")
W("| kol | ölçülmüş (ms) | FLOP-öngörülen (ms) | oran |"); W("| --- | --- | --- | --- |")
for a in ["SU-average", "SU-best-of", "Adam-1", "Adam-8", "Adam-48", "CD-1", "CD-8", "Long-run Adam"]:
    W(f"| {a} | {D['lat_meas'][a]:.2f} | {D['lat_flop'][a]:.2f} | {D['lat_meas'][a] / D['lat_flop'][a]:.2f} |")
W(""); W("## Soru 1 — CD kaç kat hızlanırsa sıralama değişir?"); W("")
W(f"Zamanlama: yük başlangıç {TMJ['load']['start']:.2f}, ölçüm öncesi {TMJ['load']['before']:.2f}, sonrası {TMJ['load']['after']:.2f}; "
  f"rerun dosyasına göre sapma adam1 ×{TMJ['drift_vs_rerun']['adam1']:.3f}, adam48 ×{TMJ['drift_vs_rerun']['adam48']:.3f}, CD-8 ×{TMJ['drift_vs_rerun']['cd8']:.3f}.")
W(""); W("| tarama s | torch CD (ms) | numba doğrudan (ms) | numba artımlı (ms) | hızlanma doğrudan | hızlanma artımlı |"); W("| --- | --- | --- | --- | --- | --- |")
for s in range(1, 9):
    W(f"| {s} | {TM[f'cd{s}']:.2f} | {TM[f'numba_direct{s}']:.3f} | {TM[f'numba_incr{s}']:.3f} | {TM[f'cd{s}']/TM[f'numba_direct{s}']:.0f}× | {TM[f'cd{s}']/TM[f'numba_incr{s}']:.0f}× |")
for sp in SP:
    s = res["s1"][sp]
    W(""); W(f"### {SP[sp]} — karşılaştırma kolu {s['reference']} ({s['ref_latency_ms']:.2f} ms, etkin hız {s['ref_eff']:.3f})"); W("")
    W(f"- r*_eşit ∈ ({s['r_star_equal'][0]}, {s['r_star_equal'][1]}]; r*_anlamlı ∈ ({s['r_star_significant'][0]}, {s['r_star_significant'][1]}] (None: ızgarada ulaşılmadı)")
    for impl, nm in (("numba_direct", "doğrudan"), ("numba_incr", "artımlı")):
        x = s["numba"][impl]
        W(f"- Derlenmiş CD ({nm}), ayarlı {x['cd']}, {x['latency_ms']:.2f} ms (×{x['speedup_vs_torch']:.0f}): etkin hız {x['cd_eff']:.3f}, "
          f"− {s['reference']} = {x['diff']:+.3f} {ci(x['ci'])}")
    W(""); W("| r | ayarlı CD | gecikme (ms) | CD etkin hız | CD − hızlı kol [GA] |"); W("| --- | --- | --- | --- | --- |")
    for x in s["rows"]:
        W(f"| {x['r']:g} | {x['cd']} | {x['latency_ms']:.2f} | {x['cd_eff']:.3f} | {x['diff']:+.3f} {ci(x['ci'])} |")
W(""); W("Not (ön kayıt): Adam derlenmedi; derlenmiş CD ile Python Adam karşılaştırması tezin aleyhine taraflıdır.")
W(""); W("## Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/juri/timing.py | kanal 11, tek senaryo | raw/timing.json, raw/timing.log |")
W(f"| python3 thesis_exp/juri/arms.py ({D['seconds']/60:.0f} dk) | kanal 12, 11 | raw/arms.json, raw/arms.log |")
W("| python3 thesis_exp/juri/analyze_s3_s1.py | bootstrap 0 | raw/s3_s1.json |")
y = H / "yorum_s3_s1.md"
if y.exists():
    W(""); W("## Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT_S3_S1.md").write_text("\n".join(o) + "\n"); print("wrote")
