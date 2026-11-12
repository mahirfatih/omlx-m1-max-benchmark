#!/usr/bin/env python3
"""Does the model know, or does it invent? A hallucination and error-risk probe.

For every language in [`../../data/languages.json`](../../data/languages.json)
the script takes one **genuine**, well-known API/feature and derives a clearly
**fabricated** twin from it (the genuine name with an `x` appended to its last
word). It then asks the model, in batches, which of the two is real.

From the answers it computes four numbers per model:

  * **accuracy** — share of names classified correctly;
  * **hallucination rate** — share of *fabricated* names the model called real;
  * **false-alarm rate** — share of *genuine* names the model called fake;
  * **Brier score** — mean squared error of the stated confidence (lower is
    better), i.e. how well the model knows what it does not know.

The two failure modes are not the same kind of mistake: a hallucination invents
an API that does not exist (dangerous when you paste model output into a build);
a false alarm is merely cautious. We report them separately, never merged.

The shape of the probe follows the long line of LLM factuality work; the
fabricated-twin method, the corpus and the scoring here are original.

Standard library only. `--selftest` needs no model and no server.

Usage:
    python3 scripts/measure/hallucination-test.py --selftest
    python3 scripts/measure/hallucination-test.py --models Qwen3.6-35B-A3B-4bit:qwen3
    python3 scripts/measure/hallucination-test.py --batch 8 --json
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data", "languages.json")
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


def load_languages(path=DATA):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["languages"]


def fake_of(real):
    """Derive the fabricated twin: append 'x' to the last word of the name."""
    m = list(re.finditer(r"[A-Za-z0-9_]+", real))
    if not m:
        return real + "x"
    last = m[-1]
    return real[:last.end()] + "x" + real[last.end():]


def probes(lang):
    """The two names for a language, in a deterministic, language-dependent order."""
    real = lang["real"]
    fake = fake_of(real)
    order = hashlib.sha256(lang["id"].encode()).digest()[0] % 2
    pair = [("real", real), ("fake", fake)]
    if order:
        pair = pair[::-1]
    return pair


def build_batches(languages, batch):
    return [languages[i:i + batch] for i in range(0, len(languages), batch)]


def batch_prompt(group):
    lines = ["For each language below I give two API or feature names. Exactly one of "
             "the two is a real, documented API/feature of that language; the other I "
             "invented. Decide for EACH name whether it is real. If you do not know the "
             "language well, say so with a low confidence instead of guessing.",
             "",
             "Return ONLY a JSON object that maps each name (exactly as written) to "
             '{"is_real": true|false, "confidence": 0.0-1.0}. No prose.', ""]
    for lang in group:
        a, b = [name for _, name in probes(lang)]
        lines.append(f'- {lang["name"]}: "{a}" and "{b}"')
    return "\n".join(lines)


def name_prompt(items):
    """A follow-up prompt listing only the names a batch left unanswered.

    A model will answer six of sixteen names and stop; asking again for the rest,
    on their own, gets them. items is a list of (language name, API name).
    """
    lines = ["For each language below, decide whether the given API or feature name "
             "is a real, documented one for that language, or invented.",
             "",
             "Return ONLY a JSON object that maps each name (exactly as written) to "
             '{"is_real": true|false, "confidence": 0.0-1.0}. No prose.', ""]
    for lang_name, name in items:
        lines.append(f'- {lang_name}: "{name}"')
    return "\n".join(lines)


def extract_json(text):
    text = text.strip()
    # Try the bare object first. Content inside the JSON can itself contain
    # backticks — the markdown probe is literally ```{r} — so a fence must never
    # be guessed at before the plain parse has been tried.
    try:
        return json.loads(text)
    except Exception:
        pass
    body = text
    # Only a reply that *opens* with a fence is fenced; strip that fence and the
    # closing one, wherever the object inside happens to put its own backticks.
    if body.startswith("```"):
        body = re.sub(r"^```[a-zA-Z]*[ \t]*\r?\n?", "", body)
        body = re.sub(r"\r?\n?```\s*$", "", body).strip()
        try:
            return json.loads(body)
        except Exception:
            pass
    start = body.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(body)):
        if body[i] == "{":
            depth += 1
        elif body[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(body[start:i + 1])
                except Exception:
                    return None
    return None


def coerce_entry(entry):
    """Return (is_real, confidence) from one model value, in any of the shapes
    a model actually emits: {"is_real": true, "confidence": 0.9}, a bare
    true/false, "real"/"fake", or 1/0.

    Confidence is None when the model did not state one — the Brier score is
    then computed only over the answers that did, instead of inventing a
    number for the rest.
    """
    if isinstance(entry, bool):
        return entry, None
    if isinstance(entry, (int, float)):
        return bool(entry), None
    if isinstance(entry, str):
        s = entry.strip().lower()
        if s in ("true", "real", "yes", "1"):
            return True, None
        if s in ("false", "fake", "no", "0"):
            return False, None
        return None, None
    if isinstance(entry, dict):
        is_real = None
        for key in ("is_real", "real", "isreal", "exists", "valid", "genuine"):
            if key in entry:
                v = entry[key]
                if isinstance(v, str):
                    v = v.strip().lower() in ("true", "real", "yes", "1")
                is_real = bool(v)
                break
        if is_real is None:
            return None, None
        conf = entry.get("confidence", entry.get("conf"))
        if conf is None:
            return is_real, None
        try:
            conf = min(1.0, max(0.0, float(conf)))
        except (TypeError, ValueError):
            conf = None
        return is_real, conf
    return None, None


def _key_variants(key):
    """The forms a model key can take when it decorates the name.

    A model will answer with the bare name ("{#eachx}") or wrap it as
    'Svelte: "{#eachx}"'. The value is the same; only the key needs unwrapping,
    so the lookup indexes every reasonable reading of a key.
    """
    out = [key]
    s = key.strip().strip('"').strip()
    out.append(s)
    if ": " in s:
        tail = s.split(": ", 1)[1].strip().strip('"').strip()
        out.append(tail)
        if tail.endswith('"'):
            out.append(tail.rstrip('"').strip())
    return [v for v in out if v]


def parse_verdicts(obj, group):
    """Map name -> (is_real, confidence, role) from a model answer object.

    Names are matched exactly, then case-insensitively, then through the
    decorations a model adds (a language prefix, surrounding quotes), because a
    model will happily re-case or wrap an identifier it otherwise got right.
    """
    out = {}
    if not isinstance(obj, dict):
        return out
    lower = {}
    for k, v in obj.items():
        if isinstance(k, str):
            for variant in _key_variants(k):
                lower.setdefault(variant.lower(), v)
    for lang in group:
        for role, name in probes(lang):
            entry = obj.get(name)
            if entry is None:
                entry = lower.get(name.lower())
            if entry is None:
                continue
            is_real, conf = coerce_entry(entry)
            if is_real is None:
                continue
            out[name] = (is_real, conf, role)
    return out


def _unescape_key(key):
    """Turn the JSON escapes a model may have half-written back into characters.

    A key comes out of the raw text as it was typed, so `\\"` and `\\\\` are the
    literal backslash sequences; decode those two and leave everything else
    (a LaTeX name's own backslash) alone.
    """
    out = []
    i = 0
    while i < len(key):
        c = key[i]
        if c == "\\" and i + 1 < len(key) and key[i + 1] in '"\\':
            out.append(key[i + 1])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def salvage_object(text):
    """Recover name -> entry pairs from a JSON object a model mangled.

    Some models emit nearly-valid JSON: an unescaped quote inside a key
    ('"Handlebars: "{{#each}}"'), a dropped closing quote, a nested value where a
    boolean belongs. `json.loads` then rejects the whole object and every good
    entry in it is lost. Each entry still has the shape `KEY: {"is_real": ...}`
    on its own, so this scans for that shape, walks back to the key and forward
    to the confidence, and rebuilds what it can. It is deliberately forgiving on
    the key (parse_verdicts unwraps decorations afterwards) and strict enough
    not to invent a verdict that is not in the text.
    """
    out = {}
    for m in re.finditer(r'"is_real"\s*:\s*(true|false)', text, re.IGNORECASE):
        pre = text[:m.start()]
        # The `{` that opens this entry's value is the last one with no brace
        # after it — not simply the previous `{`, which belongs to an earlier
        # entry and would misread every key but the first.
        mb = re.search(r"\{[^{}]*\Z", pre)
        if not mb:
            continue
        prefix = pre[:mb.start()]
        colon = prefix.rfind(":")
        if colon == -1:
            continue
        key = re.split(r"[\n,]", prefix[:colon])[-1].strip()
        key = _unescape_key(key).strip().strip('"').strip()
        if not key:
            continue
        tail = text[m.end():m.end() + 160]
        cm = re.search(r'"confiden[ce]*"\s*:\s*([0-9.]+)', tail, re.IGNORECASE)
        conf = None
        if cm:
            try:
                conf = float(cm.group(1))
            except ValueError:
                conf = None
        out[key] = {"is_real": m.group(1).lower() == "true", "confidence": conf}
    return out


def verdicts_from(text, group):
    """Map a model's raw answer to verdicts, salvaging a mangled object.

    The clean path is a valid JSON object; when that fails, the object is
    salvaged entry by entry so one bad quote does not zero a whole batch.
    """
    obj = extract_json(text)
    verdicts = parse_verdicts(obj, group) if obj is not None else {}
    if verdicts:
        return verdicts
    salvaged = salvage_object(text)
    return parse_verdicts(salvaged, group) if salvaged else {}


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
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.loads(r.read())
    choice = d["choices"][0]
    # A reasoning model writes its scratchpad to `reasoning_content` and the
    # answer to `content`; only `content` is the answer.
    content = choice["message"].get("content", "") or ""
    return time.time() - t0, content, choice.get("finish_reason", "")


def summarize(records):
    """records: list of {name, lang, role, expected, got_real, conf, answered}."""
    answered = [r for r in records if r["answered"]]
    n = len(records)
    correct = sum(1 for r in answered if r["got_real"] == r["expected"])
    fake = [r for r in answered if r["role"] == "fake"]
    real = [r for r in answered if r["role"] == "real"]
    halluc = sum(1 for r in fake if r["got_real"] is True)
    false_alarm = sum(1 for r in real if r["got_real"] is False)
    # Brier only over the answers that stated a confidence; a missing number is
    # not a zero and must not be averaged in.
    stated = [r for r in answered if isinstance(r.get("conf"), (int, float))]
    brier = (sum((r["conf"] - (1.0 if r["got_real"] == r["expected"] else 0.0)) ** 2
                 for r in stated) / len(stated)) if stated else None
    overconf_wrong = sum(1 for r in stated
                         if r["got_real"] != r["expected"] and r["conf"] >= 0.8)
    return {
        "total": n, "answered": len(answered), "correct": correct,
        "accuracy": round(correct / len(answered), 3) if answered else 0.0,
        "hallucinations": halluc, "fake_total": len(fake),
        "hallucination_rate": round(halluc / len(fake), 3) if fake else 0.0,
        "false_alarms": false_alarm, "real_total": len(real),
        "false_alarm_rate": round(false_alarm / len(real), 3) if real else 0.0,
        "brier": round(brier, 3) if brier is not None else None,
        "overconfident_wrong": overconf_wrong,
    }


def selftest():
    langs = load_languages()
    ok = True
    ids = [lang["id"] for lang in langs]
    if len(ids) != len(set(ids)):
        ok = False
        print("FAIL: duplicate language ids")
    for lang in langs:
        fake = fake_of(lang["real"])
        if fake == lang["real"] or not lang["real"]:
            ok = False
            print("FAIL: bad twin for", lang["id"])
    if fake_of("map") != "mapx" or fake_of("functools.reduce") != "functools.reducex":
        ok = False
        print("FAIL: fake_of derivation wrong:", fake_of("map"), fake_of("functools.reduce"))
    # determinism
    if probes(langs[0]) != probes(langs[0]):
        ok = False
        print("FAIL: probes not deterministic")
    # parser robustness: models emit the same verdict in several shapes, and a
    # shape the parser drops is a silent hole in every number below.
    sl = [{"id": "python", "name": "Python", "real": "functools.reduce"}]
    flat = {"functools.reduce": True, "functools.reducex": False}
    v = parse_verdicts(flat, sl)
    mixed = {"functools.reduce": "real", "functools.reducex": {"is_real": False}}
    v2 = parse_verdicts(mixed, sl)
    if (v.get("functools.reduce", (None,))[0] is not True
            or v.get("functools.reducex", (None,))[0] is not False):
        ok = False
        print("FAIL: flat boolean map not parsed:", v)
    if (v2.get("functools.reduce", (None,))[0] is not True
            or v2.get("functools.reducex", (None,))[0] is not False):
        ok = False
        print("FAIL: string/dict verdicts not parsed:", v2)
    # a model decorates the key with the language name and quotes rather than
    # returning the bare name; dropping that shape zeroes a whole batch.
    decorated = {'Python: "functools.reduce"': {"is_real": True, "confidence": 0.9},
                 'Python: "functools.reducex"': {"is_real": False, "confidence": 0.9}}
    v3 = parse_verdicts(decorated, sl)
    if (v3.get("functools.reduce", (None,))[0] is not True
            or v3.get("functools.reducex", (None,))[0] is not False):
        ok = False
        print("FAIL: decorated keys not parsed:", v3)
    if '{#eachx}' not in _key_variants('Svelte: "{#eachx}"'):
        ok = False
        print("FAIL: _key_variants:", _key_variants('Svelte: "{#eachx}"'))
    # extract_json must not mistake backticks *inside* a valid object for a code
    # fence: the markdown probe is ```{r}, and reading it as a fence drops the
    # whole batch. A bare object and a genuinely fenced one both parse.
    raw = '{"markdown": {"is_real": true}, "```{r}": {"is_real": false}}'
    if extract_json(raw) != json.loads(raw):
        ok = False
        print("FAIL: extract_json mangled backticks in content:", extract_json(raw))
    fenced = "```json\n" + raw + "\n```"
    if extract_json(fenced) != json.loads(raw):
        ok = False
        print("FAIL: extract_json missed a fenced object:", extract_json(fenced))
    # a mangled object: an unescaped quote in the key (and a second entry after
    # it), which json.loads rejects wholesale. Both verdicts must still surface.
    mangled = ('{"Python: "functools.reduce"": {"is_real": true, "confidence": 0.9},\n'
               ' "Python: "functools.reducex": {"is_real": false, "confidence": 0.4}}')
    if extract_json(mangled) is not None:
        ok = False
        print("FAIL: mangled sample was not actually invalid:", extract_json(mangled))
    v4 = verdicts_from(mangled, sl)
    if (v4.get("functools.reduce", (None,))[0] is not True
            or v4.get("functools.reducex", (None,))[0] is not False):
        ok = False
        print("FAIL: mangled object not salvaged:", v4)
    if v4.get("functools.reducex", (None, None, None))[1] != 0.4:
        ok = False
        print("FAIL: salvage lost the confidence:", v4)
    if coerce_entry({"is_real": True, "confidence": "0.8"}) != (True, 0.8):
        ok = False
        print("FAIL: confidence coercion")
    # scoring: fabricate answers
    recs = []
    for lang in langs[:3]:
        for role, name in probes(lang):
            expected = (role == "real")
            # a perfect model
            recs.append({"name": name, "lang": lang["id"], "role": role,
                         "expected": expected, "got_real": expected, "conf": 0.9, "answered": True})
    s = summarize(recs)
    if s["accuracy"] != 1.0 or s["hallucination_rate"] != 0.0:
        ok = False
        print("FAIL: perfect answers not scored perfect:", s)
    # a hallucinating model: calls every fake real
    recs2 = []
    for lang in langs[:3]:
        for role, name in probes(lang):
            expected = (role == "real")
            recs2.append({"name": name, "lang": lang["id"], "role": role,
                          "expected": expected, "got_real": True, "conf": 0.95, "answered": True})
    s2 = summarize(recs2)
    if s2["hallucination_rate"] != 1.0:
        ok = False
        print("FAIL: all-real hallucination not detected:", s2)
    else:
        print(f"ok scoring: perfect={s['accuracy']} hallucination detect={s2['hallucination_rate']}")
    print(f"{len(langs)} languages, {len(langs)*2} probes")
    print("selftest passed" if ok else "selftest FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--models", default="")
    ap.add_argument("--langs", default="", help="comma-separated language ids (default: all)")
    ap.add_argument("--batch", type=int, default=8, help="languages per request")
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--out", default="")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    langs = load_languages()
    if args.langs:
        wanted = set(args.langs.split(","))
        langs = [lang for lang in langs if lang["id"] in wanted]
        if not langs:
            raise SystemExit("no known language ids in --langs")
    batches = build_batches(langs, args.batch)

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
        print(f"MODEL: {model} | profile: {prof} | {len(langs)} languages in {len(batches)} batches", flush=True)
        unload_all(headers)
        time.sleep(3)
        try:
            call(headers, model, "Merhaba, tek kelime yaz.", 8)
        except Exception as e:
            print("  warmup failed:", str(e)[:160], flush=True)
            rows.append({"model": model, "profile": prof, "error": str(e)[:160]})
            continue
        records = []
        for bi, group in enumerate(batches, 1):
            prompt = batch_prompt(group)
            # A reasoning model can spend the whole budget on its scratchpad and
            # return either empty content or a truncated answer (finish_reason
            # "length"). Escalate the budget until the JSON parses, so a
            # non-answer is never recorded as a wrong one.
            budgets = [args.max_tokens,
                       max(args.max_tokens * 2, 4096),
                       max(args.max_tokens * 4, 8192)]
            elapsed, answer, finish, verdicts = 0.0, "", "", {}
            try:
                for budget in budgets:
                    extra, answer, finish = call(headers, model, prompt, budget)
                    elapsed += extra
                    verdicts = verdicts_from(answer, group)
                    if verdicts:
                        break
                    if finish != "length" and answer.strip():
                        # The model answered in full but nothing parsed; a larger
                        # budget will not help, so stop retrying.
                        break
            except Exception as e:
                print(f"  batch {bi}: ERROR {str(e)[:100]}", flush=True)
                for lang in group:
                    for role, name in probes(lang):
                        records.append({"name": name, "lang": lang["id"], "role": role,
                                        "expected": role == "real", "got_real": None,
                                        "conf": None, "answered": False})
                continue
            # A model can answer only some of the names and stop; ask again for
            # the ones it left out, on their own, and merge whatever comes back.
            missing = [(lang, name) for lang in group for _, name in probes(lang)
                       if name not in verdicts]
            if missing:
                sub = [lang for lang in group
                       if any(name not in verdicts for _, name in probes(lang))]
                mp = name_prompt([(lang["name"], name) for lang, name in missing])
                try:
                    extra, ans2, _ = call(headers, model, mp,
                                          max(args.max_tokens // 2, 2048))
                    elapsed += extra
                    v2 = verdicts_from(ans2, sub)
                    for k, val in v2.items():
                        verdicts.setdefault(k, val)
                except Exception:
                    pass
            for lang in group:
                for role, name in probes(lang):
                    if name in verdicts:
                        got_real, conf, _ = verdicts[name]
                        records.append({"name": name, "lang": lang["id"], "role": role,
                                        "expected": role == "real", "got_real": got_real,
                                        "conf": conf, "answered": True})
                    else:
                        records.append({"name": name, "lang": lang["id"], "role": role,
                                        "expected": role == "real", "got_real": None,
                                        "conf": None, "answered": False})
            got = sum(1 for lang in group for role, name in probes(lang) if name in verdicts)
            print(f"  batch {bi}/{len(batches)} ({len(group)} langs, {got}/{len(group) * 2} parsed, "
                  f"{finish}) in {elapsed:.1f}s", flush=True)
        s = summarize(records)
        s["model"] = model
        s["profile"] = prof
        rows.append(s)
        print(f"  -> accuracy {s['accuracy']*100:.0f}% | hallucination {s['hallucination_rate']*100:.0f}% "
              f"| false alarm {s['false_alarm_rate']*100:.0f}% | Brier {s['brier']}", flush=True)
        # keep the raw per-name records for evidence
        s["_records"] = records

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = {"date": date, "language_count": len(langs),
            "languages": [lang["id"] for lang in langs], "models": rows}
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
    ok = [r for r in data["models"] if "error" not in r]
    ok.sort(key=lambda r: (-r["hallucination_rate"], -r["accuracy"]))
    lines = ["# Hallucination & error risk", "",
             f"**Date:** {date}. {data['language_count']} languages × 2 probes "
             "(one genuine API/feature, one fabricated twin).", ""]
    lines.append("| Model | Answered | Accuracy | Hallucination (fake → “real”) | False alarm (real → “fake”) | Brier ↓ | Overconfident + wrong |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in ok:
        if not r["answered"]:
            lines.append(f"| `{r['model']}` | 0/{r['total']} | — | — | — | — | — |")
            continue
        brier = "—" if r["brier"] is None else r["brier"]
        lines.append(f"| `{r['model']}` | {r['answered']}/{r['total']} | {r['accuracy']*100:.0f}% "
                     f"({r['correct']}/{r['answered']}) | **{r['hallucination_rate']*100:.0f}%** "
                     f"({r['hallucinations']}/{r['fake_total']}) | {r['false_alarm_rate']*100:.0f}% "
                     f"({r['false_alarms']}/{r['real_total']}) | {brier} | {r['overconfident_wrong']} |")
    for r in data["models"]:
        if "error" in r:
            lines.append(f"| `{r['model']}` | — | — | — | — | — | failed |")
    lines.append("")
    lines.append("_Hallucination = a fabricated API or feature the model called real. "
                 "False alarm = a genuine one it called fake. Brier = mean squared error of the "
                 "stated confidence; 0 is perfect, 0.25 is a coin flip, lower is better, and it "
                 "is computed only over answers that stated a confidence._")
    lines.append("")
    # most-hallucinated languages, pooled across models
    from collections import Counter
    per_lang = Counter()
    tot_lang = Counter()
    for r in ok:
        for rec in r.get("_records", []):
            if rec["role"] == "fake" and rec["answered"]:
                tot_lang[rec["lang"]] += 1
                if rec["got_real"] is True:
                    per_lang[rec["lang"]] += 1
    rows = [(lang, n, tot_lang[lang]) for lang, n in
            sorted(per_lang.items(), key=lambda kv: (-kv[1], kv[0]))[:15] if n]
    if rows:
        lines.append("## Most-fooled languages (pooled over models)")
        lines.append("")
        lines.append("| Language | Models that called the fake real |")
        lines.append("|---|---:|")
        for lang, n, tot in rows:
            lines.append(f"| `{lang}` | {n}/{tot} |")
        lines.append("")
    # A run with no hallucinations skips the section above, which would leave two
    # blank lines in a row and trip the Markdown linter. Collapse any run of
    # blanks to one so the report is lint-clean whatever the result.
    out = []
    for line in lines:
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(main())
