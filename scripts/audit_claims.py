"""
audit_claims.py -- every load-bearing number in README_MUMISO.md, frozen
and re-checkable by machine.

WHY THIS FILE EXISTS
--------------------
Three times in this project a stated number turned out to be wrong: a table
whose rows came from two different antenna counts, a baseline that was
weaker than claimed, and a "strongest classical method" that was not the
strongest. Each was caught by someone deciding to look again. That is not a
process, it is luck.

So the claims live here as code. Each one recomputes its value from the
library -- not by parsing a script's printout, which rots the moment the
printing changes -- and compares against the value frozen in the report.
Run it after any change to the package:

    python3 -I scripts/audit_claims.py            # fast tiers only
    python3 -I scripts/audit_claims.py --all      # includes slow tiers

TIERS, because not every number deserves the same tolerance
-----------------------------------------------------------
  exact        mathematical identities. A drift here is a bug. rtol 1e-6.
  statistical  rates and ranks measured over scenarios. Seeded, so
               reproducible, but a tolerance wide enough to survive a torch
               version bump. rtol 5e-2.
  timing       wall-clock. NOT asserted -- machine-dependent and noisy
               (16-step Adam measured 23.7, 24.2, 26.0 and 29.4 ms across
               runs on the same box). Reported, and only the ORDERING and
               the budget fraction are checked, because those are what the
               argument rests on.

If a claim here disagrees with the report, the report is what is wrong
until proven otherwise.
"""
import sys
import pathlib
import argparse
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, effective_rank, neighbour_corr)
from ris_mu.mumiso.features import mumiso_features, n_channels
from ris_mu.mumiso.models import MuMisoNet, MODES
from ris_mu.mumiso import system as S, baselines as B

ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true", help="include slow tiers")
ap.add_argument("--only", default=None, help="substring filter on claim id")
a = ap.parse_args()

RESULTS = []


def claim(cid, section, tier, claimed, measured, note="", at_most=None):
    """
    Two kinds of claim, and conflating them is what made this file's first
    run produce three false alarms:

      VALUE claims ("the rate is 3.6688"). Checked within the tier's
      relative tolerance. The exact tier uses 1e-3, not something tighter,
      because the report quotes these to four decimals -- asserting to 1e-6
      against a four-decimal quote fails on the rounding, which is the
      report's precision, not an error.

      THRESHOLD claims ("the leakage is negligible", "the gradient matches
      finite differences"). These have no true value to hit: finite
      differences cannot do better than ~1e-8, and the residual model is
      deliberately a hair off the anchor so that gradients reach the body.
      Pass `at_most=` for these.
    """
    tol = {"exact": 1e-3, "statistical": 5e-2, "timing": None}[tier]
    if at_most is not None:
        ok = abs(measured) <= at_most
        shown = f"<={at_most:.3g}"
    elif tol is None:
        ok = None
        shown = "-"
    else:
        ok = abs(measured - claimed) / max(abs(claimed), 1e-30) <= tol
        shown = f"{claimed:.4g}"
    RESULTS.append(dict(id=cid, section=section, tier=tier, claimed=claimed,
                        measured=measured, ok=ok, note=note, at_most=at_most))
    tag = {True: "PASS", False: "FAIL", None: "info"}[ok]
    print(f"  [{tag}] {cid:<28} §{section:<4} target {shown:>11}  "
          f"measured {measured:10.4g}  {note}", flush=True)


def section(name):
    print(f"\n=== {name} ===", flush=True)


# ----------------------------------------------------------------- exact
section("exact: mathematical identities")
torch.manual_seed(0)
rng = np.random.default_rng(0)


def cn(*s):
    return (rng.normal(size=s) + 1j * rng.normal(size=s)) / np.sqrt(2)


# single-user reduction: general form vs the published Eq. (8)
Nn = 32
F1, G1, H1 = cn(1, Nn, 1), cn(1, 1, Nn), cn(1, 1, 1)
tF, tG, tH = (torch.tensor(x) for x in (F1, G1, H1))
acas = G1[0, 0] * F1[0, :, 0]
bound = (abs(H1[0, 0, 0]) + np.abs(acas).sum()) ** 2


def gain(th):
    c = torch.tensor(np.cos(th))[None]
    s = torch.tensor(np.sin(th))[None]
    return S.effective_channel(tF, tG, tH, c, s).abs().item() ** 2


claim("su_general_over_bound", "7", "exact", 1.0000,
      gain(S.su_align_phase(tF, tG, tH)[0, 0].numpy()) / bound)
claim("su_eq8_over_bound", "7", "exact", 0.8977,
      gain(-np.angle(acas)) / bound, "published Eq. (8), h_d=0 special case")

# ZF: nulls interference, respects the power constraint
Bn, Nn, T, K = 4, 32, 8, 4
F2, G2, H2 = cn(Bn, Nn, T), cn(Bn, K, Nn), cn(Bn, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F2, G2, H2))
th = torch.tensor(rng.uniform(-np.pi, np.pi, (Bn, Nn)))
He = S.effective_channel(tF, tG, tH, torch.cos(th), torch.sin(th))
A = (He @ S.zf(He, 1.0)).abs() ** 2
off = A - torch.diag_embed(torch.diagonal(A, dim1=-2, dim2=-1))
claim("zf_leakage", "7", "exact", 0.0, off.abs().max().item(),
      "inter-user interference", at_most=1e-15)
