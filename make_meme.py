#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: an original PIL illustration.

Scene: a Leonida-style sunset beach (gradient sky, sun, skyline, palms)
with make.fun's ghost mascot front and centre, holding its magenta coin.
The joke is the thirteen-year wait for GTA 6 — and that make.fun paid
the ghost to wait. Everything is drawn from primitives: no stock art,
no Rockstar assets, no screenshots.

Output: meme.png, 1200x1200, drawn at 2x and downscaled for smoothness.
"""

from math import cos, pi, sin

from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersample factor
W = 1200 * SS
H = 1200 * SS

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (24, 10, 43)          # near-black purple, outlines and silhouettes
GHOST_WHITE = (255, 255, 255)
MAGENTA = (224, 17, 138)    # make.fun coin magenta
MAGENTA_DARK = (166, 10, 102)
SUN = (255, 214, 110)
SAND = (240, 198, 128)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(draw):
    """Vertical sunset gradient: deep purple -> magenta -> orange."""
    stops = [
        (0.00, (43, 16, 85)),
        (0.38, (122, 38, 128)),
        (0.62, (214, 62, 128)),
        (0.80, (255, 122, 61)),
        (1.00, (255, 170, 66)),
    ]
    horizon = int(H * 0.86)
    for y in range(horizon):
        t = y / horizon
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                draw.line([(0, y), (W, y)], fill=lerp(c0, c1, (t - t0) / (t1 - t0)))
                break
    # Sand below the horizon line.
    draw.rectangle([0, horizon, W, H], fill=SAND)
    draw.line([(0, horizon), (W, horizon)], fill=lerp(SAND, INK, 0.25), width=3 * SS)


def draw_sun(draw):
    """A big low sun, centre stage behind the ghost."""
    cx, cy, r = int(W * 0.5), int(H * 0.70), int(150 * SS)
    for ring in range(5, 0, -1):
        glow = lerp((255, 170, 66), SUN, 0.35)
        draw.ellipse([cx - r - ring * 9 * SS, cy - r - ring * 9 * SS,
                      cx + r + ring * 9 * SS, cy + r + ring * 9 * SS],
                     outline=glow, width=4 * SS)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)


def draw_skyline(draw):
    """Simple blocky beach-city silhouette along the horizon."""
    base = int(H * 0.86)
    color = (58, 24, 92)
    # (x fraction, top fraction of skyline height, width fraction)
    towers = [
        (0.00, 0.55, 0.07), (0.08, 0.85, 0.05), (0.14, 0.40, 0.06),
        (0.21, 0.70, 0.045), (0.26, 0.50, 0.07), (0.72, 0.48, 0.06),
        (0.79, 0.78, 0.05), (0.85, 0.42, 0.06), (0.92, 0.62, 0.08),
    ]
    height = 150 * SS
    for xf, tf, wf in towers:
        x0 = int(W * xf)
        x1 = int(W * (xf + wf))
        y0 = base - int(height * tf)
        draw.rectangle([x0, y0, x1, base], fill=color)
        # A few lit windows.
        for wy in range(y0 + 14 * SS, base - 10 * SS, 26 * SS):
            for wx in range(x0 + 10 * SS, x1 - 8 * SS, 22 * SS):
                if (wx // SS + wy // SS) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 7 * SS, wy + 9 * SS],
                                   fill=(255, 205, 105))


def _frond(draw, ox, oy, angle, length, droop, width):
    """One palm frond: a polyline that arcs out and droops down."""
    pts = []
    steps = 24
    for i in range(steps + 1):
        t = i / steps
        x = ox + cos(angle) * length * t
        y = oy + sin(angle) * length * t + droop * t * t
        pts.append((x, y))
    draw.line(pts, fill=INK, width=width, joint="curve")


def draw_palm(draw, base_x, base_y, height, lean, scale=1.0):
    """A palm silhouette: curved trunk plus a crown of fronds."""
    top_x = base_x + lean
    top_y = base_y - height
    trunk = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        x = base_x + lean * t * t
        y = base_y - height * t
        trunk.append((x, y))
    draw.line(trunk, fill=INK, width=int(17 * SS * scale), joint="curve")
    # Coconuts.
    for dx, dy in ((-14, 4), (12, 10), (0, 16)):
        r = 13 * SS * scale
        draw.ellipse([top_x + dx * SS - r, top_y + dy * SS - r,
                      top_x + dx * SS + r, top_y + dy * SS + r], fill=INK)
    fronds = [
        (-2.85, 1.00), (-2.35, 1.05), (-1.80, 1.00), (-1.25, 0.92),
        (-0.70, 0.95), (-0.25, 0.85), (0.15, 0.70), (2.95, 0.80),
    ]
    for angle, lf in fronds:
        _frond(draw, top_x, top_y, angle, int(215 * SS * scale * lf),
               int(120 * SS * scale), int(11 * SS * scale))


def draw_signpost(draw):
    """A small wooden sign on the sand: LEONIDA, thataway."""
    post_x = int(W * 0.135)
    top = int(H * 0.772)
    base = int(H * 0.845)
    draw.rectangle([post_x - 9 * SS, top, post_x + 9 * SS, base],
                   fill=(110, 72, 32))
    board_w, board_h = 300 * SS, 74 * SS
    bx0, by0 = post_x - 26 * SS, top - 6 * SS
    draw.rounded_rectangle([bx0, by0, bx0 + board_w, by0 + board_h],
                           radius=12 * SS, fill=(146, 96, 42),
                           outline=(84, 54, 20), width=5 * SS)
    font = ImageFont.truetype(FONT_BOLD, 44 * SS)
    label = "LEONIDA >"
    tw = draw.textlength(label, font=font)
    draw.text((bx0 + (board_w - tw) / 2, by0 + 11 * SS), label,
              font=font, fill=(255, 236, 190))


def _ghost_outline(cx, top, width, bottom):
    """Polygon of a ghost: domed head, straight sides, scalloped hem."""
    r = width / 2
    dome_cy = top + r
    pts = []
    steps = 40
    for i in range(steps + 1):  # dome, left to right over the top
        a = pi + pi * (i / steps)
        pts.append((cx + r * cos(a), dome_cy + r * sin(a)))
    wave = 26 * SS
    hem_steps = 60
    for i in range(1, hem_steps + 1):  # hem, right to left, three scallops
        t = i / hem_steps
        x = cx + r - width * t
        y = bottom - wave * abs(sin(pi * 3 * t))
        pts.append((x, y))
    return pts


def _scale_about(pts, cx, cy, fx, fy):
    return [(cx + (x - cx) * fx, cy + (y - cy) * fy) for x, y in pts]


def _sparkle(cx, cy, tall, wide):
    """A four-pointed sparkle (the ghost's eye shape)."""
    inner = tall * 0.20
    pts = [
        (cx, cy - tall), (cx + inner, cy - inner), (cx + wide, cy),
        (cx + inner, cy + inner), (cx, cy + tall), (cx - inner, cy + inner),
        (cx - wide, cy), (cx - inner, cy - inner),
    ]
    return pts


def _star(cx, cy, radius):
    """A plain five-pointed star."""
    pts = []
    for i in range(10):
        rr = radius if i % 2 == 0 else radius * 0.45
        a = -pi / 2 + i * pi / 5
        pts.append((cx + rr * cos(a), cy + rr * sin(a)))
    return pts


def draw_ghost(draw):
    """make.fun's ghost: white, thick black outline, sparkle eyes,
    one round little hand holding a magenta coin with a white star."""
    cx = int(W * 0.5)
    top = int(H * 0.295)
    width = int(405 * SS)
    bottom = int(H * 0.735)
    # Soft shadow on the sand.
    draw.ellipse([cx - 250 * SS, bottom + 26 * SS, cx + 250 * SS,
                  bottom + 78 * SS], fill=lerp(SAND, INK, 0.20))
    outline = _ghost_outline(cx, top, width, bottom)
    mid_y = top + (bottom - top) * 0.45
    draw.polygon(outline, fill=INK)
    draw.polygon(_scale_about(outline, cx, mid_y, 0.945, 0.955),
                 fill=GHOST_WHITE)
    # Sparkle eyes.
    eye_y = top + width / 2 + 42 * SS
    for dx in (-74, 74):
        draw.polygon(_sparkle(cx + dx * SS, eye_y, 47 * SS, 18 * SS),
                     fill=INK)
    # A small, patient smile: thirteen years of it.
    draw.arc([cx - 34 * SS, eye_y + 26 * SS, cx + 34 * SS, eye_y + 78 * SS],
             start=15, end=165, fill=INK, width=7 * SS)
    # The coin, then the round little hand over its rim, holding it.
    coin_x, coin_y, coin_r = cx + 238 * SS, bottom - 52 * SS, 90 * SS
    draw.ellipse([coin_x - coin_r, coin_y - coin_r, coin_x + coin_r,
                  coin_y + coin_r], fill=MAGENTA_DARK)
    inner = coin_r - 11 * SS
    draw.ellipse([coin_x - inner, coin_y - inner, coin_x + inner,
                  coin_y + inner], fill=MAGENTA)
    draw.polygon(_star(coin_x, coin_y, 46 * SS), fill=GHOST_WHITE)
    hand_x, hand_y, hand_r = cx + 168 * SS, bottom - 88 * SS, 35 * SS
    draw.ellipse([hand_x - hand_r, hand_y - hand_r, hand_x + hand_r,
                  hand_y + hand_r], fill=GHOST_WHITE, outline=INK,
                 width=8 * SS)


def _fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_BOLD, size)


