"""Build the news-image-20261120 front page with PIL.

Draws one 1024x1024 newspaper front page summing up Friday
20 November 2026: 36 stories (13 illustrated panels + 23 ALSO items),
a six-number strip, a region bar, a numbered world map, a DATE CHECK
box and a source footer. Everything is drawn with code; no external
files are read. Output is deterministic: same bytes every run.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 238, 218)
PAPER_DARK = (238, 229, 205)
INK = (26, 26, 26)
INK_SOFT = (74, 68, 58)
RED = (176, 30, 30)
RED_DARK = (140, 22, 22)
BLUE = (38, 70, 120)
SEA = (227, 220, 196)
LAND = (216, 196, 154)
LAND_LINE = (178, 155, 109)
GOLD = (184, 134, 42)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(text, font, width):
    """Greedy word wrap; returns list of lines that fit in width px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_n(text, font, width, max_lines):
    """Wrap and hard-truncate to max_lines (last line gets an ellipsis)."""
    lines = wrap(text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and font.getlength(lines[-1] + " ...") > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + " ..."
    return lines


# ---------------------------------------------------------------- stories
# 13 illustrated panels: 3 heroes + 10 small. Bodies are kept short so
# they fit their boxes at the chosen font sizes (checked in build()).
HEROES = [
    {
        "n": 1, "cat": "WAR IN EUROPE", "art": "kyiv",
        "label": "KYIV", "sublabel": "3 bridges hit",
        "attr": "Officials' count", "loc": "KYIV, UKRAINE \u00b7 WAR",
        "head": "Russian missiles hit three Kyiv bridges",
        "body": ("About 110 missiles and 400 drones hit overnight, killing "
                 "at least nine and cutting power and water in the capital. "
                 "(Kyiv Independent, BBC)"),
        "src": "Reuters",
    },
    {
        "n": 2, "cat": "WEATHER", "art": "cyclone",
        "label": "CYCLONE AKVAN", "sublabel": "Landfall \u00b7 8 am",
        "attr": "Weather office", "loc": "ODISHA, INDIA \u00b7 CYCLONE",
        "head": "Cyclone Akvan comes ashore in eastern India",
        "body": ("Crossed the coast near Gopalpur from about 8 am; over "
                 "300,000 moved to shelters. No deaths reported. "
                 "(IMD, Deccan Herald)"),
        "src": "IMD",
    },
    {
        "n": 3, "cat": "MARKETS", "art": "selloff",
        "label": "AI SELL-OFF", "sublabel": "Asia, Friday's close",
        "attr": "Closing prices", "loc": "TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
        "head": "AI sell-off sinks Asia's stock markets",
        "body": ("Taiwan's index fell 6.2% to end its worst week since 1991. "
                 "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the "
                 "slide. (Al Jazeera, Anadolu)"),
        "src": "Morningstar / Reuters",
    },
]

SMALL = [
    {
        "n": 4, "cat": "CLIMATE", "art": "cop",
        "label": "COP31: NO DEAL", "loc": "ANTALYA \u00b7 CLIMATE",
        "title": "COP31: no deal yet",
        "body": "The draft text leaves out fossil fuels.",
        "src": "Reuters",
    },
    {
        "n": 5, "cat": "EUROPE", "art": "ukeu",
        "label": "UK\u2013EU DEAL", "loc": "BRUSSELS \u00b7 DIPLOMACY",
        "title": "UK\u2013EU reset deal",
        "body": "Food trade, youth visas, carbon link.",
        "src": "Reuters",
    },
    {
        "n": 6, "cat": "SPORT", "art": "cricket",
        "label": "PHILLIPS: 118", "loc": "WELLINGTON \u00b7 CRICKET",
        "title": "Phillips hits 118",
        "body": "Hundreds in India in all three formats.",
        "src": "Reuters",
    },
    {
        "n": 7, "cat": "SPACE", "art": "mercury",
        "label": "MERCURY", "loc": "MERCURY \u00b7 SPACE",
        "title": "BepiColombo at Mercury",
        "body": "At Mercury after 8 years; enters orbit tomorrow, 19:24 CET.",
        "src": "ESA",
    },
    {
        "n": 8, "cat": "EUROPE", "art": "strike",
        "label": "ITALY: STRIKE", "loc": "ROME \u00b7 LABOUR",
        "title": "General strike in Italy",
        "body": "Workers and students march.",
        "src": "Reuters",
    },
    {
        "n": 9, "cat": "WAR IN EUROPE", "art": "poland",
        "label": "POLAND: MISSILE", "loc": "EASTERN POLAND \u00b7 SECURITY",
        "title": "Missile lands in Poland",
        "body": "It fell in a field; two airports paused.",
        "src": "Polish MoD",
    },
    {
        "n": 10, "cat": "CULTURE", "art": "gta",
        "label": "GTA VI: $2.36BN", "loc": "GLOBAL \u00b7 CULTURE",
        "title": "GTA VI: $2.36bn day one",
        "body": "Reported Fri (Sensor Tower est.): $2.36bn, 24.58m copies.",
        "src": "Sensor Tower",
    },
    {
        "n": 11, "cat": "ECONOMY", "art": "cpi",
        "label": "JAPAN: 2.2%", "loc": "TOKYO \u00b7 ECONOMY",
        "title": "Japan inflation 2.2%",
        "body": "A December rate rise stays in view.",
        "src": "Reuters",
    },
    {
        "n": 12, "cat": "ENERGY", "art": "hormuz",
        "label": "HORMUZ", "loc": "HORMUZ \u00b7 ENERGY",
        "title": "Hormuz standoff",
        "body": "~50 ships hold offshore; Brent $92.22 early Friday.",
        "src": "straits.live / Reuters",
    },
    {
        "n": 13, "cat": "ASIA", "art": "exam",
        "label": "SUNEUNG", "loc": "SEOUL \u00b7 EDUCATION",
        "title": "Suneung cheat scandal",
        "body": "111 candidates caught cheating with smart devices.",
        "src": "BBC",
    },
]

# 23 ALSO items, numbered 14-36. Each is one short paragraph (<=80 chars
# plus source) so it fits two lines in its column.
ALSO = [
    (14, "BUKELE", "Registered Thu night for a third term; vote 28 Feb 2027.", "Reuters"),
    (15, "F1", "Russell fastest in wet Las Vegas FP2, 1:47.272.", "Formula1.com"),
    (16, "CANCER PILL", "Daraxonrasib + chemo shrank tumours in 60.7%.", "EORTC"),
    (17, "ANTHROPIC", "Shares fell 13% Friday to ~$85, near the $83 IPO price.", "Reuters"),
    (18, "NASDAQ", "Fell 3.6% Friday, erasing its 2026 gains; S&P down 7th day.", "CNN"),
    (19, "ASIA ROUT", "MSCI Asia-Pacific \u22122.5% Friday, worst week since 2020.", "Reuters"),
    (20, "EUROPE", "STOXX 600 \u22121% Friday, worst week since March; chips \u22124%+.", "Reuters"),
    (21, "VIX", "Fear gauge hit 30 on Friday, its highest since late March.", "Reuters"),
    (22, "BITCOIN", "Fell below $59,000 Friday, near its bear low of $57,700.", "CoinDesk"),
    (23, "GOLD", "Down ~2% toward $3,500, its lowest since September 2025.", "Reuters"),
    (24, "COPPER", "Set for its steepest weekly drop since April 2025.", "Reuters"),
    (25, "DOLLAR", "Index at 103.86, its strongest since April 2025.", "Reuters"),
    (26, "UK RETAIL", "Sales rose 0.7% in Oct, beating all forecasts.", "ONS / Reuters"),
    (27, "RIYADH", "Houthi attacks on Riyadh; Brent $92.22 early Friday.", "Reuters"),
    (28, "CHINA", "Lending rates held at 3.00%/3.50%, an 18th straight month.", "Xinhua"),
    (29, "DRAGON", "SpaceX Cargo Dragon undocked from the ISS on Friday.", "SpaceX / NASA"),
    (30, "USSF-317", "SpaceX retargeted its classified launch to Fri night.", "Spaceflight Now"),
    (31, "SUNCATCHER", "Google booked Blue Origin's New Glenn for solar TPUs.", "Google"),
    (32, "BADMINTON", "Rakshitha, 19, beat Olympic champion Chen Yufei.", "myKhel"),
    (33, "CRICKET", "Bavuma ruled out of 2nd Test vs Bangladesh, calf injury.", "myKhel"),
    (34, "NFL", "Texans beat the Colts 26-3 on Thursday night football.", "AP"),
    (35, "MLS", "Cincinnati beat Orlando 3-1; Real Salt Lake won on penalties.", "AP"),
    (36, "INDIA", "Nifty near 9-month highs on record $12.21bn foreign inflows.", "Reuters"),
]

# Region counts; must sum to 36 (checked in build()).
REGIONS = [
    ("EUROPE", 6), ("ASIA", 8), ("AMERICAS", 11), ("MIDDLE EAST", 2),
    ("OCEANIA", 1), ("AFRICA", 1), ("WORLD", 7),
]

# One distinct colour per region segment in the region bar.
REGION_COLORS = {
    "EUROPE": (38, 70, 120), "ASIA": (176, 30, 30),
    "AMERICAS": (110, 60, 140), "MIDDLE EAST": (150, 110, 30),
    "OCEANIA": (20, 110, 110), "AFRICA": (40, 110, 60),
    "WORLD": (80, 80, 80),
}

STATS = [
    ("110+", "MISSILES ON UKRAINE"),
    ("3", "BRIDGES HIT"),
    ("300,000+", "EVACUATED"),
    ("\u22126.2%", "TAIEX"),
    ("100,000", "YOUTH VISAS / YR"),
    ("8", "KILLED ACROSS UKRAINE"),
]

DATE_CHECK_NOT_IN = (
    "NOT IN THIS PAPER (19 Nov): Trump\u2013Xi\u2013Putin summit & declaration; "
    "ICJ Myanmar Rohingya ruling; Anthropic IPO $83 & Nasdaq debut; GTA VI "
    "midnight launch; Crimea Bridge attack; COP31 second draft; US Senate "
    "Iran war-powers vote 48\u201351; Van Gogh sale $190.4m; hippo Fiona's "
    "death; Kenya's last Ebola patient (11 Nov); ATP Turin final (Sun 22 Nov)."
)
DATE_CHECK_NOT_YET = (
    "NOT YET KNOWN: final COP31 outcome; BepiColombo orbit insertion (Sat). "
    "Asia closing prices are Friday's closes. Thursday-night events reported "
    "Friday (Bukele registration; NFL Texans\u2013Colts) are included as "
    "Friday reports."
)

# ------------------------------------------------------------- illustrations
# Every panel picture is drawn from primitives: no photos, no files.

def _sky(d, x, y, w, h, top, bottom):
    for i in range(h):
        t = i / max(1, h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))


