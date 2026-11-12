# config

The configuration registry: the example settings, the schema that validates
them, and the model-source registry that the reference docs are built from.

| File | What it is |
| :--- | :--- |
| [`settings.example.json`](settings.example.json) | A sanitized example of `~/.omlx/settings.json`, with a placeholder key. |
| [`schema.json`](schema.json) | The shape those settings must satisfy. |
| [`sources.json`](sources.json) | Every model's HuggingFace source, base model and type. |

## `settings.example.json`

Copy it to `~/.omlx/settings.json` and replace `REPLACE_WITH_YOUR_KEY`. The real
key is **never** committed; see [`../SECURITY.md`](../SECURITY.md).

The settings are explained in
[`../docs/reference/PROFILES.md`](../docs/reference/PROFILES.md). The per-model
sampling profiles live separately in
[`../profiles/omlx-profiles.json`](../profiles/omlx-profiles.json).

## `schema.json`

A compact JSON Schema for the fields in `settings.example.json`. It is not
enforced at runtime by oMLX; it documents the shape and lets a script reject a
malformed example. `scripts/checks/check-docs-fresh.py` does not validate it —
that is a deliberate choice: the schema is documentation, not a gate.

## `sources.json`

The machine-readable model registry. Each entry records the local model id, the
HuggingFace repo, the upstream base model, the quantization and the
uncensored/heretic classification. The reference page
[`../docs/reference/MODELS.md`](../docs/reference/MODELS.md) is written from this
file, and [`../reference/models.json`](../reference/models.json) is the public
copy an application can read.
