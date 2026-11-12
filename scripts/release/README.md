# `scripts/release/` — shipping the data

| Script | What it does |
| :--- | :--- |
| [`build-manifest.py`](build-manifest.py) | Writes `manifest.json` — the size, SHA-256, model count and challenge count of the report and the results data. `--check` proves the committed one still matches. |

## Running

```bash
python3 scripts/release/build-manifest.py          # regenerate
python3 scripts/release/build-manifest.py --check  # verify (used by checks + CI)
```

`manifest.json` is the file an application reads before trusting the report: it
names the bytes and their hash. Editing the report without re-running this script
leaves the manifest stale, and `check-docs-fresh.py` fails.

The manual release run is documented in
[`../../docs/release/README.md`](../../docs/release/README.md).
