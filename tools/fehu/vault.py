"""Read and write Obsidian notes: YAML-ish frontmatter plus markdown body.

Deliberately a small hand-rolled subset (scalars and flat lists) so the vault
stays dependency-free. Obsidian, Dataview and the human eye all read it fine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

FENCE = "---"


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return '""'
    text = str(value)
    if text == "":
        return '""'
    # Quote anything YAML would otherwise reinterpret.
    if text[0] in "#&*!|>%@`{[" or ": " in text or text.strip() != text:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def _parse_scalar(text: str) -> Any:
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if text in ("true", "false"):
        return text == "true"
    return text


@dataclass
class Note:
    path: Path
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def title(self) -> str:
        return self.path.stem

    def render(self) -> str:
        if not self.frontmatter:
            return self.body.rstrip() + "\n"
        lines = [FENCE]
        for key, value in self.frontmatter.items():
            if isinstance(value, (list, tuple)):
                lines.append(f"{key}:")
                lines.extend(f"  - {_format_scalar(item)}" for item in value)
            else:
                lines.append(f"{key}: {_format_scalar(value)}")
        lines.append(FENCE)
        return "\n".join(lines) + "\n\n" + self.body.strip() + "\n"

    def write(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.render(), encoding="utf-8")
        return self.path


def read(path: Path) -> Note:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith(FENCE):
        return Note(path=path, body=raw)

    _, _, rest = raw.partition(FENCE)
    block, sep, body = rest.partition(f"\n{FENCE}")
    if not sep:
        return Note(path=path, body=raw)

    frontmatter: dict[str, Any] = {}
    pending_key: str | None = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and pending_key:
            frontmatter[pending_key].append(_parse_scalar(line.lstrip()[2:]))
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not value.strip():
            frontmatter[key] = []
            pending_key = key
        else:
            frontmatter[key] = _parse_scalar(value)
            pending_key = None
    return Note(path=path, frontmatter=frontmatter, body=body.lstrip("\n"))


def link(target: str, alias: str | None = None) -> str:
    """An Obsidian wikilink. Keeps link syntax in one place."""
    return f"[[{target}|{alias}]]" if alias else f"[[{target}]]"


def slugify(text: str) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in text]
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")
