#!/usr/bin/env python3
"""Collect the environment this benchmark was measured on.

Prints a Markdown block (machine, OS, oMLX version, API endpoint) that can be
pasted straight into a report. Standard library only, no dependencies.

Usage:
    python3 scripts/collect-system-info.py          # Markdown to stdout
    python3 scripts/collect-system-info.py --json    # JSON to stdout
"""

import argparse
import json
import os
import platform
import subprocess
import sys

BASE = "http://127.0.0.1:8000"
OMLX_CLI = os.path.expanduser("~/.omlx/bin/omlx")


def sh(cmd):
    """Run a command, return stripped stdout or None."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None


def omlx_version():
    """Read the oMLX version from the CLI, then the .app bundle."""
    out = sh([OMLX_CLI, "--version"])
    if out:
        return out.splitlines()[0].strip()
    plist = "/Applications/oMLX.app/Contents/Info.plist"
    out = sh(["/usr/libexec/PlistBuddy", "-c", "Print :CFBundleShortVersionString", plist])
    return out


def api_reachable():
    """True if the local oMLX server answers on /health."""
    import urllib.request
    try:
        with urllib.request.urlopen(BASE + "/health", timeout=4) as r:
            return json.loads(r.read()).get("status") == "healthy"
    except Exception:
        return False


def collect():
    mem_bytes = sh(["sysctl", "-n", "hw.memsize"])
    chip = sh(["sysctl", "-n", "machdep.cpu.brand_string"])
    ncpu = sh(["sysctl", "-n", "hw.ncpu"])
    return {
        "chip": chip or platform.processor() or "unknown",
        "cpu_cores": int(ncpu) if ncpu and ncpu.isdigit() else None,
        "ram_gb": int(mem_bytes) // (1024 ** 3) if mem_bytes and mem_bytes.isdigit() else None,
        "os": f"macOS {sh(['sw_vers', '-productVersion'])}",
        "os_build": sh(["sw_vers", "-buildVersion"]),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "omlx_version": omlx_version(),
        "api_endpoint": BASE + "/v1",
        "api_healthy": api_reachable(),
    }


def as_markdown(d):
    rows = [
        ("Chip", d["chip"]),
        ("CPU cores", d["cpu_cores"]),
        ("Memory", f"{d['ram_gb']} GB unified" if d["ram_gb"] else None),
        ("OS", d["os"] + (f" ({d['os_build']})" if d["os_build"] else "")),
        ("Architecture", d["arch"]),
        ("oMLX version", d["omlx_version"]),
        ("API endpoint", d["api_endpoint"]),
        ("Server reachable", "yes" if d["api_healthy"] else "no"),
    ]
    lines = ["| Item | Value |", "|---|---|"]
    for k, v in rows:
        if v is not None:
            lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args()

    info = collect()
    if args.json:
        json.dump(info, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(as_markdown(info))


if __name__ == "__main__":
    main()
