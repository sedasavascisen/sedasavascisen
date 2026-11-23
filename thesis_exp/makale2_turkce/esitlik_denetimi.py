"""
Parity check of the Turkish working translation against the English paper. For every file pair (EN, TR) the multisets of
numbers, inline/display math, \\ref/\\eqref/\\cite/\\label keys, \\input and \\includegraphics must be identical.
Usage: python3 thesis_exp/makale2_turkce/esitlik_denetimi.py [file ...]   (default: all sections + 3 tables + main)
Exit code 1 on any mismatch.
"""
import re, sys, pathlib
from collections import Counter
H = pathlib.Path(__file__).parent; E = H.parent / "makale2_revizyon"
PAIRS = [(E / f"sections/{p.name}", p) for p in sorted((H / "sections").glob("*.tex"))]
PAIRS += [(E / f"tables/{n}.tex", H / f"tables/{n}.tex") for n in ("tab_aging", "tab_speeds", "tab_tracking")]
PAIRS += [(E / "mobility_paper_ieee.tex", H / "makale2_tr.tex")]
if len(sys.argv) > 1:
    PAIRS = [(a, b) for a, b in PAIRS if b.name in sys.argv[1:]]


def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def items(s, main=False):
    s = strip_comments(s)
    math = re.findall(r"\\begin\{equation\}.*?\\end\{equation\}|\$[^$]+\$", s, re.S)
    out = dict(math=Counter(m.strip() for m in math))
    txt = re.sub(r"\\begin\{equation\}.*?\\end\{equation\}|\$[^$]+\$", " ", s, flags=re.S)
    if main:                                       # preamble / author block / title differ by design
        txt = txt[txt.find("\\begin{abstract}"):]
        txt = re.sub(r"\\bibliography\{[^}]*\}", "", txt)
        txt = re.sub(r"\\url\{[^}]*\}", "", txt)
    out["numbers"] = Counter(re.findall(r"(?<![A-Za-z_\\])\d+(?:\.\d+)?", txt))
    for k in ("ref", "eqref", "cite", "label", "input", "includegraphics"):
        out[k] = Counter(re.findall(r"\\" + k + r"(?:\[[^\]]*\])?\{([^}]*)\}", txt))
    return out


bad = 0
for en, tr in PAIRS:
    if not tr.exists():
        print(f"EKSİK  {tr.relative_to(H)}"); bad += 1; continue
    a, b = items(en.read_text(), en.name.endswith("ieee.tex")), items(tr.read_text(), tr.name == "makale2_tr.tex")
    diffs = {k: (a[k] - b[k], b[k] - a[k]) for k in a if a[k] != b[k]}
    if diffs:
        bad += 1; print(f"FARK   {tr.relative_to(H)}")
        for k, (only_en, only_tr) in diffs.items():
            print(f"   {k}: yalnız EN {dict(only_en)} | yalnız TR {dict(only_tr)}")
    else:
        print(f"TAMAM  {tr.relative_to(H)}")
sys.exit(1 if bad else 0)
