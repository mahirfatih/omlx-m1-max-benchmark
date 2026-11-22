# benchmarks

The dated report the throughput sweep writes — the raw output behind the numbers
in [`../docs/reference/RESULTS.md`](../docs/reference/RESULTS.md) and
[`../README.md`](../README.md).

| File | Produced by | What it shows |
| :--- | :--- | :--- |
| [`2026-11-11-m1max.md`](2026-11-11-m1max.md) | `scripts/measure/benchmark.py` | Decode throughput (tok/s) in EN and TR, two reps per language, with load time |
| [`2026-11-22-m1max.md`](2026-11-22-m1max.md) | `scripts/measure/benchmark.py` | The three-model campaign (Kimi-Linear, GLM, Inkling) at two temperatures with Inkling MTP on/off, plus its code, grammar, long-context, repository-analysis and hallucination results |

> **Note — which report is current.** Both files are the raw throughput sweep as
> it printed. `2026-11-22-m1max.md` is the current one (and what
> [`manifest.json`](../manifest.json) hashes as `report`); `2026-11-11-m1max.md`
> is kept byte-for-byte as its predecessor and is hashed too, as
> `archive_report`, so neither can drift unnoticed.

## Regenerating

```bash
python3 scripts/measure/benchmark.py
```

It writes a dated report to `~/Desktop` by default — or to `--out <file>` — so a
sweep can land directly here. Either way the file needs a running oMLX server with
each model available, so it is **not** part of [`../test/test.sh`](../test/test.sh).

## Why this is separate from `../reference/`

- **`../reference/results.json`** is the machine-readable form — the shape
  [`../scripts/analysis/analyze-results.py`](../scripts/analysis/analyze-results.py)
  reads to build the tables and charts.
- **Here** is the human-readable report as the sweep printed it, kept verbatim
  so a reader can see the run before any processing.

One file per run, named with its date. A re-run does not overwrite an earlier
one: the comparison across dates is part of the record.
