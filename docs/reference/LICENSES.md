# Model licences — download is not a licence

Every model in this benchmark runs **locally**: no account, no API key, no per-call
bill. That is a property of where it runs, not a grant of rights. The weights carry
their own terms, and **"downloadable" and "commercially usable" are not the same
thing**. This file records what each model's own card says, so a reader can tell a
truly open model from a source-available one before shipping it into something
that earns money.

This is a reading of the published terms on Hugging Face, retrieved **2026-11-12**.
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

## Image models (served by mflux)

| Model | Upstream base | Declared licence | Commercial use of outputs | Note |
| :--- | :--- | :--- | :--- | :--- |
| `mflux-community/flux2-klein-4b-mflux-q8` | `black-forest-labs/FLUX.2-klein-4B` | **Apache-2.0** | yes | Clean; no output restrictions beyond Apache-2.0's own. |
| `VisualInference/FLUX-3-Image-Klein-MLX-8bit` | `black-forest-labs/flux-3-image-klein` | **FLUX Kommunity License v1.0** | **only under US$5M revenue** | Not open source. See below. |

## Video models (queued; not yet measured)

These are being downloaded but are not in the results yet, so they are recorded
here for the licence, not the numbers. **The same tag trap appears again:** the
quantised CogVideoX-Fun repository is labelled `apache-2.0`, but the model it is
built from is not Apache-2.0 at all.

| Model | Upstream base | Declared licence | Commercial use of outputs | Note |
| :--- | :--- | :--- | :--- | :--- |
| `AbstractFramework/wan2.2-ti2v-5b-diffusers-8bit` | `Wan-AI/Wan2.2-TI2V-5B-Diffusers` | **Apache-2.0** | yes | Clean. Text- and image-to-video, 720P@24fps, 5B. |
| `dgrauet/CogVideoX-Fun-V1.5-5b-InP-mlx-q8` | `alibaba-pai/CogVideoX-Fun-V1.5-5b-InP` | **tagged `apache-2.0`, actually the CogVideoX License** | **academic free; commercial needs registration** | Do **not** trust the `apache-2.0` tag on the quant. See below. |

### The CogVideoX-Fun case

The quant card says `apache-2.0`; the base model's `LICENSE` is **The CogVideoX
License**, which is where the real terms live:

- **Academic research is free.** Commercial use requires **registering for a basic
  commercial licence** (<https://open.bigmodel.cn/mla/form>); once registered it is
  free, but the commercial service must stay **under 1 million visits per month**,
  above which a separate licence is needed.
- Generation IP belongs to the user "to the extent permitted by applicable local
  laws". Military and illegal uses are banned, with China-specific restrictions.
- It is governed by the **laws of the People's Republic of China**, disputes to the
  Haidian District People's Court in Beijing.

So, like the gemma variant, this is a case where the licence *tag* on the quant
contradicts the licence that actually applies. Follow the base model.

## The FLUX 3 case — the reason this file exists

FLUX 3 Image Klein is released under the **FLUX Kommunity License v1.0**. It is not
Apache-2.0 like FLUX.2 klein, and the difference is not cosmetic:

- **Outputs are yours.** §1.a: outputs are not "Derivatives". §2.d: *"We claim no
  ownership rights in and to the Outputs."* The image a user generates belongs to the
  user.
- **Commercial use of those outputs is capped by revenue.** §2.a grants commercial
  output use only to a *Qualifying User*: §1.e, you plus affiliates under
  **US$5M gross annualized revenue**. Above that, a paid licence is required (§2.b,
  <https://bfl.ai/licensing>).
- **Some uses are off-limits at any revenue.** §4 bans military, surveillance,
  biometric processing, rights-infringing, unlawful, CSAM and non-consensual-intimate
  uses, and §4.b forbids using the model or its outputs to improve a competing model.
- **Attribution travels with the weights.** §3 requires the Attribution Notice if the
  weights or a derivative are redistributed (not when an image is generated).

Read the full text in
[`LICENSE.md`](https://huggingface.co/black-forest-labs/flux-3-image-klein-base/blob/main/LICENSE.md).

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
- FLUX.2 klein q8: <https://huggingface.co/mflux-community/flux2-klein-4b-mflux-q8>
- FLUX 3 klein q8: <https://huggingface.co/VisualInference/FLUX-3-Image-Klein-MLX-8bit>
