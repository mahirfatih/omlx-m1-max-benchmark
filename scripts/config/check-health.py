#!/usr/bin/env python3
"""Check that the local oMLX server is up and list the models it serves.

Reads the API key from ``~/.omlx/settings.json`` (never prints it), queries
``/health`` and ``/v1/models``, and exits non-zero if the server is unhealthy so
it can gate a scheduled run. Standard library only, no dependencies.

Usage:
    python3 scripts/check-health.py
    python3 scripts/check-health.py --base http://127.0.0.1:8000
    python3 scripts/check-health.py --wait 180
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

SETTINGS = os.path.expanduser("~/.omlx/settings.json")


def api_key():
    try:
        with open(SETTINGS) as f:
            return (json.load(f).get("auth", {}) or {}).get("api_key", "")
    except Exception:
        return ""


def get(url, key, timeout=8):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key} if key else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def healthy(base, key):
    try:
        return get(base + "/health", key).get("status") == "healthy"
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="http://127.0.0.1:8000", help="server base URL")
    ap.add_argument("--wait", type=int, default=0, help="seconds to poll for health before failing")
    args = ap.parse_args()

    key = api_key()
    deadline = time.time() + args.wait
    while True:
        if healthy(args.base, key):
            break
        if time.time() >= deadline:
            print(f"UNHEALTHY: {args.base}/health did not report 'healthy'", file=sys.stderr)
            return 1
        time.sleep(5)

    print(f"OK: {args.base} is healthy")
    try:
        models = get(args.base + "/v1/models", key)
        data = models.get("data", models)
        names = sorted(m.get("id", "?") for m in data)
        print(f"Models served: {len(names)}")
        for n in names:
            print(f"  - {n}")
    except urllib.error.HTTPError as e:
        print(f"WARN: could not list models (HTTP {e.code})", file=sys.stderr)
    except Exception as e:
        print(f"WARN: could not list models ({e})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
