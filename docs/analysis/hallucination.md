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

The run: `2026-11-12`, five models, 102 languages, 204 probes each. A second run
on `2026-11-22` added the three newer models (GLM-4.7-Flash, Kimi-Linear-48B,
Inkling-2-Mini), each under both `temp 0.2` and `temp 1.0` — eight profiles in
all, reported below the first table.

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

## The 2026-11-22 campaign

Three more models, each under `temp 0.2` and `temp 1.0` (eight profiles). Same
102-language corpus and the same probe.

| Model (profile) | Answered | Accuracy | Hallucination | False alarm | Brier ↓ |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `Kimi-Linear-48B` (`kimi-linear`) | 204/204 | 100% (203/204) | **0%** (0/102) | 1% (1/102) | 0.005 |
| `Kimi-Linear-48B` (`kimi-linear-hot`) | 204/204 | 100% (203/204) | **0%** (0/102) | 1% (1/102) | 0.005 |
| `Inkling-2-Mini` (`inkling`) | 188/204 | 100% (188/188) | **0%** (0/94) | 0% (0/94) | 0.004 |
| `Inkling-2-Mini` (`inkling-hot`) | 188/204 | 100% (188/188) | **0%** (0/94) | 0% (0/94) | 0.004 |
| `Inkling-2-Mini` (`inkling-mtp`) | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.005 |
| `Inkling-2-Mini` (`inkling-mtp-hot`) | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.007 |
| `GLM-4.7-Flash` (`glm47`) | 165/204 | 98% (161/165) | **2%** (2/85) | 2% (2/80) | 0.11 |
| `GLM-4.7-Flash` (`glm47-hot`) | 165/204 | 98% (161/165) | **2%** (2/85) | 2% (2/80) | 0.11 |

- **GLM-4.7-Flash is the first model here to invent an API.** It called the
  fabricated twins `matlab zerosx` (at confidence **1.00**) and Objective-C
  `NSArrayx` real — the same two names, in both temperature runs. That is a
  reproducible weak spot, not sampling noise: `zeros` and `NSArray` are so
  familiar that the one-letter perturbation still reads as real to it. It also
  has the worst Brier here (0.11, ~20× the others) and three "overconfident and
  wrong" probes.
- **Kimi-Linear and Inkling-2-Mini kept the older models' record: zero
  hallucinations.** Kimi raised one false alarm (Pascal `writeln`, called fake)
  and Inkling none. Both are the safe direction.
- **Temperature changes nothing.** Every model's two runs score identically
  (GLM 2%/2% twice, Kimi 0%/1% twice); the only difference is Inkling's Brier
  (0.004 vs 0.007) and answer coverage.
- **Coverage is a harness fact, not a score.** GLM answered 165/204 — it drops
  entries from otherwise-valid JSON. Two of Inkling's profiles answered 188/204
  (the thinking block runs past the output budget); its two MTP profiles answered
  all 204. Unanswered probes are excluded, never counted as misses.

Full per-probe record:
[`../../reference/hallucination-records-2026-11-22.md`](../../reference/hallucination-records-2026-11-22.md).

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

Raw runs: [`../../evidence/hallucination-2026-11-12.md`](../../evidence/hallucination-2026-11-12.md)
with [`../../reference/hallucination.json`](../../reference/hallucination.json), and
[`../../evidence/hallucination-2026-11-22.md`](../../evidence/hallucination-2026-11-22.md)
with [`../../reference/hallucination-2026-11-22.json`](../../reference/hallucination-2026-11-22.json).

## The questions and the answers themselves

The summary above says "0% hallucination"; it does not let you check. Every probe
for every model is written out — the language, the API name, whether it was real,
what the model said, and the confidence it stated — in
[`../../reference/hallucination-records.md`](../../reference/hallucination-records.md)
(the 2026-11-12 run, 1,067 lines) and
[`../../reference/hallucination-records-2026-11-22.md`](../../reference/hallucination-records-2026-11-22.md)
(the three new models), both regenerated from the JSON by
[`../../scripts/release/export-hallucination-records.py`](../../scripts/release/export-hallucination-records.py).

Two things in the first record are worth reading before trusting its headline:

- **Every miss in the 2026-11-12 run is a false alarm, not a hallucination.** No
  model of the original five called a fabricated name real on any of the 102
  languages. The two models below 0% on the false-alarm column called a _real_ API
  fake instead — the safe direction.
- **The same two names account for every miss.** `Ornith-1.5-35B` and
  `Qwen3-Coder-30B` each missed exactly `qsharp Qubit` and `mint component`, and
  nothing else. Two unrelated models failing on precisely the same pair is a
  statement about those two probes, not about either model.

The campaign record is where that changed: it shows the two fabricated names
GLM-4.7-Flash accepted (`matlab zerosx` at 1.00, `NSArrayx`) and the single false
alarm Kimi-Linear raised (`pascal writeln`).
