"""
Imperfect CSI, single-user MISO: the published phase-aware CNN-LSTM against
tuned classical optimizers (Task 2 of the thesis plan, single-user part).

Error model: ris_mu.sumiso.csi (cascaded and direct channel estimated with
relative error power e2, per-scenario scale). Phase and BS beam come from
the estimate; the rate is evaluated on the true channel.

Arms at every e2 (reported separately, never mixed):
  (a) CNN-LSTM trained on clean channels, fed the estimate (robustness only)
  (b) CNN-LSTM trained on estimates at this e2 (fresh noise every epoch),
      labels = optimum of the TRUE channel             (the actual claim)
  (b)+CD-1  one coordinate-ascent sweep on the estimate from (b)
  SU-align, CD-s (s sweeps), Adam-L (step size per L) on the estimate.
  Classical hyper-parameters are selected on validation data at every e2:
  sweeps, steps and step size, since early stopping regularizes under error.

Axis 1, static (t=0): validation = 1000 of the training draw's val split,
test = its 6000-scenario test split (seed 2026; the networks never saw it).
Axis 2, mobility (equal milliseconds): effective rate at the method's
latency, latencies from results/sumiso_mobility_eval.json (same code, timed
on an idle machine; the error does not change the cost). The estimate is
taken at t=0 for the phase; the beam uses a fresh estimate (same e2) of the
channel at the delivery time. Selection on a mobility draw with seed 12,
report on seed 11 (the single-user set of the paper).
"""
import sys
import json
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV
from ris_mu.sumiso import csi as CSI
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, features_ab, restore_common_phase

ap = argparse.ArgumentParser()
ap.add_argument("--e2", type=float, nargs="*", default=[0.0, 0.01, 0.03, 0.1, 0.3])
ap.add_argument("--n_mob", type=int, default=400)
ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--tag", default="sumiso_csi_eval")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(a.threads)

CD_S = [1, 2, 3, 5, 10, 30]
ADAM_L = [1, 2, 4, 8, 16, 32, 64]
LRS = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
LAT = json.load(open(ROOT / "results" / "sumiso_mobility_eval.json"))["latency_ms"]

z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
snr = float(z["snr_scale"])
perm = np.random.default_rng(0).permutation(len(z["theta"]))      # same split as sumiso_train.py
iva, ite = perm[28000:29000], perm[34000:]


def cas(idx):
    return SV.cascade(torch.as_tensor(z["F"][idx]), torch.as_tensor(z["G"][idx]), torch.as_tensor(z["hd"][idx]))


def load_net(tag):
    ck = torch.load(ROOT / "results" / f"{tag}.pt")
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], ck.get("head", "flat"), ck.get("n_out", 2))
    net.load_state_dict(ck["state"])
    net.eval()
    return net, ck["mu"], ck["sd"]


def cnn(netpack, ah, Bh):
    net, mu, sd = netpack
    with torch.no_grad():
        out = []
        for i in range(0, len(ah), 2000):
            x = (features_ab(ah[i:i + 2000], Bh[i:i + 2000]) - mu) / (sd + 1e-9)
            out.append(phase(net(x)))
        return restore_common_phase(torch.cat(out), ah, Bh)


def adam(ah, Bh, th0, L, lr):
    th = th0.clone().requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr)
    for _ in range(L):
        loss = -torch.log2(1 + SV.gain(th, ah, Bh) * snr).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return th.detach()


def phases(ah, Bh, nets, lr_of):
    """All arms' phases computed from the estimate."""
    al = SV.su_align(ah, Bh)
    P = {"SU-align": al}
    for s in CD_S:
        P[f"CD-{s}"] = SV.coord_ascent(ah, Bh, al, sweeps=s, tol=-1)[0]
    for L in ADAM_L:
        P[f"Adam-{L}"] = adam(ah, Bh, al, L, lr_of[L])
    P["CNN (a) clean-trained"] = cnn(nets["a"], ah, Bh)
    P["CNN (b) noise-trained"] = cnn(nets["b"], ah, Bh)
    P["CNN (b) + CD-1"] = SV.coord_ascent(ah, Bh, P["CNN (b) noise-trained"], sweeps=1, tol=-1)[0]
    return P


LAT_OF = {"CNN (a) clean-trained": LAT["CNN-LSTM"], "CNN (b) noise-trained": LAT["CNN-LSTM"],
          "CNN (b) + CD-1": LAT["CNN-LSTM+CD-1"], "CD-30": None}
LAT_OF.update({k: v for k, v in LAT.items() if k in [f"CD-{s}" for s in CD_S] + [f"Adam-{L}" for L in ADAM_L] + ["SU-align"]})
CLASSICAL = ["SU-align"] + [f"CD-{s}" for s in CD_S] + [f"Adam-{L}" for L in ADAM_L]

# ---- mobility draws: validation seed 12, report seed 11 ---------------------
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0)


def mob(seed):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(a.n_mob)
    assert abs(cfg.snr_scale() - snr) < 1e-6 * snr
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    return [SV.cascade(F, torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64),
                       torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64)) for m in range(len(TIMES))]


MOB = {"val": mob(12), "test": mob(11)}

res = dict(config=vars(a), latency_ms_source="results/sumiso_mobility_eval.json", latency_ms=LAT_OF, levels={})
rng_bs = np.random.default_rng(0)


