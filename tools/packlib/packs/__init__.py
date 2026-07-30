"""One module per pack. Each exposes SLUG, TITLE, PAGES and draw(page, index)."""

from . import rune, sacred, celestial, cat, bold_easy

ALL = {m.SLUG: m for m in (rune, sacred, celestial, cat, bold_easy)}

__all__ = ["ALL", "rune", "sacred", "celestial", "cat", "bold_easy"]
