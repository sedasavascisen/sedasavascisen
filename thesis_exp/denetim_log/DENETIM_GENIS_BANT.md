# Bağımsız sayısal denetim — Geniş bant OFDM (`thesis_exp/genis_bant/REPORT.md`)

Denetim tarihi 16 Kasım 2026, dal `thesis/p4-deneyler`, denetlenen HEAD `da6577b`. Mevcut hiçbir dosya değiştirilmedi.
Betik: `thesis_exp/denetim_log/genis_bant_denetim.py`. Ham çıktı: `genis_bant_denetim.json` ve `genis_bant_denetim_out.md` (tam tablo, aşağıya da eklendi).
Bootstrap: kendi uygulamam, `np.random.default_rng(20261116)`, 2000 yeniden örnekleme, %95 yüzdelik. Sınırdaki hücreler için ek olarak 20 ayrı tohum (1000–1019).
Seçimler, ortalamalar, eşli farklar, GA'lar, L*, L = 48 kayıpları, gecikme uydurmaları, sayımlar, §4 duyarlılığı ve G4 kayıpları yalnızca `raw/curves.json` ve `raw/timing.json` üzerinden yeniden hesaplandı (`run.py`, `sens200.py` ve `common.boot` kullanılmadı). `t = 0` hızları `curves.json`'da yok, o yüzden yalnızca `results.json` ile tutarlılıkları ve t0 ≥ etkin hız koşulu sınandı.

**Sonuç: 396 kontrolün 394'ü OK.** 2 HATA, ikisi de aynı başlık sayısından ("7/24") geliyor ve bootstrap RNG'sine bağlı bir sınır durumunu gösteriyor (aşağıda ORTA-1). Hipotez hükümlerinin hiçbiri değişmiyor. Kritik bulgu yok.

## Özet: üst bölüm ve yorumdaki iddialar

| İddia (yer) | Rapor | Yeniden hesap | Durum |
| --- | --- | --- | --- |
| L = 48 anlamlı kötü hücre sayısı (REPORT.md:7, :35) | 7/24 | Benim tohumumla 9/24. results.json GA'sıyla 7/24. İki sınır hücresi var (20 MHz, 1.5 m/s, K16 ve K64; orijinal üst GA +0.0007 ve +0.0030) | HATA değil, sınırda (ORTA-1) |
| L* tam olarak 48 | 6 | 6 | OK |
| G1 hükmü | TUTMADI | TUTMADI (7, 8 ya da 9 olması fark etmiyor) | OK |
| 200 ms: L* ufuk içindeki en büyük L'de | 15/24 | 15/24 | OK |
| 200 ms: ufuk içindeki en büyük L anlamlı kötü | 4 | 4 | OK |
| K_opt = 1 iç optimumu: 20 MHz (iki hız) ve 50 MHz 1.5 m/s'de var, diğerlerinde yok | — | aynı | OK |
| G2 seçimleri (6 hücre) ve hüküm | TUTTU | aynı seçimler, TUTTU; seçilen kol hiçbir hücrede K64 değil | OK |
| G3 | 6/6 TUTTU | 6/6 | OK |
| G4 medyan / ortalama / en kötü (24 hücre) | %0.81 / %1.68 / %7.97 | %0.8108 / %1.6763 / %7.9669. g4.json'daki kayıplar curves.json'dan yeniden türetilen değerlerle birebir aynı | OK |
| G4, L* ufuk içinde | 12 hücre, %0.91, %4.95 | 12, %0.9112, %4.9460 | OK |
| "~9 kat" (yorum) | ~9 | 9.122 / 1.016 = 8.97 | OK |
| "+0.28…+0.29" / "~+0.28" | — | +0.2808, +0.2938 | OK |
| "0.23–0.47" (CD) | — | 0.2266–0.4729 | OK |
| "16 → 48" (50 MHz, K_opt = 1) | — | 16 → 48 | OK (genelleme için bkz. KÜÇÜK-3) |
| "%4.95" | — | %4.946 | OK |
| "%0.81" | — | %0.811 | OK |
| "K16-L20 183.4 ms", "+0.24/+0.28" | — | K16-L20, 183.38 ms; +0.2392 / +0.2775 | OK |
| DEGISIKLIKLER.md:80, "50–100 MHz'deki 16 hücrenin yalnızca 3'ünde" | 3/16 | 3/16 (sınır hücreleri 20 MHz'de, bu sayıyı etkilemiyor) | OK |
| Gecikme tablosu, uydurmalar, L = 48 gecikmeleri, 56 kolun gecikmesi == results.json | — | polyfit ile birebir (maks. fark < 1e-6 ms) | OK |
| t = 0 kanalı zaman ızgarasından ve hızdan bağımsız (seçim ile değerlendirme aynı senaryo mu) | — | `WB(11,[0],50e6,n=8)` ve `WB(11,[0,37.4,438.8],50e6,v=10 km/h,n=8)`: maks. fark 0 | OK |
| Merkezlenmiş alt küme (sapma 1) | K4 = {8,24,40,56} | aynı; ağırlık merkezi +B/128 (yarım bin) | OK |

## Bulgular

### KRİTİK
Yok. Yeniden hesaplanan hiçbir sayı bir hipotez hükmünü, seçilen kolu ya da raporun yönünü değiştirmiyor.

### ORTA

**ORTA-1. "7/24" başlık sayısı bootstrap RNG'sine duyarlı** (REPORT.md:7 ve :35, DEGISIKLIKLER.md:80'deki "24 hücrenin yalnızca 7'sinde").
İki hücrede GA'nın üst sınırı sıfıra çok yakın: 20 MHz 1.5 m/s K16 (orijinal +0.0007) ve K64 (orijinal +0.0030). 20 bağımsız bootstrap tohumunda K16 %25, K64 %5 oranında anlamlı çıkıyor. Benim ana tohumumla sayı 9/24. En sık çıkan değer 7, yani raporun sayısı yanlış değil, ama kesin bir sayı gibi yazılmış.
*Öneri:* "7/24 (iki hücre sınırda: üst GA +0.001 ve +0.003; bootstrap tohumuna göre 7–9)". G1 hükmü ve 50–100 MHz için 3/16 bundan etkilenmiyor.

**ORTA-2. Makale 2'nin yeni Sınırlar cümlesi doğru ama kapsamı dar** (`makale2_revizyon/sections/section_07_conclusion.tex:16`).
Cümle: "a first OFDM check kept it for centre-frequency optimization at 20 MHz, but at 50–100 MHz it often flattened or hit the largest step count".
- "kept it for centre-frequency optimization at 20 MHz" doğru. K_opt = 1, 20 MHz'de iki hızda da L = 48 anlamlı olarak kötü (L* = 8 ve 5).
- "at 50–100 MHz it often flattened or hit the largest step count" doğru. K_opt = 1 için 4 hücrenin 3'ünde: ikisinde L* = 48 (50 MHz ve 100 MHz, 10 km/h; 50.1 ms, ufkun içinde), birinde eğri düz (100 MHz 1.5 m/s, −0.005 [−0.042, +0.033]). Dördüncüde (50 MHz 1.5 m/s, L* = 16) optimum korunuyor.
- Cümlenin dışarıda bıraktığı şey: 20 MHz'de geniş bant amaçlı kollarda (K_opt ≥ 4) 6 hücrenin 4'ünde L = 48 anlamlı olarak kötü değil (K4 10 km/h, K16 iki hızda, K64 1.5 m/s sınırda). Tüm kollar sayıldığında 50–100 MHz'de 16 hücrenin 13'ünde L = 48 anlamlı olarak kötü değil. "often" kelimesi 3/4 ve 13/16 oranlarını yumuşatıyor.
*Öneri (Kural 10):* "…kept it at 20 MHz only for centre-frequency optimization; at 50–100 MHz the 48-step arm was significantly worse in only 3 of 16 (bandwidth, speed, subcarrier-set) cells." Cümle yanlış değil, karar kullanıcının.

