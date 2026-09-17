#!/usr/bin/env bash
# prep-fork-pr — get a fork PR into a mergeable state without push access to the fork.
#
# The trap this exists to avoid: a fork PR's head lives at refs/pull/N/head,
# which is NOT the same ref as refs/heads/<same-name> on your repo — even when
# the names match. Pushing to origin/<their-branch-name> does nothing to the PR.
# Meanwhile the fork's branch is usually behind your base, so `gh pr merge`
# reports "Pull Request has merge conflicts" and stays stuck.
#
# What this does (the mechanical part):
#   1. read the PR's shape (base, fork, head ref, push permission)
#   2. check the working tree is clean enough to work in
#   3. fetch refs/pull/N/head into a local branch  pr-prep/N
#   4. merge the base branch in
#   5. print the exact push + merge commands for whoever finishes the job
#
# Conflict resolution, content edits, and the final merge are deliberately left
# to the caller — see the skill's Phase 3/4. The script stops and reports; it
# never force-pushes and never merges on its own.
#
# Usage:
#   prep-fork-pr.sh <pr-number> [--repo owner/name]
#   prep-fork-pr.sh <pr-number> --status      # just report state, change nothing
#   prep-fork-pr.sh <pr-number> --abort       # abandon an in-progress merge
#
# Exit codes:
#   0 = branch ready (already mergeable, or cleaned up by an aborted merge)
#   3 = merge left conflicts that need resolving
#   2 = cannot push to the fork (maintainerCanModify=false)
#   1 = usage / environment error

set -uo pipefail

REPO=""
PR=""
MODE="run"

while [ $# -gt 0 ]; do
  case "$1" in
    --repo)   REPO="$2"; shift 2 ;;
    --status) MODE="status"; shift ;;
    --abort)  MODE="abort"; shift ;;
    -h|--help) sed -n '2,28p' "$0"; exit 0 ;;
    ''|*[!0-9]*) echo "error: expected a PR number, got '$1'" >&2; exit 1 ;;
    *)        PR="$1"; shift ;;
  esac
done

[ -n "$PR" ] || { echo "error: PR number required" >&2; exit 1; }
command -v gh >/dev/null || { echo "error: gh CLI not found" >&2; exit 1; }
command -v python3 >/dev/null || { echo "error: python3 not found" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "error: gh not authenticated (run: gh auth login)" >&2; exit 1; }

REPO=${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null)}
[ -n "$REPO" ] || { echo "error: pass --repo owner/name" >&2; exit 1; }

WORK="pr-prep/$PR"

# ---- read the PR's shape (shared by every mode) ----------------------------
INFO=$(gh pr view "$PR" --repo "$REPO" --json \
  number,title,headRefName,headRefOid,baseRefName,isCrossRepository,maintainerCanModify,mergeable,mergeStateStatus \
  2>/dev/null) || { echo "error: could not read PR #$PR in $REPO" >&2; exit 1; }

jqget() { printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('$1'))"; }
jqnested() {
  printf '%s' "$INFO" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print((d.get('$1') or {}).get('$2', ''))"
}

TITLE=$(jqget title)
BASE=$(jqget baseRefName)
CROSS=$(jqget isCrossRepository)
CAN_MODIFY=$(jqget maintainerCanModify)
MERGEABLE=$(jqget mergeable)
MERGE_STATE=$(jqget mergeStateStatus)
HEAD_REF=$(jqget headRefName)

# Fork owner/repo — not in this JSON, so ask once more (cheap).
HEAD_OWNER=$(gh pr view "$PR" --repo "$REPO" --json headRepositoryOwner --jq '.headRepositoryOwner.login' 2>/dev/null)
HEAD_REPO=$(gh pr view "$PR" --repo "$REPO" --json headRepository --jq '.headRepository.name' 2>/dev/null)

echo "═══════════════════════════════════════════════════════════════"
echo " PR #$PR — $TITLE"
echo " base=$BASE   head=$HEAD_OWNER/$HEAD_REPO:$HEAD_REF"
echo " cross-repo=$CROSS   maintainerCanModify=$CAN_MODIFY"
echo " mergeable=$MERGEABLE ($MERGE_STATE)"
echo "═══════════════════════════════════════════════════════════════"

if [ "$MODE" = "abort" ]; then
  git merge --abort 2>/dev/null && echo "→ aborted in-progress merge"
  git checkout - >/dev/null 2>&1 || true
  git branch -D "$WORK" 2>/dev/null && echo "→ removed $WORK"
  exit 0
fi

if [ "$MODE" = "status" ]; then
  [ "$MERGEABLE" = "MERGEABLE" ] && echo "Already mergeable — nothing to do." && exit 0
  echo "Needs work: $MERGE_STATE"
  exit 0
fi

# ---- same-repo PR: trivial path --------------------------------------------
if [ "$CROSS" != "True" ]; then
  cat <<EOF
This is a same-repo PR — merge the base into its own branch directly:
    gh pr checkout $PR
    git merge origin/$BASE
    git push
EOF
  exit 0
fi

if [ "$CAN_MODIFY" != "True" ]; then
  cat <<EOF
⚠ maintainerCanModify=false — you cannot push to $HEAD_OWNER's fork.
Options:
  a) comment asking them to merge $BASE into their branch, or
  b) push a maintainer branch and retarget the PR's base to it.
     (Squash-merge still credits the original author.)
EOF
  exit 2
fi

# ---- clean tree check ------------------------------------------------------
if [ -n "$(git status --porcelain)" ]; then
  echo "error: working tree not clean — commit or stash first." >&2
  echo "       (in-progress merge? run: $0 $PR --abort)" >&2
  git status --short | sed 's/^/    /' >&2
  exit 1
fi

# ---- fetch head, branch, merge base ---------------------------------------
echo
echo "→ fetching refs/pull/$PR/head"
git fetch origin "refs/pull/$PR/head" 2>/dev/null \
  || { echo "error: fetch failed. 'gh pr checkout' can rewrite remote config;" >&2
       echo "       check with: git remote -v" >&2; exit 1; }

git branch -f "$WORK" FETCH_HEAD
git checkout "$WORK" >/dev/null 2>&1 || { echo "error: checkout $WORK failed" >&2; exit 1; }

echo "→ merging origin/$BASE"
git fetch origin "$BASE" 2>/dev/null

if git merge --no-edit "origin/$BASE" >/dev/null 2>&1; then
  echo "✓ merged cleanly — no conflicts"
else
  echo "⚠ conflicts need resolving:"
  git status --short | grep -E '^(UU|AA|DD|AU|UA|DU|UD)' | sed 's/^/    /'
  cat <<EOF

  Resolve the marked files, then continue this same command.
  For listing repos the usual fix is "keep both rows" — edit the file so both
  entries survive, then:
      git add <files> && git commit --no-edit
  To bail out:  $0 $PR --abort
EOF
  exit 3
fi

echo
echo "✓ $WORK is up to date with $BASE."
echo
echo "── next steps ────────────────────────────────────────────────"
echo " 1. review + fix content:  git diff origin/$BASE --stat"
echo " 2. push back to the fork:"
echo "      git push https://github.com/$HEAD_OWNER/$HEAD_REPO.git \\"
echo "          $WORK:refs/heads/$HEAD_REF"
echo " 3. merge:"
echo "      gh pr merge $PR --repo $REPO --squash --delete-branch"
echo " 4. clean up:  git checkout - && git branch -D $WORK"
echo "──────────────────────────────────────────────────────────────"
