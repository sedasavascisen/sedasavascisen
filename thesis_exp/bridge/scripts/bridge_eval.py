"""
Bridge task, parts 2-3: the one-shot network on the effective-rate axis (Definition 1) and dominance
(Definition 2), at 1.5 m/s and at the speeds of Table II.

Arms (phases computed from the t = 0 channel of each scenario):
  net            one forward pass (features incl. SU-align phase -> MuMisoNet -> unit circle)
  net+Adam-k     k = 1, 2, 3 Adam steps on the soft-min surrogate starting from the network output
  SU-best-of     closed form
  Adam-L         from SU-average, L in STEPS
Hyper-parameters (Adam step size per L and per k) are chosen ONLY on the static validation split
(bridge_train.build, seed 2027, va); the best classical arm for the paired comparison is chosen on a
separate mobility draw (seed 12); everything is reported on the aging set (seed 11, 400 scenarios).
Latency: one scenario at a time, one thread, median of --reps calls in --rounds rounds over --n_time
scenarios, waiting for load average < 0.5; the network's time includes feature construction.
Effective rate: per scenario, the min-user rate (ZF precoder on the current channel) of the fixed phase,
interpolated on the time grid at the arm's latency (+ T_ov = 0).
Output: thesis_exp/bridge/raw/eval_<tag>.json
"""
import sys, os, json, time, argparse, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, to_torch
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", required=True, help="thesis_exp/bridge/raw/train/<tag>.pt")
ap.add_argument("--speeds_kmh", default="5.4")
ap.add_argument("--reps", type=int, default=25)
ap.add_argument("--rounds", type=int, default=3)
ap.add_argument("--n_time", type=int, default=20)
ap.add_argument("--latency_json", default="", help="reuse latencies from a previous eval json")
ap.add_argument("--tag", default="main")
a = ap.parse_args()
torch.set_num_threads(4)
OUT = ROOT / "thesis_exp/bridge/raw"
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]
KS = [1, 2, 3]
LRS = [0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5]
TIMES = tuple(float(x) for x in np.arange(0.0, 40.0 + 0.25, 0.5)) + (50.0, 75.0, 100.0, 150.0, 200.0)

ck = torch.load(ROOT / a.ckpt)
net = MuMisoNet(N=32, n_users=4, n_tx=8, mode="exchange", residual=ck["residual"], link_ratio=ck["link_ratio"])
net.load_state_dict(ck["state"]); net.eval()
LR_FEAT = ck["link_ratio"]


def net_phase(F, G, hd, Fn, Gn, hdn):
    """F,G,hd torch; *n numpy versions (feature code is NumPy)."""
    phi = S.su_align_phase(F, G, hd).numpy()
    X = torch.from_numpy(mumiso_features(Fn, Gn, hdn, phi, link_ratio=LR_FEAT))
    with torch.no_grad():
        c, s = net.phases(X)
    return torch.atan2(s, c)


def adam(F, G, hd, start, L, lr, pt, nv):
    dl = torch.zeros_like(start, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step(); opt.zero_grad()
    return (start + dl).detach()


def minrate(F, G, hd, th, pt, nv):
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf").min(-1).values


# ---------------------------------------------------------- hyper-parameters on the static validation split
from bridge_train import build
_, cfgv, dv = build(False, 2027, 6000)
_, va, _ = split_indices(6000, seed=0)
Fv, Gv, hdv, _ = to_torch(dict(F=dv["F"][va], G=dv["G"][va], hd=dv["hd"][va]))
ptv, nvv = 1.0, 1.0 / cfgv.snr_scale()
_, th_su_v = B.su_average(Fv, Gv, hdv, ptv, nvv)
th_net_v = net_phase(Fv, Gv, hdv, dv["F"][va], dv["G"][va], dv["hd"][va])
lr_L = {L: max(LRS, key=lambda lr: minrate(Fv, Gv, hdv, adam(Fv, Gv, hdv, th_su_v, L, lr, ptv, nvv), ptv, nvv).mean().item()) for L in STEPS}
lr_k = {k: max(LRS, key=lambda lr: minrate(Fv, Gv, hdv, adam(Fv, Gv, hdv, th_net_v, k, lr, ptv, nvv), ptv, nvv).mean().item()) for k in KS}
static_val = dict(su_average=minrate(Fv, Gv, hdv, th_su_v, ptv, nvv).mean().item(), net=minrate(Fv, Gv, hdv, th_net_v, ptv, nvv).mean().item())
print("lr per L", lr_L, "lr per k", lr_k, "static val", static_val, flush=True)


def aging(seed, v):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": v, "times_ms": TIMES, "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(400)
    F = torch.as_tensor(d["F"], dtype=torch.complex64)
    Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
    return d, F, Gt, Ht, 1.0, 1.0 / cfg.snr_scale()


def arm_phases(d, F, G0, H0, pt, nv):
    _, th_su = B.su_average(F, G0, H0, pt, nv)
    _, th_best = B.su_best_of(F, G0, H0, pt, nv)
    th_net = net_phase(F, G0, H0, d["F"], d["G_t"][:, 0], d["hd_t"][:, 0])
    P = {"SU-best-of": th_best, "net": th_net}
    for k in KS:
        P[f"net+Adam-{k}"] = adam(F, G0, H0, th_net, k, lr_k[k], pt, nv)
    for L in STEPS:
        P[f"Adam-{L}"] = adam(F, G0, H0, th_su, L, lr_L[L], pt, nv)
    return P


# ---------------------------------------------------------- latency
def time_arms(d, F, G0, H0, pt, nv):
    load0 = os.getloadavg()[0]
    while os.getloadavg()[0] >= 0.5:
        time.sleep(10)
    load1 = os.getloadavg()[0]
    torch.set_num_threads(1)
    fns = {"SU-best-of": lambda i: B.su_best_of(F[i], G0[i], H0[i], pt, nv),
           "net": lambda i: net_phase(F[i], G0[i], H0[i], d["F"][i], d["G_t"][i, 0], d["hd_t"][i, 0])}
    for k in KS:
        fns[f"net+Adam-{k}"] = (lambda k: lambda i: adam(F[i], G0[i], H0[i], net_phase(F[i], G0[i], H0[i], d["F"][i], d["G_t"][i, 0], d["hd_t"][i, 0]), k, lr_k[k], pt, nv))(k)
    for L in STEPS:
        fns[f"Adam-{L}"] = (lambda L: lambda i: adam(F[i], G0[i], H0[i], B.su_average(F[i], G0[i], H0[i], pt, nv)[1], L, lr_L[L], pt, nv))(L)
    rounds = {}
    for name, f in fns.items():
        rr = []
        for r in range(a.rounds):
            per = []
            for j in range(a.n_time):
                i = slice(j, j + 1); f(i)
                t = []
                for _ in range(a.reps):
                    t0 = time.perf_counter(); f(i); t.append(time.perf_counter() - t0)
                per.append(np.median(t) * 1e3)
            rr.append(float(np.median(per)))
        rounds[name] = rr
        print(f"  latency {name:>12}: {np.median(rr):8.3f} ms  rounds {['%.3f' % x for x in rr]}", flush=True)
    torch.set_num_threads(4)
    return dict(load_start=load0, load_before=load1, load_after=os.getloadavg()[0], rounds_ms=rounds,
                median_ms={k: float(np.median(v)) for k, v in rounds.items()})


def effective(P, F, Gt, Ht, pt, nv, lat):
    out = {}
    for k, th in P.items():
        c = torch.stack([minrate(F, Gt[m], Ht[m], th, pt, nv) for m in range(len(TIMES))], 1).numpy()
        out[k] = dict(t0=c[:, 0], eff=np.array([np.interp(lat[k], TIMES, row) for row in c]))
    return out


rng = np.random.default_rng(0)
def boot(x):
    b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(2000)]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


