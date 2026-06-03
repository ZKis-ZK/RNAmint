"""
Generate animated GIFs for:
  1. rnamint_fresh_ideas.gif  — typewriter + leaf sway
  2. kis_keep_it_simple.gif   — spinning sparkle + KIS text
Run: python3 make_badge_gifs.py
"""

import math, os
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

# ── Colours ──────────────────────────────────────────────────────────
BRAND       = (102, 168, 158)   # #66a89e
BRAND_DEEP  = ( 74, 136, 128)   # #4a8880
BG_MINT     = (236, 248, 245)   # light mint background
BORDER_MINT = (178, 214, 207)   # badge border
WHITE       = (255, 255, 255)

# ── Fonts ─────────────────────────────────────────────────────────────
FONT_ROUND  = '/System/Library/Fonts/SFNSRounded.ttf'

OUT_DIR = '/Users/zoltan/RNAmint/images'


# ══════════════════════════════════════════════════════════════════════
# Helper: draw one badge frame on a white RGBA canvas
# ══════════════════════════════════════════════════════════════════════
def make_frame(canvas_w, canvas_h,
               emoji, emoji_angle,
               text, text_color, font,
               bg, border,
               pad_x=18, pad_y=10,
               emoji_size=26, radius=28):
    """Return a PIL RGBA Image for one animation frame."""
    img = Image.new('RGBA', (canvas_w, canvas_h), (*WHITE, 255))

    # --- measure full badge width from complete text -----------------
    dummy = Image.new('RGBA', (1, 1))
    with Pilmoji(dummy) as p:
        tw, th = p.getsize(text, font=font)

    badge_w = pad_x + emoji_size + 8 + tw + pad_x
    badge_h = canvas_h - 2 * pad_y
    bx, by  = (canvas_w - badge_w) // 2, pad_y   # centred

    # Badge background + border
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [bx, by, bx + badge_w, by + badge_h],
        radius=radius, fill=(*bg, 255),
        outline=(*border, 255), width=3
    )

    # Emoji (pre-rendered into a small tile, then rotated)
    tile = Image.new('RGBA', (emoji_size + 8, emoji_size + 8), (0, 0, 0, 0))
    efont = ImageFont.truetype(FONT_ROUND, emoji_size)
    with Pilmoji(tile) as p:
        p.text((0, 2), emoji, font=efont, fill=(*BRAND_DEEP, 255))
    if emoji_angle != 0:
        tile = tile.rotate(-emoji_angle, resample=Image.BICUBIC, expand=False)
    ex = bx + pad_x
    ey = by + (badge_h - tile.height) // 2
    img.alpha_composite(tile, (ex, ey))

    # Text
    tx = ex + emoji_size + 10
    ty = by + (badge_h - th) // 2
    with Pilmoji(img) as p:
        p.text((tx, ty), text, font=font, fill=(*text_color, 255))

    return img.convert('RGB')  # GIF needs RGB (no alpha)


# ══════════════════════════════════════════════════════════════════════
# GIF 1 — 🌿 RNA MINT — Fresh ideas (typewriter + leaf sway + glow)
# ══════════════════════════════════════════════════════════════════════
def make_fresh_ideas():
    W, H   = 520, 62
    font   = ImageFont.truetype(FONT_ROUND, 22)
    msg    = 'RNA MINT — Fresh ideas'
    frames, durs = [], []

    SWAY_PERIOD = 30   # frames for one full sway cycle

    def sway_angle(f):
        return 12 * math.sin(2 * math.pi * f / SWAY_PERIOD)

    sf = 0  # sway frame counter

    # Phase 1: short delay before typing starts
    for _ in range(6):
        frames.append(make_frame(W, H, '🌿', sway_angle(sf), '',
                                 BRAND_DEEP, font, BG_MINT, BORDER_MINT))
        durs.append(80)
        sf += 1

    # Phase 2: type one character at a time
    for i in range(1, len(msg) + 1):
        frames.append(make_frame(W, H, '🌿', sway_angle(sf), msg[:i],
                                 BRAND_DEEP, font, BG_MINT, BORDER_MINT))
        durs.append(70)
        if i % 2 == 0:
            sf += 1

    # Phase 3: hold with glow pulse (2 sway cycles)
    for i in range(SWAY_PERIOD * 2):
        glow = int(22 * abs(math.sin(math.pi * i / SWAY_PERIOD)))
        border = (
            max(0, BORDER_MINT[0] - glow),
            min(255, BORDER_MINT[1] + glow // 2),
            min(255, BORDER_MINT[2] + glow // 2),
        )
        frames.append(make_frame(W, H, '🌿', sway_angle(sf + i), msg,
                                 BRAND_DEEP, font, BG_MINT, border))
        durs.append(100)

    path = os.path.join(OUT_DIR, 'rnamint_fresh_ideas.gif')
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durs, loop=0, optimize=False)
    print(f'  ✓  {path}  ({len(frames)} frames)')


# ══════════════════════════════════════════════════════════════════════
# GIF 2 — ✨ KIS — Keep It Simple (spinning sparkle)
# ══════════════════════════════════════════════════════════════════════
def make_kis():
    W, H   = 340, 62
    font   = ImageFont.truetype(FONT_ROUND, 22)
    # Show two parts: "KIS" badge alone, then expand to "KIS — Keep It Simple"
    short  = 'KIS'
    full   = 'KIS — Keep It Simple'
    frames, durs = [], []

    # Spin profile matching CSS:
    # 0%→50%: rotate 0→360; 50%→90%: rotate 360→360; 90%→100%: snap back to 0
    # We map this to N_SPIN frames at 60ms each → total ~4s cycle
    N_SPIN = 66   # frames per full cycle

    def spin_angle(f):
        t = (f % N_SPIN) / N_SPIN          # 0..1
        if t < 0.5:
            return 360 * (t / 0.5)         # 0→360 in first half
        elif t < 0.9:
            return 360.0                   # hold at 360
        else:
            return 360 * (1 - (t - 0.9) / 0.1)  # snap back

    sf = 0  # spin frame

    # Phase 1: short badge ("KIS") with spinning sparkle
    hold_short = N_SPIN    # one full spin cycle
    for i in range(hold_short):
        frames.append(make_frame(W, H, '✨', spin_angle(sf + i), short,
                                 BRAND_DEEP, font, BG_MINT, BORDER_MINT,
                                 emoji_size=24))
        durs.append(60)
    sf += hold_short

    # Phase 2: type out "— Keep It Simple"
    suffix = full[len(short):]
    for i in range(len(suffix) + 1):
        frames.append(make_frame(W, H, '✨', spin_angle(sf), short + suffix[:i],
                                 BRAND_DEEP, font, BG_MINT, BORDER_MINT,
                                 emoji_size=24))
        durs.append(80)
        if i % 2 == 0:
            sf += 1

    # Phase 3: hold full text with one more spin
    for i in range(N_SPIN):
        frames.append(make_frame(W, H, '✨', spin_angle(sf + i), full,
                                 BRAND_DEEP, font, BG_MINT, BORDER_MINT,
                                 emoji_size=24))
        durs.append(60)

    path = os.path.join(OUT_DIR, 'kis_keep_it_simple.gif')
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durs, loop=0, optimize=False)
    print(f'  ✓  {path}  ({len(frames)} frames)')


if __name__ == '__main__':
    print('Generating GIFs...')
    make_fresh_ideas()
    make_kis()
    print('Done.')
