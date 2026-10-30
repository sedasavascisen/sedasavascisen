# Nasıl çalıştırılır

**Süreler hakkında.** Aşağıdaki her süre, boş bir Linux makinesinde
(yük < 0.4) komut gerçekten çalıştırılarak ölçüldü. Bu dosyanın ilk
sürümünde süreler tahmindi ve **hepsi şişkindi** — bazıları 45 kat.
Sebebi: o tahminleri, makine eğitim koşarken yaptığım koşulardan
çıkarmıştım. Sizin makineniz farklı olacaktır; bu sayıları mertebe
olarak alın, taahhüt olarak değil. Aynı komut iki koşu arasında 2–3 kat
oynayabilir.

---

## 1. Kurulum (bir kez, ~5 dakika)

### Dosyaları açın

İki arşivi **aynı klasöre** açın. Sıra önemli değil ama ikisi de aynı yere
gitmeli, çünkü ağırlıklar kodun `results/` klasörünün içine giriyor:

```bash
tar -xzf ris_mu_kodlar_2026-10-27c.tar.gz
tar -xzf ris_mu_agirliklar_2026-10-27.tar.gz
cd ris_mu_project
```

Doğru açıldığını kontrol edin:

```bash
ls ris_mu/mumiso/        # 10 .py dosyası (__init__.py dahil)
ls scripts/*.py | wc -l  # 47
ls results/*.pt | wc -l  # 10'dan fazla ağırlık dosyası
```

### Paketleri kurun

Sadece **iki** üçüncü taraf paket gerekiyor:

```bash
pip install numpy torch
```

Geliştirme ortamı Python 3.13 + torch 2.14 + numpy 2.5 idi. Python 3.9 ve
üstü, torch 2.x ile çalışması beklenir; GPU gerekmiyor, hepsi CPU'da koşar.

### Kurulumun doğru olduğunu sınayın

```bash
python3 scripts/verify_mumiso_system.py
```

**2 saniye** sürer. Sistem denklemlerini, ön kodlayıcıyı, gradyanları ve
kuantalayıcıyı sınar. Hata vermeden biterse kurulum tamamdır.

---

## 2. En önemli komut

```bash
python3 scripts/audit_claims.py
```

**4 saniye.** Projedeki 41 iddianın hepsini sınar ve `41/41` yazmalı.
Bir sayıyı teze koymadan önce bunu çalıştırın: bir şey kırılmışsa burada
görürsünüz.

Yavaş katmanı da dahil etmek için (§5 sayıları için gerekli; eğitim yok ama klasik optimizasyon var, dakikalar sürer):

```bash
python3 scripts/audit_claims.py --all
```

---

## 3. Yazım referansını yeniden üretmek

```bash
python3 scripts/make_writing_reference.py
```

**1 saniyeden az.** `results/*.json` dosyalarını okuyup
`TEZ_YAZIM_REFERANSI.md`'yi baştan yazar. Bir ölçümü yenilediğinizde bunu
çalıştırın; referans kendiliğinden güncellenir.

---

## 4. Tezdeki sayıları tek tek üretmek

Hepsi proje kökünden çalışır. Başka bir klasörden de çalıştırabilirsiniz —
betikler kendi yollarını bulur ve çıktıyı her zaman projenin `results/`
klasörüne yazar.

### Doğrulama betikleri

| Komut | Ölçülen süre | Ne yapar |
|---|---|---|
| `python3 scripts/verify_mumiso_system.py` | 2–9 sn | Sistem denklemleri, ön kodlayıcı, gradyanlar |
| `python3 scripts/verify_mumiso_channel.py` | 2–3 sn | Kanal üreteci tutarlı mı |
| `python3 scripts/verify_residual.py` | 4–7 sn | Artık kafa çapada mı başlıyor |
| `python3 scripts/verify_batch_dependence.py` | 3 sn | Veri setinin prefix kararsızlığı |
| `python3 scripts/verify_baseline_strength.py` | ~170 sn | Temel çizgiler yeterince güçlü mü |

### Tezdeki sayıları üreten betikler

| Komut | Ölçülen süre | Tezde nerede |
|---|---|---|
| `python3 scripts/mumiso_antenna_corr.py` | 1 sn | Bölüm 6, anten ekseni korelasyonu |
| `python3 scripts/mumiso_beam_staleness.py` | 2 sn | **Bölüm 5, yük taşıyan varsayım** |
| `python3 scripts/mumiso_precoder_cost.py` | 3 sn | Ek, ön kodlayıcı varsayılanının maliyeti |
| `python3 scripts/mumiso_step_cost.py` | 13 sn | Bölüm 4, adım başına gecikme |
| `python3 scripts/mumiso_gain_source.py` | 32 sn | Bölüm 6, kazancın kaynağı |
| `python3 scripts/mumiso_gain_sharing.py` | 41 sn | Bölüm 6, kazanç paylaşımının bedeli |
| `python3 scripts/mumiso_latency_repeat.py` | 56 sn | Bölüm 4, beş turluk gecikme |

