# Sitemap audit — sample site (examples/sample-site)

Worked example for the sitemap-audit skill. Run on the local fixture
files only, so live checks are marked NOT RUN below, not claimed.

## Files checked

- `sitemap-index.xml`: 2 child sitemaps listed.
- `sitemap.xml`: 4 URL entries, 3 unique.
- `sitemap-posts.xml`: 1 URL entry, 1 unique.
- `robots.txt`: disallows `/private/`, declares `sitemap-index.xml`.
- Total: 5 URL entries, 4 unique URLs. No single file is over the
  50,000-URL limit or the 50 MB limit.

## Findings (4)

### 1. Duplicate URL in sitemap — https://example.com/about
- File: `sitemap.xml`, listed 2 times.
- Fix: keep one entry for this URL and delete the duplicate.

### 2. Robots-blocked URL in sitemap — https://example.com/private/page
- File: `sitemap.xml`.
- Evidence: `robots.txt` has `Disallow: /private/`, and this URL is
  under that path.
- Fix: remove this URL from the sitemap, or remove the `/private/`
  block if the page should be crawled. Do not do both without a reason.

### 3. Canonical mismatch — https://example.com/about
- File: `sitemap.xml`; page: `pages/about.html`.
- Evidence: the page's canonical tag points to
  `https://example.com/about-us`, not to the sitemap URL.
- Fix: make the sitemap URL and the canonical URL agree on one URL,
  and redirect the other one if it is still linked anywhere.

### 4. Noindex URL in sitemap — https://example.com/draft
- File: `sitemap-posts.xml`; page: `pages/draft.html`.
- Evidence: the page carries `<meta name="robots" content="noindex">`
  but is still listed in the sitemap.
- Fix: remove this URL from the sitemap, or remove the noindex tag
  if the page should be indexed.

## Checks NOT RUN

- Status codes: NOT RUN — the fixtures are local files, not a live site.
- Redirects: NOT RUN — the fixtures are local files, not a live site.

## Verdict

4 findings. The sitemap is not safe to submit unchanged: it contains
a robots-blocked URL and a noindex URL, plus a duplicate and a
canonical mismatch.
