# Ön kayıt — "L nasıl seçilir?" tasarım kuralı (16 Kasım 2026)

**Bu dosya sınama koşularından ÖNCE commit'lenir.** Sınama sonucu ne çıkarsa çıksın aşağıdaki ölçütlere göre raporlanır; ölçütler ve koşul ızgarası sonradan değiştirilmez. Bir değişiklik gerekirse ayrı bir "sapma" bölümüne tarihiyle yazılır.

## 1) Soru

Bir baz istasyonu, RIS fazını Adam ile hesaplarken kaç adım (L) atmalı? Elde şunlar var:
- adım süresi ΔT,
- kullanıcı hızı (Doppler f_d),
- fazın kullanılacağı süre (tutma süresi W).

Makale 2'nin kapalı formu (L* ∝ x^(−2/(γ+2)), x = ΔT·f_d) yalnızca anlık etkin hız (Tanım 1) için kuruldu. Tutma süresinin optimumu büyüttüğü (W = 25/50/100 ms → L ≈ 5 / 6–8 / 16–20) ölçüldü ama açıklanmadı.

## 2) Kural (kalibrasyon verisiyle sabitlenir, sınama verisini görmez)

Kanal eskimesi f_d·t'nin fonksiyonu olarak alınır. Faz t = 0 kanalından hesaplanır, gecikme τ = L·ΔT + T_0 sonra devreye girer ve W süre tutulur.

```
R̂(L; ΔT, f_d, W) = R_floor + (R_0(L) − R_floor) · Ψ̄(f_d·τ, f_d·W)
Ψ̄(a, b)          = (1/b) ∫_0^b ψ(a + s) ds        (b → 0'da ψ(a); W = 0 anlık etkin hız)
L̂               = argmax_L R̂(L; ΔT, f_d, W)       (L ∈ {1,2,3,4,5,6,8,10,12,16,20,24,32,48})
```

**Bileşenler:**
- **R_0(L):** Adam'ın (adım boyu 0.5, SU-average başlangıcı) t = 0'daki min-kullanıcı hızı. Kalibrasyon çekilişinde ölçülür. Hızdan bağımsızdır.
- **R_floor:** Faz ile kanal ilişkisizken beklenen hız, yani eskimiş taban. Kalibrasyon çekilişinde L'ye göre ortalanır.
- **ψ(u):** Normalize eskime eğrisi; u = f_d·t. Kalibrasyon çekilişinde YALNIZCA 1.5 m/s'de ölçülür. Her L için (R(L,t) − R_floor)/(R_0(L) − R_floor) hesaplanır, sonra L'ler üzerinden ortalanıp u'da tabloya alınır (doğrusal interpolasyon; u tablonun ötesinde son değer). Hiçbir parametrik biçim varsayılmaz.
- **T_0:** SU-average başlangıcının süresi (0.30 ms); ΔT, Adam adımının süresi.

Kuralın sınama koşullarındaki tek girdisi (ΔT, f_d, W) üçlüsüdür. R_0, R_floor ve ψ kalibrasyonda sabitlenir.

## 3) Veri

| Rol | Çekiliş | Kullanım |
| --- | --- | --- |
| Kalibrasyon | yaşlanma kurgusu, **seed 12**, 400 senaryo, 1.5 m/s | R_0(L), R_floor, ψ |
| Sınama | yaşlanma kurgusu, **seed 13**, 400 senaryo; bu tezde hiç kullanılmadı | yalnızca aşağıdaki ölçüt |

Kanal modeli `common.Aging` ile aynıdır: 20 saçıcı, ZF, min-kullanıcı hızı, t = 0 ilk ızgara noktası. Sınama çekilişinde "doğru" L*, her koşulda ölçülen eğrinin argmax'ıdır (L kümesi aynı).

## 4) Koşul ızgarası (sınama, 60 koşul)

| Değişken | Değerler | Not |
| --- | --- | --- |
| Hız (km/h) | 3, 5.4, 10, 18, 30 | 1.5 m/s = 5.4 km/h kalibrasyon hızıdır; diğerleri hiç görülmedi |
| ΔT (ms/adım) | 0.33, 1.33, 5.32 | ölçülen 1.33 ms'nin ¼'ü, kendisi ve 4 katı |
| W (ms) | 0 (anlık, Tanım 1), 25, 50, 100 | |