res = dict(config=vars(a), commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           lr_per_L=lr_L, lr_per_k=lr_k, static_val=static_val, times_ms=TIMES, speeds={})
lat = None
if a.latency_json:
    lj = json.load(open(ROOT / a.latency_json)); lat = lj["latency"]["median_ms"]; res["latency"] = lj["latency"]; res["latency_reused_from"] = a.latency_json
for kmh in [float(x) for x in a.speeds_kmh.split(",")]:
    v = kmh / 3.6
    dt, Ft, Gtt, Htt, pt, nv = aging(11, v)
    dv_, Fv_, Gvt, Hvt, ptv_, nvv_ = aging(12, v)
    if lat is None:
        res["latency"] = time_arms(dt, Ft, Gtt[0], Htt[0], pt, nv); lat = res["latency"]["median_ms"]
    Pt = arm_phases(dt, Ft, Gtt[0], Htt[0], pt, nv); Pv = arm_phases(dv_, Fv_, Gvt[0], Hvt[0], ptv_, nvv_)
    Et = effective(Pt, Ft, Gtt, Htt, pt, nv, lat); Ev = effective(Pv, Fv_, Gvt, Hvt, ptv_, nvv_, lat)
    classical = ["SU-best-of"] + [f"Adam-{L}" for L in STEPS]
    best_c = max(classical, key=lambda k: Ev[k]["eff"].mean())
    rows = {k: dict(latency_ms=lat[k], t0=float(e["t0"].mean()), effective=float(e["eff"].mean()), effective_ci=boot(e["eff"])) for k, e in Et.items()}
    learned = ["net"] + [f"net+Adam-{k}" for k in KS]
    dom = {k: [c for c in classical if lat[c] <= lat[k] and Et[c]["eff"].mean() > Et[k]["eff"].mean()] for k in learned}
    diff = {k: dict(vs=best_c, mean=float((Et[k]["eff"] - Et[best_c]["eff"]).mean()), ci=boot(Et[k]["eff"] - Et[best_c]["eff"])) for k in learned}
    diff_t0 = {k: dict(vs="SU-best-of", mean=float((Et[k]["t0"] - Et["SU-best-of"]["t0"]).mean()), ci=boot(Et[k]["t0"] - Et["SU-best-of"]["t0"])) for k in learned}
    res["speeds"][str(kmh)] = dict(coherence_ms=0.423 / (v * 3e9 / 3e8) * 1e3, rows=rows, best_classical_on_val=best_c,
                                   learned_minus_best_classical=diff, learned_minus_su_best_of_t0=diff_t0, dominated_by=dom)
    print(f"== {kmh} km/h: best classical (val) {best_c} {rows[best_c]['effective']:.4f}", flush=True)
    for k in learned:
        print(f"   {k:>12} lat {lat[k]:7.3f} eff {rows[k]['effective']:.4f}  vs best {diff[k]['mean']:+.4f} {diff[k]['ci']}  dominated by {dom[k][:4]}", flush=True)
    json.dump(res, open(OUT / f"eval_{a.tag}.json", "w"), indent=1)
print("wrote", OUT / f"eval_{a.tag}.json")
