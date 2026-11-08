"""
The channel-aging curve: what you lose by not reconfiguring in time.

THE QUESTION
------------
Every latency figure in this package has been compared against a coherence
time computed from a formula. This script replaces the formula with a
measurement: optimise the phase on the channel at t = 0, hold it, and watch
the rate decay as the user walks.

It then does the thing that makes the comparison honest. A method does not
deliver its answer to the channel it was handed -- it delivers it to the
channel that exists when it finishes. So each method's EFFECTIVE rate is
its own phase evaluated at t = its own measured latency. A method that
needs 5.6 seconds is answering a question about a channel from 8 metres ago.

WHERE THIS MODEL IS TRUSTWORTHY, AND WHICH WAY IT ERRS
------------------------------------------------------
The generator holds the scatterer set fixed for the whole window and lets
only the user positions move. Over tens of milliseconds -- a few
centimetres, a fraction of a wavelength -- that is the right model and the
decay is genuine geometry.

Over seconds it is not: a user who has walked 8 metres sees different
scatterers, and this model keeps the same ones. Measured consequence, the
temporal correlation of G floors at about 0.5 instead of decaying to the
0.10 that two independent channels show, and raising the cluster count from
6 to 60 barely moves that floor (0.60 -> 0.51) because the dominant cluster
keeps the channel nearly rank-one inside a fixed subspace.

So the model UNDERSTATES the loss at long horizons. That direction matters:
it means the slow classical methods are being flattered here and still
lose. For them the script also reports the STALE reference -- a t = 0 phase
evaluated on an independent channel -- which is the true asymptote. The
honest reading of a long-latency method is "somewhere between the curve and
the stale reference", and both are printed.
"""
import sys
import pathlib
import json
import argparse
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario, to_torch
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--scenarios", type=int, default=400)
ap.add_argument("--users", type=int, default=4)
ap.add_argument("--tx", type=int, default=8)
ap.add_argument("--velocity", type=float, default=1.5)
ap.add_argument("--clusters", type=int, default=20,
                help="3GPP InH has ~15-19; the static generator's 6 is low")
ap.add_argument("--lr", type=float, default=0.5)
ap.add_argument("--ckpt", default="results/mumiso_unrolled.pt")
ap.add_argument("--tag", default="aging")
ap.add_argument("--no-learned", action="store_true",
                help="skip the learned row; use when the checkpoint was "
                     "trained against a different precoder and evaluating "
                     "it here would be an unfair comparison")
a = ap.parse_args()
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"


def say(*m):
    print(*m, flush=True)


# A fine grid where the model is trustworthy, plus the points the slow
# methods actually land on.
TIMES = (0.0, 1.0, 2.0, 5.0, 7.5, 10.0, 13.3, 15.0, 19.6, 20.0, 26.6, 28.2,
         35.0, 42.9, 50.0, 75.0, 100.0, 150.0, 200.0, 500.0, 1500.0, 5600.0)
TRUST_MS = 200.0          # beyond this the frozen scatterer set shows

# latencies measured by scripts/mumiso_budget_fraction.py on an idle box
LAT = {"su_average": 0.03, "su_best_of": 0.05, "adam8": 13.3, "adam12": 19.6,
       "adam16": 26.6, "adam20": 34.6, "learned8": 42.9,
       "cd": 1500.0, "pga": 5600.0}

torch.manual_seed(0)
panel, base = make_mumiso_scenario(n_users=a.users, n_bs_antennas=a.tx, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": a.velocity,
                      "times_ms": TIMES, "n_clusters": a.clusters})
d = MobileMuMisoChannel(panel, cfg).generate(a.scenarios)
N, T, K = panel.positions.shape[0], a.tx, a.users
M = len(TIMES)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
lam = panel.lam

F = torch.as_tensor(d["F"], dtype=torch.complex64)
Gt = [torch.as_tensor(d["G_t"][:, m], dtype=torch.complex64) for m in range(M)]
Ht = [torch.as_tensor(d["hd_t"][:, m], dtype=torch.complex64) for m in range(M)]
G0, H0 = Gt[0], Ht[0]

say(f"N={N} T={T} K={K}  {a.scenarios} scenarios  v={a.velocity} m/s  "
    f"{a.clusters} clusters")
say(f"coherence time 0.423/f_d = "
    f"{0.423/(a.velocity*panel.fc/3e8)*1e3:.1f} ms;  "
    f"model trusted to {TRUST_MS:.0f} ms\n")


def rate_at(th, m):
    return S.rates(F, Gt[m], Ht[m], torch.cos(th), torch.sin(th), pt, nv,
                   "zf").min(-1).values


