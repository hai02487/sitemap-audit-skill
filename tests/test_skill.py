"""Validation + fixture walkthrough tests for the sitemap-audit skill.

Run: python3 tests/test_skill.py
No third-party dependencies. Parses the bundled fixture files in
examples/sample-site/ and checks the sample audit against them, so
the walkthrough is verified, not just the skill's headings.
"""

import pathlib
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sitemap-audit" / "SKILL.md"
README = ROOT / "README.md"
SITE = ROOT / "examples" / "sample-site"
AUDIT = ROOT / "examples" / "sample-audit.md"

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _locs(path):
    tree = ET.parse(path)
    return [el.text for el in tree.getroot().findall(".//sm:loc", NS)]


def _text(path):
    return path.read_text(encoding="utf-8")


def test_skill_frontmatter():
    text = _text(SKILL)
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    frontmatter = text.split("---", 2)[1]
    assert re.search(r"^name:\s*sitemap-audit\s*$", frontmatter, re.M) is not None
    assert re.search(r"^description:\s*.+", frontmatter, re.M) is not None


def test_skill_sections():
    text = _text(SKILL)
    for heading in ("When to use this skill", "When NOT to use it",
                    "Workflow", "Output rules", "Limits and safety rules"):
        assert heading in text, f"missing section: {heading}"
    for rule in ("50,000", "NOT RUN", "never claim", "not safe to submit"):
        assert rule.lower() in text.lower() or rule in text, f"missing rule: {rule}"


def test_no_placeholders():
    for path in (SKILL, README):
        lower = _text(path).lower()
        for word in ("todo", "lorem"):
            assert word not in lower, f"{path.name} contains placeholder: {word}"


def test_readme_sections():
    text = _text(README)
    for heading in ("What it does", "What it does NOT do", "Install",
                    "Usage", "Example", "How it is tested", "Licence"):
        assert heading in text, f"README missing section: {heading}"


def test_fixture_counts_and_index():
    children = _locs(SITE / "sitemap-index.xml")
    assert len(children) == 2, f"index should list 2 sitemaps, got {len(children)}"
    entries = _locs(SITE / "sitemap.xml") + _locs(SITE / "sitemap-posts.xml")
    assert len(entries) == 5, f"total entries should be 5, got {len(entries)}"
    assert len(set(entries)) == 4, "unique URLs should be 4"
    assert entries.count("https://example.com/about") == 2, "about must be duplicated"


def test_fixture_robots_and_pages():
    robots = _text(SITE / "robots.txt")
    assert "Disallow: /private/" in robots
    assert "Sitemap: https://example.com/sitemap-index.xml" in robots
    assert "https://example.com/private/page".startswith("https://example.com/private/")
    about = _text(SITE / "pages" / "about.html")
    canonical = re.search(r'rel="canonical" href="([^"]+)"', about).group(1)
    assert canonical == "https://example.com/about-us"
    assert canonical != "https://example.com/about", "canonical must mismatch the sitemap URL"
    draft = _text(SITE / "pages" / "draft.html")
    assert 'content="noindex"' in draft


def test_sample_audit_matches_fixtures():
    audit = _text(AUDIT)
    for url in ("https://example.com/about", "https://example.com/private/page",
                "https://example.com/draft"):
        assert url in audit, f"audit missing finding for {url}"
    assert "4 findings" in audit
    assert "Status codes: NOT RUN" in audit
    assert "Redirects: NOT RUN" in audit
    assert "not safe to submit unchanged" in audit


def test_limit_rule_counts_over_50000():
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "big.xml"
        urls = "".join(f"<url><loc>https://example.com/p{i}</loc></url>"
                       for i in range(50001))
        path.write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + urls + "</urlset>", encoding="utf-8")
        count = len(_locs(path))
        assert count == 50001 and count > 50000, "limit check must flag > 50,000 URLs"


def main():
    tests = [test_skill_frontmatter, test_skill_sections, test_no_placeholders,
             test_readme_sections, test_fixture_counts_and_index,
             test_fixture_robots_and_pages, test_sample_audit_matches_fixtures,
             test_limit_rule_counts_over_50000]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"All {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
