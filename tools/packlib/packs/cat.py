"""Cat Coloring Pages — 5 cat motif families x 6 pages.

Original procedural cats: no copyrighted characters, and a visual language
distinct from every earlier pack.
"""

from __future__ import annotations

import math

from .. import weave
from ..page import W_ACCENT, W_DETAIL, W_OUTLINE

SLUG = "cat-coloring-pack"
TITLE = "Cat Coloring Pages - 30 Printable Cat & Kitten Designs"
PAGES = 30


# --- cat parts -----------------------------------------------------------

def cat_face(page, cx, cy, r, *, whiskers=True, sleepy=False) -> None:
    """A stylised cat face built from circles, arcs and triangles."""
    page.circle(cx, cy, r)

    # Ears: a triangle standing on the skull line, with an inner ear inside it.
    for side in (-1, 1):
        a_out = math.radians(42 if side > 0 else 138)
        a_in = math.radians(82 if side > 0 else 98)
        p_out = (cx + r * math.cos(a_out), cy + r * math.sin(a_out))
        p_in = (cx + r * math.cos(a_in), cy + r * math.sin(a_in))
        tip = (cx + side * r * 0.80, cy + r * 1.38)
        page.polyline([p_in, tip, p_out])

        gx = (p_in[0] + p_out[0] + tip[0]) / 3.0
        gy = (p_in[1] + p_out[1] + tip[1]) / 3.0
        inner = [(gx + (px - gx) * 0.52, gy + (py - gy) * 0.52)
                 for px, py in (p_in, tip, p_out)]
        page.polyline(inner)

    # Eyes.
    eye_dx, eye_dy, eye_r = r * 0.40, r * 0.16, r * 0.20
    for side in (-1, 1):
        ex, ey = cx + side * eye_dx, cy + eye_dy
        if sleepy:
            page.arc(ex, ey, eye_r, 190, 350)
        else:
            page.ellipse(ex, ey, eye_r * 0.86, eye_r)
            page.circle(ex, ey, eye_r * 0.34)

    # Nose and mouth.
    nose = r * 0.11
    page.polyline([(cx - nose, cy - r * 0.20), (cx + nose, cy - r * 0.20),
                   (cx, cy - r * 0.34)], close=True)
    page.arc(cx - nose * 1.5, cy - r * 0.46, nose * 1.6, 300, 400)
    page.arc(cx + nose * 1.5, cy - r * 0.46, nose * 1.6, 140, 240)

    if whiskers:
        for side in (-1, 1):
            for k in (-1, 0, 1):
                y = cy - r * 0.24 + k * r * 0.15
                page.polyline([(cx + side * r * 0.34, y),
                               (cx + side * r * 1.28, y + k * r * 0.16)])


def sitting_cat(page, cx, cy, h) -> None:
    """A sitting-cat silhouette: shoulders narrow, haunches wide."""
    head_r = h * 0.185
    top = cy + h * 0.06
    bottom = cy - h * 0.40
    half_top, half_bottom = h * 0.155, h * 0.315

    def half_at(t: float) -> float:
        return half_top + (half_bottom - half_top) * (t ** 1.45)

    left, right = [], []
    for i in range(25):
        t = i / 24
        y = top + (bottom - top) * t
        left.append((cx - half_at(t), y))
        right.append((cx + half_at(t), y))
    page.polyline(left)
    page.polyline(right)
    page.polyline([left[-1], right[-1]])

    cat_face(page, cx, top + head_r * 0.72, head_r, whiskers=True)

    # Tail sweeping out from the right haunch and curling up. Kept short enough
    # that it stays inside the page frame at the largest size we draw at.
    tail = []
    for i in range(33):
        t = i / 32
        a = math.radians(196 + 128 * t)
        rr = h * (0.16 + 0.07 * t)
        tail.append((cx + half_bottom * 0.80 + rr * math.cos(a),
                     bottom + h * 0.09 + rr * math.sin(a)))
    page.polyline(tail)

    # Front paws resting on the floor line.
    for side in (-1, 1):
        page.ellipse(cx + side * half_bottom * 0.46, bottom + h * 0.035,
                     h * 0.085, h * 0.048)


