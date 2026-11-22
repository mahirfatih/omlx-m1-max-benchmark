# Choosing a model

Ten models, three jobs. This is a decision aid, and every claim here is a
measurement made on this machine — the speed, the coding cases, the long-context
tasks, the hallucination probes and the red-team challenges all ran here, and
each number links to the file that produced it. Where something was **not**
measured — the red team on the three 2026-11-22 models, hallucination on Devstral
and Qwen3.8 — the page shows a dash rather than implying it was.

If you read one paragraph: **load `Qwen3.6-35B-A3B` and use it for almost
anything.** It is the fastest model here, it solved every coding problem, and it
never invented an API. Reach for a different one only for a specific reason
listed below.

## Quick decision

| If you want... | Use | Why |
| :--- | :--- | :--- |
| **One model for everything** | **Qwen3.6-35B-A3B** (`qwen3`) | 73.4 tok/s, **56/56** coding cases in 2.9 s, 0% hallucination. Nothing else beats it on any task measured here. |
| Uncensored, no meaningful loss | **Qwen3.6-35B-A3B-Uncensored-Heretic** (`qwen36-heretic`) | 71.1 tok/s, 56/56 coding, 0% hallucination — indistinguishable from the aligned model except that it does not refuse. |
| Uncensored, different family | **gemma-4-26B-A4B-it-heretic** (`gemma4-heretic`) | 60.1 tok/s, 56/56 coding, 0% hallucination. A Gemma base, so it fails differently — useful as a second opinion. |
| A non-Qwen, non-Gemma cross-check | **Ornith-1.5-35B-A3B** (`qwen3`) | 60.2 tok/s, 56/56 coding. Independent RL-trained model. |
| **Long context and a strong analyst** | **Kimi-Linear-48B** (`kimi-linear`) | 59.0 tok/s, **3/3** long context, **8/12** repo facts — and **56/56** coding at `temp 1.0`. The best of the 2026-11-22 models. |
| **Coding, when correctness matters most** | **Devstral-Small-2-24B-Instruct** (`devstral`) | 55/56, and the only model that **defines every function it is asked for**. Slow (12.4 tok/s) — pay for completeness. |
| Coding, fast and small on disk | **Qwen3-Coder-30B-A3B-Instruct** (`qwen3`) | 42.6 tok/s, 16 GB. But **45/46** and one syntax error: fast, not the most correct. |
| A reasoning MoE, long-context safe | **GLM-4.7-Flash** (`glm47`) | 34.9 tok/s, **3/3** long context, 31 GB. But the **weakest coder here** (21/46) — use it to read, not to write. |
| Nothing in particular | ~~**Qwen3.8-27B-Uncensored**~~ · ~~**Inkling-2-Mini**~~ | **Do not use on this machine.** Qwen3.8: 18.2 tok/s (4× slower), **0/3** long context. Inkling: **0/3** long context and it empties its own answer while thinking. |

## The ten models, side by side

Every cell is measured. A dash means the run has not happened, not that it failed.

