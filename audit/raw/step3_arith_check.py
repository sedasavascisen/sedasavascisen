#!/usr/bin/env python3
"""Arithmetic checks on numbers PUBLISHED in aisy.70460 (no data, no training).

Purpose: give every derived number in step3_sources.json / step0_step3_notes.md
a runnable source (CLAUDE.md "betiksiz sayi, olcum degildir").
Nothing here is a measurement of the model; it only (a) recomputes ratios the
paper states from the paper's own inputs and (b) counts learnable parameters of
the architectures written in the code files, analytically.

Run:  python3 audit/raw/step3_arith_check.py   -> writes step3_arith_check.json
"""
import json
import math
import os

out = {}

# ---- ratios quoted in the paper, recomputed from the paper's own inputs ----
out["table1_improvement_pct"] = 100 * (3.95 - 2.77) / 3.95            # paper: 29.9
out["cnn_vs_cd_pct"] = 100 * (3.50 - 2.77) / 3.50                       # paper: 21
out["cnn_vs_lstm_only_pct"] = 100 * (3.42 - 2.77) / 3.42                # paper: 19.0
out["cd_k50_vs_cnn_pct_over_cnn"] = 100 * (3.20 - 2.77) / 2.77          # paper: 15.4 ("15.4% worse")
out["cd_k50_vs_cnn_pct_over_cd"] = 100 * (3.20 - 2.77) / 3.20
out["fig9_normalized_rmse"] = 2.77 / 5.0                                # paper: 0.554
out["pso_speed_ratio"] = 15.0 / 0.08                                    # paper: 187x
out["eff_cnn"] = 1 / (2.77 * 0.08)                                      # paper: 4.51
out["eff_cd"] = 1 / (3.50 * 0.15)                                       # paper: 1.90
out["csi10_rel_increase_pct"] = 100 * (4.2 - 2.77) / 2.77               # paper: 52
# "15% superiority over PSO" at 10% CSI: only PSO number in the paper is the
# PERFECT-CSI 4.50 deg (Table 6). Margin vs that number:
out["csi10_margin_vs_pso_perfect_csi_pct"] = 100 * (4.50 - 4.2) / 4.50
out["quant_2bit_minus_cont_deg"] = 3.08 - 2.77                          # paper: 0.31 deg
# RMSE floor of uniform b-bit phase quantisation vs a continuous label:
# step = 360/2^b deg, error ~ U(-step/2, step/2) -> RMSE = step/sqrt(12)
out["quant_floor_rmse_deg"] = {b: (360 / 2 ** b) / math.sqrt(12) for b in (1, 2, 3)}

# power-law fit of Table 8 / Eq. 19 on the three "experimental" points
xs = [math.log(n / 32) for n in (32, 64, 128)]
ys = [math.log(r) for r in (2.77, 3.21, 3.89)]
mx, my = sum(xs) / 3, sum(ys) / 3
b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
a = my - b * mx
c0 = math.exp(a)
pred = [c0 * math.exp(b * x) for x in xs]
R = [2.77, 3.21, 3.89]
mR = sum(R) / 3
r2_lin = 1 - sum((r - p) ** 2 for r, p in zip(R, pred)) / sum((r - mR) ** 2 for r in R)
yh = [a + b * x for x in xs]
r2_log = 1 - sum((y - h) ** 2 for y, h in zip(ys, yh)) / sum((y - my) ** 2 for y in ys)
out["powerlaw_fit"] = {
    "alpha": b, "c0": c0, "R2_linear": r2_lin, "R2_log": r2_log,
    "pred_N256_fitted_c0": c0 * 8 ** b,
    "pred_N256_paper_formula_2.77": 2.77 * 8 ** 0.245,
    "paper_claims": {"alpha": 0.245, "c0": 2.77, "R2": 0.9998, "N256": 4.58},
}

# ---- analytic learnable-parameter counts ----
cnn = (4 * 64 * 3 + 64) + 2 * 64 + (64 * 64 * 3 + 64) + 2 * 64         # conv+BN(scale,offset)


def lstm_single_bias(i, h):   # MATLAB lstmLayer / paper Sec. 3.5 convention
    return 4 * h * (i + h) + 4 * h


def lstm_torch(i, h):         # PyTorch nn.LSTM: b_ih and b_hh
    return 4 * h * (i + h) + 8 * h


paper = {
    "cnn": cnn,
    "lstm": lstm_single_bias(64, 128) + lstm_single_bias(128, 64),
    "fc": (2048 * 256 + 256) + (256 * 128 + 128) + (128 * 64 + 64),
}
paper["total"] = sum(paper.values())
matlab = {  # theta_NN_multioutput.m lines 56-77: conv,conv,lstm128,lstm64,fc(2)
    "cnn": cnn,
    "lstm": lstm_single_bias(64, 128) + lstm_single_bias(128, 64),
    "fc_out": 64 * 2 + 2,
}
matlab["total"] = sum(matlab.values())
torch_m = {  # train_cnn_lstm.py lines 93-116, N=32
    "cnn": cnn,
    "lstm": lstm_torch(64, 128) + lstm_torch(128, 128),
    "lstm_proj": 128 * 64 + 64,
    "fc": (64 * 32 * 256 + 256) + (256 * 128 + 128) + (128 * 64 + 64) + (64 * 64 + 64),
}
torch_m["total"] = sum(torch_m.values())
out["params"] = {"paper_sec3_5_architecture": paper,
                 "theta_NN_multioutput_m": matlab,
                 "train_cnn_lstm_py_N32": torch_m,
                 "paper_claim_total": 727360}

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "step3_arith_check.json")
with open(path, "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
