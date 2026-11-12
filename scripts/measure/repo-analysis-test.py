#!/usr/bin/env python3
"""Ask every model to analyse a real repository, and measure how it answers.

The task is deliberately a *scan*, not a chat: the script builds a digest of a
target repository (its file tree, README, and the statistics inside its data
file), hands the same digest to each model, and asks for an analysis. It then
measures

  * how long the model took to answer (`answer_s`),
  * its decode speed on that answer (`tok/s`),
  * how many of the repository's own documented facts it recovered
    (`facts recovered` — a recall proxy for "did it actually read the digest").

The default target is [`net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog),
the repository this project mirrors. Point `--repo` at any checkout.

Standard library only. Needs a running oMLX server and a loaded model.

Usage:
    python3 scripts/measure/repo-analysis-test.py
    python3 scripts/measure/repo-analysis-test.py --repo ~/Sites/net-traffic-control-catalog
    python3 scripts/measure/repo-analysis-test.py --models Qwen3.6-35B-A3B-4bit:qwen3 --json
"""

import argparse
import collections
import datetime
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SETTINGS = os.path.expanduser("~/.omlx/settings.json")
BASE = "http://127.0.0.1:8000/v1"

CATALOG_URL = "https://github.com/mahirfatih/net-traffic-control-catalog"
DEFAULT_REPO = os.path.expanduser("~/Sites/net-traffic-control-catalog")

ALL_MODELS = [
    "Qwen3-Coder-30B-A3B-Instruct-4bit",
    "Ornith-1.5-35B-A3B-MLX-4bit",
    "Qwen3.6-35B-A3B-4bit",
    "Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit",
    "gemma-4-26B-A4B-it-heretic-4bit",
    "Qwen3.8-27B-Uncensored-MLX",
]

# model id : profile, in the README order (fastest first).
DEFAULT_TARGETS = [
    ("Qwen3.6-35B-A3B-4bit", "qwen3"),
    ("Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit", "qwen36-heretic"),
    ("Ornith-1.5-35B-A3B-MLX-4bit", "qwen3"),
    ("gemma-4-26B-A4B-it-heretic-4bit", "gemma4-heretic"),
    ("Qwen3-Coder-30B-A3B-Instruct-4bit", "qwen3"),
    ("Qwen3.8-27B-Uncensored-MLX", "qwen36-heretic"),
]

TASK = (
    "You are a senior engineer doing a quick triage of a repository you have never "
    "seen. Below is a digest: its file tree, its README, and statistics computed from "
    "its data file. Read it and answer in under 250 words:\n"
    "1. What is this project, in one sentence?\n"
    "2. How is it structured (the parts that matter)?\n"
    "3. One concrete data-quality or design risk you can see in the numbers.\n"
    "4. A one-line verdict: is it well-maintained?\n"
    "Cite the specific numbers you used."
)


def facts(target):
    """The repository's own documented facts — what a real scan should recover."""
    return [
        str(target["hosts"]),
        str(target["categories"]),
        str(target["services"]),
        "catalog.json",
        "seeds",
        "manifest",
        "CC0",
        "scripts",
        "docs",
        "test",
        "finance",
        "domain",
    ]


def build_digest(target):
    if not os.path.isdir(target["path"]):
        raise SystemExit(f"target repo not found: {target['path']}")

    def files(sub):
        out = []
        base = os.path.join(target["path"], sub)
        for root, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".venv", "node_modules")]
            for n in names:
                out.append(os.path.relpath(os.path.join(root, n), target["path"]))
        return out

    tree = files(".")
    top = collections.Counter(p.split(os.sep)[0] for p in tree)

    readme_path = os.path.join(target["path"], "README.md")
    readme = ""
    if os.path.exists(readme_path):
        readme = open(readme_path, encoding="utf-8", errors="ignore").read()[:1600]

    lines = []
    lines.append(f"REPOSITORY: {target['name']}")
    lines.append(f"URL: {target['url']}")
    lines.append(f"Tracked files: {len(tree)}")
    lines.append("")
    lines.append("TOP-LEVEL LAYOUT (path: file count):")
    for name, count in sorted(top.items(), key=lambda kv: -kv[1]):
        lines.append(f"  {name}/: {count}")
    lines.append("")
    lines.append("DATA FILE (catalog.json):")
    lines.append(f"  version: {target['version']}")
    lines.append(f"  generated: {target['generated']}")
    lines.append(f"  hosts (categories): {target['hosts']}")
    lines.append(f"  distinct categories: {target['categories']}")
    lines.append(f"  services: {target['services']}")
    lines.append(f"  file size: {target['bytes']} bytes")
    lines.append("  top categories by host count:")
    for cat, n in target["top_categories"]:
        lines.append(f"    {cat}: {n}")
    lines.append("")
    lines.append("NOTABLE SUBTREES:")
    lines.append("  seeds/: categories.json, services.json, public-suffix-exceptions.json")
    lines.append("  scripts/: analysis/, catalog/, checks/, release/, sources/")
    lines.append("  docs/: overview/, guides/, reference/, analysis/, architecture/, security/, testing/")
    lines.append("  test/: test.sh (offline gate), .github/workflows/{ci,release}.yml")
    lines.append("")
    lines.append("README (excerpt):")
    lines.append(readme)
    return "\n".join(lines), tree


