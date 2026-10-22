---
name: newdesign1
description: Build or iterate on the NewDesign1 landing page, a Slough App re-skin of the Airbnb Services host page, at /newdesign1/. Use when asked to build, continue, fix or compare the NewDesign1 / Airbnb-clone page.
---

# NewDesign1 build skill

The full specification lives in `assets/screenshots/NewDesign1/BUILD_PROMPT.md`. It is the single source of truth. Do not restate it; read it and follow it.

## Steps

1. Read `assets/screenshots/NewDesign1/BUILD_PROMPT.md` in full.
2. Read the five Airbnb reference screenshots in `assets/screenshots/NewDesign1/screenshots/` and the phone placeholder `assets/screenshots/NewDesign1/SloughApp_1.png` with the Read tool so you can see them.
3. Read `index.html`, `assets/css/shared.css`, `assets/css/home.css` and `assets/js/nav.js` to pick up the existing markup patterns, tokens and approved copy.
4. If `newdesign1/index.html` already exists, this is an iteration: diff the current page against the spec and the screenshots and fix the gaps rather than rebuilding.
5. Build or update `newdesign1/index.html` and `assets/css/newdesign1.css` exactly as the prompt specifies. Never edit `index.html`, `home.css` or `shared.css` for this task.
6. Run the Verification section of the prompt: serve, screenshot to `.redesign-shots/newdesign1/`, compare with the references, fix, re-shoot.
7. Do not commit. Finish with a short report: what was built, any `<!-- OWNER: confirm -->` items, and the screenshot paths.

## Guardrails

- `SloughApp_1.png` is a placeholder for every phone on the page. It already has a bezel and grey background; do not add a CSS phone frame around it.
- Use `logo.png`, never the Airbnb logo, Airbnb colours as literal hex, or Airbnb's 3D icon renders.
- Keep the Premium disclosure and the full footer link set; they are app-store requirements.
- Static HTML/CSS/JS only. No frameworks, build tools, web fonts or new external requests.
- Screenshots and other artefacts go in `.redesign-shots/`, not `/tmp`.
