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
| `python3 tools/sync_products.py` | mirror the live pages into vault product notes |
| `python3 tools/generate_hooks.py [slug] [--count N]` | title/hook variants to test |
| `python3 tools/generate_pins.py [slug] [--count N]` | Pinterest and TikTok copy |
| `python3 tools/render_previews.py <slug> <pdf>` | real preview PNGs from a real PDF |
| `python3 tools/smoke_kimi.py` | one call to verify the API key |

Standard library only — nothing to install.

## Unfinished, in priority order

1. **Email capture is not wired.** `assets/capture.js` needs a provider form URL.
   Until then the form honestly refuses to submit and stores nothing. Runbook:
   `vault/10-Business/SOPs/Wire email capture.md`.
2. **Previews are links, not images.** No page art has ever existed in this repo.
   `tools/render_previews.py` turns real product PDFs into real preview PNGs; it
   refuses to invent stand-in art, because previews that are not in the product
   misrepresent it.
3. **No Kimi key yet.** The generators are built and tested; they need a key.

## Rules

- `vault/private/` and `.env` are gitignored. This repo is public and permanent —
  revenue figures, subscriber counts and keys go in `private/` only.
- Every product is AI-assisted and disclosed as such on its listing.
- No fake scarcity, no invented testimonials, no income claims. See
  `vault/90-Meta/Prompts/house-style.md`.
- Fehu Lab total real revenue to date: **$0.00**. That figure is printed on every
  page and stays accurate.
