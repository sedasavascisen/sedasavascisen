"""
Export a single-user MISO dataset (data_sumiso/sumiso_<tag>.npz, written by
scripts/sumiso_dataset.py) to a MATLAB .mat file for
matlab_sumiso/sumiso_cnnlstm_matlab.m. Needs numpy and scipy only.

Fields (single precision):
  B_re, B_im     [S, N, T]  cascaded channel b_n = g_n F_n
  hd_re, hd_im   [S, T]     direct channel
  theta_label    [S, N]     training target: MISO -> optimum with element 1
                            at zero; SISO (T = 1) -> published -angle(g_n F_n)
  theta_opt      [S, N]     coordinate-ascent optimum (for the label rate)
  snr_scale      scalar     rate = log2(1 + snr_scale |h|^2)
  idx_tr, idx_val, idx_te   1-based, the same 70/15/15 split as sumiso_train.py

    python3 scripts/sumiso_export_mat.py --tag train     # MISO, N_t = 8
    python3 scripts/sumiso_export_mat.py --tag siso      # SISO control
"""
import argparse
import pathlib

import numpy as np
import scipy.io as sio

ap = argparse.ArgumentParser()
ap.add_argument("--tag", default="train")
ap.add_argument("--parts", type=int, default=1, help="split along scenarios so each file stays under ~50 MB")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parents[1]
z = np.load(ROOT / "data_sumiso" / f"sumiso_{a.tag}.npz")
F, G, hd = z["F"], z["G"][:, 0, :], z["hd"][:, 0, :]
B = G[:, :, None] * F                                   # [S, N, T]
th = z["theta"]
S, N, T = B.shape
if T == 1:
    lab = -np.angle(B[:, :, 0])
else:
    lab = np.angle(np.exp(1j * (th - th[:, :1])))
perm = np.random.default_rng(0).permutation(S)
ntr, nva = int(0.7 * S), int(0.15 * S)
out = dict(B_re=B.real.astype(np.float32), B_im=B.imag.astype(np.float32),
           hd_re=hd.real.astype(np.float32), hd_im=hd.imag.astype(np.float32),
           theta_label=lab.astype(np.float32), theta_opt=th.astype(np.float32),
           snr_scale=float(z["snr_scale"]),
           idx_tr=(perm[:ntr] + 1).astype(np.float64), idx_val=(perm[ntr:ntr + nva] + 1).astype(np.float64),
           idx_te=(perm[ntr + nva:] + 1).astype(np.float64))
per = ("B_re", "B_im", "hd_re", "hd_im", "theta_label", "theta_opt")
cuts = np.linspace(0, S, a.parts + 1).astype(int)
for k in range(a.parts):
    part = {f: (out[f][cuts[k]:cuts[k + 1]] if f in per else out[f]) for f in out}
    part["row_offset"] = float(cuts[k])          # rows of this part are scenarios row_offset+1 ...
    name = f"sumiso_{a.tag}.mat" if a.parts == 1 else f"sumiso_{a.tag}_part{k + 1}of{a.parts}.mat"
    dst = ROOT / "matlab_sumiso" / name
    sio.savemat(dst, part, do_compression=True)
    print(f"wrote {dst}  rows {cuts[k]}..{cuts[k + 1]}  N={N} T={T}  ({dst.stat().st_size/1e6:.1f} MB)")
