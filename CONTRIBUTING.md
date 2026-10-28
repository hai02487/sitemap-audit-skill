# Contributing

Small, focused improvements are welcome.

- Open an issue first for anything larger than a typo or a clearer example, so the scope can be agreed before work starts.
- Never weaken the safety rules: a check that was not run must be reported as NOT RUN, a finding must point to a file, URL, or page actually seen, and no sitemap, robots file, or page is changed without the user's explicit confirmation.
- Every claim in a proposed change must be verifiable: a command must be runnable, a feature must exist in code, a badge must be true.
- Run `python3 tests/test_skill.py` before opening a pull request. It must pass.
- Do not add placeholder text, invented features, or copied content without attribution.
- Python standard library only — no new dependency without a reason in the issue.
