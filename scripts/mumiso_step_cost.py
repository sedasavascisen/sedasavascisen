"""Bir ogrenilen adim, bir Adam adiminin kac katina mal oluyor?

Esit L karsilastirmasi gecikme iddiasinin YERINE GECMEZ: ogrenilen adim
basina (a) r_rel icin bir rates cagrisi, (b) gradyan icin bir ileri+geri,
(c) agin kendisi (CNN+LSTM, exchange modunda K kez) var. Adam adimi
yalnizca (b)'yi yapiyor. Yani esit adim, ogrenilen modele avantajdir.
"""
import sys, time, json
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
torch.set_num_threads(1)          # konuslandirma senaryosu: tek cekirdek
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso.features import mumiso_features
from ris_mu.mumiso.unrolled import UnrolledMuMiso
from ris_mu.mumiso import system as S, baselines as B

panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(64)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
phi=S.su_align_phase(F,G,hd)
X=torch.from_numpy(mumiso_features(d["F"],d["G"],d["hd"],phi.numpy()))
_,TH0=B.su_average(F,G,hd,pt,nv)
one=slice(0,1)

def t_adam(L, reps=40):
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
    return np.median(ts)*1e3

def t_learned(L, reps=40):
    net=UnrolledMuMiso(N=N,n_users=4,n_tx=8,steps=L,mode="exchange",use_grad=True)
    net.load_state_dict(torch.load(_pl.Path(__file__).resolve().parents[1]
                              / f"results/mumiso_eqstep_L{L}.pt")); net.eval()
    for _ in range(3):
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter()
        with torch.no_grad(): net(X[one],F[one],G[one],hd[one],pt,nv,TH0[one])
        ts.append(time.perf_counter()-t0)
    return np.median(ts)*1e3

print(f"{'L':>3}{'Adam [ms]':>12}{'ogrenilen [ms]':>16}{'maliyet orani':>15}")
print("-"*46)
out={}
for L in (1,2,4,8,16):
    a,b=t_adam(L),t_learned(L)
    out[L]=(a,b)
    print(f"{L:3d}{a:12.3f}{b:16.3f}{b/a:15.2f}x")
a1=(out[1][0]); b1=(out[1][1])
print(f"\nadim basina: Adam {a1:.3f} ms, ogrenilen {b1:.3f} ms -> {b1/a1:.2f}x")
json.dump({str(k):{'adam_ms':v[0],'learned_ms':v[1]} for k,v in out.items()},
          open(_pl.Path(__file__).resolve().parents[1]
               / "results/mumiso_step_cost.json","w"), indent=1)
print("wrote results/mumiso_step_cost.json")
