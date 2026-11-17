# Makale 2 — Kaynak kontrolü, Grup 9: Zheng2022COMST, Wang2020TWC

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Wang vd.'nin denklem (61)–(62)'deki tavan (⌈·⌉) parantezleri metin çıkarımında kayboluyor; bu yüzden PDF s. 7 sayfa görüntüsünden (`pdftoppm`) okundu. Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

Atıf yerleri `grep` ile bulundu (`mobility_paper_ieee.tex`, `sections/*.tex`, `tables/*.tex`; dal `thesis/p4-deneyler`, commit `a6b0c41`). İki anahtar da yalnızca bir kez, aynı paragrafta geçiyor: `sections/section_05_methodology.tex`, satır 24. Özette (abstract) ikisi de geçmiyor.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## ÖNCE OKUNMALI

Makale 2'deki bir iddiayla çelişen bulgu **yok**. "48 pilot sembolü" sayısı kaynağın denklem (62)'sinden K = 4, N = 32, M = N_t = 8 için birebir çıkıyor: 4 + 32 + max(3, ⌈3·32/8⌉) = 4 + 32 + 12 = 48. Bu sayı `tables/tab_tracking.tex` (T_p = 3.43 ms satırı) ve `tables/tab_cnnlstm.tex` (3.43 sütunu) içinde de dolaylı olarak kullanılıyor, dolayısıyla doğruluğu tablolara da taşınıyor.

Tek önemli eksik bir varsayım: kaynağın sonucu **yukarı bağlantı (uplink)** pilotlarıyla elde ediliyor; Makale 2 ise aşağı bağlantıda (downlink) hüzmeleme yapıyor. Bu, kestirilen kanalların aşağı bağlantıda kullanılması için TDD karşılıklılığı (reciprocity) gerektirir. Makale 2 bunu söylemiyor. Ayrıntı ve öneri [Wang2020TWC] başlığı altında.

---

## [Zheng2022COMST] Zheng vd., IEEE COMST 2022 (derleme)

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Beixiong Zheng, Changsheng You, Weidong Mei, Rui Zhang. Başlık: "A Survey on Channel Estimation and Practical Passive Beamforming Design for Intelligent Reflecting Surface Aided Wireless Communications". Dergi: IEEE Communications Surveys & Tutorials, VOL. 24, NO. 2, SECOND QUARTER 2022. İlk sayfa 1035; PDF 37 sayfa, son sayfa 1071 (PDF s. 37 üst bilgisi). DOI: 10.1109/COMST.2022.3155305. Bib: aynı yazarlar, başlık, cilt 24, sayı 2, s. 1035–1071, aynı DOI. **UYUŞUYOR.**
- **Makale 2'de nerede:** Yöntem bölümü (`sections/section_05_methodology.tex`, satır 24): "We tie $T_{\mathrm{ov}}$ and the pilot time $T_{\mathrm{p}}$ to cascaded channel estimation~\cite{Zheng2022COMST}."
- **Kaynakta karşılığı:**
  - Basılı s. 1040, PDF s. 6, §II-A "Channel Estimation for Different IRS Architectures": "Accordingly, existing approaches for estimating the IRS-associated channels can be classified into two categories for each of them, namely, “separate channel estimation” and “cascaded channel estimation”…"
  - Basılı s. 1042, PDF s. 8, §II-A-2 "Cascaded Channel Estimation With Fully-Passive IRS": "Instead, only the cascaded user-IRS-BS (BS-IRS-user) channel can be estimated at one endpoint of the communication system, e.g., the BS with higher signal processing capability, as illustrated in Fig. 4(b)." Aynı sayfa: "the cascaded channel estimation is more practically appealing due to the much lower hardware cost and energy consumption at the IRS as it does not need active sensing devices."
  - Basılı s. 1043, PDF s. 9, §II-B-1: "the training overhead for resolving the full CSI of {h_n}_{n=1}^N is generally proportional to the number of reflecting elements N and thus may incur a long estimation delay."
  - Basılı s. 1044, PDF s. 10, §II-B-2 "Multi-User System With Single IRS": "…the authors in [89] proposed to first estimate the cascaded CSI of one typical user (say, H_1 for user 1) at the BS, based on which the cascaded CSI of the remaining users (i.e., {H_k}_{k=2}^K) was then estimated with significantly reduced training overhead in the IRS-aided multi-user MISO system." Derlemenin [89] numaralı kaynağı Wang, Liu, Cui (Makale 2'nin Wang2020TWC'si). Aynı yöntem basılı s. 1048, PDF s. 14, §II-C-1'de de anılıyor.
  - Derlemede belirli bir pilot sayısı ya da milisaniye cinsinden süre verilmiyor ("max(K", "K + N", "2K + N" araması derleme metninde sonuç vermedi).
