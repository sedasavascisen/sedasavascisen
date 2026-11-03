"""
Per-scenario version of the aging table, with bootstrap confidence intervals,
a no-RIS and a random-phase row, and the link budget.

Same construction as mumiso_aging.py (seed 11, 20 scatterers, 400 scenarios,
same time grid), so its scenario means must reproduce
results/mumiso_aging_fixzf.json; that is asserted. Latencies: SU heuristics,
CD and long-run Adam ("pga" in the code) from mumiso_mobility_latency.json,
Adam-L at 13.3/8 ms per step, no-RIS and random phase at 0.
"""
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

RES = pathlib.Path(__file__).resolve().parents[1] / "results"
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
MS_PER_STEP = 13.3 / 8
NBOOT = 2000

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES,
                      "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(400)
N = panel.positions.shape[0]
pt, nv = 1.0, 1.0 / cfg.snr_scale()
F = torch.as_tensor(d["F"], dtype=torch.complex64)
Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(TIMES))]
G0, H0 = Gt[0], Ht[0]


def curve(th):
    return np.stack([S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                             "zf").min(-1).values.numpy() for m in range(len(TIMES))], 1)


def adam_phase(L, start):
    dl = torch.zeros(400, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=0.5)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


_, TH_SU = B.su_average(F, G0, H0, pt, nv)
_, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
torch.manual_seed(0)
phases = {"su_average": TH_SU, "su_best_of": TH_BEST,
          "adam8": adam_phase(8, TH_SU), "adam12": adam_phase(12, TH_SU),
          "adam16": adam_phase(16, TH_SU), "adam20": adam_phase(20, TH_SU)}
_, phases["cd"] = B.coord_descent(F, G0, H0, pt, nv)
_, phases["pga"] = B.pga(F, G0, H0, pt, nv)
_, phases["random"] = B.random_phase(F, G0, H0, pt, nv)

ref = json.load(open(RES / "mumiso_aging_fixzf.json"))
mlat = json.load(open(RES / "mumiso_mobility_latency.json"))["median"]
lat = {k: (MS_PER_STEP * int(k[4:]) if k.startswith("adam") else mlat.get(k, 0.0))
       for k in phases}
lat["random"] = 0.0
rng = np.random.default_rng(0)
idx = rng.integers(0, 400, (NBOOT, 400))


def ci(x):
    m = x[idx].mean(1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


rows = {}
for k, th in phases.items():
    c = curve(th)
    if k in ref["curve"]:
        dev = np.abs(c.mean(0) - np.array(ref["curve"][k])).max()
        assert dev < 1e-4, (k, dev)
    eff = np.array([np.interp(lat[k], TIMES, c[s]) for s in range(400)])
    rows[k] = dict(latency_ms=lat[k], t0=float(c[:, 0].mean()), t0_ci=ci(c[:, 0]),
                   effective=float(eff.mean()), effective_ci=ci(eff),
                   at_Tc=float(c[:, TIMES.index(28.2)].mean()))
    print(f"{k:>11} lat {lat[k]:8.2f}  t0 {rows[k]['t0']:.3f} {rows[k]['t0_ci']}  "
          f"eff {rows[k]['effective']:.3f} {rows[k]['effective_ci']}")

# no RIS: the direct channel alone, static (it ages too, but it is the floor)
R_no = B.no_ris(F, G0, H0, pt, nv)[0].min(-1).values.numpy()
rows["no_ris"] = dict(latency_ms=0.0, t0=float(R_no.mean()), t0_ci=ci(R_no),
                      effective=float(R_no.mean()), effective_ci=ci(R_no), at_Tc=None)
print(f"     no_ris t0 {rows['no_ris']['t0']:.3f} {rows['no_ris']['t0_ci']}")


# link budget: per-user channel gain times P/sigma^2, median over scenarios
def snr_db(He):
    g = (He.abs() ** 2).sum(-1) * pt / nv           # [S, K], all BS antennas
    return float(np.median(10 * np.log10(g.numpy())))


Hd = H0
Hc = S.effective_channel(F, G0, torch.zeros_like(H0), torch.cos(TH_SU), torch.sin(TH_SU))
Ht_su = S.effective_channel(F, G0, H0, torch.cos(TH_SU), torch.sin(TH_SU))
budget = dict(direct_only_db=snr_db(Hd), ris_path_su_average_db=snr_db(Hc),
              total_su_average_db=snr_db(Ht_su))
print("median per-user SNR (sum over BS antennas):", budget)

json.dump(dict(source="aging set (seed 11, 20 scatterers, 400 scenarios)",
               nboot=NBOOT, rows=rows, link_budget=budget),
          open(RES / "mumiso_aging_stats.json", "w"), indent=1)
print("wrote results/mumiso_aging_stats.json")
