#!/usr/bin/env python3
"""Do the models obey a format, or just say something plausible?

Every other benchmark here scores *content*. This one scores *shape*: the model
is asked to answer as a strictly valid JSON value that matches a small schema,
and the answer is validated. It measures instruction-following and structured
output, which matters the moment you pipe a model into code.

The idea of a grammar/format-adherence benchmark follows
[`egavrin/deal-llm-grammar-benchmark`](https://github.com/egavrin/deal-llm-grammar-benchmark).
The schemas, the validator and the tasks here are written for this repository
and use the standard library only — no `jsonschema`.

Standard library only. `--selftest` needs no model and no server: it proves the
validator against hand-written good/bad answers.

Usage:
    python3 scripts/measure/grammar-test.py --selftest
    python3 scripts/measure/grammar-test.py --models Qwen3.6-35B-A3B-4bit:qwen3
    python3 scripts/measure/grammar-test.py --json
"""

import argparse
import datetime
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TASKS_FILE = os.path.join(ROOT, "data", "grammar-prompts.json")


def load_tasks(path=TASKS_FILE):
    """Load the format-adherence tasks: a schema, an instruction, and one
    hand-written good and bad answer each. Kept in data/ so the prompts are
    readable and editable in one place, the way the image and video prompts are.

    Each task: a schema (subset of JSON Schema) and the instruction. The model
    must return a single JSON value and nothing else.
    """
    with open(path) as f:
        return json.load(f)["tasks"]


TASKS = load_tasks()


def type_ok(value, name):
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    return False


def validate(value, schema, path="$"):
    """Return a list of human-readable violations (empty == valid)."""
    errs = []
    t = schema.get("type")
    if t and not type_ok(value, t):
        return [f"{path}: expected {t}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path}: {value} > maximum {schema['maximum']}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errs.append(f"{path}: missing required key {key!r}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errs.append(f"{path}: unexpected key {key!r}")
        for key, sub in props.items():
            if key in value:
                errs.extend(validate(value[key], sub, f"{path}.{key}"))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path}: needs >= {schema['minItems']} items, has {len(value)}")
        if "items" in schema:
            for i, item in enumerate(value):
                errs.extend(validate(item, schema["items"], f"{path}[{i}]"))
    return errs


def extract_json(text):
    """Pull the first complete JSON value out of a model answer."""
    text = text.strip()
    # strip a fenced block if present
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text), None
    except Exception:
        pass
    # fall back to the first balanced {...} or [...]
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == opener:
                depth += 1
            elif text[i] == closer:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1]), None
                    except Exception as e:
                        return None, f"not JSON: {e}"
    return None, "no JSON value found"


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


def grade(answer, schema):
    value, err = extract_json(answer)
    if err:
        return False, err
    errs = validate(value, schema)
    return not errs, ("valid" if not errs else "; ".join(errs[:4]))


def selftest():
    ok = True
    for task in TASKS:
        tid = task["id"]
        # The good/bad answers live beside the schema in data/grammar-prompts.json,
        # so the file that defines a task also proves the validator against it.
        good_ok, why = grade(json.dumps(task["good"]), task["schema"])
        bad_ok, bad_why = grade(json.dumps(task["bad"]), task["schema"])
        if not good_ok or bad_ok:
            ok = False
            print(f"FAIL {tid}: good->{good_ok} ({why}); bad->{bad_ok} ({bad_why})")
        else:
            print(f"ok {tid}: good accepted, bad rejected")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--models", default="")
    ap.add_argument("--max-tokens", type=int, default=300)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

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
        print(f"MODEL: {model} | profile: {prof}", flush=True)
        unload_all(headers)
        time.sleep(3)
        try:
            call(headers, model, "Merhaba, tek kelime yaz.", 8)
        except Exception as e:
            print("  warmup failed:", str(e)[:160], flush=True)
            rows.append({"model": model, "profile": prof, "error": str(e)[:160]})
            continue
        row = {"model": model, "profile": prof, "tasks": {}}
        for task in TASKS:
            try:
                elapsed, answer = call(headers, model, task["instruction"], args.max_tokens)
            except Exception as e:
                row["tasks"][task["id"]] = {"valid": False, "reason": str(e)[:120]}
                print(f"  {task['id']}: ERROR {str(e)[:100]}", flush=True)
                continue
            valid, reason = grade(answer, task["schema"])
            row["tasks"][task["id"]] = {"valid": valid, "reason": reason,
                                        "answer_s": round(elapsed, 1), "raw": answer.strip()[:300]}
            print(f"  {task['id']}: {'valid' if valid else 'INVALID'} ({reason[:80]}) in {elapsed:.1f}s", flush=True)
        rows.append(row)

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = {"date": date, "tasks": [t["id"] for t in TASKS], "models": rows}
    if args.out:
        with open(args.out, "w") as f:
            f.write(render(date, rows))
        print("\nwrote", args.out, flush=True)
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("wrote", args.json_out, flush=True)
    if not args.out and not args.json_out:
        print("\n" + render(date, rows))
    return 0


def render(date, rows):
    lines = ["# Format / grammar adherence", "",
             f"**Date:** {date}. Each model was asked to return a strictly valid JSON value "
             "for three schemas; the answer was validated against the schema.", ""]
    ids = [t["id"] for t in TASKS]
    lines.append("| Model | " + " | ".join(ids) + " | Valid |")
    lines.append("|---|" + "|".join(":---:" for _ in ids) + "|---:|")
    for r in rows:
        if "error" in r:
            lines.append(f"| `{r['model']}` | " + " | ".join("—" for _ in ids) + " | failed |")
            continue
        cells = ["✅" if r["tasks"][t]["valid"] else "❌" for t in ids]
        n = sum(1 for t in ids if r["tasks"][t]["valid"])
        lines.append(f"| `{r['model']}` | " + " | ".join(cells) + f" | **{n}/{len(ids)}** |")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
