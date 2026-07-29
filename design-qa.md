# Design QA

Date: 2026-07-29

## Evidence

All captures use the same browser, page state, color scheme, and viewport within each pair.

| Surface | Viewport | Source capture | EEDIY capture | Combined review |
| --- | --- | --- | --- | --- |
| Home, desktop, light | 1280 × 720 CSS px | `.artifacts/source/source-desktop-light-top.png` | `.artifacts/source/local-home-desktop-final.png` | `.artifacts/source/qa-desktop-home.png` |
| Home, mobile, light | 390 × 844 CSS px | `.artifacts/source/source-mobile-top.png` | `.artifacts/source/local-mobile-home-final2.png` | `.artifacts/source/qa-mobile-home.png` |
| Course, mobile, light | 390 × 844 CSS px | `.artifacts/source/source-course-mobile.png` | `.artifacts/source/local-course-mobile-final.png` | `.artifacts/source/qa-mobile-course.png` |
| Course, desktop, light — CS126 recheck | same browser state; 1265 × 712 emitted px | `.artifacts/final-qa/csdiy-cs126-1440x1000.png` | `.artifacts/source/local-course-desktop-final.png` | `.artifacts/final-qa/csdiy-cs126-vs-eediy-course-layout.png` |

The browser emitted 1265 × 712 desktop images and 375 × 811 mobile images after accounting for its scrollbar.

## Review history

### Pass 1

- P1 layout: the course tree was hidden behind two extra navigation levels.
- P1 typography and density: course metadata used a large bordered table.
- P1 responsive layout: the long site title truncated in the mobile header.
- P2 icons: palette and repository icons differed from the established icon family.
- P2 branding: the home mark used one fixed size, creating different vertical rhythm across breakpoints.

All findings were corrected before the final captures.

### Final pass

- Header height, three-column grid, sidebar widths, article width, gutters, and scroll behavior align at desktop size.
- Roboto Slab and Roboto Mono, heading weights, line height, palette, and native Material surfaces align in light and dark schemes.
- The mobile header, 16 px article gutter, navigation drawer, overlay, and touch controls remain stable at 390 × 844.
- The 35 course directions are direct navigation groups; the active direction and course expand and highlight correctly.
- Course pages use three top-level sections and an unboxed document flow.
- Theme, language, navigation, search, and back-to-top controls were exercised in the browser.
- The language menu preserves the deep course path and activates the correct language tree.
- A `6.003` search returned the expected course result.
- Focus labels, semantic controls, image alternatives, reduced motion, and wide-table keyboard access are present.
- No P0, P1, or P2 finding remains.

### Final editorial integration pass

- The CSDIY CS126 page named in the review was captured again and compared in one image with the EEDIY course shell at the same emitted size. The header, three-column document grid, navigation density, article measure, table of contents, typography, link treatment, and unboxed reading flow remain visibly aligned. EEDIY keeps only product-specific differences: its identity, EE direction names, and a denser 35-direction course tree.
- After the 62-guide regeneration, the rendered `course-132` page was inspected in the same in-app browser. Its ten level-two course-content sections comprise the generated introduction/resources shell and eight authored guide sections, totaling roughly 6,500 Markdown characters. They include placement diagnostics, a 12-week/48-item execution map, explicit assignment-access limits, ten lab-observation prompts, a computational project loop, laser/fiber safety boundaries, exit evidence, official links, and an R0 evidence disclosure. The content generation did not alter the verified visual shell.
- A final cache-busted browser pass after date normalization showed `2026-07-29`, no `2026-07-30` snapshot, one stable `course-132` discussion iframe, twelve rendered level-two headings including feedback/discussion, and no horizontal overflow at the 747 CSS-pixel viewport.
- The final navigation exposes the active direction and neighboring photonics courses. The English deep path loads with `lang=en`, the same `course-132` identity, English editorial headings, and the same feedback/discussion mapping.
- A browser query for `6.003` returned ten indexed results, including the Chinese and English Signals and Systems course pages and contextual mentions.
- Each researched course page exposes three structured Issue actions, an existing-feedback search, a course-specific Discussions fallback, and a Giscus iframe configured with the stable course ID. Repository Issues and Discussions are enabled. Actual embedded posting still depends on GitHub authentication and installation of the third-party Giscus GitHub App; that authorization is tracked as a release dependency rather than being reported as already working.
- The release-time external-link gate now requires a current reviewer, review date, method, structured allowed reason, and independently checked HTTPS evidence. Target/evidence overlaps run both policies; inconsistent HTTP outcomes and poisoned cache entries fail closed. Two independent adversarial reviewers replayed the bypass cases and returned GREEN with no remaining P0/P1.
- The generated site passed 62/62 bilingual editorial checks, 60/60 independently audited mainline coverage, 216/216 translation pairs, 274/274 reachable navigation targets, 6,040 Markdown-link checks, 253 tests, a strict MkDocs build, and a fresh external-link report covering 1,886 unique URLs. Its 1,880 content targets contain 1,842 healthy and 38 reason-bound manual reviews; 13 review-evidence URLs contain 7 healthy and 6 access-policy reviews; no target or evidence URL failed.

## Final result

Visual, content, navigation, search, bilingual, feedback, and build QA passed. Embedded comment posting remains conditional on explicit Giscus App authorization.
