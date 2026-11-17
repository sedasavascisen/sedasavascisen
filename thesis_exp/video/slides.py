# -*- coding: utf-8 -*-
"""
Slide content and narration for the thesis-defence video (thesis_exp/video/build_video.py).
Every number is taken from a committed, audited report; the source is noted next to each slide.
Code excerpts are copied from the repository files named on the slide (shortened with "...").
Narration is written for speech: symbols spelled out (L*, ms, b/s/Hz).
"""

SLIDES = []


def S(kind, title, body, say, src=""):
    SLIDES.append(dict(kind=kind, title=title, body=body, say=say.strip(), src=src))


# 1 -------------------------------------------------------------------------------------------
S("title", "Hareketli RIS sistemlerinde hesaplama gecikmesi",
  """<div class="sub">Ölç, yasasını çıkar, onu kullanan bir denetleyici tasarla</div>
<div class="who">Seda Savaşçı Şen · Doktora tezi savunması · Kasım 2026</div>""",
  """Sayın jüri üyeleri, bu tezde yeniden yapılandırılabilir akıllı yüzeylerin, yani RIS'in, hareketli kullanıcılar için nasıl tasarlanması gerektiğini inceledim.
Tezin tek cümlelik iddiası şudur: hareketli RIS sistemlerinde hesaplama gecikmesi ikincil bir ölçüt değil, yöntemlerin sıralamasını belirleyen birinci sınıf bir tasarım kısıtıdır.
Bu videoda önce problemi ve senaryoyu, sonra kodları ve ölçümleri, en sonunda da bu kısıtı kullanan, tasarladığım denetleyiciyi anlatacağım.""")

# 2 -------------------------------------------------------------------------------------------
S("text", "Problem: kanal, karar verilene kadar değişir",
  """<ul>
<li>Yürüyen bir kullanıcı kanalı <b>onlarca milisaniyede</b> değiştirir (3 GHz, 1.5 m/s: eşevreli kalma süresi 28.2 ms).</li>
<li>Dikkatli bir çözücü <b>saniyeler</b> sürebilir.</li>
<li>Literatür yöntemleri genellikle <b>verildiği kanal üzerinde</b> karşılaştırır.</li>
<li>Bu tezin sorusu: <b>zaman sayılınca hangi yöntem, ne kadar süre çalıştırılmalı?</b></li>
</ul>""",
  """Problem şu. Yürüyen bir kullanıcı kanalı onlarca milisaniyede değiştirir. Üç gigahertzde, saniyede bir buçuk metre hızla yürüyen bir kullanıcı için eşevreli kalma süresi yaklaşık yirmi sekiz milisaniyedir.
Oysa dikkatli bir optimizasyon algoritması saniyeler sürebilir. Cevap hazır olduğunda soru değişmiştir.
Literatürde yöntemler çoğunlukla kendilerine verilen kanal üzerinde karşılaştırılır. Ben ise her yöntemi, işini bitirdiği anda var olan kanal üzerinde değerlendirdim.""",
  "Makale 2, Giriş; T_c = √(9/(16π))/f_d")

# 3 -------------------------------------------------------------------------------------------
S("figure", "Senaryo: kapalı ofis, yürüyen kullanıcılar",
  """<img src="../img/fig_scenario.png"><div class="cap">40×20×6 m oda · duvara monte 32 elemanlı RIS · 8 antenli baz istasyonu · 4 kullanıcı, 1.5 m/s · 3 GHz · 3GPP TR 38.901 kanal modeli · 20 saçıcı</div>""",
  """Senaryom kırk metreye yirmi metrelik, altı metre yüksekliğinde bir ofis. Duvarda otuz iki elemanlı bir RIS, karşısında sekiz antenli bir baz istasyonu var.
Dört kullanıcı saniyede bir buçuk metre hızla düz çizgiler boyunca yürüyor. Doğrudan yollar engellenmiş, yani kullanıcılara asıl katkı RIS üzerinden geliyor.
Büyük ölçekli kanal parametreleri 3GPP TR otuz sekiz dokuz yüz bir modelinden geliyor. Kullanıcılar hareket ettikçe kanal geometriden her an yeniden hesaplanıyor.""",
  "Makale 2, Şekil 1 ve §III")

