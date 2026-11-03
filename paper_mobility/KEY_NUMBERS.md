# Key numbers — mobility paper

Do not type numbers here. Every table, figure and in-text number of the
paper comes from `results/*.json` through

    python3 paper_mobility/make_paper_assets.py

which writes `tables/*.tex`, `figures/*.pdf` and `paper_numbers.txt`.
Read `paper_numbers.txt` for the current values.

Sources:

| Result | Script | Result file |
|---|---|---|
| Scenario figure (geometry of aging-set scenario 0) | `scripts/mumiso_scenario_geometry.py` | `results/mumiso_scenario_geometry.json` |
| Effective rates, aging curves | `scripts/mumiso_aging.py --no-learned --tag aging_fixzf` | `results/mumiso_aging_fixzf.json` |
| Intrinsic optimum (Adam step sweep; the paper plots the finer grid of the sensitivity run, which reproduces this file) | `scripts/mumiso_aging_sweep.py` | `results/mumiso_aging_sweep_repro.json` |
| Sensitivity: speed, acquisition delay, speed mismatch | `scripts/mumiso_aging_sensitivity.py` | `results/mumiso_aging_sensitivity.json` |
| Precoder cost vs. one Adam step | `scripts/mumiso_precoder_vs_step.py` | `results/mumiso_precoder_vs_step.json` |
| Latencies on the aging set (SU, CD, long-run Adam; Adam per-step check) | `scripts/mumiso_mobility_latency.py` | `results/mumiso_mobility_latency.json` |
| Step-size robustness of the optimum | `scripts/mumiso_aging_sensitivity.py --velocities 1.5 --overheads 0 --lr X --tag aging_lrX` | `results/mumiso_aging_lr{0.25,0.75,1.0}.json` |
| Equal steps | `scripts/mumiso_equal_step.py` | `results/mumiso_equal_step.json` |
| Equal milliseconds (rates) | `scripts/mumiso_latency_parity.py` | `results/mumiso_latency_parity.json` |
| Equal milliseconds (timings, 5 rounds) | `scripts/mumiso_latency_repeat.py` | `results/mumiso_latency_repeat.json` |
| Fresh vs stale precoder | `scripts/mumiso_beam_staleness.py --phase …` | `results/mumiso_beam_staleness*.json` |

Note: the timings stored in `mumiso_latency_parity.json` include a
load-contaminated Adam L=8 (29.7 ms). The paper therefore takes latencies
from `mumiso_latency_repeat.json` (median of five idle rounds) and only the
rates from `mumiso_latency_parity.json`.

Not yet run (needs the weights archive): `scripts/mumiso_latency_replicate.py`
re-times the equal-millisecond comparison and records load and CPU model.
