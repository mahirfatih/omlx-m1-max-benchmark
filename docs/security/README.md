# `docs/security/` — the attack surface

What a local oMLX deployment exposes, what was found on this machine, and how to
re-test it.

- [`README.md`](README.md) — this file: the threat model and the findings.
- [`OFFENSIVE-BENCHMARK.md`](OFFENSIVE-BENCHMARK.md) — the red-team capability benchmark and its results.

Two tools back this folder, both standard library only:

| Tool | Question it answers |
| :--- | :--- |
| [`../../scripts/security/security-probe.py`](../../scripts/security/security-probe.py) | Is the *server* exposed, gated, and leaking anything? |
| [`../../scripts/security/redteam-benchmark.py`](../../scripts/security/redteam-benchmark.py) | Can the *models* actually exploit a local target and reverse a binary? |

## Threat model

The deployment is a **single-user local server** on a laptop. The realistic
attacker is not a remote host; it is:

1. **A web page the user visits** — which can make cross-origin requests to
   `http://127.0.0.1:8000` from the browser. This is why CORS and CSRF matter
   even for a loopback service.
2. **Another local process** running as the same user — which can read
   `~/.omlx/settings.json` (including the API key) directly. No network control
   defends against this; file permissions do.
3. **A prompt the model processes** — untrusted text that tries to redirect the
   model ("ignore previous instructions"). Relevant because the model may be
   wired to tools.

What is **out of scope**: a remote network attacker (the server does not listen
off-host) and a privileged local attacker.

## Findings on this machine (2026-11-11)

Measured with `scripts/security/security-probe.py` and manual `curl` checks against
`http://127.0.0.1:8000`, oMLX 0.7.3.

| # | Severity | Finding | Evidence |
| :--- | :--- | :--- | :--- |
| 1 | **PASS** | Binds to loopback only | `lsof` → `TCP 127.0.0.1:8000 (LISTEN)`; the LAN IP `192.168.10.200:8000` is unreachable (`HTTP 000`). |
| 2 | **PASS** | `/v1` API requires a key | unauth `GET /v1/models` → `401`; a bogus Bearer token → `401`. |
| 3 | **PASS** | Admin API requires auth | unauth `GET /admin/api/models` → `401 {"detail":"Admin authentication required"}`. |
| 4 | **MEDIUM** | OpenAPI schema is unauthenticated | `GET /openapi.json` → `200`, leaking **131 paths / 139 operations**, including destructive admin routes. `GET /docs` → `200`. |
| 5 | **MEDIUM** | CORS allows any origin | `Access-Control-Allow-Origin: *`; `Access-Control-Allow-Credentials` is absent, so cookie-bearing cross-origin requests are not readable. |
| 6 | **INFO** | `/health` is unauthenticated | `GET /health` → `200` (expected; health probes need no auth). |
| 7 | **INFO** | Server banner | `server: uvicorn` on every response. |

### Why finding 4 matters

`/openapi.json` describes the entire admin surface — model load/unload, profile
editing, HuggingFace download/delete, global settings, logs. The endpoints
themselves are gated (finding 3), so this is **information disclosure**, not
access. It is still worth closing: an attacker learns exactly which destructive
verb to aim at, and any *future* endpoint that forgets its auth check is
advertised in advance. Because the bind is loopback-only, the practical attacker
is a local process or a cross-origin page (finding 5).

### Why finding 5 matters

`Access-Control-Allow-Origin: *` means a page the user visits can read any
**unauthenticated** response — `/health`, `/openapi.json`, `/docs`. It cannot
read `/v1` or `/admin/api` responses, because those need a key/session the page
does not have and credentials are not allowed. The residual risk is that a
malicious page can fingerprint the local server and its schema.

## Remediation

| Finding | Fix |
| :--- | :--- |
| 4 — schema leak | Serve `/openapi.json`, `/docs`, `/redoc` behind admin auth, or disable them (`docs_url=None, redoc_url=None, openapi_url=None`). File it upstream if oMLX has no switch. |
| 5 — wildcard CORS | Pin `Access-Control-Allow-Origin` to the admin UI's own origin; never combine `*` with credentials. |
| 7 — banner | Optional: suppress the `Server` header at a reverse proxy, if one is ever added. |
| 1–3 — already good | Keep the loopback bind and the auth gates; do not "temporarily" bind `0.0.0.0` to test from a phone. |

## Re-testing

```bash
python3 scripts/security/security-probe.py                  # passive: bind, auth, CORS, schema
python3 scripts/security/security-probe.py --model Qwen3.6-35B-A3B-4bit:qwen3   # + model probes
```

The probe refuses a non-loopback target unless `--allow-remote` is passed, so it
cannot be aimed at a third party by accident. Exit code is non-zero when any
finding is `HIGH` or `CRITICAL`, which makes it usable as a pre-flight gate.

## The models themselves

Server hardening is only half of it. The other half is whether the *models*
behave safely when fed hostile input. That is measured separately, and — because
three of the six are deliberately abliterated — the answer differs by model. See
[`OFFENSIVE-BENCHMARK.md`](OFFENSIVE-BENCHMARK.md).
