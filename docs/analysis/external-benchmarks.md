# External benchmarks — what we took, and what we did not

This repository is self-contained: every number comes from a script here. This
page records the outside projects we looked at, what (if anything) we adopted,
and why most of them were **cited rather than copied**. It exists so the
influence is explicit and the licence position is clear.

## The rule we applied

- **No licence file → do not copy.** A README claiming a licence is not a
  licence. We read those repositories for ideas and wrote our own problems,
  cases and scoring; we link them here.
- **Permissive licence → safe to reuse**, but we still prefer original material
  so the harness stays standard-library-only and dependency-free.

## Adopted (original work, idea credited)

| Project | Licence | What we built from it |
| :--- | :--- | :--- |
| [`liohunter1/llm-coding-benchmark`](https://github.com/liohunter1/llm-coding-benchmark) | none (README claims MIT) | The shape of [`../../problems/`](../../problems/README.md): a catalogue of algorithmic problems with executable hidden cases. Our problems, cases and solutions are original. |
| [`akitaonrails/llm-coding-benchmark`](https://github.com/akitaonrails/llm-coding-benchmark) | none | Reinforced the *run the code, do not just parse it* approach; our [`code-benchmark.py`](../../scripts/measure/code-benchmark.py) is the standard-library result. |
| [`egavrin/deal-llm-grammar-benchmark`](https://github.com/egavrin/deal-llm-grammar-benchmark) | none | The structured-output idea behind [`grammar-test.py`](../../scripts/measure/grammar-test.py) — does the model return a value that matches the schema? |
| [`HUST-AI-HYZ/MemoryAgentBench`](https://github.com/HUST-AI-HYZ/MemoryAgentBench) | MIT | The long-context memory idea behind [`context-memory-test.py`](../../scripts/measure/context-memory-test.py) — retrieval, conflict resolution and aggregation over a long context. Our generator and questions are original. |

## Cited, not adopted

| Project | Licence | Why we only link it |
| :--- | :--- | :--- |
| [`openai/frontier-evals`](https://github.com/openai/frontier-evals) | MIT | PaperBench, SWE-Lancer and EVMBench are full research harnesses (PaperBench alone ships thousands of files and needs `uv` and large dependencies). Our [offensive layer](../security/OFFENSIVE-BENCHMARK.md) echoes EVMBench's *smart-contract security* theme at a scale that fits one Mac, but we do not vendor their data. |
| [`wgwang/awesome-LLM-benchmarks`](https://github.com/wgwang/awesome-LLM-benchmarks) | none | An index, not code. Useful for survey; nothing to run. |
| [`tongye98/Awesome-Code-Benchmark`](https://github.com/tongye98/Awesome-Code-Benchmark) | MIT | An index of code benchmarks. Referenced for context, not vendored. |
| [`ooples/token-optimizer-mcp`](https://github.com/ooples/token-optimizer-mcp) | MIT | A token-reduction MCP server, not a benchmark. It is adjacent tooling (prompt/token optimisation) rather than a test we can score; linked for related work. |

## What this means for our test suite

The tests we added live beside the numbers they produce, and each one is small
enough to read in a sitting:

| Test | Script | Scores |
| :--- | :--- | :--- |
| Coding correctness | [`code-benchmark.py`](../../scripts/measure/code-benchmark.py) | do the model's solutions pass hidden cases |
| Format / grammar adherence | [`grammar-test.py`](../../scripts/measure/grammar-test.py) | is the answer a schema-valid JSON value |
| Long-context memory | [`context-memory-test.py`](../../scripts/measure/context-memory-test.py) | retrieval, conflict resolution, aggregation in a long context |

Each has an offline `--selftest` that runs with no model and no server, and each
`--selftest` is part of [`../../test/test.sh`](../../test/test.sh). That is what
makes the suite growable: a new idea becomes a script, a script proves itself
offline, and the gate stays green without a GPU.
