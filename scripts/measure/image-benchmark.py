#!/usr/bin/env python3
"""How fast does the local image model render, and does it actually write a file?

The text benchmark measures tokens per second through oMLX. This measures the
other half of the machine: the diffusion model, run by
[`mflux`](https://github.com/filipstrand/mflux), which is a **separate tool** from
oMLX (oMLX does not serve image models). Each prompt is one `mflux-generate-*`
process; the harness times it end to end and checks the PNG it claims to have
written really exists and has the expected size.

Because the mflux CLI is one-shot, every image pays the model load. The headline
is therefore **seconds per image, model load included** — the number a person
actually waits. A `reported_seconds` field carries mflux's own timing when its
log shows one; it is not required.

The model, quantisation, steps and precision come from a profile in
[`../../profiles/mflux-profiles.json`](../../profiles/mflux-profiles.json). This
script changes no state; `--selftest` runs with no model, no GPU and no network.

Usage:
    python3 scripts/measure/image-benchmark.py --selftest
    python3 scripts/measure/image-benchmark.py --profile klein-q8 --limit 2
    python3 scripts/measure/image-benchmark.py --profile flux3-klein-q8 \\
        --out evidence/image-benchmark-2026-11-12.md \\
        --json-out reference/image-benchmark.json
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES_FILE = ROOT / "profiles" / "mflux-profiles.json"
PROMPTS_FILE = ROOT / "data" / "image-prompts.json"

# Processes that already hold the GPU. Running mflux next to one of these
# corrupts both sets of numbers, so the harness refuses unless --force.
GPU_HEAVY = (
    "hallucination-test", "code-benchmark", "code-matrix-test", "grammar-test",
    "context-memory-test", "repo-analysis-test", "benchmark.py",
)


class GuardError(RuntimeError):
    """Raised when the machine is busy with another GPU job."""


def load_profiles(path=PROFILES_FILE):
    with open(path) as f:
        doc = json.load(f)
    return doc, doc.get("generation_profiles", {})


def load_prompts(path=PROMPTS_FILE):
    with open(path) as f:
        return json.load(f)


def gpu_busy():
    """Return the names of known oMLX benchmark processes currently running."""
    running = []
    for name in GPU_HEAVY:
        if shutil.which("pgrep"):
            r = subprocess.run(["pgrep", "-f", name], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                running.append(name)
    return running


def png_dimensions(path):
    """(width, height) from a PNG's IHDR, or None if it is not a PNG."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
    except OSError:
        return None
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def resolve_model(profile, override=""):
    """A local path is expanded; a bare repo id is used as-is."""
    payload = override or profile["local_path"]
    if payload.startswith("~") or payload.startswith("/"):
        return os.path.expanduser(payload)
    return payload


def build_argv(profile, prompt, out_path, model=None, seed=None, steps=None):
    """The mflux command line for one image, from a profile and one prompt."""
    s = profile["settings"]
    argv = [
        profile.get("cli", "mflux-generate-flux2"),
        "--model", resolve_model(profile, model or ""),
        "--base-model", profile["mflux_base_model"],
        "--prompt", prompt,
        "--width", str(s["width"]),
        "--height", str(s["height"]),
        "--steps", str(steps or s["steps"]),
        "--seed", str(seed if seed is not None else s["seed"]),
        "--output", str(out_path),
    ]
    if s.get("compute_precision"):
        argv += ["--compute-precision", s["compute_precision"]]
    return argv


REPORT_RE = re.compile(r"(?:time|elapsed|took|per step|s/step)[^0-9]{0,12}([0-9]+\.[0-9]+)\s*s", re.I)


def reported_seconds(stderr):
    """Best-effort: mflux's own timing line, if the log shows one."""
    for line in reversed(stderr.splitlines()):
        m = REPORT_RE.search(line)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
    return None


def run_one(profile, item, out_dir, model=None, seed=None, steps=None, timeout=1800):
    out_path = Path(out_dir) / f"{profile['name']}--{item['id']}.png"
    argv = build_argv(profile, item["prompt"], out_path, model=model, seed=seed, steps=steps)
    t0 = time.time()
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        stderr, rc = proc.stderr, proc.returncode
    except FileNotFoundError:
        return {"id": item["id"], "category": item.get("category", ""),
                "seconds": None, "reported_seconds": None, "s_per_step": None,
                "returncode": None, "ok": False, "image": str(out_path),
                "dimensions": None, "bytes": None, "sha256_16": None,
                "stderr_tail": f"{argv[0]} not found on PATH", "argv": argv}
    seconds = time.time() - t0
    dims = png_dimensions(out_path)
    size = None
    digest = None
    if out_path.exists():
        size = out_path.stat().st_size
        digest = hashlib.sha256(out_path.read_bytes()).hexdigest()[:16]
    return {
        "id": item["id"],
        "category": item.get("category", ""),
        "seconds": round(seconds, 2),
        "reported_seconds": reported_seconds(stderr),
        "s_per_step": round(seconds / max(1, steps or profile["settings"]["steps"]), 2),
        "returncode": rc,
        "ok": rc == 0 and dims is not None,
        "image": str(out_path),
        "dimensions": list(dims) if dims else None,
        "bytes": size,
        "sha256_16": digest,
        "stderr_tail": "\n".join(stderr.strip().splitlines()[-4:]),
        "argv": argv,
    }