# 4 -------------------------------------------------------------------------------------------
S("code", "Kod 1: kanal zamanla nasıl eskiyor?",
  """<div class="file">thesis_exp/p4/common.py · ris_mu/mumiso/mobile.py</div>
<pre>class Aging:
    def __init__(self, seed, times, v=1.5, n=400, clusters=20, ...):
        panel, base = make_mumiso_scenario(n_users=4, n_bs_antennas=8, seed=seed)
        cfg = MobileConfig(**{**base.__dict__, "velocity": v,
                              "times_ms": tuple(times), "n_clusters": clusters})
        self.d = MobileMuMisoChannel(panel, cfg).generate(n)
        self.G = [... self.d["G_t"][:, m] ...]   # RIS–kullanıcı kanalı, her zaman anında
        self.H = [... self.d["hd_t"][:, m] ...]  # doğrudan kanal, her zaman anında</pre>
<ul class="small"><li>Saçıcılar, yol kazançları, gölgeleme ve BS–RIS kanalı <b>sabit</b>; yalnızca kullanıcılar hareket eder.</li>
<li>Aynı tohum → aynı senaryolar; ızgara t = 0 ile başlar.</li></ul>""",
  """Kanalın nasıl eskidiğini bu sınıf modelliyor. Her senaryo için bir tohum ve bir zaman listesi veriyorum; üreteç, kullanıcıların o anlardaki konumlarına göre RIS–kullanıcı ve doğrudan kanalları yeniden hesaplıyor.
Saçıcılar, yol kazançları ve baz istasyonu ile RIS arasındaki kanal sabit tutuluyor. Değişen tek şey kullanıcıların konumu. Böylece kanal, rastgele değil, geometriye bağlı olarak sürekli değişiyor.
Bütün deneylerde aynı tohumları kullandım: seçim için on iki, rapor için on bir. Böylece her karşılaştırma aynı dört yüz senaryo üzerinde ve eşleştirilmiş olarak yapılıyor.""")

# 5 -------------------------------------------------------------------------------------------
S("code", "Kod 2: etkin hız, yöntemin kendi gecikmesinde",
  """<div class="file">thesis_exp/p4/common.py</div>
<pre>def adam(self, start, L, lr=0.5):            # faz, t = 0 kanalında optimize edilir
    ...
    for _ in range(L):
        R = S.rates(F, G0, H0, cos(th), sin(th), pt, nv, "zf")
        (-(-logsumexp(-8 * R, -1) / 8).mean()).backward(); opt.step()

def minrate(self, th, m):                   # ... ama m anındaki kanalda ölçülür
    return S.rates(F, G[m], H[m], cos(th), sin(th), pt, nv, "zf").min(-1).values

eff = A.minrate(phase, A.idx(latency_ms))   # etkin hız: kendi gecikmesinde, tam olarak</pre>
<div class="def"><b>Etkin hız:</b> fazın, yöntemin işini bitirdiği anda var olan kanaldaki en kötü kullanıcı hızı.</div>""",
  """Tezin ana ölçütü etkin hız. Faz, sıfır anındaki kanal üzerinde hesaplanıyor; ama hız, yöntemin işini bitirdiği andaki kanal üzerinde ölçülüyor.
Kodda bu iki satır: adam fonksiyonu fazı sıfır anındaki kanalda optimize ediyor; minrate fonksiyonu ise o fazı, gecikme kadar sonraki kanalda değerlendiriyor.
Önemli bir ayrıntı: değerlendirmeyi enterpolasyonla değil, her yöntemin tam gecikme anında yaptım. Kaba bir zaman ızgarasından enterpolasyon yapmanın sonuçları kaydırdığını denetimlerde gördüm ve düzelttim.""")

