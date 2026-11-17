# Makale 2 — Kaynak kontrolü, Grup 8: Kingma2015ICLR, itu_m2410, Armijo1966PJM, Tang2021TWC

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`, şekil alt yazıları dahil; dal `thesis/p4-deneyler`, commit `68b0b1b`). Özette (abstract) bu dört anahtarın hiçbiri geçmiyor. Özette "10 km/h" geçiyor ama atıf yok. `unused/` klasöründeki dosyalar değerlendirmeye alınmadı.

Tang2021TWC için Makale 2'nin modeli kodda da karşılaştırıldı: `ris_mu/channel.py` (satır 235–255), `ris_mu/mumiso/channel.py` (satır 170–190), `ris_mu/mumiso/mobile.py` (satır 240–250), `ris_mu/geometry.py` (satır 30, 58–75). Armijo için `scripts/mumiso_step_scaling.py` (satır 83–110). Kod değiştirilmedi.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI: Tang2021TWC'ye dayandırılan modelde birim hücre kazancı kaynakla tutarsız

Makale 2 şunu söylüyor: *"The cascaded amplitude follows the two-hop model of [Tang2021TWC] with a $\cos^q$ element pattern."* (`sections/section_03_system_model.tex`, satır 24).

Tang vd.'de birim hücre kazancı, normalize güç ışıma örüntüsünden denklem (2) ile hesaplanıyor: Gain = 4π / ∫∫ F(θ,φ) sinθ dθ dφ (basılı s. 423, PDF s. 3). Örnek olarak F = cos³θ veriliyor ve kazanç 8 bulunuyor: "its gain is equal to 8 (9.03 dBi)" (basılı s. 423, PDF s. 3). Güç örüntüsü F = cos^q θ olan bir yarım uzay örüntüsü için denklem (2) G = 2(q+1) verir. q = 3 için bu 8 eder ve kaynakla uyuşur.

Kodda ise:
- Güç örüntüsü cos^q. Genliğe `np.sqrt(f_in)` ve `np.sqrt(f_out)` olarak giriyor, `f_in = _centre_cos(P, bs) ** P.q`.
- Kazanç `element_gain = 2.0 * (2.0 * self.q + 1.0)` (`ris_mu/geometry.py`, satır 58–60). Bu formül, güç örüntüsü cos^(2q) olduğunda doğru olur.
- Deneylerde q = 1 kullanılıyor: `RISPanel` q verilmeden kuruluyor (`ris_mu/mumiso/channel.py`, satır 268), varsayılan değer `q: float = 1.0`.

Sonuç: Kod G = 6 kullanıyor. Tang'ın denklem (2)'si aynı cos¹ güç örüntüsü için G = 4 verir. RIS kaskadının gücü kaynaktaki modele göre 1.5 kat (+1.76 dB) yüksek. Bu analitik bir hesap; ölçüm değil.

Bu sabit bir çarpan. Yalnızca RIS üzerinden geçen bağlantıyı etkiliyor, doğrudan bağlantıyı etkilemiyor. Sonuçlara etkisi ölçülmedi. CLAUDE.md'ye göre bu tür bir değişiklik tüm paketin yeniden ölçülmesini gerektirir; kullanıcıya sorulmadan dokunulmamalı.

Makale metni q değerini vermiyor. En az değişiklikle metin şöyle düzeltilebilir: "a cos^q element pattern (q = 1) with boresight gain 2(2q+1)". Bu ifade kodla tutarlı olur ama kazancın kaynağı artık Tang değil, Makale 2'nin kendi seçimi olarak okunur. Öteki seçenek kodu G = 2(q+1)'e çekmek ve paketi yeniden ölçmek; bu karar kullanıcıya ait.

---

## Kingma2015ICLR — Kingma ve Ba, ICLR 2015

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Diederik P. Kingma, Jimmy Lei Ba. Başlık: "Adam: A Method for Stochastic Optimization". Her sayfanın üst bilgisinde "Published as a conference paper at ICLR 2015" yazıyor. Kenar damgası: "arXiv:1412.6980v9 [cs.LG] 30 Jan 2017". Bib girdisi `@inproceedings`, ICLR, 2015, `note={arXiv:1412.6980}`. ICLR 2015'in sayfa numaralı bir bildiri kitabı olmadığı için sayfa alanının bulunmaması doğru. **UYUŞUYOR.** İsteğe bağlı: sürümü sabitlemek için not alanına "v9" eklenebilir.
- **Makale 2'de nerede:** Yöntem bölümü (`sections/section_05_methodology.tex`, satır 14): "\emph{Adam}~\cite{Kingma2015ICLR} optimizes the soft-min surrogate, starting from SU-average." Başka bir atıf yok. Adam'ın adım boyu ayarı (satır 16) Makale 2'nin kendi taramasıdır ve kaynağa dayandırılmıyor.
- **Kaynakta karşılığı:**
  - PDF s. 1, Özet: "We introduce Adam, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments."
  - PDF s. 2, Algorithm 1: "Good default settings for the tested machine learning problems are α = 0.001, β1 = 0.9, β2 = 0.999 and ε = 10−8."
- **Değerlendirme:** Atıf yalnızca yöntemin adı ve kaynağı için yapılıyor. Kaynağın kendisine bir özellik ya da sayı yüklenmiyor. Doğru.
  - Makale 2'deki adım boyları (0.02–2.0 aralığından seçilen 0.75, aging setinde 0.5) kaynağın önerdiği α = 0.001'den çok farklı. Ama makale bunları kendi doğrulama taramasıyla seçtiğini açıkça yazıyor ve kaynağın varsayılanını kullandığını iddia etmiyor. Bu bir hata değil.
  - β1, β2 ve ε makalede verilmiyor. Kod `torch.optim.Adam([th], lr=step)` çağrısını yapıyor (`ris_mu/mumiso/baselines.py`, satır 232), yani PyTorch varsayılanları kullanılıyor. Bunlar kaynaktaki β1 = 0.9, β2 = 0.999, ε = 10⁻⁸ ile aynı. Yeniden üretilebilirlik için bir yan cümle eklenebilir; zorunlu değil.
  - Kaynak Adam'ı stokastik amaç fonksiyonları için öneriyor. Makale 2 ise her senaryoda belirlenimci bir vekil fonksiyon üzerinde kullanıyor. Bu yaygın bir kullanım; atıfı geçersiz kılmıyor.
- **Karar:** **DOĞRU.** İsteğe bağlı ek: "…with β1 = 0.9, β2 = 0.999, ε = 10⁻⁸ [Kingma2015ICLR]".

---

## itu_m2410 — ITU-R M.2410-0 (11/2017)

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. "Report ITU-R M.2410-0 (11/2017)". Başlık: "Minimum requirements related to technical performance for IMT-2020 radio interface(s)". M Series. Bib girdisi: ITU-R, aynı başlık, Report, ITU-R M.2410-0, Kasım 2017. **UYUŞUYOR.**
- **Makale 2'de nerede:** Dört yerde.
  - (a) Sistem modeli (`section_03_system_model.tex`, satır 27): "…the 10~km/h upper end of the IMT-2020 pedestrian class, at which indoor mobility is evaluated~\cite{itu_m2410}".
  - (b) Sonuçlar (`section_06_results.tex`, satır 57): "10~km/h, the upper end of the IMT-2020 pedestrian class at which indoor mobility is evaluated~\cite{itu_m2410}; and, beyond the pedestrian class, 18~km/h (5~m/s) and the 30~km/h of the dense-urban evaluation~\cite{3gpp_tr38913,itu_m2410}."
  - (c) `tables/tab_speeds.tex`: satırlar "10 & ITU~\cite{itu_m2410}", "18 & ITU, veh.", "30 & ITU, urban".
  - (d) Atıfsız ama aynı iddia: Sonuç bölümü (`section_07_conclusion.tex`, satır 7): "…3 at 10~km/h, the upper end of the IMT-2020 pedestrian class." Ayrıca özette "at 10~km/h the peak is at 3 steps".
- **Kaynakta karşılığı:**
  - Basılı s. 7, PDF s. 9, §4.11 "Mobility": "Mobility is the maximum mobile station speed at which a defined QoS can be achieved (in km/h)." Hemen ardından sınıflar: "Stationary: 0 km/h", "Pedestrian: 0 km/h to 10 km/h", "Vehicular: 10 km/h to 120 km/h", "High speed vehicular: 120 km/h to 500 km/h."
  - Aynı sayfa, Table 3 "Mobility classes": Indoor Hotspot – eMBB için "Stationary, Pedestrian"; Dense Urban – eMBB için "Stationary, Pedestrian, Vehicular (up to 30 km/h)"; Rural – eMBB için "Pedestrian, Vehicular, High speed vehicular".
  - Aynı sayfa: "A mobility class is supported if the traffic channel link data rate on the uplink, normalized by bandwidth, is as shown in Table 4. This assumes the user is moving at the maximum speed in that mobility class in each of the test environments."
  - Basılı s. 8, PDF s. 10, Table 4: Indoor Hotspot – eMBB 1.5 bit/s/Hz, 10 km/h; Dense Urban – eMBB 1.12 bit/s/Hz, 30 km/h; Rural – eMBB 0.8 bit/s/Hz, 120 km/h.
- **Değerlendirme:**
  - (a), (b) ve (d) için: Yaya sınıfı 0–10 km/h. Kapalı alan (Indoor Hotspot) yalnızca durağan ve yaya sınıflarını destekliyor ve hareketlilik gereksinimi bu sınıfın üst ucunda, 10 km/h'te sınanıyor (Table 3–4). "10 km/h, the upper end of the IMT-2020 pedestrian class, at which indoor mobility is evaluated" ifadesi kaynakla birebir uyuşuyor. "30 km/h of the dense-urban evaluation" ifadesi de Table 3 ("Vehicular (up to 30 km/h)") ve Table 4 (Dense Urban, 30 km/h) ile uyuşuyor. Görevde sözü edilen "every standardized indoor speed" ifadesi Makale 2'de bulunamadı (`grep "standardized"` yalnızca özetteki "standardized indoor-office … downlink" sonucunu verdi).
  - Bilgi notu: ITU'daki hareketlilik gereksinimi **yukarı bağlantı** veri hızı için tanımlı. Makale 2 aşağı bağlantıyı inceliyor ve ITU'dan yalnızca hız değerini alıyor. "At which indoor mobility is evaluated" ifadesi bu yüzden yanlış değil; daha kesin olmak isterseniz "the speed at which IMT-2020 indoor-hotspot mobility is evaluated" yazılabilir.
  - (c) için küçük bir sorun var: Tablodaki "18 & ITU, veh." satırı. ITU 18 km/h diye bir değer vermiyor. 18 km/h yalnızca araç sınıfının aralığına (10–120 km/h) düşüyor. Ayrıca Table 3'e göre kapalı alan test ortamı araç sınıfını hiç desteklemiyor. Metin bunu doğru söylüyor ("beyond the pedestrian class, 18 km/h (5 m/s)", atıfsız). Ama tablonun "Source" sütunu 18 km/h'in ITU'da tanımlı bir değer olduğu izlenimini veriyor. "30 & ITU, urban" doğru (Table 4, Dense Urban 30 km/h).
- **Karar:** (a), (b), (d) **DOĞRU.** (c) 10 ve 30 km/h satırları **DOĞRU**; 18 km/h satırı **DÜZELTİLMELİ**. Önerilen biçim: Source hücresi "ITU veh. class (10–120)" ya da "—" yapılsın ve alt yazıya şu eklensin: "18 km/h lies in the IMT-2020 vehicular class (10–120 km/h), which is not evaluated indoors [itu_m2410]."

---

## Armijo1966PJM — Armijo, Pacific J. Math. 1966

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazar: Larry Armijo. Başlık: "Minimization of functions having Lipschitz continuous first partial derivatives". Pacific Journal of Mathematics, Vol. 16, No. 1, 1966 (kapakta "November 1966"). Makale basılı s. 1–3 (PDF s. 2–4; PDF s. 1 kapak). Bib girdisi: aynı yazar ve başlık, vol. 16, no. 1, pp. 1–3, 1966, doi 10.2140/pjm.1966.16.1. PDF'te DOI basılı değil; DOI biçimi MSP'nin pjm.1966.16.1 düzeniyle tutarlı ama PDF'ten doğrulanamadı. Öteki alanlar **UYUŞUYOR.**
- **Makale 2'de nerede:** Yöntem bölümü (`section_05_methodology.tex`, satır 14): "\emph{Armijo} is steepest ascent with Armijo's rule~\cite{Armijo1966PJM} on the same surrogate, with a per-scenario backtracking line search." Sonuçlarda (satır 31, Fig. alt yazısı satır 36) "Armijo" adı yöntem etiketi olarak geçiyor; orada atıf yok.
- **Kaynakta karşılığı:**
  - Basılı s. 1, PDF s. 2, giriş paragrafı: "It is then shown that the usual steepest descent and modified steepest descent algorithms converge under the same hypotheses. The modified steepest descent algorithm allows for the possibility of variable stepsize." (PDF metninde "some" olarak çıkan kelime bağlamdan "same".)
  - Basılı s. 2, PDF s. 3, Corollary 2 "(The Modified Steepest Descent Algorithm)": a_m = a/2^(m−1) ve x_{k+1} = x_k − a_{m_k} ∇f(x_k); burada m_k, f(x_k − a_m ∇f(x_k)) − f(x_k) ≤ −(1/2) a_m |∇f(x_k)|² koşulunu sağlayan en küçük pozitif tam sayı.
  - Basılı s. 3, PDF s. 4, §3 "Discussion": "the modified steepest descent algorithm of Corollary 2 allows for the possibility of variable stepsize and does not require knowledge of the value of the Lipschitz constant K."
- **Değerlendirme:** "Armijo's rule" denilen geri izlemeli (backtracking) yeterli-azalma koşulu bu makaledeki Corollary 2'dir: adım boyu yarıya indirilerek koşul sağlanana kadar küçültülüyor. Makale 2 bunu en büyükleme (ascent) yönünde kullanıyor; bu, −f üzerinde aynı kural. Atıf doğru.
  - Uygulama ayrıntısı, bilgi için (`scripts/mumiso_step_scaling.py`, satır 83–110): Kod yeterli-artış sabiti olarak c = 10⁻⁴ kullanıyor (Armijo 1966'da 1/2). Küçültme oranı 0.5 (kaynakla aynı). En fazla 12 geri izleme yapılıyor. Başarılı bir adımdan sonra sonraki adım iki katından başlıyor; başarısız aramadan sonra a0'a dönüyor. Bu, kuralın yaygın genelleştirilmiş biçimi. Kaynaktaki sabit başlangıç adımı ve 1/2 sabitinden farklı ama "Armijo's rule" adını kullanmayı geçersiz kılmıyor. Makale bu sabitleri vermiyor; yeniden üretilebilirlik için eklenebilir.
- **Karar:** **DOĞRU.** İsteğe bağlı ek: "…Armijo's sufficient-increase rule [Armijo1966PJM] (constant 10⁻⁴, halving, initial step doubled after each accepted step)…".

---

## Tang2021TWC — Tang vd., IEEE TWC 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Wankai Tang, Ming Zheng Chen, Xiangyu Chen, Jun Yan Dai, Yu Han, Marco Di Renzo, Yong Zeng, Shi Jin, Qiang Cheng, Tie Jun Cui. Başlık: "Wireless Communications With Reconfigurable Intelligent Surface: Path Loss Modeling and Experimental Measurement". Dergi: IEEE Transactions on Wireless Communications, VOL. 20, NO. 1, JANUARY 2021. İlk sayfa 421, son sayfa 439 (PDF 19 sayfa). DOI: 10.1109/TWC.2020.3024887. **UYUŞUYOR.**
- **Makale 2'de nerede:** Sistem modeli (`section_03_system_model.tex`, satır 24): "All links follow the 3GPP TR~38.901 indoor-office model~\cite{3gpp_channel}: its path loss, LoS probability, Rician factor and log-normal shadowing … The cascaded amplitude follows the two-hop model of~\cite{Tang2021TWC} with a $\cos^q$ element pattern." Başka bir atıf yok.
- **Kaynakta karşılığı:**
  - Basılı s. 421, PDF s. 1, Özet: "In this article, free-space path loss models for RIS-assisted wireless communications are developed for different scenarios by studying the physics and electromagnetic nature of RISs." Ölçümle doğrulama: "three fabricated RISs (metasurfaces) are utilized to further corroborate the theoretical findings through experimental measurements conducted in a microwave anechoic chamber."
  - Basılı s. 423, PDF s. 3, §II-B ve denklem (1)–(2): "An example of normalized power radiation pattern is the following [40]", F(θ,φ) = cos³θ (θ ∈ [0, π/2]), aksi halde 0. Dipnot 3: "The form cos^α can be used to match the normalized power radiation pattern of different unit cell and antenna designs with an appropriate α [40]." Kazanç: "its gain is equal to 8 (9.03 dBi)".
  - Aynı sayfa, dipnot 4: "Since the channel model of the direct link has already been well studied [42], this work focuses on the RIS-assisted link and aims to provide its free-space path loss".
  - Basılı s. 424, PDF s. 4, Theorem 1: Pr = Pt · Gt Gr G dx dy λ² / (64π³) · |Σ Σ √(F_combine) Γ_{n,m} / (r^t r^r) e^{…}|².
  - Basılı s. 425, PDF s. 5, Proposition 1, denklem (5)–(6), uzak alan hüzmeleme durumu: PL = 64π³ (d1 d2)² / (Gt Gr G M² N² dx dy λ² F(θt,φt) F(θr,φr) A²). Metin: "the free-space path loss of RIS-assisted wireless communications is proportional to (d1 d2)² in the far-field case."
- **Değerlendirme:**
  - **Uyuşan kısım:** Kod (`ris_mu/channel.py`, satır 235–255) her eleman için a_n = √(Gt Gr G F_in F_out dx dy) · λ / ((4π)^1.5 d1 d2) genliğini kullanıyor. (4π)³ = 64π³ olduğu için bu, Tang'ın Theorem 1 / denklem (5) uzak alan ifadesinin eleman başına karşılığı. 1/(d1 d2) ölçeklenmesi, Gt Gr G dx dy λ² sabiti ve giriş/çıkış örüntü çarpımı F_in·F_out kaynakla aynı. cos^q biçimi dipnot 3'teki cos^α genellemesine dayanıyor. "Two-hop model" kaynağın kendi terimi değil ama yapıyı doğru anlatıyor. Makalenin RIS'i BS'nin Fraunhofer mesafesinin ötesine koyması da kaynağın uzak alan koşuluyla tutarlı.
  - **Kaynakta olmayan kısım 1 (3GPP ile birleştirme):** Tang yalnızca **serbest uzay** yol kaybı modeli veriyor (dipnot 4, Özet). Makale 2 her atlamaya TR 38.901'in serbest uzay üstü kaybını (`pl.excess_db`), LoS durumunu ve gölgelemeyi ekliyor; kodun yorumu da bunu söylüyor ("split here into one amplitude factor per hop so that the two hops can carry their own LoS state, excess loss and shadowing"). Bu birleştirme Makale 2'nin kendi seçimi. Tang'da yok ve Tang'ın ölçüm doğrulaması bu birleşik modeli kapsamıyor (ölçümler yansımasız odada). Mevcut cümle sırası ("All links follow 3GPP … The cascaded amplitude follows … [Tang]") yanlış değil. Ama okuyucu 3GPP+Tang birleşiminin Tang'da doğrulandığını sanabilir; birleştirmenin yazarlara ait olduğu açıkça yazılmalı.
  - **Kaynakta olmayan kısım 2 (birim hücre kazancı):** Yukarıdaki "ÖNCE OKUNMALI" bölümüne bakın. Kodun kazancı G = 2(2q+1), Tang'ın denklem (2)'sinin cos^q güç örüntüsü için verdiği G = 2(q+1) ile uyuşmuyor (q = 1'de 6'ya karşı 4). Makale q değerini de vermiyor.
  - Bilgi notu: Kod, örüntüyü her eleman yerine panel merkezinde hesaplıyor ("evaluated at the panel centre … constant to within about two degrees"). Bu, Tang'ın denklem (5)'teki uzak alan yaklaşımıyla aynı.
- **Karar:** **DÜZELTİLMELİ.** Önerilen biçim: "The cascaded amplitude uses the far-field free-space model of [Tang2021TWC], Gt Gr G dx dy λ² F_in F_out / (64π³ d1² d2²) per element, with a cos^q unit-cell power pattern (q = 1); we add the TR 38.901 excess loss and shadowing to each hop." Ayrıca G için bir seçim yapılmalı. Ya kaynakla tutarlı G = 2(q+1) = 4'e geçilip paket yeniden ölçülür, ya da metne "boresight gain 2(2q+1) = 6" yazılır ve bu değerin Tang'ın denklem (2)'sinden farklı olduğu belirtilir. Bu karar kullanıcıya ait.

---

## Özet tablo

| Anahtar | Karar | Gerekçe |
|---|---|---|
| Kingma2015ICLR | DOĞRU | Yalnızca yöntem adı için atıf. Özet (PDF s. 1) ve Algorithm 1 (PDF s. 2) uyuşuyor. Kod PyTorch varsayılanlarını kullanıyor; bunlar kaynaktaki β1, β2, ε ile aynı. Adım boyu Makale 2'nin kendi taraması. Künye uyuşuyor (arXiv v9: "Published as a conference paper at ICLR 2015") |
| itu_m2410 | DOĞRU; tablodaki 18 km/h satırı DÜZELTİLMELİ | §4.11 ve Table 3–4 (basılı s. 7–8, PDF s. 9–10): yaya sınıfı 0–10 km/h, kapalı alanda yalnızca durağan ve yaya, sınama 10 km/h'te; Dense Urban 30 km/h. 18 km/h ITU'da tanımlı değil (yalnızca araç sınıfı 10–120 km/h aralığında) ve kapalı alanda araç sınıfı yok; `tab_speeds.tex`'teki "ITU, veh." etiketi yanıltıcı. Künye uyuşuyor |
| Armijo1966PJM | DOĞRU | Corollary 2 (basılı s. 2, PDF s. 3): yarıya indirerek geri izleme ve yeterli azalma; ascent biçimi aynı kural. Kodda c = 10⁻⁴ ve adım ikiye katlama var (kaynakta 1/2, sabit başlangıç); bu sabitlerin eklenmesi isteğe bağlı. Künye uyuşuyor; DOI PDF'te basılı değil |
| Tang2021TWC | DÜZELTİLMELİ | 1/(d1 d2), Gt Gr G dx dy λ²/(64π³), F_in·F_out ve cos^α biçimi uyuşuyor (Theorem 1, denklem (1)–(2), (5), s. 423–425). Ancak (i) kaynak serbest uzay modeli veriyor; 3GPP fazla kaybı ve gölgeleme ile birleştirme yazarlara ait. (ii) Kodun kazancı G = 2(2q+1) = 6, kaynağın denklem (2)'sinin cos^q güç örüntüsü için verdiği 2(q+1) = 4 ile tutarsız: kaskad gücü +1.76 dB. Etkisi ölçülmedi. q makalede verilmiyor. Künye uyuşuyor |

Künye uyuşmazlığı bulunmadı. ÇIKARILMALI kararı yok. Üç düzeltme var: (1) Tang atfındaki model cümlesi ve birim hücre kazancı tutarsızlığı (kullanıcı kararı gerekiyor), (2) `tab_speeds.tex`'teki 18 km/h "ITU, veh." etiketi, (3) isteğe bağlı olarak Adam ve Armijo sabitlerinin metne eklenmesi.
