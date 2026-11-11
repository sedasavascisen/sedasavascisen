# Köprü: tek geçişli faz-farkında ağ, etkin hız ölçütünde — rapor

Rapor commit'i `c1d72d0`. Eğitim verisi (onaylı seçenek ii): yaşlanma kümesinin yapısıyla (20 saçıcı, t=0) üretilmiş statik küme, seed 2027, 6000 senaryo, bölme 4200/900/900. Değerlendirme: yaşlanma kümesi (seed 11, 400 senaryo); seçimler yalnızca statik doğrulama kümesinde ve ayrı bir hareketlilik çekilişinde (seed 12).

## 1) Bulgular

1. **Yapılandırma seçimi (doğrulama, tohum 0):** net_res0_lr0_s0: 4.0423; net_res0_lr1_s0: 4.0152; net_res1_lr0_s0: 4.2720; net_res1_lr1_s0: 3.9881. SU-average aynı kümede 4.2709. Seçilen: `net_res1_lr0_s0`.
2. **Seçilen yapılandırmanın test min-hızı (3 tohum):** 4.2397, 4.2404, 4.2408; makalenin statik kümesinde eğitilen ikincil kol: 3.4784 (o kümenin testi).
3. **Etkin hız, 5.4 km/h** (doğrulamada seçilen en iyi klasik: Adam-5, 6.0382 b/s/Hz):
   - net: gecikme 2.847 ms, etkin 4.6204; fark -1.4179 [-1.5032, -1.3357]; baskınlayan klasik kollar: SU-best-of, Adam-1
   - net+Adam-1: gecikme 4.599 ms, etkin 5.4267; fark -0.6115 [-0.6669, -0.5603]; baskınlayan klasik kollar: Adam-1, Adam-2
   - net+Adam-2: gecikme 6.032 ms, etkin 5.7069; fark -0.3313 [-0.3691, -0.2965]; baskınlayan klasik kollar: Adam-2, Adam-3, Adam-4
   - net+Adam-3: gecikme 7.469 ms, etkin 5.8320; fark -0.2063 [-0.2317, -0.1804]; baskınlayan klasik kollar: Adam-3, Adam-4, Adam-5
4. **Tablo II hızları** (gecikmeler aynı ölçümden):
   - 3.0 km/h: en iyi klasik Adam-10; net -1.6534 [-1.7536, -1.5574], baskınlanan öğrenilen kol sayısı 4/4
   - 5.4 km/h: en iyi klasik Adam-5; net -1.4179 [-1.5065, -1.3366], baskınlanan öğrenilen kol sayısı 4/4
   - 10.0 km/h: en iyi klasik Adam-3; net -1.1672 [-1.2396, -1.0887], baskınlanan öğrenilen kol sayısı 4/4
   - 18.0 km/h: en iyi klasik Adam-2; net -0.9373 [-1.0148, -0.8626], baskınlanan öğrenilen kol sayısı 4/4
   - 30.0 km/h: en iyi klasik Adam-1; net -0.7134 [-0.7752, -0.6487], baskınlanan öğrenilen kol sayısı 4/4
5. **Periyodik çalışma** (seçim seed 12, rapor seed 11):
   - T_p=0.0 ms: soğuk 5.877 (U=b2b, L=4), sıcak 6.338 (U=b2b, L=3), ağ 5.666 (U=b2b, L=3); ağ−soğuk -0.212 [-0.226, -0.197], ağ−sıcak -0.672 [-0.707, -0.638]
   - T_p=0.86 ms: soğuk 5.249 (U=b2b, L=8), sıcak 5.450 (U=10.0, L=3), ağ 5.096 (U=20.0, L=3); ağ−soğuk -0.153 [-0.179, -0.129], ağ−sıcak -0.354 [-0.389, -0.320]
   - T_p=1.71 ms: soğuk 5.085 (U=40.0, L=12), sıcak 5.234 (U=20.0, L=3), ağ 4.979 (U=40.0, L=3); ağ−soğuk -0.105 [-0.140, -0.069], ağ−sıcak -0.255 [-0.301, -0.210]
   - T_p=3.43 ms: soğuk 4.975 (U=80.0, L=12), sıcak 4.995 (U=80.0, L=16), ağ 4.844 (U=80.0, L=3); ağ−soğuk -0.131 [-0.167, -0.095], ağ−sıcak -0.150 [-0.193, -0.108]

