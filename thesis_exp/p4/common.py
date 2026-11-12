"""
Shared pieces for the Prompt 4 experiments (thesis_exp/p4/*). Aging-set construction exactly as
scripts/mumiso_aging.py (make_mumiso_scenario(seed), 20 scatterers, 400 scenarios, ZF precoder,
min-user rate, soft-min Adam with beta = 8). The random stream of the mobile generator does not depend
on the time grid (one blockage draw at the first grid index), so any `times_ms` list gives the SAME
scenarios PROVIDED t = 0 is the first entry (LoS state, K-factor and shadowing are decided from the
positions at index 0); `check_same_scenarios` verifies this against results/mumiso_aging_fixzf.json.
Latencies: thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json (one thread, idle machine).
"""
import json, pathlib, subprocess
import numpy as np, torch
ROOT = pathlib.Path(__file__).resolve().parents[2]
import sys; sys.path.insert(0, str(ROOT))
from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

LAT = json.load(open(ROOT / "thesis_exp/infra/raw/mumiso_mobility_latency_rerun.json"))["median"]
_ML = {int(k[4:]): v for k, v in LAT.items() if k.startswith("adam")}
_LS = sorted(_ML)
def adam_latency(L):
    return float(np.interp(L, _LS, [_ML[x] for x in _LS]))

STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48]


def commit():
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()


class Aging:
    def __init__(self, seed, times, v=1.5, n=400, clusters=20, share_gains=False, scatter_override=None):
        torch.manual_seed(0)
        panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=seed)
        kw = {**base.__dict__, "velocity": v, "times_ms": tuple(times), "n_clusters": clusters}
        self.cfg = MobileConfig(**kw)
        self.gen = MobileMuMisoChannel(panel, self.cfg)
        self.d = self.gen.generate(n)
        self.times = list(times)
        self.F = torch.as_tensor(self.d["F"], dtype=torch.complex64)
        self.G = [torch.as_tensor(self.d["G_t"][:, m], dtype=torch.complex64) for m in range(len(times))]
        self.H = [torch.as_tensor(self.d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(times))]
        self.pt, self.nv, self.n, self.N = 1.0, 1.0 / self.cfg.snr_scale(), n, panel.positions.shape[0]

    def idx(self, t):
        return self.times.index(t)

    def minrate(self, th, m, F=None, G=None, H=None):
        F = self.F if F is None else F; G = self.G[m] if G is None else G; H = self.H[m] if H is None else H
        return S.rates(F, G, H, torch.cos(th), torch.sin(th), self.pt, self.nv, "zf").min(-1).values

    def curve(self, th, grid):
        return torch.stack([self.minrate(th, self.idx(t)) for t in grid], 1).numpy()

    def adam(self, start, L, lr=0.5, F=None, G=None, H=None):
        F = self.F if F is None else F; G = self.G[self.idx(0.0)] if G is None else G; H = self.H[self.idx(0.0)] if H is None else H
        dl = torch.zeros_like(start, requires_grad=True); opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = start + dl
            R = S.rates(F, G, H, torch.cos(th), torch.sin(th), self.pt, self.nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward(); opt.step(); opt.zero_grad()
        return (start + dl).detach()

    def su_average(self, F=None, G=None, H=None):
        m0 = self.idx(0.0)
        return B.su_average(self.F if F is None else F, self.G[m0] if G is None else G, self.H[m0] if H is None else H, self.pt, self.nv)[1]

    def su_best_of(self, F=None, G=None, H=None):
        m0 = self.idx(0.0)
        return B.su_best_of(self.F if F is None else F, self.G[m0] if G is None else G, self.H[m0] if H is None else H, self.pt, self.nv)[1]


def check_same_scenarios(A):
    ref = json.load(open(ROOT / "results/mumiso_aging_fixzf.json"))
    th = A.su_average()
    got = A.minrate(th, A.idx(0.0)).mean().item()
    want = ref["curve"]["su_average"][ref["times_ms"].index(0.0)]
    assert abs(got - want) < 1e-4, (got, want)
    return got


def effective(curve, grid, lat):
    """curve [S, len(grid)] -> per-scenario value interpolated at latency `lat` (ms)."""
    return np.array([np.interp(lat, grid, row) for row in curve])


_rng = np.random.default_rng(0)
def boot(x, n=2000):
    b = [x[_rng.integers(0, len(x), len(x))].mean() for _ in range(n)]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