def inspect_repo(path):
    cat_path = os.path.join(path, "catalog.json")
    d = json.load(open(cat_path))
    cats = d["categories"]
    counter = collections.Counter(cats.values())
    services = d["services"]
    return {
        "name": os.path.basename(path),
        "path": path,
        "url": CATALOG_URL,
        "version": d.get("version"),
        "generated": d.get("generated"),
        "hosts": len(cats),
        "categories": len(counter),
        "services": len(services),
        "bytes": os.path.getsize(cat_path),
        "top_categories": counter.most_common(12),
    }


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
            "temperature": 0.2, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.loads(r.read())
    elapsed = time.time() - t0
    txt = d["choices"][0]["message"].get("content", "") or ""
    usage = d.get("usage") or {}
    tokens = usage.get("completion_tokens") or max(1, len(txt) // 4)
    return elapsed, tokens, txt


def score_answer(txt, expected):
    low = txt.lower()
    found = [f for f in expected if f.lower() in low]
    missing = [f for f in expected if f.lower() not in low]
    return found, missing, (len(found) / len(expected) if expected else 0.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=DEFAULT_REPO, help="path to the target repository")
    ap.add_argument("--models", default="", help="comma-separated id:profile list (default: all six)")
    ap.add_argument("--max-tokens", type=int, default=700)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--out", default="", help="write the report to this path")
    ap.add_argument("--json-out", default="", help="also write the machine-readable data here")
    args = ap.parse_args()

    target = inspect_repo(args.repo)
    digest, _ = build_digest(target)
    expected = facts(target)
    prompt = TASK + "\n\n" + digest

    targets = DEFAULT_TARGETS
    if args.models:
        targets = [tuple(x.split(":", 1)) if ":" in x else (x, "qwen3")
                   for x in args.models.split(",") if x]

    if not wait_health():
        raise SystemExit("oMLX server is not healthy")

    headers = {"Authorization": "Bearer " + load_key(), "Content-Type": "application/json"}
    results = []
    for model, prof in targets:
        print("=" * 70, flush=True)
        print(f"MODEL: {model} | profile: {prof}", flush=True)
        unload_all(headers)
        time.sleep(3)
        try:
            load_s, _, _ = call(headers, model, "Merhaba, tek kelime yaz.", 8)
        except Exception as e:
            print("  warmup failed:", str(e)[:160], flush=True)
            results.append({"model": model, "profile": prof, "error": str(e)[:160]})
            continue
        try:
            answer_s, tokens, txt = call(headers, model, prompt, args.max_tokens)
        except urllib.error.HTTPError as e:
            msg = e.read()[:160].decode("utf-8", "ignore")
            results.append({"model": model, "profile": prof, "error": msg})
            print("  ERROR:", msg, flush=True)
            continue
        except Exception as e:
            results.append({"model": model, "profile": prof, "error": str(e)[:160]})
            print("  ERROR:", str(e)[:160], flush=True)
            continue
        found, missing, coverage = score_answer(txt, expected)
        tps = tokens / answer_s if answer_s else 0.0
        results.append({
            "model": model, "profile": prof, "load_s": round(load_s, 1),
            "answer_s": round(answer_s, 2), "tokens": tokens, "tps": round(tps, 1),
            "recovered": len(found), "of": len(expected), "coverage": round(coverage, 3),
            "missing": missing, "excerpt": txt.strip()[:600],
        })
        print(f"  load {load_s:.1f}s | answer {answer_s:.1f}s | {tokens} tok | {tps:.1f} tok/s "
              f"| facts {len(found)}/{len(expected)}", flush=True)

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = {"date": date, "target": {k: target[k] for k in
            ("name", "url", "version", "generated", "hosts", "categories", "services", "bytes")},
            "expected_facts": expected, "models": results}
    if args.json:
        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    else:
        text = render(date, target, expected, results)

    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print("\nwrote", args.out, flush=True)
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("wrote", args.json_out, flush=True)
    if not args.out and not args.json_out:
        print("\n" + text)


def render(date, target, expected, results):
    ok = [r for r in results if "error" not in r]
    ok.sort(key=lambda r: (-r["coverage"], r["answer_s"]))
    lines = [f"# Repository analysis — `{target['name']}`", ""]
    lines.append(f"**Target:** [{target['url']}]({target['url']}) — "
                 f"catalog.json v{target['version']}, {target['hosts']} hosts, "
                 f"{target['categories']} categories, {target['services']} services, "
                 f"{target['bytes']} bytes.")
    lines.append("")
    lines.append(f"**Date:** {date}. Each model was given the same digest (file tree, README, "
                 "data statistics) and the same analysis task, then measured.")
    lines.append("")
    lines.append("| Model | Profile | Answer (s) | Tokens | tok/s | Facts recovered | Score |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for r in ok:
        short = r["model"].replace("-MLX-4bit", "").replace("-4bit", "")
        lines.append(f"| `{short}` | `{r['profile']}` | {r['answer_s']:.1f} | {r['tokens']} | "
                     f"{r['tps']:.1f} | {r['recovered']}/{r['of']} | **{r['coverage']*100:.0f}%** |")
    for r in results:
        if "error" in r:
            lines.append(f"| `{r['model']}` | `{r['profile']}` | — | — | — | — | failed |")
    lines.append("")
    lines.append("_Facts recovered = how many of the repository's own documented facts "
                 f"(`{', '.join(expected)}`) the answer cites. It is a recall proxy for "
                 "whether the model read the digest rather than pattern-matched._")
    lines.append("")
    for r in ok:
        lines.append(f"## `{r['model']}`")
        lines.append("")
        lines.append(f"- **Answer:** {r['answer_s']:.1f}s, {r['tokens']} tokens, {r['tps']:.1f} tok/s")
        lines.append(f"- **Recovered {r['recovered']}/{r['of']}**" +
                     (f"; missed: {', '.join(r['missing'])}" if r["missing"] else " — all facts cited"))
        lines.append("")
        lines.append("> " + r["excerpt"].replace("\n", "\n> "))
        lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
