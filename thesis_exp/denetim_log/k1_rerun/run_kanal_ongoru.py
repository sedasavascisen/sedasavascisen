"""
Prompt 4.1 — channel prediction. The BS has the channel at t = 0 and, for the predictive arms, also at
t = -Delta (and -2 Delta). It predicts the user-side channels G(tau), h_d(tau) at the deployment time tau
(= the arm's measured latency), optimises on the PREDICTED channel, and the phase is scored on the TRUE
channel at tau (Definition 1). F (BS-RIS) is static and known.

Predictors (per complex coefficient):
  none    use the t = 0 channel (the paper's setting)
  lin2    linear extrapolation through t = -Delta, 0                       (1 extra snapshot)
  lin3    least-squares line through t = -2Delta, -Delta, 0                 (2 extra snapshots)
  quad3   quadratic through the same three points                          (2 extra snapshots)
  kalman3 constant-velocity Kalman filter over the three snapshots; with scalar q, r its gain is
          data-independent, so it is a linear 3-tap predictor whose weights depend on q/r only;
          q/r chosen on the validation draw from {1e-4 ... 1e2}                  (2 extra snapshots)
Extra pilots: each extra snapshot is one more 48-symbol cascaded-channel estimate (Wang et al., K = 4,
N = 32, N_t = 8): 3.43 / 1.71 / 0.86 ms of airtime at 15 / 30 / 60 kHz. Reported, NOT charged in the
single-shot effective rate (the snapshots precede t = 0).
Arms per predictor: SU-best-of (latency of su_best_of) and SU-average + Adam-L, L in STEPS (latencies from
the re-measured one-thread run, thesis_exp/infra). Prediction compute time is not added (it is a few
multiply-adds per coefficient; measured separately in the report if needed).
Selection of L per (Delta, predictor) on the validation draw (seed 12); report on seed 11 with paired
bootstrap against the best no-prediction arm (also selected on seed 12).
Output: thesis_exp/p4/kanal_ongoru/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str('/home/user/sedasavascisen/thesis_exp/p4'))
import numpy as np, torch
from common import Aging, STEPS, adam_latency, LAT, boot, commit, check_same_scenarios
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--e2", type=float, default=0.0,
                help="estimation error of every snapshot (t=0 and history): CN noise with power e2 x the mean "
                     "coefficient power of that scenario and link (per-scenario scale, independent per snapshot, seed 3)")
cli = ap.parse_args()
torch.set_num_threads(2)
OUT = pathlib.Path('/tmp/claude-0/-home-user-sedasavascisen/36a1538b-b28f-5b37-970a-9a1a9a74083b/scratchpad/rerun_k1/kanal_ongoru'); OUT.mkdir(exist_ok=True)
DELTAS = [1.0, 2.0, 5.0]
GRID = [float(x) for x in np.arange(0.0, 40.0 + 0.25, 0.5)] + [50.0, 75.0, 100.0]
HIST = sorted({-d for d in DELTAS} | {-2 * d for d in DELTAS})
TIMES = GRID + HIST          # t = 0 MUST be the first grid point: the generator decides LoS state,
                             # Rician K and shadowing from the positions at index 0
QR = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 1e1, 1e2]


def kalman_weights(delta, tau, qr):
    """Weights w on (h(-2D), h(-D), h(0)) of the CV-Kalman prediction h_hat(tau) = sum w_i h_i (r = 1)."""
    Fm = np.array([[1.0, delta], [0.0, 1.0]])
    Q = qr * np.array([[delta ** 3 / 3, delta ** 2 / 2], [delta ** 2 / 2, delta]])
    Hm = np.array([[1.0, 0.0]])
    W = np.zeros((2, 3))                       # state as a linear map of the 3 observations
    P = np.diag([1e8, 1e8])
    for i in range(3):
        if i > 0:
            W = Fm @ W; P = Fm @ P @ Fm.T + Q
        S_ = Hm @ P @ Hm.T + 1.0
        K = P @ Hm.T / S_
        e = np.zeros((1, 3)); e[0, i] = 1.0
        W = W + K @ (e - Hm @ W)
        P = (np.eye(2) - K @ Hm) @ P
    return (np.array([[1.0, tau]]) @ W)[0]


def noisy(A, e2, seed):
    """Replace the snapshots the BS observes (t = 0 and the history) by estimates; A.G/A.H stay TRUE."""
    A.Gobs, A.Hobs = list(A.G), list(A.H)
    if e2 <= 0:
        return
    g = torch.Generator().manual_seed(seed)
    def est(X):
        p = (X.abs() ** 2).mean(dim=tuple(range(1, X.dim())), keepdim=True)
        z = torch.complex(torch.randn(X.shape, generator=g), torch.randn(X.shape, generator=g)) / 2 ** 0.5
        return X + (e2 * p).sqrt() * z.to(X.dtype)
    for t in [0.0] + HIST:
        m = A.idx(t); A.Gobs[m] = est(A.G[m]); A.Hobs[m] = est(A.H[m])


def predict(A, kind, delta, tau, qr=None):
    m0, m1 = A.idx(0.0), A.idx(-delta)
    class _O: pass
    o = _O(); o.G, o.H = A.Gobs, A.Hobs
    return _predict(o, A, kind, delta, tau, qr, m0, m1)


def _predict(A, AA, kind, delta, tau, qr, m0, m1):
    if kind == "none":
        return A.G[m0], A.H[m0]
    if kind == "lin2":
        a = tau / delta
        return A.G[m0] + a * (A.G[m0] - A.G[m1]), A.H[m0] + a * (A.H[m0] - A.H[m1])
    m2 = AA.idx(-2 * delta)
    ts = np.array([-2 * delta, -delta, 0.0])
    if kind == "lin3":
        X = np.stack([np.ones(3), ts], 1); w = np.array([1.0, tau]) @ np.linalg.pinv(X)
    elif kind == "quad3":
        X = np.stack([np.ones(3), ts, ts ** 2], 1); w = np.array([1.0, tau, tau ** 2]) @ np.linalg.inv(X)
    else:
        w = kalman_weights(delta, tau, qr)
    w = [float(x) for x in w]
    return (w[0] * A.G[m2] + w[1] * A.G[m1] + w[2] * A.G[m0], w[0] * A.H[m2] + w[1] * A.H[m1] + w[2] * A.H[m0])


def arms_eff(A, kind, delta, qr=None):
    """per-scenario effective rate for SU-best-of and Adam-L on the predicted channel."""
    out = {}
    lat = LAT["su_best_of"]; Gp, Hp = predict(A, kind, delta, lat, qr)
    th = A.su_best_of(G=Gp, H=Hp)
    out["SU-best-of"] = (lat, A.curve(th, GRID))
    for L in STEPS:
        lat = adam_latency(L); Gp, Hp = predict(A, kind, delta, lat, qr)
        th = A.adam(A.su_average(G=Gp, H=Hp), L, G=Gp, H=Hp)
        out[f"Adam-{L}"] = (lat, A.curve(th, GRID))
    return {k: np.array([np.interp(lat, GRID, row) for row in c]) for k, (lat, c) in out.items()}


val, test = Aging(12, TIMES), Aging(11, TIMES)
noisy(val, cli.e2, 3); noisy(test, cli.e2, 4)
res = dict(commit=commit(), e2=cli.e2, deltas_ms=DELTAS, extra_pilot_airtime_ms_per_snapshot={"15kHz": 3.43, "30kHz": 1.71, "60kHz": 0.86},
           su_average_t0_check=check_same_scenarios(test), runs={})
base_v, base_t = arms_eff(val, "none", 1.0), arms_eff(test, "none", 1.0)
bkey = max(base_v, key=lambda k: base_v[k].mean())
res["no_prediction"] = dict(selected_on_val=bkey, test=float(base_t[bkey].mean()), test_ci=boot(base_t[bkey]),
                            by_arm={k: float(v.mean()) for k, v in base_t.items()})
print("no prediction:", bkey, res["no_prediction"]["test"], flush=True)
for delta in DELTAS:
    for kind in ("lin2", "lin3", "quad3", "kalman3"):
        if kind == "kalman3":
            sc = {qr: max(v.mean() for v in arms_eff(val, kind, delta, qr).values()) for qr in QR}
            qr = max(sc, key=sc.get)
        else:
            qr = None
        ev, et = arms_eff(val, kind, delta, qr), arms_eff(test, kind, delta, qr)
        k = max(ev, key=lambda x: ev[x].mean())
        d = et[k] - base_t[bkey]
        res["runs"][f"{kind}|{delta}"] = dict(qr=qr, extra_snapshots=1 if kind == "lin2" else 2, selected_on_val=k,
                                              test=float(et[k].mean()), test_ci=boot(et[k]),
                                              minus_no_prediction=float(d.mean()), minus_no_prediction_ci=boot(d),
                                              by_arm={a: float(v.mean()) for a, v in et.items()})
        print(kind, delta, k, round(float(et[k].mean()), 4), round(float(d.mean()), 4), boot(d), flush=True)
        json.dump(res, open(OUT / ("results.json" if cli.e2 == 0 else f"results_e2_{cli.e2:g}.json"), "w"), indent=1)
print("wrote results", cli.e2)
