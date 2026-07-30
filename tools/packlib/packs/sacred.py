"""Sacred Geometry — 6 construction families x 5 pages.

Compass-and-straightedge constructions only: no glyphs, no knotwork, so the
visual language stays distinct from the rune pack.
"""

from __future__ import annotations

import math

from ..page import W_ACCENT, W_DETAIL, W_OUTLINE

SLUG = "sacred-geometry-coloring-pack"
TITLE = "Sacred Geometry - A Compass & Straightedge Coloring Book"
PAGES = 30

SQRT3 = math.sqrt(3.0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0


def _hex_centres(rings: int, spacing: float) -> list[tuple[float, float]]:
    """Centres of a hexagonal lattice out to `rings` rings."""
    out = []
    for q in range(-rings, rings + 1):
        for r in range(max(-rings, -q - rings), min(rings, -q + rings) + 1):
            out.append((spacing * (q + r / 2.0), spacing * (SQRT3 / 2.0) * r))
    return out


def _flower(page, n: int) -> None:
    """Flower-of-life lattice: overlapping circles on a hex grid."""
    cx, cy, R = page.cx, page.cy, page.radius
    rings = 3 + n % 3
    spacing = R / (rings + 0.55)

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.circle(cx, cy, R * 0.955)

    # Overlapping by exactly one radius is what produces the bloom. Keeping the
    # whole circle inside the frame, not just its centre, stops the lattice
    # spilling past the border.
    page.width(W_DETAIL)
    for dx, dy in _hex_centres(rings, spacing):
        if math.hypot(dx, dy) + spacing <= R * 0.955:
            page.circle(cx + dx, cy + dy, spacing)

    page.width(W_ACCENT)
    if n % 2:
        page.bead_band(cx, cy, R * 0.905, 36, R * 0.024)
    page.circle(cx, cy, spacing)


def _metatron(page, n: int) -> None:
    """Fruit of life plus the chord web between its thirteen centres."""
    cx, cy, R = page.cx, page.cy, page.radius
    spacing = R / 3.15
    centres = [(0.0, 0.0)]
    for i in range(6):
        a = math.pi / 2 + math.pi / 3 * i
        centres.append((spacing * math.cos(a), spacing * math.sin(a)))
    for i in range(6):
        a = math.pi / 2 + math.pi / 3 * i
        centres.append((2 * spacing * math.cos(a), 2 * spacing * math.sin(a)))

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    # Chord web underneath, so the circles read on top of it.
    page.width(W_ACCENT)
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            page.line(cx + centres[i][0], cy + centres[i][1],
                      cx + centres[j][0], cy + centres[j][1])

    page.width(W_DETAIL)
    for dx, dy in centres:
        page.circle(cx + dx, cy + dy, spacing)

    # Guide circles and frame vary across the whole family, so no two pages of
    # this construction come out identical.
    page.width(W_ACCENT)
    for k in range(1, 2 + n):
        guide = spacing * (0.75 + 0.55 * k)
        if guide <= R * 0.93:
            page.circle(cx, cy, guide)

    page.width(W_OUTLINE)
    page.regular_polygon(cx, cy, R * 0.96, 6, rotation_deg=90 + n * 11)


_SOLIDS: dict[str, tuple[list[tuple[float, float, float]], list[tuple[int, int]]]] = {}


def _edges_by_shortest(verts):
    shortest = min(math.dist(verts[i], verts[j])
                   for i in range(len(verts)) for j in range(i + 1, len(verts)))
    return [(i, j) for i in range(len(verts)) for j in range(i + 1, len(verts))
            if abs(math.dist(verts[i], verts[j]) - shortest) < 1e-6]


def _build_solids() -> None:
    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    _SOLIDS["tetrahedron"] = (tetra, [(i, j) for i in range(4) for j in range(i + 1, 4)])

    cube = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    _SOLIDS["cube"] = (cube, _edges_by_shortest(cube))

    octa = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    _SOLIDS["octahedron"] = (octa, _edges_by_shortest(octa))

    ico = []
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            ico += [(0, s1, s2 * PHI), (s1, s2 * PHI, 0), (s2 * PHI, 0, s1)]
    _SOLIDS["icosahedron"] = (ico, _edges_by_shortest(ico))

    dodec = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            dodec += [(0, s1 / PHI, s2 * PHI), (s1 / PHI, s2 * PHI, 0),
                      (s2 * PHI, 0, s1 / PHI)]
    _SOLIDS["dodecahedron"] = (dodec, _edges_by_shortest(dodec))


_build_solids()
_SOLID_ORDER = ["tetrahedron", "cube", "octahedron", "icosahedron", "dodecahedron"]


def _solid(page, n: int) -> None:
    """Platonic-solid wireframe, orthographically projected."""
    cx, cy, R = page.cx, page.cy, page.radius
    verts, edges = _SOLIDS[_SOLID_ORDER[n % len(_SOLID_ORDER)]]

    yaw, pitch = math.radians(26 + n * 21), math.radians(19 + n * 11)

    def project(v):
        x, y, z = v
        x, z = x * math.cos(yaw) - z * math.sin(yaw), x * math.sin(yaw) + z * math.cos(yaw)
        y, z = (y * math.cos(pitch) - z * math.sin(pitch),
                y * math.sin(pitch) + z * math.cos(pitch))
        return x, y

    flat = [project(v) for v in verts]
    extent = max(math.hypot(x, y) for x, y in flat) or 1.0
    scale = R * 0.86 / extent
    pts = [(cx + x * scale, cy + y * scale) for x, y in flat]

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.945)
    page.tick_rim(cx, cy, R * 0.945, R, 72)

    # Spokes to every vertex. A bare tetrahedron is four lines on an empty page;
    # the spokes give the sparse solids enough closed regions to colour.
    page.width(W_ACCENT)
    for x, y in pts:
        page.line(cx, cy, x, y)

    # A half-scale copy inside, so every solid reads as a nested compound.
    page.width(W_ACCENT)
    inner = [(cx + (x - cx) * 0.45, cy + (y - cy) * 0.45) for x, y in pts]
    for i, j in edges:
        page.line(*inner[i], *inner[j])

    page.width(W_DETAIL)
    for i, j in edges:
        page.line(*pts[i], *pts[j])

    page.width(W_ACCENT)
    for x, y in pts:
        page.circle(x, y, R * 0.026)


