"""
Partial-CSI experiment, evaluation (pre-registered: ON_KAYIT_KISMI_CSI.md).

--part static   (no timing): validation split (6000) selects every classical
                configuration and the hybrids' sweep count; the test split
                (6000, never used for selection) is evaluated once.
                Writes results/sumiso_partial_static.json.
--part mobility (timing on an idle machine): 1.5 m/s, selection on seed 12,
                report on seed 11 (400 scenarios each); effective rate at
                pilot time + measured latency. Writes results/sumiso_partial_mobility.json.

Arms at M observed elements (M + 1 pilots)
  classical  Interp+CD-s, LMMSE+CD-s (s = 0 is the closed form SU-align on the
             estimate), LMMSE+Adam-L (step size per L on validation),
             Group(c x r) with group phases by exact CD (shapes tuned on
             validation, deviation 1); at M = 32 these reduce to full CSI.
  learned    A / B / C (seed s), common phase restored with the LMMSE estimate;
             A/B + CD-s on the LMMSE estimate, s in {1, 2, 3} chosen on validation.
Rates on the true full channel, BS beam matched to it: log2(1 + snr |a + B^T v|^2).
"""
import sys
import os
import json
import time
import pathlib
import argparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import torch

from ris_mu.sumiso import solver as SV
from ris_mu.sumiso import partial as P
from ris_mu.sumiso.cnn_lstm import PhaseAwareCNNLSTM, phase, restore_common_phase

ap = argparse.ArgumentParser()
ap.add_argument("--part", required=True, choices=["static", "mobility"])
ap.add_argument("--M", type=int, nargs="*", default=[8, 16, 32])
ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--n_mob", type=int, default=400)
ap.add_argument("--reps", type=int, default=25)
ap.add_argument("--rounds", type=int, default=3)
ap.add_argument("--n_time", type=int, default=20)
ap.add_argument("--idle", type=float, default=0.5)
ap.add_argument("--smoke", action="store_true", help="code check on 500 validation scenarios only (test split untouched, nothing written)")
ap.add_argument("--seeds8", default="0,1,2", help="seeds evaluated at M = 8")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
torch.set_num_threads(a.threads)

CD_S = [0, 1, 2, 3, 5, 10, 30]
ADAM_L = [1, 2, 4, 8, 16, 32, 64]
LRS = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
HYB_S = [1, 2, 3]
SEEDS = {8: [int(x) for x in a.seeds8.split(",")], 16: [0], 32: [0]}
T_PILOT_MS = 3.43 / 48            # one OFDM symbol at 15 kHz (paper, Section V-D)

z = np.load(ROOT / "data_sumiso" / "sumiso_train.npz")
snr = float(z["snr_scale"])
perm = np.random.default_rng(0).permutation(len(z["theta"]))      # sumiso_train.py split
itr, iva, ite = perm[:28000], perm[28000:34000], perm[34000:]


def cas(ix):
    return SV.cascade(torch.as_tensor(z["F"][ix]), torch.as_tensor(z["G"][ix]), torch.as_tensor(z["hd"][ix]))


A_tr, B_tr = cas(itr)
rate = lambda th, A, B: torch.log2(1 + snr * SV.gain(th, A, B))


def cd(A, Bh, th0, s):
    return th0 if s == 0 else SV.coord_ascent(A, Bh, th0, sweeps=s, tol=-1)[0]


def adam(A, Bh, th0, L, lr):
    th = th0.clone().requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr)
    for _ in range(L):
        loss = -torch.log2(1 + SV.gain(th, A, Bh) * snr).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return th.detach()


def load_net(model, M, seed):
    ck = torch.load(ROOT / "results" / f"sumiso_partial_{model}_M{M}_s{seed}.pt")
    net = PhaseAwareCNNLSTM(ck["C"], ck["N"], "seq", 2) if model == "A" else \
        P.CNN2DBiLSTM(ck["C"], ck["N"], 2 if model == "B" else 1)
    net.load_state_dict(ck["state"])
    net.eval()
    return net, ck["mu"], ck["sd"]


def net_phase(pack, A, B, m, Bl):
    net, mu, sd = pack
    with torch.no_grad():
        out = [phase(net((P.features_partial(A[i:i + 2000], B[i:i + 2000], m) - mu) / (sd + 1e-9)))
               for i in range(0, len(A), 2000)]
    return restore_common_phase(torch.cat(out), A, Bl)


