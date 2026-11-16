"""OZET.md + REPORT_S3_S1.md + REPORT_S4_S2.md + REPORT_S5.md -> JURI_RAPORU.pdf (python-markdown -> HTML -> Chromium,
thesis_exp/rapor_pdf/print_pdf.js). No numbers are computed here. Usage: python3 thesis_exp/juri/build_pdf.py"""
import pathlib, subprocess, re
import markdown
H = pathlib.Path(__file__).parent; T = H.parent
css = re.search(r"<style>(.*?)</style>", (T / "rapor_pdf" / "build.py").read_text(), re.S).group(1).replace("{{", "{").replace("}}", "}")
parts = []
for i, f in enumerate(["OZET.md", "REPORT_S3_S1.md", "REPORT_S4_S2.md", "REPORT_S5.md"]):
    src = (H / f).read_text().replace("L*", "L\\*").replace("r*", "r\\*")
    body = markdown.Markdown(extensions=["tables", "fenced_code"]).convert(src)
    parts.append(f'<section class="{"part" if i else ""}">{body}</section>')
doc = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Jüri soruları</title><style>{css}</style></head><body>{"".join(parts)}</body></html>'
(H / "JURI_RAPORU.html").write_text(doc)
subprocess.run(["node", str(T / "rapor_pdf" / "print_pdf.js"), str(H / "JURI_RAPORU.html"), str(H / "JURI_RAPORU.pdf")], check=True)
print("wrote", H / "JURI_RAPORU.pdf")
