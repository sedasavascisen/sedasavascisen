"""Anten ekseni korelasyonu: kazanclar antene gore bagimsiz cekilince ne oluyor?

UYARI -- IKINCI BLOK GUVENILIR DEGIL, SUPERSEDED.
--------------------------------------------------
Bu dosyanin BIRINCI blogu ("MEVCUT KOD") saglamdir ve teze girebilir:
anten ekseni korelasyonu 0.204 (LoS 0.818, NLoS 0.130), eleman ekseni
0.639, anten etkin rank 7.26/8.

IKINCI blok ("DUZELTILMIS") kazanc paylasiminin bedelini tahmin etmeye
calisir ve YANLIStir: sacicilari ve Ricean K'yi kendi rng'siyle yeniden
cekiyor, dolayisiyla iki kolu farkli senaryolarda karsilastiriyor. Toplam
korelasyonun 0.290 -> 0.085 duserken NLoS'un 0.022 -> 0.294 CIKMASI bu
tutarsizligin isareti.

Kazanc paylasiminin bedeli icin `scripts/mumiso_gain_sharing.py` kullanin:
rastgele akisi koruyarak ayni senaryolarda olcer (capa -%31.98,
PGA -%8.15, optimizasyonun degeri 1.75x -> 2.36x).
"""
import sys
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
import numpy as np
from ris_mu.mumiso.channel import (make_mumiso_scenario, MuMisoChannel,
                                   neighbour_corr, effective_rank)
from ris_mu.channel import _unit_power

panel,cfg = make_mumiso_scenario(n_users=4,n_bs_antennas=8,seed=11)
ch = MuMisoChannel(panel,cfg)
d  = ch.generate(1500)
F, los = d["F"], d["los_ris_bs"]          # F [S,N,T]
T = F.shape[2]

def ant(Fs):                               # satirlar (S,N), kolonlar T
    return neighbour_corr(Fs.reshape(-1, T))
def el(Fs):                                # satirlar (S,T), kolonlar N
    return neighbour_corr(Fs.transpose(0,2,1).reshape(-1, Fs.shape[1]))

print("=== MEVCUT KOD (kazanc her anten icin bagimsiz) ===")
print(f"  anten ekseni komsu korelasyonu : tum {ant(F):.3f}   "
      f"LoS {ant(F[los]):.3f}   NLoS {ant(F[~los]):.3f}")
print(f"  eleman ekseni                  : tum {el(F):.3f}")
print(f"  anten ekseni etkin rank        : {effective_rank(F.reshape(-1,T)):.2f} / {T}")

# --- ayni fizik, ama kazanclar anten ekseninde PAYLASILMIS -------------
print("\n=== DUZELTILMIS (her sacici icin TEK kazanc, antenler paylasiyor) ===")
P, k = ch.panel, ch.k
rng = np.random.default_rng(0)
S, L = len(F), cfg.n_clusters
bsa  = d["bs_array"]                       # [S,T,3]
scat = rng.uniform([0,0,0], np.asarray(cfg.room,float), (S,L,3))
kap_lin = 10**(ch.pl.rice_k_db(rng, S)/10)

def ris_link(gains_shape):
    d_el = P.distances(bsa)                            # [S,T,N]
    gain = P.pattern(bsa)
    h_los = _unit_power(np.sqrt(gain)/np.maximum(d_el,1.0)
                        * np.exp(-1j*k*d_el))
    d1 = np.linalg.norm(bsa[...,None,:] - scat[:,None], axis=-1)   # [S,T,L]
    d2 = P.distances(scat[:,None])                                 # [S,1,L,N]
    g_s = P.pattern(scat[:,None])
    g = (rng.standard_normal(gains_shape)+1j*rng.standard_normal(gains_shape))/np.sqrt(2)
    if gains_shape == (S,1,L): g = np.broadcast_to(g,(S,T,L))
    amp = np.sqrt(g_s)/np.maximum(d1[...,None]*d2,1.0)
    h_nlos = _unit_power(np.sum(g[...,None]*amp
                                * np.exp(-1j*k*(d1[...,None]+d2)), axis=-2))
    kp = np.where(los, kap_lin, 0.0)[:,None,None]
    return (np.sqrt(kp/(kp+1))*h_los + np.sqrt(1/(kp+1))*h_nlos).transpose(0,2,1)

F_ind = ris_link((S,T,L))      # mevcut davranis, yeniden uretilmis
F_shr = ris_link((S,1,L))      # kazanclar antenler arasinda paylasilmis
for nm,Fx in (("bagimsiz (mevcut)",F_ind), ("paylasilmis (dogru)",F_shr)):
    print(f"  {nm:22} anten korelasyonu {ant(Fx):.3f}  "
          f"(NLoS {ant(Fx[~los]):.3f})  etkin rank {effective_rank(Fx.reshape(-1,T)):.2f}/{T}")