class Arms:
    """All phase rules at one M, with their classical hyper-parameters."""
    def __init__(self, M):
        self.M, self.m = M, P.mask(M)
        self.lmmse = P.LMMSE(A_tr, B_tr, self.m)
        self.nets = {f"{mod}-s{s}": load_net(mod, M, s) for mod in "ABC" for s in SEEDS[M]}
        self.lr_of = {}

    def estimates(self, A, B):
        return {"Interp": P.interp_fill(B, self.m), "LMMSE": self.lmmse(A, B)}

    def tune_adam(self, A, B):
        Bl = self.lmmse(A, B)
        al = SV.su_align(A, Bl)
        for L in ADAM_L:
            sc = {lr: float(rate(adam(A, Bl, al, L, lr), A, B).mean()) for lr in LRS}
            self.lr_of[L] = max(sc, key=sc.get)

    def classical(self, A, B):
        out = {}
        for name, Bh in self.estimates(A, B).items():
            al = SV.su_align(A, Bh)
            for s in CD_S:
                out[f"{name}+CD-{s}"] = cd(A, Bh, al, s)
            if name == "LMMSE":
                for L in ADAM_L:
                    out[f"LMMSE+Adam-{L}"] = adam(A, Bh, al, L, self.lr_of[L])
        for sh in P.GROUP_SHAPES[self.M]:
            out[f"Group{sh[0]}x{sh[1]}"] = P.group_solve(A, B, self.M, sh)
        return out

    def learned(self, A, B):
        Bl = self.lmmse(A, B)
        out = {}
        for k, pack in self.nets.items():
            th = net_phase(pack, A, B, self.m, Bl)
            out[k] = th
            if k[0] in "AB":
                for s in HYB_S:
                    out[f"{k}+CD-{s}"] = cd(A, Bl, th, s)
        return out


rng_bs = np.random.default_rng(0)


def boot(d, lo=2.5, hi=97.5):
    bs = np.array([d[rng_bs.integers(0, len(d), len(d))].mean() for _ in range(2000)])
    return [float(np.percentile(bs, lo)), float(np.percentile(bs, hi))]


def rmse_deg(th_hat, th):
    d = torch.angle(torch.exp(1j * ((th_hat - th_hat[:, :1]) - (th - th[:, :1])).to(torch.complex64)))
    return float(torch.sqrt((d ** 2).mean()) * 180 / np.pi)


