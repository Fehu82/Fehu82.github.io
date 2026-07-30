# private/ — not committed

This directory is gitignored. It is the only place in this vault that is safe for
information you would not publish on a billboard, because the rest of the repo is
public on GitHub and permanent.

Belongs here:

- `ledger.md` — real revenue, units, payouts, subscriber counts
- conversion rates, traffic numbers
- anything resembling a key, token or account credential
- notes about suppliers, buyers or people

Does **not** belong here — put it in the tracked part of the vault so it is
versioned and shared:

- SOPs, prompts, templates
- product notes, content candidates
- decisions and reasoning

## Start the ledger

Create `ledger.md` here and follow the schema in `30-Ledger/Ledger.md`. Record
zeros. A week of $0.00 is data, and blank weeks hide how long a channel has
actually been given.

## Verify it is ignored

```bash
git check-ignore -v vault/private/ledger.md
```

That must print a matching `.gitignore` rule. If it prints nothing, stop and fix
`.gitignore` before writing anything real here.

_(This README is the one file in `private/` that is committed, as a placeholder
so the directory exists in a fresh clone — see the negation rule in `.gitignore`.)_
