# Denetim durumu (ajan günceller)

Son tur: 2026-11-15 04:26 (`20261115_0426.md`). Tur sayısı: 9. Makale 1 kapsam dışı (13 Kasım).

## run.py inceleme sırası
1. thesis_exp/p4/onkodlayici_siralama/run.py — İNCELENDİ (tur 1; WIN parametresi tur 4: U24, U27)
2. thesis_exp/p4/onkodlayici_pilot/run.py — İNCELENDİ (tur 1)
3. thesis_exp/p4/kusurlu_csi/run.py — İNCELENDİ (tur 2)
4. thesis_exp/p4/ayrik_faz/run.py — İNCELENDİ (tur 3); run_exact.py + run_3bit.py — İNCELENDİ (tur 4, sorun yok)
   + gecikme_muhasebesi/run.py — İNCELENDİ (tur 3)
5. thesis_exp/p4/kanal_ongoru/run.py — İNCELENDİ (tur 4; U30 q/r ızgara ucu, U31 e2 yalnız fazı bozuyor / ölçek 4.4'ten farklı)
   + izgara_kontrol/run.py — İNCELENDİ (tur 4, yeni; U32 küçük notlar)
   + onkodlayici_csi/run.py — KOD İNCELENDİ (tur 4); ham sonuçla yeniden (tur 5, yeni sorun yok)
   + rapor_pdf/build.py, 00_sade_ozet.md, 01_denetim_ozeti.md — İNCELENDİ (tur 4; U28, U29)
6. thesis_exp/p4/konum_faz/run.py — İNCELENDİ (tur 5; U43)
7. thesis_exp/p4/optimize_sure/run.py — İNCELENDİ (tur 6; U44, U46)
8. thesis_exp/p4/common.py — İNCELENDİ (tur 6; U50)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/*.py — İNCELENDİ (tur 7; K4, U51, U52, U55)
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py — İNCELENDİ (tur 7; m1_on_38901.py kapsam dışı; U53, U54)
   → Sıra bitti. Sonraki turlar: K4 sınıfı (mutlak ızgara yuvarlaması) taraması; `grep round( p4/*/run*.py` tur 7'de: yalnız onkodlayici_pilot/run.py:47,61 (bilinen v1, siralama ile yerine konmuş); csi/siralama dağıtıma hizalı.
11. thesis_exp/p4/takip_duzeltme/run.py + bridge_tracking_fix.py — İNCELENDİ (tur 8; K4 düzeltmesi doğru, --fix 0 yayımlanmış mantıkla birebir; U59–U63)
12. thesis_exp/p4/takip_duzeltme/exact_full_check.py — İNCELENDİ (tur 9; denetçi betiğinin kopyası, fark yalnız yorum + çıktı yolu)
(13. wt_audit — Makale 1, kapsam dışı)

## İzlenen rapor bölümleri
- AYRINTILI §1.2, §2–§10: tur 1–2; §5.1–5.6: tur 3; §5.1 (141–143) ve §5.5 3 bit: tur 4.
- TOPLU §1–§4: tur 1–3; 4.5 satırı tur 4.
- p4/*/REPORT.md: tur 1–3 birebir; tur 4'te ayrik_faz (1/2/3 bit), izgara_kontrol, onkodlayici_siralama (+ W=25 3b bölümü) kopyada birebir.
- kanal_ongoru `runs.*`: tur 3 ve tur 4 (3 dosya, 36 satır).
- rapor_pdf 00/01: tur 4; tur 5'te bu gecenin eklemeleri.
- Tur 5: siralama W=25/W=100 ham + §3b + yorum; onkodlayici_csi ham + REPORT + yorum; AYRINTILI §1.2/14–15, §5.7–5.9, §8; TOPLU yeni 3 satır; TEZ_TAVSIYELERI yeni 2 satır; konum_faz REPORT + AYRINTILI §5.2. Kopyada birebir: siralama, onkodlayici_csi, konum_faz.
- audit_claims.py --all: 126/126 (tur 1–3); tur 4'te ÜRETİLEMEDİ; tur 5'te boş makinede 126/126 (47 s).
- Tur 6: optimize_sure REPORT + AYRINTILI §5.6 + TOPLU:39 + TEZ:52; onkodlayici_pilot REPORT 84 hücre programla + DÜZELTME tablosu; siralama 3 pencere için ayırt edilemeyen kol kümeleri; YANIT_20261115_0026 10 madde. Kopyada birebir: optimize_sure, siralama, onkodlayici_csi; onkodlayici_pilot birebir DEĞİL (U47, elle eklenmiş DÜZELTME bloğu).
- audit_claims.py --all tur 6: 126/126 (01:32, 50 s).
- Tur 7: bridge REPORT ve infra REPORT kopyada birebir; onkodlayici_pilot (DÜZELTME dahil) ve optimize_sure kopyada birebir; bridge eval_speeds 5 hız + dominated_by yeniden hesap; definitions.json 10 süre + 6 oran; siralama 9 pencere×numeroloji seçilen kol + kümeler; köprü net_res1_lr0_s0 yeniden eğitimi bit-bit aynı.
- audit_claims.py --all tur 7: 126/126 (02:35, 49 s).
- Tur 8: takip_duzeltme REPORT §1/§2/§2b + 10 ham dosya; AYRINTILI:76/133/217/241, TOPLU:28/44, TEZ:48, 00:27, 01:20/30; paper tab_tracking.tex 12 hücre + section_06:74 beş nitel iddia fix1 ile; denetçi tam entegrasyon (S/t8/exact_full.py) 3 T_p. Kopyada birebir: takip_duzeltme, kusurlu_csi. audit_claims --all 126/126 (51 s).
- Tur 9 (son kapsamlı tur, PDF öncesi): build.py'nin bütün bölümleri (A, B §1.1/§2 hariç, C, D, Ek 1–13) tutarlılık açısından; siralama 3 pencere × 4 sütun programla (seçilen, hız, SU farkı, ayırt edilemeyen küme, Adam-3/6/48/CD/PGA farkları, ilk 4); onkodlayici_csi 6 satır; definitions.json 6 oran; takip_duzeltme fix0 4 T_p × 2 betik (fark 0) ve exact_full 3 dosya. Kopyada 11 klasörün hepsi yeniden üretildi: 10 birebir, optimize_sure DEĞİL (U65). audit_claims --all 126/126 (45 s).
- Kapsanmayanlar:
  - (siralama ana tablosu tur 9'da programla kapandı)
  - (bridge hız tablosu tur 7'de kapandı)

## Kural kontrolü notu
- Taban `8991ea5`. Tur 1–6'da dallarda (tur 5–6: HEAD, altyapi, bridge) `results/` ve `paper_mobility/` boş; dışarıda yalnızca `.gitignore`, `CLAUDE.md`.

## Arka plan işleri (tur 9, 04:26)
- Yok.

## Açık bulgular
- **U64 (tur 9):** AYRINTILI:280 (§9) ve siralama yorum.md:12/REPORT:88 "pilot ücreti ile kestirim hatası birlikte modellenmedi" — §5.9/onkodlayici_csi ile çelişiyor.
- **U65 (tur 9):** optimize_sure/REPORT.md yorum.md'nin gerisinde (REPORT:40 torch.compile nitelemesi, :52 L=1 nitelemesi yok); make_report.py yeniden koşulmalı, yoksa PDF Ek 9 eski.
- **U66 (tur 9):** siralama yorum.md:16 "Farklar küçük ama anlamlı: Adam-6 0.021…" — 15 kHz GA [−0.052, +0.008] sıfırı içeriyor.
- **U67 (tur 9):** tur sayıları/tablolar: 00:20 "yedi turda" + "açık kalan ikisi"; 01:12–20 tablo tur 7'de bitiyor, 01:22 "yalnızca K3" K4 öncesi, 01:44–46; AYRINTILI:263 tur 7'de bitiyor; TEZ:3–4 "turları 1–3"; başlıklar "11–12 Kasım" (AYRINTILI:1,3; TEZ:1; build.py:88 "11–13 Kasım").
- **U68 (tur 9):** TEZ:66 "kalan 8 gün", TEZ:70/36 eğitimler "sürüyor" (AYRINTILI:270 ve 00:21'e göre durduruldu), TEZ:95 yapılmış işler, AYRINTILI:283 "§8 bitecek".
- **U69 (tur 9):** düzeltilmiş Tablo III makale gecikmesiyle (ms_per_step 1.6625), §2b köprü kendi gecikmesiyle (Adam-L başlangıç dahil, 1.903/8.700 ms), tezin geri kalanı 1.328 ms; hiçbir yerde söylenmiyor (TEZ:48, REPORT §3, AYRINTILI §4 Adam-5 6.038 vs p4 Adam-6 6.077). Infra açık soru 2 hâlâ açık.
- **U70 (tur 9):** takip_duzeltme REPORT:3/§2b yeniden üretimi yalnız 0.86 diye yazıyor (make_report yalnız onu sınıyor); exact_full_tp*.json commit alanı yok; AYRINTILI §10 döngüsü eksik (4 klasör, run_exact/run_3bit, WIN, check_definitions, exact_full_check); AYRINTILI:22/§5 "altı karşılaştırma"; H17 etki sütunu eksik; 2.65 vs 2.656; TAM_RAPOR 70a500f'de, tur 8–9 düzeltmeleri yok (U48).
- U59, U60, U61, U63 → KAPANDI (tur 9 kontrol; U61 kalan küçük kısım U70'te). **U62 → KAPANDI** (4 T_p × 2 betik, fark 0).
- **U59 (tur 8):** fix1 pilot ücreti faz karışımına orantılı (run.py:163–169, bridge_tracking_fix.py:122–128); tam entegrasyonla politika başına ≤0.0072, seçimler ve sıcak−soğuk değişmiyor. Belge notu.
- **U60 (tur 8):** yorum.md:6 "GA genişliği kadar ya da daha fazla" — tam genişlik için yanlış (0.054 < 0.061 / 0.101); yarı genişlik için doğru.
- **U61 (tur 8):** T_p=0 "değişmiyor" ama iki basamakta +0.52→+0.53 (tab_tracking.tex:6, section_06:74); seçilen L iki hücrede değişiyor (0.86 soğuk 4→3, 3.43 sıcak 8→24); özetlerde tam düzeltilmiş satır yok. Makalenin 5 nitel iddiası fix1'de tutuyor.
- **U62 (tur 8):** --fix 0 yeniden üretimi yalnız T_p=0.86 (kod diff'iyle diğerleri eşdeğer). Küçük.
- **U63 (tur 8):** fix*.json commit 238d846 (koşu sonu okunuyor; run.py aynı); bridge_tracking_fix.py:24 scratchpad yoluna bağlı, yedeği yok; :20 docstring çıktı yolu eski; run.py:34 "50-200 ms" miras.
- **K4 → KAPANDI (tur 8):** düzeltilmiş kopyalar doğrulandı; kalanlar U59–U63.
- **K4 (tur 7, KRİTİK):** bridge_tracking.py:75,85,95 ve yayımlanmış scripts/mumiso_tracking.py:91,107,111 pilot süresini ve devreye almayı mutlak 0.5 ms ızgaraya yuvarlıyor (0.86→1.0, 1.71→1.5 ms; b2b'de değişken). Birinci derece tahmin (ölçüm değil, S/bridge_t7/est/pilot_rounding.py): köprü ağ−soğuk T_p=0.86 −0.153→≈−0.066; Tablo III sıcak−soğuk 0.86 +0.222→≈+0.267, 1.71 +0.146→≈+0.095. Kesirli ağırlıklı kopya betikle yeniden koşu gerekli.
- **U51 (tur 7):** köprü seçim eğitimleri commit 349d253 (betik yok); seçilen yapılandırma bit-bit yeniden üretildi, diğer üçü değil.
- **U52 (tur 7):** "Makale 1'in ağı RMSE'de iyi, etkin hızda baskınlanıyor" (TEZ:13, 00:19, AYRINTILI:123) — köprü ağı MuMisoNet (yalnız gövde ortak), RMSE ile ölçülmedi, ≈ SU-average (t0 4.6264 / 4.6240).
- **U53 (tur 7):** static_split_usage.py sabit kodlu; mumiso_unrolled.py:141 testin 900'ünü kullanıyor; "700" yalnızca "yayımlanmış sayıya giren" tanımıyla doğru (AYRINTILI:68/113, TOPLU:27, infra §1.4).
- **U54 (tur 7):** aging_sweep_newlat.py:10–12, stats_newlat.py:8–9 docstring eski gecikme tanımı; "wrote results/" print'leri; mobility_latency tek senaryo.
- **U55 (tur 7):** tracking NET_STEPS ≤ 3; eval TIMES 40 ms üstü kaba (Adam-32/48). Küçük.
- **U56 (tur 7):** 3.09 compile oranı yorum.md:1/AYRINTILI:189/TOPLU:39'da niteleme dışı; L=1'de "~2.7 tanımdan bağımsız" değil; check_definitions.py dirty yok; TEZ:46/AYRINTILI:70,74/00:25 15 kHz istisnaları; 01:32 W=50 kaydı; AYRINTILI:255 "00:2x"; 00:20 ve 01 tablo güncel değil.
- **U57 (tur 7):** common.commit() izlenmeyen dosyaları görmüyor (küçük).
- **U58 (tur 7):** mumiso_tracking.py:149 Tablo III politikasını raporlanan kümede seçiyor.
- U47 → GERİ ÇEKİLDİ (tur 7; kopyada kardeş klasör eksikti). U44 → büyük ölçüde KAPANDI (kalan U56). U45 → W=50 için KAPANDI (kalan U56/4). U46 → kısmen (U56/1). U49 → kısmen (U56/5). U50 → KAPANDI (not U57). U36 → KAPANDI. U48 açık (PDF 07:15 planı).
- **U44 (tur 6):** optimize_sure: Adam kolu SU-average başlangıcını içeriyor (run.py:47), öğrenilen kol öznitelik+başlangıç hariç (run.py:39–41,65) ve enable_grad altında (run.py:109 ölü `and False`; makale mumiso_step_cost.py:46,50 no_grad). Denetçi kontrolü: L=1 oranı 1.86 (run.py tanımı) / 2.66 (makale tanımı) / 2.14 (simetrik); L=8 2.87 / 2.72 / 2.64. Hüküm aynı; belge eksik.
- **U45 (tur 6, öncelikli):** W=50'de seçilenden ayırt edilemeyen küme Adam-3…20 (üç numeroloji), "Adam-4…8" değil. W=25/15 kHz'de Adam-2 de; W=100/15 kHz'de Adam-5…48. Etkilenen: siralama yorum.md:1–3, AYRINTILI:64/66, TOPLU:25, TEZ:45/46, 00_sade_ozet:25/31, 01_denetim_ozeti:32.
- **U46 (tur 6):** TEZ:52, TOPLU:39, AYRINTILI:189 "oran 2.8–3.1" — compile satırı optimize sürüm değil (yeniden derleme sınırı, karmaşık sayı); yorum.md:6 söylüyor, özetler söylemiyor.
- **U47 (tur 6):** onkodlayici_pilot REPORT.md:3–11 DÜZELTME bloğu elle; make_report.py üretmiyor.
- **U48 (tur 6):** TAM_RAPOR.html/pdf (00:25) tur 5 düzeltmelerinden önce; HTML:169 ve :2179 "denenmedi".
- **U49 (tur 6):** AYRINTILI:254 cümle bozuk (tur 4 YANIT atfı tur 5 cümlesine kaymış).
- **U50 (tur 6):** common.py: commit() kirli bayrağı yok (K1/U24/U38 kökü); check_same_scenarios yalnızca t=0 tek skaler; effective() ölü (aralık dışı sabit uç).
- U34 → metinlerde KAPANDI, PDF kısmı U48'e taşındı. U35, U37–U43 → KAPANDI (tur 6 kontrol). U36 → büyük ölçüde KAPANDI (TEZ_TAVSIYELERI'nde sınır cümlesi yok; küçük). CPU notu → KAPANDI (ayrik_faz yorum.md:15). Kural 7 onay kaydı YANIT'ta (kabul).
- **U24:** run.py:107 commit() hâlâ sonda (belgelendi; bkz. U38).
- U25, U26, U28 → KAPANDI (tur 5'te kontrol edildi; U26 kısmen, bkz. U41). U27 → kısmen (U39).
- U29 → büyük ölçüde KAPANDI (tur 5); kalan kısım U34'te.
- U30, U31, U32 → KAPANDI (AYRINTILI:152, izgara yorum.md; tur 5).
- **K3:** tur 4'te run_exact/run_3bit ile çözülmüş olarak doğrulandı → KAPANDI. U20 → KAPANDI (lr-val tasarımı). U21–U23 → KAPANDI (YANIT_20261112_1532.md, kontrol edildi).
- **U11:** konum_faz σ farkları için eşli test yok (açık).
- **U19:** bridge raporunda aynı fark iki GA ile (başka dal; dokunulmadı).
