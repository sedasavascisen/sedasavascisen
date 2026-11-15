# Denetim durumu (ajan günceller)

Son tur: 2026-11-15 01:26 (`20261115_0126.md`). Tur sayısı: 6. Makale 1 kapsam dışı (13 Kasım).

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
9. origin/thesis/bridge: thesis_exp/bridge/scripts/*.py  ← sıradaki
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py
(11. wt_audit — Makale 1, kapsam dışı)

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
- Kapsanmayanlar:
  - siralama tabloları satır satır (ana tablo);
  - bridge hız tablosu.

## Kural kontrolü notu
- Taban `8991ea5`. Tur 1–6'da dallarda (tur 5–6: HEAD, altyapi, bridge) `results/` ve `paper_mobility/` boş; dışarıda yalnızca `.gitignore`, `CLAUDE.md`.

## Arka plan işleri (tur 6, 01:26)
- Yok.

## Açık bulgular
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
