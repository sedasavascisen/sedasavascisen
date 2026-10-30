"""
compile_results.py
------------------
Collects every experiment's JSON output into the tables and figures used in
the write-up, and prints a single consolidated summary.

Usage:  python scripts/compile_results.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUT = "results"


def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


def section(title):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def table_head_ablation(d):
    if not d:
        return
    section("1  Where the accuracy of the published model comes from "
            "(legacy channel)")
    print(f"{'body':<10}{'head':<8}{'params':>10}{'RMSE':>10}{'SR@5':>9}")
    print("-" * 47)
    for v in d.values():
        print(f"{v['body']:<10}{v['head']:<8}{v['params']:>10,}"
              f"{v['test_rmse']:>9.2f}°{v['test_sr5']:>8.2f}%")
    dense = [v for v in d.values() if v["head"] == "dense"]
    local = [v for v in d.values() if v["head"] == "local"]
    print(f"\n  mean RMSE with the dense head : {np.mean([v['test_rmse'] for v in dense]):6.2f}°")
    print(f"  mean RMSE with the local head : {np.mean([v['test_rmse'] for v in local]):6.2f}°")
    best_local = min(local, key=lambda v: v["test_rmse"])
    print(f"  best local-head model         : {best_local['body']} "
          f"({best_local['params']:,} params, {best_local['test_rmse']:.2f}°)")
    none_local = [v for v in local if v["body"] == "none"][0]
    print(f"  element-independent control   : {none_local['test_rmse']:.2f}° "
          f"with {none_local['params']:,} params")


def table_csi(d):
    if not d:
        return
    section("2  When spatial processing earns its place")
    models = sorted({v["model"] for v in d.values()},
                    key=lambda m: ("element" not in m, m))
    sigmas = sorted({v["sigma"] for v in d.values()})
    print(f"{'channel':<11}{'sigma':>7}" + "".join(f"{m:>16}" for m in models))
    print("-" * (18 + 16 * len(models)))
    for ch in ("legacy", "geometric"):
        for s in sigmas:
            row = f"{ch:<11}{s:>7.2f}"
            for m in models:
                row += f"{d[f'{ch}|{s}|{m}']['rmse']:>15.2f}°"
            print(row)
    print("\n  gain from mixing over the element-local model "
          "(negative means mixing wins):")
    for ch in ("legacy", "geometric"):
        cells = []
        for s in sigmas:
            base = d[f"{ch}|{s}|element-local"]["rmse"]
            best = min(d[f"{ch}|{s}|{m}"]["rmse"] for m in models if m != "element-local")
            cells.append(f"sigma={s}: {100*(best-base)/base:+5.1f}%")
        print(f"    {ch:<10} " + "   ".join(cells))


def table_multiuser(d):
    if not d:
        return
    section("3  Multi-user design trained without labels")
    ref = d["PGA max-min"]["min_rate"]
    print(f"{'method':<17}{'min rate':>10}{'sum rate':>10}{'% of PGA':>10}"
          f"{'ms/sample':>11}{'params':>10}")
    print("-" * 68)
    for k, v in d.items():
        ms = f"{v['ms_per_sample']:.3f}" if "ms_per_sample" in v else "-"
        pr = f"{v.get('params', 0):,}" if v.get("params") else "-"
        print(f"{k:<17}{v['min_rate']:>10.3f}{v['sum_rate']:>10.3f}"
              f"{100*v['min_rate']/ref:>9.1f}%{ms:>11}{pr:>10}")


def table_generalisation(d):
    if not d:
        return
    section("4  What the symmetries buy")
    o = d["user_ordering"]
    print("relabelling the users (same scenarios, 8 permutations):")
    for k, v in o.items():
        print(f"  {k:<13} min-rate {v['mean']:.4f} +- {v['std']:.4f}"
              f"   spread {v['spread']:.4f}")
    print("\nuser counts never seen in training:")
    print(f"{'U':>3}{'equivariant':>14}{'PGA':>10}{'% of PGA':>10}"
          f"{'SU closed':>12}{'MU-CNN-LSTM':>14}")
    print("-" * 63)
    for U, v in sorted(d["user_count"].items(), key=lambda kv: int(kv[0])):
        mu = f"{v['mu_cnn_lstm']:.3f}" if v["mu_cnn_lstm"] else "undefined"
        print(f"{int(U):>3}{v['equivariant']:>14.3f}{v['pga']:>10.3f}"
              f"{100*v['equivariant']/v['pga']:>9.1f}%"
              f"{v['su_closed']:>12.3f}{mu:>14}")


def table_mixed(d):
    if not d:
        return
    section("5  Training across user counts")
    print(f"{'U':>3}{'trained U=4':>13}{'trained mixed':>15}{'SU closed':>12}"
          f"{'PGA':>9}{'mixed % PGA':>13}")
    print("-" * 65)
    for U, v in sorted(d.items(), key=lambda kv: int(kv[0])):
        print(f"{int(U):>3}{v['fixed']:>13.3f}{v['mixed']:>15.3f}"
              f"{v['su_closed']:>12.3f}{v['pga']:>9.3f}{100*v['mixed']/v['pga']:>12.1f}%")
    print("\n  margin over the single-user closed form:")
    for U, v in sorted(d.items(), key=lambda kv: int(kv[0])):
        print(f"    U={U}:  trained U=4 "
              f"{100*(v['fixed']-v['su_closed'])/v['su_closed']:+6.1f}%"
              f"    trained mixed "
              f"{100*(v['mixed']-v['su_closed'])/v['su_closed']:+6.1f}%")


def figures():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.3))

    ab = load("step1b_head_ablation.json")
    if ab:
        ax = axes[0]
        bodies = ["none", "CNN", "CNN-LSTM"]
        for head, mk in (("dense", "o--"), ("local", "s-")):
            ys = [next((v["test_rmse"] for v in ab.values()
                        if v["body"] == b and v["head"] == head), np.nan)
                  for b in bodies]
            ax.plot(bodies, ys, mk, label=f"{head} head", markersize=7)
        ax.set_yscale("log")
        ax.set_ylabel("test RMSE [deg]")
        ax.set_title("Head, not body, sets the accuracy")
        ax.legend(); ax.grid(alpha=.3, which="both")

    cs = load("step3_csi_transfer.json")
    if cs:
        ax = axes[1]
        sigmas = sorted({v["sigma"] for v in cs.values()})
        for ch, mk in (("legacy", "o--"), ("geometric", "s-")):
            ys = []
            for s in sigmas:
                base = cs[f"{ch}|{s}|element-local"]["rmse"]
                best = min(cs[f"{ch}|{s}|{m}"]["rmse"]
                           for m in {v["model"] for v in cs.values()}
                           if m != "element-local")
                ys.append(100 * (best - base) / base)
            ax.plot(sigmas, ys, mk, label=ch, markersize=7)
        ax.axhline(0, color="k", lw=.8)
        ax.set_xlabel(r"CSI error $\sigma$")
        ax.set_ylabel("RMSE change from spatial mixing [%]")
        ax.set_title("Mixing helps only on a correlated channel")
        ax.legend(); ax.grid(alpha=.3)

    gn = load("step5_generalisation.json")
    mx = load("step5b_mixed_users.json")
    if gn:
        ax = axes[2]
        us = sorted(int(u) for u in gn["user_count"])
        eq = [gn["user_count"][str(u)]["equivariant"] for u in us]
        pg = [gn["user_count"][str(u)]["pga"] for u in us]
        su = [gn["user_count"][str(u)]["su_closed"] for u in us]
        ax.plot(us, pg, "k^-", label="PGA (iterative)")
        ax.plot(us, eq, "s-", label="equivariant, trained U=4")
        if mx:
            ax.plot([int(u) for u in sorted(mx, key=int)],
                    [mx[u]["mixed"] for u in sorted(mx, key=int)],
                    "D-", label="equivariant, trained mixed U")
        ax.plot(us, su, "o--", label="SU closed form")
        ax.axvline(4, color="gray", ls=":", lw=1)
        ax.annotate("trained here", (4, ax.get_ylim()[1]), fontsize=8,
                    ha="center", va="top", color="gray")
        ax.set_xlabel("number of users U")
        ax.set_ylabel("min rate [b/s/Hz]")
        ax.set_title("Generalisation across user count")
        ax.legend(fontsize=8); ax.grid(alpha=.3)

    plt.tight_layout()
    p = os.path.join(OUT, "summary_figures.png")
    plt.savefig(p, dpi=150)
    print(f"\nfigure -> {p}")


if __name__ == "__main__":
    table_head_ablation(load("step1b_head_ablation.json"))
    table_csi(load("step3_csi_transfer.json"))
    table_multiuser(load("step4_multiuser.json"))
    table_generalisation(load("step5_generalisation.json"))
    table_mixed(load("step5b_mixed_users.json"))
    figures()
