#!/usr/bin/env python3
"""Draw the news-image-20261119 front page (1024 x 1024) with PIL.

Build helper: run it once to produce entry.png, then main.py (stdlib
only) copies that file to /output/entry.png. Run:
    python3 compose.py
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_SRC = os.path.join(HERE, "assets",
                        "media-generation-hero-summit-0-6e1dd226-20a5-4ee7-9ea0-e1fe15446bfc.webp")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 32
CW = W - 2 * MARGIN  # 960

PAPER = (253, 253, 248)
INK = (12, 12, 12)
GREY = (90, 90, 90)
RULE = (30, 30, 30)
ACCENT = (140, 20, 20)


def font(name, size):
    return ImageFont.truetype(
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif", s)             # noqa: E731
SERIF_I = lambda s: font("DejaVuSerif", s)  # no serif italic installed
SANS_B = lambda s: font("DejaVuSans-Bold", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans", s)               # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill=INK):
    draw.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")


def story(draw, x, y, w, kicker, headline, body):
    draw.text((x, y), kicker, font=SANS_B(15), fill=ACCENT)
    y += 22
    for line in wrap(draw, headline, SERIF_B(23), w):
        draw.text((x, y), line, font=SERIF_B(23), fill=INK)
        y += 28
    y += 2
    for line in wrap(draw, body, SERIF(15), w):
        draw.text((x, y), line, font=SERIF(15), fill=INK)
        y += 20
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------
    d.line([(MARGIN, 26), (W - MARGIN, 26)], fill=RULE, width=3)
    draw_center(d, 34, "THE WORLD IN ONE PAGE", SERIF_B(58))
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=RULE, width=2)
    draw_center(d, 116, "Thursday, 19 November 2026", SANS_B(20))
    d.line([(MARGIN, 146), (W - MARGIN, 146)], fill=RULE, width=1)

    # --- main headline + deck ------------------------------------
    draw_center(d, 156, "TRUMP, XI AND PUTIN HOLD", SERIF_B(44))
    draw_center(d, 206, "FIRST THREE-WAY SUMMIT", SERIF_B(44))
    deck = ("Seventy minutes at Kylin Villa, Shenzhen, produce a four-point "
            "\u201cDeclaration toward Peace\u201d \u2014 but no arms-control "
            "deal and no mention of Ukraine or Iran.")
    y = 258
    for line in wrap(d, deck, SERIF_I(20), CW):
        draw_center(d, y, line, SERIF_I(20), fill=(40, 40, 40))
        y += 26

    # --- hero illustration ---------------------------------------
    hero = Image.open(HERO_SRC).convert("RGB")
    hw, hh = 960, 272
    scaled = hero.resize((hw, int(hero.height * hw / hero.width)),
                         Image.LANCZOS)
    top = max(0, (scaled.height - hh) // 2 - 30)
    hero = scaled.crop((0, top, hw, top + hh))
    img.paste(hero, (MARGIN, 312))
    d.rectangle([MARGIN, 312, MARGIN + hw - 1, 312 + hh - 1],
                outline=RULE, width=2)
    caption = ("AI illustration: the three leaders meet in Shenzhen, with the "
               "flags of China, the United States and Russia behind them.")
    y = 592
    for line in wrap(d, caption, SERIF_I(14), CW):
        d.text((MARGIN, y), line, font=SERIF_I(14), fill=GREY)
        y += 19

    d.line([(MARGIN, 634), (W - MARGIN, 634)], fill=RULE, width=2)

    # --- four story blocks, 2 x 2 --------------------------------
    col_w = 468
    x2 = MARGIN + col_w + 24
    d.line([(W / 2, 650), (W / 2, 940)], fill=(180, 180, 180), width=1)
    d.line([(MARGIN, 798), (W - MARGIN, 798)], fill=(180, 180, 180), width=1)

    story(d, MARGIN, 646, col_w, "THE SUMMIT",
          "A first for the three, a modest deal",
          "The four points cover UN reform, refined-petroleum supply, "
          "immunity of state officials and talks on reducing nuclear risks. "
          "Putin later said the meeting set no ambitious goals.")
    story(d, x2, 646, col_w, "THE HAGUE",
          "ICJ: Myanmar committed genocide",
          "The court ruled Myanmar committed genocide against the Rohingya "
          "in 2017 operations in Rakhine State \u2014 the first time it has "
          "held a state responsible. Gambia brought the case in 2019; "
          "refugees in Bangladesh cheered.")
    story(d, MARGIN, 810, col_w, "RIYADH",
          "Missile hits Riyadh's tallest tower",
          "A suspected Houthi missile struck the PIF Tower, the city's "
          "tallest skyscraper and HQ of Saudi Arabia's sovereign wealth "
          "fund, blowing out windows across seven to eight floors. The "
          "Houthis said airstrikes in Yemen killed 15.")
    story(d, x2, 810, col_w, "MARKETS",
          "Anthropic's record IPO",
          "Anthropic began Nasdaq trading as ANT at $83, opened at $111.50 "
          "and topped $2 trillion in value \u2014 the largest IPO on "
          "record \u2014 as the S&P 500 fell 2.02% for a fifth straight "
          "loss on AI-valuation worries.")

    # --- ALSO strip ----------------------------------------------
    d.line([(MARGIN, 952), (W - MARGIN, 952)], fill=RULE, width=2)
    also = ("ALSO \u00b7 Ukraine hits the Crimean Bridge for a third time in "
            "four days \u00b7 Denmark ratifies the US Greenland security deal "
            "109\u20130 \u00b7 EU proposes a \u20ac45bn loan to Ukraine \u00b7 "
            "Van Gogh sells for a record $190.4m \u00b7 Nikkei drops 4.68%")
    y = 962
    for line in wrap(d, also, SANS(15), CW):
        d.text((MARGIN, y), line, font=SANS(15), fill=INK)
        y += 20

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {size} bytes")
    assert size <= 1048576, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
