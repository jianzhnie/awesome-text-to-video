#!/usr/bin/env bash
# pr-triage — dump open PRs, then run the automatable hard checks over each.
#
# Answers "which of these PRs can I merge, and which need a human decision?"
# Reports facts; does NOT decide. Subjective calls (brand impersonation,
# competitor confusion, whether a promo entry belongs at all) are surfaced as
# NEEDS-HUMAN by scan_prs.py.
#
# Usage:
#   triage.sh                      # current repo, all open PRs
#   triage.sh --repo owner/name    # explicit repo
#   triage.sh --limit 50           # cap how many PRs to list
#   triage.sh --pr 26              # triage a single PR
#   triage.sh --no-link-check      # skip network link checks (fast, offline)
#   triage.sh --json               # machine-readable
#   triage.sh --diff 23            # just print PR 23's diff and exit
#
# Exit codes: 0 = ran fine (regardless of findings). 1 = usage/environment error.

set -uo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

REPO=""
LIMIT=100
JSON=0
DIFF=""
NO_LINK=0
ONLY_PR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --repo)          REPO="$2"; shift 2 ;;
    --limit)         LIMIT="$2"; shift 2 ;;
    --pr)            ONLY_PR="$2"; shift 2 ;;
    --json)          JSON=1; shift ;;
    --no-link-check) NO_LINK=1; shift ;;
    --diff)          DIFF="$2"; shift 2 ;;
    -h|--help)       sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

command -v gh >/dev/null || { echo "error: gh CLI not found" >&2; exit 1; }
command -v python3 >/dev/null || { echo "error: python3 not found" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "error: gh not authenticated (run: gh auth login)" >&2; exit 1; }

# Auto-detect repo from the current directory when not given.
if [ -z "$REPO" ]; then
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null) \
    || { echo "error: not in a git repo with a GitHub remote; pass --repo owner/name" >&2; exit 1; }
fi

if [ -n "$DIFF" ]; then
  gh pr diff "$DIFF" --repo "$REPO"
  exit $?
fi

FIELDS='number,title,author,createdAt,isDraft,mergeable,mergeStateStatus,additions,deletions,changedFiles,headRefName,headRefOid,headRepositoryOwner,headRepository,baseRefName,isCrossRepository,maintainerCanModify,url'

PRS=$(gh pr list --repo "$REPO" --state open --limit "$LIMIT" --json "$FIELDS" 2>/dev/null) \
  || { echo "error: failed to list PRs for $REPO" >&2; exit 1; }

COUNT=$(printf '%s' "$PRS" | python3 -c 'import sys,json; print(len(json.load(sys.stdin)))')

echo "═══════════════════════════════════════════════════════════════"
echo " PR triage — $REPO — $COUNT open PR(s)"
echo "═══════════════════════════════════════════════════════════════"

if [ "$COUNT" -eq 0 ]; then
  echo " Nothing to do."
  exit 0
fi

# Summary table (header row + one line per PR).
printf '%s' "$PRS" | python3 "$SCRIPT_DIR/scan_prs.py" --table

echo
echo "═══════════════════════════════════════════════════════════════"
echo " HARD CHECKS  (automatable — facts, not judgement calls)"
echo "═══════════════════════════════════════════════════════════════"

SCAN_ARGS=(--repo "$REPO" --limit "$LIMIT")
[ "$NO_LINK" -eq 1 ] && SCAN_ARGS+=(--no-link-check)
[ -n "$ONLY_PR" ]    && SCAN_ARGS+=(--pr "$ONLY_PR")
[ "$JSON" -eq 1 ]    && SCAN_ARGS+=(--json)

python3 "$SCRIPT_DIR/scan_prs.py" "${SCAN_ARGS[@]}"
