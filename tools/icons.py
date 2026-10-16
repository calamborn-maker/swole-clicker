#!/usr/bin/env python3
"""Swole Clicker icon set — hand-drawn SVG symbols in one style (48×48, chunky dark outline, flat game palette).

    python3 tools/icons.py            # rewrites the sprite between the ICONS markers in index.html
    python3 tools/icons.py --sheet F  # also writes a contact sheet HTML to F (for review)

Use in the game:  ic('pushup')  →  <svg class="ic"><use href="#i-pushup"/></svg>
"""
import re, sys, pathlib

O = '#1b1408'          # outline
SW = 2.6               # outline width
GOLD, GOLD2 = '#ffcc33', '#e0a000'
STEEL, STEEL2, IRON = '#b8c2d1', '#6d7789', '#2f3542'
RED, ORANGE, BLUE, BLUE2 = '#ff4d5e', '#ff8a3d', '#45a0ff', '#2a6fd6'
GREEN, GREEN2, PURPLE, PURPLE2 = '#4fd47e', '#22a356', '#a979ff', '#7445d6'
SKIN, SKIN2, WHITE, BROWN, BROWN2, PINK = '#f4c99f', '#d99a68', '#f6f2ea', '#b07a45', '#7d5230', '#ff8fb1'


def sh(tag, fill, **a):
    """filled shape with the standard outline"""
    attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<{tag} {attrs} fill="{fill}" stroke="{O}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"/>'


def ln(d, col=O, w=SW):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def fig(*limbs, w=5.4, col=SKIN):
    """outlined pictogram limbs: every outline first, then every fill, so joints stay clean"""
    o = ''.join(ln(d, O, w + 3.4) for d in limbs)
    f = ''.join(ln(d, col, w) for d in limbs)
    return o + f


def head(cx, cy, r=4.6, col=SKIN):
    return sh('circle', col, cx=cx, cy=cy, r=r)


def shine(d):  # small white highlight stroke
    return ln(d, 'rgba(255,255,255,.55)', 2)


def plate(cx, cy, rx, ry, col=IRON):
    return sh('rect', col, x=cx - rx, y=cy - ry, width=rx * 2, height=ry * 2, rx=min(rx, ry) * .6)


def barbell(y, x1=4, x2=44, pr=8, col=IRON):
    return (sh('rect', STEEL, x=x1 + 2, y=y - 1.6, width=x2 - x1 - 4, height=3.2, rx=1.6)
            + plate(x1 + 4, y, 2.6, pr, col) + plate(x2 - 4, y, 2.6, pr, col)
            + plate(x1 + 9, y, 2.2, pr * .72, col) + plate(x2 - 9, y, 2.2, pr * .72, col))


def dumbbell(cx, cy, ang=0, s=1.0, col=IRON):
    g = (sh('rect', STEEL, x=-11 * s, y=-2 * s, width=22 * s, height=4 * s, rx=2 * s)
         + sh('rect', col, x=-15 * s, y=-7 * s, width=7 * s, height=14 * s, rx=2.4 * s)
         + sh('rect', col, x=8 * s, y=-7 * s, width=7 * s, height=14 * s, rx=2.4 * s)
         + shine(f'M{-13 * s} {-4 * s}v{4 * s}') + shine(f'M{10 * s} {-4 * s}v{4 * s}'))
    return f'<g transform="translate({cx} {cy}) rotate({ang})">{g}</g>'


def floor(y=43, x1=5, x2=43):
    return ln(f'M{x1} {y}H{x2}', O, 3)


I = {}

# ---------------------------------------------------------------- shop items: tap gear
I['pushup'] = floor(41) + fig('M14 27L39 33', 'M17 28L16 39', 'M39 33L42 39', w=5.6) + head(10, 24)
I['curls'] = (sh('rect', STEEL, x=8, y=21.5, width=32, height=5, rx=2.5)
              + sh('path', STEEL, d='M15 21.5c3 0 4-3 6-3s3 3 3 3 1-3 3-3 3 3 6 3v5c-3 0-4 3-6 3s-3-3-3-3-1 3-3 3-3-3-6-3z')
              + plate(7, 24, 4, 12, RED) + plate(41, 24, 4, 12, RED) + plate(2.6, 24, 2.4, 8) + plate(45.4, 24, 2.4, 8)
              + shine('M6 16v8') + shine('M40 16v8'))
