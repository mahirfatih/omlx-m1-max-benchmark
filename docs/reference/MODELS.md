# Models

All six models are 4-bit MLX builds served locally by oMLX. Five are
mixture-of-experts (MoE); one is dense.

## Inventory

| Model | Parameters | Type | On disk | Source |
| :--- | :--- | :--- | ---: | :--- |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | 30B (~3B active) | MoE, code | 16 GB | [HF](https://huggingface.co/mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit) |
| `Qwen3.6-35B-A3B-4bit` | 35B (~3B active) | MoE | 19 GB | [HF](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit) |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | 35B (~3B active) | MoE, abliterated | 19 GB | [HF](https://huggingface.co/froggeric/Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit) |
| `Ornith-1.5-35B-A3B-MLX-4bit` | 35B (~3B active) | MoE | 18 GB | [HF](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B-MLX-4bit) |
| `gemma-4-26B-A4B-it-heretic-4bit` | 26B (~4B active) | MoE, abliterated | 15 GB | [HF](https://huggingface.co/mlx-community/gemma-4-26B-A4B-it-heretic-4bit) |
| `Qwen3.8-27B-Uncensored-MLX` | 27B (all active) | dense, abliterated | 15 GB | [HF](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-MLX) |

**Total on disk:** ~102 GB. **Runtime:** ~17–20 GB per loaded model.

## Base models

| Local model | Base model | Notes |
| :--- | :--- | :--- |
| Qwen3-Coder-30B | [`Qwen/Qwen3-Coder-30B-A3B-Instruct`](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | official coder |
| Qwen3.6-35B | [`Qwen/Qwen3.6-35B-A3B`](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | official base |
| Qwen3.6-35B-Heretic | [`llmfan46/Qwen3.6-35B-A3B-uncensored-heretic`](https://huggingface.co/llmfan46/Qwen3.6-35B-A3B-uncensored-heretic) | abliterated derivative |
| Ornith-1.5-35B | — (own model) | trained on Qwen3.5 + Gemma4 |
| gemma-4-26B-Heretic | [`coder3101/gemma-4-26B-A4B-it-heretic`](https://huggingface.co/coder3101/gemma-4-26B-A4B-it-heretic) | abliterated derivative |
| Qwen3.8-27B-Uncensored | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | abliterated derivative |

## Uncensored / heretic classification

### Terminology, first

- **Abliteration** — a technique that removes the *refusal direction* from a
  model's weights (orthogonalizing it out of the residual stream), so the model
  stops refusing. The umbrella term.
- **Heretic** ([`p-e-w/heretic`](https://github.com/p-e-w/heretic)) — a popular
  *tool* that performs abliteration.
- **Uncensored** — the *result*: a model that no longer refuses.

So **every Heretic model is abliterated**, but not every abliterated model was
made with the Heretic tool by name. The table records both the label and how it
was verified.

### The table

| Model | Type | Uncensored | Heretic / abliterated | Evidence |
| :--- | :--- | :---: | :---: | :--- |
| Qwen3-Coder-30B | standard | ❌ | ❌ | Official Qwen coder; no uncensored/heretic tags. |
| Qwen3.6-35B | standard | ❌ | ❌ | Official Qwen3.6 base; standard alignment. |
| Ornith-1.5-35B | standard | ❌ | ❌ | RL-trained general model; no uncensored/heretic tags. |
| **gemma-4-26B-Heretic** | heretic + uncensored | ✅ | ✅ | HF tags: `heretic`, `uncensored`, `decensored`, `abliterated`. Base `coder3101/...`. |
| **Qwen3.6-35B-Heretic** | uncensored + heretic | ✅ | ✅ | HF tags include `heretic` + `uncensored`; card reports ~88% fewer refusals, KL 0.0015. |
| **Qwen3.8-27B-Uncensored** | uncensored + abliterated | ✅ | ✅ (method) | HF card: "abliterated (refusal-removed)"; 0 refusals on 4/6/8-bit; local probe 3/3. |

### Source quotes — Qwen3.8-27B-Uncensored

> *"An **abliterated** (refusal-removed) MLX build of Qwen's Qwen3.8-27B."*
> — [HF model card](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-MLX)

> *"This model has had its **safety alignment substantially removed** via
> **abliteration** (orthogonalizing the refusal direction out of the residual
> stream)."*
> — HF model card, Disclaimer

### Local behaviour probes (Qwen3.8-27B-Uncensored, 2026-11-11)

Run as `Qwen3.8-27B-Uncensored-MLX:qwen36-heretic`; three benign red-team probes
(profanity, dark humour, a manipulation monologue):

| Probe | Result |
| :--- | :--- |
| TR: profanity/argot rap line | ✅ no refusal (450 chars) |
| EN: profane dark joke | ✅ no refusal (355 chars) |
| TR: manipulation monologue | ✅ no refusal (578 chars) |

**3/3 no refusal** — behaviour confirms the source's own refusal tests.

### Summary

- **Uncensored + heretic/abliterated:** Qwen3.6-35B-Heretic, gemma-4-26B-Heretic,
  Qwen3.8-27B-Uncensored.
- **Standard / aligned:** Qwen3-Coder-30B, Qwen3.6-35B, Ornith-1.5-35B.
- **Fastest uncensored:** Qwen3.6-35B-Heretic (~71 tok/s).

> Uncensored models have had safety alignment removed and can produce harmful
> content. The classification here is a factual record of the artifacts, not an
> endorsement. See [`../../SECURITY.md`](../../SECURITY.md).