def art_kyiv(d, x, y, w, h):
    _sky(d, x, y, w, h, (24, 28, 52), (74, 68, 96))
    for sx, sy in [(x + 20, y + 8), (x + 90, y + 16), (x + 170, y + 6),
                   (x + 240, y + 14), (x + 280, y + 22)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(240, 230, 180))
    # missile trails
    for mx, my, ln in [(x + 40, y + 20, 46), (x + 130, y + 12, 60),
                       (x + 220, y + 26, 40)]:
        d.line([(mx, my), (mx + ln, my + 26)], fill=(255, 190, 90), width=2)
        d.ellipse([mx + ln - 3, my + 23, mx + ln + 3, my + 29],
                  fill=(255, 220, 130))
    # river
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(52, 78, 110))
    d.line([(x, y + h - 22), (x + w, y + h - 22)], fill=(120, 150, 180))
    # bridge deck + arches
    by = y + h - 40
    d.rectangle([x + 8, by, x + w - 8, by + 6], fill=(30, 30, 34))
    for ax in (x + 40, x + 130, x + 220):
        d.arc([ax, by - 26, ax + 60, by + 8], 180, 360, fill=(200, 60, 40),
              width=3)
        d.line([(ax + 30, by - 26), (ax + 30, by)], fill=(200, 60, 40),
               width=2)
    # damaged span: broken deck + smoke
    d.line([(x + 150, by), (x + 168, by + 12)], fill=(200, 60, 40), width=3)
    for sx, sy, r in [(x + 160, by - 34, 7), (x + 172, by - 46, 9),
                      (x + 186, by - 58, 11)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 118, 112))
    # city blocks
    for bx, bw, bh in [(x + 14, 26, 18), (x + 52, 20, 26), (x + 250, 24, 20)]:
        d.rectangle([bx, by - bh, bx + bw, by], fill=(16, 16, 22))
        d.rectangle([bx + 5, by - bh + 5, bx + 9, by - bh + 9],
                    fill=(255, 200, 90))


