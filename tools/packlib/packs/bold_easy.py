"""Bold and Easy — 5 everyday categories x 6 pages.

One large subject per page, extra-thick outlines, almost no interior detail:
the deliberate opposite of the lab's intricate packs. Built for small hands,
shaky hands, and anyone who wants to finish a page in one sitting.
"""

from __future__ import annotations

import math

from ..page import W_ACCENT, W_DETAIL, W_OUTLINE

SLUG = "bold-easy-coloring-pack"
TITLE = "Bold and Easy Coloring Pages - 30 Simple Thick-Line Designs"
PAGES = 30

# Three times the library default — the whole point of the pack.
BOLD = W_OUTLINE * 3.0      # 6.0
BOLD_DETAIL = W_DETAIL * 3.0  # 4.2
BOLD_ACCENT = W_ACCENT * 3.0  # 3.0


def _rounded_rect(page, cx, cy, w, h, r) -> None:
    """A rectangle with rounded corners, as one closed path."""
    r = min(r, w / 2, h / 2)
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    pts = []
    for corner, (ax, ay) in enumerate(((x1 - r, y1 - r), (x0 + r, y1 - r),
                                       (x0 + r, y0 + r), (x1 - r, y0 + r))):
        start = 90 * corner
        for i in range(13):
            a = math.radians(start + 90 * i / 12)
            pts.append((ax + r * math.cos(a), ay + r * math.sin(a)))
    page.polyline(pts, close=True)


# --- animal faces --------------------------------------------------------

def _animal(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    page.width(BOLD)
    kind = n % 6

    if kind == 0:      # cat
        page.circle(cx, cy, R * 0.62)
        for s in (-1, 1):
            page.polyline([(cx + s * R * 0.34, cy + R * 0.52),
                           (cx + s * R * 0.56, cy + R * 0.96),
                           (cx + s * R * 0.62, cy + R * 0.40)])
        for s in (-1, 1):
            page.circle(cx + s * R * 0.24, cy + R * 0.12, R * 0.10)
        page.polyline([(cx - R * 0.09, cy - R * 0.10), (cx + R * 0.09, cy - R * 0.10),
                       (cx, cy - R * 0.22)], close=True)
        page.width(BOLD_DETAIL)
        for s in (-1, 1):
            for k in (-1, 1):
                page.polyline([(cx + s * R * 0.22, cy - R * 0.16 + k * R * 0.12),
                               (cx + s * R * 0.80, cy - R * 0.16 + k * R * 0.20)])

    elif kind == 1:    # dog
        page.ellipse(cx, cy, R * 0.56, R * 0.60)
        for s in (-1, 1):
            page.ellipse(cx + s * R * 0.62, cy + R * 0.10, R * 0.20, R * 0.42)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.22, cy + R * 0.16, R * 0.10)
        page.ellipse(cx, cy - R * 0.24, R * 0.16, R * 0.12)
        page.width(BOLD_DETAIL)
        page.polyline([(cx, cy - R * 0.36), (cx, cy - R * 0.50)])
        page.arc(cx - R * 0.14, cy - R * 0.50, R * 0.14, 250, 360)
        page.arc(cx + R * 0.14, cy - R * 0.50, R * 0.14, 180, 290)

    elif kind == 2:    # bear
        page.circle(cx, cy, R * 0.60)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.50, cy + R * 0.50, R * 0.20)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.22, cy + R * 0.14, R * 0.085)
        page.ellipse(cx, cy - R * 0.22, R * 0.24, R * 0.18)
        page.width(BOLD_DETAIL)
        page.ellipse(cx, cy - R * 0.18, R * 0.09, R * 0.07)

    elif kind == 3:    # frog
        page.ellipse(cx, cy - R * 0.08, R * 0.66, R * 0.50)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.34, cy + R * 0.46, R * 0.22)
            page.circle(cx + s * R * 0.34, cy + R * 0.46, R * 0.08)
        page.width(BOLD_DETAIL)
        page.arc(cx, cy - R * 0.10, R * 0.36, 200, 340)

    elif kind == 4:    # pig
        page.circle(cx, cy, R * 0.58)
        for s in (-1, 1):
            page.polyline([(cx + s * R * 0.32, cy + R * 0.48),
                           (cx + s * R * 0.52, cy + R * 0.84),
                           (cx + s * R * 0.58, cy + R * 0.36)])
        page.ellipse(cx, cy - R * 0.18, R * 0.26, R * 0.20)
        page.width(BOLD_DETAIL)
        for s in (-1, 1):
            page.ellipse(cx + s * R * 0.10, cy - R * 0.18, R * 0.05, R * 0.08)
            page.circle(cx + s * R * 0.26, cy + R * 0.18, R * 0.075)

    else:              # owl
        page.ellipse(cx, cy, R * 0.56, R * 0.68)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.26, cy + R * 0.24, R * 0.22)
            page.circle(cx + s * R * 0.26, cy + R * 0.24, R * 0.085)
        page.polyline([(cx - R * 0.10, cy + R * 0.06), (cx + R * 0.10, cy + R * 0.06),
                       (cx, cy - R * 0.14)], close=True)
        page.width(BOLD_DETAIL)
        for k in range(3):
            page.arc(cx, cy - R * 0.20 - k * R * 0.16, R * 0.34, 200, 340)


