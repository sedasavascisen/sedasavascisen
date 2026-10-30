#!/usr/bin/env python3
"""Tek bir dosyada butun kaynak kodun son hali.

Neden bu betik var: kullanici kodlari Claude Code'a gecirirken "butun
kodlarin son hali" diye okunabilir tek bir dosya istedi. Elle kopyalamak
yerine uretiyoruz, boylece dosya her zaman diskteki gercek halle ayni
kalir -- bu projede elle yazilmis her sayinin yanlis cikmasi gibi, elle
kopyalanmis her kaynak da eskir.

Kullanim:
    python3 scripts/dump_source.py              # KOD_SON_HALI.md
    python3 scripts/dump_source.py --core-only  # sadece ris_mu/mumiso
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Sira anlatim sirasi: once sistem denklemleri (tek dogruluk kaynagi),
# sonra uzerine kurulan her sey.
CORE_ORDER = [
    "ris_mu/mumiso/__init__.py",
    "ris_mu/mumiso/system.py",
    "ris_mu/mumiso/channel.py",
    "ris_mu/mumiso/mobile.py",
    "ris_mu/mumiso/csi.py",
    "ris_mu/mumiso/features.py",
    "ris_mu/mumiso/models.py",
    "ris_mu/mumiso/unrolled.py",
    "ris_mu/mumiso/baselines.py",
    "ris_mu/mumiso/train.py",
]

LEGACY_ORDER = [
    "ris_mu/__init__.py",
    "ris_mu/geometry.py",
    "ris_mu/pathloss.py",
    "ris_mu/channel.py",
    "ris_mu/features.py",
    "ris_mu/models.py",
    "ris_mu/losses.py",
    "ris_mu/baselines.py",
    "ris_mu/train.py",
]

# Betikler rol rol gruplanir; alfabetik liste ne ise yaradigini gostermiyor.
SCRIPT_GROUPS = [
    ("Denetim ve dogrulama (her oturumda kosturulacaklar)", [
        "audit_claims.py",
        "audit_fair_comparison.py",
        "audit_precoder_csi.py",
        "audit_section4_cause.py",
        "verify_mumiso_system.py",
        "verify_mumiso_channel.py",
        "verify_mumiso_models.py",
        "verify_mobile.py",
        "verify_residual.py",
        "verify_batch_dependence.py",
        "verify_baseline_strength.py",
        "verify_crossover.py",
        "verify_head_claim.py",
        "verify_matlab_architecture.py",
    ]),
    ("Bolum 4 -- cok kullanicili ogrenme (titiz olumsuz sonuc)", [
        "mumiso_run.py",
        "mumiso_unrolled.py",
        "mumiso_equal_step.py",
        "mumiso_latency_parity.py",
        "mumiso_latency_repeat.py",
        "mumiso_step_cost.py",
        "mumiso_budget.py",
        "mumiso_budget_fraction.py",
        "mumiso_headroom.py",
        "anchor_same_split.py",
        "diagnose_learnability.py",
        "diagnose_mumiso_gap.py",
        "step1_control.py",
        "step1b_head_ablation.py",
        "step4_multiuser.py",
        "step4b_residual.py",
        "step4c_equiv_long.py",
        "step5_generalisation.py",
        "step5b_mixed_users.py",
    ]),
    ("Bolum 5 -- hareketlilik (tezin omurgasi)", [
        "mumiso_aging.py",
        "mumiso_frontier.py",
        "mumiso_beam_staleness.py",
    ]),
    ("Bolum 6 -- gercekci senaryo ve donanim", [
        "mumiso_antenna_corr.py",
        "mumiso_gain_sharing.py",
        "mumiso_gain_source.py",
        "mumiso_precoder_cost.py",
        "mumiso_csi_room.py",
        "mumiso_quant_latency.py",
        "step3_csi_transfer.py",
        "step6_quantised_phase.py",
        "diagnose_realism.py",
    ]),
    ("Raporlama", [
        "compile_results.py",
        "make_writing_reference.py",
        "dump_source.py",
    ]),
]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _emit(out: list[str], rel: str) -> tuple[int, str]:
    path = ROOT / rel
    src = path.read_text(encoding="utf-8")
    nlines = len(src.splitlines())
    digest = _sha(src)
    out.append(f"### `{rel}`\n")
    out.append(f"*{nlines} satir · sha256:{digest}*\n")
    out.append("```python")
    out.append(src.rstrip("\n"))
    out.append("```\n")
    return nlines, digest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core-only", action="store_true",
                    help="sadece ris_mu/mumiso paketini yaz")
    ap.add_argument("--out", default="KOD_SON_HALI.md")
    args = ap.parse_args()

    today = _dt.date.today().isoformat()
    out: list[str] = []
    index: list[tuple[str, int, str]] = []

    out.append("# Kodun son hali\n")
    out.append(
        f"Bu dosya `scripts/dump_source.py` tarafindan **{today}** tarihinde "
        "diskteki kaynaktan uretildi. Elle duzenlenmez; kaynak degisince "
        "betigi yeniden kosturun.\n"
    )
    out.append(
        "Her dosyanin basliginda satir sayisi ve icerigin sha256 ozeti var. "
        "Claude Code'da bir dosyayi acip bu ozetle karsilastirabilirsiniz: "
        "ayni ise dosya bu listedekiyle birebir aynidir.\n"
    )
    out.append("> **Yayimlanmis MATLAB kodu bu pakette yok ve bu paketten "
               "etkilenmez.** `duzeltilmis_kodlar` ayri durur ve yayimlanan "
               "sonuclari uretmeye devam eder.\n")
    out.append("---\n")
    out.append("<!--INDEX-->\n")

    out.append("## 1. Cekirdek paket: `ris_mu/mumiso/`\n")
    out.append(
        "Tezin butun sayilari bu on dosyadan cikiyor. `system.py` tek "
        "dogruluk kaynagidir: SINR, oran ve on kodlayici sadece orada "
        "tanimli, digerleri onu cagirir.\n"
    )
    for rel in CORE_ORDER:
        n, d = _emit(out, rel)
        index.append((rel, n, d))

    if not args.core_only:
        out.append("## 2. Onceki tek kullanicili paket: `ris_mu/`\n")
        out.append(
            "Yayimlanmis makalenin Python karsiligi ve tek-RIS deneyleri. "
            "Cok kullanicili is bunun **uzerine** kuruldu, bunu "
            "degistirmedi. Kiyas icin burada.\n"
        )
        for rel in LEGACY_ORDER:
            n, d = _emit(out, rel)
            index.append((rel, n, d))

        out.append("## 3. Betikler: `scripts/`\n")
        out.append(
            "47 betik. Alfabetik degil, **tezdeki roluyle** gruplandi. "
            "Bir sayiyi teze koymadan once onu ureten betigi burada bulup "
            "kosturun.\n"
        )
        seen = set()
        for title, names in SCRIPT_GROUPS:
            out.append(f"### {title}\n")
            for name in names:
                rel = f"scripts/{name}"
                if not (ROOT / rel).exists():
                    out.append(f"*(yok: `{rel}`)*\n")
                    continue
                seen.add(name)
                n, d = _emit(out, rel)
                index.append((rel, n, d))
        leftover = sorted(
            p.name for p in (ROOT / "scripts").glob("*.py") if p.name not in seen
        )
        if leftover:
            out.append("### Gruplanmamis\n")
            for name in leftover:
                n, d = _emit(out, f"scripts/{name}")
                index.append((f"scripts/{name}", n, d))

    total = sum(n for _, n, _ in index)
    toc = ["## Icindekiler\n",
           f"**{len(index)} dosya · {total} satir**\n",
           "| Dosya | Satir | sha256 |", "|---|---:|---|"]
    toc += [f"| `{rel}` | {n} | `{d}` |" for rel, n, d in index]
    toc.append("")
    body = "\n".join(out).replace("<!--INDEX-->", "\n".join(toc))

    dest = ROOT / args.out
    dest.write_text(body + "\n", encoding="utf-8")
    print(f"{dest}  ({len(index)} dosya, {total} satir, "
          f"{dest.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
