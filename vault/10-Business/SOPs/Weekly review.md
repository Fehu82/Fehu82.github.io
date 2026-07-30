---
type: sop
cadence: weekly
tags:
  - fehu/sop
---

# Weekly review

Thirty minutes, once a week. This is the loop that makes the machine a machine
rather than a pile of scripts — it is the only step that turns results back into
inputs.

## 1. Read the money (10 min)

Open Gumroad → Analytics. For the last 7 days record:

| What | Where it comes from |
|---|---|
| Sales count and revenue | Gumroad dashboard |
| Which product sold | Gumroad, per-product |
| **Which `utm_content` earned it** | Gumroad referrer/UTM breakdown |
| Views per product page | Gumroad listing views |
| New subscribers | Your email provider (once [[Wire email capture]] is done) |

Write these into `vault/private/ledger.md`. Real numbers stay out of the public
repo — see [[Ledger]].

## 2. Score what shipped (10 min)

Open `20-Content/Hooks/` and `20-Content/Pins/` and find the checkboxes you
ticked this week. For each one that got a sale or unusual traffic, mark it:

```
- [x] shipped · channel: pinterest · date: 2026-08-04 · sales: 2
```

Then answer one question in the ledger: **which angle won?** Not which wording —
which buying motive. "Gift for grandparent" beating "wind-down ritual" tells you
what to generate more of; a specific title winning tells you almost nothing.

## 3. Regenerate against what won (5 min)

```bash
python3 tools/generate_hooks.py <slug> --count 8
python3 tools/generate_pins.py <slug> --count 5
```

Before running, add a line to the top of `90-Meta/Prompts/house-style.md` noting
the winning angle so the next generation leans that way.

## 4. Pick next week's one thing (5 min)

One. Not a list. In priority order, the honest queue is:

1. [[Wire email capture]] — nothing else compounds until this is done
2. Real previews on the five pages that show blank boxes (`tools/render_previews.py`)
3. Ship the winning angle to more pins
4. A seventh product

Write the choice in [[Content calendar]] and stop.

## What not to do here

- Do not add ad spend. The machine is designed to work at zero marginal cost;
  a budget turns a slow compounding thing into a fast losing one.
- Do not chase a channel with no sales for less than three weeks of posting.
  Pinterest in particular indexes slowly — pins routinely take 4–8 weeks to
  find traffic.
- Do not rewrite copy that has never been shipped. Untested variants are not
  evidence of anything.

Related: [[Fehu Lab MOC]], [[Ledger]], [[Content calendar]]