# --- food ----------------------------------------------------------------

def _food(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    page.width(BOLD)
    kind = n % 6

    if kind == 0:      # apple
        page.circle(cx, cy - R * 0.10, R * 0.58)
        page.width(BOLD_DETAIL)
        page.polyline([(cx, cy + R * 0.44), (cx + R * 0.04, cy + R * 0.86)])
        # Leaf as two mirrored bulges — an angular quad reads as a flag.
        bx, by = cx + R * 0.05, cy + R * 0.64
        tx, ty = cx + R * 0.44, cy + R * 0.88
        dx, dy = tx - bx, ty - by
        length = math.hypot(dx, dy)
        ux, uy = -dy / length, dx / length
        for sign in (1, -1):
            page.polyline([
                (bx + dx * t + ux * sign * math.sin(math.pi * t) * length * 0.28,
                 by + dy * t + uy * sign * math.sin(math.pi * t) * length * 0.28)
                for t in (i / 16 for i in range(17))
            ])

    elif kind == 1:    # ice cream cone
        page.arc(cx, cy + R * 0.20, R * 0.42, 0, 180)
        page.circle(cx - R * 0.22, cy + R * 0.44, R * 0.26)
        page.circle(cx + R * 0.22, cy + R * 0.44, R * 0.26)
        page.circle(cx, cy + R * 0.66, R * 0.26)
        page.polyline([(cx - R * 0.42, cy + R * 0.20), (cx, cy - R * 0.86),
                       (cx + R * 0.42, cy + R * 0.20)])
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            page.polyline([(cx + k * R * 0.20 - R * 0.10, cy + R * 0.06),
                           (cx + k * R * 0.20 + R * 0.14, cy - R * 0.44)])

    elif kind == 2:    # cupcake
        _rounded_rect(page, cx, cy - R * 0.40, R * 0.90, R * 0.52, R * 0.10)
        page.arc(cx, cy - R * 0.14, R * 0.48, 0, 180)
        page.circle(cx - R * 0.24, cy + R * 0.12, R * 0.24)
        page.circle(cx + R * 0.24, cy + R * 0.12, R * 0.24)
        page.circle(cx, cy + R * 0.36, R * 0.26)
        page.circle(cx, cy + R * 0.72, R * 0.12)
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            page.polyline([(cx + k * R * 0.24, cy - R * 0.64),
                           (cx + k * R * 0.24, cy - R * 0.16)])

    elif kind == 3:    # donut
        page.circle(cx, cy, R * 0.66)
        page.circle(cx, cy, R * 0.22)
        page.width(BOLD_DETAIL)
        for i in range(9):
            a = 2 * math.pi * i / 9
            page.polyline([(cx + R * 0.44 * math.cos(a) - R * 0.07,
                            cy + R * 0.44 * math.sin(a)),
                           (cx + R * 0.44 * math.cos(a) + R * 0.07,
                            cy + R * 0.44 * math.sin(a) + R * 0.09)])

    elif kind == 4:    # pear
        pts = []
        for i in range(73):
            t = 2 * math.pi * i / 72
            rr = R * (0.34 + 0.20 * (1 - math.sin(t)) / 2)
            pts.append((cx + rr * math.cos(t), cy - R * 0.14 + rr * 1.42 * math.sin(t)))
        page.polyline(pts, close=True)
        page.width(BOLD_DETAIL)
        page.polyline([(cx, cy + R * 0.60), (cx, cy + R * 0.90)])

    else:              # mushroom
        page.arc(cx, cy + R * 0.06, R * 0.68, 0, 180)
        page.polyline([(cx - R * 0.68, cy + R * 0.06), (cx + R * 0.68, cy + R * 0.06)])
        _rounded_rect(page, cx, cy - R * 0.42, R * 0.44, R * 0.90, R * 0.16)
        page.width(BOLD_DETAIL)
        for dx, dy, rr in ((-0.34, 0.30, 0.13), (0.10, 0.42, 0.16), (0.40, 0.22, 0.11)):
            page.circle(cx + R * dx, cy + R * dy, R * rr)


# --- vehicles ------------------------------------------------------------

def _vehicle(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    page.width(BOLD)
    kind = n % 6

    if kind == 0:      # car
        _rounded_rect(page, cx, cy - R * 0.10, R * 1.50, R * 0.44, R * 0.12)
        page.polyline([(cx - R * 0.52, cy + R * 0.12), (cx - R * 0.30, cy + R * 0.56),
                       (cx + R * 0.34, cy + R * 0.56), (cx + R * 0.56, cy + R * 0.12)])
        page.width(BOLD_DETAIL)
        page.polyline([(cx + R * 0.02, cy + R * 0.56), (cx + R * 0.02, cy + R * 0.12)])
        page.width(BOLD)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.52, cy - R * 0.40, R * 0.22)

    elif kind == 1:    # bus
        _rounded_rect(page, cx, cy + R * 0.06, R * 1.56, R * 0.94, R * 0.14)
        page.width(BOLD_DETAIL)
        for k in range(3):
            _rounded_rect(page, cx - R * 0.46 + k * R * 0.44, cy + R * 0.28,
                          R * 0.30, R * 0.28, R * 0.05)
        page.width(BOLD)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.52, cy - R * 0.50, R * 0.20)

    elif kind == 2:    # truck
        _rounded_rect(page, cx - R * 0.42, cy + R * 0.10, R * 0.86, R * 0.72, R * 0.08)
        _rounded_rect(page, cx + R * 0.52, cy - R * 0.06, R * 0.60, R * 0.40, R * 0.08)
        page.width(BOLD_DETAIL)
        _rounded_rect(page, cx + R * 0.56, cy + R * 0.10, R * 0.32, R * 0.20, R * 0.04)
        page.width(BOLD)
        for x in (-0.56, 0.10, 0.62):
            page.circle(cx + R * x, cy - R * 0.40, R * 0.19)

    elif kind == 3:    # train engine
        _rounded_rect(page, cx - R * 0.20, cy + R * 0.04, R * 1.20, R * 0.62, R * 0.10)
        _rounded_rect(page, cx + R * 0.56, cy + R * 0.22, R * 0.44, R * 0.98, R * 0.08)
        page.circle(cx - R * 0.52, cy + R * 0.62, R * 0.20)
        page.width(BOLD_DETAIL)
        page.polyline([(cx - R * 0.68, cy + R * 0.82), (cx - R * 0.36, cy + R * 0.82)])
        page.width(BOLD)
        for x in (-0.62, -0.16, 0.30):
            page.circle(cx + R * x, cy - R * 0.44, R * 0.18)

    elif kind == 4:    # boat
        page.polyline([(cx - R * 0.86, cy - R * 0.20), (cx + R * 0.86, cy - R * 0.20),
                       (cx + R * 0.56, cy - R * 0.66), (cx - R * 0.56, cy - R * 0.66)],
                      close=True)
        page.polyline([(cx, cy - R * 0.20), (cx, cy + R * 0.92)])
        page.polyline([(cx + R * 0.06, cy + R * 0.86), (cx + R * 0.66, cy + R * 0.10),
                       (cx + R * 0.06, cy + R * 0.10)], close=True)
        page.polyline([(cx - R * 0.06, cy + R * 0.72), (cx - R * 0.52, cy + R * 0.10),
                       (cx - R * 0.06, cy + R * 0.10)], close=True)
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            page.arc(cx + k * R * 0.56, cy - R * 0.88, R * 0.24, 200, 340)

    else:              # plane
        page.ellipse(cx, cy, R * 0.86, R * 0.24)
        page.polyline([(cx - R * 0.10, cy + R * 0.12), (cx + R * 0.16, cy + R * 0.78),
                       (cx + R * 0.44, cy + R * 0.78), (cx + R * 0.34, cy + R * 0.12)],
                      close=True)
        page.polyline([(cx - R * 0.10, cy - R * 0.12), (cx + R * 0.16, cy - R * 0.78),
                       (cx + R * 0.44, cy - R * 0.78), (cx + R * 0.34, cy - R * 0.12)],
                      close=True)
        page.polyline([(cx - R * 0.86, cy), (cx - R * 0.96, cy + R * 0.44),
                       (cx - R * 0.60, cy + R * 0.14)], close=True)
        page.width(BOLD_DETAIL)
        for k in range(3):
            page.circle(cx + R * (0.30 - k * 0.28), cy + R * 0.02, R * 0.07)


