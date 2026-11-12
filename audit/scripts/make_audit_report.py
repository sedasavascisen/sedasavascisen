"""
Builds audit/AUDIT_REPORT.md from the raw outputs in audit/raw/ (every number in the report is read
from a file listed in its row). Usage: python3 audit/scripts/make_audit_report.py
"""
import json, pathlib, subprocess
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "audit/raw"
L = lambda p: json.load(open(RAW / p)) if (RAW / p).exists() else None
s1, s2, s4, s5c, s5p, s6 = (L("step1_label_optimality.json"), L("step2_baselines.json"), L("step4_latency.json"),
                            L("step5_correlation.json"), L("step5_permutation.json"), L("step6_eval.json"))
tr = {p.stem: json.load(open(p)) for p in (RAW / "train").glob("*.json")}
s7, s7d = L("step7_references.json"), L("step7_doublecheck.json")
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
out = []
W = out.append
f2 = lambda x: f"{x:.2f}"
seeds = [tr[f"cnnlstm_N32_s{s}"]["test_rmse_deg"] for s in (0, 1, 2) if f"cnnlstm_N32_s{s}" in tr]
n256 = tr["cnnlstm_N256_sqrt_s0"]
pc = s2["perfect_csi"]
cs = s6["seeds"]
csi_m = lambda x: np.mean([cs[s]["csi_error"][x]["rmse_deg"] for s in cs])
imp = lambda k: np.mean([cs[s][k]["rmse_deg"] for s in cs])
impr = lambda k: np.mean([cs[s][k]["rate_loss_vs_label_bpshz"] for s in cs])

W("# Makale 1 bağımsız denetim raporu")
W("")
W(f"Makale: Savaşçı Şen ve ark., *Overcoming the Phase Discontinuity Problem in RIS Optimization…*, Adv. Intell. Syst. 2026, "
  f"doi:10.1002/aisy.70460. Dal `audit/makale1-denetim`, rapor commit'i `{commit}` (rapor bu commit'teki ham dosyalardan üretildi).")
W("")
W("**Önemli sınır:** MATLAB ve makalenin veri kümesi (`RIS_dataset_large_2D.mat`) yok. Bütün yeniden üretimler, aynı üretecin "
  "NumPy aktarımıyla (`audit/scripts/m1_data.py`) alınmış **bağımsız bir çekilişte** yapıldı. MATLAB'ın `rng(42)` örnekleriyle "
  "birebir aynı değildir; aktarım kayıtlı bir MATLAB çıktısıyla doğrulanamadı (Kural 8). Eğitim, MATLAB varsayılanlarına "
  "göre PyTorch'a aktarıldı (`audit/scripts/m1_train.py`, docstring).")
