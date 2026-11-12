# `scripts/config/` — the server configuration

Tools that read or write the live oMLX configuration under `~/.omlx/`.

| Script | What it does |
| :--- | :--- |
| [`check-health.py`](check-health.py) | Polls `/health`, lists the served models, exits non-zero if unhealthy. |
| [`apply-profiles.py`](apply-profiles.py) | Reconciles the committed [`profiles/omlx-profiles.json`](../../profiles/omlx-profiles.json) with the live `~/.omlx/`. |

## `check-health.py`

```bash
python3 scripts/config/check-health.py
python3 scripts/config/check-health.py --wait 180    # poll for up to 3 minutes
```

Reads the key from `~/.omlx/settings.json`, prints every model the server
advertises, and returns non-zero if `/health` never reports `healthy` — usable
as a pre-flight gate.

## `apply-profiles.py`

```bash
python3 scripts/config/apply-profiles.py            # dry-run diff
python3 scripts/config/apply-profiles.py --check    # non-zero on drift
python3 scripts/config/apply-profiles.py --apply    # write, with backups
```

`--apply` copies each live file to `<file>.bak-<timestamp>` before writing, then
reminds you to restart oMLX:

```bash
~/.omlx/bin/omlx stop; sleep 4; ~/.omlx/bin/omlx start
```

The setting-by-setting explanation is in
[`../../docs/reference/PROFILES.md`](../../docs/reference/PROFILES.md).
