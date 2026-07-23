#!/usr/bin/env python3
"""Screenshot the Hitting/Setting/Receiving lesson page for visual QA."""
from playwright.sync_api import sync_playwright
import pathlib, time

URL = "file://" + str(pathlib.Path(__file__).parent / "hitting-setting-receiving.html")
OUT = pathlib.Path("/tmp/mvb_shots")
OUT.mkdir(exist_ok=True)

def reveal_all(page):
    page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    time.sleep(0.6)

with sync_playwright() as p:
    b = p.chromium.launch()

    # Desktop
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.goto(URL); time.sleep(0.8); reveal_all(pg)
    pg.screenshot(path=str(OUT/"lesson_desktop_full.png"), full_page=True)
    for sel, name in [(".lesson-hero","hero"),(".lesson-intro","intro"),
                      (".skill-row","skills")]:
        try:
            pg.locator(sel).first.scroll_into_view_if_needed(); time.sleep(0.3)
            pg.locator(sel).first.screenshot(path=str(OUT/f"lesson_desktop_{name}.png"))
        except Exception as e:
            print("skip", name, e)
    pg.close()

    # Mobile
    pm = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pm.goto(URL); time.sleep(0.8); reveal_all(pm)
    pm.screenshot(path=str(OUT/"lesson_mobile_full.png"), full_page=True)
    pm.close()

    b.close()
print("shots ->", OUT)
