# FIGURE GENERATION INSTRUCTIONS
# ================================

## 🎨 READY TO GENERATE

Figür scripti hazır: `generate_figures.py`

**Commit**: `c58c58e`

---

## ✅ 4 FİGÜR ÜRETİLECEK

### **Figure 3: Fresh vs Stale Beam** (11.7-14.2×)
- Data: KEY_NUMBERS.md (mumiso_beam_staleness.py)
- Shows: 3 phase methods, fresh vs stale bars
- Annotation: "11.7-14.2× Fresh Beam Advantage"
- **CORRECTED**: Uses 3.59-4.36 bps/Hz (NOT 9.61)

### **Figure 5: Intrinsic Optimum** (L*≈8 CORRECTED)
- Data: KEY_NUMBERS.md (mumiso_equal_step.py)
- Shows: Rate vs L curve with L=8 peak
- Annotations:
  - L=8: "Peak 5.380 bps/Hz (L*≈8)"
  - L=4: "5.025 bps/Hz (93% of peak)"
  - L=48: "5.064 bps/Hz (staleness -5.9%)"
- **CRITICAL FIX**: Shows L*≈8 (NOT L*=4!)

### **Figure 6: Ranking Reversal**
- Data: KEY_NUMBERS.md (mumiso_equal_step.py, mumiso_latency_parity.py)
- Shows: Side-by-side comparison
  - (a) Equal-Steps: Learned wins 5/5
  - (b) Equal-ms: Adam dominates 5/5
- Demonstrates Proposition 1

### **Figure 7: Jakes Correlation Decay**
- Data: Mathematical (ρ(τ) = J₀(2πfdτ))
- Shows: Correlation vs delay
- Marks: L=4, L=8, Tc, L=16, L=48
- Regions: Fresh (green) vs Stale (red)

---

## 🔧 NASIL ÇALIŞTIR

### **Yöntem 1: Lokal Bilgisayarınızda** (Önerilen)

```bash
cd paper_mobility/

# Gerekli paketleri yükle
pip install matplotlib scipy

# Figürleri üret
python3 generate_figures.py
```

**Çıktı**:
```
figures/fig3_fresh_vs_stale.pdf
figures/fig5_intrinsic_optimum_corrected.pdf
figures/fig6_ranking_reversal.pdf
figures/fig7_jakes_correlation.pdf
```

Her figür hem PDF (vector) hem PNG (raster) formatında üretilir.

---

### **Yöntem 2: Colab/Jupyter**

```python
!git clone https://github.com/sedasavascisen/sedasavascisen
%cd sedasavascisen/paper_mobility
!pip install matplotlib scipy
!python3 generate_figures.py
```

---

### **Yöntem 3: Docker/Container**

```bash
docker run -it --rm -v $(pwd):/work python:3.9 bash
cd /work/paper_mobility
pip install matplotlib scipy
python3 generate_figures.py
```

---

## ✅ ÜRETİLDİKTEN SONRA

### **1. Figürleri LaTeX'e Ekle**

`mobility_paper.tex` içinde:

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/fig3_fresh_vs_stale.pdf}
\caption{Fresh vs stale beam performance...}
\label{fig:fresh_vs_stale}
\end{figure}
```

### **2. Kontrol Et**

```bash
# PDF önizleme
pdflatex mobility_paper.tex
# Veya
xelatex mobility_paper.tex
```

### **3. Commit Et**

```bash
git add figures/*.pdf
git commit -m "Add generated figures (KEY_NUMBERS data, L*=8 corrected)"
git push
```

---

## 📊 DOĞRULAMA

Script çalıştığında şu mesajları göreceksiniz:

```
GENERATING FIGURES WITH CORRECT KEY_NUMBERS.md DATA
======================================================================

Generating Figure 3: Fresh vs Stale Beam...
✓ Saved: figures/fig3_fresh_vs_stale.pdf
  Data: Fresh 3.59-4.36 bps/Hz, Stale 0.306 bps/Hz, Ratio 11.7-14.2×

Generating Figure 5: Intrinsic Optimum (CORRECTED L*=8)...
✓ Saved: figures/fig5_intrinsic_optimum_corrected.pdf
  Data: L=8 peak (5.380 bps/Hz), L=48 stale (5.064 bps/Hz, -5.9%)
  CORRECTED: Shows L*≈8, NOT L*=4

Generating Figure 6: Equal-Millisecond Ranking Reversal...
✓ Saved: figures/fig6_ranking_reversal.pdf
  Data: 5/5 learned points dominated under equal-ms

Generating Figure 7: Jakes Correlation vs Delay...
✓ Saved: figures/fig7_jakes_correlation.pdf
  Data: ρ(τ) = J₀(2π·15·τ), Tc=28.2ms marks fresh/stale boundary

======================================================================
FIGURE GENERATION COMPLETE
======================================================================

CRITICAL CORRECTIONS:
  ✓ Figure 5 now shows L*≈8 as peak (NOT L*=4)
  ✓ All rates match Section VI tables (5.025-5.380 bps/Hz)
  ✓ Fresh beam ratio 11.7-14.2× (correct)

Ready for inclusion in paper!
```

---

## ⚠️ ÖNEMLİ NOTLAR

### **Figure 5 KRİTİK DÜZELTİLDİ**

- ❌ **ESKİ**: "Intrinsic Optimum L*=4"
- ✅ **YENİ**: "Intrinsic Optimum L*≈8"

Bu düzeltme Theorem 1 ile tutarlı!

### **Tüm Sayılar KEY_NUMBERS.md'den**

- Fresh beam: 3.59-4.36 bps/Hz (NOT 9.61)
- L=4: 5.025 bps/Hz
- L=8: 5.380 bps/Hz (PEAK)
- L=48: 5.064 bps/Hz (staleness)

Section VI tablolarıyla TAM UYUMLU!

### **IEEE Kalitesi**

- Vector PDF (scalable, no pixelation)
- Times New Roman font
- 300 DPI for raster versions
- Proper annotations and legends

---

## 🎯 ALTERNATİF: Yüklenen Figürleri Kullan

Eğer yeni figürler üretmek istemezsen:

**Kullanılabilir**:
- ✅ Figure 2 (Quantization vs Aging)
- ✅ Figure 4 (Ranking Reversal - qualitative)

**Kullanma**:
- ❌ Figure 1 (wrong scenario)
- ❌ Figure 3 (wrong absolute values)
- ❌ Figure 5 (contradicts L*≈8)

Ama **önerim**: Yeni figürleri üret (5 dakika sürer)

---

## 📞 YARDIM

Script çalışmazsa:

1. Python version: `python3 --version` (≥3.7 gerekli)
2. Matplotlib: `pip list | grep matplotlib`
3. Scipy: `pip list | grep scipy`

Sorun devam ederse:
```bash
pip install --upgrade matplotlib scipy
```

---

**Hazır mısın?** Script `generate_figures.py` dosyasında seni bekliyor! 🎨🚀
