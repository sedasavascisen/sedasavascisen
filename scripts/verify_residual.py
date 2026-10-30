"""Does the residual model start exactly at su_average, and stay symmetric?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 200, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d); pt, nv = 1.0, 1.0/cfg.snr_scale()
phi = S.su_align_phase(F, G, hd).numpy()
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi))
_, th_su = B.su_average(F, G, hd, pt, nv)
def mr(th): return S.rates(F,G,hd,torch.cos(th),torch.sin(th),pt,nv,"zf").min(-1).values.mean().item()
print(f"su_average reference rate : {mr(th_su):.4f}\n")

print("=== at initialisation the residual model should BE su_average ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True).eval()
    with torch.no_grad(): c, s = net.phases(X)
    th = torch.atan2(s, c)
    dev = torch.atan2(torch.sin(th-th_su), torch.cos(th-th_su)).abs().max().item()
    print(f"  {m:>10}: max circular deviation {dev:.3e}   rate {mr(th):.4f}")

print("\n=== permutation symmetry preserved with the anchor? (eval) ===")
rng = np.random.default_rng(0)
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True).eval()
    # perturb the head so it is not trivially the anchor
    with torch.no_grad():
        for prm in net.head.net[-1].parameters(): prm.add_(torch.randn_like(prm)*0.1)
    with torch.no_grad():
        base = torch.stack(net.phases(X))
        devs = []
        for _ in range(5):
            p = torch.tensor(rng.permutation(Kus))
            devs.append((torch.stack(net.phases(X[:, p])) - base).abs().max().item())
    mx = max(devs)
    print(f"  {m:>10}: {'INVARIANT' if mx<1e-5 else f'dev {mx:.3e}'}")

print("\n=== gradients finite at the zero-init singular point? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode=m, residual=True)
    c, s = net.phases(X[:16])
    R = S.rates(F[:16],G[:16],hd[:16],c,s,pt,nv,"zf")
    S.maxmin_loss(R).backward()
    bad = [n for n,prm in net.named_parameters()
           if prm.grad is not None and not torch.isfinite(prm.grad).all()]
    nz = sum(1 for n,prm in net.named_parameters()
             if prm.grad is not None and prm.grad.abs().max()>0)
    tot = sum(1 for _ in net.parameters())
    print(f"  {m:>10}: non-finite grads {len(bad)}   params with gradient {nz}/{tot}")