def art_cyclone(d, x, y, w, h):
    _sky(d, x, y, w, h, (150, 180, 200), (210, 215, 205))
    cx, cy = x + w // 2 - 10, y + h // 2 - 4
    # spiral arms
    for k in range(3):
        pts = []
        for a in range(0, 540, 12):
            import math
            r = 4 + a * 0.055
            ang = math.radians(a + k * 120)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.8))
        d.line(pts, fill=(255, 255, 255), width=4)
        d.line(pts, fill=(90, 120, 150), width=1)
    d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=(60, 80, 110))
    # rain streaks
    for rx in range(x + 8, x + w - 4, 14):
        d.line([(rx, y + 6), (rx - 4, y + 18)], fill=(140, 165, 190), width=1)
    # coastline + sea
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 110, 140))
    d.polygon([(x, y + h - 16), (x + w * 0.35, y + h - 26),
               (x + w * 0.7, y + h - 14), (x + w, y + h - 20),
               (x + w, y + h - 16)], fill=(190, 175, 130))
    # shelter roofs
    for hx in (x + 30, x + 90, x + 200):
        d.polygon([(hx, y + h - 30), (hx + 12, y + h - 38),
                   (hx + 24, y + h - 30)], fill=(176, 30, 30))


def art_selloff(d, x, y, w, h):
    # Left ~55%: falling bars. Right ~45%: dark data table of closes.
    split = int(w * 0.55)
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    d.line([(x + 8, y + h - 14), (x + split - 6, y + h - 14)], fill=INK, width=1)
    d.line([(x + 8, y + 6), (x + 8, y + h - 14)], fill=INK, width=1)
    # falling bars: Taiex, Nikkei, KOSPI, Hang Seng
    vals = [62, 48, 52, 19]
    bw = (split - 30) // 4
    for i, v in enumerate(vals):
        bx = x + 14 + i * bw
        bh = int(v * (h - 30) / 62)
        d.rectangle([bx, y + h - 14 - bh, bx + bw - 8, y + h - 14],
                    fill=(176, 30, 30))
    d.line([(x + 12, y + 10), (x + split - 10, y + h - 26)], fill=(140, 22, 22),
           width=3)
    d.polygon([(x + split - 22, y + h - 34), (x + split - 8, y + h - 26),
               (x + split - 22, y + h - 18)], fill=(140, 22, 22))
    # data table of Friday closes
    d.rectangle([x + split, y, x + w, y + h], fill=(20, 30, 50))
    rows = [("TAIPEI", "\u22126.2%"), ("SEOUL", "\u22125.2%"),
            ("TOKYO", "\u22125.1%"), ("HONG KONG", "\u22121.9%")]
    f_c = F(SANS_B, 10)
    for i, (city, pct) in enumerate(rows):
        ry = y + 8 + i * 17
        d.text((x + split + 8, ry), city, font=f_c, fill=(255, 255, 255))
        pw = f_c.getlength(pct)
        d.text((x + w - 8 - pw, ry), pct, font=f_c, fill=(255, 90, 80))


