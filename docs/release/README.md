# `docs/release/` — shipping a snapshot

This repository has no versioned releases in the semver sense. It publishes
**dated snapshots** of a measurement. A snapshot is "released" when:

1. The report under [`../../benchmarks/`](../../benchmarks) is final.
2. [`../../reference/results.json`](../../reference/results.json) matches it.
3. `manifest.json` is regenerated, so its SHA-256 describes the exact bytes.

## The run

```bash
# 1. regenerate the manifest from the committed data
python3 scripts/release/build-manifest.py

# 2. prove nothing is stale
python3 scripts/release/build-manifest.py --check
./test/test.sh

# 3. tag the snapshot and push
git tag -a v2026-11-11 -m "Benchmark snapshot 2026-11-11 (M1 Max)"
git push origin v2026-11-11
```

The tag is date-based, not semver: a benchmark is a point in time, and
`v2026-11-11` says more than `v1.0.0` about what a reader gets.

## What ships

- The Markdown report (the whole point).
- `reference/results.json` (the machine-readable numbers).
- `manifest.json` (the checksum that proves the first two are the bytes cited).

Model weights are **not** shipped; they live on HuggingFace and keep their own
licences. See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## The CI pair

[`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml) runs the
offline gate on demand. There is no push-triggered release: a snapshot is a
deliberate, manual act.
