---
name: sitemap-audit
description: Audit a site's sitemap.xml and robots.txt for errors search engines act on. Use when a user asks to check, audit, or fix a sitemap, robots file, indexing problem, or a page that is not appearing in search. Works from the site's actual sitemap and robots files and each listed page, never from a guessed URL list.
---

# sitemap-audit

Audit sitemap.xml and robots.txt, and report only the checks you actually ran.

## When to use this skill

Use it when the user asks to:
- Audit a sitemap.xml, a sitemap index, or a robots.txt file.
- Find why a page is not indexed, or why a wrong page is indexed.
- Check a site after a redesign, a move, or a batch of new pages.
- Review sitemap files before submitting them to a search engine.

## When NOT to use it

- Do not use it as a full SEO audit. It does not check page speed, content
  quality, backlinks, or keyword rankings. Those are separate jobs.
- Do not use it on a site the user does not own or does not have
  permission to audit. Fetching someone else's pages to crawl them is
  not part of this job.
- Do not use it to fix anything by itself. This skill reports findings
  and the exact fix for each one; it changes no sitemap, robots file,
  or page until the user confirms the change.
- Do not use it to claim a status-code or redirect result you did not
  fetch. If you did not request a URL, that check is marked NOT RUN,
  never passed.

## Workflow

### 1. Collect the real files, in this order
1. Fetch `robots.txt` from the site root. Record every `Disallow` rule
   and every `Sitemap:` line it declares.
2. Fetch every sitemap file the robots file declares. If a file is a
   sitemap index, fetch every child sitemap it lists, and record which
   child each URL came from.
3. If a sitemap file cannot be fetched, stop and report that file as
   unreachable. Do not audit the URLs you could not see.

### 2. Count, then check the limits
1. Count URL entries per sitemap file and in total, counting duplicates
   separately from unique URLs.
2. Flag any single sitemap file with more than 50,000 URLs, and any
   sitemap file larger than 50 MB uncompressed. Those are the sitemap
   protocol limits; a file over either limit must be split.
3. Flag any URL that appears more than once, in the same file or
   across files, with the file names and the count.

### 3. Cross-check robots against the sitemap
For each unique sitemap URL, check it against the robots rules:
- Flag any sitemap URL whose path is disallowed by robots.txt. A
  blocked URL in a sitemap tells a search engine to index a page
  it is told not to crawl. The fix is to remove the URL from the
  sitemap, or remove the block, not both at once without a reason.
- Flag any sitemap file that robots.txt does not declare, and any
  robots-declared sitemap file that returns nothing. Either way the
  two files disagree, and that disagreement is itself a finding.

### 4. Check each listed page (only pages you actually fetched)
For each unique sitemap URL, fetch the page and record:
1. Status code. Flag 4xx and 5xx URLs, and flag any URL that redirects
   to a different URL: a sitemap should list the final destination,
   not a redirect. Record the redirect chain you actually followed.
2. Canonical tag. Flag a page whose canonical URL is different from
   its sitemap URL. The fix is to make the sitemap and the canonical
   agree on one URL, and to keep the other as a redirect if it is
   still linked anywhere.
3. Noindex. Flag a page with a `noindex` robots meta tag or header
   that is still listed in a sitemap. A noindexed page must come out
   of the sitemap; a page that belongs in search must lose the
   noindex, not both silently.
4. If a page cannot be fetched, report it as unfetched and list it
   separately. Never mark its canonical or noindex check as passed.

### 5. Report in this fixed format
1. Files checked, with URL counts per file and the total unique count.
2. Findings, one per problem, each with: the URL, the file it came
   from, what is wrong, and the exact fix. Order findings by severity:
   unreachable files first, then blocked or noindex URLs, then
   canonical mismatches, then redirects, then duplicates, then
   limit warnings.
3. Checks NOT RUN, listed by name, with why they were not run (for
   example, no live fetch was possible, or a file was unreachable).
4. A one-line verdict: how many findings, and whether the sitemap
   is safe to submit as it stands. A sitemap with any unreachable
   file, blocked URL, or noindex URL is not safe to submit unchanged.

## Good example (a finding)

> **Noindex URL in sitemap** — `https://example.com/draft`, from
> `sitemap-posts.xml`. The page carries a `noindex` robots meta tag
> but is still listed in the sitemap. Fix: remove it from the sitemap,
> or remove the noindex tag if the page should be indexed.

It names the URL, the file, the evidence, and one exact fix.

## Bad example (do not write like this)

> Your sitemap looks mostly fine and all pages return 200, with a few
> small issues to tidy up later.

It claims status results without evidence, hides which pages have
problems, and gives no fix for any of them.

## Output rules

- Output the complete audit report, ready to save or paste.
- Every finding must point to a file, a URL, or a fetched page you
  actually saw. If you cannot point to it, leave the finding out
  and say what you still need.
- Never invent a status code, a redirect, a canonical URL, or a
  count. If a number comes from a file, say which file.
- Never change a sitemap, a robots file, or a page as part of the
  audit. Report the fix, wait for confirmation, then change it
  as a separate step.
- Never claim the site is indexed, ranked, or submitted anywhere.
  This audit checks the files; indexing itself is the search
  engine's decision and is outside what was checked.

## Limits and safety rules

- This skill reads sitemap, robots, and page files only. It sends
  nothing to a search engine and submits nothing on the user's behalf.
- It does not delete URLs, pages, or files without the user's
  explicit confirmation of the exact URL and the exact change.
- It does not work from a remembered or guessed sitemap. If the
  site has no sitemap file, the report says so and stops at that
  fact; it does not invent one.
- Local fixture files (see `examples/sample-site`) cannot prove
  live status codes or redirects. An audit run on fixtures must
  mark those checks NOT RUN, exactly as the sample audit does.
