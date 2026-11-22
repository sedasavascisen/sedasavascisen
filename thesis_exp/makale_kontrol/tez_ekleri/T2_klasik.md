**Klasik yöntemlerin yayımlanan koddaki uygulaması**

| Yöntem | Amaçta h_d | Başlangıç | Güncelleme | Durma |
|---|---|---|---|---|
| CD | var | bütün fazlar 0 | eleman başına kapalı form, sürekli faz | sabit K tarama (K = 5) |
| AO | var | bütün fazlar 0 | CD ile aynı güncelleme | sabit, K = 1 |
| SPA | var | h_d | elemanları sırayla hizalama | tek geçiş |
| PGD | var | bütün fazlar 0 | gradyan adımı 0.2 + birim modüle izdüşüm | sabit 50 yineleme |
| "WMMSE" (betik) | var | bütün fazlar 0 | eleman başına bir gradyan adımı (0.1) | 1 yineleme |
| PSO | var (alınan güç) | rastgele, tekdüze | 20 parçacık | sabit 30 yineleme |
| Etiket (Denk. 8) | yok | — | −∠(G_n F_n) | — |

Kaynak: aisy_paket/orijinal/ris_CD.m; ris_AO/SPA/PGD/WMMSE/PSO.m satır satır aktarımı audit/scripts/step2_baselines.py
