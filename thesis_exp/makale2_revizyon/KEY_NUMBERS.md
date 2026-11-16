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
| Published CNN-LSTM, training and static test (Sec. VI-G); dataset from `scripts/sumiso_dataset.py` | `scripts/sumiso_train.py` (variants: `--head seq`, `--features raw`, `--data sumiso_siso --label published`) | `results/sumiso_cnnlstm*.json` |
| Published CNN-LSTM under mobility, Table VII | `scripts/sumiso_mobility_eval.py --ckpt sumiso_cnnlstm_seq` | `results/sumiso_mobility_eval.json` |
| Step-size robustness of the optimum | `scripts/mumiso_aging_sensitivity.py --velocities 1.5 --overheads 0 --lr X --tag aging_lrX` | `results/mumiso_aging_lr{0.25,0.75,1.0}.json` |
| Aging table with CIs, no-RIS, random phase, link budget | `scripts/mumiso_aging_stats.py` | `results/mumiso_aging_stats.json` |
| Step-cost scaling, Armijo baseline, paired bootstrap | `scripts/mumiso_step_scaling.py` | `results/mumiso_step_scaling.json` |
| Periodic re-optimization (cold/warm) — REVISED | `thesis_exp/p4/takip_duzeltme/run.py --fix 1` (corrected copy of `scripts/mumiso_tracking.py`); table: `thesis_exp/makale2_revizyon/make_tab_tracking_corrected.py` | `thesis_exp/p4/takip_duzeltme/raw/fix1_tp*.json` |
| Small-delay model of L*(x) (Proposition 1); N=64 second scenario | `scripts/mumiso_optimum_model.py` | `results/mumiso_optimum_model.json` |
| Model robustness: fit-range sensitivity, growing kappa, slope CI, balance ratio, Fraunhofer check | `scripts/mumiso_optimum_model_checks.py` | `results/mumiso_optimum_model_checks.json` |
| Equal steps | `scripts/mumiso_equal_step.py` | `results/mumiso_equal_step.json` |
| Equal milliseconds (rates) | `scripts/mumiso_latency_parity.py` | `results/mumiso_latency_parity.json` |
| Equal milliseconds (timings, 5 rounds) | `scripts/mumiso_latency_repeat.py` | `results/mumiso_latency_repeat.json` |
| Fresh vs stale precoder | `scripts/mumiso_beam_staleness.py --phase …` | `results/mumiso_beam_staleness*.json` |

Note: the timings stored in `mumiso_latency_parity.json` include a
load-contaminated Adam L=8 (29.7 ms). The paper therefore takes latencies
from `mumiso_latency_repeat.json` (median of five rounds; that script does not record the load) and only the
rates from `mumiso_latency_parity.json`.

Not yet run (needs the weights archive): `scripts/mumiso_latency_replicate.py`
re-times the equal-millisecond comparison and records load and CPU model.
| Standardized user speeds (3, 5.4, 10, 18, 30 km/h), Table speeds | `scripts/mumiso_standard_speeds.py` | `results/mumiso_standard_speeds.json` |
| Coordinate descent with 1-8 sweeps (VI-A) | `scripts/mumiso_cd_budget.py` | `results/mumiso_cd_budget.json` |
| Shared scattering gains (VI-D) | `scripts/mumiso_standard_speeds.py --share_gains --kmh 5.4,10 --tag standard_speeds_shared` | `results/mumiso_standard_speeds_shared.json` |


## Revision 16 Nov 2026 — sources of the new numbers

| Where | Numbers | Script | Raw output |
| --- | --- | --- | --- |
| §V, exact-latency note | ≤ 0.006 (Table I within horizon), 0.008 / 0.037 (CD / long-run Adam), ≤ 0.027 (Adam sweep), 14.0 → 14.2% | `thesis_exp/p4/izgara_kontrol/run_tab1.py`, `run.py` | `raw/results_tab1.json`, `raw/results.json` |
| §V, re-measured latency | 1.33 ms; L* = 6; 14.9%; 0.26 (0.15–0.37) | `thesis_exp/infra/scripts/mumiso_mobility_latency.py` (branch thesis/altyapi); `izgara_kontrol/run.py` (rerun set) | `thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json`; `izgara_kontrol/raw/results.json` |
| §VI-H, precoder pilots | 5.21; 3.54 / 4.00 / 4.33; T_r = 1–2 ms; Adam 3–20 tied; W = 25/50/100 → 5 / 6–8 / 16–20 (16–24 free); 0.02–0.04 | `thesis_exp/p4/onkodlayici_siralama/run.py` (WIN = 25, 50, 100) | `raw/results.json`, `raw/results_win25.json`, `raw/results_win100.json` |
| §VI-H, imperfect CSI | 6.08 → 3.54; ≤ 10 dB tied; 22.6 dB median | `thesis_exp/p4/kusurlu_csi/run.py`; `thesis_exp/denetim_log/scripts/u13_csi_rel_err.py` | `kusurlu_csi/raw/results.json`; `u13_csi_rel_err.out` |
| §VI-H, CSI + pilots | 0.05–0.06 at 30 dB; tied at 20 dB; CD, long-run Adam behind | `thesis_exp/p4/onkodlayici_csi/run.py` | `raw/results.json` |
| §VI-H, discrete phases | L* = 5/6/6; 9.5/14.1/14.9%; 16–501 ms; 1 bit: +0.25 (0.16–0.33), −0.04 (−0.11, 0.02) | `thesis_exp/p4/ayrik_faz/run.py` (timing), `run_exact.py`, `run_3bit.py` | `raw/results.json`, `raw/results_exact.json`, `raw/results_3bit.json` |
