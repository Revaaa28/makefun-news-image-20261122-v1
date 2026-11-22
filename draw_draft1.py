#!/usr/bin/env python3
"""THE SUNDAY LEDGER - one page summing up Sunday 22 November 2026.
Deterministic Pillow drawing: no randomness, no clocks, no network.
Run twice -> identical bytes.
"""
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
LGREY = (214, 206, 186)

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
    return w_

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 46], fill=INK)
center("24 STORIES  ·  5 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
       13, F(SANS_B, 19), fill=(252, 244, 214))
f_mast = F(SERIF_B, 74)
center("THE SUNDAY LEDGER", 56, f_mast)
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

# ---------------------------------------------------------------- hero art
def art_cop31(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(238, 228, 196), outline=INK, width=2)
    # big screen with globe
    d.rectangle([x + 88, y + 8, x + w_ - 88, y + 62], fill=(44, 62, 84))
    d.ellipse([x + w_ / 2 - 20, y + 13, x + w_ / 2 + 20, y + 53], outline=(240, 240, 220), width=3)
    d.line([x + w_ / 2 - 20, y + 33, x + w_ / 2 + 20, y + 33], fill=(240, 240, 220), width=2)
    d.line([x + w_ / 2, y + 13, x + w_ / 2, y + 53], fill=(240, 240, 220), width=2)
    d.text((x + 96, y + 24), "COP31", font=F(SANS_B, 17), fill=(255, 255, 255))
    # delegate rows: desks + heads
    for r in range(3):
        yy = y + 72 + r * 24
        for c in range(6):
            xx = x + 18 + c * 48
            d.rectangle([xx, yy + 8, xx + 38, yy + 20], fill=TAND)
            d.ellipse([xx + 13, yy - 2, xx + 25, yy + 10], fill=(120, 84, 54))
    # flag bunting
    cols = [RED, (40, 90, 160), (30, 130, 70), (230, 170, 30), (120, 60, 150), RED]
    for i, cc in enumerate(cols):
        xx = x + 8 + i * 16
        d.polygon([(xx, y + 4), (xx + 13, y + 4), (xx + 6, y + 15)], fill=cc)
        xx2 = x + w_ - 21 - i * 16
        d.polygon([(xx2, y + 4), (xx2 + 13, y + 4), (xx2 + 6, y + 15)], fill=cc)

def art_ship(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(198, 216, 222), outline=INK, width=2)
    # ice floes
    for (ix, iy, iw) in [(14, 16, 52), (90, 8, 38), (210, 12, 58), (256, 26, 34)]:
        d.polygon([(x + ix, y + iy + 8), (x + ix + 10, y + iy), (x + ix + iw, y + iy + 2),
                   (x + ix + iw + 8, y + iy + 10), (x + ix + 6, y + iy + 13)],
                  fill=(240, 246, 248), outline=(150, 170, 180))
    # drone + dotted path
    dx, dy = x + w_ - 92, y + 22
    for i in range(7):
        d.ellipse([dx - 66 + i * 10, dy + 26 - i * 3, dx - 62 + i * 10, dy + 30 - i * 3], fill=INK)
    d.polygon([(dx, dy), (dx + 30, dy + 7), (dx, dy + 14)], fill=INK)
    d.rectangle([dx - 8, dy + 4, dx + 2, dy + 10], fill=INK)
    d.line([dx - 14, dy - 4, dx - 2, dy + 4], fill=INK, width=3)
    d.line([dx - 14, dy + 18, dx - 2, dy + 10], fill=INK, width=3)
    # ship
    by = y + h_ - 38
    d.polygon([(x + 30, by), (x + w_ - 24, by), (x + w_ - 44, by + 20), (x + 48, by + 20)], fill=(52, 58, 66))
    d.rectangle([x + 30, by - 8, x + w_ - 24, by], fill=DARKRED)
    box_cols = [(196, 90, 40), (50, 110, 170), (40, 150, 90), (210, 170, 40), (140, 70, 150)]
    for i, cc in enumerate(box_cols):
        bx = x + 52 + i * 38
        d.rectangle([bx, by - 26, bx + 34, by - 9], fill=cc, outline=INK, width=1)
    d.rectangle([x + w_ - 78, by - 44, x + w_ - 46, by - 9], fill=(230, 230, 224), outline=INK, width=1)
    for wy_ in range(3):
        d.rectangle([x + w_ - 72, by - 39 + wy_ * 10, x + w_ - 52, by - 34 + wy_ * 10], fill=(250, 220, 120))
    # waves
    for r in range(2):
        yy = by + 24 + r * 7
        for wx in range(x + 12, x + w_ - 20, 26):
            d.arc([wx, yy, wx + 18, yy + 8], 0, 180, fill=(70, 110, 130), width=2)

