# Reproducing the benchmark

From a clean Mac to a fresh report. Every command here is run from the repository
root.

## Prerequisites

- Apple Silicon Mac with enough unified memory for the models you want to test
  (this benchmark used an M1 Max with 64 GB).
- macOS 15+ (this benchmark used 26.7.2).
- [oMLX](https://omlx.ai) installed and running.
- The models you intend to benchmark, downloaded into a directory oMLX reads.
- **Python 3** — standard library only; there is nothing to `pip install`.

## 1. Install and start oMLX

Download the app from <https://omlx.ai>, or build from source:

```bash
git clone https://github.com/jundot/omlx
cd omlx && pip install -e .
```

The server listens on `http://127.0.0.1:8000`. Confirm it is up:

```bash
python3 scripts/config/check-health.py
```

This prints the health status and every model the server advertises. If it
reports `UNHEALTHY`, start oMLX and retry — `check-health.py --wait 180` polls
for three minutes.

## 2. Inventory the machine and the models

```bash
python3 scripts/measure/collect-system-info.py       # environment header
python3 scripts/measure/model-sizes.py               # disk footprint per model
```

`collect-system-info.py` reads the oMLX version, chip, RAM and OS.
`model-sizes.py` walks the model directories from `~/.omlx/settings.json` and
prints weights-vs-folder sizes.

## 3. Apply the profiles (optional)

The repository ships a **sanitized snapshot** of the working oMLX profiles in
[`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json). To reconcile
your live oMLX configuration with it:

```bash
python3 scripts/config/apply-profiles.py            # show the diff (writes nothing)
python3 scripts/config/apply-profiles.py --apply    # write it, with timestamped backups
```

`--apply` copies each live file to `<file>.bak-YYYYMMDD-HHMMSS` before writing,
then tells you to restart oMLX:

```bash
~/.omlx/bin/omlx stop; sleep 4; ~/.omlx/bin/omlx start
```

If you prefer to configure by hand, every setting is listed in
[`../reference/PROFILES.md`](../reference/PROFILES.md).

## 4. Run the throughput benchmark

```bash
python3 scripts/measure/benchmark.py
```

The script reads the API key from `~/.omlx/settings.json` (it never prints it),
unloads every known model, then measures each in turn. The full Markdown report
is written to `~/Desktop/omlx-benchmark-<timestamp>.md` and printed to the
terminal.

To benchmark a different set of models, edit the `TARGETS` list at the top of the
script — each entry is `"<model-id>:<profile>"`.

## 5. Validate multi-language code generation (optional)

```bash
python3 scripts/measure/code-matrix-test.py
```

This asks four models to write a small program in Python, Node.js, Bash and
Swift, then checks each output with `py_compile` / `node --check` / `bash -n` /
`swiftc -parse`. It needs `node`, `bash` and `swiftc` on the machine.

## 6. Analyse a real repository (optional)

```bash
python3 scripts/measure/repo-analysis-test.py \
    --repo ~/Sites/net-traffic-control-catalog \
    --out evidence/repo-analysis-$(date +%F).md \
    --json-out reference/repo-analysis.json
```

The default target is
[`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog),
the project this repository mirrors. Point `--repo` at any checkout. The script
builds one digest, gives it to every model, and scores the answers on how many
of the repository's own facts they cite. The reading is in
[`../analysis/net-traffic-control-catalog.md`](../analysis/net-traffic-control-catalog.md).

## 7. Record the result

Copy the generated report into `benchmarks/` with a dated name, e.g.
`benchmarks/2026-11-11-m1max.md`, and open a pull request — see
[`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `check-health.py` says UNHEALTHY | server not started | start the oMLX app; retry with `--wait` |
| A model errors on load | not enough memory | unload other models; reduce model count |
| `KeyError` on `settings.json` | oMLX never run | launch oMLX once so it writes `~/.omlx/` |
| Numbers far below the table | background load / throttling | close GPU-heavy apps; keep runs short |
| `load (s)` looks huge | cold cache | expected on the first request of a session |
