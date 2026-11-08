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

(henüz yok)