claim("zf_power", "7", "exact", 1.0,
      (S.zf(He, 1.0).abs() ** 2).sum((-1, -2)).mean().item(), "||W||_F^2 = Pt")
claim("mrt_power", "7", "exact", 1.0,
      (S.mrt(He, 1.0).abs() ** 2).sum((-1, -2)).mean().item(), "||W||_F^2 = Pt")

# rate gradient against finite differences
Bn, Nn, T, K = 2, 16, 4, 3
F3, G3, H3 = cn(Bn, Nn, T), cn(Bn, K, Nn), cn(Bn, K, T)
tF, tG, tH = (torch.tensor(x) for x in (F3, G3, H3))
th0 = rng.uniform(-np.pi, np.pi, (Bn, Nn))


def obj(t, grad=False):
    tt = torch.tensor(t, requires_grad=grad)
    R = S.rates(tF, tG, tH, torch.cos(tt), torch.sin(tt), 1.0, 1e-3)
    return R.min(-1).values.sum(), tt


v, tt = obj(th0, True)
v.backward()
g_auto = tt.grad.numpy().copy()
eps = 1e-6
g_fd = np.zeros_like(th0)
for b in range(Bn):
    for n in range(Nn):
        tp = th0.copy(); tp[b, n] += eps
        tm = th0.copy(); tm[b, n] -= eps
        g_fd[b, n] = (obj(tp)[0].item() - obj(tm)[0].item()) / (2 * eps)
claim("grad_vs_fd_relative", "7", "exact", 0.0,
      np.abs(g_auto - g_fd).max() / np.abs(g_fd).max(),
      "autograd vs finite diff; fd cannot do better than ~1e-8",
      at_most=1e-5)

# raw network output is scale invariant after unit_phase
gsc = torch.tensor(rng.uniform(0.2, 5.0, (Bn, Nn)))
c0, s0 = torch.tensor(np.cos(th0)), torch.tensor(np.sin(th0))
R1 = S.rates(tF, tG, tH, *S.unit_phase(c0, s0), 1.0, 1e-3)
R2 = S.rates(tF, tG, tH, *S.unit_phase(gsc * c0, gsc * s0), 1.0, 1e-3)
claim("scale_invariance", "7", "exact", 0.0, (R1 - R2).abs().max().item(),
      at_most=1e-9)

# straight-through quantiser: value on the grid, gradient equal to one
for bits in (1, 2, 3):
    cc = torch.tensor(np.cos(th0), requires_grad=True)
    ss = torch.tensor(np.sin(th0), requires_grad=True)
    cq, sq = S.quantise_ste(cc, ss, bits)
    step = 2 * np.pi / (2 ** bits)
    tq = torch.atan2(sq, cq).detach().numpy()
    claim(f"ste_{bits}bit_on_grid", "7", "exact", 0.0,
          float(np.abs(tq / step - np.round(tq / step)).max()), at_most=1e-12)
    # d theta_q / d theta must be 1, not 0: perturb theta and watch theta_q
    th_t = torch.tensor(th0, requires_grad=True)
    cq, sq = S.quantise_ste(torch.cos(th_t), torch.sin(th_t), bits)
    torch.atan2(sq, cq).sum().backward()
    claim(f"ste_{bits}bit_gradient_is_one", "7", "exact", 1.0,
          th_t.grad.abs().mean().item(), "straight-through, not zero")

# permutation symmetry at inference
C = n_channels(8)
X = torch.randn(6, 4, C, 32)
for mode in MODES:
    net = MuMisoNet(N=32, n_users=4, n_tx=8, mode=mode).eval()
    base = net(X).detach()
    dev = max((net(X[:, torch.tensor(rng.permutation(4))]).detach()
               - base).abs().max().item() for _ in range(6))
    if mode == "concat":
        # At initialisation an untrained net is near-random, so this number
        # is not the real test. The real one is post-training, on the RATE:
        # measured 1.67e-02 (residual) and 2.46e-02 (absolute) for concat
        # against 2.46e-06 for deepsets. See the run logs in results/.
        claim("perm_concat_is_sensitive", "7", "timing", 0.0, dev,
              "at init; real test is post-training on the rate")
    else:
        claim(f"perm_{mode}_invariant", "7", "exact", 0.0, dev, at_most=1e-5)

# residual mode starts at the anchor
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(200)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
Xs = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
_, th_su = B.su_average(F, G, hd, pt, nv)
net = MuMisoNet(N=N, n_users=4, n_tx=8, mode="exchange", residual=True).eval()
with torch.no_grad():
    c, s = net.phases(Xs)
dev = torch.atan2(torch.sin(torch.atan2(s, c) - th_su),
                  torch.cos(torch.atan2(s, c) - th_su)).abs().max().item()
claim("residual_starts_at_anchor", "7", "exact", 0.0, dev,
      "radians; deliberately a hair off so gradients reach the body",
      at_most=2e-3)

# ----------------------------------------------------- statistical (fast)
section("statistical: channel diagnostics (1000 scenarios, N=32 T=8 K=4)")
d2 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                         seed=11)).generate(1000)
Gv = d2["G"].reshape(-1, N)
Ft = d2["F"].transpose(0, 2, 1).reshape(-1, 8)
claim("g_rank_pooled_1000", "6", "statistical", 15.73, effective_rank(Gv))
claim("g_rank_user0_1000", "6", "statistical", 15.58,
      effective_rank(d2["G"][:, 0]))
