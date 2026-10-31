# KEY NUMBERS FOR MOBILITY PAPER
# ================================
# All numbers sourced from TEZ_YAZIM_REFERANSI.md
# Scripts: scripts/mumiso_beam_staleness.py, mumiso_aging*.py, mumiso_latency*.py

## MAIN CLAIM 1: Fresh Beam Value
**Fresh beam is 11.7-14.2× more valuable than stale optimized phase**

At coherence time Tc = 28.2 ms (3 GHz, 1.5 m/s):
- Phase chosen at t=0, beamforming either fresh or stale

| Phase Selection | Fresh Beam | Stale Beam | Ratio |
|-----------------|-----------|------------|-------|
| su_average      | 3.5862    | 0.3060     | **11.7×** |
| su_best_of      | 3.9243    | 0.3052     | **12.9×** |
| adam8           | 4.3584    | 0.3066     | **14.2×** |

Source: `scripts/mumiso_beam_staleness.py`
Results: `results/mumiso_beam_staleness*.json`

**IMPORTANT**: Previous claim was "17×" but this was NOT reproducible (no script existed).
Corrected measurement: 11.7-14.2×

Stale value is ~0.305 for all three phase selections.
Fresh value ranges: 3.59-4.36


## MAIN CLAIM 2: Intrinsic Optimum
**L=4 steps is optimal; convergence (L=48) costs 14% rate**

Intrinsic optimum: **L = 4 → 5.982 bps/Hz**
Convergence: L = 48 → 5.064 bps/Hz (14% loss)

Stale phase baseline: ~4.35 bps/Hz (doesn't collapse to zero)


## MAIN CLAIM 3: Method Ranking Under Equal Latency
**Equal iterations: learned wins. Equal milliseconds: learned loses (5/5 dominated)**

Manually verified main rows (from Section 5b draft):

| Method          | t=0 Rate | Latency  | Effective Rate |
|-----------------|----------|----------|----------------|
| su_average      | 4.624    | ~0 ms    | 4.624          |
| su_best_of      | 5.276    | 0.05 ms  | 5.276          |
| **Adam-8**      | —        | 13.3 ms  | **5.849**      |
| Adam-16         | —        | 26.6 ms  | 5.324          |
| Coord descent   | —        | ~1500 ms | 4.921          |
| **PGA**         | **7.117**| ~5600 ms | **4.667**      |

PGA has highest t=0 rate (7.117) but becomes 4.667 after aging (5600 ms delay).
Adam-8 is OPTIMAL: 5.849 effective rate at 13.3 ms.

Source: Section 5b draft, manually verified


## MOBILITY PARAMETERS

Coherence time: **Tc = 28.2 ms**
- Carrier frequency: fc = 3 GHz
- Velocity: v = 1.5 m/s (walking)
- Doppler: fd = 15.0 Hz
- Calculation: Tc = 1/(2*fd) = 28.2 ms

Channel correlation: ρ(τ) = J0(2π fd τ)
- Measured correlation floor: ~0.5 (vs ~0.10 for independent draws)
- Scatterer count 6→60: floor only drops 0.60→0.51
- **Reliable validity horizon: τ ≤ 200 ms**

Source: `results/mumiso_aging_fixzf.json`, `mumiso_aging_sweep_fixzf.json`


## EQUAL STEPS vs EQUAL MILLISECONDS

**Equal STEPS** — learned rule wins at all budgets:

| L  | Learned | Tuned Adam | Ratio | Paired Diff - 2 SE | Win Rate |
|----|---------|------------|-------|-------------------|----------|
| 1  | 4.4599  | 4.3810     | 1.018 | +0.0608           | 74.8%    |
| 2  | 4.8792  | 4.6927     | 1.040 | +0.1602           | 83.2%    |
| 4  | 5.2855  | 5.0253     | 1.052 | +0.2279           | 83.7%    |
| 8  | 5.5932  | 5.3800     | 1.040 | +0.1840           | 83.2%    |
| 16 | 5.8003  | 5.7389     | 1.011 | +0.0393           | 68.3%    |

Step size tuned on validation at each budget; optimum is 0.75 at all L.
Source: `results/mumiso_equal_step.json`

**Equal MILLISECONDS** — all 5 points dominated, 5/5 trials:

| Learned L | Latency | Rate   | Dominating Adam   |
|-----------|---------|--------|-------------------|
| 1         | 6.71 ms | 4.4599 | L=2: 4.48 ms, 4.6927 |
| 2         | 14.59 ms| 4.8792 | L=4: 9.30 ms, 5.0253 |
| 4         | 25.79 ms| 5.2855 | L=8: 17.48 ms, 5.3800|
| 8         | 52.34 ms| 5.5932 | L=16: 36.62 ms, 5.7389|
| 16        | 99.15 ms| 5.8003 | L=32: 76.57 ms, 6.0132|

Step cost ratio: ~2.7× (one learned step ≈ 2.7 Adam steps)
Timing jitter across trials: 1.06×-1.41× (idle machine, 5 trials)

Source: `results/mumiso_latency_parity.json`, `mumiso_latency_repeat.json`


## MEASUREMENT TRAPS

**Machine load affects latency measurements NON-NEUTRALLY**
- Example: Training running → Adam 17.5 ms → 29.7 ms
- Conclusion flipped: "learned on frontier" → actually all 5 dominated
- Rule: `cat /proc/loadavg` → first number < 0.5 required

**Timing jitter**
- 5 trials, idle machine: 1.06×-1.41× variation
- Report: ALL trials, not cherry-picked runs

**Reproducibility**
- EVERY number must have executable script in scripts/
- This project violated this rule twice → both numbers wrong:
  * "Budget compliance 95%" → actual 85-90%
  * "Fresh/stale 17×" → actual 11.7-14.2×


## SYSTEM CONFIGURATION

- Users: K = 4 (single antenna)
- BS antennas: T = 8 (ULA, λ/2 spacing)
- RIS elements: N = 64 (8×8 panel)
- Room: 40m × 20m × 6m (InH-Office)
- Channel: 3GPP TR 38.901 geometry-based
- Scenarios: 1200 train, 300 val, 300 test
- Seed: 42 (deterministic, reproducible)


## AUDIT STATUS

Current: 41/41 passing
Target: 56/56 (after Task 2 & 3)

All claims include sabotage test: 
- Opened model weights written to untrained model
- 7/41 claims fail → confirms measurement integrity


## REFERENCES TO SCRIPTS

- Fresh beam value: `scripts/mumiso_beam_staleness.py`
- Aging analysis: `scripts/mumiso_aging.py`, `mumiso_aging_sweep.py`
- Latency parity: `scripts/mumiso_latency_parity.py`
- Latency repeat: `scripts/mumiso_latency_repeat.py`
- Equal steps: `scripts/mumiso_equal_step.py`
- Audit claims: `scripts/audit_claims.py`
