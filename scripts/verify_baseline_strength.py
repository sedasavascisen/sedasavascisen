"""Is the fixed baseline strong enough? Compare against the lazier method."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 400, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d); pt, nv = 1.0, 1.0/cfg.snr_scale()
def mr(th): return S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf").min(-1).values.mean().item()

print(f"{NS} scenarios, N={N}, T={T}, K={Kus}, max-min [b/s/Hz]\n")
for nm, fn in [("su_average", B.su_average), ("cd", B.coord_descent),
               ("pga (Adam, 3 restarts)", B.pga), ("ao (3 starts + Adam)", B.ao)]:
    t0 = time.time(); R, th = fn(F, G, hd, pt, nv)
    print(f"  {nm:>24}  {S.rate_metrics(R)['min_rate']:7.4f}   ({time.time()-t0:5.1f}s)")

print("\n=== the lazy check: plain Adam from su_average, 400 steps ===")
_, th_su = B.su_average(F, G, hd, pt, nv)
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(400):
    th = th_su + dl
    R = S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf")
    loss = -(-torch.logsumexp(-8.0*R,dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
lazy = mr(th_su + dl.detach())
R_ao, _ = B.ao(F, G, hd, pt, nv)
ao = S.rate_metrics(R_ao)["min_rate"]
print(f"  lazy Adam  {lazy:.4f}    ao  {ao:.4f}")
print(f"  verdict: {'AO is at least as strong -- OK' if ao >= lazy - 0.05 else f'AO STILL WEAK by {lazy-ao:.3f}'}")

print("\n=== longer Adam: has it converged, or does more help? ===")
for iters in (400, 1000, 2000):
    R, _ = B.ao(F, G, hd, pt, nv, pga_iters=iters)
    print(f"  ao with {iters:5d} Adam steps : {S.rate_metrics(R)['min_rate']:7.4f}")