# 6 -------------------------------------------------------------------------------------------
S("code", "Kod 3: gecikme nasıl ölçüldü?",
  """<div class="file">scripts/mumiso_mobility_latency.py · thesis_exp/juri/timing2.py</div>
<pre>while os.getloadavg()[0] >= 0.5:      # makine boşalana kadar bekle
    time.sleep(15)
torch.set_num_threads(1)              # tek iş parçacığı
...
for r in range(5):                    # 5 tur
    rounds[k].append(med_ms(fn, reps, warm))   # her turda medyan
med = {k: float(np.median(v)) for k, v in rounds.items()}</pre>
<ul class="small"><li>Tek senaryo, tek iş parçacığı, ısınma turları, 5 turun medyanı; yük öncesi ve sonrası kayıtlı.</li>
<li>Örnek: bir Adam adımı ≈ 1.1–1.3 ms; koordinat inişi ≈ 0.5–0.9 s; SU-best-of ≈ 1.2–2.5 ms.</li></ul>""",
  """Gecikmeyi ölçmek bu tezde bir yan iş değil, ana ölçümün kendisi. Bu yüzden katı bir protokol kullandım.
Makine boşalana kadar bekledim, tek iş parçacığıyla çalıştım, ısınma turlarından sonra beş turun medyanını aldım ve ölçüm öncesi ile sonrası yükü kaydettim.
Bu önemli, çünkü bir ölçümde eğitim arka planda çalışırken alınan sayılar yanlış bir sonuç üretmişti. Ölçümü boş makinede tekrarladığımda sonuç tersine döndü. O günden sonra her gecikme bu protokolle ölçüldü.""",
  "CLAUDE.md, ölçüm tuzakları")

# 7 -------------------------------------------------------------------------------------------
S("figure", "Sonuç 1: kâğıt üzerindeki en iyi yöntemler kaybediyor",
  """<table class="t"><tr><th>Yöntem</th><th>t = 0 hızı</th><th>Gecikme</th><th>Etkin hız</th></tr>
<tr><td>SU-best-of (sezgisel)</td><td>5.276</td><td>2.5 ms</td><td><b>5.272</b></td></tr>
<tr><td>Adam, L = 8</td><td>6.443</td><td>13.3 ms</td><td><b>5.849</b></td></tr>
<tr><td>Koordinat inişi</td><td>6.925</td><td>880.8 ms</td><td>4.975</td></tr>
<tr><td>Uzun koşulu Adam</td><td>7.117</td><td>5851.7 ms</td><td>4.667</td></tr></table>
<div class="cap">b/s/Hz, en kötü kullanıcı · SU-best-of, koordinat inişinin 0.297 [0.204, 0.390], uzun koşulu Adam'ın 0.604 [0.415, 0.805] önünde</div>""",
  """İlk sonuç. Tabloda soldan ikinci sütun yöntemlerin sıfır anındaki hızı. Bu sütuna bakarsanız en iyi yöntemler koordinat inişi ve uzun koşulu Adam.
Ama onlar sıfır virgül dokuz ve beş virgül dokuz saniye sürüyor. O sürede kullanıcılar metrelerce yürüyor. Etkin hızlarına baktığımızda iki buçuk milisaniyelik basit bir sezgisel yöntemin gerisine düşüyorlar.
Sıralama tersine dönüyor. Ve bu bir bütçe yapaylığı değil: koordinat inişinin tek bir taraması bile yüz yedi milisaniye, yani yaklaşık dört eşevreli kalma süresi.""",
  "Makale 2, Tablo II ve §VI-A")

# 8 -------------------------------------------------------------------------------------------
S("figure", "Sonuç 2: bir içsel optimum var",
  """<img src="../img/fig_intrinsic_optimum.png"><div class="cap">1.5 m/s'de en iyi adım sayısı L* = 4–6 · 48 adıma kadar koşmak %14 kaybettirir · 10 km/h'de L* = 3</div>""",
  """İkinci sonuç: daha fazla iterasyon her zaman daha iyi değil. Adam'ın adım sayısı arttıkça sıfır anındaki hız yükseliyor ama gecikme de artıyor.
İkisi dengelendiğinde bir optimum çıkıyor. Saniyede bir buçuk metrede en iyi adım sayısı dört ile altı arası. Kırk sekiz adıma kadar koşmak yüzde on dört kaybettiriyor. Saatte on kilometrede optimum üç adıma iniyor.
Bu optimumu iç optimum diye adlandırdım. Daha sonra jüri sorusu olarak, korelasyon tabanı olmayan bir Clarke kanalında da var olduğunu gösterdim.""",
  "Makale 2, Şekil 3; jüri S2")