def boot(diff):
    bs = [diff[rng_bs.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


for e2 in a.e2:
    print(f"=== e2 = {e2}", flush=True)
    nets = {"a": load_net("sumiso_cnnlstm_seq"),
            "b": load_net("sumiso_cnnlstm_seq" if e2 == 0 else f"sumiso_cnnlstm_seq_csi{e2:g}")}
    g = torch.Generator().manual_seed(1000 + int(round(e2 * 1e4)))
    # --- static
    Av, Bv = cas(iva); Avh, Bvh = CSI.estimate(Av, Bv, e2, g)
    At, Bt = cas(ite); Ath, Bth = CSI.estimate(At, Bt, e2, g)
    al_v = SV.su_align(Avh, Bvh)
    lr_of = {}
    for L in ADAM_L:
        sc = {lr: float(CSI.rate_mismatched(adam(Avh, Bvh, al_v, L, lr), Av, Bv, Avh, Bvh, snr).mean()) for lr in LRS}
        lr_of[L] = max(sc, key=sc.get)
    Pv = phases(Avh, Bvh, nets, lr_of)
    Pt = phases(Ath, Bth, nets, lr_of)
    val = {k: float(CSI.rate_mismatched(th, Av, Bv, Avh, Bvh, snr).mean()) for k, th in Pv.items()}
    rt = {k: CSI.rate_mismatched(th, At, Bt, Ath, Bth, snr).numpy() for k, th in Pt.items()}
    best_cl = max(CLASSICAL, key=lambda k: val[k])
    oracle = float(torch.log2(1 + snr * SV.gain(torch.as_tensor(z["theta"][ite]).float(), At, Bt)).mean())
    static = dict(adam_lr=lr_of, val=val, test={k: float(v.mean()) for k, v in rt.items()},
                  classical_selected_on_val=best_cl, oracle_true_channel=oracle,
                  b_minus_best_classical=float((rt["CNN (b) noise-trained"] - rt[best_cl]).mean()),
                  b_minus_best_classical_ci=boot(rt["CNN (b) noise-trained"] - rt[best_cl]),
                  bcd_minus_best_classical=float((rt["CNN (b) + CD-1"] - rt[best_cl]).mean()),
                  bcd_minus_best_classical_ci=boot(rt["CNN (b) + CD-1"] - rt[best_cl]),
                  b_minus_a=float((rt["CNN (b) noise-trained"] - rt["CNN (a) clean-trained"]).mean()))
    # --- mobility, equal milliseconds
    mobres = {}
    for part in ("val", "test"):
        C = MOB[part]
        A0, B0 = C[0]
        A0h, B0h = CSI.estimate(A0, B0, e2, g)
        P = phases(A0h, B0h, nets, lr_of)
        est_t = [CSI.estimate(A, B, e2, g) for A, B in C]          # beam from a fresh estimate at each time
        eff = {}
        for k, th in P.items():
            if LAT_OF.get(k) is None:
                continue
            curve = np.stack([CSI.rate_mismatched(th, A, B, ah, Bh, snr).numpy()
                              for (A, B), (ah, Bh) in zip(C, est_t)], 1)
            eff[k] = np.array([np.interp(LAT_OF[k], TIMES, row) for row in curve])
        mobres[part] = eff
    cl_m = [k for k in CLASSICAL if k in mobres["val"]]
    best_m = max(cl_m, key=lambda k: mobres["val"][k].mean())
    te = mobres["test"]
    mobility = dict(val={k: float(v.mean()) for k, v in mobres["val"].items()},
                    test={k: float(v.mean()) for k, v in te.items()},
                    classical_selected_on_val=best_m,
                    b_minus_best_classical=float((te["CNN (b) noise-trained"] - te[best_m]).mean()),
                    b_minus_best_classical_ci=boot(te["CNN (b) noise-trained"] - te[best_m]),
                    bcd_minus_best_classical=float((te["CNN (b) + CD-1"] - te[best_m]).mean()),
                    bcd_minus_best_classical_ci=boot(te["CNN (b) + CD-1"] - te[best_m]))
    # dominance: is there a classical arm with lower latency and higher test effective rate?
    for k in ("CNN (b) noise-trained", "CNN (b) + CD-1"):
        dom = [c for c in cl_m if LAT_OF[c] < LAT_OF[k] and te[c].mean() > te[k].mean()]
        mobility[f"dominated_by[{k}]"] = dom
    res["levels"][str(e2)] = dict(static=static, mobility=mobility)
    print(f"  static : best classical (val) {best_cl} {static['test'][best_cl]:.4f} | (a) {static['test']['CNN (a) clean-trained']:.4f} "
          f"| (b) {static['test']['CNN (b) noise-trained']:.4f} | (b)+CD-1 {static['test']['CNN (b) + CD-1']:.4f} "
          f"| SU-align {static['test']['SU-align']:.4f} | oracle {oracle:.4f}")
    print(f"           (b)-best {static['b_minus_best_classical']:+.4f} CI {static['b_minus_best_classical_ci']}, "
          f"(b)+CD-1 - best {static['bcd_minus_best_classical']:+.4f} CI {static['bcd_minus_best_classical_ci']}")
    print(f"  mobility: best classical (val) {best_m} {mobility['test'][best_m]:.4f} | (b) {mobility['test']['CNN (b) noise-trained']:.4f} "
          f"| (b)+CD-1 {mobility['test']['CNN (b) + CD-1']:.4f} | dominated_by (b): {mobility['dominated_by[CNN (b) noise-trained]']}")
    json.dump(res, open(ROOT / "results" / f"{a.tag}.json", "w"), indent=1)
print("wrote", a.tag)
