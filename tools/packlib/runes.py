"""Elder-Futhark-inspired rune staves as normalised polylines.

Each rune is a list of polylines in a box of x∈[-0.45, 0.45], y∈[-1, 1], so a
rune can be scaled and centred anywhere on a page. These are stylised drawing
forms built for coloring pages, not a palaeographic reference.
"""

from __future__ import annotations

import math

# name -> list of polylines, each a list of (x, y) in the normalised box
STAVES: dict[str, list[list[tuple[float, float]]]] = {
    "Fehu": [
        [(0, -1), (0, 1)],
        [(0, 0.55), (0.45, 0.95)],
        [(0, 0.10), (0.45, 0.50)],
    ],
    "Uruz": [
        [(-0.35, -1), (-0.35, 1), (0.35, 0.45), (0.35, -1)],
    ],
    "Thurisaz": [
        [(0, -1), (0, 1)],
        [(0, 0.55), (0.42, 0.15), (0, -0.25)],
    ],
    "Ansuz": [
        [(0, -1), (0, 1)],
        [(0, 0.95), (0.42, 0.50)],
        [(0, 0.45), (0.42, 0.00)],
    ],
    "Raidho": [
        [(0, -1), (0, 1)],
        [(0, 1), (0.40, 0.70), (0, 0.35)],
        [(0, 0.30), (0.42, -1)],
    ],
    "Kenaz": [
        [(0.35, 1), (-0.30, 0), (0.35, -1)],
    ],
    "Gebo": [
        [(-0.40, 1), (0.40, -1)],
        [(0.40, 1), (-0.40, -1)],
    ],
    "Wunjo": [
        [(0, -1), (0, 1)],
        [(0, 1), (0.40, 0.62), (0, 0.30)],
    ],
    "Hagalaz": [
        [(-0.38, -1), (-0.38, 1)],
        [(0.38, -1), (0.38, 1)],
        [(-0.38, 0.25), (0.38, -0.25)],
    ],
    "Naudhiz": [
        [(0, -1), (0, 1)],
        [(-0.40, -0.35), (0.40, 0.35)],
    ],
    "Isa": [
        [(0, -1), (0, 1)],
    ],
    "Jera": [
        [(-0.05, 0.95), (0.40, 0.50), (-0.05, 0.10)],
        [(0.05, -0.95), (-0.40, -0.50), (0.05, -0.10)],
    ],
    "Eihwaz": [
        [(0, -1), (0, 1)],
        [(0, 1), (0.40, 0.72)],
        [(0, -1), (-0.40, -0.72)],
    ],
    "Pertho": [
        [(-0.20, -1), (-0.20, 1)],
        [(-0.20, 1), (0.34, 0.58)],
        [(-0.20, -1), (0.34, -0.58)],
    ],
    "Algiz": [
        [(0, -1), (0, 1)],
        [(0, 0.35), (-0.42, 1)],
        [(0, 0.35), (0.42, 1)],
    ],
    "Sowilo": [
        [(0.35, 0.95), (-0.22, 0.50), (0.28, 0.00), (-0.30, -0.95)],
    ],
    "Tiwaz": [
        [(0, -1), (0, 1)],
        [(-0.38, 0.50), (0, 1), (0.38, 0.50)],
    ],
    "Berkana": [
        [(0, -1), (0, 1)],
        [(0, 1), (0.40, 0.65), (0, 0.25)],
        [(0, 0.25), (0.40, -0.15), (0, -0.55)],
    ],
}

# The 18 runes carried by the rune pack's mandala pages, in listing order.
MANDALA_RUNES = [
    "Fehu", "Uruz", "Thurisaz", "Ansuz", "Raidho", "Kenaz",
    "Gebo", "Wunjo", "Hagalaz", "Naudhiz", "Isa", "Jera",
    "Eihwaz", "Pertho", "Algiz", "Sowilo", "Tiwaz", "Berkana",
]

# Two-rune compositions sharing one stave, with the meaning pairing published
# on the listing.
BIND_RUNES = [
    ("Fehu", "Wunjo", "wealth and joy"),
    ("Algiz", "Tiwaz", "ward and victory"),
    ("Sowilo", "Raidho", "sun on the road"),
    ("Kenaz", "Naudhiz", "torch and signal"),
    ("Jera", "Berkana", "seed and new growth"),
    ("Gebo", "Uruz", "gift and inheritance"),
]


def draw_rune(page, name: str, cx: float, cy: float, scale: float,
              rotation_deg: float = 0.0) -> None:
    """Draw a rune centred at (cx, cy), scaled so y spans 2*scale."""
    theta = math.radians(rotation_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    for stroke in STAVES[name]:
        points = []
        for x, y in stroke:
            sx, sy = x * scale, y * scale
            points.append((cx + sx * cos_t - sy * sin_t,
                           cy + sx * sin_t + sy * cos_t))
        page.polyline(points)


def draw_bind_rune(page, left: str, right: str, cx: float, cy: float,
                   scale: float) -> None:
    """Two runes sharing one central vertical stave."""
    page.polyline([(cx, cy - scale), (cx, cy + scale)])
    for name, mirror in ((left, -1.0), (right, 1.0)):
        for stroke in STAVES[name]:
            # Skip the rune's own stave; the shared one already stands.
            xs = {round(x, 3) for x, _ in stroke}
            if xs == {0.0} and len(stroke) == 2:
                continue
            page.polyline([(cx + x * scale * mirror, cy + y * scale)
                           for x, y in stroke])
