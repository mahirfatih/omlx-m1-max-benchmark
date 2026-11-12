# Image generation — seconds per image

**Date:** 2026-11-12. One `mflux-generate-*` process per prompt, run through [mflux](https://github.com/filipstrand/mflux), which is separate from the oMLX text server. Time is end-to-end wall clock, **model load included** (the CLI is one-shot).

| Model (profile) | Licence | Image | s/img | s/step | Size | OK |
|---|---|---:|---:|---:|---|:---:|
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `photoreal-market` | 28.04 | 7.01 | 1024×1024, 1.9 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `portrait-hands` | 22.48 | 5.62 | 1024×1024, 1.7 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `text-poster` | 22.42 | 5.61 | 1024×1024, 0.3 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `composition-stilllife` | 22.47 | 5.62 | 1024×1024, 1.4 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `stylised-risograph` | 22.57 | 5.64 | 1024×1024, 2.0 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `product-headphones` | 22.54 | 5.63 | 1024×1024, 1.0 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `photoreal-architecture` | 22.55 | 5.64 | 1024×1024, 1.8 MB | ✅ |
| `mflux-community/flux2-klein-4b-mflux-q8` (klein-q8) | apache-2.0 | `text-signage` | 22.46 | 5.62 | 1024×1024, 1.7 MB | ✅ |

_s/img is what a person waits for one finished image on this machine. Because each CLI call reloads the model, it is a cold number; the steady-state per-step cost is the `s/step` column._

## The images themselves

Each one ran in ~22.5 s at 1024×1024, so this is the model's normal output, not a
selected best-of. The prompt is quoted under each so you can judge the result
against what was actually asked.

### `photoreal-market` — photoreal

> Photorealistic rainy-night street market in Istanbul, wet cobblestones reflecting red and yellow awnings, steam rising from a food stall, shallow depth of field, shot on 35mm, natural colour grading.

![Rainy-night street market, klein-q8](images/klein-q8--photoreal-market.png)

### `portrait-hands` — portrait

> Close-up portrait of an older fisherman mending a net, weathered hands clearly visible with all fingers, warm low sun from the left, detailed skin and rope texture, neutral background.

![Close-up portrait of a fisherman mending a net, klein-q8](images/klein-q8--portrait-hands.png)

### `text-poster` — text rendering

> Minimalist swiss-style poster with the exact headline "LOCAL FIRST" in bold black Helvetica on an off-white background, a single thin red horizontal rule below the text, generous margins, flat vector look.

![Minimalist poster reading LOCAL FIRST, klein-q8](images/klein-q8--text-poster.png)

### `composition-stilllife` — composition

> Overhead still life on a dark oak table: exactly three objects — a white ceramic mug, a brass pocket watch, and a ripe pomegranate cut in half. Warm side light, soft shadows, each object distinct and fully in frame.

![Overhead still life of three objects, klein-q8](images/klein-q8--composition-stilllife.png)

### `stylised-risograph` — stylised

> Two-colour risograph print of a fox sitting in tall grass at dusk, visible paper grain and slight misregistration, limited palette of teal and warm orange, bold shapes, no outlines.

![Two-colour risograph fox, klein-q8](images/klein-q8--stylised-risograph.png)

### `product-headphones` — product shot

> Studio product shot of matte-black over-ear headphones on a seamless light-grey backdrop, three-point softbox lighting, subtle reflection on the surface below, crisp edges, commercial catalogue style.

![Studio product shot of headphones, klein-q8](images/klein-q8--product-headphones.png)

### `photoreal-architecture` — photoreal

> Wide architectural photograph of a concrete brutalist library at golden hour, long shadows across a plaza, a single figure walking, tilt-shift correction so verticals are straight, high dynamic range.

![Brutalist library at golden hour, klein-q8](images/klein-q8--photoreal-architecture.png)

### `text-signage` — text rendering

> Photograph of a small neighbourhood coffee shop window at night with the hand-painted sign reading "OPEN" in warm neon-green light, condensation on the glass, brass fittings, cinematic bokeh of the street behind.

![Coffee shop window with a legible neon-green OPEN sign, klein-q8](images/klein-q8--text-signage.png)

The two text prompts are the interesting ones: they are the failure mode people
expect from a small local model, and here both headlines render legibly.
