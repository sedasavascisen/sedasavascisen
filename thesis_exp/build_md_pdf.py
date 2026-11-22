"""Any thesis_exp markdown -> PDF (same pipeline as the other reports). Usage: python3 thesis_exp/build_md_pdf.py FILE.md [...]"""
import sys, pathlib, subprocess, re
import markdown
T = pathlib.Path(__file__).parent
css = re.search(r"<style>(.*?)</style>", (T / "rapor_pdf" / "build.py").read_text(), re.S).group(1).replace("{{", "{").replace("}}", "}")
for f in map(pathlib.Path, sys.argv[1:]):
    src = re.sub(r"\b([Lr])\*(?!\*)", r"\1\\*", f.read_text())
    src = re.sub(r"(?m)^ {2,3}(- )", r"    \1", src)
    src = re.sub(r"(?m)^((?![ \t]*(?:[-|#><]|\d+\.))\S.*)\n([ \t]*- )", r"\1\n\n\2", src)
    body = markdown.Markdown(extensions=["tables", "fenced_code"]).convert(src)
    h = f.with_suffix(".html")
    h.write_text(f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{f.stem}</title><style>{css}</style></head><body>{body}</body></html>')
    subprocess.run(["node", str(T / "rapor_pdf" / "print_pdf.js"), str(h), str(f.with_suffix(".pdf"))], check=True); h.unlink()
    print("wrote", f.with_suffix(".pdf"))
