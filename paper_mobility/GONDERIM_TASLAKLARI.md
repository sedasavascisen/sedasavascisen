# Gönderim taslakları — IEEE Transactions on Wireless Communications

*Taslak. Göndermeden önce [köşeli parantez] içindekileri doldurun ve ortak
yazarlara onaylatın.*

---

## 1. Kapak mektubu (İngilizce; IEEE Author Portal'a yapıştırılacak: https://ieee.atyponrex.com/journal/twc)

November 9, 2026

Dear Editor,

We are pleased to submit our manuscript entitled **"Latency-Aware Phase
Optimization for Reconfigurable Intelligent Surfaces Serving Mobile
Users"** by Seda Savaşçı Şen, Ali Çalhan and Murtaza Cicioğlu for
consideration as a regular paper in the *IEEE Transactions on Wireless
Communications*.

Reconfigurable intelligent surface (RIS) phase optimizers are almost always
compared by the rate they reach on the channel they were given. For mobile
users this hides a race between computation and channel change: a pedestrian
changes the channel within tens of milliseconds, while a careful solver may
need seconds. Our manuscript makes this race measurable. We evaluate every
method on the channel that exists when it finishes, its *effective rate*,
with latencies measured on a real processor, in the 3GPP TR 38.901
indoor-office scenario with walking users.

The main findings are:

1. Under this criterion, the solvers with the highest rate on paper lose to a
   single-user heuristic that takes milliseconds, at every standardized user
   speed we examined (3 km/h of 3GPP TR 38.913 and 10 km/h of ITU-R M.2410,
   among others).
2. More iterations help only up to a point. The best number of optimizer steps
   is governed by a single quantity, the step time relative to the Doppler
   frequency, and a small-delay model explains how it scales.
3. A learned update rule that beats a tuned classical optimizer step for step
   loses to it millisecond for millisecond.

We believe the manuscript fits the scope of the Transactions because it
addresses a practical question at the core of RIS-aided wireless system
design, which optimizer a base station should run and for how long, with a
general evaluation framework, an analytical model and an extensive, reproducible
measurement study. The results also give a concrete methodological
recommendation for the learning-for-communications literature: learned and
classical methods should be compared on measured latency, against classical
baselines tuned at each budget.

Every number in the manuscript is produced by a script from stored measurement
files, and the code and results are publicly available at
https://github.com/sedasavascisen/ris-latency-mobility. The use of AI tools is
disclosed in the Acknowledgment, in accordance with IEEE policy.

This manuscript is
original, has not been published, and is not under consideration elsewhere.
All authors have approved the submission.

Thank you for your consideration.

Sincerely,

Seda Savaşçı Şen (corresponding author)
Department of Electrical and Electronics Engineering, Düzce University,
Düzce, Türkiye
sedasavascisen@duzce.edu.tr

---

## 2. Önerilen hakemler (IEEE Author Portal "Suggested Reviewers")

Seçim ölçütü: makalede atıf yaptığımız ve konuya en yakın çalışmaların
yazarları; yazarlarla bilinen ortak çalışması olmayanlar.
**Kurum ve e-postaları göndermeden önce kurum sayfalarından teyit edin;
burada uydurulmuş bir adres yok, bilerek boş bırakıldı.**

| # | Ad | İlgili çalışması (kaynakçamızda) | Neden uygun | Kurum / e-posta |
|---|---|---|---|---|
| 1 | Anastasios Papazafeiropoulos | Channel aging in RIS-aided massive MIMO (IEEE TVT 2023) | RIS'te kanal eskimesi: makalenin temel konusu | **TWC editörü — öneriden çıkarın** |
| 2 | Wei Yu | Learning to reflect and beamform (IEEE JSAC 2021); active sensing for beam tracking with RIS (IEEE TWC 2025) | RIS için öğrenme ve hareketli kullanıcı takibi | [teyit edin] |
| 3 | Chongwen Huang | DRL for RIS-assisted multiuser MISO (IEEE JSAC 2020) | Öğrenmeye dayalı RIS faz tasarımı | **TWC editörü — öneriden çıkarın** |
| 4 | Tiejun Lv | Two-timescale RIS optimization in fast-changing channels (IEEE TWC 2022) | Hızlı değişen kanalda RIS optimizasyonu | [teyit edin] |
| 5 | Marco Di Renzo | RIS with outdated CSI (IEEE TCOM 2022); RIS overview (IEEE JSAC 2020) | RIS'te eskimiş kanal bilgisi | [teyit edin] |

*İsteğe bağlı "karşı olunan hakem" (opposed reviewers): gerekmedikçe boş
bırakın.*

---

## 3. IEEE Author Portal'da istenecek diğer bilgiler (hazırlık listesi)

| Alan | Değer |
|---|---|
| Makale türü | Regular paper |
| Başlık | Latency-Aware Phase Optimization for Reconfigurable Intelligent Surfaces Serving Mobile Users |
| Anahtar kelimeler | Reconfigurable intelligent surface; mobility; computation latency; effective rate; channel aging; deep unfolding; multi-user MISO |
| Yazarlar ve sıra | Seda Savaşçı Şen (sorumlu), Ali Çalhan, Murtaza Cicioğlu |
| E-postalar | sedasavascisen@duzce.edu.tr; alicalhan@gmail.com; murtazacicioglu@uludag.edu.tr |
| ORCID | Seda Savaşçı Şen: 0000-0001-8569-6454 · Ali Çalhan: 0000-0002-5798-3103 · Murtaza Cicioğlu: 0000-0002-5657-7402 |
| Sayfa sayısı | 9 (çift sütun) |
| Dosyalar | PDF (IEEE PDF eXpress uyumlu), LaTeX kaynağı (zip), şekiller |
| Kod/veri | https://github.com/sedasavascisen/ris-latency-mobility |
| Fon | Yok |
| Çıkar çatışması | Yok |
