# MATLAB ile bağımsız kontrol: faz-farkında CNN–LSTM, tek kullanıcılı MISO

Bu klasör, Python'da elde edilen sonuçları sizin MATLAB ortamınızda (GPU ile)
bağımsız olarak doğrulamak içindir. **Yayımlanmış kodunuza dokunmaz**; yeni bir
dosyadır.

## Dosyalar
| Dosya | Ne |
|---|---|
| `sumiso_cnnlstm_matlab.m` | Eğitim + test + gecikme ölçümü. Mimari ve eğitim ayarları `theta_NN_multioutput.m` ile aynı; yalnızca girdi 4T kanal |
| `sumiso_train_part1of2.mat`, `sumiso_train_part2of2.mat` | MISO veri seti (N_t=8, 40 000 senaryo), iki parça; betik ikisini birleştirir |
| `sumiso_siso.mat` | SISO kontrol veri seti (N_t=1) |

Veri setleri `scripts/sumiso_dataset.py` ve `scripts/sumiso_export_mat.py`
ile üretildi; eğitim/doğrulama/test bölmesi Python'daki ile **aynı**.

## Nasıl çalıştırılır
1. Bu klasörü bilgisayarınıza indirin (GitHub'dan dalı indirip `matlab_sumiso/`).
2. MATLAB'da bu klasöre geçin.
3. Betiğin başındaki ayarlar:
   - `tag = 'train'` → MISO (asıl deney)
   - `tag = 'siso'` → SISO kontrolü
   - `nEpochs = 50` → yayımlanmış reçete; ikinci koşuda `150` (kapasite kontrolü)
4. `run('sumiso_cnnlstm_matlab.m')`
5. Ekrana çıkan `=== SUMISO MATLAB RESULTS ===` ile `=== END ===` arasındaki
   bloğu kopyalayıp bana gönderin.

## Önerilen koşular (sırayla)
| # | tag | nEpochs | Neyi sınar |
|---|---|---|---|
| 1 | `train` | 50 | Python sonucu MATLAB'da da çıkıyor mu (beklenen RMSE ~61°, hız ~12.49) |
| 2 | `siso` | 50 | Tek antende beklenen ~15° |
| 3 | `train` | 150 | Daha uzun eğitim sonucu değiştiriyor mu (eksik eğitim itirazına cevap) |

Python'daki karşılıkları (aynı test bölmesi, 6000 senaryo): etiket 12.893,
SU-hizalama 12.431, CD-1 12.857, CNN–LSTM 12.490, CNN–LSTM + CD-1 12.855 b/s/Hz.
