"""
Feasibility of a wideband-OFDM extension of the latency framework.

Question: in the thesis scenario, is the wideband penalty (one RIS phase
vector has to serve every subcarrier) large enough to matter, and how does
the per-step cost grow with the number of subcarriers K_sub?

Scenario: the single-user aging set of scripts/sumiso_dataset.py with the
evaluation seed (make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=11),
3 GHz, wall 8x4 RIS, 20 scatterers, direct link blocked by 40 dB), t = 0
snapshot, --scenarios draws (default 300, one generator chunk, so every
bandwidth sees exactly the same channels).

Wideband channels come from MobileMuMisoChannel.generate(freq_offsets_hz=...)
(phase-only re-evaluation at fc + df, amplitudes at fc). This captures BOTH
the multipath delay spread and the intra-aperture delay (beam squint).

Sections (each is written into results/wideband_feasibility.json, merging
with what is already there):

  --part delay   RMS delay spread and coherence bandwidth, from a dense
                 512-point grid over 400 MHz: IFFT (Hann window) of the
                 per-element cascaded links b_nt(f) = g_n(f) F_nt(f)
                 (PDP of the cascade with uncorrelated RIS phases) and of the
                 effective channel h(f; theta_c) at the centre-frequency
                 optimum; bulk delay of the BS-RIS-UE centre path removed
                 first; PDP thresholded at -30 dB of its peak. Coherence
                 bandwidth = smallest df where the frequency correlation
                 |R(df)| falls below 0.9 / 0.5. Also for the 4-user aging set.
  --part gain    For B in {1,5,20,50,100} MHz and K_sub in {16,64}
                 (subcarriers at the centres of K_sub equal bins of B):
                   per-subcarrier optimum (upper bound, exact CD per f),
                   one wideband phase (exact CD on the sum-power objective
                   sum_f |h_f|^2 == narrowband problem with K_sub*T virtual
                   antennas, best of SU-align + 3 random + narrowband start,
                   then Adam on the sum-rate objective, best kept),
                   narrowband phase (exact CD at fc) applied to all f,
                   random phase (context).
                 Rates: mean_f log2(1 + snr |h_f|^2), snr = cfg.snr_scale()
                 per subcarrier (same per-subcarrier SNR at every B).
  --part cost    Operation counts of one objective+gradient evaluation and
                 one CD sweep vs K_sub; wall-clock ONLY if the 1-min load
                 average is < 0.5 at start (otherwise skipped and said so).
  --part squint  Analytic beam-squint estimate, no simulation.

Usage:
  python3 scripts/wideband_feasibility.py --part cost     # idle machine first
  python3 scripts/wideband_feasibility.py --part squint
  python3 scripts/wideband_feasibility.py --part delay    # ~1 min
  python3 scripts/wideband_feasibility.py --part gain     # a few min
"""
import sys
import json
import time
import pathlib
import argparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import torch

from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.sumiso import solver as SV

ap = argparse.ArgumentParser()
ap.add_argument("--part", choices=("delay", "gain", "cost", "squint", "all"), default="all")
ap.add_argument("--scenarios", type=int, default=300)
a = ap.parse_args()
OUT = ROOT / "results/wideband_feasibility.json"
BWS = (1e6, 5e6, 20e6, 50e6, 100e6)
KSUBS = (16, 64)
C0 = 299_792_458.0


def say(*m):
    print(*m, flush=True)


def load():
    try:
        return json.load(open(OUT))
    except (OSError, ValueError):
        return {}


def save(key, val):
    res = load()
    res[key] = val
    res.setdefault("_meta", {}).update(
        scenario="make_mumiso_scenario(n_users=1, n_bs_antennas=8, seed=11), "
                 "MobileConfig(velocity=1.5, times_ms=(0.0,), n_clusters=20)",
        approximation="phase-only re-evaluation at fc+df (k_f = 2 pi (fc+df)/c); "
                      "amplitudes / path loss / normalisation at fc",
        script="scripts/wideband_feasibility.py")
    json.dump(res, open(OUT, "w"), indent=1)
    say(f"  -> {OUT.relative_to(ROOT)} [{key}]")