def _spiral(page, n: int) -> None:
    """Archimedean, golden, Theodorus and phyllotaxis constructions."""
    cx, cy, R = page.cx, page.cy, page.radius
    kind = n % 4

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    if kind == 0:  # Archimedean arms
        page.width(W_DETAIL)
        arms = 3 + n % 3
        for arm in range(arms):
            offset = 2 * math.pi * arm / arms
            pts = []
            for i in range(601):
                t = i / 600 * 6 * math.pi
                r = R * 0.90 * t / (6 * math.pi)
                pts.append((cx + r * math.cos(t + offset), cy + r * math.sin(t + offset)))
            page.polyline(pts)
        page.width(W_ACCENT)
        page.tick_rim(cx, cy, R * 0.90, R, 60)

    elif kind == 1:  # Golden spiral nested in its squares
        page.width(W_DETAIL)
        size = R * 1.05
        x0, y0 = cx - size * 0.55, cy - size * 0.62
        for step in range(8):
            s = size / (PHI ** step)
            quad = step % 4
            if quad == 0:
                x, y = x0, y0
            corners = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
            page.polygon(corners)
            pivot = corners[(quad + 2) % 4]
            page.arc(pivot[0], pivot[1], s, 90 * ((quad + 2) % 4), 90 * ((quad + 2) % 4) + 90)
            # Walk to the next, smaller square inside the current one.
            if quad == 0:
                x, y = x + s - s / PHI, y + s
            elif quad == 1:
                x, y = x - s / PHI, y + s - s / PHI
            elif quad == 2:
                x, y = x, y - s / PHI
            else:
                x, y = x + s, y

    elif kind == 2:  # Theodorus — the spiral of unit right triangles
        page.width(W_DETAIL)
        unit = R * 0.215
        angle = 0.0
        px, py = cx + unit, cy
        page.line(cx, cy, px, py)
        for k in range(1, 20):
            r_prev = unit * math.sqrt(k)
            angle += math.atan2(unit, r_prev)
            r_next = unit * math.sqrt(k + 1)
            nx, ny = cx + r_next * math.cos(angle), cy + r_next * math.sin(angle)
            if r_next > R * 0.94:
                break
            page.line(px, py, nx, ny)
            page.line(cx, cy, nx, ny)
            px, py = nx, ny

    else:  # Phyllotaxis — sunflower packing, no connectors to tangle
        page.width(W_DETAIL)
        count = 200 + (n % 3) * 55
        golden = math.pi * (3 - math.sqrt(5))
        for i in range(1, count):
            r = R * 0.93 * math.sqrt(i / count)
            a = i * golden
            page.circle(cx + r * math.cos(a), cy + r * math.sin(a),
                        R * 0.013 + R * 0.028 * (i / count))


