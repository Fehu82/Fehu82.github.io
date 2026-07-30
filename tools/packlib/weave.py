"""Interlaced knotwork with true over-under weave.

Two strands run round a ring as opposed sine waves, so they cross 2k times. At
each crossing one strand is drawn continuously and the other is broken, and
which one is broken alternates — that break is what the eye reads as "under".

Bands are drawn as their two edges, leaving a colorable channel between them.
"""

from __future__ import annotations

import math

TWO_PI = 2.0 * math.pi


def _segments(points: list[tuple[float, float, float]],
              gaps: list[tuple[float, float]]) -> list[list[tuple[float, float]]]:
    """Split a (t, x, y) polyline wherever t falls inside a gap window."""
    runs: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    for t, x, y in points:
        hidden = any(lo <= t <= hi for lo, hi in gaps)
        if hidden:
            if len(current) > 1:
                runs.append(current)
            current = []
        else:
            current.append((x, y))
    if len(current) > 1:
        runs.append(current)
    return runs


def _wrap_windows(centres: list[float], half: float) -> list[tuple[float, float]]:
    """Gap windows around each crossing, duplicated across the 0/2π seam."""
    windows = []
    for c in centres:
        windows.append((c - half, c + half))
        windows.append((c - half + TWO_PI, c + half + TWO_PI))
        windows.append((c - half - TWO_PI, c + half - TWO_PI))
    return windows


def sine_braid(page, cx: float, cy: float, radius: float, amplitude: float,
               lobes: int, band_half_width: float, *, samples_per_lobe: int = 26,
               gap_fraction: float = 0.30, phase: float = 0.0) -> None:
    """One interlaced band ring: two strands weaving over and under each other.

    `lobes` is how many times each strand swings out and back; the strands cross
    2 * lobes times. `gap_fraction` is the break in the under-strand as a share
    of the spacing between crossings, so the weave reads the same at any lobe
    count — a fixed gap in radians looks tight on a busy ring and gaping on a
    sparse one.
    """
    n = max(240, samples_per_lobe * lobes * 2)
    gap = gap_fraction * (math.pi / lobes)

    def strand_points(sign: float, offset: float):
        pts = []
        for i in range(n + 1):
            t = TWO_PI * i / n
            r = radius + sign * amplitude * math.sin(lobes * t + phase)
            # Perpendicular offset for the band edge, in the radial direction.
            rr = r + offset
            pts.append((t, cx + rr * math.cos(t), cy + rr * math.sin(t)))
        return pts

    # Crossings are where the two radii meet: sin(lobes*t + phase) == 0.
    crossings = [(math.pi * k - phase) / lobes for k in range(2 * lobes)]
    crossings = [c % TWO_PI for c in crossings]
    crossings.sort()

    # Alternate which strand is interrupted at successive crossings.
    a_under = _wrap_windows(crossings[0::2], gap)
    b_under = _wrap_windows(crossings[1::2], gap)

    for sign, gaps in ((1.0, a_under), (-1.0, b_under)):
        for offset in (-band_half_width, band_half_width):
            for run in _segments(strand_points(sign, offset), gaps):
                page.polyline(run)


def braid_band(page, cx: float, cy: float, radius: float, lobes: int,
               amplitude: float, band_half_width: float, phase: float = 0.0) -> None:
    """Convenience wrapper matching the medallion band proportions."""
    sine_braid(page, cx, cy, radius, amplitude, lobes, band_half_width,
               gap_fraction=0.32, phase=phase)


def _circle_intersections(c0, r0, c1, r1):
    """The two points where circles (c0, r0) and (c1, r1) meet, or []."""
    (x0, y0), (x1, y1) = c0, c1
    dx, dy = x1 - x0, y1 - y0
    d = math.hypot(dx, dy)
    if d == 0 or d > r0 + r1 or d < abs(r0 - r1):
        return []
    a = (r0 * r0 - r1 * r1 + d * d) / (2 * d)
    h_sq = r0 * r0 - a * a
    if h_sq <= 0:
        return []
    h = math.sqrt(h_sq)
    mx, my = x0 + a * dx / d, y0 + a * dy / d
    ox, oy = -dy * (h / d), dx * (h / d)
    return [(mx + ox, my + oy), (mx - ox, my - oy)]


def circle_with_gaps(page, cx: float, cy: float, r: float,
                     gap_angles: list[float], gap_half: float,
                     steps: int = 220) -> None:
    """A circle broken at the given angles — the breaks read as passing under."""
    windows = _wrap_windows([a % TWO_PI for a in gap_angles], gap_half)
    pts = []
    for i in range(steps + 1):
        t = TWO_PI * i / steps
        pts.append((t, cx + r * math.cos(t), cy + r * math.sin(t)))
    runs = _segments(pts, windows)
    # A circle with no break would otherwise be split at the 0/2π seam only;
    # rejoin the first and last runs so it draws as one closed curve.
    if len(runs) > 1 and not windows:
        runs = [runs[-1] + runs[0]] + runs[1:-1]
    for run in runs:
        page.polyline(run)


def interlaced_ring(page, cx: float, cy: float, ring_r: float, count: int,
                    link_r: float, rotation_deg: float = 0.0,
                    gap_half: float = 0.14) -> None:
    """A closed chain of overlapping circles that genuinely interlock.

    Where two neighbouring links overlap there are two crossing points. Each
    link passes over its neighbour at one and under at the other — break the
    circle at the "under" point and the chain reads as woven rather than as a
    pile of circles.
    """
    centres = []
    for i in range(count):
        a = math.radians(rotation_deg) + TWO_PI * i / count
        centres.append((cx + ring_r * math.cos(a), cy + ring_r * math.sin(a)))

    breaks: list[list[float]] = [[] for _ in range(count)]
    for i in range(count):
        j = (i + 1) % count
        hits = _circle_intersections(centres[i], link_r, centres[j], link_r)
        if len(hits) != 2:
            continue
        # Order the two crossings consistently so the weave alternates.
        p_first, p_second = sorted(hits, key=lambda p: math.atan2(
            p[1] - centres[i][1], p[0] - centres[i][0]))
        # Link i dives under at the first crossing; link j at the second.
        breaks[i].append(math.atan2(p_first[1] - centres[i][1],
                                    p_first[0] - centres[i][0]))
        breaks[j].append(math.atan2(p_second[1] - centres[j][1],
                                    p_second[0] - centres[j][0]))

    for i, (bx, by) in enumerate(centres):
        circle_with_gaps(page, bx, by, link_r, breaks[i], gap_half)


def chain_ring(page, cx: float, cy: float, ring_r: float, link_r: float,
               *, spacing: float = 1.45, rotation_deg: float = 0.0,
               gap_half: float = 0.16) -> int:
    """Interlaced chain sized by its links rather than by a link count.

    Picking the count directly makes band thickness depend on radius, so
    concentric bands end up overlapping each other. Choosing the link radius and
    deriving the count keeps every band inside its own lane. `spacing` is the
    centre-to-centre distance as a multiple of link_r — below 2.0 the links
    overlap, and about 1.45 gives a comfortable interlock.
    """
    step = min(0.999, (spacing * link_r) / (2.0 * ring_r))
    count = max(3, round(math.pi / math.asin(step)))
    interlaced_ring(page, cx, cy, ring_r, count, link_r,
                    rotation_deg=rotation_deg, gap_half=gap_half)
    return count