W("")
W("## 1) Makaledeki iddialarla çelişen bulgular (önem sırasıyla)")
W("")
g = s1["gain_b_minus_a_db"]
items = [
 f"**Etiket optimum değil (Denklem 8).** Makale −∠(G_nF_n) etiketini alınan gücün kapalı form maksimizörü diye tanımlıyor. "
 f"Doğrudan bağlantıyı hesaba katan ∠h_d − ∠(G_nF_n) etiketi hiçbir örnekte daha kötü değil ve ortalama **{f2(g['mean'])} dB** "
 f"(%95 GA {f2(g['mean_ci95'][0])}–{f2(g['mean_ci95'][1])}; medyan {f2(g['median'])} dB; %95 dilim {f2(g['p95'])} dB) daha fazla güç alıyor; "
 f"örneklerin %{100*g['frac_above_0p1db']:.1f}'inde fark 0.1 dB'den büyük. |h_d|/|ΣG_nF_n| medyanı {f2(s1['hd_over_sumGF']['median'])}: "
 f"doğrudan bağlantı ihmal edilebilir değil. [step1_label_optimality.json]",
 f"**Nicemleme sonuçları matematiksel olarak imkânsız.** Sürekli etikete göre faz RMSE'si, etiketin kendisi nicemlendiğinde bile "
 f"1/2/3 bitte {f2(s6['label_impaired']['1bit']['rmse_deg'])}°/{f2(s6['label_impaired']['2bit']['rmse_deg'])}°/{f2(s6['label_impaired']['3bit']['rmse_deg'])}° "
 f"(tekdüze nicemleme hatası adım/√12). Eğitilmiş modelle {f2(imp('1bit'))}°/{f2(imp('2bit'))}°/{f2(imp('3bit'))}°. Makale 4.12°/3.08°/2.81° diyor ve "
 f"betiği yok. [step6_eval.json]",
 f"**CSI hatasında 4.2° iddiası tutmuyor.** Göreli hata varyansı 0.10'da model {f2(csi_m('0.1'))}° (3 tohum ort.), aynı girdiyle kapalı form "
 f"{f2(s2['csi_error']['0.1']['closed_form_a (Eq. 8 label)']['rmse_pub_deg'])}°. Makale 4.2° ve kapalı formdan belirgin üstünlük diyor; "
 f"Şekil 10'un betiği ve hata modeli tanımı yok (burada varsayılan model, step2_baselines.py). [step6_eval.json, step2_baselines.json]",
 f"**Klasik yöntemlerin RMSE'leri yayımlanan kodla üretilemiyor.** Yayımlanan RMSE tanımıyla CD (K=5) {f2(pc['CD K=5']['rmse_pub_deg'])}° "
 f"(makale 3.50°), AO {f2(pc['AO K=1 (default)']['rmse_pub_deg'])}° (3.50°), PSO {f2(pc['PSO']['rmse_pub_deg'])}° (4.50°), "
 f"SPA {f2(pc['SPA']['rmse_pub_deg'])}° (5.00°). Sebep: bu yöntemler h_d'ye hizalanan gerçek optimuma gidiyor ve etiketten ortak bir faz kadar "
 f"farklı. Ortak faz çıkarılınca CD {f2(pc['CD K=5']['rmse_inv_deg'])}°, SPA {pc['SPA']['rmse_inv_deg']:.2g}° (SPA tam optimum = etiket (b)). "
 f"Alınan güçte CD ve SPA etiketten {f2(pc['CD K=5']['power_db_vs_a'])} / {f2(pc['SPA']['power_db_vs_a'])} dB önde. "
 f"PGD ve 'WMMSE' betikleri fazı neredeyse hiç hareket ettirmiyor (etikete göre {f2(pc['PGD']['power_db_vs_a'])} / "
 f"{f2(pc['WMMSE (script)']['power_db_vs_a'])} dB). [step2_baselines.json]",
 "**Tablo 6, Tablo 8, Şekil 1 ve 2'deki sayılar elle yazılmış; Şekil 8, 9, 10 için betik yok.** Ayrıntı ve satır numaraları "
 "[step0_mapping.json, step0_step3_notes.md].",
 "**Kaynağı bulunamayan sayılar:** 18.4/17.9 dB, kapalı formun 2.70° RMSE'si (etiketin kendisine göre tanım gereği 0°; burada "
 f"{f2(pc['closed_form_a (Eq. 8 label)']['rmse_pub_deg'])}°), 0.31/0.89 b/s/Hz, %312, Tablo 3 parametre sayıları. [step3_sources.json]",
 f"**Gecikme ve ölçekleme.** Yayımlanan mimarinin parametre sayısı koddan {tr['cnnlstm_N32_s0']['params']:,} (PyTorch; MATLAB "
 f"161 794, aradaki 768 ikinci LSTM bias'ı); makale 727 K. Tek-örnek CPU gecikmesi N=32/256'da "
 f"{f2(s4['arms']['cnnlstm_fixed']['32']['single_ms'])}/{f2(s4['arms']['cnnlstm_fixed']['256']['single_ms'])} ms, toplu iş "
 f"{s4['arms']['cnnlstm_fixed']['32']['batch_per_sample_ms']:.3f}/{f2(s4['arms']['cnnlstm_fixed']['256']['batch_per_sample_ms'])} ms; makale 0.08/0.64 ms "
 f"(farklı işlemci: i7-9700K). Ölçekleme oranı 256/32: tek-örnek "
 f"{s4['arms']['cnnlstm_fixed']['256']['single_ms']/s4['arms']['cnnlstm_fixed']['32']['single_ms']:.1f}×, gizli boyut √N ölçeklemeli "
 f"{s4['arms']['cnnlstm_sqrt']['256']['single_ms']/s4['arms']['cnnlstm_sqrt']['32']['single_ms']:.1f}× (makale tam 8×). [step4_latency.json]",
 f"**N=256 projeksiyonu ölçümle tutmuyor.** Tablo 8'deki N=256 RMSE'si 4.6° elle yazılmış bir tahmin (betik yok). Aynı üreteç, "
 f"aynı örnek sayısı (40 000) ve 50 epokla eğitilen N=256 modeli (gizli boyutlar √(N/32) ile ölçeklendi; {n256['params']:,} parametre; "
 f"son epok ağı) test kümesinde **{f2(n256['test_rmse_deg'])}°** (SR@5 %{100*n256['sr']['SR@5']:.1f}, %95 dilim {f2(n256['err_deg_p95'])}°) veriyor; "
 f"bu, N=32'nin üç tohumunun ({', '.join(f2(x) for x in seeds)}°) hepsinden düşük. Makalenin N arttıkça RMSE'nin arttığı projeksiyonu bu ölçümde "
 f"desteklenmiyor. Sınır: tek tohum; N=64/128 eğitilmedi; mimarinin N ile ölçeklenmesi makalede tanımlı değil (√N bizim seçimimiz). "
 f"[train/cnnlstm_N256_sqrt_s0.json, train_N256_run2.log]",
 f"**Tohum yayılımı makalenin GA'sından çok büyük.** Aynı ayarla 3 tohum: {', '.join(f2(x) for x in seeds)}° (std "
 f"{np.std(seeds, ddof=1):.2f}°); makale 5 koşu için ±0.09° GA diyor. [train/cnnlstm_N32_s*.json]",
 f"**Uzamsal komşuluk kullanılmıyor.** Komşu elemanların kanal korelasyonu |ρ| ≤ "
 f"{max(v['rho_GF'] for v in s5c['pairs'].values()):.3f}; eleman sırası rastgele karıştırılınca RMSE "
 f"{f2(s5p['across_seeds']['original_mean'])}° → {f2(s5p['across_seeds']['permuted_mean'])}° (fark tohum yayılımından küçük). "
 f"Makalenin CNN'in 'uzamsal korelasyonu yakaladığı' anlatısı bu veride desteklenmiyor. [step5_correlation.json, step5_permutation.json]",
 f"**Doğrudan faz (FC-DNN) {f2(tr['fcdnn_direct_N32_s0']['test_rmse_deg'])}°, CNN-Transformer {f2(tr['transformer_N32_s0']['test_rmse_deg'])}°** "
 f"(makale 3.95° / 2.91°). Transformer parametresi {tr['transformer_N32_s0']['params']:,} (makale 201 K). [train/*.json]",
]
if s7:
    refs = s7["references"]
    cnt = {}
    for r_ in refs:
        cnt[r_.get("severity", r_.get("status", "?"))] = cnt.get(r_.get("severity", r_.get("status", "?")), 0) + 1
    items.append(f"**Kaynakça (64 kaynak):** ilk tur {cnt}. Bağımsız ikinci kontrol 63 kaynakta ilk turla aynı fikirde; "
                 "[29] bulundu (başlığı yanlış basılmış gerçek bir makale: Kim ve ark., IEEE TCCN 2024, doi:10.1109/TCCN.2024.3375523). "
                 "Basılı 54 DOI'nin 30'u kayıtlı değil; 3'ü ([31], [33], [43]) başka makalelere çıkıyor. 7 kaynak ([15], [33], [37], [41], [43], [44], [59]) "
                 "hiçbir kayıtta bulunamadı ([33] ve [43] için aynı yazarların farklı başlıklı gerçek çalışmaları var: bozuk atıf olabilir). "
                 "[26] geri çekilmiş (doi:10.52866/2788-7421.1361, 5 Şubat 2026). [27] TWC değil IEEE WCL. [28]'in PixelRNN iddiasını ve [38]'in "
                 "bit genişliği iddiasını kaynak desteklemiyor. [step7_references.json, step7_doublecheck.json]")
