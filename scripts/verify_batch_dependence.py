"""zf()'nin regulatoru yigin ortalamasina bagli mi? Olcelim."""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(600)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
_,TH=B.su_average(F,G,hd,pt,nv)

def rates_for(idx, chunk):
    """idx senaryolarinin hizlari, 'chunk' buyuklugunde parcalarla hesaplanmis."""
    out=[]
    for i in range(0,len(idx),chunk):
        s=idx[i:i+chunk]
        R=S.rates(F[s],G[s],hd[s],torch.cos(TH[s]),torch.sin(TH[s]),pt,nv,"zf")
        out.append(R.min(-1).values)
    return torch.cat(out)

idx=torch.arange(600)
ref=rates_for(idx,600)          # hepsi tek cagrida
print(f"{'yigin boyu':>12}{'ortalama min hiz':>18}{'ref ile max sapma':>20}{'ortalama |sapma|':>18}")
for c in (600,300,100,50,10,1):
    r=rates_for(idx,c)
    dmax=(r-ref).abs().max().item()
    dmean=(r-ref).abs().mean().item()
    print(f"{c:12d}{r.mean().item():18.6f}{dmax:20.3e}{dmean:18.3e}")

print("\n--- ayni senaryo, farkli komsularla ---")
# senaryo 0'i tek basina, ve 599 baska senaryoyla birlikte olc
alone=rates_for(torch.tensor([0]),1).item()
with_others=ref[0].item()
print(f"  senaryo 0 tek basina        : {alone:.6f}")
print(f"  senaryo 0, 600'lu yiginda   : {with_others:.6f}")
print(f"  fark                        : {abs(alone-with_others):.3e}"
      f"  (%{100*abs(alone-with_others)/max(alone,1e-9):.3f})")

print("\n--- senaryo basina regulator ne verirdi? ---")
He=S.effective_channel(F,G,hd,torch.cos(TH),torch.sin(TH))
M=He@He.conj().transpose(-1,-2)
dg=torch.diagonal(M,dim1=-2,dim2=-1).real
per=dg.mean(-1)                      # senaryo basina
glob=dg.mean()                       # yigin geneli
print(f"  yigin geneli p_sig  : {glob.item():.4e}")
print(f"  senaryo basina p_sig: min {per.min().item():.4e}  "
      f"medyan {per.median().item():.4e}  max {per.max().item():.4e}")
print(f"  en zayif/en guclu orani : {(per.max()/per.min()).item():.1f}x")
print(f"  en zayif senaryo icin regulator {glob.item()/per.min().item():.1f}x fazla buyuk")
