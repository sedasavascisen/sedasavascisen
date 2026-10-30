# MU-MISO Çok Kullanıcılı RIS — Python

Yayınlanan makalenin **üzerine eklenen** çok kullanıcılı katman. Makaleniz,
denklemleri ve sonuçları değişmiyor; bu paket tezin yeni bölümü.

> ## ⚠ ÖN KODLAYICI HATASI — hangi sayıya güveneceğinizi belirler
>
> `zf()`'deki düzenlileştirici **mutlak** bir sabitti (`eps = 1e-9`), ama
> karşılaştırıldığı matrisin ölçeği yol kaybıyla belirleniyor. Ölçüldü: o
> sabit köşegenin %0.34'ü ve **min hızın %55'ine mal oluyordu.** 1e-6
> üstünde "düzenlileştirilmiş ZF" sessizce MRT'ye dönüşüyor. Düzeltildi;
> varsayılan artık MMSE/RZF, `eps = K(σ² + CSI hata gücü)/Pt`, ölçekten
> bağımsız.
>
> **Sonuç:** Bölüm 5d ve 5e düzeltilmiş ön kodlayıcıyla ölçüldü, onlara
> güvenin. Bölüm 4, 5, 5b, 5c ve 6'daki **mutlak** sayılar eski ön
> kodlayıcıdan ve hepsi düşük — yeniden ölçülmeyi bekliyor. Göreli
> sonuçları (hangi yöntem hangisini geçiyor) 5d'de yeniden doğruladım ve
> **ayakta kaldılar**; ama bir tabloyu tezinize almadan önce
> `audit_claims.py` ile yeniden ölçün. Detay Bölüm 11, madde 13.
>
> **Bu Bölüm 4'ün yorumunu da yumuşatıyor:** düzgün bir ön kodlayıcıyla
> çapa/en güçlü oranı 4.1× değil **1.7×**. Tek geçişli ağ hâlâ çapada
> donuyor ama yakalayamadığı başlık payı eskisinin yarısından az.
>
> **Bu sürüm bağımsız bir denetimden geçti.** Benim gerekçelerimi görmeyen
> bir ajan, iddiaları kodu çalıştırarak yeniden türetti, matematiği kendi
> yazdığı testlerle kontrol etti ve zayıf taban çizgisi aradı. Bulduğu beş
> şeyi düzelttim; **biri tez tavsiyemi tersine çevirdi** (Bölüm 4). Neyin
> düzeltildiği Bölüm 11'de, neyin arkasında kayıt olduğu Bölüm 12'de.

---

## 1. Tavsiyem: Python

MATLAB paketini çalıştıramıyorum, bunu çalıştırıyorum. Matematiği
doğrulanmış kod ile *koşmuş* kod arasındaki fark bu oturumda somut oldu:
çalıştırınca tasarımımın temel varsayımının yanlış olduğu çıktı (Bölüm 4),
ve sonra o yanlışa verdiğim açıklamanın da yanlış olduğu (Bölüm 4b).
İkisini de ancak koşturarak bulabilirdim.

Ayrıca: MATLAB'ın özel katman gerektirdiği permütasyona değişmez mimari
burada doğal; `detach()` olduğu için düz-geçiş nicemleyici kırılgan
değil; karmaşık otomatik türev çalıştığı için `mu_rate_dl.m`'deki tamamen
reel aritmetik geçici çözümü ve onunla gelen işaret hatası riski yok;
taban çizgileri toplu çalıştığı için ~100× hızlı — ki dört zayıf taban
çizgisi hatamı ancak onları defalarca koşturabildiğim için yakaladım.

**Karşı taraf:** yayınlanan makaleniz MATLAB. O kod (`duzeltilmis_kodlar`)
olduğu gibi duruyor ve yayınlanan sonucu üretmeye devam ediyor. Danışmanınız
veya jüri MATLAB bekliyorsa söyleyin, o paketi bu bulgulara göre güncellerim.

---

## 2. Kapsam ve sistem modeli

| | Baz istasyonu | Kullanıcı | Optimize edilen |
|---|---|---|---|
| **MU-MISO (bu paket)** | T anten | 1 anten | RIS fazı; ön kodlayıcı **kapalı form** (MRT/ZF) |
| tam MU-MIMO | T anten | N_r anten | RIS fazı **+** ön kodlayıcı birlikte |

Ön kodlayıcı kapalı formda tutuluyor, çünkü o zaman ölçülen her kazanç RIS
fazına atfedilebilir. İkisini birden öğrenirseniz iyi bir sonuç çıktığında
"kazanç hangisinden geldi" sorusuna cevap veremezsiniz.

```
y_k = ( h_d,k^H + g_k^H diag(v) F ) Σ_j w_j s_j + n_k

F  : [B, N, T]    BS  → RIS          v_n = exp(+j θ_n)
G  : [B, K, N]    RIS → kullanıcı k  (g_k^H satır olarak)
hd : [B, K, T]    doğrudan BS → kullanıcı
W  : [B, T, K]    ön kodlayıcı, ‖W‖_F² = Pt

SINR_k = |h_k^H w_k|² / ( Σ_{j≠k} |h_k^H w_j|² + σ² )
```

**İşaret konvansiyonuna dikkat, tezde ikisini birlikte yazacaksınız.**
`G` satırlarında `g_k^H` sakladığı için yansıma `diag(v)` olarak girer,
`diag(v^H)` olarak **değil**. Bu paketin önceki sürümünde dokümantasyon
`diag(v^H)` yazıyordu, kod `diag(v)` hesaplıyordu; denetim elle iki formu
kurup ölçtü — kod `diag(v)` formuna 1.8e-15, `diag(v^H)` formuna 9.7
uzaklıkta. Sonuç değişmiyor (θ ↔ −θ birebir) **ama** Bölüm 7'deki optimal
faz `θ_n = ∠h_d − ∠(g_n f_n)` yalnız `diag(v)` konvansiyonunda sınırın
%100'ünü verir; `diag(v^H)` ile birlikte yazılırsa **%7**'sini verir.
Düzeltildi.

