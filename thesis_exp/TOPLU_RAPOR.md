# Toplu teknik rapor — Görev 1–4 (12 Kasım 2026)

Bu dosya ayrıntılı raporların özetidir; her sayı ilgili raporda betik, tohum ve ham çıktıyla bağlıdır. Yeni sayı içermez.

| Görev | Dal | Rapor |
| --- | --- | --- |
| 1 — Makale 1 (AISY) denetimi | `audit/makale1-denetim` | `audit/AUDIT_REPORT.md` |
| 2 — Ortak altyapı | `thesis/altyapi` | `thesis_exp/infra/REPORT.md` |
| 3 — Köprü (tek geçişli ağ, etkin hız) | `thesis/bridge` | `thesis_exp/bridge/REPORT.md` |
| 4.1–4.6 — Altı karşılaştırma | `thesis/p4-deneyler` | `thesis_exp/p4/<deney>/REPORT.md` |

## 1) Yayımlanmış iddialarla çelişen bulgular (en önemliler önce)

**Makale 1 (AISY)** — ayrıntı: `audit/AUDIT_REPORT.md` §1
1. Denklem 8'deki etiket −∠(G_nF_n) alınan gücün maksimizörü değil; ∠h_d − ∠(G_nF_n) hiçbir örnekte daha kötü değil.
2. 1/2/3 bit nicemleme RMSE'leri (4.12/3.08/2.81°) matematiksel olarak imkânsız; etiketin kendisi nicemlendiğinde 51.95/25.98/12.98°.
3. %10 CSI hatasında 4.2° tutmuyor: model 19.00°, kapalı form 18.66°.
4. Klasik yöntemlerin RMSE'leri yayımlanan kodla üretilemiyor (CD K=5: 104.02°, makale 3.50°); bu yöntemler gerçek optimuma gidiyor ve etiketten ortak faz kadar ayrılıyor.
5. Tablo 6, Tablo 8, Şekil 1–2 elle yazılmış; Şekil 8–10 için betik yok.
6. **Yeni:** N=256 RMSE'si ölçüldü: 2.25° (tek tohum, √N gizli ölçekleme); makaledeki elle yazılmış tahmin 4.6°. N=32'nin üç tohumundan (3.18/2.77/3.90°) düşük; "N arttıkça RMSE artar" projeksiyonu desteklenmiyor.
7. Tohum yayılımı (std 0.58°) makalenin ±0.09° GA'sından çok büyük; uzamsal komşuluk kullanılmıyor (permütasyon farkı tohum yayılımından küçük).
8. Kaynakça: 64 kaynağın 33'ünde büyük sorun; [26] geri çekilmiş.

