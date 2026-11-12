# Naming conventions

One rule for file names, and each language's own standard for the names inside
the file. This document says what the rule is, why it is the rule, and where it
deliberately gives way to a convention the repository does not own — so a name
that looks wrong can be checked against a written decision rather than a guess.

## File names — scripts and data

Every script and data file is named in **kebab-case**: lowercase letters and
digits, words separated by a single hyphen.

```text
benchmark.py               build-manifest.py
check-docs-fresh.py        settings.example.json
collect-system-info.py     omlx-profiles.json
```

| Applies to | Extensions |
| :--- | :--- |
| Python | `.py` |
| Shell | `.sh` |
| Data | `.json` |

The name is everything before the final extension, so `settings.example.json`
is one kebab-case name (`settings.example`) and `omlx-profiles.json` is
`omlx-profiles`.

**Why kebab-case.** The tooling is a mix of Python and shell under one
`scripts/` tree, and the repository keeps *one* file-name rule for all of it.
The cost is stated plainly: [PEP 8](https://peps.python.org/pep-0008/) prefers
`lowercase_with_underscores` for a Python *module*, and a hyphen is not legal in
an importable module name. `lab-server.py` cannot be written as an `import`; a
script that needs another loads it as a subprocess instead
([`redteam-benchmark.py`](../../scripts/security/redteam-benchmark.py) spawns
[`lab-server.py`](../../scripts/security/lab-server.py)). One rule is easier to
remember than three.

## File names — everything else

Kebab-case is the rule for scripts and data only. Everything else follows a
convention this repository did not invent:

- **Markdown — UPPER-CASE.** A document is named in UPPER-CASE, with a hyphen
  between words: `README.md`, `SECURITY.md`, `CHOOSING-A-MODEL.md`,
  `OFFENSIVE-BENCHMARK.md`. The [`check-naming.py`](../../scripts/checks/check-naming.py)
  guard does not look at it.
- **Vendored, generated and VCS directories are skipped.** `.git`, `.venv`,
  `node_modules`, `__pycache__`, and any file whose name begins with a dot
  (`.gitignore`, `.DS_Store`).
- **Data values are not file names.** A model id such as
  `Qwen3.6-35B-A3B-4bit` inside `reference/results.json` is a string, never
  inspected by the guard.

One JSON key family looks like a violation and is not:

| Where | What | Why |
| :--- | :--- | :--- |
| `config/schema.json` | `$schema`, `properties`, `additionalProperties` | These are [JSON Schema](https://json-schema.org/) keywords, defined by the specification, not by us. |

## Names inside a file

### Python — PEP 8

Inside a `.py` file the ordinary [PEP 8](https://peps.python.org/pep-0008/) rules
apply — the file *name* is the one deviation, kebab-case as above.

| Kind | Convention | Example |
| :--- | :--- | :--- |
| function, variable, parameter | `snake_case` | `short_name`, `model_id` |
| class | `CapWords` | `LabHandler` |
| constant | `UPPER_CASE` | `HERE`, `API_KEY` |
| internal helper | leading underscore | `_iso_date` |

### JSON — the keys belong to their schema

The file name is kebab-case; the object keys are a data file this repository
owns and writes in **`snake_case`**, matching the syntax shown in the
[JSON reference](https://www.w3schools.com/js/json_syntax.asp) examples.

```json
{
  "manifest_version": 1,
  "generated": "2026-11-11",
  "models": 6
}
```

The file *name* is kebab-case (`results.json`), and the *values* are data — a
model id, a throughput number, a date — and carry whatever shape their own
domain requires.

## Enforcement

- [`../../scripts/checks/check-naming.py`](../../scripts/checks/check-naming.py)
  checks every `.py`, `.sh` and `.json` file name in the tree. It runs as step 2
  of [`../../test/test.sh`](../../test/test.sh).
- [`../../scripts/checks/check-docs-fresh.py`](../../scripts/checks/check-docs-fresh.py)
  fails when a document links to a file that does not exist, so a rename cannot
  leave a stale relative link behind.

## Sources

- Python: [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/).
- JSON: [Introducing JSON](https://www.json.org/json-en.html).