I['squats'] = floor(43) + fig('M20 18L25 29', 'M25 29L35 31', 'M35 31L33 41', 'M20 18L32 17', w=5.6) + head(18, 12) + barbell(16, 8, 40, 6)
I['grip'] = (sh('path', RED, d='M10 40l9-19c1-2 4-2 4 1l-6 20c-1 2-6 1-7-2z')
             + sh('path', RED, d='M38 40l-9-19c-1-2-4-2-4 1l6 20c1 2 6 1 7-2z')
             + ln('M19 16c-2-4 0-9 5-9s7 5 5 9', O, 4.6) + ln('M19 16c-2-4 0-9 5-9s7 5 5 9', STEEL, 2.2)
             + shine('M13 37l5-11') + shine('M35 37l-5-11'))
I['pullup'] = (sh('rect', STEEL, x=4, y=7, width=40, height=4, rx=2) + sh('rect', IRON, x=4, y=5, width=4, height=38, rx=1.5)
               + sh('rect', IRON, x=40, y=5, width=4, height=38, rx=1.5)
               + fig('M18 9L19 20', 'M30 9L29 20', 'M24 21L24 32', 'M24 32L21 41', 'M24 32L27 41', 'M19 20L29 20', w=5) + head(24, 15.5, 4.2))
I['press'] = (fig('M24 26L24 38', 'M24 38L20 45', 'M24 38L28 45', 'M17 9L16 21L24 25L32 21L31 9', w=5) + head(24, 19.5, 4.2)
              + barbell(8, 5, 43, 6))
I['abroll'] = (sh('circle', IRON, cx=24, cy=26, r=13) + sh('circle', RED, cx=24, cy=26, r=7.5) + sh('circle', STEEL, cx=24, cy=26, r=2.6)
               + sh('rect', STEEL, x=3, y=24, width=8, height=4, rx=2) + sh('rect', STEEL, x=37, y=24, width=8, height=4, rx=2)
               + sh('rect', '#3a3f4c', x=2, y=22, width=4, height=8, rx=1.8) + sh('rect', '#3a3f4c', x=42, y=22, width=4, height=8, rx=1.8)
               + shine('M15 18a12 12 0 0 1 8-4'))
I['eggs'] = (sh('path', '#c9b391', d='M4 28h40l-4 12H8z') + ''.join(sh('ellipse', WHITE, cx=x, cy=24, rx=5, ry=6.5) for x in (11, 21, 31))
             + sh('ellipse', '#fff8ec', cx=38, cy=24, rx=5, ry=6.5) + ln('M9 21a3 3 0 0 1 2-3', 'rgba(0,0,0,.12)', 1.6)
             + ln('M12 33v5M20 33v5M28 33v5M36 33v5', 'rgba(0,0,0,.25)', 1.6))
I['medball'] = (sh('circle', BROWN, cx=24, cy=25, r=17) + ln('M9 18c10 5 20 5 30 0', O, 2.2) + ln('M9 32c10-5 20-5 30 0', O, 2.2)
                + ln('M24 8v34', O, 2.2) + shine('M14 13a15 15 0 0 1 7-4'))
I['clap'] = ('<g transform="rotate(-18 17 28)">' + sh('path', SKIN, d='M10 44V22a3 3 0 0 1 6 0v-6a3 3 0 0 1 6 0v28z') + sh('path', SKIN, d='M10 30l-4-5a3 3 0 0 1 5-3l3 4z') + '</g>'
             + '<g transform="rotate(18 31 28)">' + sh('path', SKIN, d='M38 44V22a3 3 0 0 0-6 0v-6a3 3 0 0 0-6 0v28z') + sh('path', SKIN, d='M38 30l4-5a3 3 0 0 0-5-3l-3 4z') + '</g>'
             + ln('M24 9V3M15 11l-3-5M33 11l3-5', ORANGE, 3))