def art_factory(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(226, 216, 192), outline=INK, width=2)
    # factory block + chimneys
    d.rectangle([x + 120, y + 52, x + w_ - 14, y + h_ - 26], fill=(150, 140, 124), outline=INK, width=2)
    for i, chx in enumerate([150, 205, 258]):
        d.rectangle([x + chx, y + 18, x + chx + 20, y + 54], fill=(120, 110, 96), outline=INK, width=1)
        for s in range(3):
            d.ellipse([x + chx - 3 + s * 9, y + 4 + (i % 2) * 3, x + chx + 9 + s * 9, y + 14], outline=GREY, width=2)
    for r in range(2):
        for c in range(6):
            d.rectangle([x + 132 + c * 26, y + 62 + r * 20, x + 148 + c * 26, y + 76 + r * 20], fill=(250, 220, 120))
    # gear
    gx, gy, gr = x + 268, y + 30, 15
    for a in range(0, 360, 45):
        import math
        ax, ay = gx + gr * math.cos(math.radians(a)), gy + gr * math.sin(math.radians(a))
        d.line([gx, gy, ax, ay], fill=INK, width=5)
    d.ellipse([gx - 11, gy - 11, gx + 11, gy + 11], fill=TAND, outline=INK, width=2)
    d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=CREAM, outline=INK, width=1)
    # picket line
    for i in range(5):
        px = x + 16 + i * 24
        py = y + h_ - 56
        d.line([px + 5, py + 12, px + 5, py + 30], fill=INK, width=3)
        d.ellipse([px, py, px + 11, py + 11], fill=(120, 84, 54))
        d.line([px + 12, py + 2, px + 12, py + 26], fill=(90, 60, 30), width=2)
        d.rectangle([px + 3, py - 12, px + 26, py + 1], fill=(252, 248, 235), outline=INK, width=1)
    d.rectangle([x + 8, y + h_ - 24, x + 130, y + h_ - 10], fill=RED)
    d.text((x + 15, y + h_ - 22), "5% — FAIR PAY", font=F(SANS_B, 11), fill=(255, 255, 255))

heroes = [
    ("1 · COP31: DEAL PACKAGE ON THE TABLE — SUNDAY VOTE",
     "Negotiators ran past Friday's deadline, through Saturday and into Sunday's small hours. The summit's Australian and Turkish presidents then unveiled a new package, and President Kurum told a late-night plenary he believed every party could agree to it. Delegations had until 03:00 GMT to object; the conference sits again this morning to approve it. Kurum said the fossil-fuel wording and adaptation money for poorer countries — the two fights that deadlocked the hall — had been addressed.",
     art_cop31, "REUTERS"),
    ("2 · DRONE HITS RUSSIA-BOUND SHIP IN GULF OF FINLAND",
     "A vessel bound for Russia has been attacked by a drone in the Gulf of Finland, in the Baltic Sea. Finland's defence forces, who reported the strike in the early hours of today, say Ukraine was likely behind the attack. It is the latest sign of the Ukraine war reaching into northern waters, far from the front line: Finnish forces say the ship was hit as it crossed the gulf, the narrow sea lane between Finland and Estonia used by Russian shipping.",
     art_ship, "BBC NEWS"),
    ("3 · GERMANY: 23,000 WORKERS CALLED OUT ON STRIKE",
     "Germany's IG Metall union announced today that 23,000 car and shipyard workers across 19 companies in the north will walk out for 24 hours on Monday. Mercedes-Benz, the Meyer Werft shipyards and wind-turbine maker Siemens Gamesa are all on the list. The union wants a 5% pay rise — or, where firms break from the industry deal, binding promises on investment, products, sites and jobs.",
     art_factory, "REUTERS"),
]

