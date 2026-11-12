# evidence

The raw output of the security tools, committed so a finding can be checked
without re-running it. Each file is named with the date it was produced.

| File | Produced by | What it shows |
| :--- | :--- | :--- |
| [`security-probe-2026-11-11.md`](security-probe-2026-11-11.md) | `scripts/security/security-probe.py` | Server posture: bind, auth, schema leak, CORS. |
| [`security-probe-model-2026-11-11.md`](security-probe-model-2026-11-11.md) | `security-probe.py --model …` | Model resistance: prompt injection, system-prompt leak, jailbreaks. |
| [`redteam-2026-11-11.md`](redteam-2026-11-11.md) | `scripts/security/redteam-benchmark.py` | Offensive capability scorecard. |

## Regenerating

```bash
python3 scripts/security/security-probe.py --out evidence/security-probe-<date>.md
python3 scripts/security/security-probe.py --model <id> --out evidence/security-probe-model-<date>.md
python3 scripts/security/redteam-benchmark.py --models <ids> --out evidence/redteam-<date>.md
```

These need the server (and, for the model and red-team runs, a loaded model), so
they are not part of [`../test/test.sh`](../test/test.sh). The findings are
summarised in [`../docs/security/README.md`](../docs/security/README.md) and
[`../docs/security/OFFENSIVE-BENCHMARK.md`](../docs/security/OFFENSIVE-BENCHMARK.md).
