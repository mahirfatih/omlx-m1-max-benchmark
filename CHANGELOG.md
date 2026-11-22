# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
date-based snapshots rather than semver releases.

## [Unreleased]

### Added — the 2026-11-22 model campaign (three new models, two sampling regimes)

- Profiled and measured three newly downloaded MLX models alongside the existing
  set, on **oMLX 0.8.2** with the 64K context window:
  `Kimi-Linear-48B-A3B-Instruct-4bit` (Moonshot, 48B MoE, KDA linear-attention
  hybrid, MIT), `GLM-4.7-Flash-8bit` (Z.ai reasoning MoE, MIT) and
  `Inkling-2-Mini-oQ4e-mtp` (Thinking Machines, looped multimodal MoE with a
  bundled DSpark **MTP** draft). Full inventory in
  [`reference/models.json`](reference/models.json) and
  [`docs/reference/MODELS.md`](docs/reference/MODELS.md).
- **Eight new oMLX profiles** (`glm47`, `glm47-hot`, `kimi-linear`,
  `kimi-linear-hot`, `inkling`, `inkling-hot`, `inkling-mtp`, `inkling-mtp-hot`):
  each model at `temp 0.2` and `temp 1.0`, and Inkling additionally with its MTP
  draft on and off. All are exposed as `Model:api_name` and accepted as
  `--models id:profile` by every measurement script (new flags added to
  `benchmark.py`, `code-benchmark.py`, `grammar-test.py`, `hallucination-test.py`,
  `context-memory-test.py`, `repo-analysis-test.py`, `code-matrix-test.py` and
  `apply-profiles.py`).
- **Results** (full write-up in
  [`benchmarks/2026-11-22-m1max.md`](benchmarks/2026-11-22-m1max.md)):
  - Throughput: Kimi-Linear **59.0** tok/s (fastest of the three, a 48B MoE that
    outruns its size via linear attention), GLM-4.7-Flash **34.9**, Inkling-2-Mini
    **25.4**. Temperature made no measurable speed difference; Inkling's MTP draft
    also made none.
  - Coding: Kimi-Linear **56/56** at `temp 1.0` (51/56 at 0.2), GLM-4.7-Flash
    **19/32 → 21/46** (the weakest coder here), Inkling-2-Mini **46/46** but it
    never defines `find_median`.
  - Long-context memory: Kimi-Linear and GLM **3/3**; Inkling **0/3**.
  - Repository analysis: Kimi-Linear **8/12** facts (best of the new models), GLM
    6/12, Inkling 0–5/12 (its reasoning tokens leave the answer empty).
  - Hallucination (102 languages × 2 probes): Kimi-Linear and Inkling **0%**;
    **GLM-4.7-Flash is the first model here to call a fabricated API real** —
    `matlab zerosx` (at confidence 1.00) and Objective-C `NSArrayx`, in both
    temperature runs — with a Brier of 0.11, ~20× the rest.
- **Inkling cannot disable thinking.** It always emits a reasoning block first, so
  a small `max_tokens` yields empty `content`; this affects its short-output runs
  and is documented rather than worked around.
- New machine-readable files:
  [`reference/throughput-2026-11-22.json`](reference/throughput-2026-11-22.json),
  [`code-benchmark-2026-11-22.json`](reference/code-benchmark-2026-11-22.json),
  [`grammar-2026-11-22.json`](reference/grammar-2026-11-22.json),
  [`context-memory-2026-11-22.json`](reference/context-memory-2026-11-22.json),
  [`repo-analysis-2026-11-22.json`](reference/repo-analysis-2026-11-22.json) and
  [`hallucination-2026-11-22.json`](reference/hallucination-2026-11-22.json), with
  their raw runs under [`evidence/`](evidence) and a probe-by-probe record in
  [`reference/hallucination-records-2026-11-22.md`](reference/hallucination-records-2026-11-22.md).
- **The canonical snapshot grew to ten models.** `reference/results.json` now
  carries all ten throughput rows (the three new models at their base profile) and
  a ten-entry `disk_gb`; `reference/models.json`, `reference/huggingface.json` and
  `config/sources.json` list ten; the README (EN + TR), `docs/` pages, the
  `manifest.json` model count and the model-map poster were updated to match.
  `manifest_version` is now 2: it hashes both the 2026-11-22 report (primary) and
  the byte-stable 2026-11-11 report (archive).
- The 2026-11-11 report and the 2026-11-11 security/red-team/audit findings are
  kept **byte-stable** as dated history; the campaign did not re-run the red team,
  so the three new models are shown as `pending` there rather than scored.

### Changed — version references are now oMLX 0.8.2

- The live server is on **oMLX 0.8.2**; the repository's prose, the `environment`
  block in [`reference/results.json`](reference/results.json), the profile
  snapshot and the docs now cite 0.8.2 as the current version. The 2026-11-11
  report and its evidence keep the 0.7.3 they were measured on, so the history
  still says what produced it.

### Changed — the oMLX context window is now 64K

- oMLX's `max_context_window` is **65536** (was 32768) in the live server
  configuration — `sampling.max_context_window` plus the per-model, named-profile
  and alias-profile entries — and this repository now documents the same value in
  `profiles/omlx-profiles.json`, `config/settings.example.json` and
  `docs/reference/PROFILES.md`.
