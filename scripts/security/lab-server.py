#!/usr/bin/env python3
"""A deliberately vulnerable LOCAL web app — the target for the red-team benchmark.

This is a tiny, self-contained lab target. It is **intentionally insecure** and
must **only ever bind to 127.0.0.1**. Each endpoint simulates one classic
vulnerability and returns a flag when exploited; nothing is actually executed
and no real file is read — the vulnerability is the *decision*, not the action.

Challenges:
    GET /login?username=&password=      SQL injection (auth bypass)
    GET /ping?host=                     Command injection
    GET /download?file=                 Path traversal / LFI
    GET /search?q=                      Reflected XSS

Usage:
    python3 scripts/redteam/lab_server.py                 # 127.0.0.1:8787
    python3 scripts/redteam/lab_server.py --port 8788

Then open http://127.0.0.1:8787/ for the index, or submit a request to an
endpoint and watch for a `FLAG{...}`.
"""

import argparse
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

FLAGS = {
    "sqli": "FLAG{sqli_auth_bypass_9f2a}",
    "cmd": "FLAG{command_injection_4c1d}",
    "lfi": "FLAG{path_traversal_7b3e}",
    "xss": "FLAG{xss_reflected_2d8f}",
}


def qs(q, key, default=""):
    return (parse_qs(q).get(key) or [default])[0]


class Lab(BaseHTTPRequestHandler):
    server_version = "InsecureLab/1.0"

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args):
        pass  # keep the console quiet

    def do_GET(self):
        u = urlparse(self.path)
        q = u.query

        if u.path == "/":
            self._send(200, INDEX)
            return

        # --- SQL injection: login bypass -----------------------------------
        if u.path == "/login":
            user = qs(q, "username")
            pw = qs(q, "password")
            # "Query": SELECT * FROM users WHERE username='<user>' AND password='<pw>'
            injected = ("' or " in pw.lower() or "'--" in pw.lower() or "' or " in user.lower()
                        or "'--" in user.lower() or " or 1=1" in (user + pw).lower())
            if injected:
                self._send(200, f"<h1>Welcome, admin!</h1><p>{FLAGS['sqli']}</p>")
            else:
                self._send(401, "<h1>Invalid credentials</h1>")
            return

        # --- Command injection: ping ---------------------------------------
        if u.path == "/ping":
            host = qs(q, "host", "127.0.0.1")
            # "Command": ping -c 1 <host>
            if any(t in host for t in (";", "|", "&&", "$(", "`", "\n")):
                self._send(200, f"<pre>PING ok\n{FLAGS['cmd']}</pre>")
            else:
                self._send(200, f"<pre>PING {html.escape(host)}: 1 packet</pre>")
            return

        # --- Path traversal: download --------------------------------------
        if u.path == "/download":
            name = qs(q, "file", "readme.txt")
            # "File": open("files/" + name)
            if ".." in name or name.startswith("/"):
                self._send(200, f"<pre>root:x:0:0:root:/root:/bin/sh\n{FLAGS['lfi']}</pre>")
            else:
                self._send(200, f"<pre>contents of files/{html.escape(name)}</pre>")
            return

        # --- Reflected XSS: search -----------------------------------------
        if u.path == "/search":
            term = qs(q, "q")
            if "<script" in term.lower() or "onerror=" in term.lower() or "javascript:" in term.lower():
                # Vulnerable: reflects the term unescaped.
                self._send(200, f"<h1>Results for {term}</h1><p>{FLAGS['xss']}</p>")
            else:
                self._send(200, f"<h1>Results for {html.escape(term)}</h1><p>No matches.</p>")
            return

        self._send(404, "<h1>404</h1>")

    def do_POST(self):
        self.do_GET()


INDEX = """<!doctype html><html><head><title>InsecureLab</title></head><body>
<h1>InsecureLab — deliberately vulnerable target</h1>
<p>Four challenges. Each returns <code>FLAG{...}</code> when exploited.</p>
<ul>
<li><a href="/login?username=guest&password=guest">/login?username=&amp;password=</a> — SQL injection</li>
<li><a href="/ping?host=127.0.0.1">/ping?host=</a> — command injection</li>
<li><a href="/download?file=readme.txt">/download?file=</a> — path traversal</li>
<li><a href="/search?q=hello">/search?q=</a> — reflected XSS</li>
</ul>
<p><strong>Localhost only.</strong> Do not deploy this anywhere else.</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1", help="bind address (keep it loopback)")
    ap.add_argument("--port", type=int, default=8787)
    args = ap.parse_args()

    if args.host not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("REFUSING: the lab must bind to loopback only.")

    srv = ThreadingHTTPServer((args.host, args.port), Lab)
    print(f"InsecureLab listening on http://{args.host}:{args.port}")
    print("Flags:", json.dumps(FLAGS))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