Varsayılan senaryo: **N=32, T=8, K=4.** T>K kasıtlı — T=K'de ZF bütün
serbestlik derecesini harcıyor ve min hız gürültü tabanına iniyor
(ölçülen en güçlü klasik: T=4,K=4'te 4.06; T=8,K=4'te 5.69; T=8,K=6'da 2.70).

---

## 3. Paket

```
ris_mu/mumiso/
  system.py      sistem denklemleri (tek doğruluk kaynağı)
  channel.py     Nt antenli kanal üreteci + tanı
  features.py    ağ girdisi
  models.py      tek geçişli modeller (concat / deepsets / exchange)
  unrolled.py    öğrenilen ön koşullu gradyan yöntemi
  baselines.py   klasik referanslar
  train.py       etiketsiz eğitim döngüsü

scripts/  — doğrulama
  verify_mumiso_system.py      6 matematik kontrolü
  verify_mumiso_channel.py     şekiller, dizi korelasyonu, bağlantı bütçesi
  verify_mumiso_models.py      permütasyon simetrisi, gradyan akışı
  verify_residual.py           artık modun çapada başladığı
  verify_baseline_strength.py  taban çizgisi gerçekten güçlü mü
scripts/  — teşhis
  mumiso_headroom.py           (T,K) seçimi
  diagnose_mumiso_gap.py       boşluk hangi aileden geliyor
  diagnose_learnability.py     **§4'ün belirleyici teşhisi**
  audit_section4_cause.py      **§4b: açıklamanın testi**
scripts/  — deney
  mumiso_run.py                tek geçişli modeller
  mumiso_unrolled.py           açılmış model
  mumiso_frontier.py           gecikme-kalite sınırı
  mumiso_budget_fraction.py    gecikme DAĞILIMI ve bütçe oranı
  mumiso_budget.py             eşit bütçe karşılaştırması
  audit_fair_comparison.py     adım boyu doğrulamada seçilerek
scripts/  — sürekli doğrulama
  audit_claims.py              **her taşıyıcı sayı, makine kontrollü**
```

Mevcut tek antenli kod (`ris_mu/channel.py`, `models.py`, …) **ellenmedi** —
yayınlanan sonuçları o üretiyor. `MuMisoChannel` onu miras alıyor ve yalnız
örnek kurgusunu değiştiriyor; 3GPP TR 38.901 yol kaybı, LoS olasılığı,
Ricean K dağılımı, Gudmundson korele gölgeleme ve Tang iki-atlama kaskadı
aynen yeniden kullanılıyor.

---

## 4. Birinci bulgu: tek geçişli regresyon K>1 için çalışmıyor

Tasarımımın varsayımı: yayınlanan CNN-LSTM tek kullanıcıda kanaldan faza
tek geçişte gidiyor, çok kullanıcıda da aynısını yaparız. **Çalışmıyor.**

**Ölçüm 1 — eğitim çapada donuyor.** 12000 senaryo, 20 epok, artık mod
(yani model çapada *başlıyor* ve onu iyileştirmeye çalışıyor). Çapa
su_average = 1.1431, en güçlü klasik 5.1550:

| mimari | test min | çapa oranı | son 8 epok doğrulama yayılımı |
|---|---|---|---|
| concat | 1.1213 | 0.981 | 1.8e-05 |
| deepsets | 1.1277 | 0.987 | 1.1e-05 |
| exchange | 1.1274 | 0.986 | 3.3e-06 |

Üçü de çapanın **altında** kalıyor ve doğrulama değeri son epoklarda beşinci
ondalıkta sabit — yavaş öğrenme değil, durma. Artefakt:
`results/mumiso_sec4.json`, `results/run_sec4.log`.

Aynı koşu permütasyon simetrisini eğitim sonrası da ölçüyor: concat
**7.0e-03**, deepsets **2.2e-06**, exchange **1.5e-06**. Üç mertebe fark;
Bölüm 6'nın iddiası eğitilmiş modelde de tutuyor.

**Ölçüm 2 — en yakın komşu testi.** Öznitelik uzayında **en benzer** iki
senaryonun gerektirdiği faz kaydırması, **rastgele** iki senaryonunki kadar
ilgisiz:

```
cos(kaydırma farkı), en yakın öznitelik komşusuna : +0.0070
cos(kaydırma farkı), rastgele bir senaryoya       : +0.0018
```

**Ölçüm 3 — gözetimli uyum eğitim kümesinde bile başarısız.** Senaryo başına
oracle kaydırmalar (Adam, 600 adım → 5.07 b/s/Hz), ağ bunlara gözetimli
eğitildi:

| epok | eğitim MSE | doğrulama MSE | doğrulama hızı |
|---|---|---|---|
| 1 | 0.963 | 0.960 | 1.200 |
| 10 | 0.946 | 0.969 | 1.178 |
| 25 | 0.908 | **0.980** | 1.139 |

MSE 1.0 = tahmin hedefle ilgisiz (ikisi de birim vektör; MSE = 1 − E[cos Δ]).
Betik: `scripts/diagnose_learnability.py`.

---

## 4b. Bu bulgunun nedeni — ilk açıklamam yanlıştı

İlk sürümde şunu yazdım: *"bir senaryo için birçok faz yapılandırması
neredeyse optimal, hangisine düşüldüğü keyfi, dolayısıyla hedef girdiye göre
gürültü."* Tek kullanıcılı çalışmadaki gauge probleminin karşılığı diye
sundum.

**Denetim bu açıklamanın hiç yapılmamış tek satırlık testini sordu:** aynı
senaryoyu iki farklı başlangıçtan çöz, cevaplar uyuşuyor mu? 1200 senaryo,
600 Adam adımı, üç başlangıç (`scripts/audit_section4_cause.py`):

| başlangıç çifti | **aynı** senaryo | **farklı** senaryo |
|---|---|---|
| sıfır vs düzgün(−π,π] | **+0.5792** | +0.0053 |
| sıfır vs küçük Gauss | **+0.8149** | +0.0094 |
| düzgün vs küçük Gauss | **+0.5723** | −0.0027 |

Üç başlangıç da aynı hıza çıkıyor (5.029 / 5.043 / 5.025) ama **birbirine
uyuşuyorlar** — aynı senaryoda %58–81, farklı senaryoda %0.5. İki büyüklük
mertebesi. **Hedef girdi tarafından belirleniyor, keyfi değil.** Açıklamam
yanlıştı.

İkinci argüman daha keskin: gerçek etiket gürültüsü altında yeterli
kapasiteli bir model **eğitim** hatasını ezberleyerek sıfıra indirir,
doğrulama 1.0'da kalır. Yukarıdaki tabloda gözlenen şey — eğitim MSE
0.91'de takılı ve hâlâ yavaş düşüyor, doğrulama **yükseliyor** — klasik
**yetersiz uyum / kötü temsil** imzası.

Ayrıca hedefi kanonikleştirmek de kurtarmıyor: yakınlık cezası λ(1−cos Δ)
eklemek en yakın komşu uyumunu yükseltiyor ama **rastgele çift uyumunu
eşit ölçüde** yükseltiyor — ceza bütün kaydırmaları ortak bir ortalamaya
çekiyor, senaryoya bağlı yapı yaratmıyor.

**Doğru ifade:** *optimal kaydırma, kanalın neredeyse deterministik ama
düzgün olmayan bir fonksiyonu; bu öznitelik temsili ve bu ağ onu ifade
edemiyor.* Negatif sonuç ayakta — açıklaması değişti. Tezde bu fark önemli,
çünkü ilk versiyonum jüriye yanlış mekanizma anlatıyordu.

---

## 5. İkinci bulgu: öğrenilen güncelleme kuralı da kazanmıyor

Bölüm 4'ün teknik cevabı: ağ çözümü değil **güncelleme kuralını** öğrensin
(`unrolled.py`). Çalışıyor, ama pratik kazanç vermiyor.

**Çalışıyor.** 8 adımlık açılmış model, çapadan başlayıp test kümesinde
3.265 b/s/Hz'e çıkıyor. Adım adım izi 8. adımda hâlâ tırmanıyor:

```
1.678 → 1.585 → 1.840 → 2.073 → 2.129 → 2.623 → 2.861 → 3.265
```

Öğrendiği adım boyları: `0.746 0.944 0.866 0.691 0.684 0.460 0.338 0.156`
— önce yükseliyor sonra düşüyor, yani bir çizelge öğrenmiş ama **monoton
azalan değil** (ilk sürümde öyle demiştim, yanlıştı).

**Kritik ablasyon — tam koşuyla ölçüldü.** Aynı mimari, aynı çapa, 20 epok,
tek fark gradyanın girdi olarak verilip verilmemesi:

| | test min | adım izi (8 adım) | AO oranı |
|---|---|---|---|
| gradyan **var** | **3.265** | 1.678 → 3.265 (+%95) | 0.615 |
| gradyan **yok** | 1.152 | 1.114 → 1.152 (+%3.4) | 0.215 |

Gradyansız model çapanın (1.112) hemen üstünde kıpırdamıyor ve öğrendiği
adım boyları düz kalıyor (~0.46, hepsi aynı). Yani katkı "sinir ağı faz
buluyor" **değil**, "sinir ağı ön koşullandırma öğreniyor".

*Düzeltme:* ilk sürümde bu ablasyonu "çapanın altında kalıyor (1.067 vs
1.099)" diye yazmıştım; o sayılar 1500 örnek / 5 epoklu bir duman
koşusundandı. Tam eğitimle çapanın hafif **üstünde** ama hâlâ kıpırdamıyor.
Artefakt: `results/mumiso_unroll_nograd.json`.

