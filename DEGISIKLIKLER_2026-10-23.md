# Değişiklikler — 23 Ekim 2026

Satır satır kod incelemesi ve iki yeni deney. Aşağıda **davranışı değiştiren**
ile **yalnızca belgeyi düzelten** ayrı tutulmuştur, çünkü ikisinin tez
açısından sonucu farklı: ilki sayıları oynatır, ikincisi yazdığınız cümleyi
değiştirir.

---

## 1. Davranışı değiştiren (sayılar oynar)

### `baselines.no_ris` — ön kodlayıcı tutarsızlığı giderildi

`S.precode(hd, pt, precoder)` çağrısı `noise_var` geçirmiyordu, yani `zf`'in
argümansız varsayılanına düşüyordu; diğer **tüm** temel çizgiler `_rate` →
`S.rates` yolundan geçip MMSE regülatörünü alıyor. Taban, karşısında
tablolandığı satırlardan farklı bir ön kodlayıcıyla ölçülmüş oluyordu.

| | min hız |
|---|---|
| eski çağrı | 1.1339 |
| tutarlı (MMSE) | **1.0224** |
| tutarsızlık | **+%10.91** |

Hatanın yönü sizin aleyhinize değildi — fazla yüksek bir taban RIS kazancını
küçük gösterir. Bu düzeltmeden önce hesaplanmış "kazancın kaynağı"
rakamlarında pano-yok → rastgele-faz adımı 2.73× yerine **3.03×** olmalı.
`audit_claims.py` bu değeri sabitlemediği için kırılan iddia yok.

### `system.zf` — ölü hesap kaldırıldı (sayısal olarak nötr)

`p_sig` varsayılan yolda hesaplanıp atılıyordu. Artık yalnızca kullanan
dallarda hesaplanıyor. **Bit-bit aynı sonuç** verdiği doğrulandı
(1200 senaryoda 3.5549 / 3.6330, değişmedi) ve `verify_mumiso_system.py`
geçiyor.

---

## 2. Yalnızca belge — ama biri tezin cümlesini değiştiriyor

### `unrolled.py` — ÇÜRÜTÜLMÜŞ açıklama kaldırıldı (en önemli)

Modül başlığı şunu söylüyordu: *"The cause is multiplicity, not capacity.
Many phase configurations are near-optimal and which one an optimiser
reaches is arbitrary, so any single target is noise."* **Bu yanlış.**
Bağımsız denetim tek satırlık testle çürüttü:

| | cos uyuşması |
|---|---|
| aynı senaryo, iki farklı başlangıç | +0.58 / +0.81 / +0.57 |
| farklı senaryolar | +0.005 / +0.009 / −0.003 |

İki büyüklük mertebesi: hedef girdi tarafından **belirleniyor**, keyfi değil.
Ayrıca gerçek etiket gürültüsü olsaydı yeterli kapasiteli bir model eğitim
hatasını ezberleyerek sıfıra indirirdi; gözlenen imza (eğitim 0.896'da
takılı, doğrulama 0.925'te düz, gözetimli model çapanın **altında**: 3.4064
vs 3.4350) yetersiz uyum imzası.

Doğru ifade: optimal kaydırma kanalın neredeyse **deterministik** ama
**düzgün olmayan** bir fonksiyonu, ve bu öznitelik temsili onu ifade
edemiyor. Negatif sonuç ayakta, mekanizması değişti.

Bayat sayılar da güncellendi: oracle 5.07 → **6.1619**, çapa 1.03 →
**3.4350**, ve komşuluk testinin sırası **tersine döndü** (+0.0070/+0.0018
yerine +0.0047/+0.0089 — ikisi de sıfırdan ayırt edilemez).

### `features.py` ile ilgili yeni bulgu (kod değişmedi, belgelendi)

Normalizasyon `F`, `G`, `hd`'yi **ayrı ayrı** senaryo ölçeğine bölüyor ve
bu, RIS kaskadının doğrudan yola göre gücünü siliyor:

| | gerçek | ağın gördüğü |
|---|---|---|
| RIS/doğrudan güç oranı yayılımı | **9.4 milyon kat** | **1.000 kat** |
| gerçek ile görünen oranın korelasyonu | — | **+0.031** |

Ağ, kaskadın baskın olduğu senaryoyu doğrudan yolun baskın olduğundan
ayırt edemiyor. **Ölçülen** şey bilginin yok olduğu; **hipotez** olan şey
eklenince stall'ın düzeleceği. Test: `log10(RIS/doğrudan)`'ı kanal olarak
ekleyip üç mimariyi yeniden eğitmek.