`mumiso_beam_staleness.py` faz seçimini değiştirerek de koşturulabilir:

```bash
python3 scripts/mumiso_beam_staleness.py --phase su_average
python3 scripts/mumiso_beam_staleness.py --phase adam8
```

### Ağırlık arşivi gerektirenler

Şu betikler `results/*.pt` dosyalarını okur, yani **ağırlık arşivini
açmadan çalışmazlar**: `mumiso_step_cost`, `mumiso_latency_repeat`,
`mumiso_equal_step`, `mumiso_latency_parity`, `mumiso_budget`,
`mumiso_frontier`, `mumiso_aging`, `mumiso_quant_latency`.

Açmadıysanız hata şöyle görünür:

```
FileNotFoundError: ... 'results/mumiso_eqstep_L1.pt'
```

### Eğitim gerektirenler — asıl uzun olanlar bunlar

| Komut | Ölçülen süre | Tezde nerede |
|---|---|---|
| `python3 scripts/mumiso_run.py --samples 12000 --epochs 12 --baseline-n 300 --seed 11 --tag yeniden` | **15.4 dk** | Bölüm 4.1, üç mimarinin eğitimi |
| aynısı `--link-ratio` ile | **17.2 dk** | Bölüm 4.3, reddedilen temsil hipotezi |
| `python3 scripts/mumiso_equal_step.py --samples 6000` | eğitilmiş ağırlık gerektirir | Bölüm 4.5, eşit adım |
| `python3 scripts/mumiso_latency_parity.py --samples 6000` | eğitilmiş ağırlık gerektirir | Bölüm 4.5, eşit milisaniye |

Son ikisi `results/mumiso_eqstep_L*.pt` ağırlıklarını kullanır; ağırlık
arşivini açtıysanız yeniden eğitim gerekmez.

---

## 5. Gecikme ölçerken — makine boş olmalı

Gecikme ölçen betikler (`mumiso_step_cost`, `mumiso_latency_repeat`,
`mumiso_latency_parity`) **boş makinede** çalıştırılmalı. Bu, bu projede
fiilen yaşanmış bir hatadır: eğitim koşarken alınan bir ölçüm Adam'ın
zamanlamasını 17.5 ms'den 29.7 ms'ye şişirdi ve **hükmü tersine çevirdi**.

Kirlilik tarafsız değildir — hangi kolu daha çok yavaşlattığına göre
sonucu değiştirir.

Çalıştırmadan önce:

```bash
cat /proc/loadavg        # Linux
uptime                   # macOS
```

İlk sayı 0.5'in altındaysa güvenli. `mumiso_latency_parity.py` yükü
kendisi de ölçer ve yüksekse uyarı basar.

---

## 6. Sık karşılaşılan sorunlar

**`ModuleNotFoundError: No module named 'ris_mu'`**
Betikler kendi yollarını bulur, yani bu hata genelde arşivin yanlış
açıldığını gösterir. `ls ris_mu/mumiso/system.py` komutu dosyayı
bulmuyorsa, arşiv iç içe bir klasöre açılmıştır.

**`FileNotFoundError: results/mumiso_eqstep_L8.pt`**
Ağırlık arşivi açılmamış. `ris_mu_agirliklar_2026-10-27.tar.gz` dosyasını
aynı klasöre açın.

**Bir sayı benim raporladığımdan farklı çıkıyor**
Önce `--samples` değerinin aynı olduğunu kontrol edin. Veri seti **prefix
kararlı değil**: `generate(6000)` ile `generate(12000)[:6000]` farklı
kanallardır. Farklı örnek sayısıyla alınmış iki sayı karşılaştırılamaz.

**Çok yavaş**
Hepsi tek CPU çekirdeğinde koşuyor olabilir. Eğitim betikleri için
`OMP_NUM_THREADS` ayarını kaldırın; gecikme betikleri ise **bilerek**
tek çekirdeğe sabitlenmiştir (`torch.set_num_threads(1)`), çünkü
konuşlandırılmış bir RIS denetleyicisi bir küme değildir.

---

## 7. Yayımlanmış MATLAB kodunuza dokunulmadı

`duzeltilmis_kodlar.tar.gz` ayrı bir pakettir ve bu paketten etkilenmez.
Yayımlanan sonuçları üretmeye devam eder.
