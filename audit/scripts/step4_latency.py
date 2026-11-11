"""
Audit step 4: parameter counts and inference latency vs N (32, 64, 128, 256), CLAUDE.md timing rule:
one thread, same machine, median over reps per round, several rounds, load average before/after.
Waits until the 1-min load average is below 0.5.

Arms (untrained weights: latency does not depend on weight values):
  cnnlstm_fixed   published layer stack, LSTM 128/64 at every N
  cnnlstm_sqrt    LSTM sizes {128,64}*(N/32)^0.5 rounded to a power of two (comment in scalability_analysis.m)
  fcdnn_direct    transformer_baseline.m MLP
  cd_k5_python    ris_CD.m algorithm (sequential per-element closed-form update, K=5) in NumPy;
                  Python loop cost, NOT MATLAB's
Two latency notions, both recorded: single sample (one channel realisation, sequential calls) and
batch throughput (time for a batch of B samples / B), the latter being how theta_NN_multioutput.m
computes t_per_sample.
Output: audit/raw/step4_latency.json
"""
import os, sys, json, time, pathlib, subprocess, importlib.util
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, torch
from m1_data import generate
torch.set_num_threads(1)
ROOT = pathlib.Path(__file__).resolve().parents[2]
load0 = os.getloadavg()[0]
while os.getloadavg()[0] >= 0.5:
    time.sleep(10)
load1 = os.getloadavg()[0]

import torch.nn as nn
def pow2(x): return int(2 ** round(np.log2(x)))
class CNNLSTM(nn.Module):
    def __init__(self, h1, h2):
        super().__init__()
        self.cnn = nn.Sequential(nn.Conv1d(4, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(),
                                 nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2))
        self.l1 = nn.LSTM(64, h1, batch_first=True); self.l2 = nn.LSTM(h1, h2, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(0.3), nn.Linear(h2, 2))
    def forward(self, x):
        h = self.cnn(x).transpose(1, 2); h, _ = self.l1(h); h, _ = self.l2(h); return self.out(h)
class FCDNN(nn.Module):
    def __init__(self, N):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(4 * N, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.2),
                                 nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.2),
                                 nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, N))
    def forward(self, x): return self.net(x)

def cd_k5(F, G, hd, K=5):
    N = F.shape[0]; th = np.zeros(N); b = G * F
    for _ in range(K):
        for n in range(N):
            m = np.ones(N, bool); m[n] = False
            Hm = hd + np.sum(b[m] * np.exp(1j * th[m]))
            th[n] = np.angle(np.exp(1j * (np.angle(Hm) - np.angle(b[n]))))
    return th

REPS, ROUNDS, NS, BATCH = 50, 3, 20, 1000
res = dict(load_avg=dict(start=load0, before_timing=load1), threads=1, reps=REPS, rounds=ROUNDS, scenarios_per_round=NS,
           batch=BATCH, cpu=open('/proc/cpuinfo').read().split('model name')[1].split('\n')[0].strip(': \t'),
           torch=torch.__version__, commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           arms={})
for N in (32, 64, 128, 256):
    D = generate(max(NS, 64) + BATCH, N=N, seed=123)
    X = torch.tensor(np.stack([D["F"].real, D["F"].imag, D["G"].real, D["G"].imag], 1).astype(np.float32))
    Xf = X.transpose(1, 2).reshape(len(X), -1) if False else torch.cat([X[:, 0], X[:, 1], X[:, 2], X[:, 3]], 1)
    s = (N / 32) ** 0.5
    arms = {"cnnlstm_fixed": (CNNLSTM(128, 64), X), "cnnlstm_sqrt": (CNNLSTM(pow2(128 * s), pow2(64 * s)), X),
            "fcdnn_direct": (FCDNN(N), Xf)}
    for name, (m, inp) in arms.items():
        m.eval(); torch.manual_seed(0)
        single, batch = [], []
        with torch.no_grad():
            for r in range(ROUNDS):
                per = []
                for i in range(NS):
                    x = inp[i:i + 1]; m(x)
                    t = []
                    for _ in range(REPS):
                        t0 = time.perf_counter(); m(x); t.append(time.perf_counter() - t0)
                    per.append(np.median(t) * 1e3)
                single.append(float(np.median(per)))
                xb = inp[64:64 + BATCH]; m(xb)
                tb = []
                for _ in range(5):
                    t0 = time.perf_counter(); m(xb); tb.append(time.perf_counter() - t0)
                batch.append(float(np.median(tb) * 1e3 / BATCH))
        res["arms"].setdefault(name, {})[str(N)] = dict(
            params=int(sum(p.numel() for p in m.parameters())), single_ms_rounds=single, single_ms=float(np.median(single)),
            batch_per_sample_ms_rounds=batch, batch_per_sample_ms=float(np.median(batch)))
        print(N, name, res["arms"][name][str(N)]["params"], res["arms"][name][str(N)]["single_ms"], res["arms"][name][str(N)]["batch_per_sample_ms"], flush=True)
    single = []
    for r in range(ROUNDS):
        per = []
        for i in range(NS):
            t = []
            for _ in range(5):
                t0 = time.perf_counter(); cd_k5(D["F"][i], D["G"][i], D["hd"][i]); t.append(time.perf_counter() - t0)
            per.append(np.median(t) * 1e3)
        single.append(float(np.median(per)))
    res["arms"].setdefault("cd_k5_python", {})[str(N)] = dict(single_ms_rounds=single, single_ms=float(np.median(single)))
    print(N, "cd_k5_python", np.median(single), flush=True)
res["load_avg"]["after_timing"] = os.getloadavg()[0]
json.dump(res, open(ROOT / "audit" / "raw" / "step4_latency.json", "w"), indent=1)
print("wrote audit/raw/step4_latency.json", res["load_avg"])
