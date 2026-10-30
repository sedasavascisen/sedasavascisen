"""Sabit MMSE regulatoru zayif senaryolari sakatliyor mu?"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import torch
from ris_mu.mumiso.channel import make_mumiso_scenario, MuMisoChannel, to_torch
from ris_mu.mumiso import system as S, baselines as B

torch.manual_seed(0)
panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
N=panel.positions.shape[0]
d=MuMisoChannel(panel,cfg).generate(1200)
F,G,hd,_=to_torch(d); pt,nv=1.0,1.0/cfg.snr_scale()
K=4
_,TH=B.su_average(F,G,hd,pt,nv)
He=S.effective_channel(F,G,hd,torch.cos(TH),torch.sin(TH))
M=He@He.conj().transpose(-1,-2)
p_per=torch.diagonal(M,dim1=-2,dim2=-1).real.mean(-1)     # senaryo basina
lam = K*nv/pt
rel = lam/p_per                                            # kendi olcegine gore
print(f"MMSE lam (sabit)        : {lam:.4e}")
print(f"lam / kendi p_sig'i  -> medyan {rel.median():.3e}  "
      f"%90 {rel.quantile(0.9):.3e}  max {rel.max():.3e}")
print("\ndocstring'in kendi tablosu: 1e-6 bagil -> MRT'ye cokme, 3.4e-3 -> %55 kayip")
for thr,lbl in ((1e-6,"1e-6 (cokme esigi)"),(1e-3,"1e-3"),(1e-2,"1e-2"),(1e-1,"1e-1")):
    f=(rel>thr).float().mean().item()
    print(f"  bagil regulator > {lbl:20} : senaryolarin %{100*f:.1f}'i")

def minrate(eps_abs=None):
    W = S.zf(He,pt,eps_abs=eps_abs) if eps_abs is not None else S.zf(He,pt,noise_var=nv)
    return torch.log2(1+S.sinr(He,W,nv)).min(-1).values

r_mmse = minrate()
r_pure = minrate(eps_abs=0.0)
print(f"\n{'':22}{'MMSE (varsayilan)':>20}{'saf ZF (eps=0)':>18}{'fark':>12}")
print(f"{'tum 1200 senaryo':22}{r_mmse.mean():20.4f}{r_pure.mean():18.4f}"
      f"{100*(r_pure.mean()/r_mmse.mean()-1):11.2f}%")
# zayif kuyruk: kendi olcegine gore en cok regulatör yiyen %10
hard = rel.argsort(descending=True)[:120]
print(f"{'en kotu %10 (kuyruk)':22}{r_mmse[hard].mean():20.4f}{r_pure[hard].mean():18.4f}"
      f"{100*(r_pure[hard].mean()/r_mmse[hard].mean()-1):11.2f}%")
easy = rel.argsort()[:120]
print(f"{'en iyi %10':22}{r_mmse[easy].mean():20.4f}{r_pure[easy].mean():18.4f}"
      f"{100*(r_pure[easy].mean()/r_mmse[easy].mean()-1):11.2f}%")
print(f"\nkuyrukta kac senaryo MRT'ye cokmus (bagil>1e-6): "
      f"{(rel[hard]>1e-6).sum().item()}/120")
