# CLAUDE.md — bu projede çalışırken bilmen gerekenler

Bu bir doktora tezinin deneysel altyapısı. Buradaki sayılar savunulacak.
Aşağıdaki kuralların her biri **fiilen yaşanmış bir hatadan** çıktı.

---

## Mutlak kısıt

**Yayımlanmış MATLAB koduna dokunma.** `duzeltilmis_kodlar` ayrı bir
pakettir ve yayımlanmış sonuçları üretir. Bu proje onun *üzerine* ekleme
yapar, onu güncellemez. Kullanıcının sözleriyle: *"Bana makalemi
güncelletme sadece üzerine eklemeler yapıp doktora tezimi şekillendir."*

---

## Her oturumun ilk komutu

```bash
python3 scripts/audit_claims.py        # 108 iddia
python3 scripts/audit_claims.py --all  # §5 dahil, 123 iddia
```

`123/123` görmeden hiçbir sayıya güvenme. Bir şey kırıldıysa burada görünür.

---

## Altın kural: betiksiz sayı, ölçüm değildir

Sonuç taşıyan her sayının `scripts/` altında koşturulabilir bir kaynağı
olmak zorunda. Bu kural iki kez ihlal edildi ve **ikisinde de sayı yanlış
çıktı**:

- "Bütçede kalma oranı %95" → bağımsız ölçüm %85–90 buldu, orijinal betik
  yoktu
- "Taze/eskimiş hüzme 17 kat" → betiği yazılınca **11.7–14.2 kat** çıktı

Satır içi bir ölçüm yapıp sonucu rapora yazma. Önce betiği yaz.

---

## Ölçüm tuzakları

### Gecikme ölçerken makine boş olmalı

`mumiso_step_cost`, `mumiso_latency_repeat`, `mumiso_latency_parity` ve
`mumiso_budget_fraction` yük altında koşturulamaz. Kirlilik **tarafsız
değildir** — hangi kolu daha çok yavaşlattığına göre hükmü çevirir.

Fiilen yaşandı: eğitim koşarken alınan bir ölçüm Adam'ı 17.5 ms'den
29.7 ms'ye şişirdi ve "öğrenilen model cephede" diye yanlış bir sonuç
üretti. Boş makinede beş turda beş noktanın beşi de baskınlanmış çıktı.

Çalıştırmadan önce `cat /proc/loadavg`; ilk sayı 0.5 altında olmalı.

### Zayıf taban çizgisi — bu projede beş kez düşüldü

Öğrenilen bir yöntemi **sabit ayarlı** bir klasik yönteme karşı
karşılaştırma. Her gecikme bütçesinde klasik kolun **en iyi** ayarı
taranmalı (adım boyu **ve** objektif), doğrulama kümesinde seçilmeli,
test kümesinde raporlanmalı. Örnek: `scripts/mumiso_equal_step.py`.

Ayrıca: eşit adım ≠ eşit gecikme. Bir öğrenilen adım ~2.7 Adam adımı
ediyor. Adım ekseninde kazanan, milisaniye ekseninde kaybedebilir — bu
projede tam olarak böyle oldu.

### Veri seti prefix-kararlı değil

`generate(1000)` ile `generate(2000)[:1000]` **farklı kanallardır**;
`chunk` de veriyi değiştirir. Dağılımlar aynı, çekilişler farklı.

Farklı `--samples` ile alınmış iki sayıyı aynı tabloya koyma. Bir
checkpoint'i değerlendiriyorsan, eğitildiği `--samples` değerini kullan.

### `effective_rank` örnek sayısına bağlı

%32 yayılım var ve tekdüze bile değil (250→1000 arasında *ters* yönde
hareket ediyor). Bu sayıyı **n belirtmeden asla** yazma:
"etkin rank 21.0 (S = 16000)" doğru, "etkin rank ~21" değil.

---

## Değiştirme — sayıları oynatır

Bunlar bilinçli olarak öyle bırakıldı. Değiştirmek istiyorsan önce
kullanıcıya sor ve tüm paketi yeniden ölçmeyi planla.

