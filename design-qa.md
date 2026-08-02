# Design QA

Date: 2026-08-02
Status: **LOCAL PASS — production deployment was not requested**

This ledger records evidence from the current worktree. It does not claim that
network-wide link checks, hosted CI, or GitHub Pages have run for an uncommitted
revision.

## Visual reference

The reference remains the CSDIY Material layout: a compact navigation tree,
plain editorial copy, and course pages that foreground learning decisions. The
final EEDIY desktop capture uses the same 1440 × 900 viewport as the reference.
EEDIY keeps its own EE-specific identity and safety/resource metadata instead
of copying CSDIY content literally.

## Verified locally

- Every canonical course has paired Chinese and English source content. Every
  populated direction has a deep guide and an audited preferred mainline.
- Route stages, prerequisites, required/elective semantics, bilingual exit
  criteria, internal links, translation pairing, and navigation reachability
  pass their semantic checks.
- Catalogue admission is evidence-driven. The release pipeline contains source
  compilation, editorial overlays, semantic validation, and page generation;
  catalogue size is not a release criterion.
- The primary sidebar is reduced to Start Learning, Routes, Course Directions,
  Practice, and Resources and Community; detail pages remain searchable and
  reachable from their direction pages.
- Feedback uses direct GitHub Issue actions rather than an embedded comment
  widget. Course pages expose three actions; route and guide pages expose two.
  Chinese and English actions carry a stable ID, canonical URL, reported URL,
  and language.
- The warning-as-error quality report passes with zero findings.
- The complete unit test run reports 468 passed, 4 skipped, and 0 failed.
- Generated-page and navigation drift checks pass, as does `git diff --check`.
- A clean `mkdocs build --strict` completes successfully.
- Browser inspection at 1440 × 900 finds no horizontal overflow on the home or
  course page, no embedded comment iframe/script, and directly visible feedback
  actions.

## Deliberately not claimed

- The offline gate skips a fresh all-network external-link sweep. Run it from a
  stable network before publishing.
- Mobile viewport, keyboard-only focus order, hosted search requests, CI, and
  the deployed Pages URL still need verification against the exact release
  commit.
- No commit, push, deployment, or production mutation was performed in this
  iteration.

## Before publishing

1. Run `python scripts/check_external_links.py` and resolve genuine failures.
2. Recheck mobile navigation, search, language switching, focus visibility,
   console errors, overflow, and broken assets in the release build.
3. Commit the complete worktree changes, run hosted CI, deploy that exact
   commit, and verify the public URL.
