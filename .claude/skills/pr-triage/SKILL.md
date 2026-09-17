---
name: pr-triage
description: "Triage, review, and merge a backlog of open pull requests on a curated repo (awesome-lists, docs, README directories) — verify submission links work, catch tracking/affiliate parameters, spot third-party reseller sites posing as official products, resolve merge conflicts on fork PRs you cannot push to, then merge and thank the contributors. Use this whenever the user says things like '处理这些 PR', 'handle the review backlog', 'triage open PRs', 'merge the pending pull requests', 'there are a bunch of PRs to review', 'help me work through the PR queue', or points at a repo's /pulls page — even if they don't say the word 'triage'. Also use when a specific listing PR is stuck on 'merge conflicts' and needs to be unstuck."
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion, TaskCreate, TaskUpdate
---

# /pr-triage

Work through an open-PR backlog on a curated listing repo: verify every submission,
fix what is mechanically fixable, escalate what needs a human call, merge, and thank
the contributors.

The guiding split throughout: **automate the facts, ask about the judgement.**
"Link returns 404" is a fact — act on it. "Is this site pretending to be the official
product?" is a judgement — surface it to the user.

> **Script paths.** The scripts live at `.claude/skills/pr-triage/scripts/`. Set
> this once per session and the commands below work verbatim from the repo root:
>
> ```bash
> TRIAGE=.claude/skills/pr-triage/scripts
> ```
>
> Each script resolves its own directory internally, so they also work when called
> by absolute path or from a different working directory — only the prefix in the
> commands below needs to change.

## Inputs

```text
/pr-triage                     # current repo, all open PRs
/pr-triage owner/name          # a specific repo
/pr-triage 26 25 24            # only these PR numbers
```

## Workflow

### Phase 1 — Recon

Get the shape of the backlog before touching anything.

```bash
$TRIAGE/triage.sh --repo <owner/name>
```

This prints a summary table (draft? conflicting? fork-able?) and runs the hard
checks over each PR: dead links, tracking parameters, non-doc files touched.
Read `references/listing-policy.md` for what the checks mean and the full
NEEDS-HUMAN checklist.

If the repo is unfamiliar, also skim its README headings and its `Contributing`
section so you know the section names entries must land in — placement is a real
review criterion, not a formality:

```bash
grep -n '^#\+ ' README.md        # section map
sed -n '/## Contributing/,/^## /p' README.md
```

### Phase 2 — Classify

Sort each PR into exactly one bucket:

| Bucket | Criteria | Action |
| --- | --- | --- |
| **Clean** | Right section, live links, no tracking params, matches table format | Merge (Phase 5) |
| **Mechanical fix** | Content is fine but a param/dead link/label needs changing | Fix (Phase 3), then merge |
| **Judgement call** | Official-vs-reseller, duplicate entry, paid placement, spec mismatch | Ask the user (Phase 4) |
| **Stuck** | `CONFLICTING` / `DIRTY` against base | Unstick (Phase 3b), then merge |

Do not merge anything in the *Judgement call* bucket on your own. Batch those
questions — one `AskUserQuestion` with all of them — rather than interrupting once
per PR.

### Phase 3a — Apply mechanical fixes to a fork PR

Most listing PRs come from forks, and you usually cannot push to the contributor's
fork branch directly. The mechanism that works:

```bash
# 1. bring the PR head to a local branch and merge the base in
$TRIAGE/prep-fork-pr.sh <PR> --repo <owner/name>

# 2. if step 1 reported conflicts, resolve them (Phase 3b), then verify your edits
# 3. push the result back to the FORK's branch
git push https://github.com/<FORK_OWNER>/<FORK_REPO>.git \
    pr-prep/<PR>:refs/heads/<THEIR_BRANCH>
```

The push only succeeds when the PR has `maintainerCanModify=true`. If it is
`false`, `prep-fork-pr.sh` prints the two fallbacks (comment asking them to rebase,
or push a maintainer branch and retarget the PR base).

