# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
date-based snapshots rather than semver releases.

## [Unreleased]

### Added — coding benchmark

- `problems/` — algorithmic problems with executable hidden cases and reference
  solutions (`p01-two-sum`, `p02-longest-increasing-subsequence`,
  `p03-median-two-sorted`, `p04-merge-intervals`, `p05-word-break`).
- `scripts/measure/code-benchmark.py` — asks each model for a Python solution,
  runs it against the cases under a timeout, and scores correctness. `--selftest`
  runs the reference solutions with no model.
- `scripts/measure/merge-code-benchmark.py` — merge a re-run over an earlier run.
- The idea of a problem catalogue with executable cases follows
  [`liohunter1/llm-coding-benchmark`](https://github.com/liohunter1/llm-coding-benchmark)
  (which ships no licence file); the problems, cases and solutions here are
  original to this repository.
- `docs/analysis/code-benchmark.md`, `reference/code-benchmark.json`,
  `evidence/code-benchmark-2026-11-11.md` — the reading and the raw run.

### Added — hallucination & format & memory probes

- `data/languages.json` — a curated corpus of **102 languages** (compiled,
  interpreted, markup, template, data, HDL, blockchain, docs, diagram), each with
  one genuine, well-known API/feature. Tabulated in
  [`docs/reference/LANGUAGES.md`](docs/reference/LANGUAGES.md).
- `scripts/measure/hallucination-test.py` — asks each model whether a genuine API
  and a fabricated twin (the genuine name with `x` appended) are real, and
  reports the **hallucination rate** (fake called real), the **false-alarm rate**
  (real called fake) and a **Brier** score for the stated confidence. `--selftest`
  is offline.
- `scripts/measure/grammar-test.py` — format/grammar adherence: does the answer
  parse as a schema-valid JSON value? Standard-library validator; offline
  `--selftest`.
- `scripts/measure/context-memory-test.py` — long-context memory: retrieval,
  conflict resolution and aggregation over a generated ~6k-token document.
  Offline `--selftest`.
- `docs/analysis/hallucination.md`, `docs/analysis/external-benchmarks.md`, and
  the raw runs under `evidence/` and `reference/`.
- The external projects consulted (and why most were cited rather than copied)
  are recorded in [`docs/analysis/external-benchmarks.md`](docs/analysis/external-benchmarks.md):
  [`liohunter1`](https://github.com/liohunter1/llm-coding-benchmark),
  [`akitaonrails`](https://github.com/akitaonrails/llm-coding-benchmark),
  [`egavrin/deal-llm-grammar-benchmark`](https://github.com/egavrin/deal-llm-grammar-benchmark),
  [`HUST-AI-HYZ/MemoryAgentBench`](https://github.com/HUST-AI-HYZ/MemoryAgentBench),
  [`openai/frontier-evals`](https://github.com/openai/frontier-evals),
  [`wgwang/awesome-LLM-benchmarks`](https://github.com/wgwang/awesome-LLM-benchmarks),
  [`tongye98/Awesome-Code-Benchmark`](https://github.com/tongye98/Awesome-Code-Benchmark),
  [`ooples/token-optimizer-mcp`](https://github.com/ooples/token-optimizer-mcp).

### Added — local image layer & model licences

- `profiles/mflux-profiles.json` — two local image-generation profiles, kept
  separate from the oMLX profiles because they run under a different tool:
  - `klein-q8` — FLUX.2 klein 4B, MLX 8-bit, 4-step distilled, Apache-2.0.
  - `flux3-klein-q8` — FLUX 3 Image Klein, 16-step distilled, FLUX Kommunity
    License (conditional).
  Both use `--compute-precision float16`, the Apple M1-family speed flag.
- `scripts/measure/image-benchmark.py` — one `mflux` process per prompt, timed
  end to end, the written PNG verified; refuses to run while another GPU job is
  active. `--selftest` is offline.
- `data/image-prompts.json` — eight original prompts across the categories that
  separate image models (photorealism, hands, legible text, composition, style).
- `docs/reference/LICENSES.md` — what each model's own card says. **Download is
  not a licence:** `Ornith-1.5` declares none, the gemma variant is tagged
  Apache-2.0 but links to the Gemma terms, and FLUX 3 is the conditional
  Kommunity License (commercial output use under US$5M). It also records the two
  **video** models queued for download, where the CogVideoX-Fun quant is again
  tagged `apache-2.0` but its base is under the registration-gated CogVideoX
  License. `MODELS.md` gains a Licence column; `PROFILES.md` documents both image
  profiles.
- `test/test.sh` gains offline steps for the harness and the licence reading.

### Added — local video layer

- `profiles/video-profiles.json` — a **third** runtime layer, with its own runners
  (neither oMLX nor mflux generates video):
  - `wan22-ti2v-5b-q8` — Wan2.2 TI2V-5B (mixed q8/BF16) through
    [`mlx-gen`](https://github.com/lpalbou/mlx-gen), Apache-2.0.
  - `cogvideox-fun-1.5-5b-inp-q8` — CogVideoX-Fun V1.5 5B InP (int8) through
    [`VideoX-Fun-mlx`](https://github.com/dgrauet/VideoX-Fun-mlx), under The
    CogVideoX License.
- `scripts/measure/video-benchmark.py` — one runner process per prompt, timed end
  to end, the written clip measured with **ffprobe** (size, frame count, frame
  rate, duration, codec) rather than trusted from the log. Refuses to run while
  another GPU job is active. `--selftest` is offline.
- `data/video-prompts.json` — four original motion prompts (subject motion, a
  specified camera move, a physical pour, a wide establishing shot).
- `test/test.sh` gains an offline step for the video harness.
- No results yet: both models are still downloading and their runners are not
  installed, so the profiles and the harness are committed ahead of the numbers.

### Added — repository analysis

- `scripts/measure/repo-analysis-test.py` — measures how each model analyses a
  real repository: answer time, decode speed, and how many of the repository's
  own documented facts the answer cites. Default target:
  [`mahirfatih/net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog).
- `docs/analysis/net-traffic-control-catalog.md` — the reading: fastest ≠ best,
  and the two models that invented a file count.
- `reference/repo-analysis.json`, `evidence/repo-analysis-2026-11-11.md` — the
  data and the raw run.

### Added — security layer

- `scripts/security/security-probe.py` — audits the local oMLX server: loopback bind, LAN
  exposure, `/v1` and admin authentication, unauthenticated OpenAPI/docs,
  wildcard CORS; with `--model`, prompt-injection, system-prompt-leak and
  jailbreak probes.
- `scripts/security/redteam-benchmark.py` — offensive capability benchmark: asks each
  model for an exploit path per web challenge, sends it to a local lab, scores
  the flag; plus a reverse-engineering challenge.
- `scripts/security/lab-server.py` — deliberately vulnerable local app (SQLi,
  command injection, LFI, reflected XSS), loopback only.
- `scripts/security/make-re-challenge.py` — compiles a split-secret C binary and
  emits the `strings` / disassembly material.
- `docs/security/README.md` — threat model and findings for a default local
  oMLX 0.7.3 install.
- `docs/security/OFFENSIVE-BENCHMARK.md` — red-team methodology and scorecard.

### Added — documentation

- `docs/` tree: overview, guides, reference, architecture, diagrams, testing,
  security.
- `docs/guides/METHODOLOGY.md`, `REPRODUCING.md`, `CHOOSING-A-MODEL.md`.
- `docs/reference/MODELS.md`, `PROFILES.md`, `RESULTS.md`.
- `README.tr.md` — Turkish overview.

### Added — tooling

- `scripts/measure/collect-system-info.py`, `model-sizes.py`, `check-health.py`,
  `apply-profiles.py`.
- `scripts/README.md` — the script reference.
- `scripts/lint.sh` — the single entry point for every linter (ruff, shellcheck,
  actionlint, yamllint, markdownlint-cli2), plus `pyproject.toml` (ruff) and the
  `.markdownlint-cli2.jsonc` / `.yamllint` / `.editorconfig` configs. Ruff lints
  the harness itself; the CI `lint` job calls the same script.
- `.github/workflows/ci.yml`, `.github/CODEOWNERS`.
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`.

## [2026-11-11] — initial public release

### Added

- Throughput benchmark of six local LLMs under oMLX 0.7.3 on an Apple M1 Max
  (64 GB): decode speed in EN and TR, two reps each.
- `benchmarks/2026-11-11-m1max.md` — the raw report, including the 4-language
  code-validation matrix.
- `profiles/omlx-profiles.json` — sanitized oMLX global profiles and the model →
  profile mapping.
- `config/settings.example.json` — example global settings with a placeholder
  key.
- `scripts/measure/benchmark.py`, `scripts/measure/code-matrix-test.py`.
- Uncensored / heretic / abliterated classification with HuggingFace evidence.
- `README.md` — overview, tables, Mermaid charts, reproduction steps.
- MIT licence.