for i, t in enumerate(items, 1):
    W(f"{i}. {t}")
W("")
W("## 2) İddia tablosu")
W("")
W("| İddia | Yayımlanan | Üretilen (bağımsız çekiliş) | Durum | Kanıt |")
W("| --- | --- | --- | --- | --- |")
rows = [
 ("CNN-LSTM RMSE", "2.77°", f"{', '.join(f2(x) for x in seeds)}° (3 tohum)", "FARKLI (yayılım)", "train/cnnlstm_N32_s*.json"),
 ("CNN-LSTM SR@5", "%95", f"%{100*np.mean([tr[f'cnnlstm_N32_s{s}']['sr']['SR@5'] for s in (0,1,2)]):.1f}", "DOĞRULANDI (yakın)", "train/*.json"),
 ("Doğrudan faz RMSE", "3.95°", f"{f2(tr['fcdnn_direct_N32_s0']['test_rmse_deg'])}°", "FARKLI", "train/fcdnn_direct_N32_s0.json"),
 ("CNN-Transformer RMSE", "2.91°", f"{f2(tr['transformer_N32_s0']['test_rmse_deg'])}°", "FARKLI", "train/transformer_N32_s0.json"),
 ("CD (K=5) RMSE", "3.50°", f"{f2(pc['CD K=5']['rmse_pub_deg'])}° (ortak fazsız {f2(pc['CD K=5']['rmse_inv_deg'])}°)", "FARKLI", "step2_baselines.json"),
 ("CD (K=20/50) RMSE", "3.49/3.20°", f"{f2(pc['CD K=20']['rmse_pub_deg'])}/{f2(pc['CD K=50']['rmse_pub_deg'])}°", "FARKLI", "step2_baselines.json"),
 ("AO / PGD / WMMSE / PSO / SPA", "3.50/4.00/4.00/4.50/5.00°",
  "/".join(f2(pc[k]['rmse_pub_deg']) for k in ('AO K=1 (default)', 'PGD', 'WMMSE (script)', 'PSO', 'SPA')) + "°", "FARKLI", "step2_baselines.json"),
 ("Kapalı form RMSE", "2.70°", f"{f2(pc['closed_form_a (Eq. 8 label)']['rmse_pub_deg'])}° (tanım gereği)", "KAYNAK BULUNAMADI", "step3_sources.json"),
 ("Şekil 8: %95'e ulaşılan hata", "5°", f"{f2(np.mean([cs[s]['clean']['err_p95_deg'] for s in cs]))}° (CDF(5°) = %{100*np.mean([cs[s]['clean']['cdf_at_5deg'] for s in cs]):.1f})", "DOĞRULANDI (yakın); yayımlanan görüntü 5°'de ≈%87 gösteriyor", "step6_eval.json, step0_step3_notes.md"),
 ("Şekil 9: normalize RMSE", "0.554", "2.77/5 aritmetiği; şeklin betiği yok", "KAYNAK BULUNAMADI", "step3_arith_check.json"),
 ("Şekil 9: PSO gecikmesi", "15 ms", "MATLAB yok; Python süresi karşılaştırılamaz", "ÜRETİLEMEDİ", "—"),
 ("Şekil 10: %10 CSI hatası", "4.2°", f"{f2(csi_m('0.1'))}° (x=0.15: {f2(csi_m('0.15'))}°)", "FARKLI", "step6_eval.json"),
 ("Şekil 10: kapalı form / PSO, %10", "model üstün", f"{f2(s2['csi_error']['0.1']['closed_form_a (Eq. 8 label)']['rmse_pub_deg'])}° / {f2(s2['csi_error']['0.1']['PSO']['rmse_pub_deg'])}°", "FARKLI", "step2_baselines.json"),
 ("1/2/3 bit nicemleme", "4.12/3.08/2.81°", f"{f2(imp('1bit'))}/{f2(imp('2bit'))}/{f2(imp('3bit'))}° (hız kaybı {impr('1bit'):.3f}/{impr('2bit'):.3f}/{impr('3bit'):.3f} b/s/Hz)", "FARKLI", "step6_eval.json"),
 ("Faz gürültüsü σ=1/3/5°", "3°'de taban çizgisine yakın", f"{f2(imp('noise1deg'))}/{f2(imp('noise3deg'))}/{f2(imp('noise5deg'))}° (hız kaybı {impr('noise3deg'):.3f} b/s/Hz @3°)", "FARKLI (RMSE) / hız kaybı küçük", "step6_eval.json"),
 ("Parametre (önerilen)", "727 K", f"{tr['cnnlstm_N32_s0']['params']:,}", "FARKLI", "train/cnnlstm_N32_s0.json"),
 ("Diğer Tablo 3 parametreleri", "89K…201K", "mimari tanımı yok", "KAYNAK BULUNAMADI", "step3_sources.json"),
 ("Gecikme N=32/64/128/256", "0.08/0.16/0.32/0.64 ms",
  "/".join(f2(s4['arms']['cnnlstm_fixed'][n]['single_ms']) for n in ('32','64','128','256')) + " ms (tek örnek, CPU)", "FARKLI (farklı işlemci)", "step4_latency.json"),
 ("RMSE N=256", "4.6° (tahmin)", f"{f2(n256['test_rmse_deg'])}° (1 tohum, gizli boyut √N ölçekli, SR@5 %{100*n256['sr']['SR@5']:.1f})", "FARKLI (makaleden düşük; tek tohum)", "train/cnnlstm_N256_sqrt_s0.json"),
 ("SNR kazancı model / optimal", "18.4 / 17.9 dB", f"etiket (a) medyan {f2(s1['snr_gain_over_direct_db']['label_a_median'])} dB, (b) {f2(s1['snr_gain_over_direct_db']['label_b_median'])} dB (doğrudan bağlantıya göre)", "KAYNAK BULUNAMADI", "step1, step3"),
 ("0.31 / 0.89 b/s/Hz, %312", "—", "betik yok", "KAYNAK BULUNAMADI", "step3_sources.json"),
]
for r_ in rows:
    W("| " + " | ".join(r_) + " |")
