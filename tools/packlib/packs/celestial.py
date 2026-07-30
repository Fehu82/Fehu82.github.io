"""Celestial — 5 night-sky motif families x 6 pages.

Two-circle crescent constructions, asterism charts, orbit systems and layered
star polygons. No glyphs, no knotwork, no circle lattices, so it reads apart
from both the rune and sacred-geometry packs.
"""

from __future__ import annotations

import math
import random

from .. import weave
from ..page import W_ACCENT, W_DETAIL, W_OUTLINE

SLUG = "celestial-coloring-pack"
TITLE = "Celestial - A Moon, Stars & Orbits Coloring Book"
PAGES = 30


def _rng(n: int, salt: int) -> random.Random:
    """Seeded so a rebuild reproduces the same page, star for star."""
    return random.Random(9000 + salt * 101 + n)


def _star_field(page, cx, cy, r_inner, r_outer, count, rng, size) -> None:
    for _ in range(count):
        a = rng.uniform(0, 2 * math.pi)
        d = math.sqrt(rng.uniform((r_inner / r_outer) ** 2, 1.0)) * r_outer
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        s = size * rng.uniform(0.55, 1.35)
        page.polyline([(x - s, y), (x + s, y)])
        page.polyline([(x, y - s), (x, y + s)])
        if rng.random() < 0.4:
            page.polyline([(x - s * 0.6, y - s * 0.6), (x + s * 0.6, y + s * 0.6)])
            page.polyline([(x - s * 0.6, y + s * 0.6), (x + s * 0.6, y - s * 0.6)])


def _crescent(page, cx, cy, r, offset, flip=1.0) -> None:
    """A crescent as the classic two-circle construction.

    Only the part of the second circle that falls *inside* the first is drawn.
    Drawing both circles whole gives a lens, not a crescent — the terminator has
    to stop at the limb.
    """
    page.circle(cx, cy, r)

    bx = cx + offset * flip
    hits = weave._circle_intersections((cx, cy), r, (bx, cy), r)
    if len(hits) != 2:
        return
    angles = sorted(math.atan2(y - cy, x - bx) for x, y in hits)
    lo, hi = angles
    # Two candidate arcs; keep the one whose midpoint lies within the limb.
    for start, end in ((lo, hi), (hi, lo + 2 * math.pi)):
        mid = (start + end) / 2.0
        mx, my = bx + r * math.cos(mid), cy + r * math.sin(mid)
        if math.hypot(mx - cx, my - cy) < r:
            page.arc(bx, cy, r, math.degrees(start), math.degrees(end))
            return


def _moon_wheel(page, n: int) -> None:
    """A wheel of moon phases, each drawn as a terminator ellipse."""
    cx, cy, R = page.cx, page.cy, page.radius
    phases = 8 + (n % 3) * 2

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.945)
    page.tick_rim(cx, cy, R * 0.945, R, phases * 6)

    moon_r = R * 0.135
    ring_r = R * 0.72
    page.width(W_DETAIL)
    page.circle(cx, cy, ring_r + moon_r * 1.5)
    page.circle(cx, cy, ring_r - moon_r * 1.5)

    for i in range(phases):
        a = 2 * math.pi * i / phases + math.pi / 2
        mx, my = cx + ring_r * math.cos(a), cy + ring_r * math.sin(a)
        page.width(W_DETAIL)
        page.circle(mx, my, moon_r)
        # Terminator: an ellipse whose width tracks the phase.
        frac = i / phases
        rx = abs(math.cos(2 * math.pi * frac)) * moon_r
        if rx > moon_r * 0.06:
            page.width(W_ACCENT)
            page.ellipse(mx, my, rx, moon_r)
        else:
            page.width(W_ACCENT)
            page.line(mx, my - moon_r, mx, my + moon_r)

    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.36)
    page.width(W_ACCENT)
    _star_field(page, cx, cy, 0, R * 0.32, 26, _rng(n, 1), R * 0.030)


def _constellation(page, n: int) -> None:
    """A stylised asterism chart with a degree-ticked rim."""
    cx, cy, R = page.cx, page.cy, page.radius
    rng = _rng(n, 2)

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.90)
    page.tick_rim(cx, cy, R * 0.90, R, 72)
    page.tick_rim(cx, cy, R * 0.855, R, 12)

    # A connected asterism: points on a wandering path, never doubling back.
    count = 7 + n % 4
    pts = []
    angle = rng.uniform(0, 2 * math.pi)
    radius = R * 0.20
    for _ in range(count):
        angle += rng.uniform(0.7, 1.5)
        radius = min(R * 0.78, radius + rng.uniform(R * 0.04, R * 0.16))
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))

    page.width(W_DETAIL)
    page.polyline(pts)
    for i, (x, y) in enumerate(pts):
        r = R * 0.030 + R * 0.022 * ((i * 7) % 3)
        page.circle(x, y, r)
        page.width(W_ACCENT)
        for k in range(4):
            a = math.pi / 2 * k + math.pi / 4
            page.line(x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a),
                      x + r * 2.4 * math.cos(a), y + r * 2.4 * math.sin(a))
        page.width(W_DETAIL)

    page.width(W_ACCENT)
    _star_field(page, cx, cy, R * 0.10, R * 0.84, 40, rng, R * 0.024)