# 9 -------------------------------------------------------------------------------------------
S("figure", "Sonuç 3: optimumu tek bir sayı belirler",
  """<img src="../img/fig_step_scaling.png"><div class="cap">x = ΔT · f_d (adım süresi × Doppler) · L* ≈ x<sup>−2/(γ+2)</sup>, ölçülen üs −0.675 · yüz kat hızlı uygulamada yakınsama neredeyse bedava</div>""",
  """Üçüncü sonuç, bir ölçekleme yasası. Optimumun yeri tek bir sayıya bağlı: adım süresi çarpı Doppler frekansı. Buna x dedim.
Küçük gecikme yaklaşımıyla en iyi adım sayısının x üzeri eksi iki bölü gama artı iki gibi ölçeklendiğini türettim; ölçtüğüm üs eksi sıfır virgül altı yüz yetmiş beş.
Bunun pratik anlamı şu: daha hızlı bir donanım optimumu kaydırır ama yok etmez. Adım zaman aldığı sürece bir optimum vardır.""",
  "Makale 2, §IV ve Şekil 4")

# 10 ------------------------------------------------------------------------------------------
S("figure", "Sonuç 4: öğrenilen kural adım başına kazanır, milisaniye başına kaybeder",
  """<img src="../img/fig_equal_step_vs_ms.png"><div class="cap">Öğrenilen güncelleme kuralı eşit adımda Adam'ın önünde · ölçülmüş süreyle bütün öğrenilen yapılandırmalar Adam eğrisinin altında ve sağında</div>""",
  """Dördüncü sonuç yapay zekâ ekseniyle ilgili. Adam'ın adımlarını öğrenen bir ağ eğittim.
Eşit adım sayısında bu ağ Adam'ın önünde. Literatürde genellikle bu karşılaştırma raporlanır. Ama her adımı ölçülmüş süresiyle saydığımda, öğrenilen bütün yapılandırmalar Adam eğrisinin altında ve sağında kalıyor. Yani adım başına kazanıyor, milisaniye başına kaybediyor.
Bu tezin önemli olumsuz sonuçlarından biri ve bir değerlendirme protokolü öneriyor: öğrenilen yöntemler ölçülmüş süreyle, her bütçede ayarlanmış klasik rakiplere karşı sınanmalı.""",
  "Makale 2, Şekil 5")

# 11 ------------------------------------------------------------------------------------------
S("text", "Tasarım kuralı: optimumu önceden seçmek",
  """<div class="eq">R̂(L) = R<sub>taban</sub> + (R<sub>0</sub>(L) − R<sub>taban</sub>) · ψ̄(f<sub>d</sub>τ, f<sub>d</sub>W)</div>
<ul><li>ψ: eskime eğrisi, yalnızca 1.5 m/s'de ve seed 12'de kalibre edildi.</li>
<li>Ön kayıtlı sınama: hiç görülmemiş çekiliş (seed 13), 60 koşul, 18–30 km/h dahil.</li>
<li><b>Medyan kayıp %0.08</b>, en kötü %2.74 · sabit L = 48: ortalama %3.6 · sabit L = 5: %3.0</li></ul>""",
  """Bu yasayı bir tasarım kuralına çevirdim. Kural, her aday adım sayısı için etkin hızı öngörüyor: sıfır anındaki hız, eskime eğrisiyle ağırlıklandırılıyor.
Eğriyi yalnızca bir hızda ve bir çekilişte kalibre ettim. Sonra kuralı, sonuçları görmeden önce kayda aldığım bir protokolle, hiç görmediği bir çekilişte ve hiç görmediği hızlarda sınadım.
Altmış koşulda doğru adım sayısını seçmeye göre medyan kayıp yüzde sıfır virgül sıfır sekiz, en kötü yüzde iki virgül yetmiş dört. Sabit bir adım sayısı seçmek ise ortalama yüzde üç ile üç virgül altı kaybettiriyor.""",
  "thesis_exp/tasarim_kurali/REPORT.md")

