"""
Representation ablation for the published phase-aware CNN-LSTM.

Same network (the authors' MATLAB architecture, per-element head), same data
and training recipe; only the output changes:
  sincos      (sin, cos) with MSE                    -- published
  angle_mse   the wrapped angle with plain MSE       -- has the +-pi discontinuity
  angle_circ  the angle with loss 1 - cos(error)     -- strong periodic competitor
Two scenarios: SISO (N_t = 1, published label -angle(G_n F_n)) and MISO
(N_t = 8, optimum label with element 1 at zero); 3 seeds each
(runs: scripts/sumiso_train.py --head seq --output ... --seed ...).

Besides the test metrics stored by each run, this script reloads every
checkpoint and splits the test-set phase error by how close the label is to
the +-pi wrap: |theta| > 150 deg ("near wrap") versus |theta| < 90 deg.
That split is where the discontinuity argument predicts the difference.
Output: results/sumiso_representation.json
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features, canonical

ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
OUTS = ["sincos", "angle_mse", "angle_circ"]
SEEDS = [0, 1, 2]
res = {}
for sc, data in (("siso", "sumiso_siso"), ("miso", "sumiso_train")):
    z = np.load(ROOT / "data_sumiso" / f"{data}.npz")
    F, G, H = (torch.as_tensor(z[k]) for k in ("F", "G", "hd"))
    if sc == "siso":
        TH = -torch.angle(G[:, 0, :] * F[:, :, 0]).float()
    else:
        TH = canonical(torch.as_tensor(z["theta"]).float())
    X = features(F, G, H, "cascade")
    te = np.random.default_rng(0).permutation(len(TH))[34000:]
    near = TH[te].abs() > np.deg2rad(150)
    far = TH[te].abs() < np.deg2rad(90)
    res[sc] = {}
    for o in OUTS:
        runs = []
        for s in SEEDS:
            tag = f"sumiso_abl_{sc}_{o}_s{s}"
            r = json.load(open(ROOT / "results" / f"{tag}.json"))
            ck = torch.load(ROOT / "results" / f"{tag}.pt")
            net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck["head"], ck["n_out"])
            net.load_state_dict(ck["state"]); net.eval()
            with torch.no_grad():
                th = torch.cat([phase(net((X[te[i:i + 2000]] - ck["mu"]) / (ck["sd"] + 1e-9)))
                                for i in range(0, len(te), 2000)])
            d = torch.angle(torch.exp(1j * (th - TH[te]).to(torch.complex64))) * 180 / np.pi
            rm = lambda m: float(torch.sqrt((d[m] ** 2).mean()))
            runs.append(dict(seed=s, rmse=r["test_rmse_deg"], sr5=r["SR@5"], rate=r["rate_cnnlstm"],
                             rate_plus_1_sweep=r["rate_cnnlstm_plus_1_sweep"],
                             rmse_near_wrap=rm(near), rmse_far_from_wrap=rm(far),
                             best_val=r["best_val_rmse_deg"]))
        agg = {k: dict(mean=float(np.mean([u[k] for u in runs])), std=float(np.std([u[k] for u in runs], ddof=1)))
               for k in ("rmse", "sr5", "rate", "rate_plus_1_sweep", "rmse_near_wrap", "rmse_far_from_wrap")}
        res[sc][o] = dict(runs=runs, **agg)
    ref = json.load(open(ROOT / "results" / f"sumiso_abl_{sc}_sincos_s0.json"))
    res[sc]["_reference"] = dict(rate_su_align=ref["rate_su_align"], rate_label=ref["rate_label"],
                                 n_test=len(te), frac_near_wrap=float(near.float().mean()))
    # sincos wins in every seed? (seed-paired: same seed = same init stream and batch order)
    for o in ("angle_mse", "angle_circ"):
        res[sc][f"sincos_better_than_{o}_all_seeds"] = all(
            a_["rmse"] < b_["rmse"] for a_, b_ in zip(res[sc]["sincos"]["runs"], res[sc][o]["runs"]))
json.dump(res, open(ROOT / "results" / "sumiso_representation.json", "w"), indent=1)
for sc in res:
    print(f"== {sc}  (SU-align {res[sc]['_reference']['rate_su_align']:.3f}, optimum {res[sc]['_reference']['rate_label']:.3f}, "
          f"near-wrap fraction {res[sc]['_reference']['frac_near_wrap']:.3f})")
    for o in OUTS:
        v = res[sc][o]
        print(f"  {o:11s} RMSE {v['rmse']['mean']:6.2f}±{v['rmse']['std']:.2f}  SR@5 {100*v['sr5']['mean']:5.1f}%  "
              f"near-wrap {v['rmse_near_wrap']['mean']:6.2f}  far {v['rmse_far_from_wrap']['mean']:6.2f}  "
              f"rate {v['rate']['mean']:.3f}±{v['rate']['std']:.3f}")
    print("  sincos better in all seeds:", {o: res[sc][f"sincos_better_than_{o}_all_seeds"] for o in ("angle_mse", "angle_circ")})
