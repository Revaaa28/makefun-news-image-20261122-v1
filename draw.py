#!/usr/bin/env python3
"""THE SUNDAY LEDGER - one page summing up Sunday 22 November 2026.
Deterministic Pillow drawing: no randomness, no clocks, no network.
Run twice -> identical bytes. (Draft 2: tightened layout after draft 1.)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 235)
INK = (26, 23, 18)
RED = (168, 24, 24)
DARKRED = (128, 16, 16)
TAN = (216, 192, 138)
TAND = (188, 158, 100)
SEA = (178, 198, 205)
GREY = (92, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def center(text, y, font, fill=INK):
    d.text(((W - tw(text, font)) / 2, y), text, font=font, fill=fill)

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, text, font, width, leading, fill=INK):
    for ln in wrap(text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def banner(x, y, w_, text, font, fill=RED, txt=(255, 255, 255)):
    lines = wrap(text, font, w_ - 14)
    bh = len(lines) * (font.size + 3) + 9
    d.rectangle([x, y, x + w_, y + bh], fill=fill)
    ty = y + 5
    for ln in lines:
        d.text((x + (w_ - tw(ln, font)) / 2, ty), ln, font=font, fill=txt)
        ty += font.size + 3
    return y + bh

def tag(x, y, text):
    f = F(SANS_B, 12)
    w_ = tw(text, f) + 12
    d.rectangle([x, y, x + w_, y + 19], fill=INK)
    d.text((x + 6, y + 3), text, font=f, fill=(255, 244, 200))

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 46], fill=INK)
center("24 STORIES  ·  5 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
       13, F(SANS_B, 19), fill=(252, 244, 214))
center("THE SUNDAY LEDGER", 56, F(SERIF_B, 74))
d.line([28, 140, W - 28, 140], fill=INK, width=3)
d.line([28, 145, W - 28, 145], fill=INK, width=1)
center("SUNDAY 22 NOVEMBER 2026  ·  ONE DAY, ONE PAGE  ·  THE WORLD SINCE MIDNIGHT",
       151, F(SANS_B, 16))
center("A climate deal waits for its Sunday vote · a drone strikes in the Baltic · Germany's metalworkers down tools",
       176, F(SERIF_I, 20))

# ---------------------------------------------------------------- stats strip
stats = [
    ("~200", "NATIONS IN\nTHE ANTALYA HALL"),
    ("06:00", "GMT: SESSION TO\nAPPROVE THE DEAL"),
    ("23,000", "GERMAN WORKERS\nCALLED OUT MONDAY"),
    ("118", "INDIA'S LEAD AT\nWELLINGTON"),
    ("1,300", "GUESTS AT THE\nPOPE'S LUNCH"),
    ("50", "LAPS UNDER THE\nVEGAS LIGHTS"),
]
sx, sy, sw, sh = 28, 206, W - 56, 86
d.rectangle([sx, sy, sx + sw, sy + sh], outline=INK, width=2)
cw = sw / 6
f_num, f_lab = F(SERIF_B, 36), F(SANS_B, 11)
for i, (num, lab) in enumerate(stats):
    cx = sx + i * cw
    if i:
        d.line([cx, sy + 6, cx, sy + sh - 6], fill=GREY, width=1)
    d.text((cx + (cw - tw(num, f_num)) / 2, sy + 6), num, font=f_num, fill=DARKRED)
    ly = sy + 50
    for ln in lab.split("\n"):
        d.text((cx + (cw - tw(ln, f_lab)) / 2, ly), ln, font=f_lab, fill=INK)
        ly += 13

ry = sy + sh + 8
d.rectangle([28, ry, W - 28, ry + 26], fill=TAN, outline=INK, width=1)
center("EUROPE 13  ·  AMERICAS 6  ·  ASIA 2  ·  OCEANIA 2  ·  AFRICA 1",
       ry + 4, F(SANS_B, 16))

# ---------------------------------------------------------------- hero art (110 tall)
def art_cop31(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(238, 228, 196), outline=INK, width=2)
    d.rectangle([x + 92, y + 8, x + w_ - 92, y + 54], fill=(44, 62, 84))
    d.ellipse([x + w_ / 2 - 18, y + 12, x + w_ / 2 + 18, y + 48], outline=(240, 240, 220), width=3)
    d.line([x + w_ / 2 - 18, y + 30, x + w_ / 2 + 18, y + 30], fill=(240, 240, 220), width=2)
    d.line([x + w_ / 2, y + 12, x + w_ / 2, y + 48], fill=(240, 240, 220), width=2)
    for r in range(3):
        yy = y + 62 + r * 16
        for c in range(6):
            xx = x + 18 + c * 48
            d.rectangle([xx, yy + 6, xx + 38, yy + 14], fill=TAND)
            d.ellipse([xx + 14, yy - 2, xx + 24, yy + 8], fill=(120, 84, 54))
    cols = [RED, (40, 90, 160), (30, 130, 70), (230, 170, 30), (120, 60, 150), RED]
    for i, cc in enumerate(cols):
        xx = x + 8 + i * 16
        d.polygon([(xx, y + 4), (xx + 13, y + 4), (xx + 6, y + 15)], fill=cc)
        xx2 = x + w_ - 21 - i * 16
        d.polygon([(xx2, y + 4), (xx2 + 13, y + 4), (xx2 + 6, y + 15)], fill=cc)

def art_ship(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(198, 216, 222), outline=INK, width=2)
    for (ix, iy, iw) in [(14, 14, 52), (90, 7, 38), (206, 10, 58), (256, 24, 34)]:
        d.polygon([(x + ix, y + iy + 8), (x + ix + 10, y + iy), (x + ix + iw, y + iy + 2),
                   (x + ix + iw + 8, y + iy + 10), (x + ix + 6, y + iy + 13)],
                  fill=(240, 246, 248), outline=(150, 170, 180))
    dx, dy = x + w_ - 92, y + 20
    for i in range(7):
        d.ellipse([dx - 66 + i * 10, dy + 24 - i * 3, dx - 62 + i * 10, dy + 28 - i * 3], fill=INK)
    d.polygon([(dx, dy), (dx + 30, dy + 7), (dx, dy + 14)], fill=INK)
    d.rectangle([dx - 8, dy + 4, dx + 2, dy + 10], fill=INK)
    d.line([dx - 14, dy - 4, dx - 2, dy + 4], fill=INK, width=3)
    d.line([dx - 14, dy + 18, dx - 2, dy + 10], fill=INK, width=3)
    by = y + h_ - 36
    d.polygon([(x + 30, by), (x + w_ - 24, by), (x + w_ - 44, by + 19), (x + 48, by + 19)], fill=(52, 58, 66))
    d.rectangle([x + 30, by - 8, x + w_ - 24, by], fill=DARKRED)
    box_cols = [(196, 90, 40), (50, 110, 170), (40, 150, 90), (210, 170, 40), (140, 70, 150)]
    for i, cc in enumerate(box_cols):
        bx = x + 52 + i * 38
        d.rectangle([bx, by - 25, bx + 34, by - 9], fill=cc, outline=INK, width=1)
    d.rectangle([x + w_ - 78, by - 42, x + w_ - 46, by - 9], fill=(230, 230, 224), outline=INK, width=1)
    for wy_ in range(3):
        d.rectangle([x + w_ - 72, by - 37 + wy_ * 10, x + w_ - 52, by - 32 + wy_ * 10], fill=(250, 220, 120))
    for r in range(2):
        yy = by + 22 + r * 6
        for wx in range(x + 12, x + w_ - 20, 26):
            d.arc([wx, yy, wx + 18, yy + 8], 0, 180, fill=(70, 110, 130), width=2)

def art_factory(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(226, 216, 192), outline=INK, width=2)
    d.rectangle([x + 128, y + 44, x + w_ - 14, y + h_ - 24], fill=(150, 140, 124), outline=INK, width=2)
    for i, chx in enumerate([156, 208, 260]):
        d.rectangle([x + chx, y + 14, x + chx + 18, y + 46], fill=(120, 110, 96), outline=INK, width=1)
        for s in range(3):
            d.ellipse([x + chx - 3 + s * 8, y + 2 + (i % 2) * 3, x + chx + 8 + s * 8, y + 11], outline=GREY, width=2)
    for r in range(2):
        for c in range(5):
            d.rectangle([x + 140 + c * 30, y + 52 + r * 18, x + 158 + c * 30, y + 64 + r * 18], fill=(250, 220, 120))
    gx, gy, gr = x + 282, y + 26, 13
    for a in range(0, 360, 45):
        ax, ay = gx + gr * math.cos(math.radians(a)), gy + gr * math.sin(math.radians(a))
        d.line([gx, gy, ax, ay], fill=INK, width=5)
    d.ellipse([gx - 10, gy - 10, gx + 10, gy + 10], fill=TAND, outline=INK, width=2)
    d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=CREAM, outline=INK, width=1)
    for i in range(5):
        px = x + 14 + i * 23
        py = y + h_ - 58
        d.line([px + 5, py + 12, px + 5, py + 30], fill=INK, width=3)
        d.ellipse([px, py, px + 11, py + 11], fill=(120, 84, 54))
        d.line([px + 12, py + 2, px + 12, py + 26], fill=(90, 60, 30), width=2)
        d.rectangle([px + 3, py - 12, px + 25, py + 1], fill=(252, 248, 235), outline=INK, width=1)
    d.rectangle([x + 8, y + h_ - 24, x + 128, y + h_ - 10], fill=RED)
    d.text((x + 14, y + h_ - 22), "5% — FAIR PAY", font=F(SANS_B, 11), fill=(255, 255, 255))

heroes = [
    ("1 · COP31 DEAL PACKAGE — SUNDAY VOTE",
     "Negotiators ran past Friday's deadline, through Saturday and into Sunday's small hours. The summit's Australian and Turkish presidents then unveiled a new package; President Kurum told a late-night plenary he believed all parties could agree. Delegations had until 03:00 GMT to object.",
     art_cop31, "REUTERS"),
    ("2 · DRONE HITS RUSSIA-BOUND SHIP, GULF OF FINLAND",
     "A vessel bound for Russia has been attacked by a drone in the Gulf of Finland. Finland's defence forces, reporting the strike in today's early hours, say Ukraine was likely behind it. The hit takes the war into northern waters: the gulf is the narrow lane between Finland and Estonia used by Russian shipping.",
     art_ship, "BBC NEWS"),
    ("3 · GERMANY: 23,000 WORKERS CALLED OUT",
     "IG Metall announced today that 23,000 car and shipyard workers at 19 firms in northern Germany walk out for 24 hours on Monday. Mercedes-Benz, the Meyer Werft shipyards and Siemens Gamesa are on the list. The union wants 5% more pay — or binding promises on investment, sites and jobs.",
     art_factory, "REUTERS"),
]

hx, hy, hw, hgap = 28, 334, 309, 20
f_hb, f_hbody = F(SANS_B, 16), F(SERIF, 13)
for i, (head, body, art, src) in enumerate(heroes):
    x = hx + i * (hw + hgap)
    by = banner(x, hy, hw, head, f_hb)
    ay = by + 6
    art(x, ay, hw, 104)
    tag(x + 8, ay + 8, src)
    text_block(x + 2, ay + 112, body, f_hbody, hw - 4, 15)

# ---------------------------------------------------------------- briefs
briefs = [
    ("4 · POPE'S TABLE FOR 1,300", "Leo XIV leads the Angelus at noon, then lunches with 1,300 poor guests for the World Day of the Poor.", "cross"),
    ("5 · DAY 4 AT WELLINGTON", "India resume on 486-4, a lead of 118 over New Zealand's 368. Pant is 55 not out.", "cricket"),
    ("6 · SUNDAY AT ANFIELD", "Liverpool host Manchester United at 16:30 GMT in the Premier League's Sunday headline match.", "ball"),
    ("7 · TURIN DECIDER", "Carlos Alcaraz plays the ATP Finals title match today after a three-set semi-final win over Ben Shelton.", "tennis"),
    ("8 · VEGAS RACE DAY", "The Las Vegas Grand Prix runs under the Strip lights: 50 laps, lights out at 04:00 GMT, Verstappen from pole.", "f1"),
    ("9 · STORM WATCH: FLORIDA", "A broad low near Florida has a 30% chance of forming in 48 hours: gusty winds, dangerous surf, coastal flooding.", "storm"),
    ("10 · NFL WEEK 12", "A full Sunday slate across the United States as the NFL's playoff race tightens into the season's final stretch.", "nfl"),
    ("11 · HULL v BRIGHTON, 14:00", "Hull City host Brighton at the MKM Stadium to open Sunday's Premier League programme.", "ball"),
    ("12 · THE SAME MEAL, CITYWIDE", "Rome's soup kitchens serve the Pope's lunch in communion, so no one eats alone on the World Day of the Poor.", "bowl"),
]

def icon(x, y, s, kind):
    d.rectangle([x, y, x + s, y + s], fill=PAPER, outline=INK, width=2)
    cx, cy = x + s / 2, y + s / 2
    if kind == "cross":
        d.rectangle([cx - 3, y + 8, cx + 3, y + s - 8], fill=DARKRED)
        d.rectangle([x + 10, cy - 8, x + s - 10, cy - 2], fill=DARKRED)
    elif kind == "cricket":
        d.rectangle([cx - 4, y + 8, cx + 3, y + s - 12], fill=TAND, outline=INK, width=1)
        d.ellipse([cx + 6, y + s - 18, cx + 16, y + s - 8], fill=RED, outline=INK, width=1)
    elif kind == "ball":
        d.ellipse([x + 9, y + 9, x + s - 9, y + s - 9], outline=INK, width=2)
        d.polygon([(cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)], fill=INK)
    elif kind == "tennis":
        d.ellipse([x + 9, y + 9, x + s - 9, y + s - 9], fill=(150, 190, 60), outline=INK, width=2)
        d.arc([x + 4, y + 9, x + 26, y + s - 9], 270, 90, fill=(255, 255, 255), width=2)
        d.arc([x + s - 26, y + 9, x + s - 4, y + s - 9], 90, 270, fill=(255, 255, 255), width=2)
    elif kind == "f1":
        d.rectangle([x + 8, cy + 2, x + s - 8, cy + 9], fill=RED)
        d.rectangle([cx - 9, cy - 8, cx + 9, cy + 3], fill=INK)
        d.ellipse([x + 11, cy + 7, x + 21, cy + 17], fill=INK)
        d.ellipse([x + s - 21, cy + 7, x + s - 11, cy + 17], fill=INK)
        d.rectangle([x + 8, cy - 12, x + 13, cy + 2], fill=INK)
    elif kind == "storm":
        for a in range(0, 300, 40):
            r1 = 5 + a / 38
            x1 = cx + r1 * math.cos(math.radians(a))
            y1 = cy + r1 * math.sin(math.radians(a))
            r2 = 5 + (a + 40) / 38
            x2 = cx + r2 * math.cos(math.radians(a + 40))
            y2 = cy + r2 * math.sin(math.radians(a + 40))
            d.line([x1, y1, x2, y2], fill=(40, 90, 160), width=3)
    elif kind == "nfl":
        d.ellipse([x + 10, cy - 9, x + s - 10, cy + 9], fill=(150, 84, 40), outline=INK, width=2)
        d.line([cx - 6, cy, cx + 6, cy], fill=(255, 255, 255), width=2)
    elif kind == "bowl":
        d.pieslice([x + 9, y + 12, x + s - 9, y + s - 6], 0, 180, fill=(50, 110, 170), outline=INK, width=2)
        d.arc([x + 14, y + 4, x + 24, y + 16], 180, 330, fill=GREY, width=2)
        d.arc([x + 24, y + 2, x + 34, y + 14], 180, 330, fill=GREY, width=2)

bx, by0, bw, bh, bgap = 28, 656, 309, 58, 5
f_bb, f_bbody = F(SANS_B, 14), F(SERIF, 12)
for i, (head, body, kind) in enumerate(briefs):
    r, c = divmod(i, 3)
    x, y = bx + c * (bw + hgap), by0 + r * (bh + bgap)
    icon(x, y, 46, kind)
    d.text((x + 54, y - 2), head, font=f_bb, fill=DARKRED)
    text_block(x + 54, y + 17, body, f_bbody, bw - 56, 13)

# ---------------------------------------------------------------- map + index
my, mh = 846, 106
d.rectangle([28, my, 404, my + mh], fill=SEA, outline=INK, width=2)
lands = [
    [(48, 862), (108, 854), (134, 870), (114, 900), (86, 924), (76, 900), (50, 886)],
    [(110, 908), (132, 912), (128, 940), (112, 948), (102, 928)],
    [(186, 864), (214, 858), (220, 878), (202, 890), (184, 880)],
    [(206, 888), (232, 892), (236, 926), (216, 946), (200, 922)],
    [(228, 862), (298, 856), (332, 874), (318, 900), (264, 904), (234, 886)],
    [(298, 914), (330, 912), (336, 932), (308, 938)],
    [(356, 926), (366, 924), (364, 936), (354, 934)],
]
for poly in lands:
    d.polygon(poly, fill=TAN, outline=TAND, width=2)
pins = {1: (246, 878), 2: (224, 860), 3: (210, 868), 4: (206, 882), 5: (360, 930),
        6: (194, 862), 7: (200, 876), 8: (70, 878), 9: (92, 886), 11: (188, 870)}
f_pin = F(SANS_B, 9)
for n, (px, py) in pins.items():
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=2)
    s = str(n)
    d.text((px - tw(s, f_pin) / 2, py - 5), s, font=f_pin, fill=(255, 255, 255))
d.text((36, my + mh - 18), "WHERE THE NEWS IS — pins as numbered", font=F(SANS_B, 11), fill=INK)

index = [
    "13 · ANTALYA: objections closed 03:00",
    "14 · CHRISTCHURCH: decider next week",
    "15 · VEGAS: 6.2 km of Strip, fourth running",
    "16 · ST JOHNS RIVER still in major flood",
    "17 · THANKSGIVING travel builds in the US",
    "18 · ADDIS ABABA: the finance roadmap",
    "19 · HELSINKI: vessel was bound for Russia",
    "20 · MERCEDES, MEYER WERFT, SIEMENS",
    "21 · RED CROSS runs the Paul VI kitchens",
    "22 · ANFIELD: Liverpool 3rd, United 16th",
    "23 · MONDAY: Brentford v Everton",
    "24 · 106 TABLES laid in the Paul VI Hall",
]
ix, iy = 418, my + 4
f_idx = F(SANS_B, 11)
for i, ln in enumerate(index):
    col, row = divmod(i, 6)
    d.text((ix + col * 290, iy + row * 17), ln, font=f_idx, fill=INK)

# ---------------------------------------------------------------- date check
dy, dh = 960, 58
d.rectangle([28, dy, W - 28, dy + dh], outline=RED, width=2)
d.rectangle([28, dy, 196, dy + dh], fill=RED)
d.text((38, dy + 10), "DATE CHECK", font=F(SANS_B, 16), fill=(255, 255, 255))
d.text((38, dy + 32), "NOT SUNDAY'S NEWS", font=F(SANS_B, 10), fill=(255, 220, 200))
checks = [
    "SAT 21 NOV — Missiles downed over Saudi Arabia",
    "SAT 21 NOV — Banda Sea quake, M6.8",
    "SAT 21 NOV — Wales 26-29 AUS; ENG rout NZ",
    "SAT 21 NOV — Newcastle 2-2 Arsenal (Sat night)",
    "SAT 21 NOV — Zelensky: bridge strikes 'fair'",
    "FRI 20 NOV — Peru quake M6.7; Akvan landfall",
    "FRI 20 NOV — Roundup: $7.25bn approved",
    "FRI 20 NOV — UK-EU deal; Trump on Iran",
    "THU 19 NOV — GTA VI goes on sale",
    "18 NOV — Voyager 1 a full light-day out",
    "NOT YET — Vegas winner (04:00 GMT start)",
    "NOT CONFIRMED — BepiColombo at Mercury",
]
f_dc = F(SANS, 10)
for i, ln in enumerate(checks):
    col, row = divmod(i, 4)
    d.text((206 + col * 264, dy + 4 + row * 13), ln, font=f_dc, fill=INK)

img.save("/home/hatch/workspace/mf-news-image-20261122-v1build/entry.png")
print("saved")
