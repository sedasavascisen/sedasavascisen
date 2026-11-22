"""
Paper 2, static set (Fig. eqms): which of the 6000 scenarios each arm actually uses, read from the code that produced the figure.
  split      ris_mu.features.split_indices(6000, frac=(0.7, 0.15, 0.15), seed=0)        -> tr, va, te
  learned    scripts/mumiso_unrolled.py : trains on tr, keeps the best epoch on va[:500]   (line 'run_eval(va[:500])')
  Adam       scripts/mumiso_equal_step.py, mumiso_latency_parity.py : (lr, objective) chosen on va[:val_n], val_n = 400
  reported   same scripts : ev = te[:eval_n], eval_n = 600 ; results/mumiso_*equal_step*.json config confirms samples/eval_n/val_n
Checks sizes, disjointness, the 400 subset of the 500, and what is never used. -> veri_bolme.json
"""
import sys, json, pathlib, re, subprocess
R = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(R))
from ris_mu.features import split_indices
tr, va, te = split_indices(6000, seed=0)
src = lambda f: (R / "scripts" / f).read_text()
uses = dict(learned_val=int(re.search(r"run_eval\(va\[:(\d+)\]\)", src("mumiso_unrolled.py")).group(1)),
            adam_val=int(re.search(r'"--val-n", type=int, default=(\d+)', src("mumiso_equal_step.py")).group(1)),
            test=int(re.search(r'"--eval-n", type=int, default=(\d+)', src("mumiso_equal_step.py")).group(1)))
cfg = {f: {k: json.load(open(R / "results" / f))["config"][k] for k in ("samples", "eval_n", "val_n")}
       for f in ("mumiso_equal_step.json", "mumiso_latency_parity.json")}
trained = {L: json.load(open(R / f"results/mumiso_eqstep_L{L}.json"))["config"]["samples"] for L in (1, 2, 4, 8, 16)}
s = lambda x: set(x.tolist())
out = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=R).stdout.strip(),
           sizes=dict(train=len(tr), val=len(va), test=len(te)), uses=uses, result_configs=cfg, checkpoint_samples=trained,
           disjoint=not (s(tr) & s(va) or s(tr) & s(te) or s(va) & s(te)),
           adam_val_subset_of_learned_val=s(va[:uses["adam_val"]]) <= s(va[:uses["learned_val"]]),
           unused=dict(val=len(va) - uses["learned_val"], test=len(te) - uses["test"]))
out["unused"]["total"] = out["unused"]["val"] + out["unused"]["test"]
json.dump(out, open(pathlib.Path(__file__).with_name("veri_bolme.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
