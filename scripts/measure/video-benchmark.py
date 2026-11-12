#!/usr/bin/env python3
"""How fast does a local video model render, and what file does it actually write?

The text benchmark measures tokens per second through oMLX; the image benchmark
measures FLUX images through mflux. This measures the third layer: local **video**
generation, run by an MLX video tool — [`mlx-gen`](https://github.com/lpalbou/mlx-gen)
for Wan2.2, or [`VideoX-Fun-mlx`](https://github.com/dgrauet/VideoX-Fun-mlx) for
CogVideoX-Fun. Both are **separate tools** from oMLX, and separate from mflux.

Each prompt is one runner process; the harness times it end to end and then asks
**ffprobe** what the written file actually is — duration, resolution, frame count,
frame rate, codec — instead of trusting the runner's own log. That is the video
equivalent of reading a PNG's IHDR, and it is why ffmpeg/ffprobe is a dependency
only for a real run, never for `--selftest`.

The command line comes from a profile's `invoke` list in
[`../../profiles/video-profiles.json`](../../profiles/video-profiles.json), with
`{tokens}` filled from the profile's settings. This script changes no state;
`--selftest` runs with no model, no GPU and no network.

Usage:
    python3 scripts/measure/video-benchmark.py --selftest
    python3 scripts/measure/video-benchmark.py --profile wan22-ti2v-5b-q8 --limit 1
    python3 scripts/measure/video-benchmark.py --all-profiles \\
        --out evidence/video-benchmark-2026-11-12.md \\
        --json-out reference/video-benchmark.json
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES_FILE = ROOT / "profiles" / "video-profiles.json"
PROMPTS_FILE = ROOT / "data" / "video-prompts.json"

# Processes that already hold the GPU. Running a video job next to one of these
# corrupts both sets of numbers, so the harness refuses unless --force.
GPU_HEAVY = (
    "hallucination-test", "code-benchmark", "code-matrix-test", "grammar-test",
    "context-memory-test", "repo-analysis-test", "benchmark.py",
    "image-benchmark.py", "mlxgen", "quick_infer.py",
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
    """Return the names of known GPU-heavy processes currently running."""
    running = []
    for name in GPU_HEAVY:
        if shutil.which("pgrep"):
            r = subprocess.run(["pgrep", "-f", name], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                running.append(name)
    return running


def resolve_model(profile, override=""):
    """A local path is expanded; a bare repo id is used as-is."""
    payload = override or profile["local_path"]
    if payload.startswith("~") or payload.startswith("/"):
        return os.path.expanduser(payload)
    return payload


def token_map(profile, prompt, out_path, model=None, seed=None, steps=None, repo=None):
    s = profile.get("settings", {})
    return {
        "model": resolve_model(profile, model or ""),
        "prompt": prompt,
        "output": str(out_path),
        "repo": os.path.expanduser(repo or profile.get("repo", "")),
        "width": str(s.get("width", "")),
        "height": str(s.get("height", "")),
        "frames": str(s.get("frames", "")),
        "fps": str(s.get("fps", "")),
        "steps": str(steps if steps is not None else s.get("steps", "")),
        "guidance": str(s.get("guidance", "")),
        "seed": str(seed if seed is not None else s.get("seed", "")),
    }


def build_argv(profile, prompt, out_path, model=None, seed=None, steps=None, repo=None):
    """The runner command line for one video, from a profile and one prompt."""
    tokens = token_map(profile, prompt, out_path, model=model, seed=seed, steps=steps, repo=repo)
    argv = []
    for part in profile["invoke"]:
        out = part
        for key, val in tokens.items():
            out = out.replace("{" + key + "}", val)
        if "{" in out and "}" in out:
            raise ValueError(f"unresolved token in invoke item: {part!r}")
        argv.append(out)
    return argv


def parse_ffprobe(text):
    """Turn `ffprobe -of json` output into the fields a reader wants, or None."""
    try:
        doc = json.loads(text)
    except (ValueError, TypeError):
        return None
    streams = doc.get("streams") or []
    if not streams:
        return None
    v = streams[0]
    fmt = doc.get("format") or {}

    def as_int(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return None

    def as_float(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    def as_rate(x):
        """'16/1' or '24' -> 24.0."""
        if not x:
            return None
        if "/" in str(x):
            num, _, den = str(x).partition("/")
            n, d = as_float(num), as_float(den)
            return round(n / d, 3) if n and d else None
        return as_float(x)

    width = as_int(v.get("width"))
    height = as_int(v.get("height"))
    nb_frames = as_int(v.get("nb_frames"))
    fps = as_rate(v.get("avg_frame_rate")) or as_rate(v.get("r_frame_rate"))
    duration = as_float(fmt.get("duration"))
    if duration is None and nb_frames and fps:
        duration = round(nb_frames / fps, 3)
    return {
        "codec": v.get("codec_name"),
        "width": width,
        "height": height,
        "nb_frames": nb_frames,
        "fps": fps,
        "duration": duration,
        "bytes": as_int(fmt.get("size")),
    }


def ffprobe(path):
    """Run ffprobe on a written file; None if ffprobe is missing or the file is bad."""
    if not shutil.which("ffprobe"):
        return None
    try:
        proc = subprocess.run(
            ["ffprobe", "-v", "error",
             "-show_entries", "stream=codec_name,width,height,nb_frames,avg_frame_rate,r_frame_rate",
             "-show_entries", "format=duration,size",
             "-of", "json", str(path)],
            capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_ffprobe(proc.stdout)


def run_one(profile, item, out_dir, model=None, seed=None, steps=None, repo=None, timeout=3600):
    ext = profile.get("output_format", "mp4")
    out_path = Path(out_dir) / f"{profile['name']}--{item['id']}.{ext}"
    argv = build_argv(profile, item["prompt"], out_path,
                      model=model, seed=seed, steps=steps, repo=repo)
    t0 = time.time()
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        stderr, rc = proc.stderr, proc.returncode
    except FileNotFoundError:
        return {"id": item["id"], "category": item.get("category", ""),
                "seconds": None, "returncode": None, "ok": False, "video": str(out_path),
                "probe": None, "bytes": None, "sha256_16": None,
                "stderr_tail": f"{argv[0]} not found on PATH", "argv": argv}
    seconds = time.time() - t0
    probe = ffprobe(out_path) if out_path.exists() else None
    size, digest = None, None
    if out_path.exists():
        size = out_path.stat().st_size
        digest = hashlib.sha256(out_path.read_bytes()).hexdigest()[:16]
    return {
        "id": item["id"],
        "category": item.get("category", ""),
        "seconds": round(seconds, 2),
        "returncode": rc,
        "ok": rc == 0 and probe is not None,
        "video": str(out_path),
        "probe": probe,
        "bytes": size,
        "sha256_16": digest,
        "stderr_tail": "\n".join(stderr.strip().splitlines()[-4:]),
        "argv": argv,
    }


def selftest():
    ok = True
    _, gens = load_profiles()
    if set(gens) != {"wan22-ti2v-5b-q8", "cogvideox-fun-1.5-5b-inp-q8"}:
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
    # arg builder: every token resolves, and the essentials are present
    for name, prof in gens.items():
        argv = build_argv(prof, "a test", Path("/tmp/x." + prof.get("output_format", "mp4")))
        joined = " ".join(argv)
        if "{prompt}" in joined or "{output}" in joined or "{model}" in joined:
            ok = False
            print(f"FAIL: {name} left a token unresolved:", argv)
        if "a test" not in argv or "--prompt" not in argv or "--output" not in argv:
            ok = False
            print(f"FAIL: {name} missing prompt/output:", argv)
        if not any("{model}" not in a and (prof["model"] in a or "models" in a) for a in argv):
            ok = False
            print(f"FAIL: {name} did not resolve the model:", argv)
    # ffprobe parser against a hand-built report
    sample = json.dumps({
        "streams": [{"codec_name": "h264", "width": 480, "height": 832,
                     "nb_frames": "25", "avg_frame_rate": "16/1", "r_frame_rate": "16/1"}],
        "format": {"duration": "1.562500", "size": "123456"}})
    got = parse_ffprobe(sample)
    if not got or got["width"] != 480 or got["fps"] != 16.0 or got["nb_frames"] != 25:
        ok = False
        print("FAIL: parse_ffprobe:", got)
    # duration derived when the container omits it
    derived = parse_ffprobe(json.dumps({
        "streams": [{"width": 10, "height": 10, "nb_frames": "50", "avg_frame_rate": "25/1"}]}))
    if not derived or derived["duration"] != 2.0:
        ok = False
        print("FAIL: parse_ffprobe derived duration:", derived)
    # renderer over a fake row
    fake = {"model": "x", "profile": "wan22-ti2v-5b-q8", "license": "apache-2.0",
            "videos": [{"id": "a", "seconds": 243.4, "ok": True,
                        "probe": {"width": 480, "height": 832, "nb_frames": 25,
                                  "fps": 16.0, "duration": 1.5625, "codec": "h264", "bytes": 100},
                        "bytes": 100}]}
    if "| `a` |" not in render("2026-11-12", [fake]):
        ok = False
        print("FAIL: render")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


def render(date, rows):
    lines = ["# Video generation — seconds per clip", "",
             f"**Date:** {date}. One runner process per prompt, through an MLX video "
             "tool (`mlx-gen` or `VideoX-Fun-mlx`), which is separate from the oMLX "
             "text server and from the mflux image layer. Time is end-to-end wall "
             "clock, **model load included**. Each output is probed with `ffprobe`, "
             "so the size and length are read from the file, not the log.", ""]
    lines.append("| Model (profile) | Licence | Prompt | s/clip | Output | Frames | fps | Codec | OK |")
    lines.append("|---|---|---|---:|---|---:|---:|---|:---:|")
    for r in rows:
        for v in r["videos"]:
            p = v.get("probe") or {}
            dims = f"{p.get('width')}×{p.get('height')}" if p.get("width") else "—"
            dur = f"{p.get('duration')}s" if p.get("duration") is not None else "—"
            mb = f"{v['bytes'] / 1024 / 1024:.1f} MB" if v.get("bytes") else "—"
            lines.append(f"| `{r['model']}` ({r['profile']}) | {r['license']} | "
                         f"`{v['id']}` | {v['seconds']} | {dims}, {dur}, {mb} | "
                         f"{p.get('nb_frames', '—')} | {p.get('fps', '—')} | "
                         f"{p.get('codec', '—')} | {'✅' if v['ok'] else '❌'} |")
    lines.append("")
    lines.append("_s/clip is what a person waits for one finished clip on this "
                 "machine, model load included. The output columns come from "
                 "`ffprobe` on the written file._")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--profile", default="wan22-ti2v-5b-q8",
                    help="profile name from video-profiles.json")
    ap.add_argument("--all-profiles", action="store_true", help="run every generation profile")
    ap.add_argument("--model", default="", help="override the model path/repo")
    ap.add_argument("--repo", default="", help="override the runner repository path (VideoX-Fun-mlx)")
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
            "\nEvery GPU job shares the machine; running two at once corrupts both"
            "\nnumbers. Wait for the other job, or pass --force if you accept that.")

    prompts = load_prompts(args.prompts_file)["prompts"]
    if args.limit:
        prompts = prompts[:args.limit]
    _, gens = load_profiles()
    names = list(gens) if args.all_profiles else [args.profile]
    out_dir = args.out_dir or str(ROOT / "evidence" / "videos")

    first = gens[names[0]]
    if not shutil.which(first["invoke"][0]):
        print(f"warning: {first['invoke'][0]} not on PATH", file=sys.stderr)
    if not shutil.which("ffprobe"):
        print("warning: ffprobe not on PATH; output files cannot be probed", file=sys.stderr)

    date = time.strftime("%Y-%m-%d")
    rows = []
    for name in names:
        prof = gens[name]
        print("=" * 70, flush=True)
        print(f"PROFILE {name} | {prof['model']} | {prof['license']}", flush=True)
        row = {"model": prof["model"], "profile": name, "license": prof["license"],
               "runner": prof.get("runner"), "videos": []}
        for item in prompts:
            try:
                res = run_one(prof, item, out_dir, model=args.model or None,
                              seed=args.seed, steps=args.steps, repo=args.repo or None)
            except subprocess.TimeoutExpired:
                res = {"id": item["id"], "category": item.get("category", ""),
                       "seconds": None, "ok": False, "probe": None, "bytes": None,
                       "returncode": None, "stderr_tail": "timeout"}
            row["videos"].append(res)
            mark = "ok" if res["ok"] else "FAIL"
            p = res.get("probe") or {}
            print(f"  {item['id']}: {res['seconds']}s {mark} "
                  f"{p.get('width')}x{p.get('height')} {p.get('nb_frames')}f "
                  f"{p.get('fps')}fps", flush=True)
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
