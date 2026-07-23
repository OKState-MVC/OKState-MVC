#!/usr/bin/env python3
"""Capture viewport frames at several scroll offsets so the FIXED photo backdrop
shows through the gaps between panels (full_page screenshots don't render fixed bg)."""
from playwright.sync_api import sync_playwright
import pathlib, time

URL = "file://" + str(pathlib.Path(__file__).parent / "index.html")
OUT = pathlib.Path("/tmp/mvb_scroll"); OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    pg.goto(URL); time.sleep(0.7)
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    # make sure lazy imgs load
    pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
    total = pg.evaluate("document.body.scrollHeight")
    time.sleep(0.5)
    offsets = [0, 700, 1500, 2300, 3200, 4200, 5200]
    for i, y in enumerate(offsets):
        pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.5)
        pg.screenshot(path=str(OUT/f"y{i}_{y}.png"))
    print("total height", total, "-> frames in", OUT)
    b.close()
