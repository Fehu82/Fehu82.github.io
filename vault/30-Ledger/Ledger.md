---
type: reference
tags:
  - fehu/ledger
---

# Ledger

## Where the real numbers live

`vault/private/ledger.md` — **gitignored, never committed**. This repo is public
and permanent; anything pushed here is readable by anyone forever, including
future employers, competitors and scrapers. Revenue, subscriber counts, payout
details and conversion rates go in `private/` only.

This note holds the schema. The private file holds the values.

## Schema

Append one row per week to `vault/private/ledger.md`:

```markdown
## 2026-W32  (Aug 3–9)

| metric | value |
|---|---|
| revenue | $0.00 |
| units | 0 |
| best product | — |
| best utm_content | — |
| best angle | — |
| gumroad views | 0 |
| new subscribers | 0 |
| pins posted | 0 |
| hooks shipped | 0 |

**Winning angle this week:** —
**One thing next week:** —
```

## Rules

- **Record zeros.** A week of $0.00 is data. Blank weeks make the series
  unreadable and hide how long a channel has actually been given.
- **Revenue means settled, after Gumroad fees.** Not gross, not pending. Use the
  payout figure, so the series never flatters itself.
- **`best utm_content` is the whole point.** Without it there is no feedback and
  the generators are guessing. If Gumroad shows no UTM data, the links on the
  site are wrong — check that every outbound Gumroad link carries its tag.
- **Never backfill an estimate.** If a number is unknown, write `unknown`.

## Current honest state

Fehu Lab total real revenue to date: **$0.00**. Six products live, checkout
working, no traffic engine running yet, email capture not wired. That figure is
stated on every page of the site and should stay accurate.

Related: [[Fehu Lab MOC]], [[Weekly review]]
