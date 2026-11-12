#!/usr/bin/env bash
#
# lint.sh — the single entry point for every linter, run by hand and by CI.
#
# `ruff`, `yamllint` and `markdownlint-cli2` are fetched at a pinned version by
# uvx/npx, so the version is part of the command and a green local run and a
# green CI run are the same bytes. `shellcheck` and `actionlint` are native
# binaries and are expected on PATH; the CI `lint` job installs each one at the
# version pinned in .github/workflows/ci.yml before it calls this script.
#
# `ruff` also lints the test harness itself. That is the point: the scripts that
# judge the models are code too, and they fail the same way any code does — an
# unused variable here is a real bug that a self-test may not catch.
#
# There are no flags. Run it from anywhere; it works from the repository root.
set -euo pipefail

RUFF_VERSION="0.8.4"
YAMLLINT_VERSION="1.38.0"
MARKDOWNLINT_CLI2_VERSION="0.24.0"

cd "$(dirname "$0")/.." || exit 1

fail=0
run() {
  local name="$1"
  shift
  printf '\n== %s ==\n' "$name"
  if "$@"; then
    printf '   ok\n'
  else
    printf '   FAILED\n' >&2
    fail=1
  fi
}

SH=()
while IFS= read -r f; do SH+=("$f"); done < <(find . -name '*.sh' -not -path './.git/*' -not -path './node_modules/*')

run "ruff check (${RUFF_VERSION})" uvx "ruff@${RUFF_VERSION}" check scripts/
run "shellcheck" shellcheck "${SH[@]}"
run "actionlint" actionlint .github/workflows/*.yml
run "yamllint ${YAMLLINT_VERSION}" uvx "yamllint@${YAMLLINT_VERSION}" .
run "markdownlint-cli2 ${MARKDOWNLINT_CLI2_VERSION}" npx --yes "markdownlint-cli2@${MARKDOWNLINT_CLI2_VERSION}"

printf '\n'
if [ "$fail" -eq 0 ]; then
  printf 'all linters clean\n'
else
  printf 'lint failed\n' >&2
fi
exit "$fail"
