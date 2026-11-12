# Security

This repository is two things at once, and each has a security story:

1. **A configuration snapshot** — profiles and settings people copy to their own
   machine. The risk here is a leaked secret.
2. **A security benchmark** — tools that test a local server and local models.
   The risk here is misuse against something that is not yours.

## Secrets

**No API key, token or private key is committed.** The scripts read the key from
`~/.omlx/settings.json` at runtime and never print it. What ships is:

- [`config/settings.example.json`](config/settings.example.json) — with the
  placeholder `REPLACE_WITH_YOUR_KEY`.
- [`profiles/omlx-profiles.json`](profiles/omlx-profiles.json) — settings only,
  no authentication material.

If you fork this and add your own config, keep the key out of it. A pre-commit
check is cheap:

```bash
grep -rnE "omlx-[a-z0-9]{8,}|secret_key|Bearer [A-Za-z0-9]{20,}" . --exclude-dir=.git
```

### What a key protects, and what it does not

The oMLX API key stops another **process on the same machine** from using your
server through the socket. It does not stop a process that can read
`~/.omlx/settings.json` — that process has the key. File permissions are the
control there, not the token.

## The security benchmark is authorised-use only

[`scripts/security/security-probe.py`](scripts/security/security-probe.py) and
[`scripts/security/redteam-benchmark.py`](scripts/security/redteam-benchmark.py) are built for
**your own machine**:

- The probe **refuses a non-loopback target** unless `--allow-remote` is passed.
- The lab target ([`scripts/security/lab-server.py`](scripts/security/lab-server.py))
  binds to `127.0.0.1` only and refuses any other host.
- The web challenges are **simulated**: the lab decides whether an exploit
  succeeded; it does not run shell commands or read real files.
- The reverse-engineering challenge operates on a binary **this repository
  compiles**, not a third-party artifact.

Do not remove these rails to point the tools at a system you do not own. Doing
so is unauthorised access in most jurisdictions, and it is not what these tools
are for.

## The models are not aligned by default

Three of the six models in [`docs/reference/MODELS.md`](docs/reference/MODELS.md)
are **abliterated** — their safety alignment has been deliberately removed. They
will answer prompts that aligned models refuse. This repository records that
behaviour factually; it does not endorse it.

If you deploy one of these models behind an interface other people use, the
alignment is **your** responsibility. A server-side content filter, a constrained
tool set, and a clear scope are the controls. The model will not provide them.

## The server surface

The findings for a default local oMLX 0.7.3 install — loopback bind, `/v1` auth,
unauthenticated `/openapi.json`, wildcard CORS — and their remediations are in
[`docs/security/README.md`](docs/security/README.md). Read it before exposing the
server to anything other than `localhost`.

## Reporting

A security issue in **this repository** (a leaked secret in history, a script
that could be misused): email `irtibat@mahirfatih.com`. Do not open a public
issue for a live leak. An issue in **oMLX itself** belongs upstream at
<https://github.com/jundot/omlx>.
