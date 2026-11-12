# Repository analysis — the models on a real project

The throughput benchmark measures how *fast* a model talks. This one measures
whether it *reads*. Each model is handed the same digest of a real, shipped
repository and asked the same analysis task; the run records the answer time,
the decode speed, and how many of the repository's own documented facts the
answer cites.

**Target:** [`mahirfatih/net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog)
— a CC0 JSON catalog of 6,731 hosts, 27 categories and 22 services, ~232 KB.
This is the same shape this repository mirrors.

Raw output: [`../../evidence/repo-analysis-2026-11-11.md`](../../evidence/repo-analysis-2026-11-11.md).
Data: [`../../reference/repo-analysis.json`](../../reference/repo-analysis.json).

## What was measured

Each model was given one digest — the file tree, the README, and statistics
computed from `catalog.json` (host count, category counts, top categories) —
and this task:

> Triage this repository: what it is, how it is structured, one concrete
> data-quality risk, and a one-line verdict. Cite the specific numbers you used.

The digest is identical for every model. The data is not fed as a document to
*find* the numbers in; it is already summarised, so the task is reasoning over
supplied facts, not retrieval.

**Score** = how many of twelve documented facts the answer cites
(`6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test,
finance, domain`). It is a recall proxy: a model that genuinely read the digest
names the numbers; one that pattern-matched does not.

## Results — 2026-11-11

| Model | Answer (s) | Tokens | tok/s | Facts recovered | Score |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `Ornith-1.5-35B-A3B` | 6.8 | 366 | 53.5 | 10/12 | **83%** |
| `Qwen3-Coder-30B-A3B-Instruct` | 6.6 | 235 | 35.8 | 7/12 | **58%** |
| `Qwen3.6-35B-A3B` | 4.8 | 298 | 62.6 | 6/12 | **50%** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | 4.7 | 269 | 57.8 | 5/12 | **42%** |
| `gemma-4-26B-A4B-it-heretic` | 4.3 | 167 | 38.6 | 4/12 | **33%** |
| `Qwen3.8-27B-Uncensored-MLX` | 46.1 | 700 | 15.2 | 0/12 | **0%** |

## Reading the result

**The fastest answer was not the best one.** Ornith-1.5 wrote 366 tokens in
6.8 s (53.5 tok/s) and recovered 10 of 12 facts, including the exact host count
and the finance skew. Qwen3.6-35B answered 30% faster (4.8 s, 62.6 tok/s) and
recovered only half as many. Speed and care are different axes.

**Most models recovered the *shape* and missed the *numbers*.** The recurring
miss is the triple `6731 / 27 / 22` and the licence `CC0`. Several models
described the repository correctly in prose — "a JSON catalog mapping hostnames
to categories and services" — but never cited the counts, which is exactly the
difference between summarising and analysing.

**Three models invented the file counts.** Qwen3.6-35B and its heretic build
both stated that `scripts/` holds "6,863 files (98.4% of the tree)". The digest
says **136 tracked files**. That is a hallucination, not a rounding error, and
it is the most useful finding here: a model can reason fluently about a
repository while fabricating its structure. Ornith-1.5 did not; it repeated the
real figures.

**The slowest model returned nothing.** `Qwen3.8-27B-Uncensored` spent 46.1 s
and its entire 700-token budget, and emitted no answer text — the run is
recorded as 0/12 with an empty excerpt. At 15.2 tok/s it is also, by a wide
margin, the slowest model here (see [`../reference/RESULTS.md`](../reference/RESULTS.md)).
For an interactive analysis task it is not usable; this run is the clearest
evidence of that in the repository.

## Which model is good at what

| If you want to… | Use | Not |
| :--- | :--- | :--- |
| Analyse a repo and cite the numbers | `Ornith-1.5-35B-A3B` | gemma-4, Qwen3.8 |
| A fast first-pass summary | `Qwen3.6-35B-A3B` | Qwen3.8 |
| Anything where you will read the answer | any of the five | `Qwen3.8-27B-Uncensored` |

## Caveats

- One run per model, one digest. A single hallucinated figure is a single
  observation; the file-count error reproduced across two models, which makes it
  more than noise.
- "Facts recovered" is recall, not correctness: a model can cite a number and
  still misread it. The raw answers are the check.
- The digest is pre-summarised, so this measures reasoning over facts, not
  retrieval from a large document.

## Reproducing

```bash
python3 scripts/measure/repo-analysis-test.py \
    --repo ~/Sites/net-traffic-control-catalog \
    --out evidence/repo-analysis-$(date +%F).md \
    --json-out reference/repo-analysis.json
```

Point `--repo` at any checkout. The offline gate
([`../../test/test.sh`](../../test/test.sh), step 8) asserts that this
repository links the target and that the analysis data is present and scored.
