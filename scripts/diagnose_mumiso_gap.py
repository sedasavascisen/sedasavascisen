"""
Why is the learned model stuck near su_average?

Three questions, in order of what they would imply:
 1. Does the trained net even use its input, or is it emitting a constant?
 2. How far is it from su_average and from AO, as a circular distance?
 3. Is the gap reachable by REWEIGHTING the K alignment vectors? If an
    oracle weighting gets most of AO's rate, the family is right and the
    failure is optimisation. If it does not, beating su_average requires
    leaving that family and the task is harder than the architecture.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch

from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
NS, Kus, T = 400, 4, 8
panel, cfg = make_mumiso_scenario(n_users=Kus, n_bs_antennas=T, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(NS)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)                       # [S,K,N]
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))

def mr(th):
    return S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values

print("=== reference points ===")
_, th_su = B.su_average(F, G, hd, pt, nv)
_, th_ao = B.ao(F, G, hd, pt, nv)
r_su, r_ao = mr(th_su).mean().item(), mr(th_ao).mean().item()
print(f"  su_average {r_su:.4f}   AO {r_ao:.4f}   gap {r_ao-r_su:.4f}")

print("\n=== 1) does the trained concat net use its input? ===")
ck = pathlib.Path("results/mumiso_main_concat.pt")
if ck.exists():
    net = MuMisoNet(N=N, n_users=Kus, n_tx=T, mode="concat")
    net.load_state_dict(torch.load(ck)); net.eval()
    with torch.no_grad():
        c, s = net.phases(X)
    th_net = torch.atan2(s, c)
    r_net = mr(th_net).mean().item()
    # spread of the predicted phase ACROSS scenarios, per element
    circ_var_scen = 1 - torch.exp(1j*th_net.to(torch.complex64)).mean(0).abs()
    circ_var_elem = 1 - torch.exp(1j*th_net.to(torch.complex64)).mean(1).abs()
    print(f"  learned rate {r_net:.4f}")
    print(f"  circular variance across scenarios (per element, mean) "
          f"{circ_var_scen.mean():.4f}   0 = constant output, 1 = uniform")
    print(f"  circular variance across elements  (per scenario, mean) "
          f"{circ_var_elem.mean():.4f}")

    def cdist(a, b):
        return torch.atan2(torch.sin(a-b), torch.cos(a-b)).abs().mean().item()
    print("\n=== 2) circular distance [rad] ===")
    print(f"  net vs su_average {cdist(th_net, th_su):.4f}")
    print(f"  net vs AO         {cdist(th_net, th_ao):.4f}")
    print(f"  su_average vs AO  {cdist(th_su, th_ao):.4f}")
    print("  (uniform random would be ~pi/2 = 1.5708)")
else:
    print("  checkpoint not ready yet")

print("\n=== 3) is the gap reachable by REWEIGHTING the K alignments? ===")
# theta = angle( sum_k w_k exp(j phi_k) ),  w >= 0, optimise w per scenario
w = torch.zeros(NS, Kus, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
ph = torch.exp(1j * phi.to(torch.complex64))           # [S,K,N]
for it in range(400):
    ww = torch.softmax(w, dim=-1).to(torch.complex64)
    acc = (ww.unsqueeze(-1) * ph).sum(1)
    th = torch.angle(acc)
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0*R, dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
with torch.no_grad():
    ww = torch.softmax(w, -1).to(torch.complex64)
    th_w = torch.angle((ww.unsqueeze(-1)*ph).sum(1))
    r_w = mr(th_w).mean().item()
print(f"  ORACLE per-scenario reweighting : {r_w:.4f}")
print(f"  -> recovers {100*(r_w-r_su)/max(r_ao-r_su,1e-9):.1f}% of the "
       f"su_average -> AO gap")

print("\n=== 4) oracle phase SHIFT per element on top of su_average? ===")
# theta = th_su + delta, delta optimised freely per scenario (= PGA from su)
dl = torch.zeros(NS, N, requires_grad=True)
opt = torch.optim.Adam([dl], lr=0.05)
for it in range(400):
    th = th_su + dl
    R = S.rates(F, G, hd, torch.cos(th), torch.sin(th), pt, nv, "zf")
    loss = -(-torch.logsumexp(-8.0*R, dim=-1)/8.0).mean()
    opt.zero_grad(); loss.backward(); opt.step()
with torch.no_grad():
    r_d = mr(th_su + dl).mean().item()
print(f"  free per-element offset (gradient, 400 it) : {r_d:.4f}")
print(f"  -> recovers {100*(r_d-r_su)/max(r_ao-r_su,1e-9):.1f}% of the gap")
print("\n  Reading: if (3) is small but (4) is large, the optimum is NOT a")
print("  reweighting of the single-user alignments -- the network has to")
print("  learn a genuinely different phase pattern, and giving it phi_su as")
print("  a feature anchors it to the wrong family.")
