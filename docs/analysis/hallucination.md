# Hallucination — do the models invent APIs that do not exist?

Throughput says how fast a model writes. This says whether it will confidently
describe an API that was never written. Each of 102 languages is probed twice:
once with a **genuine** documented API or feature, once with a **fabricated
twin** made by perturbing the real name (`functools.reduce` → `functools.reducex`,
`{#each}` → `{#eachx}`). The model is asked to judge, per name, whether it is real,
and to state a confidence. A model that calls a fabricated name real is
**hallucinating**; a model that calls a genuine name fake raises a **false alarm**.

The corpus and the twins are in [`../../data/languages.json`](../../data/languages.json)
and described in [`../reference/LANGUAGES.md`](../reference/LANGUAGES.md). The probe
is [`../../scripts/measure/hallucination-test.py`](../../scripts/measure/hallucination-test.py).

The run: `2026-11-12`, five models, 102 languages, 204 probes each.

| Model | Answered | Accuracy | Hallucination (fake → "real") | False alarm (real → "fake") | Brier ↓ | Overconfident + wrong |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Qwen3.6-35B-A3B` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.001 | 0 |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.001 | 0 |
| `Ornith-1.5-35B-A3B` | 204/204 | 99% (202/204) | **0%** (0/102) | 2% (2/102) | 0.009 | 1 |
| `gemma-4-26B-A4B-it-heretic` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.0 | 0 |
| `Qwen3-Coder-30B-A3B-Instruct` | 182/204 | 99% (180/182) | **0%** (0/91) | 2% (2/91) | 0.006 | 0 |

_Hallucination = a fabricated API or feature the model called real. False alarm = a
genuine one it called fake. Brier = mean squared error of the stated confidence; 0
is perfect, 0.25 is a coin flip, lower is better, and it is computed only over
answers that stated a confidence._

## What the numbers mean

- **No model invented an API.** Across the five models, zero fabricated names
  were called real: 0/102, 0/102, 0/102, 0/102, 0/91. On this corpus, at these
  sizes, confident API invention is not the failure mode the models exhibit —
  recognising a plausible-but-fake name is something they do well.
- **The rare misses are false alarms, not hallucinations.** Ornith called two
  genuine APIs fake (and was confident enough about one to be "overconfident and
  wrong"); Qwen3-Coder did the same twice. That is the safe direction: a user
  who is told a real function does not exist will check the docs; a user told a
  fake function exists will call it.
- **Confidence is well calibrated.** Brier scores of 0.0–0.009 sit near the
  perfect end (a coin flip is 0.25). The models are not just right, they say so
  in proportion to how right they are.
- **The coverage column is a harness fact, not a model score.** Qwen3-Coder
  answered 182/204: it emits nearly-valid JSON and occasionally drops or mangles
  an entry. Those 22 probes are excluded rather than counted as wrong, so its
  accuracy is over the 182 it truly answered. See the Harness section below.

## The slow model we dropped

`Qwen3.8-27B-Uncensored` was the sixth model and is **not in the table**. It is
dense (27B read per token) and a heavy reasoner, and on this task it was too slow
to measure: across three attempts it spent **~5.2 hours of GPU time** on the same
102-language corpus and still did not finish. The other five models complete the
whole corpus in **1–2 minutes each**. On the last attempt it managed 8 of 13
batches in **88 minutes** before the run was stopped.

That is a real result even though it is not a score: on a long-context,
many-item judging task, this model's wall-clock cost is one to two orders of
magnitude above its peers, and a person waiting for it will wait hours. It is
recorded here rather than silently omitted. It is also the model that failed to
define requested function names twice in [`code-benchmark.md`](code-benchmark.md),
so slowness here did not buy thoroughness.

## Harness

The probe is deliberately conservative, because every choice below is a way to
turn a model's real answer into a wrong-looking zero:

- **A non-answer is never a wrong answer.** Empty content, a truncated reply
  (`finish_reason == "length"`), or a batch whose JSON cannot be read is scored as
  _unanswered_ and excluded from accuracy, not as a miss.
- **The budget escalates.** A reasoning model can spend a small budget on its
  scratchpad and return nothing but `length`; the probe retries at 2× and 4×
  before giving up, stopping early once the JSON parses or once the model has
  plainly finished answering.
- **A partial batch is asked again.** A model will answer six of sixteen names and
  stop; the names it left out are re-asked on their own and merged back.
- **A mangled object is salvaged.** Some models write nearly-valid JSON — an
  unescaped quote inside a key, a missing closing quote — which `json.loads`
  rejects as a whole. The probe walks the raw text for the verdict shape and
  recovers what is genuinely there.
- The scorer is validated offline: `--selftest` fabricates a perfect model and a
  fully-hallucinating one and asserts the two are scored 0% and 100%.

Each of these was found by watching a model score zero on a batch it had in fact
answered, and fixed before this run.

## Reproducing

```bash
python3 scripts/measure/hallucination-test.py --selftest          # no model
python3 scripts/measure/hallucination-test.py \
    --models Qwen3.6-35B-A3B-4bit:qwen3 --batch 8
```

`--selftest` is step 13 of [`../../test/test.sh`](../../test/test.sh) and needs no
model and no network.

Raw run: [`../../evidence/hallucination-2026-11-12.md`](../../evidence/hallucination-2026-11-12.md)
and [`../../reference/hallucination.json`](../../reference/hallucination.json).
