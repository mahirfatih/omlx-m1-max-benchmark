# Profiles

oMLX keeps model settings in two layers:

- **Global profiles** (`~/.omlx/global_templates.json`) — named setting bundles.
- **Model → profile mapping** (`~/.omlx/model_settings.json`) — which profile each
  model uses, as `active_profile_name`.

The machine-readable snapshot is
[`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json). Reconcile a
live install with it using `python3 scripts/config/apply-profiles.py`.

## The global profiles

Six global templates now exist. The three original ones are identical except for
`max_tokens`; the 2026-11-22 campaign added one per new model, each a clone of the
`qwen3`/`qwen36-heretic` baseline (64K, 4-bit KV, thinking off, temp 0.2) so the new
models run under the same conditions as the originals.

| Setting | `qwen3` | `qwen36-heretic` | `gemma4-heretic` | `glm47` | `kimi-linear` | `inkling` |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `max_context_window` | 65536 | 65536 | 65536 | 65536 | 65536 | 65536 |
| `max_tokens` | **4096** | 2048 | 2048 | **4096** | **4096** | 2048 |
| `temperature` | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |
| `top_p` | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 |
| `top_k` | 20 | 20 | 20 | 20 | 20 | 20 |
| `repetition_penalty` | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 |
| `min_p` | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| `presence_penalty` | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| `enable_thinking` | false | false | false | false | false | false |
| `turboquant_kv_enabled` | true | true | true | true | true | true |
| `turboquant_kv_bits` | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| `turboquant_skip_last` | true | true | true | true | true | true |
| `force_sampling` | false | false | false | false | false | false |
| `guided_grammar_enabled` | false | false | false | false | false | false |
| `specprefill_enabled` | false | false | false | false | false | false |
| `mtp_enabled` | false | false | false | false | false | false |
| `dflash_enabled` | false | false | false | false | false | false |

The code-oriented profiles (`qwen3`, `glm47`, `kimi-linear`) use `max_tokens 4096`;
the rest use 2048.

### Sampling-variant and MTP profiles (exposed, per model)

Beyond the global templates, each new model has **requestable per-model profiles**
that oMLX exposes as `Model:api_name`, so two sampling regimes can be compared on the
same machine. They are not global templates — they live only on their own model.

| Model | Profile | Sampling | Notes |
| :--- | :--- | :--- | :--- |
| `GLM-4.7-Flash-8bit` | `glm47` / `glm47-hot` | temp 0.2 / **1.0** | 1.0 is the model card's default |
| `Kimi-Linear-48B-A3B-Instruct-4bit` | `kimi-linear` / `kimi-linear-hot` | temp 0.2 / **1.0** | |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling` / `inkling-hot` | temp 0.2 / **1.0** | MTP off |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling-mtp` / `inkling-mtp-hot` | temp 0.2 / **1.0** | **Lightning MTP on** (bundled DSpark draft) |

## Model → profile

| Model | Profile |
| :--- | :--- |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | `qwen3` |
| `Ornith-1.5-35B-A3B-MLX-4bit` | `qwen3` |
| `Qwen3.6-35B-A3B-4bit` | `qwen3` |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | `qwen36-heretic` |
| `Qwen3.8-27B-Uncensored-MLX` | `qwen36-heretic` |
| `gemma-4-26B-A4B-it-heretic-4bit` | `gemma4-heretic` |
| `GLM-4.7-Flash-8bit` | `glm47` |
| `Kimi-Linear-48B-A3B-Instruct-4bit` | `kimi-linear` |
| `Inkling-2-Mini-oQ4e-mtp` | `inkling` |

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

- **64K context + 4-bit KV cache.** The KV cache is the thing that grows with
  context. Quantizing it to 4-bit (turboquant) keeps the runtime footprint around
  ~17–34 GB per model (the 8-bit GLM is the top of that range), which is what lets
  the memory guard accept a load on a
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

## Long prompts — Context Shrink

64K context is a deliberate speed/memory trade-off, so a long session can still
end with the server refusing the request:

```text
Prompt is too long: 39514 tokens > 32768 maximum context length
```

Raising `max_context_window` moves that wall but does not remove it, and it costs
prefill time and KV cache. If you would rather keep 64K, use
[Context Shrink](https://github.com/mahirfatih/context-shrink-mcp),
an MCP server that measures the context before the request and either drops the
oldest messages or compacts them into a summary when the estimate crosses the
limit:

| Tool | What it does |
| :--- | :--- |
| `estimate_context` | Approximate token count, remaining budget and `should_trim` |
| `trim_context` | Returns the message list with the oldest messages dropped |
| `compact_context` | Returns the list with the oldest messages replaced by a summary |

`compact_context` summarises with the local model through the OpenAI-compatible
endpoint, accepts a summary the caller wrote (no model call), or returns the
`summary_prompt` for the caller to run it in two steps.

It is plain Python and runs with the system `python3`
(`pip install mcp`), so it works beside `omlx-server` on the same Mac. Two
numbers must line up with this repository's profile, or the guard and the server
disagree:

- **Context Shrink's own window.** Its built-in default is `32768`; pin it to
  this profile with `--max-context 65536` (or
  `CONTEXT_SHRINK_MAX_CONTEXT_TOKENS=65536`). `keep_last` defaults to `8`.
- **OpenCode's window.** OpenCode plans its auto-compaction from the provider's
  `limit.context`, so the oMLX provider entry must also carry
  `"limit": { "context": 65536, "output": 4096 }` — equal to
  `max_context_window`, with `output` no larger than the profile's `max_tokens`.

The full OpenCode configuration (provider and MCP entries side by side) is in
[Context Shrink's README](https://github.com/mahirfatih/context-shrink-mcp#a-real-setup-this-projects-development-machine).

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

## Image and video — a separate repository

**oMLX serves text and nothing else.** It has no profile for an image or a video
model, because it cannot run one — images go through
[mflux](https://github.com/filipstrand/mflux) and video through
[VideoX-Fun-mlx](https://github.com/dgrauet/VideoX-Fun-mlx). Keeping them out of
`profiles/omlx-profiles.json` is deliberate: `apply-profiles.py` writes the oMLX
snapshot to `~/.omlx/`, and an image or video entry there would be applied to a
server that cannot run it.

Those layers have their own profile files, their own harnesses and their own
documentation, all in:

### → [**mahirfatih/local-generation-benchmark-m1-max**](https://github.com/mahirfatih/local-generation-benchmark-m1-max)

| Layer | Profile file (there) | What it sets |
| :--- | :--- | :--- |
| Image (mflux) | `profiles/mflux-profiles.json` | `klein-q8` (4 steps), `flux3-klein-q8` (16 steps) |
| Video (VideoX-Fun-mlx, mlx-gen) | `profiles/video-profiles.json` | `cogvideox-fun-1.5-5b-inp-q8`, `wan22-ti2v-5b-q8` |

Both links above are relative to that repository, not to this one — no image or
video profile file exists here.

## Running these yourself

The tables above describe the settings; these are the commands. oMLX runs on one
GPU, and so do the image and video tools — **never run two GPU jobs at once**,
text included. The image and video harnesses check this themselves (they refuse
to start next to another job), but if you are typing by hand, that is on you.

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

### Image and video — mflux and VideoX-Fun-mlx

The commands for the two generation layers are in
[the generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max),
beside their profiles: `mflux-generate-flux2` and `mflux-generate-flux3` for
images, `mlxgen generate` and `quick_infer.py` for video, each with the settings
that produced the committed outputs.
