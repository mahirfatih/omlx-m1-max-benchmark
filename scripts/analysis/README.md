# `scripts/analysis/` — reading the results

A single script that reformats the committed data. It loads no model and needs
no server: every number already exists in
[`../../reference/results.json`](../../reference/results.json).

| Script | What it does |
| :--- | :--- |
| [`analyze-results.py`](analyze-results.py) | Prints the throughput ranking, the red-team scorecard, and two Mermaid charts. `--json` dumps the raw data. |

## Running

```bash
python3 scripts/analysis/analyze-results.py
python3 scripts/analysis/analyze-results.py --json > /tmp/results.json
```

The output is the same table and charts that appear in the README and in
[`../../docs/reference/RESULTS.md`](../../docs/reference/RESULTS.md). If you
re-measure, update `reference/results.json` and re-run this script rather than
editing the charts by hand.
