"""
Bit-identity check for the opt-in wideband option of MobileMuMisoChannel.

Compares, with np.array_equal, every default output key of
  (1) the generator as of commit REF (before the wideband option existed),
  (2) the current generator with the option off, and
  (3) the current generator with freq_offsets_hz given,
on the thesis aging scenario (make_mumiso_scenario, 8-antenna BS, 20
scatterers) for 1 user and 4 users, several chunk sizes, two seeds.
Also checks that the wideband arrays at df = 0 reproduce the narrowband
ones (to float32 rounding; the operation order differs, so not bitwise).

Usage: python3 scripts/wideband_bitidentity_check.py   (~10 s)
Writes results/wideband_bitidentity_check.json.
"""
import sys, json, pathlib, subprocess, importlib.util
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import ris_mu.mumiso  # noqa: F401  (parent package for the old module)
from ris_mu.mumiso.channel import make_mumiso_scenario
from ris_mu.mumiso.mobile import MobileConfig, MobileMuMisoChannel

REF = "8defb93"   # last commit before the wideband option
src = subprocess.run(["git", "-C", str(ROOT), "show", f"{REF}:ris_mu/mumiso/mobile.py"],
                     capture_output=True, text=True, check=True).stdout
spec = importlib.util.spec_from_loader("ris_mu.mumiso._mobile_ref", loader=None)
old = importlib.util.module_from_spec(spec)
old.__package__ = "ris_mu.mumiso"
exec(compile(src, f"{REF}:mobile.py", "exec"), old.__dict__)

KEYS = ("F", "G_t", "hd_t", "G", "hd", "ue_t", "bs_pos", "bs_array",
        "ue_pos", "los_ris_bs", "los_ris_ue", "los_direct", "times_ms")
cases, ok_all = [], True
for n_users in (1, 4):
    for seed in (11, 2026):
        for chunk in (500, 37):
            panel, base = make_mumiso_scenario(n_users=n_users, n_bs_antennas=8, seed=seed)
            cfg = dict(base.__dict__, velocity=1.5, n_clusters=20,
                       times_ms=(0.0, 5.0, 28.2))
            n = 64
            d_old = old.MobileMuMisoChannel(panel, old.MobileConfig(**cfg)).generate(n, chunk=chunk)
            d_off = MobileMuMisoChannel(panel, MobileConfig(**cfg)).generate(n, chunk=chunk)
            d_on = MobileMuMisoChannel(panel, MobileConfig(**cfg)).generate(
                n, chunk=chunk, freq_offsets_hz=[-10e6, 0.0, 10e6])
            eq_off = {k: bool(np.array_equal(d_old[k], d_off[k])) for k in KEYS}
            eq_on = {k: bool(np.array_equal(d_old[k], d_on[k])) for k in KEYS}
            rel = lambda a, b: float(np.max(np.abs(a - b)) / np.max(np.abs(b)))
            dc = dict(F=rel(d_on["F_f"][:, 1], d_on["F"]),
                      G=rel(d_on["G_tf"][:, :, 1], d_on["G_t"]),
                      hd=rel(d_on["hd_tf"][:, :, 1], d_on["hd_t"]))
            ok = all(eq_off.values()) and all(eq_on.values()) and max(dc.values()) < 1e-5
            ok_all &= ok
            cases.append(dict(n_users=n_users, seed=seed, chunk=chunk, n=n,
                              ref_vs_off=eq_off, ref_vs_on=eq_on,
                              df0_max_rel_err=dc, ok=ok))
            print(f"K={n_users} seed={seed} chunk={chunk}: off==ref {all(eq_off.values())}, "
                  f"on==ref {all(eq_on.values())}, df=0 rel err {max(dc.values()):.1e} -> "
                  f"{'OK' if ok else 'FAIL'}")
json.dump(dict(ref_commit=REF, all_ok=ok_all, cases=cases),
          open(ROOT / "results/wideband_bitidentity_check.json", "w"), indent=1)
print("ALL OK" if ok_all else "FAILURE")
sys.exit(0 if ok_all else 1)
