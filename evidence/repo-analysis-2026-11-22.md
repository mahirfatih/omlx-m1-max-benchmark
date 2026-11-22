# Repository analysis — `net-traffic-control-catalog`

**Target:** [https://github.com/mahirfatih/net-traffic-control-catalog](https://github.com/mahirfatih/net-traffic-control-catalog) — catalog.json v1, 6731 hosts, 27 categories, 22 services, 232151 bytes.

**Date:** 2026-11-22. Each model was given the same digest (file tree, README, data statistics) and the same analysis task, then measured.

| Model | Profile | Answer (s) | Tokens | tok/s | Facts recovered | Score |
|---|---|---:|---:|---:|---:|---:|
| `Kimi-Linear-48B-A3B-Instruct` | `kimi-linear` | 5.7 | 262 | 45.9 | 8/12 | **67%** |
| `Kimi-Linear-48B-A3B-Instruct` | `kimi-linear-hot` | 4.4 | 269 | 60.5 | 7/12 | **58%** |
| `GLM-4.7-Flash-8bit` | `glm47` | 7.4 | 191 | 25.9 | 6/12 | **50%** |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling-mtp` | 34.9 | 700 | 20.1 | 5/12 | **42%** |
| `GLM-4.7-Flash-8bit` | `glm47-hot` | 4.9 | 145 | 29.6 | 4/12 | **33%** |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling-hot` | 27.8 | 700 | 25.2 | 0/12 | **0%** |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling-mtp-hot` | 29.6 | 700 | 23.7 | 0/12 | **0%** |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling` | 31.0 | 700 | 22.6 | 0/12 | **0%** |

_Facts recovered = how many of the repository's own documented facts (`6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain`) the answer cites. It is a recall proxy for whether the model read the digest rather than pattern-matched._

## `Kimi-Linear-48B-A3B-Instruct-4bit` · `kimi-linear`

- **Answer:** 5.7s, 262 tokens, 45.9 tok/s
- **Recovered 8/12**; missed: 6731, CC0, finance, domain

> 1. **What is this project?**  
> A community-maintained JSON catalog that maps 6,731 hostnames to 27 categories and 22 services for use by the “Net Traffic Control” app.
> 
> 2. **How is it structured?**  
> - **scripts/** (6,864 files) – automation: `catalog/`, `checks/`, `release/`, `sources/`  
> - **docs/** (39) – guides, architecture, security, testing docs  
> - **evidence/** (29) – analysis reports and coverage metrics  
> - **seeds/** (5) – static JSON seeds: `categories.json`, `services.json`, public-suffix exceptions  
> - **config/** (4) – CI/CD workflows in `.github/workflows/`; test.sh is the off

## `Kimi-Linear-48B-A3B-Instruct-4bit` · `kimi-linear-hot`

- **Answer:** 4.4s, 269 tokens, 60.5 tok/s
- **Recovered 7/12**; missed: 6731, manifest, CC0, finance, domain

> 1. **What is this project?**  
> A community-maintained JSON catalog that maps 6,731 hostnames to 27 categories and 22 services for use by the “Net Traffic Control” app.
> 
> 2. **How is it structured?**  
> - **`scripts/`** (6,864 files) – automation: `catalog/`, `checks/`, `release/` sub-folders handle generation, validation and publishing.  
> - **`docs/`** (39) – guides, reference, architecture, security docs.  
> - **`evidence/`** (29) – test data and validation reports.  
> - **`seeds/`** (5) – static JSON seeds (`categories.json`, `services.json`).  
> - **`config/`** (4) – build configuration.  
> - **R

## `GLM-4.7-Flash-8bit` · `glm47`

- **Answer:** 7.4s, 191 tokens, 25.9 tok/s
- **Recovered 6/12**; missed: 27, 22, seeds, manifest, CC0, finance

> 1. **What:** A curated catalog of 6,731 domains mapping hosts to categories and services for a Net Traffic Control application.
> 2. **Structure:** Data lives in `catalog.json` (hosts/services). Logic resides primarily under the massive 6,864-file `/scripts/`. Documentation is in `docs`, and tests are minimal (2 files).
> 3. **Risk:** The project relies on a single data source (`catalog.json`) which is 232KB. With **6731 hosts** and only a single `generated` date of Oct 2026, the data appears static or stale. If this file isn't updated frequently by a specific script in `/scripts/`, the catalog wi

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-mtp`

- **Answer:** 34.9s, 700 tokens, 20.1 tok/s
- **Recovered 5/12**; missed: 6731, 27, 22, CC0, test, finance, domain

> **1. What it is:** A JSON data catalog mapping host names to categories ("what a name is") and services/products ("whose it is") for the Net Traffic Control app, which loads `catalog.json` as a Category Data source.
> 
> **2. Structure:** The real data lives in `catalog.json` (232 KB, v1, generated 2026-10-20) plus `manifest.json`; seeds (`categories.json`, `services.json`, `public-suffix-exceptions.json`) drive generation; `scripts/` (analysis/, catalog/, checks/, release/, sources/) holds 6,864 files; `docs/` (39) covers overview/guides/reference/architecture/security

## `GLM-4.7-Flash-8bit` · `glm47-hot`

- **Answer:** 4.9s, 145 tokens, 29.6 tok/s
- **Recovered 4/12**; missed: 6731, 27, 22, seeds, manifest, CC0, docs, domain

> 1. **What:** A curated catalog mapping 6,731 hostnames to categories and services for a network traffic control application.
> 2. **Structure:** A data-centric repository with 6,864 scripts (likely automation), a `catalog.json` source file (`hosts`, categories/services metadata, 232KB JSON generated Oct '26), and a comprehensive documentation tree.
> 3. **Risk:** A massive data skew risk exists where the "finance" category (3570 hosts) vastly outnumbers others, potentially overwhelming downstream processing or UI rendering if not handled with pagination.
> 4. **Verdict:** Yes, it is well-maintained;

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-hot`

- **Answer:** 27.8s, 700 tokens, 25.2 tok/s
- **Recovered 0/12**; missed: 6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain

> 

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-mtp-hot`

- **Answer:** 29.6s, 700 tokens, 23.7 tok/s
- **Recovered 0/12**; missed: 6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain

> 

## `Inkling-2-Mini-oQ4e-mtp` · `inkling`

- **Answer:** 31.0s, 700 tokens, 22.6 tok/s
- **Recovered 0/12**; missed: 6731, 27, 22, catalog.json, seeds, manifest, CC0, scripts, docs, test, finance, domain

> 
