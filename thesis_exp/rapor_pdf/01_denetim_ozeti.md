# Bağımsız denetim süreci — özet

**Yöntem.** Raporları yazmamış ayrı bir ajan, saat başı `thesis_exp/denetim_log/BRIEF.md`'deki görev tanımını uyguladı:
- sayıları ham JSON'a kadar izledi;
- raporları geçici kopyada yeniden üretip farkını aldı;
- her turda bir deney betiğini yanlılık, sızıntı, zayıf taban çizgisi ve tohum açısından inceledi;
- `results/` ve `paper_mobility/` klasörlerinin değişmediğini sınadı;
- yorumlarda aşırı iddia aradı.

Denetçi dosya değiştirmedi ve commit yapmadı. Her KRİTİK bulguyu ana oturum yeniden doğruladı; düzeltmeler `YANIT_*.md` ve günlüklerde kayıtlı.

| Tur | Zaman (UTC) | İzlenen sayı | KRİTİK | UYARI | Günlük |
| --- | --- | --- | --- | --- | --- |
| 1 | 12 Kasım 14:00 | ~70 | 1 (K1) | 10 (U1–U11; U10 kapsam notu) | `20261112_1400.md` |
| 2 | 12 Kasım 14:31 | — (tur 1 düzeltmeleri + yeni bölümler) | 1 (K2) | 8 (U12–U19) | `20261112_1431.md` |
| 3 | 12 Kasım 15:32 | 300+ | 1 (K3) | 4 (U20–U23) | `20261112_1532.md`, `YANIT_20261112_1532.md` |

Her turda ham veriyle çelişen sayı aranıyor. Turların ortak sonucu: K3 dışında ham veriyle çelişen sayı yok. K3'teki hata da ham veride değil, hesaplama yöntemindeydi.

**KRİTİK bulgular ve çözümleri**

| # | Bulgu | Çözüm | Hükme etkisi |
| --- | --- | --- | --- |
| K1 | 4.1 ve 4.4'ün betikleri koşu anında commit'lenmemişti (Kural 3) | Commit'li koddan yeniden koşuldu: commit alanı dışında 316/316/316/237 değer birebir aynı (`k1_rerun.md`) | Yok |
| K2 | Bir düzeltme metni yanlış aralık getirdi ("Adam-8…48→q" yerine "Adam-10…48→q") | Metin düzeltildi | Yok |
| K3 | 4.5'te 40 ms üstü kollar kaba ızgarada (50/75/100/150 ms) interpolasyonla değerlendirilmişti; ±0.055 b/s/Hz'e kadar hata | `run_exact.py`: her kol tam gecikmesinde; L48 kaybı %9.3/%13.6 → %9.5/%14.1 | Hükümler aynı |

**Önemli uyarılar ve çözümleri**

- **Sıralama iddiası (U4):** "Sıralama değişmiyor" iddiası fazla güçlüydü. Doğrusu: en iyi küme (Adam-4…8) korunuyor, aralarındaki farklar ayırt edilemiyor.
- **Ölçüt farkı (U2):** Pilot deneyinin ölçütü (50 ms ortalaması) Tanım 1'in anlık etkin hızından farklı. Bu fark belgelendi.
- **Desteklenmeyen cümle (U12):** Kusurlu CSI'da "hata arttıkça L küçülüyor" cümlesi ölçümle desteklenmiyordu. Veriden üretilen cümleyle değiştirildi (en iyi L: 6/3/5/1/6/4).
- **ρ tanımı (U13):** ρ, 400 senaryonun ortalama gücüne göre tanımlı. 30 dB, senaryo başına medyanda 22.6 dB etkin SNR'ye karşılık geliyor. Denetçinin betiği depoya alınıp yeniden koşuldu.
- **Betiksiz sayı (U16):** "~0.016" betiksiz bir tahmindi. Yerine ölçüm kondu (`p4/gecikme_muhasebesi`): 0.0001–0.021 b/s/Hz.
- **Adım boyu (U20):** Adam'ın adım boyu sabitti. Doğrulamada seçilen tasarım eklendi; hüküm değişmedi.

**Açık kalan:**
- U11: konum tabanlı fazda σ düzeyleri arasında eşli test yok.
- U19: köprü raporunda aynı fark iki ayrı GA ile verilmiş. Rapor başka dalda; değiştirilmedi.

**Kapsam değişikliği (13 Kasım):** Makale 1, kullanıcı isteğiyle denetim kapsamından çıkarıldı.