def cat_loaf(page, cx, cy, w) -> None:
    """The classic loaf: a flat-topped rounded blob, paws tucked under."""
    h = w * 0.78
    base = cy - h * 0.42
    pts = []
    for i in range(81):
        t = math.pi * i / 80
        # sin raised below 1 flattens the top into a loaf rather than a dome
        pts.append((cx - w * math.cos(t), base + h * (math.sin(t) ** 0.62)))
    pts.append((cx + w, base))
    pts.append((cx - w, base))
    page.polyline(pts, close=True)

    # Ears sitting on the loaf's shoulders.
    for side in (-1, 1):
        bx = cx + side * w * 0.30
        by = base + h * (math.sin(math.acos(0.30)) ** 0.62)
        page.polyline([(bx - side * w * 0.12, by),
                       (bx + side * w * 0.04, by + h * 0.26),
                       (bx + side * w * 0.20, by - h * 0.02)])

    # Face, low on the loaf where a real cat's is.
    fy = base + h * 0.46
    for side in (-1, 1):
        page.circle(cx + side * w * 0.24, fy, w * 0.052)
    page.polyline([(cx - w * 0.055, fy - h * 0.14), (cx + w * 0.055, fy - h * 0.14),
                   (cx, fy - h * 0.23)], close=True)
    page.arc(cx - w * 0.075, fy - h * 0.30, w * 0.078, 300, 400)
    page.arc(cx + w * 0.075, fy - h * 0.30, w * 0.078, 140, 240)

    # Tucked front paws.
    for side in (-1, 1):
        page.arc(cx + side * w * 0.34, base, w * 0.20, 15, 165)


def paw_print(page, cx, cy, r) -> None:
    page.ellipse(cx, cy - r * 0.30, r * 0.62, r * 0.50)
    for i, side in enumerate((-1.45, -0.50, 0.50, 1.45)):
        lift = r * (0.62 if abs(side) < 1 else 0.44)
        page.ellipse(cx + side * r * 0.34, cy + lift, r * 0.20, r * 0.26)


def _pattern_fill(page, cx, cy, rx, ry, kind, step) -> None:
    """Stripe / chevron / dot / scale fills clipped to an ellipse."""
    n = max(3, int(2 * ry / step))
    if kind == 0:  # stripes
        for i in range(1, n):
            y = cy - ry + i * step
            half = rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry) ** 2))
            page.polyline([(cx - half, y), (cx + half, y)])
    elif kind == 1:  # chevrons
        for i in range(1, n):
            y = cy - ry + i * step
            half = rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry) ** 2))
            page.polyline([(cx - half, y), (cx, y + step * 0.62), (cx + half, y)])
    elif kind == 2:  # dots
        rows = max(3, int(2 * ry / (step * 1.2)))
        for i in range(rows):
            y = cy - ry + (i + 0.5) * (2 * ry / rows)
            half = rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry) ** 2))
            cols = max(1, int(2 * half / (step * 1.2)))
            for j in range(cols):
                x = cx - half + (j + 0.5) * (2 * half / cols)
                page.circle(x, y, step * 0.26)
    else:  # scales
        rows = max(3, int(2 * ry / (step * 0.9)))
        for i in range(rows):
            y = cy - ry + (i + 0.5) * (2 * ry / rows)
            half = rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry) ** 2))
            cols = max(1, int(2 * half / step))
            for j in range(cols):
                x = cx - half + (j + 0.5) * (2 * half / cols)
                page.arc(x, y, step * 0.46, 200, 340)


# --- families ------------------------------------------------------------

