# Verification U44 (round 6; copied from the verifier's scratch script): effect of grad mode on learned arm and of SU-average start on Adam arm,
# same setup as thesis_exp/p4/optimize_sure/run.py (seed 11, NS scenarios, torch.manual_seed 0, 1 thread).
import sys, os, time, json, pathlib
ROOT = pathlib.Path("/home/user/sedasavascisen"); sys.path.insert(0, str(ROOT))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
torch.set_num_threads(1); torch.manual_seed(0)
REPS, ROUNDS, NS = 20, 3, 20
load_start = os.getloadavg()
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
load0 = os.getloadavg()
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
d = MuMisoChannel(panel, cfg).generate(20)
F, G, hd, _ = to_torch(d); pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
TH0 = B.su_average(F, G, hd, pt, nv)[1]
info = dict(N_panel=int(panel.positions.shape[0]), n_clusters=getattr(cfg, "n_clusters", None))
def adam(L, with_start):
    def f(i):
        sl = slice(i, i + 1)
        th0 = B.su_average(F[sl], G[sl], hd[sl], pt, nv)[1] if with_start else TH0[sl]
        dl = torch.zeros_like(th0, requires_grad=True); opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            th = th0 + dl
            R = S.rates(F[sl], G[sl], hd[sl], torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward(); opt.step(); opt.zero_grad()
        return th0 + dl.detach()
    return f
def learned(L, nograd, with_feat=False):
    net = UnrolledMuMiso(N=32, n_users=4, n_tx=8, steps=L, mode="exchange", use_grad=True).eval()
    def f(i):
        sl = slice(i, i + 1)
        ctx = torch.no_grad() if nograd else torch.enable_grad()
        with ctx:
            if with_feat:
                ph = S.su_align_phase(F[sl], G[sl], hd[sl])
                x = torch.from_numpy(mumiso_features(d["F"][sl], d["G"][sl], d["hd"][sl], ph.numpy()))
                t0 = B.su_average(F[sl], G[sl], hd[sl], pt, nv)[1]
            else:
                x, t0 = X[sl], TH0[sl]
            return net(x, F[sl], G[sl], hd[sl], pt, nv, t0)
    return f
def timeit(f):
    rounds = []
    for _ in range(ROUNDS):
        per = []
        for i in range(NS):
            f(i); f(i); t = []
            for _ in range(REPS):
                a = time.perf_counter(); f(i); t.append(time.perf_counter() - a)
            per.append(np.median(t) * 1e3)
        rounds.append(float(np.median(per)))
    return dict(rounds_ms=rounds, median_ms=float(np.median(rounds)))
arms = {}
for L in (1, 8):
    arms[f"Adam-{L} start-in"] = timeit(adam(L, True))
    arms[f"Adam-{L} start-out"] = timeit(adam(L, False))
    arms[f"learned-{L} enable_grad"] = timeit(learned(L, False))
    arms[f"learned-{L} no_grad"] = timeit(learned(L, True))
    arms[f"learned-{L} no_grad+feat+start"] = timeit(learned(L, True, True))
    for k in list(arms)[-5:]: print(k, round(arms[k]["median_ms"], 3), [round(x, 3) for x in arms[k]["rounds_ms"]], flush=True)
out = dict(commit=__import__("subprocess").run(["git","rev-parse","HEAD"],capture_output=True,text=True,cwd=ROOT).stdout.strip(), info=info, load_start=load_start, load_before=load0, load_after=os.getloadavg(), threads=torch.get_num_threads(), torch=torch.__version__, arms=arms)
json.dump(out, open(pathlib.Path(__file__).parent / "raw" / "definitions.json", "w"), indent=1)
print(info, load0, out["load_after"])
