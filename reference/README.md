# reference

Public, machine-readable copies of the facts in this repository. An application
can read these without parsing Markdown.

| File | What it holds |
| :--- | :--- |
| [`models.json`](models.json) | Every model: id, size, HuggingFace repo, classification. |
| [`huggingface.json`](huggingface.json) | The verified HuggingFace links and upstream base models. |
| [`results.json`](results.json) | Every measured number: throughput, disk, and the red-team scorecard. |
| [`repo-analysis.json`](repo-analysis.json) | The repository-analysis run: per-model answer time, decode speed and fact recall on [`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog). |
| [`code-benchmark.json`](code-benchmark.json) | The coding-correctness run: per-model, per-problem pass counts and the code that produced them. |
| [`grammar.json`](grammar.json) | The format/grammar run: per-model, per-schema validity. |
| [`context-memory.json`](context-memory.json) | The long-context memory run: retrieval, conflict and aggregate answers. |

The hallucination corpus itself lives in
[`../data/languages.json`](../data/languages.json) and is tabulated in
[`../docs/reference/LANGUAGES.md`](../docs/reference/LANGUAGES.md).

The **licences** of the models are read from their own cards and tabulated in
[`../docs/reference/LICENSES.md`](../docs/reference/LICENSES.md): download is not
the same as a grant, so that file separates the Apache-2.0 models from the
conditional (FLUX 3) and the undeclared (Ornith-1.5).

These are the public counterparts of [`../config/sources.json`](../config/sources.json)
(the registry) and the prose in [`../docs/reference/`](../docs/reference/). The
analysis script reads `results.json`; the manifest hashes it.

`results.json` is the **single source** of the numbers in the README and the
charts. If you re-measure, edit it (or regenerate it from a new run) and re-run
`python3 scripts/analysis/analyze-results.py`.
