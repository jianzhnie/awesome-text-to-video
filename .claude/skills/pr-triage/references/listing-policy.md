# Listing review policy & reviewer checklist

What to look for when reviewing a PR against a curated list (awesome-list, README
directory, docs index), and how to handle each common case.

## What a good entry looks like

1. **Lands in the right section.** A prompt tool belongs under *Related Tools*, not
   in the *Generative Models* table. Placement is a real review criterion — a
   correctly-written entry in the wrong table is still a change request.
2. **Matches the table's column shape.** Read the header row of the target table
   and match it exactly. A row pasted into a 6-column table as 2 columns renders
   as a broken line.
3. **Matches the table's naming style.** Most tables bold the product name
   (`| **Name** |`). A bare linked name (`| [name](url) |`) stands out.
4. **Concise and specific.** One sentence on what it does; not marketing copy.
   Cut adjectives that carry no information ("powerful", "revolutionary",
   "cutting-edge").
5. **Links resolve and are canonical.** Prefer the product's own domain or its
   repository. No tracking parameters. No URL shorteners.
6. **Not a duplicate.** Check the whole README, not just the target table — the
   same product often appears in a models table *and* a references list.

## Reviewer checklist

Run this against every PR. The first four are automatable (`scripts/triage.sh`);
the rest need eyes.

| # | Check | Automated? |
| --- | --- | --- |
| 1 | Links resolve (no 404/410, no unreachable hosts) | ✅ |
| 2 | No tracking / affiliate / UTM parameters in added links | ✅ |
| 3 | Only documentation files touched (no CI, manifest, lockfile) | ✅ |
| 4 | Mergeable against base; draft state | ✅ |
| 5 | Lands in the correct section | ❌ |
| 6 | Table row matches the column count and naming style | ❌ |
| 7 | Not already present elsewhere in the README | ❌ |
| 8 | Site is the official product, not a reseller/proxy of one already listed | ❌ |
| 9 | Claimed specs match what the linked page actually says | ❌ |
| 10 | Free of undisclosed paid-placement signals | ❌ |

## The audit patterns

These are the recurring shapes worth recognising. Each is real, drawn from actual
listing PRs.

### Tracking / affiliate parameters

**Looks like:** `https://example.com/?utm_source=awesome-list&utm_medium=directory&utm_campaign=listing-wave-c`

**Why it matters:** it is a fingerprint of paid directory placement driven by an
agency, not an organic recommendation. `utm_campaign=listing-wave-*` and similar
in particular means the submitter is being paid per listing. Even when the entry
is legitimate, the parameter leaks referrer data and signals an arrangement the
list does not disclose.

**Resolution:** keep the entry, strip the parameters. `scripts/scan_prs.py` prints
the cleaned URL for you. Explain the change in the thank-you comment so it does
not read as arbitrary.

### Third-party reseller posing as the product

**Looks like:** a domain like `minimax3.org`, `veo4.pro`, `sora2-video.io`, or a
site whose own schema.org description says "Independent AI video generation
platform". Frequently it resells access to a model that is already in the list
under its official entry.

**Why it matters:** read next to the official entry, the reader assumes both are
official. The reseller gets free credibility; the reader gets a worse deal; the
list gets less trustworthy.

**Resolution:** do **not** silently reject — the site is real and the model
information may be useful. Relabel so the distinction is unmissable, e.g. product
name `**MiniMax H3 (第三方)**` with a highlight cell ending
`; third-party platform, not an official MiniMax product`. Surface the call to
the user first; they may prefer rejection.

**Detection cues:** domain squatting on the official name (`<product><digit>.<tld>`),
"independent" / "unofficial" in the site's own metadata, a marketing page with no
product documentation, only a "start creating" funnel.

### Dead code / paper links

**Looks like:** `[[Code](https://github.com/Author/Repo)]` where the repo 404s
while the paper and project page both resolve.

**Why it matters:** a 404 on a *code* link usually means the repo is private or
not yet published (common for a freshly-accepted paper), not that the submission
is fake. Verify the other links before judging the whole PR.

**Resolution:** drop the dead link, keep the verified ones, merge, and comment
inviting a follow-up PR when the repo goes public. Do not reject the whole entry
over one dead link — but do check whether the dead link *is* the entry (a tool
whose only link is dead is not a valid entry).

### Duplicate entries

**Looks like:** the same product added to a second table, or under two names
(`videos.social` / `Videos Social`).

**Resolution:** keep one, in the more specific table; note it in the comment.

### Spec inflation

**Looks like:** "4K output" on a site whose own pricing page lists 1080p.

**Resolution:** check the linked page for the claim. If it does not match, either
correct the row or flag for the user. Never merge a spec you could not verify.

## House conventions for this repo

Adjust these when applying the skill to a different list — they are recorded here
because they are conventions, not rules derivable from the README.

- **Squash-merge** one-entry listing PRs, so the list keeps one commit per addition.
- **Never merge tracking parameters**, even when otherwise accepting the entry.
- **Thank every contributor**, including (especially) when you changed their
  submission, and state exactly what you changed.
- **Table format:** `| **Name** | Maker | Best For | Max Output | Highlights | Link |`.
  Name is bold; emoji prefix on most rows but not required; link cell is
  `[domain.com](https://domain.com)`.
- **Preserve authorship** when re-committing on a fork PR:
  `git commit --amend --no-edit --author="<original>"`.

## Escalation template

When an entry trips a judgement call, batch it into one `AskUserQuestion` rather
than interrupting per-PR. Frame each option as a concrete action, put your
recommendation first, and include the evidence in the description:

> **Q:** PR #26's `minimax3.org` calls itself an "independent" platform — it is a
> third-party reseller, and the official MiniMax entry is already in the same
> table. How should I handle it?
>
> - **Merge, relabelled `**MiniMax H3 (第三方)**`** *(Recommended)* — keeps the
>   information, makes the distinction unmissable.
> - **Reject** — it resells traffic from a product already listed.
> - **Merge as-is** — no change to the contributor's content.
