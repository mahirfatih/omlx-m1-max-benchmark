# oMLX benchmark — project audit

**Date:** 2026-11-11  
**Scope:** data quality, scripts, tests, CI, release, reproducibility and docs.

## Executive summary

The repository is clean, linear and runnable. `./test/test.sh` passes every
offline check: syntax, kebab-case naming, the manifest, relative links, the
analysis render and the security rails. The layout mirrors
[`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog):
the same top-level files, the same `docs/` and `scripts/` subfolders, the same
`config/`, `reference/`, `evidence/`, `test/` and `.github/` shape.

The measured result is stable: six models, one machine, one run each. The open
risks are about **coverage and reproducibility**, not correctness — every number
traces to a committed file.

## Findings

### Open findings

| # | Priority | Area | Finding | Proposed fix |
|---|---|---|---|---|
| 1 | HIGH | Coverage | The reverse-engineering challenge is 0/6: no model recovered the split secret. The benchmark reports a ceiling it cannot see above. | Add a tool-loop variant (decompiler / debugger in the loop) so the RE axis measures the *pipeline*, not just the text model. |
| 2 | HIGH | Reproducibility | Every throughput figure is a single run. Short outputs (150–200 tokens) make one outlier move the average. | Run each model N=3 and commit the median with a min/max spread. |
| 3 | MEDIUM | Server posture | `/openapi.json` is unauthenticated and leaks the whole admin surface (131 paths / 139 operations). | Serve schema and `/docs` behind admin auth, or disable them (`docs_url=None, openapi_url=None`). Recorded in [`../../evidence/security-probe-2026-11-11.md`](../../evidence/security-probe-2026-11-11.md). |
| 4 | MEDIUM | Server posture | Wildcard CORS (`Access-Control-Allow-Origin: *`). | Restrict to trusted origins; localhost-only limits the blast radius but a visited page can still read unauthenticated responses. |
| 5 | MEDIUM | Model safety | `Qwen3.8-27B-Uncensored` follows instructions embedded in untrusted content (`INJECTION-SUCCESS`). Expected for a raw LLM, but must be documented before it is wired to tools. | Keep tools out of the prompt path, or separate data from instructions. Recorded in [`../../evidence/security-probe-model-2026-11-11.md`](../../evidence/security-probe-model-2026-11-11.md). |
| 6 | LOW | Coverage | The web challenges are textbook and may be memorised; a harder target would lower every score. | Add at least one non-canonical challenge (a logic flaw, an auth bypass with no signature) to separate reasoning from recall. |

### Closed findings

| Topic | Status |
|---|---|
| `scripts/*.py` flat layout diverged from the reference repo | Closed: moved into `measure/`, `security/`, `config/`, `analysis/`, `checks/`, `release/`; every path reference updated. |
| Manifest missing / potentially stale | Closed: `scripts/release/build-manifest.py` writes it and `--check` gates it in `test/test.sh`. |
| Documents linked to non-existent files after the move | Closed: `check-docs-fresh.py` resolves every relative link and runs in the suite. |
| Non-kebab-case file names (`lab_server.py`) | Closed: renamed to `lab-server.py`; `check-naming.py` gates it. |
| This audit not indexed | Closed: listed in [`../README.md`](../README.md). |

## Release and CI checks

- [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml) runs
  `./test/test.sh` on push and pull request.
- [`../../.github/workflows/release.yml`](../../.github/workflows/release.yml) is
  manual-only and rehearses by default: it runs the suite, prints the notes and
  the assets it *would* attach, and stops unless `publish` is set to true.
- The manifest is the release contract: report bytes + results bytes + SHA-256.
  A hand edit to either file fails `build-manifest.py --check`.

## Priority next work

1. A tool-loop variant of the reverse-engineering challenge.
2. N=3 throughput runs, committed as a median with spread.
3. Fix the server posture findings (schema auth, CORS) and re-run the probe.
4. One non-canonical web challenge.
5. A second machine, so the numbers are not a single-host claim.

## Final verification

```text
./test/test.sh     -> all checks passed
working tree       -> clean
```
