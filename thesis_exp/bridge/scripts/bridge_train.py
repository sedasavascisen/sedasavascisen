"""
Bridge task, part 1: train the one-shot phase-aware network (MuMisoNet: per-element (cos, sin), projected
onto the unit circle) WITHOUT labels on the soft-min surrogate (beta = 8), as in the thesis
(ris_mu/mumiso/train.py: Adam 2e-3, lr halved at 60 % and 85 % of the epochs, batch 64, grad clip 1,
checkpoint = best VALIDATION min-rate).

Training data (approved option (ii), 11 Nov 2026): a static set built with the AGING construction
(MobileMuMisoChannel, 20 scatterers, t = 0 snapshot, make_mumiso_scenario(seed=--data_seed)), 6000 samples,
split_indices(6000, seed=0) -> 4200 / 900 / 900. --static_paper uses instead the paper's static set
(MuMisoChannel default, 6 scatterers, seed 11) as the secondary, out-of-distribution arm.

Configurations: --residual {1,0} (rotation around SU-average vs direct projection) x --link_ratio {0,1}
(features.link_ratio). Mode 'exchange' (the learned update rule's mode in the paper).
Output: thesis_exp/bridge/raw/train/<tag>.json + .pt
"""
import sys, json, time, argparse, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.models import MuMisoNet, count_params
from ris_mu.mumiso import system as S
from ris_mu.mumiso.train import train_model, evaluate
from ris_mu.features import split_indices

ap = argparse.ArgumentParser()
ap.add_argument("--residual", type=int, default=1)
ap.add_argument("--link_ratio", type=int, default=0)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--epochs", type=int, default=12)
ap.add_argument("--samples", type=int, default=6000)
ap.add_argument("--data_seed", type=int, default=2027)
ap.add_argument("--static_paper", action="store_true")
ap.add_argument("--threads", type=int, default=2)
a, _ = ap.parse_known_args()
torch.set_num_threads(a.threads)
OUT = ROOT / "thesis_exp/bridge/raw/train"; OUT.mkdir(parents=True, exist_ok=True)
tag = f"net_res{a.residual}_lr{a.link_ratio}_s{a.seed}" + ("_staticpaper" if a.static_paper else "")


def build(static_paper, data_seed, samples):
    torch.manual_seed(0)
    if static_paper:
        panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
        d = MuMisoChannel(panel, cfg).generate(samples)
    else:
        panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=data_seed)
        cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,), "n_clusters": 20})
        d = MobileMuMisoChannel(panel, cfg).generate(samples)
        d = dict(d, G=d["G_t"][:, 0], hd=d["hd_t"][:, 0])
    return panel, cfg, d


if __name__ == "__main__":
    panel, cfg, d = build(a.static_paper, a.data_seed, a.samples)
    F, G, hd, _ = to_torch(dict(F=d["F"], G=d["G"], hd=d["hd"]))
    pt, nv = 1.0, 1.0 / cfg.snr_scale()
    phi = S.su_align_phase(F, G, hd).numpy()
    X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi, link_ratio=bool(a.link_ratio)))
    tr, va, te = split_indices(a.samples, seed=0)
    torch.manual_seed(a.seed)
    net = MuMisoNet(N=panel.positions.shape[0], n_users=4, n_tx=8, mode="exchange",
                    residual=bool(a.residual), link_ratio=bool(a.link_ratio))
    t0 = time.time()
    net, hist = train_model(net, X, F, G, hd, pt, nv, (tr, va, te), epochs=a.epochs, seed=a.seed)
    v_min, v_sum = evaluate(net, X, F, G, hd, pt, nv, va)
    t_min, t_sum = evaluate(net, X, F, G, hd, pt, nv, te)
    from ris_mu.mumiso import baselines as B
    anchor_val = S.rate_metrics(B.su_average(F[va], G[va], hd[va], pt, nv)[0])["min_rate"]
    res = dict(tag=tag, config=vars(a), commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
               params=count_params(net), val_min=v_min, test_min=t_min, val_su_average=anchor_val,
               train_minutes=(time.time() - t0) / 60, history=hist)
    torch.save(dict(state=net.state_dict(), residual=bool(a.residual), link_ratio=bool(a.link_ratio)), OUT / f"{tag}.pt")
    json.dump(res, open(OUT / f"{tag}.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "history"}, indent=1))
