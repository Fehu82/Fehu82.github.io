"""Paths and credentials, resolved from the environment.

Loads a local .env if present so the scripts work without an activated shell,
but never writes one and never logs a key.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT = REPO_ROOT / "vault"
VAULT_PRIVATE = VAULT / "private"
PRODUCTS = VAULT / "10-Business" / "Products"
HOOKS = VAULT / "20-Content" / "Hooks"
PINS = VAULT / "20-Content" / "Pins"
PROMPTS = VAULT / "90-Meta" / "Prompts"

# Every product page is a directory of the same name at the repo root.
SITE_BASE = "https://fehu82.github.io"
GUMROAD_BASE = "https://3323568385272.gumroad.com/l"


def load_dotenv(path: Path | None = None) -> None:
    """Read KEY=VALUE lines from .env into os.environ without overwriting."""
    env_path = path or (REPO_ROOT / ".env")
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


class ConfigError(RuntimeError):
    """Raised when a required setting is missing — never contains the value."""


def provider() -> str:
    return os.environ.get("FEHU_PROVIDER", "kimi").strip().lower()


def require(name: str, hint: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigError(f"{name} is not set. {hint}")
    return value
