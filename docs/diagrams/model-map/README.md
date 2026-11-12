# Model map

One page that answers a single question: **which local model for which job**, and how fast
it actually ran on this machine.

- [`model-map-dark.png`](model-map-dark.png) — the poster, dark theme, 2000 px wide
- [`model-map-light.png`](model-map-light.png) — the same poster, light theme
- [`model-map.html`](model-map.html) — the interactive original; the theme button switches
  between the two without a reload

## What it shows

The seven LLMs this repository benchmarks, ordered by the job they win: default, second
opinion, uncensored, fast coding, long context, and the one that is not worth loading.
Bars are decode throughput in tokens per second, linear from 0 to the fastest model
(73.4 tok/s). The six cards underneath are what the measurement says — coding passes,
hallucination rate, long-context results, red team, repository analysis, and the spread
between fastest and slowest.

Every number comes from the tables in this repository; none of it is new measurement.

## Scope

Text only. Image and video generation do not run on oMLX, so they are not on this poster.

## Regenerating the PNGs

```sh
python3 scripts/render/render-model-map.py docs/diagrams/model-map/model-map.html \
  docs/diagrams/model-map/model-map-dark.png dark
python3 scripts/render/render-model-map.py docs/diagrams/model-map/model-map.html \
  docs/diagrams/model-map/model-map-light.png light
```

The script needs Chromium at `/Applications/Chromium.app/Contents/MacOS/Chromium` and
nothing else — it renders at 2×, finds the last non-background row, and crops to it, so the
PNG never carries empty space and never cuts the footer. It deletes its own temporary files.

If a number in the poster changes, change it in the HTML, re-run both commands, and commit
the HTML and both PNGs together — `test/test.sh` fails if they disagree with the tables.
