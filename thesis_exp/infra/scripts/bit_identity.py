"""
Infra task 1: are the published aging results bit-for-bit reproducible with the current code?
Compares the redirected re-runs in thesis_exp/infra/raw/ with the committed files in results/
(exact equality of every number; the JSON trees are walked recursively).
Output: thesis_exp/infra/raw/bit_identity.json
"""
import json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
# results/ file -> (re-run file in thesis_exp/infra/raw, top-level keys skipped)
# The paper reads mumiso_aging_sweep_repro.json (make_paper_assets.py line 131); the older
# mumiso_aging_sweep_fixzf.json has no generating script (see the sweep script's docstring) and is compared for information.
pairs = {"mumiso_aging_fixzf.json": ("mumiso_aging_fixzf.json", ["config"]),
         "mumiso_aging_sweep_repro.json": ("mumiso_aging_sweep_fixzf.json", []),
         "mumiso_aging_sweep_fixzf.json": ("mumiso_aging_sweep_fixzf.json", [])}
def walk(a, b, path, diffs, skip):
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k in skip and path == "": continue
            if k not in a or k not in b: diffs.append(f"{path}/{k}: missing"); continue
            walk(a[k], b[k], f"{path}/{k}", diffs, skip)
    elif isinstance(a, list):
        if len(a) != len(b): diffs.append(f"{path}: len {len(a)} vs {len(b)}"); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f"{path}[{i}]", diffs, skip)
    elif a != b:
        diffs.append(f"{path}: {a!r} vs {b!r}")
res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(), files={})
for f, (g, skip) in pairs.items():
    a = json.load(open(ROOT / "results" / f)); b = json.load(open(ROOT / "thesis_exp/infra/raw" / g))
    d = []; walk(a, b, "", d, set(skip))
    res["files"][f] = dict(rerun=g, identical=not d, n_differences=len(d), first_differences=d[:10], skipped_keys=skip)
json.dump(res, open(ROOT / "thesis_exp/infra/raw/bit_identity.json", "w"), indent=1)
print(json.dumps(res, indent=1))
