# Verification U59 (round 8; copied from the verifier's scratch script): fix1 multiplies the time-mixed rate by (1 - pilot overlap); exact = integrate only data time.
import sys, json, time
sys.path.insert(0, "/home/user/sedasavascisen")
import numpy as np, torch
torch.set_num_threads(1); torch.manual_seed(0)
from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel
from ris_mu.mumiso import system as S, baselines as B
DT=0.5; TIMES=tuple(float(x) for x in np.arange(0.0,200.0+DT/2,DT)); M=len(TIMES); MSS=13.3/8; WINDOW=(100.0,200.0)
panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=11)
cfg = MobileConfig(**{**base.__dict__, "velocity": 1.5, "times_ms": TIMES, "n_clusters": 20})
d = MobileMuMisoChannel(panel, cfg).generate(400); N = panel.positions.shape[0]
pt, nv = 1.0, 1.0/cfg.snr_scale()
F=torch.as_tensor(d["F"],dtype=torch.complex64); G=torch.as_tensor(d["G_t"],dtype=torch.complex64); H=torch.as_tensor(d["hd_t"],dtype=torch.complex64)
_, th0 = B.su_average(F, G[:,0], H[:,0], pt, nv)
mr=lambda th,m: S.rates(F,G[:,m],H[:,m],torch.cos(th),torch.sin(th),pt,nv,"zf").min(-1).values.numpy()
def adam(start,m,L):
    dl=torch.zeros(400,N,requires_grad=True); opt=torch.optim.Adam([dl],lr=0.5)
    for _ in range(L):
        th=start+dl; R=S.rates(F,G[:,m],H[:,m],torch.cos(th),torch.sin(th),pt,nv,"zf")
        (-(-torch.logsumexp(-8.0*R,-1)/8.0).mean()).backward(); opt.step(); opt.zero_grad()
    return start+dl.detach()
grid=lambda t:int(round(t/DT))
def sim(L,t_p,warm,period):
    busy=t_p+L*MSS; cyc=busy if period is None else period
    dep={}; ev=[]; piv=[]; snap=0.0
    while snap<TIMES[-1]:
        m=grid(snap)
        if warm:
            ks=[k for k in dep if k<=m]; st=dep[max(ks)] if ks else th0
        else: st=B.su_average(F,G[:,m],H[:,m],pt,nv)[1]
        th=adam(st,m,L)
        if grid(snap+busy)<M: dep[grid(snap+busy)]=th
        if snap+busy<=TIMES[-1]+DT: ev.append((snap+busy,th))
        if t_p>0: piv.append((snap,snap+t_p))
        snap+=cyc
    if not ev or min(ev)[0]>WINDOW[0] or TIMES[min(dep)]>WINDOW[0]: return None
    ev.sort(key=lambda e:e[0]); sel=[m for m in range(M) if WINDOW[0]<=TIMES[m]<=WINDOW[1]]
    prod=np.zeros((400,len(sel))); exact=np.zeros((400,len(sel))); nmix=0
    for j,m in enumerate(sel):
        a,b=TIMES[m],TIMES[m]+DT
        bef=[e for e in ev if e[0]<=a]; cuts=[(a,bef[-1][1] if bef else th0)]+[(t,ph) for t,ph in ev if a<t<b]
        acc=np.zeros(400); ex=np.zeros(400)
        for i,(t0,ph) in enumerate(cuts):
            t1=cuts[i+1][0] if i+1<len(cuts) else b
            r=mr(ph,m); acc+=(t1-t0)/DT*r
            pil=sum(max(0.0,min(t1,q1)-max(t0,q0)) for q0,q1 in piv)
            ex+=((t1-t0)-pil)/DT*r
        ov=sum(max(0.0,min(b,q1)-max(a,q0)) for q0,q1 in piv)
        if len(cuts)>1 and ov>0: nmix+=1
        prod[:,j]=acc*max(0.0,1-ov/DT); exact[:,j]=ex
    return prod.mean(1).astype(np.float32), exact.mean(1), nmix

tf=json.load(open("/home/user/sedasavascisen/thesis_exp/p4/takip_duzeltme/raw/fix1_tp%s.json"%sys.argv[1]))
key=list(tf["runs"])[0]; tp=float(key)
STEPS=[1,2,3,4,6,8,12,16,24,48]; PERIODS=[None,10.0,20.0,40.0,80.0]
rng=np.random.default_rng(0); idx=rng.integers(0,400,(2000,400))
res={}; best={}
for mode in ("cold","warm"):
    P={}; E={}
    for U in PERIODS:
        for L in STEPS:
            busy=tp+L*MSS; cyc=busy if U is None else U
            if busy>cyc+1e-9: continue
            r=sim(L,tp,mode=="warm",U)
            if r is None: continue
            P[(U,L)],E[(U,L)],_=r
    stored=tf["runs"][key][mode]["mean"]
    maxdev=max(abs(float(P[k].mean())-stored[f"{'b2b' if k[0] is None else k[0]}|{k[1]}"]) for k in P)
    assert len(P)==len(stored),(len(P),len(stored))
    me={k:float(v.mean()) for k,v in E.items()}; kb=max(me,key=me.get)
    near=[k for k in E if np.percentile((E[kb]-E[k])[idx].mean(1),2.5)<=0]
    best[mode]=E[kb]
    res[mode]=dict(prod_vs_stored_maxdev=maxdev,best=[kb[0],kb[1],me[kb]],near=[[k[0],k[1]] for k in near],
                   max_abs_exact_minus_prod=max(abs(me[k]-float(P[k].mean())) for k in P))
    print(mode,res[mode],flush=True)
dd=best["warm"]-best["cold"]
res["warm_minus_cold_exact"]=dict(diff=float(dd.mean()),ci=[float(np.percentile(dd[idx].mean(1),q)) for q in (2.5,97.5)])
res["warm_minus_cold_stored"]=tf["warm_minus_cold"][key]
print(res["warm_minus_cold_exact"],res["warm_minus_cold_stored"])
json.dump(res,open(f"/home/user/sedasavascisen/thesis_exp/p4/takip_duzeltme/raw/exact_full_tp{sys.argv[1]}.json","w"),indent=1)