| Model | tok/s | Coding | Long context | Hallucination | Red-team | On disk |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Qwen3.6-35B-A3B` | **73.4** | 56/56 | 2/3 | 0% | 4/5 | 19 GB |
| `Qwen3.6-35B-Uncensored-Heretic` | 71.1 | 56/56 | 2/3 | 0% | 4/5 | 19 GB |
| `Ornith-1.5-35B-A3B` | 60.2 | 56/56 | 2/3 | 0% | 4/5 | 18 GB |
| `gemma-4-26B-A4B-it-heretic` | 60.1 | 56/56 | 2/3 | 0% | 4/5 | 15 GB |
| `Kimi-Linear-48B` | 59.0 | **56/56**² | **3/3** | 0% | — | 27 GB |
| `Qwen3-Coder-30B-A3B-Instruct` | 42.6 | 45/46 | 2/3 | 0% | 3/5 | 16 GB |
| `GLM-4.7-Flash` | 34.9 | 21/46³ | **3/3** | **2%**⁵ | — | 31 GB |
| `Inkling-2-Mini` | 25.4 | 46/46⁴ | **0/3** | 0% | — | 16 GB |
| `Qwen3.8-27B-Uncensored` | 18.2 | 34/34¹ | **0/3** | — | 4/5 | 15 GB |
| `Devstral-Small-2-24B-Instruct` | 12.4 | **55/56** | **3/3** | — | — | 25 GB |

¹ 100% of what it answered — but it only wrote 3 of the 5 functions, so two
problems were never attempted. ² At `temp 1.0`; at `temp 0.2` it is 51/56. ³ The
better of its two runs (`temp 1.0`); at `temp 0.2` it is 19/32. ⁴ It never defines
`find_median`, so it only ever answers four of the five problems. ⁵ The one model
that called a fabricated API real (`matlab zerosx`, `NSArrayx`) — in both
temperature runs, at up to 1.00 confidence.

## By role

### Agentic coding loop

The loop is latency-sensitive: every tool call pays the decode speed. **Qwen3.6-35B-A3B**
is the default and there is no close second — it is the fastest model here and it
passed every coding case in under 3 seconds. **Qwen3.6-35B-Heretic** is the choice
when content policy, not speed, is the constraint; it is within 3% of the top
model on every measurement.

**Reach for Devstral only when the answer must be complete.** It is 6× slower
(12.4 tok/s), but on the coding suite it is the model that never left a function
unwritten. That is the failure that actually costs you a debugging session: not a
slow answer, an answer that silently omits half the work.

### Chat and writing

Anything from the top four works and they are within 13 tok/s of each other.
**gemma-4-26B-Heretic** earns its place as a *different* model — when Gemma and a
Qwen agree, the answer is less likely to be a family quirk.

### Long documents

**Kimi-Linear-48B and Devstral both passed all three long-context tasks**,
including the aggregate question — pulling three facts from three separate places
into one answer — that the four Qwen/Gemma models failed. Kimi does it at 59 tok/s
to Devstral's 12.4, which makes it the better default for a long prompt: a 48B MoE
that outruns its size because three of its four layers are *linear attention*
(Kimi Delta Attention). GLM-4.7-Flash also scores 3/3, so the new models read a
document better than the old ones did.

The task is small (three questions, one run of 6.3 k tokens), so treat this as
"worth a second look", not "solved". But 3/3 against four models at 2/3 is the
clearest signal in this repository.

### Unsafe or unrestricted work

**Qwen3.6-35B-Heretic** first — it matches the aligned model on every capability
measurement and simply does not refuse. **gemma-4-26B-Heretic** is the second
opinion from a different family.

**Note what the red-team table does *not* show:** the uncensored models score
exactly what the aligned ones do (4/5). Removing the refusal did not make them
better at finding a bug, because a refusal is not what was in the way. The three
2026-11-22 models were not put through the red team at all.

### What not to run

**Qwen3.8-27B-Uncensored.** It is the only *dense* 27B model here, so every token
reads all 27B of weights, and on this machine that costs 4× the speed of the MoE
models for worse results: 0/3 on long context, two coding functions never
written, 34.8 s per answer. Nothing measured here justifies the trade.

**Inkling-2-Mini.** It cannot turn off its thinking block, so a small output
budget is spent reasoning and the answer comes back empty — it produced **no text
at all** in three of its four repository-analysis profiles, and it is the only
model here with **0/3** on long context while still being the slowest generator.
Its bundled MTP draft did not speed it up either.

## Why the slow ones are slow

Speed on this machine is set by memory bandwidth, not compute. A Mixture-of-Experts
model reads only its active experts per token (~3–4B of a 35B model); a dense
model reads the whole weight set.

```text
tok/s   model                    weights read per token
 73.4   Qwen3.6-35B-A3B          MoE  ~3B active
 71.1   Qwen3.6-35B-Heretic      MoE  ~3B active
 60.2   Ornith-1.5-35B-A3B       MoE  ~3B active
 60.1   gemma-4-26B-A4B-heretic  MoE  ~4B active
 59.0   Kimi-Linear-48B          MoE  ~3B active, 3/4 layers linear attention
 42.6   Qwen3-Coder-30B          MoE  ~3B active
 34.9   GLM-4.7-Flash            MoE  ~3B active, 8-bit
 25.4   Inkling-2-Mini           MoE  ~3.4B active, looped, multimodal
 18.2   Qwen3.8-27B-Uncensored   dense  27B  <- 4x slower, same reason
 12.4   Devstral-Small-2-24B     dense  24B  <- slowest, and the most complete
