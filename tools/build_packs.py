#!/usr/bin/env python3
"""Build the printable coloring pack PDFs.

The PDF this produces is the product. That is the point: previews rendered from
it are genuinely pages the buyer receives, so the listing claim holds.

    python3 tools/build_packs.py                      # all packs
    python3 tools/build_packs.py rune-coloring-pack   # one
    python3 tools/build_packs.py --out dist           # somewhere else

Output defaults to assets/packs/<slug>.pdf (gitignored — these are the goods).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.packlib.page import LETTER_H, LETTER_W, Page, new_canvas  # noqa: E402
from tools.packlib import packs  # noqa: E402

DEFAULT_OUT = Path("assets/packs")


def build_pack(module, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{module.SLUG}.pdf"
    canvas = new_canvas(str(target), module.TITLE)
    for index in range(module.PAGES):
        page = Page(canvas)
        module.draw(page, index)
        canvas.showPage()
    canvas.save()
    return target


def verify(path: Path, expected_pages: int) -> list[str]:
    """Check what the listings claim: page count, size, and page uniqueness."""
    from pypdf import PdfReader

    problems = []
    reader = PdfReader(str(path))
    if len(reader.pages) != expected_pages:
        problems.append(f"expected {expected_pages} pages, got {len(reader.pages)}")

    digests = set()
    for i, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        w, h = float(box.width), float(box.height)
        if abs(w - LETTER_W) > 0.5 or abs(h - LETTER_H) > 0.5:
            problems.append(f"page {i} is {w:.0f}x{h:.0f}, not Letter")
        digests.add(hashlib.sha256(page.get_contents().get_data()).hexdigest())

    if len(digests) != len(reader.pages):
        problems.append(
            f"only {len(digests)} unique page streams across "
            f"{len(reader.pages)} pages — some pages are duplicates"
        )
    problems.extend(_check_margins(path))
    return problems


def _check_margins(path: Path, tolerance: float = 2.0) -> list[str]:
    """Flag pages whose ink runs past the print-safe frame.

    Home printers clip the edges, so art that overflows here comes out cut off.
    Needs PyMuPDF; skipped silently when it is not installed.
    """
    try:
        import fitz  # type: ignore
    except ImportError:
        return []

    from tools.packlib.page import MARGIN

    problems = []
    document = fitz.open(str(path))
    for i, page in enumerate(document, start=1):
        drawings = page.get_drawings()
        if not drawings:
            continue
        x0 = min(d["rect"].x0 for d in drawings)
        y0 = min(d["rect"].y0 for d in drawings)
        x1 = max(d["rect"].x1 for d in drawings)
        y1 = max(d["rect"].y1 for d in drawings)
        over = max(MARGIN - x0, MARGIN - y0,
                   x1 - (LETTER_W - MARGIN), y1 - (LETTER_H - MARGIN))
        if over > tolerance:
            problems.append(f"page {i} overflows the print margin by {over:.0f}pt")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slugs", nargs="*", help="pack slugs (default: all)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--skip-verify", action="store_true")
    args = parser.parse_args()

    selected = args.slugs or list(packs.ALL)
    unknown = [s for s in selected if s not in packs.ALL]
    if unknown:
        print(f"Unknown pack(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Known: {', '.join(packs.ALL)}", file=sys.stderr)
        return 1

    failed = False
    for slug in selected:
        module = packs.ALL[slug]
        target = build_pack(module, args.out)
        size_kb = target.stat().st_size / 1024
        line = f"  {target}  {module.PAGES} pages  {size_kb:.0f} KB"

        if args.skip_verify:
            print(line)
            continue

        problems = verify(target, module.PAGES)
        if problems:
            failed = True
            print(f"{line}  FAILED")
            for problem in problems:
                print(f"      ! {problem}")
        else:
            print(f"{line}  verified")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