- **Değerlendirme:** Atıf, pilot süresini hangi kanal kestirimi çerçevesine bağladığını göstermek için genel bir çerçeve atfı. Derleme "cascaded channel estimation" kavramını tanımlıyor, pasif RIS için bunun tek seçenek olduğunu söylüyor ve eğitim yükünün N ile büyüdüğünü belirtiyor. Ayrıca Makale 2'nin bir sonraki cümlede kullandığı Wang vd. yöntemini çok kullanıcılı tek-RIS kurulumu için temsilci yöntem olarak anıyor. Atfa herhangi bir sayı yüklenmemiş; yüklenen kavram kaynakta var.
  - Küçük nüans: Derleme T_ov (edinim gecikmesi) için bir değer vermiyor; Makale 2 de vermiyor. "Tie … to" ifadesi yalnızca kavramsal bağ kuruyor, bu haliyle sorun yok.
- **Karar:** **DOĞRU.**

---

## [Wang2020TWC] Wang, Liu, Cui, IEEE TWC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Zhaorui Wang, Liang Liu, Shuguang Cui. Başlık: "Channel Estimation for Intelligent Reflecting Surface Assisted Multiuser Communications: Framework, Algorithms, and Analysis". Dergi: IEEE Transactions on Wireless Communications, VOL. 19, NO. 10, OCTOBER 2020. İlk sayfa 6607; PDF 14 sayfa, son sayfa 6620 (PDF s. 14 üst bilgisi). DOI: 10.1109/TWC.2020.3004330. Bib: aynı yazarlar, başlık, cilt 19, sayı 10, s. 6607–6620, aynı DOI. **UYUŞUYOR.**
- **Makale 2'de nerede:** Yöntem bölümü (`sections/section_05_methodology.tex`, satır 24): "With the scheme of~\cite{Wang2020TWC}, 48 pilot symbols suffice for $K=4$, $N=32$ and $N_t=8$ in the noise-free case." Bir sonraki cümle bu 48 sembolü 5G NR numerolojisiyle süreye çeviriyor (3.43, 1.71, 0.86 ms; o kısım [3gpp_nr_phy] atfına ait, bu grubun kapsamı dışında).
- **Kaynakta karşılığı:**
  - Basılı s. 6613, PDF s. 7, §IV-D "Overall Channel Estimation Overhead", denklem (62) (sayfa görüntüsünden okundu): "To summarize, for perfectly estimating all the direct channels h_k's and reflected channels g_{k,n}'s in the case without noise at the BS, the minimum pilot sequence length is τ̃ = τ̃_1 + τ̃_2 + τ̃_3 = K + N + max(K − 1, ⌈(K − 1)N/M⌉)."
  - Basılı s. 6612, PDF s. 6, §IV-C, Theorem 2: "In the case of M < N, the minimum value of τ_3 to guarantee perfect estimation of λ according to (36) is given by τ̃_3 = ⌈(K − 1)N/M⌉" (denklem 49). M ≥ N için Theorem 1: τ̃_3 = K − 1.
  - Basılı s. 6607, PDF s. 1, Özet: "Under this framework, we analytically prove that a time duration consisting of K + N + max(K − 1, ⌈(K − 1)N/M⌉) pilot symbols is sufficient for perfectly recovering all the KMN + KM channel coefficients under the case without receiver noise at the BS."
  - Simgeler ve varsayımlar, basılı s. 6609, PDF s. 3, §II "System Model": "We consider a narrow-band wireless system with K single-antenna users simultaneously communicating with a BS in the uplink, where the BS is equipped with M antennas. An IRS equipped with N passive reflecting elements is deployed…" Aynı paragraf: "We assume quasi-static block-fading channels, where all the channels remain approximately constant in each fading block."
  - Korelasyonun kullanıldığı yer, basılı s. 6608, PDF s. 2, §I-C: kullanıcıların yansıyan kanalları tipik kullanıcınınkinin ölçeklenmiş hali olduğundan "only the scaling factors (scalars), rather than the whole channels (vectors), need to be estimated." (Denklem 21: g_{k,n} = λ_{k,n} g_{1,n}.)
