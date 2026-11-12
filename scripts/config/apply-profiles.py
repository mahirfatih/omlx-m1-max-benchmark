#!/usr/bin/env python3
"""Apply (or diff) the oMLX profiles recorded in this repository.

The committed [`profiles/omlx-profiles.json`](../profiles/omlx-profiles.json) is a
**sanitized snapshot** of a working oMLX configuration: three global profiles
(`qwen3`, `qwen36-heretic`, `gemma4-heretic`), the model → profile mapping, and
the per-model resolved profile settings. This tool reconciles that snapshot with
the live files under ``~/.omlx/``.

It is **dry-run by default**: with no flags it prints what would change and
writes nothing. Pass ``--apply`` to write. Pass ``--check`` to exit non-zero if
the live configuration differs from the snapshot (useful in CI on the host).

Touched live files (only with ``--apply``):
    ~/.omlx/global_templates.json   global_profiles
    ~/.omlx/model_profiles.json     model_profiles
    ~/.omlx/model_settings.json     active_profile_name per model

Standard library only, no dependencies.

Usage:
    python3 scripts/apply-profiles.py            # show the diff
    python3 scripts/apply-profiles.py --check    # non-zero if it differs
    python3 scripts/apply-profiles.py --apply    # write the settings
"""

import argparse
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, "..", "..", "profiles", "omlx-profiles.json")
OMLX = os.path.expanduser("~/.omlx")


def load(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def diff_summary(snapshot, live_templates, live_profiles, live_settings):
    """Return a list of human-readable differences between snapshot and live."""
    changes = []
    for name, prof in snapshot.get("global_profiles", {}).items():
        live = live_templates.get(name)
        if live is None:
            changes.append(f"global profile `{name}`: missing locally")
        elif live.get("settings") != prof.get("settings"):
            changes.append(f"global profile `{name}`: settings differ")
    for model, mapping in snapshot.get("model_to_profile", {}).items():
        ms = (live_settings.get("models", {}) or {}).get(model, {})
        if ms.get("active_profile_name") != mapping:
            changes.append(f"model `{model}`: active profile {ms.get('active_profile_name')!r} → {mapping!r}")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="write the snapshot to ~/.omlx (default: dry run)")
    ap.add_argument("--check", action="store_true", help="exit non-zero if live config differs from the snapshot")
    args = ap.parse_args()

    snap = load(SNAPSHOT)
    if not snap:
        print(f"ERROR: cannot read snapshot {SNAPSHOT}", file=sys.stderr)
        return 2

    tpl_path = os.path.join(OMLX, "global_templates.json")
    prof_path = os.path.join(OMLX, "model_profiles.json")
    set_path = os.path.join(OMLX, "model_settings.json")

    live_tpl = load(tpl_path, {})
    live_prof = load(prof_path, {})
    live_set = load(set_path, {})
    if not live_set:
        print(f"ERROR: oMLX config not found under {OMLX}", file=sys.stderr)
        return 2

    changes = diff_summary(snap, live_tpl.get("templates", {}), live_prof.get("profiles", {}), live_set)

    if not changes:
        print("OK: live oMLX configuration matches the snapshot.")
        return 0

    print("Differences between snapshot and live configuration:")
    for c in changes:
        print(f"  - {c}")

    if args.check:
        return 1
    if not args.apply:
        print("\n(dry run — pass --apply to write)")
        return 1

    stamp = time.strftime("%Y%m%d-%H%M%S")
    for p in (tpl_path, prof_path, set_path):
        if os.path.exists(p):
            shutil.copy2(p, f"{p}.bak-{stamp}")

    # global templates
    live_tpl["templates"] = snap.get("global_profiles", {})
    with open(tpl_path, "w") as f:
        json.dump(live_tpl, f, indent=2, ensure_ascii=False)

    # per-model resolved profiles
    live_prof["profiles"] = snap.get("model_profiles", {})
    with open(prof_path, "w") as f:
        json.dump(live_prof, f, indent=2, ensure_ascii=False)

    # model -> active profile
    live_set.setdefault("models", {})
    for model, mapping in snap.get("model_to_profile", {}).items():
        live_set["models"].setdefault(model, {})
        live_set["models"][model]["active_profile_name"] = mapping
    with open(set_path, "w") as f:
        json.dump(live_set, f, indent=2, ensure_ascii=False)

    print(f"\nApplied. Backups written with suffix .bak-{stamp}")
    print("Restart oMLX so the new profiles take effect:")
    print("  ~/.omlx/bin/omlx stop; sleep 4; ~/.omlx/bin/omlx start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
