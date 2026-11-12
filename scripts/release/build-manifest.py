#!/usr/bin/env python3
"""Write (or check) `manifest.json` — the checksum an application can pin to.

The manifest records the size, SHA-256, model count and result count of the
committed benchmark report and the results data, so a reader can verify it has
not drifted. Standard library only.

Usage:
    python3 scripts/release/build-manifest.py            # write manifest.json
    python3 scripts/release/build-manifest.py --check    # non-zero if stale
"""

import argparse
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
REPORT = os.path.join(ROOT, "benchmarks", "2026-11-11-m1max.md")
RESULTS = os.path.join(ROOT, "reference", "results.json")
MANIFEST = os.path.join(ROOT, "manifest.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build():
    d = json.load(open(RESULTS))
    return {
        "manifest_version": 1,
        "report": "benchmarks/2026-11-11-m1max.md",
        "report_bytes": os.path.getsize(REPORT),
        "report_sha256": sha256(REPORT),
        "results": "reference/results.json",
        "results_sha256": sha256(RESULTS),
        "generated": d["date"],
        "models": len(d["throughput"]),
        "challenges": len(d.get("redteam", {}).get("challenges", [])),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify the committed manifest is current")
    args = ap.parse_args()

    if not (os.path.exists(REPORT) and os.path.exists(RESULTS)):
        print("ERROR: report or results file missing", file=sys.stderr)
        return 2

    current = build()
    if args.check:
        try:
            committed = json.load(open(MANIFEST))
        except Exception as e:
            print(f"ERROR: cannot read manifest: {e}", file=sys.stderr)
            return 2
        committed.pop("generated_unix", None)
        if committed != current:
            print("STALE: manifest.json does not match the data", file=sys.stderr)
            print("  committed:", json.dumps(committed, sort_keys=True), file=sys.stderr)
            print("  expected: ", json.dumps(current, sort_keys=True), file=sys.stderr)
            return 1
        print("OK: manifest.json is current")
        return 0

    current["generated_unix"] = int(time.time())
    with open(MANIFEST, "w") as f:
        json.dump(current, f, indent=2)
        f.write("\n")
    print(f"wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