- Why: long local coding sessions kept ending in
  `Prompt is too long: 39514 tokens > 32768 maximum context length`, and the agent
  compacted its history almost every turn. The models measured here are
  hybrid-attention (`Qwen3.6-35B-A3B` runs 30 of its 40 layers as linear
  attention), so the KV cache grows slowly — roughly 1.3 GB at 64K versus 0.7 GB at
  32K for the full-attention layers — while the native ceiling is 262144 tokens.
  Widening the window costs little memory and removes both symptoms.
- This supersedes the "keep the window narrow" advice in the entry below: the
  Context Shrink MCP is still the right tool when memory or speed must stay tight,
  it simply has headroom now.

### Added — the long-prompt answer, Context Shrink

- `README.md`, `README.tr.md` and `docs/reference/PROFILES.md` now recommend
  [Context Shrink](https://github.com/mahirfatih/context-shrink-mcp)
  for the case where a long session ends in
  `Prompt is too long: 39514 tokens > 32768 maximum context length`. Keeping the
  32K window is a deliberate speed/memory choice, so the cheaper fix is a smaller
  prompt, not a wider window: the MCP measures the context before the request and
  either **drops** the oldest messages or **compacts** them into a summary.
- Its three tools are named and described: `estimate_context`, `trim_context`
  and `compact_context`, with defaults that match this repository's `qwen3`
  profile (`max_context_tokens 32768`, `keep_last 8`).

### Changed — image and video generation moved to their own repository

- The image (mflux) and video (VideoX-Fun-mlx) layers are no longer measured or
  shipped here. **oMLX serves text and only text** — it cannot run a diffusion
  model, so an image or video profile in this repository described a server that
  cannot use it. Both layers now live in
  [mahirfatih/local-generation-benchmark-m1-max](https://github.com/mahirfatih/local-generation-benchmark-m1-max),
  with their harnesses, prompts, profiles, machine-readable results and the
  **committed outputs** (16 images, 4 clips).
- Removed from here: `scripts/measure/image-benchmark.py`,
  `scripts/measure/video-benchmark.py`, `scripts/release/export-video-evidence.py`,
  `data/image-prompts.json`, `data/video-prompts.json`,
  `profiles/mflux-profiles.json`, `profiles/video-profiles.json`, the three
  `evidence/*-benchmark-*.md` pages, `evidence/images/`, `evidence/videos/`, and
  the three `reference/*benchmark*.json` files. The full history of how they were
  built is preserved in the entries below.
- `README.md`, `docs/reference/{COMPARISON,PROFILES,MODELS,LICENSES}.md`,
  `docs/reference/README.md` and `scripts/measure/README.md` now point at the new
  repository instead of describing the layers; the image/video columns and test
  rows were dropped. `test/test.sh` no longer runs the two moved selftests, so the
  gate is now 15 steps.
- The **grammar** and **red-team** prompts were also moved out of their harnesses
  into [`data/grammar-prompts.json`](data/grammar-prompts.json) and
  [`data/redteam-prompts.json`](data/redteam-prompts.json), so every prompt set is
  now a readable file rather than code — matching the image and video prompts.

### Added — the model comparison page

- `docs/reference/COMPARISON.md` — the single page to start from: one row per
  model, one column per task (coding, chat, long context, uncensored work,
  hallucination, red-team, images, video), with every number traced to the run
  file it came from and the sample sizes stated.
- Wired into `README.md` (table of contents, the model table, and from
  `docs/reference/README.md`).
- It records what the individual pages only imply: that the model labelled
  "Coder" is not the best coder here (45/46 against four models at 56/56), that
  the uncensored tier buys nothing in the red-team suite (all five working
  models score 4/5), and that the densest model is the one to avoid on this
  machine (18.2 tok/s, and 0/3 on long context where everyone else gets 2/3).

### Added — Devstral-Small-2, the second code model

- Profiled `Devstral-Small-2-24B-Instruct-2512-8bit` (Mistral Devstral Small 2,
  24B dense, 8-bit MLX, Apache-2.0) in `profiles/omlx-profiles.json`. It is a
  **mistral3** architecture and oMLX ships `mlx_lm/models/mistral3.py`, so it
  loads; the model card documents it as multimodal, but the benchmark drives it
  text-only.
- Coding run: **55/56 cases**, all five functions defined, 13.8 s per answer. It
  loses only the empty-string edge case on `word-break` that Qwen3-Coder also
  loses, and it is the only code-labelled model here that defined every function
  it was asked for.
- `evidence/code-benchmark-devstral-2026-11-12.md`,
  `reference/code-benchmark-devstral.json`.

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
- The first full run. No model invented an API (0/102 fabricated names called real
  on every model that finished); the rare misses are false alarms, the safe
  direction. `Qwen3.8-27B-Uncensored` was dropped from the table: three attempts
  spent ~5.2 hours of GPU time without finishing the corpus the others complete in
  1–2 minutes. The harness gained four robustness fixes found during the run — a
  truncated answer escalates its budget, a partial batch is re-asked for the names
  it left out, a decorated key (`'Svelte: "{#eachx}"'`) is unwrapped, and a mangled
  JSON object is salvaged rather than scored as zero.
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
- The first real run: `klein-q8` renders a 1024×1024 image in **~22.5 s** (5.6
  s/step, 4 steps; the first image is ~28 s because the model loads). Legible
  text and hands come out clean. The saved PNGs are in `evidence/images/`. The
  `flux3-klein-q8` profile was corrected to the model actually on disk
  (`mflux-community/flux-3-image-klein-base-mflux-q8`, `--base-model
  flux3-klein-base`) — the earlier entry pointed at a repository that is not the
  one mflux downloaded.
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
