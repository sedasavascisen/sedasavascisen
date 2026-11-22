"""RAPOR.md -> RAPOR.pdf (same pipeline as makale2_revizyon/kaynak_kontrol/build_pdf.py)."""
import pathlib, subprocess, re
import markdown
H = pathlib.Path(__file__).parent; T = H.parent
css = re.search(r"<style>(.*?)</style>", (T / "rapor_pdf" / "build.py").read_text(), re.S).group(1).replace("{{", "{").replace("}}", "}")
src = re.sub(r"\b([Lr])\*(?!\*)", r"\1\\*", (H / "RAPOR.md").read_text())
src = re.sub(r"(?m)^ {2,3}(- )", r"    \1", src)
src = re.sub(r"(?m)^((?![ \t]*(?:[-|#><]|\d+\.))\S.*)\n([ \t]*- )", r"\1\n\n\2", src)
body = markdown.Markdown(extensions=["tables", "fenced_code"]).convert(src)
(H / "RAPOR.html").write_text(f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Madde 8–14 ve 19</title><style>{css}</style></head><body>{body}</body></html>')
subprocess.run(["node", str(T / "rapor_pdf" / "print_pdf.js"), str(H / "RAPOR.html"), str(H / "RAPOR.pdf")], check=True)
print("wrote")