def art_cop(d, x, y, w, h):
    _sky(d, x, y, w, h, (140, 170, 190), (205, 210, 195))
    cx, cy, r = x + w // 2, y + h // 2 - 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 180),
              outline=(40, 80, 120), width=2)
    d.arc([cx - r + 6, cy - r + 4, cx + r - 4, cy + r - 6], 200, 340,
          fill=(40, 90, 60), width=3)
    d.arc([cx - r + 10, cy - r + 8, cx + r - 8, cy + r - 10], 180, 300,
          fill=(60, 120, 70), width=2)
    # thermometer showing 1.5C
    tx = x + w - 26
    d.rectangle([tx, y + 8, tx + 8, y + h - 16], fill=(255, 255, 255),
                outline=INK)
    d.rectangle([tx + 1, y + h - 26, tx + 7, y + h - 17], fill=RED)
    d.ellipse([tx - 3, y + h - 22, tx + 11, y + h - 8], fill=RED)


def art_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    # Union Jack (simplified): blue field, white + red crosses
    ux, uy, uw, uh = x + 10, y + 8, 62, 34
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(30, 50, 110))
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(255, 255, 255),
           width=8)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(255, 255, 255),
           width=8)
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(200, 30, 40),
           width=3)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(200, 30, 40),
           width=3)
    # EU flag: blue field, circle of stars
    ex, ey, ew, eh = x + w - 72, y + 8, 62, 34
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(20, 40, 120))
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ex + ew // 2 + 12 * math.cos(a)
        sy = ey + eh // 2 + 9 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    # handshake bridge below
    d.line([(x + 20, y + h - 16), (x + w - 20, y + h - 16)], fill=INK, width=2)


def art_cricket(d, x, y, w, h):
    _sky(d, x, y, w, h, (120, 170, 90), (190, 210, 140))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(110, 150, 70))
    # stumps
    sx = x + w - 34
    for i in range(3):
        d.rectangle([sx + i * 6, y + h - 40, sx + i * 6 + 3, y + h - 18],
                    fill=(220, 190, 120))
    d.rectangle([sx, y + h - 43, sx + 15, y + h - 41], fill=(220, 190, 120))
    # bat
    d.polygon([(x + 60, y + 12), (x + 72, y + 10), (x + 78, y + 34),
               (x + 66, y + 36)], fill=(200, 160, 90))
    d.rectangle([x + 68, y + 34, x + 72, y + 48], fill=(120, 80, 40))
    # ball
    d.ellipse([x + 96, y + 30, x + 108, y + 42], fill=RED)
    d.arc([x + 96, y + 30, x + 108, y + 42], 300, 60, fill=(255, 255, 255))


def art_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 20))
    for sx, sy in [(x + 12, y + 8), (x + 60, y + 6), (x + 130, y + 12),
                   (x + 170, y + 6), (x + 30, y + 30), (x + 150, y + 34)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # Mercury
    mx, my, mr = x + 44, y + h // 2 + 6, 20
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 148, 128))
    for cx, cy, cr in [(mx - 8, my - 6, 4), (mx + 7, my + 3, 3),
                       (mx - 2, my + 9, 5), (mx + 10, my - 9, 2)]:
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(140, 122, 104))
    # orbit ellipse + spacecraft
    d.ellipse([x + 8, y + 2, x + w - 8, y + h - 6], outline=(200, 200, 220))
    scx, scy = x + w - 40, y + 16
    d.rectangle([scx - 8, scy - 4, scx + 8, scy + 4], fill=(220, 220, 230))
    d.rectangle([scx - 18, scy - 2, scx - 8, scy + 2], fill=(60, 120, 200))
    d.rectangle([scx + 8, scy - 2, scx + 18, scy + 2], fill=(60, 120, 200))


