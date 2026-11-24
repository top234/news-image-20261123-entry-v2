#!/usr/bin/env python3
"""news-image-20261123 v2 — 'The World in One Day', drawn from scratch with PIL.
Deterministic: no random, no clock, no network. Output: 1024x1024 PNG.
All facts from FACTS.md only. Exclusions honoured: COP31 COLLAPSED (no deal),
Peru M6.8 (GFZ, never M6.9), Shenzhen declaration only, no Monday US closes,
no casualty numbers beyond the file."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 248, 238)
INK = (22, 22, 22)
RED = (185, 18, 28)
RED_D = (140, 10, 20)
NAVY = (15, 32, 51)
GOLD = (176, 132, 40)
GREY = (90, 86, 78)
LINE = (60, 55, 48)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill, leading=None):
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    tmp = Image.new("RGB", (1, h))
    px = tmp.load()
    for i in range(h):
        t = i / (h - 1)
        px[0, i] = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
    img.paste(tmp.resize((x1 - x0, h)), (x0, y0))


# ---------------------------------------------------------------- heroes
def hero_cop31(d, x, y, w, h):
    """Empty COP31 negotiation hall at dawn: big windows, orange dawn sky,
    long rows of desks with flags, scattered papers, empty chairs."""
    vgrad_box = (x, y, x + w, y + h)
    vgrad(d._image, vgrad_box, (255, 176, 102), (255, 226, 170))
    # sun glow
    d.ellipse([x + w * 0.62, y + h * 0.08, x + w * 0.92, y + h * 0.55],
              fill=(255, 214, 130))
    d.ellipse([x + w * 0.68, y + h * 0.16, x + w * 0.86, y + h * 0.44],
              fill=(255, 240, 190))
    # window frames (dark mullions)
    for i in range(5):
        wx = x + i * w // 4
        d.rectangle([wx - 3, y, wx + 3, y + int(h * 0.62)], fill=(70, 45, 30))
    d.rectangle([x, y + int(h * 0.60), x + w, y + int(h * 0.63)], fill=(70, 45, 30))
    # far wall + floor
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(122, 88, 58))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + int(h * 0.66)),
               (x, y + int(h * 0.66))], fill=(96, 66, 42))
    # three rows of long desks, receding (all inside the box)
    for r, (ry, rw, dh) in enumerate([(0.60, 0.86, 10), (0.70, 0.94, 12),
                                      (0.80, 1.0, 14)]):
        cx = x + w // 2
        dw = int(w * rw)
        d.rectangle([cx - dw // 2, y + int(h * ry), cx + dw // 2,
                     y + int(h * ry) + dh], fill=(58, 38, 24))
        d.rectangle([cx - dw // 2, y + int(h * ry), cx + dw // 2,
                     y + int(h * ry) + 3], fill=(214, 178, 120))
        # flags along the desk
        n = 9 - r
        for i in range(n):
            fx = cx - dw // 2 + 12 + i * (dw - 24) // max(1, n - 1)
            cols = [(185, 18, 28), (20, 60, 140), (20, 120, 60), (240, 200, 40),
                    (255, 255, 255), (120, 40, 140), (0, 120, 160),
                    (200, 90, 20), (40, 40, 40)]
            d.line([fx, y + int(h * ry) - 16, fx, y + int(h * ry)],
                   fill=(40, 26, 16), width=1)
            d.polygon([(fx, y + int(h * ry) - 16), (fx + 11, y + int(h * ry) - 13),
                       (fx, y + int(h * ry) - 10)], fill=cols[i % len(cols)])
        # empty chairs
        for i in range(6):
            chx = cx - dw // 2 + 18 + i * (dw - 36) // 5
            d.rectangle([chx - 7, y + int(h * ry) + dh + 1, chx + 7,
                         y + int(h * ry) + dh + 6], fill=(40, 26, 16))
    # scattered papers on the floor
    for (px, py, pw) in [(0.10, 0.74, 12), (0.24, 0.86, 10), (0.68, 0.76, 12),
                         (0.82, 0.88, 10), (0.45, 0.90, 11), (0.55, 0.82, 9)]:
        d.polygon([(x + int(w * px), y + int(h * py)),
                   (x + int(w * px) + pw, y + int(h * py) - 3),
                   (x + int(w * px) + pw + 3, y + int(h * py) + 4),
                   (x + int(w * px) + 2, y + int(h * py) + 6)],
                  fill=(250, 246, 232), outline=(150, 140, 120))


def hero_sparta(d, x, y, w, h):
    """Sparta II ablaze on a night sea, red tug Murman alongside, smoke column."""
    vgrad(d._image, (x, y, x + w, y + h), (8, 18, 38), (28, 52, 84))
    # moon + stars
    d.ellipse([x + int(w * 0.82), y + 8, x + int(w * 0.90), y + 24],
              fill=(235, 230, 200))
    for (sx, sy) in [(0.08, 0.10), (0.22, 0.06), (0.45, 0.12), (0.60, 0.05),
                     (0.95, 0.18), (0.30, 0.18)]:
        d.ellipse([x + int(w * sx), y + int(h * sy), x + int(w * sx) + 2,
                   y + int(h * sy) + 2], fill=(220, 220, 200))
    # smoke column
    for i, (sx, sy, sr) in enumerate([(0.52, 0.06, 26), (0.50, 0.16, 32),
                                      (0.55, 0.28, 30), (0.48, 0.40, 26)]):
        d.ellipse([x + int(w * sx) - sr, y + int(h * sy) - sr // 2,
                   x + int(w * sx) + sr, y + int(h * sy) + sr // 2],
                  fill=(70 - i * 6, 70 - i * 6, 78 - i * 6))
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(10, 28, 52))
    for i in range(7):
        wy = y + int(h * (0.66 + i * 0.05))
        d.arc([x - 20 + i * 8, wy - 6, x + w // 3 + i * 30, wy + 8],
              200, 340, fill=(60, 110, 160), width=2)
    # fire glow on water
    d.polygon([(x + int(w * 0.42), y + int(h * 0.66)),
               (x + int(w * 0.62), y + int(h * 0.66)),
               (x + int(w * 0.70), y + h), (x + int(w * 0.34), y + h)],
              fill=(150, 70, 20))
    # tanker hull (dark, listing slightly)
    d.polygon([(x + int(w * 0.06), y + int(h * 0.52)),
               (x + int(w * 0.78), y + int(h * 0.50)),
               (x + int(w * 0.74), y + int(h * 0.66)),
               (x + int(w * 0.10), y + int(h * 0.68))], fill=(18, 18, 22))
    d.polygon([(x + int(w * 0.06), y + int(h * 0.52)),
               (x + int(w * 0.78), y + int(h * 0.50)),
               (x + int(w * 0.78), y + int(h * 0.54)),
               (x + int(w * 0.06), y + int(h * 0.56))], fill=(120, 30, 22))
    # containers
    for i in range(4):
        cx0 = x + int(w * (0.12 + i * 0.13))
        d.rectangle([cx0, y + int(h * 0.40), cx0 + 34, y + int(h * 0.50)],
                    fill=[(40, 90, 130), (150, 60, 40), (60, 110, 70),
                          (170, 130, 40)][i], outline=(10, 10, 14))
    # bridge tower
    d.rectangle([x + int(w * 0.66), y + int(h * 0.34), x + int(w * 0.76),
                 y + int(h * 0.50)], fill=(200, 200, 190))
    d.rectangle([x + int(w * 0.67), y + int(h * 0.37), x + int(w * 0.75),
                 y + int(h * 0.42)], fill=(255, 200, 80))
    # flames
    for (fx, fy, fs) in [(0.20, 0.42, 26), (0.32, 0.40, 32), (0.45, 0.42, 28),
                         (0.58, 0.44, 22), (0.70, 0.46, 18)]:
        d.polygon([(x + int(w * fx) - fs // 2, y + int(h * fy)),
                   (x + int(w * fx) - fs // 4, y + int(h * fy) - fs),
                   (x + int(w * fx), y + int(h * fy) - fs * 3 // 2),
                   (x + int(w * fx) + fs // 4, y + int(h * fy) - fs),
                   (x + int(w * fx) + fs // 2, y + int(h * fy))],
                  fill=(255, 140, 20))
        d.polygon([(x + int(w * fx) - fs // 4, y + int(h * fy)),
                   (x + int(w * fx), y + int(h * fy) - fs),
                   (x + int(w * fx) + fs // 4, y + int(h * fy))],
                  fill=(255, 220, 80))
    # red tug Murman alongside, small
    tx, ty = x + int(w * 0.80), y + int(h * 0.58)
    d.polygon([(tx, ty), (tx + 52, ty - 4), (tx + 48, ty + 12), (tx + 4, ty + 14)],
              fill=(185, 18, 28))
    d.rectangle([tx + 12, ty - 14, tx + 34, ty], fill=(240, 240, 230))
    d.rectangle([tx + 16, ty - 22, tx + 28, ty - 14], fill=(40, 40, 44))
    d.line([tx + 8, ty + 6, tx - 14, ty - 2], fill=(220, 200, 160), width=2)


def hero_wallst(d, x, y, w, h):
    """Wall Street: plunging red chart on a dark grid, big red arrow, VIX gauge."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 30))
    for i in range(1, 6):
        gy = y + i * h // 6
        d.line([x, gy, x + w, gy], fill=(38, 52, 72), width=1)
    for i in range(1, 7):
        gx = x + i * w // 7
        d.line([gx, y, gx, y + h], fill=(30, 42, 60), width=1)
    # faint green history line, then the plunge
    pts_old = [(x + 6, y + int(h * 0.30)), (x + int(w * 0.18), y + int(h * 0.26)),
               (x + int(w * 0.30), y + int(h * 0.34))]
    d.line(pts_old, fill=(70, 160, 110), width=3, joint="curve")
    pts = [(x + int(w * 0.30), y + int(h * 0.34)),
           (x + int(w * 0.42), y + int(h * 0.30)),
           (x + int(w * 0.52), y + int(h * 0.44)),
           (x + int(w * 0.62), y + int(h * 0.52)),
           (x + int(w * 0.72), y + int(h * 0.66)),
           (x + int(w * 0.84), y + int(h * 0.74)),
           (x + int(w * 0.94), y + int(h * 0.86))]
    # red area under the plunge
    area = pts + [(x + int(w * 0.94), y + h), (x + int(w * 0.30), y + h)]
    d.polygon(area, fill=(90, 16, 22))
    d.line(pts, fill=(235, 40, 50), width=5, joint="curve")
    for (px, py) in pts[1:]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 220, 220),
                  outline=(235, 40, 50))
    # big down arrow
    ax, ay = x + int(w * 0.80), y + int(h * 0.10)
    d.polygon([(ax, ay), (ax + 26, ay), (ax + 26, ay + 26), (ax + 38, ay + 26),
               (ax + 13, ay + 52), (ax - 12, ay + 26), (ax, ay + 26)],
              fill=(235, 40, 50))
    # VIX gauge, bottom left
    gx, gy, gr = x + 14, y + h - 16, 34
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 180, 360, fill=(120, 130, 150),
          width=5)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 180, 252, fill=(235, 40, 50),
          width=5)
    import math
    ang = math.radians(180 + 72)  # needle toward high VIX
    d.line([gx, gy, gx + int(gr * 0.85 * math.cos(ang)),
            gy + int(gr * 0.85 * math.sin(ang))], fill=(255, 255, 255), width=3)
    d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=(255, 255, 255))
    d.text((gx + gr + 8, gy - 26), "VIX 35.89", font=F(SANS_B, 13),
           fill=(255, 255, 255))
    d.text((gx + gr + 8, gy - 10), "nearly double", font=F(SANS, 10),
           fill=(170, 180, 195))
    # dark backing so the labels stay readable over the chart
    d.rectangle([x + 6, y + 4, x + 178, y + 42], fill=(12, 18, 30))
    d.text((x + 10, y + 8), "S&P 500  -8.6%  WEEK", font=F(SANS_B, 12),
           fill=(255, 120, 120))
    d.text((x + 10, y + 24), "Nasdaq  -10%  WEEK", font=F(SANS_B, 12),
           fill=(255, 120, 120))


