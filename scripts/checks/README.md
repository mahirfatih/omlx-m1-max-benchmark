# `scripts/checks/` — the static guarantees

Everything that proves a change is safe **without** a model, a server or a
network. This is what [`../../test/test.sh`](../../test/test.sh) runs.

| Script | What it proves |
| :--- | :--- |
| [`check-docs-fresh.py`](check-docs-fresh.py) | Relative links resolve; `manifest.json` matches the data; no secret is committed. |
| [`check-naming.py`](check-naming.py) | Every `.py` / `.mjs` / `.js` / `.sh` / `.json` file is kebab-case. |

## Running

```bash
python3 scripts/checks/check-docs-fresh.py
python3 scripts/checks/check-naming.py
```

## Why these, and not more

The measurement scripts need a GPU and a loaded model; the security scripts need
a server. Neither belongs in a check that a reviewer runs on a pull request. These
two are the parts that can run anywhere, so they are the parts that gate a merge.
A hand edit to a **generated** file — the manifest, a diagram — is caught here
rather than discovered later.

The rule behind `check-naming.py` is in
[`../../docs/guides/NAMING.md`](../../docs/guides/NAMING.md).
