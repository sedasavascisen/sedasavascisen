# Makale 2: birebir Türkçe çalışma çevirisi

`makale2_tr.pdf` dosyası, IEEE TWC'ye gönderilecek İngilizce makalenin (`../makale2_revizyon/mobility_paper_ieee.tex`, commit 009fad4; 21. tur değişiklikleri çeviride zaten açık) cümle cümle Türkçe çevirisidir. Okuma ve tez yazımı için bir çalışma kopyası; gönderilecek metin İngilizce olandır.

- **Ortak bırakılanlar:** şekiller ve kaynakça İngilizce makaleyle ortak (`graphicspath`, `\bibliography` İngilizce klasöre bakıyor). Şekillerin içindeki etiketler İngilizce. Üç tablonun metni çevrildi; tablodaki sayılar değişmedi.
- **Eşlik denetimi:** `python3 esitlik_denetimi.py`. Her dosyada sayılar, matematik ifadeleri, `\ref`, `\eqref`, `\cite`, `\label`, `\input` ve `\includegraphics` İngilizceyle birebir aynı; 11/11 TAMAM.
- **Terimler:** `SOZLUK.md`.
- **Derleme:** `pdflatex makale2_tr; bibtex makale2_tr; pdflatex ×3`. Sonuç 10 sayfa; Türkçe metin İngilizceden daha uzun.
- **Bağlamdan açık yazılan iki belirsizlik:**
  - §VI-H'deki "it" koordinat inişi;
  - Sonuç bölümündeki "moves a flat optimum up" ifadesi daha fazla adım demek.
- **İngilizce makale değişirse** bu çeviri de güncellenmeli; eşlik denetimi farkı gösterir.
