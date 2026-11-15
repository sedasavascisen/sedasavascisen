"""Builds thesis_exp/p4/takip_duzeltme/REPORT.md: Paper 2 Table III (results/mumiso_tracking.json, read only)
against the corrected copy (raw/fix1_tp*.json) and the reproduction check (raw/fix0_tp0.86.json)."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent; ROOT = H.parents[2]
pub = json.load(open(ROOT / "results/mumiso_tracking.json"))
r0 = json.load(open(H / "raw/fix0_tp0.86.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
ci = lambda x: f"[{x[0]:+.3f}, {x[1]:+.3f}]"
W("# Makale 2 Tablo III — periyodik çalışmada pilot ve devreye alma yuvarlaması (denetim K4)"); W("")
md = max(abs(pub["runs"]["0.86"][m]["mean"][k] - r0["runs"]["0.86"][m]["mean"][k]) for m in ("cold", "warm") for k in pub["runs"]["0.86"][m]["mean"])
W(f"Rapor commit'i `{c}`. Yayımlanmış `scripts/mumiso_tracking.py` (Tablo III) 0.5 ms ızgarada pilot süresini `round(t_p/0.5)` örneğe, devreye alma anını en yakın ızgara noktasına yuvarlıyor; "
  "0.86 / 1.71 / 3.43 ms pilotlar ızgara üstü döngülerde 1.0 / 1.5 / 3.5 ms ücretleniyor ve hata döngü uzunluğuna (kola) göre değişiyor. "
  "`run.py` bu betiğin kopyası (yayımlanmış betiğe dokunulmadı): `--fix 0` aynı mantık, `--fix 1` kesirli pilot ücreti ve tam devreye alma anı. "
  f"**Yeniden üretim:** `--fix 0`, T_p = 0.86 ms'de yayımlanmış dosyayla en fazla {md:.1e} fark (birebir). Diğer her şey (senaryolar, adımlar, periyotlar, 100–200 ms penceresi, "
  "bootstrap, seçimin raporlanan kümede yapılması) yayımlanmış betikle aynı.")
W(""); W("## 1) Sıcak − soğuk (en iyi politika vs en iyi politika)"); W("")
W("| T_p (ms) | Yayımlanmış [%95 GA] | Düzeltilmiş [%95 GA] | Fark |"); W("| --- | --- | --- | --- |")
rows = []
for tp, key in (("0", "0.0"), ("0.86", "0.86"), ("1.71", "1.71"), ("3.43", "3.43")):
    f = json.load(open(H / f"raw/fix1_tp{tp}.json")); fw = f["warm_minus_cold"][list(f["warm_minus_cold"])[0]]; pw = pub["warm_minus_cold"][key]
    W(f"| {tp} | {pw['diff']:+.4f} {ci(pw['ci'])} | {fw['diff']:+.4f} {ci(fw['ci'])} | {fw['diff'] - pw['diff']:+.4f} |")
    rows.append((tp, key, f))
W(""); W("## 2) En iyi politikalar"); W("")
W("| T_p | Kip | Yayımlanmış: U, L, hız | Düzeltilmiş: U, L, hız [%95 GA] | Arka arkaya en iyi L (yay. / düz.) |"); W("| --- | --- | --- | --- | --- |")
for tp, key, f in rows:
    fk = list(f["runs"])[0]
    for m in ("cold", "warm"):
        P, F = pub["runs"][key][m], f["runs"][fk][m]
        W(f"| {tp} | {'soğuk' if m == 'cold' else 'sıcak'} | {P['best']['period'] or 'b2b'}, {P['best']['L']}, {P['best']['rate']:.4f} | "
          f"{F['best']['period'] or 'b2b'}, {F['best']['L']}, {F['best']['rate']:.4f} [{F['best']['ci'][0]:.4f}, {F['best']['ci'][1]:.4f}] | "
          f"{P['back_to_back']['best_L']} / {F['back_to_back']['best_L']} |")
_bp = pathlib.Path("/tmp/claude-0/-home-user-sedasavascisen/36a1538b-b28f-5b37-970a-9a1a9a74083b/scratchpad/wt_bridge/thesis_exp/bridge/raw/tracking.json")
_bpub = json.load(open(_bp)) if _bp.exists() else json.loads(subprocess.run(["git", "show", "origin/thesis/bridge:thesis_exp/bridge/raw/tracking.json"], capture_output=True, text=True, cwd=ROOT).stdout)
_b0 = json.load(open(H / "raw/bridge_fix0_tp0.86.json"))["by_pilot"]["0.86"]
_rep = all(abs(_bpub["by_pilot"]["0.86"][k]["rate"] - _b0[k]["rate"]) < 1e-9 for k in ("cold", "warm", "net"))
W(""); W("## 2b) Köprü raporunun periyodik çalışması (thesis/bridge, bridge_tracking.py)"); W("")
W(f"Aynı düzeltme, köprü betiğinin kopyasına (`bridge_tracking_fix.py`; girdiler thesis/bridge dalının salt okunur çalışma ağacından) uygulandı. "
  f"Yeniden üretim (`--fix 0`, T_p = 0.86): {'birebir' if _rep else 'FARKLI'}. Seçim seed 12, rapor seed 11 (köprü betiğindeki gibi).")
W(""); W("| T_p | Ağ − soğuk: yayımlanmış [%95 GA] | düzeltilmiş [%95 GA] | Ağ − sıcak: yayımlanmış [%95 GA] | düzeltilmiş [%95 GA] |"); W("| --- | --- | --- | --- | --- |")
for tp in ("0", "0.86", "1.71", "3.43"):
    _f = json.load(open(H / f"raw/bridge_fix1_tp{tp}.json"))["by_pilot"]; _k = list(_f)[0]; F = _f[_k]; P = _bpub["by_pilot"][_k]
    W(f"| {tp} | {P['net_minus_cold']['diff']:+.3f} {ci(P['net_minus_cold']['ci'])} | {F['net_minus_cold']['diff']:+.3f} {ci(F['net_minus_cold']['ci'])} | "
      f"{P['net_minus_warm']['diff']:+.3f} {ci(P['net_minus_warm']['ci'])} | {F['net_minus_warm']['diff']:+.3f} {ci(F['net_minus_warm']['ci'])} |")
W(""); W("## 3) Komut ve ham çıktı"); W("")
W("`OMP_NUM_THREADS=1 python3 thesis_exp/p4/takip_duzeltme/run.py --fix {0,1} --pilot {0,0.86,1.71,3.43}` → raw/fix{0,1}_tp*.json, *.log. Köprü: `OMP_NUM_THREADS=1 python3 thesis_exp/p4/takip_duzeltme/bridge_tracking_fix.py --fix {0,1} --pilot ...` → raw/bridge_fix*_tp*.json. Betikler koşudan önce commit'lendi.")
y = H / "yorum.md"
if y.exists():
    W(""); W("## 4) Yorum (bulgulardan ayrı)"); W(""); W(y.read_text().strip())
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
