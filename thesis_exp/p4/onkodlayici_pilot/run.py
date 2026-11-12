"""
Prompt 4.3 — charge the precoder-refresh pilots as airtime and sweep the refresh period.

The thesis assumes the ZF precoder W is recomputed from the CURRENT effective channel at every instant,
for free. Here W is refreshed every R ms from an effective-channel estimate (perfect estimate, K = 4
orthogonal pilot symbols, one per user); between refreshes the last W is used on the true, changing
channel; during the pilot symbols no data is sent (charged as the data fraction 1 - t_p/R). The RIS phase is fixed at t = 0 (the arm's latency is
added to the deployment time, as in Definition 1).
Pilot symbol duration (NR, one OFDM symbol incl. CP): 71.4 / 35.7 / 17.9 us at 15 / 30 / 60 kHz
(3.43 / 1.71 / 0.86 ms per 48 symbols, the values used in the paper).
Reported: time-averaged min-user rate over the window [deploy, deploy + 50 ms] (about 2 coherence times
at 1.5 m/s) for R in R_GRID and the three numerologies, against
  fresh     W recomputed at every grid point, no pilot cost (the paper's assumption)
  never     W from the deployment instant only.
Phases: SU-best-of and SU-average + Adam-6 (step 0.5), both from the t = 0 channel.
Output: thesis_exp/p4/onkodlayici_pilot/raw/results.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from common import Aging, adam_latency, LAT, boot, commit, check_same_scenarios
from ris_mu.mumiso import system as S
torch.set_num_threads(2)
OUT = pathlib.Path(__file__).parent / "raw"; OUT.mkdir(exist_ok=True)
DT = 0.1
GRID = [round(float(x), 4) for x in np.arange(0.0, 70.0 + DT / 2, DT)]
R_GRID = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
SYM_MS = {"15kHz": 3.43 / 48, "30kHz": 1.71 / 48, "60kHz": 0.86 / 48}
K_PILOTS = 4
WIN = 50.0

A = Aging(11, GRID)
chk = check_same_scenarios(A)


def He(th, m):
    return S.effective_channel(A.F, A.G[m], A.H[m], torch.cos(th), torch.sin(th))


def rate_with(th, m, m_ref):
    """min-user rate at grid m with W computed from the effective channel at grid m_ref."""
    W = S.precode(He(th, m_ref), A.pt, "zf", noise_var=A.nv)
    return torch.log2(1.0 + S.sinr(He(th, m), W, A.nv)).min(-1).values


def run(th, lat):
    m_dep = int(round(lat / DT))
    sel = [m for m in range(len(GRID)) if lat <= GRID[m] <= lat + WIN]
    fresh = np.stack([rate_with(th, m, m).numpy() for m in sel], 1).mean(1)
    never = np.stack([rate_with(th, m, m_dep).numpy() for m in sel], 1).mean(1)
    out = dict(fresh=float(fresh.mean()), never=float(never.mean()), by={})
    for num, sym in SYM_MS.items():
        tp = K_PILOTS * sym
        out["by"][num] = {}
        for Rr in R_GRID:
            vals = []
            for m in sel:
                since = GRID[m] - lat
                k = int(np.floor(since / Rr + 1e-9))
                t_ref = lat + k * Rr
                m_ref = int(round(t_ref / DT))
                vals.append(rate_with(th, m, m_ref).numpy())
            # pilots occupy tp ms of every R ms period (no data): charged as the data fraction 1 - tp/R
            # (exact for a rate that is constant within the pilot interval; avoids 0.1 ms grid rounding of tp)
            v = np.stack(vals, 1).mean(1) * max(0.0, 1.0 - tp / Rr)
            out["by"][num][str(Rr)] = dict(rate=float(v.mean()), ci=boot(v), minus_fresh=float((v - fresh).mean()),
                                           minus_fresh_ci=boot(v - fresh), pilot_fraction=min(1.0, tp / Rr))
        bestR = max(out["by"][num], key=lambda r: out["by"][num][r]["rate"])
        out["by"][num]["best_R_ms"] = float(bestR)
        print(f"  {num}: best R {bestR} ms -> {out['by'][num][bestR]['rate']:.4f}  (fresh {out['fresh']:.4f}, never {out['never']:.4f})", flush=True)
    return out


res = dict(commit=commit(), su_average_t0_check=chk, window_ms=WIN, grid_ms=DT, pilots_per_refresh=K_PILOTS, symbol_ms=SYM_MS, phases={})
th_best = A.su_best_of()
print("SU-best-of", flush=True); res["phases"]["SU-best-of"] = run(th_best, LAT["su_best_of"])
th_adam = A.adam(A.su_average(), 6)
print("Adam-6", flush=True); res["phases"]["Adam-6"] = run(th_adam, adam_latency(6))
json.dump(res, open(OUT / "results.json", "w"), indent=1)
print("wrote", OUT / "results.json")