def art_strike(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 190, 170), (230, 220, 195))
    # crowd silhouettes
    for i, cx in enumerate(range(x + 14, x + w - 10, 26)):
        d.ellipse([cx, y + h - 34, cx + 12, y + h - 22], fill=INK)
        d.polygon([(cx - 2, y + h - 22), (cx + 14, y + h - 22),
                   (cx + 10, y + h - 8), (cx + 2, y + h - 8)], fill=INK)
        if i % 3 == 0:
            d.rectangle([cx - 6, y + h - 52, cx + 18, y + h - 40],
                        fill=(255, 255, 255), outline=RED)


def art_poland(d, x, y, w, h):
    _sky(d, x, y, w, h, (170, 190, 205), (215, 220, 210))
    # land + border
    d.polygon([(x + 10, y + 8), (x + w - 60, y + 6), (x + w - 10, y + h - 10),
               (x + 30, y + h - 8)], fill=(200, 185, 140),
              outline=(120, 100, 70))
    d.line([(x + w - 60, y + 6), (x + w - 10, y + h - 10)], fill=RED, width=2)
    # missile arrows crossing the border
    for my in (y + 22, y + 36):
        d.line([(x + w - 70, my), (x + w - 26, my + 8)], fill=RED, width=3)
        d.polygon([(x + w - 26, my + 8), (x + w - 36, my + 2),
                   (x + w - 36, my + 14)], fill=RED)


def art_gta(d, x, y, w, h):
    _sky(d, x, y, w, h, (250, 170, 90), (200, 90, 120))
    # sun
    d.ellipse([x + w - 52, y + 4, x + w - 16, y + 40], fill=(255, 220, 120))
    # skyline
    base = y + h - 12
    for bx, bw, bh in [(x + 6, 22, 30), (x + 32, 16, 44), (x + 52, 26, 26),
                       (x + 82, 18, 52), (x + 104, 24, 34), (x + 132, 20, 46),
                       (x + 156, 24, 28)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(40, 30, 50))
        for wy in range(base - bh + 5, base - 4, 8):
            for wx in range(bx + 4, bx + bw - 3, 7):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))


def art_cpi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    d.line([(x + 8, y + h - 14), (x + w - 6, y + h - 14)], fill=INK, width=1)
    d.line([(x + 8, y + 6), (x + 8, y + h - 14)], fill=INK, width=1)
    pts = [(x + 12, y + h - 26), (x + 60, y + h - 30), (x + 110, y + h - 38),
           (x + 160, y + 12)]
    d.line(pts, fill=RED, width=3)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=RED)


