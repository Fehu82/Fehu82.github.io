---
type: moc
tags:
  - fehu/hub
---

# ᚠ Fehu Lab — Map of Content

The brain behind [fehu82.github.io](https://fehu82.github.io). Open this folder as
a vault in Obsidian; every note below is plain markdown, so Claude, Kimi and you
all read and write the same files.

> [!warning] This vault is in a **public** repo
> `vault/private/` is gitignored and is the only safe place for real revenue
> numbers, subscriber counts and keys. Everything else here is world-readable
> forever. See [[Ledger]].

## Start here

- [[Weekly review]] — the loop that decides what gets made next
- [[Wire email capture]] — **the highest-value unfinished job on the site**
- [[Publish a product]] — how a new pack goes from PDF to live listing
- [[Ledger]] — what to record when a sale happens

## The machine

```
Kimi generates variants   →   tools/generate_hooks.py, tools/generate_pins.py
        ↓
you ship them organically →   Pinterest, TikTok  (see [[Content calendar]])
        ↓
UTM-tagged Gumroad links  →   Gumroad reports which utm_content earned the sale
        ↓
result lands in           →   vault/private/ledger.md
        ↓
next week reads what won  →   [[Weekly review]]
```

No ad spend, no autonomous purchasing, no cold outreach. The only inputs are
time and the products that already exist.

## Products

Synced from the live site by `python3 tools/sync_products.py` — the site is the
source of truth, this vault mirrors it.

- [[bold-easy-coloring-pack]] — $4.99
- [[cat-coloring-pack]] — $4.99
- [[celestial-coloring-pack]] — $6
- [[sacred-geometry-coloring-pack]] — $6
- [[rune-coloring-pack]] — $7
- [[night-drift-playbook]] — $9

## Content

- [[Content calendar]] — what ships, where, when
- `20-Content/Hooks/` — generated title and hook candidates, untested
- `20-Content/Pins/` — generated Pinterest and TikTok copy, unposted

## Reference

- [[Kimi setup]] — connecting the generation engine
- [[Obsidian setup]] — syncing this vault to your machine
- [[What I did not build]] — the parts of the source videos that were declined,
  and why

## Honest state

As of the last edit: six products live with working checkout, **$0.00 revenue to
date**, email capture **not wired**, previews **missing** on five pages. The
first two of those are the whole game right now — traffic and copy are worth
nothing until a visitor can buy and a lead can be kept.
