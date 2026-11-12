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