def _cat_mandala(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.bead_band(cx, cy, R * 0.935, 28 + (n % 3) * 8, R * 0.025)
    page.circle(cx, cy, R * 0.875)

    page.width(W_DETAIL)
    ring = 8 + (n % 3) * 2
    for i in range(ring):
        a = 2 * math.pi * i / ring + math.pi / 2
        paw_print(page, cx + R * 0.755 * math.cos(a), cy + R * 0.755 * math.sin(a),
                  R * 0.075)
    page.circle(cx, cy, R * 0.625)

    petals = 10 + (n % 4) * 2
    for i in range(petals):
        a = 360.0 * i / petals
        page.teardrop_petal(cx + R * 0.50 * math.cos(math.radians(a)),
                            cy + R * 0.50 * math.sin(math.radians(a)),
                            a, R * 0.145, R * 0.050)
    page.circle(cx, cy, R * 0.475)
    page.star_polygon(cx, cy, R * 0.44, 10 + (n % 3) * 2, 3, rotation_deg=90)

    page.width(W_OUTLINE)
    cat_face(page, cx, cy - R * 0.03, R * 0.245, sleepy=(n % 3 == 2))


def _portrait(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    sides = [6, 8, 5, 4, 7, 3][n % 6]

    page.width(W_OUTLINE)
    page.regular_polygon(cx, cy, R * 0.97, sides, rotation_deg=90)
    page.width(W_ACCENT)
    page.regular_polygon(cx, cy, R * 0.90, sides, rotation_deg=90)
    page.regular_polygon(cx, cy, R * 0.83, sides, rotation_deg=90 + 180 / sides)

    page.width(W_DETAIL)
    for i in range(sides):
        a = math.radians(90 + 360 * i / sides)
        page.circle(cx + R * 0.865 * math.cos(a), cy + R * 0.865 * math.sin(a),
                    R * 0.038)

    page.width(W_OUTLINE)
    cat_face(page, cx, cy - R * 0.10, R * 0.42, sleepy=(n % 2 == 1))

    # Chest curve below the chin, with the pattern kept inside it — floating
    # stripes above the head read as stray marks, not decoration.
    page.width(W_ACCENT)
    page.arc(cx, cy - R * 0.10, R * 0.60, 205, 335)
    _pattern_fill(page, cx, cy - R * 0.58, R * 0.30, R * 0.085, n % 4, R * 0.048)


def _knotwork_cat(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    page.width(W_DETAIL)
    weave.chain_ring(page, cx, cy, R * 0.845, R * 0.105,
                     spacing=1.40 + 0.04 * (n % 3), rotation_deg=n * 9.0)
    weave.chain_ring(page, cx, cy, R * 0.615, R * 0.088,
                     spacing=1.46, rotation_deg=n * 13.0)

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.495)

    page.width(W_OUTLINE)
    sitting_cat(page, cx, cy - R * 0.06, R * 0.80)


def _patterned(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_ACCENT)
    page.circle(cx, cy, R)
    page.tick_rim(cx, cy, R * 0.955, R, 48 + n * 8)

    page.width(W_OUTLINE)
    sitting_cat(page, cx, cy + R * 0.02, R * 1.15)

    # Pattern inside the body mass only, so the outline stays colorable. The
    # step varies across the whole family so no two patterned cats repeat.
    page.width(W_ACCENT)
    _pattern_fill(page, cx, cy - R * 0.30, R * 0.36, R * 0.30, n % 4,
                  R * (0.058 + 0.009 * n))

    page.width(W_DETAIL)
    for side in (-1, 1):
        paw_print(page, cx + side * R * 0.70, cy - R * 0.72, R * 0.085)


def _paw_wheel(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.945)

    page.width(W_DETAIL)
    for ring_i, (rr, count, size) in enumerate((
        (R * 0.815, 10 + n * 2, R * 0.088),
        (R * 0.585, 6 + n, R * 0.078),
    )):
        page.circle(cx, cy, rr + size * 1.5)
        page.circle(cx, cy, rr - size * 1.5)
        for i in range(count):
            a = 2 * math.pi * i / count + math.pi / 2 + ring_i * 0.3
            paw_print(page, cx + rr * math.cos(a), cy + rr * math.sin(a), size)

    page.width(W_OUTLINE)
    cat_loaf(page, cx, cy - R * 0.08, R * 0.34)


_FAMILIES = [_cat_mandala, _portrait, _knotwork_cat, _patterned, _paw_wheel]


def draw(page, index: int) -> None:
    _FAMILIES[index % len(_FAMILIES)](page, index // len(_FAMILIES))