**ORTA-3. yorum.md, G4 maddesi (yorum.md:3): "Bu seçimlerin çoğu 200 ms ufkunun dışındaki bölgeye düşüyor" tam doğru değil.**
Örnek verilen tuhaf seçimlerden K_opt = 16, 1.5 m/s'deki L = 1, 10.1 ms'dir ve ufkun içindedir. Ufkun dışında kalan, L* = 32'dir (292.8 ms). En büyük üç G4 kaybı (%7.97, %6.25, %2.95) bu hücrelerden geliyor. Yalnızca 10 km/h'deki L = 24 (219.9 ms) ufkun dışında. Ayrıca "ψ'nin salınımlı bölgesinden yararlanıp" bir mekanizma iddiası. Kural u = 0.151 (L = 1) ve u = 6.11 (L = 24) noktalarında çağrılıyor ve kalibrasyon tablosu u ≤ 33'ü kapsıyor, yani tablo dışına taşma yok. Ama salınımın gerçekten varlığını bu denetim sınamadı: ÜRETİLEMEDİ, çünkü ψ eğrisi incelenmedi.
*Öneri:* "K_opt = 16'da kural 1.5 m/s'de L = 1 seçiyor (ufuk içinde); oysa L* = 32, 292.8 ms ile ufkun dışında. En büyük kayıplar buradan geliyor." Mekanizma "hipotez" olarak etiketlenmeli.

### KÜÇÜK

1. **SU-average gecikmesi iki kez sayılıyor** (run.py:52 ve run.py:75). Zamanlama lambda'sı `v_.adam(v_.su_average(), L, k)` olduğu için a_K, SU-average süresini zaten içeriyor. Buna karşın run.py:75 (ve g4.py:37) `T0 = 0.30 ms`'yi bir kez daha ekliyor. Sonuç: bütün Adam kolları yaklaşık 0.3 ms geç değerlendiriliyor. Formül ON_KAYIT'ta böyle ön kayıtlı olduğu için bir sapma değil. Etkisi önemsiz (en küçük gecikme 2.3 ms; seçimlerin belirlendiği ölçek 5–300 ms). Raporun §0'ında bir satırla belirtilebilir.
2. **"koşu commit'i `77d0b17`" kayıt anını gösteriyor, başlangıcı değil** (REPORT.md:3; run.py:102). `commit()` koşunun sonunda çağrılıyor. Eğriler 09:24'te `b8f349d`/`5a8b86e` ile başladı, `77d0b17` ("report builder", 09:55) koşu sürerken commit'lendi. Bu aralıkta `wb.py` ve `run.py` değişmedi (diff yalnızca g4.py, make_report.py ve log), bu yüzden sayılar etkilenmiyor. *Öneri:* "koşu başlangıcı `5a8b86e`, kayıt `77d0b17`; kod aynı".
3. **yorum.md:2: "10 km/h'de L*'ın 1.5 m/s'dekinden büyük çıkması" genel bir eğilim gibi yazılmış.** 12 (B, K_opt) çiftinin 6'sında L* büyüyor, 3'ünde küçülüyor (20 MHz K1 8→5, 20 MHz K64 16→10, 50 MHz K4 48→32), 3'ünde değişmiyor. *Öneri:* "çoğu (6/12) çiftte".
4. **G4'ün τ tanımı tasarım kuralınınkinden farklı** (g4.py:37: `0.30 + a_K + b_K·L`; tasarim_kurali/rule.py:37: `L·dT + T0`). g4.py docstring'i bunu açıkça söylüyor ve bu τ kolun gerçek gecikmesine eşit, ama ON_KAYIT'ta ve raporda belirtilmemiş. Ayrıca rapordaki "yalnızca ölçülen adım maliyetiyle" ifadesi (REPORT.md:38, yorum.md:3) eksik: kurala kolun seed-12 geniş bant R0(L) eğrisi de veriliyor. Kesişimsiz τ ile kuralın seçimi ÜRETİLEMEDİ, çünkü seed-12'nin t = 0 eğrisi (R0) ham çıktılarda yok.
5. **wb.py:28–29'daki yorum "ON_KAYIT.md sapma 2" diyor**; merkezleme sapma 1'dir.
6. **Gecikmede tur-arası yayılım raporda yok** (CLAUDE.md kural 5). timing.json'da var; örneğin K4 L16 için 40.2–49.7 ms, K64 L16 için 579.7–635.4 ms. Ayrıca L > 16 gecikmeleri (L = 48 ve seçilen L = 32 dahil), L ∈ {1, 4, 16} üzerindeki üç noktalı uydurmanın dış değerlemesi. Bu, §0'a bir sınır olarak eklenebilir.
7. **sens200.py:4'teki docstring "L* (seed 11, restricted grid)" diyor**, kod (sens200.py:37) ise kısıtsız g4 L*'ını kullanıyor. Süzgeç olarak ikisi eşdeğer (kısıtsız L* ufuk içindeyse kısıtlı L* ile aynıdır), sayı değişmiyor.

## Mantık ve süreç denetimi

