# Ön kayıt: az pilotla (kısmi kanal bilgisiyle) faz tasarımı

**Kayıt tarihi:** 8 Kasım 2026. Bu dosya, hiçbir sonuç görülmeden önce
commit'lendi. Sonradan yapılan her değişiklik bu dosyanın sonundaki
"Sapmalar" bölümüne tarihli olarak yazılır; yukarıdaki metin değiştirilmez.

## Soru

Kanal kestirimi pilot sayısıyla sınırlıyken (32 elemanlı RIS'in yalnızca
bir kısmının kaskad kanalı biliniyorken), öğrenilen faz-farkında bir model,
aynı pilotlarla çalışan **en iyi ayarlı** klasik yöntemi geçer mi?

## Senaryo (sabit)

- Tek kullanıcılı MISO, makalenin tek kullanıcılı seti ile aynı kurgu:
  3GPP InH-Office, 8 antenli BS, 8×4 RIS (N = 32), 20 saçıcı, 3 GHz.
- Veri: `data_sumiso/sumiso_train.npz` (40 000 senaryo, seed 2026),
  `sumiso_train.py` ile aynı 70/15/15 bölme (permütasyon seed 0).
  Eğitim 28 000, doğrulama 6000 (seçim yalnızca burada), test 6000
  (bir kez bakılır).
- Eleman sırası: n = 4·sütun + satır (sütun 0–7, yatay; satır 0–3, dikey).
- **Gözlem modeli (ON/OFF kestirim):** pilot 0 tüm elemanlar kapalı → a
  (doğrudan kanal); pilot i yalnızca i. gözlenen eleman açık → b_i. Gözlem
  gürültüsüz. M gözlenen eleman = M + 1 pilot.
  - **9 pilot (M = 8, birincil):** sütun ∈ {0, 2, 4, 6} × satır ∈ {0, 2}.
  - **17 pilot (M = 16):** dama tahtası, (sütun + satır) çift.
  - **33 pilot (M = 32):** tam kanal.
- Hız, gerçek ve tam kanal üzerinde, BS hüzmesi o kanala eşlenmiş:
  log2(1 + snr·|a + Σ v_n b_n|²). Etiket: tam gerçek kanalın optimumu
  (mevcut koordinat yükselişi etiketleri).

## Kollar

**Öğrenilen** (girdi: gözlenmeyen b_n sıfırlanmış kaskad öznitelikleri +
maske kanalı + a; çıkış: 32 fazın tümü; eğitim reçetesi `sumiso_train.py`
ile aynı: 50 epok, Adam 1e-3, yarılama 15/30/45, batch 256, kırpma 1.0;
checkpoint doğrulama faz RMSE'siyle seçilir; ortak faz, LMMSE
kestirimiyle kapalı formda geri yüklenir):

- **A: yayımlanmış CNN–LSTM** (`head=seq`), yalnızca girdi kanal sayısı
  +1 (maske).
- **B: faz-farkında 2B-CNN–BiLSTM** (yeni model). 2 × [Conv2d 3×3 + BN +
  ReLU] (64 kanal) panelin 8×4 ızgarası üzerinde, Dropout 0.2; eleman
  dizisi üzerinde BiLSTM(64 → 2×64), BiLSTM(128 → 2×32), Dropout 0.3,
  eleman başına Linear(64 → 2) = (sin, cos). Faz-farkında MSE kaybı.
  Gerekçe: panel 2B (1B dizide dikey komşu 4, yatay komşu 1 eleman uzakta)
  ve eksik değer doldurma iki yönlüdür.
- **C: ablasyon.** B'nin aynısı, tek çıkış (doğrudan açı) ve düz MSE kaybı.
  Sin/cos katkısının bu problemde gerekli olup olmadığını sınar.
- Melez kollar: A ve B'nin çıkışı başlangıç alınarak LMMSE kestirimi
  üzerinde s ∈ {1, 2, 3} CD taraması (s doğrulamada seçilir).

Tohumlar: M = 8'de her model için 3 tohum (0, 1, 2); M = 16 ve 32'de
tohum 0. **Birincil karşılaştırma tohum 0 modeliyle yapılır**; diğer
tohumlar sağlamlık için raporlanır.

