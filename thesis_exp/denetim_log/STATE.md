# Denetim durumu (ajan günceller)

Son tur: 2026-11-12 14:00 (`20261112_1400.md`). Tur sayısı: 1.

## run.py inceleme sırası
1. thesis_exp/p4/onkodlayici_siralama/run.py — İNCELENDİ (tur 1)
2. thesis_exp/p4/onkodlayici_pilot/run.py — İNCELENDİ (tur 1)
3. thesis_exp/p4/kusurlu_csi/run.py  ← sıradaki
4. thesis_exp/p4/ayrik_faz/run.py
5. thesis_exp/p4/kanal_ongoru/run.py
6. thesis_exp/p4/konum_faz/run.py
7. thesis_exp/p4/optimize_sure/run.py (not: satır 82 Adam jit.trace hatası betiğin kendi raise'i)
8. thesis_exp/p4/common.py (tur 1'de kısmen okundu: adam_latency SU-average'ı içermiyor, U3)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/bridge_eval.py, bridge_train.py, bridge_tracking.py
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py (mumiso_mobility_latency.py ve aging_sweep_newlat.py tur 1'de kısmen okundu)
11. wt_audit: audit/scripts/step1…step6, m1_data.py, m1_train.py

## İncelenenler
- Tur 1:
  - onkodlayici_siralama/run.py: sızıntı yok, hizalı ızgara doğru. Bulgular U3, U4, U7, U11.
  - onkodlayici_pilot/run.py: H7 (biliniyor), testte R seçimi (U1).

## İzlenen rapor bölümleri
- AYRINTILI_RAPOR.md §1.1, §1.2, §5.1–5.6: bütün sayılar ham JSON'a kadar izlendi (tur 1). Yanlış sayı yok.
- TOPLU_RAPOR.md §1, §2: AYRINTILI ile çapraz kontrol edildi (tur 1). U5, U6.
- audit/AUDIT_REPORT.md §1 ve §2'den yaklaşık 12 sayı (tur 1).
- p4/*/REPORT.md: 7/7 klasör kopyada yeniden üretildi. Commit satırı dışında birebir (tur 1).
- audit_claims.py --all: 126/126 (tur 1, 56 s, tek iş parçacığı).
- Kapsanmayanlar:
  - AYRINTILI §2, §3, §4, §6–§10
  - infra/REPORT.md tablosunun geri kalanı
  - bridge/REPORT.md (origin/thesis/bridge)
  - AUDIT_REPORT §2'nin gecikme ve ölçek satırları

## Kural kontrolü notu
- `origin/master` yalnızca README içeren ilk commit. Bu yüzden `git diff origin/master -- results/ paper_mobility/` anlamsız.
- Denetim öncesi son commit `8991ea5`'e karşı karşılaştır. Tur 1'de dört dalda boş çıktı.
- `audit/` ve `thesis_exp/` dışında değişen yalnızca `.gitignore` ve `CLAUDE.md` (kullanıcı kuralları).

## Açık bulgular
- **K1 (KRİTİK, Kural 3):**
  - kanal_ongoru (`raw` commit 38b25bd) ve kusurlu_csi (`raw` commit 06fc9d2): kayıtlı commit'te run.py yok.
  - kusurlu_csi/REPORT.md:3 ve ayrik_faz/REPORT.md:3 rapor üretim HEAD'ini gösteriyor, ölçüm commit'ini değil.
  - Sayılar çürütülmedi.
- **U1:** onkodlayici_pilot/run.py:68 R'yi testte seçiyor. REPORT.md:27,40 (yanlı v1 tabloları).
- **U2:** AYRINTILI:65 (5.213, 50 ms pencere ortalaması) ile :67 (6.075, anlık Tanım 1) farklı ölçütler; ikisi de "makalenin varsayımı". 50 ms penceresinin duyarlılığı denenmedi.
- **U3:** common.py:21-22. Adam-L gecikmesi SU-average başlangıcını (0.297 ms) içermiyor. Etkisi ~0.016 b/s/Hz, dar karşılaştırmalarda belirtilmeli.
- **U4:** "sıralama değişmiyor / ilk dört aynı sırada" nokta tahmini (AYRINTILI:66, TOPLU:25, siralama REPORT:57).
- **U5:** ayrik_faz/REPORT.md:72, yorum.md:2, TOPLU:38. "dCD t=0'da her kolu geçiyor" 2 bitte yanlış; "en iyi Adam→q 5.57" yerine 5.58 olmalı.
- **U6:** TOPLU:34 "L* 10–12" yerine 8–12 olmalı.
- **U7:** siralama REPORT:52 "raw/probe.json" diyor, kod probe_aligned.json yazıyor; probe.json yanlı v1 çıktısı ama adı öyle değil.
- **U8:** ayrık faz 3 biti kapsamıyor, gerekçe yok.
- **U9:** Adam-6 etkin hızı 6.075 (infra) / 6.077 (p4), interpolasyon ızgarası farkı, belgelenmemiş.
- **U11:**
  - konum_faz σ düzeyleri arasında eşli test yok.
  - siralama seed 12 senaryo kimliği sınanmıyor.
