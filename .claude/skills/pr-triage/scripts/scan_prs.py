#!/usr/bin/env python3
"""Per-PR hard checks for listing PRs.

Fetches each open PR's diff, extracts the URLs it ADDS, and reports facts:
dead links, tracking/affiliate params, and non-doc files touched. It does not
make judgement calls — brand impersonation, competitor confusion, and "is this
promo entry appropriate at all" are printed as NEEDS-HUMAN for the invoker.

This lives in Python rather than bash+sed+grep because URL extraction and
regex over diffs is exactly where shell quoting fails silently.

Usage:
    scan_prs.py --repo owner/name [--limit 50] [--no-link-check]
    scan_prs.py --repo owner/name --pr 26          # scan just one PR

Reads the PR list from `gh pr list`; requires `gh` on PATH and authenticated.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# ---- what "hard problem" means ---------------------------------------------
# Tracking / affiliate / attribution parameters that should never be merged into
# a curated list: they signal paid placement and leak referrer data.
TRACKING_RE = re.compile(
    r'[?&](utm_[a-z_]+|ref|aff|affiliate|referrer|source|fbclid|gclid|mc_cid|mc_eid|'
    r'_hsenc|_hsmi|yclid|igshid|si|spm)='r'|listing-wave',
    re.IGNORECASE,
)

# URL extraction. Stops at characters that terminate a URL in markdown/HTML.
URL_RE = re.compile(r'https?://[^\s\)\]\}\(<>"\'`,;]+')

# Files a listing PR may touch. Anything else is worth a human glance.
DOC_OK_RE = re.compile(r'(^README|\.md$|\.mdx$|\.rst$|\.txt$)', re.IGNORECASE)

BROWSER_UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120 Safari/537.36'
)

OK_CODES = {200, 201, 202, 203, 204, 301, 302, 303, 307, 308}
SOFT_CODES = {401, 403, 405, 429}  # bot-blocked / rate-limited: can't conclude

# Tracking-param-free equivalents are printed so the fix is copy-pasteable.
def strip_tracking(url: str) -> str:
    """Return url with tracking query params removed (keeps real params)."""
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
    """Run a command, return stdout, empty string on any failure."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return proc.stdout if proc.returncode == 0 else ''
    except (subprocess.TimeoutExpired, OSError):
        return ''


def added_urls(diff: str) -> list[str]:
    """URLs appearing on added lines only (ignores removed lines and headers)."""
    urls: list[str] = []
    for line in diff.splitlines():
        if not line.startswith('+') or line.startswith('+++'):
            continue
        urls.extend(URL_RE.findall(line))
    # normalise trailing punctuation, dedupe preserving order
    seen, out = set(), []
    for u in urls:
        u = u.rstrip('.,;:')
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def touched_files(diff: str) -> list[str]:
    """Files the diff writes to, excluding deletions (/dev/null)."""
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
    """Return (verdict, code). verdict in ok/dead/soft/unknown."""
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
    """Collect every hard-check finding for one PR."""
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
        result['links'].append({'url': '(could not fetch diff)', 'verdict': 'unknown', 'code': '?'})
        return result

    urls = added_urls(diff)

    # tracking params
    for u in urls:
        if TRACKING_RE.search(u):
            result['tracking'].append({'url': u, 'clean': strip_tracking(u)})

    # non-doc files
    for f in touched_files(diff):
        if not DOC_OK_RE.search(f):
            result['non_doc_files'].append(f)

    # link checks (parallel — these are network-bound)
    if do_link_check and urls:
        with ThreadPoolExecutor(max_workers=8) as pool:
            verdicts = list(pool.map(check_url, urls))
        for u, (verdict, code) in zip(urls, verdicts):
            result['links'].append({'url': u, 'verdict': verdict, 'code': code})

    return result