def selftest():
    ok = True
    profiles, gens = load_profiles()
    if set(gens) != {"klein-q8", "flux3-klein-q8"}:
        ok = False
        print("FAIL: unexpected profiles:", sorted(gens))
    prompts = load_prompts()
    ids = [p["id"] for p in prompts["prompts"]]
    if len(ids) != len(set(ids)):
        ok = False
        print("FAIL: duplicate prompt ids")
    for p in prompts["prompts"]:
        if not p.get("prompt") or not p.get("category"):
            ok = False
            print("FAIL: prompt missing text/category:", p.get("id"))
        if p.get("category") not in prompts["categories"]:
            ok = False
            print("FAIL: unknown category:", p.get("category"))
    # arg builder: the M1-family float16 flag and the fixed seed must be present
    for name, prof in gens.items():
        argv = build_argv(prof, "a test", Path("/tmp/x.png"))
        if "--compute-precision" not in argv or "float16" not in argv:
            ok = False
            print(f"FAIL: {name} missing float16 flag:", argv)
        if "--seed" not in argv or "--steps" not in argv:
            ok = False
            print(f"FAIL: {name} missing seed/steps:", argv)
    # PNG header reader against a hand-built IHDR
    tmp = Path("/tmp/_imgbt_selftest.png")
    tmp.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR"
                    + struct.pack(">II", 1024, 768) + b"\x08\x06\x00\x00\x00")
    if png_dimensions(tmp) != (1024, 768):
        ok = False
        print("FAIL: png_dimensions")
    tmp.unlink(missing_ok=True)
    # renderer over a fake row
    fake = {"model": "x", "profile": "klein-q8", "license": "apache-2.0",
            "images": [{"id": "a", "seconds": 12.0, "s_per_step": 3.0,
                        "dimensions": [1024, 1024], "bytes": 100, "ok": True}]}
    if "| `a` |" not in render("2026-11-12", [fake]):
        ok = False
        print("FAIL: render")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


def render(date, rows):
    lines = ["# Image generation — seconds per image", "",
             f"**Date:** {date}. One `mflux-generate-*` process per prompt, run "
             "through [mflux](https://github.com/filipstrand/mflux), which is "
             "separate from the oMLX text server. Time is end-to-end wall clock, "
             "**model load included** (the CLI is one-shot).", ""]
    lines.append("| Model (profile) | Licence | Image | s/img | s/step | Size | OK |")
    lines.append("|---|---|---:|---:|---:|---|:---:|")
    for r in rows:
        for img in r["images"]:
            dims = "×".join(str(d) for d in img["dimensions"]) if img["dimensions"] else "—"
            mb = f"{img['bytes'] / 1024 / 1024:.1f} MB" if img["bytes"] else "—"
            lines.append(f"| `{r['model']}` ({r['profile']}) | {r['license']} | "
                         f"`{img['id']}` | {img['seconds']} | {img['s_per_step']} | "
                         f"{dims}, {mb} | {'✅' if img['ok'] else '❌'} |")
    lines.append("")
    lines.append("_s/img is what a person waits for one finished image on this "
                 "machine. Because each CLI call reloads the model, it is a cold "
                 "number; the steady-state per-step cost is the `s/step` column._")
    # Collapse any run of blank lines to one and drop trailing blanks, so the
    # report is lint-clean however many rows there are (same fix as the
    # hallucination harness, whose section-skipping produced the same MD012).
    out = []
    for line in lines:
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--profile", default="klein-q8", help="profile name from mflux-profiles.json")
    ap.add_argument("--all-profiles", action="store_true", help="run every generation profile")
    ap.add_argument("--model", default="", help="override the model path/repo")
    ap.add_argument("--prompts-file", default=str(PROMPTS_FILE))
    ap.add_argument("--limit", type=int, default=0, help="only the first N prompts")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--force", action="store_true", help="run even if another GPU job is active")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    busy = gpu_busy()
    if busy and not args.force:
        raise SystemExit(
            "GPU is busy with: " + ", ".join(busy) +
            "\noMLX and mflux share the machine; running both corrupts the numbers."
            "\nWait for the other job, or pass --force if you accept that.")

    prompts = load_prompts(args.prompts_file)["prompts"]
    if args.limit:
        prompts = prompts[:args.limit]
    _, gens = load_profiles()
    names = list(gens) if args.all_profiles else [args.profile]
    out_dir = args.out_dir or str(ROOT / "evidence" / "images")

    if not shutil.which(gens[names[0]].get("cli", "mflux-generate-flux2")):
        print(f"warning: {gens[names[0]].get('cli')} not on PATH", file=sys.stderr)

    date = time.strftime("%Y-%m-%d")
    rows = []
    for name in names:
        prof = gens[name]
        print("=" * 70, flush=True)
        print(f"PROFILE {name} | {prof['model']} | {prof['license']}", flush=True)
        row = {"model": prof["model"], "profile": name, "license": prof["license"],
               "cli": prof.get("cli"), "images": []}
        for item in prompts:
            try:
                res = run_one(prof, item, out_dir, model=args.model or None,
                              seed=args.seed, steps=args.steps)
            except subprocess.TimeoutExpired:
                res = {"id": item["id"], "category": item.get("category", ""),
                       "seconds": None, "s_per_step": None, "ok": False,
                       "dimensions": None, "bytes": None, "returncode": None,
                       "stderr_tail": "timeout", "reported_seconds": None}
            row["images"].append(res)
            mark = "ok" if res["ok"] else "FAIL"
            print(f"  {item['id']}: {res['seconds']}s "
                  f"({res['s_per_step']}s/step) {mark} {res['dimensions']}", flush=True)
        rows.append(row)

    data = {"date": date, "rows": rows}
    if args.out:
        Path(args.out).write_text(render(date, rows))
        print("wrote", args.out, flush=True)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print("wrote", args.json_out, flush=True)
    if not args.out and not args.json_out:
        print("\n" + render(date, rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