**Eşit adım sayısında kazanç küçük.** 450 senaryo, aynı çapa:

| L | öğrenilen | düz Adam (lr=0.05) | **ayarlanmış** Adam (lr=0.5) |
|---|---|---|---|
| 1 | 1.788 | 1.199 | 1.730 |
| 4 | 2.103 | 1.462 | 2.534 |
| 8 | **3.309** | 1.787 | 3.043 |

Ayarlanmamış Adam'a karşı %85 önde; **adım boyunu ayarlamak** farkı %8.7'ye
indiriyor. İlk sayıyı raporlamak zayıf-taban-çizgisi hatası olurdu.

**Adım boyu seçimi kiraz toplama değildi.** Doğrulama kümesinde 8 değer
tarandı; lr=0.5'i doğrulama bağımsız seçiyor (L=8 ve L=16). Donmuş lr ile
test: öğrenilen 3.357, Adam-8 3.084, Adam-16 3.753, Adam-32 4.324.
(`scripts/audit_fair_comparison.py`)

**Öğrenilen kural, senaryo-başına-oracle-lr Adam'ı bile geçiyor.** L=8'de
öğrenilen 3.357, her senaryo için en iyi lr'nin seçildiği Adam 3.312. Yani
ön koşullandırma avantajı bir ayar artefaktı değil. Kaybettiği yer
**yalnızca** adım maliyeti.

**Pratik uyarı, modelin lehine:** adım boyu ayarı ~%50 fark ediyor (L=8'de
en kötü lr 1.64, en iyi 3.08). Ayarlanmamış bir gradyan çıkışı dağıtımda
çok daha kötü iş yapar; öğrenilen model ayar gerektirmiyor.

### Eşit gecikmede kaybediyor

Hız 400 senaryo üzerinde toplu, gecikme 60 ayrı senaryoda batch=1, boş
makinede, kütüphane varsayılan iş parçacığıyla
(`scripts/mumiso_budget_fraction.py`). Bütçe T_c = 28.2 ms:

| yöntem | min hız | p05 | p50 | p95 | bütçede (%) |
|---|---|---|---|---|---|
| su_average | 1.266 | 0.0 | 0.0 | 0.0 | 100 |
| **su_best_of** | **1.827** | 0.0 | 0.0 | 0.1 | **100** |
| **ayarlanmış Adam, 8 adım** | **3.223** | 12.3 | **13.3** | 18.4 | **100** |
| ayarlanmış Adam, 12 adım | 3.569 | 18.4 | 19.6 | 29.9 | 87 |
| ayarlanmış Adam, 16 adım | 3.844 | 24.6 | 26.6 | 35.7 | 72 |
| ayarlanmış Adam, 18 adım | 3.930 | 27.3 | 29.8 | 39.1 | 20 |
| **öğrenilen, 8 adım** | 3.440 | 36.0 | **42.9** | 55.0 | **0** |
| ayarlanmış Adam, 20 adım | 4.024 | 31.2 | 34.6 | 47.0 | 0 |
| ayarlanmış Adam, 24 adım | 4.171 | 37.8 | 44.7 | 59.2 | 0 |
| koordinat inişi | 3.76 | — | ~1500 | — | 0 |
| **PGA (3 rastgele başlangıç)** | **5.18** | — | ~5600 | — | 0 |
| AO (cd+su+rastgele) | 5.18 | — | ~6500 | — | 0 |

**İki not, ikisi de daha önceki ifademi düzeltiyor.**

*"16 adım bütçeye sığıyor" yanlıştı.* Nokta medyanı (26.6 ms) sığıyor ama
koşuların yalnız **%72'si** sığıyor. ≥%90 güvenilirlik isterseniz bütçeye
sığan en iyi yöntem **8 adım: 3.223 b/s/Hz, p50 13.3 ms, %100.** Daha
gevşek bir eşiği kabul ederseniz 16 adım 3.844 veriyor. Hangi eşiği
seçtiğinizi tezde yazın; sayı ona göre değişiyor.

*Ölçüm rejimini karıştırmayın.* Bu betiğin ilk sürümü hızı yalnız
zamanladığı 60 senaryodan ortalıyordu ve `torch` iş parçacığını 1'e
sabitliyordu: su_average 0.876 (400 senaryoda 1.266) ve bütün gecikmeler
~%50 şişkin çıkıyordu. İkisi de düzeltildi — min hız ağır kuyruklu, 60 çekiş
ortalamasını tutturmuyor.

*Ve aynı yöntem için iki sayı göreceksiniz.* `mumiso_frontier.py` 450
senaryoda su_average 1.192 / Adam-8 3.123 / Adam-16 3.669 ölçüyor; bu tablo
400 senaryoda 1.266 / 3.223 / 3.844. İkisi de doğru — farklı örneklemler,
ve min hız ortalaması n=400'de %6 civarı oynuyor. **Tezde bir tabloyu
seçin ve senaryo sayısını yazın**, iki tablodan sayı karıştırmayın.
`audit_claims.py --all` ikisini de ayrı ayrı donduruyor.

**Öğrenilen model Pareto sınırında değil — domine ediliyor.** 12 adımlık
Adam onu *her iki eksende* geçiyor: 3.569 vs 3.440 ve 19.6 vs 42.9 ms. Bir
öğrenilen adım ~5.4 ms, Adam'ın adımı ~1.6 ms; adım başına %8.7'lik kalite
avantajı 3.3×'lik maliyeti karşılamıyor. Yapısal bir dezavantaj daha: model 8 adım için eğitildi, daha
uzun çalıştırılamıyor; Adam çalıştırılabilir.