def render_table(prs: list[dict]) -> str:
    """Fixed-width summary table for `gh pr list` JSON."""
    lines = [f"{'#':>4}  {'STATE':<12} {'AUTHOR':<22} {'FORK':<10} TITLE", '-' * 100]
    for p in prs:
        flags = []
        if p['isDraft']:
            flags.append('DRAFT')
        if p['mergeable'] == 'CONFLICTING' or p['mergeStateStatus'] == 'DIRTY':
            flags.append('CONFLICT')
        elif p['mergeable'] == 'UNKNOWN':
            flags.append('(calc)')

        cross = 'fork' if p['isCrossRepository'] else 'same'
        can_modify = 'mod' if p.get('maintainerCanModify') else 'no-mod'
        state = ','.join(flags) if flags else 'clean'
        author = p['author']['login'][:21]
        title = p['title'][:42]
        lines.append(f"{p['number']:>4}  {state:<12} {author:<22} {cross + '/' + can_modify:<10} {title}")
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', help='owner/name (required unless --table)')
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--pr', type=int, help='scan only this PR number')
    ap.add_argument('--no-link-check', action='store_true', help='skip network link checks')
    ap.add_argument('--json', action='store_true', help='emit JSON instead of text')
    ap.add_argument('--table', action='store_true',
                    help='read PR-list JSON on stdin and print only the summary table')
    args = ap.parse_args()

    if args.table:
        print(render_table(json.load(sys.stdin)))
        return 0

    if not args.repo:
        ap.error('--repo is required (or use --table)')

    fields = ('number,title,author,isDraft,mergeable,mergeStateStatus,'
              'headRefName,headRepositoryOwner,headRepository,isCrossRepository,'
              'maintainerCanModify')
    raw = run(['gh', 'pr', 'list', '--repo', args.repo, '--state', 'open',
               '--limit', str(args.limit), '--json', fields])
    if not raw:
        print(f'error: could not list PRs for {args.repo} (is gh authenticated?)', file=sys.stderr)
        return 1

    prs = json.loads(raw)
    if args.pr:
        prs = [p for p in prs if p['number'] == args.pr]
        if not prs:
            print(f'error: PR #{args.pr} is not open', file=sys.stderr)
            return 1

    if not prs:
        print(f'No open PRs in {args.repo}.')
        return 0

    results = [scan_pr(args.repo, p, not args.no_link_check) for p in prs]

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    for r in results:
        print()
        print(f"── PR #{r['number']} — {r['title']} (@{r['author']}) " + '─' * 8)
        if r['draft']:
            print('   ⚠ DRAFT — mark ready for review before merging')
        if r['conflicting']:
            print('   ⚠ CONFLICTING with base — needs a conflict resolution commit')
        if r['cross_repo']:
            pushable = 'CAN push fixes' if r['maintainer_can_modify'] else 'CANNOT push (maintainerCanModify=false)'
            print(f"   fork: {r['head_owner']}/{r['head_repo']}:{r['head_ref']} — {pushable}")
            print(f"         PR head is refs/pull/{r['number']}/head, NOT refs/heads/{r['head_ref']} on origin")

        if r['tracking']:
            print('   ⚠ TRACKING/affiliate params — strip before merge:')
            for t in r['tracking']:
                print(f"      {t['url']}")
                print(f"      → {t['clean']}")

        if r['non_doc_files']:
            print('   ⚠ non-doc files changed:')
            for f in r['non_doc_files']:
                print(f'      {f}')

        if r['links']:
            dead = [l for l in r['links'] if l['verdict'] == 'dead']
            soft = [l for l in r['links'] if l['verdict'] == 'soft']
            unk = [l for l in r['links'] if l['verdict'] == 'unknown']
            ok = [l for l in r['links'] if l['verdict'] == 'ok']
            for l in dead:
                print(f"   ✗ DEAD  ({l['code']})  {l['url']}")
            for l in unk:
                print(f"   ?  check     {l['url']}")
            for l in soft:
                print(f"   ~  blocked   ({l['code']}) {l['url']}  (verify by hand)")
            for l in ok:
                print(f"   ✓  ok        {l['url']}")

    # Roll-up so the invoker sees at a glance what needs a decision.
    n_clean = sum(
        1 for r in results
        if not r['tracking'] and not r['non_doc_files'] and not r['draft']
        and not r['conflicting']
        and not any(l['verdict'] == 'dead' for l in r['links'])
    )
    print()
    print('═' * 63)
    print(f' {n_clean}/{len(results)} PR(s) have no automatable problem.')
    print(' Always apply the NEEDS-HUMAN checks (official vs reseller, duplicate')
    print(' entries, paid placement, spec accuracy, section fit) before merging.')
    print('═' * 63)
    return 0


if __name__ == '__main__':
    sys.exit(main())