### `models.py` — doğrudan çelişki giderildi

Modül başlığı "son katman **sıfırla başlatılır**, eğitim tam çapada başlar"
diyordu; kod `weight.mul_(0.01)` yapıyor ve neden sıfırlanmadığını
açıklıyor (sıfırlamak ilk adımda gradyanı 22 tensörden 2'sine ulaştırıyor).
Ayrıca kalıntı bölümünün sayıları bayat ve biri kendi içinde tutarsızdı:
"1.15'te takıldı, su_average'ın 1.27'sini kıl payı geçti" — 1.15 < 1.27.

### `unrolled.py` — `×0.01` ölçeklemesi ölü kod

`_delta` `atan2(y₁, y₀)` ile bitiyor ve atan2 ölçekten bağımsız:
`atan2(0.01·y)` ile `atan2(y)` arasında 2.4e-07 fark. Yani ölçekleme
**hiçbir şey yapmıyor**. Başlangıçta `_delta` ortalama 1.4243 rad (81.6°)
üretiyor, 0.5 adım boyuyla her adımda ~41° dönüş — `models.py`'nin iddia
ettiği 0.6°'nin ~70 katı. Sonuçları bozmuyor; niyeti belgeleyip yerine
getirmeyen ölü kod olarak işaretlendi.

### `channel.py` — üç düzeltme

**(a) Anten ekseni iddiası yanlıştı.** Başlık "her iki yönde korelasyonlu
açıklık, anten korelasyonu 0.77, etkin rank 2.32/4" diyordu. Yeniden ölçüm:

| konfigürasyon | eleman ekseni | anten ekseni | anten etkin rank |
|---|---|---|---|
| T=4, 600 örnek | 0.620 | **0.234** | **3.71 / 4** |
| T=8, 1500 örnek | 0.639 | **0.204** | **7.26 / 8** |

Anten ekseni LoS'ta 0.818, NLoS'ta **0.130** — yani var olan korelasyonu
neredeyse tamamen LoS terimi taşıyor. Eski sayılar eksen karıştıran bir
dilimlemeden geliyordu (`F` `[S,N,T]` olduğu için anten satırları
`F.reshape(-1,T)`, eleman satırları `F.transpose(0,2,1).reshape(-1,N)`).

**(b) Küme kazançları anten ekseninde paylaşılmıyor**, oysa başlık
paylaşıldığını iddia ediyordu. Ebeveyn `_ris_link` `gains = _crandn(d1.shape)`
çağırıyor ve BS–RIS için `d1` şekli `[S,T,L]`. Fizikçe her saçıcının tek
yansıma katsayısı vardır. Bedeli ölçüldü (akış korunarak, aynı senaryolar):

| | mevcut | fiziksel | fark |
|---|---|---|---|
| NLoS anten korelasyonu | 0.095 | 0.279 | 2.9× |
| çapa (su_average) | 3.5549 | 2.4180 | **−%31.98** |
| PGA | 6.2147 | 5.7081 | **−%8.15** |

Hatanın yönü **aleyhinize**: fazla anten çeşitliliği ZF'yi kolaylaştırıyor,
yani hızlar iyimser. Ama beklenmedik bir yan etki var — çapa PGA'dan çok
daha fazla düştüğü için **optimizasyonun değeri artıyor**: 1.75× → **2.36×**.
Mevcut model sizin katkınızı olduğundan küçük gösteriyor. Kod
değiştirilmedi; karar sizin.

**(c) Veri seti prefix-kararlı değil.** `generate(1000)` ≠
`generate(2000)[:1000]` ve `chunk` de veriyi değiştiriyor (dağılımlar aynı,
çekilişler farklı). Farklı `--samples` ile alınmış iki sayı aynı tabloya
konamaz. Belgelendirildi.

**(d) `effective_rank` uyarısı eklendi**: örnek sayısına bağlı (%32 yayılım)
ve tekdüze değil (250→1000 ters yönde). `n` belirtilmeden alıntılanamaz.

### `csi.py` — hata ölçeğinin yığına bağlılığı not edildi

`_noisy` ölçeği tüm tensörün ortalamasından alıyor, yani bir senaryonun
etkin hata seviyesi kaç senaryoyla birlikte geçirildiğine bağlı.
Karşılaştırılabilirlik uyarısı, doğruluk hatası değil.

### `baselines.su_best_of` — bayat sayılar güncellendi

"+%48.0 (1.1344 → 1.6791)" ve "1.112 → 3.265" hatalı ön kodlayıcı
döneminden. Yeniden ölçüm: **3.5549 → 4.2151, +%18.6**. Bulgu ayakta,
eski boyutunun üçte biri.

---

## 3. Yeni betikler

### `scripts/mumiso_equal_step.py` — eşit adım bütçesi

Her bütçede klasik kolun **adım boyu × objektif** ızgarası doğrulamada
seçiliyor, test kümesinde raporlanıyor; ayrıca senaryo başına **oracle**
üst sınırı. Öğrenilen model her L için **ayrı eğitiliyor** (8 adıma eğitilip
L'de kesilmiyor). İki düzeltme ters yöne çekiyor, yani deney kurgulanmış
değil.

Sonuç (çapa 3.5386, `su_best_of` 4.2371):

| L | öğrenilen | ayarlanmış Adam | oran | eşleşt. fark − 2 s.e. | kazanma oranı |
|---|---|---|---|---|---|
| 1 | 4.4599 | 4.3810 | 1.018 | +0.0608 | %74.8 |
| 2 | 4.8792 | 4.6927 | 1.040 | +0.1602 | %83.2 |
| 4 | 5.2855 | 5.0253 | **1.052** | +0.2279 | %83.7 |
| 8 | 5.5932 | 5.3800 | 1.040 | +0.1840 | %83.2 |
| 16 | 5.8003 | 5.7389 | 1.011 | +0.0393 | %68.3 |

Öğrenilen kural **her bütçede** kazanıyor. Izgara her L'de gerçek bir iç
tepe veriyor (0.5 < 0.75 > 1.0); yumuşak/sert objektif farkı 0.008–0.018,
yani sonucu belirlemiyor.

### `scripts/mumiso_latency_parity.py` — eşit MİLİSANİYE

Eşit adım, eşit gecikme **değil**. Ölçüm: bir öğrenilen adım bir Adam
adımının **2.5–3.3 katı** (ortalama ~3×), çünkü her adımda `rates` iki kez
ve CNN+LSTM gövdesi K kez çalışıyor.

Baskınlık testi — interpolasyon yok, yalnızca ölçülmüş noktalar.

> **27 EKİM DÜZELTMESİ.** Bu bölümün ilk sürümü "beş noktadan dördü
> baskınlanmış, L=4 cephede" diyordu. **L=4 de baskınlanmış.** İlk ölçüm
> eğitim koşarken alınmış ve Adam'ın zamanlamalarını şişirmiş: Adam L=8
> 29.70 ms olarak kaydedilmiş, boş makinede 17.48 ms. 23 Ekim'de "%65
> zamanlama gürültüsü" diye not ettiğim şey gürültü değil **CPU
> çekişmesiydi** — ve yönü öğrenilen modelin lehineydi, yani kendi
> uyarımı yanlış teşhis etmişim. Aşağıdaki tablo boş makinede (yük 0.06)
> beş bağımsız turda yeniden ölçülmüş hâlidir
> (`results/mumiso_latency_repeat.json`).

| öğrenilen L | gecikme | hız | baskınlayan Adam | 5 turun kaçında |
|---|---|---|---|---|
| 1 | 6.71 ms | 4.4599 | L=2: 4.48 ms, 4.6927 | **5/5** |
| 2 | 14.59 ms | 4.8792 | L=4: 9.30 ms, 5.0253 | **5/5** |
| 4 | 25.79 ms | 5.2855 | L=8: 17.48 ms, 5.3800 | **5/5** |
| 8 | 52.34 ms | 5.5932 | L=16: 36.62 ms, 5.7389 | **5/5** |
| 16 | 99.15 ms | 5.8003 | L=32: 76.57 ms, 6.0132 | **5/5** |

**Beş noktanın beşi de kesin baskınlanmış, beş turun beşinde.** Öğrenilen
kuralın gecikme ekseninde cephede hiçbir noktası yok. Baskınlayan Adam
ayarı her satırda hem daha hızlı hem daha yüksek hızlı.

Boş makinede turlar arası oynama 1.06×–1.41×, yani zamanlamalar aslında
yeterince kararlı; hükmü bozan şey gürültü değil kirlilikti. Adım maliyeti
oranı da daraldı: tutarlı biçimde **~2.7×** (L=1'de 6.71/2.54, L=16'da
99.15/36.62).

Betiğin eski hükmü doğrusal interpolasyona dayanıyordu; hız–gecikme eğrisi
içbükey olduğu için interpolasyon gerçeğin altında kalır ve sapma öğrenilen
modelin lehinedir. Betik artık **baskınlık** hesaplıyor.

**Bulgu:** adım başına kazanıyor (%1.1–5.2), milisaniye başına **her yerde**
kaybediyor. İyileştirme adımın maliyetinden (~2.7×) küçük. Bu,
`mumiso_frontier.py`'nin düzeltme öncesi hükmünü onaylıyor.

**Ders:** gecikme ölçümü yük altında alınamaz, ve kirlilik tarafsız değil —
hangi kolu daha çok yavaşlattığına göre hükmü çevirebilir.
`mumiso_budget_fraction.py` meşgul makinede raporlamayı bu yüzden
reddediyor; `mumiso_latency_parity.py` artık yükü ölçüp uyarıyor.

### `scripts/anchor_same_split.py`

Çapayı modellerin puanlandığı **tam** test bölmesinde ölçer. Bulgu 1'in her
oranının paydası bu.

---

## 4. `audit_claims.py` — 11 yeni iddia

Bulgu 1 ve 2'nin kayıtlı sonuçlarını raporun söylediklerine sabitler.
41/41 geçiyor. **Gerçekten patladığı doğrulandı**: tek geçişli modellere
açılmış modelin sayısı yazıldığında yedi iddia başarısız oluyor — bu
projede bir kez fiilen yaşanmış hatanın tam kendisi.

Bilinen boşluk betikte yazılı: modellerin kendi test bölmesindeki çapa
yeniden ölçülmüyor, JSON'dan okunuyor.

---

## 5. Karar sizin olan üç şey

Hiçbiri yapılmadı, çünkü üçü de paketteki tüm sayıları oynatır.

1. **Ön kodlayıcı varsayılanını `eps_abs=0` yapmak.** Kusursuz CSI'da
   %2.20 kazandırır, en zor %10'luk dilimde %4.95. Ama MMSE kusurlu CSI
   altında karşılığını veriyor (−20 dB'de 1.314 vs 1.310), ve varsayılanı
   değiştirmek her sayıyı oynatır.
2. **Kazançları anten ekseninde paylaştırmak.** Fizikçe doğru. Hızları
   düşürür (çapa −%32, PGA −%8) ama optimizasyonun değerini 1.75×'ten
   2.36×'e çıkarır. Ebeveyn sınıfta düzgün implementasyon + kendi
   doğrulama betiği gerekir.
3. **`unrolled.py`'de başlangıcı gerçekten küçültmek** (`step_init` ya da
   kafaya öğrenilebilir genlik). Her açılmış modeli yeniden eğitmek gerekir.

---

# Ek — 27 Ekim

## Temsil hipotezi: kuruldu, test edildi, REDDEDİLDİ

`features.py`'ye iki opsiyonel kanal eklendi (`link_ratio=True`, varsayılan
**kapalı**): normalizasyonun sildiği ölçeklerin logları.

    C-2   log10(sG * sF / sH)        kaskad / doğrudan oranı
    C-1   log10(sG * sF) + 8         mutlak kaskad ölçeği

Bilgi gerçekten geri geldi: gerçek log güç oranıyla korelasyon
**+0.031 → +1.0000**.

Aynı kanal çekilişi (temel çizgiler birebir aynı: random 2.9767,
su_average 3.4154, su_best_of 4.0461, cd 5.7945, pga 6.0783), aynı epok
sayısı, tek fark iki kanal:

| Mimari | Oran kanalı YOK | Oran kanalı VAR | Değişim |
|---|---|---|---|
| concat | 3.5368 | 3.4770 | −%1.69 |
| deepsets | 3.5367 | 3.4233 | **−%3.21** |
| exchange | 3.5260 | 3.4459 | −%2.27 |

**Üçü de kötüleşti.** Düşüş iki modelde kendi epok-arası gürültüsünün
dışında (deepsets gürültü %0.29, exchange %0.13). Yani eksik bilgi,
stall'ın sebebi değildi.

Bu, Bulgu 1'i **güçlendiriyor**: jürinin en doğal itirazı ("daha iyi
öznitelik denediniz mi?") artık ölçümle kapalı.

### Geriye dönük uyumluluk

`link_ratio` varsayılan `False`. Doğrulandı: eski 37 kanal **bit-bit aynı**
(fark 0.000e+00), 22 ağırlık dosyası yükleniyor, 41 denetim iddiası
geçiyor. `MuMisoNet` ve `UnrolledMuMiso` bayrağı alıyor; `mumiso_run.py`
`--link-ratio` ile çağrılıyor.

## Gecikme hükmü düzeltildi

Yukarıdaki gecikme bölümüne bakın: 23 Ekim'deki "L=4 cephede" satırı
yanlıştı, CPU çekişmesiyle şişmiş bir zamanlamadan kaynaklanıyordu.
Boş makinede beş turda **beş noktanın beşi de baskınlanmış**.

## Yeni dosya

`TEZ_YAZIM_REFERANSI.md` — teze atıf yapılacak her sayı, bölüm bölüm,
kaynak dosyasıyla birlikte. `results/*.json` içinden **üretildi**, elle
yazılmadı.

## 27 Ekim — ikinci double check: "17 kat" yanlıştı

Bölüm 5'in **yük taşıyan** varsayımı (hüzme taze, faz eskimiş) uzun süre
"17 kat (4.718 / 0.279)" diye alıntılandı. O ölçüm betiğe yazılmamıştı.
`scripts/mumiso_beam_staleness.py` ile ölçüldüğünde:

| Faz seçimi | Taze hüzme | Eskimiş hüzme | Oran |
|---|---|---|---|
| su_average | 3.5862 | 0.3060 | **11.7×** |
| su_best_of | 3.9243 | 0.3052 | **12.9×** |
| adam8 | 4.3584 | 0.3066 | **14.2×** |

Hiçbir faz seçimi 17 kat vermiyor; eskimiş değer her üçünde ~0.305, 0.279
değil. **Nitel iddia sağlam** (bir büyüklük mertebesi) ama sayı yanlıştı.
Bölüm 5b taslağı, yazım referansı ve bu kayıt düzeltildi.

### Betiksiz kalan ölçümler betiğe taşındı

Bu projenin kendi kuralı: *sonuç taşıyan ve arkasında betik olmayan bir
sayı, ölçüm değildir.* Denetimde dört sayının betiği olmadığı görüldü.
Yedi yeni betik:

| Betik | Neyi üretiyor |
|---|---|
| `mumiso_beam_staleness.py` | Taze/eskimiş hüzme oranı (yukarıdaki) |
| `mumiso_gain_source.py` | Kazancın kaynağı tablosu |
| `mumiso_gain_sharing.py` | Anten ekseninde kazanç paylaşımının bedeli |
| `mumiso_antenna_corr.py` | Anten/eleman ekseni korelasyonu |
| `mumiso_precoder_cost.py` | Ön kodlayıcı varsayılanının maliyeti |
| `mumiso_step_cost.py` | Adım başına gecikme |
| `mumiso_latency_repeat.py` | Beş turluk gecikme tekrarı |
| `verify_batch_dependence.py` | Prefix kararsızlığı gösterimi |
| `make_writing_reference.py` | `TEZ_YAZIM_REFERANSI.md`'yi üretir |

Kazancın kaynağı tablosu birebir yeniden üretildi: no_ris 1.0224,
random 3.1002, su_average 3.5549, su_best_of 4.2151, pga 6.2147,
random/pga = 0.50.

---

## 30 Ekim 2026 — kod devri

### Yeni dosyalar

- `scripts/dump_source.py` ve urettigi `KOD_SON_HALI.md`: 67 dosyanin
  tam metni, her birinin satir sayisi ve sha256 ozetiyle. Elle
  kopyalanmiyor, uretiliyor -- bu projede elle yazilan her seyin
  eskimesi gibi elle kopyalanan kaynak da eskir.
- `CLAUDE_CODE_PROMPT.md`: Claude Code'a verilecek acilis istemi.
  Gorev kuyrugu, kabul olcutleri ve olcum tuzaklari.

### Duzeltme: CLAUDE.md'nin oncelik bolumu celisiyordu

`CLAUDE.md` "su anda olcum degil yazim asamasinda, istenmedikce uzun
kosu baslatma" diyordu. Kullanici 30 Ekim'de sirayi tersine cevirdi:
once bulgular, sonra yazim, yaklasik iki ay. Dosya oldugu gibi
devredilseydi Claude Code siradaki uc deneyi reddederdi. Bolum
yeniden yazildi; olcum fazi 20 Kasim'da kapaniyor.

### BULGU: kazanc paylasimi prototipi ebeveyn sinifa oldugu gibi tasinamaz

`scripts/mumiso_gain_sharing.py` paylasimi `_crandn`'in **seklinden
tahmin ederek** aciyor (`len(shape)==3 and shape[1]==self.T`).
`_crandn` uc yerden cagriliyor ve ikisinin sekli ayni tipte:

| Cagri | Sekil | Paylasim acilmali mi |
|---|---|---|
| `_ris_link` BS->RIS | `(S,T,L)` | evet |
| `_ris_link` UE->RIS | `(S,K,L)` | hayir |
| `_direct_link` | `(S,K,L)` | hayir |

Olcum (tahmin degil), cekilis cekilis:

```
T=8 K=4 : (100,8,6) ACILDI · (100,4,6) kapali · (100,1,8,6) ACILDI
T=4 K=4 : (100,4,6) ACILDI · (100,4,6) ACILDI · (100,1,4,6) ACILDI
```

`T == K` iken paylasim **kullanici eksenine tasiyor**, ki fizikce
sacma. Tezde T=4 konfigurasyonu var (anten korelasyonu tablosunun ilk
satiri), yani tuzak gercekten tetiklenir.

**Yayimlanan sayilar etkilenmedi**: -%31.98 / -%8.15 olcumu
`n_bs_antennas=8, n_users=4` ile alindi, yani sezginin dogru calistigi
rejimde. Ebeveyn sinifa gecirirken sekil tahmini birakilacak; paylasim
cagri yerinde acik bir argumanla belirtilecek.

---

## 2026-11-05 — Bagimsiz denetim: tek kullanicili MISO (CNN–LSTM) sonuclari

Bagimsiz bir denetim ajani 4 Kasim'da eklenen sumiso calismasini inceledi.
Bulgular dogrulandi ve duzeltildi. **Kullaniciya da bildirildi.**

### HATA (kritik): "CNN–LSTM t=0'da bile kapali formun altinda"

Makalede (ozet, giris, VI-G, sonuc), `CNN_LSTM_HAREKETLILIK_SONUCLARI.md`'de ve
kullaniciya verilen raporda boyle yazildi. **Yanlis.**

| Orneklem | CNN − SU-align [%95 GA] |
|---|---|
| 400 (seed 11, makale kumesi) | −0.034 [−0.094, +0.026] — anlamsiz |
| 6000 (seed 11) | **+0.059** [+0.041, +0.077] |
| 6000 (seed 13) | **+0.040** [+0.023, +0.059] |

Dogru ifade: **tek bir Adam adimi** (0.59 ms, CNN 1.12 ms) CNN'i her uc cekiliste
anlamli bicimde baskinliyor (−0.143, −0.090, −0.104). Olumsuz hukum degismedi,
gerekcesi degisti. Kaynak: `scripts/sumiso_mobility_eval.py` (`paired_t0`),
`scripts/sumiso_t0_robustness.py`. Denetim iddiasi `su_cnn_below_closed_form_t0`
kaldirildi; yerine `su_cnn_vs_align_t0_not_significant`,
`su_cnn_above_align_large_draws`, `su_cnn_dominated_by_adam1` (sabotaj testli).

### HATA: "iki hukum de t=0'da gecerli, zamanlamaya bagli degil"

(CNN + CD-1) − CD-1 t=0'da anlamsiz (−0.009 [−0.021, +0.004]). Hukum yalnizca
gecikmeyle (4.26 ms'ye 2.48 ms) gecerli. Cumle kaldirildi.

### HATA: gecikme yuk altinda olculdu

`sumiso_mobility_eval` yuk 0.66'dan, `sumiso_discrete_eval` 0.43 bekleme sonrasi
0.60'tan basladi (kural: < 0.5). Iki betik artik yuk < 0.5 olana kadar bekliyor ve
yeniden olculdu (0.16 ve 0.43'te basladi). `sumiso_csi_eval` yeni gecikmelerle yeniden
kostu. Hukumler degismedi; sayilar guncellendi (orn. CNN 1.18 → 1.12 ms).

### HATA: en iyi yontem test kumesinde seciliyordu

`sumiso_mobility_eval` artik seed 12 cekilisinde seciyor (her T_ov'de CD-1).
T_ov=0'da eski "CD-2" ile CD-1 arasindaki fark 0.003, yani beraberlik.

### Betiksiz iki sayi

- Etiket kalitesi "1.3e-3 icinde": betigi yoktu. `scripts/sumiso_label_check.py`
  yazildi: Adam etiketi senaryo basina en fazla **0.0048** geciyor (300 senaryo).
- MD'deki "CD-10 23 ms'de 12.154": satir ici enterpolasyondu; JSON'daki deger kullaniliyor.

### Asiri iddia ve eksik aciklamalar (duzeltildi)

- "Avantaj cok antenli hareketli durumda tasinmiyor": SISO'da da kapali form kesin
  optimum; makaledeki 2.77° bu ureteçte uretilemedi (14.99°). Metin bunu acikca soyluyor.
- "Ag baglasimi ogrenmiyor" → "kucuk bir kismini yakaliyor" (aradaki farkin %12.8'i).
- Ham girdi (83.84°) duz basla egitildi; 66.45° ile kiyaslanmali.
- Egitim 40 000 degil 28 000 senaryo (6000 secim, 6000 test).
- PyTorch kodundan alinan uc tercih (z-skor, kirpma, en iyi checkpoint) aciklandi.
- Ayrik faz: 1 bitte straight-through modeli (b) ile ayni; baskinlik listeleri
  ortalamaya dayali — referansa not dusuldu.

---

## 2026-11-06 — Bagimsiz denetim: konumdan faz tahmini (yere ozgu oda)

**Kullaniciya bildirildi.** Kullaniciya "modeliniz kosullu olarak ise yariyor" denmisti.
Denetim bunun dayanaksiz oldugunu gosterdi; dogrulandi:

- **Ogrenmeye ozgu degil.** Ayni olcum noktalarindan egitimsiz kNN-20 radyo haritasi
  CNN'i 5 odanin 5'inde geciyor (−0.08 ile −0.22, GA sifiri disliyor;
  `scripts/site_radio_map.py`). CNN yalnizca en yakin komsu etiketini geciyor.
- **"Geometrik" rakip zayifti.** 1. odada konum kullanmayan tek sabit faz (12.69)
  geometrik yonlendirmeyi (12.43) geciyor. "CNN − geometrik +0.42…+0.91" ogrenmenin
  katkisini abartiyor.
- **Pilot varsayimi sonucu belirliyor.** CSI koluna 33 pilot (N+1) yazildi. F oda icin
  sabit ve bilinirse yalnizca g ve h_d kestirilir; ~5–17 pilot yeter. Denetcinin
  olcumunde CNN ustunlugu ~9 pilotta kayboluyor (bu olcumun proje betigi YOK).
- **Mekanizma:** CNN kucuk olcekli sonumlenmeyi izlemiyor; mekansal ortalamali, yavas
  eskiyen bir faz uretiyor. Klasik karsiligi (iki zaman olcekli, istatistiksel CSI)
  karsilastirilmadi.
- **Hata:** `site.py` h_d'yi ebeveynin `_direct_link_g`'si ile uretiyor; bu fonksiyon
  normalizasyonu parca (chunk) uzerinden yapiyor, yani h_d konumun tam belirlenimci
  fonksiyonu degil (%2–39 fark). Site sonuclarinin hepsi bu hatayi tasiyor; duzeltilmedi.
- Ayrica: yorungeler engellerin icinden geciyor; LoS kalibrasyonunun betigi yok;
  golgeleme cekirdegi ebeveynden farkli (Gauss).

Denetim iddialari: `site_knn_beats_cnn_all_sites`, `site_cnn_beats_nn_lookup_all_sites`.
`TEZ_YAZIM_REFERANSI.md` 6.6'ya hukum notu eklendi.

### 2026-11-06 (devam) — duzeltme ve yeniden olcum

- `site.py`: h_d artik konum basina normalize (`Site._direct_link`); parca bagimsizligi
  sinandi (chunk 1 / 777 / 2000 ayni). Yorungeler oda duvarlarindan yansiyor.
- Eski site sonuclari `results/stale_pre_hdfix/` altina tasindi (alintilanmayacak).
  Konum hatasi ve egitim boyutu kosulari yeniden YAPILMADI.
- Yeniden olcum (5 oda): radyo haritasi (egitimsiz, kullanim bicimi) CNN'i statikte
  (−0.07…−0.19) ve pilot maliyeti dahil dinamikte (−0.06…−0.18) her odada geciyor.
  F bilinirse CSI kolu 9 pilotla CNN'i 5 odanin 4'unde geciyor.
- Hukum degismedi: konum tabanli kazanc ogrenmeye ozgu degil.
- Denetim: eski site iddialari kaldirildi, 7 yeni iddia (6'si sabotaj testli).
  Toplam 77 (`--all` 92).

---

## 2026-11-07 — Standart kullanici hizlari ve makalenin tam bagimsiz denetimi

- Danisman elestirisi (1.5 m/s yavas): standartlar dogrulandi (3GPP TR 38.913: 3 km/h;
  ITU-R M.2410-0 §4.11: yaya sinifi 0-10 km/h, ic mekan hareketlilik testi 10 km/h).
  `scripts/mumiso_standard_speeds.py` ile 3 / 5.4 / 10 / 30 km/h olculdu; makaleye
  Tablo IV ve paragraf eklendi. Kaynaklar `HIZ_STANDARTLARI.md`.
- Tam bagimsiz denetim: sayi hatasi yok. Duzeltilenler:
  - Tablo IV'te 1.5 m/s satiri (L*=4, %14.2) ana taramayla (L*=5, %14.0) celisiyordu:
    ince izgarada L=4 ve 5 esit; metinde aciklandi.
  - Ozet: CNN cumlesi "tek kullaniciya tasinmis" diye kapsamlandi; "yavas yontemler"
    "varsayilan butceleriyle" diye nitelendi; periyodik guncellemede "en fazla 8 adim
    yeterli" (govdedeki istatistiksel ifadeyle uyumlu); 191 kelime.
  - "Her hizda gecerli" -> T_ov=0 icin; 30 km/h'de L>=24 guvenilir ufkun otesinde.
  - Denetim kapsami cumlesi guncellendi; YZ beyanina "onceki calismadan/proje
    gunlugunden alintilanan degerler disinda" eklendi.
  - Tablo sirasi atif sirasina getirildi; Tablo VIII basligina T_ov=1.71 notu.
  - Bolum V'e iki 6000 senaryoluk cekilis eklendi; sinirliliklara CD/uzun Adam
    butcelerinin sabit oldugu eklendi.
  - Depodaki PDF yeniden derlendi (eskimisti).

---

## 2026-11-07 — 10 sayfa yeniden yazim ve denetimi

- Kullanici istegi: en fazla 10 sayfa, vurucu giris, sade dil, dogrudan sonuclar.
  Makale 9 sayfaya indi; bes ikincil tablo ve ek cikarildi (ek: `paper_mobility/unused/`).
- 5 m/s (18 km/h) hiz calismasina eklendi (L*=2, L=48 bedeli %8.0, guvenilir ufkun otesinde).
- Bagimsiz denetim (sayi hatasi yok) kisaltmada dusen cekinceleri buldu; geri kondu:
  ozet ve sonucta on kodlayici varsayimi; "gecikme karar verir" yalnizca olculen rejim
  icin; CNN tek kullaniciya tasindi; hiz tablosunda 18 ve 30 km/h icin guvenilir ufuk
  isareti; gecikme eklenince 18/30 km/h'de optimum cozulemiyor; 1.66 ms'nin kaynagi;
  donanim ve maliyet orani cekincesi; CNN kontrol deneyi (14.99° / 2.77°); modelin
  orneklem ici kontrolu ve ±0.08; pilot varsayimlari; N=64 icin yakin alan; Gudmundson
  sapmasi; L=24-64 ayar izgarasi; zamanlama yayilimlari; denetim sayisi 99.

---

## 2026-11-08 — Iki saglamlik deneyi (TWC oncesi)

- `ris_mu/mumiso/mobile.py`: `share_gains` bayragi hareketli ureteçte de calisiyor
  (once yok sayiliyordu). Tam diziler once cekiliyor, sonra ilk anten yayiliyor;
  rastgele akis degismiyor. Varsayilan (False) bit duzeyinde ayni (sinandi; tam
  denetim 105/105).
- Paylasilan kazanclar (`--share_gains`): mutlak hizlar dusuyor (1.5 m/s'de 5.984 →
  5.398) ama L* ayni (4–6; 10 km/h'de 3), L=48 bedeli artiyor (%17.7, %14.2),
  SU-best-of CD ve uzun Adam'i geciyor.
- CD butcesi (`scripts/mumiso_cd_budget.py`): cok kullanicili tek tarama 107 ms
  (~4 T_c); 1–8 taramanin en iyisi (2 tarama, 5.014) SU-best-of'un 0.26 altinda
  [0.17, 0.36]. "Yavas yontemler kaybeder" sabit butcenin urunu degil.
- Makale VI-A ve VI-D'ye eklendi; 9 sayfa (yol haritasi cumlesi cikarildi, iki
  sekil %92 genislik).
