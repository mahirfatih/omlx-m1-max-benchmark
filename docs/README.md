# docs

A map of the documents in this repository. The top-level
[`README.md`](../README.md) is the quick tour; start here when you want the
detail behind a number, a rule or a decision. Each folder answers one question —
read the one that matches what you are doing.

## How the folders are organised

| Folder | The question it answers | Written or generated |
| :--- | :--- | :--- |
| [`overview/`](overview) | What was measured, on what machine | written |
| [`guides/`](guides) | How do I reproduce or extend it | written |
| [`reference/`](reference) | What is in the repository right now | written (from measured data) |
| [`analysis/`](analysis) | What do the results mean | written |
| [`architecture/`](architecture) | The diagram's input outline | the source of a generated pair |
| [`diagrams/`](diagrams) | The interactive diagram and its companion | **generated** |
| [`security/`](security) | Is the server and are the models safe | written (from probe output) |
| [`release/`](release) | How a snapshot ships | written |
| [`testing/`](testing) | How do I verify the scripts | written |

There is no build system. Every number in this repository comes from one of the
scripts in [`../scripts/`](../scripts), run on the machine in
[`overview/`](overview/README.md). The scripts are the source of truth; the
documents explain what they measured.

## Overview — what was measured

- [`overview/README.md`](overview/README.md) — the benchmark in one page: machine, method, headline result.
- [`overview/BACKGROUND.md`](overview/BACKGROUND.md) — what oMLX is, and why the measurements look the way they do.

## Guides — how do I work on it

- [`guides/METHODOLOGY.md`](guides/METHODOLOGY.md) — exactly what was measured, how, and what the numbers mean.
- [`guides/REPRODUCING.md`](guides/REPRODUCING.md) — from a clean Mac to a fresh report, step by step.
- [`guides/CHOOSING-A-MODEL.md`](guides/CHOOSING-A-MODEL.md) — which of the six models fits which job.
- [`guides/NAMING.md`](guides/NAMING.md) — the file-name rule and the conventions inside a file.

## Analysis — what the numbers mean

- [`analysis/README.md`](analysis/README.md) — why the ranking looks the way it does, and what is not measured.
- [`analysis/redteam.md`](analysis/redteam.md) — the offensive-capability reading: web exploitation vs reverse engineering.
- [`analysis/net-traffic-control-catalog.md`](analysis/net-traffic-control-catalog.md) — the models on a real repository: answer time, decode speed, and how much of it they recover.
- [`analysis/code-benchmark.md`](analysis/code-benchmark.md) — the models' code, executed: which pass hidden cases and where they fail.
- [`analysis/hallucination.md`](analysis/hallucination.md) — 102 languages × 2 probes (a real API and a fabricated twin): whether the models invent APIs, and the slow model that was dropped.
- [`analysis/external-benchmarks.md`](analysis/external-benchmarks.md) — the outside projects we looked at, their licences, and what we took.

## Reference — what is in it right now

- [`reference/MODELS.md`](reference/MODELS.md) — all six models, sizes, sources, and the uncensored/heretic classification.
- [`reference/PROFILES.md`](reference/PROFILES.md) — every oMLX profile and setting, with the reasoning, plus the separate `mflux` image profiles and the `mlx-gen` / `VideoX-Fun-mlx` video profiles.
- [`reference/RESULTS.md`](reference/RESULTS.md) — the measured throughput table, charts, and the raw report location.
- [`reference/LANGUAGES.md`](reference/LANGUAGES.md) — the 102-language corpus probed by the hallucination test.
- [`reference/LICENSES.md`](reference/LICENSES.md) — what each model's own card says: which are Apache-2.0, which is conditional, and which declares no licence at all.

## Security — is the server and are the models safe

- [`security/README.md`](security/README.md) — the server posture and the model-resistance findings.
- [`security/OFFENSIVE-BENCHMARK.md`](security/OFFENSIVE-BENCHMARK.md) — the red-team scorecard and which model is good at what.
- [`security/audit.md`](security/audit.md) — the project audit: what is open, what is closed, what is next.

## Release — how a snapshot ships

- [`release/README.md`](release/README.md) — the dated-snapshot contract and the manifest.

## Architecture — the diagram's input

- [`architecture/README.md`](architecture/README.md) — what the architecture diagram shows.
- [`architecture/source.json`](architecture/source.json) — the outline the diagram is built from.

## Diagrams — the generated pair

- [`diagrams/architecture/architecture.html`](diagrams/architecture/architecture.html) — the interactive, click-through diagram.
- [`diagrams/architecture/architecture.md`](diagrams/architecture/architecture.md) — the written companion.
- [`diagrams/README.md`](diagrams/README.md) — how the pair is generated.

## Testing — how do I verify it

- [`testing/README.md`](testing/README.md) — what runs without a model and without the network.

## Which one do I want?

| You are asking... | Read |
| :--- | :--- |
| "what machine, and what did it measure?" | [`overview/README.md`](overview/README.md) |
| "what is oMLX?" | [`overview/BACKGROUND.md`](overview/BACKGROUND.md) |
| "what exactly is a tok/s number here?" | [`guides/METHODOLOGY.md`](guides/METHODOLOGY.md) |
| "how do I run this myself?" | [`guides/REPRODUCING.md`](guides/REPRODUCING.md) |
| "which model should I use?" | [`guides/CHOOSING-A-MODEL.md`](guides/CHOOSING-A-MODEL.md) |
| "which models are uncensored or heretic?" | [`reference/MODELS.md`](reference/MODELS.md) |
| "can I use these models commercially?" | [`reference/LICENSES.md`](reference/LICENSES.md) |
| "what are the tuned profiles?" | [`reference/PROFILES.md`](reference/PROFILES.md) |
| "what were the numbers?" | [`reference/RESULTS.md`](reference/RESULTS.md) |
| "why is the fastest model fastest?" | [`analysis/README.md`](analysis/README.md) |
| "do the models' solutions actually pass tests?" | [`analysis/code-benchmark.md`](analysis/code-benchmark.md) |
| "do they invent APIs that do not exist?" | [`analysis/hallucination.md`](analysis/hallucination.md) |
| "can the models actually hack?" | [`security/OFFENSIVE-BENCHMARK.md`](security/OFFENSIVE-BENCHMARK.md) |
| "is the server exposed?" | [`security/README.md`](security/README.md) |
| "how does a request flow?" | [`diagrams/architecture/architecture.md`](diagrams/architecture/architecture.md) |
| "what can I check without a GPU?" | [`testing/README.md`](testing/README.md) |
| "how do I contribute?" | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) |

## Elsewhere in the repository

- [`../README.md`](../README.md) — the project overview and the quick tour.
- [`../README.tr.md`](../README.tr.md) — the same overview in Turkish.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — how to contribute a measurement.
- [`../SECURITY.md`](../SECURITY.md) — secrets policy and the model-behaviour disclaimer.
- [`../scripts/README.md`](../scripts/README.md) — the script reference: what every helper does and how to run it.
