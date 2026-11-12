# Repository analysis — `net-traffic-control-catalog`

**Target:** [https://github.com/mahirfatih/net-traffic-control-catalog](https://github.com/mahirfatih/net-traffic-control-catalog) — catalog.json v1, 6731 hosts, 27 categories, 22 services, 232151 bytes.

**Date:** 2026-11-12. Each model was given the same digest (file tree, README, data statistics) and the same analysis task, then measured.

| Model | Profile | Answer (s) | Tokens | tok/s | Facts recovered | Score |
|---|---|---:|---:|---:|---:|---:|
| `Ornith-1.5-35B-A3B` | `qwen3` | 6.8 | 366 | 53.5 | 10/12 | **83%** |
| `Qwen3-Coder-30B-A3B-Instruct` | `qwen3` | 6.6 | 235 | 35.8 | 7/12 | **58%** |
| `Qwen3.6-35B-A3B` | `qwen3` | 4.8 | 298 | 62.6 | 6/12 | **50%** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | `qwen36-heretic` | 4.7 | 269 | 57.8 | 5/12 | **42%** |
| `gemma-4-26B-A4B-it-heretic` | `gemma4-heretic` | 4.3 | 167 | 38.6 | 4/12 | **33%** |
| `Qwen3.8-27B-Uncensored-MLX` | `qwen36-heretic` | 46.1 | 700 | 15.2 | 0/12 | **0%** |

_Facts recovered = how many of the repository's own documented facts (`6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain`) the answer cites. It is a recall proxy for whether the model read the digest rather than pattern-matched._

## `Ornith-1.5-35B-A3B-MLX-4bit`

- **Answer:** 6.8s, 366 tokens, 53.5 tok/s
- **Recovered 10/12**; missed: manifest, CC0

> **1. One sentence:** A JSON catalog mapping ~6,700 hostnames to categories and services, consumed by a network-traffic-control app to group/label domains.
>
> **2. Structure:** Data lives in `catalog.json` (6,731 hosts, 27 categories, 22 services) with canonical inputs under `seeds/`; ~98% of tracked files are `scripts/` (analysis, catalog, checks, release, sources), backed by docs and an offline `test.sh` gate.
>
> **3. Data-quality risk:** Extreme category skew — _finance_ alone is 3,570 of 6,731 hosts (53%), with the top two categories (_finance_ + _government_) at 68% and the bottom ten (health,

## `Qwen3-Coder-30B-A3B-Instruct-4bit`

- **Answer:** 6.6s, 235 tokens, 35.8 tok/s
- **Recovered 7/12**; missed: 6731, manifest, CC0, test, finance

> 1. **What is this project, in one sentence?**  
> This is a catalog of domain categories and services used for traffic control on networks.
>
> 2. **How is it structured (the parts that matter)?**  
> It's structured around a `catalog.json` file containing 6,731 host entries and 22 services. Key directories include `scripts/` for automation, `docs/` for documentation and analysis, and `seeds/` with seed data files.
>
> 3. **One concrete data-quality or design risk?**  
> The catalog has only 22 services but 27 distinct categories, suggesting potential inconsistency or underutilization of service definitio

## `Qwen3.6-35B-A3B-4bit`

- **Answer:** 4.8s, 298 tokens, 62.6 tok/s
- **Recovered 6/12**; missed: 6731, 27, 22, manifest, CC0, test

> 1. **Project Definition:** This is a static JSON-based data catalog mapping network hostnames to categories and services, designed as an input source for a "Net Traffic Control" application.
>
> 2. **Structure:** The repository is heavily skewed toward automation: `scripts/` contains 6,863 files (98.4% of all tracked files), while human-readable content (`docs/`, `README.md`) and core data (`catalog.json`) constitute a tiny fraction. The architecture separates source definitions (`seeds/`), validation logic, and the final generated `catalog.json`.
>
> 3. **Data Risk:** There is a severe class imbala

## `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit`

- **Answer:** 4.7s, 269 tokens, 57.8 tok/s
- **Recovered 5/12**; missed: 6731, 27, 22, seeds, manifest, CC0, test

> 1. **Project Definition:** This is a static JSON-based data catalog mapping internet hostnames to categories and services, designed as an external source for a "Net Traffic Control" application.
>
> 2. **Structure:** The repository is heavily skewed toward automation: `scripts/` contains 6,863 files (98.4% of the tree), handling analysis and catalog generation, while `docs/` (39 files) provides reference material. The core data resides in `catalog.json`, supported by seed definitions and CI workflows.
>
> 3. **Data Risk:** There is a severe category imbalance: "finance" hosts (3,570) constitute 53%

## `gemma-4-26B-A4B-it-heretic-4bit`

- **Answer:** 4.3s, 167 tokens, 38.6 tok/s
- **Recovered 4/12**; missed: 6731, 27, 22, catalog.json, manifest, CC0, test, domain

> 1. This project is a data catalog that maps hostnames to specific categories and services for use in network traffic control applications.
>
> 2. The repository is structured as a data-generation pipeline: `seeds/` contains the base definitions, `scripts/` handles the logic for processing and generating the catalog, and `docs/` provides the necessary documentation and coverage analysis.
>
> 3. There is a significant data skew risk: the `finance` category contains 3,570 hosts (over 53% of the total 6,731 hosts), which may indicate an imbalance in data granularity or a heavy bias toward specific secto

## `Qwen3.8-27B-Uncensored-MLX`

- **Answer:** 46.1s, 700 tokens, 15.2 tok/s
- **Recovered 0/12**; missed: 6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain

>
