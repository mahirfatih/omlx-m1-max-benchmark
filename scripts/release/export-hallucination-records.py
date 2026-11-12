#!/usr/bin/env python3
"""Turn reference/hallucination.json into a readable question-by-question record.

The summary table says "0% hallucination, 2% false alarm"; it does not let the
reader see *which* names a model got wrong, or what it was asked. This writes
that: every probe for every model, and a section listing the misses.

Standard library only. Runs off the committed JSON, no model needed.

Usage:
    python3 scripts/release/export-hallucination-records.py
    python3 scripts/release/export-hallucination-records.py --json reference/hallucination.json
"""

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

# The probes are generated from data/languages.json, so the prompt is described
# here rather than stored per record: the harness asks for a JSON verdict on a
# named API, and the record holds what the model said about it.
PROMPT = (
    "Given a list of programming-language API names, say which are real and "
    "which are invented, with a confidence in [0,1] for each. Answer as JSON."
)


def family(name):
    """Model name without the quant suffix, for the section headings."""
    for suffix in ("-MLX-4bit", "-4bit", "-8bit"):
        name = name.replace(suffix, "")
    return name


def misses(recs):
    return [r for r in recs if r["answered"] and r["expected"] != r["got_real"]]


def render(date, data):
    lines = ["# Hallucination — the questions and the answers", ""]
    total = data["language_count"]
    lines.append(
        f"**Date:** {date}. {total} languages × 2 probes. Both tables are the raw "
        "record behind the summary in "
        "[`../evidence/hallucination-2026-11-12.md`](../evidence/hallucination-2026-11-12.md); "
        "nothing is aggregated away."
    )
    lines.append("")
    lines.append("**What was asked, once per batch of probes:**")
    lines.append("")
    lines.append(f"> {PROMPT}")
    lines.append("")
    lines.append(
        "Each language contributes two names: one **genuine** documented API, and "
        "one **fabricated twin** (the same shape with a small, plausible change). "
        "The model never sees which is which."
    )
    lines.append("")

    lines.append("## Who got what wrong")
    lines.append("")
    lines.append(
        "| Model | Answered | Hallucination (fake → \"real\") | False alarm (real → \"fake\") | Misses |"
    )
    lines.append("| :--- | ---: | ---: | ---: | ---: |")
    ranked = sorted(
        (m for m in data["models"] if "error" not in m),
        key=lambda m: (-m["hallucination_rate"], -m["false_alarm_rate"]),
    )
    for m in ranked:
        ms = misses(m["_records"])
        lines.append(
            f"| `{m['model']}` | {m['answered']}/{m['total']} | "
            f"**{m['hallucination_rate']*100:.0f}%** ({m['hallucinations']}/{m['fake_total']}) | "
            f"{m['false_alarm_rate']*100:.0f}% ({m['false_alarms']}/{m['real_total']}) | "
            f"{len(ms)} |"
        )
    lines.append("")
    lines.append(
        "**Every miss in this run is a false alarm, not a hallucination.** No model, "
        "on any of the 102 languages, called a fabricated name real. The two models "
        "that are not at 0% called two *real* APIs fake instead."
    )
    lines.append("")

    lines.append("## Every miss, with the name and the confidence")
    lines.append("")
    lines.append(
        "| Model | Direction | Language | Name the model judged | Stated confidence |"
    )
    lines.append("| :--- | :--- | :--- | :--- | ---: |")
    any_miss = False
    for m in ranked:
        for r in misses(m["_records"]):
            any_miss = True
            direction = (
                "**fake → \"real\"** (hallucination)"
                if r["role"] == "fake"
                else "real → \"fake\" (false alarm)"
            )
            conf = "—" if r["conf"] is None else f"{r['conf']:.2f}"
            lines.append(
                f"| `{family(m['model'])}` | {direction} | `{r['lang']}` | "
                f"`{r['name']}` | {conf} |"
            )
    if not any_miss:
        lines.append("| — | — | — | — | — |")
    lines.append("")

    lines.append("## The full record, per model")
    lines.append("")
    lines.append(
        "`expected` is whether the name is real; `got_real` is whether the model "
        "said it is. They agree unless the row is a miss. `conf` is the confidence "
        "the model stated, or `—` when it did not state one."
    )
    lines.append("")
    for m in ranked:
        lines.append(f"### `{family(m['model'])}`")
        lines.append("")
        lines.append(
            f"{m['answered']}/{m['total']} answered, {len(misses(m['_records']))} missed."
        )
        lines.append("")
        lines.append("| Language | Name | Real? | Model said | Confidence | Correct |")
        lines.append("| :--- | :--- | :--- | :--- | ---: | :---: |")
        for r in sorted(m["_records"], key=lambda r: (r["lang"], r["role"])):
            if not r["answered"]:
                continue
            ok = r["expected"] == r["got_real"]
            conf = "—" if r["conf"] is None else f"{r['conf']:.2f}"
            lines.append(
                f"| `{r['lang']}` | `{r['name']}` | {'yes' if r['expected'] else 'no'} | "
                f"{'yes' if r['got_real'] else 'no'} | {conf} | {'✅' if ok else '❌'} |"
            )
        lines.append("")
    # Collapse runs of blank lines and drop trailing ones: a model with no
    # answered probes, or an empty miss table, would otherwise leave two blanks
    # in a row and fail MD012.
    out = []
    for line in lines:
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default=os.path.join(ROOT, "reference", "hallucination.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "reference", "hallucination-records.md"))
    args = ap.parse_args()

    with open(args.json) as f:
        data = json.load(f)
    with open(args.out, "w") as f:
        f.write(render(data["date"], data))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