# ---------------------------------------------------------------- mini icons
def mini_icon(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cx, cy = x + w // 2, y + h // 2
    if kind == "capitol":
        d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 6], fill=(70, 70, 78))
        d.rectangle([x + 16, y + h - 26, x + w - 16, y + h - 12],
                    fill=(240, 240, 235))
        for i in range(5):
            px = x + 22 + i * (w - 44) // 4
            d.rectangle([px, y + h - 24, px + 5, y + h - 12], fill=(70, 70, 78))
        d.pieslice([cx - 16, y + 4, cx + 16, y + 30], 180, 360,
                   fill=(140, 30, 40))
        d.rectangle([cx - 2, y + 2, cx + 2, y + 8], fill=(140, 30, 40))
    elif kind == "drone":
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 110, 95))
        d.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 16],
                    fill=(90, 88, 84))
        for i in range(4):
            d.rectangle([x + 18 + i * 14, y + h - 30, x + 26 + i * 14,
                         y + h - 22], fill=(255, 200, 90))
        d.ellipse([cx - 16, y + 6, cx + 16, y + 16], fill=(60, 60, 66))
        d.line([cx - 26, y + 11, cx - 16, y + 11], fill=(60, 60, 66), width=2)
        d.line([cx + 16, y + 11, cx + 26, y + 11], fill=(60, 60, 66), width=2)
        d.ellipse([cx - 22, y + 4, cx - 10, y + 8], fill=(120, 120, 126))
        d.ellipse([cx + 10, y + 4, cx + 22, y + 8], fill=(120, 120, 126))
    elif kind == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(20, 40, 66))
        d.polygon([(x + 6, y + h - 18), (x + w - 6, y + h - 22),
                   (x + w - 12, y + h - 8), (x + 12, y + h - 6)],
                  fill=(30, 30, 34))
        d.rectangle([x + 18, y + h - 34, x + w - 30, y + h - 20],
                    fill=(150, 60, 40))
        d.polygon([(x + int(w * 0.55), y + h - 34), (x + int(w * 0.62), y + h - 48),
                   (x + int(w * 0.70), y + h - 34)], fill=(255, 140, 20))
        d.polygon([(x + int(w * 0.58), y + h - 34), (x + int(w * 0.62), y + h - 44),
                   (x + int(w * 0.66), y + h - 34)], fill=(255, 220, 80))
    elif kind == "ipo":
        d.rectangle([x, y, x + w, y + h], fill=(16, 40, 28))
        for i in range(5):
            gx = x + 10 + i * (w - 20) // 4
            d.line([gx, y + 6, gx, y + h - 6], fill=(50, 90, 65), width=1)
        d.line([(x + 10, y + h - 12), (x + int(w * 0.4), y + h - 30),
                (x + int(w * 0.7), y + h - 22), (x + w - 10, y + 8)],
               fill=(80, 220, 130), width=4, joint="curve")
        d.text((x + 8, y + 4), "$83", font=F(SANS_B, 12), fill=(255, 255, 255))
    elif kind == "chip":
        d.rectangle([x, y, x + w, y + h], fill=(24, 24, 40))
        d.rectangle([cx - 18, cy - 16, cx + 18, cy + 16], fill=(40, 120, 90),
                    outline=(200, 220, 200), width=2)
        d.rectangle([cx - 9, cy - 8, cx + 9, cy + 8], fill=(220, 230, 220))
        for i in range(4):
            d.line([cx - 18 + i * 12, cy - 16, cx - 18 + i * 12, cy - 24],
                   fill=(200, 200, 200), width=2)
            d.line([cx - 18 + i * 12, cy + 16, cx - 18 + i * 12, cy + 24],
                   fill=(200, 200, 200), width=2)
    elif kind == "fire":
        d.rectangle([x, y, x + w, y + h], fill=(40, 30, 26))
        d.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 6],
                    fill=(110, 100, 90))
        d.rectangle([x + 16, y + h - 30, x + w - 16, y + h - 14],
                    fill=(80, 74, 66))
        d.polygon([(cx - 14, y + h - 28), (cx - 6, y + 10), (cx, y + h - 30),
                   (cx + 8, y + 8), (cx + 14, y + h - 28)], fill=(255, 140, 20))
        d.polygon([(cx - 7, y + h - 28), (cx, y + 20), (cx + 7, y + h - 28)],
                  fill=(255, 220, 80))
    elif kind == "africa":
        d.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
        d.polygon([(cx - 16, y + 6), (cx + 14, y + 6), (cx + 18, y + 18),
                   (cx + 8, y + h - 8), (cx - 2, y + h - 12), (cx - 14, y + 22)],
                  fill=(200, 140, 60))
        d.ellipse([cx - 4, y + 12, cx + 8, y + 22], fill=(140, 30, 40))
    elif kind == "march":
        d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
        for i, px in enumerate([0.18, 0.38, 0.58, 0.78]):
            px0 = x + int(w * px)
            d.ellipse([px0 - 6, y + 10, px0 + 6, y + 22], fill=(60, 50, 44))
            d.rectangle([px0 - 7, y + 22, px0 + 7, y + h - 8],
                        fill=[(185, 18, 28), (20, 90, 140), (200, 140, 40),
                              (40, 110, 70)][i])
        d.rectangle([x + 8, y + 4, x + w - 8, y + 12], fill=(255, 255, 255))
        d.text((x + 12, y + 4), "COST OF LIVING", font=F(SANS_B, 8),
               fill=(185, 18, 28))
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(235, 235, 228))
        d.rectangle([x + 10, y + 8, x + int(w * 0.48), y + 26],
                    fill=(220, 60, 50))
        d.polygon([(x + int(w * 0.48), y + 8), (x + int(w * 0.48), y + 26),
                   (x + int(w * 0.48) - 8, y + 17)], fill=(220, 60, 50))
        d.rectangle([x + int(w * 0.52), y + 8, x + w - 10, y + 26],
                    fill=(255, 150, 50))
        d.rectangle([x + 14, y + 30, x + w - 14, y + h - 8], fill=(250, 248, 240))
        d.text((x + 18, y + 30), "DELHI TALKS", font=F(SANS_B, 10),
               fill=(22, 22, 22))
    elif kind == "school":
        d.rectangle([x, y, x + w, y + h], fill=(30, 50, 90))
        d.rectangle([cx - 26, cy - 8, cx + 26, cy + 16], fill=(250, 248, 240))
        d.rectangle([cx - 20, cy - 2, cx + 20, cy + 10], fill=(200, 220, 240))
        d.text((cx - 14, cy - 1), "AI?", font=F(SANS_B, 11), fill=(185, 18, 28))
        d.line([cx - 30, cy + 18, cx + 30, cy - 12], fill=(235, 40, 50), width=4)


