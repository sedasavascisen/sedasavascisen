"""OZET.md + FINAL.md + FINAL_EK.md + GUNLUK.md -> SISTEM_RAPORU.pdf (same pipeline as thesis_exp/juri/build_pdf.py)."""
import pathlib, subprocess, re
import markdown
H = pathlib.Path(__file__).parent; T = H.parent
css = re.search(r"<style>(.*?)</style>", (T / "rapor_pdf" / "build.py").read_text(), re.S).group(1).replace("{{", "{").replace("}}", "}")
parts = []
for i, f in enumerate(["OZET.md", "FINAL.md", "FINAL_EK.md", "GUNLUK.md"]):
    src = re.sub(r"\b([Lr])\*(?!\*)", r"\1\\*", (H / f).read_text())
    src = re.sub(r"(?m)^ {2,3}(- )", r"    \1", src)
    src = re.sub(r"(?m)^((?![ \t]*(?:[-|#>]|\d+\.))\S.*)\n([ \t]*- )", r"\1\n\n\2", src)
    src = src.replace("|W", "&#124;W")
    parts.append(f'<section class="{"part" if i else ""}">{markdown.Markdown(extensions=["tables", "fenced_code"]).convert(src)}</section>')
(H / "SISTEM_RAPORU.html").write_text(f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>RIS denetleyicisi</title><style>{css}</style></head><body>{"".join(parts)}</body></html>')
subprocess.run(["node", str(T / "rapor_pdf" / "print_pdf.js"), str(H / "SISTEM_RAPORU.html"), str(H / "SISTEM_RAPORU.pdf")], check=True)
print("wrote")