if a.part == "static":
    if a.smoke:
        iva, ite = iva[:500], iva[:500]
    Av, Bv = cas(iva)
    At, Bt = cas(ite)
    TH_t = torch.as_tensor(z["theta"][ite]).float()
    res = dict(config=vars(a), n=dict(train=len(itr), val=len(iva), test=len(ite)), levels={})
    for M in a.M:
        t0 = time.time()
        R = Arms(M)
        R.tune_adam(Av, Bv)
        Pv = {**R.classical(Av, Bv), **R.learned(Av, Bv)}
        val = {k: float(rate(th, Av, Bv).mean()) for k, th in Pv.items()}
        cl = [k for k in val if k.startswith(("Interp", "LMMSE", "Group"))]
        best_cl = max(cl, key=val.get)
        hyb = {mod_s: max([f"{mod_s}+CD-{s}" for s in HYB_S], key=val.get)
               for mod_s in R.nets if mod_s[0] in "AB"}
        Pt = {**R.classical(At, Bt), **R.learned(At, Bt)}        # the single look at the test split
        rt = {k: rate(th, At, Bt).numpy() for k, th in Pt.items()}
        test = {k: float(v.mean()) for k, v in rt.items()}
        lev = dict(pilots=M + 1, adam_lr=R.lr_of, lmmse_mean_norm=R.lmmse.mean_norm,
                   val=val, test=test, classical_selected_on_val=best_cl,
                   hybrid_selected_on_val=hyb,
                   oracle_label=float(rate(TH_t, At, Bt).mean()),
                   full_csi_su_align=float(rate(SV.su_align(At, Bt), At, Bt).mean()),
                   test_rmse_deg={k: rmse_deg(Pt[k], TH_t) for k in R.nets}, diffs={})
        for k in list(R.nets) + list(hyb.values()):
            d = rt[k] - rt[best_cl]
            lev["diffs"][f"{k} - best classical"] = dict(mean=float(d.mean()), ci95=boot(d),
                                                       ci975=boot(d, 1.25, 98.75))
        for s in SEEDS[M]:
            for x, y in (("B", "A"), ("B", "C")):
                d = rt[f"{x}-s{s}"] - rt[f"{y}-s{s}"]
                lev["diffs"][f"{x}-s{s} - {y}-s{s}"] = dict(mean=float(d.mean()), ci95=boot(d))
        if M == 8:
            d = lev["diffs"]["B-s0 - best classical"]
            lev["primary"] = dict(criterion="B-s0 - best classical, 97.5% paired CI lower bound > 0",
                                  mean=d["mean"], ci975=d["ci975"], met=bool(d["ci975"][0] > 0))
            dA = lev["diffs"]["A-s0 - best classical"]
            lev["primary_A"] = dict(mean=dA["mean"], ci975=dA["ci975"], met=bool(dA["ci975"][0] > 0))
        res["levels"][str(M)] = lev
        print(f"=== M={M} ({M + 1} pilots)  {time.time() - t0:.0f}s")
        print(f"  best classical (val): {best_cl}  test {test[best_cl]:.4f}  | oracle {lev['oracle_label']:.4f}")
        for k in R.nets:
            print(f"  {k:6s} test {test[k]:.4f}  RMSE {lev['test_rmse_deg'][k]:5.1f} deg  "
                  f"diff {lev['diffs'][k + ' - best classical']['mean']:+.4f} CI97.5 {lev['diffs'][k + ' - best classical']['ci975']}")
        for k in hyb.values():
            print(f"  {k:12s} test {test[k]:.4f}  diff {lev['diffs'][k + ' - best classical']['mean']:+.4f} "
                  f"CI95 {lev['diffs'][k + ' - best classical']['ci95']}")
        if "primary" in lev:
            print("  PRIMARY:", lev["primary"])
        if not a.smoke:
            json.dump(res, open(ROOT / "results" / "sumiso_partial_static.json", "w"), indent=1)
    print("smoke test only, nothing written" if a.smoke else "wrote results/sumiso_partial_static.json")

