# RIS eleman kazancı: Tang ve ark. ile tutarsızlık ve duyarlılık (17 Kasım 2026)

## Bulgu (kaynak kontrolü grup 8; bağımsız olarak doğrulandı)

- **Kodun yaptığı:** `ris_mu/geometry.py` (`element_gain`) eleman kazancını G = 2(2q+1) alıyor. Kanal kodu (`ris_mu/channel.py:247–252`) ise örüntüyü güç örüntüsü olarak cos^q kullanıyor (genlikte √f_in).
- **Doğru değer:** cos^q güç örüntüsünün tepe kazancı 4π / ∫cos^q dΩ = 2(q+1). Sayısal integral q = 1 için 4.000 veriyor. Tang ve ark.'ın denklem (2)'si (s. 423) ve kendi örnekleri de bunu veriyor: cos³ için 8.
- **Fark:** q = 1'de kod 6 kullanıyor, Tang 4 veriyor. RIS yolunun gücü 1.5 kat (+1.76 dB) fazla.

## Duyarlılık (paket değiştirilmedi; kazanç yalnızca bu süreçte yamandı)

Komut `python3 thesis_exp/kazanc_duyarlilik/run.py`, ham çıktı `raw/results.json`. Kurgu: seed 11, 400 senaryo, taze ön kodlayıcı, aynı oturumda ölçülen gecikmeler.

| | 1.5 m/s, G = 6 | 1.5 m/s, G = 4 | 10 km/h, G = 6 | 10 km/h, G = 4 |
| --- | --- | --- | --- | --- |
| L* | Adam-6 | Adam-6 | Adam-4 | Adam-4 |
| L*'daki etkin hız | 6.151 | 5.845 | 5.913 | 5.622 |
| L = 48 kaybı | %14.8 | %15.3 | %13.5 | %13.1 |
| CD − SU-best-of [GA] | −0.215 [−0.316, −0.112] | −0.247 [−0.343, −0.151] | −0.278 [−0.390, −0.165] | −0.293 [−0.405, −0.175] |
| En iyi kol | Adam-6 | Adam-6 | Adam-4 | Adam-4 |
| SU-average t = 0 | 4.624 | 4.389 | 4.624 | 4.389 |

**Sonuç:** Tang'in kazancıyla mutlak hızlar yaklaşık %5 düşüyor: L*'daki etkin hız 1.5 m/s'de 0.31, 10 km/h'de 0.29 b/s/Hz. L*, L = 48 kaybı, CD'nin konumu ve en iyi kol değişmiyor. Bulgular kazanç seçimine duyarlı değil; yalnızca mutlak hızlar etkileniyor.

## Karar (kullanıcının)

1. **Paketi düzeltip bütün sayıları yeniden ölçmek** (CLAUDE.md: fizik değişikliği, tüm paket yeniden ölçülür).
2. **Paketi olduğu gibi bırakmak ve makalede açıkça belirtmek.** Bu yaklaşımın örneği, paylaşılan kazançlar sınırlamasıdır. Örnek cümle: "Our element gain 2(2q+1) differs from the 2(q+1) of [Tang] for a cos^q power pattern; with the latter, absolute rates fall by about 5% and L*, the losses and the rankings are unchanged."
