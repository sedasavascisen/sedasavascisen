"""
Robustness of Paper 2, Fig. 5 (static set) to the validation/test subsets. User-approved exception to the closed
measurement phase (22 Nov 2026). Rates only: NO new timing; panel (b) dominance reuses the stored per-round medians
(results/mumiso_latency_repeat.json), exactly as make_paper_assets.py does.

Same channels, split, checkpoints and grids as the published run (scripts/mumiso_equal_step.py, mumiso_latency_parity.py):
  samples 6000, seed 11, split_indices(seed=0); Adam objective in {soft, hard};
  step sizes: ten values for L <= 16, six values for L = 24..64 (paper Sec. V-B, Tuning).
Variants
  V0  Adam tuned on va[:400], reported on te[:600]   -> MUST reproduce results/mumiso_equal_step.json + parity rates
  V1a Adam tuned on va[:500] (the learned rule's own validation subset), reported on te[:600]
  V1  Adam tuned on va[:500], reported on all 900 test scenarios (learned arm needs the weights archive)
Paper claims checked in each variant
  (a) learned beats tuned Adam at every L in {1,2,4,8,16}; win fraction range (paper: 68-84 %); paired bootstrap CI
  (b) every learned configuration is dominated by a faster-and-better Adam configuration in each of 5 timing rounds
  chosen (lr, objective) per budget (paper: 0.75 soft-min for every L <= 16)
-> saglamlik_900.json, printed table
"""
import sys, json, pathlib, subprocess, statistics as st
R = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(R))
import numpy as np, torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B
from ris_mu.features import split_indices

torch.manual_seed(11)
panel, cfg = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
N = panel.positions.shape[0]
d = MuMisoChannel(panel, cfg).generate(6000)
F, G, hd, _ = to_torch(d)
pt, nv = 1.0, 1.0 / cfg.snr_scale()
phi = S.su_align_phase(F, G, hd)
X = torch.from_numpy(mumiso_features(d["F"], d["G"], d["hd"], phi.numpy()))
tr, va, te = split_indices(6000, seed=0)
_, TH0 = B.su_average(F, G, hd, pt, nv)
LRS10 = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
LRS6 = [0.2, 0.35, 0.5, 0.75, 1.0, 1.5]
LB, CB = [1, 2, 4, 8, 16], [1, 2, 4, 8, 16, 24, 32, 48, 64]


def rate(th, ids):
    return S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th), pt, nv, "zf").min(-1).values


def adam(ids, L, lr, obj):                       # identical to both published scripts
    dl = torch.zeros(len(ids), N, requires_grad=True)
    opt = torch.optim.Adam([dl], lr=lr)
    for _ in range(L):
        th = TH0[ids] + dl
        Rr = S.rates(F[ids], G[ids], hd[ids], torch.cos(th), torch.sin(th), pt, nv, "zf")
        loss = -(-torch.logsumexp(-8.0 * Rr, dim=-1) / 8.0).mean() if obj == "soft" else -Rr.min(-1).values.mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return TH0[ids] + dl.detach()


