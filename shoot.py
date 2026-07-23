#!/usr/bin/env python3
"""Screenshot the home page for visual QA (desktop + mobile, full + sections)."""
from playwright.sync_api import sync_playwright
import pathlib, time

URL = "file://" + str(pathlib.Path(__file__).parent / "index.html")
OUT = pathlib.Path("/tmp/mvb_shots")
OUT.mkdir(exist_ok=True)

def reveal_all(page):
    # force all reveal elements visible so screenshots aren't blank mid-animation
    page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    time.sleep(0.6)

with sync_playwright() as p:
    b = p.chromium.launch()

    # Desktop
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.goto(URL); time.sleep(0.8); reveal_all(pg)
    pg.screenshot(path=str(OUT/"desktop_full.png"), full_page=True)
    for sel, name in [(".hero","hero"),(".welcome-card","welcome"),
                      (".team-panel","team"),(".portal-panel","portal")]:
        try:
            pg.locator(sel).first.scroll_into_view_if_needed(); time.sleep(0.3)
            pg.locator(sel).first.screenshot(path=str(OUT/f"desktop_{name}.png"))
        except Exception as e:
            print("skip", name, e)
    pg.close()

    # Mobile
    pm = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pm.goto(URL); time.sleep(0.8); reveal_all(pm)
    pm.screenshot(path=str(OUT/"mobile_full.png"), full_page=True)
    pm.close()

    b.close()
print("shots ->", OUT)
