#!/usr/bin/env python3
"""Mirror the live storefront into the vault as one note per product.

Run after any change to a product page. Regenerates the frontmatter block and
the generated section; anything you wrote under "## Notes" is preserved.

    python3 tools/sync_products.py
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fehu import config, site, vault  # noqa: E402

NOTES_HEADING = "## Notes"


def build_note(product: site.Product) -> vault.Note:
    path = config.PRODUCTS / f"{product.slug}.md"
    existing_notes = ""
    if path.exists():
        previous = vault.read(path)
        _, sep, tail = previous.body.partition(NOTES_HEADING)
        if sep:
            existing_notes = tail.strip()

    body = f"""# {product.name}

{product.description}

| | |
|---|---|
| Price | **${product.price}** |
| Checkout | {product.gumroad_url} |
| Page | {product.page_url} |
| Tracked link | `{product.utm_url}` |

Use the tracked link everywhere off-site — Pinterest, TikTok bio, newsletter.
Gumroad reports the `utm_content` value, which is how {vault.link('Weekly review')}
tells which page earned a sale.

## Content for this product

- Hooks: `vault/20-Content/Hooks/{product.slug}.md`
- Pins: `vault/20-Content/Pins/{product.slug}.md`

## Notes

{existing_notes or "_Your own observations go here — this section survives every sync._"}
"""

    return vault.Note(
        path=path,
        frontmatter={
            "type": "product",
            "slug": product.slug,
            "price_usd": product.price,
            "gumroad": product.gumroad_url,
            "page": product.page_url,
            "utm_content": product.slug,
            "status": "live",
            "synced": date.today().isoformat(),
            "tags": ["fehu/product"],
        },
        body=body,
    )


def main() -> int:
    products = site.load_products()
    if not products:
        print("No product pages found — is this being run from the repo root?")
        return 1

    config.PRODUCTS.mkdir(parents=True, exist_ok=True)
    for product in products:
        written = build_note(product).write()
        print(f"  {written.relative_to(config.REPO_ROOT)}  (${product.price})")

    print(f"\nSynced {len(products)} products into the vault.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