# 12 ------------------------------------------------------------------------------------------
S("text", "Jürinin olası soruları: ön kayıtlı deneylerle",
  """<table class="t sm"><tr><th>Soru</th><th>Ölçülmüş cevap</th></tr>
<tr><td>CD'yi C ile yazsaydınız?</td><td>Yalnız CD derlenirse (62–63 kat) Python Adam'ı geçer. Hepsi eşit hızlanırsa (1–1000 kat) Adam her noktada önde. <b>Sıralamayı dil değil, gecikme oranı belirler.</b></td></tr>
<tr><td>L* modelin yapaylığı mı?</td><td>Korelasyon tabanı olmayan Clarke kanalında da var: L* = 3–8, L = 48 kaybı %27–32.</td></tr>
<tr><td>Ryu ve ark.'tan farkınız?</td><td>Süreyi yalnızca bütçe kısıtı yapan seçim 0.43–1.41 b/s/Hz kaybettirir. Fark: süreyi eskimeye katmak.</td></tr>
<tr><td>Ön kodlayıcı da eskirse?</td><td>~1 ms'de çöküş (5.41 → 4.03). Ön kodlayıcı her slotta tazelenmeli: iki zaman ölçeği zorunlu.</td></tr></table>""",
  """Savunmaya hazırlanırken jürinin sorabileceği en zor soruları kendime sordum ve her birini ön kayıtlı bir deneyle yanıtladım.
Koordinat inişini C ile yazsaydım ne olurdu? Yalnız onu derlersem Python Adam'ı geçiyor; bunu açıkça yazıyorum. Ama bütün yöntemler eşit hızlandırılırsa Adam her noktada önde kalıyor. Yani sıralamayı programlama dili değil, gecikme oranı belirliyor.
İç optimum modelin bir yapaylığı mı? Hayır, korelasyon tabanı olmayan bir kanalda da var.
Ryu ve arkadaşlarından farkım ne? Süreyi yalnızca bir bütçe kısıtı olarak kullanmak bir virgül dörde kadar kaybettiriyor; benim katkım süreyi kanal eskimesine katmak.
Ön kodlayıcı da eskirse? O zaman her şey bir milisaniyede çöküyor. Bu, ön kodlayıcının her slotta tazelenmesinin bir tercih değil zorunluluk olduğunu gösteriyor.""",
  "thesis_exp/juri/REPORT_S3_S1.md, REPORT_S4_S2.md")

# 13 ------------------------------------------------------------------------------------------
S("text", "Geniş bant OFDM: zaman bütçesinin ikinci ekseni",
  """<ul><li>Tek RIS faz vektörü bütün alt taşıyıcılara hizmet eder; optimizasyona <b>K_opt</b> alt taşıyıcı alınır.</li>
<li>Her ek alt taşıyıcı adımı pahalılaştırır: K_opt = 16'da adım ~9 kat pahalı.</li>
<li><b>20 MHz:</b> dar bant amacı yeter. <b>100 MHz:</b> K_opt = 16 seçilir, en iyi dar bant kolunu <b>+0.28…+0.29</b> geçer (200 ms ufku içinde de).</li>
<li>Dürüst sınır: iç optimum dar banda özgü; 50–100 MHz'de 16 hücrenin yalnızca 3'ünde L = 48 anlamlı kötü.</li></ul>""",
  """Tezin son deneysel adımı geniş bant. OFDM'de tek bir RIS faz vektörü bütün alt taşıyıcılara hizmet ediyor. Optimizasyona kaç alt taşıyıcı alacağım da bir karar, çünkü her ek alt taşıyıcı adımı pahalılaştırıyor.
Yirmi megahertzde dar bant amacı yetiyor. Yüz megahertzde ise on altı alt taşıyıcı üzerinden optimize etmek, adım dokuz kat pahalı olmasına rağmen en iyi dar bant kolunu sıfır virgül yirmi sekiz geçiyor.
Yani gecikme geniş bantta da kararı belirliyor, ama artık iki eksende: kaç adım ve kaç alt taşıyıcı. Burada dürüst bir sınır da var: dar banttaki iç optimum geniş bantta genelleşmiyor. Bunu makalede açıkça yazdım.""",
  "thesis_exp/genis_bant/REPORT.md")

