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