def art_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 130, 160))
    # two land masses leaving a narrow strait
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h),
               (x, y + h)], fill=(200, 185, 140))
    d.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h),
               (x + w * 0.72, y + h)], fill=(200, 185, 140))
    # tankers waiting in the strait
    for tx, ty in [(x + w // 2 - 8, y + 12), (x + w // 2 - 4, y + 30),
                   (x + w // 2 - 10, y + 48)]:
        d.rectangle([tx, ty, tx + 22, ty + 6], fill=(30, 30, 34))
        d.rectangle([tx + 14, ty - 5, tx + 18, ty], fill=(30, 30, 34))


def art_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    # desk + paper
    d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 14], fill=(150, 110, 70))
    d.rectangle([x + 24, y + 8, x + w - 60, y + h - 24], fill=(255, 255, 255),
                outline=INK)
    for i, ly in enumerate(range(y + 14, y + h - 28, 7)):
        d.line([(x + 30, ly), (x + w - 66, ly)], fill=(120, 120, 120), width=1)
    # phone with alert: small enough to fit whole inside the tile,
    # bottom edge visible, standing on the desk
    px, py = x + w - 44, y + 8
    d.rectangle([px, py, px + 20, py + 24], fill=(20, 20, 26),
                outline=(200, 200, 200))
    d.rectangle([px + 2, py + 2, px + 18, py + 22], fill=(255, 240, 180))
    # dark screen inset inside the phone body (3px margin each side)
    d.rectangle([px + 3, py + 3, px + 17, py + 18], fill=(28, 34, 52))


ART = {
    "kyiv": art_kyiv, "cyclone": art_cyclone, "selloff": art_selloff,
    "cop": art_cop, "ukeu": art_ukeu, "cricket": art_cricket,
    "mercury": art_mercury, "strike": art_strike, "poland": art_poland,
    "gta": art_gta, "cpi": art_cpi, "hormuz": art_hormuz, "exam": art_exam,
}


def _draw_art_clipped(img, fn, x, y, w, h):
    """Draw one panel picture onto its own tile, then paste the tile.

    Nothing drawn by the art function can escape the art box: any
    stroke that overshoots the tile edge is cut by the tile itself.
    """
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    fn(td, 0, 0, w, h)
    img.paste(tile, (x, y), tile)

# ------------------------------------------------------------------- map
# Simplified continent outlines in (lon, lat).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42),
     (-75, 35), (-80, 32), (-81, 26), (-90, 21), (-97, 16), (-94, 17),
     (-86, 13), (-83, 9), (-79, 9), (-92, 15), (-105, 20), (-110, 23),
     (-114, 28), (-120, 34), (-124, 40), (-124, 48), (-130, 55),
     (-150, 60), (-165, 60)],
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -34), (-65, -41),
     (-68, -50), (-70, -54), (-73, -37), (-72, -20), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68),
     (44, 68), (40, 60), (32, 60), (28, 55), (23, 54), (19, 54), (14, 54),
     (8, 54), (0, 49), (-2, 44), (-9, 37)],
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
     (-8, 5), (-4, 5), (6, 4), (9, 4), (12, -2), (13, -10), (12, -17),
     (16, -28), (20, -35), (26, -34), (32, -26), (35, -20), (40, -15),
     (41, -10), (46, -1), (51, 11), (44, 11), (40, 15), (38, 18),
     (35, 22), (32, 31), (22, 33), (11, 34)],
    [(40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 59),
     (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38),
     (120, 32), (122, 28), (118, 25), (110, 21), (108, 18), (105, 10),
     (103, 8), (100, 8), (98, 10), (95, 16), (92, 21), (88, 22), (86, 20),
     (80, 15), (77, 8), (76, 10), (72, 20), (68, 23), (62, 25), (57, 26),
     (52, 26), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36), (30, 36),
     (27, 37), (26, 38), (23, 36), (22, 37), (26, 40), (30, 41), (35, 42),
     (40, 44), (44, 42), (44, 46), (40, 52), (44, 55), (42, 60), (40, 66)],
    [(113, -22), (114, -30), (115, -34), (120, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (136, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
]

# Story number -> (lon, lat) on the map. 7 (Mercury) is drawn in an inset.
PINS = {
    1: (33.5, 52.5), 2: (85.0, 19.3), 3: (120.5, 22.6), 4: (30.0, 35.5),
    5: (0.5, 52.5), 6: (174.8, -41.3), 8: (11.0, 40.5), 9: (18.5, 55.5),
    10: (-74.0, 40.7), 11: (141.2, 35.5), 12: (56.3, 26.5),
    13: (127.0, 39.7),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK)
    mx0, my0 = x + 4, y + 4
    mw, mh = w - 8, h - 8

    def proj(lon, lat):
        px = mx0 + (lon + 180.0) / 360.0 * mw
        py = my0 + (75.0 - lat) / 130.0 * mh
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    # pin 7 inset: Mercury is off this map
    ix0, iy0, iw, ih = x + w - 128, y + 6, 122, 30
    d.rectangle([ix0, iy0, ix0 + iw, iy0 + ih], fill=(20, 20, 28),
                outline=(255, 255, 255))
    d.ellipse([ix0 + 8, iy0 + 9, ix0 + 22, iy0 + 23], fill=(168, 148, 128))
    d.ellipse([ix0 + 12, iy0 + 12, ix0 + 15, iy0 + 15], fill=(140, 122, 104))
    d.text((ix0 + 28, iy0 + 4), "7 \u00b7 MERCURY", font=F(SANS_B, 9),
           fill=(255, 255, 255))
    d.text((ix0 + 28, iy0 + 16), "off this map", font=F(SANS, 8),
           fill=(210, 210, 210))
    for n, (lon, lat) in sorted(PINS.items()):
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = F(SANS_B, 9).getlength(t)
        d.text((px - tw / 2, py - 6), t, font=F(SANS_B, 9),
               fill=(255, 255, 255))


# ------------------------------------------------------------------ layout
def _rule(d, x, y, w, thick=2):
    d.line([(x, y), (x + w, y)], fill=INK, width=thick)


def _banner(d, x, y, w, text, font, bg=RED, fg=(255, 255, 255)):
    d.rectangle([x, y, x + w, y + 15], fill=bg)
    d.text((x + 5, y + 2), text, font=font, fill=fg)


def draw_masthead(d, x, y, w):
    # Kicker line: left red, right count.
    f_kick = F(SANS_B, 11)
    d.text((x, y), "THE WORLD IN ONE DAY", font=f_kick, fill=RED_DARK)
    f_count = F(SANS_B, 10)
    count = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    cw_ = f_count.getlength(count)
    d.text((x + w - cw_, y + 1), count, font=f_count, fill=INK)
    _rule(d, x, y + 16, w, 3)
    # Giant date masthead: largest serif bold that fits the width.
    title = "Friday 20 November 2026"
    f_title = None
    for size in (68, 66, 64, 62, 60, 58, 56):
        f = F(SERIF_B, size)
        if f.getlength(title) <= w:
            f_title = f
            break
    tw = f_title.getlength(title)
    d.text((x + (w - tw) / 2, y + 22), title, font=f_title, fill=INK)
    lead = ("Russian missiles hit Kyiv's bridges \u00b7 Cyclone Akvan strikes "
            "India \u00b7 An AI sell-off sinks Asia's markets \u00b7 UK and EU "
            "seal a deal")
    f_lead = F(SERIF, 13)
    lines = wrap(lead, f_lead, w - 40)
    ly = y + 96
    for ln in lines:
        lw = f_lead.getlength(ln)
        d.text((x + (w - lw) / 2, ly), ln, font=f_lead, fill=INK_SOFT)
        ly += 16
    return ly


def draw_stats(d, x, y, w):
    bw = (w - 5 * 6) // 6
    f_num = F(SANS_B, 19)
    f_lab = F(SANS_B, 8)
    for i, (num, lab) in enumerate(STATS):
        bx = x + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 44], outline=INK, width=1,
                    fill=(250, 246, 236))
        nw = f_num.getlength(num)
        d.text((bx + (bw - nw) / 2, y + 3), num, font=f_num, fill=RED_DARK)
        lw = f_lab.getlength(lab)
        d.text((bx + (bw - lw) / 2, y + 28), lab, font=f_lab, fill=INK)
    return y + 44


