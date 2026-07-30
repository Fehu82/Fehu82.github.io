---
type: reference
tags:
  - fehu/meta
---

# Obsidian setup

## Open the vault

Obsidian → **Open folder as vault** → select the `vault/` directory inside this
repo. Everything is plain markdown with YAML frontmatter and `[[wikilinks]]`;
nothing here needs a plugin to be readable.

## Keep it in sync

Install the **Obsidian Git** community plugin (Settings → Community plugins →
Browse → "Obsidian Git"). Point it at this repository and set auto-commit to
something calm — every 10 minutes, or on vault close.

That is the connection: your notes and the repo are the same files, so anything
you write in Obsidian is what the scripts read on the next run, and anything the
scripts generate appears in Obsidian without an import step.

## Useful but optional plugins

- **Dataview** — every note carries typed frontmatter, so queries work out of
  the box. To list everything live:

  ````
  ```dataview
  TABLE price_usd AS Price, status
  FROM #fehu/product
  SORT price_usd DESC
  ```
  ````

- **Templater** — for the templates in `90-Meta/Templates/`.

## The one hard rule

> [!warning] `vault/private/` is gitignored — keep it that way
> This repo is public. `private/` is the only directory here that is not
> world-readable. Real revenue, subscriber counts, payout details and anything
> resembling a key belong there and nowhere else. If you ever move this vault to
> a private repo, that constraint relaxes — until then it does not.

Obsidian Git will not push `private/` because git ignores it. Obsidian Sync (the
paid service) does not use git and **will** sync it between your own devices,
which is fine — that is a different thing from publishing it.

## Layout

```
vault/
  Fehu Lab MOC.md          ← start here
  10-Business/Products/    ← synced from the live site, do not hand-edit above "## Notes"
  10-Business/SOPs/        ← the runbooks
  20-Content/              ← calendar, generated hooks and pins
  30-Ledger/               ← schema only; values live in private/
  90-Meta/                 ← setup notes, templates, prompt library
  private/                 ← gitignored
```

Related: [[Fehu Lab MOC]], [[Kimi setup]]
