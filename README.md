# Fehu82.github.io

Fehu Lab storefronts — printable coloring packs and the Night-Drift Playbook —
plus the Obsidian vault and tooling that run them.

Live at **https://fehu82.github.io**

## Layout

```
index.html              landing page, six product cards
<slug>/index.html       one storefront per product
assets/capture.js       email capture — ONE constant switches it on site-wide
vault/                  Obsidian vault: SOPs, product notes, content, ledger schema
tools/                  Kimi/Claude generators and the site→vault sync
```

## The loop

```
Kimi generates copy variants  →  tools/generate_hooks.py, tools/generate_pins.py
you ship them organically     →  Pinterest, TikTok
UTM-tagged Gumroad links      →  Gumroad reports which utm_content earned the sale
results recorded              →  vault/private/ledger.md  (gitignored)
next week reads what won      →  vault/10-Business/SOPs/Weekly review.md
```

No ad spend, no automated outreach, no purchasing. Time and existing products are
the only inputs.

## Setup

```bash
cp .env.example .env          # paste your Moonshot key; .env is gitignored
python3 tools/smoke_kimi.py   # verify the connection
python3 tools/sync_products.py
```

Open `vault/` in Obsidian (Open folder as vault) and install the **Obsidian Git**
plugin to keep notes and repo in sync. See `vault/90-Meta/Obsidian setup.md`.

## Tools

| Command | Does |
|---|---|
| `python3 tools/build_packs.py [slug]` | build the pack PDFs — **these are the products** |
| `python3 tools/render_previews.py <slug> <pdf>` | preview PNGs from a real PDF |
| `python3 tools/sync_products.py` | mirror the live pages into vault product notes |
| `python3 tools/generate_hooks.py [slug] [--count N]` | title/hook variants to test |
| `python3 tools/generate_pins.py [slug] [--count N]` | Pinterest and TikTok copy |
| `python3 tools/smoke_kimi.py` | one call to verify the API key |

The Kimi tools are standard library only. Building packs needs `reportlab`;
verification additionally uses `pypdf`, and `pymupdf` + `Pillow` for previews:

```bash
pip install reportlab pypdf pymupdf pillow
```

## The packs

`tools/packlib/` generates all five coloring packs — 150 pages of black vector
line art, no bitmaps, no fills. Generation is deterministic: the same code always
produces the same pages, which is what makes "these previews are real pages from
the product" a checkable claim rather than a promise.

```
packlib/page.py     US Letter, print-safe margins, drawing primitives
packlib/weave.py    interlocking chain knotwork with real over-under
packlib/runes.py    Elder-Futhark-inspired staves
packlib/packs/      one module per pack
```

`build_packs.py` verifies every build: 30 pages, uniform Letter mediabox, 30
unique page content streams, and no ink outside the printable frame. That last
check caught five pages that would have printed clipped.

> [!warning] `assets/packs/` is gitignored on purpose
> Those PDFs are the paid products. This repo is public — committing them would
> give the whole catalogue away. Build locally, upload to Gumroad.

## Unfinished, in priority order

1. **Email capture is not wired.** Two ways to fix it, both one line in
   `assets/capture.js`. The fast one needs no account at all: set `CAPTURE_TO`
   to a dedicated address, push, submit once, click the confirmation link.
   Until then the form honestly refuses to submit and stores nothing. Runbook:
   `vault/10-Business/SOPs/Wire email capture.md`.
2. **The generated packs are not on Gumroad yet.** `tools/build_packs.py` now
   produces all five PDFs and the site shows real previews rendered from them —
   but the files behind the Gumroad checkout links are still whatever was
   uploaded before. Until they are replaced, buyers receive a different file
   from the one previewed. Uploading needs the Gumroad account.
3. **No Kimi key yet.** The generators are built and tested; they need a key.

## Rules

- `vault/private/` and `.env` are gitignored. This repo is public and permanent —
  revenue figures, subscriber counts and keys go in `private/` only.
- Every product is AI-assisted and disclosed as such on its listing.
- No fake scarcity, no invented testimonials, no income claims. See
  `vault/90-Meta/Prompts/house-style.md`.
- Fehu Lab total real revenue to date: **$0.00**. That figure is printed on every
  page and stays accurate.
