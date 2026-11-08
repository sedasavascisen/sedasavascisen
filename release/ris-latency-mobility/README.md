# Latency Can Reverse the Ranking — code and results

Code and stored measurement results for

> S. Savaşçı Şen, A. Çalhan, M. Cicioğlu, "Latency Can Reverse the Ranking:
> Effective-Rate Evaluation of RIS Phase Optimization for Mobile Users,"
> submitted to *IEEE Transactions on Wireless Communications*, 2026.

RIS phase optimizers are evaluated on the channel that exists when they
finish (the *effective rate*), with measured latencies, in a 3GPP TR 38.901
indoor-office multi-user MISO downlink with walking users.

## Layout

| Path | Contents |
|---|---|
| `ris_mu/` | Simulation package: 3GPP indoor-office channel with mobility (`mumiso/`), single-user extension and the ported phase-aware CNN–LSTM (`sumiso/`) |
| `scripts/` | One script per experiment; each writes a JSON file to `results/` |
| `results/` | The stored measurement results behind every table and figure |
| `paper/make_paper_assets.py` | Builds every table (`paper/tables/`) and figure (`paper/figures/`) of the paper from `results/` |

## Quick start

```bash
pip install -r requirements.txt
python3 paper/make_paper_assets.py      # regenerates all tables and figures from results/
```

This reproduces the paper's tables exactly from the stored results.

## Which script produces which result

| Paper item | Script | Result file |
|---|---|---|
| Scenario figure | `scripts/mumiso_scenario_geometry.py` | `mumiso_scenario_geometry.json` |
| Effective rates, aging curves (Table I, Fig. 2) | `scripts/mumiso_aging.py --no-learned --tag aging_fixzf` | `mumiso_aging_fixzf.json` |
| Step sweep (Fig. 3) | `scripts/mumiso_aging_sweep.py`, `scripts/mumiso_aging_sensitivity.py` | `mumiso_aging_sweep_repro.json`, `mumiso_aging_sensitivity.json`, `mumiso_aging_lr*.json` |
| Paired statistics | `scripts/mumiso_aging_stats.py` | `mumiso_aging_stats.json` |
| Step-cost scaling and small-delay model (Fig. 4) | `scripts/mumiso_step_scaling.py`, `scripts/mumiso_optimum_model.py`, `scripts/mumiso_optimum_model_checks.py` | `mumiso_step_scaling.json`, `mumiso_optimum_model*.json` |
| Standardized user speeds (Table II) | `scripts/mumiso_standard_speeds.py` | `mumiso_standard_speeds.json` |
| Periodic re-optimization (Table III) | `scripts/mumiso_tracking.py` | `mumiso_tracking.json` |
| Learned update rule vs. Adam (Fig. 5) | `scripts/mumiso_equal_step.py`, `scripts/mumiso_latency_parity.py`, `scripts/mumiso_latency_repeat.py` | `mumiso_equal_step.json`, `mumiso_latency_*.json` |
| Ported CNN–LSTM (Table IV) | `scripts/sumiso_dataset.py`, `scripts/sumiso_train.py`, `scripts/sumiso_mobility_eval.py`, `scripts/sumiso_t0_robustness.py`, `scripts/sumiso_label_check.py` | `sumiso_*.json`, `sumiso_cnnlstm_seq.pt` |
| Fresh vs. stale precoder | `scripts/mumiso_beam_staleness.py`, `scripts/mumiso_precoder_vs_step.py` | `mumiso_beam_staleness*.json`, `mumiso_precoder_vs_step.json` |
| Latencies | `scripts/mumiso_mobility_latency.py` | `mumiso_mobility_latency.json` |

## Notes on re-running

- **Latency measurements** (`mumiso_mobility_latency`, `mumiso_latency_*`,
  `sumiso_mobility_eval`, `mumiso_standard_speeds` uses stored latencies) must
  run on an idle machine with one thread; check `cat /proc/loadavg` first.
  Contention is not neutral: it slows the arms by different amounts.
- **Scenario draws are not prefix-stable**: `generate(1000)` is not
  `generate(2000)[:1000]`. Evaluate a trained model with the sample count it
  was trained with.
- **Learned update rule**: the networks are trained with
  `scripts/mumiso_unrolled.py`; their weights (`results/mumiso_eqstep_L*.pt`)
  are not included and are available from the authors on request. The stored
  results in `results/` are the ones reported.
- **CNN–LSTM dataset**: `scripts/sumiso_dataset.py` regenerates
  `data_sumiso/` (about 1.5 minutes); it is not included.
- Latencies were measured on an Intel Xeon CPU at 2.1 GHz with one PyTorch
  thread (unoptimized Python); see Section V of the paper.

## Citation

Please cite the paper above if you use this code. The phase-aware CNN–LSTM is
from S. Savaşçı Şen *et al.*, *Advanced Intelligent Systems*, 2026,
doi:10.1002/aisy.70460.

## License

MIT (see `LICENSE`).
