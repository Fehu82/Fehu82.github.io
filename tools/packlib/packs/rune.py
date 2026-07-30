"""Rune Mandalas — 18 rune mandalas, 6 knotwork medallions, 6 bind-runes.

Interleaved as published: three mandalas, a medallion, a bind-rune, repeating.
"""

from __future__ import annotations

import math

from .. import runes, weave
from ..page import W_ACCENT, W_DETAIL, W_OUTLINE

SLUG = "rune-coloring-pack"
TITLE = "Rune Mandalas - A Viking Knotwork Coloring Book"
PAGES = 30

# 6 cycles of [mandala, mandala, mandala, medallion, bind-rune]
_CYCLE = ["mandala", "mandala", "mandala", "medallion", "bind"]


def _kind(index: int) -> tuple[str, int]:
    """(kind, ordinal-within-kind) for a page index."""
    cycle, pos = divmod(index, len(_CYCLE))
    kind = _CYCLE[pos]
    if kind == "mandala":
        return kind, cycle * 3 + pos
    return kind, cycle


def _mandala(page, n: int) -> None:
    rune = runes.MANDALA_RUNES[n % len(runes.MANDALA_RUNES)]
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.circle(cx, cy, R * 0.93)

    # Outer band alternates between beads and a ticked rim.
    page.width(W_ACCENT)
    if n % 2 == 0:
        page.bead_band(cx, cy, R * 0.865, 24 + (n % 3) * 6, R * 0.032)
    else:
        page.tick_rim(cx, cy, R * 0.82, R * 0.925, 48 + (n % 4) * 12)

    # Ring of the pack's runes, upright and facing out.
    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.79)
    ring_count = 8 + (n % 3) * 2
    for i in range(ring_count):
        a = 2 * math.pi * i / ring_count + math.pi / 2
        rx, ry = cx + R * 0.70 * math.cos(a), cy + R * 0.70 * math.sin(a)
        name = runes.MANDALA_RUNES[(n + i) % len(runes.MANDALA_RUNES)]
        runes.draw_rune(page, name, rx, ry, R * 0.062)

    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.615)

    # Seed-of-life petal ring.
    petals = 6 if n % 3 == 0 else (8 if n % 3 == 1 else 12)
    page.petal_ring(cx, cy, R * 0.42, petals, R * 0.235, rotation_deg=90)

    # Star-polygon core.
    page.width(W_DETAIL)
    star_points, star_step = [(7, 2), (8, 3), (9, 2), (12, 5), (5, 2), (10, 3)][n % 6]
    page.star_polygon(cx, cy, R * 0.40, star_points, star_step, rotation_deg=90)

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.275)
    page.bead_band(cx, cy, R * 0.325, 16, R * 0.019)

    # The bold central rune.
    page.width(W_OUTLINE * 1.35)
    runes.draw_rune(page, rune, cx, cy, R * 0.20)


def _medallion(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    # Three concentric interlaced knot bands. Each band is a closed chain of
    # overlapping links that pass over and under one another.
    # Sizing by link radius rather than link count is what keeps each band
    # inside its own lane instead of bleeding into its neighbours.
    links = [(0.115, 0.105, 0.095), (0.100, 0.094, 0.088),
             (0.128, 0.112, 0.098), (0.108, 0.100, 0.092),
             (0.120, 0.108, 0.090), (0.095, 0.090, 0.085)][n % 6]
    spacings = (1.38, 1.45, 1.52, 1.42, 1.48, 1.35)
    radii = (R * 0.815, R * 0.560, R * 0.310)
    for band, (rad, link) in enumerate(zip(radii, links)):
        page.width(W_DETAIL)
        weave.chain_ring(page, cx, cy, rad, R * link,
                         spacing=spacings[(n + band) % 6],
                         rotation_deg=band * 11.0)

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.185)

    # Centre alternates: star, rune, or petal cluster.
    centre = n % 3
    page.width(W_OUTLINE)
    if centre == 0:
        page.star_polygon(cx, cy, R * 0.150, 8, 3, rotation_deg=90)
        page.width(W_ACCENT)
        page.circle(cx, cy, R * 0.055)
    elif centre == 1:
        runes.draw_rune(page, runes.MANDALA_RUNES[(n * 5) % 18], cx, cy, R * 0.130)
    else:
        page.petal_ring(cx, cy, R * 0.075, 6, R * 0.075, rotation_deg=90)
        page.width(W_ACCENT)
        page.circle(cx, cy, R * 0.150)


def _bind(page, n: int) -> None:
    left, right, _meaning = runes.BIND_RUNES[n % len(runes.BIND_RUNES)]
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.94)
    page.bead_band(cx, cy, R * 0.885, 30, R * 0.026)

    # Ring of the two component runes, alternating.
    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.80)
    for i in range(10):
        a = 2 * math.pi * i / 10 + math.pi / 2
        rx, ry = cx + R * 0.705 * math.cos(a), cy + R * 0.705 * math.sin(a)
        runes.draw_rune(page, left if i % 2 == 0 else right, rx, ry, R * 0.058)

    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.615)
    page.star_polygon(cx, cy, R * 0.575, 12, 5, rotation_deg=90)

    # The bind-rune itself: two runes sharing one stave.
    page.width(W_OUTLINE * 1.5)
    runes.draw_bind_rune(page, left, right, cx, cy, R * 0.40)


def draw(page, index: int) -> None:
    kind, n = _kind(index)
    if kind == "mandala":
        _mandala(page, n)
    elif kind == "medallion":
        _medallion(page, n)
    else:
        _bind(page, n)
