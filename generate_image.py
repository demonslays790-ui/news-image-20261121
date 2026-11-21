#!/usr/bin/env python3
"""Draw entry.png: one front page summing up Saturday 21 November 2026.

Stories (all reported on 21 November 2026 by wire services and that day's
morning papers):
  * Trump, Xi and Putin hold a trilateral summit in Shenzhen, on the
    sidelines of the APEC conference (The Hindu morning digest, 21 Nov).
  * Myanmar rejects the ICJ genocide verdict on the Rohingya as rights
    groups urge sanctions (AP/AFP, 21 Nov).
  * COP31 in Antalya runs into overtime, deadlocked after the draft deal
    dropped fossil fuels (AFP, 21 Nov).
  * Russia pounds Ukraine anew after Putin vowed retaliation; a Russian
    missile crashed in Poland, which Warsaw calls a provocation (AP, 21 Nov).
  * Denmark accuses Russian intelligence of a plot to kill a Ukrainian on
    its soil and expels a Russian diplomat (AP, 21 Nov).
  * A tanker/LPG ship is hit by a projectile near the Strait of Hormuz off
    Oman and catches fire; a seafarer is missing (UKMTO reports, 21 Nov).
  * Cost-of-living protests join forces across Europe (AFP, 21 Nov).
  * Also: GTA VI launches worldwide; Nikhil Gupta jailed 19.5 years in New
    York in the Sikh separatist murder-for-hire plot; Bolsonaro in hospital.

The drawing is fully deterministic: fixed geometry, fixed colours, no clock,
no randomness, so every run writes identical bytes.
"""

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
    x, y = xy
    size = fnt.size
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


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
    import math
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
    # United States: stripes and a blue canton.
    d.rectangle([x, y, x + s, y + int(s * 0.66)], fill=(255, 255, 255), outline=INK, width=3)
    for i in range(4):
        yy = y + i * int(s * 0.165)
        d.rectangle([x, yy, x + s, yy + int(s * 0.082)], fill=RED)
    d.rectangle([x, y, x + int(s * 0.42), y + int(s * 0.36)], fill=NAVY)
    # China: red field, gold star.
    x2 = x + s + 26
    d.rectangle([x2, y, x2 + s, y + int(s * 0.66)], fill=(222, 41, 16), outline=INK, width=3)
    d.polygon([(x2 + 22, y + 10), (x2 + 30, y + 30), (x2 + 51, y + 30), (x2 + 34, y + 42),
               (x2 + 40, y + 62), (x2 + 22, y + 50), (x2 + 4, y + 62), (x2 + 10, y + 42),
               (x2 - 7, y + 30), (x2 + 14, y + 30)], fill=GOLD)
    # Russia: white, blue, red bands.
    x3 = x2 + s + 26
    d.rectangle([x3, y, x3 + s, y + int(s * 0.66)], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([x3, y + int(s * 0.22), x3 + s, y + int(s * 0.44)], fill=(0, 57, 166))
    d.rectangle([x3, y + int(s * 0.44), x3 + s, y + int(s * 0.66)], fill=(213, 43, 30))


# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=4)

# Masthead
d.rectangle([26, 26, W - 26, 146], fill=NAVY)
d.text((52, 40), "THE WORLD TODAY", font=font(SERIF_BOLD, 58), fill=(255, 255, 255))
d.text((52, 104), "Saturday, 21 November 2026", font=font(SANS_BOLD, 35), fill=GOLD)
d.text((W - 52, 58), "ONE DAY.\nONE PAGE.", font=font(SANS_BOLD, 24), fill=(190, 205, 235), anchor="ra")

# Lead story: the Shenzhen summit
d.rectangle([26, 158, W - 26, 378], fill=LEAD_BG, outline=PANEL_LINE, width=2)
icon_flags(d, 56, 190, 100)
d.text((56, 286), "SHENZHEN, CHINA", font=font(SANS_BOLD, 24), fill=RED)
text_block(d, (452, 182), "TRUMP, XI & PUTIN MEET FACE TO FACE",
           font(SANS_BOLD, 46), INK, W - 452 - 48)
text_block(d, (452, 300), "A rare trilateral summit, held on the sidelines "
                          "of the APEC conference in China.",
           font(SANS, 26), (52, 58, 72), W - 452 - 48)

# Six panels, two columns by three rows
panels = [
    ("MYANMAR REJECTS GENOCIDE VERDICT",
     "Rights groups urge sanctions after the world court's Rohingya ruling.",
     icon_scales),
    ("COP31 DEADLOCKED IN OVERTIME",
     "Antalya climate talks stall after the draft deal drops fossil fuels.",
     icon_globe),
    ("RUSSIA POUNDS UKRAINE ANEW",
     "Fresh strikes follow Putin's vow of retaliation; a Russian missile crashes in Poland.",
     icon_burst),
    ("DENMARK FOILS ASSASSINATION PLOT",
     "Russian intelligence accused over a Ukrainian target; a diplomat is expelled.",
     icon_shield),
    ("TANKER ABLAZE NEAR HORMUZ",
     "A ship is hit by a projectile off Oman and catches fire; a seafarer is missing.",
     icon_ship),
    ("EUROPE MARCHES OVER PRICES",
     "Cost-of-living protesters join forces in cities across the continent.",
     icon_crowd),
]
PX, PY, PW, PH, GAP = 26, 390, 473, 152, 12
for i, (headline, sub, icon) in enumerate(panels):
    col, row = i % 2, i // 2
    x, y = PX + col * (PW + GAP), PY + row * (PH + GAP)
    d.rectangle([x, y, x + PW, y + PH], fill=PANEL, outline=PANEL_LINE, width=2)
    icon(d, x + 60, y + PH // 2, 36)
    text_block(d, (x + 118, y + 14), headline, font(SANS_BOLD, 27), INK, PW - 136)
    text_block(d, (x + 118, y + 82), sub, font(SANS, 20), (52, 58, 72), PW - 136)

# Bottom ticker
TY = PY + 3 * (PH + GAP) - GAP + 12
d.rectangle([26, TY, W - 26, H - 26], fill=(30, 30, 34))
d.text((48, TY + 14), "ALSO TODAY", font=font(SANS_BOLD, 24), fill=GOLD)
text_block(d, (48, TY + 46),
           "GTA VI launches worldwide to rave reviews  •  Plotter jailed 19½ years in "
           "New York in the Sikh separatist murder-for-hire case  •  Brazil's Bolsonaro "
           "is taken to hospital",
           font(SANS, 21), (238, 238, 238), W - 96)

img.save("entry.png", optimize=True)
print("entry.png written")