def _yantra(page, n: int) -> None:
    """Interlocking upward and downward triangles inside a lotus frame."""
    cx, cy, R = page.cx, page.cy, page.radius

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)
    gate = R * 0.70
    page.polygon([(cx - gate, cy - gate), (cx + gate, cy - gate),
                  (cx + gate, cy + gate), (cx - gate, cy + gate)])

    # Lotus ring sits inside the gate square, as the traditional layout has it —
    # outside, the petals collide with the square's corners.
    page.width(W_DETAIL)
    page.circle(cx, cy, R * 0.615)
    petals = 14 + n * 3
    for i in range(petals):
        a = 360.0 * i / petals
        page.teardrop_petal(cx + R * 0.475 * math.cos(math.radians(a)),
                            cy + R * 0.475 * math.sin(math.radians(a)),
                            a, R * 0.135, R * 0.045)
    page.circle(cx, cy, R * 0.455)

    layers = 4 + (n % 3)
    for k in range(layers):
        r = R * 0.425 * (1.0 - k * 0.155)
        page.regular_polygon(cx, cy, r, 3, rotation_deg=90 if k % 2 == 0 else 270)

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.070)


def _vesica(page, n: int) -> None:
    """Vesica piscis lenses and the constructions that fall out of them."""
    cx, cy, R = page.cx, page.cy, page.radius
    count = [2, 3, 4, 6, 5][n % 5]
    r = R * 0.52
    half = r * 0.5

    page.width(W_OUTLINE)
    page.circle(cx, cy, R)

    page.width(W_DETAIL)
    if count == 2:
        page.circle(cx - half, cy, r)
        page.circle(cx + half, cy, r)
        page.width(W_ACCENT)
        page.polygon([(cx, cy + r * SQRT3 / 2), (cx - half - r, cy),
                      (cx, cy - r * SQRT3 / 2), (cx + half + r, cy)])
        page.line(cx, cy - r, cx, cy + r)
    else:
        for i in range(count):
            a = 2 * math.pi * i / count + math.pi / 2
            page.circle(cx + half * math.cos(a), cy + half * math.sin(a), r)
        page.width(W_ACCENT)
        page.regular_polygon(cx, cy, half + r, count, rotation_deg=90)

    page.width(W_ACCENT)
    page.circle(cx, cy, R * 0.955)
    page.bead_band(cx, cy, R * 0.905, 24 + (n % 3) * 12, R * 0.022)


_FAMILIES = [_flower, _metatron, _solid, _spiral, _yantra, _vesica]


def draw(page, index: int) -> None:
    _FAMILIES[index % len(_FAMILIES)](page, index // len(_FAMILIES))