| Ne | Neden öyle | Bedeli |
|---|---|---|
| `zf`'in MMSE varsayılanı | Kusurlu CSI'da karşılığını veriyor | Kusursuz CSI'da %2.20 (zor kuyrukta %4.95) |
| Anten ekseninde bağımsız kazançlar | Fizikçe yanlış ama tüm sayılar buna göre | Düzeltmek: çapa −%32, PGA −%8 |
| `unrolled.py`'deki `×0.01` | Ölü kod (`atan2` ölçekten bağımsız) ama kaldırmak sonuçları oynatmaz; dokunma | — |
| `features.link_ratio=False` | Geriye dönük uyum; 22 ağırlık dosyası buna bağlı | Açmak C'yi 37→39 yapar |

---

## Docstring'lere güvenme, ölçüme güven

Bu paketteki birkaç docstring, düzeltilmiş ön kodlayıcıdan **önceki**
sayıları taşıyordu ve biri Bulgu 1'in **çürütülmüş** açıklamasını
anlatıyordu. Hepsi düzeltildi ama ders kaldı: bir docstring'deki sayıyı
alıntılamadan önce üreten betiği koştur.

Özellikle: `[PRE-FIX]` ya da "stale" etiketi taşıyan her şey.

---

## Tezin çerçevesi

Savunu cümlesi: *hesaplama gecikmesi, hareketli RIS sistemlerinde
ikincil bir ölçüt değil, yöntem sıralamasını belirleyen birinci sınıf bir
tasarım kısıtıdır.*

Üç eksen: **hareketlilik** (olumlu sonuç, tezin omurgası), **çok
kullanıcılı öğrenme** (titiz negatif sonuç), **gerçekçi senaryo**
(kısmi).

Yapay zekâ ekseni **kapandı ve olumsuz**: tek geçişli tahmin çapada
donuyor (eğitilmemiş = eğitilmiş, 3.7230/3.7230), öğrenilen güncelleme
kuralı adım başına kazanıp milisaniye başına her noktada kaybediyor.
Bunu "çalışıyor" diye yeniden çerçevelemeye çalışma.

---

## Kullanıcının önceliği (30 Ekim 2026'da güncellendi)

Yaklaşık **iki ayı var** ve sırayı kendisi koydu: *önce bulgular, sonra
yazım*. Ölçüm fazı **20 Kasım'da kapanır**; o tarihten sonra yeni deney
açılmaz, eldekiyle yazılır.

Sıradaki üç iş, fayda/maliyet sırasıyla:

1. **Kazanç paylaşımını ebeveyn sınıfa işle** — en ucuz, en kârlı.
   Faz optimizasyonunun değerini 1.75×'ten 2.36×'e çıkarıyor.
2. **Kusurlu CSI** — öğrenmenin klasiği yenme şansının en yüksek
   olduğu tek rejim. İki kol ayrı raporlanır: temiz eğitilmiş modele
   gürültü vermek ≠ gürültüyle eğitmek.
3. **Ayrık faz (1/2/3 bit)** — jüri soracak. Aleyhte çıkma ihtimali
   yüksek (tek-RIS'te 1 bitte ayrık CD, 5.600'e 3.544 kazandı). Aleyhte
   çıkarsa da yazılır.

Öngörücü faz tasarımı **plan dışı**: önkoşulu olan dönüşlü yörünge yok
(`straight_line=False` dönüş üretmiyor). Gelecek çalışma.

Ayrıntılı görev tanımları ve kabul ölçütleri: `CLAUDE_CODE_PROMPT.md`.

---

## Dosya haritası

| Dosya | Ne |
|---|---|
| `TEZ_YAZIM_REFERANSI.md` | Teze girecek her sayı, bölüm bölüm, kaynağıyla |
| `NASIL_CALISTIRILIR.md` | Kurulum ve her betiğin ölçülmüş süresi |
| `DEGISIKLIKLER_2026-10-23.md` | Düzeltilen her hatanın kaydı |
| `README_MUMISO.md` | Bulguların uzun anlatımı |
| `ris_mu/mumiso/system.py` | Sistem denklemleri — tek doğruluk kaynağı |
| `scripts/audit_claims.py` | 123 iddia; sabotaj testiyle doğrulandı |
| `scripts/make_writing_reference.py` | Referansı yeniden üretir |
| `aisy_paket/` | AISY makalesinin temiz MATLAB paketi ve bulunan tutarsızlıklar (`README_TR.md`); `orijinal/` dokunulmaz |
| `ON_KAYIT_KISMI_CSI.md` | Ön kayıtlı kısmi CSI deneyi ve sonucu |

Yeni bir ölçüm yaptıysan: betiği `scripts/` altına koy, sonucu
`results/*.json`'a yaz, sonra `python3 scripts/make_writing_reference.py`.
