# K1 çözümü — commit'li koddan bit-bit yeniden koşu (12 Kasım)

**Sorun (denetim turu 1, K1):** `p4/kanal_ongoru` (ölçüm commit'i 38b25bd) ve `p4/kusurlu_csi` (06fc9d2) koşulurken `run.py` commit'lenmemişti. Kayıtlı commit'te betik yoktu (Kural 3).

**Yapılan:** İki betik, commit'li hâlleriyle (f413f63) koşuldu.
- **Kopyadaki farklar:** Yalnızca iki satır değiştirildi: içe aktarma yolu mutlak yapıldı, çıktı klasörü scratchpad'e yönlendirildi (kopyalar ve `diff` çıktıları: `k1_rerun/run_*.py`, `k1_rerun/run_*.diff`).
- **Kimler koştu:** 4 koşu sırayla: e2 = 0, 0.01, 0.1 ve kusurlu CSI.
- **Commit numaraları:** Koşu sürerken HEAD f413f63 → 02c742c ilerledi. `git diff f413f63 02c742c -- run.py common.py ris_mu/` boş, yani betikler ve kütüphane iki commit'te aynı.

**Sonuç:** Commit alanı dışında **bütün değerler birebir aynı.**

| Dosya | Karşılaştırılan değer | Fark |
| --- | --- | --- |
| kanal_ongoru/raw/results.json | 316 | yalnızca /commit |
| kanal_ongoru/raw/results_e2_0.01.json | 316 | yalnızca /commit |
| kanal_ongoru/raw/results_e2_0.1.json | 316 | yalnızca /commit |
| kusurlu_csi/raw/results.json | 237 | yalnızca /commit |

Yeniden koşu çıktıları `thesis_exp/denetim_log/k1_rerun/` altında. Bu sayıların betik bağı artık f413f63 / 02c742c commit'lerindeki `run.py` ile kuruludur. Özgün `raw/` dosyalarına dokunulmadı.
