"""Fehu Lab tooling — the engine behind the Obsidian vault.

Nothing in this package talks to the network at import time, and no module
holds a credential. Keys come from the environment (see .env.example).
"""

__all__ = ["config", "llm", "vault", "site"]
