#!/usr/bin/env bash
#
# Every check this repository has that needs no model and no network.
#
#     ./test/test.sh              # everything
#     ./test/test.sh --fast       # skip the full py_compile sweep
#
# The suite is deliberately plain: Python 3 standard library only, no install
# step. A benchmark repository's checks should be runnable by anybody who opened
# a pull request.

set -euo pipefail

cd "$(dirname "$0")/.."

FAST=0
for arg in "$@"; do
    case "$arg" in
        --fast) FAST=1 ;;
        -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

step "1. Python syntax"
if [ "$FAST" -eq 0 ]; then
    python3 -m py_compile scripts/*/*.py
fi
python3 - <<'PY'
import ast, pathlib, sys
bad = 0
for p in pathlib.Path("scripts").rglob("*.py"):
    try:
        ast.parse(p.read_text())
    except SyntaxError as e:
        print(f"{p}: {e}")
        bad += 1
sys.exit(1 if bad else 0)
PY

step "2. Naming — source and data files are kebab-case"
python3 scripts/checks/check-naming.py

step "3. Manifest — matches the report and results"
python3 scripts/release/build-manifest.py --check

step "4. Docs — links resolve, no secrets committed"
python3 scripts/checks/check-docs-fresh.py

step "5. Analysis — renders from the committed data"
python3 scripts/analysis/analyze-results.py > /dev/null

step "6. Environment — reads the machine without a server"
python3 scripts/measure/collect-system-info.py > /dev/null
python3 scripts/measure/model-sizes.py > /dev/null

step "7. Security rails — the lab refuses a non-loopback bind"
python3 - <<'PY'
import sys
src = open("scripts/security/lab-server.py").read()
assert 'args.host not in ("127.0.0.1", "localhost", "::1")' in src, "loopback guard removed"
src2 = open("scripts/security/security-probe.py").read()
assert "not is_loopback(host) and not args.allow_remote" in src2, "remote guard removed"
print("rails present")
PY

step "8. Reference project — linked, and the analysis is present"
python3 - <<'PY'
import json, pathlib, sys

URL = "https://github.com/mahirfatih/net-traffic-control-catalog"
script = pathlib.Path("scripts/measure/repo-analysis-test.py")
assert script.exists(), "repo-analysis-test.py is missing"

doc = pathlib.Path("docs/analysis/net-traffic-control-catalog.md")
assert doc.exists(), "the reference analysis document is missing"
assert URL in doc.read_text(), "the reference project is not linked in the analysis doc"

data = json.loads(pathlib.Path("reference/repo-analysis.json").read_text())
assert data["target"]["url"] == URL, "analysis JSON points at the wrong project"
assert data["models"], "analysis JSON has no model results"
assert all("coverage" in m for m in data["models"] if "error" not in m), "a result is missing its score"
print(f"reference linked; {len(data['models'])} model results, target {data['target']['name']}")
PY

step "9. Coding benchmark — the reference solutions pass every case"
python3 scripts/measure/code-benchmark.py --selftest

step "10. Format adherence — the JSON validator accepts good and rejects bad"
python3 scripts/measure/grammar-test.py --selftest

step "11. Long-context memory — the needles are planted and the scorer agrees"
python3 scripts/measure/context-memory-test.py --selftest

step "12. External benchmarks are documented with their licences"
python3 - <<'PY'
import pathlib
doc = pathlib.Path("docs/analysis/external-benchmarks.md")
assert doc.exists(), "docs/analysis/external-benchmarks.md is missing"
text = doc.read_text()
for url in (
    "https://github.com/liohunter1/llm-coding-benchmark",
    "https://github.com/akitaonrails/llm-coding-benchmark",
    "https://github.com/egavrin/deal-llm-grammar-benchmark",
    "https://github.com/HUST-AI-HYZ/MemoryAgentBench",
    "https://github.com/openai/frontier-evals",
):
    assert url in text, f"external benchmark not credited: {url}"
print("external benchmarks documented")
PY

step "13. Hallucination probe — the twin is fake and the scorer discriminates"
python3 scripts/measure/hallucination-test.py --selftest

step "14. Language corpus — every listed language has a genuine API and a twin"
python3 - <<'PY'
import json, pathlib, sys
sys.path.insert(0, "scripts/measure")
import importlib.util
spec = importlib.util.spec_from_file_location("ht", "scripts/measure/hallucination-test.py")
ht = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ht)
langs = ht.load_languages()
assert len(langs) >= 100, f"expected >= 100 languages, found {len(langs)}"
for lang in langs:
    assert lang["real"], f"{lang['id']} has no genuine API"
    assert ht.fake_of(lang["real"]) != lang["real"], f"{lang['id']} twin equals the real name"
doc = pathlib.Path("docs/reference/LANGUAGES.md")
assert doc.exists(), "docs/reference/LANGUAGES.md is missing"
print(f"{len(langs)} languages, twins derived, corpus documented")
PY

step "15. Model licences — documented, and the conditional ones are flagged"
python3 - <<'PY'
import pathlib
doc = pathlib.Path("docs/reference/LICENSES.md")
assert doc.exists(), "docs/reference/LICENSES.md is missing"
text = doc.read_text()
# The point of the file: download is not a licence, and two models are not open.
for needle in ("FLUX Kommunity License", "not declared", "Apache-2.0"):
    assert needle in text, f"licences doc no longer mentions: {needle}"
models = pathlib.Path("docs/reference/MODELS.md").read_text()
assert "LICENSES.md" in models, "MODELS.md does not point at the licence reading"
print("licences documented; conditional and undeclared models flagged")
PY

printf '\n\033[1;32mAll checks passed.\033[0m\n'
step "16. Mermaid — every diagram is closed and renders"
python3 - <<'PY'
import pathlib, re, sys
blocks = []
for p in pathlib.Path(".").rglob("*.md"):
    if ".git" in p.parts:
        continue
    text = p.read_text()
    for m in re.finditer(r"```mermaid\n(.*?)```", text, re.S):
        blocks.append((str(p), m.group(1)))
if not blocks:
    print("no mermaid blocks found")
    sys.exit(0)
bad = 0
for path, body in blocks:
    if not body.strip():
        print(f"{path}: empty mermaid block")
        bad += 1
        continue
    depth = 0
    for line in body.splitlines():
        t = line.strip()
        if t.startswith("subgraph"):
            depth += 1
        elif t == "end":
            depth -= 1
            if depth < 0:
                # 'end' also closes alt/opt/loop/par in sequence diagrams and
                # terminal states in state diagrams; treat those as no-ops here.
                depth = 0
    if depth != 0:
        print(f"{path}: unbalanced subgraph/end (depth {depth})")
        bad += 1
print(f"{len(blocks)} mermaid blocks checked for structure")
sys.exit(1 if bad else 0)
PY
CHROME=""
for c in /Applications/Chromium.app/Contents/MacOS/Chromium \
         /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome; do
    if [ -x "$c" ]; then CHROME="$c"; break; fi
done
if command -v mmdc >/dev/null 2>&1 && [ -n "$CHROME" ]; then
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "$tmpdir"' EXIT
    i=0
    fail=0
    for f in $(grep -rl '```mermaid' --include='*.md' . | grep -v .git); do
        python3 - "$f" "$tmpdir" <<'PY'
import re, pathlib, sys
src, outdir = sys.argv[1], sys.argv[2]
text = pathlib.Path(src).read_text()
for idx, m in enumerate(re.finditer(r"```mermaid\n(.*?)```", text, re.S)):
    pathlib.Path(f"{outdir}/{idx}.mmd").write_text(m.group(1))
PY
        for mmd in "$tmpdir"/*.mmd; do
            [ -e "$mmd" ] || continue
            i=$((i+1))
            if ! PUPPETEER_EXECUTABLE_PATH="$CHROME" mmdc -i "$mmd" -o "$tmpdir/out-$i.svg" >/dev/null 2>&1; then
                echo "render failed: $f (block $i)"
                fail=1
            fi
        done
    done
    rm -rf "$tmpdir"
    trap - EXIT
    if [ "$fail" -ne 0 ]; then
        echo "mermaid render FAILED"
        exit 1
    fi
    echo "all mermaid blocks render with mmdc"
else
    echo "mmdc or a browser not found; structure check only"
fi