def boot(x, n=2000, seed=0):
    rng = np.random.default_rng(seed); x = np.asarray(x)
    m = x[rng.integers(0, len(x), (n, len(x)))].mean(1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


nets = {}
for L in LB:                                       # weights archive is not in the repo; use it if it is unpacked
    ck = R / f"results/mumiso_eqstep_L{L}.pt"
    if ck.exists():
        n = UnrolledMuMiso(N=N, n_users=4, n_tx=8, steps=L, mode="exchange", use_grad=True)
        n.load_state_dict(torch.load(ck)); n.eval(); nets[L] = n
# without weights: the learned rule's per-scenario rates on te[:600], stored by the published run
STORED = {L: torch.tensor(json.load(open(R / "results/mumiso_latency_parity.json"))["learned"][str(L)]["per_scenario"]) for L in LB}
rep = json.load(open(R / "results/mumiso_latency_repeat.json"))
n_rounds = len(rep["learned"]["1"])
out = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=R).stdout.strip(), variants={})
for name, nval, ntest in (("V0_val400_test600", 400, 600), ("V1a_val500_test600", 500, 600), ("V1_val500_test900", 500, 900)):
    vv, ev = va[:nval], te[:ntest]
    res = dict(n_val=nval, n_test=ntest, adam={}, learned={}, eqstep={})
    for L in CB:
        grid = LRS10 if L <= 16 else LRS6
        sc = {(lr, ob): rate(adam(vv, L, lr, ob), vv).mean().item() for ob in ("soft", "hard") for lr in grid}
        lr, ob = max(sc, key=sc.get)
        r = rate(adam(ev, L, lr, ob), ev)
        res["adam"][L] = dict(lr=lr, obj=ob, rate=r.mean().item()); res["adam"][L]["_r"] = r
    res["learned_source"] = "checkpoints" if len(nets) == len(LB) else ("stored per-scenario rates (te[:600])" if ntest == 600 else None)
    for L in (LB if res["learned_source"] else []):
        if nets:
            with torch.no_grad():
                th = nets[L](X[ev], F[ev], G[ev], hd[ev], pt, nv, TH0[ev])
            th = th[0] if isinstance(th, tuple) else th
            r = rate(th, ev)
        else:
            r = STORED[L]
        dif = (r - res["adam"][L]["_r"]).numpy()
        res["learned"][L] = dict(rate=r.mean().item())
        res["eqstep"][L] = dict(diff=float(dif.mean()), ci=boot(dif), win=float((dif > 0).mean()))
    ar_ = {L: res["adam"][L]["rate"] for L in CB}
    for L in CB:
        res["adam"][L].pop("_r")
    out["variants"][name] = res
    if not res["learned_source"]:
        print(f"\n== {name}: learned arm NOT evaluated (weights archive missing)")
        print("  adam:", {L: (round(ar_[L], 4), res["adam"][L]["lr"], res["adam"][L]["obj"]) for L in CB})
        continue
    lr_ = {L: res["learned"][L]["rate"] for L in LB}; ar_ = {L: res["adam"][L]["rate"] for L in CB}
    dom = {}
    for L in LB:                                   # make_paper_assets.py: dominated_in_round
        rounds = sum(any(rep["adam"][str(k)][r] <= rep["learned"][str(L)][r] and ar_[k] >= lr_[L] for k in map(int, rep["adam"]))
                     for r in range(n_rounds))
        dom[L] = rounds
    res["dominated_rounds"] = dom; res["n_rounds"] = n_rounds
    print(f"\n== {name}")
    for L in LB:
        e = res["eqstep"][L]
        print(f"  L={L:2d} learned {lr_[L]:.4f} adam {ar_[L]:.4f} ({res['adam'][L]['lr']}/{res['adam'][L]['obj']}) "
              f"diff {e['diff']:+.4f} [{e['ci'][0]:+.4f},{e['ci'][1]:+.4f}] win {100*e['win']:.1f}%  dominated {dom[L]}/{n_rounds}")
    print("  adam 24-64:", {L: (round(ar_[L], 4), res["adam"][L]["lr"], res["adam"][L]["obj"]) for L in CB if L > 16})
# V0 must reproduce the published files
pub = json.load(open(R / "results/mumiso_equal_step.json"))["rows"]; par = json.load(open(R / "results/mumiso_latency_parity.json"))
v0 = out["variants"]["V0_val400_test600"]
out["v0_reproduces_published"] = dict(
    max_abs_learned=max(abs(v0["learned"][L]["rate"] - pub[str(L)]["learned"]) for L in LB),
    max_abs_adam_le16=max(abs(v0["adam"][L]["rate"] - pub[str(L)]["swept"]) for L in LB),
    max_abs_adam_24_64=max(abs(v0["adam"][L]["rate"] - par["classical"][str(L)]["rate"]) for L in CB if L > 16),
    max_abs_win=max(abs(v0["eqstep"][L]["win"] - pub[str(L)]["learned_wins_frac"]) for L in LB))
print("\nV0 vs published:", out["v0_reproduces_published"])
json.dump(out, open(pathlib.Path(__file__).with_name("saglamlik_900.json"), "w"), indent=1)