# ---------------------------------------------------------------- main draw
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d._image = img
    M = 24
    CW = W - 2 * M  # 976

    # masthead
    d.text((M, 12), "THE WORLD IN ONE DAY", font=F(SERIF_B, 27), fill=INK)
    d.text((M + 352, 16), "35 STORIES  ·  6 REGIONS", font=F(SANS_B, 12),
           fill=RED)
    d.text((M + 352, 32), "EVERY ONE DATED  ·  MONDAY 23 NOVEMBER 2026",
           font=F(SANS_B, 10), fill=GREY)
    d.line([M, 48, W - M, 48], fill=INK, width=3)
    d.line([M, 52, W - M, 52], fill=INK, width=1)

    # giant date title
    d.text((M, 58), "Monday 23 November 2026", font=F(SERIF_B, 42), fill=INK)
    d.text((M, 104), "COP31 collapses with no deal  •  Sparta II towed out after a drone hit  •  Wall Street in correction",
           font=F(SERIF_I, 14), fill=RED)

    # stat strip
    stats = [("35", "STORIES"), ("6", "REGIONS"), ("258", "HOUSE SEATS"),
             ("$120bn", "DROPPED"), ("16", "CREW SAVED"), ("35.89", "VIX")]
    sy, sh = 128, 46
    cell = CW // 6
    for i, (num, cap) in enumerate(stats):
        x0 = M + i * cell
        if i:
            d.line([x0, sy + 4, x0, sy + sh - 4], fill=(200, 190, 170), width=1)
        d.text((x0 + 10, sy), num, font=F(SANS_B, 26), fill=RED)
        d.text((x0 + 10, sy + 30), cap, font=F(SANS_B, 10), fill=INK)
    d.line([M, sy + sh, W - M, sy + sh], fill=INK, width=1)

    # region bar (proportional, sums to 35)
    regions = [("EUROPE 9", 9, (30, 80, 160)), ("MIDDLE EAST 2", 2, (220, 110, 30)),
               ("AMERICAS 10", 10, (185, 18, 28)),
               ("ASIA-PACIFIC 9", 9, (20, 130, 130)),
               ("AFRICA 2", 2, (60, 140, 70)), ("WORLD 3", 3, (110, 110, 110))]
    ry = 184
    bx = M
    for name, n, col in regions:
        bw = int(CW * n / 35)
        d.rectangle([bx, ry, bx + bw - 2, ry + 16], fill=col)
        lab = name if bw > 60 else str(n)
        d.text((bx + 4, ry + 3), lab, font=F(SANS_B, 10), fill=(255, 255, 255))
        bx += bw
    d.text((M, ry + 20), "STORIES BY REGION — EUROPE 9 · MIDDLE EAST 2 · AMERICAS 10 · ASIA-PACIFIC 9 · AFRICA 2 · WORLD 3  =  35",
           font=F(SANS_B, 9), fill=GREY)

    # ---- hero cards
    heroes = [
        ("1  COP31 COLLAPSES", "SUN 22 NOV",
         "No deal in Antalya — the 'Antalya Pact' never mentioned fossil fuels.",
         "UN talks ended Sunday with NO agreement. $120bn finance target dropped. Longest COP ever — 44 hours overtime.",
         hero_cop31),
        ("2  SPARTA II TOWED OUT", "SUN 22 NOV",
         "Russian cargo ship hit by drones is towed from Finnish waters.",
         "Hit by at least 2 drones Sat, towed out Sun by rescue vessel Murman. 16 crew evacuated; 1 slightly hurt.",
         hero_sparta),
        ("3  WALL STREET IN CORRECTION", "FRI 20 NOV",
         "Worst week since April 2025 — S&P 500 down 8.6%.",
         "Nasdaq fell ~10% in the week; VIX closed Friday at 35.89. Nvidia -14% Friday. Bitcoin below $60,000.",
         hero_wallst),
    ]
    hy, hh = 222, 192
    hw = (CW - 16) // 3
    for i, (kick, tag, head, body, painter) in enumerate(heroes):
        x0 = M + i * (hw + 8)
        d.rectangle([x0, hy, x0 + hw, hy + hh], outline=INK, width=1)
        ih = int(hh * 0.55)
        painter(d, x0 + 1, hy + 1, hw - 2, ih)
        ty = hy + ih + 6
        d.text((x0 + 8, ty), kick, font=F(SANS_B, 11), fill=RED)
        d.text((x0 + hw - 62, ty), tag, font=F(SANS_B, 9), fill=GREY)
        ty += 15
        ty = text_block(d, x0 + 8, ty, wrap(d, head, F(SERIF_B, 14), hw - 16),
                        F(SERIF_B, 14), INK, leading=16)
        text_block(d, x0 + 8, ty + 2,
                   wrap(d, body, F(SANS, 10), hw - 16), F(SANS, 10), INK,
                   leading=12)

    # ---- small cards 4-13 (2 rows x 5)
    small = [
        ("4  DEMOCRATS TAKE HOUSE", "SUN", "capitol",
         "AP: Democrats clinch at least 258 House seats, most since 1992."),
        ("5  KYIV DRONE STRIKE", "MON", "drone",
         "At least 14 missing after a Russian drone hit a building, Zelenskiy says."),
        ("6  TANKERS UNDER FIRE", "SUN", "tanker",
         "UKMTO: tanker incident in Gulf of Oman; 3 tankers struck near Hormuz."),
        ("7  ANTHROPIC RECORD IPO", "THU/FRI", "ipo",
         "Priced $83, raised ~$107.3bn — biggest IPO ever; shares fell 8.5% Fri."),
        ("8  NVIDIA IN TURMOIL", "FRI", "chip",
         "Huang out 12 Nov; SEC inquiry, subpoena; stock -14% Friday."),
        ("9  INDONESIA FACTORY FIRE", "MON", "fire",
         "7 body bags recovered, 50 missing after a factory fire."),
        ("10  SOUTH SUDAN ATTACK", "MON", "africa",
         "SPLA-IO attack leaves 24 civilians dead, AFP reports."),
        ("11  LISBON MARCHES", "MON", "march",
         "Thousands march in Lisbon as living costs fuel anger."),
        ("12  NEPAL–INDIA TALKS", "MON", "flags",
         "Nepal PM Balendra Shah holds talks with PM Modi in Delhi."),
        ("13  SEOUL MINISTER QUITS", "MON", "school",
         "Education Minister resigns over an AI cheating scandal."),
    ]
    sy0, sh2 = 420, 118
    sw = (CW - 4 * 8) // 5
    for idx, (kick, tag, kind, body) in enumerate(small):
        r, c = divmod(idx, 5)
        x0 = M + c * (sw + 8)
        y0 = sy0 + r * (sh2 + 8)
        d.rectangle([x0, y0, x0 + sw, y0 + sh2], outline=INK, width=1)
        mini_icon(d, x0 + 1, y0 + 1, sw - 2, 44, kind)
        ty = y0 + 48
        d.text((x0 + 6, ty), kick, font=F(SANS_B, 9), fill=RED)
        d.text((x0 + sw - 38, ty), tag, font=F(SANS_B, 8), fill=GREY)
        text_block(d, x0 + 6, ty + 13,
                   wrap(d, body, F(SANS, 9), sw - 12), F(SANS, 9), INK,
                   leading=11)

    # ---- map + list
    my = 676
    d.line([M, my - 6, W - M, my - 6], fill=INK, width=2)
    d.text((M, my), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    d.text((M, my + 15), "13 pinned stories, numbered as above",
           font=F(SANS, 9), fill=GREY)
    mx, mw = M, 296
    map_y0, map_y1 = my + 32, my + 196
    d.rectangle([mx, map_y0, mx + mw, map_y1], fill=(238, 234, 222),
                outline=(180, 170, 150))
    # dotted continents (ellipse blobs)
    blobs = [(55, 45, 48, 32), (95, 128, 26, 36), (165, 38, 28, 22),
             (170, 105, 30, 42), (235, 55, 55, 38), (255, 148, 22, 14),
             (205, 130, 18, 12)]
    for gy in range(map_y0 + 6, map_y1 - 4, 7):
        for gx in range(mx + 6, mx + mw - 4, 7):
            lx, ly = gx - mx, gy - map_y0
            inside = any(((lx - bx) / br) ** 2 + ((ly - by) / bh) ** 2 <= 1
                         for bx, by, br, bh in blobs)
            if inside:
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(90, 100, 110))
    pins = [(185, 55, 1), (182, 22, 2), (66, 50, 3), (84, 68, 4), (168, 40, 5),
            (208, 88, 6), (28, 52, 7), (44, 70, 8), (255, 120, 9),
            (180, 105, 10), (148, 52, 11), (225, 75, 12), (265, 55, 13)]
    for px, py, num in pins:
        ax, ay = mx + px, map_y0 + py
        d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(num)
        tw = d.textlength(t, font=F(SANS_B, 10))
        d.text((ax - tw / 2, ay - 7), t, font=F(SANS_B, 10), fill=(255, 255, 255))
    d.text((M, map_y1 + 6), "1 Antalya  2 Gulf of Finland  3 New York  4 Washington  5 Kyiv",
           font=F(SANS, 9), fill=GREY)
    d.text((M, map_y1 + 18), "6 Gulf of Oman  7 San Francisco  8 Santa Clara  9 Indonesia",
           font=F(SANS, 9), fill=GREY)
    d.text((M, map_y1 + 30), "10 South Sudan  11 Lisbon  12 Delhi  13 Seoul",
           font=F(SANS, 9), fill=GREY)

    # list 14-35, two columns
    lx0 = M + 320
    lw = W - M - lx0
    d.text((lx0, my), "ALSO ON MONDAY 23 NOVEMBER — 22 MORE STORIES",
           font=F(SANS_B, 12), fill=RED)
    items = [
        (14, "India's record 720/9d in Wellington Test"),
        (15, "Myanmar slams ASEAN ruling 'unfair'"),
        (16, "WHO: fighting disrupts Congo Ebola response"),
        (17, "Poland: Russia 'twice tried to kill' rapper"),
        (18, "Liverpool rout 10-man Man Utd"),
        (19, "Shenzhen declaration — no binding arms deal"),
        (20, "Iran war cost $48.3bn; Senate rejects war powers"),
        (21, "US, Mexico, Bolivia lose measles-free status"),
        (22, "BIS chip-export rule for China data centres"),
        (23, "Microsoft 365, FAA, AWS, Chase, NSA all down"),
        (24, "France presses UN on Myanmar"),
        (25, "Kerch Bridge hit again"),
        (26, "Peru M6.8 quake, 129 km deep; no casualties"),
        (27, "'El Chapo Isidro' captured"),
        (28, "Estonia shuts border crossings (5 closed)"),
        (29, "Greenland deal passes 109-0"),
        (30, "ICJ Myanmar genocide ruling"),
        (31, "~900,000 AI chips for China approved"),
        (32, "Yongbyon expansion"),
        (33, "Bangladesh unrest"),
        (34, "US–Venezuela deal"),
        (35, "Missiles land in Poland"),
    ]
    colw = (lw - 12) // 2
    ly = my + 20
    for i, (num, txt) in enumerate(items):
        col, row = divmod(i, 11)
        x0 = lx0 + col * (colw + 12)
        y0 = ly + row * 18
        d.text((x0, y0), f"{num}.", font=F(SANS_B, 10), fill=RED)
        d.text((x0 + 24, y0), txt, font=F(SANS, 10), fill=INK)

    # ---- DATE CHECK box
    dy = 922
    d.rectangle([M, dy, W - M, dy + 66], outline=RED, width=2)
    d.text((M + 8, dy + 4), "DATE CHECK — HOW WE KNOW IT IS MONDAY 23 NOVEMBER 2026",
           font=F(SANS_B, 11), fill=RED)
    cols = [
        ("METHOD", "Every story dated from its first Reuters / AP wire or official release. Tags: MON 23 Nov · SUN 22 Nov · FRI 20 Nov · WEEK earlier."),
        ("NOT PRINTED", "No 'COP31 deal' — talks collapsed. No Peru M6.9 (GFZ: M6.8). No 'Shenzhen peace deal' — declaration only. No Monday US closes."),
        ("STILL TO COME", "COP31 follow-up talks · Monday US market open · Kyiv rescue updates."),
    ]
    cw3 = (CW - 16) // 3
    for i, (h, t) in enumerate(cols):
        x0 = M + 8 + i * cw3
        d.text((x0, dy + 20), h, font=F(SANS_B, 9), fill=RED)
        text_block(d, x0, dy + 32, wrap(d, t, F(SANS, 9), cw3 - 14),
                   F(SANS, 9), INK, leading=11)

    # footer
    d.line([M, 996, W - M, 996], fill=INK, width=1)
    d.text((M, 1002), "Sources: Reuters, AP, AFP, GFZ, UKMTO, Yle  •  Press time: Monday 23 November 2026, 06:00 GMT  •  35 stories, every one dated",
           font=F(SANS, 10), fill=GREY)
    return img


if __name__ == "__main__":
    out = os.environ.get("OUTPUT_DIR", ".")
    os.makedirs(out, exist_ok=True)
    img = build()
    img.save(os.path.join(out, "entry.png"), optimize=True)
    print("wrote", os.path.join(out, "entry.png"), img.size)
