# Slough App – Category Icon Set (NewDesign1)

Prompt for generating the eight category icons used in the "What you'll find in Slough App" row on `/newdesign1/`. The current icons are flat inline SVGs and look out of place against the Airbnb Services reference. Replace them with rendered 3D objects that match the reference exactly.

Reference image: `assets/screenshots/NewDesign1/icon-style-reference.png` (Airbnb Services category row: Catering, Chefs, Hair styling, Makeup, Massage, Personal training, Photography, Prepared meals, Spa treatments).

---

## Master style prompt

Use this block verbatim at the start of every icon generation. Only the **Subject** section changes per icon.

```
Photorealistic 3D rendered product icon in the style of Airbnb's Services category illustrations.

STYLE
- Clean 3D render, soft studio lighting from the upper left, one gentle key light plus soft fill, no hard specular hotspots.
- Realistic physical materials: brushed metal, matte plastic, natural wood grain, cotton fabric, soft rubber. Nothing cartoonish, nothing flat, no outlines.
- Three-quarter view, camera slightly above the object (around 25–30 degrees), tilted so the top face and one side are both visible. Same camera angle for every icon in the set.
- Small, grounded composition: one hero object plus one or two supporting props arranged in a tight cluster, overlapping slightly, as if placed on a table. Props must be real-world physical objects, never UI symbols, speech bubbles, arrows, pins or glyphs.
- Soft contact shadow directly beneath the objects, very short and diffuse. No long cast shadows, no floor plane, no horizon.
- Pure white background (#FFFFFF). Object occupies about 60–70% of the frame width, centred, with even padding on all sides.
- Colour: natural, slightly desaturated, product-photography palette. Mostly neutral tones (greys, blacks, warm wood, cream) with one or two restrained accent colours per icon. Avoid saturated primaries, gradients, glows or neon.
- Scale consistency: every icon should read at the same visual weight and occupy a similar footprint so the eight sit evenly in a row.
- Square 1:1 canvas, 1024×1024, high detail, no text, no labels, no watermark, no people.

SUBJECT
{subject}
```

---

## Per-icon subjects

Replace `{subject}` with the matching block.

### 1. Local feed
```
A folded local newspaper with a visible masthead area (no readable text) lying at a slight angle, with a small white ceramic coffee cup on a saucer resting on top-right of the fold, and a pair of reading glasses tucked against the paper. Newsprint off-white, cup glossy white, glasses thin dark tortoiseshell frames.
```

### 2. For Sale
```
A small open kraft cardboard moving box with the flaps up, a folded red-and-white price tag on a string hanging over the front edge, and a single item inside peeking over the rim, such as a matte-black desk lamp head or a pair of vintage white trainers. Warm brown corrugated card, cream string, muted red tag.
```

### 3. Jobs
```
A slim dark-brown leather briefcase lying flat, three-quarter view, with a cream manila folder resting half-open on top and a matte-black fountain pen laid diagonally across the folder. Leather with soft grain and brass clasps, folder slightly textured paper.
```

### 4. Groups
```
A small round wooden café table top (seen from above-angle) with three mismatched coffee mugs in a tight triangle — one white ceramic, one speckled grey stoneware, one pale blue enamel — and a small notepad with a pencil beside them. Light oak wood, mugs matte-glazed, no steam.
```

### 5. Events
```
A pair of printed admission tickets with perforated stubs, slightly fanned, resting on a small coil of warm white festoon string lights with two visible glass bulbs (switched off, not glowing). Tickets in cream card with a muted coral stripe, light cable in soft black rubber.
```

### 6. Families
```
A stack of three wooden toy building blocks in muted sage, mustard and dusty blue, with a small cuddly brown teddy bear sitting against the stack and a child's pale wooden ride-on toy car wheel visible beside it. Natural beech wood, soft plush fabric.
```

### 7. Sport
```
A classic black-and-white panel football resting against a pair of folded athletic shorts in dark navy, with a single white sports sock draped over the shorts and a small silver whistle on a black lanyard at the front. Leather-look ball, matte fabric.
```

### 8. Food
```
A round wooden serving board with a sliced crusty sourdough loaf, a small white ramekin of butter, and a wedge of hard cheese with a short cheese knife laid across the board. Toasted bread crust, light oak board, pale yellow butter, soft natural cheese colour.
```

---

## Negative prompt

Append to every generation:

```
flat illustration, vector art, cartoon, clipart, line art, emoji, UI icon, glossy plastic look, neon, saturated colours, gradient background, drop shadow on background, long cast shadow, floor reflection, text, letters, numbers, logo, watermark, people, hands, faces, isometric grid, blurry, low detail, cropped object
```

---

## Consistency checklist (review all eight together before export)

- [ ] Same camera angle and height across every icon.
- [ ] Same light direction (upper left) and shadow softness.
- [ ] Objects sit at the same scale and fill roughly the same area of the canvas.
- [ ] All backgrounds are identical pure white with no vignette.
- [ ] No icon uses more than two accent colours; the set as a whole reads as neutral with occasional warm/cool touches.
- [ ] No symbols, glyphs, bubbles, pins or UI metaphors — physical objects only.
- [ ] Nothing is cut off at the canvas edge.

## Export (as done 2026-10-22)

- Generated with Gemini via the mcp-image server at 1024×1024 using the reference image as a style input.
- Raw renders kept in `assets/screenshots/NewDesign1/icons/raw/` with a contact sheet for side-by-side review.
- Each raw render was auto-cropped to its content, padded to a square with an 8% margin, and resized to 320×320 JPEG so all eight share the same visual scale. `.nd-ico` renders at 128×128 CSS px, so 320 covers 2.5× displays.
- Final files: `assets/screenshots/NewDesign1/icons/{local-feed,for-sale,jobs,groups,events,families,sport,food}.jpg`.
- Markup: each inline `<svg>` inside `.nd-ico` in `newdesign1/index.html` was replaced with `<img src="../assets/screenshots/NewDesign1/icons/<name>.jpg" width="320" height="320" alt="" loading="lazy">`.
- Note: the first Families render came back with a "Childcare" caption baked in. Re-running with an explicit "no caption, no title, no word" instruction fixed it. Keep that line in the prompt.