**Koordinat inişi de domine ediliyor** (1535 ms'de 3.76, Adam 32 adımda
48 ms'de 4.16). Literatürde standart olan bu yöntem, bu problemde
ayarlanmış gradyan çıkışına göre hem yavaş hem kötü.

**En güçlü klasik yöntem AO değil PGA.** 3 rastgele yeniden başlatma,
AO'nun (koordinat inişi + su_average + rastgele başlangıç) önünde — 3/3
yapılandırmada doğrulandı, küçük ama tutarlı farkla. Yani AO'ya koyduğum cd
ve su_average başlangıçları rastgele başlangıçtan **daha kötü**. Ama
"AO Pareto sınırında değil" iddiasını geri çekiyorum: iki yöntemin hızı
%0.07 fark ediyor ve hangisinin daha hızlı ölçüldüğü koşudan koşuya
değişiyor — o ifade gecikme gürültüsüyle belirleniyordu.

### Dürüst sonuç

Bu kurulumda, bu ölçekte, CPU'da: **öğrenilen optimizatör karşılığını
vermiyor.** Adım başına kalite avantajı gerçek ama küçük; gecikme maliyeti
onu fazlasıyla yiyor. Adil olmak için: maliyetin tamamı batch=1'de CPU'da
çalışan 272,842 parametreli bir CNN-LSTM'den geliyor; ağ ~3× hızlanırsa
(daha küçük ağ, GPU, nicemlenmiş çıkarım) sınıra girer. Kararı verecek
deney bu — ve tezde yapılması gereken şey de bu, "sinir ağı daha iyi"
demek değil.

---

## 5b. Buradan çıkan asıl tez sonucu

3 GHz'de yürüyen bir kullanıcı (1.5 m/s): f_d = 15.0 Hz, **T_c = 28.2 ms**.

- **PGA ~5600 ms ile ~199×, AO ~6500 ms ile ~232×, koordinat inişi
  ~1500 ms ile ~54× bütçe dışında.** Literatürün standart RIS optimizasyon
  yöntemleri hareketli senaryoda *fiziksel olarak kullanılamaz*, ne kadar
  iyi hız buldukları önemsiz.
- **Bütçeye güvenilir biçimde sığan en iyi yöntem: 8 adım ayarlanmış
  gradyan çıkışı — 3.223 b/s/Hz, p50 13.3 ms, koşuların %100'ü bütçede.**
  En güçlü klasiğin (PGA 5.18) **%62'si.** Eşiği %70'e çekerseniz 16 adım
  3.844 ile **%74**'e çıkıyor. Hangi güvenilirlik eşiğini seçtiğinizi
  yazın — tezde tek bir sayı değil, bir eğri var.
- Öğrenilen model (p50 42.9 ms) bütçeye **hiçbir ölçümde** sığmıyor, ve
  12 adımlık Adam onu hem hızda hem gecikmede geçiyor.
- Çapayı `su_best_of` yaparsanız bedava 1.827 alıyorsunuz (su_average
  1.266), yani bütçe sıfırken bile.

"Tutarlılık süresi kısıtı altında çok kullanıcılı RIS faz optimizasyonu"
diye çerçevelenebilir ve her sayısı ölçülmüş. Sinir ağı burada negatif
sonuç olarak yer alıyor.

**Bölüm 5d bu argümanı hesaptan ölçüme çeviriyor** ve beklediğimden güçlü
çıktı: yöntemlerin sıralaması hareketlilik altında tersine dönüyor ve en
iyi adım sayısı 4.

---

## 5d. Kanal yaşlanması — ölçüldü, ve sıralamayı tersine çeviriyor

Bölüm 5b'nin bütçe argümanı bir *hesaba* dayanıyordu (T_c = 0.423/f_d).
Artık ölçüm var: `ris_mu/mumiso/mobile.py` yürüyen kullanıcı üretiyor —
saçıcılar, yol kazançları, LoS durumu ve gölgeleme zaman boyunca **sabit**,
yalnız konum değişiyor. (Kazançlar her adımda yeniden çekilseydi ardışık
anlar bağımsız olurdu ve ölçülecek bir yaşlanma kalmazdı.)

### Bir yöntem, bitirdiğinde var olan kanala cevap verir

Asıl fikir bu. t=0'da bulduğunuz faz, yöntem bitene kadar eskimiş olur.
Yani bir yöntemin **geçerli hızı**, kendi gecikmesindeki kanalda elde
ettiği hızdır. 400 senaryo, 1.5 m/s, 20 saçıcı, **düzeltilmiş ön
kodlayıcı**:

| yöntem | t=0 hızı | gecikme | **geçerli hız** | korunan |
|---|---|---|---|---|
| su_average | 4.624 | ~0 | 4.624 | 1.00 |
| su_best_of | 5.276 | 0.05 ms | **5.276** | 1.00 |
| **Adam 8 adım** | 6.443 | 13.3 ms | **5.849** | 0.91 |
| Adam 12 adım | 6.631 | 19.6 ms | 5.533 | 0.83 |
| Adam 16 adım | 6.754 | 26.6 ms | 5.324 | 0.79 |
| Adam 20 adım | 6.835 | 34.6 ms | 5.262 | 0.77 |
| koordinat inişi | 6.925 | ~1500 ms | 4.921 | 0.71 |
| **PGA** | **7.117** | ~5600 ms | **4.667** | 0.66 |
| *eskimiş taban (bağımsız kanal)* | — | — | *~4.35* | — |

**t=0 sıralamasının en iyisi (PGA, 7.117) geçerli sıralamanın en kötüsü
(4.667).** Ve 0.05 ms'lik bedava bir sezgisel (su_best_of, 5.276),
literatürün en güçlü yöntemini hareketlilik altında **geçiyor.**

### Yük taşıyan varsayım — tezde mutlaka yazın

Yukarıdaki tablo **ön kodlayıcının her anda yeniden hesaplandığını**
varsayıyor; yalnız RIS fazı eskiyor. Fiziksel olarak doğru taraf bu — ön
kodlama dijital ve mikrosaniyeler sürüyor, yavaş olan faz optimizasyonu ve
RIS donanımına yazma.

Ama bu varsayım sonucun **neredeyse tamamını** taşıyor. Ön kodlayıcı da
eskirse (8 adım Adam fazı, 300 senaryo):

| t [ms] | taze ön kodlayıcı | eski ön kodlayıcı |
|---|---|---|
| 0 | 6.052 | 6.052 |
| 13.3 | 5.395 | 0.687 |
| 28.2 | **4.718** | **0.279** |
| 100 | 4.402 | 0.175 |

Bir tutarlılık süresinde **17 kat** fark. Yani "RIS fazının eskimesi şu
kadara mal olur" cümlesi ancak ön kodlayıcı yetişiyorsa doğru; bütün zincir
eskiyorsa faz ikinci dereceden bir mesele haline geliyor ve asıl kayıp ön
kodlayıcıdan geliyor.

Bu ders Bölüm 5e'de ikinci kez, başka bir deneyden çıkıyor: **darboğaz faz
değil ön kodlayıcı.** İki bağımsız ölçümün aynı şeyi söylemesi, tezde
üzerine basabileceğiniz bir sonuç.

### Daha çok optimize etmek sizi daha kötü yapıyor

t=0 hızı tekdüze artıyor, geçerli hız **içsel bir maksimuma** sahip:

| Adam adımı | gecikme | t=0 hızı | geçerli hız |
|---|---|---|---|
| 0 (su_best_of) | 0.05 ms | 5.276 | 5.276 |
| 2 | 3.3 ms | 5.784 | 5.749 |
| **4** | **6.7 ms** | 6.128 | **5.982 ← en iyi** |
| 6 | 10.0 ms | 6.316 | 5.970 |
| 8 | 13.3 ms | 6.443 | 5.849 |
| 16 | 26.6 ms | 6.754 | 5.328 |
| 32 | 53.2 ms | 6.970 | 5.201 |
| 48 | 79.8 ms | 7.037 | 5.135 |

Optimum **4 adım.** Yakınsamaya bakarak tasarlarsanız 48 adım seçersiniz,
t=0'da %34 daha iyi görünürsünüz ve gerçekte optimumdan **%14** geride
olursunuz. (Bozuk ön kodlayıcıyla bu ceza %32'ydi — hata düzeldikçe etki
küçüldü ama yönü ve içsel maksimum aynı kaldı.)

Bu, tezin tek grafikte anlatılabilecek sonucu: *hareketli bir senaryoda
faz optimizasyonunun doğruluğu değil, doğruluk-gecikme takası optimize
edilir, ve optimum beklenenden çok daha erken.*

### Modelin nerede güvenilir olduğu, ve hangi yöne yanlı olduğu

Üretece saçıcı kümesini pencere boyunca sabit tutturuyorum. Onlarca
milisaniyede (birkaç santim, dalga boyunun kesri) bu doğru model ve
bozulma gerçek geometriden geliyor.

Saniyeler mertebesinde değil: 8 metre yürümüş bir kullanıcı farklı
saçıcılar görür, bu model aynılarını tutuyor. Ölçülen sonuç — G'nin
zamansal korelasyonu iki bağımsız kanalın gösterdiği 0.10'a inmek yerine
**~0.5'te tabana oturuyor**, ve saçıcı sayısını 6'dan 60'a çıkarmak bu
tabanı neredeyse hiç kıpırdatmıyor (0.60 → 0.51), çünkü baskın saçıcı
kanalı sabit bir altuzayda neredeyse rank-1 tutuyor.

Yani model uzun ufukta kaybı **eksik** gösteriyor. Bu yön önemli: yavaş
klasik yöntemler burada **kayırılıyor** ve yine kaybediyorlar. Onlar için
tablo "eskimiş taban"ı da veriyor (t=0 fazının bağımsız bir kanalda aldığı
hız) — gerçek değer eğriyle o taban arasında. 200 ms'ye kadar eğriye
güvenin; ötesinde tabana yakın okuyun.

Betikler: `scripts/verify_mobile.py` (kanal sürekli mi, doğru hızda mı
dekorele oluyor mu), `scripts/mumiso_aging.py` (eğri ve geçerli hızlar).

---

---

## 5e. Kusurlu CSI — ve ön kodlayıcının asıl darboğaz olduğu

Hipotez şuydu: klasik optimizatör gürültülü CSI'yi doğruymuş gibi optimize
eder ve hatanın üstüne aşırı uyar; birçok hata gerçeklemesi üzerinde
eğitilmiş bir model dayanıklı olabilir. Eğitim koşmadan önce **yer var mı**
diye baktım (`scripts/mumiso_csi_room.py`), ve ölçüm beni başka bir yere
götürdü.

İlk sonuç fiziksel değildi: −20 dB hatada (yani %1 hata gücü) hız oracle'ın
%28'ine çöküyordu. İzini sürünce sorun CSI'de değil ön kodlayıcıda çıktı —
yukarıdaki `zf()` hatası. **Düzeltmeden önce bu deney benim hipotezimi
değil, ZF'in matris tersi duyarlılığını ölçüyordu.**

Bu kendi başına tezde yeri olan bir bulgu: **yüksek SNR'da kusurlu CSI
altında darboğaz RIS fazı değil, ön kodlayıcıdır.** ZF'in artık girişimi
gürültüyle değil kanal gücüyle ölçeklendiği için sistem girişim-limitli
hale geliyor ve faz seçimi onun yanında silikleşiyor.

### "Dayanıklı ön kodlayıcı" iddiamı geri çekiyorum

Önce şöyle yazmıştım: doğru cevap düzenlileştiriciye hata gücünü katmak
(MMSE/RZF). Ölçtüm, **işe yaramıyor** (400 senaryo, faz ve ön kodlayıcı
tahminden, hız gerçek kanalla):

| hata | eps=0 | MMSE(gürültü) | MMSE+hata | en iyi taranan |
|---|---|---|---|---|
| mükemmel | 5.756 | 5.720 | 5.720 | 5.757 @1e-5 |
| −20 dB | **1.310** | 1.314 | **1.214** | 1.337 @1e-2 |
| −15 dB | 0.689 | 0.690 | 0.667 | 0.704 @1e-2 |
| −10 dB | 0.307 | 0.307 | 0.307 | 0.319 @1e-1 |

Hata gücünü katmak −20 dB'de **%7 kaybettiriyor**, ve en iyi taranan
düzenlileştirici bile eps=0'ı yalnız %2 geçiyor. Nedeni: MMSE **toplam**
hız için türetilmiş, bu paket **max-min** raporluyor — amacı tek en kötü
kullanıcı belirliyor ve ön kodlayıcıyı MRT'ye çekmek ona yardım etmiyor.

Yani çöküş bir ayar hatası değil, **ZF'in hata duyarlılığı özsel.** Hiçbir
skaler düzenlileştirici onu kaldırmıyor. `err_power` parametresi kodda
kaldı (toplam-hız çalışması için) ama varsayılanı 0 ve docstring'de bu
ölçüm yazılı.

Sıradaki adım hâlâ geçerli: hipotezi (ağ hataya dayanıklı olabilir mi) bu
koşullarda sormak. Ama artık biliyoruz ki karşısında duracak şey
"dayanıklı ön kodlayıcı" değil, düzenlileştirilmemiş ZF.

**Yöntem notu, bu deneyin kurgusundan:** faz **ve** ön kodlayıcı tahminden
hesaplanıyor, hız gerçek kanalla değerlendiriliyor. Ön kodlayıcıyı gerçek
kanaldan hesaplamak cezanın çoğunu saklar ve her şeyi olduğundan iyi
gösterir. Ve karşılaştırma her hata seviyesinde **en iyi adım sayısına**
karşı yapılmalı — erken durdurma da bir düzenlileştirici, "ağ 32 adımlık
Adam'ı geçiyor" hiçbir şey kanıtlamaz.

---

## 5f. Faz optimizasyonu ne kadarını getiriyor — tezde bunu açıkça yazın

Ön kodlayıcı düzeltildikten sonra, tezin çerçevesini etkileyen bir sayıyı
ölçtüm (400 senaryo, düzeltilmiş ön kodlayıcı):

| | min hız | bir öncekine göre |
|---|---|---|
| RIS yok | 1.122 | — |
| **rastgele faz** | **3.371** | **3.0×** |
| su_average | 3.765 | 1.12× |
| su_best_of | 4.417 | 1.17× |
| PGA (en güçlü) | 6.397 | 1.45× |

İki ayrı kazanç var ve karıştırılmamalı:

- **RIS'i konuşlandırmak: 3.0×.** Yüzey oradaysa, fazı rastgele bile olsa
  hızı üçe katlıyor.
- **Fazı optimize etmek: 1.90×** (rastgele 3.371 → PGA 6.397).

Yani **rastgele bir yüzey, optimize edilmiş olanın %53'ünü zaten
veriyor.** %90 ek kazanç küçük değil, ama tezin "faz optimizasyonu her
şeydir" izlenimi vermemesi gerekir — ve jüri bu ayrımı sorar. Önceki
bozuk ön kodlayıcıyla bu oran çok daha dramatik görünüyordu (çapa/en
güçlü 4.1×), yani hata bu çerçeveyi de bozuyordu.

Bölüm 5d ile birleştirince tablo şu: hareketlilik altında optimize
edilmiş fazın avantajı daha da erir, çünkü optimizasyon süresi boyunca
faz eskir. 5d'deki geçerli hızlarda PGA 4.667, rastgeleye kıyasla yalnız
1.38×.

## 5c. Zayıf taban çizgisi: dört kere yanıldım

Size "zayıf taban çizgisi seçerseniz sonuç havada kalır" diye yazdıktan
sonra tam o hataya dört kez düştüm. Dördü de ölçümle yakalandı, üçünü ben
yakaladım, dördüncüsünü denetim.

**1.** `ao` yalnız koordinat inişi çağırıyordu — `cd` ile birebir aynı
sonucu veriyordu, iki taban çizgisi gibi görünüp tek şey ölçülüyordu.

**2.** İnce ayar normalize-gradyan + geri adım kullanıyordu: aynı amaç
fonksiyonunda, aynı başlangıçtan 3.96, düz Adam 5.25. %32 fark. *(Not: o
kod artık pakette yok, dolayısıyla 3.96 sayısı bu paketten yeniden
üretilemez — yalnız 5.25 yarısı üretilebilir: 5.2469.)*

**3.** Öğrenilen modelin "düz Adam'ı %85 geçiyor" sonucu. Adam'ın adım
boyunu ayarlayınca %8.7'ye indi, gecikmeyi hesaba katınca tersine döndü.

**4. (denetim bunu buldu) Her şeyin ölçüldüğü ÇAPA zayıftı.** `su_average`,
bellekte zaten duran K+1 adayın en kötüsü:

| | min hız | maliyet |
|---|---|---|
| su_average (kullandığım) | 1.134 | ~0 ms |
| **en iyi-of-(K+1)** | **1.679** | ~0 ms |

**+%48, bedava.** `su_align_phase` K fazın hepsini zaten döndürüyor; hatta
öznitelik kanalı −3/−2 olarak ağa veriliyorlar. su_average senaryoların
yalnız **%14'ünde** kazanıyor; tek-kullanıcı hizalamaları %86'sını alıyor.
`su_best_of` olarak koda eklendi.

Sonuçları: açılmış modelin kazancı su_average'a göre 2.94×, doğru çapaya
göre **1.94×**. Bölüm 4'ün "model çapanın altında" ifadesi *güçleniyor*
(1.01 vs 1.68). Bölüm 5b'nin sonucu ayakta ama bütçe içi hız ~%3 eksik
raporlanmıştı.

**En güçlü klasiklerin değerleri** (varsayılan 1000 Adam adımıyla, 400
senaryo): su_average 1.2659, cd 3.8521, **PGA 5.3793**, AO 5.3678.
*(İlk sürümde 5.28/5.27 yazmıştım — onlar 400-adım değerleriydi, paketin
varsayılanı 1000.)* AO adım sayısıyla hâlâ tırmanıyor (400→5.27,
1000→5.37, 2000→5.40), yani raporlanan değer bir **taban**, tavan değil.

Kendi kodunuza uygulayacağınız kural: *"daha tembel bir yöntem bunu geçer
mi?"* Dört taban çizgim de bu soruyla düştü — ikisi klasik yöntem, biri
kendi önerdiğim yöntem, biri de her şeyin altındaki çapa.

---

## 6. Kanal tanısı

**N=32, T=8, K=4, 1000 senaryo** (tek yapılandırma):

| ölçüt | değer |
|---|---|
| G etkin rank (kullanıcılar havuzlanmış) | 15.73 / 32 |
| G etkin rank (tek kullanıcı) | 15.58 |
| F etkin rank (anten 0) | 13.46 |
| G komşu eleman \|korelasyon\| | 0.572 |
| F komşu eleman \|korelasyon\| | 0.692 |
| **anten ekseni** komşu \|korelasyon\| | 0.740 |
| **anten ekseni** etkin rank | 4.00 / 8 |
| LoS oranı (BS→RIS / RIS→UE / doğrudan) | 0.383 / 0.270 / 0.297 |

Hem eleman hem anten ekseninde düzgün korele bir açıklık; anten ekseni
rankı 4.00/8, yani tam rank değil.

### Etkin rank: mutlak değer quote etmeyin

Tahmin edici örnek sayısına güçlü biçimde bağlı **ve tek yönlü değil**:

| örnek | G etkin rank |
|---|---|
| 250 | 16.57 |
| 1000 | **16.07** ← düşüyor |
| 4000 | 20.75 |
| 16000 | 21.18 |

Katlar arası yayılım **%29**. İlk sürümde "örnek sayısıyla yukarı kayıyor"
demiştim — 250→1000 aralığında *düşüyor*, yani mekanizma iddiam o aralıkta
tutmuyor. Ayrıca aynı ayarda aynı sayıda örnek bile RNG akışına göre %2.2
oynuyor (1000 senaryo tek çağrıda 15.73, 4000'lik çağrının ilk 1000'i
16.07).

Pratik kural: **"N örnekle ölçülen değer şudur"** diye yazın, ve
yapılandırmaları yalnız eşit örnek sayısında karşılaştırın.
`audit_claims.py` bunu kontrol ediyor (önceki sürümdeki kontrol ilk 1000
senaryoyu yeniden kullanıyordu ve asla başarısız olamazdı — denetim
yakaladı).

### F'nin rankına değil G'ye bakın

Burada F'nin rankı sağlıklı (13.46) çünkü saçıcı geometrisi her örnekte
yeniden çekiliyor. Ama BS→RIS bağlantısı *deterministik yönlendirme
vektörü çarpı tek skaler kazanç* olan bir üreteçte F'nin rankı yapısal
olarak 1 çıkar ve sayı hiçbir şey söylemez — MATLAB üretecinde tam bunu
ölçtüm (1.03).

---

## 7. Doğrulanan matematik

| kontrol | sonuç |
|---|---|
| Tek kullanıcıya indirgeme, genel form | analitik sınırın **1.0000**'ı |
| Tek kullanıcıya indirgeme, Denklem (8) | **0.8977**'si |
| SINR/hız ifadesi, bağımsız numpy referansı | **2.3e-13** (ZF), 5.6e-16 (MRT) |
| ZF sızıntı/sinyal | **2.6e-20** (complex128), **6.9e-13** (complex64) |
| ‖W‖_F² = Pt (MRT ve ZF) | **1.000000**, Pt=1 ve Pt=4 |
| Hız gradyanı vs sonlu fark | göreli **7.97e-09** |
| Ham ağ çıkışı ölçekten bağımsız | **6.06e-12** |
| Düz-geçiş: dθ_q/dθ | **tam 1.000000** (naif `round` **0.000000** verir) |
| Yumuşak min, gerçek min'in alt sınırı | β=8'de boşluk ≤ log(K)/β, R≈0.5/3/16'da ihlal yok |
| Permütasyon değişmezliği (deepsets/exchange) | **8.7e-11 / 1.7e-10** |
| BatchNorm simetriyi bozuyor mu | **hayır**; tek kaynak dropout örneklemesi |
| Artık mod çapada mı başlıyor | sapma **2.2e-04** rad |
| Gradyan bütün parametrelere akıyor mu | **26/26** |
| CD monotonluğu | 1.3457 → 3.8406, min adım **+3.35e-02** |

**ZF hakkında iki uyarı.** (a) Sızıntı duyarlılığa bağlı: complex128'de
2.6e-20, complex64'te 6.9e-13 — ve bu paketin bütün deneyleri complex64
koşuyor. İhmal edilebilir, ama 1e-21 rakamı deneylerin koştuğu rejimin
hassasiyetini abartıyor. (b) **Kötü koşullu halde nulling çalışmıyor:** iki
kullanıcının etkin kanalı 1e-6 aralıklı olduğunda sızıntı/sinyal = 1.0.
Düzenlileştirilmiş ZF için doğru davranış, ama "ZF girişimi sıfırlar"
ifadesi koşullanmaya bağlı.

### Denklem (8) üzerine

Tek kullanıcıda genel optimum `θ_n = ∠h_d − ∠(g_n f_n)`; makaledeki
`θ_n = −∠(g_n f_n)` bunun `h_d = 0` özel hali. Makale doğrudan yolun bloke
olduğu senaryoyu çalışıyor ve orada iki ifade aynı. Tezde yeri Bölüm 3'te
**kapsam genişletmesi**, errata değil.

---

## 8. Çalıştırma

```bash
# sürekli doğrulama — her değişiklikten sonra
python3 -I scripts/audit_claims.py            # hızlı katmanlar
python3 -I scripts/audit_claims.py --all      # taban çizgileri dahil

# matematik ve mimari
python3 -I scripts/verify_mumiso_system.py
python3 -I scripts/verify_mumiso_models.py
python3 -I scripts/verify_baseline_strength.py

# §4'ün belirleyici teşhisi ve §4b'nin açıklama testi
python3 -I scripts/diagnose_learnability.py
python3 -I scripts/audit_section4_cause.py

# asıl sonuç: gecikme dağılımı ve bütçe (BOŞ MAKİNEDE)
python3 -I scripts/mumiso_budget_fraction.py
python3 -I scripts/mumiso_frontier.py
```

Bağımlılık: `numpy`, `torch`. GPU gerekmiyor; bütün sayılar CPU'da üretildi.
Gecikme ölçen betikleri **boş makinede** çalıştırın.

---

## 9. Bulgulara göre tez yapısı — tavsiyem

**Bölüm 3 — Sistem modeli ve tek kullanıcılı temel.** Yayınlanan makale
olduğu gibi. Tek ekleme: genel optimal faz, Denklem (8)'in `h_d = 0`
özel hali olarak. Kapsam genişletmesi dili.

**Bölüm 4 — Çok kullanıcılı genişlemenin sınırı.** Üç ölçüm (yukarıda).
**Dikkat — ilk tavsiyemi geri alıyorum:** bunu *"problem formülasyonu kötü
konumlu, mimari yetersiz değil"* diye yazmayın. Ölçüm tersini gösteriyor:
hedef girdi tarafından belirleniyor (aynı senaryonun iki çözümü %58–81
uyuşuyor) ve gözlenen eğitim/doğrulama imzası yetersiz uyum imzası. Doğru
ifade: *"optimal faz, kanalın neredeyse deterministik ama düzgün olmayan
bir fonksiyonu; bu temsil ve bu mimari onu ifade edemiyor."* Yani mesele
**temsil ve koşullanma**, keyfilik değil.

**Bölüm 5 — Öğrenilen güncelleme kuralı (test edildi, reddedildi).** İki
somut çıktı: (a) ön koşullandırma öğrenilebilir ve adım başına %8.7
kazandırıyor, oracle-lr Adam'ın bile üstünde; (b) 272k parametreli bir
güncelleme ağının adım maliyeti o kazancı CPU'da fazlasıyla yiyor. Açık
bırakılan deney net: ~3× daha hızlı bir güncelleme ağı. Jüriye "denedim,
ölçtüm, şu koşulda işe yarardı" demek "sinir ağı daha iyi" demekten çok
daha güçlü.

**Bölüm 5b — Tutarlılık süresi kısıtı (asıl pozitif sonuç).** Yukarıdaki
tablo.

**Bölüm 6 — Permütasyon simetrisi.** deepsets ve exchange çıkarımda tam
değişmez (1e-10), eğitim sonrası da (2.2e-06 / 1.5e-06); concat değil
(7.0e-03). BatchNorm'un simetriyi bozmadığı, tek kaynağın dropout
örneklemesi olduğu ölçüldü.

**Ama hangi değişmez mimariyi seçtiğiniz fark etmiyor** — aşağıya bakın.
Bu bölümü "permütasyon değişmezliği bedava ve doğruluk için değerli, ama
performans getirmiyor" diye yazın.

---

## 9b. Mimari seçimi fark etmiyor — ölçüldü

İlk sürümde exchange'i "MATLAB'ın yapamadığı güçlü olan" diye sundum ve
yalnız onu eğitmiştim. Denetim bunun doğrulanmamış olduğunu söyledi;
üçünü de eğittim. Açılmış modelde, aynı çapadan, 8 adım:

| mod | test min | parametre | epok |
|---|---|---|---|
| **deepsets** | **3.3074** | **264,522** | 20 |
| exchange | 3.2648 | 272,842 | 30 |
| concat | 3.2620 | 288,138 | 20 |

**En basiti ve en az parametrelisi en iyi** — hatta deepsets 20 epokta
exchange'in 30 epoğunu geçiyor, yani sonuç epok farkına rağmen (aslında
onun *aleyhine*) geçerli.