# 14 ------------------------------------------------------------------------------------------
S("code", "Tasarlanan sistem: gecikme farkındalıklı denetleyici",
  """<div class="file">thesis_exp/sistem/controllers.py, periodic.py</div>
<pre>for a in arms:                           # aday hat: başlangıç + Adam L adımı
    tau = lat[a]                         # bu donanımda ölçülmüş gecikme
    u, b = f_d * tau / 1000, f_d * W / 1000
    r = R_floor + (R0[a] - R_floor) * psi_bar(u, b)   # öngörülen etkin hız
    if r > best_value: best, best_value = a, r
return best                              # SU-avg / SU-best-of / önceki faz × L</pre>
<ul class="small"><li><b>Girdiler:</b> Doppler kestirimi, taşıyıcı, ölçülmüş gecikmeler, faz tutma süresi W, varsa önceki faz.</li>
<li><b>Karar:</b> başlangıç noktası ve adım sayısı; 28 GHz'de taşıyıcıya özgü eskime eğrisi.</li></ul>""",
  """Şimdi tezin tasarım katkısına geliyorum. Yukarıdaki yasaları birleştirerek gecikme farkındalıklı bir denetleyici tasarladım.
Denetleyici her güncellemede aday hatları değerlendiriyor: başlangıç noktası olarak SU-average, SU-best-of ya da periyodik çalışmada bir önceki fazı alıyor, üzerine sıfır ile kırk sekiz arası Adam adımı ekliyor.
Her aday için ölçülmüş gecikmeyi ve Doppler kestirimini kullanarak etkin hızı öngörüyor ve en yüksek öngörüyü veren hattı seçiyor. Kod bu kadar kısa; çünkü işi yapan, daha önce ölçülen ve doğrulanan yasalar.""")

# 15 ------------------------------------------------------------------------------------------
S("text", "Mühürlü test: hiç görülmemiş çekilişte, tek sefer",
  """<table class="t sm"><tr><th>Karşılaştırma (seed 41, 12 koşul)</th><th>Sistem − karşılaştırma [%95 GA]</th></tr>
<tr><td>SU-best-of</td><td>+0.434 [+0.397, +0.470]</td></tr>
<tr><td>Gecikmeyi yok sayan Adam-48</td><td>+0.434 [+0.393, +0.475]</td></tr>
<tr><td>Makalenin kapalı formu</td><td>+0.097 [+0.077, +0.118]</td></tr>
<tr><td>Kapalı form, SU-best-of başlangıçlı</td><td>+0.040 [+0.029, +0.052]</td></tr>
<tr><td>Seed 12'de seçilen en iyi sabit hat</td><td>+0.087 [+0.072, +0.102]</td></tr>
<tr><td>Periyodik kip: sıcak başlangıcın katkısı</td><td>+0.051 [+0.037, +0.066]</td></tr></table>
<div class="cap">Kâhine (geriye dönük en iyi seçim) uzaklık: 0.0026 b/s/Hz · ön kayıtlı H1, H2, H3 tuttu · 362/362 bağımsız denetim</div>""",
  """Denetleyiciyi bir gece boyunca geliştirdim, her fikri yalnızca geliştirme çekilişinde sınadım ve başarısız olanlar dahil bütün denemeleri günlüğe yazdım. Sonra son sürümü dondurdum ve gece hiç dokunulmayan bir çekilişte tek bir kez test ettim.
Sonuç: denetleyici beş karşılaştırma yönteminin hepsini anlamlı farkla geçiyor ve geriye dönük olarak mümkün olan en iyi seçime yalnızca sıfır virgül sıfır sıfır üç uzaklıkta.
Bağımsız denetim daha güçlü taban çizgilerini de sordu. En iyi sabit hatta karşı fark sıfır virgül sıfır seksen yedi, başlangıcı da iyi seçilmiş kapalı forma karşı sıfır virgül sıfır kırk. Kazancın kaynaklarını ayrı ayrı raporluyorum: başlangıç seçimi, adım sayısı seçimi ve periyodik çalışmada sıcak başlangıç.""",
  "thesis_exp/sistem/FINAL.md, FINAL_EK.md")

# 16 ------------------------------------------------------------------------------------------
S("text", "Yapay zekâ ekseni: en elverişli rejimde de olumsuz",
  """<ul><li>28 GHz, 1.5 m/s: eşevreli kalma süresi ~3 ms — öğrenmeye en elverişli rejim.</li>
<li>0.43 ms'lik tek geçişli ağ, 1.24 ms'lik SU-best-of'un <b>0.38</b> gerisinde.</li>
<li>4 kat veri, 3 tohum, 2 kat geniş ağ: yine <b>−0.31…−0.36</b>.</li>
<li>Ağ öğreniyor (optimizasyonsuz SU-average'ı +0.04…+0.09 geçiyor), ama kalite tavanı düşük.</li>
<li>sin/cos ile doğrudan açı farkı 3 tohumdan yalnızca 1'inde anlamlı.</li></ul>""",
  """Yapay zekâ eksenini de dürüstçe kapattım. Öğrenmenin klasiği yenme şansının en yüksek olduğu rejimi bilerek aradım: yirmi sekiz gigahertz, eşevreli kalma süresi yaklaşık üç milisaniye.
Sıfır virgül kırk üç milisaniyede karar veren tek geçişli ağ, bir virgül yirmi dört milisaniyelik basit sezgiselin gerisinde kaldı. Veriyi dört katına çıkardım, üç farklı tohum ve iki kat geniş bir ağ denedim; açık daraldı ama kapanmadı.
Ağ gerçekten öğreniyor, ama kalite tavanı basit yöntemin altında. Bu sonuç bu mimari ailesi ve bu bütçe için geçerli. Tezde öğrenmenin katkısı bir yöntem olarak değil, bir değerlendirme protokolü olarak kalıyor.""",
  "thesis_exp/juri/REPORT_S5.md, REPORT_S5b.md")

