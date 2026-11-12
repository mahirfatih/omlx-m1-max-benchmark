# `docs/reference/` — what is in it right now

The facts: every model, every profile, every measured number. Written from the
data the scripts produced, not generated, but easy to re-derive.

- [`MODELS.md`](MODELS.md) — all six models: size, source, and uncensored/heretic classification.
- [`PROFILES.md`](PROFILES.md) — every oMLX profile and setting, with the reasoning.
- [`RESULTS.md`](RESULTS.md) — the throughput table, charts, and the raw report location.

## Provenance of these numbers

| Number | Comes from | Command |
| :--- | :--- | :--- |
| Throughput (tok/s) | `benchmarks/2026-11-11-m1max.md` | `python3 scripts/measure/benchmark.py` |
| Disk size | the model folder | `python3 scripts/measure/model-sizes.py` |
| Runtime memory | oMLX guard measurements | (recorded in [`RESULTS.md`](RESULTS.md)) |
| Environment | the live machine | `python3 scripts/measure/collect-system-info.py` |
| Code-validation matrix | `benchmarks/2026-11-11-m1max.md` | `python3 scripts/measure/code-matrix-test.py` |

A **generated** mark in [`../README.md`](../README.md) means: re-run the named
script rather than editing the number. The reference pages here are hand-written
explanations of those outputs.
