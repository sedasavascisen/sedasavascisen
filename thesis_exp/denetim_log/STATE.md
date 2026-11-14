# Denetim durumu (ajan günceller)

Son tur: 2026-11-14 23:26 (`20261114_2326.md`). Tur sayısı: 4. Makale 1 kapsam dışı (13 Kasım).

## run.py inceleme sırası
1. thesis_exp/p4/onkodlayici_siralama/run.py — İNCELENDİ (tur 1; WIN parametresi tur 4: U24, U27)
2. thesis_exp/p4/onkodlayici_pilot/run.py — İNCELENDİ (tur 1)
3. thesis_exp/p4/kusurlu_csi/run.py — İNCELENDİ (tur 2)
4. thesis_exp/p4/ayrik_faz/run.py — İNCELENDİ (tur 3); run_exact.py + run_3bit.py — İNCELENDİ (tur 4, sorun yok)
   + gecikme_muhasebesi/run.py — İNCELENDİ (tur 3)
5. thesis_exp/p4/kanal_ongoru/run.py — İNCELENDİ (tur 4; U30 q/r ızgara ucu, U31 e2 yalnız fazı bozuyor / ölçek 4.4'ten farklı)
   + izgara_kontrol/run.py — İNCELENDİ (tur 4, yeni; U32 küçük notlar)
   + onkodlayici_csi/run.py — KOD İNCELENDİ (tur 4, koşu sürüyor; U25 eşsiz gürültü + tohum çakışması, U26 lr 4.4'ten)
   + rapor_pdf/build.py, 00_sade_ozet.md, 01_denetim_ozeti.md — İNCELENDİ (tur 4; U28, U29)
6. thesis_exp/p4/konum_faz/run.py  ← sıradaki
7. thesis_exp/p4/optimize_sure/run.py
8. thesis_exp/p4/common.py (kısmen okundu: commit(), boot global rng, curve/minrate gerçek kanalda ZF)
9. origin/thesis/bridge: thesis_exp/bridge/scripts/*.py
10. origin/thesis/altyapi: thesis_exp/infra/scripts/*.py
(11. wt_audit — Makale 1, kapsam dışı)

## İzlenen rapor bölümleri
- AYRINTILI §1.2, §2–§10: tur 1–2; §5.1–5.6: tur 3; §5.1 (141–143) ve §5.5 3 bit: tur 4.
- TOPLU §1–§4: tur 1–3; 4.5 satırı tur 4.
- p4/*/REPORT.md: tur 1–3 birebir; tur 4'te ayrik_faz (1/2/3 bit), izgara_kontrol, onkodlayici_siralama (+ W=25 3b bölümü) kopyada birebir.
- kanal_ongoru `runs.*`: tur 3 ve tur 4 (3 dosya, 36 satır).
- rapor_pdf 00/01: tur 4.
- audit_claims.py --all: 126/126 (tur 1–3); tur 4'te ÜRETİLEMEDİ (yük altında >10 dk, durduruldu). Makine boşken koşulmalı.
- Kapsanmayanlar:
  - onkodlayici_pilot / siralama tabloları satır satır;
  - W=100 ve onkodlayici_csi ham sonuçları (koşu sürüyor);
  - bridge hız tablosu.

## Kural kontrolü notu
- Taban `8991ea5`. Tur 1–4'te dört dalda `results/` ve `paper_mobility/` boş; dışarıda yalnızca `.gitignore`, `CLAUDE.md`.

## Arka plan işleri (tur 4, 23:26)
- onkodlayici_csi/run.py (THREADS=2) 23:04'ten beri sürüyor; ρ=30 dB kolları ilerliyor.
- onkodlayici_siralama WIN=100 (THREADS=2) 23:20'den beri sürüyor. W=25 bitti, ec03907'de commit'lendi (commit alanı 66aa57b, U24).
- m1_train yok (Makale 1 durduruldu).

## Açık bulgular
- **U24:** onkodlayici_siralama/run.py:107 commit() koşu sonunda; W=100 sonucunun commit alanı başlangıç HEAD'i olmayabilir.
- **U25:** onkodlayici_csi/run.py:49 kestirim gürültüsü kollar arasında eşsiz (4.4 eşliydi); doğrulama kolu j+10 = test kolu j tohumu.
- **U26:** onkodlayici_csi lr 4.4'ten (farklı ölçüt); raporda belirtilmeli.
- **U27:** siralama docstring "50 ms"; sabit 1−t_p/R ücreti kısa pencerede büyük R'yi hafif kayırıyor.
- **U28:** 01_denetim_ozeti.md:18 "K3 dışında ham veriyle çelişen sayı yok" yanlış (K2, U5, U6).
- **U29:** 00_sade_ozet.md:18/:20/:25 aşırı iddialar ("5–8 adım, her durumda", "en iyi değişmiyor", "hepsi düzeltildi"); build.py:3/:85 "yeni sayı içermez" ama A/C bölümleri elle yazılmış sayılar içeriyor; PDF izgara_kontrol'ü içermiyor.
- **U30:** kanal_ongoru kalman q/r = 100 (ızgara ucu) e2=0'da.
- **U31:** kanal_ongoru e2 yalnızca fazı bozuyor (ZF gerçek kanalda); hata ölçeği 4.4'ten farklı; belgelenmeli.
- **U32:** izgara_kontrol/yorum.md betiksiz 13.96; "makalenin adım kümesi" ayrımı; çift yuvarlama 0.287.
- **K3:** tur 4'te run_exact/run_3bit ile çözülmüş olarak doğrulandı → KAPANDI. U20 → KAPANDI (lr-val tasarımı). U21–U23 → KAPANDI (YANIT_20261112_1532.md, kontrol edildi).
- **U11:** konum_faz σ farkları için eşli test yok (açık).
- **U19:** bridge raporunda aynı fark iki GA ile (başka dal; dokunulmadı).
