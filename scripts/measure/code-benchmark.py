#!/usr/bin/env python3
"""Score a model's code by running it, not just by parsing it.

[`code-matrix-test.py`](code-matrix-test.py) checks that generated code
*compiles*. This script checks that it *passes cases*: the model is asked for a
solution to a problem in [`../../problems/`](../../problems/), the code block is
extracted, executed against hidden test cases under a timeout, and scored on how
many pass.

Standard library only. `--selftest` needs no server and no model and proves the
harness against the reference solutions; the full run needs a loaded model.

Usage:
    python3 scripts/measure/code-benchmark.py --selftest
    python3 scripts/measure/code-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
    python3 scripts/measure/code-benchmark.py --problems p01-two-sum --json
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PROBLEMS = os.path.join(ROOT, "problems")
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

# The runner executes the model's code in a separate process and writes the
# verdict to a file, so a solution that prints to stdout cannot corrupt it.
RUNNER = r'''
import json, sys, math

sol_path, cases_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

def write(obj):
    json.dump(obj, open(out_path, "w"))

spec = json.load(open(cases_path))
ns = {"__name__": "__solution__"}
load_error = None
try:
    with open(sol_path) as f:
        code = f.read()
    exec(compile(code, sol_path, "exec"), ns)
except Exception as e:
    # A model's own top-level demo or an undefined __name__ must not sink an
    # otherwise-defined solution: remember the error and look for the function.
    load_error = (str(e) or e.__class__.__name__)[:160]

fn = ns.get(spec["function"])
if not callable(fn):
    reason = "function %r not defined" % spec["function"]
    if load_error:
        reason += " (top-level error: %s)" % load_error
    write({"error": reason})
    sys.exit(0)

unordered = spec.get("unordered", False)

def same(got, exp):
    if isinstance(exp, float) or isinstance(got, float):
        try:
            return abs(float(got) - float(exp)) < 1e-6
        except (TypeError, ValueError):
            return False
    if unordered and isinstance(got, (list, tuple)) and isinstance(exp, (list, tuple)):
        try:
            return sorted(got) == sorted(exp)
        except TypeError:
            return list(got) == list(exp)
    return got == exp

results = []
for c in spec["cases"]:
    try:
        got = fn(*c["args"])
        results.append({"name": c["name"], "ok": bool(same(got, c["expected"])),
                        "got": repr(got)[:80]})
    except Exception as e:
        results.append({"name": c["name"], "ok": False, "error": (str(e) or e.__class__.__name__)[:160]})

json.dump(results, open(out_path, "w"))
'''


def problem_ids():
    if not os.path.isdir(PROBLEMS):
        return []
    return sorted(d for d in os.listdir(PROBLEMS)
                  if os.path.isfile(os.path.join(PROBLEMS, d, "tests", "test-cases.json")))


def load_statement(pid):
    return open(os.path.join(PROBLEMS, pid, "problem.md"), encoding="utf-8").read()


def case_path(pid):
    return os.path.join(PROBLEMS, pid, "tests", "test-cases.json")


def reference_path(pid):
    return os.path.join(PROBLEMS, pid, "solutions", "solution.py")


def extract_code(text):
    m = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip() + "\n"


def run_solution(pid, code, timeout=20):
    """Execute `code` against the problem's cases. Returns (results, error)."""
    with tempfile.TemporaryDirectory(prefix="codebench-") as tmp:
        sol = os.path.join(tmp, "solution.py")
        runner = os.path.join(tmp, "runner.py")
        out = os.path.join(tmp, "result.json")
        with open(sol, "w") as f:
            f.write(code)
        with open(runner, "w") as f:
            f.write(RUNNER)
        try:
            subprocess.run([sys.executable, "-I", runner, sol, case_path(pid), out],
                           cwd=tmp, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return [], f"timeout after {timeout}s"
        if not os.path.exists(out):
            return [], "no result (the solution crashed or hung before writing)"
        try:
            data = json.load(open(out))
        except Exception as e:
            return [], f"unreadable result: {e}"
        if isinstance(data, dict) and "error" in data:
            return [], data["error"]
        return data, None


def score(results):
    total = len(results)
    passed = sum(1 for r in results if r.get("ok"))
    return passed, total, (passed / total if total else 0.0)


def selftest():
    ids = problem_ids()
    if not ids:
        print("no problems found under problems/", file=sys.stderr)
        return 2
    ok = True
    for pid in ids:
        code = open(reference_path(pid)).read()
        results, error = run_solution(pid, code)
        if error:
            print(f"FAIL {pid}: {error}")
            ok = False
            continue
        passed, total, _ = score(results)
        flag = "ok" if passed == total else "FAIL"
        if passed != total:
            ok = False
            failures = [r["name"] for r in results if not r.get("ok")]
            print(f"{flag} {pid}: {passed}/{total} (failed: {', '.join(failures)})")
        else:
            print(f"{flag} {pid}: {passed}/{total}")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


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
            "temperature": 0.1, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.loads(r.read())
    return time.time() - t0, d["choices"][0]["message"].get("content", "") or ""


def benchmark(args):
    ids = args.problems.split(",") if args.problems else problem_ids()
    for pid in ids:
        if pid not in problem_ids():
            raise SystemExit(f"unknown problem: {pid}")
    targets = [tuple(x.split(":", 1)) if ":" in x else (x, "qwen3")
               for x in args.models.split(",") if x]
    if not wait_health():
        raise SystemExit("oMLX server is not healthy")

    headers = {"Authorization": "Bearer " + load_key(), "Content-Type": "application/json"}
    rows = []
    for model, profile in targets:
        print("=" * 70, flush=True)
        print(f"MODEL: {model} | profile: {profile}", flush=True)
        unload_all(headers)
        time.sleep(3)
        try:
            call(headers, model, "Merhaba, tek kelime yaz.", 8)
        except Exception as e:
            print("  warmup failed:", str(e)[:160], flush=True)
            continue
        row = {"model": model, "profile": profile, "problems": {}}
        for pid in ids:
            prompt = ("Solve this coding problem in Python. Return ONLY a fenced "
                      "```python code block, no explanation.\n\n" + load_statement(pid))
            try:
                elapsed, text = call(headers, model, prompt, args.max_tokens)
            except Exception as e:
                row["problems"][pid] = {"error": str(e)[:160]}
                print(f"  {pid}: ERROR {str(e)[:120]}", flush=True)
                continue
            results, error = run_solution(pid, extract_code(text))
            if error:
                row["problems"][pid] = {"error": error, "answer_s": round(elapsed, 1)}
                print(f"  {pid}: {error}", flush=True)
                continue
            passed, total, frac = score(results)
            failed = [r["name"] for r in results if not r.get("ok")]
            row["problems"][pid] = {"passed": passed, "total": total, "score": round(frac, 3),
                                    "failed": failed, "answer_s": round(elapsed, 1),
                                    "code": extract_code(text)[:800]}
            print(f"  {pid}: {passed}/{total} in {elapsed:.1f}s", flush=True)
        rows.append(row)

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = {"date": date, "problems": ids, "models": rows}
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n" if args.json else render(date, ids, rows)
    if args.out:
        open(args.out, "w").write(text)
        print("\nwrote", args.out, flush=True)
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("wrote", args.json_out, flush=True)
    if not args.out and not args.json_out:
        print("\n" + text)


def render(date, ids, rows):
    lines = ["# Coding benchmark — does the code pass?", ""]
    lines.append(f"**Date:** {date}. Each model was asked for a Python solution to "
                 f"{len(ids)} problem(s); the code was run against hidden cases and scored.")
    lines.append("")
    header = "| Model | " + " | ".join(p.split("-")[0] for p in ids) + " | Total |"
    lines.append(header)
    lines.append("|---|" + "|".join(":---:" for _ in ids) + "|---:|")
    for r in rows:
        cells = []
        for pid in ids:
            d = r["problems"].get(pid, {})
            if "error" in d:
                cells.append("❌")
            else:
                cells.append(f"{d['passed']}/{d['total']}")
        passed = sum(d.get("passed", 0) for d in r["problems"].values())
        total = sum(d.get("total", 0) for d in r["problems"].values())
        lines.append(f"| `{r['model']}` | " + " | ".join(cells) + f" | **{passed}/{total}** |")
    lines.append("")
    for r in rows:
        lines.append(f"## `{r['model']}`")
        lines.append("")
        for pid in ids:
            d = r["problems"].get(pid, {})
            if "error" in d:
                lines.append(f"- **{pid}:** {d['error']}")
            else:
                miss = ("; failed: " + ", ".join(d["failed"])) if d["failed"] else ""
                lines.append(f"- **{pid}:** {d['passed']}/{d['total']} in {d['answer_s']}s{miss}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the reference solutions (no model, no server)")
    ap.add_argument("--models", default="", help="comma-separated id:profile list")
    ap.add_argument("--problems", default="", help="comma-separated problem ids (default: all)")
    ap.add_argument("--max-tokens", type=int, default=900)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--out", default="", help="write the report here")
    ap.add_argument("--json-out", default="", help="also write the machine-readable data here")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.models:
        ap.error("give --selftest or --models")
    benchmark(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
