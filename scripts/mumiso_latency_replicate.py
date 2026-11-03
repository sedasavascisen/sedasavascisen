"""Re-run of mumiso_latency_repeat.py that also records the load average,
the CPU model and the per-round dominance verdict (the original logs none of
them). Timing code is copied unchanged; only the output file differs. Needs
the weights archive (results/mumiso_eqstep_L*.pt). Run on an idle machine:
check `cat /proc/loadavg` < 0.5 first."""

import sys, time, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
LOAD0=float(open("/proc/loadavg").read().split()[0])
CPU=next((l.split(":",1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")),"unknown")
torch.set_num_threads(1)
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

panel,cfg=make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(64)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
phi=S.su_align_phase(F,G,hd)
X=torch.from_numpy(mumiso_features(d["F"],d["G"],d["hd"],phi.numpy()))
_,TH0=B.su_average(F,G,hd,pt,nv)
one=slice(0,1)

def t_adam(L,reps=25):
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        dl=torch.zeros(1,N,requires_grad=True)
        opt=torch.optim.Adam([dl],lr=0.75)
        for _ in range(L):
            th=TH0[one]+dl
            R=S.rates(F[one],G[one],hd[one],torch.cos(th),torch.sin(th),pt,nv,"zf")
            loss=-(-torch.logsumexp(-8.0*R,-1)/8.0).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        ts.append(time.perf_counter()-t0)
    return float(np.median(ts)*1e3)

NETS={}
def t_learned(L,reps=25):
    if L not in NETS:
        n=UnrolledMuMiso(N=N,n_users=4,n_tx=8,steps=L,mode="exchange",use_grad=True)
        n.load_state_dict(torch.load(_pl.Path(__file__).resolve().parents[1]
                              / f"results/mumiso_eqstep_L{L}.pt")); n.eval()
        NETS[L]=n
    net=NETS[L]
    with torch.no_grad():
        for _ in range(3): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
        ts.append(time.perf_counter()-t0)
    return float(np.median(ts)*1e3)

LB=[1,2,4,8,16]; CB=[1,2,4,8,16,24,32,48]
rounds={'learned':{L:[] for L in LB}, 'adam':{L:[] for L in CB}}
for r in range(5):
    for L in LB: rounds['learned'][L].append(t_learned(L))
    for L in CB: rounds['adam'][L].append(t_adam(L))
    print(f"  tur {r+1}/5 bitti", flush=True)

print(f"\n{'':>10}{'medyan':>9}{'min':>9}{'max':>9}{'max/min':>9}")
for arm in ('learned','adam'):
    print(f"-- {arm}")
    for L,v in rounds[arm].items():
        v=np.array(v)
        print(f"{'L='+str(L):>10}{np.median(v):9.2f}{v.min():9.2f}{v.max():9.2f}"
              f"{v.max()/v.min():9.2f}x")

# hizlar 23 Ekim olcumunden (ayni test kumesi, degismedi)
RATE_L={1:4.4599,2:4.8792,4:5.2855,8:5.5932,16:5.8003}
RATE_A={1:4.3810,2:4.6927,4:5.0253,8:5.3800,16:5.7389,24:5.9110,32:6.0132,48:6.1072}

print("\n=== baskinlik hukmu her turda ayni mi? ===")
stab={L:[] for L in LB}
for r in range(5):
    for L in LB:
        lms=rounds['learned'][L][r]; lr_=RATE_L[L]
        dom=[k for k in CB if rounds['adam'][k][r]<=lms and RATE_A[k]>=lr_]
        stab[L].append(bool(dom))
for L in LB:
    n=sum(stab[L])
    print(f"  ogrenilen L={L:<3}: 5 turun {n}'inde BASKINLANMIS  {stab[L]}")
out={k:{str(a):b for a,b in v.items()} for k,v in rounds.items()}
out.update(cpu=CPU, threads=1, load_before=LOAD0,
           load_after=float(open("/proc/loadavg").read().split()[0]),
           dominated_rounds={str(L):stab[L] for L in LB})
json.dump(out, open(_pl.Path(__file__).resolve().parents[1]
               / "results/mumiso_latency_replicate.json","w"), indent=1)
print(f"\nload {LOAD0} -> {out['load_after']}; CPU {CPU}")
print("wrote results/mumiso_latency_replicate.json")
