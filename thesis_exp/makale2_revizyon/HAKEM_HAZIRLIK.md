# Hakem sorarsa: statik kümenin alt kümeleri (Şekil 5)

Karar (22 Kasım 2026, kullanıcı): makale bu hâliyle gönderilir. 900 test senaryosuyla kontrol, yalnızca hakem isterse yapılır.

## Olası soru 1: "Neden iki yöntem farklı doğrulama alt kümeleriyle ayarlandı?"

**Durum: ölçüldü, kapandı.**
- Adam'ın 400 senaryosu, öğrenilen modelin 500 senaryosunun ilk 400'ü; iki küme ayrık değil.
- Adam bütün 500 senaryoda ayarlanınca da her bütçede (L = 1…64) aynı ayarı seçiyor: 0.75, soft-min. Bütün sonuçlar birebir aynı.
- Makalede: "(all 500 give the same choice)".
- Kaynak: `veri_bolme/saglamlik_900.py` → `saglamlik_900.json` (V1a). V0 yayımlanan sayıları fark 0 ile yeniden üretiyor.

## Olası soru 2: "900 test senaryosunun 300'üne ne oldu?"

**Durum: açık; hakem isterse yapılacak.**
- 600, betiklerin varsayılan değeri (`--eval-n 600`). Gerekçesi hiçbir yerde yazılı değil. "Prefix-stable" cümlesi bunu açıklamıyor; makaleye uydurma bir gerekçe yazılmadı.
- Adam tarafı 900 senaryoda hesaplandı (`saglamlik_900.json`, V1). Öğrenilen kural için ağırlıklar gerekiyor.

Hakem isterse iki yol var:
1. **Ağırlık arşivi bulunursa:** `ris_mu_agirliklar_2026-10-27.tar.gz` depo köküne açılır ve `python3 thesis_exp/makale2_revizyon/veri_bolme/saglamlik_900.py` koşturulur. Yaklaşık 1 dakika sürer. Betik ağırlıkları kendisi bulur ve V1'i tamamlar.
2. **Arşiv yoksa:** beş model yeniden eğitilir. Komut, her L ∈ {1, 2, 4, 8, 16} için:
   `python3 scripts/mumiso_unrolled.py --samples 6000 --epochs 12 --steps L --mode exchange --use-grad --bs 32 --lr 0.001 --baseline-n 300 --seed 11 --tag eqstep_L{L}`
   - Ayarlar `results/mumiso_eqstep_L*.json` config'inden alındı.
   - İlk eğitim 2 saat 18 dakika sürmüştü (`results/run_eqstep_all.log`).
   - Önce 600 senaryoda yayımlanan sayılarla karşılaştırılır (V0). Birebir değilse bu açıkça yazılır.
   - Çıktılar `results/`'e değil `thesis_exp/` altına yönlendirilmeli (Kural 2).

**Hakeme önerilen yanıtın özü:** alt küme boyutları betiklerin sabit varsayılanları. Doğrulama alt kümesinin sonuca etkisi yok (ölçüldü). 900 senaryonun hepsiyle değerlendirme isteğe göre yapılabilir.
