# Denetim durumu (ajan günceller)

Son tur: 2026-11-12 14:31 (`20261112_1431.md`). Tur sayısı: 2.

## run.py inceleme sırası
1. thesis_exp/p4/onkodlayici_siralama/run.py — İNCELENDİ (tur 1)
2. thesis_exp/p4/onkodlayici_pilot/run.py — İNCELENDİ (tur 1)
3. thesis_exp/p4/kusurlu_csi/run.py — İNCELENDİ (tur 2; csi.py `_noisy`/`rates_mismatched` dahil)
4. thesis_exp/p4/ayrik_faz/run.py  ← sıradaki (dCD zamanlaması, yuvarlama bedava, 1 bit dCD-1 − Adam-5→q eşli fark yok)
5. thesis_exp/p4/kanal_ongoru/run.py
6. thesis_exp/p4/konum_faz/run.py
7. thesis_exp/p4/optimize_sure/run.py (not: satır 82 Adam jit.trace hatası betiğin kendi raise'i)
8. thesis_exp/p4/common.py (tur 1–2'de kısmen okundu: adam_latency SU-average'ı içermiyor, U3)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/bridge_eval.py, bridge_train.py, bridge_tracking.py
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py (mumiso_mobility_latency.py, aging_sweep_newlat.py kısmen; make_infra_report.py tur 2'de koşuldu)
11. wt_audit: audit/scripts/step1…step6, m1_data.py, m1_train.py (make_audit_report.py tur 2'de koşuldu)

## İncelenenler
- Tur 1: onkodlayici_siralama (U3, U4, U7, U11), onkodlayici_pilot (H7, U1).
- Tur 2: kusurlu_csi/run.py — seçim doğrulamada, eşli gürültü, sızıntı yok. Bulgular U12, U13, U14.

## İzlenen rapor bölümleri
- AYRINTILI §1.1, §1.2, §5.1–5.6: tur 1'de bütün sayılar. §2, §3, §4, §5.4, §6–§10: tur 2.
- TOPLU §1–§4: tur 1–2.
- AUDIT_REPORT §1–§2: tur 1'de yaklaşık 12 sayı; tur 2'de gecikme ve ölçek satırları (0.80/1.11/1.64/2.66, 3.3×/13.6×).
- infra/REPORT.md ve bridge/REPORT.md: tur 2'de make_*_report.py kopyada koşuldu, birebir aynı. Yani bütün tablo ham veriye bağlı.
- AUDIT_REPORT.md: tur 2'de make_audit_report.py kopyada koşuldu (commit'li dosyalarla), birebir aynı.
- p4/*/REPORT.md, 7 klasör: tur 1 ve tur 2'de yeniden üretildi, birebir aynı.
- TEZ_TAVSIYELERI.md (yeni, 02c742c): tur 2 (U17).
- audit_claims.py --all: 126/126 (tur 1 ve tur 2).
- Kapsanmayanlar:
  - kanal_ongoru `runs.*` GA'larının tek tek kontrolü (yalnızca aralık uçları bakıldı).
  - konum_faz σ satırları tek tek.
  - optimize_sure tur dağılımları.

## Kural kontrolü notu
- Karşılaştırma tabanı `8991ea5`. Tur 1 ve 2'de dört dalda `results/` ve `paper_mobility/` boş çıktı.
- Dışarıda değişen yalnızca `.gitignore` ve `CLAUDE.md`.

## Arka plan eğitimleri (tur 2 anı)
- N=64 s0 bitti: 3.049°, commit `089c578`, henüz commit'lenmedi.
- N=128 s0: 20/50. epok.
- N=256 s1: 21/50. epok (~540 s/epok).

## Açık bulgular
- **K1:** değerler bit-bit doğrulandı (tur 2). Belge eksikleri U15'te. K1 kapatılabilir, U15 açık.
- **K2 (KRİTİK, yeni):** ayrik_faz/yorum.md:2 ve REPORT.md:72 "dCD-1 (6.14) Adam-8…48→q'nun altında" yanlış. Adam-8→q 6.1068 < 6.1407; doğrusu Adam-10…48.
- **U1:** H12 ile kapandı (R'ler aynı: 2/1/1, doğrulandı).
- **U2, U4, U6, U7, U9, U10:** düzeltildi (tur 2'de doğrulandı).
- **U3:** metin düzeltildi; sayısı U16'da.
- **U5:** düzeltildi, ama K2'yi getirdi.
- **U8:** kısmen düzeltildi; TOPLU'da eksik (U18).
- **U11:** konum_faz σ eşli testi açık.
- **U12:** kusurlu_csi REPORT.md:25 / make_report.py:22 ve TEZ_TAVSIYELERI.md:46. "Hata büyüdükçe L* küçülüyor" desteklenmiyor (6/3/5/1/6/4).
- **U13:** ρ "katsayı başına pilot SNR'si" değil. Hata ölçeği yığın genelinde (csi._noisy). ρ=30 dB, G için senaryo başına medyan 22.6 dB demek. val/test yığın gücü farklı.
- **U14:** kusurlu_csi lr sınırda (5 dB, 0 dB); teslim anı kestirimi ücretsiz; val'de check_same_scenarios yok.
- **U15:** K1 belge eksiği. REPORT'lar k1_rerun'a bağlanmamış; iki satırlık diff depoda yok.
- **U16:** "~0.016 b/s/Hz" betiksiz (AYRINTILI:136, ayrik_faz yorum:3, TEZ_TAVSIYELERI:59).
- **U17:** TEZ_TAVSIYELERI.md:
  - :44 kaynak yanlış (x = ΔT·f_d infra REPORT'ta yok);
  - :3-4 "yanlış sayı yok";
  - :99-102 CSI aşırı iddiası;
  - Kural 9 sınırı.
- **U18:** TOPLU ÜRETİLEMEDİ listesinde sweep_fixzf ve 3 bit eksik; AYRINTILI §7'de 3 bit yanlış kategoride.
- **U19 (küçük):** bridge REPORT'ta 5.4 km/h için aynı farka iki ayrı GA.
