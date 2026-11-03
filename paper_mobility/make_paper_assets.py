"""
Builds every table and figure of the mobility paper from results/*.json.

No number in the paper's tables or figures is typed by hand: this script
reads the measurement files, writes LaTeX tables to tables/ and vector PDFs
to figures/, and prints the in-text numbers so they can be checked against
the prose.

    python3 paper_mobility/make_paper_assets.py
"""
import json
import pathlib
import statistics as st

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
RES = HERE.parent / "results"
FIG = HERE / "figures"
TAB = HERE / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)


def load(name):
    return json.load(open(RES / name))


plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.labelsize": 8,
    "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "lines.linewidth": 1.2, "lines.markersize": 4, "axes.grid": True,
    "grid.alpha": 0.3, "savefig.bbox": "tight", "pdf.fonttype": 42,
})
COL_W = 3.45
C = {"adam": "#1f5fa8", "learned": "#c2412d", "grey": "#555555",
     "su_average": "#7a7a7a", "su_best_of": "#2a9d8f", "adam8": "#1f5fa8",
     "pga": "#8e44ad", "cd": "#b5838d"}

out = []


def say(s=""):
    out.append(s)
    print(s)


# ------------------------------------------------------------------ aging
age = load("mumiso_aging_fixzf.json")
T_C = age["coherence_ms"]
times = np.array(age["times_ms"])
say(f"coherence time T_c = {T_C:.1f} ms; trust horizon {age['trust_ms']:.0f} ms")

# Latencies: SU heuristics, CD and long-run Adam as timed by
# scripts/mumiso_mobility_latency.py (one protocol, one machine); Adam-L on the
# same per-step model as the sweep (13.3 ms / 8), checked against that timing.
mlat = load("mumiso_mobility_latency.json")
MS_PER_STEP = 13.3 / 8
GRID_END = times.max()
eff = {}
for k in ["su_average", "su_best_of", "adam8", "adam12", "adam16", "adam20", "cd", "pga"]:
    lat = MS_PER_STEP * int(k[4:]) if k.startswith("adam") else mlat["median"][k]
    curve = age["curve"][k]
    eff[k] = dict(t0=curve[0], latency_ms=lat,
                  effective=float(np.interp(lat, times, curve)),
                  stale=age["stale"][k], trusted=lat <= age["trust_ms"],
                  beyond_grid=lat > GRID_END)
rows = list(eff)
say(f"mlat   cpu {mlat['cpu']}; load {mlat['load_before']:.2f}->{mlat['load_after']:.2f}; "
    + ", ".join(f"{k} {v:.3f}" for k, v in mlat["median"].items()))
say(f"mlat   adam per-step " + ", ".join(f"L{k}:{v:.2f}" for k, v in mlat["per_step"].items())
    + f"; slope {mlat['slope_ms_per_step']:.2f} ms/step; model {MS_PER_STEP:.3f}")
sp = {k: max(v) / min(v) for k, v in mlat["rounds"].items()}
say(f"mlat   round spread {min(sp.values()):.2f}-{max(sp.values()):.2f}")
names = {"su_average": "SU-average", "su_best_of": "SU-best-of",
         "adam8": "Adam, $L=8$", "adam12": "Adam, $L=12$",
         "adam16": "Adam, $L=16$", "adam20": "Adam, $L=20$",
         "cd": "Coord. descent", "pga": "Long-run Adam"}
stats = load("mumiso_aging_stats.json")
for k in rows:      # the per-scenario run must reproduce the stored means
    assert abs(stats["rows"][k]["effective"] - eff[k]["effective"]) < 1e-3, k
hw = [(r["effective_ci"][1] - r["effective_ci"][0]) / 2 for r in stats["rows"].values()]
say(f"stats  95% CI half-width of scenario means: {min(hw):.2f}-{max(hw):.2f} b/s/Hz")
for k in ("no_ris", "random"):
    r = stats["rows"][k]
    say(f"stats  {k}: {r['t0']:.3f} [{r['t0_ci'][0]:.3f}, {r['t0_ci'][1]:.3f}]")
lb = stats["link_budget"]
say(f"budget median per-user SNR: direct only {lb['direct_only_db']:.1f} dB, RIS path "
    f"(SU-average) {lb['ris_path_su_average_db']:.1f} dB, total {lb['total_su_average_db']:.1f} dB")
