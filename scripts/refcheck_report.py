"""
Builds the citation-check report (Turkish) for the mobility paper from the
reference-check results (one JSON per batch) and an optional double-check JSON.

  python3 scripts/refcheck_report.py <refcheck_dir> <out.html>

Inputs in <refcheck_dir>: citations.json (every citing sentence per reference),
results_batch_*.json (per-reference verification), optional doublecheck.json
(independent second pass: list of {key, agrees, note_tr, corrected_verdicts}).
Each citing sentence is shown with the source passage, the supporting words
highlighted in yellow, the location (page, section, paragraph) and a verdict.
"""
import sys
import json
import html
import glob
import pathlib

src = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
res = []
for f in sorted(src.glob("results_batch_*.json")):
    res += json.load(open(f))
res.sort(key=lambda r: r.get("n") or 999)
dc = {}
if (src / "doublecheck.json").exists():
    dc = {d["key"]: d for d in json.load(open(src / "doublecheck.json"))}
cits = {c["key"]: c for c in json.load(open(src / "citations.json"))}

COL = {"destekliyor": "#2E7D32", "kısmen": "#B26A00", "desteklemiyor": "#C62828", "erişilemedi": "#5F6B7A"}
counts = {}
for r in res:
    for it in r.get("items", []):
        v = it.get("verdict", "?")
        counts[v] = counts.get(v, 0) + 1


def esc(s):
    return html.escape(str(s or ""))


def marked(passage, hl):
    p = passage or ""
    if hl and hl in p:
        i = p.index(hl)
        return esc(p[:i]) + '<mark>' + esc(hl) + '</mark>' + esc(p[i + len(hl):])
    if hl:
        return esc(p) + '<br><mark>' + esc(hl) + '</mark>'
    return esc(p)


rows, cards = [], []
for r in res:
    vs = [it.get("verdict", "?") for it in r.get("items", [])]
    worst = next((v for v in ("desteklemiyor", "kısmen", "erişilemedi", "destekliyor") if v in vs), "?")
    d = dc.get(r["key"])
    dtxt = "" if d is None else ("✓ uyumlu" if d.get("agrees") else "✗ farklı")
    rows.append(f'<tr><td>[{r.get("n")}]</td><td>{esc(r["key"])}</td><td>{"✓" if r.get("metadata_ok") else "✗"}</td>'
                f'<td>{esc(r.get("source_version"))}</td><td style="color:{COL.get(worst, "#333")};font-weight:600">{esc(worst)}</td><td>{dtxt}</td></tr>')
    items = []
    for it in r.get("items", []):
        v = it.get("verdict", "?")
        items.append(f'''<div class="item">
<p class="lbl">Makaledeki atıf cümlesi <span class="sec">({esc(it.get("section"))})</span></p>
<blockquote class="ours">{esc(it.get("citing_sentence"))}</blockquote>
<p class="lbl">Orijinal metin — sayfa {esc(it.get("page"))}, {esc(it.get("location"))}</p>
<blockquote class="src">{marked(it.get("verbatim_passage"), it.get("highlight"))}</blockquote>
<p><span class="badge" style="background:{COL.get(v, "#333")}">{esc(v)}</span> {esc(it.get("note_tr"))}</p>
</div>''')
    meta = "" if r.get("metadata_ok") else "<ul class='warn'>" + "".join(f"<li>{esc(m)}</li>" for m in r.get("metadata_issues", [])) + "</ul>"
    dblk = ""
    if d is not None:
        dblk = f'<p class="dc"><b>İkinci kontrol:</b> {"uyumlu" if d.get("agrees") else "FARKLI"} — {esc(d.get("note_tr"))}</p>'
    bib = esc((cits.get(r["key"]) or {}).get("bib"))
    cards.append(f'''<section class="card" id="{esc(r["key"])}">
<h2>[{r.get("n")}] {esc(r["key"])}</h2>
<details><summary>BibTeX kaydı</summary><pre>{bib}</pre></details>
<p><b>Künye kontrolü:</b> {"doğru" if r.get("metadata_ok") else "sorun var"}{meta}</p>
<p><b>Kaynak:</b> {esc(r.get("source_version"))} — <a href="{esc(r.get("source_url"))}">{esc(r.get("source_url"))}</a></p>
<p><b>Neden atıf yaptık:</b> {esc(r.get("why_cited_tr"))}</p>
{"".join(items)}
{dblk}
</section>''')

summary = " · ".join(f'<span style="color:{COL.get(k, "#333")};font-weight:600">{esc(k)}: {v}</span>' for k, v in counts.items())
page = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kaynakça Kontrolü</title>
<style>
:root{{--bg:#F7F6F1;--fg:#1B2333;--muted:#5F6B7A;--card:#FFFFFF;--line:#DDD8CB;--ours:#EEF3FA}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#14181F;--fg:#E8E6E1;--muted:#A3ACB9;--card:#1C222B;--line:#2E3642;--ours:#1F2A3A}}}}
:root[data-theme="dark"]{{--bg:#14181F;--fg:#E8E6E1;--muted:#A3ACB9;--card:#1C222B;--line:#2E3642;--ours:#1F2A3A}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;margin:0;padding:24px 16px}}
main{{max-width:960px;margin:0 auto}}
h1{{font-size:28px}} h2{{font-size:20px;margin:0 0 8px}}
table{{border-collapse:collapse;width:100%;font:14px/1.4 system-ui,sans-serif;display:block;overflow-x:auto}}
td,th{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;margin:18px 0}}
blockquote{{margin:6px 0 10px;padding:10px 14px;border-left:4px solid var(--line)}}
.ours{{background:var(--ours)}} .src{{font-style:normal}}
mark{{background:#FFE45C;color:#1B2333;padding:0 2px}}
.lbl{{font:600 13px system-ui,sans-serif;color:var(--muted);margin:10px 0 0}} .sec{{font-weight:400}}
.badge{{color:#fff;border-radius:6px;padding:2px 8px;font:600 13px system-ui,sans-serif}}
.warn li{{color:#C62828}} .dc{{border-top:1px dashed var(--line);padding-top:8px}}
pre{{white-space:pre-wrap;font-size:12px}} .item{{border-top:1px solid var(--line);margin-top:10px}}
</style></head><body><main>
<h1>Kaynakça kontrolü — “Latency-Aware Phase Optimization for Reconfigurable Intelligent Surfaces Serving Mobile Users”</h1>
<p>{len(res)} kaynak, {sum(counts.values())} atıf cümlesi. {summary}</p>
<p style="color:var(--muted)">Her atıf için: makaledeki cümle, kaynağın ilgili paragrafı (destekleyen kısım <mark>sarı</mark>), sayfa ve paragraf yeri, karar. Ön baskı (arXiv) sürümlerinde sayfa numaraları dergi sürümünden farklı olabilir. “Erişilemedi”: tam metne yasal olarak ulaşılamadı; yalnızca künye ve özet kontrol edildi.</p>
<table><tr><th>No</th><th>Anahtar</th><th>Künye</th><th>Kaynak</th><th>En zayıf karar</th><th>İkinci kontrol</th></tr>{"".join(rows)}</table>
{"".join(cards)}
</main></body></html>'''
out.write_text(page)
print("wrote", out, counts)