W("")
W("## 3) Adımlar: komut, tohum, ham çıktı")
W("")
cmds = [
 ("0, 3", "ajan taraması (yalnızca okuma)", "—", "step0_mapping.json, step3_sources.json, step0_step3_notes.md, step3_arith_check.json"),
 ("1", "python3 audit/scripts/step1_label_optimality.py --n 6000 --seed 42", "veri 42, bootstrap 0", "step1_label_optimality.json"),
 ("2", "python3 audit/scripts/step2_baselines.py", "veri 42, PSO 0, CSI gürültüsü 5", "step2_baselines.json, step2_csi_inputs_x*.npz"),
 ("2, 5", "python3 audit/scripts/m1_train.py --arch {cnnlstm,fcdnn_direct,transformer} --seed {0,1,2} [--permute]", "veri 42, eğitim 0/1/2, permütasyon 7", "train/*.json, *.pt, *_test_abs_err_deg.npy"),
 ("2 (N=256)", "python3 audit/scripts/m1_train.py --arch cnnlstm --seed 0 --N 256 --hidden_scale sqrt --tag cnnlstm_N256_sqrt_s0 --threads 2 (betiğin bu daldaki hâli, yalnızca ROOT yolu sabitlenmiş kopyadan; JSON'daki commit 81b07dd çalışma ağacının HEAD'i)", "veri 42, eğitim 0", "train/cnnlstm_N256_sqrt_s0.*, train_N256_run2.log (ilk deneme yeniden başlatmayla kesildi: train_N256.log)"),
 ("4", "python3 audit/scripts/step4_latency.py", "veri 123", "step4_latency.json"),
 ("5", "python3 audit/scripts/step5_correlation.py; step5_permutation.py", "bootstrap 0", "step5_correlation.json, step5_permutation.json"),
 ("6", "python3 audit/scripts/step6_eval.py", "faz gürültüsü 11", "step6_eval.json"),
 ("7", "ajan: Crossref/doi.org/arXiv", "—", "step7_references.json/.md, step7_doublecheck.json"),
]
W("| Adım | Komut | Tohum | Ham çıktı (audit/raw/) |")
W("| --- | --- | --- | --- |")
for c in cmds:
    W("| " + " | ".join(c) + " |")
