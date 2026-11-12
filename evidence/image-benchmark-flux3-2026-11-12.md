# Image generation — seconds per image

**Date:** 2026-11-12. One `mflux-generate-*` process per prompt, run through [mflux](https://github.com/filipstrand/mflux), which is separate from the oMLX text server. Time is end-to-end wall clock, **model load included** (the CLI is one-shot).

| Model (profile) | Licence | Image | s/img | s/step | Size | OK |
|---|---|---:|---:|---:|---|:---:|
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `photoreal-market` | 191.0 | 11.94 | 1024×1024, 2.2 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `portrait-hands` | 180.36 | 11.27 | 1024×1024, 1.6 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `text-poster` | 180.42 | 11.28 | 1024×1024, 0.5 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `composition-stilllife` | 180.41 | 11.28 | 1024×1024, 1.5 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `stylised-risograph` | 180.57 | 11.29 | 1024×1024, 2.2 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `product-headphones` | 180.12 | 11.26 | 1024×1024, 1.0 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `photoreal-architecture` | 180.47 | 11.28 | 1024×1024, 1.6 MB | ✅ |
| `mflux-community/flux-3-image-klein-base-mflux-q8` (flux3-klein-q8) | FLUX Kommunity License v1.0 | `text-signage` | 181.52 | 11.35 | 1024×1024, 1.7 MB | ✅ |

_s/img is what a person waits for one finished image on this machine. Because each CLI call reloads the model, it is a cold number; the steady-state per-step cost is the `s/step` column._
