"""
COPY of origin/thesis/bridge:thesis_exp/bridge/scripts/bridge_tracking.py for verification K4 (15 Nov 2026).
Inputs (eval_main.json, the trained network) are read from a read-only worktree of thesis/bridge (BRIDGE below).
--fix 0  identical logic (reproduction check against thesis/bridge raw/tracking.json)
--fix 1  fractional pilot charging and exact deployment instants (same correction as p4/takip_duzeltme/run.py)
--pilot  one T_p per process; output thesis_exp/p4/takip_duzeltme/raw/bridge_fix{0,1}_tp{T_p}.json
BRIDGE must be a checkout of origin/thesis/bridge (38b25bd); recreate with `git worktree add --detach <path> origin/thesis/bridge`.

Bridge task, part 4: periodic operation (the Table III set-up of scripts/mumiso_tracking.py) with the
one-shot network as an additional start: every cycle takes a channel snapshot, spends T_p on pilots (no data),
computes the phase and deploys it; the rate is averaged over 100-200 ms on a 0.5 ms grid.

Starts:  cold  SU-average on the new snapshot + L Adam steps        (L in STEPS)
         warm  the phase currently deployed + L Adam steps         (L in STEPS)
         net   the network on the new snapshot + L Adam steps      (L in 0..3)
Busy time per cycle = T_p + measured latency (thesis_exp/bridge/raw/eval_main.json): cold/warm use the
measured Adam-L latency (linear interpolation between measured L), net uses the measured net / net+Adam-k latency.
Adam step sizes are those chosen on the static validation split (eval_main.json).
Selection of (period U, L) for each start is done on a separate mobility draw (seed 12); the reported
numbers are on the aging set (seed 11). Paired bootstrap (2000) of net minus the best cold / warm policy.
Output (original script): thesis_exp/bridge/raw/tracking.json; this copy writes thesis_exp/p4/takip_duzeltme/raw/bridge_fix*.json
"""
import sys, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
BRIDGE = pathlib.Path("/tmp/claude-0/-home-user-sedasavascisen/36a1538b-b28f-5b37-970a-9a1a9a74083b/scratchpad/wt_bridge")
import argparse
_ap = argparse.ArgumentParser(); _ap.add_argument("--fix", type=int, required=True); _ap.add_argument("--pilot", type=float, required=True)
CLI = _ap.parse_args()
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B

torch.set_num_threads(1)
EV = json.load(open(BRIDGE / "thesis_exp/bridge/raw/eval_main.json"))
LAT = EV["latency"]["median_ms"]
LR_L = {int(k): v for k, v in EV["lr_per_L"].items()}; LR_K = {int(k): v for k, v in EV["lr_per_k"].items()}
CK = torch.load(BRIDGE / EV["config"]["ckpt"])
net = MuMisoNet(N=32, n_users=4, n_tx=8, mode="exchange", residual=CK["residual"], link_ratio=CK["link_ratio"])
net.load_state_dict(CK["state"]); net.eval()
DT = 0.5
TIMES = tuple(float(x) for x in np.arange(0.0, 200.0 + DT / 2, DT))
STEPS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 48]
NET_STEPS = [0, 1, 2, 3]
PERIODS = [None, 10.0, 20.0, 40.0, 80.0]
PILOTS = [CLI.pilot]
WINDOW = (100.0, 200.0)
_LS = sorted(int(k[5:]) for k in LAT if k.startswith("Adam-"))
adam_lat = lambda L: float(np.interp(L, _LS, [LAT[f"Adam-{x}"] for x in _LS]))
net_lat = lambda L: LAT["net"] if L == 0 else LAT[f"net+Adam-{L}"]


def load(seed):
    torch.manual_seed(0)
    panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=seed)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(400)
    return d, torch.as_tensor(d["F"], dtype=torch.complex64), torch.as_tensor(d["G_t"], dtype=torch.complex64), \
        torch.as_tensor(d["hd_t"], dtype=torch.complex64), 1.0, 1.0 / cfg.snr_scale()


