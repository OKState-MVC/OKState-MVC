#!/usr/bin/env python3
"""Prep the 9 "Players to Study" photos into face-centered squares for the
circular nodes on players.html. Squares are 720x720 so they stay crisp when a
node balloons large. Re-runnable; crop centers are fractional (independent of
the source pixel dims). Outputs to site/assets/img/player-*.jpg (offline).
"""
from PIL import Image, ImageOps
import os

SRC = "/c/ClaudeWorkspace/MVB Training Website"
OUT = os.path.join(SRC, "site", "assets", "img")
os.makedirs(OUT, exist_ok=True)

# (source filename, out slug, center_x_frac, center_y_frac, side_frac_of_width)
PLAYERS = [
    ("Ran Takahashi (Use for Emulating Player Style Page).jpg",   "player-takahashi", 0.46, 0.30, 0.92),
    ("Matt Anderson (Use for Emulating Player Style Page).jpg",   "player-anderson",  0.42, 0.42, 0.95),
    ("Kento Miyaura (Use for Emulating Player Style Page).jpg",   "player-miyaura",   0.55, 0.32, 0.95),
    ("Cole Hartke (Use for Emulating Player Style Page).jpg",     "player-hartke",    0.40, 0.37, 0.82),
    ("Cameron Thorne (Use for Emulating Player Style Page).jpg",  "player-thorne",    0.50, 0.40, 0.95),
    ("Simon Torwie (Use for Emulating Player Style Page).jpg",    "player-torwie",    0.55, 0.36, 0.90),
    ("Micah Christenson Setting (Use for Emulating Player Style Section).jpg", "player-christenson", 0.48, 0.36, 0.94),
    ("Luciano De Cecco (Use for Emulating Player Style Page).jpg","player-dececco",   0.46, 0.30, 0.95),
    ("Tomohiro Yamamoto (Use for Emulating Player Style Page).jpg","player-yamamoto", 0.52, 0.38, 0.95),
]

SIDE = 720
for src, slug, cxf, cyf, sidef in PLAYERS:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src))).convert("RGB")
    W, H = im.size
    cx, cy = cxf * W, cyf * H
    half = (sidef * W) / 2.0
    half = min(half, W / 2.0, H / 2.0)          # never exceed the image
    left, top, right, bottom = cx - half, cy - half, cx + half, cy + half
    if left < 0:   right -= left;  left = 0
    if top < 0:    bottom -= top;  top = 0
    if right > W:  left -= (right - W); right = W
    if bottom > H: top -= (bottom - H); bottom = H
    left, top = max(0.0, left), max(0.0, top)
    box = (int(round(left)), int(round(top)), int(round(right)), int(round(bottom)))
    sq = im.crop(box).resize((SIDE, SIDE), Image.LANCZOS)
    dst = os.path.join(OUT, slug + ".jpg")
    sq.save(dst, format="JPEG", quality=86, optimize=True, progressive=True)
    print("player", slug, box, "->", dst)

print("DONE")