## 2) Tablo

| Kol | Gecikme (ms) | t=0 hız | Etkin hız [%95 GA] | Durum | Kanıt |
| --- | --- | --- | --- | --- | --- |
| SU-best-of | 1.632 | 5.2762 | 5.2771 [5.0521, 5.5124] | — | raw/eval_main.json |
| net | 2.847 | 4.6264 | 4.6204 [4.3786, 4.8455] | BASKINLANIYOR | raw/eval_main.json |
| net+Adam-1 | 4.599 | 5.4739 | 5.4267 [5.1905, 5.6687] | BASKINLANIYOR | raw/eval_main.json |
| net+Adam-2 | 6.032 | 5.7963 | 5.7069 [5.4699, 5.9381] | BASKINLANIYOR | raw/eval_main.json |
| net+Adam-3 | 7.469 | 5.9911 | 5.8320 [5.5984, 6.0774] | BASKINLANIYOR | raw/eval_main.json |
| Adam-1 | 1.903 | 5.4750 | 5.4657 [5.2214, 5.7024] | — | raw/eval_main.json |
| Adam-2 | 3.256 | 5.7961 | 5.7707 [5.5301, 6.0071] | — | raw/eval_main.json |
| Adam-3 | 4.730 | 5.9865 | 5.9228 [5.6967, 6.1560] | — | raw/eval_main.json |
| Adam-4 | 5.984 | 6.1118 | 6.0035 [5.7688, 6.2362] | — | raw/eval_main.json |
| Adam-5 | 7.205 | 6.2188 | 6.0382 [5.7933, 6.2834] | — | raw/eval_main.json |
| Adam-6 | 8.700 | 6.3162 | 6.0434 [5.7923, 6.2679] | — | raw/eval_main.json |
| Adam-8 | 11.172 | 6.4428 | 5.9879 [5.7524, 6.2261] | — | raw/eval_main.json |
| Adam-10 | 13.577 | 6.5321 | 5.8834 [5.6643, 6.1308] | — | raw/eval_main.json |
| Adam-12 | 16.733 | 6.6218 | 5.7410 [5.5028, 5.9786] | — | raw/eval_main.json |
| Adam-16 | 22.059 | 6.7488 | 5.5093 [5.2854, 5.7350] | — | raw/eval_main.json |
| Adam-20 | 26.583 | 6.8386 | 5.4044 [5.1822, 5.6397] | — | raw/eval_main.json |
| Adam-24 | 33.404 | 6.9002 | 5.3189 [5.0874, 5.5637] | — | raw/eval_main.json |
| Adam-32 | 42.931 | 6.9822 | 5.2805 [5.0405, 5.5388] | — | raw/eval_main.json |
| Adam-48 | 66.072 | 7.0496 | 5.1937 [4.9607, 5.4255] | — | raw/eval_main.json |

## 3) Komutlar, tohumlar, ham çıktılar

| Adım | Komut | Tohum | Ham çıktı |
| --- | --- | --- | --- |
| eğitim | bridge_train.py --residual {0,1} --link_ratio {0,1} --seed 0; seçilen yapılandırma --seed 1,2; --static_paper | veri 2027 (ikincil: 11), eğitim 0/1/2 | raw/train/*.json |
| etkin hız | bridge_eval.py --ckpt raw/train/<seçilen>_s0.pt --tag main (gecikme ölçümü, yük < 0.5) | seçim 12, rapor 11, bootstrap 0 | raw/eval_main.json |
| hızlar | bridge_eval.py --speeds_kmh 3,5.4,10,18,30 --latency_json raw/eval_main.json --tag speeds | aynı | raw/eval_speeds.json |
| periyodik | bridge_tracking.py | seçim 12, rapor 11 | raw/tracking.json |

## 4) Açık sorular

1. Ağ diğer tohumlarla değerlendirilsin mi? (Etkin hız ana değerlendirmesi tohum 0 ile yapıldı; tohum yayılımı 2. bulguda.)
2. Sonuç tezde 'tek geçiş başlangıç noktasında takılıyor; gecikme ekseninde de baskınlanıyor' diye mi yazılsın?

## 5) Yorum (bulgulardan ayrı)

- Kalıntı (residual) mod ağı SU-average başlangıcının etrafında tutuyor; bu, tezdeki 3.7230/3.7230 bulgusunun bu veride tekrarı.