if a.part == "mobility":
    from ris_mu.mumiso.channel import make_mumiso_scenario
    from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
    TIMES = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.5, 10.0, 13.3, 15.0, 20.0, 28.2,
             35.0, 50.0, 75.0, 100.0, 150.0, 200.0)
    torch.set_num_threads(1)
    load0 = os.getloadavg()[0]

    def draw(seed):
        torch.manual_seed(0)
        panel, base = make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=seed)
        cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
        d = MobileMuMisoChannel(panel, cfg).generate(a.n_mob)
        assert abs(cfg.snr_scale() - snr) < 1e-6 * snr
        F = torch.as_tensor(d["F"], dtype=torch.complex64)
        return [SV.cascade(F, torch.as_tensor(d["G_t"][:, k], dtype=torch.complex64),
                           torch.as_tensor(d["hd_t"][:, k], dtype=torch.complex64)) for k in range(len(TIMES))]

    MOB = {"val": draw(12), "test": draw(11)}
    Av6, Bv6 = cas(iva)
    GROUP_S = [1, 2, 3, 5, 10, 30]

    def group_cd(A, B, M, sh, s):
        """Online grouping: group phases by s CD sweeps from SU-align (single start)."""
        g = P.groups(M, sh)
        Bg = torch.stack([B[:, g == k].sum(1) for k in range(M)], 1)
        return SV.coord_ascent(A, Bg, SV.su_align(A, Bg), sweeps=s, tol=-1)[0][:, g]

    res = dict(config=vars(a), pilot_symbol_ms=T_PILOT_MS, times_ms=TIMES, levels={})
    arms_by_M, fns = {}, {}
    for M in a.M:
        R = Arms(M)
        R.tune_adam(Av6, Bv6)
        arms_by_M[M] = R

        def rules(R=R, M=M):
            """name -> function(A, B) -> phase; B is the TRUE channel, each rule sees only its pilots."""
            f = {}
            for s in CD_S:
                f[f"Interp+CD-{s}"] = lambda A, B, s=s: cd(A, P.interp_fill(B, R.m), SV.su_align(A, P.interp_fill(B, R.m)), s)
                f[f"LMMSE+CD-{s}"] = lambda A, B, s=s: (lambda Bl: cd(A, Bl, SV.su_align(A, Bl), s))(R.lmmse(A, B))
            for L in ADAM_L:
                f[f"LMMSE+Adam-{L}"] = lambda A, B, L=L: (lambda Bl: adam(A, Bl, SV.su_align(A, Bl), L, R.lr_of[L]))(R.lmmse(A, B))
            for sh in P.GROUP_SHAPES[M]:
                for s in GROUP_S:
                    f[f"Group{sh[0]}x{sh[1]}+CD-{s}"] = lambda A, B, sh=sh, s=s: group_cd(A, B, M, sh, s)
            for k, pack in R.nets.items():
                if not k.endswith("s0"):
                    continue
                f[k] = lambda A, B, pack=pack: net_phase(pack, A, B, R.m, R.lmmse(A, B))
                if k[0] in "AB":
                    for s in HYB_S:
                        f[f"{k}+CD-{s}"] = lambda A, B, pack=pack, s=s: (lambda Bl: cd(A, Bl, net_phase(pack, A, B, R.m, Bl), s))(R.lmmse(A, B))
            return f
        fns[M] = rules()

    # --- latency: idle machine, one scenario, one thread, median of reps, rounds
    t_wait = time.time()
    while os.getloadavg()[0] >= a.idle:           # CLAUDE.md: never time under load
        time.sleep(10)
    load1 = os.getloadavg()[0]
    print(f"timing starts at load {load1:.2f} after waiting {time.time() - t_wait:.0f} s", flush=True)
    A0, B0 = MOB["test"][0]

    def timeit(fn):
        out = []
        for r in range(a.rounds):
            per = []
            for i in range(a.n_time):
                args = (A0[i:i + 1], B0[i:i + 1])
                if True:
                    fn(*args)
                    t = []
                    for _ in range(a.reps):
                        t0 = time.perf_counter()
                        fn(*args)
                        t.append(time.perf_counter() - t0)
                per.append(np.median(t) * 1e3)
            out.append(float(np.median(per)))
        return out

    lat_rounds = {M: {k: timeit(f) for k, f in fns[M].items()} for M in a.M}
    load2 = os.getloadavg()[0]
    res["load_avg"] = dict(start=load0, before_timing=load1, after_timing=load2)
    res["latency_rounds_ms"] = {str(M): v for M, v in lat_rounds.items()}
    torch.set_num_threads(a.threads)

    for M in a.M:
        lat = {k: float(np.median(v)) for k, v in lat_rounds[M].items()}
        tp = (M + 1) * T_PILOT_MS
        eff = {}
        for part in ("val", "test"):
            C = MOB[part]
            A0p, B0p = C[0]
            eff[part] = {}
            for k, f in fns[M].items():
                th = f(A0p, B0p)
                curve = torch.stack([rate(th, A, B) for A, B in C], 1).numpy()
                eff[part][k] = np.array([np.interp(tp + lat[k], TIMES, row) for row in curve])
        cl = [k for k in eff["val"] if k.startswith(("Interp", "LMMSE", "Group"))]
        best = max(cl, key=lambda k: eff["val"][k].mean())
        te = eff["test"]
        lev = dict(pilots=M + 1, pilot_ms=tp, latency_ms=lat,
                   val={k: float(v.mean()) for k, v in eff["val"].items()},
                   test={k: float(v.mean()) for k, v in te.items()},
                   classical_selected_on_val=best, diffs={}, dominated_by={})
        for k in te:
            if k[0] in "ABC":
                d = te[k] - te[best]
                lev["diffs"][f"{k} - best classical"] = dict(mean=float(d.mean()), ci95=boot(d))
                lev["dominated_by"][k] = [c for c in cl if lat[c] < lat[k] and te[c].mean() > te[k].mean()]
        res["levels"][str(M)] = lev
        print(f"=== M={M}: pilots {tp:.2f} ms; best classical (val) {best} lat {lat[best]:.2f} ms test {lev['test'][best]:.4f}")
        for k in lev["diffs"]:
            kk = k.split(" - ")[0]
            print(f"  {kk:12s} lat {lat[kk]:6.2f} ms  test {lev['test'][kk]:.4f}  {lev['diffs'][k]['mean']:+.4f} CI {lev['diffs'][k]['ci95']}"
                  f"  dominated by {len(lev['dominated_by'][kk])}")
    json.dump(res, open(ROOT / "results" / "sumiso_partial_mobility.json", "w"), indent=1)
    print("wrote results/sumiso_partial_mobility.json")
