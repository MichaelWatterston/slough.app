# NewDesign1 — Build prompt

Copy everything below the line into Claude Code (or run `/newdesign1`, which loads this file for you).

---

## Task

Build a new Slough App landing page that is a structural and visual clone of the Airbnb Services host page (https://www.airbnb.com/host/services), re-skinned with Slough App branding and copy. Build it as a **new page**, not by overwriting the current homepage:

- HTML: `newdesign1/index.html` (served at `/newdesign1/`)
- CSS: `assets/css/newdesign1.css`

Do not touch `index.html`, `assets/css/home.css`, or `assets/css/shared.css` except where this prompt says so. Promoting the new page to the homepage is a separate decision for the owner once they have approved it.

## Reference material (all in this repo)

| File | What it is |
|---|---|
| `assets/screenshots/NewDesign1/screenshots/1.png` | Airbnb section 1: header + hero |
| `assets/screenshots/NewDesign1/screenshots/2.png` | Airbnb section 2: category icon grid |
| `assets/screenshots/NewDesign1/screenshots/3.png` | Airbnb section 3: avatar cluster + two big stats |
| `assets/screenshots/NewDesign1/screenshots/4.png` | Airbnb section 4: centred single phone |
| `assets/screenshots/NewDesign1/screenshots/5.png` | Airbnb section 5: two grey cards, each with a phone |
| `assets/screenshots/NewDesign1/SloughApp_1.png` | **Phone placeholder.** Use this image everywhere Airbnb shows a phone. It already includes the iPhone bezel and a light grey background, and is cropped at the bottom of the phone (same crop as Airbnb's hero phone). Do not wrap it in a CSS phone frame. |
| `logo.png` (repo root) | Slough App logo. Use this, never the Airbnb logo. `assets/screenshots/NewDesign1/logo.png` is an identical copy. |
| `index.html` | Current homepage. Source of all approved copy, the store-badge SVG markup, the GA snippet, meta tags and footer links. |
| `assets/css/shared.css` | Design tokens, nav, footer, reveal animation. Load it first. |
| `assets/js/nav.js` | Burger menu behaviour. Load it with `defer`. |

Open all five screenshots and `SloughApp_1.png` with the Read tool before writing any code.

Airbnb sections that are **not** in the screenshots but are on the live page, and should also be cloned (structure only, re-skinned):

6. "World-class tools for your local business": centred headline, then four feature rows/cards (title + one-line body).
7. "Your questions, answered": FAQ in groups, each question an accordion row.
8. Footer: simple, with legal links and a repeated primary CTA.

## Architecture rules (must match the existing site)

The site is plain static HTML/CSS/JS hosted on GitHub Pages with a custom domain (`CNAME`, `.nojekyll`, `_config.yml`). There is no build step, no framework, no npm. Keep it that way.

- One HTML file per page in its own folder with `index.html`, so URLs are `/newdesign1/`.
- Head order copied from `index.html`: GA tag (`G-REX65RTK9G`), charset, viewport, description, `og:*` tags, `theme-color`, canonical `https://www.slough.app/newdesign1/`, favicon (`../favicon.ico`), then `../assets/css/shared.css`, then `../assets/css/newdesign1.css`, then `<title>`.
- Relative asset paths from a sub-folder use `../` (see `get-slough-app/index.html` for the pattern). Internal links are root-relative with trailing slashes (`/become-a-tester/`).
- Nav: reuse the existing `.nav` / `.nav-inner` / `.brand` / `.nav-links` / `.nav-right` / `.nav-burger` markup so `nav.js` works unchanged. Airbnb's header is just a logo and one pill button, so in `newdesign1.css` hide `.nav-links` and style `.nav-cta` as the pill. Keep the burger for mobile.
- Footer: reuse the existing `<footer>` markup and link set verbatim (Home, Get the App, Become a Tester, Get Notified, Help & Contact, Child Safety, Terms, Privacy, © 2026). These links are required for app-store compliance. Add a "Get the app" badges row above it to mirror Airbnb's repeated CTA.
- Store badges: copy the App Store and Google Play `<a class="store-badge">` blocks from `index.html` exactly, including the inline SVGs and the two store URLs.
- Scroll reveal: add `class="reveal"` to section blocks and include the same `IntersectionObserver` snippet from the bottom of `index.html`.
- Fonts: system stack from `shared.css`. Do not add web fonts or external requests beyond GA.
- Colours: use the CSS variables in `shared.css` (`--c-blue`, `--c-purple`, `--brand-gradient`, `--ink`, `--ink-2`, `--muted`, `--line`, `--soft`). Airbnb's pink (#FF385C) maps to `--c-blue` for solid buttons, or `--brand-gradient` for the single primary CTA. Airbnb's #222 text maps to `--ink`, #6A6A6A to `--muted`, #F7F7F7 cards to `--soft`.
- Icons: category tiles use generated 3D object renders or, as a fallback, inline SVG object illustrations (see section 3). Safety cards use inline SVG line icons (24px viewBox, stroke 2) inside rounded colour swatches. Never copy Airbnb's own renders.
- No images other than `logo.png`, `SloughApp_1.png`, `assets/qr-download.svg` and the badge SVGs. Avatar circles in section 3 are CSS-only (gradient discs or initials), no stock photos.
- Accessibility: one `h1`, logical heading order, `alt` text on every image, `aria-label` on icon-only links, FAQ built with `<details>/<summary>`.

## Section-by-section spec

Match Airbnb's layout, proportions, spacing rhythm (roughly 120px between sections on desktop, 72px on mobile), max content width (about 1120px for text, 1440px for the hero), big tight-tracked bold headlines (clamp 2.25rem to 3.5rem, letter-spacing -0.03em, line-height 1.05) and grey 1.25rem subheads. Replace all Airbnb copy with Slough App copy. Reuse approved sentences from `index.html` wherever they fit; do not invent statistics or claims.

**1. Header** (screenshot 1). Logo left (36px), nothing in the middle, one pill CTA right: "Get the app" linking to `#download`. White, sticky, thin bottom border on scroll.

**2. Hero** (screenshot 1). Two columns on desktop, stacked on mobile. Left: `h1` "Slough,\nin your pocket." (reuse the `.accent` gradient treatment on the second line), lede "The community app built exclusively for Slough. What's happening, what's for sale, who's hiring and who to meet." Right: `SloughApp_1.png` large, bottom-cropped so the phone runs off the bottom edge of the hero exactly as in the Airbnb screenshot. Make the hero background blend into the image's light grey (sample it, roughly #F6F6F6) with a white-to-grey vertical gradient so there is no visible rectangle around the PNG.

**3. Category grid** (screenshot 2). Centred headline "Everything local, nothing else." and subhead "Generic community apps spread content across the country. We keep everything inside the town." Then a centred grid of eight tiles, 4 across on desktop, 3 across on tablet, 2 across on mobile: Local feed, For Sale, Jobs, Groups, Events, Families, Sport, Food. Each tile is an object illustration (about 128px) above a short label, with no background swatch, matching Airbnb's floating 3D objects.

Icons: the target is Airbnb-style 3D rendered objects (megaphone, cardboard box with price tag, briefcase with hard hat, speech bubbles, event ticket with confetti, toy house with peg-doll family, football with whistle, curry bowl with naan) on a white background. Generate them with the `mcp__mcp-image__generate_image` tool as 1:1 PNGs and save them to `assets/screenshots/NewDesign1/icons/<slug>.png`, then reference them with `<img>` inside `.nd-ico`. If image generation is unavailable, keep the inline SVG object illustrations already in `newdesign1/index.html` as the fallback.

**4. Reach / stats** (screenshot 3). Centred headline "Join your neighbours." and subhead "Everyone on Slough App lives in or around Slough. No postcode filtering, no noise from other cities." Five overlapping CSS avatar discs, middle one largest. Below, two stacked stats separated by a hairline: "100%" / "of posts, listings, jobs and groups are inside Slough" and "Free" / "to join and use, with every essential feature free forever". Small footnote under them: "Slough App Premium is optional. See the Premium section below."

**5. Single phone** (screenshot 4). Centred headline "See what's happening on your street." subhead "Post updates, photos and videos to a feed that only Slough sees. Reply, react and stay in the loop with neighbours." Then `SloughApp_1.png` centred at about 400px wide, bottom-cropped like the reference, with a soft shadow.

**6. Two cards** (screenshot 5). Centred headline "Buy, sell, work and meet, close to home." subhead "Trade with people nearby, find roles from Slough employers and join groups across 14 categories." Two `--soft` cards with 24px radius, each containing `SloughApp_1.png` cropped at the bottom of the card. Captions under each: "Buy and sell with people nearby" / "List in seconds, message safely in-app, collect from somewhere you already know." and "Work close to home. Meet your people." / "Local jobs and side gigs, plus interest-based groups for sport, families, food, faith and more."

**7. Tools** (live page, no screenshot). Centred headline "Safe by design." subhead "We actively moderate content and respond quickly to reports. You always have the final say over what you see." Four feature cards in a 2x2 grid (4x1 on wide desktop), copy taken from the Safety section of `index.html`: Report & block, Hide content, Delete your data, Active moderation.

**8. Premium notice.** Airbnb has no equivalent, but this text is an app-store requirement and must stay on any homepage candidate. Reuse the `.premium` card copy from `index.html` verbatim (Optional tag, "Slough App Premium", renewal sentence, "Premium is entirely optional" line) styled as a quiet bordered card in the same visual language as section 7.

**9. FAQ** (live page, no screenshot). Headline "Your questions, answered." Three groups with three `<details>` rows each. Write answers only from facts already on the site; where a fact is unknown, write a short neutral answer and add an HTML comment `<!-- OWNER: confirm -->`.
- Getting started: Is Slough App free? Which phones does it work on? Do I need to live in Slough?
- Using the app: How do I sell something? How do I find local jobs? How do groups work?
- Safety and data: How do I report a post or user? Can I hide things I don't want to see? How do I delete my account?

**10. Download CTA + footer.** Section `id="download"`: headline "Download for free", one line, then the two store badges and the QR code (`assets/qr-download.svg`, 160px, label "Scan to download"), mirroring the current `.final` section. Then the shared footer.

## Responsive behaviour

Breakpoints to match the rest of the site: 720px, 880px, 980px, 1200px. Hero stacks below 880px with the phone centred under the text. Category grid 2 across under 720px. Cards in section 6 stack under 880px. Nothing may overflow horizontally at 360px.

## Verification (do this, do not skip)

1. Serve the repo root: `python3 -m http.server 8080` from the repo root, then open `http://localhost:8080/newdesign1/`.
2. Screenshot the page at 1440 wide and 390 wide (full page). If Playwright is available use `npx playwright screenshot --full-page --viewport-size=1440,900 http://localhost:8080/newdesign1/ .redesign-shots/newdesign1/desktop.png` and the same with `390,844` to `mobile.png`. Save screenshots only inside `.redesign-shots/newdesign1/`, never in `/tmp`.
3. Read your screenshots and compare them side by side with `screenshots/1.png` to `5.png`. Fix layout, spacing and typography differences and re-shoot until each section is a recognisable match.
4. Confirm: no console errors, no horizontal scroll at 360px, every link resolves, burger menu opens and closes, `details` rows toggle, reveal animation runs, Lighthouse-style checks pass (one h1, alt text present).
5. Do not commit. Report what was built, what was left for the owner to confirm, and the two screenshot paths.
