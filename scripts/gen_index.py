#!/usr/bin/env python3
"""Posbírá sestavená PDF a vygeneruje rozcestník index.html pro GitHub Pages.

Použití: python3 scripts/gen_index.py --site _site
Očekává, že předtím proběhl ./build.sh all (PDF v <okruh>/out/ a <okruh>/priklady/out/).
"""
import argparse
import datetime as dt
import html
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GROUPS = [
    ("01_spolecna_matematika", "Společná část: matematika"),
    ("02_spolecna_informatika", "Společná část: informatika"),
    ("03_specializace_ui_su", "Specializace Umělá inteligence, zaměření Strojové učení"),
]

def title_of(okruh_dir: Path) -> tuple[str, str]:
    """Vrátí (kód, název) z makra \\szztitul{Název}{Kód}{...} ve výkladu."""
    tex = (okruh_dir / "src" / "main.tex").read_text(encoding="utf-8")
    m = re.search(r"\\szztitul\{([^}]*)\}\{([^}]*)\}", tex)
    if m:
        return m.group(2), m.group(1)
    code, _, rest = okruh_dir.name.partition("_")
    return code, rest.replace("_", " ")


def pages(pdf: Path) -> int | None:
    """Počet stran z logu LaTeXu (<okruh>/tmp/<jméno>.log), pdfinfo v CI kontejneru být nemusí."""
    log = pdf.parent.parent / "tmp" / f"{pdf.stem}.log"
    try:
        m = re.search(r"Output written on .*?\((\d+) pages?", log.read_text(encoding="utf-8", errors="replace"), re.S)
        return int(m.group(1)) if m else None
    except OSError:
        return None


def label(pdf: Path) -> str:
    n = pages(pdf)
    return f"{n} s." if n else f"{pdf.stat().st_size / 1e6:.1f} MB"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="_site")
    site = Path(ap.parse_args().site)
    (site / "pdf").mkdir(parents=True, exist_ok=True)

    sections = []
    for group, heading in GROUPS:
        cards = []
        for okruh in sorted(p for p in (ROOT / group).iterdir() if (p / "src" / "main.tex").is_file()):
            code, name = title_of(okruh)
            links = []
            docs = [(okruh / "out" / "main.pdf", f"{code}.pdf", "Výklad")]
            docs.append((okruh / "priklady" / "out" / "main.pdf", f"{code}-priklady.pdf", "Příklady otázek"))
            for src, dst, lab in docs:
                if not src.is_file():
                    continue
                shutil.copy2(src, site / "pdf" / dst)
                extra = label(src)
                if lab == "Příklady otázek":
                    nq = len(list((okruh / "priklady" / "src").glob("q_*.tex")))
                    extra = f"{nq} otázek, {extra}"
                cls = "primary" if lab == "Výklad" else "secondary"
                links.append(
                    f'<a class="{cls}" href="pdf/{dst}">{html.escape(lab)}<span class="meta">{html.escape(extra)}</span></a>'
                )
            cards.append(
                f'<li class="card"><div class="code">{html.escape(code)}</div>'
                f'<div class="name">{html.escape(name)}</div><div class="links">{"".join(links)}</div></li>'
            )
        sections.append(f"<section><h2>{html.escape(heading)}</h2><ul>{''.join(cards)}</ul></section>")

    sha = os.environ.get("GITHUB_SHA", "")[:7]
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    built = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    source = f' · <a href="https://github.com/{repo}">zdrojové texty na GitHubu</a>' if repo else ""
    commit = f" z commitu <code>{sha}</code>" if sha else ""

    tmpl = (ROOT / "scripts" / "templates" / "index.html").read_text(encoding="utf-8")
    page = (tmpl.replace("{{SECTIONS}}", "\n".join(sections))
                .replace("{{BUILT}}", f"Sestaveno {built}{commit}{source}"))
    (site / "index.html").write_text(page, encoding="utf-8")
    print(f"index: {site / 'index.html'} ({len(list((site / 'pdf').glob('*.pdf')))} PDF)")


if __name__ == "__main__":
    main()