def draw_regions(d, x, y, w):
    # One coloured segment per region (equal widths), white bold text.
    seg = w // len(REGIONS)
    f = F(SANS_B, 11)
    for i, (name, n) in enumerate(REGIONS):
        sx = x + i * seg
        sw = seg if i < len(REGIONS) - 1 else w - i * seg
        d.rectangle([sx, y, sx + sw, y + 20], fill=REGION_COLORS[name])
        text = "%s %d" % (name, n)
        tw = f.getlength(text)
        d.text((sx + (sw - tw) / 2, y + 4), text, font=f,
               fill=(255, 255, 255))
    return y + 20


def draw_hero(img, d, x, y, w, h, hero):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1,
                fill=(250, 246, 236))
    # Art on top; bold label overlaid on the picture, not a banner above it.
    ax, ay, aw, ah = x + 6, y + 6, w - 12, 76
    _draw_art_clipped(img, ART[hero["art"]], ax, ay, aw, ah)
    f_lab = F(SANS_B, 14)
    lw = f_lab.getlength(hero["label"])
    d.rectangle([ax + 4, ay + 4, ax + 4 + lw + 12, ay + 26], fill=RED)
    d.text((ax + 10, ay + 8), hero["label"], font=f_lab,
           fill=(255, 255, 255))
    f_sub = F(SANS_B, 10)
    sw = f_sub.getlength(hero["sublabel"])
    d.rectangle([ax + 4, ay + 30, ax + 4 + sw + 12, ay + 46], fill=(255, 255, 255))
    d.text((ax + 10, ay + 33), hero["sublabel"], font=f_sub, fill=INK)
    # Attribution strip under the picture.
    d.rectangle([ax, ay + ah, ax + aw, ay + ah + 13], fill=INK)
    d.text((ax + 6, ay + ah + 2), hero["attr"], font=F(SANS_B, 9),
           fill=(255, 255, 255))
    # Numbered location + category.
    ly = ay + ah + 15
    d.ellipse([x + 8, ly, x + 24, ly + 16], fill=BLUE)
    d.text((x + 8 + 8 - 3, ly + 2), str(hero["n"]), font=F(SANS_B, 10),
           fill=(255, 255, 255))
    d.text((x + 28, ly + 2), hero["loc"], font=F(SANS_B, 10), fill=BLUE)
    # Headline + body (source embedded in parentheses, as the top 10 do).
    f_head = F(SERIF_B, 14)
    hy = ly + 18
    for ln in wrap_n(hero["head"], f_head, w - 16, 2):
        d.text((x + 8, hy), ln, font=f_head, fill=INK)
        hy += 17
    f_body = F(SANS, 11)
    by = hy + 2
    for ln in wrap_n(hero["body"], f_body, w - 16, 3):
        d.text((x + 8, by), ln, font=f_body, fill=INK_SOFT)
        by += 13
    return y + h


def draw_small(img, d, x, y, w, h, panel):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1,
                fill=(250, 246, 236))
    # Art on top; short punchy label overlaid on the picture.
    ax, ay, aw, ah = x + 5, y + 5, w - 10, 44
    _draw_art_clipped(img, ART[panel["art"]], ax, ay, aw, ah)
    f_lab = F(SANS_B, 10)
    lw = f_lab.getlength(panel["label"])
    lab_w = min(lw + 10, aw - 8)
    d.rectangle([ax + 3, ay + 3, ax + 3 + lab_w, ay + 17], fill=RED)
    d.text((ax + 8, ay + 5), panel["label"], font=f_lab,
           fill=(255, 255, 255))
    # Attribution strip under the picture.
    d.rectangle([ax, ay + ah, ax + aw, ay + ah + 10], fill=INK)
    d.text((ax + 5, ay + ah + 1), panel["src"], font=F(SANS_B, 7),
           fill=(255, 255, 255))
    # Numbered location + category.
    ly = ay + ah + 12
    d.ellipse([x + 6, ly, x + 18, ly + 12], fill=BLUE)
    d.text((x + 6 + 6 - 2, ly + 1), str(panel["n"]), font=F(SANS_B, 8),
           fill=(255, 255, 255))
    d.text((x + 21, ly + 1), panel["loc"], font=F(SANS_B, 8), fill=BLUE)
    # Title + body.
    ty = ly + 14
    d.text((x + 6, ty), panel["title"], font=F(SANS_B, 11), fill=INK)
    f_body = F(SANS, 9)
    by = ty + 15
    for ln in wrap_n(panel["body"], f_body, w - 12, 2):
        d.text((x + 6, by), ln, font=f_body, fill=INK_SOFT)
        by += 12
    return y + h

