# `docs/analysis/` — reading the numbers

What the measurements mean, beyond the table.

- [`README.md`](README.md) — this file: the analysis and the red-team reading.
- [`redteam.md`](redteam.md) — the offensive-capability analysis in full.
- [`net-traffic-control-catalog.md`](net-traffic-control-catalog.md) — how the models analyse a real repository, measured.
- [`code-benchmark.md`](code-benchmark.md) — the models' code, executed: which pass hidden cases and where they fail.
- [`hallucination.md`](hallucination.md) — 102 languages, each probed with a real API and a fabricated twin: do the models invent APIs, and what did the one slow model cost.
- [`external-benchmarks.md`](external-benchmarks.md) — the outside projects we looked at.

## Throughput: why the order is what it is

The ranking (73 → 12 tok/s) tracks two properties, not model "size":

1. **Active parameters per token.** Eight of ten models are MoE; they read only
   ~3–4B parameters to produce a token. Qwen3.8-27B and Devstral-Small-2 are
   **dense** — they read all 27B/24B — and are last by a wide margin.
2. **Memory bandwidth per byte read.** On a bandwidth-bound machine, decode speed
   is roughly `bandwidth / bytes-read-per-token`. A 4-bit MoE that touches only
   its active experts lands in the tens of tokens per second.

The two 35B MoE models (Qwen3.6 and its heretic build) are within ~3% of each
other, which is what you expect when the only change is the abliteration of
directions the model rarely uses. Kimi-Linear-48B is the interesting counter-case:
a 48B MoE that reaches the 35B pair's speed because 3 of its 4 layers use
**linear attention** (Kimi Delta Attention), so its per-token read is far smaller
than its name suggests.

## Speed vs openness

| Model | tok/s | Uncensored |
| :--- | ---: | :---: |
| Qwen3.6-35B | 73.4 | no |
| Qwen3.6-35B-Heretic | 71.1 | **yes** |
| Ornith-1.5-35B | 60.2 | no |
| gemma-4-26B-Heretic | 60.1 | **yes** |
| Kimi-Linear-48B | 59.0 | no |
| Qwen3-Coder-30B | 42.6 | no |
| GLM-4.7-Flash | 34.9 | no |
| Inkling-2-Mini | 25.4 | no |
| Qwen3.8-27B-Uncensored | 18.2 | **yes** |
| Devstral-Small-2-24B | 12.4 | no |

You do not pay a speed tax for being uncensored: the fastest uncensored model is
second overall, and the fastest model overall is only ~3% ahead. That is the
single most useful finding for someone choosing a daily driver.

## The red-team result, in one line

**Web exploitation is solved; reverse engineering is not.** See
[`redteam.md`](redteam.md) (the 2026-11-22 campaign did not re-run it).

## What is not measured

- Answer quality (correctness, helpfulness).
- Tool-calling reliability.
- Long-context accuracy.
- Time-to-first-token (the axis oMLX's own claims are about).

A throughput number is a speed limit, not a review.