def _crescent_medallion(page, n: int) -> None:
    """A big crescent in a petal-and-bead medallion."""
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.bead_band(cx, cy, R * 0.935, 30 + (n % 3) * 6, R * 0.026)

    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.865)
    petals = 12 + (n % 4) * 4
    for i in range(petals):
        a = 360.0 * i / petals
        page.teardrop_petal(cx + R * 0.70 * math.cos(math.radians(a)),
                            cy + R * 0.70 * math.sin(math.radians(a)),
                            a, R * 0.155, R * 0.052)
    page.circle(cx, cy, R * 0.685)

    page.width(W_OUTLINE)
    _crescent(page, cx, cy, R * 0.545, R * (0.22 + 0.06 * (n % 3)),
              flip=1.0 if n % 2 == 0 else -1.0)

    page.width(W_ACCENT)
    _star_field(page, cx, cy, 0, R * 0.50, 18, _rng(n, 3), R * 0.028)


def _orbits(page, n: int) -> None:
    """An orbital system: rings, bodies, and a comet on a sampled ellipse."""
    cx, cy, R = page.cx, page.cy, page.radius
    rng = _rng(n, 4)

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    # The primary.
    page.width(W_OUTLINE)
    page.circle(cx, cy, R * 0.135)
    page.width(W_ACCENT)
    for k in range(12):
        a = 2 * math.pi * k / 12
        page.line(cx + R * 0.155 * math.cos(a), cy + R * 0.155 * math.sin(a),
                  cx + R * 0.215 * math.cos(a), cy + R * 0.215 * math.sin(a))

    rings = 3 + n % 3
    page.width(W_DETAIL)
    # Spread the rings across the available radius rather than by a fixed step,
    # so a five-ring system still lands inside the frame.
    for i in range(rings):
        rr = R * (0.34 + (0.86 - 0.34) * (i / max(1, rings - 1)))
        squash = 1.0 - 0.10 * ((i + n) % 3)
        page.ellipse(cx, cy, rr, rr * squash)
        # A body riding the ring.
        a = rng.uniform(0, 2 * math.pi)
        bx, by = cx + rr * math.cos(a), cy + rr * squash * math.sin(a)
        body = R * (0.036 + 0.020 * ((i + n) % 3))
        page.circle(bx, by, body)
        if (i + n) % 3 == 0:
            page.width(W_ACCENT)
            page.ellipse(bx, by, body * 2.1, body * 0.55)
            page.width(W_DETAIL)

    # Comet: a long ellipse offset from the primary, with a tail. The axes are
    # chosen so the far end of the orbit still lands inside the page frame.
    page.width(W_DETAIL)
    a_axis, b_axis = R * 0.58, R * 0.26
    shift = a_axis * 0.34
    tilt = math.radians(18 + n * 24)
    pts = []
    for i in range(241):
        t = 2 * math.pi * i / 240
        ex, ey = a_axis * math.cos(t) - shift, b_axis * math.sin(t)
        pts.append((cx + ex * math.cos(tilt) - ey * math.sin(tilt),
                    cy + ex * math.sin(tilt) + ey * math.cos(tilt)))
    page.polyline(pts, close=True)

    head = pts[len(pts) // 5]
    page.circle(head[0], head[1], R * 0.040)
    page.width(W_ACCENT)
    for k in range(5):
        spread = math.radians(-16 + 8 * k)
        length = R * (0.16 + 0.03 * abs(2 - k))
        page.line(head[0], head[1],
                  head[0] + length * math.cos(tilt + math.pi + spread),
                  head[1] + length * math.sin(tilt + math.pi + spread))

    _star_field(page, cx, cy, R * 0.25, R * 0.95, 34, rng, R * 0.022)


def _starburst(page, n: int) -> None:
    """Layered star polygons over a ticked rim."""
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.955)
    page.tick_rim(cx, cy, R * 0.90, R * 0.955, 96)

    # Gentle {p/q} ratios only. A {16/7} star is so spiky it fills the page with
    # crossings and leaves nothing large enough to colour.
    layers = [(12, 5), (10, 3), (8, 3), (6, 2)]
    page.width(W_DETAIL)
    for i, (points, step) in enumerate(layers):
        r = R * (0.86 - 0.17 * i)
        page.star_polygon(cx, cy, r, points, step,
                          rotation_deg=90 + i * (9 + n * 4))

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.115)
    page.bead_band(cx, cy, R * 0.175, 12, R * 0.020)
    _star_field(page, cx, cy, R * 0.88, R * 0.95, 16, _rng(n, 5), R * 0.020)


_FAMILIES = [_moon_wheel, _constellation, _crescent_medallion, _orbits, _starburst]


def draw(page, index: int) -> None:
    _FAMILIES[index % len(_FAMILIES)](page, index // len(_FAMILIES))
