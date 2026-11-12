# scripts

Tooling for this benchmark. **Python 3 standard library only** — no
dependencies, no install step, nothing to `pip install`. Every script prints
human-readable Markdown (or JSON with `--json`) and can be run on its own.

The scripts are the source of truth: a number in the README is a number one of
these produced. Each folder answers one question.

## Run everything

```sh
./test/test.sh
```

That is the offline gate: syntax, naming, manifest, links, the analysis render,
and the security rails. No model, no server, no network. It is what CI runs. See
[`../test/README.md`](../test/README.md).

The scripts that *do* need a loaded model or a running server are deliberately
not in it — their outputs are committed under `benchmarks/` and
[`../evidence/`](../evidence/README.md).

## What each script does

### Measurement — [`measure/`](measure/)

| Script | What it does |
| :--- | :--- |
| [`benchmark.py`](measure/benchmark.py) | Decode throughput for every model: unloads all, warms up, asks an EN and a TR prompt twice each, writes a Markdown report. |
| [`code-matrix-test.py`](measure/code-matrix-test.py) | Asks four models for a small program in Python / Node / Bash / Swift and validates each with `py_compile` / `node --check` / `bash -n` / `swiftc -parse`. |
| [`code-benchmark.py`](measure/code-benchmark.py) | Runs a model's solution to the problems in [`../problems/`](../problems/README.md) against hidden cases and scores correctness. `--selftest` runs the reference solutions with no model. |
| [`grammar-test.py`](measure/grammar-test.py) | Format/grammar adherence: does the answer parse as a schema-valid JSON value? `--selftest` needs no model. |
| [`context-memory-test.py`](measure/context-memory-test.py) | Long-context memory: retrieval, conflict resolution and aggregation over a generated ~6k-token document. `--selftest` builds it offline. |
| [`hallucination-test.py`](measure/hallucination-test.py) | Hallucination & error risk across the 102-language corpus in [`../data/languages.json`](../data/languages.json): does the model call a fabricated API real? `--selftest` needs no model. |
| [`collect-system-info.py`](measure/collect-system-info.py) | Prints the machine, OS, oMLX version and API endpoint as a Markdown table. |
| [`model-sizes.py`](measure/model-sizes.py) | Walks the model directories and prints weights-vs-folder size per model. |

### Security — [`security/`](security/)

These audit **your own** machine. Both bind to loopback; `security-probe.py`
refuses a non-loopback target unless `--allow-remote` is passed.

| Script | What it does |
| :--- | :--- |
| [`security-probe.py`](security/security-probe.py) | Audits the server: bind address, LAN exposure, `/v1` and admin auth, unauthenticated OpenAPI/docs, wildcard CORS. With `--model`, also probes prompt injection, system-prompt leak and jailbreak refusals. |
| [`redteam-benchmark.py`](security/redteam-benchmark.py) | Measures offensive capability: starts the local lab, asks each model for an exploit path per challenge, sends it, and checks for a flag; then runs a reverse-engineering challenge. |
| [`lab-server.py`](security/lab-server.py) | A deliberately vulnerable local web app (SQLi, command injection, LFI, XSS). Loopback only. **Do not deploy.** |
| [`make-re-challenge.py`](security/make-re-challenge.py) | Compiles a small C binary with a split secret and emits the `strings` / disassembly material for the RE challenge. |

### Configuration — [`config/`](config/)

| Script | What it does |
| :--- | :--- |
| [`check-health.py`](config/check-health.py) | Polls `/health`, lists the served models, exits non-zero if unhealthy. `--wait 180` polls. |
| [`apply-profiles.py`](config/apply-profiles.py) | Reconciles the committed [`profiles/omlx-profiles.json`](../profiles/omlx-profiles.json) with the live `~/.omlx/`. Dry-run by default; `--apply` writes with backups; `--check` exits non-zero on drift. |

### Analysis — [`analysis/`](analysis/)

| Script | What it does |
| :--- | :--- |
| [`analyze-results.py`](analysis/analyze-results.py) | Reformat [`../reference/results.json`](../reference/results.json) into the ranking, the red-team scorecard and Mermaid charts. Loads no model. |

### Checks — [`checks/`](checks/)

| Script | What it does |
| :--- | :--- |
| [`check-docs-fresh.py`](checks/check-docs-fresh.py) | Static drift check: relative links resolve, the manifest is current, no secret is committed. |
| [`check-naming.py`](checks/check-naming.py) | Naming guard: every `.py`, `.mjs`, `.js`, `.sh` and `.json` file must be kebab-case. See [`../docs/guides/NAMING.md`](../docs/guides/NAMING.md). |

### Release — [`release/`](release/)

| Script | What it does |
| :--- | :--- |
| [`build-manifest.py`](release/build-manifest.py) | Writes `manifest.json` — the size, SHA-256, model and challenge counts. `--check` proves the committed one still describes the report and results. |

## Linting

`scripts/lint.sh` is the single entry point for every linter, run by hand and by
CI. It fetches `ruff`, `yamllint` and `markdownlint-cli2` at pinned versions
(via `uvx`/`npx`) and expects `shellcheck` and `actionlint` on PATH:

```bash
./scripts/lint.sh
```

`ruff` lints the harness itself — the scripts that judge the models are code too,
and an unused variable or an undefined name there would silently corrupt a
number. `shellcheck` covers the shell, `actionlint` and `yamllint` the workflows,
`markdownlint-cli2` the documents. This is separate from the offline gate
(`test/test.sh`), which needs no network.

## Running them

```bash
python3 scripts/measure/collect-system-info.py      # environment
python3 scripts/measure/model-sizes.py              # disk footprint
python3 scripts/config/check-health.py              # is the server up?
python3 scripts/config/apply-profiles.py            # diff profiles
python3 scripts/measure/benchmark.py                # throughput
python3 scripts/measure/code-matrix-test.py         # code validation
python3 scripts/security/security-probe.py          # server security
python3 scripts/security/security-probe.py --model Qwen3.6-35B-A3B-4bit:qwen3
python3 scripts/security/redteam-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
```

All scripts read the API key from `~/.omlx/settings.json` and never print it.

## Conventions

- **Standard library only.** No `requests`, no `httpx`. A reviewer should be
  able to run any script with a stock macOS Python.
- **Markdown by default, `--json` for machines.** Reports are meant to be pasted
  into a document or diffed.
- **Fail loudly.** A missing server, a bad key or an unreadable config exits
  non-zero rather than printing a misleading zero.
- **No secrets in output.** The API key is read, used in headers, and never
  logged. `profiles/` and `config/` ship placeholders, not real keys.
