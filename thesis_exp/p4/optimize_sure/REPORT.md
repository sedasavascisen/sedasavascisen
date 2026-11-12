# Deney 4.6 — Optimize edilmiş çalışma süreleri: Adam adımı ve öğrenilen adım (rapor)

Commit `c84b50c` (ölçüm commit'i `06c9b17986af81356a97143638a30a46f123775b`). torch 2.15.0+cu132, CPU: Intel(R) Xeon(R) Processor @ 2.10GHz, iş parçacığı 1, CUDA: False. Yük ortalaması: başlangıç 0.62, ölçüm öncesi 0.49, sonrası 1.00. Öğrenilen adım: UnrolledMuMiso (exchange, use_grad), eğitilmemiş ağırlıklar (ağırlık değeri yürütme yolunu değiştirmez). Adam: SU-average başlangıcı + L adım (soft-min, β=8, lr 0.5). 20 senaryo; senaryo başına 20 çağrının medyanı, senaryolar üzerinden medyan, 3 tur.

## 1) Süreler (ms, tur medyanlarının medyanı)

| Kol | Medyan (ms) | Turlar (ms) |
| --- | --- | --- |
| Adam-1 [eager] | 1.703 | 1.735, 1.685, 1.703 |
| learned-1 [eager] | 3.544 | 3.469, 3.830, 3.544 |
| Adam-8 [eager] | 10.405 | 10.405, 10.421, 9.935 |
| learned-8 [eager] | 29.178 | 29.178, 30.938, 29.102 |
| Adam-1 [torch.compile] | 2.184 | 2.284, 2.184, 2.169 |
| learned-1 [torch.compile] | 4.220 | 133.441, 4.220, 4.152 |
| Adam-8 [torch.compile] | 13.487 | 13.487, 13.532, 13.273 |
| learned-8 [torch.compile] | 41.679 | 41.651, 41.679, 41.863 |
| Adam-1 [torch.jit.trace] | ÜRETİLEMEDİ: RuntimeError: Adam's step uses torch.optim and autograd inside the loop; torch.jit.trace cannot capture the optimiser update | — |
| learned-1 [torch.jit.trace] | ÜRETİLEMEDİ: RuntimeError: Cannot insert a Tensor that requires grad as a constant. Consider making it a parameter or input, or detaching the gradient Tensor: -1.7194 [ torch.FloatTensor{1} ] | — |
| Adam-8 [torch.jit.trace] | ÜRETİLEMEDİ: RuntimeError: Adam's step uses torch.optim and autograd inside the loop; torch.jit.trace cannot capture the optimiser update | — |
| learned-8 [torch.jit.trace] | ÜRETİLEMEDİ: RuntimeError: Cannot insert a Tensor that requires grad as a constant. Consider making it a parameter or input, or detaching the gradient Tensor: -1.7194 [ torch.FloatTensor{1} ] | — |
| GPU | ÜRETİLEMEDİ: torch.cuda.is_available() is False on this machine | — |

## 2) Öğrenilen / Adam süre oranı

| Arka uç, L | Oran |
| --- | --- |
| eager L=1 | 2.08 |
| eager L=8 | 2.80 |
| torch.compile L=1 | 1.93 |
| torch.compile L=8 | 3.09 |

## 3) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/optimize_sure/run.py | senaryo seed 11, torch.manual_seed 0 | raw/results.json, raw/run.log |

## 4) Yorum (bulgulardan ayrı)

- **Optimizasyon hükmü değiştirmedi.** Öğrenilen adım her denenen arka uçta Adam'dan yavaş: L=8'de 2.80× (eager) ve 3.09× (torch.compile). CLAUDE.md'deki "bir öğrenilen adım ~2.7 Adam adımı ediyor" bulgusuyla tutarlı.
- **torch.compile bu iş yükünde hızlandırmadı, iki kolu da yavaşlattı.** Adam-8 10.41 → 13.49 ms, öğrenilen-8 29.18 → 41.68 ms. Bunun iki kaydedilmiş nedeni var:
  - Inductor karmaşık sayılı işlemler için kod üretmiyor (run.log uyarısı).
  - Öğrenilen kolun `forward`'ı yeniden derleme sınırına (256) takıldı. Bu, kolun büyük ölçüde derlenmemiş yolda ve koruma (guard) yüküyle koştuğu anlamına geliyor.

  Bu nedenle "torch.compile" satırı bu kod için iyi optimize edilmiş bir sürüm değil. Karmaşık işlemleri gerçek/sanal parçalara ayıran bir yeniden yazım denenmedi.
- **learned-1 [torch.compile] ilk turu 133 ms** (derleme ısınmaya sığmadı). Medyan, sonraki iki turla aynı düzeyde (4.2 ms).
- **torch.jit.trace iki kolda da ÜRETİLEMEDİ.** Adam'da optimizasyon adımı izlenemiyor. Öğrenilen kolda iç gradyan (use_grad) izlemede sabite gömülemiyor.
- **GPU ölçümü ÜRETİLEMEDİ: bu makinede CUDA yok.** GPU'da tek senaryoluk küçük işlemlerde çekirdek başlatma yükü baskın olur; ama bu ölçülmedi, sıralama hakkında bir şey söylenemez.
- **Adam-1 [eager] 1.70 ms SU-average başlangıcını da içeriyor.** Altyapı raporundaki 1.328 ms/adım yalnızca adımın süresi. İkisi aynı tanım değil.
- **Ölçüm sonrası yük 1.00.** Ölçülen tek iş parçacıklı süreç ve derleme işçileri buna katkı veriyor; ölçüm öncesi 0.49.
