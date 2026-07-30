"""Page setup: US Letter, print-safe margins, black-on-white line art only."""

from __future__ import annotations

import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas

LETTER_W, LETTER_H = letter  # 612 x 792 pt

# Home printers lose roughly a quarter inch on every edge. Keeping art inside
# this frame means nothing important is ever clipped.
MARGIN = 42.0

# Default stroke weights. The bold-easy pack multiplies these by 3.
W_OUTLINE = 2.0
W_DETAIL = 1.4
W_ACCENT = 1.0


class Page:
    """One drawable page. Wraps a reportlab canvas with centred coordinates."""

    def __init__(self, canvas: rl_canvas.Canvas):
        self.c = canvas
        self.cx = LETTER_W / 2.0
        self.cy = LETTER_H / 2.0
        self.c.setStrokeColorRGB(0, 0, 0)
        self.c.setLineCap(1)   # round caps — no ragged corners when printed
        self.c.setLineJoin(1)

    # ---- frame -----------------------------------------------------------

    @property
    def safe(self) -> tuple[float, float, float, float]:
        """(x0, y0, x1, y1) of the print-safe area."""
        return (MARGIN, MARGIN, LETTER_W - MARGIN, LETTER_H - MARGIN)

    @property
    def radius(self) -> float:
        """Largest radius that fits the safe frame from centre."""
        return min(LETTER_W, LETTER_H) / 2.0 - MARGIN

    def width(self, w: float) -> None:
        self.c.setLineWidth(w)

    # ---- primitives ------------------------------------------------------

    def line(self, x1, y1, x2, y2) -> None:
        self.c.line(x1, y1, x2, y2)

    def circle(self, cx, cy, r) -> None:
        if r > 0.15:
            self.c.circle(cx, cy, r, stroke=1, fill=0)

    def ellipse(self, cx, cy, rx, ry) -> None:
        if rx > 0.15 and ry > 0.15:
            self.c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=1, fill=0)

    def arc(self, cx, cy, r, start_deg, end_deg, segments: int = 0) -> None:
        """Circular arc as a polyline — reliable across viewers."""
        if r <= 0.15:
            return
        sweep = abs(end_deg - start_deg)
        n = segments or max(6, int(sweep / 4.0))
        pts = []
        for i in range(n + 1):
            a = math.radians(start_deg + (end_deg - start_deg) * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.polyline(pts)

    def polyline(self, points, close: bool = False) -> None:
        pts = [p for p in points]
        if len(pts) < 2:
            return
        path = self.c.beginPath()
        path.moveTo(*pts[0])
        for p in pts[1:]:
            path.lineTo(*p)
        if close:
            path.close()
        self.c.drawPath(path, stroke=1, fill=0)

    def polygon(self, points) -> None:
        self.polyline(points, close=True)

    # ---- composite shapes ------------------------------------------------

    def regular_polygon(self, cx, cy, r, sides, rotation_deg=0.0) -> None:
        self.polygon(self.ngon_points(cx, cy, r, sides, rotation_deg))

    @staticmethod
    def ngon_points(cx, cy, r, sides, rotation_deg=0.0):
        return [
            (
                cx + r * math.cos(math.radians(rotation_deg) + 2 * math.pi * i / sides),
                cy + r * math.sin(math.radians(rotation_deg) + 2 * math.pi * i / sides),
            )
            for i in range(sides)
        ]

    def star_polygon(self, cx, cy, r, points, step, rotation_deg=0.0) -> None:
        """A {p/q} star polygon — the classic compass-drawn star."""
        if math.gcd(points, step) != 1:
            # Degenerate: draw each closed orbit separately so nothing is lost.
            for offset in range(math.gcd(points, step)):
                verts = []
                i = offset
                for _ in range(points // math.gcd(points, step)):
                    a = math.radians(rotation_deg) + 2 * math.pi * i / points
                    verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
                    i = (i + step) % points
                self.polygon(verts)
            return
        verts = []
        i = 0
        for _ in range(points):
            a = math.radians(rotation_deg) + 2 * math.pi * i / points
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            i = (i + step) % points
        self.polygon(verts)

    def ring_of(self, cx, cy, r_ring, count, rotation_deg, draw):
        """Call draw(x, y, angle_deg) at `count` points around a ring."""
        for i in range(count):
            a = math.radians(rotation_deg) + 2 * math.pi * i / count
            draw(cx + r_ring * math.cos(a), cy + r_ring * math.sin(a), math.degrees(a))

    def bead_band(self, cx, cy, r_ring, count, bead_r, rotation_deg=0.0) -> None:
        self.ring_of(cx, cy, r_ring, count, rotation_deg,
                     lambda x, y, a: self.circle(x, y, bead_r))

    def petal_ring(self, cx, cy, r_ring, count, petal_r, rotation_deg=0.0) -> None:
        """Seed-of-life style overlapping circles."""
        self.ring_of(cx, cy, r_ring, count, rotation_deg,
                     lambda x, y, a: self.circle(x, y, petal_r))

    def tick_rim(self, cx, cy, r_in, r_out, count, rotation_deg=0.0) -> None:
        def tick(x, y, a):
            ar = math.radians(a)
            self.line(cx + r_in * math.cos(ar), cy + r_in * math.sin(ar),
                      cx + r_out * math.cos(ar), cy + r_out * math.sin(ar))
        self.ring_of(cx, cy, 1.0, count, rotation_deg, tick)

    def teardrop_petal(self, cx, cy, angle_deg, length, half_width) -> None:
        """A pointed petal aimed outward from (cx, cy)."""
        a = math.radians(angle_deg)
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux
        tip = (cx + ux * length, cy + uy * length)
        left = (cx + ux * length * 0.42 + px * half_width,
                cy + uy * length * 0.42 + py * half_width)
        right = (cx + ux * length * 0.42 - px * half_width,
                 cy + uy * length * 0.42 - py * half_width)
        self.polyline([(cx, cy), left, tip], close=False)
        self.polyline([(cx, cy), right, tip], close=False)


def new_canvas(path: str, title: str) -> rl_canvas.Canvas:
    c = rl_canvas.Canvas(path, pagesize=letter)
    c.setTitle(title)
    c.setAuthor("Fehu Lab")
    c.setSubject("Printable coloring pages — black line art on white")
    return c