def draw_also(d, x, y, w, h):
    d.text((x, y), "ALSO \u2014 MORE OF FRIDAY 20 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=INK)
    _rule(d, x, y + 16, w, 1)
    col_w = (w - 14) // 2
    f_item = F(SANS, 8)
    f_num = F(SANS_B, 9)
    rows = (len(ALSO) + 1) // 2
    iy = y + 21
    for row in range(rows):
        for col in range(2):
            idx = row * 2 + col
            if idx >= len(ALSO):
                continue
            n, tag, text, src = ALSO[idx]
            cx = x + col * (col_w + 14)
            full = "%s \u2014 %s (%s)" % (tag, text, src)
            lines = wrap_n(full, f_item, col_w - 22, 2)
            d.text((cx, iy), "%d." % n, font=f_num, fill=RED_DARK)
            ly = iy
            for ln in lines:
                d.text((cx + 22, ly), ln, font=f_item, fill=INK)
                ly += 11
        iy += 24
    return iy


def draw_date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2,
                fill=(250, 242, 228))
    d.text((x + 8, y + 5), "DATE CHECK \u2014 WHAT IS NOT IN THIS PAPER",
           font=F(SANS_B, 11), fill=RED_DARK)
    f = F(SANS, 9)
    ly = y + 22
    for para in (DATE_CHECK_NOT_IN, DATE_CHECK_NOT_YET):
        for ln in wrap(para, f, w - 16):
            d.text((x + 8, ly), ln, font=f, fill=INK)
            ly += 11
        ly += 3
    return y + h


def draw_footer(d, x, y, w):
    _rule(d, x, y, w, 1)
    f = F(SANS, 9)
    line1 = ("Verified against primary sources \u00b7 Reuters \u00b7 IMD \u00b7 "
             "ESA \u00b7 Morningstar \u00b7 Sensor Tower \u00b7 BBC \u00b7 "
             "Formula1.com \u00b7 EORTC \u00b7 PBoC \u00b7 ONS \u00b7 "
             "straits.live \u00b7 CoinDesk \u00b7 CNN")
    line2 = ("All illustrations are original drawings made for this page "
             "\u00b7 Friday 20 November 2026 \u00b7 36 stories")
    for i, ln in enumerate((line1, line2)):
        tw = f.getlength(ln)
        d.text((x + (w - tw) / 2, y + 4 + i * 12), ln, font=f,
               fill=INK_SOFT)
    return y + 30


# ------------------------------------------------------------------- build
def build(out_path):
    # ---- content counts (hard checks) ----
    assert len(HEROES) == 3 and len(SMALL) == 10
    assert len(ALSO) == 23
    assert [p["n"] for p in HEROES] + [p["n"] for p in SMALL] == list(
        range(1, 14))
    assert [a[0] for a in ALSO] == list(range(14, 37))
    assert sum(n for _, n in REGIONS) == 36
    assert len(STATS) == 6
    assert set(PINS) == set(range(1, 14)) - {7}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx  # 976

    # paper edge
    d.rectangle([6, 6, W - 7, H - 7], outline=(120, 110, 88), width=1)
    y = 14
    y = draw_masthead(d, mx, y, cw)
    _rule(d, mx, y + 4, cw, 1)
    y += 10
    y = draw_stats(d, mx, y, cw)
    y += 5
    y = draw_regions(d, mx, y, cw)
    y += 6

    # heroes: 3 across
    hero_w = (cw - 2 * 8) // 3
    hero_h = 192
    for i, hero in enumerate(HEROES):
        draw_hero(img, d, mx + i * (hero_w + 8), y, hero_w, hero_h, hero)
    y += hero_h + 6

    # small panels: 2 rows of 5
    sm_w = (cw - 4 * 8) // 5
    sm_h = 116
    for row in range(2):
        for col in range(5):
            panel = SMALL[row * 5 + col]
            draw_small(img, d, mx + col * (sm_w + 8), y, sm_w, sm_h, panel)
        y += sm_h + 6

    # bottom: map + date check on the left, ALSO on the right
    left_w = 500
    right_x = mx + left_w + 14
    right_w = cw - left_w - 14
    map_h = 170
    d.text((mx, y), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    _rule(d, mx, y + 16, left_w, 1)
    draw_map(d, mx, y + 21, left_w, map_h - 21)
    dc_y = y + map_h + 6
    dc_h = 118
    draw_date_check(d, mx, dc_y, left_w, dc_h)
    also_end = draw_also(d, right_x, y, right_w, 0)
    bottom = max(dc_y + dc_h, also_end)
    assert bottom <= 966, "layout overflow: bottom=%d" % bottom

    fy = bottom + 8
    draw_footer(d, mx, fy, cw)
    assert fy + 30 <= 1012, "footer overflow"

    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
    print("wrote", target)
