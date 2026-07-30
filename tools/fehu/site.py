"""Read the live storefront as the single source of truth.

Every product page already carries a schema.org Product block, so the site —
not a hand-kept list — defines what exists, what it costs and where it sells.
The vault mirrors this; it never invents it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from . import config


@dataclass(frozen=True)
class Product:
    slug: str
    name: str
    description: str
    price: str
    gumroad_url: str
    page_url: str
    path: Path

    @property
    def utm_url(self) -> str:
        return f"{self.gumroad_url}?utm_source=site&utm_medium=product-page&utm_content={self.slug}"


class _LdJsonParser(HTMLParser):
    """Collect the contents of every application/ld+json script tag."""

    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[str] = []
        self._capturing = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._capturing = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._capturing = False

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self.blocks.append(data)


def _product_from_page(path: Path) -> Product | None:
    parser = _LdJsonParser()
    parser.feed(path.read_text(encoding="utf-8"))
    for block in parser.blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if data.get("@type") != "Product":
            continue
        offer = data.get("offers", {})
        slug = path.parent.name
        return Product(
            slug=slug,
            name=data.get("name", slug),
            description=data.get("description", ""),
            price=str(offer.get("price", "")),
            gumroad_url=offer.get("url", f"{config.GUMROAD_BASE}/{slug}"),
            page_url=f"{config.SITE_BASE}/{slug}/",
            path=path,
        )
    return None


def load_products(repo_root: Path | None = None) -> list[Product]:
    """Every product page in the repo, sorted by slug."""
    root = repo_root or config.REPO_ROOT
    found = []
    for page in sorted(root.glob("*/index.html")):
        if page.parent.name.startswith((".", "_")) or page.parent.name in {"tools", "vault"}:
            continue
        product = _product_from_page(page)
        if product:
            found.append(product)
    return found