I['bands'] = (ln('M14 12C2 22 6 38 24 38S46 22 34 12', O, 8.4) + ln('M14 12C2 22 6 38 24 38S46 22 34 12', GREEN, 5)
              + sh('rect', IRON, x=8, y=5, width=12, height=7, rx=3) + sh('rect', IRON, x=28, y=5, width=12, height=7, rx=3))

# ---------------------------------------------------------------- shop items: idle gear
I['shake'] = (sh('path', BLUE, d='M14 16h20l-2.5 26a3 3 0 0 1-3 3h-9a3 3 0 0 1-3-3z') + sh('rect', WHITE, x=12, y=10, width=24, height=7, rx=2.5)
              + sh('rect', IRON, x=20, y=4, width=8, height=6, rx=1.5) + ln('M16 26h16', 'rgba(255,255,255,.5)', 2)
              + sh('path', '#fff', d='M19 31h10l-1 6h-8z') + shine('M17 19l1.5 18'))
I['dumbbell'] = dumbbell(24, 24, -30, 1.15)
I['bench'] = (sh('rect', IRON, x=8, y=4, width=4, height=30, rx=1.5) + sh('rect', IRON, x=36, y=4, width=4, height=30, rx=1.5)
              + barbell(10, 3, 45, 7) + sh('rect', RED, x=12, y=26, width=24, height=6, rx=2.5)
              + sh('rect', IRON, x=15, y=32, width=4, height=11, rx=1) + sh('rect', IRON, x=29, y=32, width=4, height=11, rx=1))
I['dips'] = (sh('rect', IRON, x=9, y=12, width=4, height=32, rx=1.5) + sh('rect', IRON, x=35, y=12, width=4, height=32, rx=1.5)
             + sh('rect', STEEL, x=4, y=12, width=16, height=4.5, rx=2.2) + sh('rect', STEEL, x=28, y=12, width=16, height=4.5, rx=2.2)
             + sh('rect', IRON, x=6, y=40, width=36, height=4, rx=1.5) + fig('M24 21L24 32', 'M24 32L22 40', w=4.6) + head(24, 16.5, 3.8)
             + fig('M17 14L20 22L24 23', 'M31 14L28 22L24 23', w=4.2))
I['latpull'] = (sh('rect', IRON, x=6, y=4, width=4, height=40, rx=1.5) + sh('rect', IRON, x=6, y=4, width=36, height=4, rx=1.5)
                + sh('circle', STEEL, cx=38, cy=10, r=3.4) + ln('M38 13V22', O, 1.8) + ln('M24 8V17', O, 1.8)
                + sh('path', STEEL, d='M12 17h24l2 4H10z') + sh('rect', IRON, x=33, y=26, width=10, height=17, rx=1.5)
                + ln('M34 30h8M34 34h8M34 38h8', STEEL, 1.8) + sh('rect', RED, x=13, y=35, width=14, height=5, rx=2))
I['shrugbar'] = (sh('path', STEEL, d='M14 15h20l7 9-7 9H14l-7-9z') + sh('path', '#1d2230', d='M17 19h14l4 5-4 5H17l-4-5z')
                 + plate(4.5, 24, 2.4, 9) + plate(43.5, 24, 2.4, 9) + sh('rect', SKIN2, x=19, y=21, width=3, height=6, rx=1)
                 + sh('rect', SKIN2, x=26, y=21, width=3, height=6, rx=1))
I['legpress'] = (sh('path', IRON, d='M10 40L36 8l4 3L14 43z') + sh('rect', BLUE2, x=3, y=33, width=14, height=6, rx=2) + sh('rect', BLUE2, x=3, y=24, width=6, height=12, rx=2)
                 + '<g transform="rotate(-51 30 18)">' + sh('rect', STEEL, x=20, y=13, width=20, height=6, rx=2) + plate(34, 11, 3, 7, RED) + '</g>'
                 + ln('M3 44h40', O, 3))
I['lateral'] = (fig('M24 22L24 33', 'M24 33L20 43', 'M24 33L28 43', 'M24 22L10 19', 'M24 22L38 19', w=5) + head(24, 15.5, 4.4)
                + dumbbell(7, 18.5, 90, .42) + dumbbell(41, 18.5, 90, .42))