def channel(n_users=1, S=None, offsets=None):
    S = S or a.scenarios
    panel, base = make_mumiso_scenario(n_users=n_users, n_bs_antennas=8, seed=11)
    cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": (0.0,),
                          "n_clusters": 20})
    d = MobileMuMisoChannel(panel, cfg).generate(S, freq_offsets_hz=offsets)
    return panel, cfg, d


def pct(x):
    x = np.asarray(x, float)
    return dict(mean=float(np.mean(x)), median=float(np.median(x)),
                p5=float(np.percentile(x, 5)), p95=float(np.percentile(x, 95)))


# --------------------------------------------------------------- delay spread
def rms_from_pdp(p, tau):
    """p [..., Nf] power vs delay tau [Nf]; -30 dB threshold of peak."""
    p = np.where(p >= p.max(-1, keepdims=True) * 1e-3, p, 0.0)
    w = p / p.sum(-1, keepdims=True)
    m1 = (w * tau).sum(-1)
    return np.sqrt(np.maximum((w * tau ** 2).sum(-1) - m1 ** 2, 0.0))


def coh_bw(H, df, thr):
    """H [S, Nf, X] -> smallest lag (Hz) where mean |R| < thr."""
    Nf = H.shape[1]
    p0 = np.mean(np.sum(np.abs(H) ** 2, -1))
    out = None
    for lag in range(1, Nf // 2):
        r = np.abs(np.mean(np.sum(H[:, lag:] * H[:, :-lag].conj(), -1))) / p0
        if r < thr:
            out = lag * df
            break
    return out


def part_delay():
    Nf, span = 512, 400e6
    df = span / Nf
    offs = (np.arange(Nf) - Nf // 2) * df
    res = {"grid": dict(n_freq=Nf, span_hz=span, df_hz=df,
                        delay_window_s=1 / df, resolution_s=1 / span)}
    for n_users, S in ((1, a.scenarios), (4, 100)):
        t0 = time.time()
        panel, cfg, d = channel(n_users, S, offs)
        Ff = d["F_f"]                      # [S,Nf,N,T]
        Gf = d["G_tf"][:, 0]               # [S,Nf,K,N]
        ris_c = panel.positions.mean(0)
        tau0 = (np.linalg.norm(d["bs_pos"] - ris_c, axis=-1)[:, None]
                + np.linalg.norm(d["ue_pos"] - ris_c, axis=-1)) / C0   # [S,K]
        win = np.hanning(Nf)
        tau = np.fft.fftfreq(Nf, df)       # wraps: [0, +), then negative
        rows = {}
        for u in range(n_users):
            rot = np.exp(1j * 2 * np.pi * offs[None, :] * tau0[:, u, None])   # remove bulk
            b = Gf[:, :, u, :, None] * Ff * rot[..., None, None]             # [S,Nf,N,T]
            Bt = np.fft.ifft(b * win[None, :, None, None], axis=1)
            pdp_el = np.mean(np.abs(Bt) ** 2, axis=(2, 3))                  # [S,Nf]
            # narrowband optimum (exact CD at fc) -> effective channel
            A_c, B_c = SV.cascade(torch.as_tensor(d["F"]),
                                  torch.as_tensor(d["G"][:, u:u + 1]),
                                  torch.as_tensor(d["hd"][:, u:u + 1]))
            th_c, _ = SV.solve(A_c, B_c)
            v = np.exp(1j * th_c.numpy())
            hd = d["hd_tf"][:, 0, :, u, :] * rot[..., None]
            h = hd + np.einsum("sn,sfnt->sft", v, b)                          # [S,Nf,T]
            pdp_eff = np.sum(np.abs(np.fft.ifft(h * win[None, :, None], axis=1)) ** 2, -1)
            ts_el = rms_from_pdp(pdp_el, tau)
            ts_eff = rms_from_pdp(pdp_eff, tau)
            bl = b.reshape(S, Nf, -1)
            rows[f"user{u}"] = dict(
                tau_rms_ns_cascade_links=pct(ts_el * 1e9),
                tau_rms_ns_effective_at_theta_c=pct(ts_eff * 1e9),
                Bc90_hz_cascade_links=coh_bw(bl, df, 0.9),
                Bc50_hz_cascade_links=coh_bw(bl, df, 0.5),
                Bc90_hz_effective=coh_bw(h, df, 0.9),
                Bc50_hz_effective=coh_bw(h, df, 0.5),
                Bc_rule_1_over_5tau_hz=float(1 / (5 * np.median(ts_el))),
                Bc_rule_1_over_50tau_hz=float(1 / (50 * np.median(ts_el))))
            say(f"  K={n_users} user{u}: tau_rms median {np.median(ts_el)*1e9:.1f} ns "
                f"(links), {np.median(ts_eff)*1e9:.1f} ns (effective); "
                f"Bc50 {rows[f'user{u}']['Bc50_hz_cascade_links']/1e6:.2f} MHz, "
                f"Bc90 {rows[f'user{u}']['Bc90_hz_cascade_links']/1e6:.2f} MHz")
        res[f"users{n_users}"] = dict(scenarios=S, users=rows, seconds=time.time() - t0)
    save("delay_spread", res)


# ---------------------------------------------------------------- gain loss
def rate(g, snr):
    return torch.log2(1 + snr * g)


def gains_all(theta, A, B):
    """theta [S,N]; A [S,K,T]; B [S,K,N,T] -> g [S,K]."""
    h = A + torch.einsum("sn,sknt->skt", torch.exp(1j * theta.to(torch.complex64)), B)
    return (h.abs() ** 2).sum(-1)


def adam_refine(theta0, A, B, snr, steps=300, lr=0.03):
    th = theta0.clone().requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr)
    best = theta0.clone()
    with torch.no_grad():
        bv = rate(gains_all(best, A, B), snr).mean(1)
    for _ in range(steps):
        r = rate(gains_all(th, A, B), snr).mean(1)
        with torch.no_grad():
            up = r > bv
            best[up] = th.detach()[up]
            bv = torch.where(up, r, bv)
        opt.zero_grad()
        (-r.sum()).backward()
        opt.step()
    return best


def part_gain():
    torch.manual_seed(0)
    res = {}
    for Bw in BWS:
        offs = {K: ((np.arange(K) + 0.5) / K - 0.5) * Bw for K in KSUBS}
        t0 = time.time()
        panel, cfg, d = channel(1, None, np.concatenate([offs[K] for K in KSUBS]))
        snr = cfg.snr_scale()
        S, N, T = d["F"].shape
        A_c, B_c = SV.cascade(torch.as_tensor(d["F"]), torch.as_tensor(d["G"]),
                              torch.as_tensor(d["hd"]))
        th_c, _ = SV.solve(A_c, B_c)
        row, j0 = {}, 0
        for K in KSUBS:
            sl = slice(j0, j0 + K)
            j0 += K
            Ff = torch.as_tensor(d["F_f"][:, sl])                       # [S,K,N,T]
            Gf = torch.as_tensor(d["G_tf"][:, 0, sl, 0])                # [S,K,N]
            Hf = torch.as_tensor(d["hd_tf"][:, 0, sl, 0])               # [S,K,T]
            Bf = Gf[..., None] * Ff                                     # [S,K,N,T]
            # per-subcarrier optimum
            a1, b1 = SV.cascade(Ff.reshape(S * K, N, T), Gf.reshape(S * K, 1, N),
                                Hf.reshape(S * K, 1, T))
            _, g_sub = SV.solve(a1, b1)
            g_sub = g_sub.reshape(S, K)
            # one wideband phase: sum-power CD == narrowband with K*T antennas
            aw = Hf.reshape(S, K * T)
            bw = Bf.permute(0, 2, 1, 3).reshape(S, N, K * T)
            th_w, gsum = SV.solve(aw, bw)
            th_w2, gsum2 = SV.coord_ascent(aw, bw, th_c.clone())
            th_w = torch.where((gsum2 > gsum)[:, None], th_w2, th_w)
            th_r = adam_refine(th_w, Hf, Bf, snr)
            g_wb = gains_all(th_r, Hf, Bf)
            g_nb = gains_all(th_c, Hf, Bf)
            g_rnd = gains_all((torch.rand(S, N) * 2 - 1) * torch.pi, Hf, Bf)

            def rr(g):
                return rate(g, snr).mean(1)

            def db(gx):          # per-scenario gain loss vs per-subcarrier optimum
                return 10 * torch.log10(g_sub.mean(1) / gx.mean(1)).numpy()

            R_ub, R_wb, R_nb, R_rnd = rr(g_sub), rr(g_wb), rr(g_nb), rr(g_rnd)
            row[f"K{K}"] = dict(
                rate_per_subcarrier_opt=float(R_ub.mean()),
                rate_single_wideband_phase=float(R_wb.mean()),
                rate_narrowband_phase=float(R_nb.mean()),
                rate_random_phase=float(R_rnd.mean()),
                rate_loss_pct_wideband_vs_ub=float(100 * (1 - R_wb.mean() / R_ub.mean())),
                rate_loss_pct_narrowband_vs_ub=float(100 * (1 - R_nb.mean() / R_ub.mean())),
                rate_loss_pct_narrowband_vs_wideband=float(100 * (1 - R_nb.mean() / R_wb.mean())),
                gain_loss_db_wideband_vs_ub=pct(db(g_wb)),
                gain_loss_db_narrowband_vs_ub=pct(db(g_nb)),
                gain_loss_db_random_vs_ub=pct(db(g_rnd)),
                adam_refine_gain_db_over_sumpower_cd=float(10 * np.log10(
                    float(gains_all(th_r, Hf, Bf).mean()) /
                    float(gains_all(th_w, Hf, Bf).mean()))))
            say(f"  B={Bw/1e6:5.0f} MHz K={K:2d}: R_ub {R_ub.mean():.4f} R_wb {R_wb.mean():.4f} "
                f"R_nb {R_nb.mean():.4f} R_rnd {R_rnd.mean():.4f} | dB loss wb "
                f"{np.mean(db(g_wb)):.3f} nb {np.mean(db(g_nb)):.3f}")
        row["seconds"] = time.time() - t0
        res[f"B{int(Bw/1e6)}MHz"] = row
    res["scenarios"] = a.scenarios
    res["snr_scale"] = float(cfg.snr_scale())
    save("gain_loss", res)


# --------------------------------------------------------------------- cost
def part_cost():
    la = float(open("/proc/loadavg").read().split()[0])
    N, T = 32, 8
    ops = {}
    for K in (1,) + KSUBS:
        ops[f"K{K}"] = dict(
            forward_complex_mac=K * N * T,           # h_f = a_f + B_f^T v
            forward_plus_grad_complex_mac=3 * K * N * T,
            cd_sweep_complex_mac=N * 3 * K * T,      # z_n, remove, add per element
            log_evals=K)
    res = dict(load_avg_1min_at_start=la, op_counts=ops,
               note="All per-step costs are linear in K_sub*N*T; the narrowband "
                    "problem is K_sub = 1.")
    if la >= 0.5:
        res["timing"] = "skipped: 1-min load average >= 0.5"
        say(f"  load {la} >= 0.5: timing skipped")
    else:
        torch.manual_seed(0)
        tm = {}
        for batch in (1, 300):
            for K in (1,) + KSUBS:
                A = torch.randn(batch, K, T, dtype=torch.complex64)
                B = torch.randn(batch, K, N, T, dtype=torch.complex64)
                th = torch.zeros(batch, N, requires_grad=True)

                def step():
                    r = rate(gains_all(th, A, B), 1.0).mean()
                    r.backward()

                aw = A.reshape(batch, K * T)
                bw = B.permute(0, 2, 1, 3).reshape(batch, N, K * T)

                def sweep():
                    SV.coord_ascent(aw, bw, torch.zeros(batch, N), sweeps=1)

                out = {}
                for name, fn, reps in (("grad_step_ms", step, 300), ("cd_sweep_ms", sweep, 30)):
                    for _ in range(10):
                        fn()
                    ts = []
                    for _ in range(reps):
                        t0 = time.perf_counter()
                        fn()
                        ts.append(time.perf_counter() - t0)
                    out[name] = float(np.median(ts) * 1e3)
                tm[f"batch{batch}_K{K}"] = out
                say(f"  batch {batch} K {K}: {out}")
        res["timing"] = tm
        res["load_avg_1min_at_end"] = float(open("/proc/loadavg").read().split()[0])
        res["threads"] = torch.get_num_threads()
    save("cost", res)


# ------------------------------------------------------------------- squint
def part_squint():
    rows = []
    cases = [("3 GHz, 8x4 (N=32), D=0.4 m (task value)", 3e9, 32, 0.4),
             ("3 GHz, 8x4 (N=32), D = side 8*lambda/2", 3e9, 32, 8 * C0 / 3e9 / 2),
             ("28 GHz, 16x16 (N=256), D = side 16*lambda/2", 28e9, 256, 16 * C0 / 28e9 / 2),
             ("28 GHz, 32x32 (N=1024), D = side 32*lambda/2", 28e9, 1024, 32 * C0 / 28e9 / 2)]
    for name, fc, n, D in cases:
        for B in (100e6, 400e6):
            full = 2 * np.pi * B * D / C0               # phase spread, band edge to edge
            edge = full / 2                              # edge subcarrier vs fc
            # linear phase ramp of total spread phi across the aperture ->
            # normalised array gain (sin(phi/2)/(phi/2))^2; two-hop RIS
            # geometry can double the delay difference (sin in + sin out)
            loss = {}
            for fac in (1, 2):
                phi = fac * edge
                g = (np.sin(phi / 2) / (phi / 2)) ** 2
                loss[f"edge_gain_loss_db_factor{fac}"] = float(-10 * np.log10(g))
            rows.append(dict(case=name, fc_hz=fc, N=n, D_m=D, B_hz=B,
                             fractional_bw=B / fc,
                             phase_spread_full_band_rad=full,
                             phase_spread_full_band_deg=float(np.degrees(full)),
                             phase_err_edge_vs_centre_deg=float(np.degrees(edge)),
                             **loss))
            say(f"  {name}, B={B/1e6:.0f} MHz: 2piBD/c = {full:.3f} rad "
                f"({np.degrees(full):.1f} deg); edge loss {loss['edge_gain_loss_db_factor1']:.3f} dB "
                f"(x2 geometry {loss['edge_gain_loss_db_factor2']:.3f} dB)")
    save("beam_squint", dict(
        formula="phase spread across aperture D over band B = 2 pi B D / c (end-fire worst "
                "case); edge subcarrier vs centre = half that; gain loss for a linear ramp "
                "phi: -10 log10 sinc^2(phi/2)",
        rows=rows))


parts = ("cost", "squint", "delay", "gain") if a.part == "all" else (a.part,)
for p in parts:
    say(f"== {p}")
    {"delay": part_delay, "gain": part_gain, "cost": part_cost, "squint": part_squint}[p]()