def _centred(draw, cx, y, text, font, fill, stroke):
    tw = draw.textlength(text, font=font)
    draw.text((cx - tw / 2, y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=INK)


def draw_captions(draw):
    cx = W // 2
    max_w = int(W * 0.92)
    top_font = _fit_font(draw, "13 YEARS WAITING FOR GTA 6…", max_w, 96 * SS)
    _centred(draw, cx, int(H * 0.045), "13 YEARS WAITING", top_font,
             GHOST_WHITE, 10 * SS)
    _centred(draw, cx, int(H * 0.045) + 108 * SS, "FOR GTA 6…", top_font,
             GHOST_WHITE, 10 * SS)
    # A dark caption bar along the bottom, classic meme style.
    bar_y0, bar_y1 = int(H * 0.828), int(H * 0.995)
    draw.rounded_rectangle([int(W * 0.03), bar_y0, int(W * 0.97), bar_y1],
                           radius=26 * SS, fill=INK)
    bot_font = _fit_font(draw, "GOOD THING make.fun", max_w, 80 * SS)
    _centred(draw, cx, bar_y0 + 24 * SS, "GOOD THING make.fun", bot_font,
             GHOST_WHITE, 0)
    _centred(draw, cx, bar_y0 + 24 * SS + 96 * SS, "PAID ME TO WAIT",
             bot_font, SUN, 0)


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_sky(draw)
    draw_sun(draw)
    draw_skyline(draw)
    draw_palm(draw, int(W * 0.055), int(H * 0.86), int(H * 0.46),
              int(60 * SS), 1.0)
    draw_palm(draw, int(W * 0.965), int(H * 0.86), int(H * 0.40),
              int(-52 * SS), 0.85)
    draw_ghost(draw)
    draw_signpost(draw)
    draw_captions(draw)
    img = img.resize((1200, 1200), Image.LANCZOS)
    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
