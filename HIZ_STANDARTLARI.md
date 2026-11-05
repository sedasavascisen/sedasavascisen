# Kullanıcı hızı: standartlar ve bu çalışmadaki karşılıkları

*6 Kasım 2026. Danışman eleştirisi: "1.5 m/s yavaş." Standartlarda iç mekân için
hangi hızların kullanıldığı aşağıda, kaynağıyla.*

## Standart değerler

| Hız | m/s | Kaynak | Ne için |
|---|---|---|---|
| **3 km/h** | 0.83 | 3GPP TR 38.913, Tablo 6.1.1-1 (Indoor hotspot): *"100% Indoor, 3km/h, 10 users per TRxP"* | İç mekân değerlendirmesinin **temel** kullanıcı hızı |
| **10 km/h** | 2.78 | ITU-R M.2410 (IMT-2020 asgari gereksinimler): yaya sınıfı 0–10 km/h; Indoor Hotspot-eMBB hareketlilik gereksinimi 10 km/h'de | İç mekân **hareketlilik testi**, yaya sınıfının üst sınırı |
| 30 km/h | 8.33 | ITU-R M.2410: Dense Urban-eMBB hareketlilik değerlendirmesi | İç mekân dışı; burada yalnızca **zorlama testi** |
| (5.4 km/h) | 1.5 | Bu çalışmanın ana değeri | 3 ile 10 km/h arasında; yaya sınıfında |

Ayrıca: ITU-R M.2410 hareketlilik sınıfları: durağan 0 km/h, yaya 0–10 km/h,
araç 10–120 km/h, yüksek hızlı araç 120–500 km/h.

**Sonuç:** 1.5 m/s, 3GPP'nin iç mekân temel hızından (3 km/h) **daha hızlı**,
ITU'nun iç mekân hareketlilik test hızından (10 km/h) daha yavaş. Bu yüzden
ana ölçümler 3, 10 ve (zorlama olarak) 30 km/h'de tekrarlandı:
`scripts/mumiso_standard_speeds.py` → `results/mumiso_standard_speeds.json`.

## Kaynaklar (erişim 6 Kasım 2026)
- 3GPP TR 38.913, "Study on scenarios and requirements for next generation access
  technologies", §6.1.1 Indoor hotspot, Tablo 6.1.1-1. Ayna:
  https://www.itecspec.com/3gpp/38.913/s/6.1.1 (resmî metin: 3gpp.org)
- 3GPP TR 38.914, §4.1 Indoor hotspot (aynı değer: 3 km/h):
  https://itecspec.com/3gpp/38.914/s/4.1
- ITU-R M.2410-0 (11/2017), "Minimum requirements related to technical performance
  for IMT-2020 radio interface(s)", §4.11 Mobility: sınıflar ("Pedestrian: 0 km/h to
  10 km/h"), Tablo 3 (Indoor Hotspot – eMBB: "Stationary, Pedestrian"), Tablo 4
  (Indoor Hotspot – eMBB: 1.5 bit/s/Hz, 10 km/h; Dense Urban – eMBB: 1.12, 30 km/h).
  **Resmî PDF'ten metin olarak doğrulandı:**
  https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-M.2410-2017-PDF-E.pdf
- ITU-R M.2412 (IMT-2020 değerlendirme kılavuzu), içindekiler:
  https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-M.2412-2017-TOC-HTM-E.htm
- IEEE 802.11-18/1573r4 (802.11ax'in IMT-2020 iç mekân öz-değerlendirmesi; hareketliliğin
  ITU-R yöntemiyle değerlendirildiğini belirtir):
  https://mentor.ieee.org/802.11/dcn/18/11-18-1573-04-AANI-summary-of-802-11ax-self-evaluation-for-imt-2020-embb-indoor-hotspot-and-dense-urban-test-environments.docx

## Karşılaştırmalı sonuç tablosu
Üretilen tablo: `TEZ_YAZIM_REFERANSI.md` → "Kullanici hizi: standartlar" bölümü, ve makalede Tablo (\ref{tab:speeds}).
