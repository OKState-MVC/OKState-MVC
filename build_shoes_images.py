#!/usr/bin/env python3
"""Prep images for the Shoes & Equipment sub-page.

The shoe + gear photos are shown inside CIRCLES, and the prompt is explicit that
the WHOLE item must stay visible in the circle. Source shots have wildly varying
backgrounds (white product shots, a teal KT-tape box, a dark Slunks logo, photos
of people wearing gear). To make the circles read as one clean, consistent set of
"product bubbles", each item is fitted (contain, with padding) onto a square white
canvas. A square + object-fit:cover in CSS then fills the circle perfectly with the
whole item comfortably inside the inscribed circle.

The Slunks logo is the exception: it's a near-full-screen banner, not a circle, so
it's just optimized on its own dark background.

Re-runnable anytime. Pillow required (already available in this env).
"""
from PIL import Image, ImageOps
import os

SRC = "/c/ClaudeWorkspace/MVB Training Website"
OUT = os.path.join(SRC, "site", "assets", "img")
os.makedirs(OUT, exist_ok=True)

CANVAS = 640          # square bubble size
PAD = 0.12            # fraction of canvas kept clear on every side (keeps item off the circle edge)
BG = (255, 255, 255)  # clean white bubble background

# (source filename, out slug)  -> squared white product bubble
BUBBLES = [
    # 7 shoes, in the prompt's listed order
    ("Nike React Hyperset (Use for Shoe Page).jpg",        "shoe-hyperset"),
    ("Nikola Jokic Joker 1 (Use for Shoe Page).jpg",       "shoe-joker"),
    ("Sky Elite FF 3 (Use for Shoe Page).jpg",             "shoe-skyelite"),
    ("Giannis Immortality (Use for Shoe Page).jpg",        "shoe-giannis"),
    ("D.O.N. Issue 6 (Use for Shoe Page).jpg",             "shoe-don"),
    ("Way of Wade 808 5 Ultra V2 (Use for Shoe Page).jpg", "shoe-wow"),
    ("Kobe 6 Protros (Use for Shoe Page).jpg",             "shoe-kobe"),
    # 6 braces / sleeves, in the prompt's listed order
    ("Knee Sleeve Image.jpg",     "gear-knee"),
    ("Ankle Brace Image.jpg",     "gear-ankle"),
    ("Sholder Brace Image.jpg",   "gear-shoulder"),
    ("Foam Roller Image.jpg",     "gear-foam"),
    ("Resistance Band Image.jpg", "gear-band"),
    ("KT Tape Image.jpg",         "gear-kt"),
]

for src, slug in BUBBLES:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src))).convert("RGB")
    inner = int(CANVAS * (1 - 2 * PAD))
    fitted = ImageOps.contain(im, (inner, inner), Image.LANCZOS)
    canvas = Image.new("RGB", (CANVAS, CANVAS), BG)
    ox = (CANVAS - fitted.width) // 2
    oy = (CANVAS - fitted.height) // 2
    canvas.paste(fitted, (ox, oy))
    dst = os.path.join(OUT, slug + ".jpg")
    canvas.save(dst, format="JPEG", quality=86, optimize=True, progressive=True)
    print("bubble", slug, fitted.size, "->", dst)

# Slunks logo: wide banner on its own dark background, just optimized.
im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, "Slunks Image.jpg"))).convert("RGB")
W, H = im.size
longedge = 1400
scale = min(1.0, longedge / float(max(W, H)))
if scale < 1.0:
    im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
dst = os.path.join(OUT, "slunks.jpg")
im.save(dst, format="JPEG", quality=88, optimize=True, progressive=True)
print("banner slunks", im.size, "->", dst)

print("DONE")
