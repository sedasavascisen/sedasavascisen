"""
One command that tells you whether the mobility paper is consistent.

    python3 scripts/check_paper.py            # all fast checks
    python3 scripts/check_paper.py --audit    # also run audit_claims.py --all
    python3 scripts/check_paper.py --assets PY  # also regenerate tables/numbers
                                              #   with interpreter PY (needs matplotlib)

Checks, each PASS/FAIL:
  build      pdflatex+bibtex in a temporary copy: no errors, no undefined
             references or citations, no overfull boxes, no ignored sections
  pages      at most 13 pages (IEEE TWC limit, references included)
  abstract   75-200 words (IEEE TWC)
  numbers    every decimal number in the text occurs in paper_numbers.txt or
             in a results/*.json the paper uses (or is in KNOWN below, each
             with its reason)
  cites      every \\cite key exists in the .bib and every .bib entry is cited
  labels     every \\ref / \\eqref has a \\label
  todo       lists the remaining \\todo{} placeholders (informational)
  assets     (optional) regenerating tables and paper_numbers.txt leaves them
             unchanged
  audit      (optional) audit_claims.py --all reports no failure
Exit status 1 if any check fails.
"""
import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper_mobility"
MAIN = "mobility_paper_ieee"

# Numbers that appear in the text but are inputs, definitions or arithmetic on
# sourced values, not measurements. Every entry needs a reason.
KNOWN = {
    "0.423": "coherence-time constant T_c = 0.423/f_d",
    "38.901": "3GPP TR 38.901", "38.211": "3GPP TS 38.211",
    "0.5": "half wavelength / step size", "0.25": "Adam step size tried",
    "0.75": "Adam step size", "1.0": "step size / speed / ratio grid",
    "1.5": "speed", "1.8": "speed", "3.0": "speed / multiplier",
    "0.05": "long-run Adam step size", "0.02": "step-size grid end",
    "2.0": "step-size grid end / ratio grid", "0.1": "grid", "1.66": "13.3/8 ms per step",
    "13.3": "Adam-8 latency used by mumiso_aging.py", "0.0": "zero delay",
    "2.5": "SU-best-of latency (2.54 ms) / x = 2.5e-2", "5.98": "5.980/5.982 rounded",
    "0.006": "5.2824 - 5.2762", "0.188": "6.3162 - 6.1280", "0.198": "Delta(6) - Delta(4)",
    "0.52": "6.357 - 5.833", "0.17": "CI half width", "0.24": "CI half width",
    "0.26": "spread 0.257", "0.12": "precoder 0.123 ms", "0.2": "L=4..6 within 0.2%",
    "17.48": "DEGISIKLIKLER_2026-10-23.md / mumiso_latency_parity.py docstring",
    "29.70": "results/mumiso_latency_parity.json (contaminated Adam L=8)",
    "0.025": "x at this setup", "0.075": "x at m=3", "6.0": "BS distance 5.98 m",
    "6.4": "Fraunhofer distance 6.40 m",
}
RESULT_KEYS = ("aging", "beam", "precoder", "mobility_latency", "latency_repeat",
               "latency_parity", "step_scaling", "tracking", "optimum_model",
               "equal_step", "scenario_geometry")


def tex_text():
    files = [PAPER / f"{MAIN}.tex"] + sorted(PAPER.glob("sections/*.tex"))
    return "".join(f.read_text() for f in files)


def check_build():
    with tempfile.TemporaryDirectory() as d:
        dst = pathlib.Path(d) / "p"
        shutil.copytree(PAPER, dst, ignore=shutil.ignore_patterns("*.aux", "*.log", "*.bbl", "*.blg", "*.out"))
        run = lambda *c: subprocess.run(c, cwd=dst, capture_output=True, text=True)
        run("pdflatex", "-interaction=nonstopmode", MAIN)
        run("bibtex", MAIN)
        for _ in range(3):
            run("pdflatex", "-interaction=nonstopmode", MAIN)
        log = (dst / f"{MAIN}.log").read_text(errors="ignore")
        bad = [l for l in log.splitlines()
               if l.startswith("!") or "undefined" in l.lower() or l.startswith("Overfull")
               or "useless" in l or "may have changed" in l]
        pages = None
        m = re.search(r"Output written on .*?\((\d+) pages", log)
        if m:
            pages = int(m.group(1))
        return bad, pages


