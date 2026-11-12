# oMLX security self-assessment

**Worst finding:** `MEDIUM`  
**Findings by severity:** MEDIUM 2, LOW 1, INFO 3, PASS 4

| Severity | Finding | Evidence |
|---|---|---|
| **MEDIUM** | Unauthenticated OpenAPI schema exposure | GET /openapi.json → HTTP 200; leaks 131 paths / 139 operations (entire admin surface, including destructive endpoints) |
| **MEDIUM** | CORS allows any origin | Access-Control-Allow-Origin: * (credentials not allowed) |
| **LOW** | Interactive API docs are exposed without auth | GET /docs → HTTP 200 |
| **INFO** | /health is unauthenticated | GET /health → HTTP 200 without a key (expected; health probes need no auth) |
| **INFO** | Server fingerprint | Server header: uvicorn |
| **INFO** | Model-level probes skipped | no --model given; pass one to test prompt injection and jailbreak posture |
| **PASS** | Server is not exposed to the LAN | <http://192.168.10.200:8000/health> was unreachable |
| **PASS** | /v1 API requires authentication | unauth GET /v1/models → HTTP 401 |
| **PASS** | Wrong API key is rejected | bogus Bearer token → HTTP 401 |
| **PASS** | Admin API requires authentication | unauth GET /admin/api/models → HTTP 401 |

## Details

### [MEDIUM] Unauthenticated OpenAPI schema exposure

- **Evidence:** GET /openapi.json → HTTP 200; leaks 131 paths / 139 operations (entire admin surface, including destructive endpoints)
- **Reproduce:** `curl -s http://127.0.0.1:8000/openapi.json | head`
- **Remediation:** Serve /openapi.json and /docs behind admin auth, or disable them in production (FastAPI: docs_url=None, redoc_url=None, openapi_url=None). Localhost-only limits the blast radius.

### [MEDIUM] CORS allows any origin

- **Evidence:** Access-Control-Allow-Origin: * (credentials not allowed)
- **Reproduce:** `curl -s -D - -o /dev/null -X OPTIONS -H 'Origin: https://evil.example' http://127.0.0.1:8000/admin/api/models`
- **Remediation:** A page the user visits can still read unauthenticated responses (health, schema). Restrict Access-Control-Allow-Origin to trusted origins.

### [LOW] Interactive API docs are exposed without auth

- **Evidence:** GET /docs → HTTP 200
- **Reproduce:** `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/docs`
- **Remediation:** Disable Swagger UI in production, or require auth to reach it.

### [INFO] /health is unauthenticated

- **Evidence:** GET /health → HTTP 200 without a key (expected; health probes need no auth)
- **Reproduce:** `curl -s http://127.0.0.1:8000/health`
- **Remediation:** Acceptable if the endpoint reveals nothing sensitive. Keep it out of any public exposure.

### [INFO] Server fingerprint

- **Evidence:** Server header: uvicorn
- **Reproduce:** `curl -s -D - -o /dev/null http://127.0.0.1:8000/health`
- **Remediation:** Cosmetic; banner suppression is optional.

### [INFO] Model-level probes skipped

- **Evidence:** no --model given; pass one to test prompt injection and jailbreak posture
- **Reproduce:** `python3 scripts/security/security-probe.py --model Qwen3.6-35B-A3B-4bit:qwen3`
- **Remediation:** -

### [PASS] Server is not exposed to the LAN

- **Evidence:** <http://192.168.10.200:8000/health> was unreachable
- **Reproduce:** `curl -m 5 http://192.168.10.200:8000/health`
- **Remediation:** -

### [PASS] /v1 API requires authentication

- **Evidence:** unauth GET /v1/models → HTTP 401
- **Reproduce:** `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/v1/models`
- **Remediation:** -

### [PASS] Wrong API key is rejected

- **Evidence:** bogus Bearer token → HTTP 401
- **Reproduce:** `-`
- **Remediation:** -

### [PASS] Admin API requires authentication

- **Evidence:** unauth GET /admin/api/models → HTTP 401
- **Reproduce:** `-`
- **Remediation:** -