- **Değerlendirme:** Sayı doğru. Kaynakta M BS anten sayısı, N RIS eleman sayısı, K tek antenli kullanıcı sayısı. Makale 2'de BS anten sayısı N_t = 8, N = 32, K = 4 ve kullanıcılar tek antenli (`section_03_system_model.tex`, satır 5). M = 8 < N = 32 olduğu için Theorem 2 geçerli: τ̃_3 = ⌈3·32/8⌉ = 12 > K − 1 = 3. Toplam: K + N + 12 = 48. "Noise-free case" nitelemesi kaynağın "without receiver noise at the BS" koşuluyla birebir örtüşüyor. "Suffice" sözcüğü de kaynağın "sufficient"/"minimum" ifadesine uygun. Gürültülü durumda kaynak LMMSE kestirimcileri veriyor (§V) ve Phase II pilot uzunluğunu artırmayı öneriyor; yani 48 gerçek sistemde bir alt sınır. Makale 2 bunu "noise-free" diyerek zaten belirtiyor.
  - Eksik varsayım: kaynağın çerçevesi **yukarı bağlantı** pilotlarına dayanıyor (kullanıcılar pilot gönderiyor, BS kestiriyor). Makale 2'nin modeli aşağı bağlantı. Kestirilen kanalın aşağı bağlantıda kullanılması TDD karşılıklılığını gerektirir. Ayrıca kaynak dar bantlı bir model kullanıyor ve "pilot symbol" bir zaman dilimi demek. Makale 2'nin "bir pilot = bir OFDM sembolü" eşlemesi bir varsayım; Makale 2 bunu açıkça varsayım olarak yazdığı için sorun değil.
  - Kaynak, yarı-durağan blok sönümleme altında çalışıyor (tüm 48 sembol boyunca kanal sabit). Hareketli kullanıcıda bu, pilot süresinin (≤ 3.43 ms) eşevreli kalma süresinden kısa olmasını gerektirir. Makale 2'nin konusu tam da bu olduğu için çelişki değil, ama varsayım olarak belirtilebilir.
- **Karar:** **DOĞRU** (sayı ve koşul). Varsayımları tam yazmak için önerilen biçim (isteğe bağlı): "With the uplink scheme of~\cite{Wang2020TWC}, which exploits the common RIS--BS channel shared by the single-antenna users, $K+N+\max(K-1,\lceil (K-1)N/N_t\rceil)=48$ pilot symbols suffice for $K=4$, $N=32$ and $N_t=8$ in the noise-free case, assuming TDD reciprocity for the downlink."

---

## Özet tablo

| Anahtar | Künye | Makale 2'deki yer | Kaynaktaki karşılık | Karar |
|---|---|---|---|---|
| Zheng2022COMST | UYUŞUYOR | §V Yöntem, `section_05_methodology.tex` s. 24: T_ov ve T_p'yi cascaded kanal kestirimine bağlama | Basılı s. 1040–1044, §II-A, §II-B: cascaded kestirim tanımı, eğitim yükünün N ile büyümesi, [89] = Wang vd. temsilci yöntem | **DOĞRU** |
| Wang2020TWC | UYUŞUYOR | §V Yöntem, aynı satır: "48 pilot symbols suffice for K=4, N=32, N_t=8 in the noise-free case" | Basılı s. 6613, §IV-D, denk. (62): K + N + max(K−1, ⌈(K−1)N/M⌉) → 4+32+12 = 48; gürültüsüz, tek antenli kullanıcılar, uplink, yarı-durağan kanal | **DOĞRU** (isteğe bağlı: uplink/TDD varsayımı ve formül eklenebilir) |