**Klasik** (hepsi aynı pilotlarla; her yapılandırma doğrulamada seçilir):

1. **Doğrusal ara değer + CD-s:** gözlenmeyen b_n, ızgara üzerinde
   komşu gözlenen elemanlardan karmaşık doğrusal ara değerle (kenarda en
   yakın komşu); s ∈ {0 (kapalı form), 1, 2, 3, 5, 10, 30}.
2. **LMMSE ara değer + CD-s** (en güçlü klasik rakip): gözlenmeyen
   b_n'nin gözlenenler ve a verildiğinde doğrusal MMSE kestirimi; ortalama
   ve 256×256 kovaryans eğitim bölmesinden; s aynı küme. Ayrıca LMMSE +
   Adam-L (L ∈ {1, 2, 4, 8, 16, 32, 64}, adım boyu 10 değerden).
3. **Eleman gruplama** (Zheng & Zhang tarzı): M grup (M = 8: 2×2 blok;
   M = 16: 2 sütunluk 1×2 blok), grup içi elemanlar aynı fazı paylaşır;
   pilot i, i. grubun tüm elemanları açıkken grup toplam kanalını ölçer;
   grup fazları tam CD ile (30 tarama) çözülür.
4. **Tam kanal + CD** (33 pilot): yalnızca hareketlilik ekseninde, pilot
   süresi ödenerek; statik eksende üst sınır.

"En iyi klasik", her pilot sayısında 1–3'ün tüm yapılandırmaları arasından
**doğrulama ortalama hızına göre** seçilen tek yapılandırmadır.

## Başarı ölçütü (birincil, tek)

9 pilotta, test kümesinde (6000 senaryo), statik hızda:

> **B (tohum 0, tek başına) − en iyi klasik** farkının eşleştirilmiş
> bootstrap güven aralığının (2000 örnek) alt sınırı > 0.

İki model (A ve B) sınandığı için güven düzeyi Bonferroni ile **%97.5**
(yüzdelikler 1.25 ve 98.75). A için aynı sınama ayrıca raporlanır.
Ölçüt sağlanırsa "B, 9 pilotta en iyi klasik rakibi geçti" denir;
sağlanmazsa "geçemedi" denir. Her iki sonuç da tezde raporlanır.

## İkincil (yorumlayıcı, ölçüt değil)

- 17 ve 33 pilotta aynı karşılaştırma.
- Melez kollar (B + LMMSE-CD) − en iyi klasik.
- B − A (mimari katkısı), B − C (sin/cos katkısı), tohum yayılımı.
- **Hareketlilik ekseni (tezin ana sorusu):** 1.5 m/s, seçim seed 12,
  rapor seed 11 (400 senaryo); etkin hız, pilot süresi (sembol başına
  71.4 µs, 15 kHz) + ölçülmüş hesaplama gecikmesi sonunda. Gecikmeler
  boş makinede (yük < 0.5), tek iş parçacığı, tek senaryo, medyan;
  mevcut CD-s/Adam-L gecikmeleri `results/sumiso_mobility_eval.json`'dan
  aynı koddan alınır, yeni kollar (LMMSE, ara değer, gruplama, A, B)
  aynı yöntemle ölçülür. Baskınlık (daha hızlı ve daha iyi klasik kol)
  raporlanır.

## Kurallar

- Mimari, kayıp, eğitim reçetesi, pilot desenleri ve rakip kümesi
  yukarıdaki gibi dondurulmuştur. Sonuç kötü çıkarsa yeni model, yeni
  desen ya da yeni ayar **eklenmez**.
- Test kümesine birincil sınama için tek kez bakılır.
- Hata (bug) bulunursa düzeltilir, tüm kollar yeniden koşturulur ve
  "Sapmalar"a yazılır.
- Betikler: `scripts/sumiso_partial_train.py`,
  `scripts/sumiso_partial_eval.py`; sonuçlar `results/sumiso_partial_*.json`.

## Kapsam dışı (bilerek)

Gözlem gürültüsü, öğrenilmiş pilot tasarımı, parametrik (açı tabanlı)
kestirim, çok kullanıcılı durum. Zaman kalırsa gürültü (e2 = 0.03) aynı
kurallarla ikincil olarak eklenebilir; birincil ölçütü etkilemez.

## Sapmalar

