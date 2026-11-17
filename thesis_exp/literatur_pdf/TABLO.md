# Kullanıcının verdiği 10 makale: doğrulanmış künyeler ve tezle karşılaştırma

Kaynak: her makalenin PDF'i (yerel, `pdf/` klasörü; git'te yok) ve ondan çıkarılan not (`notlar/`). Bütün sayılar notlarda sayfa ve tablo referansıyla verilmiştir.

## 1. Künyeler: listendeki bilgiyle karşılaştırma

| # | Doğru künye (PDF'te basılı) | Listendeki bilgi | Durum |
| --- | --- | --- | --- |
| 1 | J. Chen, W. Shen, S. Luo, S. Ma, C. Xing, L. Hanzo, *IEEE Internet of Things Journal*, 11(1), 677–691, 2024, doi:10.1109/JIOT.2023.3286279 | "IEEE TVT / ePrints Soton" | **Dergi yanlış:** TVT değil, IoT-J. |
| 2 | C. Xu, L. Xiang, J. An, C. Dong, S. Sugiura, R. G. Maunder, L.-L. Yang, L. Hanzo, *IEEE Internet of Things Journal*, 10(1), 682–703, 2023, doi:10.1109/JIOT.2022.3203895 | "C. Xu, J. An, T. Bai, L. Hanzo; IEEE OJVT" | **Yazarlar ve dergi yanlış:** IoT-J, 8 yazar. |
| 3 | C. Xu, J. An, T. Bai, S. Sugiura, R. G. Maunder, Z. Wang, L.-L. Yang, L. Hanzo, *IEEE TVT*, 72(1), **718–734**, 2023, doi:10.1109/TVT.2022.3203818 | "pp. 642–658" | **Sayfalar yanlış;** yazar listesi eksik. |
| 4 | T. Li, H. Tong, Y. Xu, X. Su, G. Qiao, *IEEE TVT*, 71(8), 8630–8645, 2022, doi:10.1109/TVT.2022.3174420 | aynı | Doğru. |
| 5 | Q. Zhang, C. Yu, Y. Zhao, B. Wang, J. Zhao, "Channel estimation for RIS-aided communication in high-speed railway based on deep transfer learning" | "C. Yu et al., Beijing Jiaotong Univ." | **Ön baskı;** yayın yeri, yıl ve DOI yok. İlk yazar Zhang; kurum çoğunlukla Doğu Çin Jiaotong Üniv. Hakemli kaynak olarak atıf yapılmamalı. |
| 6 | A. Abdallah, A. Celik, M. M. Mansour, A. M. Eltawil, *IEEE TWC*, 22(5), 3503–3521, 2023, doi:10.1109/TWC.2022.3219140 | aynı | Doğru. |
| 7 | R. Li, S. Sun, M. Tao, *IEEE TWC*, 22(3), 2171–2184, 2023, doi:10.1109/TWC.2022.3210227 | "IEEE TWC / ResearchGate" | Doğru; cilt, sayı ve sayfa eklendi. |
| 8 | A. Siriwanitpong, K. Sanada, H. Hatano, K. Mori, P. Boonsrimuang, *IEEE Access*, 13, 13128–13142, **2025**, doi:10.1109/ACCESS.2025.3531009 | "IEEE Access, 2024" | **Yıl yanlış;** RIS içermiyor. |
| 9 | S. Singh, S. Majhi, U. Satija, *IEEE Communications Letters*, 29(5), 1092–1096, 2025, doi:10.1109/LCOMM.2025.3554345 | "M. M. Amri et al., IEEE SPL" | **Yazarlar ve dergi yanlış.** |
| 10 | P. Nuti, E. Balti, B. L. Evans, *IEEE VTC2022-Spring*, doi:10.1109/VTC2022-Spring54318.2022.9860779 | "GLOBECOM / arXiv:2112.08316" | **Konferans yanlış:** VTC değil GLOBECOM yazılmış. arXiv numarası PDF'ten doğrulanamadı. |

## 2. Tezin ekseniyle karşılaştırma

| # | Konu | Hareketlilik / Doppler | Geniş bant | RIS fazı | Hesaplama süresi | Süre eskimeye katılıyor mu? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | mmWave IoV kanal kestirimi | 80 km/h, 30 GHz | OFDM, 256 alt taşıyıcı | tüm alt taşıyıcılara ortak | yalnızca O(·) | Hayır |
| 2 | OTFS ve OFDM, SAGIN | yüksek Doppler | OFDM / OTFS | gecikme-Doppler alanında | O(·), çarpma sayısı | Hayır |
| 3 | Yüksek hareketlilikte kestirim | 45–135 mph, 2.6 GHz | dar bant | kapalı form | YOK; "neredeyse anlık" varsayımı | Hayır |
| 4 | Çift IRS, HSR | yüksek hızlı tren | — | BCD/MM optimizasyonu | O(·) | Hayır |
| 5 | Derin transfer öğrenmesi, HSR | 300 km/h, 3.5 GHz | OFDM, 624 alt taşıyıcı | yalnızca kestirim | YOK | Hayır |
| 6 | Derin öğrenme ve sıkıştırmalı algılama ile kestirim | — | frekans seçici | yalnızca kestirim | O(·) tabloları | Hayır |
| 7 | Ergodik hız, istatistiksel CSI | (istatistiksel) | MIMO-OFDM | Riemann eşlenik gradyan | O(·) | İstatistiksel CSI ile kaçınıyor |
| 8 | 1D CNN kestirim, HSR (RIS yok) | 500 km/h'ye kadar | OFDM | — | yalnızca parametre sayısı | Hayır |
| 9 | CNN ile CFO kestirimi, RIS-MIMO-OFDM | — | OFDM, 3GPP TDL | — | **63 ms/örnek çıkarım** | Hayır |
| 10 | Geniş bant RIS faz optimizasyonu (PGA) | — | MIMO-OFDM, 28 GHz | ortak faz, PGA | O(·) | Hayır |

**Sonuç (bu 10 makale için):** hiçbiri optimizasyonun ya da kestirimin kendi duvar saati süresini kanal eskimesine katmıyor. Yalnızca biri (9) çıkarım süresi raporluyor. Bu, tezin "gecikme sabit bir sistem parametresi olarak ya da hiç modellenmiyor" tespitini destekliyor. 3 numaralı makale açıkça "neredeyse anlık" varsayımı yapıyor (s. 718). Literatür boşluğu iddiası yine de "bu örneklem ve önceki tarama içinde, bilgimiz dahilinde" diye yazılmalı.

## 3. Denetleyicideki olası rolleri

| Rol | Makaleler |
| --- | --- |
| Ön uç: Doppler ve kanal kestirimi (denetleyicinin f_d girdisi) | 1, 3, 5, 6, 8 |
| Yavaş döngü: istatistiksel CSI ile RIS tasarımı | 7 |
| Geniş bant optimizasyon motoru: PGA, ortak faz | 10 |
| Karşılaştırma ve tartışma: OTFS, CFO, çift IRS | 2, 4, 9 |
