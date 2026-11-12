#!/usr/bin/env python3
"""Can a model find a fact buried in a long context — and reconcile two that conflict?

Throughput tells you how fast a model decodes; this tells you whether a long
context is actually *used*. The script builds a long, boring document with a few
facts planted inside it, asks one question at a time, and scores the answer:

  * **retrieval** — one unique code planted mid-document;
  * **conflict** — the same code stated twice, the second correcting the first;
    the answer must be the corrected value;
  * **aggregate** — three facts planted in three different regions.

The idea follows the long-context memory line of work, in particular
[`HUST-AI-HYZ/MemoryAgentBench`](https://github.com/HUST-AI-HYZ/MemoryAgentBench)
(MIT). The generator, the questions and the scoring here are original.

Standard library only. `--selftest` needs no model and no server: it builds the
context and proves the needles are present and the scorer agrees.

Usage:
    python3 scripts/measure/context-memory-test.py --selftest
    python3 scripts/measure/context-memory-test.py --models Qwen3.6-35B-A3B-4bit:qwen3
    python3 scripts/measure/context-memory-test.py --fills 800 --json
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

SETTINGS = os.path.expanduser("~/.omlx/settings.json")
BASE = "http://127.0.0.1:8000/v1"

ALL_MODELS = [
    "Qwen3-Coder-30B-A3B-Instruct-4bit",
    "Ornith-1.5-35B-A3B-MLX-4bit",
    "Qwen3.6-35B-A3B-4bit",
    "Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit",
    "gemma-4-26B-A4B-it-heretic-4bit",
    "Qwen3.8-27B-Uncensored-MLX",
]

DEFAULT_TARGETS = [
    ("Qwen3.6-35B-A3B-4bit", "qwen3"),
    ("Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit", "qwen36-heretic"),
    ("Ornith-1.5-35B-A3B-MLX-4bit", "qwen3"),
    ("gemma-4-26B-A4B-it-heretic-4bit", "gemma4-heretic"),
    ("Qwen3-Coder-30B-A3B-Instruct-4bit", "qwen3"),
    ("Qwen3.8-27B-Uncensored-MLX", "qwen36-heretic"),
]

FILLER = [
    "The archive team logged routine maintenance for the {n}th shelf that morning.",
    "A clerk noted the ambient humidity reading as acceptable for storage {n}.",
    "Routine inspection {n} found no anomalies in the north corridor.",
    "The backup rotation {n} completed without incident.",
    "Inventory pass {n} matched the expected shelf counts.",
    "A memo ({n}) reminded staff about the updated filing convention.",
    "The weekly report {n} restated the standard retention window.",
    "No access requests were filed against batch {n}.",
]


def planted():
    """The facts and questions. Codes are derived so they are stable but not guessable."""
    tag = hashlib.sha256(b"omlx-context-memory").hexdigest()[:8]
    retrieval_code = f"AX-{tag}-7391"
    first_code = f"V1-{tag}-2210"
    corrected_code = f"V2-{tag}-8850"
    agg = {
        "router": f"RT-{tag[:4]}-014",
        "deadline": "the eleventh of March",
        "owner": "the platform team",
    }
    return {
        "retrieval_code": retrieval_code,
        "first_code": first_code,
        "corrected_code": corrected_code,
        "agg": agg,
    }


def build_context(fills, facts):
    """A long document with the needles placed at ~20%, ~60% and ~85% depth."""
    n_total = max(60, fills)
    positions = {
        int(n_total * 0.20): ("retrieval", f"IMPORTANT: the maintenance access code is {facts['retrieval_code']}."),
        int(n_total * 0.60): ("conflict1", f"Correction notice: the release code was misprinted as {facts['first_code']}."),
        int(n_total * 0.85): ("conflict2", f"Superseding notice: disregard all earlier release codes; the release code is {facts['corrected_code']}."),
    }
    a = facts["agg"]
    positions[int(n_total * 0.30)] = (
        "agg_router", f"Infrastructure note: the edge router is designated {a['router']}.")
    positions[int(n_total * 0.50)] = (
        "agg_deadline", f"Project note: the migration deadline is {a['deadline']}.")
    positions[int(n_total * 0.75)] = (
        "agg_owner", f"Governance note: the service owner is {a['owner']}.")

    lines = ["ARCHIVE LOG — quarterly maintenance record. Read carefully; facts are scattered.",
             ""]
    for i in range(n_total):
        if i in positions:
            lines.append("")
            lines.append(positions[i][1])
            lines.append("")
        lines.append(FILLER[i % len(FILLER)].format(n=i))
    return "\n".join(lines), positions


def questions(facts):
    a = facts["agg"]
    return [
        {"id": "retrieval",
         "prompt": "What is the maintenance access code? Answer with the code only.",
         "expected": facts["retrieval_code"]},
        {"id": "conflict",
         "prompt": "What is the release code? If it was corrected, give the corrected value. Answer with the code only.",
         "expected": facts["corrected_code"], "forbidden": facts["first_code"]},
        {"id": "aggregate",
         "prompt": ("From the infrastructure, project and governance notes, report the edge router, "
                    "the migration deadline and the service owner. One short line."),
         # Each group is a set of accepted surface forms; a fact counts if any
         # variant appears. Grading on a single literal string punishes a correct
         # answer that writes "11th March" instead of "the eleventh of March".
         "expected_all": [
             [a["router"]],
             [a["deadline"], "11th march", "11 march", "march 11"],
             [a["owner"], "platform team"],
         ]},
    ]


def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def grade(q, answer):
    if "expected_all" in q:
        groups = q["expected_all"]
        hit = sum(1 for alts in groups if any(normalize(v) in normalize(answer) for v in alts))
        return (hit == len(groups)), f"{hit}/{len(groups)} facts"
    ok = normalize(q["expected"]) in normalize(answer)
    if "forbidden" in q and normalize(q["forbidden"]) in normalize(answer):
        ok = False
    return ok, q["expected"]


def wait_health(t=240):
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=8) as r:
                if json.loads(r.read()).get("status") == "healthy":
                    return True
        except Exception:
            pass
        time.sleep(5)
    return False


def load_key():
    with open(SETTINGS) as f:
        return json.load(f)["auth"]["api_key"]


def unload_all(headers):
    for m in ALL_MODELS:
        req = urllib.request.Request(BASE + f"/models/{m}/unload", data=b"{}", headers=headers, method="POST")
        try:
            urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            pass


def call(headers, model, prompt, max_tokens):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    return time.time() - t0, d["choices"][0]["message"].get("content", "") or ""


def selftest():
    facts = planted()
    ctx, positions = build_context(400, facts)
    ok = True
    # every needle must actually appear in the context
    for code in (facts["retrieval_code"], facts["first_code"], facts["corrected_code"]):
        if code not in ctx:
            ok = False
            print("FAIL: needle missing from context:", code)
    # the scorer must agree on a correct and a wrong answer
    qs = questions(facts)
    good = {qs[0]["id"]: qs[0]["expected"], qs[1]["id"]: qs[1]["expected"],
            qs[2]["id"]: " ".join(facts["agg"].values())}
    bad = {qs[0]["id"]: "I could not find it", qs[1]["id"]: facts["first_code"],
           qs[2]["id"]: facts["agg"]["router"]}
    for q in qs:
        g_ok, _ = grade(q, good[q["id"]])
        b_ok, _ = grade(q, bad[q["id"]])
        if not g_ok or b_ok:
            ok = False
            print(f"FAIL {q['id']}: good->{g_ok} bad->{b_ok}")
        else:
            print(f"ok {q['id']}: good accepted, bad rejected")
    print(f"context: {len(ctx)} chars, ~{len(ctx)//4} tokens, {len(positions)} plants")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--models", default="")
    ap.add_argument("--fills", type=int, default=400, help="filler lines (context size)")
    ap.add_argument("--max-tokens", type=int, default=120)
    ap.add_argument("--out", default="")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    facts = planted()
    ctx, _ = build_context(args.fills, facts)
    qs = questions(facts)
    targets = DEFAULT_TARGETS
    if args.models:
        targets = [tuple(x.split(":", 1)) if ":" in x else (x, "qwen3")
                   for x in args.models.split(",") if x]
    if not wait_health():
        raise SystemExit("oMLX server is not healthy")

    headers = {"Authorization": "Bearer " + load_key(), "Content-Type": "application/json"}
    rows = []
    for model, prof in targets:
        print("=" * 70, flush=True)
        print(f"MODEL: {model} | profile: {prof} | context ~{len(ctx)//4} tokens", flush=True)
        unload_all(headers)
        time.sleep(3)
        try:
            call(headers, model, "Merhaba, tek kelime yaz.", 8)
        except Exception as e:
            print("  warmup failed:", str(e)[:160], flush=True)
            rows.append({"model": model, "profile": prof, "error": str(e)[:160]})
            continue
        row = {"model": model, "profile": prof, "tasks": {}}
        for q in qs:
            prompt = ctx + "\n\n---\nQUESTION: " + q["prompt"]
            try:
                elapsed, answer = call(headers, model, prompt, args.max_tokens)
            except Exception as e:
                row["tasks"][q["id"]] = {"ok": False, "reason": str(e)[:120]}
                print(f"  {q['id']}: ERROR {str(e)[:100]}", flush=True)
                continue
            ok, reason = grade(q, answer)
            row["tasks"][q["id"]] = {"ok": ok, "reason": reason, "answer_s": round(elapsed, 1),
                                     "raw": answer.strip()[:200]}
            print(f"  {q['id']}: {'ok' if ok else 'MISS'} in {elapsed:.1f}s", flush=True)
        rows.append(row)

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = {"date": date, "context_chars": len(ctx), "context_tokens_est": len(ctx) // 4,
            "tasks": [q["id"] for q in qs], "models": rows}
    if args.out:
        with open(args.out, "w") as f:
            f.write(render(date, data))
        print("\nwrote", args.out, flush=True)
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("wrote", args.json_out, flush=True)
    if not args.out and not args.json_out:
        print("\n" + render(date, data))
    return 0


def render(date, data):
    ids = data["tasks"]
    lines = ["# Long-context memory", "",
             f"**Date:** {date}. Context ~{data['context_tokens_est']} tokens "
             f"({data['context_chars']} chars) with facts planted at increasing depth.", ""]
    lines.append("| Model | " + " | ".join(ids) + " | Recalled |")
    lines.append("|---|" + "|".join(":---:" for _ in ids) + "|---:|")
    for r in data["models"]:
        if "error" in r:
            lines.append(f"| `{r['model']}` | " + " | ".join("—" for _ in ids) + " | failed |")
            continue
        cells = ["✅" if r["tasks"][t]["ok"] else "❌" for t in ids]
        n = sum(1 for t in ids if r["tasks"][t]["ok"])
        lines.append(f"| `{r['model']}` | " + " | ".join(cells) + f" | **{n}/{len(ids)}** |")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
