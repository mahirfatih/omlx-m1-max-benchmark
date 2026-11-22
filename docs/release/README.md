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
git tag -a v2026-11-22 -m "Benchmark snapshot 2026-11-22 (M1 Max)"
git push origin v2026-11-22
```

The tag is date-based, not semver: a benchmark is a point in time, and
`v2026-11-22` says more than `v1.0.0` about what a reader gets.

## What ships

- The Markdown reports (the whole point): the current campaign's report, with the
  previous campaign kept byte-stable alongside it under `benchmarks/`.
- `reference/results.json` (the machine-readable numbers).
- `manifest.json` (`manifest_version` 2): the checksums that prove both reports
  (`report` and `archive_report`) and `reference/results.json` are the bytes
  cited.

Model weights are **not** shipped; they live on HuggingFace and keep their own
licences. See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## The CI pair

[`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml) runs the
offline gate on demand. There is no push-triggered release: a snapshot is a
deliberate, manual act.