```

The two dense models are slow for the same reason and it is not a defect — it is
the arithmetic of reading 24–27B parameters for every single token off a shared
memory bus. If a task is latency-tolerant, that cost can buy completeness
(Devstral) or nothing (Qwen3.8).

## Memory and residency

All models are **lazy-loaded** and unloaded after 180 s idle, so nothing occupies
memory when it is not in use. One loaded model costs ~16–34 GB; two cost ~40–65 GB.
Switching is cheap, which is why the benchmark unloads between models.

| Model | On disk | Loaded (approx.) |
| :--- | ---: | ---: |
| gemma-4-26B-Heretic | 15 GB | ~16 GB |
| Qwen3.8-27B-Uncensored | 15 GB | ~17 GB |
| Qwen3-Coder-30B | 16 GB | ~18 GB |
| Inkling-2-Mini | 16 GB | ~18 GB |
| Ornith-1.5-35B | 18 GB | ~19 GB |
| Qwen3.6-35B / -Heretic | 19 GB | ~20 GB |
| Devstral-Small-2-24B | 25 GB | ~26 GB |
| Kimi-Linear-48B | 27 GB | ~28 GB |
| GLM-4.7-Flash | 31 GB | ~34 GB |

Exact runtime memory depends on context length; longer contexts grow the KV cache
even at 4-bit. GLM-4.7-Flash is 8-bit and the largest single footprint here — on a
64 GB machine, do not expect to hold it and another large model at once.

## What is still not measured

- **Tool-calling reliability.** Not measured, though the models differ in format
  support; oMLX advertises formats for JSON, Qwen, Gemma, GLM and MiniMax.
- **Instruction-following on long, multi-step tasks.** The coding suite measures
  single-function answers, not agentic persistence.
- **The red team on the 2026-11-22 models.** Kimi-Linear, GLM and Inkling were not
  run through it; the table shows a dash rather than a guess.
- **Hallucination on Devstral and Qwen3.8.** Those two have not been probed; the
  three 2026-11-22 models were probed in the campaign, and the table shows their
  numbers rather than a dash.
- **Anything at a different context length.** Every measurement here is at the
  settings in [`../reference/PROFILES.md`](../reference/PROFILES.md).

## Where the numbers come from

| Column | File | Script |
| :--- | :--- | :--- |
| tok/s | `reference/results.json` | `scripts/measure/benchmark.py` |
| Coding | `reference/code-benchmark.json`, `…-2026-11-22.json` | `scripts/measure/code-benchmark.py` |
| Long context | `reference/context-memory.json`, `…-2026-11-22.json` | `scripts/measure/context-memory-test.py` |
| Hallucination | `reference/hallucination.json`, `…-2026-11-22.json` | `scripts/measure/hallucination-test.py` |
| Red-team | `evidence/redteam-*.md` | `scripts/security/redteam-benchmark.py` |

The hallucination numbers above are per-model summaries. The probe-by-probe record
— every language, every API name, what each model said about it, and the
confidence it stated — is
[`../../reference/hallucination-records.md`](../../reference/hallucination-records.md)
(the original 2026-11-12 run) and
[`../../reference/hallucination-records-2026-11-22.md`](../../reference/hallucination-records-2026-11-22.md)
(the three new models). It is worth reading before trusting a "0%": it is where you
can see that GLM-4.7-Flash called `matlab zerosx` real at confidence 1.00, and that
every other miss in either run is the safe direction — a real API called fake.

The full cross-task view, including images and video, is
[`../reference/COMPARISON.md`](../reference/COMPARISON.md). The per-model licence
reading is [`../reference/MODELS.md`](../reference/MODELS.md), and the settings
each model runs with are in [`../reference/PROFILES.md`](../reference/PROFILES.md).