- **Hükümler ON_KAYIT ile birebir uyumlu.** G1 ölçütü "L = 48 − L* GA'sı sıfırın altında, her hücrede"; G2 seçilen kolun K_opt'una bakıyor (20 MHz ≤ 4, 100 MHz ≥ 16, iki hızda); G3 6/6; G4 keşifsel. make_report.py yeni bir ölçüt eklemiyor. G1'deki L* aynı test çekilişinde argmax ile seçiliyor; bu anlamlılık lehine bir seçim yanlılığı yaratır, dolayısıyla "TUTMADI" hükmü bu açıdan muhafazakârdır.
- **G2'nin sağlamlığı (ek kontrol).** 100 MHz'de K16 kolunun seed-12'de en iyi K ≤ 4 koluna karşı marjı küçük (0.047 ve 0.027). Ama seed 11'de eşli fark anlamlı: 1.5 m/s'de K16-L32 − K4-L48 = +0.109 [+0.059, +0.159], 10 km/h'de K16-L32 − K4-L32 = +0.081 [+0.023, +0.133]. Ana hüküm kırılgan değil.
- **Aleyhte bulgu yumuşatılmamış.** G1'in başarısızlığı raporun en üstünde yazıyor, Kural 10'a uygun. Tek yumuşatma riski Makale 2 cümlesindeki "often" (ORTA-2).
- **Sapmalar koşudan önce kayda geçmiş.** Git sırası: ON_KAYIT ilk sürümü `2da84ad` (07:48); sapmalar 1–3 ve merkezleme `0b8943e` (09:03); timing.json `b8f349d` (09:24:13); eğri koşusu başladı `5a8b86e` (09:24:42); g4.py `7595ff7` (09:30, eğriler bitmeden); sonuçlar `f3652a6` (10:22). Usul notu: sapma 3, timing.json commit'lenmeden 21 dakika önce kısmi zamanlama değerlerini aktarıyor. Zamanlama, merkezlenmemiş alt kümeli `843e42e` koduyla ölçüldü; alt küme boyutu aynı olduğu için bu sapma 1'de doğru gerekçelendirilmiş.
- **200 ms duyarlılığı açıkça ön kayıt dışı.** §4 başlığında "ÖN KAYIT DIŞI, sonuçlar görüldükten sonra yazıldı" yazıyor; üst bölümde "Ön kayıt dışı duyarlılıkta (§4)" yazıyor; sens200.json'da `note: "not pre-registered"` var. Uygun.
- **Kod incelemesi (sonucu değiştirecek hata bulunmadı).**
  - Gecikme ızgarası: kollar gecikmeye göre sıralanmış, 8'li gruplanmış, `times = [0] + lat`, `minrate(PH[x], j + 1)` ile doğru indeks okunuyor (run.py:92–97).
  - t = 0 kanalı ızgaradan ve hızdan bağımsız; bu yüzden fazlar değerlendirilen senaryolarla aynı senaryolarda optimize ediliyor (sınandı, fark 0).
  - Tohumlar seçim için 12, rapor için 11; `torch.manual_seed(0)` her WB'de çağrılıyor.
  - Alt küme merkezlenmiş. K_opt = 1 fc'de, ızgara fc etrafında simetrik.
  - CD için `iters=8`, `coord_descent`'in varsayılanı (baselines.py:163).
  - ψ tablosu kuralın kullandığı u aralığını (≤ 16.5) kapsıyor, dış değerleme yok.

## Tam kontrol tablosu (betik çıktısı)

Denetlenen commit `da6577b`; bootstrap tohumu 20261116 (2000, %95 yuzdelik).

