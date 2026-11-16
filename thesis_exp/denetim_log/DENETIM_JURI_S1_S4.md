# Bağımsız sayısal denetim — Jüri soruları 3, 1, 4, 2 (16 Kasım 2026)

Hedefler: `thesis_exp/juri/REPORT_S3_S1.md`, `REPORT_S4_S2.md` (sonlarındaki `yorum_s3_s1.md` ve `yorum_s4_s2.md` dahil). Ön kayıtlar: `ON_KAYIT_S3_S1.md` (Sapma 1 dahil) ve `ON_KAYIT_S4_S2.md`. Dal `thesis/p4-deneyler`, HEAD `3bd3733`. Denetim betiği `thesis_exp/denetim_log/juri_denetim.py`. Commit yapılmadı.

Yöntem: yalnızca ham JSON'lardan yeniden hesap yapıldı. Kanal üretilmedi, torch kullanılmadı; makinede eğitim koşuyordu. Tek süreç, `nice 19`, yaklaşık 10 s sürdü. Bootstrap iki biçimde koşuldu:
- Bağımsız: `default_rng(20261116)`, 2000 eşli yeniden örnekleme, yüzdelik %95.
- S4/S2 için ek olarak `common.boot` akışının birebir kopyası (tohum 0, aynı çağrı sırası).

Kendall τ ayrıca, kendi τ-a uygulamamla hesaplandı.

**Sonuç: 392 OK, 1 HATA, 1 ÜRETİLEMEDİ.** Ayrıca 29 bilgi satırı var. HATA, yorumdaki bir sayının hıza yanlış genellenmesi. Raporlardaki bütün tablo değerleri, seçimler ve dört hipotez kararı ham veriden yeniden üretildi. S4/S2 GA'ları `summary.json` ile birebir (1e-9) eşleşiyor. Bağımsız bootstrap'te en büyük sapma 0.013; birlikte eskime koşulunda dağılım geniş ve bu fark Monte Carlo gürültüsü düzeyinde.

## ⚠ En üstte (Kural 10)