**Makale 2 (hareketlilik)** — ayrıntı: `thesis_exp/infra/REPORT.md`, `thesis_exp/p4/onkodlayici_pilot/REPORT.md`
9. **Ön kodlayıcı tazeleme pilotları ücretlendirilince etkin hız büyük ölçüde düşüyor.** Taze ve bedava W varsayımıyla en iyi kol 5.213 b/s/Hz (bu deneyin ölçütü: devreye girdikten sonraki 50 ms'nin ortalaması; Tanım 1'in anlık etkin hızı değil — o 6.075); pilot ücretiyle (R doğrulamada seçildi) 3.539 (15 kHz), 4.003 (30 kHz), 4.334 (60 kHz): %32/%23/%17 kayıp. SU-best-of 4.911 → 3.385/3.811/4.126; hiç tazelenmezse 0.761. **Sıralama korunuyor:** bütün kollarla yapılan devam deneyinde nokta tahminleriyle ilk dört kol (Adam-6, 5, 8, 4) her durumda aynı sırada; bunlar arasındaki farkların GA'sı sıfırı içeriyor, yani kesin olan sıra değil, en iyi kümenin (Adam-4…8) değişmemesi; en iyi kolun SU-best-of'a üstünlüğü +0.303'ten +0.153/+0.193/+0.209'a iniyor (GA'lar sıfırın üstünde); CD ve PGA en altta. [p4/onkodlayici_siralama/REPORT.md] *Düzeltme (12 Kasım):* bu maddenin ilk sürümündeki 3.303/3.718/4.025 ve 3.537/4.013/4.344, tazeleme anlarını mutlak ızgaraya yuvarlayan yanlı ilk koşudandı.
10. Tek iş parçacıklı yeniden ölçümle Adam adımı 1.66 değil 1.328 ms; L* = 6 (makale 5, metin 4–6), L=48 kaybı %14.4 (makale %14.0). SU-best-of − Adam-20: −0.086 [−0.174, 0.002] (makale −0.004). Ana bulgular korunuyor, sayılar değişiyor.
11. Kullanılmayan senaryo sayısı 800 değil 700 (doğrulamanın 500'ü kullanılıyor).

## 2) Görev 3 ve 4: bulgular

| Deney | Ana sonuç | Rapor |
| --- | --- | --- |
| Köprü | Tek geçişli ağ ve ağ+Adam-1/2/3 kolları 5.4 km/h'de klasik kollarca baskınlanıyor (ağ − en iyi klasik: −1.418 [−1.503, −1.336]); 3–30 km/h'nin hepsinde 4/4 öğrenilen kol baskınlanıyor; periyodik çalışmada da ağ geride. | `thesis_exp/bridge/REPORT.md` |
| 4.1 Kanal öngörüsü | Gürültüsüz anlık görüntülerle +0.19 ile +0.42 b/s/Hz kazanç ve en iyi L'nin 8–12'ye kayması; e2 = 0.01 kestirim hatasıyla bütün öngörücü/Δ birleşimleri öngörüsüzün altında (−0.10 ile −1.29). Model öngörüyü kayırıyor (sabit saçıcı, düz yörünge). | `p4/kanal_ongoru/REPORT.md` |
| 4.2 Konum tabanlı faz | Yalnızca LoS geometrisinden faz, kanal tabanlı SU-best-of'un 0.83–0.86 b/s/Hz altında; konum hatası (0–1 m) sonucu değiştirmiyor. | `p4/konum_faz/REPORT.md` |
| 4.3 Ön kodlayıcı pilotları (+ bütün kollarla sıralama) | Yukarıda madde 9. En iyi tazeleme periyodu 1–2 ms. 4.3 raporunun pilot ücretli tabloları yanlı; başında düzeltme notu var. | `p4/onkodlayici_pilot/REPORT.md`, `p4/onkodlayici_siralama/REPORT.md` |
| 4.4 Pilot SNR'li CSI | Etkin hız 6.077 (kusursuz) → 3.537 (30 dB) → 1.402 (20 dB); testte en iyi L 6 → 3 → 5 (tekdüze değil); 10 dB ve altında yöntemler ayırt edilemiyor. | `p4/kusurlu_csi/REPORT.md` |
| 4.5 Ayrık faz | L* (testte en iyi) 1 bitte 5, 2 bitte 6; Adam-48→q kaybı %9.5 / %14.1 (düzeltilmiş: tam gecikmede değerlendirme). dCD t=0'da 1 bitte önde (2 bitte değil), etkin hızda 2 bitte kaybediyor; 1 bitte yalnızca tek taramalı dCD (16.2 ms) en iyi yuvarlanmış Adam düzeyinde (eşli fark −0.044 [−0.114, +0.024]). | `p4/ayrik_faz/REPORT.md` |
| 4.6 Optimize süreler | Öğrenilen/Adam süre oranı L=8'de 2.80 (eager), 3.09 (torch.compile); torch.compile bu kodda iki kolu da yavaşlattı. jit.trace ve GPU: ÜRETİLEMEDİ. | `p4/optimize_sure/REPORT.md` |

## 3) ÜRETİLEMEDİ listesi

- Makale 1'in birebir yeniden üretimi: MATLAB ve `RIS_dataset_large_2D.mat` yok (bağımsız NumPy çekilişi kullanıldı).
- Makale 1 Şekil 9 PSO gecikmesi (MATLAB yok).
- 4.6: torch.jit.trace (iki kol), GPU (CUDA yok).
- `results/mumiso_aging_sweep_fixzf.json`: üreten betik yok (makale kullanmıyor).

Koşulmamış (üretilemeyen değil): 4.5 için 3 bit.

## 4) Açık sorular (karar sizin)

1. (Yapıldı, 12 Kasım) Pilot ücreti altında bütün kolların sıralaması: en iyi küme ve yavaş çözücülerin yeri değişmiyor (madde 9).
2. (Sürüyor) N=256 tohum 1–2, N=64 ve N=128 üçer tohum; bitince denetim raporu güncellenecek.
3. Makale 1 bulgularının yayımlanmış makale açısından ne anlama geldiği danışmanla değerlendirilmeli.
4. Ölçüm fazı 20 Kasım'da kapanıyor; yukarıdaki iki ek iş bu tarihten önce bitebilecek büyüklükte.