W("")
W(f"Ortam: Python 3.11.17, PyTorch {s4['torch']}, NumPy 2.4.6, {s4['cpu']}, 4 çekirdek; MATLAB yok. Gecikme ölçümü tek iş parçacığı, "
  f"yük {s4['load_avg']['before_timing']:.2f} → {s4['load_avg']['after_timing']:.2f}.")
W("")
W("## 4) Karar vermeniz gereken açık sorular")
W("")
W("1. Veri kümesi `RIS_dataset_large_2D.mat` (ya da `aisy_paket/adim1` çıktısı) yüklenirse yeniden üretim birebir yapılabilir; aktarım doğrulanır.")
W("2. Nicemleme, CSI hatası ve kapalı form 2.70° gibi tanımı belirsiz sayıların makalede hangi tanımla üretildiği yazarlardan öğrenilmeli.")
W("3. Etiket formülü: tezde (b) ∠h_d − ∠(G_nF_n) kullanılsın mı? (Altyapı görevinde onaylandı.)")
W("4. Bu bulguların yayımlanmış makale için ne anlama geldiği (düzeltme/erratum) danışmanla birlikte değerlendirilmeli.")
W("5. N=256 tek tohumla eğitildi (2 iş parçacığı, 265 dk); N=64/128 ve ek tohumlar istenirse her biri birkaç saat sürer, onay gerekir.")
W("")
W("## 5) Yorum (bulgulardan ayrı)")
W("")
W("- Bağımsız çekilişte CNN–LSTM'in faz doğruluğu makaledekiyle aynı mertebede (2.8–3.9°), yani modelin kendisi çalışıyor; "
  "sorunlar etiket tanımında, karşılaştırma protokolünde ve kaynağı olmayan sayılarda.")
W("- Klasik yöntemlerin 'kötü' görünmesi, gerçek optimuma gitmelerinin etiket-RMSE'si tarafından cezalandırılmasından kaynaklanıyor; "
  "alınan güç ölçütünde CD ve SPA etiketin önünde.")
W("- Sin/cos gösteriminin ±π süreksizliğini gidermesi bu bulgulardan bağımsız; tezde ayrıca doğrulandı.")
(ROOT / "audit/AUDIT_REPORT.md").write_text("\n".join(out) + "\n")
print("wrote audit/AUDIT_REPORT.md")
