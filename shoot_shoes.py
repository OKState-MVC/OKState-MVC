#!/usr/bin/env python3
"""QA screenshots for the Shoes & Equipment sub-page.
Forces all .reveal elements visible, then captures desktop full-page + viewport
scroll frames (position:fixed backdrop doesn't render in full_page shots) + mobile.
Writes to /tmp/mvb_shots/shoes/.
"""
from playwright.sync_api import sync_playwright
import os, pathlib

URL = "file://" + os.path.abspath("shoes.html")
OUT = "/tmp/mvb_shots/shoes"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

FORCE = "document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"

with sync_playwright() as p:
    b = p.chromium.launch()

    # ---- desktop 1440 ----
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    pg.goto(URL); pg.evaluate(FORCE); pg.wait_for_timeout(400)
    total = pg.evaluate("document.body.scrollHeight")
    pg.screenshot(path=f"{OUT}/desktop-full.png", full_page=True)
    # scroll frames so the darker-grey fixed backdrop renders
    y = 0; i = 0
    while y < total:
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(250)
        pg.screenshot(path=f"{OUT}/desktop-frame-{i}.png")
        y += 850; i += 1
    print("desktop total height", total, "frames", i)
    pg.close()

    # ---- mobile 390 ----
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    m.goto(URL); m.evaluate(FORCE); m.wait_for_timeout(400)
    m.screenshot(path=f"{OUT}/mobile-full.png", full_page=True)
    m.close()

    # ---- assertions: home wiring + slunks link + backdrop + counts ----
    a = b.new_page()
    a.goto("file://" + os.path.abspath("index.html"))
    card03 = a.get_attribute('a.portal-card:has(.portal-card__num:text-is("03"))', "href")
    a.goto(URL); a.evaluate(FORCE)
    slunks_href = a.get_attribute("a.slunks-logo", "href")
    shoe_duos = a.eval_on_selector_all(".duo-grid--seven .duo", "els=>els.length")
    gear_duos = a.eval_on_selector_all(".duo-grid--six .duo", "els=>els.length")
    bg = a.eval_on_selector("body", "el=>getComputedStyle(el,'::before').backgroundImage ? 'has-backdrop' : 'none'")
    print("home card03 ->", card03)
    print("slunks link ->", slunks_href[:48], "...")
    print("shoe duos:", shoe_duos, " gear duos:", gear_duos)
    a.close()
    b.close()
print("DONE ->", OUT)
