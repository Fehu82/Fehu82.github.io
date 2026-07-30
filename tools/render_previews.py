#!/usr/bin/env python3
"""Render preview PNGs from the real product PDFs, and wire them into a page.

The storefront currently shows empty preview boxes because no image has ever
existed in this repo. The fix is to publish real pages from the actual PDF a
buyer receives — not generated stand-ins that look like the product but are not
in it. This script therefore refuses to run without a source PDF.

    # put the real file here first (assets/source-pdfs/ is gitignored)
    python3 tools/render_previews.py rune-coloring-pack \\
        assets/source-pdfs/rune.pdf --pages 1 4 7 16 22 30

Requires pdftoppm (poppler-utils) or PyMuPDF:
    apt-get install poppler-utils      # or:  pip install pymupdf
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fehu import config  # noqa: E402

DEFAULT_PAGES = [1, 4, 7, 16, 22, 30]


def render_with_poppler(pdf: Path, pages: list[int], out_dir: Path, dpi: int) -> list[Path]:
    written = []
    for page in pages:
        stem = out_dir / f"page-{page:02d}"
        subprocess.run(
            [
                "pdftoppm", "-png", "-r", str(dpi),
                "-f", str(page), "-l", str(page),
                "-singlefile", str(pdf), str(stem),
            ],
            check=True,
            capture_output=True,
        )
        written.append(stem.with_suffix(".png"))
    return written


def render_with_pymupdf(pdf: Path, pages: list[int], out_dir: Path, dpi: int) -> list[Path]:
    import fitz  # type: ignore

    document = fitz.open(pdf)
    written = []
    for page in pages:
        if page > document.page_count:
            raise SystemExit(f"PDF has {document.page_count} pages; {page} requested")
        pixmap = document[page - 1].get_pixmap(dpi=dpi)
        target = out_dir / f"page-{page:02d}.png"
        pixmap.save(target)
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="product slug, e.g. rune-coloring-pack")
    parser.add_argument("pdf", type=Path, help="path to the real product PDF")
    parser.add_argument("--pages", type=int, nargs="+", default=DEFAULT_PAGES)
    parser.add_argument("--dpi", type=int, default=110)
    args = parser.parse_args()

    if not args.pdf.exists():
        print(
            f"No such PDF: {args.pdf}\n\n"
            "This script will not invent preview art. Previews must be real pages\n"
            "from the file the buyer downloads, or the listing misrepresents the\n"
            "product. Put the actual PDF somewhere and pass its path.",
            file=sys.stderr,
        )
        return 2

    product_dir = config.REPO_ROOT / args.slug
    if not (product_dir / "index.html").exists():
        print(f"No product page at {args.slug}/index.html", file=sys.stderr)
        return 2

    out_dir = product_dir / "previews"
    out_dir.mkdir(parents=True, exist_ok=True)

    if shutil.which("pdftoppm"):
        written = render_with_poppler(args.pdf, args.pages, out_dir, args.dpi)
    else:
        try:
            written = render_with_pymupdf(args.pdf, args.pages, out_dir, args.dpi)
        except ImportError:
            print(
                "Need either poppler-utils (apt-get install poppler-utils)\n"
                "or PyMuPDF (pip install pymupdf) to rasterise the PDF.",
                file=sys.stderr,
            )
            return 2

    print(f"Rendered {len(written)} previews into {out_dir.relative_to(config.REPO_ROOT)}/\n")
    print("Now replace the <div class=\"gallery\"> contents in "
          f"{args.slug}/index.html with:\n")
    for path in written:
        page_number = path.stem.split("-")[1]
        print(
            f'<figure><img src="previews/{path.name}" loading="lazy" width="850" '
            f'height="1100" alt="Page {int(page_number)} of {args.slug}, '
            f'black line art on white, unretouched">'
            f"<figcaption>page {int(page_number)}</figcaption></figure>"
        )
    print("\nThen drop the previews/ line from .gitignore's assets rule if needed "
          "and commit the PNGs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
