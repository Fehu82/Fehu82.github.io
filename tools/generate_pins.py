#!/usr/bin/env python3
"""Generate Pinterest and TikTok copy per product.

Printable coloring books sell on Pinterest — it is a search engine for exactly
this buyer, it indexes pin descriptions, and it costs nothing. This writes the
copy; you make the pin image from real product pages and post it.

    python3 tools/generate_pins.py
    python3 tools/generate_pins.py cat-coloring-pack --count 6
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fehu import config, llm, site, vault  # noqa: E402

SYSTEM = """You write Pinterest and TikTok copy for Fehu Lab, a small shop
selling printable coloring-book PDFs.

House rules, non-negotiable:
- Never invent a feature, page count or bonus that is not in the description
  you are given.
- No fake scarcity, no invented reviews, no income or "get rich" claims.
- Keywords must read as natural sentences, not a keyword dump.
- The products are AI-assisted and disclosed as such. Never imply hand-drawn.

Return a JSON array and nothing else. Each element:
{"pin_title": str, "pin_description": str, "tiktok_caption": str, "keywords": [str]}
- pin_title: under 100 characters, leads with what a searcher types.
- pin_description: 2 to 3 sentences, under 480 characters, naturally seeded
  with the search terms.
- tiktok_caption: under 150 characters, spoken-voice, no hashtag wall.
- keywords: 5 to 8 lowercase search phrases a buyer would really use."""


def prompt_for(product: site.Product, count: int) -> str:
    return f"""Product name: {product.name}
Price: ${product.price}
Description as published: {product.description}

Write {count} distinct pin/caption sets. Aim each at a different searcher:
someone buying a gift, a teacher, a parent, an adult buying for their own
wind-down, a hobbyist in the theme. Do not repeat a search intent."""


def render(product: site.Product, sets: list[dict], model: str) -> vault.Note:
    blocks = []
    for index, item in enumerate(sets, start=1):
        keywords = item.get("keywords", [])
        keyword_line = ", ".join(str(k) for k in keywords) if keywords else "—"
        blocks.append(
            f"### P{index:02d}\n\n"
            f"**Pin title** {str(item.get('pin_title', '')).strip()}\n\n"
            f"**Pin description**\n\n> {str(item.get('pin_description', '')).strip()}\n\n"
            f"**TikTok caption** {str(item.get('tiktok_caption', '')).strip()}\n\n"
            f"**Keywords** `{keyword_line}`\n\n"
            f"- [ ] posted   ·   date: ______   ·   saves/views: ______\n"
        )

    body = f"""# Pins — {product.name}

Generated {date.today().isoformat()} by `{model}`. Copy only — the pin image must
come from real pages of the actual PDF, never from generated art that is not in
the product.

Product note: {vault.link(product.slug)}

**Paste this as the pin destination link:**

```
{product.utm_url.replace('utm_medium=product-page', 'utm_medium=pinterest')}
```

{chr(10).join(blocks)}
"""
    return vault.Note(
        path=config.PINS / f"{product.slug}.md",
        frontmatter={
            "type": "pins",
            "product": product.slug,
            "generated": date.today().isoformat(),
            "model": model,
            "status": "unposted",
            "tags": ["fehu/content"],
        },
        body=body,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="product slugs (default: all)")
    parser.add_argument("--count", type=int, default=5, help="sets per product")
    args = parser.parse_args()

    products = site.load_products()
    if args.slugs:
        wanted = set(args.slugs)
        products = [p for p in products if p.slug in wanted]
        missing = wanted - {p.slug for p in products}
        if missing:
            print(f"Unknown slug(s): {', '.join(sorted(missing))}")
            return 1

    config.PINS.mkdir(parents=True, exist_ok=True)
    for product in products:
        print(f"  {product.slug} ...", end=" ", flush=True)
        reply = llm.chat(SYSTEM, prompt_for(product, args.count))
        sets = llm.extract_json_array(reply.text)
        written = render(product, sets, reply.model).write()
        print(f"{len(sets)} sets -> {written.relative_to(config.REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (llm.LLMError, config.ConfigError) as error:
        print(f"\n{error}", file=sys.stderr)
        raise SystemExit(2) from error
