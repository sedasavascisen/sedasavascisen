# Makale 2 revizyonu — değişiklik listesi (16 Kasım 2026)

**Kapsam:** Bu klasör, `paper_mobility/`'nin (dal `claude/review-ris-comparison-J8TI0`, TWC'ye hazırlanan sürüm) bir kopyası. Özgün `paper_mobility/`'ye dokunulmadı.

**Kuralla ilişkisi:** 11 Kasım kurallarının 2. ve 9. maddeleri makale metnine dokunmayı yasaklıyor. Bu revizyon, kullanıcının 16 Kasım'daki açık isteğiyle ("makale 2'yi tekrar gözden geçir düzeltmeleri yap") yapıldı. Yayımlanmış/gönderilmiş dosyaları korumak için kopyada çalışıldı.

**Sonuç:** Derlenmiş PDF `mobility_paper_ieee.pdf`, 9 sayfa (TWC ücretsiz sınırı 10). Hata ya da tanımsız referans yok.

## Değişiklikler

| # | Yer | Ne değişti | Neden | Kaynak |
| --- | --- | --- | --- | --- |
| 1 | `tables/tab_tracking.tex` (Tablo III) | 0.86 ms soğuk: L 4 → 3, hız 5.20 → 5.24; sıcak 5.42 → 5.51; fark +0.22 → +0.28. 1.71 ms: soğuk 5.09 → 5.08, sıcak 5.23 → 5.17, fark +0.15 → +0.09. 3.43 ms sıcak: L 8 → 24. 0 ms fark +0.52 → +0.53. | Benzetim pilot süresini ve devreye alma anını 0.5 ms ızgarasına yuvarlıyordu (denetim K4). Tablo, makalenin kendi tablo kodu ile düzeltilmiş veriden üretildi (`make_tab_tracking_corrected.py`). Yayımlanmış mantık dört T_p'de birebir yeniden üretildi. | `thesis_exp/p4/takip_duzeltme/` |
| 2 | §VI-E metni | "Warm starting gains up to 0.52" → 0.53 | Tablo III ile uyum. Bölümdeki diğer nitel iddiaların hepsi düzeltilmiş veride tutuyor; örneğin her satırda en fazla 8 adımlık bir politika en iyiden ayırt edilemiyor. | aynı |
| 3 | §V (yöntem), periyodik benzetim | "pilot airtime is charged as the fraction of each grid step it occupies, and each phase takes effect at its exact deployment instant" eklendi | Düzeltilmiş yöntemin tanımı | aynı |
| 4 | §V (yöntem), istatistik | Tam gecikmede değerlendirmenin etkisi eklendi: en fazla 0.027 b/s/Hz, L* aynı, L=48 maliyeti %14.0 → %14.2 | Denetim K3 sonrası Makale 2 kontrolü | `thesis_exp/p4/izgara_kontrol/` |
| 5 | §V (yöntem), gecikme | Boş makinede tek iş parçacıklı yeniden ölçüm (1.33 ms/adım) ve yeni bölüme atıf eklendi | "1.49–2.02 ms aralığında" cümlesinin yanında daha düşük bir ölçüm var; açıkça belirtildi | `thesis_exp/infra/` (dal thesis/altyapi) |
| 6 | **Yeni §VI-H "Robustness to the Remaining Assumptions"** | Beş paragraf: adım süresi, ön kodlayıcı pilotları (ve faz tutma süresi), kusurlu kanal bilgisi (pilotla birlikte), ayrık faz (1/2/3 bit) | Makalenin sınırlılık olarak bıraktığı varsayımlar artık ölçüldü | `p4/izgara_kontrol`, `p4/onkodlayici_siralama` (+ W = 25/100 ms), `p4/kusurlu_csi`, `p4/onkodlayici_csi`, `p4/ayrik_faz` |
| 7 | §VI-G "Fresh-Beam" | "whose airtime we do not charge" → "Section VI-H charges their airtime" | Artık ücretlendirildi | `p4/onkodlayici_siralama` |
| 8 | §VII Sonuç, sınırlılıklar | Ön kodlayıcı/CSI cümlesi güncellendi; faz tutma süresiyle en iyi adım sayısının arttığı eklendi; "imperfect channel knowledge and discrete phases … follow" kaldırıldı | Bu ikisi yapıldı | yukarıdakiler |
| 9 | Özet | "costs 14.0%" → "costs 14%" | Grid yöntemiyle %14.0, tam değerlendirmeyle %14.2; ikisi de "14%" | `p4/izgara_kontrol` |

## Değiştirilmeyenler (bilinçli)

- **Tablo I ve Şekil 3 (gecikmeler):** Makalenin 1.66 ms/adım gecikmesiyle bırakıldı. Yeni gecikmeyle yeniden üretim tezde var; makalede yalnızca §VI-H'de özetlendi. Tablo III de 1.66 ms ile düzeltildi; yeni gecikmeyle yeniden üretim yapılmadı.
- **Tablo III'teki seçim kuralı:** Makale zaten "best configurations are selected and reported on the same scenarios unless stated" diyor; dokunulmadı.
- **Sonuç maddesi 2 ("A few steps are optimal"):** Sınırlılıklar paragrafına "the best step count also grows when a phase is held for longer" eklendi; madde metni değişmedi.

