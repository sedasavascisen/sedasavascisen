"""
Prompt 4.6 — optimised execution times of an Adam step and a learned step; cost ratio.

Learned step: ris_mu.mumiso.unrolled.UnrolledMuMiso (mode 'exchange', use_grad True, as in the paper's
learned update rule), with steps in {1, 8}. Weights are untrained: execution time does not depend on the
weight values (no data-dependent control flow), so no retraining is needed for TIMING.
Adam: SU-average start + L steps on the soft-min surrogate (beta 8), L in {1, 8}.
Back-ends tried, each recorded as measured or as the error that prevented it:
  eager            plain PyTorch (the paper's setting)
  torch.compile    default mode (Inductor, CPU)
  torch.jit.trace  of the full call (expected to fail where autograd is used inside the forward)
  GPU              torch.cuda.is_available() is False on this machine -> UNPRODUCIBLE here
Protocol (CLAUDE.md): idle machine (load < 0.5 before timing), one thread, one scenario, median of
REPS calls per scenario, median over scenarios, ROUNDS rounds; load before/after recorded.
Inputs: static-set construction of the paper (make_mumiso_scenario seed 11, 6 scatterers), 20 scenarios.
Output: thesis_exp/p4/optimize_sure/raw/results.json
"""
import sys, os, time, json, pathlib, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import commit, ROOT
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
REPS, ROUNDS, NS = 20, 3, 20

load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(15)
load1 = os.getloadavg()[0]
torch.set_num_threads(1)
torch.manual_seed(0)
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
TH0 = B.su_average(F, G, hd, pt, nv)[1]


def adam_call(L):
    def f(i):
        sl = slice(i, i + 1)
        th0 = B.su_average(F[sl], G[sl], hd[sl], pt, nv)[1]
        dl = torch.zeros_like(th0, requires_grad=True); opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            th = th0 + dl
            R = S.rates(F[sl], G[sl], hd[sl], torch.cos(th), torch.sin(th), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward(); opt.step(); opt.zero_grad()
        return th0 + dl.detach()
    return f


def learned_call(L, backend):
    net = UnrolledMuMiso(N=32, n_users=4, n_tx=8, steps=L, mode="exchange", use_grad=True).eval()
    fwd = net
    if backend == "torch.compile":
        fwd = torch.compile(net)
    elif backend == "torch.jit.trace":
        fwd = torch.jit.trace(lambda x, F_, G_, h_, t_: net(x, F_, G_, h_, pt, nv, t_), (X[:1], F[:1], G[:1], hd[:1], TH0[:1]), check_trace=False)
        return lambda i: fwd(X[i:i + 1], F[i:i + 1], G[i:i + 1], hd[i:i + 1], TH0[i:i + 1])
    return lambda i: fwd(X[i:i + 1], F[i:i + 1], G[i:i + 1], hd[i:i + 1], pt, nv, TH0[i:i + 1])


def adam_backend(L, backend):
    f = adam_call(L)
    if backend == "torch.compile":
        rates_c = torch.compile(S.rates)
        def f(i, L=L):
            sl = slice(i, i + 1)
            th0 = B.su_average(F[sl], G[sl], hd[sl], pt, nv)[1]
            dl = torch.zeros_like(th0, requires_grad=True); opt = torch.optim.Adam([dl], lr=0.5)
            for _ in range(L):
                th = th0 + dl
                R = rates_c(F[sl], G[sl], hd[sl], torch.cos(th), torch.sin(th), pt, nv, "zf")
                (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward(); opt.step(); opt.zero_grad()
            return th0 + dl.detach()
    elif backend == "torch.jit.trace":
        raise RuntimeError("Adam's step uses torch.optim and autograd inside the loop; torch.jit.trace cannot capture the optimiser update")
    return f


def timeit(f):
    rounds = []
    for _ in range(ROUNDS):
        per = []
        for i in range(NS):
            f(i); f(i)
            t = []
            for _ in range(REPS):
                t0 = time.perf_counter(); f(i); t.append(time.perf_counter() - t0)
            per.append(np.median(t) * 1e3)
        rounds.append(float(np.median(per)))
    return dict(rounds_ms=rounds, median_ms=float(np.median(rounds)))


res = dict(commit=commit(), torch=torch.__version__, cuda_available=torch.cuda.is_available(),
           cpu=open("/proc/cpuinfo").read().split("model name")[1].split("\n")[0].strip(": \t"),
           load_avg=dict(start=load0, before=load1), threads=1, arms={})
for backend in ("eager", "torch.compile", "torch.jit.trace"):
    for L in (1, 8):
        for name, mk in (("Adam", lambda: adam_backend(L, backend)), ("learned", lambda: learned_call(L, backend))):
            key = f"{name}-{L} [{backend}]"
            try:
                f = mk()
                with (torch.no_grad() if (name == "learned" and False) else torch.enable_grad()):
                    res["arms"][key] = timeit(f)
                print(key, res["arms"][key]["median_ms"], flush=True)
            except Exception as e:
                res["arms"][key] = dict(error=f"ÜRETİLEMEDİ: {type(e).__name__}: {str(e)[:300]}")
                print(key, "FAILED", type(e).__name__, flush=True)
res["arms"]["GPU"] = dict(error="ÜRETİLEMEDİ: torch.cuda.is_available() is False on this machine")
res["load_avg"]["after"] = os.getloadavg()[0]
ratios = {}
for backend in ("eager", "torch.compile", "torch.jit.trace"):
    for L in (1, 8):
        a_, l_ = res["arms"].get(f"Adam-{L} [{backend}]", {}), res["arms"].get(f"learned-{L} [{backend}]", {})
        if "median_ms" in a_ and "median_ms" in l_:
            ratios[f"{backend} L={L}"] = l_["median_ms"] / a_["median_ms"]
res["learned_over_adam"] = ratios
json.dump(res, open(OUT / "results.json", "w"), indent=1)
print(json.dumps(ratios, indent=1))