1. **ORTA. CD-7 ve CD-8'in gecikmesi olduğundan küçük ölçülmüş.** Zamanlanan tek senaryoda (seed 11, indeks 0) CD 5. taramada yakınsıyor; 6. tarama erken durmayı tetikliyor. Bu yüzden ölçülen değerler s = 6, 7 ve 8 için aynı:
   - numba artımlı: 2.54 / 2.54 / 2.54 ms;
   - numba doğrudan: 7.59 / 7.60 / 7.60 ms;
   - torch: 485.6 / 460.7 / 485.1 ms.

   Oysa 400 senaryonun çoğunda 7. ve 8. tarama fazları hâlâ değiştiriyor. t0'da CD-7 ≠ CD-8 olan senaryo sayısı seed 11'de 288/400, seed 12'de 290/400. CD-6 ≠ CD-8 olanlar sırasıyla 325 ve 332.

   Yani CD-8, gerçekte yaptığı işin yaklaşık 6/8'i kadar bir gecikmeyle değerlendiriliyor. Bu da CD lehine bir yanlılık.

   Manşet bulgu buna dayanıyor: "derlenmiş artımlı CD-8, 2.54 ms, Adam-6'yı +0.717 geçiyor". Etkinin sınırı ham veriden kestirilebiliyor. CD-8'in 3.23 ms'deki (r = 150) etkin hızı:
   - 1.5 m/s: 6.839 (2.54 ms'de 6.868);
   - 10 km/h: 6.689 (2.54 ms'de 6.763).

   Fark +0.69 ile +0.78 civarında kalıyor, yani **yön değişmiyor**. r* ∈ (10, 15] yalnızca CD-1'e dayandığı için etkilenmiyor. Etkilenen yerler şunlar:
   - S1 tablosunda CD-8'in seçildiği satırlar (1.5 m/s'de r ≥ 100, 10 km/h'de r ≥ 200);
   - artımlı ve doğrudan numba satırları;
   - s1b'deki CD-8 satırları (yanlılık CD lehine; s1b'nin "Adam önde" sonucunu güçlendirir yönde);
   - S3-E'de CD-8'in ölçülmüş/FLOP oranı (0.33; FLOP 8 taramayı sayıyor, ölçüm 6 taramayı).
2. **ORTA. S4-H1 "TUTTU" kararı Kararlar bölümünde nitelenmemiş.** Birlikte eskimede L* = 1 ızgaranın alt ucunda, yani sansürlü. 1.5 m/s'de optimizasyonsuz SU-average (4.472, 0.23 ms), Adam-1'den (4.026) daha iyi. Gerçek optimum Adam ailesinin dışında.

   "L = 48 < L*" bu durumda neredeyse tanım gereği doğru; iç optimum hakkında hiçbir şey söylemiyor. Nitelendirme yalnızca "Yorum (bulgulardan ayrı)" bölümünde, `yorum_s4_s2.md:3`'te geçiyor. Karar satırında (`REPORT_S4_S2.md:7`, `analyze_s4_s2.py:37`) yok.

   Kararın kendisi ön kayda uygun ve doğru. Ama "TUTTU" tek başına okunursa iç optimumun birlikte eskimede de sürdüğü sanılabilir; bu, bulgunun tersi.

   Öneri: karar satırı "TUTTU (biçimsel; L* = 1 ızgara alt sınırında, iç optimum YOK; en iyi kol SU-average)" olsun. Aynı not S4-H2'ye de eklenmeli; SU-best-of (3.872) bile SU-average'ın gerisinde.
3. **ORTA. Makale lehine aşırı genelleme (`yorum_s4_s2.md:1`).** Yorum şöyle diyor: "Makaledeki sonuç modelin bir yapaylığı değil; muhafazakâr bir alt sınır." Ön kayıt Clarke modelini "mevcut modelin tersi yönde bir uç" diye tanımlıyor: i.i.d. tam güçlü inovasyon, LoS da eskiyor.

   İki uç modelde L = 48 kaybının birinde daha büyük çıkması, makaledeki değerin genel bir alt sınır olduğunu göstermez. Öneri: "iki uç modelde de iç optimum var; L = 48 kaybı Clarke'ta %27–32, makale kanalında %13.5–14.8".
4. **KÜÇÜK/ORTA. Yorumdaki "Seçilen kollar (Adam-6, Adam-4) makaledekiyle aynı" ifadesi yanlış (`yorum_s3_s1.md:5`).** Makalenin özetinde (`paper_mobility/mobility_paper_ieee.tex:31`) şöyle yazıyor: "at 10 km/h the peak is at 3 steps". Burada ise Adam-4 seçiliyor. 1.5 m/s için ("4–6 steps") ifade doğru. Bu oturumdaki makine 0.69–0.86 kat daha hızlı olduğu için kayma beklenen bir şey, ama "aynı" denemez.

   Aynı yorumdaki "makaledeki kanaldaki %13.5–14.8" ifadesi de bu oturumda ölçülmüş değer. Makalenin kendi rakamı 1.5 m/s'de %14.0.

## Kontrol edilen başlıca sayılar

| rapor yeri | rapor | yeniden hesap | durum |
| --- | --- | --- | --- |
| E (FLOP / hız değerlendirmesi) | 11008 | 8·(1024 + 256 + 64 + 32) = 11008; FLOP tablosu ON_KAYIT ile birebir | OK |
| Adam adım eğimi (Sapma 1 kalibrasyonu) | 1.086 ms | 1.0859 (timing2 polyfit) | OK |
| ölçülmüş/FLOP oran aralığı | 0.32–0.99 | 0.319–0.989 (25 kol) | OK |
| sapma adam1 / adam48 / CD-8 | 0.862 / 0.775 / 0.690 | 0.862 / 0.775 / 0.690 | OK |
| S3-H1 1.5 m/s, 9 bütçe: seçimler, etkin hızlar, fark, GA | tablo | 9/9 satır OK, GA sapması ≤ 0.009 | OK |
| S3-H1 10 km/h, 9 bütçe | tablo | 9/9 satır OK | OK |
| S3-H1 kararı | TUTTU | TUTTU (B ≥ 20'de GA üst < 0) | OK |
| Kendall τ 1.5 m/s / 10 km/h | 0.900 / 0.873 | 0.900 / 0.873 (τ-a, 25 kol) | OK |
| S3-E seçimleri | Adam-6 / Adam-4 (ikisi de) | aynı | OK |
| S1 karşılaştırma kolu | Adam-6 (6.63 ms, 6.151) / Adam-4 (4.46 ms, 5.913) | aynı | OK |
| S1 r ızgarası, 2 × 18 satır | tablo | 36/36 OK | OK |
| r*_eşit = r*_anlamlı | (10, 15] her iki hız | (10, 15]; 1.5 m/s r = 15 GA alt sınırı +0.004 (rapor +0.007), sınırda | OK |
| derlenmiş artımlı CD − Adam | +0.717 [+0.670, +0.762] / +0.850 [+0.795, +0.905] | +0.717 [+0.675, +0.761] / +0.850 [+0.797, +0.903] | OK |
| derlenmiş doğrudan CD − Adam | +0.514 / +0.603 | aynı | OK |
| hızlanma tablosu (×59 … ×208) | tablo | 8/8 OK | OK |
| s1b, CD kısmı (seçim ve etkin hız, 36 satır) | tablo | arms.json'dan 36/36 OK | OK |
| s1b, r = 1 satırı (Adam, fark, GA) | −1.183 / −0.941 | aynı | OK |
| s1b, r > 1 Adam etkin hızları ve GA | tablo | **ÜRETİLEMEDİ.** Adam'ın gecikme/r noktaları arms.json'da yok; yalnızca s1b.json'da özet var, senaryo başına değer yok. Yeniden üretmek kanal üretimi ister; yasaklandı. Tablo s1b.json/log ile tutarlı. | — |
| üst bölüm s1b aralıkları | −1.40…−0.12, −0.096; −1.42…−0.12, −0.103 | −1.397…−0.115, −0.096; −1.421…−0.121, −0.103 | OK |
| yorum: "en büyük 1.40 (r = 3)" | hız belirtilmemiş | 1.5 m/s'de 1.397 (r = 3); **10 km/h'de 1.421 (r = 5)** | HATA (küçük) |
| yorum: t0 Adam-48 7.04, CD-8 6.93 | 7.04 / 6.93 | 7.037 / 6.925 | OK |
| S4/S2 tablosu, 9 satır × 8 sütun | tablo | 9/9 OK; GA'lar common.boot kopyasıyla birebir | OK |
| tutarlılık: fresh (s4_s2) = arms.json @meas | — | max \|fark\| = 0 (2 seed × 24 kol × 2 hız) | OK |
| S4-H1, S4-H2, S2-H1, S2-H2 | 4 × TUTTU | 4 × TUTTU | OK |
| yorum S4: τ = 0'da 5.412 | 5.412 | t0 Adam-1 = 5.412 (SU-average değil; iki koşul τ = 0'da tanım gereği aynı) | OK |
| yorum S4: 1.15 ms'de %25 kayıp | ~%25 | %25.6 (joint / fresh Adam-1) | OK |
| yorum S4: "10 ms'de hız 1.07", "görece değişim %0.5 (−23 dB) / %38" | — | **ÜRETİLEMEDİ.** s4_s2.json'da 10 ms noktası yok (en yakın Adam-10, 11.03 ms: 1.002); kanal değişimi ham veride hiç yok. Kaynağı betiksiz (altın kural). | — |
| yorum S2: L* 3.4–8.8 ms, kayıp %27–32, taze %13.5–14.8 | — | 3.37–8.80; %26.97–32.36; %13.48–14.83 | OK |
| J0 (trapez) | — | kuvvet serisine göre max hata 2.8e-14 (x ≤ 5) | OK |
| derlenmiş CD geçerliliği (n = 24, %75–92 aynı faz) | ON_KAYIT | **ÜRETİLEMEDİ.** numba fazları ham veride yok | — |

Satır satır tam tablo aşağıdaki "Ek"te.

## Mantık ve ön kayıt

- **Commit sırası doğru.**
  - `ON_KAYIT_S3_S1.md`, `0e2d8a7` (12:29:20) commit'inde. `timing.json` bu commit üzerinde koştu.
  - Sapma 1 ve `ON_KAYIT_S4_S2.md`, `bdcd899` (12:32:29) commit'inde. `timing2.json`, `arms.json` ve `s4_s2.json` bu commit üzerinde, temiz ağaçta koştu (commit alanı `bdcd899`, "+dirty" yok).
  - Sapma 1'de `0e2d8a7` → `bdcd899` farkı yalnızca eklemeden ibaret; ön kaydın gövdesi değişmedi. Karar mantığı (`analyze_s3_s1.py`) sonuçlardan sonra değişmedi; `285b988` yalnızca rapor bölümleri ekledi.
- **Sapma 1 doğru kaydedilmiş.** Sapma, `timing.py` sonucu görüldükten sonra ama `arms.py`'den önce yazılmış; hem kol gecikmelerini hem FLOP kalibrasyonunu (1.328 → 1.086 ms) kapsıyor. Eksik: rapor başlığında Sapma 1 adıyla anılmıyor, yalnızca yorumda "(sapma 1)" diye geçiyor. Öneri: başlığa "Sapma 1: bütün gecikmeler bu oturumda yeniden ölçüldü" satırı.
- **s1b doğru etiketli** ("ÖN KAYIT DIŞI, sonuçlar görüldükten sonra"). Ancak `s1b.json` commit alanı `d7ac933+dirty`: betik koşturulduğunda commit'lenmemişti, ilk kez `285b988`'de girdi. Kural 3 (yol + commit) zayıf. KÜÇÜK.
- **Kural 10.** Makale aleyhine bulgu (yalnız CD derlenirse sıralama döner) en üstte ve yumuşatılmamış. Ancak bu üst bölüm ilk rapor sürümünde (`d7ac933`) yoktu; s1b ile aynı commit'te, onunla dengelenmiş olarak eklendi. Üst bölümdeki "Sıralamayı dil değil, kolların gecikme oranı belirliyor." cümlesi yorumdur ve bulgular bölümünde durmamalı; yorum'a taşınmalı. KÜÇÜK.
- **"yalnızca CD derlenirse … ×191" ifadesi iki değişikliği karıştırıyor.** Artımlı sürüm hem derleme hem rank-1 algoritma değişikliği içeriyor; aynı algoritma torch'ta da uygulanabilir. Yalnız derleme (doğrudan, ×64–69) de sıralamayı döndürüyor (+0.514 / +0.603), yani sonuç sağlam. Ama manşet "derlenir ve artımlı güncellenirse" demeli. s1b'nin "dil değil" sonucu da algoritmik farkı ayırmıyor. KÜÇÜK.
- **S4 ön kaydında "seed 12 seçimi de ayrıca raporlanır" deniyor;** seed 12 L seçimi tabloda yok. Tablodaki "seed 12'de en iyi kol" sütunu tüm kollar üzerinden. Değerler L* ile aynı; tek fark Clarke 1.5 m/s'de (Adam-5'e karşı Adam-4). KÜÇÜK.
- **L* seed 11'de argmax, GA da seed 11'de** (ön kayda ve Makale 2'ye uygun). Bu kazananın laneti yanlılığı içeriyor ve L*−L48 farkını hafifçe büyütüyor. Marjlar büyük olduğu için kararlar etkilenmez; not düşülmeli.
- **Kural 5 (tur-arası yayılım) raporda yok.**
  - torch CD turları bimodal: cd1 = 72.9 / 73.8 / 75.7 / 142.4 / 149.4 ms (max/min 2.05); cd2'de max/min 2.59.
  - r*, cd1 medyanına (75.72) bağlı. Yavaş turlar gerçek olsaydı r* daha yüksek çıkardı; hızlı turların temiz olduğu varsayımı makul ama raporlanmalı.
  - Yük ölçüm sırasında 0.13'ten 0.68'e (timing) ve 0.28'den 0.69'a (timing2) çıktı; muhtemelen ölçümün kendi yükü. timing2 yükleri raporda yok.

## Kod incelemesi

| önem | yer | bulgu | öneri |
| --- | --- | --- | --- |
| ORTA | `timing.py:21-23,51`; `cd_fast.py:253,290`; `baselines.py:207`; `arms.py:29` | CD-s gecikmesi tek senaryodan alınıyor. Bu senaryo 6. taramada erken duruyor, bu yüzden CD-7 ve CD-8 ≈ CD-6. 400 senaryonun %72'sinde 8. tarama fazları değiştiriyor. Erken durma semantiği torch (toplu, max < 1e-7) ve numba (senaryo başına) arasında farklı. Zamanlama tek senaryo olduğu için ikisi burada eşdeğer, ama faz hesabında (toplu torch, 400 senaryo) erken durma pratikte hiç tetiklenmiyor. Yani gecikme ile fazlar aynı işi temsil etmiyor. | CD-s'yi birkaç senaryoda zamanlayıp medyan alın, ya da zamanlamada erken durmayı kapatın (s tam tarama). Ayrıca senaryo başına gerçek tarama sayısını kaydedin. CD-7 ve CD-8 satırlarını yeniden değerlendirin. |
| KÜÇÜK | `timing2.py:21,36` (`TH0` önceden hesaplanıyor); `arms.py:17,26` | Adam-L gecikmesi SU-average başlangıcını (0.23 ms) içermiyor. Bu, Makale 2 kuralıyla tutarlı: `scripts/mumiso_mobility_latency.py:65,84` de aynısını yapıyor. Ama torch CD başlangıcı içeriyor (`baselines.py:188`), FLOP modeli Adam-L'ye 2E ekliyor, numba CD ise içermiyor. Bu tutarsızlık Adam-1'in ölçülmüş/FLOP oranını 0.64'e düşürüyor. Karar etkisi ihmal edilebilir; Adam-6'nın 6.63 → 6.86 ms olması hızı yaklaşık 0.001 düşürür (Adam-6/Adam-8 eğiminden), yani CD lehine. | Raporda bayraklayın. FLOP'ta SU-average'ı ya her iki tarafta sayın ya da hiçbirinde. |
| OK | `arms.py:36,54`; `s4_s2.py:19,43`; `s1b_equal_speedup.py:21,32` | `round(., 9)` indeksleme tutarlı: zaman ızgarası ve sorgu aynı ifadeyle kuruluyor. Farklı ızgaralarla koşan s4_s2 fresh kolu, arms.json @meas ile bit bit aynı. Bu, ızgaradan bağımsızlığı da doğruluyor. | — |
| OK | `s4_s2.py:36,45`, `s4_s2.py:23-25` | Birlikte eskime: W0 = `S.zf(H_eff(0; θ), pt, noise_var = nv)`, aynı θ; τ'da `S.sinr(H_eff(τ; θ), W0, nv)`. Düzenleyici (K·nv/pt) ve güç `rates` ile aynı. Ön kayda uygun. | — |
| OK | `s4_s2.py:37,47-55` | Clarke: p, t = 0 kanalında kullanıcı başına eleman (G) ya da anten (h_d) ortalama gücü; E ~ CN(0, p), senaryo başına tek çekiliş, tohum 1000·seed + hız indeksi; ρ = J0(2π v f_c/c · τ), f_c = 3 GHz (`ris_mu/geometry.py:25` ile aynı). Ön kayda uygun. | — |
| OK | `scipy_free_j0.py` | J0 trapez integrali, seriye göre hata < 3e-14. | — |
| KÜÇÜK | `s4_s2.py:31` | Clarke için t = 0 kanalı `Aging(seed, [0.0])` ile, varsayılan v = 1.5 alınıyor. Fresh ise her hızda yeni `Aging(..., v)` kullanıyor. t = 0 kanalının v'den bağımsız olduğu varsayılıyor. Ham veriden doğrulanamaz; fresh = arms eşliği bunu yalnızca dolaylı destekliyor. | `check_same_scenarios` benzeri bir t = 0 eşitlik kontrolü ekleyin. |

## Ek: betik çıktısı (satır satır)

kontrol: 392 OK, 1 HATA, 1 ÜRETİLEMEDİ, 29 bilgi
| kontrol | rapor | yeniden hesap | durum |
| --- | --- | --- | --- |
| timing.json median adam1 = median(rounds) | 1.142 | 1.142 | OK |
| timing.json median adam48 = median(rounds) | 49.55 | 49.55 | OK |
| timing.json median cd1 = median(rounds) | 75.72 | 75.72 | OK |
| timing.json median cd2 = median(rounds) | 163.1 | 163.1 | OK |
| timing.json median cd3 = median(rounds) | 263.8 | 263.8 | OK |
| timing.json median cd4 = median(rounds) | 335.6 | 335.6 | OK |
| timing.json median cd5 = median(rounds) | 429 | 429 | OK |
| timing.json median cd6 = median(rounds) | 485.6 | 485.6 | OK |
| timing.json median cd7 = median(rounds) | 460.7 | 460.7 | OK |
| timing.json median cd8 = median(rounds) | 485.1 | 485.1 | OK |
| timing.json median numba_direct1 = median(rounds) | 1.283 | 1.283 | OK |
| timing.json median numba_incr1 = median(rounds) | 0.4477 | 0.4477 | OK |
| timing.json median numba_direct2 = median(rounds) | 2.544 | 2.544 | OK |
| timing.json median numba_incr2 = median(rounds) | 0.8498 | 0.8498 | OK |
| timing.json median numba_direct3 = median(rounds) | 3.804 | 3.804 | OK |
| timing.json median numba_incr3 = median(rounds) | 1.271 | 1.271 | OK |
| timing.json median numba_direct4 = median(rounds) | 5.112 | 5.112 | OK |
| timing.json median numba_incr4 = median(rounds) | 1.714 | 1.714 | OK |
| timing.json median numba_direct5 = median(rounds) | 6.368 | 6.368 | OK |
| timing.json median numba_incr5 = median(rounds) | 2.124 | 2.124 | OK |
| timing.json median numba_direct6 = median(rounds) | 7.586 | 7.586 | OK |
| timing.json median numba_incr6 = median(rounds) | 2.541 | 2.541 | OK |
| timing.json median numba_direct7 = median(rounds) | 7.595 | 7.595 | OK |
| timing.json median numba_incr7 = median(rounds) | 2.539 | 2.539 | OK |
| timing.json median numba_direct8 = median(rounds) | 7.602 | 7.602 | OK |
| timing.json median numba_incr8 = median(rounds) | 2.543 | 2.543 | OK |
| timing2.json median su_average = median(rounds) | 0.2311 | 0.2311 | OK |
| timing2.json median su_best_of = median(rounds) | 1.238 | 1.238 | OK |
| timing2.json median adam1 = median(rounds) | 1.154 | 1.154 | OK |
| timing2.json median adam2 = median(rounds) | 2.281 | 2.281 | OK |
| timing2.json median adam4 = median(rounds) | 4.455 | 4.455 | OK |
| timing2.json median adam8 = median(rounds) | 8.804 | 8.804 | OK |
| timing2.json median adam16 = median(rounds) | 17.71 | 17.71 | OK |
| timing2.json median adam32 = median(rounds) | 34.8 | 34.8 | OK |
| timing2.json median adam48 = median(rounds) | 52.25 | 52.25 | OK |
| timing2.json median pga = median(rounds) | 3952 | 3952 | OK |
| Adam eğimi (ms/adım, timing2 polyfit) = rapor 1.086 | 1.086 | 1.086 | OK |
| lat_meas = timing/timing2 medyanları (+ Adam interp), max |fark| | 0 | 0 | OK |
| E (ON_KAYIT formülü) = 11008 | 1.101e+04 | 1.101e+04 | OK |
| arms.json E_flops | 1.101e+04 | 1.101e+04 | OK |
| FLOP tablosu = ON_KAYIT tablosu, max |fark| | 0 | 0 | OK |
| ms_per_flop | 3.288e+04 | 3.288e+04 | OK |
| S3-E SU-average ölçülmüş/FLOP/oran | [+0.230, +0.720, +0.320] | [+0.231, +0.724, +0.319] | OK |
| S3-E SU-best-of ölçülmüş/FLOP/oran | [+1.240, +2.900, +0.430] | [+1.238, +2.896, +0.428] | OK |
| S3-E Adam-1 ölçülmüş/FLOP/oran | [+1.150, +1.810, +0.640] | [+1.154, +1.810, +0.638] | OK |
| S3-E Adam-8 ölçülmüş/FLOP/oran | [+8.800, +9.410, +0.940] | [+8.804, +9.412, +0.935] | OK |
| S3-E Adam-48 ölçülmüş/FLOP/oran | [+52.250, +52.850, +0.990] | [+52.248, +52.849, +0.989] | OK |
| S3-E CD-1 ölçülmüş/FLOP/oran | [+75.720, +186.780, +0.410] | [+75.721, +186.783, +0.405] | OK |
| S3-E CD-8 ölçülmüş/FLOP/oran | [+485.060, +1484.130, +0.330] | [+485.062, +1484.127, +0.327] | OK |
| S3-E Long-run Adam ölçülmüş/FLOP/oran | [+3952.070, +4346.320, +0.910] | [+3952.067, +4346.319, +0.909] | OK |
| oran aralığı (bütün 25 kol) min,max = 0.32–0.99 | [+0.320, +0.990] | [+0.319, +0.989] | OK |
| sapma adam1/adam48/CD-8 | [+0.862, +0.775, +0.690] | [+0.862, +0.775, +0.690] | OK |
| yük başlangıç/öncesi/sonrası (timing.json) | [+0.060, +0.060, +0.750] | [+0.056, +0.056, +0.753] | OK |
| S1 zamanlama s=1 torch/nd/ni/×d/×i | [+75.720, +1.283, +0.448, +59.000, +169.000] | [+75.721, +1.283, +0.448, +59.000, +169.000] | OK |
| S1 zamanlama s=2 torch/nd/ni/×d/×i | [+163.050, +2.544, +0.850, +64.000, +192.000] | [+163.053, +2.544, +0.850, +64.000, +192.000] | OK |
| S1 zamanlama s=3 torch/nd/ni/×d/×i | [+263.790, +3.804, +1.271, +69.000, +208.000] | [+263.794, +3.804, +1.271, +69.000, +208.000] | OK |
| S1 zamanlama s=4 torch/nd/ni/×d/×i | [+335.620, +5.112, +1.714, +66.000, +196.000] | [+335.616, +5.112, +1.714, +66.000, +196.000] | OK |
| S1 zamanlama s=5 torch/nd/ni/×d/×i | [+428.960, +6.368, +2.124, +67.000, +202.000] | [+428.959, +6.368, +2.124, +67.000, +202.000] | OK |
| S1 zamanlama s=6 torch/nd/ni/×d/×i | [+485.590, +7.586, +2.541, +64.000, +191.000] | [+485.587, +7.586, +2.541, +64.000, +191.000] | OK |
| S1 zamanlama s=7 torch/nd/ni/×d/×i | [+460.730, +7.595, +2.539, +61.000, +181.000] | [+460.727, +7.595, +2.539, +61.000, +181.000] | OK |
| S1 zamanlama s=8 torch/nd/ni/×d/×i | [+485.060, +7.602, +2.543, +64.000, +191.000] | [+485.062, +7.602, +2.543, +64.000, +191.000] | OK |
| S3-H1 1.5 m/s B=2 seçimler | Adam-1/Adam-1 | Adam-1/Adam-1 | OK |
| S3-H1 1.5 m/s B=2 etkinler, fark | [+5.409, +5.409, +0.000] | [+5.409, +5.409, +0.000] | OK |
| S3-H1 1.5 m/s B=2 GA | [+0.000, +0.000] | [+0.000, +0.000] | OK |
| S3-H1 1.5 m/s B=5 seçimler | Adam-4/Adam-4 | Adam-4/Adam-4 | OK |
| S3-H1 1.5 m/s B=5 etkinler, fark | [+6.059, +6.059, +0.000] | [+6.059, +6.059, +0.000] | OK |
| S3-H1 1.5 m/s B=5 GA | [+0.000, +0.000] | [+0.000, +0.000] | OK |
| S3-H1 1.5 m/s B=10 seçimler | Adam-8/Adam-6 | Adam-8/Adam-6 | OK |
| S3-H1 1.5 m/s B=10 etkinler, fark | [+6.139, +6.151, -0.012] | [+6.139, +6.151, -0.012] | OK |
| S3-H1 1.5 m/s B=10 GA | [-0.036, +0.014] | [-0.037, +0.013] | OK |
| S3-H1 1.5 m/s B=20 seçimler | Adam-16/Adam-6 | Adam-16/Adam-6 | OK |
| S3-H1 1.5 m/s B=20 etkinler, fark | [+5.720, +6.151, -0.431] | [+5.720, +6.151, -0.431] | OK |
| S3-H1 1.5 m/s B=20 GA | [-0.494, -0.370] | [-0.495, -0.368] | OK |
| S3-H1 1.5 m/s B=50 seçimler | Adam-32/Adam-6 | Adam-32/Adam-6 | OK |
| S3-H1 1.5 m/s B=50 etkinler, fark | [+5.335, +6.151, -0.817] | [+5.335, +6.151, -0.817] | OK |
| S3-H1 1.5 m/s B=50 GA | [-0.905, -0.728] | [-0.903, -0.730] | OK |
| S3-H1 1.5 m/s B=100 seçimler | Adam-48/Adam-6 | Adam-48/Adam-6 | OK |
| S3-H1 1.5 m/s B=100 etkinler, fark | [+5.239, +6.151, -0.912] | [+5.239, +6.151, -0.912] | OK |
| S3-H1 1.5 m/s B=100 GA | [-1.009, -0.823] | [-1.008, -0.822] | OK |
| S3-H1 1.5 m/s B=200 seçimler | Adam-48/Adam-6 | Adam-48/Adam-6 | OK |
| S3-H1 1.5 m/s B=200 etkinler, fark | [+5.239, +6.151, -0.912] | [+5.239, +6.151, -0.912] | OK |
| S3-H1 1.5 m/s B=200 GA | [-1.007, -0.823] | [-1.002, -0.822] | OK |
| S3-H1 1.5 m/s B=1000 seçimler | Adam-48/Adam-6 | Adam-48/Adam-6 | OK |
| S3-H1 1.5 m/s B=1000 etkinler, fark | [+5.239, +6.151, -0.912] | [+5.239, +6.151, -0.912] | OK |
| S3-H1 1.5 m/s B=1000 GA | [-1.007, -0.816] | [-1.006, -0.817] | OK |
| S3-H1 1.5 m/s B=6000 seçimler | Long-run Adam/Adam-6 | Long-run Adam/Adam-6 | OK |
| S3-H1 1.5 m/s B=6000 etkinler, fark | [+4.737, +6.151, -1.414] | [+4.737, +6.151, -1.414] | OK |
| S3-H1 1.5 m/s B=6000 GA | [-1.563, -1.253] | [-1.563, -1.262] | OK |
| S3-H1 1.5 m/s karar | TUTTU | TUTTU | OK |
| S3-E 1.5 m/s Kendall tau (tau-a, 25 kol) | 0.9 | 0.9 | OK |
| S3-E 1.5 m/s seçilen ölç/FLOP | Adam-6/Adam-6 | Adam-6/Adam-6 | OK |
| S3-E 1.5 m/s etkinler | [+6.151, +6.151] | [+6.151, +6.151] | OK |
| S1 1.5 m/s karşılaştırma kolu | Adam-6 | Adam-6 | OK |
| S1 1.5 m/s kol gecikmesi, etkin | [+6.630, +6.151] | [+6.629, +6.151] | OK |
| S1 1.5 m/s r=1 ayarlı CD | CD-2 | CD-2 | OK |
| S1 1.5 m/s r=1 gecikme, CD etkin, fark | [+163.050, +4.968, -1.183] | [+163.053, +4.968, -1.183] | OK |
| S1 1.5 m/s r=1 GA | [-1.277, -1.087] | [-1.281, -1.088] | OK |
| S1 1.5 m/s r=1.5 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=1.5 gecikme, CD etkin, fark | [+50.480, +4.967, -1.185] | [+50.480, +4.967, -1.185] | OK |
| S1 1.5 m/s r=1.5 GA | [-1.276, -1.100] | [-1.270, -1.094] | OK |
| S1 1.5 m/s r=2 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=2 gecikme, CD etkin, fark | [+37.860, +5.049, -1.103] | [+37.860, +5.049, -1.103] | OK |
| S1 1.5 m/s r=2 GA | [-1.194, -1.009] | [-1.195, -1.010] | OK |
| S1 1.5 m/s r=3 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=3 gecikme, CD etkin, fark | [+25.240, +5.167, -0.985] | [+25.240, +5.167, -0.985] | OK |
| S1 1.5 m/s r=3 GA | [-1.062, -0.908] | [-1.068, -0.902] | OK |
| S1 1.5 m/s r=5 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=5 gecikme, CD etkin, fark | [+15.140, +5.632, -0.520] | [+15.144, +5.632, -0.520] | OK |
| S1 1.5 m/s r=5 GA | [-0.571, -0.465] | [-0.577, -0.464] | OK |
| S1 1.5 m/s r=7 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=7 gecikme, CD etkin, fark | [+10.820, +5.888, -0.263] | [+10.817, +5.888, -0.263] | OK |
| S1 1.5 m/s r=7 GA | [-0.307, -0.221] | [-0.307, -0.221] | OK |
| S1 1.5 m/s r=10 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=10 gecikme, CD etkin, fark | [+7.570, +6.074, -0.078] | [+7.572, +6.074, -0.078] | OK |
| S1 1.5 m/s r=10 GA | [-0.115, -0.040] | [-0.116, -0.042] | OK |
| S1 1.5 m/s r=15 ayarlı CD | CD-1 | CD-1 | OK |
| S1 1.5 m/s r=15 gecikme, CD etkin, fark | [+5.050, +6.194, +0.042] | [+5.048, +6.194, +0.042] | OK |
| S1 1.5 m/s r=15 GA | [+0.007, +0.078] | [+0.004, +0.077] | OK |
| S1 1.5 m/s r=20 ayarlı CD | CD-2 | CD-2 | OK |
| S1 1.5 m/s r=20 gecikme, CD etkin, fark | [+8.150, +6.313, +0.162] | [+8.153, +6.313, +0.162] | OK |
| S1 1.5 m/s r=20 GA | [+0.124, +0.200] | [+0.125, +0.198] | OK |
| S1 1.5 m/s r=30 ayarlı CD | CD-2 | CD-2 | OK |
| S1 1.5 m/s r=30 gecikme, CD etkin, fark | [+5.440, +6.478, +0.327] | [+5.435, +6.478, +0.327] | OK |
| S1 1.5 m/s r=30 GA | [+0.292, +0.362] | [+0.291, +0.362] | OK |
| S1 1.5 m/s r=50 ayarlı CD | CD-3 | CD-3 | OK |
| S1 1.5 m/s r=50 gecikme, CD etkin, fark | [+5.280, +6.589, +0.438] | [+5.276, +6.589, +0.438] | OK |
| S1 1.5 m/s r=50 GA | [+0.399, +0.474] | [+0.400, +0.476] | OK |
| S1 1.5 m/s r=70 ayarlı CD | CD-4 | CD-4 | OK |
| S1 1.5 m/s r=70 gecikme, CD etkin, fark | [+4.790, +6.672, +0.521] | [+4.795, +6.672, +0.521] | OK |
| S1 1.5 m/s r=70 GA | [+0.480, +0.561] | [+0.480, +0.562] | OK |
| S1 1.5 m/s r=100 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=100 gecikme, CD etkin, fark | [+4.850, +6.755, +0.604] | [+4.851, +6.755, +0.604] | OK |
| S1 1.5 m/s r=100 GA | [+0.562, +0.646] | [+0.561, +0.647] | OK |
| S1 1.5 m/s r=150 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=150 gecikme, CD etkin, fark | [+3.230, +6.839, +0.688] | [+3.234, +6.839, +0.688] | OK |
| S1 1.5 m/s r=150 GA | [+0.646, +0.730] | [+0.646, +0.731] | OK |
| S1 1.5 m/s r=200 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=200 gecikme, CD etkin, fark | [+2.430, +6.873, +0.721] | [+2.425, +6.873, +0.721] | OK |
| S1 1.5 m/s r=200 GA | [+0.677, +0.767] | [+0.677, +0.767] | OK |
| S1 1.5 m/s r=300 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=300 gecikme, CD etkin, fark | [+1.620, +6.899, +0.748] | [+1.617, +6.899, +0.748] | OK |
| S1 1.5 m/s r=300 GA | [+0.704, +0.791] | [+0.700, +0.793] | OK |
| S1 1.5 m/s r=500 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=500 gecikme, CD etkin, fark | [+0.970, +6.914, +0.763] | [+0.970, +6.914, +0.763] | OK |
| S1 1.5 m/s r=500 GA | [+0.716, +0.810] | [+0.716, +0.808] | OK |
| S1 1.5 m/s r=1000 ayarlı CD | CD-8 | CD-8 | OK |
| S1 1.5 m/s r=1000 gecikme, CD etkin, fark | [+0.490, +6.922, +0.770] | [+0.485, +6.922, +0.770] | OK |
| S1 1.5 m/s r=1000 GA | [+0.723, +0.818] | [+0.723, +0.817] | OK |
| S1 1.5 m/s r*_eşit, r*_anlamlı üst uç | [+15.000, +15.000] | [+15.000, +15.000] | OK |
| S1 1.5 m/s doğrudan kol | CD-3 | CD-3 | OK |
| S1 1.5 m/s doğrudan gecikme, ×, etkin, fark | [+3.800, +69.000, +6.666, +0.514] | [+3.804, +69.000, +6.666, +0.514] | OK |
| S1 1.5 m/s doğrudan GA | [+0.478, +0.552] | [+0.475, +0.554] | OK |
| S1 1.5 m/s artımlı kol | CD-8 | CD-8 | OK |
| S1 1.5 m/s artımlı gecikme, ×, etkin, fark | [+2.540, +191.000, +6.868, +0.717] | [+2.543, +191.000, +6.868, +0.717] | OK |
| S1 1.5 m/s artımlı GA | [+0.670, +0.762] | [+0.675, +0.761] | OK |
| s1b 1.5 m/s r=1 ayarlı CD + CD etkin (arms.json'dan) | [+4.968] | [+4.968] | OK |
| s1b 1.5 m/s r=1 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 1.5 m/s r=1.5 ayarlı CD + CD etkin (arms.json'dan) | [+4.967] | [+4.967] | OK |
| s1b 1.5 m/s r=1.5 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=2 ayarlı CD + CD etkin (arms.json'dan) | [+5.049] | [+5.049] | OK |
| s1b 1.5 m/s r=2 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=3 ayarlı CD + CD etkin (arms.json'dan) | [+5.167] | [+5.167] | OK |
| s1b 1.5 m/s r=3 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=5 ayarlı CD + CD etkin (arms.json'dan) | [+5.632] | [+5.632] | OK |
| s1b 1.5 m/s r=5 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=7 ayarlı CD + CD etkin (arms.json'dan) | [+5.888] | [+5.888] | OK |
| s1b 1.5 m/s r=7 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=10 ayarlı CD + CD etkin (arms.json'dan) | [+6.074] | [+6.074] | OK |
| s1b 1.5 m/s r=10 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=15 ayarlı CD + CD etkin (arms.json'dan) | [+6.194] | [+6.194] | OK |
| s1b 1.5 m/s r=15 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 1.5 m/s r=20 ayarlı CD + CD etkin (arms.json'dan) | [+6.313] | [+6.313] | OK |
| s1b 1.5 m/s r=20 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 1.5 m/s r=30 ayarlı CD + CD etkin (arms.json'dan) | [+6.478] | [+6.478] | OK |
| s1b 1.5 m/s r=30 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 1.5 m/s r=50 ayarlı CD + CD etkin (arms.json'dan) | [+6.589] | [+6.589] | OK |
| s1b 1.5 m/s r=50 ayarlı CD adı | CD-3 | CD-3 | OK |
| s1b 1.5 m/s r=70 ayarlı CD + CD etkin (arms.json'dan) | [+6.672] | [+6.672] | OK |
| s1b 1.5 m/s r=70 ayarlı CD adı | CD-4 | CD-4 | OK |
| s1b 1.5 m/s r=100 ayarlı CD + CD etkin (arms.json'dan) | [+6.755] | [+6.755] | OK |
| s1b 1.5 m/s r=100 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=150 ayarlı CD + CD etkin (arms.json'dan) | [+6.839] | [+6.839] | OK |
| s1b 1.5 m/s r=150 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=200 ayarlı CD + CD etkin (arms.json'dan) | [+6.873] | [+6.873] | OK |
| s1b 1.5 m/s r=200 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=300 ayarlı CD + CD etkin (arms.json'dan) | [+6.899] | [+6.899] | OK |
| s1b 1.5 m/s r=300 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=500 ayarlı CD + CD etkin (arms.json'dan) | [+6.914] | [+6.914] | OK |
| s1b 1.5 m/s r=500 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=1000 ayarlı CD + CD etkin (arms.json'dan) | [+6.922] | [+6.922] | OK |
| s1b 1.5 m/s r=1000 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 1.5 m/s r=1 Adam etkin, CD−Adam, GA | [+6.151, -1.183, -1.278, -1.090] | [+6.151, -1.183, -1.285, -1.083] | OK |
| s1b 1.5 m/s üst bölüm aralığı min,max,en kötü üst GA | [-1.400, -0.120, -0.096] | [-1.397, -0.115, -0.096] | OK |
| s1b 1.5 m/s bütün r'lerde GA üst < 0 | evet | evet | OK |
| s1b 1.5 m/s rapor tablosu = s1b.json (satır sayısı eşleşen) | 18 | 18 | OK |
| S3-H1 10 km/h B=2 seçimler | Adam-1/Adam-1 | Adam-1/Adam-1 | OK |
| S3-H1 10 km/h B=2 etkinler, fark | [+5.402, +5.402, +0.000] | [+5.402, +5.402, +0.000] | OK |
| S3-H1 10 km/h B=2 GA | [+0.000, +0.000] | [+0.000, +0.000] | OK |
| S3-H1 10 km/h B=5 seçimler | Adam-4/Adam-4 | Adam-4/Adam-4 | OK |
| S3-H1 10 km/h B=5 etkinler, fark | [+5.913, +5.913, +0.000] | [+5.913, +5.913, +0.000] | OK |
| S3-H1 10 km/h B=5 GA | [+0.000, +0.000] | [+0.000, +0.000] | OK |
| S3-H1 10 km/h B=10 seçimler | Adam-8/Adam-4 | Adam-8/Adam-4 | OK |
| S3-H1 10 km/h B=10 etkinler, fark | [+5.651, +5.913, -0.262] | [+5.651, +5.913, -0.262] | OK |
| S3-H1 10 km/h B=10 GA | [-0.320, -0.210] | [-0.321, -0.205] | OK |
| S3-H1 10 km/h B=20 seçimler | Adam-16/Adam-4 | Adam-16/Adam-4 | OK |
| S3-H1 10 km/h B=20 etkinler, fark | [+5.238, +5.913, -0.675] | [+5.238, +5.913, -0.675] | OK |
| S3-H1 10 km/h B=20 GA | [-0.757, -0.591] | [-0.760, -0.589] | OK |
| S3-H1 10 km/h B=50 seçimler | Adam-32/Adam-4 | Adam-32/Adam-4 | OK |
| S3-H1 10 km/h B=50 etkinler, fark | [+5.153, +5.913, -0.760] | [+5.153, +5.913, -0.760] | OK |
| S3-H1 10 km/h B=50 GA | [-0.852, -0.673] | [-0.853, -0.668] | OK |
| S3-H1 10 km/h B=100 seçimler | Adam-48/Adam-4 | Adam-48/Adam-4 | OK |
| S3-H1 10 km/h B=100 etkinler, fark | [+5.116, +5.913, -0.797] | [+5.116, +5.913, -0.797] | OK |
| S3-H1 10 km/h B=100 GA | [-0.900, -0.704] | [-0.890, -0.700] | OK |
| S3-H1 10 km/h B=200 seçimler | Adam-48/Adam-4 | Adam-48/Adam-4 | OK |
| S3-H1 10 km/h B=200 etkinler, fark | [+5.116, +5.913, -0.797] | [+5.116, +5.913, -0.797] | OK |
| S3-H1 10 km/h B=200 GA | [-0.888, -0.701] | [-0.897, -0.703] | OK |
| S3-H1 10 km/h B=1000 seçimler | Adam-48/Adam-4 | Adam-48/Adam-4 | OK |
| S3-H1 10 km/h B=1000 etkinler, fark | [+5.116, +5.913, -0.797] | [+5.116, +5.913, -0.797] | OK |
| S3-H1 10 km/h B=1000 GA | [-0.897, -0.707] | [-0.892, -0.708] | OK |
| S3-H1 10 km/h B=6000 seçimler | Long-run Adam/Adam-4 | Long-run Adam/Adam-4 | OK |
| S3-H1 10 km/h B=6000 etkinler, fark | [+4.680, +5.913, -1.233] | [+4.680, +5.913, -1.233] | OK |
| S3-H1 10 km/h B=6000 GA | [-1.440, -1.030] | [-1.443, -1.026] | OK |
| S3-E 10 km/h Kendall tau (tau-a, 25 kol) | 0.873 | 0.8733 | OK |
| S3-E 10 km/h seçilen ölç/FLOP | Adam-4/Adam-4 | Adam-4/Adam-4 | OK |
| S3-E 10 km/h etkinler | [+5.913, +5.913] | [+5.913, +5.913] | OK |
| S1 10 km/h karşılaştırma kolu | Adam-4 | Adam-4 | OK |
| S1 10 km/h kol gecikmesi, etkin | [+4.460, +5.913] | [+4.455, +5.913] | OK |
| S1 10 km/h r=1 ayarlı CD | CD-2 | CD-2 | OK |
| S1 10 km/h r=1 gecikme, CD etkin, fark | [+163.050, +4.972, -0.941] | [+163.053, +4.972, -0.941] | OK |
| S1 10 km/h r=1 GA | [-1.043, -0.850] | [-1.034, -0.846] | OK |
| S1 10 km/h r=1.5 ayarlı CD | CD-3 | CD-3 | OK |
| S1 10 km/h r=1.5 gecikme, CD etkin, fark | [+175.860, +4.999, -0.914] | [+175.863, +4.999, -0.914] | OK |
| S1 10 km/h r=1.5 GA | [-1.007, -0.813] | [-1.017, -0.818] | OK |
| S1 10 km/h r=2 ayarlı CD | CD-2 | CD-2 | OK |
| S1 10 km/h r=2 gecikme, CD etkin, fark | [+81.530, +5.048, -0.865] | [+81.527, +5.048, -0.865] | OK |
| S1 10 km/h r=2 GA | [-0.959, -0.776] | [-0.958, -0.775] | OK |
| S1 10 km/h r=3 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=3 gecikme, CD etkin, fark | [+25.240, +5.013, -0.900] | [+25.240, +5.013, -0.900] | OK |
| S1 10 km/h r=3 GA | [-0.986, -0.811] | [-0.990, -0.811] | OK |
| S1 10 km/h r=5 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=5 gecikme, CD etkin, fark | [+15.140, +5.108, -0.804] | [+15.144, +5.108, -0.804] | OK |
| S1 10 km/h r=5 GA | [-0.889, -0.721] | [-0.890, -0.727] | OK |
| S1 10 km/h r=7 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=7 gecikme, CD etkin, fark | [+10.820, +5.361, -0.552] | [+10.817, +5.361, -0.552] | OK |
| S1 10 km/h r=7 GA | [-0.619, -0.489] | [-0.617, -0.488] | OK |
| S1 10 km/h r=10 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=10 gecikme, CD etkin, fark | [+7.570, +5.699, -0.214] | [+7.572, +5.699, -0.214] | OK |
| S1 10 km/h r=10 GA | [-0.262, -0.168] | [-0.265, -0.166] | OK |
| S1 10 km/h r=15 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=15 gecikme, CD etkin, fark | [+5.050, +5.973, +0.061] | [+5.048, +5.973, +0.061] | OK |
| S1 10 km/h r=15 GA | [+0.021, +0.101] | [+0.019, +0.101] | OK |
| S1 10 km/h r=20 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=20 gecikme, CD etkin, fark | [+3.790, +6.104, +0.191] | [+3.786, +6.104, +0.191] | OK |
| S1 10 km/h r=20 GA | [+0.152, +0.229] | [+0.153, +0.228] | OK |
| S1 10 km/h r=30 ayarlı CD | CD-1 | CD-1 | OK |
| S1 10 km/h r=30 gecikme, CD etkin, fark | [+2.520, +6.209, +0.296] | [+2.524, +6.209, +0.296] | OK |
| S1 10 km/h r=30 GA | [+0.257, +0.336] | [+0.256, +0.338] | OK |
| S1 10 km/h r=50 ayarlı CD | CD-2 | CD-2 | OK |
| S1 10 km/h r=50 gecikme, CD etkin, fark | [+3.260, +6.447, +0.534] | [+3.261, +6.447, +0.534] | OK |
| S1 10 km/h r=50 GA | [+0.491, +0.577] | [+0.494, +0.576] | OK |
| S1 10 km/h r=70 ayarlı CD | CD-2 | CD-2 | OK |
| S1 10 km/h r=70 gecikme, CD etkin, fark | [+2.330, +6.535, +0.622] | [+2.329, +6.535, +0.622] | OK |
| S1 10 km/h r=70 GA | [+0.577, +0.671] | [+0.579, +0.670] | OK |
| S1 10 km/h r=100 ayarlı CD | CD-3 | CD-3 | OK |
| S1 10 km/h r=100 gecikme, CD etkin, fark | [+2.640, +6.611, +0.698] | [+2.638, +6.611, +0.698] | OK |
| S1 10 km/h r=100 GA | [+0.652, +0.745] | [+0.650, +0.745] | OK |
| S1 10 km/h r=150 ayarlı CD | CD-4 | CD-4 | OK |
| S1 10 km/h r=150 gecikme, CD etkin, fark | [+2.240, +6.707, +0.794] | [+2.237, +6.707, +0.794] | OK |
| S1 10 km/h r=150 GA | [+0.742, +0.844] | [+0.743, +0.846] | OK |
| S1 10 km/h r=200 ayarlı CD | CD-8 | CD-8 | OK |
| S1 10 km/h r=200 gecikme, CD etkin, fark | [+2.430, +6.776, +0.863] | [+2.425, +6.776, +0.863] | OK |
| S1 10 km/h r=200 GA | [+0.809, +0.915] | [+0.809, +0.916] | OK |
| S1 10 km/h r=300 ayarlı CD | CD-8 | CD-8 | OK |
| S1 10 km/h r=300 gecikme, CD etkin, fark | [+1.620, +6.850, +0.937] | [+1.617, +6.850, +0.937] | OK |
| S1 10 km/h r=300 GA | [+0.882, +0.991] | [+0.882, +0.995] | OK |
| S1 10 km/h r=500 ayarlı CD | CD-8 | CD-8 | OK |
| S1 10 km/h r=500 gecikme, CD etkin, fark | [+0.970, +6.894, +0.981] | [+0.970, +6.894, +0.981] | OK |
| S1 10 km/h r=500 GA | [+0.921, +1.037] | [+0.925, +1.038] | OK |
| S1 10 km/h r=1000 ayarlı CD | CD-8 | CD-8 | OK |
| S1 10 km/h r=1000 gecikme, CD etkin, fark | [+0.490, +6.916, +1.003] | [+0.485, +6.916, +1.003] | OK |
| S1 10 km/h r=1000 GA | [+0.946, +1.060] | [+0.942, +1.067] | OK |
| S1 10 km/h r*_eşit, r*_anlamlı üst uç | [+15.000, +15.000] | [+15.000, +15.000] | OK |
| S1 10 km/h doğrudan kol | CD-2 | CD-2 | OK |
| S1 10 km/h doğrudan gecikme, ×, etkin, fark | [+2.540, +64.000, +6.516, +0.603] | [+2.544, +64.000, +6.516, +0.603] | OK |
| S1 10 km/h doğrudan GA | [+0.560, +0.647] | [+0.558, +0.650] | OK |
| S1 10 km/h artımlı kol | CD-8 | CD-8 | OK |
| S1 10 km/h artımlı gecikme, ×, etkin, fark | [+2.540, +191.000, +6.763, +0.850] | [+2.543, +191.000, +6.763, +0.850] | OK |
| S1 10 km/h artımlı GA | [+0.795, +0.905] | [+0.797, +0.903] | OK |
| s1b 10 km/h r=1 ayarlı CD + CD etkin (arms.json'dan) | [+4.972] | [+4.972] | OK |
| s1b 10 km/h r=1 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 10 km/h r=1.5 ayarlı CD + CD etkin (arms.json'dan) | [+4.999] | [+4.999] | OK |
| s1b 10 km/h r=1.5 ayarlı CD adı | CD-3 | CD-3 | OK |
| s1b 10 km/h r=2 ayarlı CD + CD etkin (arms.json'dan) | [+5.048] | [+5.048] | OK |
| s1b 10 km/h r=2 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 10 km/h r=3 ayarlı CD + CD etkin (arms.json'dan) | [+5.013] | [+5.013] | OK |
| s1b 10 km/h r=3 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=5 ayarlı CD + CD etkin (arms.json'dan) | [+5.108] | [+5.108] | OK |
| s1b 10 km/h r=5 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=7 ayarlı CD + CD etkin (arms.json'dan) | [+5.361] | [+5.361] | OK |
| s1b 10 km/h r=7 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=10 ayarlı CD + CD etkin (arms.json'dan) | [+5.699] | [+5.699] | OK |
| s1b 10 km/h r=10 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=15 ayarlı CD + CD etkin (arms.json'dan) | [+5.973] | [+5.973] | OK |
| s1b 10 km/h r=15 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=20 ayarlı CD + CD etkin (arms.json'dan) | [+6.104] | [+6.104] | OK |
| s1b 10 km/h r=20 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=30 ayarlı CD + CD etkin (arms.json'dan) | [+6.209] | [+6.209] | OK |
| s1b 10 km/h r=30 ayarlı CD adı | CD-1 | CD-1 | OK |
| s1b 10 km/h r=50 ayarlı CD + CD etkin (arms.json'dan) | [+6.447] | [+6.447] | OK |
| s1b 10 km/h r=50 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 10 km/h r=70 ayarlı CD + CD etkin (arms.json'dan) | [+6.535] | [+6.535] | OK |
| s1b 10 km/h r=70 ayarlı CD adı | CD-2 | CD-2 | OK |
| s1b 10 km/h r=100 ayarlı CD + CD etkin (arms.json'dan) | [+6.611] | [+6.611] | OK |
| s1b 10 km/h r=100 ayarlı CD adı | CD-3 | CD-3 | OK |
| s1b 10 km/h r=150 ayarlı CD + CD etkin (arms.json'dan) | [+6.707] | [+6.707] | OK |
| s1b 10 km/h r=150 ayarlı CD adı | CD-4 | CD-4 | OK |
| s1b 10 km/h r=200 ayarlı CD + CD etkin (arms.json'dan) | [+6.776] | [+6.776] | OK |
| s1b 10 km/h r=200 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 10 km/h r=300 ayarlı CD + CD etkin (arms.json'dan) | [+6.850] | [+6.850] | OK |
| s1b 10 km/h r=300 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 10 km/h r=500 ayarlı CD + CD etkin (arms.json'dan) | [+6.894] | [+6.894] | OK |
| s1b 10 km/h r=500 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 10 km/h r=1000 ayarlı CD + CD etkin (arms.json'dan) | [+6.916] | [+6.916] | OK |
| s1b 10 km/h r=1000 ayarlı CD adı | CD-8 | CD-8 | OK |
| s1b 10 km/h r=1 Adam etkin, CD−Adam, GA | [+5.913, -0.941, -1.039, -0.849] | [+5.913, -0.941, -1.034, -0.847] | OK |
| s1b 10 km/h üst bölüm aralığı min,max,en kötü üst GA | [-1.420, -0.120, -0.103] | [-1.421, -0.121, -0.103] | OK |
| s1b 10 km/h bütün r'lerde GA üst < 0 | evet | evet | OK |
| s1b 10 km/h rapor tablosu = s1b.json (satır sayısı eşleşen) | 18 | 18 | OK |
| yorum: t0 Adam-48 seed 11 1.5 m/s (7.04) | 7.04 | 7.037 | OK |
| yorum: t0 CD-8 seed 11 1.5 m/s (6.93) | 6.93 | 6.925 | OK |
| yorum: 'fark en büyük 1.40 (r=3)' 1.5 m/s | [+1.400, +3.000] | [+1.397, +3.000] | OK |
| yorum: aynı ifade 10 km/h için (rapor 1.40, r=3) | [+1.400, +3.000] | [+1.421, +5.000] | HATA |
| s3_s1.json s1 1.5 m/s numba_incr diff | 0.717 | 0.7169 | OK |
| [bilgi] seed 11: t0 CD-5 ≠ CD-6 olan senaryo sayısı (/400) | — | 359 | bilgi |
| [bilgi] seed 11: t0 CD-6 ≠ CD-7 olan senaryo sayısı (/400) | — | 325 | bilgi |
| [bilgi] seed 11: t0 CD-6 ≠ CD-8 olan senaryo sayısı (/400) | — | 325 | bilgi |
| [bilgi] seed 11: t0 CD-7 ≠ CD-8 olan senaryo sayısı (/400) | — | 288 | bilgi |
| [bilgi] seed 12: t0 CD-5 ≠ CD-6 olan senaryo sayısı (/400) | — | 367 | bilgi |
| [bilgi] seed 12: t0 CD-6 ≠ CD-7 olan senaryo sayısı (/400) | — | 332 | bilgi |
| [bilgi] seed 12: t0 CD-6 ≠ CD-8 olan senaryo sayısı (/400) | — | 332 | bilgi |
| [bilgi] seed 12: t0 CD-7 ≠ CD-8 olan senaryo sayısı (/400) | — | 290 | bilgi |
| [bilgi] numba_direct s=1..8 ms | — | 1.28 2.54 3.80 5.11 6.37 7.59 7.60 7.60 | bilgi |
| [bilgi] numba_incr s=1..8 ms | — | 0.45 0.85 1.27 1.71 2.12 2.54 2.54 2.54 | bilgi |
| [bilgi] cd s=1..8 ms | — | 75.72 163.05 263.79 335.62 428.96 485.59 460.73 485.06 | bilgi |
| [bilgi] cd1 tur-arası max/min | — | 2.05 | bilgi |
| [bilgi] cd2 tur-arası max/min | — | 2.59 | bilgi |
| [bilgi] cd5 tur-arası max/min | — | 1.51 | bilgi |
| [bilgi] cd6 tur-arası max/min | — | 1.57 | bilgi |
| [bilgi] cd8 tur-arası max/min | — | 1.28 | bilgi |
| [bilgi] 1.5 m/s CD-8 etkin @2.54 ms (numba_incr) / @3.23 ms (r=150) | — | 6.868 / 6.839 | bilgi |
| [bilgi] 1.5 m/s Adam ref @meas vs +SU-average (0.23 ms) yok — en yakın: Adam-6/Adam-8 etkin | — | 6.151 / 6.139 | bilgi |
| [bilgi] 10 km/h CD-8 etkin @2.54 ms (numba_incr) / @3.23 ms (r=150) | — | 6.763 / 6.689 | bilgi |
| [bilgi] 10 km/h Adam ref @meas vs +SU-average (0.23 ms) yok — en yakın: Adam-6/Adam-8 etkin | — | 5.833 / 5.651 | bilgi |
| s4_s2.json lat = arms.json lat_meas (max |fark|) | 0 | 0 | OK |
| tutarlılık: fresh|1.5 m/s = arms.json @meas (max |fark|, 2 seed × 24 kol) | 0 | 0 | OK |
| tutarlılık: fresh|10 km/h = arms.json @meas (max |fark|, 2 seed × 24 kol) | 0 | 0 | OK |
| S4/S2 fresh 3 km/h L*, CD, en iyi kol | Adam-12/CD-1/Adam-12 | Adam-12/CD-1/Adam-12 | OK |
| S4/S2 fresh 3 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+13.300, +6.372, -0.945, +14.800, -0.234, +6.372] | [+13.258, +6.372, -0.945, +14.823, -0.234, +6.372] | OK |
| S4/S2 fresh 3 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-1.034, -0.862] | [-1.033, -0.857] | OK |
| S4/S2 fresh 3 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-0.324, -0.143] | [-0.323, -0.146] | OK |
| S4/S2 fresh 3 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-1.034, -0.862, -0.324, -0.143] | [-1.034, -0.862, -0.324, -0.143] | OK |
| [bilgi] S4/S2 fresh 3 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-12; 4.624; 5.278 | bilgi |
| S4/S2 fresh 1.5 m/s L*, CD, en iyi kol | Adam-6/CD-2/Adam-6 | Adam-6/CD-2/Adam-6 | OK |
| S4/S2 fresh 1.5 m/s L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+6.600, +6.151, -0.912, +14.800, -0.310, +6.151] | [+6.629, +6.151, -0.912, +14.827, -0.310, +6.151] | OK |
| S4/S2 fresh 1.5 m/s GA L48−L* (bağımsız bootstrap, tol 0.015) | [-1.003, -0.823] | [-1.002, -0.822] | OK |
| S4/S2 fresh 1.5 m/s GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-0.411, -0.215] | [-0.412, -0.212] | OK |
| S4/S2 fresh 1.5 m/s GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-1.003, -0.823, -0.411, -0.215] | [-1.003, -0.823, -0.411, -0.215] | OK |
| [bilgi] S4/S2 fresh 1.5 m/s seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-6; 4.624; 5.278 | bilgi |
| S4/S2 fresh 10 km/h L*, CD, en iyi kol | Adam-4/CD-2/Adam-4 | Adam-4/CD-2/Adam-4 | OK |
| S4/S2 fresh 10 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+4.500, +5.913, -0.797, +13.500, -0.303, +5.913] | [+4.455, +5.913, -0.797, +13.476, -0.303, +5.913] | OK |
| S4/S2 fresh 10 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-0.893, -0.704] | [-0.890, -0.702] | OK |
| S4/S2 fresh 10 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-0.403, -0.204] | [-0.399, -0.200] | OK |
| S4/S2 fresh 10 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-0.893, -0.704, -0.403, -0.204] | [-0.893, -0.704, -0.403, -0.204] | OK |
| [bilgi] S4/S2 fresh 10 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-4; 4.623; 5.275 | bilgi |
| S4/S2 joint 3 km/h L*, CD, en iyi kol | Adam-1/CD-1/Adam-1 | Adam-1/CD-1/Adam-1 | OK |
| S4/S2 joint 3 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+1.200, +4.612, -4.316, +93.600, -4.202, +4.612] | [+1.154, +4.612, -4.316, +93.585, -4.202, +4.612] | OK |
| S4/S2 joint 3 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-4.501, -4.124] | [-4.508, -4.124] | OK |
| S4/S2 joint 3 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-4.399, -4.010] | [-4.395, -4.005] | OK |
| S4/S2 joint 3 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-4.501, -4.124, -4.399, -4.010] | [-4.501, -4.124, -4.399, -4.010] | OK |
| [bilgi] S4/S2 joint 3 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-1; 4.569; 4.461 | bilgi |
| S4/S2 joint 1.5 m/s L*, CD, en iyi kol | Adam-1/CD-1/SU-average | Adam-1/CD-1/SU-average | OK |
| S4/S2 joint 1.5 m/s L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+1.200, +4.026, -3.797, +94.300, -3.665, +4.472] | [+1.154, +4.026, -3.797, +94.330, -3.665, +4.472] | OK |
| S4/S2 joint 1.5 m/s GA L48−L* (bağımsız bootstrap, tol 0.015) | [-3.988, -3.621] | [-3.976, -3.619] | OK |
| S4/S2 joint 1.5 m/s GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-3.843, -3.479] | [-3.847, -3.490] | OK |
| S4/S2 joint 1.5 m/s GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-3.988, -3.621, -3.843, -3.479] | [-3.988, -3.621, -3.843, -3.479] | OK |
| [bilgi] S4/S2 joint 1.5 m/s seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-1; 4.472; 3.872 | bilgi |
| S4/S2 joint 10 km/h L*, CD, en iyi kol | Adam-1/CD-1/SU-average | Adam-1/CD-1/SU-average | OK |
| S4/S2 joint 10 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+1.200, +3.215, -3.029, +94.200, -2.884, +4.263] | [+1.154, +3.215, -3.029, +94.197, -2.884, +4.263] | OK |
| S4/S2 joint 10 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-3.195, -2.847] | [-3.208, -2.850] | OK |
| S4/S2 joint 10 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-3.050, -2.724] | [-3.042, -2.725] | OK |
| S4/S2 joint 10 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-3.195, -2.847, -3.050, -2.724] | [-3.195, -2.847, -3.050, -2.724] | OK |
| [bilgi] S4/S2 joint 10 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-1; 4.263; 3.054 | bilgi |
| S4/S2 clarke 3 km/h L*, CD, en iyi kol | Adam-8/CD-1/Adam-8 | Adam-8/CD-1/Adam-8 | OK |
| S4/S2 clarke 3 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+8.800, +6.219, -2.012, +32.400, -0.765, +6.219] | [+8.804, +6.219, -2.012, +32.356, -0.765, +6.219] | OK |
| S4/S2 clarke 3 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-2.111, -1.911] | [-2.114, -1.914] | OK |
| S4/S2 clarke 3 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-0.856, -0.680] | [-0.855, -0.675] | OK |
| S4/S2 clarke 3 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-2.111, -1.911, -0.856, -0.680] | [-2.111, -1.911, -0.856, -0.680] | OK |
| [bilgi] S4/S2 clarke 3 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-8; 4.624; 5.271 | bilgi |
| S4/S2 clarke 1.5 m/s L*, CD, en iyi kol | Adam-4/CD-1/Adam-5 | Adam-4/CD-1/Adam-5 | OK |
| S4/S2 clarke 1.5 m/s L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+4.500, +5.962, -1.688, +28.300, -0.944, +5.960] | [+4.455, +5.962, -1.688, +28.318, -0.944, +5.960] | OK |
| S4/S2 clarke 1.5 m/s GA L48−L* (bağımsız bootstrap, tol 0.015) | [-1.783, -1.589] | [-1.782, -1.591] | OK |
| S4/S2 clarke 1.5 m/s GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-1.040, -0.846] | [-1.039, -0.851] | OK |
| S4/S2 clarke 1.5 m/s GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-1.783, -1.589, -1.040, -0.846] | [-1.783, -1.589, -1.040, -0.846] | OK |
| [bilgi] S4/S2 clarke 1.5 m/s seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-5; 4.623; 5.274 | bilgi |
| S4/S2 clarke 10 km/h L*, CD, en iyi kol | Adam-3/CD-1/Adam-3 | Adam-3/CD-1/Adam-3 | OK |
| S4/S2 clarke 10 km/h L* gecikme, L* etkin, L48−L*, kayıp %, CD−SBO, en iyi etkin | [+3.400, +5.726, -1.544, +27.000, -1.024, +5.726] | [+3.368, +5.726, -1.544, +26.967, -1.024, +5.726] | OK |
| S4/S2 clarke 10 km/h GA L48−L* (bağımsız bootstrap, tol 0.015) | [-1.637, -1.454] | [-1.634, -1.452] | OK |
| S4/S2 clarke 10 km/h GA CD−SBO (bağımsız bootstrap, tol 0.015) | [-1.112, -0.934] | [-1.118, -0.930] | OK |
| S4/S2 clarke 10 km/h GA L48−L* ve CD−SBO, common.boot akışının birebir kopyası (tohum 0) = summary.json | [-1.637, -1.454, -1.112, -0.934] | [-1.637, -1.454, -1.112, -0.934] | OK |
| [bilgi] S4/S2 clarke 10 km/h seed-12 L seçimi; SU-average etkin; SU-best-of etkin | — | Adam-3; 4.626; 5.260 | bilgi |
| karar S4_H1 | TUTTU | TUTTU | OK |
| karar S4_H2 | TUTTU | TUTTU | OK |
| karar S2_H1 | TUTTU | TUTTU | OK |
| karar S2_H2 | TUTTU | TUTTU | OK |
| yorum S4: τ=0 değeri 5.412 = t0 Adam-1 seed 11 (arms.json; iki koşul τ=0'da tanım gereği aynı) | 5.412 | 5.412 | OK |
| yorum S4: 1.15 ms'de ~%25 kayıp (joint Adam-1 / fresh Adam-1, 1.5 m/s) | 25 | 25.58 | OK |
| yorum S4: joint Adam-1 gecikmesi 1.15 ms | 1.15 | 1.154 | OK |
| yorum S4: '10 ms'de hız 1.07' ve 'görece değişim %0.5 / %38' | 1.07; %0.5; %38 | ÜRETİLEMEDİ (s4_s2.json'da 10 ms noktası yok; en yakın kol Adam-10 @ 11.03 ms joint 1.5 m/s = 1.002; kanal değişimi ham veride yok) | ÜRETİLEMEDİ |
| yorum S2: L* gecikmeleri 3.4–8.8 ms | [+3.400, +8.800] | [+3.368, +8.804] | OK |
| yorum S2: Clarke kayıp %27–32 | [+27.000, +32.000] | [+26.967, +32.356] | OK |
| yorum S2: taze kayıp %13.5–14.8 | [+13.500, +14.800] | [+13.476, +14.827] | OK |
| yorum S4: 1.5 m/s ve 10 km/h'de en iyi kol SU-average | SU-average/SU-average | SU-average/SU-average | OK |
| J0 (trapez) − J0 (seri), max |fark|, x ≤ 5 | 0 | 2.758e-14 | OK |
