#!/usr/bin/env python3
"""Report the size of every locally installed MLX model.

Walks the model directories oMLX reads (``~/.omlx/settings.json`` →
``model.model_dirs``, ``~/.cache/huggingface/hub`` and ``~/models`` by default),
sums the ``.safetensors`` weights and the whole folder, and prints a Markdown
table sorted biggest-first. Standard library only, no dependencies.

Usage:
    python3 scripts/model-sizes.py            # Markdown table to stdout
    python3 scripts/model-sizes.py --json     # JSON to stdout
    python3 scripts/model-sizes.py --dir ~/models
"""

import argparse
import json
import os
import sys

SETTINGS = os.path.expanduser("~/.omlx/settings.json")
DEFAULT_DIRS = [
    os.path.expanduser("~/models"),
    os.path.expanduser("~/.cache/huggingface/hub"),
]


def model_dirs():
    """Directories to scan, from oMLX settings first, then the defaults."""
    dirs = []
    try:
        with open(SETTINGS) as f:
            cfg = json.load(f)
        for d in (cfg.get("model", {}) or {}).get("model_dirs", []) or []:
            dirs.append(os.path.expanduser(d))
    except Exception:
        pass
    for d in DEFAULT_DIRS:
        if d not in dirs:
            dirs.append(d)
    return [d for d in dirs if os.path.isdir(d)]


def looks_like_model(path):
    """A model folder has a config.json and at least one weight file."""
    if not os.path.isfile(os.path.join(path, "config.json")):
        return False
    for name in os.listdir(path):
        if name.endswith(".safetensors") or name.endswith(".gguf") or name.endswith(".npz"):
            return True
    return False


def dir_size(path, suffix=None):
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            if suffix and not name.endswith(suffix):
                continue
            try:
                total += os.path.getsize(os.path.join(root, name))
            except OSError:
                pass
    return total


def scan(roots):
    found = []
    seen = set()
    for root in roots:
        for dirpath, dirnames, _files in os.walk(root):
            # Do not descend into a model folder once found.
            if looks_like_model(dirpath):
                real = os.path.realpath(dirpath)
                if real not in seen:
                    seen.add(real)
                    found.append({
                        "name": os.path.basename(dirpath),
                        "path": dirpath,
                        "weights_gb": round(dir_size(dirpath, (".safetensors", ".gguf", ".npz")) / 1024 ** 3, 2),
                        "total_gb": round(dir_size(dirpath) / 1024 ** 3, 2),
                    })
                dirnames[:] = []
    return sorted(found, key=lambda m: -m["total_gb"])


def as_markdown(models):
    if not models:
        return "No model folders found. Set `model.model_dirs` in `~/.omlx/settings.json`."
    lines = ["| Model | Weights (GB) | Folder (GB) | Path |", "|---|---:|---:|---|"]
    total = 0.0
    for m in models:
        total += m["total_gb"]
        lines.append(f"| `{m['name']}` | {m['weights_gb']} | {m['total_gb']} | `{m['path']}` |")
    lines.append(f"| **Total ({len(models)})** | | **{total:.1f}** | |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--dir", action="append", default=[], help="extra directory to scan (repeatable)")
    args = ap.parse_args()

    roots = [os.path.expanduser(d) for d in args.dir] + model_dirs()
    models = scan(roots)
    if args.json:
        json.dump({"roots": roots, "models": models}, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(as_markdown(models))


if __name__ == "__main__":
    main()
