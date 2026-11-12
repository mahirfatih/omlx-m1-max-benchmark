# benchmarks

The dated report the throughput sweep writes — the raw output behind the numbers
in [`../docs/reference/RESULTS.md`](../docs/reference/RESULTS.md) and
[`../README.md`](../README.md).

| File | Produced by | What it shows |
| :--- | :--- | :--- |
| [`2026-11-11-m1max.md`](2026-11-11-m1max.md) | `scripts/measure/benchmark.py` | Decode throughput (tok/s) in EN and TR, two reps per language, with load time |

## Regenerating

```bash
python3 scripts/measure/benchmark.py
```

It writes a dated report to `~/Desktop` by default; move it here to commit it.
This needs a running oMLX server with each model available, so it is **not** part
of [`../test/test.sh`](../test/test.sh).

## Why this is separate from `../reference/`

- **`../reference/results.json`** is the machine-readable form — the shape
  [`../scripts/analysis/analyze-results.py`](../scripts/analysis/analyze-results.py)
  reads to build the tables and charts.
- **Here** is the human-readable report as the sweep printed it, kept verbatim
  so a reader can see the run before any processing.

One file per run, named with its date. A re-run does not overwrite an earlier
one: the comparison across dates is part of the record.
