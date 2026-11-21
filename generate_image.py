#!/usr/bin/env python3
"""Draw entry.png: one front page summing up Saturday 21 November 2026.

Every story below was verified against reports published on 20-21 November
2026 (the Saturday morning papers carry Friday's news):
  * Trump, Xi and Putin hold the first-ever trilateral summit in Shenzhen,
    on the sidelines of the APEC conference; the joint statement says a
    nuclear war "cannot be won and must never be fought" (Al Jazeera, The
    Times/WSJ, Nikkei, 19-20 Nov).
  * Myanmar rejects the ICJ genocide verdict on the Rohingya as "unfair":
    the court ruled 9-6 on 19 Nov that Myanmar committed genocide, and
    ordered returns and reparations (AP, Reuters, Al Jazeera, 20 Nov).
  * COP31 in Antalya runs into overtime, deadlocked after the draft deal
    dropped fossil fuels; a third draft is due Saturday (AFP via Al
    Jazeera / Straits Times, 20-21 Nov).
  * Russia pounds Ukraine anew after Putin vowed retaliation for the
    Kerch bridge strikes: 80+ missiles and 400+ drones overnight, at
    least six killed in Kyiv; Russian missiles land in Poland, which
    Warsaw calls a deliberate provocation (AP via Daily Star, ISW, 21 Nov).
  * Denmark accuses Russian intelligence of a plot to kill Ukrainian-
    American rapper Kyivstoner at a Copenhagen concert and expels
    Russia's defence attache (Al Jazeera, Reuters, WSJ, 20 Nov).
  * LPG tanker Tara Gas is hit twice near the Strait of Hormuz off Oman
    (16-17 Nov) and catches fire; one seafarer is missing, 24 rescued
    (UKMTO, Safety4SEA, gCaptain, Gulf News, 17-20 Nov).
  * Youth-led cost-of-living protests rally in 25+ European countries
    against prices, rearmament and cuts (AFP via Daily Star, 21 Nov).
  * Also: GTA VI launches 19 Nov to a 99 on Metacritic, with perfect
    10s from IGN, GameSpot and Game Informer; Nikhil Gupta jailed 235
    months (19 1/2 years) in New York in the Pannun murder-for-hire
    plot; Bolsonaro hospitalised in Brasilia with a near-complete
    intestinal obstruction.

The drawing is fully deterministic: fixed geometry, fixed colours, no clock,
no randomness, so every run writes identical bytes. Text blocks are measured
with the real fonts and asserted inside their panels, so no text can be
clipped or overflow (the 21 Nov v1 lead body ran past its panel edge).
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (24, 28, 38)
NAVY = (16, 34, 68)
GOLD = (212, 164, 32)
RED = (168, 32, 40)
PANEL = (255, 253, 247)
PANEL_LINE = (198, 188, 164)
LEAD_BG = (226, 233, 244)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.12):
    """Draw a wrapped block; return the y just below its last line."""
    x, y = xy
    size = fnt.size
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def star_points(cx, cy, r_out, r_in, rotation=-90):
    """Five-pointed star polygon, one point up by default."""
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rotation + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- icons
def icon_scales(d, cx, cy, s, colour=INK):
    d.line([cx, cy - s, cx, cy + s], fill=colour, width=5)
    d.line([cx - s, cy - s, cx + s, cy - s], fill=colour, width=5)
    for side in (-1, 1):
        px = cx + side * s
        d.line([px, cy - s, px - int(s * 0.45), cy + int(s * 0.35)], fill=colour, width=4)
        d.line([px, cy - s, px + int(s * 0.45), cy + int(s * 0.35)], fill=colour, width=4)
        d.arc([px - int(s * 0.45), cy + int(s * 0.2), px + int(s * 0.45), cy + int(s * 0.62)],
              0, 180, fill=colour, width=4)
    d.line([cx - int(s * 0.5), cy + s, cx + int(s * 0.5), cy + s], fill=colour, width=5)


def icon_globe(d, cx, cy, s, colour=INK):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=colour, width=5)
    d.ellipse([cx - int(s * 0.45), cy - s, cx + int(s * 0.45), cy + s], outline=colour, width=3)
    d.line([cx - s, cy, cx + s, cy], fill=colour, width=3)
    d.line([cx - int(s * 0.87), cy - int(s * 0.5), cx + int(s * 0.87), cy - int(s * 0.5)], fill=colour, width=3)
    d.line([cx - int(s * 0.87), cy + int(s * 0.5), cx + int(s * 0.87), cy + int(s * 0.5)], fill=colour, width=3)


def icon_burst(d, cx, cy, s, colour=RED):
    pts = []
    for i in range(16):
        r = s if i % 2 == 0 else int(s * 0.45)
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=colour)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 214, 64))


def icon_shield(d, cx, cy, s, colour=INK):
    d.polygon([(cx, cy - s), (cx + s, cy - int(s * 0.6)), (cx + s, cy + int(s * 0.25)),
               (cx, cy + s), (cx - s, cy + int(s * 0.25)), (cx - s, cy - int(s * 0.6))],
              outline=colour, width=5)
    d.line([cx - int(s * 0.45), cy, cx - int(s * 0.12), cy + int(s * 0.38)], fill=(34, 139, 60), width=6)
    d.line([cx - int(s * 0.12), cy + int(s * 0.38), cx + int(s * 0.5), cy - int(s * 0.35)], fill=(34, 139, 60), width=6)


def icon_ship(d, cx, cy, s, colour=INK):
    d.polygon([(cx - s, cy + int(s * 0.1)), (cx + s, cy + int(s * 0.1)),
               (cx + int(s * 0.7), cy + int(s * 0.55)), (cx - int(s * 0.7), cy + int(s * 0.55))], fill=colour)
    d.rectangle([cx - int(s * 0.5), cy - int(s * 0.35), cx + int(s * 0.35), cy + int(s * 0.1)], fill=colour)
    d.polygon([(cx + int(s * 0.05), cy - int(s * 0.95)), (cx + int(s * 0.38), cy - int(s * 0.35)),
               (cx - int(s * 0.28), cy - int(s * 0.35))], fill=(255, 122, 26))
    d.polygon([(cx + int(s * 0.05), cy - int(s * 0.62)), (cx + int(s * 0.22), cy - int(s * 0.35)),
               (cx - int(s * 0.12), cy - int(s * 0.35))], fill=(255, 196, 0))
    for wx in (-0.6, 0.0, 0.6):
        d.arc([cx + int(s * wx) - 16, cy + int(s * 0.6), cx + int(s * wx) + 16, cy + int(s * 0.88)],
              180, 360, fill=(30, 90, 168), width=4)


def icon_crowd(d, cx, cy, s, colour=INK):
    # Two placards on sticks behind a row of marchers' heads and shoulders.
    for dx in (-0.62, 0.62):
        px = cx + int(s * dx)
        d.line([px, cy - int(s * 0.15), px, cy + int(s * 0.55)], fill=colour, width=4)
        d.rectangle([px - int(s * 0.3), cy - s, px + int(s * 0.3), cy - int(s * 0.42)],
                    outline=colour, width=4)
    for dx in (-0.55, 0.0, 0.55):
        hx = cx + int(s * dx)
        d.ellipse([hx - 9, cy + 0, hx + 9, cy + 18], fill=colour)
        d.pieslice([hx - 15, cy + 14, hx + 15, cy + 44], 180, 360, fill=colour)


def icon_flags(d, x, y, s):
    # United States: 13 stripes and a blue canton with a field of stars.
    h = int(s * 0.66)
    stripe = h / 13
    d.rectangle([x, y, x + s, y + h], fill=(255, 255, 255), outline=INK, width=3)
    for i in range(0, 13, 2):
        yy = y + i * stripe
        d.rectangle([x, yy, x + s, yy + stripe], fill=RED)
    canton_w, canton_h = int(s * 0.4), int(7 * stripe)
    d.rectangle([x, y, x + canton_w, y + canton_h], fill=NAVY)
    for row in range(5):
        for col in range(6):
            sx = x + 5 + col * 6.5
            sy = y + 5 + row * 6.5
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # China: red field, one large gold star in the canton, four small stars.
    x2 = x + s + 26
    d.rectangle([x2, y, x2 + s, y + h], fill=(222, 41, 16), outline=INK, width=3)
    d.polygon(star_points(x2 + 20, y + 19, 15, 6), fill=GOLD)
    for sx, sy in ((48, 10), (58, 20), (58, 32), (48, 42)):
        d.polygon(star_points(x2 + sx, y + sy, 5, 2), fill=GOLD)
    # Russia: white, blue, red bands.
    x3 = x2 + s + 26
    d.rectangle([x3, y, x3 + s, y + h], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([x3, y + int(h / 3), x3 + s, y + int(2 * h / 3)], fill=(0, 57, 166))
    d.rectangle([x3, y + int(2 * h / 3), x3 + s, y + h], fill=(213, 43, 30))


# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=4)

# Masthead
d.rectangle([26, 26, W - 26, 146], fill=NAVY)
d.text((52, 40), "THE WORLD TODAY", font=font(SERIF_BOLD, 58), fill=(255, 255, 255))
d.text((52, 104), "Saturday, 21 November 2026", font=font(SANS_BOLD, 35), fill=GOLD)
d.text((W - 52, 58), "ONE DAY.\nONE PAGE.", font=font(SANS_BOLD, 24), fill=(190, 205, 235), anchor="ra")
d.rectangle([26, 150, W - 26, 154], fill=GOLD)

# Lead story: the Shenzhen summit
LEAD_TOP, LEAD_BOTTOM = 158, 378
d.rectangle([26, LEAD_TOP, W - 26, LEAD_BOTTOM], fill=LEAD_BG, outline=PANEL_LINE, width=2)
icon_flags(d, 56, 196, 110)
d.text((56, 282), "SHENZHEN, CHINA", font=font(SANS_BOLD, 24), fill=RED)
head_end = text_block(d, (452, 180), "TRUMP, XI & PUTIN MEET FACE TO FACE",
                      font(SANS_BOLD, 44), INK, W - 452 - 48)
body_end = text_block(d, (452, 288),
                      "The first-ever summit of the three nuclear powers ends with a pledge: "
                      "nuclear war 'cannot be won and must never be fought.'",
                      font(SANS, 24), (52, 58, 72), W - 452 - 48)
assert head_end <= 284, f"lead headline overflows: ends {head_end}"
assert body_end <= LEAD_BOTTOM - 4, f"lead body overflows: ends {body_end}"

# Six panels, two columns by three rows
panels = [
    ("MYANMAR REJECTS GENOCIDE VERDICT",
     "Myanmar calls the 9-6 verdict 'unfair'; the court orders returns and reparations.",
     icon_scales),
    ("COP31 DEADLOCKED IN OVERTIME",
     "A third draft is due today as nearly 200 nations stay deadlocked.",
     icon_globe),
    ("RUSSIA POUNDS UKRAINE ANEW",
     "One of Moscow's biggest barrages kills at least six in Kyiv; missiles land in Poland.",
     icon_burst),
    ("DENMARK FOILS ASSASSINATION PLOT",
     "The target: rapper Kyivstoner; Russia's defense attache is expelled.",
     icon_shield),
    ("TANKER ABLAZE NEAR HORMUZ",
     "LPG tanker Tara Gas is hit twice off Oman; one seafarer is missing.",
     icon_ship),
    ("EUROPE MARCHES OVER PRICES",
     "Youth-led rallies in 25+ countries rage against prices and rearmament.",
     icon_crowd),
]
PX, PY, PW, PH, GAP = 26, 390, 473, 152, 12
for i, (headline, sub, icon) in enumerate(panels):
    col, row = i % 2, i // 2
    x, y = PX + col * (PW + GAP), PY + row * (PH + GAP)
    d.rectangle([x, y, x + PW, y + PH], fill=PANEL, outline=PANEL_LINE, width=2)
    icon(d, x + 60, y + PH // 2, 36)
    h_end = text_block(d, (x + 118, y + 14), headline, font(SANS_BOLD, 27), INK, PW - 136)
    s_end = text_block(d, (x + 118, y + 82), sub, font(SANS, 20), (52, 58, 72), PW - 136)
    assert h_end <= y + 78, f"panel {i} headline overflows: ends {h_end}"
    assert s_end <= y + PH - 4, f"panel {i} sub overflows: ends {s_end}"

# Bottom ticker
TY = PY + 3 * (PH + GAP) - GAP + 12
d.rectangle([26, TY, W - 26, H - 26], fill=(30, 30, 34))
d.text((48, TY + 14), "ALSO TODAY", font=font(SANS_BOLD, 24), fill=GOLD)
t_end = text_block(d, (48, TY + 46),
                   "GTA VI launches to a 99 on Metacritic  \u2022  Nikhil Gupta jailed 19\u00bd years "
                   "in the Pannun murder plot  \u2022  Bolsonaro hospitalized with an intestinal "
                   "obstruction",
                   font(SANS, 21), (238, 238, 238), W - 96)
assert t_end <= H - 30, f"ticker overflows: ends {t_end}"

img.save("entry.png", optimize=True)
print("entry.png written")
