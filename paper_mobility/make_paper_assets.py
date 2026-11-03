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

eff = age["effective"]
rows = ["su_average", "su_best_of", "adam8", "adam12", "adam16", "adam20",
        "cd", "pga"]
names = {"su_average": "SU-average", "su_best_of": "SU-best-of",
         "adam8": "Adam, $L=8$", "adam12": "Adam, $L=12$",
         "adam16": "Adam, $L=16$", "adam20": "Adam, $L=20$",
         "cd": "Coord. descent", "pga": "PGA"}
lines = [r"\begin{tabular}{lrrrr}", r"\toprule",
         r"Method & $t{=}0$ & Latency & Effective & Stale \\",
         r" & (b/s/Hz) & (ms) & (b/s/Hz) & (b/s/Hz) \\", r"\midrule"]
for k in rows:
    e = eff[k]
    lat = f"{e['latency_ms']:.2f}" if e["latency_ms"] < 1 else f"{e['latency_ms']:.1f}"
    mark = "" if e["trusted"] else r"$^\dagger$"
    lines.append(f"{names[k]} & {e['t0']:.3f} & {lat} & {e['effective']:.3f}{mark} "
                 f"& {e['stale']:.3f} \\\\")
    say(f"aging  {k:11s} t0 {e['t0']:.3f}  lat {e['latency_ms']:7.2f}  "
        f"eff {e['effective']:.3f}  stale {e['stale']:.3f}  trusted {e['trusted']}")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "tab_aging.tex").write_text("\n".join(lines) + "\n")

fig, ax = plt.subplots(figsize=(COL_W, 2.3))
for k in ("pga", "adam8", "su_best_of", "su_average"):
    ax.plot(times, age["curve"][k], marker="o", ms=2.5, color=C[k],
            label={"pga": "Projected gradient ascent"}.get(k, names[k].replace("$", "")))
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
fig.savefig(FIG / "fig_aging.pdf")
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
ax.plot(L, ef, "o-", color=C["adam"], label="Effective rate")
ax.plot(L[ib], ef[ib], "*", color=C["learned"], ms=11, zorder=5)
ax.annotate(f"best: $L={L[ib]}$, {ef[ib]:.3f}", (L[ib], ef[ib]),
            xytext=(6.5, 4.85), fontsize=7,
            arrowprops=dict(arrowstyle="-", lw=0.6))
ax.annotate(f"$L={L[-1]}$: {ef[-1]:.3f}\n({-loss48:.1%} vs. best)", (L[-1], ef[-1]),
            xytext=(L[-1] - 20, ef[-1] - 0.38), fontsize=7,
            arrowprops=dict(arrowstyle="-", lw=0.6))
ax.set_xlabel(r"Adam steps $L$ (latency $= 1.66\,L$ ms)")
ax.set_ylabel("Min-user rate (b/s/Hz)")
ax.set_ylim(4.6, 7.3)
ax.legend(loc="center", bbox_to_anchor=(0.68, 0.47))
fig.savefig(FIG / "fig_intrinsic_optimum.pdf")
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
        cells.append(f"{e['best_L']}{flag} ({e['best_eff']:.2f})")
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
a2.set_xlabel("Measured latency (ms, median of 5 idle rounds)")
a2.set_title("(b) Equal milliseconds", fontsize=8)
a2.legend(loc="lower right")
fig.tight_layout()
fig.savefig(FIG / "fig_equal_step_vs_ms.pdf")
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
fig.savefig(FIG / "fig_beam_staleness.pdf")
plt.close(fig)

(HERE / "paper_numbers.txt").write_text("\n".join(out) + "\n")
print(f"\nwrote {len(list(TAB.glob('*.tex')))} tables, figures, paper_numbers.txt")
