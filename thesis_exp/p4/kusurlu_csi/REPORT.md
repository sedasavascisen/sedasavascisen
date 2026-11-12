# Deney 4.4 — Pilot SNR'sine bağlı kusurlu CSI (rapor)

Rapor commit'i `dfcbb1c`, ölçüm commit'i `06fc9d2` (results.json; o commit'te run.py yoktu — commit'li koddan bit-bit yeniden üretim: thesis_exp/denetim_log/k1_rerun.md). Hata modeli ris_mu/mumiso/csi.py (F, G, h_d için ayrı ölçek, gücü koruyan), e2 = 1/(1+ρ), ρ = kestirim sonrası pilot SNR'si; hata ölçeği 400 senaryonun ORTALAMA gücünden alınıyor (csi._noisy), bu yüzden senaryo başına etkin SNR dağınık: ρ = 30 dB, G için senaryo başına medyan 22.6 dB, %5 dilim 11.5 dB (test kümesi; doğrulamada 24.1 / 11.9 dB) [denetim_log/scripts/u13_csi_rel_err.out]. Teslim anındaki yeni kestirimin pilot süresi hesaba katılmadı. Seçilen lr 5 dB ve 0 dB'de bazı L'ler için ızgaranın ucunda (0.1 / 1.0). Doğrulama kümesinde senaryo kimliği sınanmadı. Faz t=0 kestiriminden; teslim anında ZF, aynı ρ ile yeni bir kestirimden; hız gerçek kanalda. Adam adım boyu her ρ ve L için doğrulama çekilişinde (seed 12, etkin hız üzerinden) seçildi; rapor yaşlanma kümesi (seed 11). Gecikmeler: tek iş parçacıklı yeniden ölçüm.

## 1) Bulgular

| ρ | e2 | Doğrulamada seçilen | Etkin hız [%95 GA] | SU-best-of | Fark [%95 GA] | Testte en iyi Adam-L |
| --- | --- | --- | --- | --- | --- | --- |
| perfect | 0.0000 | Adam-6 | 6.0770 [5.8560, 6.3141] | 5.2771 | +0.7999 [+0.7350, +0.8629] | Adam-6 |
| 30dB | 0.0010 | Adam-3 | 3.5367 [3.3551, 3.7258] | 3.1931 | +0.3436 [+0.2685, +0.4184] | Adam-3 |
| 20dB | 0.0099 | Adam-5 | 1.4015 [1.2840, 1.5203] | 1.2673 | +0.1342 [+0.0691, +0.2005] | Adam-5 |
| 10dB | 0.0909 | Adam-4 | 0.2952 [0.2626, 0.3291] | 0.3019 | -0.0067 [-0.0371, +0.0236] | Adam-1 |
| 5dB | 0.2403 | Adam-20 | 0.1581 [0.1429, 0.1750] | 0.1641 | -0.0061 [-0.0248, +0.0137] | Adam-6 |
| 0dB | 0.5000 | Adam-5 | 0.1166 [0.1087, 0.1248] | 0.1173 | -0.0006 [-0.0124, +0.0114] | Adam-4 |

## 2) Komut, tohum, ham çıktı

| Komut | Tohum | Ham çıktı |
| --- | --- | --- |
| python3 thesis_exp/p4/kusurlu_csi/run.py | kanal 11/12, kestirim gürültüsü 100+i / 200+i, bootstrap 0 | raw/results.json |

## 3) Yorum (bulgulardan ayrı)

- Kestirim hatası etkin hızı çok hızlı düşürüyor; bu, düz ZF'nin kanal hatasına duyarlılığı (csi.py docstring'inde ölçülmüş).
- En iyi adım sayısı hatayla tekdüze değişmiyor: testte en iyi L 6/3/5/1/6/4, doğrulamada seçilen 6/3/5/4/20/5 (ρ = kusursuz/30/20/10/5/0 dB). 10 dB ve altında yöntemler ayırt edilemiyor (GA sıfırı içeriyor). (Önceki sürümdeki 'hata büyüdükçe L küçülüyor' cümlesi ölçümle desteklenmiyordu; denetim U12.)
- ρ'nun gerçek pilot bütçesine (sembol sayısı, iletim gücü) bağlanması bu deneyin kapsamı dışında; ρ burada serbest parametre.
