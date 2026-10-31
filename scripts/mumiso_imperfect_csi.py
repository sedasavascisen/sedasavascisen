"""
mumiso_imperfect_csi.py
------------------------
Task 2: Imperfect CSI comparison (CRITICAL for thesis).

TWO ARMS (measured separately):
  (a) Clean-trained model + noisy CSI (robustness)
  (b) Noise-trained model (the real claim)

ERROR LEVELS: At least 5 points in relative error power
  [0, -20dB, -15dB, -10dB, -5dB] = [0, 0.01, 0.03, 0.1, 0.3]

CLASSICAL BASELINE: For each error level,
  - Sweep step size [0.1, 0.3, 0.5, 0.75, 1.0, 1.5]
  - Sweep step count [4, 8, 16, 32, 64]
  - Pick best on validation, report on test
  (Early stopping is a regularizer!)

TWO AXES:
  - Equal steps (which wins per step?)
  - Equal milliseconds (which wins per ms? - on idle machine!)

OUTPUT: results/mumiso_imperfect_csi.json + audit claims
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))

import json
import time
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B, csi as CSI

# Hyperparameters
N_TRAIN = 1200
N_VAL = 300
N_TEST = 300
SEED = 42
ERROR_LEVELS_DB = [None, -20, -15, -10, -5]  # None = perfect CSI
STEP_SIZES = [0.1, 0.3, 0.5, 0.75, 1.0, 1.5]
STEP_COUNTS = [4, 8, 16, 32, 64]

def generate_data():
    """Generate train/val/test splits."""
    print("=" * 70)
    print("TASK 2: IMPERFECT CSI")
    print("=" * 70)
    print(f"\nGenerating datasets ({N_TRAIN} train, {N_VAL} val, {N_TEST} test)...")

    panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=SEED)
    chan = MuMisoChannel(panel, cfg)

    # Generate all at once to preserve stream
    total = N_TRAIN + N_VAL + N_TEST
    d_all = chan.generate(total)

    # Split
    d_train = {k: v[:N_TRAIN] for k, v in d_all.items()}
    d_val = {k: v[N_TRAIN:N_TRAIN+N_VAL] for k, v in d_all.items()}
    d_test = {k: v[N_TRAIN+N_VAL:] for k, v in d_all.items()}

    print(f"   Train: {N_TRAIN} scenarios")
    print(f"   Val:   {N_VAL} scenarios")
    print(f"   Test:  {N_TEST} scenarios")

    return cfg, d_train, d_val, d_test


def sweep_classical(d, cfg, error_db, prefix="classical"):
    """
    Sweep step size and count for classical Adam optimizer.
    Returns best config + performance.
    """
    F_true, G_true, hd_true, _ = to_torch(d)
    pt, nv = 1.0, 1.0 / cfg.snr_scale()

    # Add CSI error
    e2 = CSI.db_to_e2(error_db)
    if e2 > 0:
        gen = torch.Generator().manual_seed(SEED)
        F_est, G_est, hd_est = CSI.add_error(F_true, G_true, hd_true, e2, gen)
    else:
        F_est, G_est, hd_est = F_true, G_true, hd_true

    best_val_rate = 0.0
    best_config = None

    print(f"\n   [{prefix}] Sweeping {len(STEP_SIZES)} step sizes × {len(STEP_COUNTS)} counts...")

    for step_size in STEP_SIZES:
        for step_count in STEP_COUNTS:
            # Optimize on ESTIMATED channel
            R_est, v_opt = B.pga(F_est, G_est, hd_est, pt, nv,
                                iters=step_count, step=step_size, verbose=False)

            # Extract phase from optimized result
            cos_t = torch.cos(torch.angle(v_opt))
            sin_t = torch.sin(torch.angle(v_opt))

            # Evaluate on TRUE channel with ESTIMATED phase
            R_val = CSI.rates_mismatched(F_true, G_true, hd_true,
                                        F_est, G_est, hd_est,
                                        cos_t, sin_t, pt, nv)
            val_rate = S.rate_metrics(R_val)["min_rate"]

            if val_rate > best_val_rate:
                best_val_rate = val_rate
                best_config = {
                    "step_size": step_size,
                    "step_count": step_count,
                    "val_rate": float(val_rate)
                }

    print(f"   [{prefix}] Best: lr={best_config['step_size']}, "
          f"steps={best_config['step_count']}, val={best_val_rate:.4f}")

    return best_config


def evaluate_classical(d, cfg, error_db, best_config):
    """Evaluate classical optimizer with best config on test set."""
    F_true, G_true, hd_true, _ = to_torch(d)
    pt, nv = 1.0, 1.0 / cfg.snr_scale()

    # Add CSI error
    e2 = CSI.db_to_e2(error_db)
    if e2 > 0:
        gen = torch.Generator().manual_seed(SEED + 1)  # Different seed for test
        F_est, G_est, hd_est = CSI.add_error(F_true, G_true, hd_true, e2, gen)
    else:
        F_est, G_est, hd_est = F_true, G_true, hd_true

    # Optimize on estimated channel
    t0 = time.perf_counter()
    R_est, v_opt = B.pga(F_est, G_est, hd_est, pt, nv,
                        iters=best_config["step_count"],
                        step=best_config["step_size"],
                        verbose=False)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    # Extract phase from optimized result
    cos_t = torch.cos(torch.angle(v_opt))
    sin_t = torch.sin(torch.angle(v_opt))

    # Evaluate on true channel with estimated phase
    R_test = CSI.rates_mismatched(F_true, G_true, hd_true,
                                  F_est, G_est, hd_est,
                                  cos_t, sin_t, pt, nv)
    test_rate = S.rate_metrics(R_test)["min_rate"]

    return {
        "test_rate": float(test_rate),
        "elapsed_ms": float(elapsed_ms),
        "step_size": best_config["step_size"],
        "step_count": best_config["step_count"]
    }


def run_experiment():
    """Run full experiment for Task 2."""
    cfg, d_train, d_val, d_test = generate_data()

    results = {
        "n_train": N_TRAIN,
        "n_val": N_VAL,
        "n_test": N_TEST,
        "seed": SEED,
        "error_levels_db": ERROR_LEVELS_DB,
        "arms": {}
    }

    # ARM (a): Clean-trained + noisy CSI
    print("\n" + "=" * 70)
    print("ARM (a): Clean-trained model + noisy CSI (robustness)")
    print("=" * 70)
    print("\n⚠️  TODO: Implement learned model arm!")
    print("For now, measuring classical baseline only.\n")

    # ARM (b): Noise-trained model
    print("\n" + "=" * 70)
    print("ARM (b): Noise-trained model (the real claim)")
    print("=" * 70)
    print("\n⚠️  TODO: Implement noise-trained model!")
    print("For now, measuring classical baseline only.\n")

    # Classical baseline sweep
    print("\n" + "=" * 70)
    print("CLASSICAL BASELINE (Adam)")
    print("=" * 70)

    classical_results = []

    for error_db in ERROR_LEVELS_DB:
        err_str = "Perfect CSI" if error_db is None else f"{error_db} dB"
        print(f"\n--- Error level: {err_str} ---")

        # Sweep on validation set
        best_config = sweep_classical(d_val, cfg, error_db, prefix="val")

        # Evaluate on test set
        test_result = evaluate_classical(d_test, cfg, error_db, best_config)

        classical_results.append({
            "error_db": error_db,
            "error_power": CSI.db_to_e2(error_db),
            "best_step_size": best_config["step_size"],
            "best_step_count": best_config["step_count"],
            "val_rate": best_config["val_rate"],
            "test_rate": test_result["test_rate"],
            "elapsed_ms": test_result["elapsed_ms"]
        })

        print(f"   [test] Rate: {test_result['test_rate']:.4f}, "
              f"Time: {test_result['elapsed_ms']:.2f} ms")

    results["classical"] = classical_results

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Classical Baseline")
    print("=" * 70)
    print(f"{'Error (dB)':<12}{'e2':<8}{'Steps':<8}{'StepSize':<10}{'Rate':<10}{'Time (ms)':<10}")
    print("-" * 70)

    for r in classical_results:
        err_str = "Perfect" if r["error_db"] is None else f"{r['error_db']}"
        print(f"{err_str:<12}{r['error_power']:<8.3f}{r['best_step_count']:<8}"
              f"{r['best_step_size']:<10.2f}{r['test_rate']:<10.4f}"
              f"{r['elapsed_ms']:<10.2f}")

    # Save results
    out_path = _pl.Path(__file__).resolve().parents[1] / "results" / "mumiso_imperfect_csi.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved: {out_path.name}")
    print("\n" + "=" * 70)
    print("⚠️  NEXT STEPS:")
    print("1. Implement learned model (clean-trained)")
    print("2. Implement noise-trained model")
    print("3. Add audit claims to audit_claims.py")
    print("4. Measure latency on IDLE machine!")
    print("=" * 70)

    return results


if __name__ == "__main__":
    # Check machine load
    with open("/proc/loadavg") as f:
        load = float(f.read().split()[0])

    if load > 0.5:
        print(f"⚠️  WARNING: Machine load is {load:.2f} (should be < 0.5)")
        print("Latency measurements will be UNRELIABLE!")
        print("Please wait for machine to be idle.\n")

    run_experiment()
