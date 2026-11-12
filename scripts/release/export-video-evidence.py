#!/usr/bin/env python3
"""Build evidence/video-benchmark-<date>.md from a video-benchmark.py JSON run.

The image layer has `image-benchmark.py --out` writing its own Markdown, and we
hand-added the galleries afterwards. Videos are the same shape, so this script
takes the run's JSON, copies the produced clips next to the evidence file, and
renders the table plus one section per prompt with the prompt quoted verbatim
from data/video-prompts.json.

    python3 scripts/release/export-video-evidence.py \
        --run /tmp/videorun/results.json \
        --out evidence/video-benchmark-2026-11-12.md \
        --clips-dir evidence/videos

It changes no model state; it only reads the run and writes the two files.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / "data" / "video-prompts.json"


def load_prompts() -> dict[str, dict]:
    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    return {p["id"]: p for p in data["prompts"]}


def die(msg: str) -> "None":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def collapse(text: str) -> str:
    """Collapse runs of blank lines and drop a trailing one (house style)."""
    out: list[str] = []
    blanks = 0
    for line in text.split("\n"):
        if line.strip() == "":
            blanks += 1
            if blanks > 1:
                continue
        else:
            blanks = 0
        out.append(line)
    while out and out[-1].strip() == "":
        out.pop()
    return "\n".join(out) + "\n"


def build(run: dict, clips_dir: Path, source_dir: Path) -> str:
    prompts = load_prompts()
    date = run.get("date", "")
    lines: list[str] = []

    lines.append("# Video generation — seconds per clip")
    lines.append("")
    lines.append(
        f"**Date:** {date}. One runner process per prompt, through an MLX video tool "
        "([`VideoX-Fun-mlx`](https://github.com/dgrauet/VideoX-Fun-mlx) for the "
        "CogVideoX-Fun layer), which is separate from the oMLX text server and from "
        "the mflux image layer. Time is end-to-end wall clock, **model load "
        "included**; the runner is one-shot. Each output is probed with `ffprobe`, "
        "so the size and length are read from the file, not from the runner's log."
    )
    lines.append("")
    lines.append("| Model (profile) | Licence | Prompt | s/clip | Output | Frames | fps | Codec | OK |")
    lines.append("|---|---|---|---:|---|---:|---:|---|:---:|")
    rows = run.get("rows", [])
    for row in rows:
        for v in row["videos"]:
            p = v.get("probe") or {}
            dims = f"{p.get('width')}×{p.get('height')}" if p.get("width") else "—"
            dur = f"{p.get('duration')}s" if p.get("duration") is not None else "—"
            mb = f"{v['bytes'] / 1024 / 1024:.1f} MB" if v.get("bytes") else "—"
            secs = v.get("seconds")
            secs = f"{secs}" if secs is not None else "—"
            lines.append(
                f"| `{row['model']}` ({row['profile']}) | {row['license']} | "
                f"`{v['id']}` | {secs} | {dims}, {dur}, {mb} | "
                f"{p.get('nb_frames', '—')} | {p.get('fps', '—')} | "
                f"{p.get('codec', '—')} | {'✅' if v.get('ok') else '❌'} |"
            )
    lines.append("")
    lines.append(
        "_s/clip is what a person waits for one finished clip on this machine, model "
        "load included. The size, length and frame count come from `ffprobe` on the "
        "written file, not from the runner's own log line._"
    )
    lines.append("")
    lines.append("## The clips themselves")
    lines.append("")
    lines.append(
        "These are the model's normal output at the profile's settings, not a "
        "selected best-of. Each is written as an animated GIF of a handful of "
        "frames, so **it plays in the browser but stops abruptly** — that is the "
        "model's clip length, not an export error. The prompt is quoted under each "
        "clip so you can judge the result against what was actually asked."
    )
    lines.append("")

    for row in rows:
        profile = row["profile"]
        for v in row["videos"]:
            item = prompts.get(v["id"], {})
            cat = item.get("category", v.get("category", ""))
            lines.append(f"### `{v['id']}` — {cat}")
            lines.append("")
            lines.append(f"> {item.get('prompt', '')}")
            lines.append("")
            src = Path(v["video"]) if v.get("video") else Path()
            if v.get("ok") and src.is_file():
                clips_dir.mkdir(parents=True, exist_ok=True)
                dst = clips_dir / src.name
                shutil.copy2(src, dst)
                rel = f"videos/{dst.name}"
                p = v.get("probe") or {}
                lines.append(
                    f"![{v['id']}, {profile}]({rel})"
                )
            else:
                lines.append(f"_No clip: the run did not produce a file ({v.get('stderr_tail', '')})._")
            lines.append("")

    ok = sum(1 for row in rows for v in row["videos"] if v.get("ok"))
    total = sum(len(row["videos"]) for row in rows)
    lines.append(
        f"{ok} of {total} clips rendered. The `--frames` flag is not linear and this "
        "model tops out at 5 frames: asking for 4 decodes to 1 frame, asking for 8 "
        "decodes to the same 5 as asking for 5, and an odd count raises a reshape "
        "error because the patch size is 2. The runner's log line disagrees with the "
        "file, which is why the frame column above is `ffprobe`'s."
    )
    lines.append("")
    return collapse("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the video-benchmark.py --json-out file")
    ap.add_argument("--out", required=True, help="Markdown file to write")
    ap.add_argument("--clips-dir", default=str(ROOT / "evidence" / "videos"))
    ap.add_argument("--source-dir", default="", help="directory holding the run's clips")
    args = ap.parse_args()

    run_path = Path(args.run)
    if not run_path.is_file():
        die(f"run file not found: {run_path}")
    run = json.loads(run_path.read_text(encoding="utf-8"))
    if not run.get("rows"):
        die("run file has no rows")

    source_dir = Path(args.source_dir) if args.source_dir else run_path.parent
    md = build(run, Path(args.clips_dir), source_dir)
    Path(args.out).write_text(md, encoding="utf-8")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
