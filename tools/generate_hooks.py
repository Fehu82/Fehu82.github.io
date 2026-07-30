#!/usr/bin/env python3
"""Generate listing-copy variants with Kimi, for testing against real sales.

This is the honest half of the "340 variations" idea: produce many candidate
titles and hooks, ship them organically, and let Gumroad's UTM report say which
one earned money. No ad spend, no autonomous purchasing.

    python3 tools/generate_hooks.py                    # all products
    python3 tools/generate_hooks.py rune-coloring-pack # one
    python3 tools/generate_hooks.py --count 12
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fehu import config, llm, site, vault  # noqa: E402

SYSTEM = """You write listing copy for Fehu Lab, a small shop selling printable
coloring-book PDFs and research playbooks.

House rules, non-negotiable:
- Never invent a feature, page count, bonus or file format that is not in the
  product description you are given.
- No fake scarcity, no countdown language, no "only 3 left", no invented
  testimonials or sales figures.
- No income claims and no "get rich" framing of any kind.
- Plain, concrete, specific. Say what the buyer actually receives.
- These products are AI-assisted and disclosed as such. Never imply otherwise.

Return a JSON array and nothing else. Each element:
{"title": str, "hook": str, "angle": str}
- title: under 140 characters, marketplace-style, front-loaded with the search
  terms a buyer would actually type.
- hook: one sentence, under 200 characters, for the top of a social post.
- angle: two or three words naming the buying motive you aimed at
  (e.g. "gift for grandparent", "classroom filler", "wind-down ritual")."""


def prompt_for(product: site.Product, count: int) -> str:
    return f"""Product name: {product.name}
Price: ${product.price}
Description as published: {product.description}

Write {count} distinct variants. Vary the buying motive, not just the wording —
two variants with the same angle are wasted. Cover at least four different
angles across the set."""


def render(product: site.Product, variants: list[dict], model: str) -> vault.Note:
    rows = []
    for index, variant in enumerate(variants, start=1):
        title = str(variant.get("title", "")).strip()
        hook = str(variant.get("hook", "")).strip()
        angle = str(variant.get("angle", "")).strip()
        rows.append(
            f"### V{index:02d} — {angle or 'unspecified angle'}\n\n"
            f"**Title** {title}\n\n"
            f"**Hook** {hook}\n\n"
            f"- [ ] shipped   ·   channel: ______   ·   date: ______   ·   sales: ______\n"
        )

    body = f"""# Hooks — {product.name}

Generated {date.today().isoformat()} by `{model}`. Candidates only: nothing here
has been tested. Tick a box when you ship one, then record what it earned during
{vault.link('Weekly review')}.

Product note: {vault.link(product.slug)}
Tracked link: `{product.utm_url}`

{chr(10).join(rows)}
"""
    return vault.Note(
        path=config.HOOKS / f"{product.slug}.md",
        frontmatter={
            "type": "hooks",
            "product": product.slug,
            "generated": date.today().isoformat(),
            "model": model,
            "status": "untested",
            "tags": ["fehu/content"],
        },
        body=body,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="product slugs (default: all)")
    parser.add_argument("--count", type=int, default=8, help="variants per product")
    args = parser.parse_args()

    products = site.load_products()
    if args.slugs:
        wanted = set(args.slugs)
        products = [p for p in products if p.slug in wanted]
        missing = wanted - {p.slug for p in products}
        if missing:
            print(f"Unknown slug(s): {', '.join(sorted(missing))}")
            return 1

    config.HOOKS.mkdir(parents=True, exist_ok=True)
    for product in products:
        print(f"  {product.slug} ...", end=" ", flush=True)
        reply = llm.chat(SYSTEM, prompt_for(product, args.count))
        variants = llm.extract_json_array(reply.text)
        written = render(product, variants, reply.model).write()
        print(f"{len(variants)} variants -> {written.relative_to(config.REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (llm.LLMError, config.ConfigError) as error:
        print(f"\n{error}", file=sys.stderr)
        raise SystemExit(2) from error
