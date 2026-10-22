# Slough App – "Join your neighbours" Portrait Set (NewDesign1)

Prompts for the five circular avatars in the "Join your neighbours" section of `/newdesign1/`. The section currently shows five gradient circles with initials (AK, JP, SM, RD, LO). Replace them with ultra-realistic photographic portraits of ordinary Slough residents, cropped into the same circles.

Layout in the page: five overlapping circles in a row, one large in the centre and two smaller either side.

| Slot | CSS class | Desktop size | Mobile size | Role |
|------|-----------|--------------|-------------|------|
| 1 | `.nd-av-1` | 108px | 72px | Outer left |
| 2 | `.nd-av-2` | 108px | 72px | Inner left |
| 3 | `.nd-av-3` | 196px | 128px | Centre, hero |
| 4 | `.nd-av-4` | 108px | 72px | Inner right |
| 5 | `.nd-av-5` | 108px | 72px | Outer right |

---

## Master style prompt

Use this block verbatim at the start of every portrait. Only the **Subject** section changes.

```
Ultra-realistic candid photographic portrait, indistinguishable from a real photograph taken on a full-frame mirrorless camera with an 85mm lens at f/2.

STYLE
- Real person, real skin: visible pores, fine lines, slight skin-tone unevenness, stray hairs, natural catchlights in the eyes. No airbrushing, no beauty-filter smoothing, no plastic or waxy skin.
- Natural, warm, genuine expression: a relaxed smile or soft laugh as if a friend just said something, eyes engaged with the camera. Not a corporate headshot, not a model pose, not a stock-photo grin.
- Natural daylight: soft overcast or open-shade light from the front-left, gentle fill, no harsh flash, no studio rim light, no dramatic shadows.
- Shallow depth of field: subject sharp from eyes to ears, background softly blurred.
- Background: an everyday Slough setting rendered as soft bokeh only, never in focus and never distracting. Pick from a residential street of brick terraced houses, a park with trees, a high-street shopfront, a local café window, a bus stop, a playing field. No landmarks, no readable signs, no text.
- Colour: true-to-life, slightly muted, neutral white balance. No orange teal grade, no HDR, no heavy vignette.
- Framing: head and shoulders, face centred, top of head near the top of frame with a little room, shoulders cut off at the bottom. The face must sit comfortably inside a circle drawn in the middle of the frame, because the image will be cropped to a circle. Nothing important near the corners.
- Camera at eye level, subject looking into the lens or just off it.
- Everyday clothing appropriate to a weekday in a Berkshire town: a hoodie, a cardigan, a puffer jacket, a work polo, a shirt, a hijab, a kurta, a football top, a school-run fleece. Clean and ordinary, nothing branded, no logos, no text on clothing.
- Square 1:1 canvas, 1024×1024, photographic detail. No text, no watermark, no border, no frame, no duplicate faces.

SUBJECT
{subject}
```

---

## Per-slot subjects

The set should read as a believable cross-section of Slough, which is one of the most diverse towns in the UK. Vary age, gender, ethnicity, build and style across the five so no two look alike, and keep every one of them warm and approachable. Nobody famous, nobody who resembles a known public figure.

### Slot 1 – outer left (`AK`)
```
A South Asian woman in her early 30s wearing a soft grey hijab and a dusty-pink cardigan, laughing gently with her head tilted a fraction to one side. Background: a brick terraced street in soft bokeh.
```

### Slot 2 – inner left (`JP`)
```
A white man in his late 50s with short grey hair, stubble and crow's feet, wearing a navy fleece with a zip collar, smiling warmly with his eyes. Background: a park with green trees in soft bokeh.
```

### Slot 3 – centre hero (`SM`)
```
A Black British woman in her mid 20s with natural curly hair tied up, small gold hoop earrings, wearing a cream knitted jumper, an open relaxed smile showing a little teeth, looking straight into the lens. This is the largest circle in the layout so the face must be especially sharp and centred. Background: a high-street shopfront window in soft bokeh.
```

### Slot 4 – inner right (`RD`)
```
A Polish man in his late 30s with short light-brown hair and a trimmed beard, wearing a work polo shirt in dark green with no logo, a friendly half-smile. Background: a café interior with warm light in soft bokeh.
```

### Slot 5 – outer right (`LO`)
```
A British Sikh man in his late 60s wearing a neatly tied navy turban and a light-blue shirt under a grey V-neck jumper, white beard, kind eyes and a gentle smile. Background: a playing field with trees in soft bokeh.
```

---

## Negative prompt

Append to every generation:

```
CGI, 3D render, illustration, painting, cartoon, anime, smooth plastic skin, airbrushed, beauty filter, over-sharpened, HDR, studio backdrop, grey seamless background, ring light, harsh flash, dramatic lighting, model pose, stock photo smile, teeth-whitened grin, sunglasses, hat covering the face, hands near face, multiple people, duplicate face, extra limbs, deformed hands, asymmetrical eyes, text, caption, watermark, logo, border, frame, vignette, black and white, celebrity likeness
```

---

## Consistency checklist (review all five together before export)

- [ ] All five feel like they were shot on the same camera on the same overcast day, with light from the same side.
- [ ] Same framing: head and shoulders, face centred, roughly the same head size relative to the frame.
- [ ] Every face sits fully inside a centred circle crop with the chin and forehead clear of the edge.
- [ ] Expressions are genuine and varied, not five copies of the same smile.
- [ ] No background element is sharp enough to read as a specific place or sign.
- [ ] Clothing has no logos, slogans or text.
- [ ] No two subjects share the same hair, skin tone, age bracket and clothing colour.
- [ ] Nobody resembles a real public figure.

---

## Export (as done 2026-10-22)

All five generated first time with Gemini via the mcp-image server, no retries needed. Raw 1024px renders and a contact sheet are in `neighbours/raw/`. Steps below were applied as written; the existing 3px white `box-shadow` ring on `.nd-av` was kept, and a neutral `background` was added so the circle shows a placeholder while the image loads.


- Generate at 1024×1024 JPEG.
- Centre-crop each to a circle-safe square. The page applies `border-radius: 50%`, so no masking is needed in the file.
- Resize to 400×400 for the four side avatars and 600×600 for the centre hero, which covers 2× and 3× displays. Save as JPEG, quality 85.
- Save as `assets/screenshots/NewDesign1/neighbours/{av-1,av-2,av-3,av-4,av-5}.jpg`.
- Markup: replace each `<span class="nd-av nd-av-N">XX</span>` in `newdesign1/index.html` with `<img class="nd-av nd-av-N" src="../assets/screenshots/NewDesign1/neighbours/av-N.jpg" alt="" width="400" height="400" loading="lazy">`. Use 600 for the centre image.
- CSS: add `object-fit: cover;` to `.nd-av` and remove the gradient `background` and text styling from `.nd-av-1` through `.nd-av-5`. Keep the `z-index` values and the circular `border-radius`. Consider a thin `3px solid #fff` border so the overlapping circles separate cleanly.
- Keep the `aria-hidden="true"` on the wrapper, the images are decorative.