**1 (8 Kasım 2026, öğrenilen hiçbir model eğitilmeden önce): klasik kol
güçlendirildi.** Doğrulama kümesinde (1000 senaryo) yapılan kurulum
kontrolü, kaskad kanalın yatayda komşu elemanlar arasında neredeyse
ilişkisiz (|ρ| = 0.05), dikeyde ilişkili (|ρ| = 0.57) olduğunu gösterdi.
Bu durumda önceden kaydedilen 2×2 gruplama, gruplama ailesinin en iyi
üyesi değil. CLAUDE.md'nin "zayıf taban çizgisi" kuralı gereği grup
şekli de doğrulamada seçilen bir ayar yapıldı: M = 8 için {2×2, 1×4
(sütun), 4×1}, M = 16 için {2×1, 1×2}. Bu değişiklik yalnızca klasik
rakibi güçlendirir; öğrenilen modelin aleyhinedir.

**2 (aynı gün, aynı kontrol): LMMSE uydurması** senaryo başına gözlem
normuyla normalize edilmiş örneklerle yapılır (dosyada yazılan yöntem).
Normalize edilmemiş uydurma doğrulamada daha kötüydü (CD-30 sonrası
10.74'e karşı 10.94 b/s/Hz), bu nedenle normalize hali kullanılır.

**3 (8 Kasım 2026, sonuçtan sonra; tasarımı etkilemez): gecikme ölçümü.**
Hareketlilik eksenindeki bütün gecikmeler, `sumiso_mobility_eval.json`'dan
alınmak yerine bu betikte aynı oturumda yeniden ölçüldü. Böylece yeni kollar ve CD/Adam
aynı makine durumunda zamanlandı. Bu makinede CD-1 yaklaşık 2 kat daha hızlı
ölçüldü; iki dosyanın gecikmeleri aynı tabloya konmaz.

## Sonuç (8 Kasım 2026; test kümesine tek bakış)

**Birincil ölçüt SAĞLANMADI.** 9 pilotta B (tohum 0) − en iyi klasik
(doğrulamada seçilen: 1×4 sütun gruplama) = **−1.207 b/s/Hz**, %97.5 GA
[−1.244, −1.172]. A için −1.091 [−1.124, −1.059]. Üç tohumun hepsinde aynı.

- En iyi klasik kol her pilot sayısında **eleman gruplama** (9: 12.110,
  17: 12.595, 33: tam çözüm 12.893). Önceden kaydedilen 2×2 gruplama bile
  (11.698) iki modeli geçiyor. LMMSE ailesinin en iyisi (11.126) A'ya
  (11.019) eşit ya da biraz üstünde.
- **B − A** (2B mimari katkısı): 9 pilotta −0.116 [−0.140, −0.092] (3
  tohumda da negatif), 17 ve 33 pilotta sıfır. Yeni mimari bir şey
  kazandırmadı.
- **B − C** (sin/cos katkısı): 9/17/33 pilotta +0.442 / +0.747 / +0.688,
  hepsinin GA'sı sıfırın üstünde, her tohumda. **Yayımlanmış sin/cos
  gösterimi bu problemde de açıkça gerekli.**
- Melez (B + LMMSE üzerinde CD-3) 9 pilotta 11.120: hâlâ −0.990.
- Hareketlilik (1.5 m/s): her öğrenilen kol, daha hızlı ve daha iyi bir
  klasik kol tarafından baskınlanıyor. En iyisi 33 pilotun tamamını ödeyip
  CD-2 koşturmak (12.708); az pilot bu hızda kazandırmıyor.

Neden (yorum): kaskat kanal yatayda komşu elemanlar arasında neredeyse
ilişkisiz (|ρ| = 0.055), dikeyde ilişkili (0.558)
(`scripts/sumiso_partial_correlation.py`, doğrulama 6000). Tek tek gözlenen
8 eleman, gözlenmeyen 24'ü hakkında az bilgi taşıyor; gruplama ise aynı
pilot sayısıyla 32 elemanın hepsinin enerjisini ölçüyor. Sınır mimaride
değil, **gözlem modelinde**.

Kaynak: `results/sumiso_partial_static.json`,
`results/sumiso_partial_mobility.json`; denetim `partial_*` iddiaları.
