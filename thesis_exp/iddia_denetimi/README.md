# İddia denetleyicisi (12–16 Kasım sayıları)

```bash
python3 thesis_exp/iddia_denetimi/check_claims.py              # 89 iddia; çıkış kodu 0 = hepsi tutuyor
python3 thesis_exp/iddia_denetimi/check_claims.py --sabotage   # öz-sınama: ham dosyaların kopyalarında 8 bozma, hepsi yakalanmalı
```

**Ne yapar:** `scripts/audit_claims.py` sayıları kütüphaneden yeniden hesaplar. Bu betik ise metne yazılan sayıların ve istatistiksel ifadelerin ("tied", "significantly behind", "at most") saklanmış ham çıktılarla tutarlı olduğunu sınar. İfadeler, yanlarında saklanan bootstrap GA'larıyla karşılaştırılır.

**Kapsam:**
- Revize Makale 2'nin Tablo III'ü, §V'deki tam gecikme ve yeniden ölçüm notları, §VI-H'nin bütün sayı ve ifadeleri.
- Sonuç'taki %17–32.

**Kaynaklar:**
- `thesis_exp/p4/*/raw/*.json`
- `results/mumiso_tracking.json` (salt okunur)
- `origin/thesis/altyapi` dalındaki yeniden ölçüm dosyası
- `thesis_exp/denetim_log/scripts/u13_csi_rel_err.out`

**İlk koşu (16 Kasım):** 89/89 iddia tutuyor; sabotaj 8/8 yakalandı.

**Kural:** Yeni bir sayı teze ya da makaleye girerse, önce buraya bir iddia olarak eklenir.
