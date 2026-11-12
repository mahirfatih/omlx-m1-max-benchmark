# problems

Algorithmic coding problems with **executable** test cases. Where
[`../scripts/measure/code-matrix-test.py`](../scripts/measure/code-matrix-test.py)
only checks that a model's code *parses*, the harness here writes the model's code
to a file, runs it against hidden cases, and scores it on correctness.

The format is a small, self-contained convention:

```text
problems/<id>/
├── problem.md          # the statement given to the model
├── rubric.md           # how the score is built
├── solutions/
│   └── solution.py     # the reference solution (used by --selftest)
└── tests/
    └── test-cases.json # {"function": ..., "cases": [...]}
```

The runner is [`../scripts/measure/code-benchmark.py`](../scripts/measure/code-benchmark.py).
It is **standard library only** — no pytest, no dependencies — so it runs on a
stock macOS Python.

## Problems

| ID | Problem | Difficulty |
| :--- | :--- | :--- |
| [`p01-two-sum`](p01-two-sum/problem.md) | Two-sum, O(n) | medium |
| [`p02-longest-increasing-subsequence`](p02-longest-increasing-subsequence/problem.md) | Longest increasing subsequence | hard |
| [`p03-median-two-sorted`](p03-median-two-sorted/problem.md) | Median of two sorted arrays | expert |
| [`p04-merge-intervals`](p04-merge-intervals/problem.md) | Merge overlapping intervals | medium |
| [`p05-word-break`](p05-word-break/problem.md) | Can the string be segmented? | hard |

## Self-test (no model, no network)

```bash
python3 scripts/measure/code-benchmark.py --selftest
```

This runs each `solutions/solution.py` through the same runner the models are
scored with, and asserts every case passes. It proves the harness and the cases
agree **before** any model is involved, and it runs in
[`../test/test.sh`](../test/test.sh).

## Running against models

```bash
python3 scripts/measure/code-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
```

The model is asked for a Python solution; a ```` ```python ```` block is
extracted, executed against the cases under a timeout, and scored. Model output
is untrusted code: it runs in a throwaway temp directory as a subprocess with a
time limit. See [`../docs/testing/README.md`](../docs/testing/README.md).

## Attribution

The idea of a problem catalogue with executable cases follows
[`liohunter1/llm-coding-benchmark`](https://github.com/liohunter1/llm-coding-benchmark).
The problems, cases and reference solutions here are written for this repository.
