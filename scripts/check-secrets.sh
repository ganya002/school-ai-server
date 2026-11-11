#!/usr/bin/env bash
# Scan a git diff for secrets and real network identifiers.
# This is not a git hook. Run it before every push:
#   ./scripts/check-secrets.sh
set -euo pipefail
export GIT_PAGER=cat PAGER=cat

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if git rev-parse --verify origin/main >/dev/null 2>&1; then
  range="origin/main"
else
  range="HEAD"
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# Committed + unstaged + staged, added lines only.
{
  git diff "$range" || true
  git diff || true
  git diff --cached || true
} | command grep -E '^\+' | command grep -vE '^\+\+\+' >"$tmp" || true

if [[ ! -s "$tmp" ]]; then
  echo "check-secrets: no added lines against ${range} or the working tree."
  exit 0
fi

hits=0
report() {
  local label="$1" pattern="$2"
  local matches
  matches="$(command grep -nE "$pattern" "$tmp" || true)"
  if [[ -n "$matches" ]]; then
    echo "POSSIBLE SECRET / INTERNAL DETAIL ($label):"
    printf '%s\n' "$matches"
    echo
    hits=1
  fi
}

report "private-key" 'BEGIN (OPENSSH|RSA|DSA|EC|PGP) PRIVATE'
report "credential-assignment" '(password|passwd|api[_-]?key|secret[_-]?key|WEBUI_SECRET|authorization:[[:space:]]*Bearer)[[:space:]]*[=:][[:space:]]*[^[:space:]]+'
report "aws-key" 'AKIA[0-9A-Z]{16}'
report "mac-address" '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'

# IPv4, excluding documentation / loopback / unspecified ranges.
ipv4_hits="$(command grep -nE '[0-9]{1,3}(\.[0-9]{1,3}){3}' "$tmp" || true)"
if [[ -n "$ipv4_hits" ]]; then
  filtered="$(printf '%s\n' "$ipv4_hits" | command grep -vE '192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|127\.|0\.0\.0\.0|255\.255\.255' || true)"
  if [[ -n "$filtered" ]]; then
    echo "POSSIBLE REAL IP (use 192.0.2.x / 198.51.100.x / 203.0.113.x placeholders):"
    printf '%s\n' "$filtered"
    echo
    hits=1
  fi
fi

if [[ "$hits" -ne 0 ]]; then
  echo "check-secrets: failed. Replace secrets and real addresses with placeholders, then re-run."
  exit 1
fi

echo "check-secrets: no obvious secrets or real IPs in the diff against ${range}."
exit 0
