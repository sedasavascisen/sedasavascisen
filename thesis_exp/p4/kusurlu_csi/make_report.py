"""Builds thesis_exp/p4/kusurlu_csi/REPORT.md from raw/results.json."""
import json, pathlib, subprocess
H = pathlib.Path(__file__).parent
r = json.load(open(H / "raw/results.json"))
c = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=H).stdout.strip()
o = []; W = o.append
W("# Deney 4.4 — Pilot SNR'sine bağlı kusurlu CSI (rapor)"); W("")
W(f"Rapor commit'i `{c}`, ölçüm commit'i `{r['commit'][:7]}` (results.json). Hata modeli ris_mu/mumiso/csi.py (F, G, h_d için ayrı ölçek, gücü koruyan), e2 = 1/(1+ρ), ρ = kestirim sonrası katsayı başına pilot SNR'si. "
  "Faz t=0 kestiriminden; teslim anında ZF, aynı ρ ile yeni bir kestirimden; hız gerçek kanalda. Adam adım boyu her ρ ve L için doğrulama çekilişinde "
  "(seed 12, etkin hız üzerinden) seçildi; rapor yaşlanma kümesi (seed 11). Gecikmeler: tek iş parçacıklı yeniden ölçüm.")
W(""); W("## 1) Bulgular"); W("")
W("| ρ | e2 | Doğrulamada seçilen | Etkin hız [%95 GA] | SU-best-of | Fark [%95 GA] | Testte en iyi Adam-L |")
W("| --- | --- | --- | --- | --- | --- | --- |")
for k, v in r["levels"].items():
    W(f"| {k} | {v['e2']:.4f} | {v['selected_on_val']} | {v['test']:.4f} [{v['test_ci'][0]:.4f}, {v['test_ci'][1]:.4f}] | {v['su_best_of']:.4f} | "
      f"{v['best_minus_su_best_of']:+.4f} [{v['ci'][0]:+.4f}, {v['ci'][1]:+.4f}] | {v['L_star_test']} |")
W(""); W("## 2) Komut, tohum, ham çıktı"); W("")
W("| Komut | Tohum | Ham çıktı |"); W("| --- | --- | --- |")
W("| python3 thesis_exp/p4/kusurlu_csi/run.py | kanal 11/12, kestirim gürültüsü 100+i / 200+i, bootstrap 0 | raw/results.json |")
W(""); W("## 3) Yorum (bulgulardan ayrı)"); W("")
W("- Kestirim hatası etkin hızı çok hızlı düşürüyor; bu, düz ZF'nin kanal hatasına duyarlılığı (csi.py docstring'inde ölçülmüş).")
W("- Hata büyüdükçe en iyi adım sayısı küçülüyor; düşük ρ'da yöntemler birbirinden ayırt edilemiyor (GA sıfırı içeriyor).")
W("- ρ'nun gerçek pilot bütçesine (sembol sayısı, iletim gücü) bağlanması bu deneyin kapsamı dışında; ρ burada serbest parametre.")
(H / "REPORT.md").write_text("\n".join(o) + "\n"); print("wrote")