I['hipthrust'] = (sh('rect', BLUE2, x=2, y=20, width=11, height=8, rx=2) + sh('rect', IRON, x=5, y=28, width=4, height=15, rx=1) + floor(43, 2, 46)
                  + fig('M10 22L26 21', 'M26 21L36 28', 'M36 28L37 42', w=5.8) + head(7, 16, 4.2)
                  + sh('circle', RED, cx=26, cy=14, r=8) + sh('circle', STEEL, cx=26, cy=14, r=2.4))
I['crunch'] = (sh('rect', BLUE2, x=3, y=37, width=42, height=5, rx=2) + fig('M24 35L33 24', 'M33 24L41 35', 'M24 35L15 27', w=5.8) + head(12, 22, 4.4)
               + fig('M15 26L11 18L9 22', w=4) + ln('M27 13a10 10 0 0 0-9 3', ORANGE, 3) + sh('path', ORANGE, d='M19 11l-3 7 6 0z'))
I['legcurl'] = (sh('rect', BLUE2, x=4, y=22, width=30, height=7, rx=3) + sh('rect', IRON, x=7, y=29, width=4, height=14, rx=1)
                + sh('rect', IRON, x=27, y=29, width=4, height=14, rx=1) + sh('path', STEEL2, d='M34 25l7-10 3 2-7 10z')
                + sh('circle', RED, cx=41, cy=14, r=4.6) + sh('circle', STEEL, cx=36, cy=26, r=3) + ln('M4 43h40', O, 3))
I['calf'] = (sh('path', IRON, d='M24 36h20v7H24z') + ln('M3 43h41', O, 3) + fig('M20 5L22 27', w=8) + sh('path', SKIN, d='M17 26c4-2 8-1 10 2l7 7c1 2 0 3-2 3h-6c-3 0-5-1-7-3z')
             + ln('M8 30V12', GREEN, 3.4) + sh('path', GREEN, d='M3 15l5-8 5 8z'))
I['deadlift'] = (sh('rect', BROWN, x=2, y=37, width=44, height=7, rx=1.5) + ln('M10 40.5h28', BROWN2, 2) + barbell(27, 3, 45, 11, RED)
                 + ln('M2 37h44', O, 2.4))
I['rowing'] = (sh('rect', STEEL2, x=6, y=33, width=38, height=4, rx=2) + sh('circle', IRON, cx=10, cy=28, r=8.5) + sh('circle', STEEL, cx=10, cy=28, r=3)
               + sh('rect', BLUE2, x=27, y=28, width=10, height=5, rx=2) + sh('rect', IRON, x=40, y=37, width=4, height=6, rx=1)
               + sh('rect', IRON, x=7, y=37, width=4, height=6, rx=1) + ln('M18 28c4-1 7 0 9 3', O, 1.8) + sh('rect', RED, x=16, y=22, width=4, height=10, rx=2))
I['woodchop'] = (sh('rect', IRON, x=37, y=3, width=7, height=40, rx=2) + sh('circle', STEEL, cx=40.5, cy=8, r=3.2)
                 + ln('M38 9L15 34', O, 1.8) + sh('path', RED, d='M10 30l7 7-4 4-7-7z')
                 + ln('M12 18a20 20 0 0 0 4 20', ORANGE, 3) + sh('path', ORANGE, d='M12 15l-3 5 6 0z'))
I['flyes'] = (sh('rect', IRON, x=3, y=4, width=6, height=39, rx=2) + sh('rect', IRON, x=39, y=4, width=6, height=39, rx=2)
              + sh('circle', STEEL, cx=6, cy=10, r=2.8) + sh('circle', STEEL, cx=42, cy=10, r=2.8)
              + ln('M8 11L20 27', O, 1.8) + ln('M40 11L28 27', O, 1.8)
              + sh('rect', RED, x=17, y=26, width=6, height=8, rx=2) + sh('rect', RED, x=25, y=26, width=6, height=8, rx=2)
              + ln('M24 18v-6M20 19l-2-4M28 19l2-4', GOLD, 2.4))