Dürüst okuma: ortalama-alan değişimi yapısal olarak deepsets'i içeriyor
(sıfıra yakın başlatılmış artık terim, başlangıçta fark 0.000e+00
ölçüldü) ama **bu problemde hiçbir şey kazandırmıyor.** Kullanıcı ekseni
işleme biçimi performansın geldiği yer değil. Tezde exchange'i "daha
ifade gücü yüksek" diye yazabilirsiniz; "daha iyi sonuç veriyor" diye
yazmayın.

Bunun bir yan faydası var: MATLAB paketinde özel katman gerektirdiği için
deepsets'e inmek zorunda kalmıştım ve bunu bir eksiklik olarak yazmıştım.
Değilmiş.

## 10. Senaryo gerçekçiliği — üç aşamalı planınızın son aşaması

**Birinci öncelik: hareketlilik ve kanal yaşlanması.** Gecikme ölçümü
yapıldı; eksik olan **"28 ms'de yeniden yapılandırmazsanız ne
kaybediyorsunuz"** eğrisi. Bütçe argümanını bir hesaptan bir ölçüme
çeviriyor. `_sf_corr` zaten Gudmundson korelasyonu yapıyor; aynı mekanizma
zaman eksenine taşınabilir.

**İkinci: kusurlu CSI.** Daha önceki ölçümümüz uzamsal işlemenin yerini
ancak kanal korele **ve** CSI kusurlu olduğunda hak ettiğini gösterdi. Bu
paketin kanalı korele; ikinci koşul eksik.

