# sitemap-audit-skill

Audit sitemap.xml and robots.txt for duplicate, blocked, noindex, and canonical-mismatched URLs — and report only the checks you actually ran.

[![CI](https://github.com/hai02487/sitemap-audit-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/hai02487/sitemap-audit-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it audits a site's sitemap
files and robots file, in a fixed order:

- Fetches `robots.txt`, then every sitemap file it declares, resolving
  sitemap indexes to their child sitemaps.
- Counts URL entries per file and in total, and flags any single
  sitemap file over the 50,000-URL limit or the 50 MB limit.
- Flags duplicate URLs, sitemap URLs blocked by robots.txt, pages
  whose canonical URL differs from their sitemap URL, and pages
  with a noindex tag that are still listed in a sitemap.
- Checks status codes and redirects — but only for URLs it actually
  fetched. A check that was not run is reported as NOT RUN, never
  as passed.

## What it does NOT do

- It is not a full SEO audit. It does not check page speed, content
  quality, backlinks, or keyword rankings.
- It does not fix anything by itself. It reports each finding with
  its exact fix, and changes nothing until the user confirms it.
- It does not submit a sitemap to any search engine, and it does not
  claim a site is indexed or ranked.
- It does not audit a site the user does not own or does not have
  permission to audit.

## Who it is for

Developers and site owners who want a sitemap they can submit with
confidence, and who want the audit to say plainly which checks were
run and which were not.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/sitemap-audit .agents/skills/sitemap-audit
```

## Usage

Ask the agent to audit a site, naming the site and its sitemap and
robots files. The agent follows `skills/sitemap-audit/SKILL.md` and
returns an audit report in the skill's fixed format: files checked,
findings ordered by severity, checks NOT RUN, and a one-line verdict.

## Example

The main job, walked through on the bundled fixtures in
`examples/sample-site/` (a sitemap index, two sitemap files, a
robots file, and four page fixtures). The resulting report is
`examples/sample-audit.md`:

- Files checked: index with 2 child sitemaps, 5 URL entries, 4 unique.
- 4 findings: a duplicate URL (`/about`, listed twice), a
  robots-blocked URL (`/private/page`, under `Disallow: /private/`),
  a canonical mismatch (`/about` canonical points to `/about-us`),
  and a noindex URL in the sitemap (`/draft`).
- Checks NOT RUN: status codes and redirects, because the fixtures
  are local files, not a live site.
- Verdict: not safe to submit unchanged.

The edge case the skill also covers: a sitemap index. The sample
index lists two child sitemaps, and the audit counts and checks
both of them, not just the first file it finds. A single file over
50,000 URLs must be split; the test suite verifies that counting
rule on a generated 50,001-URL file.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check the skill's frontmatter and sections, scan the
skill and README for unfinished markers and filler text, and walk
the skill through the bundled fixtures: they re-parse the sitemap
files, re-check the robots rules and page tags, and confirm the
sample audit lists the same four findings, with status codes and
redirects marked NOT RUN.

## Contributing

Small, focused improvements are welcome. Open an issue first for
anything larger than a typo, so the scope can be agreed before
work starts. Never weaken the safety rules: a check that was not
run must be reported as NOT RUN, a finding must point to a file,
URL, or page actually seen, and no sitemap, robots file, or page
is changed without the user's explicit confirmation.

## Licence

MIT — see [LICENSE](LICENSE). This is original work, written for
this repo; it builds on the public sitemap protocol limits
(50,000 URLs and 50 MB per file) and on standard robots.txt rules,
which are documented in the skill itself.
