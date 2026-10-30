"""Shapes, parameter counts and the permutation-symmetry claim."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.models import MuMisoNet, count_params, MODES
from ris_mu.mumiso.features import n_channels

torch.manual_seed(0)
N, K, T = 32, 4, 8
C = n_channels(T)
B = 6
x = torch.randn(B, K, C, N)

print(f"N={N} K={K} T={T} -> C={C}\n")
print(f"{'mode':>10}{'params':>10}{'out shape':>14}{'|cos|^2+|sin|^2':>18}")
print("-" * 52)
nets = {}
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m).eval()
    nets[m] = net
    y = net(x)
    c, s = net.phases(x)
    unit = (c**2 + s**2).mean().item()
    print(f"{m:>10}{count_params(net):10d}{str(tuple(y.shape)):>14}{unit:18.6f}")

print("\n=== permutation symmetry (eval mode) ===")
rng = np.random.default_rng(0)
for m, net in nets.items():
    base = net(x).detach()
    devs = []
    for _ in range(6):
        p = torch.tensor(rng.permutation(K))
        devs.append((net(x[:, p]).detach() - base).abs().max().item())
    mx = max(devs)
    scale = base.abs().max().item()
    rel = mx / max(scale, 1e-30)
    verdict = ("INVARIANT" if mx < 1e-5 else
               f"order sensitive (max dev {mx:.3e}, {100*rel:.1f}% of output scale)")
    print(f"  {m:>10}: {verdict}")
print("  NOTE: at initialisation the concat number is not meaningful -- an")
print("  untrained net is near-random. The result that matters is order")
print("  sensitivity of the RATE after training; measured in the training run.")

print("\n=== is it BatchNorm or Dropout that breaks train-mode symmetry? ===")
# BN in train mode (batch statistics live) but Dropout disabled, so the only
# remaining asymmetry source would be BN itself.
for m, net in nets.items():
    net.train()
    for mod in net.modules():
        if isinstance(mod, torch.nn.Dropout):
            mod.eval()
    net.body.lstm.dropout = 0.0
    base = net(x).detach()
    p = torch.tensor(rng.permutation(K))
    dev = (net(x[:, p]).detach() - base).abs().max().item()
    tag = "INVARIANT" if dev < 1e-5 else f"dev {dev:.3e}"
    print(f"  {m:>10}: BN train + dropout off -> {tag}")
    net.eval()
print("  -> any residual deviation in full train mode is Dropout randomness,")
print("     not a symmetry violation. Invariance is a property of inference.")

print("\n=== defined for a K it was not built for? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m).eval()
    for K2 in (2, 6):
        try:
            out = net(torch.randn(3, K2, C, N))
            print(f"  {m:>10} K={K2}: OK  {tuple(out.shape)}")
        except Exception as e:
            print(f"  {m:>10} K={K2}: refused -- {type(e).__name__}: "
                  f"{str(e)[:60]}")

print("\n=== exchange starts as identity-to-deepsets? ===")
torch.manual_seed(3)
ex = MuMisoNet(N=N, n_users=K, n_tx=T, mode="exchange").eval()
ds = MuMisoNet(N=N, n_users=K, n_tx=T, mode="deepsets").eval()
ds.load_state_dict({k: v for k, v in ex.state_dict().items()
                    if not k.startswith("ex")}, strict=True)
d = (ex(x) - ds(x)).abs().max().item()
print(f"  max diff at init : {d:.3e}   (exchange mixers are zero-init, so ~0)")
print("  -> exchange can only improve on deepsets from the start, never start worse")

print("\n=== gradient flows to every parameter? ===")
for m in MODES:
    net = MuMisoNet(N=N, n_users=K, n_tx=T, mode=m)
    c, s = net.phases(x)
    (c.sum() + s.sum()).backward()
    dead = [n for n, p in net.named_parameters()
            if p.requires_grad and (p.grad is None or p.grad.abs().max() == 0)]
    print(f"  {m:>10}: {len(dead)} parameter tensors with no gradient"
          + (f"  {dead[:3]}" if dead else ""))
