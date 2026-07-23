#!/usr/bin/env python3
"""Prep images for the MVB home page.
- Crops the 7 officer photos to face-centered squares (LinkedIn-style), 640x640.
- Produces web-optimized copies of the hero + blob images.
Run from anywhere; paths are resolved relative to the workspace folder.
"""
from PIL import Image, ImageOps
import os

SRC = "/c/ClaudeWorkspace/MVB Training Website"
OUT = os.path.join(SRC, "site", "assets", "img")
os.makedirs(OUT, exist_ok=True)

# (source filename, out slug, center_x_frac, center_y_frac, side_frac_of_width)
# center/side expressed as fractions so they're independent of exact pixel dims.
OFFICERS = [
    ("Austin Wheeler Profile Picture.jpg",  "austin-wheeler", 0.385, 0.410, 0.66),
    ("Jake Johnson Profile Picture.jpg",    "jake-johnson",   0.424, 0.215, 0.32),
    ("Beck Hamilton Profile Picture.jpg",   "beck-hamilton",  0.503, 0.390, 0.31),
    ("Evden Tilley profile picture.jpg",    "evden-tilley",   0.623, 0.240, 0.42),
    ("Chris Malone Profile Picture.jpg",    "chris-malone",   0.500, 0.175, 0.36),
    ("Tyler Robinson Profile Picture.jpg",  "tyler-robinson", 0.540, 0.450, 0.35),
    ("Cat Dzanski Profile Picture.jpg",     "cat-dzanski",    0.480, 0.480, 0.28),
]

for src, slug, cxf, cyf, sidef in OFFICERS:
    im = Image.open(os.path.join(SRC, src))
    im = ImageOps.exif_transpose(im)
    W, H = im.size
    cx, cy = cxf * W, cyf * H
    half = (sidef * W) / 2.0
    left, top, right, bottom = cx - half, cy - half, cx + half, cy + half
    if left < 0:   right -= left;  left = 0
    if top < 0:    bottom -= top;  top = 0
    if right > W:  left -= (right - W); right = W
    if bottom > H: top -= (bottom - H); bottom = H
    left, top = max(0.0, left), max(0.0, top)
    box = (int(round(left)), int(round(top)), int(round(right)), int(round(bottom)))
    face = im.crop(box).convert("RGB").resize((640, 640), Image.LANCZOS)
    dst = os.path.join(OUT, slug + ".jpg")
    face.save(dst, format="JPEG", quality=88, optimize=True)
    print("officer", slug, box, "->", dst)

# Web-optimized full images (hero + blobs). Cap long edge at 1920.
FULL = [
    ("Overall team picture (use for main background).jpg", "hero.jpg", 2000),
    ("Team pyramid (use for background).jpg",              "pyramid.jpg", 1400),
    ("Team National Anthem (Use for Background).jpg",       "anthem.jpg", 1400),
]
for src, out, longedge in FULL:
    im = Image.open(os.path.join(SRC, src))
    im = ImageOps.exif_transpose(im).convert("RGB")
    W, H = im.size
    scale = min(1.0, longedge / float(max(W, H)))
    if scale < 1.0:
        im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    dst = os.path.join(OUT, out)
    im.save(dst, format="JPEG", quality=84, optimize=True)
    print("full", out, im.size, "->", dst)

print("DONE")
