"""
28 GHz version of the aging set for jury question 5. Identical to thesis_exp/p4/common.Aging except that the RIS panel
is built with fc = 28 GHz (element spacing lambda/2 at 28 GHz; 3GPP path loss at panel.fc; BS ULA spacing 0.5 lambda),
by replicating ris_mu.mumiso.channel.make_mumiso_scenario's wall-mount geometry here (the package is not modified).
Link budget: 20 dBm, 20 MHz, NF 7 dB, plus a fixed compensation comp_db (raw/link_budget.json, training seed 21)
that equalises the mean incoherent received power with the 3 GHz set; compensate=False gives the raw budget.
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "p4"))
import numpy as np, torch
from common import Aging, ROOT, commit                             # noqa: F401
from ris_mu.geometry import RISPanel
from ris_mu.mumiso.channel import MuMisoConfig
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B

FC28 = 28e9


def make28(seed, n_users=4, n_bs_antennas=8, M=8, K=4):
    cfg = MuMisoConfig(n_users=n_users, n_bs_antennas=n_bs_antennas, seed=seed)
    room = np.asarray(cfg.room, float)
    assert cfg.mount == "wall"
    panel = RISPanel(M=M, K=K, fc=FC28, center=(room[0] / 2, 0.1, 3.0), e1=(1, 0, 0), e2=(0, 0, 1), normal=(0, 1, 0))
    return panel, cfg


class Aging28(Aging):
    """Same interface as common.Aging (times must start with 0.0)."""

    def __init__(self, seed, times, v=1.5, n=400, clusters=20, compensate=True):
        torch.manual_seed(0)
        panel, base = make28(seed)
        self.cfg = MobileConfig(**{**base.__dict__, "velocity": v, "times_ms": tuple(times), "n_clusters": clusters})
        self.gen = MobileMuMisoChannel(panel, self.cfg)
        self.d = self.gen.generate(n)
        self.times = list(times)
        self.F = torch.as_tensor(self.d["F"], dtype=torch.complex64)
        self.G = [torch.as_tensor(self.d["G_t"][:, m], dtype=torch.complex64) for m in range(len(times))]
        self.H = [torch.as_tensor(self.d["hd_t"][:, m], dtype=torch.complex64) for m in range(len(times))]
        comp = json.load(open(pathlib.Path(__file__).parent / "raw/link_budget.json"))["comp_db"] if compensate else 0.0
        self.comp_db = comp
        self.pt, self.nv, self.n, self.N = 1.0, 10 ** (-comp / 10) / self.cfg.snr_scale(), n, panel.positions.shape[0]
        self.fd = v * FC28 / panel.c
