# `scripts/security/` — the security layer

Two questions, two tools. Everything here targets **your own machine**: the
probe refuses a non-loopback address, and the lab binds to `127.0.0.1` only.

| Script | Question | Needs a model |
| :--- | :--- | :---: |
| [`security-probe.py`](security-probe.py) | Is the *server* exposed, gated, leaking? With `--model`, is the *model* resistant to injection/jailbreak? | optional |
| [`redteam-benchmark.py`](redteam-benchmark.py) | Can the *model* actually exploit a local target and reverse a binary? | yes |
| [`lab-server.py`](lab-server.py) | The deliberately vulnerable target (SQLi, command injection, LFI, XSS). | no |
| [`make-re-challenge.py`](make-re-challenge.py) | Builds the split-secret C binary for the RE challenge. | no |

## Running

```bash
# server posture (no model loaded)
python3 scripts/security/security-probe.py

# server + model resistance
python3 scripts/security/security-probe.py --model Qwen3.6-35B-A3B-4bit:qwen3

# offensive capability scorecard
python3 scripts/security/redteam-benchmark.py \
    --models Qwen3.6-35B-A3B-4bit:qwen3,Qwen3.8-27B-Uncensored-MLX:qwen36-heretic
```

## The rails

- `security-probe.py` exits non-zero on a `HIGH`/`CRITICAL` finding.
- It refuses a non-loopback target unless `--allow-remote` is passed.
- `lab-server.py` refuses to bind anything but loopback.
- The web challenges are **simulated**: the lab decides whether an exploit
  succeeded; it runs no shell command and reads no real file.
- The RE binary is compiled by this repository, not a third-party artifact.

Do not remove these rails. The findings and the threat model are in
[`../../docs/security/README.md`](../../docs/security/README.md); the scorecard is
in [`../../docs/security/OFFENSIVE-BENCHMARK.md`](../../docs/security/OFFENSIVE-BENCHMARK.md).
