# Makale 2 — Kaynak kontrolü, Grup 1: [1]–[5]

Tarih: 2026-11-17. Yöntem: `pdftotext -layout` ile metin çıkarıldı. Her alıntının PDF sayfası `pdftotext -f N -l N` ile ayrıca doğrulandı. Basılı sayfa numaraları, PDF'in üst bilgisinden okundu (basılı sayfa = ilk sayfa + PDF sayfası − 1; her alıntıda tutarlı çıktı). Alıntılar PDF metninden olduğu gibi aktarıldı. Satır sonu tireleri birleştirildi.

PDF klasörü: `thesis_exp/makale2_revizyon/kaynak_kontrol/pdf/`

---

## [1] Basar vd., IEEE Access 2019

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Ertugrul Basar, Marco Di Renzo, Julien De Rosny, Merouane Debbah, Mohamed-Slim Alouini, Rui Zhang. Başlık: "Wireless Communications Through Reconfigurable Intelligent Surfaces". Dergi: IEEE Access, VOLUME 7, 2019. İlk sayfa 116753; PDF 21 sayfa olduğu için son sayfa 116773. DOI: 10.1109/ACCESS.2019.2935192. Sayı numarası basılı değil (Access dergisinde olağan). **UYUŞUYOR.**
- **Makale 2'de nerede:** Giriş, ilk cümle: "A reconfigurable intelligent surface (RIS) can turn a blocked corner of a building into a covered one [1,2,3,4];"
- **Kaynakta karşılığı:** Basılı s. 116767, PDF s. 15, §VII "Potential Use Cases".
  - "Overcoming non-LOS Scenarios – One of the most promising use cases to leverage the RISs in wireless networks consists of employing them as reconfigurable reflectors in scenarios in which the LOS path is either blocked or is not strong enough to support cell-edge users. For example, RISs can be easily attached to walls or ceilings in indoors, and can be integrated into the facades of buildings in outdoors."
  - Aynı sayfa: "Overcoming Localized Coverage Holes – Another promising case study consists of using the RISs to counteract localized coverage holes in urban scenarios, and indoor harsh propagation environments."
- **Değerlendirme:** Kaynak bir genel bakış (tutorial/overview) makalesi. Kullanım senaryoları bölümünde iki şeyi açıkça anlatıyor: LOS yolunun engellendiği durumda RIS'in yansıtıcı olarak kullanılmasını ve yerel kapsama boşluklarının (dead zone) giderilmesini. Bina cephesine montajdan da söz ediyor. "Engellenmiş bir köşeyi kapsanan bir köşeye çevirmek" ifadesi bu içeriğin doğru ve abartısız bir özeti. Ancak kaynak bunu deneysel olarak göstermiyor, bir olası kullanım senaryosu olarak sunuyor. Makaledeki "can" kipi buna uygun.
- **Karar:** **DOĞRU.**

---

## [2] Wu & Zhang, IEEE TWC 2019

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qingqing Wu, Rui Zhang. Başlık: "Intelligent Reflecting Surface Enhanced Wireless Network via Joint Active and Passive Beamforming". Dergi: IEEE Transactions on Wireless Communications, Vol. 18, No. 11, November 2019. İlk sayfa 5394; PDF 16 sayfa olduğu için son sayfa 5409. DOI: 10.1109/TWC.2019.2936025. **UYUŞUYOR.**
- **Makale 2'de nerede:** Dört yerde atıf var.
  - (a) Giriş, ilk cümle (blocked corner → covered, [1,2,3,4]).
  - (b) Giriş: "Choosing those phases is a hard, non-convex problem, attacked with iterative solvers [2, …]"
  - (c) İlgili çalışmalar: "Joint precoding and phase design has been addressed with alternating optimization and semidefinite relaxation [2], …"
  - (d) Sonuç/kısıtlar: "Semidefinite relaxation [2], WMMSE [10] and manifold methods were not timed, …"
- **Kaynakta karşılığı:**
  - (a) Basılı s. 5395, PDF s. 2, §I: "…especially when the AP-user link is severally blocked by obstacles (e.g., thick walls in indoor applications), the AP ought to adjust its beam toward the IRS to maximally leverage its reflected signal to serve the user (i.e., by creating a virtual LoS link with the user to bypass the obstacle)." ("severally" kaynakta böyle yazılmış.)
  - (b) Basılı s. 5396, PDF s. 3, §I: "However, this design problem is difficult to be solved optimally in general, due to the non-convex SINR constraints as well as the signal unit-modulus constraints imposed by passive phase shifters." Ayrıca basılı s. 5397, PDF s. 4, §II: "it is challenging to solve (P1) due to the non-convex constraints in (4) where the transmit beamforming and phase shifts are coupled."
  - (c) Basılı s. 5396, PDF s. 3, §I: "we first consider a single-user setup and apply the semidefinite relaxation (SDR) technique to obtain a high-quality approximate solution … we further propose an efficient algorithm based on the alternating optimization of the phase shifts and transmit beamforming vector in an iterative manner". SDR §III-A'da, alternating optimization §III-B'de (basılı s. 5398, PDF s. 5). Çok kullanıcılı durumda Algorithm 1 "Alternating Optimization Algorithm" (basılı s. 5401, PDF s. 8) SDR ve Gaussian randomization ile birlikte kullanılıyor.
  - (d) Kaynakta çalışma süresi ölçümü yok. "running time", "CPU" ve "computation time" araması sonuç vermedi; karmaşıklık yalnızca nitel olarak karşılaştırılıyor. Bu cümle Makale 2'nin kendi kısıtını anlatıyor; kaynaktan istenen tek şey SDR'nin orada kullanılmış olması, o da doğru.
