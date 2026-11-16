# Editör / hakem denetimi: Makale 2 revizyonu (16 Kasım 2026)

**Denetlenen:** `thesis_exp/makale2_revizyon/` (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`, PDF). Özgün `paper_mobility/` açılmadı, hiçbir kaynak dosya değiştirilmedi.
**Kapsam:** tutarlılık, mantık, dil, TWC uyumu. Sayılar ham veriyle karşılaştırılmadı. Aşağıda "doğrulansın" diye işaretlenenler sayı denetçisine aktarılacak.
**Satır numaraları:** `sections/*.tex` dosyalarında her paragraf tek satırdır. Bu yüzden satır numarası paragrafı gösterir.

---

## KRİTİK

### K1. Sınırlılıklar paragrafı §VI-H'den güçlü bir iddia kuruyor
`sections/section_07_conclusion.tex:16`, cümle şöyle: *"charging the effective-channel pilots and adding estimation error lower absolute rates strongly but leave the slow solvers behind (Section VI-H)."*

§VI-H bu cümleyi her rejimde desteklemiyor:
- `section_06_results.tex:108`: *"at 10 dB and below the methods cannot be told apart"*. Yani ρ ≤ 10 dB'de yavaş çözücüler geride **değil**, istatistiksel olarak ayırt edilemiyor.
- `section_06_results.tex:110`: 1 bitte, tek taramalı koordinat inişi en iyi yuvarlanmış Adam ile **berabere**. Ayrık fazlar Sınırlılıklar'da hiç geçmiyor. Eski cümle ("discrete phases … follow") silinmiş, yerine bir şey konmamış.

CLAUDE.md'nin 10. kuralı da burada geçerli: iddiayla çelişen bulgu yumuşatılmaz, öne yazılır.
**Öneri:** bkz. Ö1, Sınırlılıklar için önerilen metin.

### K2. Yeni bulgularla çelişen eski cümleler kalmış
| Yer | Cümle | Sorun |
|---|---|---|
| `section_02_related_work.tex:8` | *"Practical surfaces have a few bits of phase resolution~\cite{…}; we use continuous phases."* | §VI-H 1/2/3 bitlik fazları ölçüyor. Cümle artık yanlış. |
| `section_03_system_model.tex:29` | *"Channel knowledge is perfect apart from the acquisition delay we add."* | §VI-H kusurlu kanal bilgisini ölçüyor. Cümle ana sonuçlarla sınırlandırılmalı ve ileri atıf vermeli. |
| `section_04_latency_analysis.tex:14` | *"Section~\ref{sec:res_beam} prices this assumption."* | Taze-hüzme varsayımının pilot bedeli artık §VI-H'de. Atıf yalnızca VI-G'yi gösteriyor. |
| `mobility_paper_ieee.tex:31` (Özet) | *"All results assume the precoder is recomputed from the current channel."* | §VI-H'deki sonuçlar bu varsayımı kullanmıyor: pilot ücretleniyor, kestirim hatası var. "All" artık yanlış. "The main results" yazılmalı ya da cümle değiştirilmeli (bkz. Ö2). |
| `section_06_results.tex:98` (§VI-G) | *"All results assume that the BS refreshes its precoder…"* | Aynı sorun, ilk cümlede. |

### K3. PGA tanımsız
`section_06_results.tex:106` ve `:108` iki iddia kuruyor: *"coordinate descent and PGA remain significantly behind"*. Ancak PGA makalenin hiçbir yerinde tanımlanmıyor. §V-B "Methods" listesinde yok, açılımı yok, gecikmesi yok, kaynağı yok. Hakem önce "hangi algoritma, adım sayısı ne, kaç ms sürüyor?" diye sorar. Ardından da şunu sorar: "ana sonuçlarda olmayan bir yöntem neden yalnızca dayanıklılık bölümünde var?"
**Öneri:** PGA §V-B'ye bir cümleyle eklensin. Örnek: *"\emph{PGA} is projected gradient ascent on the hard minimum rate, with [L] steps and step size [·]; it is timed like Adam."* Köşeli parantezler ilgili rapordan doldurulsun. Bu yapılamıyorsa PGA §VI-H'den çıkarılsın.

### K4. Sembol çakışması (R) ve tanımsız sembol (ρ)
- `section_06_results.tex:106`: *"refreshed every $R$ ms … with $R=1$--2 ms"*. Makalede R zaten hızı gösteriyor: `R_k` (§III), `R^{\mathrm{eff}}` (Tanım 1), `R_\infty` (eq. conv_law), `\bar R^{\mathrm{eff}}` (Tanım 3). Bu çakışma bir TWC hakeminin ilk işaretleyeceği şeylerden biri. Ayrıca "every $R$ ms" yazımı, sembolü birimsiz bir sayıya çeviriyor.
  **Öneri:** `$T_{\mathrm{r}}$` (precoder refresh period) kullanılsın: *"refreshed every $T_{\mathrm{r}}$ … with $T_{\mathrm{r}}=1$--2~ms"*.
- `section_06_results.tex:108`: `ρ` tanımsız. Pilot SNR'si mi, kestirim SNR'si mi? Hatanın normalize gücü neye göre, kanal elemanı başına mı? Ayrıca makalede ρ'nun gerçek pilot SNR'si ile bağı da kurulmuyor. Bağlantı bütçesi §III'te var: 20 dBm, RIS üzerinden medyan 31.1 dB. Hakem "30 dB kestirim SNR'si bu senaryoda kaç pilot simgesine denk geliyor?" diye sorar.
  **Öneri:** *"…with additive estimation error $\tilde{\mathbf{h}}=\mathbf{h}+\mathbf{e}$, $\mathbf{e}\sim\mathcal{CN}(\mathbf{0},\frac{\sigma_h^2}{1+\rho}\mathbf{I})$ on every channel, where $\rho$ is the estimation SNR and $\sigma_h^2$ the per-entry channel power…"* Modeli bu değilse metin gerçek modele göre yazılsın.

### K5. §VI-H'deki üç taban değeri birbirine bağlanmıyor, bir değer iki deneyde aynı (doğrulansın)
- **5.21** (`:106`, "free refresh"), **6.08** (`:108`, kusursuz CSI) ve ana sonuçların tepesi **5.98** (§VI-B) var. Bunlar üç farklı "best rate". Okur hangisinin neyle kıyaslandığını çıkaramıyor. Muhtemel nedenler: 5.21 dağıtımdan sonraki 50 ms'nin ortalaması, 6.08 ise 1.33 ms adımla tek anlık etkin hız. Metin bunu söylemiyor ve "best rate" ile "best effective rate" terimlerini karıştırıyor.
- **3.54** iki ayrı deneyde çıkıyor: 15 kHz pilot ücretiyle (`:106`) ve ρ = 30 dB kusurlu CSI'da (`:108`). Bu ya bir kopyalama hatası ya da tesadüf. Sayı denetçisi ham çıktıdan teyit etmeli.
- Fiziksel makullük (doğrulansın): ρ = 30 dB'de hata gücü kanal gücünün yaklaşık 1/1000'i. Bununla etkin hızın 6.08'den 3.54'e (−%42) düşmesi şaşırtıcı. İlk cümle pilot ücreti olmadan verildiği için ("With pilot airtime charged **as well**" ikinci cümlede geliyor) bu düşüş açıklama istiyor. Hakem bunu kesinlikle sorar.

### K6. §V'deki "the findings hold" ifadesi §VI-H'nin kapsamını aşıyor
`section_05_methodology.tex:19`: *"A later re-measurement … gives 1.33 ms per step; Section~\ref{sec:res_robust} shows that the findings hold with it."*
§VI-H'nin "Step time" paragrafı (`section_06_results.tex:104`) yalnızca L*, L = 48'in maliyeti ve SU-best-of − CD farkını yeniden veriyor. Tablo III (periyodik, 1.66 ms ile), Tablo II (hızlar) ve öğrenilen kural ile Adam karşılaştırması (statik küme, ayrı zamanlama) 1.33 ms ile yeniden üretilmemiş. Bu durum `DEGISIKLIKLER.md` "Değiştirilmeyenler" bölümünde de yazıyor.
**Öneri:** *"…gives 1.33 ms per step; with it the optimum, the cost of running to $L=48$ and the loss of coordinate descent are essentially unchanged (Section~\ref{sec:res_robust})."*

Bununla bağlantılı bir mantık sorunu da var. `:104` cümlesinde, SU-best-of ile koordinat inişi arasındaki fark **Adam'ın adım süresine bağlı olmamalı**. İki yöntemin gecikmesi de ayrı ölçülüyor: 2.5 ms ve 107 ms/tarama. Fark 0.297/0.26'dan 0.26'ya (CI 0.15–0.37) değişiyorsa bunun nedeni muhtemelen bağımsız çekilişte seçim. Okur ise bunu adım süresinin etkisi sanar. Ya nedeni bir yan cümleyle yazılmalı ya da bu karşılaştırma "Step time" paragrafından çıkarılmalı.

### K7. "Practical rules" yeni bulguyu içermiyor
`section_07_conclusion.tex:14`: *"Choose the number of steps from $x$ and the acquisition delay, not from convergence."*
§VI-H (`:106`) faz tutma süresi uzadıkça seçilen adım sayısının arttığını gösteriyor: 25/50/100 ms için 5 / 6–8 / 16–20. Tablo III de aynı yönde: uzun periyotta (80 ms) L = 24, back-to-back soğuk başlatmada L = 48. Kural bu haliyle eksik ve yanlış uygulamaya yol açabilir.
**Öneri:** *"Choose the number of steps from $x$, the acquisition delay and how long the phase will be held, not from convergence; because the optimum is flat, a short update loses little even when the phase is held for 100~ms."*
Aynı bilgi şu an Sınırlılıklar'da bir kısıt gibi duruyor: *"The best step count also grows when a phase is held for longer."* Oysa bu bir bulgu. Sınırlılıklar'dan çıkarılıp sonuç maddesi 2'ye taşınmalı (bkz. Ö3).

---

## ÖNERİ

### Ö1. Sınırlılıklar paragrafı (K1 ve K7 için), önerilen metin
`section_07_conclusion.tex:16`, ikinci ve üçüncü cümlenin yerine:

> The main results assume that the BS recomputes its precoder from the current channel with perfect knowledge and that phases are continuous. Charging the precoder pilots lowers absolute rates by up to a third, and estimation error at 20--30~dB lowers them further; in both cases coordinate descent stays significantly behind (Section~\ref{sec:res_robust}). At 10~dB and below, the methods can no longer be told apart, and with 1-bit phases a single coordinate sweep ties the best rounded Adam. The estimation error is modeled as independent Gaussian noise, not through a specific pilot scheme.

Not: "up to a third" ifadesi 5.21 → 3.54 farkından hesaplandı (%32). Sayı denetçisi onaylamalı. Son cümle modeli doğru anlatmıyorsa çıkarılsın.

### Ö2. Özet ve katkı 5
**Özet** (`mobility_paper_ieee.tex:31`): şu an 196 kelime (LaTeX kaynağı) ya da 207 kelime (`pdftotext`, "Abstract—" ve sınırlarla). Önemli bir ayrım var. `TWC_KONTROL_LISTESI.md` #5'e göre [TWC-P] sınırı **75–200 kelime**. Görev tanımındaki 250, IEEE Author Center'ın genel sınırı. Kesin olan sınır 200 sayılmalı, bu yüzden pay yalnızca 4 kelime.
Önerilen değişiklik şu cümleyi değiştiriyor: *"All results assume the precoder is recomputed from the current channel."* (11 kelime). Yerine:
> Slow solvers stay behind when precoder pilots, moderate estimation error and 2--3-bit phases are included.

Bu cümle 15 kelime. Toplam tam 200 olur, sınırda kalır. Pay bırakmak için "in a standardized indoor-office" → "in an indoor-office" yapılabilir (−1).

**Katkı 5** (`section_01_introduction.tex:16`) hâlâ yalnızca taze hüzmeden söz ediyor. Oysa makale artık dört varsayımı fiyatlıyor. Önerilen metin:
> \item \textbf{The price of the assumptions.} The main results assume a precoder refreshed from perfect, current channel knowledge and continuous phases. We measure what precoder pilots, estimation error and 1--3-bit phases cost, and identify where the ranking stops holding.

Bu katkının **Sonuç'ta karşılığı yok**. Beş sonuç maddesi katkı 1–4'e karşılık geliyor, katkı 5'e değil. Altıncı bir madde önerisi:
> \item \textbf{The ranking survives realistic overheads, within limits.} Charging precoder pilots, adding moderate estimation error or rounding phases to 2--3 bits lowers rates but keeps coordinate descent behind; at low estimation SNR or with 1-bit phases the methods converge.

### Ö3. Sonuç maddesi 2 ("A few steps are optimal") ve §VI-E
`section_07_conclusion.tex:7` tek başına doğru: Tanım 1'e göre tek seferlik değerlendirmede tepe birkaç adımda. Ama okur bu maddeyi Tablo III'ün yanında okur. Tabloda 8 hücrenin 3'ünde en iyi politika 24–48 adım kullanıyor (1.71 ve 3.43 ms soğuk, 3.43 ms sıcak). §VI-H de 100 ms tutma süresinde 16–20 adım seçiyor. Önerilen metin:
> \item \textbf{A few steps are optimal, and the optimum is flat.} Adam's effective rate peaks after a handful of steps and falls with further iterations; the optimum moves from 8 steps at 3~km/h to 3 at 10~km/h. When a phase is held for longer the optimum moves up (16--20 steps for 100~ms), but six steps stay within 0.04~b/s/Hz.

§VI-E (`section_06_results.tex:74`): şu iddia tablodan doğrulanamıyor: *"in every row some policy with at most 8 steps is not significantly below the best"*. Tablo III'ün 1.71 ve 3.43 satırlarında görünen en iyi L değerleri 48 / 3 ve 48 / 24. Hangi ≤ 8 adımlık politikanın berabere kaldığı yazılmalı. Ya tabloya "best $L\le 8$" sütunu eklenmeli ya da metne şöyle bir ayrıntı konmalı: *"(at 3.43~ms, warm start with $L=8$ every 80~ms is within …)"*. Alt bölüm başlığındaki "Updates Stay Short" ifadesi de bununla sınırlanmalı. Öneri: "Pilots Set the Period; Short Updates Remain Near-Optimal".

### Ö4. §VI-H'nin yeri, başlığı ve yoğunluğu
**Başlık:** "Remaining Assumptions" ifadesi aşırı. Sabit saçıcılar, RIS anahtarlama süresi, geniş bant ve tek geometri hâlâ ölçülmemiş varsayımlar. Sınırlılıklar paragrafı bunu açıkça söylüyor. Öneri: **"Robustness to Pilots, Estimation Error and Phase Resolution"**.

**Yer:** "Step time" paragrafı bir varsayım değil, ölçüm güncellemesi. Konusu x ve L* olduğu için §VI-C ("One Number Sets the Optimum") sonuna ya da §V-C Timing'e taşınmalı. Böylece §VI-H üç paragraflık, tek temalı bir alt bölüm olur. §VI-G'den sonra gelmesi doğru, çünkü VI-G'nin son cümlesi doğrudan VI-H'ye bağlanıyor.

**Yoğunluk:** Dört paragrafta yaklaşık 35 sayı var. "Precoder pilots" paragrafında tek cümlede 9 sayı ve iki ayrı bulgu (pilot bedeli, tutma süresi) yer alıyor. Önerilen düzen:
1. "Precoder pilots" paragrafı ikiye bölünsün. İkinci paragrafın başlığı: *Phase hold time*.
2. Sayılar küçük bir tabloya taşınsın. Sütunlar: varsayım | koşul | en iyi yöntem ve hızı | en iyi Adam L | CD − en iyi fark (CI). Sayfa sayısı 9, TWC'nin ücretsiz sınırı 10. Bir sütunluk tablo sığar, ama son dizgide biyografiler eklenince sınır izlenmeli.
3. Yeni metrik tanımlansın. "average the rate over the 50 ms after deployment" ne Tanım 1 ne de Tanım 3. Hakem "bu hangi metrik?" diye sorar. Önerilen tanım:
   > For a phase deployed at $\tau_A$ and held for $W$, we report $\bar R^{\mathrm{eff}}_W=\frac{1}{W}\int_{\tau_A}^{\tau_A+W}\min_k R_k(\bs\theta_A;\mathcal H(t))\,dt$, excluding precoder-pilot intervals, with $W=50$~ms unless stated.

   Ardından "best rate" yerine `$\bar R^{\mathrm{eff}}_{50}$` yazılsın. Ayrıca "these values are not comparable with Table I" diye açıkça belirtilsin (bkz. K5).

### Ö5. Seçim protokolü ve "mobility draw"
`section_06_results.tex:102`: *"selected on an independent mobility draw, and CIs are paired on the reported one."*
- "mobility draw" tanımsız. Aynı 400 senaryoda yeni kullanıcı yörüngeleri mi, yoksa yeni senaryolar mı? §V-A tohumu sabitliyor: "seed 11 unless stated otherwise". Bağımsız çekilişin tohumu burada yazılmalı.
- Protokol ana sonuçlardan farklı. §V-D seçim ile raporlamayı aynı senaryolarda yapıyor, §VI-H ayrık çekilişte. Bu iyi bir şey, ama hakem şunu sorar: "ana sonuçlar neden ayrık seçimle yapılmadı, yapılsaydı L* değişir miydi?" Kısa bir cümle bu soruyu önceden karşılar.
- §VI-H'de Adam'ın adım boyu da seçiliyor ("step size"). Ana yaşlanma kümesinde ise adım boyu 0.5'e sabit (§V-B). İki fark (adım süresi ve seçim) aynı anda değişiyor. Bu açıkça söylenmeli.

Önerilen metin:
> The checks below use the aging set with Adam's re-measured step time of 1.33~ms. Unlike the main results, every selected quantity (precoder refresh period, Adam's step count and step size, best method) is chosen on a second set of user trajectories for the same 400 scenarios (seed [·]) and reported on the original trajectories with paired bootstrap CIs.

Köşeli parantez raporlardan doldurulsun. "Aynı senaryolar" doğru değilse metin buna göre değişsin.

### Ö6. "Imperfect channel knowledge" ve "Discrete phases" paragraflarının mantığı
- `:108`: *"the precoder from a fresh estimate"*. Hangi anın kestirimi? Dağıtım anı mı, her T_r'de mi? *"leads SU-best-of by 0.05–0.06"*: tek bir karşılaştırma için aralık verilmiş. Aralık büyük olasılıkla üç alt taşıyıcı aralığından geliyor. Bu yazılmalı: "(15--60 kHz)". *"the methods cannot be told apart"*: CD de dahil mi? Dahilse bu, Sonuç madde 1'in sınırı demektir (bkz. K1).
- `:110`: karşılaştırılan yöntemler cümle içinde değişiyor. 3 ve 2 bitte CD, yuvarlanmış SU-best-of'a karşı; 1 bitte en iyi yuvarlanmış Adam'a karşı. 2 bitte tek tarama ile 1 bitte SU-best-of'a karşı ne olduğu belirsiz. "Rounding" de tanımsız: hangi ızgaraya, en yakın noktaya mı, optimizasyondan sonra mı? Önerilen metin:
  > \emph{Discrete phases.} We round each method's continuous output to the nearest of $2^b$ uniformly spaced levels, $b\in\{1,2,3\}$, and run coordinate descent directly on the $2^b$ levels (16--501~ms). Rounded Adam keeps an intrinsic optimum ($L^\star=5$, 6 and 6; running to $L=48$ costs 9.5, 14.1 and 14.9\%). Against the best fast method (rounded SU-best-of or rounded Adam), coordinate descent is significantly behind at 3 bits with any number of sweeps and at 2 bits with two or more sweeps; at 1 bit a single sweep is statistically tied with the best rounded Adam.

  Bu metin karşılaştırılan yöntemi her bit için açıkça söylüyor. Yazarlar 2 bit/tek tarama ve 1 bit/SU-best-of durumlarını rapordan ekleyebilir.
- Bulgu tezin önceki tek-RIS sonucuyla yan yana konunca önem kazanıyor: 1 bitte ayrık CD kazanmıştı. 1 bitte yavaş çözücü avantajını geri kazanıyor ve bu Sonuç'ta açıkça söylenmeli (Ö2, altıncı madde).

### Ö7. Terminoloji birliği
| Kavram | Şu an kullanılanlar | Öneri |
|---|---|---|
| Ön kodlayıcı | "precoder" (§III–§VI-H), "beam" (§VI-G, Tablo, katkı 5'teki "fresh-beam") | Başlıkta "Fresh-Beam" kalabilir. Metinde ilk geçtiği yerde "(fresh beam: precoder recomputed from the current channel)" diye eşlenmeli. |
| Ön kodlayıcı türü | "regularized zero-forcing" (§III:10), "zero-forcing precoder" (§VI-H:106) | Her yerde "regularized zero-forcing" ya da "the precoder of Section III". |
| Yenileme | "refresh", "recompute", "recomputed" | Ön kodlayıcı için "refresh", faz için "update". "update period" yalnızca U için kullanılsın. |
| Tutma | "Holding the phase for longer", "averaged over 25, 50 and 100 ms" | Tek bir sembol: W ("hold time"). U ile ilişkisi tek cümleyle verilsin: tutma süresi ≈ U − T_p − LΔT. |
| Hız metriği | "effective rate", "best rate", "best effective rate", "time-averaged effective rate", "rate" | §VI-H'deki "best rate" ifadeleri `$\bar R^{\mathrm{eff}}_{W}$` olsun (Ö4). |
| Yineleme | "steps", "iterations" (madde 2, özet), "sweeps" (CD) | "iteration" yalnızca genel anlamda, "step" Adam/Armijo/PGA için, "sweep" CD için (§V-B'de tanımla: "one sweep updates every element once"). |
| Alt taşıyıcı | "15, 30 and 60 kHz spacing" (§VI-H:106) | "subcarrier spacing", §V-D ile aynı. |

### Ö8. Hakemin büyük olasılıkla soracakları (cevabı metne konmalı)
1. Ön kodlayıcı pilotları için 4 simge kullanılıyor, faz için kaskad kestirim 48 simge. 50 ms boyunca faz kestirimi yenilenmiyor mu? Tutma süresinde fazın pilot maliyeti nerede sayılıyor?
2. T_r = 1–2 ms seçilmiş. 15 kHz'te 4 simge ≈ 0.29 ms, yani her ms'de yaklaşık %29 ek yük demek. Bu oran 5.21 → 3.54 düşüşünü açıklıyor mu? Bir cümleyle söylenirse okur K5'teki şaşkınlığı yaşamaz.
3. Kusurlu CSI'da öğrenme ya da sağlam (robust) bir tasarım denendi mi? Denenmediyse Sınırlılıklar'a yazılmalı.
4. 1 bitte CD berabere kaldığına göre, pratik 1 bitlik yüzeyler için öneri ne?

---

## KÜÇÜK

1. `section_06_results.tex:104`: "$L^\star=6$" için bir güven aralığı ya da "within 0.5 %" aralığı verilmemiş. Ana metinde hep aralık var (örneğin "4–6"). Tutarlılık için "6 (range …)" yazılmalı.
2. `section_06_results.tex:106`: *"with differences of at most 0.04~b/s/Hz to six steps at 100~ms"* ifadesi bozuk İngilizce. Önerilen: *"at 100~ms, six steps are within 0.04~b/s/Hz of the selected count"*.
3. `section_06_results.tex:106`: *"consistent with Table~\ref{tab:tracking}"*. Tablo III 1.66 ms ile, §VI-H 1.33 ms ile hesaplanmış, üstelik metrikler farklı. "qualitatively consistent" yazılmalı.
4. `section_06_results.tex:102`: *"CIs are paired on the reported one"* ifadesi hem belirsiz hem bozuk. Ö5'teki metin önerilir.
5. `section_06_results.tex:108`: *"the phase computed from the estimate and the precoder from a fresh estimate"* mutlak yapı (absolute construction) ve ağır okunuyor. Öneri: *"…on all channels; the phase is computed from the estimate available at $t=0$ and the precoder from a fresh estimate at deployment"* (gerçek kurguya göre).
6. `section_05_methodology.tex:19`: *"this value lies within the 1.49–2.02 ms measured here. A later re-measurement … gives 1.33 ms"*. "measured here" ile "later" yan yana gelince, 1.33 ms'nin bu aralığın **dışında** olduğu gözden kaçıyor. Bu bir cümleyle söylenmeli. Hakem "neden ana sonuçlar 1.33 ile verilmiyor?" diye sorar. Önerilen ek: *"…; we keep 1.66 ms for the main results, which makes Adam slower and therefore, if anything, understates its optimum."* Bu ekleme ancak 1.33 ms ile L* gerçekten büyüyorsa doğru olur (4–6 → 6). Sayı denetçisi onaylamalı.
7. `section_05_methodology.tex:26`: *"A separate audit script checks 123 assertions"*. Proje kayıtları (CLAUDE.md) 111/126 iddiadan söz ediyor. Sayı güncel olmayabilir, sayı denetçisine aktarılsın.
8. `section_05_methodology.tex:22`: "14.0 % to 14.2 %" (tam gecikme) ve `section_06_results.tex:57` "14.2 % (14.0 % in the main sweep)" (ince ızgara) iki farklı yöntemle aynı sayıyı veriyor. Okur bu ikisini karıştırabilir. §V'deki cümleye "(the same value as on the finer grid of Table II)" eklenebilir.
9. `section_06_results.tex:106`: *"with $R$ chosen per method"* ve hemen ardından *"with $R=1$--2 ms"*. Bu aralık hangi yöntemlerin seçimi, belirtilmeli.
10. PDF'te §VI-H, tam genişlikteki Şekil 5 yüzünden 7. ve 8. sayfa arasında bölünüyor. Son dizgide sorun olmaz, ama gözden geçirme kopyasında okumayı zorlaştırıyor. `fig:eqms` için `[t]` yerleşimi bir sayfa önce zorlanabilir.
11. `tables/tab_beam_staleness.tex`, `tab_model.tex`, `tab_equal_step.tex`, `tab_equal_ms.tex` ve `tab_cnnlstm.tex` derlemeye girmiyor. Bu bilinçli olabilir, ama §VI-G'deki 11.7–14.2× tablosuz verildiği için okur kaynağını göremiyor. Sorun değil, bilgi notu.
12. Özet: "lose to a 2.5 ms single-user heuristic" ifadesinde "single-user heuristic" ilk kez geçiyor ve SU-best-of olduğu yazılmıyor. Özet için kabul edilebilir.
13. Anahtar kelimeler 5 tane (TWC/IEEE'nin 3–5 sınırına uygun). Revizyon dayanıklılık bulguları eklediği için "imperfect CSI" ya da "discrete phase" eklenmesi düşünülebilir, ama o zaman bir terim çıkarılmalı. Öneri: değiştirme.
14. LaTeX: `\ref` hatası ya da tanımsız etiket yok (`mobility_paper_ieee.log`). `sec:res_robust` üç yerde doğru çözülüyor (§V-C, §VI-G, §VII). 5 overfull/underfull uyarısı var, ama hiçbiri yeni metinden kaynaklanmıyor gibi görünüyor. Görsel kontrol önerilir.

---

## TWC uyum özeti

| Ölçüt | Durum |
|---|---|
| Sayfa | 9 (`pdfinfo`). Ücretsiz sınır 10, üst sınır 13. Uygun, ama biyografilerle son dizgide 10'a yaklaşır. Ö4'teki tablo eklenirse tekrar kontrol edilmeli. |
| Özet uzunluğu | 196 kelime (kaynak) / 207 (`pdftotext`, başlık dahil). [TWC-P] sınırı 75–200 (`TWC_KONTROL_LISTESI.md` #5). Görevdeki 250 genel IEEE sınırı. Uygun, ama yalnızca 4 kelimelik pay var. Özete her eklemede bir şey çıkarılmalı. |
| Özet içeriği | Sembol yok, kısaltmalar açık. Uygun. |
| Anahtar kelimeler | 5. Uygun. |
| Dil | Yeni metin dışında akıcı. §VI-H'de ağır mutlak yapılar ve tanımsız kısa yollar var (K3, K4, KÜÇÜK 2, 4, 5). |
