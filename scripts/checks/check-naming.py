#!/usr/bin/env python3
"""Naming guard: every source and data file is kebab-case.

Matches the reference repository's rule (`scripts/checks/check-naming.mjs` in
net-traffic-control-catalog): a file that a reader has to type should be
predictable. Markdown is out of scope — document names are allowed to be
UPPERCASE, as in the reference.

Usage:
    python3 scripts/checks/check-naming.py
"""

import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}
EXT = (".py", ".mjs", ".js", ".sh", ".json")

# kebab-case segments, optionally dotted (settings.example.json), then the extension.
PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+(-[a-z0-9]+)*)*\.(py|mjs|js|sh|json)$")


def main():
    bad = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(EXT):
                continue
            if not PATTERN.match(name):
                bad.append(os.path.relpath(os.path.join(root, name), ROOT))
    if bad:
        print("not kebab-case:")
        for p in sorted(bad):
            print(f"  {p}")
        return 1
    print("all source and data files are kebab-case")
    return 0


if __name__ == "__main__":
    sys.exit(main())
