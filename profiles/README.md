# profiles

The oMLX profiles this benchmark runs with — the machine-readable source of the
tables in [`../docs/reference/PROFILES.md`](../docs/reference/PROFILES.md).

| File | What it is |
| :--- | :--- |
| [`omlx-profiles.json`](omlx-profiles.json) | A sanitized snapshot of the global profiles and the model → profile mapping |

**This is the text layer only.** oMLX serves text LLMs; it cannot run a diffusion
model, so there is no image or video profile here. Those two layers have their
own profile files in the
[generation repository](https://github.com/mahirfatih/local-generation-benchmark-m1-max).
An image entry in this file would be written to `~/.omlx/` and applied to a
server that cannot use it.

## Shape

Two sections, matching oMLX's own two layers:

- **`global_templates`** — the named setting bundles (`qwen3`,
  `qwen36-heretic`, `gemma4-heretic`), each with its sampling parameters and
  memory-guard settings.
- **`model_settings`** — which profile each model uses, as
  `active_profile_name`.

## Applying

`scripts/config/apply-profiles.py` reconciles a live install with this snapshot:

```bash
python3 scripts/config/apply-profiles.py            # dry-run diff
python3 scripts/config/apply-profiles.py --check    # non-zero if drifted
python3 scripts/config/apply-profiles.py --apply    # write, with a .bak first
```

Read [`../docs/reference/PROFILES.md`](../docs/reference/PROFILES.md) first: it
explains why each value was chosen, which is the part a diff cannot show.
