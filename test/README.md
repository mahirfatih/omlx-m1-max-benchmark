# test

The offline gate. Everything here runs with Python 3 standard library only, no
model and no network.

```bash
./test/test.sh
./test/test.sh --fast
```

## Every step, and what it proves

| Step | Command | Catches |
| :--- | :--- | :--- |
| 1 | `py_compile` / `ast.parse` over `scripts/` | a syntax error, a broken import |
| 2 | [`../scripts/checks/check-naming.py`](../scripts/checks/check-naming.py) | a file that is not kebab-case |
| 3 | [`../scripts/release/build-manifest.py --check`](../scripts/release/build-manifest.py) | a manifest that no longer describes the report/results |
| 4 | [`../scripts/checks/check-docs-fresh.py`](../scripts/checks/check-docs-fresh.py) | a broken relative link, a committed secret |
| 5 | [`../scripts/analysis/analyze-results.py`](../scripts/analysis/analyze-results.py) | a results file the analysis cannot parse |
| 6 | [`collect-system-info.py`](../scripts/measure/collect-system-info.py), [`model-sizes.py`](../scripts/measure/model-sizes.py) | a script that crashes on a machine without oMLX |
| 7 | a source assertion | a removed loopback / remote guard in the security tools |
| 8 | a data assertion | the reference project [`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog) being unlinked, or its analysis data going missing |
| 9 | [`../scripts/measure/code-benchmark.py --selftest`](../scripts/measure/code-benchmark.py) | a problem whose reference solution or test cases are broken |

## What is deliberately **not** here

The real measurements and the red-team run need a loaded model and a running
server, so they are not in this suite:

- [`../scripts/measure/benchmark.py`](../scripts/measure/benchmark.py)
- [`../scripts/measure/code-matrix-test.py`](../scripts/measure/code-matrix-test.py)
- [`../scripts/measure/repo-analysis-test.py`](../scripts/measure/repo-analysis-test.py)
- [`../scripts/measure/code-benchmark.py`](../scripts/measure/code-benchmark.py) (the `--selftest` path *is* in the suite)
- [`../scripts/security/security-probe.py`](../scripts/security/security-probe.py)
- [`../scripts/security/redteam-benchmark.py`](../scripts/security/redteam-benchmark.py)

They are run by hand on the host, and their outputs are committed under
`benchmarks/` and [`../evidence/`](../evidence/README.md). The suite gates what it
can gate offline; it does not pretend to reproduce a GPU.

## The whole suite

The consecutive steps are what CI runs — see
[`../.github/workflows/ci.yml`](../.github/workflows/ci.yml) — so a pull request
that breaks the manifest or a link fails before review.