> **The ref trap — this is the single most common thing that goes wrong.**
> A fork PR's head is `refs/pull/N/head`, which is **not** `refs/heads/<same-name>`
> on your repo, *even when the names are identical*. Pushing to
> `origin/<their-branch-name>` changes an unrelated branch and the PR stays stuck
> reporting conflicts forever. `prep-fork-pr.sh` fetches `refs/pull/N/head`
> precisely to avoid this.
>
> Corollary: `gh pr checkout <N>` rewrites the local remote config for that branch,
> which can make later `git fetch origin` calls fail. If fetches start failing
> after a checkout, run `git remote -v` and reset the URL.

### Phase 3b — Resolve conflicts

For a curated list, the overwhelmingly common conflict is two PRs appending to the
same table, so **the resolution is "keep both rows"** — not choosing a winner.

```bash
# after prep-fork-pr.sh reports conflicts:
grep -n '<<<<<<<\|=======\|>>>>>>>' README.md     # locate them
# edit so both entries survive, in a sensible order
git add README.md
git commit --no-edit
```

Preserve the contributor's authorship when you amend or re-commit on their behalf:

```bash
git commit --amend --no-edit --author="<original author from gh pr view --json commits>"
```

Then re-run `prep-fork-pr.sh <PR>` — it will report the branch is now clean — and
push back to the fork (Phase 3a step 3).

### Phase 4 — Escalate judgement calls

Ask the user, and always include your recommendation first with the reasoning.
House policy and the full reviewer checklist live in
`references/listing-policy.md`; the recurring ones are:

- **Third-party reseller posing as the product.** Domain-squatting patterns
  (`<product>3.org`), a proud "independent" claim, reselling a product already in
  the list. Recommend labelling as third-party rather than rejecting — it is real
  information, just mislabelled.
- **Tracking / affiliate parameters.** Strip them before merging; the entry can
  stay. A `utm_campaign=listing-wave-…` style parameter is paid directory
  placement, not an honest recommendation.
- **Dead links.** Drop the dead link (or the entry, if it is the entry's own
  link); it is often a repo that is still private or renamed.
- **Duplicates.** Something already in the same table under another name.

### Phase 5 — Merge and thank

```bash
gh pr merge <PR> --squash --delete-branch
```

Use `--squash` for one-entry listing PRs so the list history stays one commit per
addition. For draft PRs, `gh pr ready <PR>` first.

Then leave a thank-you comment on **every** merged PR — including the ones you
changed. When you altered someone's submission, say exactly what you changed and
why, so the edit reads as collaboration rather than silent rewriting:

```bash
gh pr comment <PR> --body "Thanks @<author>! 🎉 Merged. One small change during
merge: <what you changed and why>. <one line of genuine specific praise>."
```

After the batch, verify nothing is left behind:

```bash
gh pr list --state open --limit 50          # expect empty, or only escalated PRs
git log --oneline -<N>                      # confirm one commit per merge
git branch -D pr-prep/*                     # clean up working branches
```

## Reporting back

When done, give the user a table of what happened to each PR (merged as-is /
merged with change X / left for you), and call out **everything you changed
without being asked** — a maintainer needs to be able to audit your edits in one
place. Offer the obvious follow-ups you noticed but did not action.

## Bundled scripts

| Script | Purpose |
| --- | --- |
| `scripts/triage.sh` | Backlog overview + hard checks. Start here. |
| `scripts/scan_prs.py` | The per-PR checks (links, params, non-doc files). Called by `triage.sh`; run directly with `--json` for machine-readable output. |
| `scripts/prep-fork-pr.sh` | Unstick/merge-prep a fork PR: fetch head, merge base, report conflicts. |

All three resolve their own directory via `BASH_SOURCE`, so they work regardless of
the caller's working directory. They only need `gh` (authenticated), `git`, and
`python3` on `PATH`.

## References

| File | Contents |
| --- | --- |
| `references/listing-policy.md` | What makes a good entry, the reviewer checklist, house conventions, and worked examples of the audit patterns (tracking params, reseller sites, dead links). |
