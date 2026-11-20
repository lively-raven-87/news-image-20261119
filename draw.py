#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news summary image (1024x1024 PNG)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 24, 38)
NAVY = (13, 27, 62)
GOLD = (198, 148, 52)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREY = (90, 96, 110)
CARD = (255, 255, 255)
LINE = (205, 198, 184)

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_MAST = font("DejaVuSerif-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_LEAD = font("DejaVuSerif-Bold.ttf", 40)
F_LEADBODY = font("DejaVuSans.ttf", 23)
F_CARDHEAD = font("DejaVuSerif-Bold.ttf", 27)
F_CARDBODY = font("DejaVuSans.ttf", 21)
F_TICK = font("DejaVuSans-Bold.ttf", 19)
F_TICKB = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 16)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_lines(lines, fnt, x, y, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

# ---------- masthead ----------
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((36, 16), "THE WORLD IN ONE IMAGE", font=font("DejaVuSans-Bold.ttf", 21), fill=GOLD)
d.text((36, 42), "WORLD NEWS", font=F_MAST, fill=(255, 255, 255))
tw = d.textlength("19 NOVEMBER 2026", font=F_DATE)
d.text((W - 36 - tw, 24), "THURSDAY", font=F_DATE, fill=(255, 255, 255))
d.text((W - 36 - tw, 56), "19 NOVEMBER 2026", font=F_DATE, fill=GOLD)
d.rectangle([0, 118, W, 124], fill=GOLD)

# ---------- lead story ----------
ly = 140
d.rectangle([28, ly, W - 28, ly + 218], fill=CARD, outline=LINE, width=2)
d.text((52, ly + 16), "SUMMIT IN SHENZHEN  •  PEACE DECLARATION", font=F_KICK, fill=RED)
lead_head = "Trump, Xi and Putin sign four-point 'Peace Declaration'"
y = ly + 46
for ln in wrap(lead_head, F_LEAD, W - 56 - 180):
    d.text((52, y), ln, font=F_LEAD, fill=INK)
    y += 46
lead_body = ("In 90 minutes in Shenzhen, the leaders pledged nuclear war must never "
             "be fought — no date for arms talks, no word on Ukraine or Iran.")
# Body starts below the leader discs, so it can use the full card width.
y = draw_lines(wrap(lead_body, F_LEADBODY, W - 56 - 52), F_LEADBODY, 52, y + 8, (52, 58, 74), 30)
# three leader discs
cx, cy = W - 118, ly + 118
for i, (label, col) in enumerate([("US", (60, 90, 160)), ("CN", (178, 34, 34)), ("RU", (40, 110, 90))]):
    x0 = cx - 150 + i * 78
    d.ellipse([x0, cy - 34, x0 + 62, cy + 28], fill=col)
    tw2 = d.textlength(label, font=font("DejaVuSans-Bold.ttf", 22))
    d.text((x0 + 31 - tw2 / 2, cy - 14), label, font=font("DejaVuSans-Bold.ttf", 22), fill=(255, 255, 255))

# ---------- 2x2 story cards ----------
cards = [
    ("WORLD COURT", RED, "ICJ: Myanmar guilty of Rohingya genocide",
     "The court ruled 9–6 the 2017 crackdown was genocide — ~10,000 killed. "
     "A first state verdict in the court's 80-year history."),
    ("GAMING", (176, 92, 0), "GTA VI launches worldwide; PSN buckles",
     "Out now on PS5 and Xbox, Metacritic 99. Sensor Tower estimates ~19m "
     "copies / $1.84B — an estimate, not official."),
    ("MARKETS", NAVY, "Anthropic IPO smashes records at $81.3B",
     "The biggest IPO ever, at a $1.5 trillion valuation. Shares jumped 34% "
     "on their Nasdaq debut."),
    ("POLITICS", TEAL, "Senate rejects Iran war-powers bid, 51–48",
     "The resolution failed 51–48. Denmark approved its Greenland defence "
     "deal 109–0 the same day."),
]
cw, ch, gap = 472, 236, 16
x0, y0 = 28, 374
for i, (kick, col, head, body) in enumerate(cards):
    x = x0 + (i % 2) * (cw + gap)
    y = y0 + (i // 2) * (ch + gap)
    d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + 8, y + ch], fill=col)
    d.text((x + 26, y + 14), kick, font=F_KICK, fill=col)
    yy = y + 44
    for ln in wrap(head, F_CARDHEAD, cw - 52):
        d.text((x + 26, yy), ln, font=F_CARDHEAD, fill=INK)
        yy += 33
    draw_lines(wrap(body, F_CARDBODY, cw - 52), F_CARDBODY, x + 26, yy + 6, (52, 58, 74), 27)

# ---------- ticker ----------
ty = 878
d.rectangle([0, ty, W, ty + 96], fill=NAVY)
d.text((36, ty + 12), "ALSO ON 19 NOVEMBER 2026", font=F_TICK, fill=GOLD)
tick1 = "Crimea bridge hit a 3rd time in a week, rail halted  •  APEC adopts 'Shenzhen Outlook'"
tick2 = "Bangladesh unrest: 4 killed  •  589m children live in conflict zones"
d.text((36, ty + 40), tick1, font=F_TICKB, fill=(235, 238, 244))
d.text((36, ty + 66), tick2, font=F_TICKB, fill=(235, 238, 244))

# ---------- footer ----------
d.text((36, 988), "Sources: Reuters, AP, AFP, Al Jazeera  •  The day's world news, Thursday 19 November 2026",
       font=F_FOOT, fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
