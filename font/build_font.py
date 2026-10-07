#!/usr/bin/env python3
"""Build Doodlebomb.ttf — spray-scrawled tag digits (and doodles) for dwm.

Glyphs live in Supplementary Private Use Area-B (U+100000..), so no normal font claims
them and dwm/Xft falls back to this font automatically.

  pip install shapely fonttools
  python3 build_font.py          -> Doodlebomb.ttf
"""
import math, random
from shapely.geometry import LineString, Polygon, Point, MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

EM, ASC, DESC = 1000, 860, 140         # glyph box: y from -60 to 800
W = 112                                # marker stroke width (font units)
rng = random.Random(1312)

# ---------- scrawl helpers ---------------------------------------------------
def wobble(pts, amp=14, step=60):
    """Subdivide a polyline and nudge points so it looks hand-sprayed."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.dist((x0, y0), (x1, y1)) // step))
        for i in range(n):
            t = i / n
            out.append((x0 + (x1 - x0) * t + rng.uniform(-amp, amp),
                        y0 + (y1 - y0) * t + rng.uniform(-amp, amp)))
    out.append(pts[-1])
    return out

def stroke(pts, w=W, amp=14, taper=True):
    """A marker stroke: wobbly line, round caps, slightly fattened start."""
    line = LineString(wobble(pts, amp))
    g = line.buffer(w / 2, cap_style=1, join_style=1, quad_segs=6)
    if taper:  # paint blob where the can starts spraying
        g = g.union(Point(line.coords[0]).buffer(w * 0.62, quad_segs=6))
    return g

def drip(x, y, length, w=W * 0.55):
    """Paint drip hanging down from (x, y)."""
    g = LineString([(x, y), (x + rng.uniform(-6, 6), y - length)]).buffer(w / 2, cap_style=1)
    return g.union(Point(x, y - length).buffer(w * 0.72, quad_segs=6))

def blob(poly_pts, amp=10):
    return Polygon(wobble(poly_pts + [poly_pts[0]], amp, 50)).buffer(0)

def circle(cx, cy, r, n=28, amp=10):
    return [(cx + r * math.cos(2 * math.pi * i / n) + rng.uniform(-amp, amp),
             cy + r * math.sin(2 * math.pi * i / n) + rng.uniform(-amp, amp)) for i in range(n)]

def rot(g, deg):
    return affinity.rotate(g, deg, origin=(420, 370))

# ---------- the glyphs -------------------------------------------------------
def g_star():          # scribbled outline star, line overshoots its start
    pts = []
    for i in range(11):
        r = 400 if i % 2 == 0 else 175
        a = math.pi / 2 + i * math.pi / 5
        pts.append((420 + r * math.cos(a), 360 + r * math.sin(a)))
    pts.append((pts[1][0] + 40, pts[1][1] + 10))
    return rot(stroke(pts, W * 0.95), -8)

def g_pentagram():     # one-stroke five point star, like a quick tag
    P = [(420 + 400 * math.cos(math.pi / 2 + k * 4 * math.pi / 5),
          350 + 400 * math.sin(math.pi / 2 + k * 4 * math.pi / 5)) for k in range(6)]
    P[-1] = (P[-1][0] + 45, P[-1][1] - 30)
    return rot(stroke(P, W * 0.9), 6)

def g_skull():
    head = blob(circle(420, 470, 320, 30, 12))
    jaw = blob([(250, 260), (590, 260), (560, 40), (280, 40)], 10)
    sk = head.union(jaw)
    for ex in (300, 540):
        sk = sk.difference(blob(circle(ex, 450, 95, 16, 9)))
    sk = sk.difference(blob([(420, 360), (370, 270), (470, 270)], 4))
    for tx in (335, 420, 505):
        sk = sk.difference(LineString([(tx, 210), (tx, 0)]).buffer(22))
    return rot(sk, -6)

def g_launch():        # filled triangle + double chevron "go" mark
    tri = blob([(20, 760), (20, -40), (540, 360)], 12)
    ch = stroke([(640, 700), (900, 360), (640, 20)], W * 1.1, taper=False)
    return unary_union([tri, ch, drip(140, 0, 90)]).buffer(0)

def g_x():
    a = stroke([(90, 760), (760, 30)], W * 1.25)
    b = stroke([(740, 770), (110, 60)], W * 1.25)
    return unary_union([a, b, drip(520, 330, 300), drip(250, 120, 140)])

def g_spiral():
    pts = []
    for i in range(80):
        t = i / 79 * 2.15 * 2 * math.pi
        r = 40 + 370 * i / 79
        pts.append((420 + r * math.cos(t), 360 + r * math.sin(t)))
    return stroke(pts, W * 1.05, amp=6)

def g_bomb():
    body = blob(circle(360, 300, 300, 30, 10))
    body = body.difference(LineString([(210, 400), (260, 470)]).buffer(28, cap_style=1))  # shine
    neck = blob([(520, 470), (640, 590), (580, 650), (460, 530)], 6)
    fuse = stroke([(610, 620), (660, 700), (740, 690)], W * 0.5, amp=6, taper=False)
    spark = unary_union([LineString([(770, 720), (770 + 120 * math.cos(a), 720 + 120 * math.sin(a))])
                         .buffer(26, cap_style=1) for a in (0.3, 1.5, 2.6, 4.0, 5.2)])
    return unary_union([body, neck, fuse, spark])

def g_bolt():
    return rot(blob([(470, 800), (130, 330), (380, 330), (250, -60),
                     (690, 450), (430, 450), (600, 800)], 10), 4)

def g_target():
    ring = blob(circle(420, 360, 360, 32, 9)).difference(blob(circle(420, 360, 250, 32, 9)))
    cross = unary_union([stroke([(420, 820), (420, -100)], W * 0.8, taper=False),
                         stroke([(-40, 360), (880, 360)], W * 0.8, taper=False)])
    dot = Point(420, 360).buffer(95)
    return unary_union([ring, cross.difference(Point(420, 360).buffer(150)), dot])

GLYPHS = [g_star, g_pentagram, g_skull, g_launch, g_x, g_spiral, g_bomb, g_bolt, g_target]

# ---------- scrawled digits 1-9 (the tag labels) -----------------------------
DW = W * 1.12                           # digits get a fatter marker

def arc(cx, cy, r, a0, a1, n=18, ry=None):
    ry = ry or r
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def tagged(*strokes, drips=(), tilt=0):
    """Union marker strokes, hang paint drips, tilt the whole digit a bit."""
    g = unary_union([stroke(p, DW, amp=12) for p in strokes] +
                    [drip(x, y, l) for x, y, l in drips])
    g = affinity.skew(g, xs=11, origin=(300, 0))      # forward lean, like a fast tag
    return affinity.rotate(g, tilt, origin=(300, 380))

def d1(): return tagged([(150, 620), (320, 790), (320, 10)], [(170, 10), (470, 10)],
                        drips=[(320, 10, 120)], tilt=-4)
def d2(): return tagged(arc(300, 570, 210, 165, -15) + [(90, 20), (530, 20)],
                        drips=[(470, 20, 90)], tilt=5)
def d3(): return tagged(arc(285, 600, 190, 155, -90) + arc(285, 215, 215, 90, -155),
                        tilt=-6)
def d4(): return tagged([(420, 0), (420, 790), (60, 260), (570, 260)],
                        drips=[(420, 0, 130)], tilt=4)
def d5(): return tagged([(510, 780), (150, 780), (115, 440)] + arc(300, 245, 230, 135, -155),
                        tilt=-3)
def d6(): return tagged([(470, 770), (300, 610), (150, 420)] + arc(300, 230, 200, 180, -180),
                        drips=[(250, 30, 80)], tilt=6)
def d7(): return tagged([(70, 780), (530, 780), (230, -10)], [(170, 380), (450, 380)],
                        drips=[(230, -10, 110)], tilt=-5)
def d8(): return tagged(arc(300, 590, 170, -90, 270, 22, 175),
                        arc(300, 215, 215, 90, 450, 24, 210), tilt=3)
def d9(): return tagged(arc(300, 570, 200, 0, 360, 24) + [(480, 420), (420, 180), (320, -10)],
                        drips=[(320, -10, 100)], tilt=-6)

DIGITS = [d1, d2, d3, d4, d5, d6, d7, d8, d9]

# ---------- font assembly ----------------------------------------------------
def fit(g):
    """Scale/translate into the box x 40..ADV-40, y -40..780."""
    minx, miny, maxx, maxy = g.bounds
    s = min(820 / (maxy - miny), 820 / (maxx - minx))
    g = affinity.scale(g, s, s, origin=(minx, miny))
    return affinity.translate(g, 40 - g.bounds[0], -40 - g.bounds[1])

def draw(geom, pen):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for p in polys:
        p = orient(p.simplify(3), sign=-1.0)   # TrueType: outer clockwise
        for ring in [p.exterior, *p.interiors]:
            c = [(round(x), round(y)) for x, y in ring.coords[:-1]]
            pen.moveTo(c[0])
            for q in c[1:]:
                pen.lineTo(q)
            pen.closePath()

def build(path="Doodlebomb.ttf"):
    # U+100000-100008: digits 1-9 (tags)   U+100010-100018: doodles (status icons, prompt)
    # Plane-16 private use: no common font (incl. Nerd Fonts) claims it, so fallback always lands here
    sets = [("num", DIGITS, 0x100000), ("doodle", GLYPHS, 0x100010)]
    names, cmap = [".notdef", "space"], {0x20: "space"}
    for pre, fns, base in sets:
        for i in range(len(fns)):
            names.append(f"{pre}{i+1}"); cmap[base + i] = f"{pre}{i+1}"
    fb = FontBuilder(EM, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap(cmap)
    glyphs, metrics = {}, {}
    for n in (".notdef", "space"):
        glyphs[n] = TTGlyphPen(None).glyph(); metrics[n] = (500, 0)
    for pre, fns, _ in sets:
        for i, fn in enumerate(fns):
            g = fit(fn().buffer(0))
            pen = TTGlyphPen(None); draw(g, pen)
            glyphs[f"{pre}{i+1}"] = pen.glyph()
            metrics[f"{pre}{i+1}"] = (int(g.bounds[2]) + 60, 40)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASC, descent=-DESC)
    fb.setupNameTable({"familyName": "Doodlebomb", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=ASC, sTypoDescender=-DESC, usWinAscent=ASC, usWinDescent=DESC)
    fb.setupPost()
    fb.save(path)
    print("wrote", path)

if __name__ == "__main__":
    build()
