import json
import urllib.request
import urllib.error
import time
import os
import datetime

SETTINGS = json.load(open('/Users/MahirFatih/.omlx/settings.json'))
API = SETTINGS['auth']['api_key']
BASE = "http://127.0.0.1:8000/v1"
H = {"Authorization": "Bearer " + API, "Content-Type": "application/json"}

ALL_MODELS = [
    "Qwen3-Coder-30B-A3B-Instruct-4bit",
    "Ornith-1.5-35B-A3B-MLX-4bit",
    "Qwen3.6-35B-A3B-4bit",
    "Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit",
    "gemma-4-26B-A4B-it-heretic-4bit",
    "Qwen3.8-27B-Uncensored-MLX",
]

TARGETS = [
    ("Qwen3-Coder-30B-A3B-Instruct-4bit:qwen3", "qwen3"),
    ("Ornith-1.5-35B-A3B-MLX-4bit:qwen3", "qwen3"),
    ("Qwen3.6-35B-A3B-4bit:qwen3", "qwen3"),
    ("Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit:qwen36-heretic", "qwen36-heretic"),
    ("gemma-4-26B-A4B-it-heretic-4bit:gemma4-heretic", "gemma4-heretic"),
    ("Qwen3.8-27B-Uncensored-MLX:qwen36-heretic", "qwen36-heretic"),
]

PROMPTS = {
    "EN": "Write a short technical explanation of about 120 words on how a hash table works, then give one small example.",
    "TR": "Bir hash tablosunun nasil calistigini yaklasik 120 kelimeyle teknik olarak acikla, sonra kucuk bir ornek ver.",
}


def wait_health(t=240):
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=8) as r:
                if json.loads(r.read()).get('status') == 'healthy':
                    return True
        except Exception:
            pass
        time.sleep(5)
    return False


def unload_all():
    for m in ALL_MODELS:
        req = urllib.request.Request(BASE + f"/models/{m}/unload", data=b"{}", headers=H, method="POST")
        try:
            urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            pass


def call(model, prompt, max_tokens=220):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2, "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(BASE + "/chat/completions", data=json.dumps(body).encode(), headers=H, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    elapsed = time.time() - t0
    txt = d['choices'][0]['message'].get('content', '') or ''
    u = d.get('usage') or {}
    ct = u.get('completion_tokens')
    if not ct:
        ct = max(1, len(txt) // 4)
    return elapsed, ct, txt


if not wait_health():
    raise SystemExit("server healthy degil")

results = []
for model, prof in TARGETS:
    print("=" * 70, flush=True)
    print("MODEL:", model, "| profil:", prof, flush=True)
    unload_all()
    time.sleep(3)
    # warmup (load + ilk cevap)
    try:
        load_t, _, _ = call(model, "Merhaba, tek kelime yaz.", max_tokens=8)
    except Exception as e:
        print("  WARMUP HATA:", str(e)[:180], flush=True)
        results.append({"model": model, "prof": prof, "error": str(e)[:180]})
        continue
    print(f"  yukleme/isindirma: {load_t:.1f}s", flush=True)
    row = {"model": model, "prof": prof, "load_s": load_t, "EN": [], "TR": [], "err": None}
    for lang, prompt in PROMPTS.items():
        for rep in range(2):
            try:
                elapsed, ct, txt = call(model, prompt)
                tps = ct / elapsed if elapsed > 0 else 0
                row[lang].append({"tps": tps, "tokens": ct, "sec": elapsed})
                print(f"  {lang} #{rep+1}: {ct} tok / {elapsed:.1f}s = {tps:.1f} tok/s", flush=True)
            except urllib.error.HTTPError as e:
                msg = e.read()[:160].decode('utf-8', 'ignore')
                row["err"] = msg
                print(f"  {lang} #{rep+1} HATA:", msg, flush=True)
            except Exception as e:
                row["err"] = str(e)[:160]
                print(f"  {lang} #{rep+1} HATA:", str(e)[:160], flush=True)
    results.append(row)

# ---- rapor ----
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
chip = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
ram = int(os.popen("sysctl -n hw.memsize").read().strip()) // (1024**3)
rows = []
for r in results:
    if r.get("err") and not r.get("EN") and not r.get("TR"):
        rows.append(r)
        continue
    allv = [x["tps"] for x in r.get("EN", []) + r.get("TR", [])]
    en = [x["tps"] for x in r.get("EN", [])]
    tr = [x["tps"] for x in r.get("TR", [])]
    r["avg"] = sum(allv) / len(allv) if allv else 0
    r["en_avg"] = sum(en) / len(en) if en else 0
    r["tr_avg"] = sum(tr) / len(tr) if tr else 0
    rows.append(r)

ok_rows = sorted([r for r in rows if r.get("avg")], key=lambda x: -x["avg"])
fail_rows = [r for r in rows if not r.get("avg")]

lines = []
lines.append("# oMLX Model Hız Testi (token akışı)\n")
lines.append(f"- **Tarih:** {now}")
lines.append(f"- **Donanım:** {chip}, {ram} GB RAM")
lines.append("- **Sunucu:** oMLX (`127.0.0.1:8000`)")
lines.append("- **Yöntem:** Her model tek tek yüklendi; İngilizce ve Türkçe prompt, her dil **2 kez** çalıştırıldı. Hız = `completion_tokens / geçen süre` (tok/s). Önce model boşaltıldı, sonra ısındırma + ölçüm.")
lines.append("- **Ayarlar:** ctx 32768, temp 0.2, max_tokens 220, thinking kapalı, KV 4-bit\n")
lines.append("## Sıralama (en hızlıdan en yavaşa)\n")
lines.append("| # | Model | Profil | EN tok/s | TR tok/s | Ortalama tok/s | Yükleme (s) |")
lines.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(ok_rows, 1):
    short = r["model"].split(":")[0]
    lines.append(f"| {i} | `{short}` | `{r['prof']}` | {r['en_avg']:.1f} | {r['tr_avg']:.1f} | **{r['avg']:.1f}** | {r['load_s']:.1f} |")
if fail_rows:
    lines.append("\n## Başarısız / ölçülemeyen\n")
    for r in fail_rows:
        lines.append(f"- `{r['model']}` → {r.get('err') or 'ölçüm yok'}")
lines.append("\n## Notlar\n")
lines.append("- Yükleme süresi ilk isteğe dahildir (model RAM'e alınır); tok/s ölçümü ısınmış modelle yapılmıştır.")
lines.append("- Değerler bu makinede, bu promptlarla alınmıştır; farklı prompt/uzunlukta değişebilir.")
lines.append("- Profiller: `qwen3` (kod, max_tokens 4096), `qwen36-heretic` (2048), `gemma4-heretic` (2048).")
md = "\n".join(lines) + "\n"

desktop = os.path.expanduser("~/Desktop")
outdir = desktop if os.path.isdir(desktop) else os.path.expanduser("~")
path = os.path.join(outdir, "omlx-benchmark-" + datetime.datetime.now().strftime("%Y%m%d-%H%M") + ".md")
with open(path, "w") as f:
    f.write(md)
print("\n\n" + md)
print("\nRAPOR KAYDEDILDI:", path, flush=True)
