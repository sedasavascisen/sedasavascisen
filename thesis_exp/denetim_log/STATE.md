# Denetim durumu (ajan günceller)

Son tur: 2026-11-15 00:26 (`20261115_0026.md`). Tur sayısı: 5. Makale 1 kapsam dışı (13 Kasım).

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
7. thesis_exp/p4/optimize_sure/run.py  ← sıradaki
8. thesis_exp/p4/common.py (kısmen okundu: commit(), boot global rng, curve/minrate gerçek kanalda ZF)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/*.py
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
- Kapsanmayanlar:
  - onkodlayici_pilot / siralama tabloları satır satır;
  - bridge hız tablosu.

## Kural kontrolü notu
- Taban `8991ea5`. Tur 1–5'te dallarda (tur 5: HEAD, altyapi, bridge) `results/` ve `paper_mobility/` boş; dışarıda yalnızca `.gitignore`, `CLAUDE.md`.

## Arka plan işleri (tur 5, 00:26)
- Yok. W=100 (00:22) ve onkodlayici_csi (00:09) bitti, 803d678'de commit'lendi.

## Açık bulgular
- **U34 (öncelikli):** W=100 sonucuyla çelişen eski cümleler: siralama yorum.md:5 ve AYRINTILI:65, TEZ_TAVSIYELERI:60 "50 ms duyarlılığı denenmedi"; AYRINTILI:64, TOPLU:25, TEZ_TAVSIYELERI:45, siralama yorum.md:1–4, 00_sade_ozet:18/:31 W=50 kaydı yok; PDF de eskiyi taşıyor.
- **U35:** 00_sade_ozet:25 "en fazla 0.04", TEZ_TAVSIYELERI:46 "≤ 0.04" yalnızca Adam-6+ için doğru (Adam-5 0.044/0.047, Adam-3 0.078).
- **U36:** "W = fazın yeniden hesaplanma aralığı" eşitlemesi gecikmesi W'yi aşan kollar için geçersiz; sınır cümlesi gerek.
- **U37:** "periyodik çalışma sonuçlarıyla tutarlı" atfı: köprü §1 madde 5 (§5 değil), Makale 2 değil; U ve L T_p ile birlikte seçiliyor.
- **U38:** siralama yorum.md: W=100 başlangıç HEAD'i 66aa57b, 97e5e5c değil (zararsız).
- **U39:** siralama run.py:17 docstring hâlâ "lat + 50".
- **U40:** W=25'te Adam-3 testte birinci; "Adam-3…8 ayırt edilemiyor" olmalı.
- **U41:** onkodlayici_csi yorum.md "her şeyi bastırıyor" aşırı; U26 etki cümlesi eksik.
- **U42:** tur 4 "10 uyarı (U24–U33)" — günlükte 9 (U24–U32); 00_sade_ozet:20 "üç turda".
- **U43:** konum_faz run.py: mean_rate_0_200ms ağırlıksız ortalama (≈0–40 ms); geom-best seçimi pt=nv=1 ile; U11 hâlâ açık.
- CPU notu (ayrik_faz dCD zamanlaması) henüz eklenmedi; W=100 (62 dk) onay kaydı teyit edilmeli.
- **U24:** run.py:107 commit() hâlâ sonda (belgelendi; bkz. U38).
- U25, U26, U28 → KAPANDI (tur 5'te kontrol edildi; U26 kısmen, bkz. U41). U27 → kısmen (U39).
- U29 → büyük ölçüde KAPANDI (tur 5); kalan kısım U34'te.
- U30, U31, U32 → KAPANDI (AYRINTILI:152, izgara yorum.md; tur 5).
- **K3:** tur 4'te run_exact/run_3bit ile çözülmüş olarak doğrulandı → KAPANDI. U20 → KAPANDI (lr-val tasarımı). U21–U23 → KAPANDI (YANIT_20261112_1532.md, kontrol edildi).
- **U11:** konum_faz σ farkları için eşli test yok (açık).
- **U19:** bridge raporunda aynı fark iki GA ile (başka dal; dokunulmadı).
