#!/usr/bin/env python3
"""Render the measured results as a Markdown summary with Mermaid charts.

Reads [`../../reference/results.json`](../../reference/results.json) — the single
machine-readable record of every number in this repository — and prints the
throughput ranking, the red-team scorecard, and two Mermaid charts. No model, no
server, no network: it only reformats committed data.

Usage:
    python3 scripts/analysis/analyze-results.py
    python3 scripts/analysis/analyze-results.py --json > analysis.json
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "reference", "results.json")


def short(name):
    return name.replace("-MLX-4bit", "").replace("-4bit", "").replace("Qwen3.6-35B-A3B-Uncensored-Heretic", "Heretic")


def render(d):
    env = d["env"] if "env" in d else d["environment"]
    rows = sorted(d["throughput"], key=lambda r: -r["avg"])
    lines = ["# Results summary", ""]
    lines.append(f"**Measured:** {d['date']} · {env['chip']} · {env['ram_gb']} GB · {env['server']}")
    lines.append("")
    lines.append("## Throughput ranking")
    lines.append("")
    lines.append("| # | Model | Profile | EN tok/s | TR tok/s | Average | Load (s) |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | `{short(r['model'])}` | `{r['profile']}` | {r['en']:.1f} | {r['tr']:.1f} | **{r['avg']:.1f}** | {r['load_s']:.1f} |")

    names = [short(r["model"]) for r in rows]
    avgs = [r["avg"] for r in rows]
    lines += ["", "```mermaid", "xychart-beta", '    title "Average decode throughput (tok/s)"',
              "    x-axis [" + ", ".join(f'"{n}"' for n in names) + "]", '    y-axis "tok/s" 0 --> 80',
              "    bar [" + ", ".join(f"{v:.1f}" for v in avgs) + "]", "```"]
    lines += ["", "```mermaid", "xychart-beta", '    title "EN vs TR throughput (tok/s)"',
              "    x-axis [" + ", ".join(f'"{n}"' for n in names) + "]", '    y-axis "tok/s" 0 --> 80',
              "    bar [" + ", ".join(f"{r['en']:.1f}" for r in rows) + "]",
              "    bar [" + ", ".join(f"{r['tr']:.1f}" for r in rows) + "]", "```",
              "", "_Series order: 1st bar = EN, 2nd = TR._"]

    rt = d.get("redteam")
    if rt:
        lines += ["", "## Red-team scorecard", ""]
        cols = rt["challenges"]
        head = "| Model | " + " | ".join(c.upper() for c in cols) + " | Score |"
        lines.append(head)
        lines.append("|---|" + "|".join(":---:" for _ in cols) + "|---:|")
        for r in sorted(rt["results"], key=lambda x: -int(x["score"].split("/")[0])):
            cells = ["✅" if r.get(c) else "❌" for c in cols]
            lines.append(f"| `{short(r['model'])}` | " + " | ".join(cells) + f" | **{r['score']}** |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="emit the raw data as JSON")
    args = ap.parse_args()
    d = json.load(open(DATA))
    if args.json:
        json.dump(d, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(render(d))


if __name__ == "__main__":
    main()