claim("f_rank_ant0_1000", "6", "statistical", 13.46,
      effective_rank(d2["F"][:, :, 0]))
claim("g_neigh_corr_1000", "6", "statistical", 0.5716, neighbour_corr(Gv))
claim("ant_neigh_corr_1000", "6", "statistical", 0.7401, neighbour_corr(Ft))
claim("ant_rank_1000", "6", "statistical", 4.00, effective_rank(Ft))
claim("los_frac_bs_ris", "6", "statistical", 0.383,
      float(d2["los_ris_bs"].mean()))

section("statistical: effective rank vs sample count (§6 caveat)")
# The previous version of this check computed effective_rank on
# d2["G"][:min(Sn, 1000)], so its 4000 and 8000 rows silently reused the
# first 1000 scenarios and the test could never fail. An independent audit
# caught it. It also found the report's stated DIRECTION is wrong: the
# estimator is not monotone upward -- 250 scenarios gives a HIGHER value
# than 1000. So what is checked here is the honest claim: the estimate
# moves by more than a few percent with sample count, therefore an absolute
# value must never be quoted without the count.
d_big = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                            seed=11)).generate(
    16000 if a.all else 4000)
ranks = {}
for Sn in (250, 1000, 4000) + ((16000,) if a.all else ()):
    ranks[Sn] = effective_rank(d_big["G"][:Sn].reshape(-1, N))
    claim(f"rank_at_{Sn}", "6", "timing", 0.0, ranks[Sn],
          f"{Sn} scenarios")
spread = (max(ranks.values()) - min(ranks.values())) / min(ranks.values())
claim("rank_estimate_is_count_dependent", "6", "exact", 1.0,
      1.0 if spread > 0.05 else 0.0,
      f"spread {100*spread:.0f}% across counts -> never quote without n")
claim("rank_is_not_monotone_up", "6", "exact", 1.0,
      1.0 if ranks[250] > ranks[1000] else 0.0,
      "report's 'drifts upward' is wrong at the low end")

