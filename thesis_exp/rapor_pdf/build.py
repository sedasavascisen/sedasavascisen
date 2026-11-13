"""
Builds the comprehensive report thesis_exp/rapor_pdf/TAM_RAPOR.pdf from the repository's own reports.
No numbers are written here: every section is an existing, committed Markdown report (some read from other
branches with `git show`), concatenated in a fixed order. Markdown -> HTML (python-markdown) -> PDF (Chromium
via Node Playwright, print_pdf.js).
Usage: python3 thesis_exp/rapor_pdf/build.py
"""
import subprocess, pathlib, datetime, html, re
import markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
H = pathlib.Path(__file__).parent
AUDIT_WT = pathlib.Path("/tmp/claude-0/-home-user-sedasavascisen/36a1538b-b28f-5b37-970a-9a1a9a74083b/scratchpad/wt_audit")


def git(*a, cwd=ROOT):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=cwd, check=True).stdout


def local(p):
    return (ROOT / p).read_text()


def branch(b, p):
    return git("show", f"origin/{b}:{p}")


commit = git("rev-parse", "--short", "HEAD").strip()
audit_commit = git("rev-parse", "--short", "origin/audit/makale1-denetim").strip()
P4 = [("Deney 4.1 — Kanal öngörüsü", "kanal_ongoru"), ("Deney 4.2 — Konum tabanlı faz", "konum_faz"),
      ("Deney 4.3 — Ön kodlayıcı pilotları", "onkodlayici_pilot"), ("Deney 4.3 devamı — Bütün kollarla sıralama", "onkodlayici_siralama"),
      ("Deney 4.4 — Kusurlu CSI", "kusurlu_csi"), ("Deney 4.5 — Ayrık faz (1/2/3 bit)", "ayrik_faz"),
      ("Deney 4.6 — Optimize süreler", "optimize_sure"), ("Doğrulama — Gecikme muhasebesi", "gecikme_muhasebesi")]

parts = [
    ("Bölüm A", "Sade özet", local("thesis_exp/rapor_pdf/00_sade_ozet.md")),
    ("Bölüm B", "Ayrıntılı teknik rapor", local("thesis_exp/AYRINTILI_RAPOR.md")),
    ("Bölüm C", "Bağımsız denetim süreci", local("thesis_exp/rapor_pdf/01_denetim_ozeti.md")),
    ("Bölüm D", "Tez için tavsiyeler", local("thesis_exp/TEZ_TAVSIYELERI.md")),
    ("Ek 1", "Görev 2 — Ortak altyapı raporu (dal thesis/altyapi)", branch("thesis/altyapi", "thesis_exp/infra/REPORT.md")),
    ("Ek 2", "Görev 3 — Köprü raporu (dal thesis/bridge)", branch("thesis/bridge", "thesis_exp/bridge/REPORT.md")),
] + [(f"Ek {i + 3}", t, local(f"thesis_exp/p4/{d}/REPORT.md")) for i, (t, d) in enumerate(P4)] + [
    (f"Ek {len(P4) + 3}", "Makale 1 denetim raporu — 13 Kasım'da donduruldu (dal audit/makale1-denetim)",
     branch("audit/makale1-denetim", "audit/AUDIT_REPORT.md")),
]

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
body, toc = [], []
for i, (tag, title, text) in enumerate(parts):
    md.reset()
    # demote headings by one level inside each part so the part title is the only h1
    text = re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", text, flags=re.M)
    sid = f"p{i}"
    toc.append(f'<li><a href="#{sid}"><span class="tag">{html.escape(tag)}</span> {html.escape(title)}</a></li>')
    body.append(f'<section class="part" id="{sid}"><div class="parthead"><span class="tag">{html.escape(tag)}</span>'
                f'<h1>{html.escape(title)}</h1></div>{md.convert(text)}</section>')