## Gönderim notu

Makale TWC'ye gönderildiyse bu değişiklikler bir revizyon turunda ya da hakem yanıtında kullanılabilir. Gönderilmediyse doğrudan bu sürüm gönderilebilir.

Yeni bölümdeki sayıların hepsi yukarıdaki raporlara bağlıdır. Bu sayılar 11 denetim turunun kapsamındaki raporlardan alındı; denetim, sayıları bu makale metnine kopyalanmış hâliyle ayrıca sınamadı.

Sözcük ve dil kontrolünü, özellikle yeni §VI-H'yi, ortak yazarlarla birlikte yapmanız önerilir.

---

## İkinci tur (16 Kasım, iki bağımsız denetimden sonra)

Denetim raporları: `DENETIM_SAYISAL.md` ve `DENETIM_EDITOR.md`. Bütün KRİTİK bulgular ana oturumda doğrulandı ve düzeltildi.

| Bulgu | Düzeltme |
| --- | --- |
| Sayısal K1: "leaves L* unchanged" yanlıştı (tam değerde L = 4 ile 5 arasındaki fark < 0.001) | "the optimum stays at 4–6 steps" |
| Sayısal K2: "at most 0.027" Tablo I'in Adam dışı kollarını kapsamıyordu | Tablo I'in kendi gecikmeleriyle ölçüldü (`p4/izgara_kontrol/run_tab1.py`; interpolasyon yayımlanmış Tablo I'i birebir veriyor). Güven ufkunun içinde ≤ 0.006, ufkun ötesinde CD 0.008 ve uzun Adam 0.037; Adam taraması ≤ 0.027. |
| Sayısal K3: sayı kaynak dosyaları eskiydi | `paper_numbers.txt`'deki Tablo III satırları düzeltilmiş veriden yeniden yazıldı; `KEY_NUMBERS.md`'ye kaynak satırı ve §VI-H kaynak tablosu eklendi |
| Sayısal K4: "one script generates every table" ve "123 assertions" | Tablo III ile §VI-H'nin ayrı betiklerden geldiği yazıldı; 126 iddia |
| Sayısal K5: 1 bitte dCD-1'in seçildiği yumuşatılmıştı | Açıkça yazıldı: tek taramalı ayrık CD seçiliyor, yuvarlanmış SU-best-of'u +0.25 (0.16–0.33) geçiyor, en iyi yuvarlanmış Adam'la berabere. Desteklenmeyen "yalnızca" ifadesi kaldırıldı. Sınırlılıklar'a da eklendi. |
| Editör 1, 2: "All results assume" ve eskimiş cümleler | Özet, Giriş katkı 5, İlgili Çalışmalar ("continuous phases"), Sistem Modeli ("channel knowledge is perfect"), §IV atfı, §VI-G ve Sonuç güncellendi |
| Editör 3, sayısal U9: PGA tanımsız | "long-run Adam" kullanıldı |
| Editör 4: R sembolü çakışıyordu, ρ tanımsızdı | $T_{\mathrm{r}}$ kullanıldı, ρ tanımlandı |
| Editör 5, sayısal U3: farklı taban değerleri | $\bar R_W$ (W ms ortalaması, pilot net) tanımlandı; 6.08 için "effective rate (Definition 1)" denildi |
| Editör 6: "the findings hold" aşırı genel | §V'de hangi sayıların yeniden hesaplandığı tek tek yazıldı (L* = 6, %14.9, 0.26) |
| Editör 7: Practical rules | "how long the phase will be held" eklendi; Sonuç maddesi 2'ye 100 ms tutmada düz optimum (16–20) eklendi |
| Editör: alt bölüm başlığı | "Robustness to Pilots, Estimation Error and Phase Resolution" |
| Sayısal U4, U7, U8, U11 | ρ'nun ortalama güce göre olduğu ve 30 dB'de senaryo başına medyan 22.6 dB; gecikme seti; "idle" yerine yük ortalaması 0.45; Tablo III başlığına "selected on the reported scenarios"; anlık görüntülerin en yakın ızgara noktasından alındığı yazıldı |
| Sayfa | İkinci turdan sonra 10 sayfaya çıkan metin, bilgi çıkarılmadan sıkılaştırılarak yeniden **9 sayfaya** indirildi. Özet 198 kelime (TWC'ye özgü sınır 75–200). |

**Değiştirilmeyenler:** Tablo III'teki 0.86 ms satırında görünen hızlardan 0.27 çıkıyor, fark sütunu +0.28 diyor (ham fark 0.2760, yuvarlama). Fark sütunu eşli farkın kendisi olduğu için bırakıldı.
