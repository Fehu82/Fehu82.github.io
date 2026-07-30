---
type: reference
tags:
  - fehu/meta
---

# Kimi setup

Kimi (Moonshot AI) is the generation engine for hooks and pins. Its API is
OpenAI-compatible, so `tools/fehu/llm.py` talks to it over plain HTTP with no
SDK and no dependencies.

## Connect it

```bash
cp .env.example .env
# paste your key into .env — it is gitignored, never commit it
python3 tools/smoke_kimi.py
```

A working run prints the model name and a four-word reply.

## Settings

| Variable | Default | Notes |
|---|---|---|
| `MOONSHOT_API_KEY` | — | from https://platform.moonshot.ai/ |
| `MOONSHOT_BASE_URL` | `https://api.moonshot.ai/v1` | use `api.moonshot.cn` for a CN account |
| `MOONSHOT_MODEL` | `kimi-k2-0905-preview` | any Kimi chat model |
| `FEHU_PROVIDER` | `kimi` | set to `claude` to run the same scripts on Claude |

Both providers sit behind one `chat()` call, so switching is one variable — the
generators do not know or care which one answered.

## Run it

```bash
python3 tools/generate_hooks.py                     # all products, 8 variants each
python3 tools/generate_pins.py cat-coloring-pack    # one product
python3 tools/generate_pins.py --count 6
```

Output lands in `20-Content/Hooks/` and `20-Content/Pins/` as markdown with
checkboxes. Nothing is posted automatically — you ship it, then score it during
[[Weekly review]].

## Where it cannot run

Not from a sandboxed Claude Code session — outbound network is blocked there and
every host returns 403. Run it on your own machine, or as a GitHub Action using
a repository secret if you want it scheduled.

## House rules baked into the prompts

The system prompts in both generators forbid invented features, fake scarcity,
fabricated testimonials and income claims, and require the AI-assisted
disclosure to stay true. If you edit them, keep those constraints — they are
what keeps the listings honest and Etsy-compliant.

Related: [[Fehu Lab MOC]], [[What I did not build]]
