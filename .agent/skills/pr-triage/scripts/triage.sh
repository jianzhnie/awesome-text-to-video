#!/usr/bin/env bash
# pr-triage —— 列出 open PR,并对每个 PR 跑可自动化的硬性检查。
#
# 回答的问题是:"这些 PR 哪些能直接合并,哪些需要人来拍板?"
# 只报告事实,不做决定。价值判断(品牌冒充、与竞品混淆、推广条目是否该收)
# 由 scan_prs.py 以「需人判断」的形式抛出。
#
# 用法:
#   triage.sh                      # 当前仓库,全部 open PR
#   triage.sh --repo owner/name    # 指定仓库
#   triage.sh --limit 50           # 限制列出数量
#   triage.sh --pr 26              # 只处理一个 PR
#   triage.sh --no-link-check      # 跳过网络链接检查(更快、可离线)
#   triage.sh --json               # 机器可读输出
#   triage.sh --diff 23            # 只打印 PR 23 的 diff 后退出
#
# 退出码:0 = 正常执行完毕(不论检查结果如何)。1 = 用法/环境错误。

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
    *) echo "未知参数: $1" >&2; exit 1 ;;
  esac
done

command -v gh >/dev/null || { echo "错误:未找到 gh CLI" >&2; exit 1; }
command -v python3 >/dev/null || { echo "错误:未找到 python3" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "错误:gh 未认证(请运行 gh auth login)" >&2; exit 1; }

# 未指定仓库时,从当前目录自动探测。
if [ -z "$REPO" ]; then
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null) \
    || { echo "错误:当前不在带 GitHub remote 的 git 仓库中;请用 --repo owner/name 指定" >&2; exit 1; }
fi

if [ -n "$DIFF" ]; then
  gh pr diff "$DIFF" --repo "$REPO"
  exit $?
fi

FIELDS='number,title,author,createdAt,isDraft,mergeable,mergeStateStatus,additions,deletions,changedFiles,headRefName,headRefOid,headRepositoryOwner,headRepository,baseRefName,isCrossRepository,maintainerCanModify,url'

PRS=$(gh pr list --repo "$REPO" --state open --limit "$LIMIT" --json "$FIELDS" 2>/dev/null) \
  || { echo "错误:无法列出 $REPO 的 PR" >&2; exit 1; }

COUNT=$(printf '%s' "$PRS" | python3 -c 'import sys,json; print(len(json.load(sys.stdin)))')

echo "═══════════════════════════════════════════════════════════════"
echo " PR 分类 —— $REPO —— $COUNT 个 open PR"
echo "═══════════════════════════════════════════════════════════════"

if [ "$COUNT" -eq 0 ]; then
  echo " 没有需要处理的 PR。"
  exit 0
fi

# 总览表(表头 + 每个 PR 一行)。
printf '%s' "$PRS" | python3 "$SCRIPT_DIR/scan_prs.py" --table

echo
echo "═══════════════════════════════════════════════════════════════"
echo " 硬性检查(可自动化 —— 是事实,不是价值判断)"
echo "═══════════════════════════════════════════════════════════════"

SCAN_ARGS=(--repo "$REPO" --limit "$LIMIT")
[ "$NO_LINK" -eq 1 ] && SCAN_ARGS+=(--no-link-check)
[ -n "$ONLY_PR" ]    && SCAN_ARGS+=(--pr "$ONLY_PR")
[ "$JSON" -eq 1 ]    && SCAN_ARGS+=(--json)

python3 "$SCRIPT_DIR/scan_prs.py" "${SCAN_ARGS[@]}"
