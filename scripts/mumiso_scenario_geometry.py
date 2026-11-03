"""
Dump the geometry of one real scenario of the aging set, for the paper's
scenario figure.

Same construction as mumiso_aging.py (seed 11, 20 scatterers, 400 scenarios,
same time grid), so the figure shows a scenario the results were computed
on, not a sketch. The generator does not return the scatterer positions, so
the random stream is replayed from a saved state: with a fixed BS the first
draw of a chunk is the scatterer set, followed by the user start points,
heights and headings. The replay is checked against the user positions the
generator does return.
"""
import sys
import copy
import json
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel

ap = argparse.ArgumentParser()
ap.add_argument("--index", type=int, default=0)
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"

TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
S = 400

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES,
                      "n_clusters": 20})
gen = MobileMuMisoChannel(panel, cfg)
assert not cfg.bs_random and S <= 500, "replay assumes fixed BS and one chunk"
state = copy.deepcopy(gen.rng.bit_generator.state)
d = gen.generate(S)

rng = np.random.Generator(type(gen.rng.bit_generator)())
rng.bit_generator.state = state
room = np.asarray(cfg.room, float)
scat = rng.uniform([0, 0, 0], room, (S, cfg.n_clusters, 3))
xy0 = rng.uniform([0, 0], room[:2], (S, cfg.n_users, 2))
z0 = rng.uniform(*cfg.user_z, (S, cfg.n_users, 1))
ang = rng.uniform(0, 2 * np.pi, (S, cfg.n_users))
p0 = np.concatenate([xy0, z0], -1)
err = np.abs(p0 - d["ue_t"][:, 0]).max()
assert err < 1e-4, f"replay does not match the generator ({err})"

i = a.index
res = dict(
    source="aging set: seed 11, 20 scatterers, 400 scenarios", index=i,
    replay_max_error_m=float(err),
    room=room.tolist(), fc_hz=float(panel.fc), wavelength_m=float(panel.lam),
    velocity=cfg.velocity, coherence_ms=0.423 / (cfg.velocity * panel.fc / 3e8) * 1e3,
    bs_pos=d["bs_pos"][i].tolist(), bs_array=d["bs_array"][i].tolist(),
    ris_elements=panel.positions.tolist(), ris_normal=list(map(float, panel.normal)),
    users_t0=d["ue_t"][i, 0].tolist(),
    users_t=dict(zip(map(str, TIMES), d["ue_t"][i].tolist())),
    heading_rad=ang[i].tolist(), scatterers=scat[i].tolist(),
    los_ris_bs=bool(d["los_ris_bs"][i]), los_ris_ue=d["los_ris_ue"][i].tolist(),
    los_direct=d["los_direct"][i].tolist(),
    direct_blocked_prob=cfg.direct_blocked_prob,
    direct_blockage_db=cfg.direct_blockage_db)
json.dump(res, open(OUT / "mumiso_scenario_geometry.json", "w"), indent=1)
print(f"replay error {err:.2e} m; wrote results/mumiso_scenario_geometry.json")
print({k: res[k] for k in ("bs_pos", "users_t0", "los_ris_bs", "los_ris_ue", "los_direct")})
