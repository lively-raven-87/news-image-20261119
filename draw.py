#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page as a 1024x1024 PNG.

Everything is drawn with Pillow: a navy masthead, one lead story, four
story cards in a 2x2 grid, a ticker strip and a source footer. Run it and
it writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (247, 243, 234)
CARD_BG = (255, 255, 255)
EDGE = (205, 198, 184)
INK = (18, 24, 38)
BODY = (52, 58, 74)
MUTED = (90, 96, 110)
NAVY = (13, 27, 62)
GOLD = (198, 148, 52)
SCARLET = (178, 34, 34)
AMBER = (176, 92, 0)
TEAL = (14, 110, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


class Page:
    """A 1024x1024 newspaper page with a word-wrap helper."""

    def __init__(self):
        self.img = Image.new("RGB", CANVAS, PAPER)
        self.d = ImageDraw.Draw(self.img)

    def wrap(self, text, font, width):
        lines, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.d.textlength(trial, font=font) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def para(self, lines, font, x, y, fill, step):
        for line in lines:
            self.d.text((x, y), line, font=font, fill=fill)
            y += step
        return y

    def save(self):
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
        self.img.save(out, "PNG", optimize=True)
        print("saved", out, os.path.getsize(out), "bytes")


page = Page()
d = page.d

# ---------- masthead ----------
d.rectangle([0, 0, 1024, 118], fill=NAVY)
d.text((36, 16), "THE WORLD IN ONE IMAGE",
       font=load(SANS_B, 21), fill=GOLD)
d.text((36, 42), "WORLD NEWS", font=load(SERIF_B, 64), fill=(255, 255, 255))
date_w = d.textlength("19 NOVEMBER 2026", font=load(SANS_B, 26))
d.text((1024 - 36 - date_w, 24), "THURSDAY", font=load(SANS_B, 26),
       fill=(255, 255, 255))
d.text((1024 - 36 - date_w, 56), "19 NOVEMBER 2026", font=load(SANS_B, 26),
       fill=GOLD)
d.rectangle([0, 118, 1024, 124], fill=GOLD)

# ---------- lead story ----------
TOP, LEFT, RIGHT = 140, 28, 1024 - 28
d.rectangle([LEFT, TOP, RIGHT, TOP + 218], fill=CARD_BG, outline=EDGE, width=2)
d.text((52, TOP + 16), "SUMMIT IN SHENZHEN  •  PEACE DECLARATION",
       font=load(SANS_B, 20), fill=SCARLET)
headline = "Trump, Xi and Putin sign four-point 'Peace Declaration'"
y = TOP + 46
for line in page.wrap(headline, load(SERIF_B, 40), 1024 - 56 - 180):
    d.text((52, y), line, font=load(SERIF_B, 40), fill=INK)
    y += 46
standfirst = ("In 90 minutes in Shenzhen, the leaders pledged nuclear war must never be "
              "fought — no date for arms talks, no word on Ukraine or Iran.")
# The standfirst starts below the leader discs, so it takes the full width.
page.para(page.wrap(standfirst, load(SANS, 23), 1024 - 56 - 52),
          load(SANS, 23), 52, y + 8, BODY, 30)
disc_y = TOP + 118
for i, (tag, colour) in enumerate([("US", (60, 90, 160)),
                                   ("CN", (178, 34, 34)),
                                   ("RU", (40, 110, 90))]):
    x0 = (1024 - 118) - 150 + i * 78
    d.ellipse([x0, disc_y - 34, x0 + 62, disc_y + 28], fill=colour)
    tag_font = load(SANS_B, 22)
    d.text((x0 + 31 - d.textlength(tag, font=tag_font) / 2, disc_y - 14),
           tag, font=tag_font, fill=(255, 255, 255))

# ---------- story cards ----------
STORIES = [
    ("WORLD COURT", SCARLET,
     "ICJ: Myanmar guilty of Rohingya genocide",
     "The court ruled 9–6 the 2017 crackdown was genocide — ~10,000 killed. "
     "A first state verdict in the court's 80-year history."),
    ("GAMING", AMBER,
     "GTA VI launches worldwide; PSN buckles",
     "Out now on PS5 and Xbox, Metacritic 99. Sensor Tower estimates ~19m "
     "copies / $1.84B — an estimate, not official."),
    ("MARKETS", NAVY,
     "Anthropic IPO smashes records at $81.3B",
     "The biggest IPO ever, at a $1.5 trillion valuation. Shares jumped 34% "
     "on their Nasdaq debut."),
    ("POLITICS", TEAL,
     "Senate rejects Iran war-powers bid, 51–48",
     "The resolution failed 51–48. Denmark approved its Greenland defence "
     "deal 109–0 the same day."),
]


def card(x, y, kick, accent, head, body):
    w, h = 472, 236
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=EDGE, width=2)
    d.rectangle([x, y, x + 8, y + h], fill=accent)
    d.text((x + 26, y + 14), kick, font=load(SANS_B, 20), fill=accent)
    yy = y + 44
    for line in page.wrap(head, load(SERIF_B, 27), w - 52):
        d.text((x + 26, yy), line, font=load(SERIF_B, 27), fill=INK)
        yy += 33
    page.para(page.wrap(body, load(SANS, 21), w - 52),
              load(SANS, 21), x + 26, yy + 6, BODY, 27)


for i, story in enumerate(STORIES):
    card(28 + (i % 2) * (472 + 16), 374 + (i // 2) * (236 + 16), *story)

# ---------- ticker ----------
TICK_TOP = 878
TICKER_LINES = [
    "Crimea bridge hit a 3rd time in a week, rail halted  •  APEC adopts 'Shenzhen Outlook'",
    "Bangladesh unrest: 4 killed  •  589m children live in conflict zones",
]
d.rectangle([0, TICK_TOP, 1024, TICK_TOP + 96], fill=NAVY)
d.text((36, TICK_TOP + 12), "ALSO ON 19 NOVEMBER 2026",
       font=load(SANS_B, 19), fill=GOLD)
for row, line in enumerate(TICKER_LINES):
    d.text((36, TICK_TOP + 40 + row * 26), line,
           font=load(SANS, 19), fill=(235, 238, 244))

# ---------- footer ----------
d.text((36, 988),
       "Sources: Reuters, AP, AFP, Al Jazeera  •  The day's world news, Thursday 19 November 2026",
       font=load(SANS, 16), fill=MUTED)

page.save()