**Üçüncü: ayrık faz.** `system.quantise_ste` hazır ve dθ_q/dθ = 1 olduğu
doğrulandı. Uyarı: daha önceki tek-RIS deneyinde ayrık koordinat inişi
düz-geçiş ağını 1-bit'te yeniyordu. Ölçmeden iddia yazmayın;
`baselines.coord_descent(..., bits=b)` gerçek ızgarada arıyor.

**Dördüncü: yol kaybı zaten yapıldı.** 3GPP TR 38.901 InH-Office.

**Yapmamanızı önerdiğim:** AERPAW/AFAR hava araçlı veri kümelerini bu teze
katmak. Senaryo iç mekân sabit RIS ve yürüyen kullanıcı; hava aracı kanalı
farklı bir Doppler ve geometri rejimi, ayrı bir çalışma.

---

## 11. Denetimin bulduğu ve düzeltilenler

| # | bulgu | durum |
|---|---|---|
| 0 | §9b'nin iki boşluğu: exchange'in üstünlüğü doğrulanmamış | üçü de eğitildi; **fark etmiyor**, §9b yazıldı |
| 1 | §4'ün **açıklaması** yanlış (hedef keyfi değil, belirlenmiş) | §4b yazıldı, §9 tavsiyesi tersine çevrildi |
| 2 | **Çapa zayıf** — su_best_of +%48 bedava | `su_best_of` eklendi, etkilenen oranlar düzeltildi |
| 3 | Dokümantasyonda `diag(v^H)`, kodda `diag(v)` | docstring'ler düzeltildi, §2'ye uyarı eklendi |
| 4 | Bütçe oranı sütununu hiçbir betik üretmiyordu, %95 aslında %85–90 | `mumiso_budget_fraction.py` yazıldı, §5b yumuşatıldı |
| 5 | `audit_claims.py`'nin monotonluk kontrolü boştu | düzeltildi; artık doğru şeyi kontrol ediyor |
| 6 | §5c'de PGA/AO 400-adım değerleriyle verilmiş | 1000-adım değerleriyle düzeltildi |
| 7 | §5c'nin süre kolonu güvenilmez, PGA/AO ters | kaldırıldı |
| 8 | "azalan adım çizelgesi" — önce yükseliyor | düzeltildi |
| 9 | ZF sızıntısı complex128 artefaktı; kötü koşullu halde nulling yok | §7'ye iki uyarı eklendi |
| 10 | "AO Pareto sınırında değil" gecikme gürültüsü | iddia geri çekildi |
| 11 | §6 aynı ölçüm için iki değer, drift tek yönlü değil | §6 yeniden yazıldı |
| 12 | §2'nin senaryo sayıları AO'nun, en güçlünün değil | PGA değerleriyle güncellendi |
| **13** | **`zf()`'nin düzenlileştiricisi mutlak sabit, min hızın %55'i** | **MMSE/RZF'ye çevrildi; 5d/5e/5f yeniden ölçüldü, 4/5/5b/5c/6 bekliyor** |
| 14 | `rates_mismatched` hata-farkında ön kodlayıcıyı kullanmıyordu | düzeltildi; `err_power` artık geçiyor |
| 15 | `csi.py` "hata her bağlantının kendi gücüyle orantılı" diyordu, kullanıcı içinde değil | docstring düzeltildi; ölçtüm, sonucu %5'ten az etkiliyor |
| 16 | MMSE düzenlileştirici bu çalışma noktasında düzenlileştiricisizden %1.4 kötü | docstring'e yazıldı; asıl kazanç ölçekten bağımsızlık |
| 17 | **"hata gücünü düzenlileştiriciye katmak dayanıklılık verir" iddiam yanlış** | ölçüldü: −20 dB'de %7 kaybettiriyor; iddia geri çekildi, `err_power` varsayılanı 0 |
| 18 | **5d'nin sonucu "ön kodlayıcı taze" varsayımına dayanıyor, 17 kat fark** | varsayım 5d'de açıkça yazıldı, iki kolonlu tablo eklendi |
| 19 | Çapa düzeltmesi %48 değil **%17** (düzgün ön kodlayıcıyla) | `audit_claims` eşiği ölçülen değerle güncellendi |
| 20 | Ön kodlayıcı değiştikten sonra 13 dondurulmuş iddia bayatladı | denetleyici hepsini yakaladı; yeniden donduruldu, 40/40 |

