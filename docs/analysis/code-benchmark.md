# Coding correctness — do the models' solutions actually pass?

Throughput says how fast a model writes; this says whether what it writes is
correct. Each model is asked for a Python solution to a problem, the ```` ```python ````
block is extracted, written to a file, **executed** against hidden cases under a
20-second timeout, and scored on how many pass. It is the executable companion to
[`../../scripts/measure/code-matrix-test.py`](../../scripts/measure/code-matrix-test.py),
which only checks that the code *parses*.

The first run: `2026-11-12`, six models, five problems, 56 cases.

| Model | p01 two-sum | p02 LIS | p03 median | p04 intervals | p05 word-break | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: |
| `Qwen3.6-35B-A3B` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Ornith-1.5-35B-A3B` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `gemma-4-26B-A4B-it-heretic` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3-Coder-30B-A3B-Instruct` | 12/12 | 10/10 | ❌ | 12/12 | 11/12 | **45/46** |
| `Devstral-Small-2-24B-Instruct` | 12/12 | 10/10 | 10/10 | 12/12 | 11/12 | **55/56** |
| `Qwen3.8-27B-Uncensored-MLX` | 12/12 | 10/10 | ❌ | 12/12 | ❌ | **34/34** |

The second run: `2026-11-22`, the three campaign models, each at both sampling
settings (and Inkling with its MTP draft on and off — identical results, so one
row per base/hot pair).

| Model (profile) | p01 two-sum | p02 LIS | p03 median | p04 intervals | p05 word-break | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: |
| `Kimi-Linear-48B` (`kimi-linear`) | 12/12 | 10/10 | 5/10 | 12/12 | 12/12 | **51/56** |
| `Kimi-Linear-48B` (`kimi-linear-hot`) | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `GLM-4.7-Flash` (`glm47`) | 12/12 | 2/10 | 5/10 | ❌ | ❌ | **19/32** |
| `GLM-4.7-Flash` (`glm47-hot`) | 12/12 | 5/10 | ❌ | 3/12 | 1/12 | **21/46** |
| `Inkling-2-Mini` (`inkling`, all variants) | 12/12 | 10/10 | ❌ | 12/12 | 12/12 | **46/46** |

## What the numbers mean

- **Four of six models were perfect.** The three general Qwen3.6/Ornith models and
  gemma-4 solved all 56 cases. On this corpus, "can it code" does not separate them.
- **The failures are load failures, not wrong answers.** A ❌ is a problem whose
  code never ran: the module failed to import, so no case could be attempted and
  the total drops (46, 34). The harness reports this as an error, not as a
  correct-looking zero.
  - Qwen3-Coder's `p03` answer had invalid indentation after an `else`
    (`expected an indented block ... line 37`) — a syntax error.
  - Qwen3.8 did not define `find_median` (p03) or `word_break` (p05) at all.
- **One case, one miss.** Qwen3-Coder's only partial pass is `p05` `empty_string`:
  its `word_break("")` returned `True` where the reference (and the statement)
  require `False`.
- **The bigger model was the slowest.** Qwen3.8 needed 18–50 s per answer;
  the 35B Qwen3.6 models needed 1.6–6.4 s. Qwen3.8 also failed to define the
  function twice. Slow did not mean thorough.
- **The model labelled "Coder" is not the best coder here.** Qwen3-Coder scored
  45/46 while four general models scored 56/56, and it was the only one to
  produce a plain syntax error. Devstral — a code model that is honest about
  being one — defined every function and passed 55/56, losing only the same
  `empty_string` edge case. Paying for a code specialisation bought completeness
  from Devstral and nothing from Qwen3-Coder.

## The 2026-11-22 campaign

- **Kimi-Linear-48B is the strongest of the three**, and the only new model that
  reached a perfect score — but only at `temp 1.0` (56/56); at `temp 0.2` it loses
  five `p03` cases (the empty-array/odd-length edges) for 51/56. On this suite the
  higher temperature bought correctness, not creativity.
- **GLM-4.7-Flash is the weakest coder here.** It failed `p04` and `p05` outright
  at `temp 0.2` (invalid syntax) and recovered only partially at `temp 1.0`
  (21/46). A reasoning model served with thinking off is not automatically a good
  code model.
- **Inkling-2-Mini is consistent but incomplete.** Every one of its four profiles
  (base, hot, MTP, MTP-hot) scored the same 46/46: it never defined `find_median`,
  so `p03` could not run. MTP on/off and temperature on/off changed nothing.
- **Unchanged: "Coder" is still not the best coder.** With the campaign added, the
  56/56 club is four models at `temp 0.2` plus Kimi-Linear at `temp 1.0`, and
  Qwen3-Coder is not in it.

## Why the failures are credible

The harness does not trust a model to grade itself. Model output is untrusted
code, and the rails are explicit ([`../../docs/testing/README.md`](../../docs/testing/README.md)):

- it runs in a throwaway temp directory, as a subprocess, under a 20 s timeout;
- the verdict is written to a file, so a solution cannot spoof it via stdout;
- the interpreter runs with `-I` (isolated: no user site, no env influence);
- a model's own top-level demo block cannot sink an otherwise-defined solution —
  the runner keeps the namespace and looks for the function even if the demo
  raised (this is what turned three spurious "no result" rows into the real
  errors above).

A ❌ here is a real, reproducible failure of the model's code.

## Reproducing

```bash
python3 scripts/measure/code-benchmark.py --selftest          # no model
python3 scripts/measure/code-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
```

`--selftest` runs each reference solution through the same runner and asserts every
case passes; it is step 9 of [`../../test/test.sh`](../../test/test.sh) and needs
no model and no network.

Raw run: [`../../evidence/code-benchmark-2026-11-11.md`](../../evidence/code-benchmark-2026-11-11.md)
and [`../../reference/code-benchmark.json`](../../reference/code-benchmark.json); the
2026-11-22 campaign is [`../../reference/code-benchmark-2026-11-22.json`](../../reference/code-benchmark-2026-11-22.json).

## Attribution

The idea of a problem catalogue with executable hidden cases follows
[`liohunter1/llm-coding-benchmark`](https://github.com/liohunter1/llm-coding-benchmark)
(which ships no licence file) and [`akitaonrails/llm-coding-benchmark`](https://github.com/akitaonrails/llm-coding-benchmark).
The problems, cases and reference solutions here are original to this repository.
See [`external-benchmarks.md`](external-benchmarks.md).
