# Model licences — download is not a licence

Every model in this repository runs **locally**: no account, no API key, no per-call
bill. That is a property of where it runs, not a grant of rights. The weights carry
their own terms, and **"downloadable" and "commercially usable" are not the same
thing**. This file records what each model's own card says, so a reader can tell a
truly open model from a source-available one before shipping it into something
that earns money.

This file covers the **text** models oMLX serves. The image and video models — the
FLUX and CogVideoX families — are read in the
[generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max),
and summarised at the end of this file.

This is a reading of the published terms on Hugging Face, retrieved **2026-11-22**
(the original six models on 2026-11-12; the 2026-11-22 campaign models then).
It is a summary, not legal advice; the licence text on each page is the authority.

## Text models (served by oMLX)

| Model | Upstream base | Declared licence | Commercial use of outputs | Note |
| :--- | :--- | :--- | :--- | :--- |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | `Qwen/Qwen3-Coder-30B-A3B-Instruct` | **Apache-2.0** | yes | Straight quantisation of an Apache-2.0 model. |
| `Qwen3.6-35B-A3B-4bit` | `Qwen/Qwen3.6-35B-A3B` | **Apache-2.0** | yes | Same. |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | `llmfan46/Qwen3.6-35B-A3B-uncensored-heretic` | **Apache-2.0** (declared) | yes | An **abliterated** derivative of an Apache-2.0 base. The licence is inherited, but the safety behaviour was removed by the uploader. |
| `Ornith-1.5-35B-A3B-MLX-4bit` | `ornith-ai/Ornith-1.5-35B-A3B` | **not declared** | **do not assume** | The model card names **no licence**. With no grant, the default is all rights reserved: downloaded, but not licensed for reuse or commercial use. |
| `gemma-4-26B-A4B-it-heretic-4bit` | `coder3101/gemma-4-26B-A4B-it-heretic` → `google/gemma-4` | **tagged `apache-2.0`, links to the Gemma licence** | **check before use** | The card is self-contradictory: the tag says Apache-2.0, but its `license_link` points at the **Gemma 4 licence**, which carries a use policy. The Gemma terms are the ones that matter. |
| `Qwen3.8-27B-Uncensored-MLX` | `Qwen/Qwen3.8-27B` | **Apache-2.0** | yes | Abliterated derivative; licence inherited. |
| `Devstral-Small-2-24B-Instruct-2512-8bit` | `mistralai/Devstral-Small-2-24B-Instruct-2512` | **Apache-2.0** | yes | Straight quantisation of an Apache-2.0 model. |
| `GLM-4.7-Flash-8bit` | `zai-org/GLM-4.7-Flash` | **MIT** | yes | Official Z.ai reasoning MoE; permissive. |
| `Kimi-Linear-48B-A3B-Instruct-4bit` | `moonshotai/Kimi-Linear-48B-A3B-Instruct` | **MIT** | yes | Official Moonshot instruct model; permissive. |
| `Inkling-2-Mini-oQ4e-mtp` | `thinkingmachines/Inkling-2-Mini` | **Apache-2.0** | yes | Official Thinking Machines model; the oQ quant inherits the base licence. |

## Image and video models (separate tools)

Images run under [`mflux`](https://github.com/filipstrand/mflux) (a few under
[`mlx-gen`](https://github.com/lpalbou/mlx-gen)) and video under
[`VideoX-Fun-mlx`](https://github.com/dgrauet/VideoX-Fun-mlx) — none is oMLX.
Their licences are read in full in the
[generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max),
alongside the models themselves. The one-line version:

- **FLUX.2 klein** (both quantisations and the *Base* twin) — Apache-2.0, clean.
- **Z-Image Turbo**, **ERNIE Image Turbo**, **Qwen Image** — Apache-2.0, clean.
- **Anima Turbo** — the **Circlestone non-commercial** licence: personal and
  research use only, *not* for commercial output.
- **FLUX 3 Image Klein** — the conditional **FLUX Kommunity License v1.0**, not
  Apache-2.0; commercial use of outputs is capped at **US$5M revenue**.
- **CogVideoX-Fun V1.5 5B** — the quant is tagged `apache-2.0`, but its base model
  is under **The CogVideoX License** (academic free, commercial registration-gated).
  Do not trust the tag.
- **Wan2.2 TI2V-5B** — Apache-2.0, clean.

## How to read the columns

- **Apache-2.0** means the weights may be used, modified and distributed, including
  commercially, with attribution. This is the only licence here that is unconditionally
  permissive.
- **"not declared"** is not a permissive default; it is the *absence* of a grant.
  `Ornith-1.5` is listed in the benchmark because it is measurable on this machine,
  but its card grants nothing, so it should be treated as unusable outside private
  evaluation until the author states otherwise.
- **A licence tag can contradict its own link.** The gemma variant is tagged
  `apache-2.0` yet cites the Gemma licence. When the two disagree, follow the link.
- **Abliterated / "heretic" / "uncensored" builds are modified models.** They inherit
  the base licence, but the uploader removed refusal behaviour; the consequences of
  what they generate are the user's, and upstream offers no warranty.

## This repository's own licence

The benchmark **code and documents** here are MIT (see [`../../LICENSE`](../../LICENSE)).
That covers this repository, not the models it measures: the model licences above are
the property of their authors and travel with the weights, not with this repo. Nothing
here redistributes model weights.

## Sources

- Qwen3-Coder: <https://huggingface.co/mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit>
- Qwen3.6: <https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit>
- Qwen3.6 heretic: <https://huggingface.co/froggeric/Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit>
- Ornith-1.5: <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B-MLX-4bit>
- gemma-4 heretic: <https://huggingface.co/mlx-community/gemma-4-26B-A4B-it-heretic-4bit>
  and the Gemma licence it links to: <https://ai.google.dev/gemma/docs/gemma_4_license>
- Qwen3.8: <https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-MLX>
- Devstral: <https://huggingface.co/mlx-community/Devstral-Small-2-24B-Instruct-2512-8bit>
- GLM-4.7-Flash: <https://huggingface.co/mlx-community/GLM-4.7-Flash-8bit>
- Kimi-Linear: <https://huggingface.co/mlx-community/Kimi-Linear-48B-A3B-Instruct-4bit>
- Inkling-2-Mini: <https://huggingface.co/mlx-community/Inkling-2-Mini-oQ4e-mtp>

Image and video model sources are listed in the
[generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max).