I['gainer'] = (sh('path', PURPLE, d='M9 15h30v25a4 4 0 0 1-4 4H13a4 4 0 0 1-4-4z') + sh('rect', IRON, x=8, y=8, width=32, height=8, rx=2.5)
               + sh('rect', GOLD, x=12, y=21, width=24, height=14, rx=2) + ln('M16 26h16M16 30h10', O, 2.2)
               + shine('M12 18v20'))
I['trainer'] = (sh('rect', BROWN, x=8, y=7, width=24, height=34, rx=3) + sh('rect', WHITE, x=11, y=12, width=18, height=26, rx=1.5)
                + sh('rect', STEEL, x=15, y=4, width=10, height=6, rx=2) + ln('M14 18l2 2 3-4M14 25l2 2 3-4M14 32l2 2 3-4', GREEN2, 2.2)
                + ln('M22 19h5M22 26h5M22 33h5', STEEL2, 2) + sh('path', GOLD, d='M32 30h7a5 5 0 1 1-5 6h-2z') + sh('circle', '#1d2230', cx=37, cy=35, r=1.6))
I['squatrack'] = (sh('rect', IRON, x=5, y=3, width=5, height=40, rx=1.5) + sh('rect', IRON, x=38, y=3, width=5, height=40, rx=1.5)
                  + sh('rect', IRON, x=5, y=3, width=38, height=4, rx=1.5) + sh('rect', STEEL2, x=3, y=40, width=42, height=4, rx=1.5)
                  + barbell(19, 1, 47, 8, RED) + ln('M10 15h3M35 15h3', O, 2.4))
I['steroids'] = (sh('rect', GREEN, x=15, y=12, width=18, height=30, rx=5) + sh('rect', IRON, x=17, y=5, width=14, height=8, rx=2)
                 + sh('path', GOLD, d='M26 18l-6 10h5l-3 9 8-12h-5l3-7z') + shine('M19 16v20')
                 + ln('M10 10l-3-3M38 10l3-3M8 24H4M40 24h4', GREEN, 2.4))
I['chef'] = (sh('path', WHITE, d='M13 27c-6-1-8-8-4-12 2-3 6-3 8-2 1-5 6-7 10-5 3-3 9-2 11 2 4 0 7 4 5 9-1 4-4 6-7 6v4H13z')
             + sh('rect', WHITE, x=13, y=29, width=24, height=9, rx=2) + ln('M19 31v5M25 31v5M31 31v5', 'rgba(0,0,0,.18)', 1.8)
             + sh('path', RED, d='M4 41h40v3H4z'))
I['gym'] = (sh('path', '#4b5568', d='M6 18h36v26H6z') + sh('path', RED, d='M3 19L24 6l21 13z') + sh('rect', '#2a6fd6', x=19, y=31, width=10, height=13, rx=1)
            + sh('rect', '#9ecbff', x=10, y=24, width=7, height=6, rx=1) + sh('rect', '#9ecbff', x=31, y=24, width=7, height=6, rx=1)
            + dumbbell(24, 15, 0, .42))
I['lab'] = (sh('path', '#e6ecf6', d='M19 5h10v11l10 20a5 5 0 0 1-4.5 7h-21A5 5 0 0 1 9 36l10-20z') + sh('path', PURPLE, d='M14 28h20l4.5 9a3 3 0 0 1-2.7 4H12.2a3 3 0 0 1-2.7-4z')
            + ln('M17 5h14', O, 3) + sh('circle', '#fff', cx=21, cy=34, r=1.8) + sh('circle', '#fff', cx=27, cy=31, r=1.3) + shine('M21 9v8'))
I['clinic'] = (ln('M15 4c0 10 18 14 18 20S15 34 15 44', O, 6) + ln('M33 4c0 10-18 14-18 20s18 10 18 20', O, 6)
               + ln('M15 4c0 10 18 14 18 20S15 34 15 44', BLUE, 3) + ln('M33 4c0 10-18 14-18 20s18 10 18 20', PINK, 3)
               + ln('M18 10h12M22 16h4M22 32h4M18 38h12', O, 2.2))
