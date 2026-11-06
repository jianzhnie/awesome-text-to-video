---
name: pr-triage
description: >-
  批量处理、审查并合并 curated 仓库(awesome-list、文档目录、README 清单)的待处理 PR:
  核查提交的链接是否有效、识别追踪/联盟参数、发现冒充官方产品的第三方代理站、
  解决无法推送的 fork PR 的合并冲突,最后合并并向贡献者致谢。
  当用户说"处理这些 PR""处理 PR 积压""审查待处理的 PR""合并这些 PR""帮我过一遍 PR"
  "把 PR 队列清一清",或直接指向某个仓库的 /pulls 页面时使用——即使没说"triage"这个词。
  当某个列表类 PR 卡在 "merge conflicts" 需要解开时,同样使用。
  Use this whenever the user says "handle the review backlog", "triage open PRs",
  "merge the pending pull requests", "there are a bunch of PRs to review", or
  points at a repo's /pulls page — even if they don't say the word "triage".
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion, TaskCreate, TaskUpdate
---

# /pr-triage

批量处理 curated 清单仓库的待处理 PR:核查每一份提交,能机械修复的直接修,需要人判断的
上报,合并,并向贡献者致谢。

贯穿全程的主轴:**自动判定事实,人工判断价值。**
"链接返回 404" 是事实——直接处理。"这个站是不是在冒充官方产品?" 是判断——交给你。

> **脚本路径。** 脚本位于 `.claude/skills/pr-triage/scripts/`。在会话开始时设置一次,
> 下面的命令即可在仓库根目录直接复制运行:
>
> ```bash
> TRIAGE=.claude/skills/pr-triage/scripts
> ```
>
> 每个脚本内部都会自行解析自身目录,因此用绝对路径调用或在其他工作目录下调用同样可行
> ——只需调整下面命令里的路径前缀。

## 用法

```text
/pr-triage                     # 当前仓库,处理全部 open PR
/pr-triage owner/name          # 指定仓库
/pr-triage 26 25 24            # 只处理这些 PR 编号
```

## 工作流

### 第一阶段 —— 侦察

动手之前先摸清积压的全貌。

```bash
$TRIAGE/triage.sh --repo <owner/name>
```

输出一张总览表(是否 draft?是否冲突?fork 是否可推送?),并对每个 PR 跑硬性检查:
失效链接、追踪参数、是否改动了非文档文件。
各检查项的含义与完整的"需人工判断"清单见
`.claude/skills/pr-triage/references/listing-policy.md`。

如果仓库不熟悉,再扫一遍 README 的章节结构和 `Contributing` 约定——条目该落在哪个章节
是实打实的审查项,不是走过场:

```bash
grep -n '^#\+ ' README.md        # 章节结构
sed -n '/## Contributing/,/^## /p' README.md   # 贡献约定
```

### 第二阶段 —— 分类

把每个 PR 归入且仅归入一类:

| 类别 | 判定标准 | 处理 |
| --- | --- | --- |
| **干净** | 章节正确、链接有效、无追踪参数、格式与表格一致 | 直接合并(第五阶段) |
| **机械修复** | 内容没问题,但有参数/死链/标签需要改 | 修(第三阶段)后合并 |
| **需人判断** | 官方 vs 代理、重复条目、付费推广、参数不实 | 问用户(第四阶段) |
| **卡住** | 相对 base 处于 `CONFLICTING` / `DIRTY` | 解冲突(第三阶段 b)后合并 |

*需人判断* 这一类**一律不要自行合并**。把问题成批收集,用一次 `AskUserQuestion`
一起问,而不是每个 PR 打断一次。

### 第三阶段 a —— 对 fork PR 施加机械修复

列表类 PR 大多来自 fork,而你通常无法直接推送贡献者的 fork 分支。可行的机制是:

```bash
# 1. 把 PR head 取到本地分支,并 merge base
$TRIAGE/prep-fork-pr.sh <PR> --repo <owner/name>

# 2. 若上一步报了冲突,先解决(第三阶段 b),再确认你的改动
# 3. 把结果推回 FORK 的分支
git push https://github.com/<FORK_OWNER>/<FORK_REPO>.git \
    pr-prep/<PR>:refs/heads/<对方的分支名>
```

只有当 PR 的 `maintainerCanModify=true` 时推送才会成功。若为 `false`,
`prep-fork-pr.sh` 会打印两条退路(留言请对方 rebase,或推一个维护者分支并改 PR base)。

