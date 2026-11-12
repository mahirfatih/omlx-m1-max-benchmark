# Profiles

oMLX keeps model settings in two layers:

- **Global profiles** (`~/.omlx/global_templates.json`) — named setting bundles.
- **Model → profile mapping** (`~/.omlx/model_settings.json`) — which profile each
  model uses, as `active_profile_name`.

The machine-readable snapshot is
[`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json). Reconcile a
live install with it using `python3 scripts/config/apply-profiles.py`.

## The three profiles

| Setting | `qwen3` | `qwen36-heretic` | `gemma4-heretic` |
| :--- | ---: | ---: | ---: |
| `max_context_window` | 32768 | 32768 | 32768 |
| `max_tokens` | **4096** | 2048 | 2048 |
| `temperature` | 0.2 | 0.2 | 0.2 |
| `top_p` | 0.95 | 0.95 | 0.95 |
| `top_k` | 20 | 20 | 20 |
| `repetition_penalty` | 1.1 | 1.1 | 1.1 |
| `min_p` | 0.05 | 0.05 | 0.05 |
| `presence_penalty` | 0.3 | 0.3 | 0.3 |
| `enable_thinking` | false | false | false |
| `turboquant_kv_enabled` | true | true | true |
| `turboquant_kv_bits` | 4.0 | 4.0 | 4.0 |
| `turboquant_skip_last` | true | true | true |
| `force_sampling` | false | false | false |
| `guided_grammar_enabled` | false | false | false |
| `specprefill_enabled` | false | false | false |
| `mtp_enabled` | false | false | false |
| `dflash_enabled` | false | false | false |

The only difference between `qwen3` and the heretic profiles is `max_tokens`
(4096 vs 2048). The heretic profiles are identical to each other.

## Model → profile

| Model | Profile |
| :--- | :--- |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | `qwen3` |
| `Ornith-1.5-35B-A3B-MLX-4bit` | `qwen3` |
| `Qwen3.6-35B-A3B-4bit` | `qwen3` |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | `qwen36-heretic` |
| `Qwen3.8-27B-Uncensored-MLX` | `qwen36-heretic` |
| `gemma-4-26B-A4B-it-heretic-4bit` | `gemma4-heretic` |

## Global settings (not per-profile)

| Setting | Value | Where |
| :--- | :--- | :--- |
| Host / port | `127.0.0.1:8000` | `settings.json` → `server` |
| Idle unload | 180 s | `settings.json` → `idle_timeout` |
| Memory guard | enabled, tier `aggressive`, soft 0.85, hard 0.95 | `settings.json` → `memory` |
| Model residency | lazy, `is_pinned = false` for all models | `model_settings.json` |
| Max concurrent requests | 1 | `scheduler` |

A sanitized example of the global settings is in
[`config/settings.example.json`](../../config/settings.example.json). **API keys
are never included**; the example uses the placeholder `REPLACE_WITH_YOUR_KEY`.

## Why these settings

- **32K context + 4-bit KV cache.** The KV cache is the thing that grows with
  context. Quantizing it to 4-bit (turboquant) keeps the runtime footprint at
  ~17–20 GB per model, which is what lets the memory guard accept a load on a
  64 GB machine instead of rejecting it.
- **`is_pinned = false` everywhere.** Pinning would load models at startup and
  spike RAM before any request arrives. Lazy loading plus a 180 s idle unload
  means the common case — one model in use — costs one model's memory.
- **`temperature 0.2`, `presence_penalty 0.3`, `repetition_penalty 1.1`.** Low
  temperature for stable code, mild repetition pressure against loops, and a
  small presence penalty against verbatim reuse.
- **Thinking off.** Reasoning-token overhead is off by default here for
  predictable latency; enable it per-request if a task needs it.
- **`max_tokens 4096` on `qwen3`.** Coding tasks emit whole files; chat does not,
  so the heretic profiles stay at 2048.

## Changing a profile

Either edit it in the oMLX dashboard, or change
[`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json) and run:

```bash
python3 scripts/config/apply-profiles.py --apply
~/.omlx/bin/omlx stop; sleep 4; ~/.omlx/bin/omlx start
```

`--apply` backs up each live file first (`<file>.bak-<timestamp>`). Run without
`--apply` for a dry-run diff, or with `--check` to exit non-zero when the live
configuration has drifted from the snapshot.

## Image generation — a separate layer (mflux)