# --- home & garden objects ----------------------------------------------

def _home(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    page.width(BOLD)
    kind = n % 6

    if kind == 0:      # house
        page.polyline([(cx - R * 0.66, cy - R * 0.10), (cx - R * 0.66, cy - R * 0.86),
                       (cx + R * 0.66, cy - R * 0.86), (cx + R * 0.66, cy - R * 0.10)])
        page.polyline([(cx - R * 0.86, cy - R * 0.10), (cx, cy + R * 0.72),
                       (cx + R * 0.86, cy - R * 0.10)], close=True)
        page.width(BOLD_DETAIL)
        _rounded_rect(page, cx, cy - R * 0.52, R * 0.34, R * 0.66, R * 0.04)
        _rounded_rect(page, cx - R * 0.44, cy - R * 0.30, R * 0.26, R * 0.26, R * 0.03)

    elif kind == 1:    # flower pot
        page.polyline([(cx - R * 0.52, cy - R * 0.12), (cx - R * 0.40, cy - R * 0.84),
                       (cx + R * 0.40, cy - R * 0.84), (cx + R * 0.52, cy - R * 0.12)],
                      close=True)
        page.width(BOLD_DETAIL)
        page.polyline([(cx - R * 0.56, cy + R * 0.02), (cx + R * 0.56, cy + R * 0.02)])
        page.width(BOLD)
        page.circle(cx, cy + R * 0.52, R * 0.20)
        for i in range(6):
            a = 2 * math.pi * i / 6 + math.pi / 2
            page.circle(cx + R * 0.36 * math.cos(a), cy + R * 0.52 + R * 0.36 * math.sin(a),
                        R * 0.19)
        page.width(BOLD_DETAIL)
        page.polyline([(cx, cy + R * 0.14), (cx, cy + R * 0.30)])

    elif kind == 2:    # watering can
        _rounded_rect(page, cx - R * 0.10, cy - R * 0.24, R * 0.94, R * 0.78, R * 0.12)
        page.polyline([(cx + R * 0.36, cy - R * 0.06), (cx + R * 0.86, cy + R * 0.44),
                       (cx + R * 0.66, cy + R * 0.56), (cx + R * 0.30, cy + R * 0.08)])
        page.arc(cx - R * 0.20, cy + R * 0.16, R * 0.34, 20, 160)
        page.width(BOLD_DETAIL)
        page.polyline([(cx + R * 0.68, cy + R * 0.50), (cx + R * 0.92, cy + R * 0.62)])

    elif kind == 3:    # teapot
        page.ellipse(cx, cy - R * 0.10, R * 0.56, R * 0.44)
        page.arc(cx + R * 0.72, cy - R * 0.10, R * 0.24, 120, 240)
        page.polyline([(cx - R * 0.52, cy + R * 0.02), (cx - R * 0.90, cy + R * 0.28),
                       (cx - R * 0.86, cy + R * 0.08), (cx - R * 0.50, cy - R * 0.16)])
        page.width(BOLD_DETAIL)
        _rounded_rect(page, cx, cy + R * 0.40, R * 0.30, R * 0.18, R * 0.06)
        page.polyline([(cx - R * 0.56, cy - R * 0.52), (cx + R * 0.56, cy - R * 0.52)])

    elif kind == 4:    # lamp
        page.polyline([(cx - R * 0.50, cy + R * 0.20), (cx - R * 0.32, cy + R * 0.76),
                       (cx + R * 0.32, cy + R * 0.76), (cx + R * 0.50, cy + R * 0.20)],
                      close=True)
        page.polyline([(cx, cy + R * 0.20), (cx, cy - R * 0.62)])
        page.arc(cx, cy - R * 0.62, R * 0.42, 180, 360)
        page.polyline([(cx - R * 0.42, cy - R * 0.62), (cx + R * 0.42, cy - R * 0.62)])
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            page.polyline([(cx + k * R * 0.24, cy + R * 0.30),
                           (cx + k * R * 0.30, cy + R * 0.68)])

    else:              # birdhouse
        _rounded_rect(page, cx, cy - R * 0.26, R * 0.90, R * 0.80, R * 0.06)
        page.polyline([(cx - R * 0.62, cy + R * 0.14), (cx, cy + R * 0.80),
                       (cx + R * 0.62, cy + R * 0.14)], close=True)
        page.circle(cx, cy - R * 0.16, R * 0.20)
        page.width(BOLD_DETAIL)
        page.polyline([(cx, cy - R * 0.40), (cx, cy - R * 0.62)])
        page.polyline([(cx, cy - R * 0.66), (cx, cy - R * 0.98)])


# --- sea & garden creatures ---------------------------------------------

def _creature(page, n: int) -> None:
    cx, cy, R = page.cx, page.cy, page.radius
    page.width(BOLD)
    kind = n % 6

    if kind == 0:      # fish
        page.ellipse(cx - R * 0.10, cy, R * 0.66, R * 0.40)
        page.polyline([(cx + R * 0.52, cy), (cx + R * 0.94, cy + R * 0.36),
                       (cx + R * 0.94, cy - R * 0.36)], close=True)
        page.width(BOLD_DETAIL)
        page.circle(cx - R * 0.44, cy + R * 0.10, R * 0.075)
        page.arc(cx - R * 0.10, cy + R * 0.40, R * 0.26, 200, 340)
        page.polyline([(cx - R * 0.16, cy + R * 0.38), (cx + R * 0.10, cy + R * 0.66),
                       (cx + R * 0.24, cy + R * 0.34)])

    elif kind == 1:    # crab
        page.ellipse(cx, cy, R * 0.62, R * 0.42)
        for s in (-1, 1):
            page.circle(cx + s * R * 0.22, cy + R * 0.16, R * 0.09)
            page.polyline([(cx + s * R * 0.58, cy + R * 0.10),
                           (cx + s * R * 0.74, cy + R * 0.34)])
            page.ellipse(cx + s * R * 0.80, cy + R * 0.44, R * 0.15, R * 0.11)
            for k in range(3):
                page.polyline([(cx + s * R * 0.50, cy - R * 0.16 - k * R * 0.10),
                               (cx + s * R * 0.80, cy - R * 0.34 - k * R * 0.14)])

    elif kind == 2:    # snail
        page.ellipse(cx - R * 0.44, cy - R * 0.34, R * 0.50, R * 0.22)
        pts = []
        for i in range(160):
            t = i / 160 * 4.4 * math.pi
            rr = R * 0.05 + R * 0.041 * t
            pts.append((cx + R * 0.24 + rr * math.cos(t), cy + R * 0.06 + rr * math.sin(t)))
        page.polyline(pts)
        page.width(BOLD_DETAIL)
        for s in (0, 1):
            tip_x = cx - R * (0.74 + 0.09 * s)
            tip_y = cy + R * (0.28 + 0.10 * s)
            page.polyline([(cx - R * 0.70, cy - R * 0.22), (tip_x, tip_y)])
            page.circle(tip_x, tip_y + R * 0.06, R * 0.055)

    elif kind == 3:    # butterfly
        page.polyline([(cx, cy - R * 0.50), (cx, cy + R * 0.46)])
        for s in (-1, 1):
            page.ellipse(cx + s * R * 0.44, cy + R * 0.30, R * 0.42, R * 0.34)
            page.ellipse(cx + s * R * 0.34, cy - R * 0.28, R * 0.32, R * 0.26)
        page.width(BOLD_DETAIL)
        page.circle(cx, cy + R * 0.52, R * 0.09)
        for s in (-1, 1):
            page.polyline([(cx, cy + R * 0.58), (cx + s * R * 0.22, cy + R * 0.88)])
            page.circle(cx + s * R * 0.44, cy + R * 0.30, R * 0.11)

    elif kind == 4:    # turtle
        page.arc(cx, cy - R * 0.16, R * 0.62, 0, 180)
        page.polyline([(cx - R * 0.62, cy - R * 0.16), (cx + R * 0.62, cy - R * 0.16)])
        page.ellipse(cx + R * 0.78, cy - R * 0.06, R * 0.20, R * 0.16)
        for s in (-1, 1):
            page.ellipse(cx + s * R * 0.46, cy - R * 0.34, R * 0.18, R * 0.12)
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            page.polyline([(cx + k * R * 0.26, cy - R * 0.16),
                           (cx + k * R * 0.20, cy + R * 0.36)])
        page.arc(cx, cy - R * 0.16, R * 0.32, 0, 180)

    else:              # bee
        page.ellipse(cx, cy, R * 0.56, R * 0.40)
        page.width(BOLD_DETAIL)
        for k in (-1, 0, 1):
            x = cx + k * R * 0.22
            half = R * 0.40 * math.sqrt(max(0.0, 1 - (k * 0.22 / 0.56) ** 2))
            page.polyline([(x, cy - half), (x, cy + half)])
        page.width(BOLD)
        page.circle(cx - R * 0.66, cy + R * 0.06, R * 0.22)
        for s in (-1, 1):
            page.polyline([(cx - R * 0.72, cy + R * 0.24),
                           (cx - R * 0.86 + s * R * 0.06, cy + R * 0.62)])
        page.ellipse(cx + R * 0.06, cy + R * 0.52, R * 0.34, R * 0.20)
        page.polyline([(cx + R * 0.54, cy), (cx + R * 0.82, cy)])


_FAMILIES = [_animal, _food, _vehicle, _home, _creature]


def draw(page, index: int) -> None:
    _FAMILIES[index % len(_FAMILIES)](page, index // len(_FAMILIES))