I['sponsor'] = (sh('path', ORANGE, d='M8 19l22-11v32L8 29z') + sh('rect', IRON, x=4, y=18, width=6, height=12, rx=2)
                + sh('path', IRON, d='M12 30l4 11h5l-3-10z') + ln('M35 17l5-3M36 24h6M35 31l5 3', GOLD, 3) + shine('M27 13v20'))
I['olympia'] = (sh('path', GOLD, d='M14 6h20v9c0 7-4 12-10 12S14 22 14 15z') + ln('M14 10H8c0 6 3 9 7 9', O, 2.8) + ln('M34 10h6c0 6-3 9-7 9', O, 2.8)
                + sh('rect', GOLD2, x=21, y=27, width=6, height=6) + sh('rect', BROWN, x=13, y=33, width=22, height=10, rx=2)
                + sh('path', '#fff6c7', d='M24 10l1.6 3.4 3.7.4-2.8 2.5.8 3.7-3.3-1.9-3.3 1.9.8-3.7-2.8-2.5 3.7-.4z')
                + shine('M17 9v6'))

# ---------------------------------------------------------------- UI: tabs, badges, buttons
I['tab-shop'] = (sh('path', ORANGE, d='M7 16h34l-3 27H10z') + ln('M17 16v-4a7 7 0 0 1 14 0v4', O, 3) + dumbbell(24, 30, 0, .5))
I['tab-upgrades'] = (sh('path', GOLD, d='M24 4l5.6 11.6 12.6 1.6-9.3 8.7 2.4 12.6L24 32.3l-11.3 6.2 2.4-12.6-9.3-8.7 12.6-1.6z')
                     + sh('path', GREEN, d='M24 15l6 7h-4v7h-4v-7h-4z'))
I['tab-stage'] = (sh('rect', STEEL, x=17, y=4, width=14, height=21, rx=7) + ln('M19 11h10M19 15h10M19 19h10', STEEL2, 1.8)
                  + ln('M12 20a12 12 0 0 0 24 0', O, 3) + ln('M24 32v8M16 42h16', O, 3.2))
I['tab-rivals'] = (sh('path', RED, d='M6 20c0-7 4-11 10-11h4c4 0 6 3 6 7v6c0 3-2 5-5 5h-9l-1 8H8z') + sh('rect', WHITE, x=6, y=29, width=12, height=6, rx=1.5)
                   + sh('path', BLUE, d='M42 26c0 7-4 11-10 11h-4c-4 0-6-3-6-7v-6c0-3 2-5 5-5h9l1-8h3z'))
I['tab-ach'] = (sh('path', BLUE2, d='M14 3h8l4 14h-8zM26 3h8l-4 14h-8z') + sh('circle', GOLD, cx=24, cy=31, r=12) + sh('circle', GOLD2, cx=24, cy=31, r=7)
                + sh('path', '#fff6c7', d='M24 26l1.5 3 3.3.4-2.4 2.3.6 3.3-3-1.6-3 1.6.6-3.3-2.4-2.3 3.3-.4z'))
I['tab-quests'] = (sh('circle', RED, cx=22, cy=26, r=17) + sh('circle', WHITE, cx=22, cy=26, r=11.5) + sh('circle', RED, cx=22, cy=26, r=6)
                   + ln('M22 26L41 7', O, 3.2) + sh('path', GOLD, d='M36 5l7-2-2 7-4 1z'))
I['tab-locker'] = (sh('rect', '#4f7fd1', x=10, y=3, width=28, height=42, rx=3) + ln('M15 9h18M15 13h18M15 17h18', '#2c4f8f', 2)
                   + sh('rect', STEEL, x=29, y=24, width=4, height=8, rx=1.5) + ln('M24 3v42', O, 2))
I['tab-stats'] = (ln('M6 6v36h36', O, 3.2) + sh('rect', BLUE, x=11, y=26, width=7, height=14, rx=1.5) + sh('rect', GREEN, x=21, y=18, width=7, height=22, rx=1.5)
                  + sh('rect', GOLD, x=31, y=9, width=7, height=31, rx=1.5))