> **ref 陷阱——这是最容易出错的一点。**
> fork PR 的 head 是 `refs/pull/N/head`,它**不是**你仓库上的
> `refs/heads/<同名分支>`,**即使两者名字完全一样**。推 `origin/<对方的分支名>`
> 只会改动一个无关分支,PR 会永远卡在冲突状态。
> `prep-fork-pr.sh` 之所以去取 `refs/pull/N/head`,正是为了避开这一点。
>
> 推论:`gh pr checkout <N>` 会改写该分支的本地 remote 配置,导致后续 `git fetch origin`
> 失败。若 checkout 之后 fetch 开始报错,先 `git remote -v` 检查并重置 URL。

### 第三阶段 b —— 解决冲突

在 curated 清单仓库里,冲突绝大多数是两个 PR 往同一张表追加内容,所以
**解决方式是"两行都保留"**,而不是选一个赢家。

```bash
# $TRIAGE/prep-fork-pr.sh 报冲突之后:
grep -n '<<<<<<<\|=======\|>>>>>>>' README.md     # 定位冲突位置
# 编辑文件,让两条条目都保留,顺序合理即可
git add README.md
git commit --no-edit
```

代替贡献者重做提交时,要保留其署名:

```bash
git commit --amend --no-edit --author="<从 gh pr view --json commits 取到的原作者>"
```

然后重跑 `$TRIAGE/prep-fork-pr.sh <PR>`——它会报告分支已干净——再推回 fork(第三阶段 a 的第 3 步)。

### 第四阶段 —— 上报需人判断的问题

问用户时,永远把你的建议放在第一个,并给出理由。
仓库的既有约定与完整审查清单在 `.claude/skills/pr-triage/references/listing-policy.md`;
反复出现的几类是:

- **冒充官方产品的第三方代理站。** 域名抢注特征(`<产品名>3.org`)、
  自称"独立"平台、转售一个已经在清单里的产品。建议标注为第三方,而不是拒绝——
  信息本身是真的,只是标签错了。
- **追踪 / 联盟参数。** 合并前剥掉参数,条目可以保留。
  `utm_campaign=listing-wave-…` 这类参数是付费目录收录的指纹,不是真诚推荐。
- **失效链接。** 删掉失效链接(若失效链接本身就是该条目的唯一链接,则删掉整个条目);
  常见原因是仓库还没公开或已改名。
- **重复条目。** 同一张表里换个名字又出现了。

### 第五阶段 —— 合并并致谢

```bash
gh pr merge <PR> --squash --delete-branch
```

单条目的列表类 PR 用 `--squash`,让清单历史保持"一次新增一个提交"。
若 PR 是 draft,先 `gh pr ready <PR>`。

然后给**每一个**已合并的 PR 留一条致谢评论——包括你改动过的那些。
若你改动了别人的提交,要明确说明改了什么、为什么,让这次编辑读起来像协作,
而不是无声的改写:

```bash
gh pr comment <PR> --body "感谢 @<作者>!🎉 已合并。合并时做了一处调整:
<改了什么、为什么>。<一句真诚且具体的称赞>。"
```

一批处理完后,确认没有遗漏:

```bash
gh pr list --state open --limit 50          # 应为空,或只剩已上报的 PR
git log --oneline -<N>                      # 确认每次合并对应一个提交
git branch -D pr-prep/*                     # 清理工作分支
```

## 汇报

完成后,给用户一张表说明每个 PR 的去向(原样合并 / 改动 X 后合并 / 留给你决定),
并**单独列出所有你未经要求就做的改动**——维护者需要能在一个地方审计你的编辑。
同时提出你注意到但没动手处理的明显后续事项。

## 随附脚本

| 脚本 | 用途 |
| --- | --- |
| `.claude/skills/pr-triage/scripts/triage.sh` | 总览 + 硬性检查。从这里开始。 |
| `.claude/skills/pr-triage/scripts/scan_prs.py` | 逐 PR 检查(链接、参数、非文档文件)。由 `triage.sh` 调用;可加 `--json` 直接运行以获取机器可读输出。 |
| `.claude/skills/pr-triage/scripts/prep-fork-pr.sh` | 解开/准备 fork PR:取 head、merge base、报告冲突。 |

三个脚本内部都通过 `BASH_SOURCE` 解析自身目录,因此在任意工作目录下调用均可。
运行环境只需要 `PATH` 上有 `gh`(已认证)、`git`、`python3`。

## 参考文档

| 文件 | 内容 |
| --- | --- |
| `.claude/skills/pr-triage/references/listing-policy.md` | 什么样的条目算合格、审查清单、仓库既有约定,以及各类审计模式(追踪参数、代理站、死链)的实例。 |
