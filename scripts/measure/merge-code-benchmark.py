#!/usr/bin/env python3
"""Merge coding-benchmark JSON runs into one file.

Used when a first run has bad rows for some models and a re-run covers the rest:
the later run for a model replaces the earlier one, keyed by model id.

    python3 scripts/measure/merge-code-benchmark.py main.json rerun.json --out merged.json
"""

import argparse
import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def merge(docs):
    base = docs[0]
    order = []
    rows = {}
    for doc in docs:
        for row in doc.get("models", []):
            if row["model"] not in rows:
                order.append(row["model"])
            rows[row["model"]] = row
    base["models"] = [rows[m] for m in order]
    base["problems"] = docs[0].get("problems", [])
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="JSON files, later overrides earlier per model")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    merged = merge([load(p) for p in args.inputs])
    with open(args.out, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"merged {len(merged['models'])} models -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
