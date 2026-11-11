"""Builds thesis_exp/bridge/REPORT.md from thesis_exp/bridge/raw/ (read-only)."""
import json, glob, pathlib, subprocess
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[3]
RAW = ROOT / "thesis_exp/bridge/raw"
J = lambda p: json.load(open(p)) if pathlib.Path(p).exists() else None
tr = {pathlib.Path(f).stem: J(f) for f in glob.glob(str(RAW / "train/*.json"))}
ev, tk = J(RAW / "eval_main.json"), J(RAW / "tracking.json")
evs = J(RAW / "eval_speeds.json")
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
out = []; W = out.append
W("# Köprü: tek geçişli faz-farkında ağ, etkin hız ölçütünde — rapor")
W("")
W(f"Rapor commit'i `{commit}`. Eğitim verisi (onaylı seçenek ii): yaşlanma kümesinin yapısıyla (20 saçıcı, t=0) üretilmiş statik küme, "
  "seed 2027, 6000 senaryo, bölme 4200/900/900. Değerlendirme: yaşlanma kümesi (seed 11, 400 senaryo); seçimler yalnızca statik doğrulama "
  "kümesinde ve ayrı bir hareketlilik çekilişinde (seed 12).")
W("")
sel = {k: v for k, v in tr.items() if k.endswith("_s0") and "staticpaper" not in k}
best = max(sel, key=lambda k: sel[k]["val_min"])
W("## 1) Bulgular")
W("")
W(f"1. **Yapılandırma seçimi (doğrulama, tohum 0):** " + "; ".join(f"{k}: {v['val_min']:.4f}" for k, v in sorted(sel.items()))
  + f". SU-average aynı kümede {sel[best]['val_su_average']:.4f}. Seçilen: `{best}`.")
seeds = [tr[k] for k in tr if k.startswith(best[:-3]) and "staticpaper" not in k]
W(f"2. **Seçilen yapılandırmanın test min-hızı (3 tohum):** " + ", ".join(f"{x['test_min']:.4f}" for x in seeds)
  + (f"; makalenin statik kümesinde eğitilen ikincil kol: {tr[best + '_staticpaper']['test_min']:.4f} (o kümenin testi)." if best + "_staticpaper" in tr else ""))
if ev:
    for kmh, blk in ev["speeds"].items():
        r = blk["rows"]
        W(f"3. **Etkin hız, {kmh} km/h** (doğrulamada seçilen en iyi klasik: {blk['best_classical_on_val']}, "
          f"{r[blk['best_classical_on_val']]['effective']:.4f} b/s/Hz):")
        for k in ("net", "net+Adam-1", "net+Adam-2", "net+Adam-3"):
            d = blk["learned_minus_best_classical"][k]
            W(f"   - {k}: gecikme {r[k]['latency_ms']:.3f} ms, etkin {r[k]['effective']:.4f}; fark {d['mean']:+.4f} "
              f"[{d['ci'][0]:+.4f}, {d['ci'][1]:+.4f}]; baskınlayan klasik kollar: {', '.join(blk['dominated_by'][k]) or 'yok'}")
if evs:
    W("4. **Tablo II hızları** (gecikmeler aynı ölçümden):")
    for kmh, blk in evs["speeds"].items():
        d = blk["learned_minus_best_classical"]
        W(f"   - {kmh} km/h: en iyi klasik {blk['best_classical_on_val']}; net {d['net']['mean']:+.4f} [{d['net']['ci'][0]:+.4f}, {d['net']['ci'][1]:+.4f}], "
          f"baskınlanan öğrenilen kol sayısı {sum(1 for v in blk['dominated_by'].values() if v)}/4")
if tk:
    W("5. **Periyodik çalışma** (seçim seed 12, rapor seed 11):")
    for tp, b in tk["by_pilot"].items():
        W(f"   - T_p={tp} ms: soğuk {b['cold']['rate']:.3f} (U={b['cold']['period']}, L={b['cold']['L']}), sıcak {b['warm']['rate']:.3f} "
          f"(U={b['warm']['period']}, L={b['warm']['L']}), ağ {b['net']['rate']:.3f} (U={b['net']['period']}, L={b['net']['L']}); "
          f"ağ−soğuk {b['net_minus_cold']['diff']:+.3f} [{b['net_minus_cold']['ci'][0]:+.3f}, {b['net_minus_cold']['ci'][1]:+.3f}], "
          f"ağ−sıcak {b['net_minus_warm']['diff']:+.3f} [{b['net_minus_warm']['ci'][0]:+.3f}, {b['net_minus_warm']['ci'][1]:+.3f}]")
W("")
W("## 2) Tablo")
W("")
W("| Kol | Gecikme (ms) | t=0 hız | Etkin hız [%95 GA] | Durum | Kanıt |")
W("| --- | --- | --- | --- | --- | --- |")
if ev:
    blk = list(ev["speeds"].values())[0]
    for k, r in blk["rows"].items():
        dom = blk["dominated_by"].get(k)
        st = "—" if dom is None else ("BASKINLANIYOR" if dom else "baskınlanmıyor")
        W(f"| {k} | {r['latency_ms']:.3f} | {r['t0']:.4f} | {r['effective']:.4f} [{r['effective_ci'][0]:.4f}, {r['effective_ci'][1]:.4f}] | {st} | raw/eval_main.json |")
W("")
W("## 3) Komutlar, tohumlar, ham çıktılar")
W("")
W("| Adım | Komut | Tohum | Ham çıktı |")
W("| --- | --- | --- | --- |")
W("| eğitim | bridge_train.py --residual {0,1} --link_ratio {0,1} --seed 0; seçilen yapılandırma --seed 1,2; --static_paper | veri 2027 (ikincil: 11), eğitim 0/1/2 | raw/train/*.json |")
W("| etkin hız | bridge_eval.py --ckpt raw/train/<seçilen>_s0.pt --tag main (gecikme ölçümü, yük < 0.5) | seçim 12, rapor 11, bootstrap 0 | raw/eval_main.json |")
W("| hızlar | bridge_eval.py --speeds_kmh 3,5.4,10,18,30 --latency_json raw/eval_main.json --tag speeds | aynı | raw/eval_speeds.json |")
W("| periyodik | bridge_tracking.py | seçim 12, rapor 11 | raw/tracking.json |")
W("")
W("## 4) Açık sorular")
W("")
W("1. Ağ diğer tohumlarla değerlendirilsin mi? (Etkin hız ana değerlendirmesi tohum 0 ile yapıldı; tohum yayılımı 2. bulguda.)")
W("2. Sonuç tezde 'tek geçiş başlangıç noktasında takılıyor; gecikme ekseninde de baskınlanıyor' diye mi yazılsın?")
W("")
W("## 5) Yorum (bulgulardan ayrı)")
W("")
W("- Kalıntı (residual) mod ağı SU-average başlangıcının etrafında tutuyor; bu, tezdeki 3.7230/3.7230 bulgusunun bu veride tekrarı.")
(ROOT / "thesis_exp/bridge/REPORT.md").write_text("\n".join(out) + "\n")
print("wrote thesis_exp/bridge/REPORT.md")