| bolum | kalem | rapor | yeniden hesap | durum |
| --- | --- | --- | --- | --- |
| §1 | K1 medyan L=1,4,16 | 1.73 5.39 17.18 | +1.7290, +5.3884, +17.1784 | OK |
| §1 | K1 uydurma | +0.98 + 1.016·L | +0.9838, +1.0164 | OK |
| §1 | K1 L=48 gecikme | 50.1 | +50.0678 | OK |
| §1 | K1 uydurma == timing.json | 0.983772 1.016404 | +0.9838, +1.0164 | OK |
| §1 | K4 medyan L=1,4,16 | 3.40 12.38 40.35 | +3.3986, +12.3832, +40.3536 | OK |
| §1 | K4 uydurma | +1.73 + 2.426·L | +1.7317, +2.4257 | OK |
| §1 | K4 L=48 gecikme | 118.5 | +118.4632 | OK |
| §1 | K4 uydurma == timing.json | 1.731700 2.425725 | +1.7317, +2.4257 | OK |
| §1 | K16 medyan L=1,4,16 | 9.74 37.15 146.59 | +9.7418, +37.1498, +146.5867 | OK |
| §1 | K16 uydurma | +0.64 + 9.122·L | +0.6383, +9.1221 | OK |
| §1 | K16 L=48 gecikme | 438.8 | +438.7941 | OK |
| §1 | K16 uydurma == timing.json | 0.638306 9.122064 | +0.6383, +9.1221 | OK |
| §1 | K64 medyan L=1,4,16 | 31.46 139.96 593.33 | +31.4641, +139.9590, +593.3294 | OK |
| §1 | K64 uydurma | -7.93 + 37.550·L | -7.9326, +37.5500 | OK |
| §1 | K64 L=48 gecikme | 1794.8 | +1794.7650 | OK |
| §1 | K64 uydurma == timing.json | -7.932649 37.550020 | -7.9326, +37.5500 | OK |
| §1 | tum kol gecikmeleri == results.json (max abs fark, ms) | 0 | +0.0000 | OK |
| §1 | yuk baslangic/once/sonra | 0.03 0.03 1.00 | +0.0298, +0.0298, +1.0000 | OK |
| §1 | SU-best-of / CD (ms) | 1.63 702.97 | +1.6292, +702.9659 | OK |
| yorum | K16/K1 adim maliyeti orani (~9 kat) | 9 | +8.9748 | OK |
| §3 | 20/1.5mps secilen (seed 12) | K4-L4 | K4-L4 | OK |
| §3 | 20/1.5mps etkin hiz | 5.398 | +5.3982 | OK |
| §3 | 20/1.5mps - SU-best-of (nokta) | +0.448  | +0.4485 | OK |
| §3 | 20/1.5mps - SU-best-of GA | [+0.396, +0.501] | +0.3963, +0.5040 | OK |
| §3 | 20/1.5mps dar bant kolu | K1-L8 | K1-L8 | OK |
| §3 | 20/1.5mps - dar bant (nokta) | +0.013  | +0.0131 | OK |
| §3 | 20/1.5mps - dar bant GA | [-0.025, +0.050]  | -0.0239, +0.0496 | OK |
| §3 | 20/1.5mps CD - secilen (nokta) | -0.473  | -0.4729 | OK |
| §3 | 20/1.5mps CD - secilen GA | [-0.557, -0.386] | -0.5613, -0.3871 | OK |
| §3K | 20/1.5mps/K1 L* | 8 | 8 | OK |
| §3K | 20/1.5mps/K1 gecikme(L*) | 9.4 | +9.4117 | OK |
| §3K | 20/1.5mps/K1 >200 ms bayragi | False | False | OK |
| §3K | 20/1.5mps/K1 etkin hiz(L*) | 5.385 | +5.3851 | OK |
| §3K | 20/1.5mps/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.545 | 5.545 | OK |
| §3K | 20/1.5mps/K1 L48-L* (nokta) | -0.304  | -0.3037 | OK |
| §3K | 20/1.5mps/K1 L48-L* GA | [-0.369, -0.239] | -0.3688, -0.2383 | OK |
| §3K | 20/1.5mps/K1 L48 kaybi % | 5.64 | +5.6393 | OK |
| §3K | 20/1.5mps/K4 L* | 4 | 4 | OK |
| §3K | 20/1.5mps/K4 gecikme(L*) | 11.7 | +11.7313 | OK |
| §3K | 20/1.5mps/K4 >200 ms bayragi | False | False | OK |
| §3K | 20/1.5mps/K4 etkin hiz(L*) | 5.398 | +5.3982 | OK |
| §3K | 20/1.5mps/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.649 | 5.649 | OK |
| §3K | 20/1.5mps/K4 L48-L* (nokta) | -0.205  | -0.2054 | OK |
| §3K | 20/1.5mps/K4 L48-L* GA | [-0.275, -0.135] | -0.2744, -0.1360 | OK |
| §3K | 20/1.5mps/K4 L48 kaybi % | 3.81 | +3.8055 | OK |
| §3K | 20/1.5mps/K16 L* | 32 | 32 | OK |
| §3K | 20/1.5mps/K16 gecikme(L*) | 292.8 | +292.8410 | OK |
| §3K | 20/1.5mps/K16 >200 ms bayragi | True | True | OK |
| §3K | 20/1.5mps/K16 etkin hiz(L*) | 5.118 | +5.1181 | OK |
| §3K | 20/1.5mps/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.386 | 6.386 | OK |
| §3K | 20/1.5mps/K16 L48-L* (nokta) | -0.069  | -0.0688 | OK |
| §3K | 20/1.5mps/K16 L48-L* GA | [-0.138, +0.001] | -0.1404, -0.0006 | OK |
| §3K | 20/1.5mps/K16 L48 kaybi % | 1.34 | +1.3435 | OK |
| §3K | 20/1.5mps/K64 L* | 16 | 16 | OK |
| §3K | 20/1.5mps/K64 gecikme(L*) | 593.2 | +593.1643 | OK |
| §3K | 20/1.5mps/K64 >200 ms bayragi | True | True | OK |
| §3K | 20/1.5mps/K64 etkin hiz(L*) | 5.078 | +5.0778 | OK |
| §3K | 20/1.5mps/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.205 | 6.205 | OK |
| §3K | 20/1.5mps/K64 L48-L* (nokta) | -0.088  | -0.0883 | OK |
| §3K | 20/1.5mps/K64 L48-L* GA | [-0.179, +0.003] | -0.1865, -0.0002 | OK |
| §3K | 20/1.5mps/K64 L48 kaybi % | 1.74 | +1.7397 | OK |
| §3 | 20/10kmh secilen (seed 12) | K1-L4 | K1-L4 | OK |
| §3 | 20/10kmh etkin hiz | 5.218 | +5.2176 | OK |
| §3 | 20/10kmh - SU-best-of (nokta) | +0.272  | +0.2720 | OK |
| §3 | 20/10kmh - SU-best-of GA | [+0.217, +0.325] | +0.2179, +0.3250 | OK |
| §3 | 20/10kmh dar bant kolu | K1-L4 | K1-L4 | OK |
| §3 | 20/10kmh - dar bant (nokta) | +0.000  | +0.0000 | OK |
| §3 | 20/10kmh - dar bant GA | [+0.000, +0.000]  | +0.0000, +0.0000 | OK |
| §3 | 20/10kmh CD - secilen (nokta) | -0.365  | -0.3648 | OK |
| §3 | 20/10kmh CD - secilen GA | [-0.459, -0.271] | -0.4552, -0.2744 | OK |
| §3K | 20/10kmh/K1 L* | 5 | 5 | OK |
| §3K | 20/10kmh/K1 gecikme(L*) | 6.4 | +6.3625 | OK |
| §3K | 20/10kmh/K1 >200 ms bayragi | False | False | OK |
| §3K | 20/10kmh/K1 etkin hiz(L*) | 5.218 | +5.2180 | OK |
| §3K | 20/10kmh/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.406 | 5.406 | OK |
| §3K | 20/10kmh/K1 L48-L* (nokta) | -0.186  | -0.1859 | OK |
| §3K | 20/10kmh/K1 L48-L* GA | [-0.256, -0.116] | -0.2561, -0.1179 | OK |
| §3K | 20/10kmh/K1 L48 kaybi % | 3.56 | +3.5623 | OK |
| §3K | 20/10kmh/K4 L* | 32 | 32 | OK |
| §3K | 20/10kmh/K4 gecikme(L*) | 79.7 | +79.6516 | OK |
| §3K | 20/10kmh/K4 >200 ms bayragi | False | False | OK |
| §3K | 20/10kmh/K4 etkin hiz(L*) | 5.162 | +5.1621 | OK |
| §3K | 20/10kmh/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.369 | 6.369 | OK |
| §3K | 20/10kmh/K4 L48-L* (nokta) | -0.025  | -0.0250 | OK |
| §3K | 20/10kmh/K4 L48-L* GA | [-0.086, +0.034] | -0.0898, +0.0374 | OK |
| §3K | 20/10kmh/K4 L48 kaybi % | 0.48 | +0.4835 | OK |
| §3K | 20/10kmh/K16 L* | 32 | 32 | OK |
| §3K | 20/10kmh/K16 gecikme(L*) | 292.8 | +292.8410 | OK |
| §3K | 20/10kmh/K16 >200 ms bayragi | True | True | OK |
| §3K | 20/10kmh/K16 etkin hiz(L*) | 5.075 | +5.0751 | OK |
| §3K | 20/10kmh/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.386 | 6.386 | OK |
| §3K | 20/10kmh/K16 L48-L* (nokta) | -0.012  | -0.0117 | OK |
| §3K | 20/10kmh/K16 L48-L* GA | [-0.084, +0.060] | -0.0854, +0.0590 | OK |
| §3K | 20/10kmh/K16 L48 kaybi % | 0.23 | +0.2303 | OK |
| §3K | 20/10kmh/K64 L* | 10 | 10 | OK |
| §3K | 20/10kmh/K64 gecikme(L*) | 367.9 | +367.8642 | OK |
| §3K | 20/10kmh/K64 >200 ms bayragi | True | True | OK |
| §3K | 20/10kmh/K64 etkin hiz(L*) | 4.975 | +4.9750 | OK |
| §3K | 20/10kmh/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.020 | 6.020 | OK |
| §3K | 20/10kmh/K64 L48-L* (nokta) | -0.194  | -0.1940 | OK |
| §3K | 20/10kmh/K64 L48-L* GA | [-0.308, -0.075] | -0.3064, -0.0751 | OK |
| §3K | 20/10kmh/K64 L48 kaybi % | 3.90 | +3.9004 | OK |
| §3 | 50/1.5mps secilen (seed 12) | K4-L4 | K4-L4 | OK |
| §3 | 50/1.5mps etkin hiz | 5.136 | +5.1362 | OK |
| §3 | 50/1.5mps - SU-best-of (nokta) | +0.341  | +0.3409 | OK |
| §3 | 50/1.5mps - SU-best-of GA | [+0.298, +0.385] | +0.2964, +0.3858 | OK |
| §3 | 50/1.5mps dar bant kolu | K1-L12 | K1-L12 | OK |
| §3 | 50/1.5mps - dar bant (nokta) | +0.078  | +0.0776 | OK |
| §3 | 50/1.5mps - dar bant GA | [+0.039, +0.115]  | +0.0400, +0.1169 | OK |
| §3 | 50/1.5mps CD - secilen (nokta) | -0.227  | -0.2266 | OK |
| §3 | 50/1.5mps CD - secilen GA | [-0.301, -0.154] | -0.3007, -0.1538 | OK |
| §3K | 50/1.5mps/K1 L* | 16 | 16 | OK |
| §3K | 50/1.5mps/K1 gecikme(L*) | 17.5 | +17.5429 | OK |
| §3K | 50/1.5mps/K1 >200 ms bayragi | False | False | OK |
| §3K | 50/1.5mps/K1 etkin hiz(L*) | 5.061 | +5.0612 | OK |
| §3K | 50/1.5mps/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.250 | 5.250 | OK |
| §3K | 50/1.5mps/K1 L48-L* (nokta) | -0.065  | -0.0652 | OK |
| §3K | 50/1.5mps/K1 L48-L* GA | [-0.114, -0.020] | -0.1118, -0.0200 | OK |
| §3K | 50/1.5mps/K1 L48 kaybi % | 1.29 | +1.2878 | OK |
| §3K | 50/1.5mps/K4 L* | 48 | 48 | OK |
| §3K | 50/1.5mps/K4 gecikme(L*) | 118.5 | +118.4632 | OK |
| §3K | 50/1.5mps/K4 >200 ms bayragi | False | False | OK |
| §3K | 50/1.5mps/K4 etkin hiz(L*) | 5.155 | +5.1548 | OK |
| §3K | 50/1.5mps/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.878 | 5.878 | OK |
| §3K | 50/1.5mps/K4 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 50/1.5mps/K4 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 50/1.5mps/K4 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 50/1.5mps/K16 L* | 32 | 32 | OK |
| §3K | 50/1.5mps/K16 gecikme(L*) | 292.8 | +292.8410 | OK |
| §3K | 50/1.5mps/K16 >200 ms bayragi | True | True | OK |
| §3K | 50/1.5mps/K16 etkin hiz(L*) | 5.181 | +5.1812 | OK |
| §3K | 50/1.5mps/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.016 | 6.016 | OK |
| §3K | 50/1.5mps/K16 L48-L* (nokta) | -0.039  | -0.0395 | OK |
| §3K | 50/1.5mps/K16 L48-L* GA | [-0.100, +0.023] | -0.1050, +0.0171 | OK |
| §3K | 50/1.5mps/K16 L48 kaybi % | 0.76 | +0.7615 | OK |
| §3K | 50/1.5mps/K64 L* | 16 | 16 | OK |
| §3K | 50/1.5mps/K64 gecikme(L*) | 593.2 | +593.1643 | OK |
| §3K | 50/1.5mps/K64 >200 ms bayragi | True | True | OK |
| §3K | 50/1.5mps/K64 etkin hiz(L*) | 5.097 | +5.0969 | OK |
| §3K | 50/1.5mps/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.867 | 5.867 | OK |
| §3K | 50/1.5mps/K64 L48-L* (nokta) | -0.034  | -0.0340 | OK |
| §3K | 50/1.5mps/K64 L48-L* GA | [-0.114, +0.042] | -0.1158, +0.0478 | OK |
| §3K | 50/1.5mps/K64 L48 kaybi % | 0.67 | +0.6678 | OK |
| §3 | 50/10kmh secilen (seed 12) | K4-L32 | K4-L32 | OK |
| §3 | 50/10kmh etkin hiz | 5.119 | +5.1190 | OK |
| §3 | 50/10kmh - SU-best-of (nokta) | +0.326  | +0.3263 | OK |
| §3 | 50/10kmh - SU-best-of GA | [+0.256, +0.395] | +0.2608, +0.3946 | OK |
| §3 | 50/10kmh dar bant kolu | K1-L24 | K1-L24 | OK |
| §3 | 50/10kmh - dar bant (nokta) | +0.176  | +0.1761 | OK |
| §3 | 50/10kmh - dar bant GA | [+0.116, +0.236]  | +0.1126, +0.2370 | OK |
| §3 | 50/10kmh CD - secilen (nokta) | -0.300  | -0.3005 | OK |
| §3 | 50/10kmh CD - secilen GA | [-0.382, -0.219] | -0.3837, -0.2205 | OK |
| §3K | 50/10kmh/K1 L* | 48 | 48 | OK |
| §3K | 50/10kmh/K1 gecikme(L*) | 50.1 | +50.0678 | OK |
| §3K | 50/10kmh/K1 >200 ms bayragi | False | False | OK |
| §3K | 50/10kmh/K1 etkin hiz(L*) | 4.976 | +4.9765 | OK |
| §3K | 50/10kmh/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.375 | 5.375 | OK |
| §3K | 50/10kmh/K1 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 50/10kmh/K1 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 50/10kmh/K1 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 50/10kmh/K4 L* | 32 | 32 | OK |
| §3K | 50/10kmh/K4 gecikme(L*) | 79.7 | +79.6516 | OK |
| §3K | 50/10kmh/K4 >200 ms bayragi | False | False | OK |
| §3K | 50/10kmh/K4 etkin hiz(L*) | 5.119 | +5.1190 | OK |
| §3K | 50/10kmh/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.829 | 5.829 | OK |
| §3K | 50/10kmh/K4 L48-L* (nokta) | -0.000  | -0.0000 | OK |
| §3K | 50/10kmh/K4 L48-L* GA | [-0.045, +0.046] | -0.0463, +0.0464 | OK |
| §3K | 50/10kmh/K4 L48 kaybi % | 0.00 | +0.0002 | OK |
| §3K | 50/10kmh/K16 L* | 48 | 48 | OK |
| §3K | 50/10kmh/K16 gecikme(L*) | 438.8 | +438.7941 | OK |
| §3K | 50/10kmh/K16 >200 ms bayragi | True | True | OK |
| §3K | 50/10kmh/K16 etkin hiz(L*) | 5.128 | +5.1280 | OK |
| §3K | 50/10kmh/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 6.073 | 6.073 | OK |
| §3K | 50/10kmh/K16 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 50/10kmh/K16 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 50/10kmh/K16 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 50/10kmh/K64 L* | 16 | 16 | OK |
| §3K | 50/10kmh/K64 gecikme(L*) | 593.2 | +593.1643 | OK |
| §3K | 50/10kmh/K64 >200 ms bayragi | True | True | OK |
| §3K | 50/10kmh/K64 etkin hiz(L*) | 5.035 | +5.0350 | OK |
| §3K | 50/10kmh/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.867 | 5.867 | OK |
| §3K | 50/10kmh/K64 L48-L* (nokta) | -0.189  | -0.1887 | OK |
| §3K | 50/10kmh/K64 L48-L* GA | [-0.286, -0.091] | -0.2837, -0.0844 | OK |
| §3K | 50/10kmh/K64 L48 kaybi % | 3.75 | +3.7479 | OK |
| §3 | 100/1.5mps secilen (seed 12) | K16-L32 | K16-L32 | OK |
| §3 | 100/1.5mps etkin hiz | 5.228 | +5.2283 | OK |
| §3 | 100/1.5mps - SU-best-of (nokta) | +0.496  | +0.4960 | OK |
| §3 | 100/1.5mps - SU-best-of GA | [+0.420, +0.577] | +0.4254, +0.5714 | OK |
| §3 | 100/1.5mps dar bant kolu | K1-L48 | K1-L48 | OK |
| §3 | 100/1.5mps - dar bant (nokta) | +0.281  | +0.2808 | OK |
| §3 | 100/1.5mps - dar bant GA | [+0.220, +0.342]  | +0.2204, +0.3395 | OK |
| §3 | 100/1.5mps CD - secilen (nokta) | -0.331  | -0.3306 | OK |
| §3 | 100/1.5mps CD - secilen GA | [-0.390, -0.273] | -0.3889, -0.2731 | OK |
| §3K | 100/1.5mps/K1 L* | 16 | 16 | OK |
| §3K | 100/1.5mps/K1 gecikme(L*) | 17.5 | +17.5429 | OK |
| §3K | 100/1.5mps/K1 >200 ms bayragi | False | False | OK |
| §3K | 100/1.5mps/K1 etkin hiz(L*) | 4.952 | +4.9521 | OK |
| §3K | 100/1.5mps/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.035 | 5.035 | OK |
| §3K | 100/1.5mps/K1 L48-L* (nokta) | -0.005  | -0.0045 | OK |
| §3K | 100/1.5mps/K1 L48-L* GA | [-0.042, +0.033] | -0.0406, +0.0335 | OK |
| §3K | 100/1.5mps/K1 L48 kaybi % | 0.09 | +0.0919 | OK |
| §3K | 100/1.5mps/K4 L* | 32 | 32 | OK |
| §3K | 100/1.5mps/K4 gecikme(L*) | 79.7 | +79.6516 | OK |
| §3K | 100/1.5mps/K4 >200 ms bayragi | False | False | OK |
| §3K | 100/1.5mps/K4 etkin hiz(L*) | 5.130 | +5.1303 | OK |
| §3K | 100/1.5mps/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.494 | 5.494 | OK |
| §3K | 100/1.5mps/K4 L48-L* (nokta) | -0.011  | -0.0114 | OK |
| §3K | 100/1.5mps/K4 L48-L* GA | [-0.045, +0.022] | -0.0463, +0.0231 | OK |
| §3K | 100/1.5mps/K4 L48 kaybi % | 0.22 | +0.2216 | OK |
| §3K | 100/1.5mps/K16 L* | 32 | 32 | OK |
| §3K | 100/1.5mps/K16 gecikme(L*) | 292.8 | +292.8410 | OK |
| §3K | 100/1.5mps/K16 >200 ms bayragi | True | True | OK |
| §3K | 100/1.5mps/K16 etkin hiz(L*) | 5.228 | +5.2283 | OK |
| §3K | 100/1.5mps/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.786 | 5.786 | OK |
| §3K | 100/1.5mps/K16 L48-L* (nokta) | -0.040  | -0.0402 | OK |
| §3K | 100/1.5mps/K16 L48-L* GA | [-0.094, +0.013] | -0.0966, +0.0081 | OK |
| §3K | 100/1.5mps/K16 L48 kaybi % | 0.77 | +0.7683 | OK |
| §3K | 100/1.5mps/K64 L* | 16 | 16 | OK |
| §3K | 100/1.5mps/K64 gecikme(L*) | 593.2 | +593.1643 | OK |
| §3K | 100/1.5mps/K64 >200 ms bayragi | True | True | OK |
| §3K | 100/1.5mps/K64 etkin hiz(L*) | 5.154 | +5.1539 | OK |
| §3K | 100/1.5mps/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.671 | 5.671 | OK |
| §3K | 100/1.5mps/K64 L48-L* (nokta) | -0.023  | -0.0233 | OK |
| §3K | 100/1.5mps/K64 L48-L* GA | [-0.104, +0.052] | -0.0982, +0.0522 | OK |
| §3K | 100/1.5mps/K64 L48 kaybi % | 0.45 | +0.4520 | OK |
| §3 | 100/10kmh secilen (seed 12) | K16-L32 | K16-L32 | OK |
| §3 | 100/10kmh etkin hiz | 5.188 | +5.1883 | OK |
| §3 | 100/10kmh - SU-best-of (nokta) | +0.457  | +0.4567 | OK |
| §3 | 100/10kmh - SU-best-of GA | [+0.378, +0.541] | +0.3782, +0.5404 | OK |
| §3 | 100/10kmh dar bant kolu | K1-L24 | K1-L24 | OK |
| §3 | 100/10kmh - dar bant (nokta) | +0.294  | +0.2938 | OK |
| §3 | 100/10kmh - dar bant GA | [+0.229, +0.362]  | +0.2235, +0.3629 | OK |
| §3 | 100/10kmh CD - secilen (nokta) | -0.385  | -0.3851 | OK |
| §3 | 100/10kmh CD - secilen GA | [-0.444, -0.323] | -0.4512, -0.3188 | OK |
| §3K | 100/10kmh/K1 L* | 48 | 48 | OK |
| §3K | 100/10kmh/K1 gecikme(L*) | 50.1 | +50.0678 | OK |
| §3K | 100/10kmh/K1 >200 ms bayragi | False | False | OK |
| §3K | 100/10kmh/K1 etkin hiz(L*) | 4.934 | +4.9338 | OK |
| §3K | 100/10kmh/K1 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.139 | 5.139 | OK |
| §3K | 100/10kmh/K1 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 100/10kmh/K1 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 100/10kmh/K1 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 100/10kmh/K4 L* | 48 | 48 | OK |
| §3K | 100/10kmh/K4 gecikme(L*) | 118.5 | +118.4632 | OK |
| §3K | 100/10kmh/K4 >200 ms bayragi | False | False | OK |
| §3K | 100/10kmh/K4 etkin hiz(L*) | 5.119 | +5.1192 | OK |
| §3K | 100/10kmh/K4 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.530 | 5.530 | OK |
| §3K | 100/10kmh/K4 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 100/10kmh/K4 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 100/10kmh/K4 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 100/10kmh/K16 L* | 48 | 48 | OK |
| §3K | 100/10kmh/K16 gecikme(L*) | 438.8 | +438.7941 | OK |
| §3K | 100/10kmh/K16 >200 ms bayragi | True | True | OK |
| §3K | 100/10kmh/K16 etkin hiz(L*) | 5.192 | +5.1922 | OK |
| §3K | 100/10kmh/K16 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.826 | 5.826 | OK |
| §3K | 100/10kmh/K16 L48-L* (nokta) | +0.000  | +0.0000 | OK |
| §3K | 100/10kmh/K16 L48-L* GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §3K | 100/10kmh/K16 L48 kaybi % | 0.00 | +0.0000 | OK |
| §3K | 100/10kmh/K64 L* | 16 | 16 | OK |
| §3K | 100/10kmh/K64 gecikme(L*) | 593.2 | +593.1643 | OK |
| §3K | 100/10kmh/K64 >200 ms bayragi | True | True | OK |
| §3K | 100/10kmh/K64 etkin hiz(L*) | 5.110 | +5.1103 | OK |
| §3K | 100/10kmh/K64 t=0 hizi (yalniz results.json ile tutarlilik; t0>=etkin) | 5.671 | 5.671 | OK |
| §3K | 100/10kmh/K64 L48-L* (nokta) | -0.203  | -0.2034 | OK |
| §3K | 100/10kmh/K64 L48-L* GA | [-0.303, -0.110] | -0.3054, -0.1037 | OK |
| §3K | 100/10kmh/K64 L48 kaybi % | 3.98 | +3.9803 | OK |
| ust | G1: L=48 anlamli kotu hucre sayisi (7/24) | 7 24 | +9.0000, +24.0000 | HATA |
| ust | G1: kendi GA ile results.json GA'si ayni hukum | 24 | +22.0000 | HATA |
| ust | L* tam 48 olan hucre (6) | 6 | +6.0000 | OK |
| ust | G1 hukmu | TUTMADI | TUTMADI | OK |
| DEGISIKLIKLER | 50-100 MHz'de anlamli hucre (3/16) | 3 16 | +3.0000, +16.0000 | OK |
| ust | K1: 20 MHz iki hiz + 50 MHz 1.5 m/s korunuyor (anlamli), digerleri degil | 20/1.5mps:True 20/10kmh:True 50/1.5mps:True 50/10kmh:False 100/1.5mps:False 100/10kmh:False | 20/1.5mps:True 20/10kmh:True 50/1.5mps:True 50/10kmh:False 100/1.5mps:False 100/10kmh:False | OK |
| §2 | G2 hukmu (20 MHz K<=4 ve 100 MHz K>=16) | TUTTU | TUTTU | OK |
| §2 | G2: secilen kol K64 degil (sapma 2) | True | True | OK |
| §2 | G3: CD anlamli geride (6/6) | 6 6 | +6.0000, +6.0000 | OK |
| yorum | G3 araligi 0.23-0.47 | 0.23 0.47 | +0.2266, +0.4729 | OK |
| ust/yorum | 100 MHz secilen - dar bant (+0.28...+0.29; ~+0.28) | 0.28 0.29 | +0.2808, +0.2938 | OK |
| §4 | 20/1.5mps secilen <=200 | K4-L4 | K4-L4 | OK |
| §4 | 20/1.5mps gecikme | 11.7 | +11.7313 | OK |
| §4 | 20/1.5mps etkin hiz | 5.398 | +5.3982 | OK |
| §4 | 20/1.5mps dar bant kolu | K1-L8 | K1-L8 | OK |
| §4 | 20/1.5mps - dar bant (nokta) | +0.013  | +0.0131 | OK |
| §4 | 20/1.5mps - dar bant GA | [-0.023, +0.049] | -0.0247, +0.0498 | OK |
| §4 | 20/10kmh secilen <=200 | K1-L4 | K1-L4 | OK |
| §4 | 20/10kmh gecikme | 5.3 | +5.3461 | OK |
| §4 | 20/10kmh etkin hiz | 5.218 | +5.2176 | OK |
| §4 | 20/10kmh dar bant kolu | K1-L4 | K1-L4 | OK |
| §4 | 20/10kmh - dar bant (nokta) | +0.000  | +0.0000 | OK |
| §4 | 20/10kmh - dar bant GA | [+0.000, +0.000] | +0.0000, +0.0000 | OK |
| §4 | 50/1.5mps secilen <=200 | K4-L4 | K4-L4 | OK |
| §4 | 50/1.5mps gecikme | 11.7 | +11.7313 | OK |
| §4 | 50/1.5mps etkin hiz | 5.136 | +5.1362 | OK |
| §4 | 50/1.5mps dar bant kolu | K1-L12 | K1-L12 | OK |
| §4 | 50/1.5mps - dar bant (nokta) | +0.078  | +0.0776 | OK |
| §4 | 50/1.5mps - dar bant GA | [+0.040, +0.116] | +0.0391, +0.1150 | OK |
| §4 | 50/10kmh secilen <=200 | K4-L32 | K4-L32 | OK |
| §4 | 50/10kmh gecikme | 79.7 | +79.6516 | OK |
| §4 | 50/10kmh etkin hiz | 5.119 | +5.1190 | OK |
| §4 | 50/10kmh dar bant kolu | K1-L24 | K1-L24 | OK |
| §4 | 50/10kmh - dar bant (nokta) | +0.176  | +0.1761 | OK |
| §4 | 50/10kmh - dar bant GA | [+0.114, +0.240] | +0.1120, +0.2401 | OK |
| §4 | 100/1.5mps secilen <=200 | K16-L20 | K16-L20 | OK |
| §4 | 100/1.5mps gecikme | 183.4 | +183.3763 | OK |
| §4 | 100/1.5mps etkin hiz | 5.187 | +5.1867 | OK |
| §4 | 100/1.5mps dar bant kolu | K1-L48 | K1-L48 | OK |
| §4 | 100/1.5mps - dar bant (nokta) | +0.239  | +0.2392 | OK |
| §4 | 100/1.5mps - dar bant GA | [+0.188, +0.294] | +0.1835, +0.2935 | OK |
| yorum | 100/1.5mps K16-L20 183.4 ms ve +0.24/+0.28 | 183.4 0.24 | +183.3763, +0.2392 | OK |
| §4 | 100/10kmh secilen <=200 | K16-L20 | K16-L20 | OK |
| §4 | 100/10kmh gecikme | 183.4 | +183.3763 | OK |
| §4 | 100/10kmh etkin hiz | 5.172 | +5.1720 | OK |
| §4 | 100/10kmh dar bant kolu | K1-L24 | K1-L24 | OK |
| §4 | 100/10kmh - dar bant (nokta) | +0.277  | +0.2775 | OK |
| §4 | 100/10kmh - dar bant GA | [+0.219, +0.341] | +0.2180, +0.3387 | OK |
| yorum | 100/10kmh K16-L20 183.4 ms ve +0.24/+0.28 | 183.4 0.28 | +183.3763, +0.2775 | OK |
| ust | sens200: L* ufuk icindeki en buyuk L'de (15/24) | 15 24 | +15.0000, +24.0000 | OK |
| ust | sens200: ufuk icindeki en buyuk L anlamli kotu (4) | 4 | +4.0000 | OK |
| §5 | 20MHz_1.5mps_K1 adim / kural L | 1.016 8 | +1.0164, +8.0000 | OK |
| §5 | 20MHz_1.5mps_K1 L* (curves) | 8 | 8 | OK |
| §5 | 20MHz_1.5mps_K1 kayip % (curves'ten) | 0.00 | +0.0000 | OK |
| §5 | 20MHz_1.5mps_K4 adim / kural L | 2.426 4 | +2.4257, +4.0000 | OK |
| §5 | 20MHz_1.5mps_K4 L* (curves) | 4 | 4 | OK |
| §5 | 20MHz_1.5mps_K4 kayip % (curves'ten) | 0.00 | +0.0000 | OK |
| §5 | 20MHz_1.5mps_K16 adim / kural L | 9.122 1 | +9.1221, +1.0000 | OK |
| §5 | 20MHz_1.5mps_K16 L* (curves) | 32 | 32 | OK |
| §5 | 20MHz_1.5mps_K16 kayip % (curves'ten) | 2.95 | +2.9544 | OK |
| §5 | 20MHz_1.5mps_K64 adim / kural L | 37.550 24 | +37.5500, +24.0000 | OK |
| §5 | 20MHz_1.5mps_K64 L* (curves) | 16 | 16 | OK |
| §5 | 20MHz_1.5mps_K64 kayip % (curves'ten) | 1.72 | +1.7187 | OK |
| §5 | 20MHz_10kmh_K1 adim / kural L | 1.016 3 | +1.0164, +3.0000 | OK |
| §5 | 20MHz_10kmh_K1 L* (curves) | 5 | 5 | OK |
| §5 | 20MHz_10kmh_K1 kayip % (curves'ten) | 0.60 | +0.6023 | OK |
| §5 | 20MHz_10kmh_K4 adim / kural L | 2.426 2 | +2.4257, +2.0000 | OK |
| §5 | 20MHz_10kmh_K4 L* (curves) | 32 | 32 | OK |
| §5 | 20MHz_10kmh_K4 kayip % (curves'ten) | 0.02 | +0.0182 | OK |
| §5 | 20MHz_10kmh_K16 adim / kural L | 9.122 24 | +9.1221, +24.0000 | OK |
| §5 | 20MHz_10kmh_K16 L* (curves) | 32 | 32 | OK |
| §5 | 20MHz_10kmh_K16 kayip % (curves'ten) | 0.54 | +0.5406 | OK |
| §5 | 20MHz_10kmh_K64 adim / kural L | 37.550 16 | +37.5500, +16.0000 | OK |
| §5 | 20MHz_10kmh_K64 L* (curves) | 10 | 10 | OK |
| §5 | 20MHz_10kmh_K64 kayip % (curves'ten) | 0.23 | +0.2313 | OK |
| §5 | 50MHz_1.5mps_K1 adim / kural L | 1.016 8 | +1.0164, +8.0000 | OK |
| §5 | 50MHz_1.5mps_K1 L* (curves) | 16 | 16 | OK |
| §5 | 50MHz_1.5mps_K1 kayip % (curves'ten) | 0.52 | +0.5205 | OK |
| §5 | 50MHz_1.5mps_K4 adim / kural L | 2.426 3 | +2.4257, +3.0000 | OK |
| §5 | 50MHz_1.5mps_K4 L* (curves) | 48 | 48 | OK |
| §5 | 50MHz_1.5mps_K4 kayip % (curves'ten) | 0.78 | +0.7766 | OK |
| §5 | 50MHz_1.5mps_K16 adim / kural L | 9.122 1 | +9.1221, +1.0000 | OK |
| §5 | 50MHz_1.5mps_K16 L* (curves) | 32 | 32 | OK |
| §5 | 50MHz_1.5mps_K16 kayip % (curves'ten) | 6.25 | +6.2478 | OK |
| §5 | 50MHz_1.5mps_K64 adim / kural L | 37.550 24 | +37.5500, +24.0000 | OK |
| §5 | 50MHz_1.5mps_K64 L* (curves) | 16 | 16 | OK |
| §5 | 50MHz_1.5mps_K64 kayip % (curves'ten) | 0.81 | +0.8142 | OK |
| §5 | 50MHz_10kmh_K1 adim / kural L | 1.016 3 | +1.0164, +3.0000 | OK |
| §5 | 50MHz_10kmh_K1 L* (curves) | 48 | 48 | OK |
| §5 | 50MHz_10kmh_K1 kayip % (curves'ten) | 1.51 | +1.5146 | OK |
| §5 | 50MHz_10kmh_K4 adim / kural L | 2.426 2 | +2.4257, +2.0000 | OK |
| §5 | 50MHz_10kmh_K4 L* (curves) | 32 | 32 | OK |
| §5 | 50MHz_10kmh_K4 kayip % (curves'ten) | 3.18 | +3.1808 | OK |
| §5 | 50MHz_10kmh_K16 adim / kural L | 9.122 24 | +9.1221, +24.0000 | OK |
| §5 | 50MHz_10kmh_K16 L* (curves) | 48 | 48 | OK |
| §5 | 50MHz_10kmh_K16 kayip % (curves'ten) | 0.81 | +0.8073 | OK |
| §5 | 50MHz_10kmh_K64 adim / kural L | 37.550 16 | +37.5500, +16.0000 | OK |
| §5 | 50MHz_10kmh_K64 L* (curves) | 16 | 16 | OK |
| §5 | 50MHz_10kmh_K64 kayip % (curves'ten) | 0.00 | +0.0000 | OK |
| §5 | 100MHz_1.5mps_K1 adim / kural L | 1.016 8 | +1.0164, +8.0000 | OK |
| §5 | 100MHz_1.5mps_K1 L* (curves) | 16 | 16 | OK |
| §5 | 100MHz_1.5mps_K1 kayip % (curves'ten) | 1.05 | +1.0457 | OK |
| §5 | 100MHz_1.5mps_K4 adim / kural L | 2.426 4 | +2.4257, +4.0000 | OK |
| §5 | 100MHz_1.5mps_K4 L* (curves) | 32 | 32 | OK |
| §5 | 100MHz_1.5mps_K4 kayip % (curves'ten) | 2.11 | +2.1134 | OK |
| §5 | 100MHz_1.5mps_K16 adim / kural L | 9.122 1 | +9.1221, +1.0000 | OK |
| §5 | 100MHz_1.5mps_K16 L* (curves) | 32 | 32 | OK |
| §5 | 100MHz_1.5mps_K16 kayip % (curves'ten) | 7.97 | +7.9669 | OK |
| §5 | 100MHz_1.5mps_K64 adim / kural L | 37.550 24 | +37.5500, +24.0000 | OK |
| §5 | 100MHz_1.5mps_K64 L* (curves) | 16 | 16 | OK |
| §5 | 100MHz_1.5mps_K64 kayip % (curves'ten) | 0.23 | +0.2300 | OK |
| §5 | 100MHz_10kmh_K1 adim / kural L | 1.016 3 | +1.0164, +3.0000 | OK |
| §5 | 100MHz_10kmh_K1 L* (curves) | 48 | 48 | OK |
| §5 | 100MHz_10kmh_K1 kayip % (curves'ten) | 3.00 | +3.0004 | OK |
| §5 | 100MHz_10kmh_K4 adim / kural L | 2.426 2 | +2.4257, +2.0000 | OK |
| §5 | 100MHz_10kmh_K4 L* (curves) | 48 | 48 | OK |
| §5 | 100MHz_10kmh_K4 kayip % (curves'ten) | 4.95 | +4.9460 | OK |
| §5 | 100MHz_10kmh_K16 adim / kural L | 9.122 24 | +9.1221, +24.0000 | OK |
| §5 | 100MHz_10kmh_K16 L* (curves) | 48 | 48 | OK |
| §5 | 100MHz_10kmh_K16 kayip % (curves'ten) | 1.00 | +1.0021 | OK |
| §5 | 100MHz_10kmh_K64 adim / kural L | 37.550 16 | +37.5500, +16.0000 | OK |
| §5 | 100MHz_10kmh_K64 L* (curves) | 16 | 16 | OK |
| §5 | 100MHz_10kmh_K64 kayip % (curves'ten) | 0.00 | +0.0000 | OK |
| §2 | G4 medyan/ortalama/en kotu % | 0.81 1.68 7.97 | +0.8108, +1.6763, +7.9669 | OK |
| §2 | G4 g4.json ile curves yeniden turetimi ayni (max abs fark, %) | 0 | +0.0000 | OK |
| §4 | G4 L* ufuk icinde: hucre / medyan / en kotu (12, 0.91, 4.95) | 12 0.91 4.95 | +12.0000, +0.9112, +4.9460 | OK |
| yorum | 50 MHz K1: L* 16 -> 48 | 16 48 | +16.0000, +48.0000 | OK |
| kod | t=0 kanali zaman izgarasi ve hizdan bagimsiz (max abs fark) | 0 | +0.0000 | OK |
| kod | alt kume agirlik merkezi / B (K4, K16, K64) | 0.0078 0.0078 0.0 | +0.0078, +0.0078, +0.0000 | OK |
| kod | K4 alt kumesi {8,24,40,56} | [8, 24, 40, 56] | [8, 24, 40, 56] | OK |
