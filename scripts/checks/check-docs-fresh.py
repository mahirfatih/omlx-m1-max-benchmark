#!/usr/bin/env python3
"""Static drift check — what a hand edit to a generated file would break.

Three guarantees, all offline:

1. **Relative links resolve.** Every `[text](relative/path)` in a Markdown file
   points at a file that exists.
2. **The manifest is current.** `manifest.json` matches the report and results
   it describes (same check as `scripts/release/build-manifest.py --check`).
3. **No secret is committed.** No oMLX API key or Bearer token appears in a
   tracked text file.

Usage:
    python3 scripts/checks/check-docs-fresh.py
"""

import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}

SECRET_PATTERNS = [
    re.compile(r"omlx-[a-z0-9]{16,}"),
    re.compile(r"secret_key\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-]{24,}"),
]


def walk_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            yield os.path.join(root, name)


def check_links():
    bad = []
    for path in walk_files():
        if not path.endswith(".md"):
            continue
        text = open(path, encoding="utf-8").read()
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = link.split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                bad.append(f"{os.path.relpath(path, ROOT)}: {link}")
    return bad


def check_manifest():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "release", "build-manifest.py"), "--check"],
                       capture_output=True, text=True)
    return [] if r.returncode == 0 else [r.stderr.strip() or "manifest stale"]


def check_secrets():
    bad = []
    for path in walk_files():
        if not path.endswith((".md", ".json", ".py", ".sh", ".yml", ".yaml", ".txt")):
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                bad.append(f"{os.path.relpath(path, ROOT)}: matches {pat.pattern!r}")
    return bad


def main():
    problems = []
    problems += [f"broken link: {x}" for x in check_links()]
    problems += [f"manifest: {x}" for x in check_manifest()]
    problems += [f"secret: {x}" for x in check_secrets()]
    if problems:
        print("\n".join(problems))
        return 1
    print("docs fresh: links resolve, manifest current, no secrets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
