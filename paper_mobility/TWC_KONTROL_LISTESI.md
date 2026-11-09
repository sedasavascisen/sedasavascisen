# IEEE TWC gönderim kuralları: kontrol listesi

*Denetim tarihi: 9 Kasım 2026. Denetlenen dosyalar: `mobility_paper_ieee.tex`,
`sections/*.tex`, `references/references.bib`, `mobility_paper_ieee.pdf`
(9 sayfa, letter, IEEEtran journal) ve `GONDERIM_TASLAKLARI.md`.
Bu denetimde makaleye dokunulmadı.*

## Kaynaklar

| Kısa ad | URL | Sürüm / tarih | Erişim |
|---|---|---|---|
| **[TWC-P]** TWC Policies and Guidelines | https://www.comsoc.org/publications/journals/ieee-twc/policies-guidelines | Sayfanın genel bir tarihi yok. "Conference vs Journal" bölümü "Updated: October 13, 2017" diyor, APC bölümü "submitted in 2026" diyor. | 9 Kasım 2026, curl 200. `.../ieee-twc/submit-manuscript` adresi aynı içeriği veriyor. |
| **[TWC-EB]** TWC Editorial Board | https://www.comsoc.org/publications/journals/ieee-twc/ieee-transactions-wireless-communications-editorial-board | Tarih yok | curl 200 |
| **[AC-AI]** IEEE Author Center, Submission and Peer Review Policies ("Guidelines for AI-Generated Content") | https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/ | Sürüm tarihi yok, yalnızca "© 2026 IEEE" | curl 403 (bot engeli). WebFetch ile okundu, yerel kopya yok. |
| **[AC-S]** IEEE Author Center, Structure Your Article | https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/ | Tarih yok | WebFetch |
| **[AC-PP]** IEEE Author Center, Post-Publication Policies (preprint) | https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/post-publication-policies/ | Tarih yok | WebFetch |
| **[AC-CL]** IEEE Author Center, Checklist for Submitting for Peer Review | https://journals.ieeeauthorcenter.ieee.org/submit-your-article-for-peer-review/checklist-for-submitting-your-article-for-peer-review/ | Tarih yok | WebFetch. Yalnızca 5 genel madde var (dergi seç, kuralları oku, sorumlu yazar, dosyalar, ORCID). |
| **[AC-G]** IEEE Author Center, Create Graphics | https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/ | Tarih yok | WebFetch. Çözünürlük ve biçim kuralları alt sayfalarda, onlar okunmadı. |

**Erişilemeyenler:**
- `comsoc.org/.../ieee-twc/information-authors` ve `.../ieee-transactions-wireless-communications-submit-manuscript` adresleri 404 verdi.
- IEEE Xplore TWC sayfası (`punumber=7693`) ve PSPB Operations Manual PDF'i (`pspb.ieee.org/images/files/PSPB/opsmanual.pdf`) 418 verdi. [TWC-P] AI politikası için bu kılavuzun §8.2.1'ine gönderme yapıyor. Onun yerine aynı politikanın Author Center özeti [AC-AI] kullanıldı.

**Önemli not:** TWC artık ScholarOne'ı kullanmıyor, gönderim **IEEE Author Portal** üzerinden yapılıyor (https://ieee.atyponrex.com/journal/twc). [TWC-P] şöyle diyor: *"All submissions are handled Electronically through the … IEEE Author Portal"*. Aynı sayfanın ORCID bölümünde hâlâ eski ScholarOne adımları duruyor.

## Kural tablosu

Durum değerleri: **uygun**, **uygun değil**, **kullanıcı yapacak**, **belirsiz**.

