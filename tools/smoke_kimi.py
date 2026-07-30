#!/usr/bin/env python3
"""Verify the Kimi connection with one cheap call.

    cp .env.example .env      # then paste your key into .env
    python3 tools/smoke_kimi.py

This cannot succeed inside a sandboxed session with no outbound network — run
it on your own machine.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fehu import config, llm  # noqa: E402


def main() -> int:
    config.load_dotenv()
    provider = config.provider()
    key_var = "MOONSHOT_API_KEY" if provider == "kimi" else "ANTHROPIC_API_KEY"
    key = os.environ.get(key_var, "")

    print(f"{'provider':<20}{provider}")
    print(f"{key_var:<20}{'set (' + str(len(key)) + ' chars)' if key else 'MISSING'}")
    if provider == "kimi":
        base = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.ai/v1")
        model = os.environ.get("MOONSHOT_MODEL", "kimi-k2-0905-preview")
        print(f"{'base url':<20}{base}")
        print(f"{'model':<20}{model}")
    print()

    reply = llm.chat(
        "You are a connection test. Answer in exactly four words.",
        "Confirm you are reachable.",
        temperature=0.0,
    )
    print(f"reply from {reply.provider}/{reply.model}:")
    print(f"  {reply.text.strip()}")
    print("\nConnection works. The generators will run.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (llm.LLMError, config.ConfigError) as error:
        print(f"\nFailed: {error}", file=sys.stderr)
        raise SystemExit(2) from error