def adam_phase(L, start):
    dl = torch.zeros(a.scenarios, N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=a.lr)
    for _ in range(L):
        th = start + dl
        R = S.rates(F, G0, H0, torch.cos(th), torch.sin(th), pt, nv, "zf")
        (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
        opt.step()
        opt.zero_grad()
    return start + dl.detach()


# --------------------------------------------------------------- phases
say("computing each method's phase on the t=0 channel ...")
t0 = time.time()
_, TH_SU = B.su_average(F, G0, H0, pt, nv)
_, TH_BEST = B.su_best_of(F, G0, H0, pt, nv)
phases = {"su_average": TH_SU, "su_best_of": TH_BEST,
          "adam8": adam_phase(8, TH_SU), "adam12": adam_phase(12, TH_SU),
          "adam16": adam_phase(16, TH_SU), "adam20": adam_phase(20, TH_SU)}
if not a.no_learned:
    net = UnrolledMuMiso(N=N, n_users=K, n_tx=T, steps=8, mode="exchange",
                         use_grad=True)
    net.load_state_dict(torch.load(a.ckpt))
    net.eval()
    phi = S.su_align_phase(F, G0, H0)
    X = torch.from_numpy(mumiso_features(d["F"], d["G_t"][:, 0],
                                         d["hd_t"][:, 0], phi.numpy()))
    with torch.no_grad():
        phases["learned8"] = net(X, F, G0, H0, pt, nv, TH_SU)
_, phases["cd"] = B.coord_descent(F, G0, H0, pt, nv)
_, phases["pga"] = B.pga(F, G0, H0, pt, nv)
say(f"  done in {time.time()-t0:.0f}s\n")

# ---------------------------------------------------------- stale floor
# a t=0 phase on an INDEPENDENT channel: the true asymptote of staleness
perm = torch.randperm(a.scenarios, generator=torch.Generator().manual_seed(1))
stale = {k: S.rates(F, G0[perm], H0[perm], torch.cos(v), torch.sin(v), pt, nv,
                    "zf").min(-1).values.mean().item()
         for k, v in phases.items()}

# ----------------------------------------------------------- the curve
say("=== rate of a phase fixed at t=0, as the user walks ===")
hdr = f"{'t [ms]':>8}{'disp [lam]':>11}" + "".join(
    f"{k[:9]:>10}" for k in phases)
say(hdr)
say("-" * len(hdr))
curve = {k: [] for k in phases}
for m in range(M):
    disp = a.velocity * TIMES[m] / 1e3 / lam
    row = f"{TIMES[m]:8.1f}{disp:11.2f}"
    for k, th in phases.items():
        v = rate_at(th, m).mean().item()
        curve[k].append(v)
        row += f"{v:10.3f}"
    say(row + ("" if TIMES[m] <= TRUST_MS else "   <- model optimistic"))

say(f"\n{'stale (independent channel)':>29}" + "".join(
    f"{stale[k]:10.3f}" for k in phases))

# ------------------------------------------------- the effective rate
say("\n=== EFFECTIVE rate: each method's phase at t = its own latency ===")
say(f"{'method':>12}{'t=0 rate':>10}{'latency':>10}{'eff. rate':>11}"
    f"{'kept':>7}{'stale':>9}  note")
say("-" * 76)
eff = {}
for k, th in phases.items():
    lat = LAT[k]
    # interpolate the curve at the method's latency
    v = float(np.interp(lat, TIMES, curve[k]))
    eff[k] = dict(t0=curve[k][0], latency_ms=lat, effective=v,
                  kept=v / curve[k][0], stale=stale[k],
                  trusted=lat <= TRUST_MS)
    note = "" if lat <= TRUST_MS else "model optimistic; true value nearer 'stale'"
    say(f"{k:>12}{curve[k][0]:10.3f}{lat:10.1f}{v:11.3f}"
        f"{v/curve[k][0]:7.2f}{stale[k]:9.3f}  {note}")

best = max((k for k in eff if eff[k]["trusted"]),
           key=lambda k: eff[k]["effective"])
say(f"\n  best effective rate among methods inside the trusted horizon: "
    f"{best}  ({eff[best]['effective']:.3f} b/s/Hz)")
say("  the slow methods' t=0 rates are higher, but they are answers to a")
say("  channel that no longer exists by the time they arrive -- and this")
say("  model flatters them, because it keeps their scatterers alive.")

json.dump(dict(config=vars(a), times_ms=list(TIMES), trust_ms=TRUST_MS,
               curve={k: list(map(float, v)) for k, v in curve.items()},
               stale=stale, effective=eff, latencies=LAT,
               coherence_ms=0.423 / (a.velocity * panel.fc / 3e8) * 1e3),
          open(OUT / f"mumiso_{a.tag}.json", "w"), indent=1)
say(f"\nwrote results/mumiso_{a.tag}.json")