def run(seed):
    d, F, G, H, pt, nv = load(seed)
    M = len(TIMES)
    th0 = B.su_average(F, G[:, 0], H[:, 0], pt, nv)[1]
    minrate = lambda th, m: S.rates(F, G[:, m], H[:, m], torch.cos(th), torch.sin(th), pt, nv, "zf").min(-1).values

    def adam(start, m, L, lr):
        dl = torch.zeros(400, 32, requires_grad=True); opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = start + dl
            R = S.rates(F, G[:, m], H[:, m], torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward(); opt.step(); opt.zero_grad()
        return (start + dl).detach()

    def netphase(m):
        phi = S.su_align_phase(F, G[:, m], H[:, m]).numpy()
        X = torch.from_numpy(mumiso_features(d["F"], d["G_t"][:, m], d["hd_t"][:, m], phi, link_ratio=CK["link_ratio"]))
        with torch.no_grad():
            c, s = net.phases(X)
        return torch.atan2(s, c)

    grid = lambda t: int(round(t / DT))

    def simulate(start, L, t_p, period):
        busy = t_p + (net_lat(L) if start == "net" else adam_lat(L))
        cycle = busy if period is None else period
        if busy > cycle + 1e-9:
            return None
        deploy, pilot, snap = {}, np.zeros(M, bool), 0.0
        events, pil_iv = [], []
        while snap < TIMES[-1]:
            m = grid(snap)
            pilot[m:min(grid(snap + t_p), M)] = t_p > 0
            if start == "net":
                th = netphase(m)
                th = adam(th, m, L, LR_K[L]) if L > 0 else th
            else:
                if start == "warm":
                    ks = [k for k in deploy if k <= m]; s0 = deploy[max(ks)] if ks else th0
                else:
                    s0 = B.su_average(F, G[:, m], H[:, m], pt, nv)[1]
                th = adam(s0, m, L, LR_L.get(L, 0.5) if L in LR_L else LR_L[min(LR_L, key=lambda x: abs(x - L))])
            if grid(snap + busy) < M:
                deploy[grid(snap + busy)] = th
            if snap + busy <= TIMES[-1] + DT:
                events.append((snap + busy, th))
            if t_p > 0:
                pil_iv.append((snap, snap + t_p))
            snap += cycle
        if not deploy or TIMES[min(deploy)] > WINDOW[0]:
            return None
        sel = [m for m in range(M) if WINDOW[0] <= TIMES[m] <= WINDOW[1]]
        if CLI.fix:
            ev = sorted(events, key=lambda e: e[0])
            out_ = np.zeros((400, len(sel)))
            for j, m in enumerate(sel):
                a, b = TIMES[m], TIMES[m] + DT
                bef = [e for e in ev if e[0] <= a]
                cuts = [(a, bef[-1][1] if bef else th0)] + [(t, ph) for t, ph in ev if a < t < b]
                acc = np.zeros(400)
                for i, (t0_, ph) in enumerate(cuts):
                    t1_ = cuts[i + 1][0] if i + 1 < len(cuts) else b
                    acc += (t1_ - t0_) / DT * minrate(ph, m).numpy()
                ov = sum(max(0.0, min(b, q1) - max(a, q0)) for q0, q1 in pil_iv)
                out_[:, j] = acc * max(0.0, 1.0 - ov / DT)
            return out_.mean(1).astype(np.float32)
        rates, cur = np.zeros((400, M), np.float32), th0
        for m in range(M):
            if m in deploy:
                cur = deploy[m]
            rates[:, m] = 0.0 if pilot[m] else minrate(cur, m).numpy()
        sel = [m for m in range(M) if WINDOW[0] <= TIMES[m] <= WINDOW[1]]
        return rates[:, sel].mean(1)

    out = {}
    for t_p in PILOTS:
        out[t_p] = {}
        for start, steps in (("cold", STEPS), ("warm", STEPS), ("net", NET_STEPS)):
            tab = {}
            for U in PERIODS:
                for L in steps:
                    v = simulate(start, L, t_p, U)
                    if v is not None:
                        tab[(U, L)] = v
            out[t_p][start] = tab
            print(f"seed {seed} T_p={t_p} {start}: {len(tab)} policies", flush=True)
    return out


val, test = run(12), run(11)
rng = np.random.default_rng(0)
idx = rng.integers(0, 400, (2000, 400))
res = dict(fix=CLI.fix, bridge_inputs_commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=BRIDGE).stdout.strip(),
           commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           latency_source="thesis_exp/bridge/raw/eval_main.json", window_ms=WINDOW, by_pilot={})
for t_p in PILOTS:
    blk = {}
    sel = {s: max(val[t_p][s], key=lambda k: val[t_p][s][k].mean()) for s in ("cold", "warm", "net")}
    for s, k in sel.items():
        v = test[t_p][s][k]
        blk[s] = dict(period="b2b" if k[0] is None else k[0], L=k[1], rate=float(v.mean()),
                      ci=[float(np.percentile(v[idx].mean(1), q)) for q in (2.5, 97.5)])
    for s in ("cold", "warm"):
        dd = test[t_p]["net"][sel["net"]] - test[t_p][s][sel[s]]
        blk[f"net_minus_{s}"] = dict(diff=float(dd.mean()), ci=[float(np.percentile(dd[idx].mean(1), q)) for q in (2.5, 97.5)])
    res["by_pilot"][str(t_p)] = blk
    print(t_p, json.dumps(blk), flush=True)
_o = ROOT / f"thesis_exp/p4/takip_duzeltme/raw/bridge_fix{CLI.fix}_tp{CLI.pilot:g}.json"
json.dump(res, open(_o, "w"), indent=1)
print("wrote", _o)