- **Değerlendirme:** Kaynak tek hücreli, çok antenli AP ve tek antenli kullanıcılardan oluşan bir sistemde, kullanıcı başına SINR kısıtları altında toplam gönderim gücünü en aza indiren ortak aktif/pasif hüzmeleme problemi kuruyor. Problemin dışbükey olmadığını açıkça söylüyor. Çözüm olarak SDR (+ Gaussian randomization) ve yinelemeli alternating optimization öneriyor. Dolayısıyla (b), (c) ve (d) kaynağı doğru temsil ediyor. "Joint precoding and phase design" ifadesi de "joint active and passive beamforming" ile örtüşüyor.
  - Küçük bir not (b) için: SDR'nin kendisi yinelemeli değil, bir dışbükey SDP ve ardından rastgeleleştirme. Kaynaktaki yinelemeli yöntem alternating optimization. "[2, …]" listesinin tamamı "iterative solvers" olarak nitelendiği için bu bir hata sayılmaz.
  - Bir başka not: kaynağın amacı güç en aza indirme; Makale 2 hız/SNR odaklıysa bile "phase design problem is non-convex" genellemesi geçerli.
  - (a) için: kaynak engellenmiş doğrudan bağlantıyı ve "sanal LoS" fikrini kısaca anıyor. Ancak bu makale bir kapsama genişletme çalışması değil, bir optimizasyon makalesi. İlk cümledeki [2] atfı savunulabilir ama zayıf; [1], [3] ve [4] bu iddiayı çok daha doğrudan destekliyor.
- **Karar:** (b), (c), (d) **DOĞRU**. (a) **DOĞRU**, ama ilk cümleden çıkarılabilir. Önerilen biçim: "…into a covered one [1,3,4];". [2] zaten ikinci cümlede ve ilgili çalışmalarda asıl rolüyle (optimizasyon) atıflanıyor. Değiştirmek zorunlu değil.

---

