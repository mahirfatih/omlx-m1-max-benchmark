# evidence

The raw output of the harnesses, committed so a finding or a number can be
checked without re-running it. Each file is named with the date it was produced.

## Security

| File | Produced by | What it shows |
| :--- | :--- | :--- |
| [`security-probe-2026-11-11.md`](security-probe-2026-11-11.md) | `scripts/security/security-probe.py` | Server posture: bind, auth, schema leak, CORS. |
| [`security-probe-model-2026-11-11.md`](security-probe-model-2026-11-11.md) | `security-probe.py --model …` | Model resistance: prompt injection, system-prompt leak, jailbreaks. |
| [`redteam-2026-11-11.md`](redteam-2026-11-11.md) | `scripts/security/redteam-benchmark.py` | Offensive capability scorecard. |

## Capability runs

The transcript each measurement script printed, kept verbatim so the numbers in
[`../reference/`](../reference/README.md) can be audited against the run that
produced them.

| File | Produced by | What it shows |
| :--- | :--- | :--- |
| [`code-matrix-2026-11-22.md`](code-matrix-2026-11-22.md) | `scripts/measure/code-matrix-test.py` | Python / Node / Bash / Swift syntax matrix for the 2026-11-22 profiles. |
| [`code-benchmark-2026-11-11.md`](code-benchmark-2026-11-11.md) · [`-devstral-2026-11-12.md`](code-benchmark-devstral-2026-11-12.md) · [`-2026-11-22.md`](code-benchmark-2026-11-22.md) | `scripts/measure/code-benchmark.py` | Per-problem coding pass counts and the code that produced them. |
| [`grammar-2026-11-11.md`](grammar-2026-11-11.md) · [`-2026-11-22.md`](grammar-2026-11-22.md) | `scripts/measure/grammar-test.py` | Format/grammar adherence per schema. |
| [`context-memory-2026-11-11.md`](context-memory-2026-11-11.md) · [`-2026-11-22.md`](context-memory-2026-11-22.md) | `scripts/measure/context-memory-test.py` | Long-context retrieval, conflict and aggregate answers. |
| [`hallucination-2026-11-12.md`](hallucination-2026-11-12.md) · [`-2026-11-22.md`](hallucination-2026-11-22.md) | `scripts/measure/hallucination-test.py` | 102 languages × 2 probes, per model. |
| [`repo-analysis-2026-11-11.md`](repo-analysis-2026-11-11.md) · [`-2026-11-22.md`](repo-analysis-2026-11-22.md) | `scripts/measure/repo-analysis-test.py` | Repository-analysis fact recall on a real project. |

> **Note — the campaign did not re-run everything.** The 2026-11-22 campaign ran
> the capability suites above against the three new models, but **not** the
> red-team harness, so there is no `redteam-2026-11-22.md`; those models are shown
> as `pending` in the red-team tables rather than with a guessed score.

## Regenerating

Security:

```bash
python3 scripts/security/security-probe.py --out evidence/security-probe-<date>.md
python3 scripts/security/security-probe.py --model <id> --out evidence/security-probe-model-<date>.md
python3 scripts/security/redteam-benchmark.py --models <ids> --out evidence/redteam-<date>.md
```

Capability runs (each takes `--models id:profile` and `--out`):

```bash
python3 scripts/measure/code-matrix-test.py --models <ids> --out evidence/code-matrix-<date>.md
python3 scripts/measure/code-benchmark.py --models <ids> --out evidence/code-benchmark-<date>.md \
    --json-out reference/code-benchmark-<date>.json
```

These all need the server (and, for most, a loaded model), so they are not part of
[`../test/test.sh`](../test/test.sh). The findings are summarised in
[`../docs/security/README.md`](../docs/security/README.md),
[`../docs/security/OFFENSIVE-BENCHMARK.md`](../docs/security/OFFENSIVE-BENCHMARK.md)
and [`../docs/analysis/`](../docs/analysis/README.md).
