#!/usr/bin/env python3
"""对列表类 PR 逐条做硬性检查。

拉取每个 open PR 的 diff,提取其中**新增**的 URL,报告事实:失效链接、
追踪/联盟参数、是否改动了非文档文件。它不做价值判断——品牌冒充、与竞品混淆、
"这条推广到底该不该收" 一律打印为「需人判断」交给调用方。

用 Python 而非 bash+sed+grep 实现,是因为从 diff 里提取 URL 和跑正则,
恰恰是 shell 引号最容易静默出错的地方。

用法:
    scan_prs.py --repo owner/name [--limit 50] [--no-link-check]
    scan_prs.py --repo owner/name --pr 26          # 只扫一个 PR

PR 列表来自 `gh pr list`;需要 `PATH` 上有 `gh` 且已认证。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# ---- 什么算"硬性问题" ------------------------------------------------------
# 绝不该被合并进 curated 清单的追踪/联盟/归因参数:它们暗示付费收录,并泄露 referrer 数据。
TRACKING_RE = re.compile(
    r'[?&](utm_[a-z_]+|ref|aff|affiliate|referrer|source|fbclid|gclid|mc_cid|mc_eid|'
    r'_hsenc|_hsmi|yclid|igshid|si|spm)='r'|listing-wave',
    re.IGNORECASE,
)

# URL 提取。遇到 markdown/HTML 中会终止 URL 的字符即停止。
URL_RE = re.compile(r'https?://[^\s\)\]\}\(<>"\'`,;]+')

# 列表类 PR 允许改动的文件;其余都值得人工看一眼。
DOC_OK_RE = re.compile(r'(^README|\.md$|\.mdx$|\.rst$|\.txt$)', re.IGNORECASE)

BROWSER_UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120 Safari/537.36'
)

OK_CODES = {200, 201, 202, 203, 204, 301, 302, 303, 307, 308}
SOFT_CODES = {401, 403, 405, 429}  # 被反爬拦截 / 限流:无法下结论


# 打印剥离追踪参数后的等价 URL,方便直接复制粘贴修复。
def strip_tracking(url: str) -> str:
    """返回去掉追踪查询参数的 url(保留真实参数)。"""
    if '?' not in url:
        return url
    base, _, query = url.partition('?')
    kept = []
    for part in query.split('&'):
        if not part:
            continue
        key = part.split('=', 1)[0].lower()
        if TRACKING_RE.match('?' + part):
            continue
        if key in {'ref', 'aff', 'affiliate', 'referrer', 'source', 'fbclid',
                   'gclid', 'mc_cid', 'mc_eid', '_hsenc', '_hsmi', 'yclid',
                   'igshid', 'si', 'spm'} or key.startswith('utm_'):
            continue
        kept.append(part)
    return base + ('?' + '&'.join(kept) if kept else '')


def run(cmd: list[str]) -> str:
    """执行命令,返回 stdout;任何失败都返回空串。"""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return proc.stdout if proc.returncode == 0 else ''
    except (subprocess.TimeoutExpired, OSError):
        return ''


def added_urls(diff: str) -> list[str]:
    """只取新增行上的 URL(忽略删除行和 diff 头)。"""
    urls: list[str] = []
    for line in diff.splitlines():
        if not line.startswith('+') or line.startswith('+++'):
            continue
        urls.extend(URL_RE.findall(line))
    # 去掉尾部标点,保序去重
    seen, out = set(), []
    for u in urls:
        u = u.rstrip('.,;:')
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def touched_files(diff: str) -> list[str]:
    """diff 写入的文件,不含删除(/dev/null)。"""
    files = []
    for line in diff.splitlines():
        if line.startswith('+++ ') or line.startswith('--- '):
            path = line[4:].strip()
            if path in ('/dev/null',):
                continue
            path = re.sub(r'^[ab]/', '', path)
            if path not in files:
                files.append(path)
    return files


def check_url(url: str) -> tuple[str, str]:
    """返回 (判定, 状态码)。判定取值 ok/dead/soft/unknown。"""
    try:
        proc = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L',
             '--max-time', '20', '-A', BROWSER_UA, url],
            capture_output=True, text=True, timeout=30,
        )
        code = proc.stdout.strip() or '000'
    except (subprocess.TimeoutExpired, OSError):
        return 'unknown', '000'

    if code in {str(c) for c in OK_CODES}:
        return 'ok', code
    if code in {str(c) for c in SOFT_CODES}:
        return 'soft', code
    if code == '000':
        return 'dead', code
    if code in ('404', '410'):
        return 'dead', code
    return 'unknown', code


def scan_pr(repo: str, pr: dict, do_link_check: bool) -> dict:
    """收集单个 PR 的全部硬性检查结果。"""
    num = pr['number']
    diff = run(['gh', 'pr', 'diff', str(num), '--repo', repo])

    result = {
        'number': num,
        'title': pr['title'],
        'author': pr['author']['login'],
        'draft': pr['isDraft'],
        'conflicting': pr['mergeable'] == 'CONFLICTING' or pr['mergeStateStatus'] == 'DIRTY',
        'cross_repo': pr['isCrossRepository'],
        'maintainer_can_modify': bool(pr.get('maintainerCanModify')),
        'head_owner': (pr.get('headRepositoryOwner') or {}).get('login', ''),
        'head_repo': (pr.get('headRepository') or {}).get('name', ''),
        'head_ref': pr['headRefName'],
        'links': [],
        'tracking': [],
        'non_doc_files': [],
    }

    if not diff:
        result['links'].append({'url': '(无法获取 diff)', 'verdict': 'unknown', 'code': '?'})
        return result

    urls = added_urls(diff)

    # 追踪参数
    for u in urls:
        if TRACKING_RE.search(u):
            result['tracking'].append({'url': u, 'clean': strip_tracking(u)})

    # 非文档文件
    for f in touched_files(diff):
        if not DOC_OK_RE.search(f):
            result['non_doc_files'].append(f)

    # 链接检查(并发——这部分是网络IO瓶颈)
    if do_link_check and urls:
        with ThreadPoolExecutor(max_workers=8) as pool:
            verdicts = list(pool.map(check_url, urls))
        for u, (verdict, code) in zip(urls, verdicts):
            result['links'].append({'url': u, 'verdict': verdict, 'code': code})

    return result


def display_width(s: str) -> int:
    """字符串在等宽终端里的显示宽度——CJK 全角字符占 2 列,其余占 1 列。

    直接用 len() 补空格会让含中文的表头和数据列错位,因为 len('状态')==2
    但它在终端里占 4 列。
    """
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)


def pad(s: str, width: int, align: str = '<') -> str:
    """按显示宽度补齐到 width 列。"""
    s = str(s)
    fill = ' ' * max(0, width - display_width(s))
    return fill + s if align == '>' else s + fill


def render_table(prs: list[dict]) -> str:
    """把 `gh pr list` 的 JSON 渲染成定宽总览表。"""
    lines = [f"{pad('#', 4, '>')}  {pad('状态', 12)} {pad('作者', 22)} {pad('FORK', 10)} 标题",
             '-' * 100]
    for p in prs:
        flags = []
        if p['isDraft']:
            flags.append('DRAFT')
        if p['mergeable'] == 'CONFLICTING' or p['mergeStateStatus'] == 'DIRTY':
            flags.append('冲突')
        elif p['mergeable'] == 'UNKNOWN':
            flags.append('(计算中)')

        cross = 'fork' if p['isCrossRepository'] else '同库'
        can_modify = '可推' if p.get('maintainerCanModify') else '不可推'
        state = ','.join(flags) if flags else '干净'
        lines.append(
            f"{pad(p['number'], 4, '>')}  {pad(state, 12)} "
            f"{pad(p['author']['login'], 22)} {pad(cross + '/' + can_modify, 10)} "
            f"{p['title'][:42]}"
        )
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', help='owner/name(除非用 --table,否则必填)')
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--pr', type=int, help='只扫这个 PR 编号')
    ap.add_argument('--no-link-check', action='store_true', help='跳过网络链接检查')
    ap.add_argument('--json', action='store_true', help='输出 JSON 而非文本')
    ap.add_argument('--table', action='store_true',
                    help='从 stdin 读 PR 列表 JSON,只打印总览表')
    args = ap.parse_args()

    if args.table:
        print(render_table(json.load(sys.stdin)))
        return 0

    if not args.repo:
        ap.error('必须提供 --repo(或使用 --table)')

    fields = ('number,title,author,isDraft,mergeable,mergeStateStatus,'
              'headRefName,headRepositoryOwner,headRepository,isCrossRepository,'
              'maintainerCanModify')
    raw = run(['gh', 'pr', 'list', '--repo', args.repo, '--state', 'open',
               '--limit', str(args.limit), '--json', fields])
    if not raw:
        print(f'错误:无法列出 {args.repo} 的 PR(gh 是否已认证?)', file=sys.stderr)
        return 1

    prs = json.loads(raw)
    if args.pr:
        prs = [p for p in prs if p['number'] == args.pr]
        if not prs:
            print(f'错误:PR #{args.pr} 不是 open 状态', file=sys.stderr)
            return 1

    if not prs:
        print(f'{args.repo} 没有 open PR。')
        return 0

    results = [scan_pr(args.repo, p, not args.no_link_check) for p in prs]

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    for r in results:
        print()
        print(f"── PR #{r['number']} — {r['title']} (@{r['author']}) " + '─' * 8)
        if r['draft']:
            print('   ⚠ DRAFT — 合并前先标记为 ready for review')
        if r['conflicting']:
            print('   ⚠ 相对 base 冲突 — 需要一个解决冲突的提交')
        if r['cross_repo']:
            pushable = '可推送修复' if r['maintainer_can_modify'] else '不可推送 (maintainerCanModify=false)'
            print(f"   fork: {r['head_owner']}/{r['head_repo']}:{r['head_ref']} — {pushable}")
            print(f"         PR head 是 refs/pull/{r['number']}/head,而非 origin 上的 refs/heads/{r['head_ref']}")

        if r['tracking']:
            print('   ⚠ 追踪/联盟参数 — 合并前剥离:')
            for t in r['tracking']:
                print(f"      {t['url']}")
                print(f"      → {t['clean']}")

        if r['non_doc_files']:
            print('   ⚠ 改动了非文档文件:')
            for f in r['non_doc_files']:
                print(f'      {f}')

        if r['links']:
            dead = [l for l in r['links'] if l['verdict'] == 'dead']
            soft = [l for l in r['links'] if l['verdict'] == 'soft']
            unk = [l for l in r['links'] if l['verdict'] == 'unknown']
            ok = [l for l in r['links'] if l['verdict'] == 'ok']
            for l in dead:
                print(f"   ✗ 失效  ({l['code']})  {l['url']}")
            for l in unk:
                print(f"   ?  待查      {l['url']}")
            for l in soft:
                print(f"   ~  被拦截   ({l['code']}) {l['url']}  (需人工复核)")
            for l in ok:
                print(f"   ✓  正常      {l['url']}")

    # 汇总,让调用方一眼看到哪些需要做决定。
    n_clean = sum(
        1 for r in results
        if not r['tracking'] and not r['non_doc_files'] and not r['draft']
        and not r['conflicting']
        and not any(l['verdict'] == 'dead' for l in r['links'])
    )
    print()
    print('═' * 63)
    print(f' {n_clean}/{len(results)} 个 PR 没有可自动发现的问题。')
    print(' 合并前仍须逐项人工核对:官方 vs 代理站、重复条目、付费收录、')
    print(' 参数真实性、章节归属。')
    print('═' * 63)
    return 0


if __name__ == '__main__':
    sys.exit(main())