lines = [r"\begin{tabular}{lrrrr}", r"\toprule",
         r"Method & $t{=}0$ & Latency & Effective & Stale \\",
         r" & (b/s/Hz) & (ms) & (b/s/Hz) & (b/s/Hz) \\", r"\midrule",
         f"No RIS (direct link) & {stats['rows']['no_ris']['t0']:.3f} & -- & -- & -- \\\\",
         f"Random phase & {stats['rows']['random']['t0']:.3f} & -- & -- & -- \\\\"]
for k in rows:
    e = eff[k]
    lat = f"{e['latency_ms']:.2f}" if e["latency_ms"] < 1 else f"{e['latency_ms']:.1f}"
    mark = ("" if e["trusted"] else r"$^\dagger$") + (r"$^\ast$" if e["beyond_grid"] else "")
    lines.append(f"{names[k]} & {e['t0']:.3f} & {lat} & {e['effective']:.3f}{mark} "
                 f"& {e['stale']:.3f} \\\\")
    say(f"aging  {k:11s} t0 {e['t0']:.3f}  lat {e['latency_ms']:7.2f}  "
        f"eff {e['effective']:.3f}  stale {e['stale']:.3f}  trusted {e['trusted']}")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_aging.tex").write_text("\n".join(lines) + "\n")

fig, ax = plt.subplots(figsize=(COL_W, 2.3))
for k in ("pga", "adam8", "su_best_of", "su_average"):
    ax.plot(times, age["curve"][k], marker="o", ms=2.5, color=C[k],
            label={"pga": "Long-run Adam (1000 steps, 3 starts)"}.get(k, names[k].replace("$", "")))
ax.axvline(T_C, color="k", ls="--", lw=0.8)
ax.text(T_C * 1.08, 7.0, r"$T_c$", fontsize=7)
ax.axvspan(age["trust_ms"], times.max() * 1.2, color="0.9", zorder=0)
ax.text(age["trust_ms"] * 1.15, 6.95, "model\noptimistic", fontsize=6, color="0.35",
        va="top")
