"""Build the gta6-meme-x-01 replacement meme: a Leonida rental-car return
receipt that turns the thirteen-year wait for GTA 6 into itemised charges,
paid in full by the driver's AI agent with its make.fun bounty payout.

Drawn from scratch with PIL; fully deterministic (no randomness, no
external assets). Run:  python3 make_receipt.py   ->  writes meme.png
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1440
PAPER = (251, 250, 246)
INK = (26, 26, 46)
GREY = (110, 110, 125)
FAINT = (196, 194, 205)
RED = (192, 39, 45)
NAVY = (20, 20, 51)
MAGENTA = (214, 22, 132)
MAGENTA_DARK = (166, 12, 100)
GOLD = (255, 205, 84)
MINT = (126, 240, 160)
BAND_TEXT = (238, 238, 250)
BAND_SUB = (198, 198, 228)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centred(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def dashed_rule(draw, y, x0=72, x1=W - 72):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + 14, x1), y)], fill=GREY, width=2)
        x += 24


def dotted_leader(draw, x0, x1, y_base):
    x = x0
    while x < x1:
        draw.ellipse([x, y_base - 3, x + 4, y_base + 1], fill=GREY)
        x += 14


def sparkle(cx, cy, r):
    """A four-pointed sparkle: long points, pinched waist."""
    pts = []
    waist = r * 0.18
    for k in range(8):
        ang = math.pi / 2 * (k // 2) + (math.pi / 4 if k % 2 else 0)
        rad = r if k % 2 == 0 else waist * 2.2
        # alternate: cardinal points long, diagonals pinched to the waist
        if k % 2 == 0:
            ang = math.pi / 2 * (k // 2)
            rad = r
        else:
            ang = math.pi / 2 * (k // 2) + math.pi / 4
            rad = waist
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    return pts


def star(cx, cy, r):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def draw_ghost(size):
    """make.fun's ghost, drawn fresh at `size` px tall on transparency:
    white body, thick dark outline, wavy hem, two sparkle eyes, a smile,
    and a round little hand holding a magenta coin with a white star."""
    s = 4  # supersample
    gw, gh = int(size * 0.82), size
    layer = Image.new("RGBA", (gw * s, gh * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = gw * s / 2
    top = 6 * s
    hem = gh * s - 10 * s
    half = gw * s * 0.40
    outline = max(3, int(size * 0.028)) * s

    body = []
    steps = 60
    for i in range(steps + 1):  # dome, left to right over the top
        ang = math.pi - math.pi * i / steps
        body.append((cx + half * math.cos(ang), top + half * (1 - math.sin(ang)) * 0 + (top + half) - half * math.sin(ang)))
    body.append((cx + half, hem))
    waves = 5
    for i in range(1, waves * 2):  # wavy hem, right to left
        x = cx + half - (2 * half) * i / (waves * 2)
        y = hem - (size * 0.045 * s) * (1 if i % 2 else 0)
        body.append((x, y))
    body.append((cx - half, hem))
    d.polygon(body, fill=(255, 255, 255, 255))
    d.line(body + [body[0]], fill=INK + (255,), width=outline, joint="curve")

    eye_y = top + half + size * 0.10 * s
    for ex in (cx - half * 0.42, cx + half * 0.42):
        d.polygon(sparkle(ex, eye_y, size * 0.085 * s), fill=INK + (255,))
    d.arc([cx - size * 0.075 * s, eye_y + size * 0.05 * s,
           cx + size * 0.075 * s, eye_y + size * 0.17 * s],
          start=15, end=165, fill=INK + (255,), width=max(2, outline // 2))

    coin_r = size * 0.21 * s
    coin_c = (cx + half * 0.98, hem - size * 0.10 * s)
    hand_r = size * 0.075 * s
    hand_c = (coin_c[0] - coin_r * 0.82, coin_c[1] - coin_r * 0.55)
    d.ellipse([hand_c[0] - hand_r, hand_c[1] - hand_r,
               hand_c[0] + hand_r, hand_c[1] + hand_r],
              fill=(255, 255, 255, 255), outline=INK + (255,), width=outline // 2)
    d.ellipse([coin_c[0] - coin_r, coin_c[1] - coin_r,
               coin_c[0] + coin_r, coin_c[1] + coin_r],
              fill=MAGENTA + (255,), outline=MAGENTA_DARK + (255,), width=outline // 2)
    d.polygon(star(coin_c[0], coin_c[1], coin_r * 0.58), fill=(255, 255, 255, 255))

    return layer.resize((gw, gh), Image.LANCZOS)


def draw_stamp(base, text):
    """A rotated red '13 YEARS LATE' rubber stamp over the fields."""
    stamp = Image.new("RGBA", (560, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp)
    d.rounded_rectangle([6, 6, 554, 144], radius=18,
                        outline=RED + (215,), width=7)
    d.rounded_rectangle([20, 20, 540, 130], radius=12,
                        outline=RED + (215,), width=3)
    f = font(SANS_B, 62)
    w = d.textlength(text, font=f)
    d.text(((560 - w) / 2, 40), text, font=f, fill=RED + (225,))
    stamp = stamp.rotate(11, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(stamp, (575, 322))


def main():
    img = Image.new("RGB", (W, H), PAPER).convert("RGBA")
    d = ImageDraw.Draw(img)

    # document frame: one sheet of paper, double-ruled border
    d.rectangle([26, 26, W - 26, H - 26], outline=INK, width=3)
    d.rectangle([40, 40, W - 40, H - 40], outline=FAINT, width=2)

    # --- letterhead -----------------------------------------------------
    centred(d, 74, "LEONIDA RENTALS", font(SANS_B, 86), INK)
    centred(d, 178, "VICE CITY INT'L AIRPORT · LEONIDA", font(MONO, 33), GREY)
    centred(d, 228, "— RENTAL RETURN RECEIPT —", font(MONO_B, 38), INK)
    centred(d, 282, "RECEIPT NO. 0002013 · COUNTER 6 · CLERK: L. KEYS",
            font(MONO, 27), GREY)
    dashed_rule(d, 336)

    # --- the rental itself ----------------------------------------------
    f_field = font(MONO, 35)
    f_label = font(MONO_B, 35)
    rows = [
        ("PICKED UP:", "LOS SANTOS — SEP 17, 2013"),
        ("RETURNED:", "VICE CITY — NOV 19, 2026"),
        ("KEPT FOR:", "4,745 DAYS"),
    ]
    y = 362
    for label, value in rows:
        d.text((72, y), label, font=f_label, fill=INK)
        d.text((330, y), value, font=f_field, fill=INK)
        y += 54
    draw_stamp(img, "13 YEARS LATE")
    d = ImageDraw.Draw(img)
    dashed_rule(d, 548)

    # --- itemised charges: the wait, converted into arithmetic ----------
    centred(d, 574, "CHARGES", font(MONO_B, 38), INK)
    items = [
        ("One-way drop fee (Los Santos → Vice City)", 313),
        ("Late fee — 4,745 days @ trailer rates", 1300),
        ('Promised back "Fall 2025" — rescheduled', 26),
        ('Promised back "May 2026" — rescheduled again', 26),
        ("Unlisted drivers: Jason & Lucia", 137),
        ("Cleaning: alligator on the back seat", 224),
    ]
    total = sum(amount for _, amount in items)
    assert total == 2026, f"the joke only works at $2,026 — got {total}"

    f_item = font(MONO, 33)
    f_amt = font(MONO, 33)
    y = 640
    for label, amount in items:
        amt = f"${amount:,}.00"
        amt_w = d.textlength(amt, font=f_amt)
        d.text((72, y), label, font=f_item, fill=INK)
        label_w = d.textlength(label, font=f_item)
        dotted_leader(d, 72 + label_w + 16, W - 72 - amt_w - 16, y + 30)
        d.text((W - 72 - amt_w, y), amt, font=f_amt, fill=INK)
        y += 57

    dashed_rule(d, 998)
    f_total = font(MONO_B, 48)
    d.text((72, 1022), "TOTAL DUE", font=f_total, fill=INK)
    tot = f"${total:,}.00"
    d.text((W - 72 - d.textlength(tot, font=f_total), 1022), tot,
           font=f_total, fill=INK)

    # --- payment band: the agent pays ------------------------------------
    band = [56, 1100, W - 56, 1318]
    d.rounded_rectangle(band, radius=26, fill=NAVY)
    disc_r = 100
    disc_c = (band[0] + 128, (band[1] + band[3]) // 2)
    d.ellipse([disc_c[0] - disc_r, disc_c[1] - disc_r,
               disc_c[0] + disc_r, disc_c[1] + disc_r], fill=MAGENTA)
    ghost = draw_ghost(204)
    img.paste(ghost, (disc_c[0] - ghost.width // 2 + 6,
                      disc_c[1] - ghost.height // 2), ghost)
    d = ImageDraw.Draw(img)

    tx = band[0] + 262
    d.text((tx, band[1] + 28), "PAID BY MY AI AGENT",
           font=font(SANS_B, 53), fill=BAND_TEXT)
    d.text((tx, band[1] + 98), "Bounty payout it earned on make.fun",
           font=font(SANS, 31), fill=BAND_SUB)
    f_money = font(MONO_B, 33)
    credit = "+$2,026.00 CREDIT"
    d.text((tx, band[1] + 148), credit, font=f_money, fill=MINT)
    credit_w = d.textlength(credit, font=f_money)
    d.text((tx + credit_w + 34, band[1] + 148), "REMAINING DUE: $0.00",
           font=f_money, fill=GOLD)

    # --- small print -------------------------------------------------------
    centred(d, 1334, "Thank you for waiting. All thirteen years of it.",
            font(MONO, 24), GREY)
    centred(d, 1366, "LEONIDA RENTALS · NO REFUNDS ON YOUTH",
            font(MONO, 24), GREY)

    out = img.convert("RGB")
    out.save("meme.png", optimize=True)
    print("wrote meme.png", out.size)


if __name__ == "__main__":
    main()