hx, hy, hw, hgap = 28, 334, 309, 20
f_hb, f_hbody = F(SANS_B, 17), F(SERIF, 14)
for i, (head, body, art, src) in enumerate(heroes):
    x = hx + i * (hw + hgap)
    by = banner(x, hy, hw, head, f_hb)
    ay = by + 6
    art(x, ay, hw, 128)
    tag(x + 8, ay + 8, src)
    text_block(x + 2, ay + 138, body, f_hbody, hw - 4, 18)

# ---------------------------------------------------------------- briefs
briefs = [
    ("4 · POPE'S TABLE FOR 1,300", "Leo XIV leads the Angelus at noon, then lunches with 1,300 poor guests in the Paul VI Hall for the World Day of the Poor.", "cross"),
    ("5 · DAY 4 AT WELLINGTON", "India resume on 486-4, a lead of 118 over New Zealand's 368. Pant is 55 not out; two days remain at the Basin Reserve.", "cricket"),
    ("6 · SUNDAY AT ANFIELD", "Liverpool host Manchester United at 16:30 GMT in the Premier League's Sunday headline match.", "ball"),
    ("7 · TURIN DECIDER", "Carlos Alcaraz plays the ATP Finals title match today after a three-set semi-final win over Ben Shelton.", "tennis"),
    ("8 · VEGAS RACE DAY", "The Las Vegas Grand Prix runs under the Strip lights: 50 laps, lights out at 04:00 GMT, Verstappen from pole.", "f1"),
    ("9 · STORM WATCH: FLORIDA", "A broad low near Florida has a 30% chance of forming in 48 hours: gusty winds, dangerous surf, coastal flooding.", "storm"),
    ("10 · NFL WEEK 12", "A full Sunday slate across the United States as the NFL's playoff race tightens into the season's final stretch.", "nfl"),
    ("11 · HULL v BRIGHTON, 14:00", "Hull City host Brighton at the MKM Stadium to open the Premier League's Sunday programme.", "ball"),
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
        import math
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

bx, by0, bw, bh, bgap = 28, 640, 309, 62, 8
f_bb, f_bbody = F(SANS_B, 14), F(SERIF, 12)
for i, (head, body, kind) in enumerate(briefs):
    r, c = divmod(i, 3)
    x, y = bx + c * (bw + hgap), by0 + r * (bh + bgap)
    icon(x, y, 46, kind)
    d.text((x + 54, y - 2), head, font=f_bb, fill=DARKRED)
    text_block(x + 54, y + 17, body, f_bbody, bw - 56, 14)

# ---------------------------------------------------------------- map + index
my = 856
d.rectangle([28, my, 452, 972], fill=SEA, outline=INK, width=2)
# simplified tan continents (schematic blobs)
lands = [
    [(52, 876), (120, 868), (150, 884), (128, 916), (96, 940), (84, 916), (56, 902)],            # N America
    [(122, 924), (148, 928), (142, 958), (124, 966), (112, 944)],                                # S America
    [(206, 878), (238, 872), (244, 892), (224, 904), (204, 894)],                                # Europe
    [(228, 902), (258, 906), (262, 940), (240, 962), (222, 936)],                                # Africa
    [(252, 876), (330, 870), (368, 888), (352, 914), (292, 918), (258, 900)],                    # Asia
    [(330, 928), (366, 926), (372, 946), (340, 952)],                                             # Australia
    [(392, 940), (404, 938), (402, 950), (390, 948)],                                             # NZ
]
for poly in lands:
    d.polygon(poly, fill=TAN, outline=TAND, width=2)
pins = {1: (268, 890), 2: (240, 878), 3: (228, 884), 4: (224, 894), 5: (398, 944),
        6: (216, 880), 7: (222, 888), 8: (76, 892), 9: (100, 900), 11: (218, 882)}
f_pin = F(SANS_B, 10)
for n, (px, py) in pins.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
    s = str(n)
    d.text((px - tw(s, f_pin) / 2, py - 6), s, font=f_pin, fill=(255, 255, 255))
d.text((36, 950), "WHERE THE NEWS IS — pins 1-12 as numbered", font=F(SANS_B, 11), fill=INK)

index = [
    "13 · ANTALYA: objections to the package closed at 03:00 GMT",
    "14 · CHRISTCHURCH hosts the Test decider next week",
    "15 · VEGAS: 6.2 km of Strip, the race's fourth running",
    "16 · ST JOHNS RIVER still in major flood after Florida's rains",
    "17 · THANKSGIVING travel builds across the US",
    "18 · ADDIS ABABA: next year's summit takes the finance roadmap",
    "19 · HELSINKI: the attacked vessel was bound for Russia",
    "20 · STRIKE LIST: Mercedes-Benz, Meyer Werft, Siemens Gamesa",
    "21 · RED CROSS volunteers run the Paul VI Hall kitchens",
    "22 · ANFIELD TABLE: Liverpool third, United sixteenth",
    "23 · MATCHWEEK 11 closes Monday: Brentford v Everton",
    "24 · 106 TABLES laid in the Paul VI Hall for the lunch",
]
ix, iy = 466, my + 2
f_idx = F(SANS_B, 13)
for i, ln in enumerate(index):
    col, row = divmod(i, 6)
    d.text((ix + col * 272, iy + row * 19), ln, font=f_idx, fill=INK)

# ---------------------------------------------------------------- date check
dy = 978
d.rectangle([28, dy, W - 28, dy + 40], outline=RED, width=2)
d.rectangle([28, dy, 208, dy + 40], fill=RED)
d.text((38, dy + 4), "DATE CHECK", font=F(SANS_B, 15), fill=(255, 255, 255))
d.text((38, dy + 21), "NOT SUNDAY'S NEWS", font=F(SANS_B, 10), fill=(255, 220, 200))
checks = [
    "SAT 21 NOV — Five missiles downed over Saudi Arabia",
    "SAT 21 NOV — Banda Sea quake, M6.8, off Timor-Leste",
    "SAT 21 NOV — Wales 26-29 Australia; England rout All Blacks",
    "SAT 21 NOV — Newcastle 2-2 Arsenal (Sat night, St James')",
    "SAT 21 NOV — Zelensky: bridge strikes a 'fair response'",
    "SAT 21 NOV — FBI most-wanted cartel figure held (BBC, Sat)",
    "SAT 21 NOV — Man convicted over LA's Palisades fire",
    "SAT 21 NOV — France marches: 82,500 out nationwide",
    "SAT 21 NOV — Two tankers hit in the Strait of Hormuz",
    "SAT 21 NOV — Cap Cana governments dialogue concludes",
    "FRI 20 NOV — Peru quake M6.7; Cyclone Akvan landfall",
    "FRI 20 NOV — $7.25bn Roundup settlement approved",
    "FRI 20 NOV — UK-EU deal signed; Trump on Iran (Fri)",
    "THU 19 NOV — GTA VI goes on sale",
    "18 NOV — Voyager 1 passes a full light-day from the Sun",
    "2025 — Starc's 7 for 58 was last year's Ashes",
    "NOT YET — A Vegas winner: lights out 04:00 GMT today",
    "NOT CONFIRMED — BepiColombo's Mercury orbit entry",
]
f_dc = F(SANS, 10)
for i, ln in enumerate(checks):
    col, row = divmod(i, 6)
    d.text((220 + col * 262, dy + 3 + row * 13), ln, font=f_dc, fill=INK)

img.save("/home/hatch/workspace/mf-news-image-20261122-v1build/entry.png")
print("saved")