# ------------------------------------------------------- statistical slow
if a.all:
    section("statistical: baselines and the frontier ordering (slow)")
    d3 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                             seed=11)).generate(600)
    F3, G3, H3, _ = to_torch(d3)
    ev = slice(0, 450)
    _, TH0 = B.su_average(F3, G3, H3, pt, nv)

    def rate_of(th):
        return S.rates(F3[ev], G3[ev], H3[ev], torch.cos(th), torch.sin(th),
                       pt, nv, "zf").min(-1).values.mean().item()

    def adam_phase(L, lr=0.5):
        dl = torch.zeros(450, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=lr)
        for _ in range(L):
            th = TH0[ev] + dl
            R = S.rates(F3[ev], G3[ev], H3[ev], torch.cos(th), torch.sin(th),
                        pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        return TH0[ev] + dl.detach()

    claim("su_average_rate", "5", "statistical", 3.664, rate_of(TH0[ev]))
    claim("adam8_rate", "5", "statistical", 5.378, rate_of(adam_phase(8)))
    claim("adam16_rate", "5", "statistical", 5.743, rate_of(adam_phase(16)))
    claim("adam32_rate", "5", "statistical", 6.015, rate_of(adam_phase(32)))
    q_cd = S.rate_metrics(B.coord_descent(F3[ev], G3[ev], H3[ev], pt,
                                          nv)[0])["min_rate"]
    q_pga = S.rate_metrics(B.pga(F3[ev], G3[ev], H3[ev], pt,
                                 nv)[0])["min_rate"]
    q_ao = S.rate_metrics(B.ao(F3[ev], G3[ev], H3[ev], pt, nv)[0])["min_rate"]
    claim("cd_rate", "5", "statistical", 5.910, q_cd)
    claim("pga_rate", "5", "statistical", 6.202, q_pga)
    claim("ao_rate", "5", "statistical", 6.201, q_ao)
    claim("pga_beats_ao", "5", "exact", 1.0, 1.0 if q_pga >= q_ao else 0.0,
          "report says PGA is the strongest, not AO")
    claim("cd_dominated_by_adam32", "5", "exact", 1.0,
          1.0 if rate_of(adam_phase(32)) > q_cd else 0.0,
          "report says coordinate descent is dominated")

    # The latency table in the report comes from a DIFFERENT sample (400
    # scenarios, mumiso_budget_fraction.py) than the frontier rows above
    # (450, mumiso_frontier.py), and the min-rate mean moves about 6% at
    # this n. Both are frozen here so that quoting one while measuring the
    # other shows up as a failure instead of as a puzzling 6% drift.
    section("statistical: the OTHER sample the latency table uses (400)")
    d4 = MuMisoChannel(*make_mumiso_scenario(n_users=4, n_bs_antennas=8,
                                             seed=11)).generate(400)
    F4, G4, H4, _ = to_torch(d4)
    _, T4 = B.su_average(F4, G4, H4, pt, nv)
    _, T4b = B.su_best_of(F4, G4, H4, pt, nv)

    def rate4(th):
        return S.rates(F4, G4, H4, torch.cos(th), torch.sin(th), pt, nv,
                       "zf").min(-1).values.mean().item()

    def adam4(L, start):
        dl = torch.zeros(400, N, requires_grad=True)
        opt = torch.optim.Adam([dl], lr=0.5)
        for _ in range(L):
            t = start + dl
            R = S.rates(F4, G4, H4, torch.cos(t), torch.sin(t), pt, nv, "zf")
            (-(-torch.logsumexp(-8.0 * R, -1) / 8.0).mean()).backward()
            opt.step()
            opt.zero_grad()
        return start + dl.detach()

    claim("bf_su_average", "5", "statistical", 3.765, rate4(T4))
    claim("bf_su_best_of", "5", "statistical", 4.417, rate4(T4b))
    claim("bf_adam8", "5", "statistical", 5.569, rate4(adam4(8, T4)))
    claim("bf_adam12", "5", "statistical", 5.775, rate4(adam4(12, T4)))
    claim("bf_adam16", "5", "statistical", 5.934, rate4(adam4(16, T4)))
    # The audit found su_average to be a weak anchor and measured the fix
    # at +48%. With the precoder bug fixed that drops to +17% -- the finding
    # is real but much smaller, and the threshold here records the measured
    # value rather than the one from the broken configuration.
    claim("su_best_of_gain_over_average", "5", "statistical", 1.173,
          rate4(T4b) / rate4(T4), "anchor fix, properly precoded")

# --------------------------------------------------- sec4 / unrolled claims
# WHY THESE EXIST
# ---------------
# Everything above re-measures something. The numbers behind Bulgu 1 and
# Bulgu 2 come from training runs that take ~15-45 min each, so an audit
# cannot reproduce them. What it CAN do is pin the saved results to the
# claims the report makes about them -- which is exactly the failure mode
# this project already hit once: the report quoted the UNROLLED model's
# 3.50 -> 5.64 as evidence about the ONE-SHOT models. A number lifted from
# the wrong file reads perfectly plausible. These checks make that specific
# mistake fail loudly.
#
# KNOWN GAP, stated rather than papered over: the anchor on the models' own
# 1800-scenario test split (su_average 3.5363, su_best_of 4.1730) is the
# denominator of every Bulgu 1 ratio in the report, and it is NOT re-measured
# here -- doing so means regenerating all 12000 scenarios. It is measured by
# scripts/anchor_same_split.py and read from results/anchor_full_test.json.
# So a regression in the SU baselines would not fail this section; it would
# fail the §5 statistical tier above, which does re-measure them on its own
# sample. That is weaker than checking the same split, and worth closing.
section("saved results: Bulgu 1 and Bulgu 2 (consistency, not re-measurement)")

import json as _json

_RES = pathlib.Path(__file__).resolve().parents[1] / "results"


def _load(name):
    p = _RES / name
    return _json.loads(p.read_text()) if p.exists() else None


_s4 = _load("mumiso_sec4_fixzf.json")
_un = _load("mumiso_unrolled_fixzf.json")
_ng = _load("mumiso_nograd_fixzf.json")

if _s4 is None or _un is None or _ng is None:
    print("  [skip] one of the fixzf result files is missing -- rerun "
          "mumiso_run.py / mumiso_unrolled.py with --tag *_fixzf")
else:
    # --- Bulgu 1: the three one-shot models sit ON the anchor -------------
    for _m, _v in (("concat", 3.536795), ("deepsets", 3.536696),
                   ("exchange", 3.526039)):
        claim(f"sec4_{_m}_test_min", "4", "statistical", _v,
              _s4["models"][_m]["test_min"], "from mumiso_sec4_fixzf.json")
    claim("sec4_target_is_pga", "4", "exact", 1,
          int(_s4["target"]["method"] == "pga"),
          "the number to beat is PGA, chosen by measurement")
    claim("sec4_target_rate", "4", "statistical", 6.078346,
          _s4["target"]["rate"])
    # The spread ACROSS architectures is the real claim of Bulgu 1: the
    # choice of architecture does not matter. Asserting it as a bound means
    # a future run that separates them will fail here instead of quietly
    # contradicting the report.
    _mins = [_s4["models"][k]["test_min"] for k in ("concat", "deepsets",
                                                    "exchange")]
    claim("sec4_architecture_spread_tiny", "4", "statistical",
          0.0, (max(_mins) - min(_mins)) / max(_mins),
          "architecture choice changes nothing", at_most=0.01)

    # --- Bulgu 2: the gradient input is what matters ---------------------
    claim("unrolled_anchor", "4", "statistical", 3.5758257, _un["anchor"])
    claim("unrolled_with_grad", "4", "statistical", 5.6359273,
          _un["test_min"], "gradient given as input")
    claim("unrolled_without_grad", "4", "statistical", 3.6160022,
          _ng["test_min"], "same model, gradient withheld")
    claim("unrolled_grad_is_on", "4", "exact", 1,
          int(bool(_un["config"]["use_grad"])))
    claim("unrolled_nograd_is_off", "4", "exact", 0,
          int(bool(_ng["config"]["use_grad"])))
    # Same anchor for both arms, or the comparison means nothing.
    claim("ablation_shares_anchor", "4", "exact", 0.0,
          abs(_un["anchor"] - _ng["anchor"]), "both arms, one anchor",
          at_most=1e-6)
    # Nor may it be a capacity difference.
    claim("ablation_capacity_matched", "4", "statistical", 0.0,
          abs(_un["params"] - _ng["params"]) / _un["params"],
          "parameter counts within 1%", at_most=0.01)
    # The finding itself, as a ratio so it survives a change of scale.
    # `claim` only bounds from ABOVE, so the "gradient buys >10x" claim is
    # written as its reciprocal <= 0.1. Writing it the natural way round
    # with a huge at_most would assert nothing at all -- the exact kind of
    # toothless threshold this audit exists to catch.
    claim("nograd_gain_is_under_a_tenth", "4", "statistical", 0.0,
          (_ng["test_min"] / _ng["anchor"] - 1.0)
          / (_un["test_min"] / _un["anchor"] - 1.0),
          "gradient input buys >10x the anchor-relative gain", at_most=0.1)
    claim("nograd_barely_moves", "4", "statistical", 0.0,
          _ng["test_min"] / _ng["anchor"] - 1.0,
          "without the gradient the model stays at the anchor",
          at_most=0.05)
    # And the guard against the mistake that actually happened: the
    # one-shot models must NOT be credited with the unrolled model's rate.
    claim("bulgu1_not_bulgu2", "4", "exact", 1,
          int(max(_mins) < 0.75 * _un["test_min"]),
          "one-shot models are nowhere near the unrolled model")

# ------------------------------------------------------ SU-MISO CNN-LSTM
# The published phase-aware CNN-LSTM ported to single-user mobility MISO
# (scripts/sumiso_mobility_eval.py) and under imperfect CSI
# (scripts/sumiso_csi_eval.py). Consistency of the saved results; the
# verdicts are written as 0/1 so that swapping two numbers flips them.
section("saved results: published CNN-LSTM, single-user MISO")
_me = _load("sumiso_mobility_eval.json")
_ce = _load("sumiso_csi_eval.json")
if _me is None or _ce is None:
    print("  [skip] sumiso_mobility_eval.json or sumiso_csi_eval.json missing")
else:
    claim("su_cnn_rate_t0", "8", "exact", 12.3554, _me["rate_t0"]["CNN-LSTM"])
    claim("su_align_rate_t0", "8", "exact", 12.3892, _me["rate_t0"]["SU-align"])
    # Corrected 2026-11-05 (independent audit): the network is NOT below
    # closed-form alignment -- not significant on the 400 set, slightly ABOVE
    # it on 6000-scenario draws. What holds is dominance by one Adam step.
    _rb = _load("sumiso_t0_robustness.json")
    _p0 = _me["paired_t0"]
    claim("su_cnn_vs_align_t0_not_significant", "8", "exact", 1,
          int(_p0["CNN-LSTM - SU-align"][1] < 0 < _p0["CNN-LSTM - SU-align"][2]),
          "400 set: CI of CNN - SU-align contains zero")
    claim("su_cnn_above_align_large_draws", "8", "exact", 1,
          int(_rb is not None and all(v["cnn_minus_su_align"]["ci95"][0] > 0 for v in _rb["draws"].values())),
          "6000-scenario draws (seeds 11, 13): CNN slightly above SU-align")
    claim("su_cnn_dominated_by_adam1", "8", "exact", 1,
          int(_me["latency_ms"]["Adam-1"] < _me["latency_ms"]["CNN-LSTM"]
              and _p0["CNN-LSTM - Adam-1"][2] < 0
              and _rb is not None and all(v["cnn_minus_adam1"]["ci95"][1] < 0 for v in _rb["draws"].values())),
          "one Adam step is faster and significantly better, on all three draws")
    claim("su_timing_started_idle", "8", "exact", 1,
          int(_me["load_avg"]["before_timing"] < 0.5),
          "latency timing began below load 0.5")
    _lc = _load("sumiso_label_check.json")
    if _lc is not None:
        claim("su_label_vs_long_adam", "8", "statistical", 0.0, _lc["max_adam_minus_label"],
              "3-start 1000-step Adam beats a CD label by at most this (300 scenarios)", at_most=0.01)
    claim("su_cnn_cd1_below_cd1_all_tov", "8", "exact", 1,   # effective rates, i.e. with latency
          int(all(v["CNN-LSTM+CD-1"]["effective"] < v["CD-1"]["effective"]
                  for v in _me["effective"].values())),
          "the network is a worse start for one CD sweep than alignment")
    claim("su_classical_best_all_tov", "8", "exact", 1,
          int(all(v["_best"].startswith("CD-") for v in _me["effective"].values())),
          "best arm at every acquisition delay is coordinate ascent")
    _lv = _ce["levels"]
    claim("csi_levels", "8", "exact", 5, len(_lv), "five error levels")
    claim("csi_b_below_classical_static", "8", "exact", 1,
          int(all(v["static"]["b_minus_best_classical_ci"][1] < 0 for v in _lv.values())),
          "noise-trained model below tuned classical at every e2 (CI)")
    claim("csi_bcd1_below_classical_static", "8", "exact", 1,
          int(all(v["static"]["bcd_minus_best_classical_ci"][1] < 0 for v in _lv.values())),
          "network + 1 sweep below tuned classical at every e2 (CI)")
    claim("csi_b_dominated_mobility", "8", "exact", 1,
          int(all(len(v["mobility"]["dominated_by[CNN (b) noise-trained]"]) > 0 for v in _lv.values())),
          "a faster classical arm with higher effective rate exists at every e2")
    claim("csi_b_below_classical_mobility", "8", "exact", 1,
          int(all(v["mobility"]["b_minus_best_classical_ci"][1] < 0 for v in _lv.values())))
    claim("csi_no_early_stopping_gain", "8", "exact", 1,
          int(all(v["static"]["classical_selected_on_val"] in ("Adam-64", "CD-30", "CD-10")
                  for v in _lv.values())),
          "under CSI error the selected classical arm is still a converged one")
    claim("csi_b_minus_best_e2_0.3", "8", "exact", -0.6490,
          _lv["0.3"]["static"]["b_minus_best_classical"])

# --------------------------------------- representation ablation (sin/cos)
# scripts/sumiso_representation_summary.py: same network, sin/cos output
# (published) vs direct angle with MSE vs direct angle with 1 - cos loss,
# SISO and MISO, 3 seeds each.
section("saved results: phase representation ablation")
_rp = _load("sumiso_representation.json")
if _rp is None or _ce is None:
    print("  [skip] sumiso_representation.json or sumiso_csi_eval.json missing")
else:
    claim("rep_siso_sincos_rmse", "8", "statistical", 14.63, _rp["siso"]["sincos"]["rmse"]["mean"])
    claim("rep_miso_sincos_rmse", "8", "statistical", 61.49, _rp["miso"]["sincos"]["rmse"]["mean"])
    for _sc in ("siso", "miso"):
        claim(f"rep_{_sc}_sincos_best_every_seed", "8", "exact", 1,
              int(_rp[_sc]["sincos_better_than_angle_mse_all_seeds"]
                  and _rp[_sc]["sincos_better_than_angle_circ_all_seeds"]),
              "sin/cos has the lowest RMSE in each of the 3 seeds")
    claim("rep_siso_loss_is_at_the_wrap", "8", "exact", 1,
          int(_rp["siso"]["angle_mse"]["rmse_near_wrap"]["mean"] > 3 * _rp["siso"]["sincos"]["rmse_near_wrap"]["mean"]
              and _rp["siso"]["angle_mse"]["rmse_far_from_wrap"]["mean"] < 1.2 * _rp["siso"]["sincos"]["rmse_far_from_wrap"]["mean"]),
          "direct-angle MSE fails near +-pi, not elsewhere")
    claim("rep_miso_sincos_still_below_cd1", "8", "exact", 1,
          int(_rp["miso"]["sincos"]["rate"]["mean"] < _ce["levels"]["0.0"]["static"]["test"]["CD-1"]),
          "the better representation does not close the gap to one CD sweep")

# ------------------------------------------------ discrete phase (1/2/3 bit)
section("saved results: discrete phases, single-user MISO")
_dp = _load("sumiso_discrete_eval.json")
if _dp is None:
    print("  [skip] sumiso_discrete_eval.json missing")
else:
    _lv = _dp["levels"]
    _cnn = lambda d: [k for k in d if k.startswith("CNN")]
    claim("disc_1bit_discrete_cd10", "8", "exact", 12.0739, _lv["1"]["static"]["test"]["discrete CD-10"])
    claim("disc_static_best_is_discrete_cd", "8", "exact", 1,
          int(all(v["static"]["classical_selected_on_val"].startswith("discrete CD") for v in _lv.values())),
          "validation selects discrete CD at every bit width")
    claim("disc_1bit_search_beats_rounding", "8", "exact", 1,
          int(_lv["1"]["static"]["test"]["discrete CD-10"] > _lv["1"]["static"]["test"]["CD-10 -> round"] + 0.1),
          "at 1 bit, searching the grid beats rounding a continuous optimum by >0.1")
    claim("disc_cnn_below_classical_mobility", "8", "exact", 1,
          int(all(v["mobility"][f"diff_to_classical[{k}]"][2] < 0
                  for v in _lv.values() for k in _cnn(v["mobility"]["test"]))),
          "every learned arm below the selected classical arm, every bit width (CI)")
    claim("disc_label_training_no_gain", "8", "exact", 1,
          int(all(v["static"]["test"]["CNN (b) discrete labels"] <= v["static"]["test"]["CNN (a) continuous labels"] + 0.01
                  for v in _lv.values())),
          "training on discrete labels does not beat rounding the continuous model")
    claim("disc_timing_started_idle", "8", "exact", 1, int(_dp["load_avg"]["before_timing"] < 0.5),
          "latency timing began below load 0.5")
    claim("disc_cnn_cd1_dominated", "8", "exact", 1,   # mean-based dominance (faster and higher mean)
          int(all(len(v["mobility"]["dominated_by[CNN (c) straight-through + discrete CD-1]"]) > 0 for v in _lv.values())),
          "network + 1 discrete sweep is dominated by a faster, better classical arm")

# ------------------------------------------- position-based phases (site)
# Regenerated 2026-11-06 after the h_d fix; pre-fix results are in
# results/stale_pre_hdfix/ and are not checked. Verdict: the position-based
# gain is NOT specific to learning (a training-free radio map beats the CNN).
section("saved results: position-based phases in a fixed site")
_ss = _load("site_eval_static.json")
_rm = _load("site_radio_map.json")
_sd = _load("site_eval_dynamic.json")
if _ss is None or _rm is None or _sd is None:
    print("  [skip] site_eval_static / site_radio_map / site_eval_dynamic missing")
else:
    claim("site_los_fraction_mean", "8", "statistical", 0.247,
          float(np.mean([v["los_fraction"] for v in _ss.values()])), "RIS-user LoS fraction, 5 test sets")
    claim("site_cnn_beats_geometric_static", "8", "exact", 1,
          int(all(v["by_sigma"]["0.0"]["cnn_minus_geometric"][1] > 0 for v in _ss.values())))
    claim("site_radio_map_beats_cnn_static", "8", "exact", 1,
          int(all(v["cnn_minus_radio_map_lookup"][2] < 0 for v in _rm.values())),
          "deployed kNN radio map (no training) above the CNN in every site (CI)")
    claim("site_cnn_beats_nn_lookup_static", "8", "exact", 1,
          int(all(v["cnn_minus_nn"][1] > 0 for v in _rm.values())))
    claim("site_fixed_phase_beats_geometric_site1", "8", "exact", 1,
          int(_rm["1"]["fixed_site_phase"] > _rm["1"]["geometric"]), "the geometric arm is a weak baseline")
    claim("site_dyn_radio_map_beats_cnn", "8", "exact", 1,
          int(all(v["cnn_minus"]["position + radio map"][2] < 0 for v in _sd["sites"].values())),
          "with pilot overhead too, the radio map is above the CNN in every site")
    claim("site_timing_started_idle", "8", "exact", 1,
          int(all(v["load_before_timing"] < 0.5 for v in _sd["sites"].values())))

# ------------------------------------- partial CSI (pre-registered, 9/17/33 pilots)
# ON_KAYIT_KISMI_CSI.md; scripts/sumiso_partial_train.py, sumiso_partial_eval.py.
section("saved results: partial CSI from reduced pilots (pre-registered)")
_pc = _load("sumiso_partial_static.json")
if _pc is None:
    print("  [skip] sumiso_partial_static.json missing")
else:
    _l8, _l16, _l32 = (_pc["levels"][k] for k in ("8", "16", "32"))
    claim("partial_primary_not_met", "8", "exact", 0, int(_l8["primary"]["met"]),
          "B does not beat the best classical arm at 9 pilots (97.5% CI)")
    claim("partial_primary_B_minus_best", "8", "exact", -1.2069, _l8["primary"]["mean"])
    claim("partial_best_classical_9", "8", "exact", 12.1099, _l8["test"][_l8["classical_selected_on_val"]],
          _l8["classical_selected_on_val"])
    claim("partial_best_is_grouping", "8", "exact", 1,
          int(all(l["classical_selected_on_val"].startswith("Group") for l in (_l8, _l16, _l32))),
          "validation selects element grouping at every pilot count")
    claim("partial_every_net_below_classical", "8", "exact", 1,
          int(all(v["ci95"][1] < 0 for l in (_l8, _l16, _l32) for k, v in l["diffs"].items()
                  if k.endswith(" - best classical"))),
          "every learned and hybrid arm below the best classical arm (CI), all pilot counts")
    claim("partial_sincos_beats_angle", "8", "exact", 1,
          int(all(v["ci95"][0] > 0 for l in (_l8, _l16, _l32) for k, v in l["diffs"].items() if " - C-" in k)),
          "B (sin/cos) above C (direct angle) at every pilot count and seed (CI)")
    claim("partial_B_minus_C_9", "8", "exact", 0.442, _l8["diffs"]["B-s0 - C-s0"]["mean"])
    claim("partial_2d_no_gain_9", "8", "exact", 1,
          int(all(_l8["diffs"][f"B-s{s} - A-s{s}"]["ci95"][1] < 0 for s in (0, 1, 2))),
          "the 2D-BiLSTM is below the published CNN-LSTM at 9 pilots, every seed (CI)")

_pr = _load("sumiso_partial_correlation.json")
if _pr is not None:
    claim("partial_corr_horizontal", "8", "statistical", 0.055, _pr["val_6000"]["horizontal_lag4"],
          "|rho| horizontal neighbours, cascaded channel (val 6000)")
    claim("partial_corr_vertical", "8", "statistical", 0.558, _pr["val_6000"]["vertical_lag1"],
          "|rho| vertical neighbours")
_pm = _load("sumiso_partial_mobility.json")
if _pm is None:
    print("  [skip] sumiso_partial_mobility.json missing")
else:
    _ml = _pm["levels"]
    claim("partial_mob_timing_idle", "8", "exact", 1, int(_pm["load_avg"]["before_timing"] < 0.5),
          "latency timing began below load 0.5")
    claim("partial_mob_every_net_dominated", "8", "exact", 1,
          int(all(len(v) > 0 for l in _ml.values() for v in l["dominated_by"].values())),
          "every learned arm has a faster classical arm with a higher effective rate")
    claim("partial_mob_every_net_below", "8", "exact", 1,
          int(all(v["ci95"][1] < 0 for l in _ml.values() for v in l["diffs"].values())),
          "every learned arm below the selected classical arm at its pilot count (CI)")
    _bestM = max(_ml, key=lambda M: _ml[M]["val"][_ml[M]["classical_selected_on_val"]])
    claim("partial_mob_full_csi_best", "8", "exact", 32, int(_bestM),
          "at 1.5 m/s, paying for all 33 pilots beats every reduced-pilot arm (validation)")

# ---------------------------------------------------- standardised speeds
# scripts/mumiso_standard_speeds.py: 3 km/h (3GPP TR 38.913), 10 km/h
# (ITU-R M.2410 indoor mobility), 30 km/h (stress test), and the paper's 5.4.
section("saved results: standardised user speeds")
_sp = _load("mumiso_standard_speeds.json")
if _sp is None:
    print("  [skip] mumiso_standard_speeds.json missing")
else:
    _b0 = {k: v["by_t_ov"]["0.0"] for k, v in _sp["speeds"].items()}
    claim("speeds_Lstar_pattern", "8", "exact", 1,
          int([_b0[k]["best_L"] for k in ("3", "5.4", "10", "18", "30")] == [8, 4, 3, 2, 1]),
          "best step count 8 / 4 / 3 / 2 / 1 at 3 / 5.4 / 10 / 18 / 30 km/h")
    claim("speeds_loss48_10kmh", "8", "exact", 10.5, _b0["10"]["loss_L48_pct"][0], "% cost of L=48 at 10 km/h")
    claim("speeds_loss48_3kmh", "8", "exact", 14.52, _b0["3"]["loss_L48_pct"][0], "% cost of L=48 at 3 km/h")
    claim("speeds_reversal_every_speed", "8", "exact", 1,
          int(all(b["su_best_minus_cd"][1] > 0 and b["su_best_minus_pga"][1] > 0 for b in _b0.values())),
          "2.5 ms SU-best-of above CD and long-run Adam at every speed (CI)")
    _m10 = _load("sumiso_mobility_eval_10kmh.json")
    if _m10 is not None:
        _m18 = _load("sumiso_mobility_eval_18kmh.json")
        if _m18 is not None:
            claim("speeds_18kmh_cnn_dominated", "8", "exact", 1,
                  int(all("Adam-1" in v["_dominated_by[CNN-LSTM]"] for v in _m18["effective"].values())),
                  "single-user CNN-LSTM at 5 m/s: dominated by Adam-1 at every T_ov")
        claim("speeds_10kmh_cnn_verdict", "8", "exact", 1,
              int(all(v["_best"] == "CD-1" and "Adam-1" in v["_dominated_by[CNN-LSTM]"] for v in _m10["effective"].values())),
              "single-user CNN-LSTM at 10 km/h: CD-1 best, Adam-1 dominates the CNN, every T_ov")
    claim("speeds_paper_speed_consistent", "8", "statistical", 14.0, _b0["5.4"]["loss_L48_pct"][0],
          "finer grid at 1.5 m/s agrees with the main sweep's 14.0%")

# ------------------------------------- robustness: CD budget, shared gains
section("saved results: tuned coordinate-descent budget and shared gains")
_cdb = _load("mumiso_cd_budget.json")
_shg = _load("mumiso_standard_speeds_shared.json")
if _cdb is None or _shg is None:
    print("  [skip] mumiso_cd_budget.json or mumiso_standard_speeds_shared.json missing")
else:
    claim("cd_one_sweep_ms", "8", "statistical", 107.0, _cdb["latency_ms"]["cd1"], "one multi-user CD sweep, idle timing")
    claim("cd_budget_su_best_wins", "8", "exact", 1,
          int(all(v["su_best_minus_best_cd"][1] > 0 for v in _cdb["speeds"].values())),
          "SU-best-of above the best CD budget (1-8 sweeps) at 1.5 m/s and 10 km/h (CI)")
    claim("cd_budget_timing_idle", "8", "exact", 1, int(_cdb["load_avg"]["before_timing"] < 0.5))
    _sb = {k: v["by_t_ov"]["0.0"] for k, v in _shg["speeds"].items()}
    claim("shared_gains_Lstar", "8", "exact", 1,
          int(set([4, 5, 6]) <= set(_sb["5.4"]["within_half_percent"]) and _sb["10"]["best_L"] == 3),
          "shared gains: L* 4-6 at 1.5 m/s, 3 at 10 km/h")
    claim("shared_gains_loss48", "8", "exact", 17.7, round(_sb["5.4"]["loss_L48_pct"][0], 1))
    claim("shared_gains_reversal", "8", "exact", 1,
          int(all(b["su_best_minus_cd"][1] > 0 and b["su_best_minus_pga"][1] > 0 for b in _sb.values())),
          "shared gains: SU-best-of above CD and long-run Adam (CI)")

# ----------------------------------------------------------------- report
section("summary")
fails = [r for r in RESULTS if r["ok"] is False]
n_checked = sum(1 for r in RESULTS if r["ok"] is not None)
print(f"  {n_checked - len(fails)}/{n_checked} asserted claims hold; "
      f"{sum(1 for r in RESULTS if r['ok'] is None)} informational")
if fails:
    print("\n  FAILED:")
    for r in fails:
        print(f"    {r['id']} (§{r['section']}): claimed {r['claimed']:.4g}, "
              f"measured {r['measured']:.4g}")
    print("\n  The report is wrong until proven otherwise. Fix the report, or")
    print("  find the regression in the package that moved the number.")
if not a.all:
    print("\n  (slow tiers skipped; rerun with --all before trusting §5)")
sys.exit(1 if fails else 0)