## [3] Di Renzo vd., IEEE JSAC 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Marco Di Renzo, Alessio Zappone, Merouane Debbah, Mohamed-Slim Alouini, Chau Yuen, Julien de Rosny, Sergei Tretyakov. Başlık: "Smart Radio Environments Empowered by Reconfigurable Intelligent Surfaces: How It Works, State of Research, and The Road Ahead". Dergi: IEEE Journal on Selected Areas in Communications, Vol. 38, No. 11, November 2020. İlk sayfa 2450; PDF 76 sayfa olduğu için son sayfa 2525. DOI: 10.1109/JSAC.2020.3007211. **UYUŞUYOR.**
- **Makale 2'de nerede:** Giriş, ilk cümle ([1,2,3,4]).
- **Kaynakta karşılığı:** Basılı s. 2461, PDF s. 12, §IV "Smart Radio Environments", IV-A "Potential Applications of Reconfigurable Intelligent Surfaces in Smart Radio Environments" (Fig. 10'a atıfla): "Coverage enhancement. An RIS can be configured in order to create adaptable non-line-of-sight links in dead-zone (or low coverage) areas in which line-of-sight communication is not possible or it is not sufficient."
- **Değerlendirme:** Kapsamlı bir genel bakış makalesi. Uygulamalar listesinin ilk maddesi, LoS iletişimin mümkün olmadığı ölü bölgelerde kapsama iyileştirmesi; bu, atıf cümlesinin tam karşılığı. Abartı yok.
- **Karar:** **DOĞRU.**

---

## [4] Wu vd., IEEE TCOM 2021

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Qingqing Wu, Shuowen Zhang, Beixiong Zheng, Changsheng You, Rui Zhang. Başlık: "Intelligent Reflecting Surface-Aided Wireless Communications: A Tutorial" ("(Invited Paper)" ibaresiyle). Dergi: IEEE Transactions on Communications, Vol. 69, No. 5, May 2021. İlk sayfa 3313; PDF 39 sayfa olduğu için son sayfa 3351. DOI: 10.1109/TCOMM.2021.3051897. **UYUŞUYOR.** "Invited Paper" ibaresi künyeye eklenmek zorunda değil.
- **Makale 2'de nerede:** Giriş, ilk cümle ([1,2,3,4]).
- **Kaynakta karşılığı:** Basılı s. 3315, PDF s. 3, §I-B "What Is IRS?" (Fig. 3'e atıfla): "For instance, IRS is particularly useful for the coverage extension in mmWave and THz communications that are highly vulnerable to blockage."
- **Değerlendirme:** Tutorial makalesi. Kapsama genişletmeyi, engellenmeye açık bağlantılar için öne çıkan bir uygulama olarak açıkça sunuyor. Atıf cümlesi kaynağı doğru temsil ediyor.
- **Karar:** **DOĞRU.**

---

## [5] Dai vd., IEEE Access 2020

- **Künye karşılaştırması:** PDF'teki bilgiler şunlar. Yazarlar: Linglong Dai, Bichai Wang, Min Wang, Xue Yang, Jingbo Tan, Shuangkaisheng Bi, Shenheng Xu, Fan Yang, Zhi Chen, Marco Di Renzo, Chan-Byoung Chae, Lajos Hanzo. Başlık: "Reconfigurable Intelligent Surface-Based Wireless Communications: Antenna Design, Prototyping, and Experimental Results". Dergi: IEEE Access, VOLUME 8, 2020. İlk sayfa 45913; PDF 11 sayfa olduğu için son sayfa 45923. DOI: 10.1109/ACCESS.2020.2977772. **UYUŞUYOR.**
- **Makale 2'de nerede:** Giriş: "RIS hardware has been prototyped [5], and one prototype has strengthened a link through a concrete wall [6]."
- **Kaynakta karşılığı:**
  - Basılı s. 45913, PDF s. 1, Özet: "In this paper, we develop a new type of high-gain yet low-cost RIS that bears 256 elements. … This radical design forms the basis for the world's first wireless communication prototype using RIS having 256 two-bit elements."
  - Basılı s. 45914, PDF s. 2, dipnot 1: "In this paper, the RIS is deployed at the transmitter [7] for performance evaluation, which can also be used for intelligent reflection relay [6], [7]."
  - Fig. 5 (PDF s. 4): "Photograph of the fabricated RIS having 16 × 16 2-bit elements."
- **Değerlendirme:** Kaynak gerçekten bir donanım prototipi. PIN diyotlu 2 bit faz kaydırmalı, 16×16 elemanlı bir RIS üretilmiş ve ölçülmüş: 2.3 GHz'de 21.7 dBi, 28.5 GHz'de 19.1 dBi. Bu RIS, USRP tabanlı bir haberleşme prototipine entegre edilmiş. "RIS hardware has been prototyped [5]" doğru.
  - Dikkat edilecek nüans: bu prototipte RIS, bir besleme antenince aydınlatılan **verici anteni** olarak kullanılıyor (RIS tabanlı verici); verici ile alıcı arasında yansıtıcı röle olarak değil. Yansıtıcı kullanım yalnızca dipnotta bir olasılık olarak anılıyor.
  - Makale 2 yansıtıcı (pasif röle) RIS modelliyorsa, [5]'in neyi prototiplediğini belirtmek jüri sorusunu önler. Cümle şimdiki haliyle yanlış değil.
- **Karar:** **DOĞRU.** İsteğe bağlı netleştirme önerisi: "RIS hardware has been prototyped, e.g., a 256-element 2-bit RIS used as a transmit antenna [5], and one prototype has strengthened a link through a concrete wall [6]."

---

## Özet tablo

| n | Karar | Gerekçe |
|---|---|---|
| [1] | DOĞRU | §VII (s. 116767): LOS'un engellendiği durumlarda RIS yansıtıcı olarak kullanılıyor, kapsama boşlukları gideriliyor; künye uyuşuyor |
| [2] | DOĞRU (ilk cümlede zayıf) | Dışbükey olmama (s. 5396–5397), SDR ve alternating optimization (s. 5396, 5398) açıkça var; ilk cümlede yalnızca kısa bir "virtual LoS" anışı var (s. 5395), oradan çıkarılması önerilir (zorunlu değil); künye uyuşuyor |
| [3] | DOĞRU | §IV-A (s. 2461): "Coverage enhancement … dead-zone areas"; künye uyuşuyor |
| [4] | DOĞRU | §I-B (s. 3315): "coverage extension … vulnerable to blockage"; künye uyuşuyor |
| [5] | DOĞRU (netleştirme önerilir) | 256 elemanlı 2 bit RIS üretilmiş ve ölçülmüş bir prototip var; ama RIS verici anteni olarak kullanılıyor, yansıtıcı röle olarak değil (dipnot 1, s. 45914); künye uyuşuyor |

Künye uyuşmazlığı bulunmadı. ÇIKARILMALI kararı yok.