The profiles above configure **oMLX**, which serves the text LLMs. The image
model is **not** served by oMLX and has no oMLX profile: it is run by
[`mflux`](https://github.com/filipstrand/mflux), a native-MLX diffusion tool, so
its settings live in a separate file,
[`profiles/mflux-profiles.json`](../../profiles/mflux-profiles.json). Keeping
them apart matters — `apply-profiles.py` writes the oMLX snapshot to
`~/.omlx/`, and an image entry there would be applied to a server that cannot
run it.

| Setting | `klein-q8` | `flux3-klein-q8` |
| :--- | ---: | ---: |
| Model | `mflux-community/flux2-klein-4b-mflux-q8` | `mflux-community/flux-3-image-klein-base-mflux-q8` |
| Base model | `black-forest-labs/FLUX.2-klein-4B` | `black-forest-labs/flux-3-image-klein-base` |
| CLI | `mflux-generate-flux2` | `mflux-generate-flux3` |
| Quantization | MLX affine, 8-bit | MLX affine, 8-bit (modified) |
| Width × height | 1024 × 1024 | 1024 × 1024 |
| Steps | 4 | 16 |
| Guidance scale | 1.0 | — (none; distilled) |
| Seed | 42 | 42 |
| Compute precision | `float16` | `float16` |
| Licence | Apache-2.0 | **FLUX Kommunity License** |

**`klein-q8`** — the quantization is 8-bit MLX affine across the text encoder,
transformer and VAE, stored in the weights (no `--quantize` flag). The 4 steps and
guidance 1.0 are the distilled-sampling values from the [FLUX.2 \[klein\] model
card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B); width, height
and seed are fixed so a run is reproducible. It inherits Apache-2.0 from the base
model.

**`flux3-klein-q8`** — FLUX 3 Image Klein is a 5.6B transformer with a Qwen3-VL-4B
text encoder; the distilled checkpoint runs **16 steps with no guidance**, and
`--guidance` is ignored on it. The uploader modified the MLX build: the transformer
is 8-bit and the **text encoder is truncated to layers 0–31** and quantized to
8-bit — worth remembering when reading a quality difference. Its licence is the
[FLUX Kommunity License v1.0](https://huggingface.co/black-forest-labs/flux-3-image-klein-base/blob/main/LICENSE.md),
**not** Apache-2.0; the output rules (including the US$5M revenue line) are in
[`LICENSES.md`](LICENSES.md).

Both run **float16 compute** (`--compute-precision float16`): the Apple M1 family has
no native bfloat16, and MLX's matmul and attention kernels are fastest in float16
there. mflux measured FLUX.2 klein 4B (q4) at 6.8 → 5.0 s/step (−22%) with the flag.
It changes the image slightly for a given seed, so the run records it.

## Video profiles

Video is a **third layer** with its own runners and its own file,
[`profiles/video-profiles.json`](../../profiles/video-profiles.json). Neither mflux
nor oMLX generates video: [**mlx-gen**](https://github.com/lpalbou/mlx-gen) runs
Wan2.2, and [**VideoX-Fun-mlx**](https://github.com/dgrauet/VideoX-Fun-mlx) runs
CogVideoX-Fun. Setting the three layers apart is deliberate: `apply-profiles.py`
writes only the oMLX snapshot to `~/.omlx/`, and an image or video entry there would
be applied to a server that cannot run it.

| Setting | `wan22-ti2v-5b-q8` | `cogvideox-fun-1.5-5b-inp-q8` |
| :--- | ---: | ---: |
| Model (as the runner resolves it) | `Wan-AI/Wan2.2-TI2V-5B-Diffusers` | `dgrauet/CogVideoX-Fun-V1.5-5b-InP-mlx-q8` |
| Base model | `Wan-AI/Wan2.2-TI2V-5B-Diffusers` | `alibaba-pai/CogVideoX-Fun-V1.5-5b-InP` |
| Runner | `mlxgen generate` | `python scripts/quick_infer.py` |
| Quantization | mixed q8 / BF16 | int8 (transformer block linears) |
| Width × height | 480 × 832 | 672 × 384 |
| Frames | 25 | 5 |
| fps | 16 | — (GIF) |
| Steps | 20 | 50 |
| Guidance | 5 | 6.0 |
| Seed | 42 | 42 |
| Output | `.mp4` | animated `.gif` |
| Licence | Apache-2.0 | **The CogVideoX License** |

**`wan22-ti2v-5b-q8`** — Wan2.2 TI2V-5B is a 5B MoE video model with a Wan2.2-VAE
(16×16×4 compression), supporting text- and image-to-video up to 720P@24fps. The
canvas, frame count and step count here are a **conservative baseline for a 64 GB
machine** with `--low-ram`, deliberately smaller than the uploader's validation
profile (1280×704, 17 frames, 20 steps on 128 GB, which peaked near 104 GiB). The
licence is Apache-2.0, inherited from the base model.

The model id is `Wan-AI/Wan2.2-TI2V-5B-Diffusers` and this is not cosmetic:
mlx-gen resolves a model **against its own Hugging Face cache** and does not read
the oMLX-style quantised folder at `~/models/AbstractFramework/wan2.2-ti2v-5b-diffusers-8bit`
(16.9 GB on this machine). Pointing it there fails; the download that makes the
profile runnable is `mlxgen download --model Wan-AI/Wan2.2-TI2V-5B-Diffusers`.

**`cogvideox-fun-1.5-5b-inp-q8`** — CogVideoX-Fun V1.5 5B is a diffusers-style DiT
ported to MLX; `quick_infer.py` writes an animated GIF and has its own defaults (used
here: 672×384, 5 frames, 50 steps, guidance 6.0). Its licence is **not** the
`apache-2.0` tag on the quant: the base model is under **The CogVideoX License**
(academic free, commercial registration-gated) — see [`LICENSES.md`](LICENSES.md).
The runner *code* (VideoX-Fun-mlx) is Apache-2.0; the *weights* are not.

A real run of either profile needs its runner installed and its model downloaded;
`scripts/measure/video-benchmark.py` refuses to start while any other GPU job is
active, and reads the finished clip's size, frame count, frame rate and duration
back with **ffprobe** rather than trusting the runner's log.

## Running these yourself

The tables above describe the settings; these are the commands. Three separate
tools, one GPU — **never run two of them at once**, text, image and video
included. The harness checks this itself (`scripts/measure/video-benchmark.py`
refuses to start next to another GPU job), but if you are typing the commands by
hand, that is on you.

### Text — oMLX

Profiles are applied through oMLX, not through a flag. Point the client at
`http://127.0.0.1:8000/v1` and select the model; oMLX picks the profile from the
model → profile map above.

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer $OMLX_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"Qwen3.6-35B-A3B-4bit",
       "messages":[{"role":"user","content":"hello"}],
       "max_tokens":220,"temperature":0.2}'
```

Reconcile a live install with the committed snapshot:

```bash
python3 scripts/config/apply-profiles.py            # dry-run diff
python3 scripts/config/apply-profiles.py --check    # non-zero if drifted
python3 scripts/config/apply-profiles.py --apply    # write, with a .bak first
```

### Image — mflux

The CLI is one-shot: it loads the model, generates, writes the PNG, exits. The
first image therefore includes model load (see the `s/img` note in the image
evidence). Output size is whatever `--height`/`--width` say.

```bash
# klein-q8 — the 22.5 s/image profile. Steps and guidance come from the model card.
mflux-generate-flux2 \
  --model mflux-community/flux2-klein-4b-mflux-q8 \
  --base-model flux2-klein-4b \
  --prompt "Photorealistic rainy-night street market in Istanbul, wet cobblestones" \
  --width 1024 --height 1024 --steps 4 --guidance 1.0 --seed 42 \
  --compute-precision float16 \
  --output market.png
```

```bash
# flux3-klein-q8 — the 180.4 s/image profile. Distilled: 16 steps, no guidance.
mflux-generate-flux3 \
  --model mflux-community/flux-3-image-klein-base-mflux-q8 \
  --base-model flux3-klein-base \
  --prompt "Minimalist swiss-style poster with the exact headline \"LOCAL FIRST\"" \
  --width 1024 --height 1024 --steps 16 --seed 42 \
  --compute-precision float16 \
  --output poster.png
```

`--guidance` is ignored on the FLUX 3 distilled checkpoint — passing it does
nothing rather than erroring, which is worth knowing before you tune it.

To run the whole eight-prompt suite instead of one prompt:

```bash
python3 scripts/measure/image-benchmark.py --profile klein-q8 --out-dir ~/Desktop/out
```

### Video — mlx-gen and VideoX-Fun-mlx

```bash
# wan22-ti2v-5b-q8 — the venv is not on PATH by default.
export PATH="$HOME/Sites/.mlxgen-venv/bin:$PATH"
mlxgen download --model Wan-AI/Wan2.2-TI2V-5B-Diffusers   # once
mlxgen generate \
  --model Wan-AI/Wan2.2-TI2V-5B-Diffusers \
  --prompt "a cup of coffee steaming on a windowsill, morning light" \
  --width 480 --height 832 --frames 25 --fps 16 \
  --steps 20 --guidance 5 --seed 42 \
  --low-ram --output clip.mp4
```

```bash
# cogvideox-fun-1.5-5b-inp-q8 — the runner writes a GIF, not an mp4.
python3 ~/Sites/VideoX-Fun-mlx/scripts/quick_infer.py \
  --model-path ~/Sites/VideoX-Fun-mlx/models/cogvideox-fun-q8 \
  --prompt "a cup of coffee steaming on a windowsill, morning light" \
  --width 672 --height 384 --frames 5 --steps 50 \
  --guidance-scale 6.0 --seed 42 \
  --output clip.gif
```

Two traps, both already hit here:

- `quick_infer.py`'s `--model-path` defaults to the uploader's own machine
  (`/Users/dgrauet/Work/...`). Always pass your own downloaded path.
- The CogVideoX weights download **very unevenly**. `huggingface_hub` with
  `HF_HUB_ENABLE_HF_TRANSFER=1` measured **0.40 MB/s** for this repo and stalled;
  plain `curl -C -` against the resolve endpoint measured **7.7 MB/s**, 19× faster,
  and resumed cleanly. If a large video download looks stuck, switch to curl.
