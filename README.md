# The Crash Course on Volleyball — OSU Men's Volleyball Club

A one-stop guide for anyone who wants to learn volleyball, built for prospective members
of the Oklahoma State University Men's Volleyball Club.

Curated by Jake Johnson. Apple-style static site — no build step, fully offline-capable.

## Pages
- **Home** — `index.html`
- **Hitting, Setting & Receiving** — `hitting-setting-receiving.html`
- **Reffing** — `reffing.html`
- **Shoes & Equipment** — `shoes.html`
- **Players to Study** — `players.html`
- **What We Expect of You / Our Philosophy** — `what-we-expect.html`

## Navigation
Every content page carries a breadcrumb pill (top-left), a prev/next chapter pager at the
bottom, and a footer mini-portal linking all five sections. The **Our Philosophy** page keeps
its deliberate quiet ending (breadcrumb only — no pager or footer portal).

Every page also has a small fixed **social dock** (top-left vertical capsule) with the Instagram
and GroupMe logos — both live and opening in a new tab. Directly below it sits the circular
**info dock** ("!" button) that expands to the Register / Pay-dues links.

## Running locally
Open `index.html` in any browser (works over `file://`). No server or build tools required.

The `build_*.py` / `shoot_*.py` scripts are development helpers (image optimization + Playwright QA)
and are not needed to view or host the site.

## After you deploy (social share previews)
Each page has Open Graph / Twitter tags so the link shows a preview card when shared. The
`og:image` currently points to a **relative** path (`assets/img/hero.jpg`), which most modern
scrapers resolve fine. For maximum compatibility with older scrapers, once you have your live
domain, change the `og:image` / `twitter:image` URLs in each page's `<head>` to the absolute
`https://your-domain/assets/img/hero.jpg`.
