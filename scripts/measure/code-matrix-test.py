import json
import urllib.request
import urllib.error
import time
import subprocess
import tempfile
import os
import re
import sys

API = json.load(open('/Users/MahirFatih/.omlx/settings.json'))['auth']['api_key']
BASE = "http://127.0.0.1:8000/v1"
H = {"Authorization": "Bearer " + API, "Content-Type": "application/json"}
ALL = ["Qwen3-Coder-30B-A3B-Instruct-4bit", "Ornith-1.5-35B-A3B-MLX-4bit",
       "Qwen3.6-35B-A3B-4bit", "Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit",
       "gemma-4-26B-A4B-it-heretic-4bit", "Qwen3.8-27B-Uncensored-MLX"]


def wait_health(t=240):
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=8) as r:
                if json.loads(r.read()).get('status') == 'healthy':
                    return True
        except Exception:
            pass
        time.sleep(6)
    return False


def unload_all():
    for m in ALL:
        req = urllib.request.Request(BASE + f"/models/{m}/unload", data=b"{}", headers=H, method="POST")
        try:
            urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            pass


def gen(model, prompt, max_tokens=400):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(), headers=H, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    return d['choices'][0]['message'].get('content', '') or ''


def extract_code(text):
    m = re.search(r"```[a-zA-Z0-9]*\s*\n(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    return text.strip()


def validate(lang, code):
    # returns (ok, detail)
    if not code:
        return False, "bos cikti"
    try:
        if lang == 'python':
            compile(code, '<gen>', 'exec')
            return True, "python compile OK"
        if lang == 'nodejs':
            with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
                f.write(code)
                p = f.name
            r = subprocess.run(['node', '--check', p], capture_output=True, text=True, timeout=30)
            os.unlink(p)
            return (r.returncode == 0), ("node --check OK" if r.returncode == 0 else r.stderr.strip()[:120])
        if lang == 'bash':
            r = subprocess.run(['bash', '-n'], input=code, capture_output=True, text=True, timeout=30)
            return (r.returncode == 0), ("bash -n OK" if r.returncode == 0 else r.stderr.strip()[:120])
        if lang == 'swift':
            with tempfile.NamedTemporaryFile('w', suffix='.swift', delete=False) as f:
                f.write(code)
                p = f.name
            r = subprocess.run(['swiftc', '-parse', p], capture_output=True, text=True, timeout=60)
            os.unlink(p)
            return (r.returncode == 0), ("swiftc -parse OK" if r.returncode == 0 else r.stderr.strip()[:120])
    except FileNotFoundError:
        return None, "runtime yok"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)[:120]
    return False, "bilinmeyen"


TASKS = {
    'python': "Sadece Python kodu yaz (aciklama yok). Bir listenin en buyuk 3 elemanini donduren fonksiyon `top3(lst)`.",
    'nodejs': "Sadece JavaScript (Node.js) kodu yaz (aciklama yok). Bir string'i ters ceviren `reverseStr(s)` fonksiyonu.",
    'bash': "Sadece Bash script yaz (aciklama yok). Bir dizindeki .log dosyalarini sayan script.",
    'swift': "Sadece Swift kodu yaz (aciklama yok). Bir Int dizisindeki cift sayilari donduren `evens(_:)` fonksiyonu.",
}

MODELS = [
    ("Qwen3-Coder-30B-A3B-Instruct-4bit:qwen3", "qwen3"),
    ("Qwen3.6-35B-A3B-4bit:qwen3", "qwen3"),
    ("Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit:qwen36-heretic", "qwen36-heretic"),
    ("gemma-4-26B-A4B-it-heretic-4bit:gemma4-heretic", "gemma4-heretic"),
]

if not wait_health():
    print("SERVER healthy DEGIL")
    sys.exit(1)
print("SERVER healthy\n", flush=True)

for model, prof in MODELS:
    print("=" * 70)
    print("MODEL:", model, "| profil:", prof, flush=True)
    unload_all()
    time.sleep(4)
    for lang, prompt in TASKS.items():
        t0 = time.time()
        try:
            out = gen(model, prompt)
            code = extract_code(out)
            ok, detail = validate(lang, code)
            mark = "OK" if ok else ("YOK" if ok is None else "FAIL")
            print(f"  [{lang:6}] {mark:4} | {detail} | {time.time()-t0:5.1f}s", flush=True)
        except urllib.error.HTTPError as e:
            print(f"  [{lang:6}] HATA | {e.read()[:140].decode('utf-8','ignore')}", flush=True)
        except Exception as e:
            print(f"  [{lang:6}] HATA | {str(e)[:140]}", flush=True)
print("\nBITTI", flush=True)
