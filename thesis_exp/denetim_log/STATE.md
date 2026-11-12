# Denetim durumu (ajan günceller)

Son tur: 2026-11-12 15:32 (`20261112_1532.md`). Tur sayısı: 3.

## run.py inceleme sırası
1. thesis_exp/p4/onkodlayici_siralama/run.py — İNCELENDİ (tur 1)
2. thesis_exp/p4/onkodlayici_pilot/run.py — İNCELENDİ (tur 1)
3. thesis_exp/p4/kusurlu_csi/run.py — İNCELENDİ (tur 2; csi.py `_noisy`/`rates_mismatched` dahil)
4. thesis_exp/p4/ayrik_faz/run.py — İNCELENDİ (tur 3; K3 ızgara, U20 lr)
   + thesis_exp/p4/gecikme_muhasebesi/run.py — İNCELENDİ (tur 3, yeni betik; sorun yok, U23'te belge eksiği)
5. thesis_exp/p4/kanal_ongoru/run.py  ← sıradaki (kalman q/r seçimi doğrulamada mı; öngörü ufku; e2'li öngörüsüz kol; ızgara U21)
6. thesis_exp/p4/konum_faz/run.py
7. thesis_exp/p4/optimize_sure/run.py (not: satır 82 Adam jit.trace hatası betiğin kendi raise'i; learned-1 compile 1. tur 133 ms ısınma)
8. thesis_exp/p4/common.py (tur 1–3'te kısmen okundu: adam_latency SU-average'ı içermiyor; GRID her betikte ayrı)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/bridge_eval.py, bridge_train.py, bridge_tracking.py
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py (yaşlanma taramalarında kaba ızgara/interpolasyon var mı — K3 bağlantısı)
11. wt_audit: audit/scripts/step1…step6, m1_data.py, m1_train.py

## İncelenenler
- Tur 1: onkodlayici_siralama (U3, U4, U7, U11), onkodlayici_pilot (H7, U1).
- Tur 2: kusurlu_csi/run.py — seçim doğrulamada, eşli gürültü, sızıntı yok. Bulgular U12, U13, U14.
- Tur 3: ayrik_faz/run.py — seçim doğrulamada, tohumlar doğru, dCD zamanlaması boş makinede; ızgara 40 ms üstünde kaba (K3), Adam lr taranmamış (U20). gecikme_muhasebesi/run.py — doğru; ayrik_faz ile ≤ 40 ms kollarda 4 basamak aynı.

## İzlenen rapor bölümleri
- AYRINTILI §1.1, §1.2, §2–§10: tur 1–2. §5.1–5.6: tur 3'te yeniden, hepsi.
- TOPLU §1–§4: tur 1–3.
- AUDIT_REPORT §1–§2: tur 1–2.
- infra/REPORT.md, bridge/REPORT.md, AUDIT_REPORT.md: tur 2'de kopyada birebir yeniden üretildi.
- p4/*/REPORT.md: 7 klasör tur 1–2'de birebir; tur 3'te değişen ayrik_faz, kusurlu_csi, kanal_ongoru yeniden birebir.
- kanal_ongoru `runs.*`: tur 3'te 36 satırın hepsi (GA'lar dahil).
- konum_faz σ satırları: tur 3'te hepsi.
- optimize_sure turları: tur 3'te hepsi.
- TEZ_TAVSIYELERI.md: tur 2–3.
- audit_claims.py --all: 126/126 (tur 1, 2, 3).
- Kapsanmayanlar:
  - onkodlayici_pilot / onkodlayici_siralama tablolarının satır satır kontrolü (tur 1'de örneklem).
  - bridge REPORT hız tablosu satır satır.
  - infra aging sweep ızgarası.

## Kural kontrolü notu
- Karşılaştırma tabanı `8991ea5`. Tur 1–3'te dört dalda `results/` ve `paper_mobility/` boş.
- Dışarıda değişen yalnızca `.gitignore` ve `CLAUDE.md`.

## Arka plan eğitimleri (tur 3 anı, 15:32)
- N=64 s0 bitti: 3.049° (commit'lenmedi).
- N=128 s0 bitti: 2.580°, SR@5 %97.0, 101 dk (commit'lenmedi).
- N=256 s1: 31/50. epok.
- N=64 s1: 15:32'de başladı.

## Açık bulgular
- **K3 (KRİTİK, yeni):** ayrik_faz/run.py:23 ızgarası 40 ms üstünde 50/75/100/150 ms. 11 kolun etkin hızı ±0.055'e kadar yanlış. Adam-48→q kaybı %9.3/%13.6 → tam anda %9.5/%14.1. Yerler: yorum.md:1, REPORT.md:71, AYRINTILI:167, TOPLU:38. Hükümler büyük olasılıkla değişmiyor; GA'lar yeniden hesaplanmalı.
- **U20:** ayrik_faz Adam lr 0.5 sabit; kusursuz CSI'da doğrulama 8 L için 0.75, L48 için 1.0 seçiyor.
- **U21:** aynı kaba ızgara kanal_ongoru:38, kusurlu_csi:22, konum_faz:25'te. Yalnızca Adam-32/48 satırları etkileniyor, seçilen kollar değil.
- **U22:** kusurlu_csi REPORT.md:3 lr sınır cümlesi eksik; uç değerler her düzeyde var, seçilen kolda yalnızca 5/0 dB.
- **U23:** küçük izler:
  - kusurlu_csi/run.py:5 docstring "per coefficient";
  - TOPLU:37 "L*" testte argmax etiketi yok;
  - TEZ_TAVSIYELERI:4 "ham veriyle çelişen sayı yok" K3 ile eskidi;
  - gecikme_muhasebesi REPORT yok;
  - u13 .out commit taşımıyor;
  - ana oturum yanıtı denetçi günlüğüne eklendi.
- **Kapandı (tur 3'te doğrulandı):** K1, K2, U12, U13, U15, U16, U17, U18. U14 → U22 ile kısmen açık. U19 gerekçeyle dokunulmadı.
- **U11:** konum_faz σ farkları için eşli test hâlâ yok ("konum hatası sonucu değiştirmiyor"). Satır değerleri doğru.
- **Not:** AUDIT_REPORT.md:16 ve :70 "N=64/128 eğitilmedi" eskidi. s0 dizisi 3.049 / 2.580 / 2.247°; tek tohum.
