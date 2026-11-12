# `scripts/measure/` — the measurements

What produces the numbers. Every script here talks to a running oMLX server and
prints Markdown (or JSON with `--json`). The image and video harnesses are **not**
here — oMLX cannot run either, so they live in the
[generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max).

| Script | Measures | Needs a model |
| :--- | :--- | :---: |
| [`benchmark.py`](benchmark.py) | Decode throughput (tok/s) in EN and TR, two reps each. Writes a report to `~/Desktop`. | yes |
| [`code-matrix-test.py`](code-matrix-test.py) | Code correctness across Python / Node / Bash / Swift, validated with each toolchain. | yes |
| [`code-benchmark.py`](code-benchmark.py) | **Runs** a model's solution to the problems in [`../../problems/`](../../problems/) against hidden cases and scores it. `--selftest` proves the harness with no model. | yes |
| [`grammar-test.py`](grammar-test.py) | Format/grammar adherence: is the answer a schema-valid JSON value? Tasks come from [`../../data/grammar-prompts.json`](../../data/grammar-prompts.json). `--selftest` validates the validator. | yes |
| [`context-memory-test.py`](context-memory-test.py) | Long-context memory: retrieval, conflict resolution and aggregation in a ~6k-token document. `--selftest` builds it offline. | yes |
| [`hallucination-test.py`](hallucination-test.py) | Hallucination & error risk over the [`../../data/languages.json`](../../data/languages.json) corpus (102 languages): does the model call a fabricated API real? `--selftest` is offline. | yes |
| [`repo-analysis-test.py`](repo-analysis-test.py) | How each model analyses a real repository: answer time, tok/s, and how many of the repo's own facts it recovers. Default target: [`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog). | yes |
| [`merge-code-benchmark.py`](merge-code-benchmark.py) | Merge two coding-benchmark JSON runs (a re-run overrides a model's earlier row). | no |
| [`collect-system-info.py`](collect-system-info.py) | The environment header: chip, RAM, OS, oMLX version, API endpoint. | no |
| [`model-sizes.py`](model-sizes.py) | Weights-vs-folder size per model on disk. | no |

## Running

```bash
python3 scripts/measure/collect-system-info.py
python3 scripts/measure/model-sizes.py
python3 scripts/measure/benchmark.py
python3 scripts/measure/code-matrix-test.py
python3 scripts/measure/code-benchmark.py --selftest
python3 scripts/measure/code-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
python3 scripts/measure/grammar-test.py --selftest
python3 scripts/measure/context-memory-test.py --selftest
python3 scripts/measure/hallucination-test.py --selftest
python3 scripts/measure/repo-analysis-test.py --repo ~/Sites/net-traffic-control-catalog
```

`benchmark.py` reads the API key from `~/.omlx/settings.json` and unloads every
known model before each run, so the numbers are not contaminated by a
previously loaded model. The output is the same table that appears in
[`../../docs/reference/RESULTS.md`](../../docs/reference/RESULTS.md).
