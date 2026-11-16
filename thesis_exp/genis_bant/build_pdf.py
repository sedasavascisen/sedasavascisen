"""REPORT.md -> REPORT.pdf (python-markdown -> HTML -> Chromium via thesis_exp/rapor_pdf/print_pdf.js).
No numbers are computed here. Usage: python3 thesis_exp/genis_bant/build_pdf.py"""
import pathlib, subprocess, re
import markdown
H = pathlib.Path(__file__).parent
PRINT = H.parents[0] / "rapor_pdf" / "print_pdf.js"
src = (H / "REPORT.md").read_text().replace("L*", "L\\*")      # L* is notation, not emphasis
body = markdown.Markdown(extensions=["tables", "fenced_code"]).convert(src)
css = re.search(r"<style>(.*?)</style>", (H.parents[0] / "rapor_pdf" / "build.py").read_text(), re.S).group(1)
css = css.replace("{{", "{").replace("}}", "}")
doc = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Geniş bant OFDM</title><style>{css}</style></head><body>{body}</body></html>'
(H / "REPORT.html").write_text(doc)
subprocess.run(["node", str(PRINT), str(H / "REPORT.html"), str(H / "REPORT.pdf")], check=True)
print("wrote", H / "REPORT.pdf")
