# Mühürlü teste ek: bağımsız denetimin bulguları (17 Kasım 2026)

`FINAL.md` değiştirilmedi. Bu ekteki sayılar bağımsız denetim betiğinden gelir: `thesis_exp/denetim_log/sistem_denetim.py`, rapor `DENETIM_SISTEM.md`. Betik kayıtlı küplerden hesaplar, bootstrap tohumu kendisine aittir. Denetim FINAL.md'deki 362 sayıyı doğruladı (HATA yok). H1, H2 ve H3 kararları değişmedi. Aşağıdaki karşılaştırmalar ön kayıtlı değildir.

## ⚠ En üstte: kazancın daha güçlü taban çizgilerine karşı boyutu (CLAUDE.md, zayıf taban çizgisi kuralı)

| Karşılaştırma (seed 41) | Sistem − karşılaştırma [GA] |
| --- | --- |
| Taze kip: K4 (kapalı form, protokoldeki gibi SU-average başlangıçlı) | +0.097 [+0.077, +0.118] (FINAL.md) |
| Taze kip: aynı kapalı form, SU-best-of başlangıçlı | **+0.040 [+0.029, +0.052]** |
| Taze kip: seed 12'de seçilip her koşulda sabit tutulan tek hat (best+3; seed 41'de 5.0370) | **+0.087 [+0.072, +0.102]** |
| Periyodik kip: K4 (taze hatlar) | +0.150 [+0.132, +0.170] (FINAL.md) |
| Periyodik kip: kapalı form, sıcak başlangıçlı (warm+L_K4) | **+0.020 [+0.009, +0.030]** |
| Periyodik kip: K2 sıcak başlangıçlı (warm+5) | +0.101 [+0.086, +0.117] |
| Periyodik kip: K5 sıcak başlangıçlı (warm+6) | +0.121 [+0.104, +0.137] |

**Okuma:**
- **Taze kip:** sistemin K4'e karşı kazancının yaklaşık %59'u yalnızca başlangıç seçiminden (SU-best-of) geliyor. Adım sayısını koşula göre seçmenin kendi katkısı +0.040; küçük ama anlamlı.
- **Periyodik kip:** büyük farkların çoğu sıcak başlangıçtan geliyor. Karşılaştırmalara da sıcak başlangıç verildiğinde sistemin üstünlüğü +0.020'ye iniyor, ama anlamlı kalıyor.
- **Sonuç:** sistem en güçlü taban çizgilerini de geçiyor, ancak payın çoğu üç tasarım kararının birleşiminden geliyor: başlangıç seçimi, sıcak başlangıç ve adım sayısı seçimi. Tezde bu üçü ayrı ayrı raporlanmalı.

## Ek 1'in istediği satır

Sıcak hatların taze-yalnız sisteme katkısı (seed 41, P = 20 ms): V4 5.1957, yalnızca taze 5.1445, fark **+0.051 [+0.037, +0.066]**. Bu satır `final_test.py`'nin çıktısında yoktu.

## Seçim kuralından sapma

PROTOKOL gece kuralı 2'ye göre seed 14'te ortalaması en yüksek sürüm dondurulmalıydı: tur 3'ün b = 1.1 sapmalı sürümü (5.2946). Dondurulan v1b'nin ortalaması 5.2930'du; v1b, "doğru kestirimde anlamlı kazanç yok" gerekçesiyle seçildi. `FROZEN.md`'nin "kurala göre" ifadesi bu yüzden yanlış. Seed 41'de iki sürümün farkı −0.0003 [−0.003, +0.003]; sonuçlar etkilenmez.

## Diğer sınırlar

- **H2'nin niteliği:** H2, eşdeğerlik testi değil, "anlamlı olarak kötü değil" testi. A4|W20'nin GA'sı geniş: [−0.048, +0.040].
- **Bootstrap:** protokol koşullar ve senaryolar üzerinden bootstrap tanımlıyor; kod yalnızca senaryoları yeniden örnekliyor.
- **Zamanlama:** ara L'lerin Adam süresi enterpolasyonla bulundu. Zamanlama sırasında yük 0.74'e çıktı; eşik 0.5'ti.
- **Periyodik kip:** tek bir güncelleme adımıyla, sabit bir önceki fazla kuruldu.
- **Sağlamlık:** Doppler kestirim hatası ve periyot sonuçları yalnızca seed 14'te alındı; seed 41'de sınanmadı.
- **Keşifsel doğrulama:** v1b, seed 41'de v0'ı +0.011 [+0.007, +0.015] geçiyor; seed 14'teki seçim yeni çekilişte de doğrulanıyor.
