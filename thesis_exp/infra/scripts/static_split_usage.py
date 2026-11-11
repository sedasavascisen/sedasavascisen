"""
Infra task 3: which of the 6000 static-set scenarios (samples=6000, split_indices(seed=0)) each
paper-relevant script actually touches. Evidence is the code lines quoted in `uses`.
Output: thesis_exp/infra/raw/static_split_usage.json
"""
import sys, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from ris_mu.features import split_indices
tr, va, te = split_indices(6000, seed=0)
uses = {
 "mumiso_unrolled.py (learned rule, --samples 6000 for eqstep_L*)": {
   "train": ("tr (all)", "train loop over tr"), "val": ("va[:500]", "lines 104/128: run_eval(va[:500]); best epoch kept (lines 131-133)"),
   "test": ("te[:300]", "line 68: bte = te[:a.baseline_n], baseline_n=300 in eqstep configs")},
 "mumiso_equal_step.py (paper Fig. 5, static set)": {
   "val": ("va[:400]", "line 108: vv = va[:a.val_n] (lr choice)"), "test": ("te[:600]", "line 107: ev = te[:a.eval_n]; line 229: te[:300]")},
 "mumiso_latency_parity.py": {"val": ("va[:400]", "line 113"), "test": ("te[:600]", "line 113")},
}
used_val = set(va[:500].tolist()); used_test = set(te[:600].tolist())
res = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           split=dict(train=len(tr), val=len(va), test=len(te)), paper_text="4200 training, 400 validation, 600 testing",
           uses=uses,
           val_used_by_any=len(used_val), val_never_used=len(va) - len(used_val),
           test_used_by_any=len(used_test), test_never_used=len(te) - len(used_test),
           never_used_total=(len(va) - len(used_val)) + (len(te) - len(used_test)),
           note="val[400:500] is used only by the learned rule's checkpoint selection; the paper's '400 for validation' "
                "describes the classical lr choice only.")
out = ROOT / "thesis_exp/infra/raw/static_split_usage.json"
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "uses"}, indent=1))
