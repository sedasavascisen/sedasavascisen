"""Kazanc paylasiminin bedeli -- rastgele AKIS korunarak.

Onemli: _crandn ayni SAYIDA deger tuketmeli, yoksa akis kayar ve
senaryolar da degisir (ilk denemem tam bu yuzden gecersizdi).
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np, torch
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   to_torch, neighbour_corr, effective_rank)
from ris_mu.mumiso import system as S, baselines as B

class SharedGainChannel(MuMisoChannel):
    def _crandn(self, shape):
        g = super()._crandn(shape)            # AYNI sayida deger tuket
        if len(shape) == 3 and shape[1] == self.T:        # (S,T,L)
            return np.broadcast_to(g[:, :1], shape).copy()
        if len(shape) == 4 and shape[2] == self.T:        # (S,K,T,L)
            return np.broadcast_to(g[:, :, :1], shape).copy()
        return g

NS=1200
def build(cls):
    panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
    return cls(panel,cfg).generate(NS), cfg

res={}
for nm,cls in (("mevcut (bagimsiz)",MuMisoChannel),
               ("paylasilmis (fiziksel)",SharedGainChannel)):
    d,cfg = build(cls); res[nm]=(d,cfg)

# akis korundu mu? senaryolar ayni mi?
d0=res["mevcut (bagimsiz)"][0]; d1=res["paylasilmis (fiziksel)"][0]
same = (np.abs(d0["ue_pos"]-d1["ue_pos"]).max()==0
        and (d0["los_ris_bs"]==d1["los_ris_bs"]).all()
        and (d0["los_ris_ue"]==d1["los_ris_ue"]).all())
print(f"ayni senaryolar (konum + LoS): {'EVET - karsilastirma gecerli' if same else 'HAYIR - gecersiz'}")
print(f"  G farki (0 olmamali, kazanclar degisti): {np.abs(d0['G']-d1['G']).max():.3e}")
print(f"  hd farki: {np.abs(d0['hd']-d1['hd']).max():.3e}")
print(f"  F farki : {np.abs(d0['F']-d1['F']).max():.3e}\n")

print(f"{'model':>22}{'anten kor.':>12}{'NLoS':>8}{'anten rank':>12}"
      f"{'capa':>10}{'PGA':>10}")
print("-"*74)
vals={}
for nm,(d,cfg) in res.items():
    F,G,hd,_ = to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
    T=F.shape[2]; los=d["los_ris_bs"]
    ac=neighbour_corr(d["F"].reshape(-1,T))
    an=neighbour_corr(d["F"][~los].reshape(-1,T))
    er=effective_rank(d["F"].reshape(-1,T))
    R0,_=B.su_average(F,G,hd,pt,nv); r0=S.rate_metrics(R0)["min_rate"]
    Rp,_=B.pga(F[:300],G[:300],hd[:300],pt,nv); rp=S.rate_metrics(Rp)["min_rate"]
    vals[nm]=(ac,an,er,r0,rp)
    print(f"{nm:>22}{ac:12.3f}{an:8.3f}{er:12.2f}{r0:10.4f}{rp:10.4f}")
a,b=vals["mevcut (bagimsiz)"],vals["paylasilmis (fiziksel)"]
print(f"\nfiziksel modelin bedeli: capa %{100*(b[3]/a[3]-1):+.2f}   PGA %{100*(b[4]/a[4]-1):+.2f}")
print(f"anten korelasyonu: {a[0]:.3f} -> {b[0]:.3f}   NLoS: {a[1]:.3f} -> {b[1]:.3f}")
print(f"anten etkin rank : {a[2]:.2f} -> {b[2]:.2f} / 8")
