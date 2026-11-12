# Choosing a model

Six models, three jobs. This page is a decision aid, not a quality ranking —
quality was not measured here.

## Quick decision

| If you want... | Use | Why |
| :--- | :--- | :--- |
| Fastest general model, coding included | **Qwen3.6-35B-A3B** (`qwen3`) | 73.4 tok/s, largest output budget (4096), official Qwen alignment. |
| Fastest **uncensored** model | **Qwen3.6-35B-A3B-Uncensored-Heretic** (`qwen36-heretic`) | 71.1 tok/s, abliterated, ~88% fewer refusals, negligible capability loss. |
| A non-Qwen uncensored option | **gemma-4-26B-A4B-it-heretic** (`gemma4-heretic`) | 60.1 tok/s, Google Gemma base, heretic + decensored. |
| A different architecture to cross-check | **Ornith-1.5-35B-A3B** (`qwen3`) | 60.2 tok/s, independent RL-trained model, not a Qwen/Gemma variant. |
| Coding with a deep context | **Qwen3-Coder-30B-A3B-Instruct** (`qwen3`) | Purpose-built coder, 42.6 tok/s, only 16 GB on disk. |
| Maximum size / uncensored, latency-tolerant | **Qwen3.8-27B-Uncensored** (`qwen36-heretic`) | 27B **dense** abliterated; 18.2 tok/s — half the speed, for batch work. |

## By role

### Agentic coding loop

The loop is latency-sensitive: every tool call pays the decode speed. **Qwen3.6-35B-A3B**
is the default — fastest, and its `qwen3` profile allows 4096 output tokens, which
matters when the model writes a whole file. **Qwen3.6-35B-Heretic** is the choice
when content policy is the constraint rather than speed; it is within ~3% of the
top model.

### Chat and writing

**gemma-4-26B-Heretic** and **Qwen3.6-35B-Heretic** both sit at ~60–71 tok/s and
are uncensored. Gemma is a useful second opinion because it is not a Qwen
derivative; when the two agree, the answer is less likely to be a family quirk.

### Draft-heavy batch work

If a job can wait — long generations, offline data processing — **Qwen3.8-27B-Uncensored**
trades speed for size. At 18.2 tok/s it is roughly four times slower than the
MoE models, but it is a 27B dense abliterated model and reads the whole weight
set per token.

## The speed / openness map

```text
tok/s
 73 ┤ ● Qwen3.6-35B        (standard)
 71 ┤   ● Heretic          (uncensored + heretic)
 60 ┤     ● Ornith ● gemma-4-heretic
 43 ┤       ● Qwen3-Coder
 18 ┤         ● Qwen3.8-Uncensored
    └────────────────────────────────────────────────
        fast, aligned → slow, uncensored/large
```

## Memory and residency

All six models are **lazy-loaded** and unloaded after 180 s idle, so no model
occupies memory when it is not in use. One loaded model costs ~17–20 GB; two cost
~38 GB; the guard accepts a third only if the prefill estimate fits. This is why
switching models is cheap and why the benchmark unloads between models.

| Model | On disk | Loaded (approx.) |
| :--- | ---: | ---: |
| gemma-4-26B-Heretic | 15 GB | ~16 GB |
| Qwen3.8-27B-Uncensored | 15 GB | ~17 GB |
| Qwen3-Coder-30B | 16 GB | ~18 GB |
| Ornith-1.5-35B | 18 GB | ~19 GB |
| Qwen3.6-35B | 19 GB | ~20 GB |
| Qwen3.6-35B-Heretic | 19 GB | ~20 GB |

Exact runtime memory depends on context length; longer contexts grow the KV cache
even at 4-bit.

## What is not in this decision

- **Answer quality.** Not measured. Test on your own tasks before committing.
- **Tool-calling reliability.** Not measured, though the models differ in
  format support; oMLX advertises formats for JSON, Qwen, Gemma, GLM and MiniMax.
- **Long-context accuracy.** The 32K context is configured, not evaluated.

See [`../reference/MODELS.md`](../reference/MODELS.md) for the full model table and
the uncensored/heretic evidence, and
[`../reference/PROFILES.md`](../reference/PROFILES.md) for the settings each model
runs with.