Madde 13'ü denetim yakalamadı, ben de kusurlu CSI deneyine girmeseydim
yakalamazdım — ancak hata modelini kurup sonucun fiziksel olmadığını
görünce ortaya çıktı. Dersi: *bir sayı fiziksel olarak mümkün mü* diye
sormak, kodu okumaktan bazen daha etkili.

Denetimin **doğruladığı**: §7'nin 13 satırı, §4'ün üç ölçümü ve §5'in
dokuz kalite sayısı dört ondalığa kadar; matematikte hesaplama hatası yok.

---

## 12. Neyin arkasında kayıt var, neyin yok

Bir iddianın arkasında artefakt yoksa tezde kullanılmamalı. Durum:

**Artefaktı var:** §7'nin tamamı (`audit_claims.py`, 25/25 geçiyor);
§4 Ölçüm 2 ve 3 (`diagnose_learnability.py`); §4b
(`audit_section4_cause.py`); §5'in kalite sayıları
(`results/mumiso_unrolled.json`, `mumiso_budget.json`,
`mumiso_audit_fair.json`, `mumiso_frontier.json`); §6
(`audit_claims.py`); §5c'nin 1., 3. ve 4. maddeleri; §4 Ölçüm 1
(`results/mumiso_sec4.json` — üç mimari, 20 epok); §9b
(`mumiso_unroll_concat.json`, `mumiso_unroll_deepsets.json`,
`mumiso_unrolled.json`).

**Koşuyor, bu satır yazıldığında henüz bitmemişti:** §5'in gradyan
ablasyonu (`results/mumiso_unroll_nograd.json`). Bitene kadar o ablasyonun
sayıları küçük bir duman koşusundan (1500 örnek, 5 epok) geliyor.

**Artefaktı yok, tezde kullanmayın:** §5c'nin 2. maddesindeki 3.96
(o kod pakette yok); `models.py` docstring'indeki %32 / %148 / 3.25 /
π-2 sayılarının bir kısmı (bir bölümü `diagnose_mumiso_gap.py`'den
üretilebilir, "dense head 3.25" önceki pakete ait); §6'nın MATLAB
karşılaştırmaları ve §10'un 1-bit sayıları (başka pakete ait, oradan
alıntı).