Etkin hız: faz τ = L·ΔT + 0.30 ms'de devreye girer. W > 0 için [τ, τ + W] üzerinde, kolun kendi devreye girme anına hizalı 0.5 ms ızgarada yamuk kuralıyla zaman ortalaması alınır. Her (hız, ΔT, L) için ayrı ızgara kurulur; böylece interpolasyon ve ızgara yanlılığı oluşmaz. W = 0 için τ'daki tam değer kullanılır. Kural da aynı ayrıklaştırmayı kullanır (u ekseninde Δu = f_d·0.5 ms). Pilot ve kestirim hatası yok; ana deney bu ikisini ayrı tutuyor.

## 5) Ölçütler ve hipotezler

Her koşul c için kayıp şöyle tanımlanır:

```
kayıp_c(kural) = 1 − R_test(L̂_c) / R_test(L*_c)        (%; sınama çekilişinde, 400 senaryo ortalaması)
```

**Karşılaştırma kuralları:**
- (a) her zaman L = 48 (yakınsamaya kadar koş);
- (b) her zaman L = 5 (makalenin ana sonucu);
- (c) makalenin kapalı formu: L = round(5 · (x / 0.025)^(−0.675)), W'yi yok sayar.

**Hipotezler (önceden):**
- **H1:** Kuralın kaybının 60 koşul üzerindeki medyanı **≤ %1**, en kötü koşulu **≤ %3**.
- **H2:** Koşul başına eşli kayıp farkında, kural (a) ve (b)'den daha iyi. Ölçüt: senaryolar üzerinde eşli bootstrap (2000, %95), koşullar üzerinden ortalama kayıp farkının GA'sı sıfırın altında.
- **H3:** W > 0 koşullarında kural, (c)'den daha iyi (aynı ölçüt).

**Karar:**
- H1, H2 ve H3 tutarsa kural tezin "pratik kural" katkısı olarak önerilir.
- Herhangi biri tutmazsa, hangi koşulda bozulduğu (hız, ΔT ya da W) raporlanır. Kural düzeltilip aynı sınama verisinde yeniden denenmez; bu ön kaydın ruhuna aykırı olur.

## 5b) Kalibrasyon tanılaması (sınamadan önce kaydedildi, 16 Kasım)

`raw/calibration.json` (seed 12):
- R_floor = 3.883 b/s/Hz, f_d = 15.01 Hz.
- **ψ'nin L'ler arasındaki en büyük yayılımı 0.11.** u = 0.25 / 1 / 5 / 10'da sırasıyla 0.064 / 0.035 / 0.026 / 0.058. Normalize eskime eğrisi L'den tam bağımsız değil; kuralın bilinen bir yaklaşıklığıdır.
- Kuralın kendi çıktısı (sınama verisi görülmeden): 1.5 m/s, ΔT = 1.33 ms için W = 0 / 25 / 50 / 100 ms'de L̂ = 6 / 5 / 8 / 24.
- Kod düzeltmesi: NumPy 2'de `np.trapz` → `np.trapezoid`. Sayısal etkisi yok, ön kayıttan önce yapıldı.

## 6) Keşifsel (hipotez değil, ayrı raporlanır)

- Pilot ücreti (onkodlayici_siralama modeli) ve kestirim hatası (ρ = 30 dB) altında kuralın kaybı.
- 1 ve 2 bit fazda kuralın kaybı.

## 7) Betikler ve sıra

1. `calibrate.py` (seed 12): R_0, R_floor, ψ → `raw/calibration.json`. Kural `rule.py`'de, yalnızca bu dosyayı okur.
2. Bu ön kayıt ve 1. adımın çıktısı commit'lenir.
3. `validate.py` (seed 13): 60 koşulda L*_c, R_test, kural ve karşılaştırma kuralları → `raw/validation.json`. Eşli bootstrap tohumu 0.
4. `make_report.py` → `REPORT.md`. Hipotez kararları bu dosyadaki ölçütlere göre verilir.

**Süre tahmini:**
- Kalibrasyon ~10 dk.
- Sınama: 5 hız × 400 senaryo × 14 L × ince zaman ızgarası, ~30–60 dk. Gecikme ölçümü içermediği için boş makine gerekmez.
