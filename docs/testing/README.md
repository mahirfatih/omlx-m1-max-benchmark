# Testing

How this repository is verified — what runs without a model, what needs the
server, and what needs the network (nothing does, except a live run).

## What runs where

| Layer | Entry point | Needs oMLX | Needs a model |
| :--- | :--- | :---: | :---: |
| Script syntax | `python3 -m py_compile scripts/*/*.py` | no | no |
| Environment | `python3 scripts/measure/collect-system-info.py` | no | no |
| Model inventory | `python3 scripts/measure/model-sizes.py` | no | no |
| Server health | `python3 scripts/config/check-health.py` | **yes** | no |
| Profile drift | `python3 scripts/config/apply-profiles.py --check` | no | no |
| Server security | `python3 scripts/security/security-probe.py` | **yes** | no |
| Model security | `python3 scripts/security/security-probe.py --model …` | **yes** | **yes** |
| Throughput | `python3 scripts/measure/benchmark.py` | **yes** | **yes** |
| Code matrix | `python3 scripts/measure/code-matrix-test.py` | **yes** | **yes** |
| Repository analysis | `python3 scripts/measure/repo-analysis-test.py` | **yes** | **yes** |
| Coding correctness | `python3 scripts/measure/code-benchmark.py` | **yes** | **yes** |
| Coding harness self-test | `python3 scripts/measure/code-benchmark.py --selftest` | no | no |
| Format/grammar adherence | `python3 scripts/measure/grammar-test.py` | **yes** | **yes** |
| Grammar self-test | `python3 scripts/measure/grammar-test.py --selftest` | no | no |
| Long-context memory | `python3 scripts/measure/context-memory-test.py` | **yes** | **yes** |
| Memory self-test | `python3 scripts/measure/context-memory-test.py --selftest` | no | no |
| Hallucination & error risk | `python3 scripts/measure/hallucination-test.py` | **yes** | **yes** |
| Hallucination self-test | `python3 scripts/measure/hallucination-test.py --selftest` | no | no |
| Red-team | `python3 scripts/security/redteam-benchmark.py --models …` | **yes** | **yes** |

## The offline gate

Everything that can run without a server is safe in CI:

```bash
python3 -m py_compile scripts/*/*.py
python3 scripts/measure/collect-system-info.py > /dev/null
python3 scripts/measure/model-sizes.py     > /dev/null
python3 scripts/config/apply-profiles.py --check || true   # only meaningful on a host with ~/.omlx
```

`apply-profiles.py --check` exits non-zero when the live oMLX configuration has
drifted from the committed snapshot; on a machine without oMLX it fails cleanly
and should be ignored. On the benchmark host it is the guard that keeps
[`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json) honest.

## Linting the test code

The gate proves the harness behaves; the linter proves the harness is *sound*.
`./scripts/lint.sh` runs `ruff` over `scripts/` (the test code included), plus
`shellcheck`, `actionlint`, `yamllint` and `markdownlint-cli2`. It is the job the
CI `lint` job runs. Unlike the offline gate it uses the network, to fetch the
pinned tool versions with `uvx`/`npx`.

## The coding benchmark

`scripts/measure/code-benchmark.py` asks a model for a solution to a problem in
`problems/`, extracts the Python, **runs** it against hidden cases, and scores
correctness. It is the executable companion to `code-matrix-test.py`, which only
checks that code parses.

Model output is untrusted code. The rails:

- it runs in a throwaway temp directory, as a subprocess, under a 20 s timeout;
- the result is written to a file, so a solution cannot spoof it via stdout;
- the interpreter runs with `-I` (isolated: no user site, no env influence).

It is still code execution. Run it only against local models you trust, on your
own machine. `--selftest` runs the reference solutions and needs neither a model
nor a server; it is step 9 of [`../../test/test.sh`](../../test/test.sh).

## The other capability probes

Three more scripts share the same shape — one prompt per item, a score, an
offline `--selftest`:

- **`grammar-test.py`** scores *shape*: the model must return a JSON value that
  matches a schema. The validator is a small standard-library subset of JSON
  Schema.
- **`context-memory-test.py`** scores *use of a long context*: facts are planted
  at increasing depth in a generated ~6k-token document, including a corrected
  fact that supersedes an earlier one.
- **`hallucination-test.py`** scores *factuality* over
  [`../../data/languages.json`](../../data/languages.json) (102 languages): for
  each language a genuine API/feature and a fabricated twin are shown, and the
  model must say which is real. It reports the hallucination rate (fake called
  real) separately from the false-alarm rate (real called fake), plus a Brier
  score for the stated confidence.

## The security layer

Two tools, two questions — see [`../security/README.md`](../security/README.md):

- **`security-probe.py`** audits the server (bind, auth, CORS, schema leak) and,
  with `--model`, the model's resistance to prompt injection and jailbreaks.
  Exit code is non-zero on a `HIGH`/`CRITICAL` finding, so it can gate a run.
- **`redteam-benchmark.py`** measures offensive capability against a local
  deliberately-vulnerable lab and a local RE binary. It is a *capability*
  benchmark, not a safety gate.

## The lab target

`scripts/security/lab-server.py` is an intentionally vulnerable app. It binds to
loopback only and refuses any other host. Do not deploy it. Its flags are fixed
in source so the harness can score a model's exploit:

| Challenge | Endpoint | Exploit |
| :--- | :--- | :--- |
| SQL injection | `/login` | `' OR '1'='1`, `admin'--` |
| Command injection | `/ping?host=` | `;`, `&#124;`, `$(...)`, backticks |
| Path traversal | `/download?file=` | `../`, absolute path |
| Reflected XSS | `/search?q=` | `<script>`, `onerror=`, `javascript:` |

## The RE target

`scripts/security/make-re-challenge.py` compiles a small C binary whose password
is assembled from two string pieces at runtime, so `strings` shows only a half.
The model is given the `strings` output and the disassembly and must recover the
full password. The secret lives in `meta.json`, never in the model's prompt.

## The whole thing, in order

```bash
# 1. syntax
python3 -m py_compile scripts/*/*.py

# 2. inventory + health
python3 scripts/measure/collect-system-info.py
python3 scripts/measure/model-sizes.py
python3 scripts/config/check-health.py

# 3. security
python3 scripts/security/security-probe.py
python3 scripts/security/security-probe.py --model Qwen3.6-35B-A3B-4bit:qwen3

# 4. capability
python3 scripts/measure/benchmark.py
python3 scripts/measure/code-matrix-test.py
python3 scripts/security/redteam-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
python3 scripts/measure/repo-analysis-test.py --repo ~/Sites/net-traffic-control-catalog
```
