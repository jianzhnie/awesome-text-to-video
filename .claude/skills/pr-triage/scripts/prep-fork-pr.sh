#!/usr/bin/env bash
# prep-fork-pr —— 在没有 fork 推送权限的前提下,把 fork PR 弄成可合并状态。
#
# 这个脚本要避开的坑:fork PR 的 head 位于 refs/pull/N/head,它**不是**你仓库上的
# refs/heads/<同名分支>,即使名字完全一样。推 origin/<对方的分支名> 对 PR 毫无影响。
# 同时 fork 的分支通常落后于你的 base,于是 `gh pr merge` 报 "Pull Request has
# merge conflicts" 并一直卡住。
#
# 本脚本负责机械部分:
#   1. 读取 PR 的形态(base、fork、head ref、推送权限)
#   2. 确认工作区干净,可以动手
#   3. 把 refs/pull/N/head 取到本地分支 pr-prep/N
#   4. 把 base 分支 merge 进来
#   5. 打印出完成后续工作所需的精确 push + merge 命令
#
# 冲突解决、内容修改、最终合并都刻意留给调用方——见 skill 的第三、四阶段。
# 脚本只报告,绝不 force-push,也绝不自行合并。
#
# 用法:
#   prep-fork-pr.sh <PR编号> [--repo owner/name]
#   prep-fork-pr.sh <PR编号> --status      # 只报告状态,不做任何改动
#   prep-fork-pr.sh <PR编号> --abort       # 放弃进行中的 merge
#
# 退出码:
#   0 = 分支已就绪(本就可合并,或已通过 --abort 清理)
#   3 = merge 产生冲突,需要解决
#   2 = 无法推送到该 fork(maintainerCanModify=false)
#   1 = 用法/环境错误

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
    ''|*[!0-9]*) echo "错误:期望一个 PR 编号,实际收到 '$1'" >&2; exit 1 ;;
    *)        PR="$1"; shift ;;
  esac
done

[ -n "$PR" ] || { echo "错误:必须提供 PR 编号" >&2; exit 1; }
command -v gh >/dev/null || { echo "错误:未找到 gh CLI" >&2; exit 1; }
command -v python3 >/dev/null || { echo "错误:未找到 python3" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "错误:gh 未认证(请运行 gh auth login)" >&2; exit 1; }

REPO=${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null)}
[ -n "$REPO" ] || { echo "错误:请用 --repo owner/name 指定仓库" >&2; exit 1; }

WORK="pr-prep/$PR"

# ---- 读取 PR 形态(各模式共用) ---------------------------------------------
INFO=$(gh pr view "$PR" --repo "$REPO" --json \
  number,title,headRefName,headRefOid,baseRefName,isCrossRepository,maintainerCanModify,mergeable,mergeStateStatus \
  2>/dev/null) || { echo "错误:无法读取 $REPO 中的 PR #$PR" >&2; exit 1; }

jqget() { printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('$1'))"; }

TITLE=$(jqget title)
BASE=$(jqget baseRefName)
CROSS=$(jqget isCrossRepository)
CAN_MODIFY=$(jqget maintainerCanModify)
MERGEABLE=$(jqget mergeable)
MERGE_STATE=$(jqget mergeStateStatus)
HEAD_REF=$(jqget headRefName)

# fork 的 owner/repo 不在上面的 JSON 里,再查一次(开销很小)。
HEAD_OWNER=$(gh pr view "$PR" --repo "$REPO" --json headRepositoryOwner --jq '.headRepositoryOwner.login' 2>/dev/null)
HEAD_REPO=$(gh pr view "$PR" --repo "$REPO" --json headRepository --jq '.headRepository.name' 2>/dev/null)

echo "═══════════════════════════════════════════════════════════════"
echo " PR #$PR — $TITLE"
echo " base=$BASE   head=$HEAD_OWNER/$HEAD_REPO:$HEAD_REF"
echo " 跨仓库=$CROSS   maintainerCanModify=$CAN_MODIFY"
echo " 可合并=$MERGEABLE ($MERGE_STATE)"
echo "═══════════════════════════════════════════════════════════════"

if [ "$MODE" = "abort" ]; then
  git merge --abort 2>/dev/null && echo "→ 已放弃进行中的 merge"
  git checkout - >/dev/null 2>&1 || true
  git branch -D "$WORK" 2>/dev/null && echo "→ 已删除 $WORK"
  exit 0
fi

if [ "$MODE" = "status" ]; then
  [ "$MERGEABLE" = "MERGEABLE" ] && echo "已可合并——无需处理。" && exit 0
  echo "需要处理:$MERGE_STATE"
  exit 0
fi

# ---- 同仓库 PR:直接走简单路径 ----------------------------------------------
if [ "$CROSS" != "True" ]; then
  cat <<EOF
这是同仓库 PR —— 直接把 base merge 进它自己的分支即可:
    gh pr checkout $PR
    git merge origin/$BASE
    git push
EOF
  exit 0
fi

if [ "$CAN_MODIFY" != "True" ]; then
  cat <<EOF
⚠ maintainerCanModify=false —— 你无法推送到 $HEAD_OWNER 的 fork。
可选方案:
  a) 留言请对方把 $BASE merge 进他们的分支,或
  b) 推一个维护者分支,并把 PR 的 base 改为它。
     (用 squash 合并时,原作者署名仍然保留。)
EOF
  exit 2
fi

# ---- 检查工作区 ------------------------------------------------------------
if [ -n "$(git status --porcelain)" ]; then
  echo "错误:工作区不干净——请先提交或 stash。" >&2
  echo "      (有进行中的 merge?运行:$0 $PR --abort)" >&2
  git status --short | sed 's/^/    /' >&2
  exit 1
fi

# ---- 取 head、建分支、merge base -------------------------------------------
echo
echo "→ 正在取 refs/pull/$PR/head"
git fetch origin "refs/pull/$PR/head" 2>/dev/null \
  || { echo "错误:fetch 失败。'gh pr checkout' 会改写 remote 配置;" >&2
       echo "      用 git remote -v 检查一下" >&2; exit 1; }

git branch -f "$WORK" FETCH_HEAD
git checkout "$WORK" >/dev/null 2>&1 || { echo "错误:无法检出 $WORK" >&2; exit 1; }

echo "→ 正在 merge origin/$BASE"
git fetch origin "$BASE" 2>/dev/null

if git merge --no-edit "origin/$BASE" >/dev/null 2>&1; then
  echo "✓ 干净合并——无冲突"
else
  echo "⚠ 存在冲突,需要解决:"
  git status --short | grep -E '^(UU|AA|DD|AU|UA|DU|UD)' | sed 's/^/    /'
  cat <<EOF

  解决上面标记的文件,然后重新执行同一条命令继续。
  列表类仓库通常的处理方式是"两行都保留"——编辑文件让两条条目都存活,然后:
      git add <文件> && git commit --no-edit
  想放弃:$0 $PR --abort
EOF
  exit 3
fi

echo
echo "✓ $WORK 已与 $BASE 同步。"
echo
echo "── 后续步骤 ─────────────────────────────────────────────────"
echo " 1. 复核并修改内容:  git diff origin/$BASE --stat"
echo " 2. 推回 fork:"
echo "      git push https://github.com/$HEAD_OWNER/$HEAD_REPO.git \\"
echo "          $WORK:refs/heads/$HEAD_REF"
echo " 3. 合并:"
echo "      gh pr merge $PR --repo $REPO --squash --delete-branch"
echo " 4. 清理:  git checkout - && git branch -D $WORK"
echo "─────────────────────────────────────────────────────────────"
