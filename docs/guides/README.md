# `docs/guides/` — how do I work on it

The operator's documents: how the benchmark is measured, how to reproduce it, and
how to choose a model.

- [`METHODOLOGY.md`](METHODOLOGY.md) — exactly what was measured, and what the numbers mean.
- [`REPRODUCING.md`](REPRODUCING.md) — from a clean Mac to a fresh report.
- [`CHOOSING-A-MODEL.md`](CHOOSING-A-MODEL.md) — which model fits which job.

## The shape of a run

Every measurement in this repository comes from one of three scripts:

| Script | What it produces |
| :--- | :--- |
| [`../../scripts/measure/benchmark.py`](../../scripts/measure/benchmark.py) | The throughput table (EN/TR, two reps) in Markdown. |
| [`../../scripts/measure/code-matrix-test.py`](../../scripts/measure/code-matrix-test.py) | The 4-language code-validation matrix (Python/Node/Bash/Swift). |
| [`../../scripts/measure/collect-system-info.py`](../../scripts/measure/collect-system-info.py) | The environment header for a report. |

`model-sizes.py`, `check-health.py` and `apply-profiles.py` are supporting tools:
they inventory the models, confirm the server is up, and reconcile the profiles,
but they do not produce a result of their own.