I['gains'] = (ln('M6 33H30', O, 14.4) + ln('M30 33L35 12', O, 12.4)
              + sh('path', SKIN, d='M9 28c1-8 7-12 13-12s11 4 12 11z') + sh('circle', SKIN, cx=35, cy=9, r=6.5)
              + ln('M6 33H30', SKIN, 11) + ln('M30 33L35 12', SKIN, 9)
              + '<path d="M10.4 28c1.2-7 6.5-10.6 11.6-10.6s9.8 3.4 10.7 10.6z" fill="' + SKIN + '"/>' + '<circle cx="35" cy="9" r="5.2" fill="' + SKIN + '"/>'
              + ln('M15 25c3-4 10-4 13 0', SKIN2, 2) + ln('M30 37c2 0 3-1 4-2', SKIN2, 2))
I['trophy'] = I['olympia']
I['gear'] = (sh('path', STEEL, d='M21 4h6l1 5 4 2 4-3 4 4-3 4 2 4 5 1v6l-5 1-2 4 3 4-4 4-4-3-4 2-1 5h-6l-1-5-4-2-4 3-4-4 3-4-2-4-5-1v-6l5-1 2-4-3-4 4-4 4 3 4-2z')
             + sh('circle', IRON, cx=24, cy=24, r=6))
I['turn'] = (ln('M37 18A14 14 0 0 0 11 20', O, 7) + ln('M11 30a14 14 0 0 0 26-2', O, 7) + ln('M37 18A14 14 0 0 0 11 20', BLUE, 3.6) + ln('M11 30a14 14 0 0 0 26-2', BLUE, 3.6)
             + sh('path', BLUE, d='M33 12l9 2-4 8z') + sh('path', BLUE, d='M15 36l-9-2 4-8z'))
I['video'] = (sh('rect', '#3a3f4c', x=4, y=10, width=40, height=28, rx=4) + sh('rect', '#9ecbff', x=8, y=14, width=32, height=20, rx=2)
              + sh('path', RED, d='M20 18l10 6-10 6z') + ln('M18 42h12', O, 3))
I['bolt'] = sh('path', GOLD, d='M27 3L9 27h12l-4 18 22-26H27z')
I['muscle'] = I['gains']
I['lock'] = (sh('rect', GOLD, x=10, y=21, width=28, height=22, rx=3) + ln('M16 21v-6a8 8 0 0 1 16 0v6', O, 3.4)
             + sh('circle', IRON, cx=24, cy=31, r=3) + ln('M24 33v4', O, 2.6))
I['question'] = sh('circle', '#3a4150', cx=24, cy=24, r=18) + ln('M18 18a6 6 0 1 1 8 6c-2 1-2 3-2 5', '#cfd6e4', 3.6) + sh('circle', '#cfd6e4', cx=24, cy=36, r=2)


def sprite():
    syms = ''.join(f'<symbol id="i-{k}" viewBox="0 0 48 48">{v}</symbol>' for k, v in I.items())
    return f'<svg id="icons" width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>'


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    p = root / 'index.html'
    s = p.read_text()
    new = '<!--ICONS-->' + sprite() + '<!--/ICONS-->'
    if '<!--ICONS-->' in s:
        s = re.sub(r'<!--ICONS-->.*?<!--/ICONS-->', lambda m: new, s, flags=re.S)
    else:
        s = s.replace('<body>', '<body>\n' + new, 1)
    p.write_text(s)
    print(f'{len(I)} icons → index.html')
    if '--sheet' in sys.argv:
        out = sys.argv[sys.argv.index('--sheet') + 1]
        cells = ''.join(f'<div class="c"><svg width="64" height="64"><use href="#i-{k}"/></svg><svg width="28" height="28"><use href="#i-{k}"/></svg><span>{k}</span></div>' for k in I)
        pathlib.Path(out).write_text(f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#151a24;font:12px sans-serif;color:#cfd6e4">'
                                     f'{sprite()}<div style="display:grid;grid-template-columns:repeat(9,1fr);gap:6px;padding:8px">'
                                     f'<style>.c{{background:#1e2533;border:1px solid #2c3346;border-radius:8px;padding:6px;display:flex;flex-direction:column;align-items:center;gap:3px}}</style>{cells}</div></body>')


if __name__ == '__main__':
    main()