today = datetime.date.today().isoformat()
doc = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Tam rapor</title><style>
@page {{ size: A4; margin: 18mm 15mm 18mm 15mm; }}
:root {{ --ink:#1b1f24; --mute:#5b6470; --line:#d5dae0; --accent:#1f4e79; --soft:#f3f6f9; }}
body {{ font-family: 'DejaVu Sans', sans-serif; font-size: 9.2pt; line-height: 1.45; color: var(--ink); background:#fff; }}
h1 {{ font-size: 17pt; color: var(--accent); margin: 0 0 6pt; }}
h2 {{ font-size: 12.5pt; color: var(--accent); margin: 14pt 0 5pt; border-bottom: 1px solid var(--line); padding-bottom: 2pt; }}
h3 {{ font-size: 10.5pt; margin: 11pt 0 4pt; }} h4, h5, h6 {{ font-size: 9.6pt; margin: 9pt 0 3pt; }}
p, li {{ orphans: 3; widows: 3; }} ul, ol {{ padding-left: 16pt; margin: 3pt 0 6pt; }}
code {{ font-family: 'DejaVu Sans Mono', monospace; font-size: 8pt; background: var(--soft); padding: 0 2pt; border-radius: 2px; word-break: break-word; }}
pre {{ background: var(--soft); padding: 6pt; font-size: 7.6pt; white-space: pre-wrap; border-radius: 3px; }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 7.6pt; page-break-inside: auto; }}
tr {{ page-break-inside: avoid; }} th, td {{ border: 1px solid var(--line); padding: 2.5pt 4pt; vertical-align: top; text-align: left; word-break: normal; overflow-wrap: break-word; }}
td code {{ word-break: break-all; }}
.cover th {{ white-space: nowrap; }}
th {{ background: var(--soft); }}
blockquote {{ margin: 6pt 0; padding: 4pt 8pt; border-left: 3px solid #c0392b; background: #fbf1f0; }}
.part {{ page-break-before: always; }} .parthead {{ border-bottom: 2px solid var(--accent); margin-bottom: 8pt; }}
.tag {{ display:inline-block; font-size: 8pt; color:#fff; background: var(--accent); padding: 1pt 5pt; border-radius: 3px; margin-right: 4pt; }}
.cover {{ height: 240mm; display:flex; flex-direction:column; justify-content:center; }}
.cover h1 {{ font-size: 24pt; }} .cover .sub {{ font-size: 12pt; color: var(--mute); margin-bottom: 18pt; }}
.cover table {{ width: auto; font-size: 9pt; }} .toc li {{ margin: 2pt 0; list-style: none; }} .toc a {{ color: var(--ink); text-decoration: none; }}
</style></head><body>
<div class="cover"><h1>Tez deneyleri — kapsamlı teknik rapor</h1>
<div class="sub">Hareketli RIS sistemlerinde hesaplama gecikmesi · 11–13 Kasım 2026 çalışmaları</div>
<table><tr><th>Hazırlanma</th><td>{today}</td></tr>
<tr><th>Kaynak</th><td>dal <code>thesis/p4-deneyler</code> @ <code>{commit}</code>; ekler <code>thesis/altyapi</code>, <code>thesis/bridge</code>, <code>audit/makale1-denetim</code> @ <code>{audit_commit}</code></td></tr>
<tr><th>Üretim</th><td><code>python3 thesis_exp/rapor_pdf/build.py</code> — depodaki raporların birleşimi; bu belge yeni sayı içermez</td></tr>
<tr><th>Not</th><td>Tez ya da makale metni değildir (Kural 9). Makale 1 incelemesi 13 Kasım'da kullanıcı isteğiyle durduruldu.</td></tr></table>
<h2>İçindekiler</h2><ul class="toc">{''.join(toc)}</ul></div>
{''.join(body)}
</body></html>"""
(H / "TAM_RAPOR.html").write_text(doc)
subprocess.run(["node", str(H / "print_pdf.js"), str(H / "TAM_RAPOR.html"), str(H / "TAM_RAPOR.pdf")], check=True)
print("wrote", H / "TAM_RAPOR.pdf")