ax.set_xscale("symlog", linthresh=1.0)
ax.set_xlim(0, times.max() * 1.2)
ax.set_xlabel(r"Time since the phase was computed, $\tau$ (ms)")
ax.set_ylabel("Min-user rate (b/s/Hz)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2, frameon=False)
fig.savefig(FIG / "fig_aging.pdf", metadata={"CreationDate": None})
plt.close(fig)

# ------------------------------------------------------- intrinsic optimum
# check: the finer sensitivity sweep must contain the reproduction run
sens = load("mumiso_aging_sensitivity.json")
base = sens["by_velocity"]["1.5"]["by_overhead"]["0.0"]["rows"]
rep_rows = {r["L"]: r for r in load("mumiso_aging_sweep_repro.json")}
for r in base:
    if r["L"] in rep_rows:
        assert abs(r["effective"] - rep_rows[r["L"]]["effective"]) < 1e-6, r["L"]
sw = base
L = np.array([r["L"] for r in sw])
t0 = np.array([r["t0"] for r in sw])
ef = np.array([r["effective"] for r in sw])
lat = np.array([r["latency_ms"] for r in sw])
ib = int(np.argmax(ef))
loss48 = 1 - ef[-1] / ef[ib]
say(f"sweep  best L={L[ib]} eff {ef[ib]:.4f} at {lat[ib]:.2f} ms;  "
    f"L={L[-1]} eff {ef[-1]:.4f} ({loss48:.1%} below);  t0 at L=48 {t0[-1]:.4f}")
for r in sw:
    say(f"sweep  L={r['L']:2d} lat {r['latency_ms']:6.2f} t0 {r['t0']:.4f} eff {r['effective']:.4f}")

fig, ax = plt.subplots(figsize=(COL_W, 2.3))
ax.plot(L, t0, "s--", color=C["grey"], mfc="white", label=r"$t{=}0$ rate (no aging)")
ax.plot(L, ef, "o-", color=C["adam"], label="Effective rate, Adam (1.66 ms/step)")
scl = load("mumiso_step_scaling.json")
arm = scl["armijo"]
aL = np.array(arm["steps"]); aE = np.array([arm["eff_by_L"][str(x)] for x in arm["steps"]])
keep = aL <= 48
ax.plot(aL[keep], aE[keep], "^:", color=C["learned"], ms=3.5,
        label=f"Effective rate, Armijo ({arm['ms_per_step']:.2f} ms/step)")
ax.plot(L[ib], ef[ib], "*", color=C["learned"], ms=11, zorder=5)
ax.annotate(f"best: $L={L[ib]}$, {ef[ib]:.3f}", (L[ib], ef[ib]),
            xytext=(6.5, 4.85), fontsize=7,
            arrowprops=dict(arrowstyle="-", lw=0.6))
ax.annotate(f"$L={L[-1]}$: {ef[-1]:.3f}\n({-loss48:.1%} vs. best)", (L[-1], ef[-1]),
            xytext=(L[-1] - 20, ef[-1] - 0.38), fontsize=7,
            arrowprops=dict(arrowstyle="-", lw=0.6))
ax.set_xlabel(r"Optimizer steps $L$")
ax.set_ylabel("Min-user rate (b/s/Hz)")
ax.set_ylim(4.6, 7.3)
ax.legend(loc="center", bbox_to_anchor=(0.62, 0.47), fontsize=6)
fig.savefig(FIG / "fig_intrinsic_optimum.pdf", metadata={"CreationDate": None})
plt.close(fig)

say(f"sweep  t0 at best L {t0[ib]:.4f}; t0 rise best->48 {t0[-1]/t0[ib]-1:.1%}")

# ------------------------------------------------------------ sensitivity
vel = list(sens["by_velocity"])
ovs = list(sens["by_velocity"][vel[0]]["by_overhead"])
lines = [r"\begin{tabular}{l" + "r" * len(ovs) + "}", r"\toprule",
         r"& \multicolumn{%d}{c}{Acquisition delay $T_{\mathrm{ov}}$ (ms)} \\" % len(ovs),
         r"$v$ (m/s), $T_c$ & " + " & ".join(f"{float(o):g}" for o in ovs) + r" \\",
         r"\midrule"]
for v in vel:
    blk = sens["by_velocity"][v]
    cells = []
    for o in ovs:
        e = blk["by_overhead"][o]
        flag = r"$^\ddagger$" if float(o) > blk["coherence_ms"] / 2 else ""
        near = [r["L"] for r in e["rows"] if r["L"] > 0 and r["effective"] >= 0.995 * e["best_eff"]]
        rng = f"{min(near)}" if min(near) == max(near) else f"{min(near)}--{max(near)}"
        cells.append(f"{e['best_L']}{flag} ({rng})")
        say(f"sens   v={v} T_ov={o} L within 0.5%: {near}")
        say(f"sens   v={v} T_ov={o} best L={e['best_L']} eff {e['best_eff']:.4f} "
            f"spread {max(r['effective'] for r in e['rows'])-min(r['effective'] for r in e['rows']):.3f}")
    lines.append(f"{float(v):g}, {blk['coherence_ms']:.1f}~ms & " + " & ".join(cells) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_sensitivity.tex").write_text("\n".join(lines) + "\n")
l48 = [1 - [r for r in e["rows"] if r["L"] == 48][0]["effective"] / e["best_eff"]
       for v in vel for o, e in sens["by_velocity"][v]["by_overhead"].items()
       if float(o) <= sens["by_velocity"][v]["coherence_ms"] / 2]
say(f"sens   L=48 loss vs optimum (unflagged cells): {min(l48):.1%}-{max(l48):.1%}")
for va, row in sens["mismatch"].items():
    say(f"mism   assumed {va} (L={row[va]['L']}): " +
        ", ".join(f"true {vt}: {x['loss']:.2%}" for vt, x in row.items()))

for lr in ("0.25", "0.75", "1.0"):
    e = load(f"mumiso_aging_lr{lr}.json")["by_velocity"]["1.5"]["by_overhead"]["0.0"]
    r48 = [r for r in e["rows"] if r["L"] == 48][0]["effective"]
    say(f"lr     {lr}: best L={e['best_L']} eff {e['best_eff']:.4f}; L=48 {r48:.4f} "
        f"({1 - r48 / e['best_eff']:.1%} below)")
pc = load("mumiso_precoder_vs_step.json")
rr = [x["ratio"] for x in pc["rounds"]]
say(f"precod median precoder {pc['median']['precoder_ms']*1e3:.0f} us, adam step "
    f"{pc['median']['adam_step_ms']*1e3:.0f} us, ratio median {pc['median']['ratio']:.1f} "
    f"range {min(rr):.1f}-{max(rr):.1f}; load {pc['load_before']:.2f}->{pc['load_after']:.2f}")

# ------------------------------------------------------------ equal step
eq = load("mumiso_equal_step.json")
lines = [r"\begin{tabular}{rrrrrr}", r"\toprule",
         r"$L$ & Learned & Adam & Ratio & Diff.\,$-2$\,s.e. & Wins \\",
         r" & (b/s/Hz) & (b/s/Hz) & & (b/s/Hz) & (\%) \\", r"\midrule"]
for k in sorted(eq["rows"], key=int):
    v = eq["rows"][k]
    lo = v["paired_mean_diff"] - 2 * v["paired_sem"]
    lines.append(f"{k} & {v['learned']:.3f} & {v['swept']:.3f} & "
                 f"{v['learned_over_swept']:.3f} & {lo:+.3f} & "
                 f"{100 * v['learned_wins_frac']:.1f} \\\\")
    say(f"eqstep L={k:>2} learned {v['learned']:.4f} adam {v['swept']:.4f} "
        f"ratio {v['learned_over_swept']:.3f} lo {lo:+.4f} win {100*v['learned_wins_frac']:.1f}% "
        f"lr {v['best_lr']} obj {v['best_obj']}")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_equal_step.tex").write_text("\n".join(lines) + "\n")
say(f"eqstep anchor {eq['anchor']:.4f}; config samples={eq['config']['samples']} "
    f"eval_n={eq['config']['eval_n']} val_n={eq['config']['val_n']}")

# ---------------------------------------------------- equal milliseconds
lat_ = load("mumiso_latency_parity.json")
rep = load("mumiso_latency_repeat.json")
lm = {int(k): st.median(v) for k, v in rep["learned"].items()}
am = {int(k): st.median(v) for k, v in rep["adam"].items()}
lr_ = {int(k): v["rate"] for k, v in lat_["learned"].items()}
ar_ = {int(k): v["rate"] for k, v in lat_["classical"].items()}


def dominated_in_round(Lk, r):
    """Is learned L dominated by some Adam budget using round r's timings?"""
    tl = rep["learned"][str(Lk)][r]
    return any(rep["adam"][str(k)][r] <= tl and ar_[k] >= lr_[Lk] for k in am)


n_rounds = len(rep["learned"]["1"])
lines = [r"\begin{tabular}{rrr|rrr}", r"\toprule",
         r"\multicolumn{3}{c|}{Learned update} & \multicolumn{3}{c}{Dominating Adam} \\",
         r"$L$ & ms & b/s/Hz & $L$ & ms & b/s/Hz \\", r"\midrule"]
dom_points = []
for Lk in sorted(lm):
    cands = [(k, am[k], ar_[k]) for k in am if am[k] <= lm[Lk] and ar_[k] >= lr_[Lk]]
    rounds = sum(dominated_in_round(Lk, r) for r in range(n_rounds))
    if cands:
        k, ms, r = max(cands, key=lambda t: t[2])
        dom_points.append((Lk, k))
        lines.append(f"{Lk} & {lm[Lk]:.2f} & {lr_[Lk]:.3f} & {k} & {ms:.2f} & {r:.3f} \\\\")
    else:
        lines.append(f"{Lk} & {lm[Lk]:.2f} & {lr_[Lk]:.3f} & \\multicolumn{{3}}{{c}}{{none}} \\\\")
    say(f"eqms   learned L={Lk:>2} {lm[Lk]:6.2f} ms rate {lr_[Lk]:.4f} -> "
        f"{'Adam L=%d %.2f ms %.4f' % (k, ms, r) if cands else 'FRONT'}; "
        f"dominated in {rounds}/{n_rounds} rounds")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_equal_ms.tex").write_text("\n".join(lines) + "\n")
ps_l = {k: lm[k] / k for k in lm}
ps_a = {k: am[k] / k for k in am}
ratios = [ps_l[k] / ps_a[k] for k in lm if k in am and k >= 2]
say("per-step ms learned " + ", ".join(f"L{k}:{v:.2f}" for k, v in ps_l.items()))
say("per-step ms adam    " + ", ".join(f"L{k}:{v:.2f}" for k, v in ps_a.items()))
say(f"per-step cost ratio (L>=2): {min(ratios):.2f}-{max(ratios):.2f}")
spread = []
for side in ("learned", "adam"):
    for k, v in rep[side].items():
        spread.append(max(v) / min(v))
say(f"round-to-round timing spread (max/min): {min(spread):.2f}-{max(spread):.2f}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.1, 2.4))
ks = sorted(lm)
x = np.arange(len(ks))
a1.bar(x - 0.19, [lr_[k] for k in ks], 0.38, color=C["learned"], label="Learned update")
a1.bar(x + 0.19, [eq["rows"][str(k)]["swept"] for k in ks], 0.38, color=C["adam"],
       label="Tuned Adam")
a1.set_xticks(x, [f"$L={k}$" for k in ks])
a1.set_ylim(4.0, 6.2)
a1.set_ylabel("Min-user rate (b/s/Hz)")
a1.set_title("(a) Equal number of steps", fontsize=8)
a1.legend(loc="upper left")
a1.grid(axis="x", visible=False)
ka = sorted(am)
a2.plot([am[k] for k in ka], [ar_[k] for k in ka], "s-", color=C["adam"], label="Tuned Adam")
a2.plot([lm[k] for k in ks], [lr_[k] for k in ks], "o-", color=C["learned"],
        label="Learned update")
for k in ka:
    a2.annotate(f"{k}", (am[k], ar_[k]), xytext=(-3, 5), textcoords="offset points",
                fontsize=6, color=C["adam"])
for k in ks:
    a2.annotate(f"{k}", (lm[k], lr_[k]), xytext=(3, -9), textcoords="offset points",
                fontsize=6, color=C["learned"])
a2.set_xscale("log")
a2.set_xlabel("Measured latency (ms, median of 5 rounds)")
a2.set_title("(b) Equal milliseconds", fontsize=8)
a2.legend(loc="lower right")
fig.tight_layout()
fig.savefig(FIG / "fig_equal_step_vs_ms.pdf", metadata={"CreationDate": None})
plt.close(fig)

# ---------------------------------------------------------- beam staleness
bs = {"su_average": load("mumiso_beam_staleness_su_average.json"),
      "su_best_of": load("mumiso_beam_staleness.json"),
      "adam8": load("mumiso_beam_staleness_adam8.json")}
lines = [r"\begin{tabular}{lrrr}", r"\toprule",
         r"Phase chosen at $t=0$ & Fresh beam & Stale beam & Ratio \\",
         r" & (b/s/Hz) & (b/s/Hz) & \\", r"\midrule"]
bnames = {"su_average": "SU-average", "su_best_of": "SU-best-of", "adam8": "Adam, $L=8$"}
for k, d in bs.items():
    c = d["at_coherence"]
    assert d["config"]["phase"] == k, (k, d["config"]["phase"])
    lines.append(f"{bnames[k]} & {c['fresh']:.3f} & {c['stale']:.3f} & "
                 f"{c['ratio']:.1f}$\\times$ \\\\")
    say(f"beam   {k:11s} at {c['t_ms']} ms fresh {c['fresh']:.4f} stale {c['stale']:.4f} "
        f"ratio {c['ratio']:.2f}  (scen {d['config']['scenarios']}, tx {d['config']['tx']})")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_beam_staleness.tex").write_text("\n".join(lines) + "\n")

fig, ax = plt.subplots(figsize=(COL_W, 2.0))
for k, d in bs.items():
    t = [r["t_ms"] for r in d["rows"]]
    ax.plot(t, [r["fresh"] for r in d["rows"]], "o-", color=C[k], ms=2.5,
            label=f"{bnames[k]}, fresh beam".replace("$", ""))
    ax.plot(t, [r["stale"] for r in d["rows"]], "x--", color=C[k], ms=3,
            label=f"{bnames[k]}, stale beam".replace("$", ""))
ax.axvline(T_C, color="k", ls="--", lw=0.8)
ax.set_xscale("symlog", linthresh=1.0)
ax.set_xlim(0, 260)
ax.set_xlabel(r"Time since phase and beam were computed, $\tau$ (ms)")
ax.set_ylabel("Min-user rate (b/s/Hz)")
ax.legend(ncol=2, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, -0.28),
          frameon=False)
fig.savefig(FIG / "fig_beam_staleness.pdf", metadata={"CreationDate": None})
plt.close(fig)

# ------------------------------------------------------- step-cost scaling
sc = scl["scaling"]
ms_ = sorted(sc, key=float)
xs = np.array([sc[m]["x"] for m in ms_])
Ls = np.array([sc[m]["best_L"] for m in ms_])
lo_ = np.array([min(sc[m]["not_sig_below_best"]) for m in ms_])
hi_ = np.array([max(sc[m]["not_sig_below_best"]) for m in ms_])
loss = np.array([sc[m]["loss_L256"]["mean"] for m in ms_]) * 100
lci = np.array([sc[m]["loss_L256"]["ci"] for m in ms_]) * 100
for m in ms_:
    v = sc[m]
    say(f"scale  m={m} dT={v['ms_per_step']:.3f} ms x={v['x']:.4f} L*={v['best_L']} "
        f"near={v['not_sig_below_best']} best={v['best_eff']:.3f} "
        f"lossL256={100*v['loss_L256']['mean']:.1f}% [{100*v['loss_L256']['ci'][0]:.1f},"
        f"{100*v['loss_L256']['ci'][1]:.1f}] beyond200={v['L256_beyond_trust']}")
pm = scl["paper_m1"]
say(f"scale  m=1 loss L48 vs L5 {100*pm['loss_L48_vs_L5']:.1f}% "
    f"[{100*pm['ci'][0]:.1f}, {100*pm['ci'][1]:.1f}]")
say(f"scale  adam t0 L64..256: " + ", ".join(f"{L}:{scl['adam_t0_by_L'][str(L)]:.3f}" for L in (48, 64, 96, 128, 256)))
at = arm["timing"]
q = np.array(at["rounds_armijo"]) / np.array(at["rounds_adam"])
say(f"armijo ratio {at['ratio']:.2f} (per-scenario {q.min():.2f}-{q.max():.2f}); "
    f"ms/step {arm['ms_per_step']:.2f}; best L={arm['best_L']} eff {arm['best_eff']:.3f} "
    f"near={arm['not_sig_below_best']}; load {at['load_at_script_start']:.2f}/{at['load_before']:.2f}")
av = scl["adam_vs_armijo_best"]
say(f"armijo adam best minus armijo best {av['diff']:.3f} [{av['ci'][0]:.3f}, {av['ci'][1]:.3f}]; "
    f"t0 L=48 armijo {arm['t0_by_L']['48']:.3f} adam {scl['adam_t0_by_L']['48']:.3f}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(COL_W, 1.9))
a1.fill_between(xs, lo_, hi_, color=C["adam"], alpha=0.18, lw=0)
a1.plot(xs, Ls, "o-", color=C["adam"])
a1.set_xscale("log"); a1.set_yscale("log")
a1.set_xlabel(r"$x=\Delta T\, f_d$")
a1.set_ylabel(r"Best step count $L^\star$")
a1.set_title("(a) Optimum", fontsize=8)
a2.errorbar(xs, loss, yerr=[loss - lci[:, 0], lci[:, 1] - loss], fmt="o-", color=C["adam"],
            ms=3, capsize=2, lw=1.0)
a2.set_xscale("log")
a2.set_xlabel(r"$x=\Delta T\, f_d$")
a2.set_ylabel(r"Loss of $L{=}256$ vs. $L^\star$ (%)")
a2.set_title("(b) Cost of convergence", fontsize=8)
x1 = sc["1.0"]["x"]
for a_ in (a1, a2):
    a_.axvline(x1, color="0.5", ls="--", lw=0.7)
a1.text(x1 * 1.15, 60, "this\nsetup", fontsize=6, color="0.35", va="top")
fig.tight_layout()
fig.savefig(FIG / "fig_step_scaling.pdf", metadata={"CreationDate": None})
plt.close(fig)

# ---------------------------------------------------------------- tracking
trk = load("mumiso_tracking.json")
tL = trk["steps"]
ovs_t = trk["overheads"]
lines = [r"\begin{tabular}{r" + "rr" * len(ovs_t) + "}", r"\toprule",
         " & " + " & ".join(r"\multicolumn{2}{c}{$T_{\mathrm{ov}}=%g$~ms}" % o for o in ovs_t) + r" \\",
         r"$L$ & " + " & ".join(["cold", "warm"] * len(ovs_t)) + r" \\", r"\midrule"]
best = {}
for o in ovs_t:
    for mode in ("cold", "warm"):
        best[(o, mode)] = trk["runs"][f"{o}|{mode}"]
for L in tL:
    cells = []
    for o in ovs_t:
        for mode in ("cold", "warm"):
            r = best[(o, mode)]
            v = f"{r['mean_by_L'][str(L)]:.2f}"
            cells.append(r"\textbf{%s}" % v if L in r["not_sig_below_best"] else v)
    lines.append(f"{L} & " + " & ".join(cells) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_tracking.tex").write_text("\n".join(lines) + "\n")
for o in ovs_t:
    for mode in ("cold", "warm"):
        r = best[(o, mode)]
        say(f"track  T_ov={o} {mode}: best L={r['best_L']} {r['best']:.3f} "
            f"[{r['ci_best'][0]:.3f}, {r['ci_best'][1]:.3f}] near={r['not_sig_below_best']} "
            f"L48 {r['mean_by_L']['48']:.3f} ({1 - r['mean_by_L']['48'] / r['best']:.1%} below)")

# ---------------------------------------------------------- pilot overhead
Kp, Np, Mp = 4, 32, 8
n_min = Kp + Np + max(Kp - 1, int(np.ceil((Kp - 1) * Np / Mp)))
n_sep = Kp * (Np + 1)
for scs in (15, 30, 60):
    tsym = 15.0 / (14 * scs)                 # ms per OFDM symbol: 14 per slot of 15/scs ms
    say(f"pilot  SCS {scs} kHz: symbol {tsym*1e3:.1f} us; {n_min} symbols -> "
        f"{n_min*tsym:.2f} ms; {n_sep} symbols -> {n_sep*tsym:.2f} ms")

# ------------------------------------------------------------- scenario
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

geo = load("mumiso_scenario_geometry.json")
room = np.array(geo["room"])
bs = np.array(geo["bs_pos"])
ris = np.array(geo["ris_elements"])
ris_c = ris.mean(0)
ues = np.array(geo["users_t0"])
scat = np.array(geo["scatterers"])
head = np.array(geo["heading_rad"])
UCOL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]   # validated categorical slots 1-4
INK, GREY = "#2b2b2b", "#9a9a9a"
say(f"scen   {geo['source']}, index {geo['index']}; replay error {geo['replay_max_error_m']:.1e} m; "
    f"LoS BS-RIS {geo['los_ris_bs']}, RIS-UE {geo['los_ris_ue']}, direct {geo['los_direct']}")

fig = plt.figure(figsize=(7.16, 3.05))
gs = fig.add_gridspec(2, 2, width_ratios=[1.75, 1.0], height_ratios=[1.0, 1.0],
                      wspace=0.16, hspace=0.62, left=0.06, right=0.99, top=0.93, bottom=0.2)
ax = fig.add_subplot(gs[:, 0])
ax.add_patch(Rectangle((0, 0), room[0], room[1], fill=False, lw=1.0, ec=INK))
ax.plot([0, room[0]], [0, 0], color=INK, lw=2.2, solid_capstyle="butt")
ax.scatter(scat[:, 0], scat[:, 1], s=7, c=GREY, marker="o", lw=0, zorder=2)
ls_bs = "-" if geo["los_ris_bs"] else "--"
ax.plot([bs[0], ris_c[0]], [bs[1], ris_c[1]], ls_bs, color=INK, lw=1.0, zorder=3)
for k, u in enumerate(ues):
    ax.plot([bs[0], u[0]], [bs[1], u[1]], ":", color=GREY, lw=0.8, zorder=1)
    m = (bs[:2] + u[:2]) / 2
    ax.plot(*m, marker="x", ms=4, mew=0.9, color=GREY, zorder=2)
    ls = "-" if geo["los_ris_ue"][k] else "--"
    ax.plot([ris_c[0], u[0]], [ris_c[1], u[1]], ls, color=UCOL[k], lw=1.1, zorder=3)
    ax.plot(u[0], u[1], "o", ms=6.5, mfc=UCOL[k], mec="white", mew=1.0, zorder=5)
    dx, dy = 1.5 * np.cos(head[k]), 1.5 * np.sin(head[k])
    ax.annotate("", (u[0] + 2 * dx, u[1] + 2 * dy), (u[0], u[1]), zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=7))
    ax.annotate(f"U{k+1}", (u[0], u[1]), xytext=(5, -10) if dy > 0 else (5, 4),
                textcoords="offset points", fontsize=7, color=INK, zorder=6)
ax.plot(ris_c[0], ris_c[1], marker="s", ms=6, mfc=INK, mec="white", mew=0.8, zorder=6)
ax.annotate(f"RIS ($N={len(ris)}$)", (ris_c[0], ris_c[1]), xytext=(-52, 5),
            textcoords="offset points", fontsize=7)
ax.plot(bs[0], bs[1], marker="^", ms=7.5, mfc=INK, mec="white", mew=0.8, zorder=6)
ax.annotate("BS ($N_t=8$)", (bs[0], bs[1]), xytext=(-48, 2), textcoords="offset points",
            fontsize=7)
ax.text(0.7, room[1] - 0.7, f"$v={geo['velocity']:g}$ m/s, $f_c=3$ GHz\n"
        f"$T_c={geo['coherence_ms']:.1f}$ ms ({geo['velocity']*geo['coherence_ms']:.0f} mm walked)",
        fontsize=6.5, va="top", color=INK)
ax.set_xlim(-0.5, room[0] + 0.5)
ax.set_ylim(-0.8, room[1] + 1.2)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_aspect("equal")
ax.set_xlabel("$x$ (m)", labelpad=1)
ax.set_ylabel("$y$ (m)", labelpad=1)
ax.set_title("(a) Top view", fontsize=8)
ax.grid(False)
handles = [Line2D([], [], color=INK, ls="-", lw=1.1, label="LoS link"),
           Line2D([], [], color=INK, ls="--", lw=1.1, label="NLoS link"),
           Line2D([], [], color=GREY, ls=":", lw=0.9, marker="x", ms=4,
                  label="Direct link, blocked (+40 dB)"),
           Line2D([], [], color=GREY, ls="", marker="o", ms=3, label="Scatterers (20)"),
           Line2D([], [], color=INK, lw=0.9, marker=">", ms=3,
                  label="Walking direction (2 s at 1.5 m/s)")]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=5,
           fontsize=6.5, frameon=False, handlelength=2.2, columnspacing=1.2)

sx = fig.add_subplot(gs[0, 1])
sx.add_patch(Rectangle((0, 0), room[1], room[2], fill=False, lw=1.0, ec=INK))
sx.plot([0, 0], [0, room[2]], color=INK, lw=2.2)
sx.scatter(scat[:, 1], scat[:, 2], s=6, c=GREY, lw=0, zorder=2)
sx.plot([bs[1], ris_c[1]], [bs[2], ris_c[2]], ls_bs, color=INK, lw=1.0)
for k, u in enumerate(ues):
    ls = "-" if geo["los_ris_ue"][k] else "--"
    sx.plot([ris_c[1], u[1]], [ris_c[2], u[2]], ls, color=UCOL[k], lw=1.0)
    sx.plot(u[1], u[2], "o", ms=5.5, mfc=UCOL[k], mec="white", mew=0.9, zorder=5)
    off = {0: (2, -10), 1: (4, -9), 2: (-6, 5), 3: (-14, 4)}[k]
    sx.annotate(f"U{k+1}", (u[1], u[2]), xytext=off, textcoords="offset points",
                fontsize=6.5)
sx.plot(ris_c[1], ris_c[2], marker="s", ms=5.5, mfc=INK, mec="white", mew=0.8, zorder=6)
sx.plot(bs[1], bs[2], marker="^", ms=7, mfc=INK, mec="white", mew=0.8, zorder=6)
sx.annotate("RIS", (ris_c[1], ris_c[2]), xytext=(4, 3), textcoords="offset points", fontsize=6.5)
sx.annotate("BS", (bs[1], bs[2]), xytext=(4, 3), textcoords="offset points", fontsize=6.5)
sx.set_xlim(-0.4, room[1] + 0.4)
sx.set_ylim(-0.2, room[2] + 0.2)
sx.set_yticks([0, 2, 4, 6])
sx.set_xlabel("$y$ (m), distance from the RIS wall", labelpad=1)
sx.set_ylabel("$z$ (m)", labelpad=1)
sx.set_title("(b) Side view (axes not to equal scale)", fontsize=8)
sx.grid(False)

lam_cm = geo["wavelength_m"] * 100
rx = fig.add_subplot(gs[1, 1])
e = (ris - ris_c) * 100
rx.scatter(e[:, 0], e[:, 2], s=10, marker="s", c=INK, lw=0)
b = (np.array(geo["bs_array"]) - bs) * 100
rx.scatter(b[:, 0], np.full(len(b), -16.0), s=16, marker="^", c=INK, lw=0)
rx.text(21, 0, "RIS, $8\\times4$\n($x$--$z$ plane)", fontsize=6.5, va="center")
rx.text(21, -16, "BS ULA\n(along $x$)", fontsize=6.5, va="center")
rx.set_xlim(-22, 46)
rx.set_ylim(-21, 9)
rx.set_yticks([])
for side in ("left", "right", "top"):
    rx.spines[side].set_visible(False)
rx.set_xticks([-20, -10, 0, 10, 20])
rx.set_xlabel("$x$ (cm) relative to the array centre", labelpad=1)
rx.set_title(f"(c) Arrays, element spacing $\\lambda/2={lam_cm/2:.1f}$ cm", fontsize=8)
rx.grid(False)
fig.savefig(FIG / "fig_scenario.pdf", metadata={"CreationDate": None})
plt.close(fig)

(HERE / "paper_numbers.txt").write_text("\n".join(out) + "\n")
print(f"\nwrote {len(list(TAB.glob('*.tex')))} tables, figures, paper_numbers.txt")
