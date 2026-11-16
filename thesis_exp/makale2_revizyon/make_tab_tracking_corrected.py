"""
Writes tables/tab_tracking.tex of the REVISED paper copy from the corrected periodic-operation simulation
(thesis_exp/p4/takip_duzeltme/raw/fix1_tp*.json: fractional pilot charging, exact deployment instants;
verification K4). Formatting is the same code as paper_mobility/make_paper_assets.py ("tracking" block),
so only the data source differs. Also prints the near-best check behind the paper's sentence
"in every row some policy with at most 8 steps is not significantly below the best".
"""
import json, pathlib
H = pathlib.Path(__file__).parent
RAW = H.parent / "p4" / "takip_duzeltme" / "raw"
fmtU = lambda U: "b2b" if U is None else f"{U:g}"
lines = [r"\begin{tabular}{r|rrr|rrr|r}", r"\toprule",
         r" & \multicolumn{3}{c|}{Cold start} & \multicolumn{3}{c|}{Warm start} & \\",
         r"$T_{\mathrm{p}}$ (ms) & $U$ & $L$ & rate & $U$ & $L$ & rate & warm$-$cold \\", r"\midrule"]
for tp in ("0", "0.86", "1.71", "3.43"):
    trk = json.load(open(RAW / f"fix1_tp{tp}.json"))
    key = list(trk["runs"])[0]
    c, w = trk["runs"][key]["cold"], trk["runs"][key]["warm"]
    wc = trk["warm_minus_cold"][key]
    cell = lambda b: f"{fmtU(b['period'])} & {b['L']} & {b['rate']:.2f}"
    lines.append(f"{float(tp):g} & {cell(c['best'])} & {cell(w['best'])} & "
                 f"{wc['diff']:+.2f}" + (r"$^\S$" if wc['ci'][0] <= 0 <= wc['ci'][1] else "") + r" \\")
    for mode in ("cold", "warm"):
        r = trk["runs"][key][mode]
        small = [x for x in r["near_best"] if x["L"] <= 8]
        print(f"T_p={tp} {mode}: best U={r['best']['period']} L={r['best']['L']} {r['best']['rate']:.3f}; "
              f"near-best L={sorted(x['L'] for x in r['near_best'])}; any L<=8 near best: {bool(small)}")
    print(f"T_p={tp} warm-cold {wc['diff']:.4f} [{wc['ci'][0]:.4f}, {wc['ci'][1]:.4f}]")
lines += [r"\bottomrule", r"\end{tabular}"]
(H / "tables" / "tab_tracking.tex").write_text("\n".join(lines) + "\n")
print("wrote tables/tab_tracking.tex")
