# `docs/analysis/` — reading the numbers

What the measurements mean, beyond the table.

- [`README.md`](README.md) — this file: the analysis and the red-team reading.
- [`redteam.md`](redteam.md) — the offensive-capability analysis in full.
- [`net-traffic-control-catalog.md`](net-traffic-control-catalog.md) — how the six models analyse a real repository, measured.

## Throughput: why the order is what it is

The ranking (73 → 18 tok/s) tracks two properties, not model "size":

1. **Active parameters per token.** Five of six models are MoE; they read only
   ~3–4B parameters to produce a token. Qwen3.8-27B is **dense** — it reads all
   27B — and is last by a wide margin.
2. **Memory bandwidth per byte read.** On a bandwidth-bound machine, decode speed
   is roughly `bandwidth / bytes-read-per-token`. A 4-bit MoE that touches only
   its active experts lands in the tens of tokens per second.

The two 35B MoE models (Qwen3.6 and its heretic build) are within ~3% of each
other, which is what you expect when the only change is the abliteration of
directions the model rarely uses.

## Speed vs openness

| Model | tok/s | Uncensored |
| :--- | ---: | :---: |
| Qwen3.6-35B | 73.4 | no |
| Qwen3.6-35B-Heretic | 71.1 | **yes** |
| Ornith-1.5-35B | 60.2 | no |
| gemma-4-26B-Heretic | 60.1 | **yes** |
| Qwen3-Coder-30B | 42.6 | no |
| Qwen3.8-27B-Uncensored | 18.2 | **yes** |

You do not pay a speed tax for being uncensored: the fastest uncensored model is
second overall, and the fastest model overall is only ~3% ahead. That is the
single most useful finding for someone choosing a daily driver.

## The red-team result, in one line

**Web exploitation is solved; reverse engineering is not.** See
[`redteam.md`](redteam.md).

## What is not measured

- Answer quality (correctness, helpfulness).
- Tool-calling reliability.
- Long-context accuracy.
- Time-to-first-token (the axis oMLX's own claims are about).

A throughput number is a speed limit, not a review.