| # | Kural (kaynak, kısa alıntı) | Durum | Makaledeki kanıt | Gereken düzeltme |
|---|---|---|---|---|
| 1 | **Sayfa sınırı** [TWC-P]: *"may not exceed 13 double-column single-spaced pages (10-point font size) including … all references"* | uygun | PDF 9 sayfa (`pdfinfo`). `\documentclass[journal]{IEEEtran}` varsayılan olarak 10 pt ve çift sütun. | — |
| 2 | **Biçim ve şablon** [TWC-P]: *"Official templates can be accessed in IEEE Template Selector"*. Gönderilen dosya PDF olmalı: *"the actual submitted manuscript should be in PDF form"*. | uygun | IEEEtran journal şablonu kullanılıyor. PDF'teki 47 fontun hepsi gömülü (`pdffonts`), Type 3 font yok. | — |
| 3 | **Şekil ve tabloların yeri** [TWC-P]: *"Figures and tables should be placed along with text, rather than at the end"* | uygun | Şekil ve tablolar §III ve §VI içinde, metinle birlikte duruyor. | — |
| 4 | **Zorunlu fazla sayfa ücreti** [TWC-P]: *"US$220 for each Transactions page exceeding ten printed pages"*. Ücret *"final typeset length, including biographies and pictures"* üzerinden hesaplanır. | belirsiz | Bugün 9 sayfa, biyografi ve fotoğraf yok. Son dizgide biyografiler (yaklaşık 1/3–1/2 sayfa) ve hakem eklemeleri 10 sayfayı aşabilir. | Revizyonda 10 sayfa sınırı izlenmeli. Gönülsüz ücret ilk 10 sayfa için sayfa başına US$110. |
| 5 | **Özet uzunluğu** [TWC-P]: *"The abstract should be 75 to 200 words"*. [AC-S] genel üst sınırı 250 kelime ve tek paragraf olarak veriyor. | uygun (sınırda) | `pdftotext` ile 199 kelime ("Abstract—" dahil), LaTeX kaynağında yaklaşık 193 kelime. Tek paragraf. | Özete tek kelime bile eklenirse sınır aşılır. Her değişiklikten sonra kelimeler yeniden sayılmalı. |
| 6 | **Özet içeriği** [AC-S]: *"without abbreviations, footnotes, references, or mathematical equations"*. Ayrıca: *"do not include mathematical symbols in your … abstract"*. | uygun değil | Özette `$t=0$` sembolü var. Açılmamış kısaltmalar var: "3GPP", "MISO", "CPU". | `$t=0$` yerine "at the start" ya da "before any delay" yazılmalı. "MISO" açık yazılmalı ("multiple-input single-output") ya da çıkarılmalı. "CPU" yerine "one processor thread" yazılabilir. Kelime sayısı 200'ü geçmemeli (bkz. #5). |
| 7 | **Başlık** [TWC-P]: *"The title should be descriptive and specific"* | uygun | Makale başlığı: "Latency-Aware Phase Optimization for Reconfigurable Intelligent Surfaces Serving Mobile Users" | Ama bkz. #19: hazırlık listesindeki başlık bundan farklı. |
| 8 | **Anahtar kelime sayısı** [AC-S]: *"Include 3-5 keywords or phrases"* | uygun değil | Index Terms bölümünde 7 terim var. | 5 terime indirilmeli. Örnek: Reconfigurable intelligent surfaces; mobility; channel aging; latency; MISO communication. Aynı liste portala da girilmeli. [TWC-P] bir sayı belirtmiyor, kural IEEE'nin genel kılavuzundan. |
| 9 | **Standart terimler** [AC-S]: *"Using the IEEE Thesaurus can help you find the best standardized keywords"* | belirsiz | "effective rate", "computation latency" ve "deep unfolding" büyük olasılıkla Thesaurus terimi değil. Thesaurus erişim gerektirdiği için doğrulanamadı. | Kullanıcı terimleri IEEE Thesaurus'ta kontrol etmeli. |
| 10 | **Makale yapısı** [TWC-P]: *"introduction shall motivate the contribution, review relevant prior work … and summarize the main outcomes"* | uygun | Giriş katkıları listeliyor (§I-A), ayrıca bir İlgili Çalışmalar bölümü (§II) var. | — |
| 11 | **Sonuç bölümü** [TWC-P]: Conclusions *"do not restate the claims in the abstract, but rather provides a summary of key takeaways"* | uygun değil | `section_07_conclusion.tex` maddelerinin 1, 2 ve 5'i özetin cümlelerini neredeyse aynen tekrarlıyor ("0.9--5.9~s and lose to a 2.5~ms single-user heuristic", "peaks at 4--6 steps … costs 14.0\%"). | Maddeler sayıları tekrarlamak yerine çıkarımları anlatmalı. "Practical rules" ve "Limitations" paragrafları zaten doğru türde. Sayılar değişmemeli, yalnızca anlatım değişmeli. |
| 12 | **Yazar bilgisi** [TWC-P]: sayfa sınırına *"names of the authors and their complete contact information"* dahil. [AC-S]: *"the country and corresponding author's e-mail address must be included"*. | uygun | `\thanks` dipnotlarında her yazarın bölümü, kurumu, ülkesi (Türkiye) ve e-postası var. Sorumlu yazar belirtilmiş. | (İsteğe bağlı) Ç. Çalhan için gmail yerine kurumsal adres kullanılabilir. |
| 13 | **Fon bilgisinin yeri** [AC-S]: finansal destek ilk dipnotta yazılır, *"not in the Acknowledgment"* | uygun | Fon yok (hazırlık listesinde "Fon: Yok"). Teşekkür bölümünde fon bilgisi yok. | Fon varsa ilk dipnota eklenmeli. |
| 14 | **AI kullanımının açıklanması** [AC-AI]: AI kullanımı *"shall be disclosed in the acknowledgments section"*. Kullanılan sistem adıyla belirtilmeli: *"The AI system used shall be identified"*. AI içerik kullanılan bölümler, AI'ın *"the level at which the AI system was used"* kısa açıklamasıyla birlikte belirtilmeli. | belirsiz (kısmen uygun) | Teşekkür bölümünde açıklama var: Claude (Anthropic) adıyla geçiyor ve kullanım düzeyi anlatılıyor (metin taslağı, kod, şekiller, kaynak kontrolü). **Hangi bölümlerde** kullanıldığı söylenmiyor. | Bir cümle eklenmeli. Örnek: "AI-assisted drafting was used in all sections; …" ya da AI kullanılan bölümlerin listesi. Kullanıcı ifadeyi ortak yazarlarla onaylamalı. |
| 15 | **Kaynakça** [AC-S]: *"only cite references that directly support your work"*. Biçim IEEE Editorial Style'a uymalı. | uygun | `IEEEtran.bst` kullanılıyor. 48 kaynağın 48'i de metinde atıflı. | — |
| 16 | **Benzer çalışmayı açıklama** [TWC-P]: *"Notice of any substantially similar paper … must be disclosed at the time of submission … and cited in the actual manuscript"* | kullanıcı yapacak | Yazarların AISY 2026 makalesi (`SavasciSen2026AISY`) §II'de atıflı. Simülasyon altyapısı bu çalışmadan Python'a taşınmış. | AISY makalesi portalda "related/similar paper" alanına yazılmalı. Konferans sürümü varsa ikisi de bildirilmeli. |
| 17 | **Daha önce reddedilen makale** [TWC-P]: gönderimde *"new submission or a resubmission"* sorusu cevaplanır | kullanıcı yapacak | — | Portaldaki soru dürüstçe cevaplanmalı. |
| 18 | **ORCID** [TWC-P]: *"All IEEE publications require an … ORCID for all authors"* | uygun değil, kullanıcı yapacak | Hazırlık listesinde Seda Savaşçı Şen'in ORCID'i "[eksik]". | ORCID alınıp Author Portal hesabına bağlanmalı. Sorumlu yazar bu olmadan gönderim yapamaz. |
| 19 | **Portal alanlarının makaleyle tutarlı olması** (genel gereklilik) | uygun değil | Hazırlık listesindeki başlık "Latency Can Reverse the Ranking: …", makaledeki ve kapak mektubundaki başlık "Latency-Aware Phase Optimization …". Listedeki 7 anahtar kelime makaledekilerle aynı, ama sayı fazla (bkz. #8). | Portala girilecek başlık makaledeki başlıkla aynı yapılmalı. |
| 20 | **Gönderim sistemi** [TWC-P]: *"IEEE Author Portal [https://ieee.atyponrex.com/journal/twc]"* | uygun değil (taslak) | `GONDERIM_TASLAKLARI.md` hem kapak mektubunda hem önerilen hakemler bölümünde "ScholarOne" diyor. | Taslaktaki "ScholarOne" ifadeleri "IEEE Author Portal" olarak değiştirilmeli. Ayrıca [TWC-P]'ye göre portalda 100 kelimelik özet artık istenmiyor: *"removing the requirement of a 100 word summary"*. |
| 21 | **Kapak mektubu** | belirsiz | [TWC-P] kapak mektubunu zorunlu tutmuyor. Taslak mevcut, tarih alanı "[Date]" olarak boş. | Tarih doldurulmalı. "not under consideration elsewhere" cümlesi #16 ile tutarlı olmalı, AISY makalesinden ayrılan noktalar bir cümleyle anılabilir. |
| 22 | **Önerilen ve karşı olunan hakemler** | belirsiz | [TWC-P] yazarlar için bu konuda bir kural koymuyor. Editör yönergesine göre editör en az bir hakemi kendisi seçer, *"not cited in the paper's references"*. **Önerilen 5 hakemden 2'si (Chongwen Huang, Anastasios Papazafeiropoulos) şu an TWC editörü** ([TWC-EB]). | Editör olan isimlerin yerine başka uzmanlar önerilmesi tavsiye edilir. Kurumlar ve e-postalar teyit edilmeli. |
| 23 | **Telif formu** [TWC-P]: gönderimin sonunda *"a signed copy of the IEEE Copyright Form"* istenir | kullanıcı yapacak | — | Gönderim sonunda açılan elektronik form imzalanmalı. |
| 24 | **Preprint (arXiv)** [TWC-P] ve [AC-PP]: önceden yayımlanmış her preprint'in ilk ekranına şu not eklenmeli: *"This work has been submitted to the IEEE for possible publication. …"* | kullanıcı yapacak | Depoda bir arXiv sürümüne dair iz yok. | arXiv'e yüklenecekse bu not eklenmeli. Kabulden sonra IEEE telif notu konmalı. |
| 25 | **Veri ve kod** | belirsiz | [TWC-P] veri ya da kod paylaşımını zorunlu tutmuyor. Makalede "Data and Code Availability" bölümü var. Verilen bağlantı (`github.com/sedasavascisen/ris-latency-mobility`) bu oturumdan doğrulanamadı (403). | Gönderimden önce deponun herkese açık olduğu ve içeriğinin tam olduğu kontrol edilmeli. Çift-kör değil tek-kör inceleme yapıldığı için yazar adının bağlantıda görünmesi sorun değil. |
| 26 | **Biyografiler** | belirsiz | [TWC-P] gönderim aşamasında biyografi istemiyor, yalnızca fazla sayfa ücretinin biyografilerle hesaplandığını söylüyor. Makalede biyografi yok. | Gönderim için gerekli değil. Kabulden sonra eklenmeli (bkz. #4). |
| 27 | **Şekiller** [AC-G]: *"checking whether they can be interpreted correctly from a greyscale printout"* | belirsiz | Şekillerin gri tonlamada okunup okunmadığı görsel olarak kontrol edilmedi. Şekillerin fontları gömülü (TrueType). | Gri tonlamada bakılmalı. Çizgiler kalın olmalı ve her birinin ayrı işaretçisi olmalı. |
| 28 | **İngilizce** [TWC-P]: *"must be written in fluent English, or will be returned without review"* | uygun | Metin akıcı. | — |
| 29 | **Kapsam** [TWC-P]: kanal özelliklerinin *"play a prominent role"* | uygun | Çalışma kanalın eskimesi, Doppler ve 3GPP InH kanal modeli üzerine kurulu. | — |
| 30 | **Yıllık gönderim sınırı ve "Part I/II" yasağı** [TWC-P] | uygun | Bir yazar yılda en çok 36 yeni gönderi yapabilir. Başlıkta "Part" yok. | — |

## Yapılması gerekenler

### Metinde düzeltilecek
*Bu denetimde metne dokunulmadı. Düzeltmeleri kullanıcı onaylamalı.*

1. **Özet (#6):** `$t=0$` sembolü çıkarılmalı. "MISO" açık yazılmalı ya da çıkarılmalı, "3GPP" ve "CPU" sadeleştirilmeli. Bu sırada özet 200 kelimeyi geçmemeli (#5; şu an 199).
2. **Index Terms (#8):** 7 terim 5'e indirilmeli, mümkünse IEEE Thesaurus terimleri kullanılmalı (#9).
3. **Sonuç (#11):** Maddeler 1, 2 ve 5 özetin cümlelerini tekrarlamayacak biçimde, çıkarım odaklı yeniden yazılmalı. Sayılar değişmemeli.
4. **AI açıklaması (#14):** AI'ın hangi bölümlerde kullanıldığını söyleyen bir ifade eklenmeli.
5. **`GONDERIM_TASLAKLARI.md` (#19, #20, #21, #22):**
   - Başlık makaledeki başlıkla aynı yapılmalı.
   - "ScholarOne" yerine "IEEE Author Portal" yazılmalı.
   - Kapak mektubunda "[Date]" doldurulmalı.
   - Hakem listesinden TWC editörü olan iki kişi çıkarılmalı.

### Gönderimde kullanıcının yapacağı
1. Seda Savaşçı Şen için ORCID alınıp portal hesabına bağlanmalı. **Bu zorunlu** (#18).
2. Portalda benzer çalışma olarak AISY 2026 makalesi bildirilmeli (#16). "Previously rejected" sorusu cevaplanmalı (#17).
3. Gönderim sonunda IEEE telif formu imzalanmalı (#23).
4. GitHub deposunun herkese açık ve eksiksiz olduğu doğrulanmalı (#25).
5. arXiv'e yüklenecekse IEEE gönderim notu eklenmeli (#24).
6. Anahtar kelimeler IEEE Thesaurus'ta kontrol edilmeli (#9). Şekiller gri tonlamada kontrol edilmeli (#27).
7. Kabulden sonra biyografiler eklenmeli ve 10 sayfa sınırı izlenmeli (#4, #26).

---

## Güncelleme (9 Kasım 2026, kontrol listesinden sonra yapılanlar)

| Madde | Durum |
|---|---|
| Özette sembol ve açılmamış kısaltma | **Düzeltildi.** `$t=0$` → "on the initial channel"; "3GPP … MISO" → "standardized indoor-office multi-user multiple-input single-output"; "CPU" → "processor". Özet 192 kelime. |
| Anahtar kelime sayısı (3–5) | **Düzeltildi.** 5 terim: Reconfigurable intelligent surface, phase optimization, mobility, channel aging, computation latency. |
| Sonuç bölümünün özeti tekrar etmesi | **Düzeltildi.** 1., 2. ve 5. maddeler yorum odaklı yeniden yazıldı; özetteki sayılar tekrarlanmıyor. |
| YZ beyanında bölümlerin belirtilmesi | **Düzeltildi.** "to draft and edit the text of all sections". |
| Taslaklardaki eski başlık, ScholarOne, [Date] | **Düzeltildi.** Yeni başlık, IEEE Author Portal, tarih. |
| Önerilen hakemlerden ikisi TWC editörü | **Kullanıcı yapacak.** Papazafeiropoulos ve C. Huang listede "çıkarın" olarak işaretlendi; yerlerine iki isim gerekiyor. |
| Sorumlu yazarın ORCID'i | **Tamam.** 0000-0001-8569-6454 |
| AISY 2026 makalesini portalda ilgili yayın olarak bildirmek | **Kullanıcı yapacak.** |
| GitHub bağlantısı | **Kullanıcı yapacak.** Depo açılmadan gönderilmemeli; makale bu adresi veriyor. |
