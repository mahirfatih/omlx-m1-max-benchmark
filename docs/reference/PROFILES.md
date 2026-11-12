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