# 17 ------------------------------------------------------------------------------------------
S("text", "Dürüst sınırlar",
  """<ul><li>Tek geometri, tek kanal modeli (Clarke kanalı sağlamlık kontrolü olarak).</li>
<li>Gecikmeler tek iş parçacıklı Python'da; sıralama gecikme oranına bağlı.</li>
<li>RIS eleman kazancı Tang ve ark.'tan farklı: mutlak hızlar ~%5 yüksek, L* ve en iyi yöntem değişmiyor.</li>
<li>Ana sonuçlarda kusursuz CSI; pilot, kestirim hatası ve 1–3 bit faz ayrıca sınandı.</li>
<li>İç optimum dar banda özgü; ön kodlayıcının her slotta tazelenmesi gerekir.</li></ul>""",
  """Her tez gibi bu tezin de sınırları var ve bunları açıkça yazdım.
Tek bir geometri ve tek bir kanal modeli kullandım; Clarke kanalı yalnızca bir sağlamlık kontrolü. Gecikmeleri tek iş parçacıklı Python'da ölçtüm; bu yüzden sıralamanın gecikme oranına bağlı olduğunu ayrıca gösterdim.
Kaynak kontrolünde, RIS eleman kazancının Tang ve arkadaşlarının formülünden farklı olduğunu buldum. Etkisini ölçtüm: mutlak hızlar yaklaşık yüzde beş yüksek, ama optimum adım sayısı ve en iyi yöntem değişmiyor. Makalede bunu tek cümleyle belirttim.
Ön kayıt, mühürlü test ve bağımsız denetimler, bu sınırların sonuçları nerede etkilediğini görmemi sağladı.""",
  "Makale 2, §III ve §VII; thesis_exp/kazanc_duyarlilik")

# 18 ------------------------------------------------------------------------------------------
S("title", "Sonuç",
  """<div class="sub">Gecikme, hareketli RIS'te yöntem sıralamasını belirler.</div>
<ul class="concl"><li><b>Ölçüt:</b> etkin hız — kâğıt üzerindeki en iyiler kaybeder.</li>
<li><b>Yasa:</b> iç optimum L*, x = ΔT·f_d ile ölçeklenir; tasarım kuralı medyan %0.08 kayıp.</li>
<li><b>Tasarım:</b> gecikme farkındalıklı denetleyici, mühürlü testte kâhine 0.003 yakın.</li>
<li><b>Genişleme:</b> geniş bantta ikinci eksen — kaç alt taşıyıcı.</li>
<li><b>Titiz olumsuz sonuç:</b> öğrenme, ölçülmüş zamanda kazanmıyor.</li></ul>""",
  """Özetle: hareketli RIS sistemlerinde hesaplama gecikmesi yöntem sıralamasını belirliyor.
Etkin hız ölçütüyle kâğıt üzerindeki en iyi yöntemlerin kaybettiğini gösterdim. Bir iç optimum ve onun ölçekleme yasasını buldum, bunu ön kayıtlı olarak doğrulanmış bir tasarım kuralına çevirdim. Bu yasaları kullanan bir denetleyici tasarladım; hiç görülmemiş bir çekilişte olası en iyi seçime çok yakın çalışıyor. Geniş bantta zaman bütçesinin ikinci eksenini ortaya koydum. Ve yapay zekâ ekseninde titiz bir olumsuz sonuç ve bir değerlendirme protokolü bıraktım.
Bütün sayılar betiklere, ham verilere ve tohumlara bağlı; her biri bağımsız olarak denetlendi. Dinlediğiniz için teşekkür ederim.""")