def check_abstract():
    s = (PAPER / f"{MAIN}.tex").read_text()
    a = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", s, re.S).group(1)
    return len(re.sub(r"\$[^$]*\$", "X", a).split())


def check_numbers():
    src = (PAPER / "paper_numbers.txt").read_text()
    for f in glob.glob(str(ROOT / "results" / "mumiso_*.json")) + glob.glob(str(ROOT / "results" / "sumiso_*.json")):
        if "sumiso_" in f or any(k in f for k in RESULT_KEYS):
            src += " " + " ".join(re.findall(r"-?\d+\.\d+(?:e-?\d+)?", open(f).read()))
    nums = set()
    for x in re.findall(r"-?\d+\.\d+(?:e-?\d+)?", src):
        v = abs(float(x))
        for dgt in (1, 2, 3, 4):
            nums.add(f"{v:.{dgt}f}")
        for dgt in (1, 2):
            nums.add(f"{100 * v:.{dgt}f}")
        nums.add(f"{v / 1000:.1f}")
        nums.add(f"{v / 1000:.2f}")
    tex = tex_text()
    miss = []
    for m in re.finditer(r"(\d+\.\d+)", tex):
        x = m.group(1)
        if x not in nums and x not in KNOWN:
            miss.append((x, tex[max(0, m.start() - 60):m.end() + 10].replace("\n", " ")))
    return miss


def check_cites():
    tex = tex_text()
    cited = {k.strip() for g in re.findall(r"\\cite\{([^}]*)\}", tex) for k in g.split(",")}
    bib = set(re.findall(r"@\w+\{([^,]+),", (PAPER / "references" / "references.bib").read_text()))
    return cited - bib, bib - cited


def check_labels():
    tex = tex_text()
    refs = set(re.findall(r"\\(?:eq)?ref\{([^}]*)\}", tex))
    labels = set(re.findall(r"\\label\{([^}]*)\}", tex))
    return refs - labels


def check_assets(py):
    before = {p: p.read_bytes() for p in list(PAPER.glob("tables/*.tex")) + [PAPER / "paper_numbers.txt"]}
    r = subprocess.run([py, str(PAPER / "make_paper_assets.py")], capture_output=True, text=True)
    if r.returncode:
        return [f"make_paper_assets.py failed: {r.stderr[-300:]}"]
    changed = [str(p.relative_to(ROOT)) for p, b in before.items() if p.read_bytes() != b]
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--assets", metavar="PYTHON")
    a = ap.parse_args()
    fails = 0

    def report(name, ok, detail=""):
        nonlocal fails
        fails += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name:9s} {detail}")

    bad, pages = check_build()
    report("build", not bad and pages is not None, f"{len(bad)} problem lines" + ("".join(f"\n            {b}" for b in bad[:8])))
    report("pages", pages is not None and pages <= 13, f"{pages} pages (limit 13; >10 incurs page charges)")
    w = check_abstract()
    report("abstract", 75 <= w <= 200, f"{w} words (75-200)")
    miss = check_numbers()
    report("numbers", not miss, f"{len(miss)} unsourced" + "".join(f"\n            {x} | {c}" for x, c in miss[:12]))
    nb, nc = check_cites()
    report("cites", not nb and not nc, f"missing in bib: {sorted(nb)}; never cited: {sorted(nc)}")
    nl = check_labels()
    report("labels", not nl, f"refs without label: {sorted(nl)}")
    todos = re.findall(r"\\todo\{([^}]*)\}", tex_text())
    print(f"[INFO] todo      {len(todos)} placeholders: " + "; ".join(t[:40] for t in todos))
    if a.assets:
        ch = check_assets(a.assets)
        report("assets", not ch, "unchanged" if not ch else f"changed: {ch}")
    if a.audit:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "audit_claims.py"), "--all"],
                           capture_output=True, text=True, cwd=ROOT)
        last = [l for l in r.stdout.splitlines() if "asserted claims" in l]
        ok = bool(last) and "hold" in last[-1] and r.returncode == 0
        m = re.search(r"(\d+)/(\d+)", last[-1]) if last else None
        ok = ok and m and m.group(1) == m.group(2)
        report("audit", bool(ok), last[-1].strip() if last else r.stdout[-200:])
    print(f"\n{'ALL CHECKS PASS' if not fails else f'{fails} CHECK(S) FAILED'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
